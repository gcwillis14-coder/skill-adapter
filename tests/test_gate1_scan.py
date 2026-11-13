#!/usr/bin/env python3
"""Unit tests for skills/skill-adapter/scripts/gate1_scan.py."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "skill-adapter" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from gate1_scan import scan_directory  # noqa: E402


class Gate1ScanTests(unittest.TestCase):
    def test_clean_skill_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "clean-skill"
            root.mkdir()
            (root / "SKILL.md").write_text("---\nname: clean-skill\n---\n# Clean\n", encoding="utf-8")
            report = scan_directory(root)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["skills_found"], ["SKILL.md"])
            self.assertEqual(report["halt_reasons"], [])
            self.assertEqual(report["flags"], [])

    def test_bidi_and_zero_width_halt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bidi-skill"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: bidi-skill\n---\n# Test\u202ehidden\n", encoding="utf-8"
            )
            report = scan_directory(root)
            self.assertEqual(report["status"], "HALT")
            self.assertTrue(any("U+202E" in r for r in report["halt_reasons"]))

    def test_out_of_root_symlink_halts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            outside = tmp_path / "secret.txt"
            outside.write_text("secret", encoding="utf-8")
            root = tmp_path / "sym-skill"
            root.mkdir()
            (root / "SKILL.md").write_text("# Sym\n", encoding="utf-8")
            os.symlink(outside, root / "leak.txt")
            report = scan_directory(root)
            self.assertEqual(report["status"], "HALT")
            self.assertTrue(any("Out-of-root symlink" in r for r in report["halt_reasons"]))

    def test_binary_null_bytes_halt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bin-skill"
            root.mkdir()
            (root / "SKILL.md").write_text("# Bin\n", encoding="utf-8")
            (root / "payload.dat").write_bytes(b"\x00\x01\x02")
            report = scan_directory(root)
            self.assertEqual(report["status"], "HALT")
            self.assertTrue(any("null bytes" in r for r in report["halt_reasons"]))

    def test_svg_is_scanned_as_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "svg-skill"
            root.mkdir()
            (root / "SKILL.md").write_text("# SVG\n", encoding="utf-8")
            (root / "diagram.svg").write_text(
                "<svg><text>safe\u202ehidden</text></svg>\n", encoding="utf-8"
            )
            report = scan_directory(root)
            self.assertEqual(report["status"], "HALT")
            self.assertTrue(any("diagram.svg" in r and "U+202E" in r for r in report["halt_reasons"]))

    def test_plugin_suite_and_base64_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "suite"
            (root / "skills" / "alpha").mkdir(parents=True)
            (root / "skills" / "beta").mkdir(parents=True)
            (root / "hooks").mkdir()
            (root / "plugin.json").write_text('{"name":"suite"}\n', encoding="utf-8")
            (root / "skills" / "alpha" / "SKILL.md").write_text("# Alpha\n", encoding="utf-8")
            (root / "skills" / "beta" / "SKILL.md").write_text(
                "# Beta\nSee ../shared.md\n" + ("A" * 68) + "\n", encoding="utf-8"
            )
            report = scan_directory(root)
            self.assertEqual(report["status"], "FLAGGED")
            self.assertEqual(
                report["skills_found"],
                ["skills/alpha/SKILL.md", "skills/beta/SKILL.md"],
            )
            self.assertTrue(any("plugin.json" in f for f in report["flags"]))
            self.assertTrue(any("hooks/" in f for f in report["flags"]))
            self.assertTrue(any(".." in f for f in report["flags"]))
            self.assertTrue(any("base64-like" in f for f in report["flags"]))


if __name__ == "__main__":
    unittest.main()
