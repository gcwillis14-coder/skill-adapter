#!/usr/bin/env python3
"""Unit tests for tests/validate_skills.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_skills import validate_skill_dir


class ValidateSkillDirTests(unittest.TestCase):
    def _make_skill(self, root: Path, dir_name: str, files: dict[str, str]) -> Path:
        skill_dir = root / dir_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        for rel_path, content in files.items():
            target = skill_dir / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return skill_dir

    def test_valid_skill_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "sample-skill",
                {
                    "SKILL.md": (
                        "---\n"
                        "name: sample-skill\n"
                        "description: Validate sample skill behavior.\n"
                        "disable-model-invocation: true\n"
                        "metadata:\n"
                        "  adapted_from: upstream\n"
                        "---\n\n"
                        "# Sample\n\n"
                        "Read [guide](references/guide.md) and run `scripts/check.py`.\n"
                    ),
                    "references/guide.md": "# Guide\n\nClean text.\n",
                    "scripts/check.py": "print('ok')\n",
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertTrue(res.passed, res.errors)
            self.assertEqual(res.name, "sample-skill")

    def test_rejects_typo_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "sample-skill",
                {
                    "SKIILL.md": "---\nname: sample-skill\ndescription: x\n---\n",
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertFalse(res.passed)
            self.assertTrue(any("SKIILL.md" in err for err in res.errors))

    def test_rejects_malformed_or_incomplete_frontmatter(self) -> None:
        cases = (
            ("---\nname: [broken\ndescription: example\n---\n", "Invalid YAML"),
            ("---\nname: sample-skill\n---\n", "description"),
        )
        for content, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmp:
                skill_dir = self._make_skill(Path(tmp), "sample-skill", {"SKILL.md": content})
                result = validate_skill_dir(skill_dir)
                self.assertFalse(result.passed)
                self.assertTrue(any(expected in error for error in result.errors), result.errors)

    def test_rejects_name_mismatch_and_bad_casing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "Bad_Name",
                {
                    "SKILL.md": "---\nname: other-name\ndescription: x\n---\n",
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertFalse(res.passed)
            self.assertGreaterEqual(len(res.errors), 1)

    def test_rejects_over_long_description_and_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            long_name = "a" * 65
            skill_dir = self._make_skill(
                Path(tmp),
                long_name,
                {
                    "SKILL.md": f"---\nname: {long_name}\ndescription: {'x' * 1025}\n---\n",
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertFalse(res.passed)
            self.assertTrue(any("64" in e for e in res.errors))
            self.assertTrue(any("1024" in e for e in res.errors))

    def test_rejects_500_or_more_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            body = "\n".join(f"Line {i}" for i in range(500))
            skill_dir = self._make_skill(
                Path(tmp),
                "long-skill",
                {
                    "SKILL.md": f"---\nname: long-skill\ndescription: ok\n---\n{body}\n",
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertFalse(res.passed)
            self.assertTrue(any("< 500" in e for e in res.errors))

    def test_rejects_broken_and_nested_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "link-skill",
                {
                    "SKILL.md": (
                        "---\nname: link-skill\ndescription: ok\n---\n\n"
                        "[deep](references/nested/deep.md)\n"
                        "[missing](references/missing.md)\n"
                        "[escape](../outside.md)\n"
                    ),
                    "references/nested/deep.md": "# Deep\n",
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertFalse(res.passed)
            self.assertTrue(any("deeper than 1 level" in e for e in res.errors))
            self.assertTrue(any("Broken relative link" in e for e in res.errors))
            self.assertTrue(any("escapes" in e for e in res.errors))

    def test_rejects_google_docs_markers_and_stray_escapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self._make_skill(
                Path(tmp),
                "dirty-skill",
                {
                    "SKILL.md": (
                        "---\nname: dirty-skill\ndescription: ok\n---\n\n"
                        "\\# Heading\n"
                        "\uec03code\uec02\n"
                    ),
                },
            )
            res = validate_skill_dir(skill_dir)
            self.assertFalse(res.passed)
            self.assertTrue(any("U+EC03" in e for e in res.errors))
            self.assertTrue(any("U+EC02" in e for e in res.errors))
            self.assertTrue(any("Stray markdown" in e for e in res.errors))


if __name__ == "__main__":
    unittest.main()
