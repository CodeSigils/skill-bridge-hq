#!/usr/bin/env python3
"""Tests for the standalone validate-skill.py script."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


def load_script(name: str):
    path = Path(__file__).with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_skill_mod = load_script("validate-skill")


class ValidateSkillTests(unittest.TestCase):
    def _make_skill(
        self,
        tmp: Path,
        dirname: str,
        content: str,
    ) -> Path:
        """Create a minimal skill directory with SKILL.md."""
        skill_dir = tmp / dirname
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        return skill_dir

    def test_valid_skill_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "my-skill",
                "---\nname: my-skill\ndescription: A useful skill\n---\n# My Skill\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertEqual(errors, [])

    def test_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "my-skill",
                "# My Skill\nNo frontmatter here.\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("missing or invalid" in e for e in errors))

    def test_name_directory_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "wrong-dir",
                "---\nname: right-name\ndescription: useful\n---\n# Test\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("does not match directory" in e for e in errors))

    def test_invalid_name_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "my_skill",
                "---\nname: my_skill\ndescription: useful\n---\n# Test\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("invalid or missing skill name" in e for e in errors))

    def test_empty_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "my-skill",
                "---\nname: my-skill\ndescription: \n---\n# Test\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("missing non-empty description" in e for e in errors))

    def test_unlabelled_fence(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "my-skill",
                "---\nname: my-skill\ndescription: useful\n---\n```\nexample\n```\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("has no language" in e for e in errors))

    def test_missing_relative_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "my-skill",
                (
                    "---\nname: my-skill\ndescription: useful\n---\n"
                    "[missing](does-not-exist.md)\n"
                ),
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("missing link target" in e for e in errors))

    def test_description_too_long(self):
        with tempfile.TemporaryDirectory() as tmp:
            long_desc = "x" * 1025
            skill_dir = self._make_skill(
                Path(tmp),
                "my-skill",
                f"---\nname: my-skill\ndescription: {long_desc}\n---\n# Test\n",
            )
            errors = validate_skill_mod.validate_skill(
                skill_dir / "SKILL.md", root=Path(tmp)
            )
            self.assertTrue(any("exceeds 1024 characters" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
