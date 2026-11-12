#!/usr/bin/env python3
"""Deterministic Gate 1 static-text hygiene scanner for external skill directories.

Scans a source skill or plugin repository strictly as raw bytes/text (never executing
any code) and reports:
- Out-of-root or internal symlinks
- Path traversal ('..') in markdown links or script references
- Non-UTF-8 or binary files
- Invisible bidi override, zero-width, and suspicious control characters
- Long base64-like payloads
- Active hook/MCP/plugin manifests (hooks.json, mcp_config.json, .mcp.json, plugin.json, hooks/)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

BIDI_AND_ZERO_WIDTH = {
    0x200B,  # ZERO WIDTH SPACE
    0x200C,  # ZERO WIDTH NON-JOINER
    0x200D,  # ZERO WIDTH JOINER
    0x200E,  # LEFT-TO-RIGHT MARK
    0x200F,  # RIGHT-TO-LEFT MARK
    0x202A,  # LEFT-TO-RIGHT EMBEDDING
    0x202B,  # RIGHT-TO-LEFT EMBEDDING
    0x202C,  # POP DIRECTIONAL FORMATTING
    0x202D,  # LEFT-TO-RIGHT OVERRIDE
    0x202E,  # RIGHT-TO-LEFT OVERRIDE
    0x2066,  # LEFT-TO-RIGHT ISOLATE
    0x2067,  # RIGHT-TO-LEFT ISOLATE
    0x2068,  # FIRST STRONG ISOLATE
    0x2069,  # POP DIRECTIONAL ISOLATE
}

BASE64_BLOB_RE = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{64,}={0,2}(?![A-Za-z0-9+/=])")
PARENT_TRAVERSAL_RE = re.compile(r"(?:^|[\s(\"'`])\.\./")
MANIFEST_NAMES = {"hooks.json", "mcp_config.json", ".mcp.json", "plugin.json"}
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip", ".tar", ".gz",
    ".pyc", ".so", ".dylib", ".dll", ".exe", ".bin", ".wasm",
}


def _find_suspicious_chars(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for line_num, line in enumerate(text.splitlines(), start=1):
        for col, ch in enumerate(line, start=1):
            code = ord(ch)
            if code in BIDI_AND_ZERO_WIDTH or (code == 0xFEFF and (line_num > 1 or col > 1)):
                findings.append(
                    {
                        "line": line_num,
                        "col": col,
                        "codepoint": f"U+{code:04X}",
                        "name": unicodedata.name(ch, "UNKNOWN"),
                    }
                )
            elif unicodedata.category(ch) == "Cc" and ch not in ("\t", "\n", "\r"):
                findings.append(
                    {
                        "line": line_num,
                        "col": col,
                        "codepoint": f"U+{code:04X}",
                        "name": unicodedata.name(ch, "CONTROL"),
                    }
                )
    return findings


def scan_directory(target_dir: Path) -> dict[str, Any]:
    """Scan target_dir as static text and return a structured Gate 1 hygiene report."""
    resolved_root = target_dir.resolve()
    halt_reasons: list[str] = []
    flags: list[str] = []
    skills_found: list[str] = []
    files_scanned = 0

    for root, dirs, files in os.walk(target_dir, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in (".git", "__pycache__"))
        root_path = Path(root)

        for entry in list(dirs) + sorted(files):
            full = root_path / entry
            rel = full.relative_to(target_dir).as_posix()

            if full.is_symlink():
                target = full.resolve()
                try:
                    target.relative_to(resolved_root)
                    flags.append(f"Internal symlink: {rel} -> {target}")
                except ValueError:
                    halt_reasons.append(f"Out-of-root symlink: {rel} -> {target}")
                continue

            if full.is_dir():
                if entry == "hooks":
                    flags.append(f"Hooks directory present: {rel}/")
                continue

            files_scanned += 1
            if entry == "SKILL.md":
                skills_found.append(rel)
            if entry in MANIFEST_NAMES:
                flags.append(f"Plugin/hook/MCP manifest present: {rel}")

            if full.suffix.lower() in BINARY_EXTENSIONS:
                flags.append(f"Asset/binary extension skipped from text scan: {rel}")
                continue

            raw = full.read_bytes()
            if b"\x00" in raw:
                halt_reasons.append(f"Binary null bytes detected in text file: {rel}")
                continue

            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                halt_reasons.append(f"Non-UTF-8 file detected: {rel} ({exc})")
                continue

            suspicious = _find_suspicious_chars(text)
            if suspicious:
                sample = ", ".join(
                    f"L{s['line']}:{s['codepoint']}({s['name']})" for s in suspicious[:5]
                )
                halt_reasons.append(
                    f"Hidden bidi/zero-width/control characters in {rel}: {sample}"
                )

            for line_num, line in enumerate(text.splitlines(), start=1):
                if PARENT_TRAVERSAL_RE.search(line):
                    flags.append(f"Parent-directory traversal '..' in {rel}:{line_num}")
                if BASE64_BLOB_RE.search(line) and not line.strip().startswith("data:image/"):
                    flags.append(f"Long base64-like token in {rel}:{line_num}")

    status = "HALT" if halt_reasons else ("FLAGGED" if flags else "PASS")
    return {
        "target": str(target_dir),
        "status": status,
        "files_scanned": files_scanned,
        "skills_found": sorted(skills_found),
        "halt_reasons": halt_reasons,
        "flags": flags,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic Gate 1 static-text hygiene scanner for skill directories."
    )
    parser.add_argument("path", help="Path to the extracted or cloned source skill/repo directory.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON output.")
    args = parser.parse_args(argv)

    target = Path(args.path)
    if not target.exists() or not target.is_dir():
        print(f"Error: directory not found: {target}", file=sys.stderr)
        return 2

    report = scan_directory(target)
    if args.json_output:
        print(json.dumps(report, indent=2))
    else:
        print(f"Gate 1 Hygiene Scan: {report['status']} ({report['files_scanned']} files)")
        if report["skills_found"]:
            print("Skills found: " + ", ".join(report["skills_found"]))
        for item in report["halt_reasons"]:
            print(f"  [HALT] {item}")
        for item in report["flags"]:
            print(f"  [FLAG] {item}")

    return 1 if report["status"] == "HALT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
