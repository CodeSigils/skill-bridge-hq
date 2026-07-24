#!/usr/bin/env python3
"""Deterministic unit tests for repository validators."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def load_script(name: str):
    path = Path(__file__).with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_docs = load_script("validate-docs")
verify_urls = load_script("verify-marketplace-urls")
ci_check = load_script("ci-check")


class DocumentationTests(unittest.TestCase):
    def test_parse_folded_description(self):
        content = "---\nname: example\ndescription: >\n  folded value\n---\n# Example\n"
        frontmatter = validate_docs.parse_frontmatter(content)
        self.assertEqual(frontmatter["description"], "folded value")

    def test_skill_name_must_match_directory(self):
        original_root = validate_docs.ROOT
        with tempfile.TemporaryDirectory() as directory:
            validate_docs.ROOT = Path(directory)
            try:
                path = Path(directory) / "wrong" / "SKILL.md"
                path.parent.mkdir()
                path.write_text("---\nname: right\ndescription: useful\n---\n# Test\n", encoding="utf-8")
                errors = validate_docs.validate_skill(path)
            finally:
                validate_docs.ROOT = original_root
        self.assertTrue(any("does not match directory" in error for error in errors))

    def test_missing_relative_link_is_rejected(self):
        path = validate_docs.ROOT / "README.md"
        errors = validate_docs.check_relative_links(path, "[missing](does-not-exist.md)")
        self.assertTrue(any("missing link target" in error for error in errors))

    def test_unlabelled_fence_is_rejected(self):
        errors = validate_docs.check_fences("```\nexample\n```", "example.md")
        self.assertTrue(any("has no language" in error for error in errors))


class PortabilityTests(unittest.TestCase):
    """Tests for the ci-check.py portability gate."""

    def test_clean_file_passes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# My Skill\n\nThis is a portable skill with no platform refs.\n")
            f.flush()
            violations = ci_check.scan_file(Path(f.name))
        self.assertEqual(violations, [])

    def test_hermes_tool_name_caught(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Use skill_view to inspect the result.\n")
            f.flush()
            violations = ci_check.scan_file(Path(f.name))
        self.assertTrue(any("Hermes tool name" in v[2] for v in violations))

    def test_hermes_config_path_caught(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Config lives at ~/.hermes/config.yaml\n")
            f.flush()
            violations = ci_check.scan_file(Path(f.name))
        self.assertTrue(any("Hermes config path" in v[2] for v in violations))

    def test_hermes_cli_command_caught(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Run `hermes skills install foo` to add it.\n")
            f.flush()
            violations = ci_check.scan_file(Path(f.name))
        self.assertTrue(any("Hermes CLI command" in v[2] for v in violations))

    def test_case_insensitive_match(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("The Skill_View tool is handy.\n")
            f.flush()
            violations = ci_check.scan_file(Path(f.name))
        self.assertTrue(any("Hermes tool name" in v[2] for v in violations))

    def test_empty_directory_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = ci_check.iter_skill_markdown_files(root)
            self.assertEqual(files, [])


class ContractDriftTests(unittest.TestCase):
    """Tests for verify-marketplace-urls.py contract drift detection."""

    def test_status_mismatch_detected(self):
        entry = {"expected_statuses": [200], "max_redirects": 5}
        result = verify_urls.CheckResult(404, 0, "-", "https://example.com")
        reasons = verify_urls.contract_drift_reasons(entry, result)
        self.assertIn("status=404", reasons)

    def test_json_schema_failure_detected(self):
        entry = {
            "expected_statuses": [200],
            "content_type": "json",
            "json_schema": {"type": "object", "required_keys": ["count"]},
        }
        result = verify_urls.CheckResult(200, 0, "SCHEMA:missing-count", "https://example.com")
        reasons = verify_urls.contract_drift_reasons(entry, result)
        self.assertIn("SCHEMA:missing-count", reasons)

    def test_all_matching_entry_is_valid(self):
        entry = {
            "expected_statuses": [200, 301],
            "max_redirects": 2,
            "canonical_url": "https://example.com/current",
        }
        result = verify_urls.CheckResult(200, 1, "-", "https://example.com/current")
        self.assertTrue(verify_urls.result_is_valid(entry, result))
        self.assertEqual(verify_urls.contract_drift_reasons(entry, result), [])

    def test_multiple_drift_reasons(self):
        entry = {
            "expected_statuses": [200],
            "max_redirects": 0,
            "canonical_url": "https://example.com/original",
        }
        result = verify_urls.CheckResult(500, 3, "-", "https://example.com/other")
        reasons = verify_urls.contract_drift_reasons(entry, result)
        self.assertEqual(len(reasons), 3)
        self.assertTrue(any("status=500" in r for r in reasons))
        self.assertTrue(any("redirects=3" in r for r in reasons))
        self.assertTrue(any("final_url=" in r for r in reasons))


class ContractTests(unittest.TestCase):
    def test_array_schema(self):
        self.assertEqual(
            verify_urls.validate_json_shape([], {"type": "array"}),
            "VALID_SCHEMA",
        )

    def test_object_required_keys(self):
        result = verify_urls.validate_json_shape(
            {"count": 1},
            {"type": "object", "required_keys": ["count", "skills"]},
        )
        self.assertEqual(result, "SCHEMA:missing-skills")

    def test_manifest_rejects_schema_without_json(self):
        entry = {
            "name": "test",
            "url": "https://example.com",
            "expected_statuses": [200],
            "source_section": "test",
            "json_schema": {"type": "object"},
        }
        with self.assertRaisesRegex(ValueError, "content_type=json"):
            verify_urls.validate_entry(entry)

    def test_expected_401_is_valid_without_json(self):
        entry = {
            "expected_statuses": [401],
            "max_redirects": 0,
        }
        result = verify_urls.CheckResult(401, 0, "HTTP_401", "https://example.com")
        self.assertTrue(verify_urls.result_is_valid(entry, result))

    def test_redirect_limit_detects_canonical_drift(self):
        entry = {
            "expected_statuses": [200],
            "max_redirects": 0,
        }
        result = verify_urls.CheckResult(200, 1, "-", "https://example.com/new")
        self.assertEqual(
            verify_urls.contract_drift_reasons(entry, result),
            ["redirects=1"],
        )

    def test_canonical_url_detects_target_drift(self):
        entry = {
            "expected_statuses": [200],
            "canonical_url": "https://example.com/current",
        }
        result = verify_urls.CheckResult(200, 0, "-", "https://example.com/moved")
        self.assertEqual(
            verify_urls.contract_drift_reasons(entry, result),
            ["final_url=https://example.com/moved"],
        )

    def test_manifest_rejects_negative_redirect_limit(self):
        entry = {
            "name": "test",
            "url": "https://example.com",
            "expected_statuses": [200],
            "source_section": "test",
            "max_redirects": -1,
        }
        with self.assertRaisesRegex(ValueError, "non-negative"):
            verify_urls.validate_entry(entry)


if __name__ == "__main__":
    unittest.main()
