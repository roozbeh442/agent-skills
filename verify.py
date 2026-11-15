#!/usr/bin/env python3
"""Run the repository's complete dependency-free verification."""

from __future__ import annotations

import ast
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_SKILLS = {"algorithm-design", "barrage-me", "demonstrator-skill"}
FORBIDDEN_PATHS = ("/home/rooz", "/Users/rooz", "\\Users\\rooz", "~/rooz")


def validate_skills() -> list[str]:
    errors: list[str] = []
    found = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if found != EXPECTED_SKILLS:
        errors.append(f"expected skills {sorted(EXPECTED_SKILLS)}, found {sorted(found)}")

    for name in sorted(EXPECTED_SKILLS):
        skill_file = ROOT / "skills" / name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"missing {skill_file.relative_to(ROOT)}")
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = re.match(r"---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not match:
            errors.append(f"invalid frontmatter in {skill_file.relative_to(ROOT)}")
            continue
        frontmatter = match.group(1)
        if f"name: {name}" not in frontmatter:
            errors.append(f"name mismatch in {skill_file.relative_to(ROOT)}")
        if "description:" not in frontmatter:
            errors.append(f"missing description in {skill_file.relative_to(ROOT)}")
    return errors


def validate_portability() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix == ".pyc":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for forbidden in FORBIDDEN_PATHS:
            if forbidden in text and path.name != "verify.py":
                errors.append(f"hard-coded path {forbidden!r} in {path.relative_to(ROOT)}")
    return errors


def validate_python() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
            ast.parse(source, filename=str(path), feature_version=(3, 8))
        except SyntaxError as error:
            errors.append(
                f"Python 3.8 compatibility error in {path.relative_to(ROOT)}: {error}"
            )
    return errors


def main() -> int:
    errors = validate_skills() + validate_portability() + validate_python()
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1

    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print("\nAll repository checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
