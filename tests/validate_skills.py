#!/usr/bin/env python3
"""Structural validator for agentskills.io-compatible skill directories.

Checks each skill directory for:
1. Exact `SKILL.md` filename (and flags common typos such as `SKIILL.md` or `skill.md`).
2. Valid YAML frontmatter (`name` matches parent directory, lowercase hyphenated
   <= 64 chars; `description` non-empty <= 1024 chars; valid optional types).
3. `< 500` lines in `SKILL.md`.
4. Relative markdown links in `SKILL.md` exist on disk, stay inside the skill
   directory, and are `<= 1` subdirectory level deep (e.g. `references/doc.md`).
5. Zero Google Docs `U+EC03` / `U+EC02` markers and zero stray markdown
   backslash escapes outside code blocks and inline code.
6. No symlinks escaping the skill directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
STRAY_ESCAPE_PATTERN = re.compile(r"\\([#*`<>[\]_])")
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_PATTERN = re.compile(r"`+[^`]*`+")

EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")
FORBIDDEN_MARKERS = ("\uec03", "\uec02")
TYPO_SKILL_FILENAMES = {"skill.md", "skiill.md", "skill.markdown", "skills.md"}


@dataclass
class ValidationResult:
    skill_dir: str
    passed: bool
    line_count: int = 0
    name: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _strip_inline_code(line: str) -> str:
    """Remove inline backtick spans from a single markdown line."""
    return INLINE_CODE_PATTERN.sub("", line)


def _extract_frontmatter(text: str) -> tuple[dict[str, Any] | None, int, list[str]]:
    """Parse YAML frontmatter starting on line 1. Returns (data, body_start_line, errors)."""
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0, ["SKILL.md must begin with YAML frontmatter delimiter '---' on line 1."]

    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return None, 0, ["SKILL.md frontmatter is missing closing '---' delimiter."]

    raw_yaml = "\n".join(lines[1:end_idx])
    try:
        parsed = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as exc:
        return None, end_idx + 1, [f"Invalid YAML frontmatter: {exc}"]

    if not isinstance(parsed, dict):
        return None, end_idx + 1, ["YAML frontmatter must parse to a key-value mapping."]

    return parsed, end_idx + 1, errors


def _validate_frontmatter(
    data: dict[str, Any], skill_dir: Path
) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("Frontmatter 'name' is required and must be a non-empty string.")
        name_val = None
    else:
        name_val = name
        if len(name) > 64:
            errors.append(f"Frontmatter 'name' exceeds 64 characters ({len(name)}): {name!r}")
        if not NAME_PATTERN.match(name):
            errors.append(
                f"Frontmatter 'name' must be lowercase alphanumeric with single hyphens: {name!r}"
            )
        if name != skill_dir.name:
            errors.append(
                f"Frontmatter 'name' ({name!r}) must match parent directory ({skill_dir.name!r})."
            )

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("Frontmatter 'description' is required and must be a non-empty string.")
    elif len(description) > 1024:
        errors.append(
            f"Frontmatter 'description' exceeds 1024 characters ({len(description)})."
        )

    if "disable-model-invocation" in data and not isinstance(
        data["disable-model-invocation"], bool
    ):
        errors.append("Frontmatter 'disable-model-invocation' must be a boolean if present.")

    if "metadata" in data and not isinstance(data["metadata"], dict):
        errors.append("Frontmatter 'metadata' must be a mapping if present.")

    if "compatibility" in data:
        compat = data["compatibility"]
        if not isinstance(compat, str) or len(compat) > 500:
            errors.append("Frontmatter 'compatibility' must be a string <= 500 chars if present.")

    return name_val, errors


def _iter_non_code_lines(text: str, start_line: int = 0) -> list[tuple[int, str]]:
    """Return (1-based line_num, line) pairs outside fenced code blocks."""
    result: list[tuple[int, str]] = []
    in_fence = False
    fence_char = ""
    for idx, line in enumerate(text.splitlines(), start=1):
        if idx <= start_line:
            continue
        fence_match = FENCE_PATTERN.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
            elif marker[0] == fence_char:
                in_fence = False
                fence_char = ""
            continue
        if not in_fence:
            result.append((idx, line))
    return result


def _clean_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")].strip()
    else:
        # Strip optional markdown link title: path/to/file "title"
        target = re.split(r"\s+['\"]", target, maxsplit=1)[0].strip()
    target = target.split("#", 1)[0].strip()
    return target


def _check_links_in_file(
    md_path: Path,
    skill_root: Path,
    body_start_line: int,
    enforce_one_level: bool,
) -> list[str]:
    errors: list[str] = []
    text = md_path.read_text(encoding="utf-8")
    resolved_root = skill_root.resolve()

    for line_num, line in _iter_non_code_lines(text, start_line=body_start_line):
        cleaned = _strip_inline_code(line)
        for match in MARKDOWN_LINK_PATTERN.finditer(cleaned):
            raw_target = match.group(1)
            if not raw_target or raw_target.strip().startswith("#"):
                continue
            target = _clean_link_target(raw_target)
            if not target:
                continue
            lower = target.lower()
            if lower.startswith(EXTERNAL_SCHEMES):
                continue
            if target.startswith("/"):
                errors.append(
                    f"{md_path.name}:{line_num}: Link {target!r} must be relative, not absolute."
                )
                continue

            candidate = (md_path.parent / target).resolve()
            try:
                rel_to_root = candidate.relative_to(resolved_root)
            except ValueError:
                errors.append(
                    f"{md_path.name}:{line_num}: Link {target!r} escapes the skill directory."
                )
                continue

            if enforce_one_level:
                posix_parts = PurePosixPath(rel_to_root.as_posix()).parts
                if len(posix_parts) > 2:
                    errors.append(
                        f"{md_path.name}:{line_num}: Relative link {target!r} is deeper than 1 level ({rel_to_root.as_posix()})."
                    )

            if not candidate.exists():
                errors.append(
                    f"{md_path.name}:{line_num}: Broken relative link target {target!r}."
                )
    return errors


def _check_hygiene(md_path: Path, skill_root: Path) -> list[str]:
    errors: list[str] = []
    rel = md_path.relative_to(skill_root).as_posix()
    text = md_path.read_text(encoding="utf-8")

    for line_num, line in enumerate(text.splitlines(), start=1):
        for marker in FORBIDDEN_MARKERS:
            if marker in line:
                errors.append(
                    f"{rel}:{line_num}: Contains forbidden Google Docs marker U+{ord(marker):04X}."
                )

    for line_num, line in _iter_non_code_lines(text, start_line=0):
        cleaned = _strip_inline_code(line)
        for esc in STRAY_ESCAPE_PATTERN.finditer(cleaned):
            errors.append(
                f"{rel}:{line_num}: Stray markdown backslash escape {esc.group(0)!r}."
            )
    return errors


def _check_symlinks(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    resolved_root = skill_dir.resolve()
    for root, dirs, files in os.walk(skill_dir, followlinks=False):
        root_path = Path(root)
        for entry in list(dirs) + list(files):
            full = root_path / entry
            if full.is_symlink():
                rel = full.relative_to(skill_dir).as_posix()
                target = full.resolve()
                try:
                    target.relative_to(resolved_root)
                    errors.append(f"Symlink not permitted inside skill directory: {rel}")
                except ValueError:
                    errors.append(
                        f"Symlink escapes skill directory: {rel} -> {target}"
                    )
    return errors


def validate_skill_dir(skill_dir: Path) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.exists() or not skill_dir.is_dir():
        return ValidationResult(
            skill_dir=str(skill_dir),
            passed=False,
            errors=[f"Skill path is not a directory: {skill_dir}"],
        )

    entries = os.listdir(skill_dir)
    if "SKILL.md" not in entries:
        typos = [e for e in entries if e.lower() in TYPO_SKILL_FILENAMES and e != "SKILL.md"]
        msg = "Missing exact 'SKILL.md' file."
        if typos:
            msg += f" Found similarly named file(s): {', '.join(sorted(typos))}"
        return ValidationResult(
            skill_dir=str(skill_dir),
            passed=False,
            errors=[msg],
        )

    for entry in entries:
        if entry != "SKILL.md" and entry.lower() in TYPO_SKILL_FILENAMES:
            errors.append(f"Found stray duplicate/typo skill filename: {entry}")

    errors.extend(_check_symlinks(skill_dir))

    skill_md = skill_dir / "SKILL.md"
    try:
        text = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return ValidationResult(
            skill_dir=str(skill_dir),
            passed=False,
            errors=[f"SKILL.md is not valid UTF-8: {exc}"],
        )

    lines = text.splitlines()
    line_count = len(lines)
    if line_count >= 500:
        errors.append(f"SKILL.md has {line_count} lines; must be < 500 lines.")

    frontmatter, body_start_line, fm_errors = _extract_frontmatter(text)
    errors.extend(fm_errors)

    name_val: str | None = None
    if frontmatter is not None:
        name_val, val_errors = _validate_frontmatter(frontmatter, skill_dir)
        errors.extend(val_errors)

    errors.extend(_check_links_in_file(skill_md, skill_dir, body_start_line, enforce_one_level=True))

    for md_file in sorted(skill_dir.rglob("*.md")):
        if md_file.is_symlink():
            continue
        errors.extend(_check_hygiene(md_file, skill_dir))
        if md_file != skill_md:
            errors.extend(_check_links_in_file(md_file, skill_dir, body_start_line=0, enforce_one_level=False))

    return ValidationResult(
        skill_dir=str(skill_dir),
        passed=len(errors) == 0,
        line_count=line_count,
        name=name_val,
        errors=errors,
        warnings=warnings,
    )


def discover_default_skills(repo_root: Path) -> list[Path]:
    """Discover skills/skill-adapter and all fixture skill directories."""
    targets: list[Path] = []
    main_skill = repo_root / "skills" / "skill-adapter"
    if main_skill.exists():
        targets.append(main_skill)

    fixtures_dir = repo_root / "tests" / "fixtures"
    if fixtures_dir.exists():
        for skill_md in sorted(fixtures_dir.rglob("SKILL.md")):
            targets.append(skill_md.parent)
    return targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate one or more skill directories against v1 structural rules."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Skill directory path(s) to validate. Defaults to skills/skill-adapter and tests/fixtures/**/SKILL.md dirs.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit machine-readable JSON output.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    if args.paths:
        targets = [Path(p) for p in args.paths]
    else:
        targets = discover_default_skills(repo_root)

    if not targets:
        print("No skill directories found to validate.", file=sys.stderr)
        return 2

    results = [validate_skill_dir(target) for target in targets]
    all_passed = all(r.passed for r in results)

    if args.json_output:
        print(
            json.dumps(
                {
                    "all_passed": all_passed,
                    "count": len(results),
                    "results": [asdict(r) for r in results],
                },
                indent=2,
            )
        )
    else:
        for res in results:
            status = "PASS" if res.passed else "FAIL"
            print(f"[{status}] {res.skill_dir} (lines={res.line_count}, name={res.name})")
            for err in res.errors:
                print(f"  ERROR: {err}")
            for warn in res.warnings:
                print(f"  WARN:  {warn}")
        passed_count = sum(1 for r in results if r.passed)
        print(f"\nValidated {len(results)} skill(s): {passed_count} passed, {len(results) - passed_count} failed.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
