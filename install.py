#!/usr/bin/env python3
"""Install this repository's skills for Codex and Claude Code."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path


COPY_MARKER = ".agent-skills-install.json"
MANAGED_BY = "agent-skills/install.py"


@dataclass(frozen=True)
class Result:
    destination: Path
    status: str
    message: str


def repository_root() -> Path:
    """Return the repository containing this installer, independent of cwd."""
    return Path(__file__).resolve().parent


def discover_skills(root: Path) -> list[Path]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        raise ValueError(f"Skills directory not found: {skills_root}")
    skills = sorted(
        path for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if not skills:
        raise ValueError(f"No skills found under: {skills_root}")
    return skills


def destination_roots(home: Path) -> tuple[Path, Path]:
    return home / ".agents" / "skills", home / ".claude" / "skills"


def tree_digest(root: Path, *, exclude_marker: bool = False) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if exclude_marker and relative.as_posix() == COPY_MARKER:
            continue
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def marker_data(skill: Path) -> dict[str, object]:
    return {
        "schema": 1,
        "managed_by": MANAGED_BY,
        "skill": skill.name,
        "source_digest": tree_digest(skill),
    }


def read_marker(destination: Path) -> dict[str, object] | None:
    marker = destination / COPY_MARKER
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def is_managed_copy(destination: Path, skill_name: str) -> bool:
    data = read_marker(destination)
    return bool(
        data
        and data.get("schema") == 1
        and data.get("managed_by") == MANAGED_BY
        and data.get("skill") == skill_name
    )


def copy_is_current(source: Path, destination: Path) -> bool:
    if not is_managed_copy(destination, source.name):
        return False
    marker = read_marker(destination)
    assert marker is not None
    source_digest = tree_digest(source)
    return (
        marker.get("source_digest") == source_digest
        and tree_digest(destination, exclude_marker=True) == source_digest
    )


def create_managed_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging_parent = Path(tempfile.mkdtemp(prefix=f".{source.name}.installing-", dir=destination.parent))
    candidate = staging_parent / source.name
    backup: Path | None = None
    try:
        shutil.copytree(source, candidate)
        (candidate / COPY_MARKER).write_text(
            json.dumps(marker_data(source), indent=2) + "\n", encoding="utf-8"
        )
        if destination.exists():
            backup = destination.parent / f".{destination.name}.backup-{uuid.uuid4().hex}"
            destination.rename(backup)
        candidate.rename(destination)
        if backup is not None:
            shutil.rmtree(backup)
    except BaseException:
        if backup is not None and backup.exists() and not destination.exists():
            backup.rename(destination)
        raise
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)


def install_one(
    source: Path,
    destination: Path,
    *,
    mode: str,
    check: bool,
    dry_run: bool,
    replace_links: bool,
) -> Result:
    if mode == "symlink":
        if destination.is_symlink():
            if destination.resolve(strict=False) == source.resolve():
                return Result(destination, "ok", "correct symlink")
            if not replace_links:
                return Result(destination, "conflict", "points to a different location")
            if check:
                return Result(destination, "outdated", "symlink needs replacement")
            if not dry_run:
                destination.unlink()
                destination.symlink_to(source, target_is_directory=True)
            return Result(destination, "changed", "replaced symlink")
        if destination.exists():
            return Result(destination, "conflict", "real file or directory exists")
        if check:
            return Result(destination, "missing", "symlink is not installed")
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source, target_is_directory=True)
        return Result(destination, "changed", "created symlink")

    if destination.is_symlink():
        return Result(destination, "conflict", "symlink exists; copy mode will not replace it")
    if destination.exists():
        if not destination.is_dir() or not is_managed_copy(destination, source.name):
            return Result(destination, "conflict", "unmanaged file or directory exists")
        if copy_is_current(source, destination):
            return Result(destination, "ok", "managed copy is current")
        if check:
            return Result(destination, "outdated", "managed copy needs updating")
        if not dry_run:
            create_managed_copy(source, destination)
        return Result(destination, "changed", "updated managed copy")
    if check:
        return Result(destination, "missing", "managed copy is not installed")
    if not dry_run:
        create_managed_copy(source, destination)
    return Result(destination, "changed", "created managed copy")


def run_install(
    root: Path,
    home: Path,
    *,
    mode: str = "symlink",
    check: bool = False,
    dry_run: bool = False,
    replace_links: bool = False,
) -> list[Result]:
    results: list[Result] = []
    for skill in discover_skills(root):
        for destination_root in destination_roots(home):
            results.append(
                install_one(
                    skill,
                    destination_root / skill.name,
                    mode=mode,
                    check=check,
                    dry_run=dry_run,
                    replace_links=replace_links,
                )
            )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install repository skills for Codex and Claude Code."
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Create managed copies instead of symlinks; rerun after updates.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check installation state without changing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without applying them.",
    )
    parser.add_argument(
        "--replace-links",
        action="store_true",
        help="Replace incorrect symlinks; never replaces real files or directories.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "copy" if args.copy else "symlink"
    try:
        results = run_install(
            repository_root(),
            Path.home(),
            mode=mode,
            check=args.check,
            dry_run=args.dry_run,
            replace_links=args.replace_links,
        )
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    for result in results:
        print(f"{result.status:8} {result.destination} — {result.message}")
    problems = {"conflict", "missing", "outdated"}
    return 1 if any(result.status in problems for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())
