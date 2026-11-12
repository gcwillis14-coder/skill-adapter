#!/usr/bin/env python3
"""Bounded static-text hygiene checks, NOT a semantic prompt-injection detector.

Use on a private, stable snapshot. No imported code is executed. PASS is only a
hygiene result; semantic review and installation approval are still required.
Only the root .git directory is excluded, explicitly, as transport metadata.
Git tree modes must be checked separately before checkout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import unicodedata
from pathlib import Path
from typing import Any

BASE64_BLOB_RE = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{64,}={0,2}(?![A-Za-z0-9+/=])")
PARENT_TRAVERSAL_RE = re.compile(r"(?:^|[\s(\"'`])\.\./")
MANIFEST_NAMES = {"hooks.json", "mcp_config.json", ".mcp.json", "plugin.json"}
SCRIPT_EXTENSIONS = {".py", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl"}
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 16 * 1024 * 1024
MAX_ENTRIES = 4096
MAX_DEPTH = 32


def _find_suspicious_chars(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    line, col = 1, 0
    for index, ch in enumerate(text):
        col += 1
        category = unicodedata.category(ch)
        if ((category == "Cf" and not (ch == "\ufeff" and index == 0))
                or (category == "Cc" and ch not in "\t\n\r")):
            findings.append({"line": line, "col": col, "codepoint": f"U+{ord(ch):04X}",
                             "name": unicodedata.name(ch, "CONTROL")})
            if len(findings) >= 20:
                break
        if ch == "\n":
            line, col = line + 1, 0
    return findings


def scan_directory(target_dir: Path) -> dict[str, Any]:
    """Fail closed on incomplete inspection and hash inspected regular files.

    This is not an OS sandbox or protection against concurrent hostile mutation.
    Binary/oversized inputs require a separate review, not a silent skip.
    """
    target_dir = Path(os.path.abspath(target_dir))
    halts: list[str] = []
    flags: list[str] = []
    skills: list[str] = []
    excluded: list[str] = []
    manifest: list[dict[str, Any]] = []
    files_seen = files_scanned = entries_seen = total_bytes = 0
    pending: list[tuple[Path, int]] = []
    try:
        if not stat.S_ISDIR(target_dir.lstat().st_mode):
            halts.append("Scan root must be a real directory, not a symlink or special file")
        else:
            resolved_root = target_dir.resolve(strict=True)
            pending.append((target_dir, 0))
    except (OSError, RuntimeError) as exc:
        halts.append(f"Cannot inspect scan root: {exc!r}")

    while pending:
        directory, depth = pending.pop()
        try:
            if directory.is_symlink() or not directory.resolve(strict=True).is_relative_to(resolved_root):
                halts.append(f"Changed or escaping directory: {str(directory)!r}")
                continue
            children = []
            with os.scandir(directory) as iterator:
                for entry in iterator:
                    entries_seen += 1
                    if entries_seen > MAX_ENTRIES:
                        halts.append(f"Entry limit exceeded ({MAX_ENTRIES}); scan incomplete")
                        pending.clear()
                        break
                    children.append(entry.name)
            if entries_seen > MAX_ENTRIES:
                break
        except (OSError, RuntimeError) as exc:
            halts.append(f"Cannot enumerate {str(directory)!r}: {exc!r}")
            continue
        for name in sorted(children):
            full = directory / name
            rel = full.relative_to(target_dir).as_posix()
            if any(unicodedata.category(ch).startswith("C") for ch in rel):
                halts.append(f"Hidden/control characters in filename: {rel!r}")
            try:
                info = full.lstat()
                if stat.S_ISLNK(info.st_mode):
                    try:
                        outside = not full.resolve(strict=True).is_relative_to(resolved_root)
                        label = "Out-of-root symlink" if outside else "Internal symlink"
                    except (OSError, RuntimeError):
                        label = "Broken or looping symlink"
                    halts.append(f"{label}: {rel!r}; symlinks are not inspected or installed")
                    continue
                if stat.S_ISDIR(info.st_mode):
                    if name == ".git" and full.parent == target_dir:
                        excluded.append(rel + "/")
                    elif depth >= MAX_DEPTH:
                        halts.append(f"Depth limit exceeded at {rel!r}; scan incomplete")
                    else:
                        if name == "hooks":
                            flags.append(f"Hooks directory present: {(rel + '/')!r}")
                        pending.append((full, depth + 1))
                    continue
                files_seen += 1
                if not stat.S_ISREG(info.st_mode):
                    halts.append(f"Special file (FIFO/socket/device) not read: {rel!r}")
                    continue
                if info.st_nlink > 1:
                    halts.append(f"Hard-linked file not accepted in snapshot: {rel!r}")
                    continue
                if info.st_size > MAX_FILE_BYTES or total_bytes + info.st_size > MAX_TOTAL_BYTES:
                    halts.append(f"Byte limit exceeded at {rel!r}; file not fully scanned")
                    continue
                fd = os.open(full, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
                with os.fdopen(fd, "rb") as stream:
                    opened = os.fstat(stream.fileno())
                    if (not stat.S_ISREG(opened.st_mode) or
                            (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino)):
                        halts.append(f"File changed before read: {rel!r}")
                        continue
                    remaining = min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total_bytes)
                    raw = stream.read(remaining + 1)
                    after = os.fstat(stream.fileno())
                if len(raw) > remaining:
                    halts.append(f"Byte limit exceeded during read: {rel!r}")
                    continue
                if (after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_mode, after.st_nlink) != (
                        info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_mode, info.st_nlink):
                    halts.append(f"File changed during read: {rel!r}")
                    continue
                total_bytes += len(raw)
                executable = bool(info.st_mode & 0o111)
                manifest.append({"path": rel, "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                                 "mode": stat.S_IMODE(info.st_mode), "executable": executable})
                if name == "SKILL.md":
                    skills.append(rel)
                if name in MANIFEST_NAMES:
                    flags.append(f"Plugin/hook/MCP manifest present: {rel!r}")
                if executable or full.suffix.lower() in SCRIPT_EXTENSIONS or "scripts" in full.relative_to(target_dir).parts[:-1]:
                    flags.append(f"Script/executable requires review before installation: {rel!r}")
                if b"\x00" in raw:
                    halts.append(f"Binary null bytes detected in file: {rel!r}")
                    continue
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError as exc:
                    halts.append(f"Non-UTF-8 file detected: {rel!r} ({exc!r})")
                    continue
                files_scanned += 1
                suspicious = _find_suspicious_chars(text)
                if suspicious:
                    sample = ", ".join(f"L{s['line']}:{s['col']}:{s['codepoint']}" for s in suspicious[:5])
                    halts.append(f"Hidden bidi/zero-width/control characters in {rel!r}: {sample}")
                for line_num, line in enumerate(text.split("\n"), start=1):
                    if PARENT_TRAVERSAL_RE.search(line):
                        flags.append(f"Parent-directory traversal '..' in {rel!r}:{line_num}")
                    if BASE64_BLOB_RE.search(line):
                        flags.append(f"Long base64-like token in {rel!r}:{line_num}")
            except (OSError, RuntimeError) as exc:
                halts.append(f"Cannot inspect {rel!r}: {exc!r}")
    if not files_seen and not halts:
        halts.append("No source files found; empty inspection is not a PASS")
    manifest.sort(key=lambda item: item["path"])
    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True, ensure_ascii=True,
                                       separators=(",", ":")).encode("ascii")).hexdigest()
    return {"target": str(target_dir), "status": "HALT" if halts else ("FLAGGED" if flags else "PASS"),
            "files_seen": files_seen, "files_scanned": files_scanned, "bytes_read": total_bytes,
            "skills_found": sorted(skills), "halt_reasons": halts, "flags": flags,
            "excluded_metadata": sorted(excluded), "file_manifest": manifest, "snapshot_sha256": digest,
            "semantic_review_required": True}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static hygiene only; semantic review is always required.")
    parser.add_argument("path", help="Private, stable source snapshot directory")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON output")
    args = parser.parse_args(argv)
    target = Path(args.path)
    if not target.exists() or not target.is_dir():
        print(f"Error: directory not found: {str(target)!r}", file=sys.stderr)
        return 2
    report = scan_directory(target)
    if args.json_output:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(f"Gate 1 Hygiene Scan: {report['status']} ({report['files_scanned']} text files)")
        print("Semantic review is still required; this is NOT a safety certification.")
        print("Snapshot SHA-256: " + report["snapshot_sha256"])
        for key, label in (("halt_reasons", "HALT"), ("flags", "FLAG")):
            for item in report[key]:
                print(f"  [{label}] {ascii(item)[1:-1]}")
        for item in report["excluded_metadata"]:
            print(f"  [EXCLUDED GIT METADATA] {item!r}")
    return 1 if report["status"] == "HALT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
