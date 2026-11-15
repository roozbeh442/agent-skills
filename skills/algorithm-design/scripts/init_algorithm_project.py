#!/usr/bin/env python3
"""Create a minimal standalone uv algorithm library atomically."""

from __future__ import annotations

import argparse
import keyword
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


PROJECT_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def write(root: Path, relative_path: str, content: str, executable: bool = False) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    if executable:
        path.chmod(0o755)


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a standalone uv project for an approved algorithm design."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Distribution name using lowercase letters, digits, and hyphens.",
    )
    parser.add_argument(
        "--destination",
        required=True,
        help="Exact new project root. Existing paths are refused.",
    )
    parser.add_argument(
        "--python",
        default="3.11",
        help="Target Python version understood by uv (default: 3.11).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not PROJECT_NAME.fullmatch(args.name):
        raise SystemExit(
            "Project name must use lowercase letters, digits, and single hyphens "
            "(example: trajectory-solver)."
        )
    package_name = args.name.replace("-", "_")
    if not package_name.isidentifier() or keyword.iskeyword(package_name):
        raise SystemExit(
            "Project name must also produce a valid Python package name; "
            "do not begin with a digit or use a Python keyword."
        )
    if shutil.which("uv") is None:
        raise SystemExit("uv is required but was not found on PATH.")

    destination = Path(args.destination).expanduser().resolve()
    if destination.exists():
        raise SystemExit(f"Refusing existing destination: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.building-", dir=destination.parent)
    )
    try:
        run(
            [
                "uv",
                "init",
                "--lib",
                "--name",
                args.name,
                "--description",
                "Standalone algorithm side project",
                "--author-from",
                "none",
                "--python",
                args.python,
                "--vcs",
                "none",
                "--no-workspace",
                str(temporary),
            ],
            destination.parent,
        )
        run(["uv", "add", "--dev", "pytest", "--no-sync"], temporary)

        write(
            temporary,
            f"src/{package_name}/__init__.py",
            f'"""Public interface for the {args.name} algorithm package."""\n',
        )
        write(
            temporary,
            f"src/{package_name}/algorithm.py",
            '"""Approved algorithm implementation."""\n',
        )

        write(
            temporary,
            "README.md",
            f"""
            # {args.name}

            Standalone algorithm side project. Its approved methods, assumptions,
            flowchart, and validation evidence are maintained in `ALGORITHM.md`.

            ## Development

            - Synchronize dependencies: `uv sync`
            - Run all verification: `./test.sh`
            - Import package: `import {package_name}`
            """,
        )
        write(
            temporary,
            "AGENTS.md",
            """
            # Agent guidance

            Keep this a standalone, importable algorithm project. Do not add application
            UI, API, database, or storage concerns. Use uv for dependency management and
            command execution. Keep the structure simple and begin with one algorithm
            module; split it only when responsibilities justify it.

            Treat the user-approved `ALGORITHM.md` as the behavioral source of truth.
            Obtain approval before changing equations, physical models, numerical methods,
            constants, units, coordinate systems, validity limits, public behavior, or
            acceptance tolerances. Map every substantive flowchart section to exactly one
            primary function, class, or class method. Do not combine mapped sections or
            hide substantive behavior in uncharted helpers. Obtain approval before changing
            this mapping and keep its flowchart-to-code-to-test traceability current.

            Use pytest for calculations, contracts, failure behavior, and validation.
            Keep `./test.sh` as the single full-project verification entry point and invoke
            each mandatory suite exactly once. Run it after changes and never claim unrun
            checks passed. Keep every Markdown file below 500 lines. Do not overwrite or
            rewrite Git history without permission.
            """,
        )
        write(
            temporary,
            "CLAUDE.md",
            """
            # Claude Code guidance

            @AGENTS.md
            """,
        )
        write(
            temporary,
            "ALGORITHM.md",
            f"""
            # {args.name} algorithm

            Replace this placeholder with the user-approved algorithm design before
            implementing calculations.

            The completed design must record the contract, methods, equations, units,
            assumptions, validity limits, Mermaid flowchart, validation plan, and public
            import interface.

            ## Traceability

            | Flow ID | Responsibility | Primary function/class/method | Unit tests | Integration or reference tests | Status |
            |---|---|---|---|---|---|
            """,
        )
        write(
            temporary,
            "test.sh",
            """
            #!/usr/bin/env bash
            set -euo pipefail
            cd "$(dirname "$0")"
            uv run pytest
            """,
            executable=True,
        )
        write(
            temporary,
            ".gitignore",
            """
            .venv/
            __pycache__/
            *.py[cod]
            .pytest_cache/
            .coverage
            htmlcov/
            """,
        )
        write(
            temporary,
            f"tests/test_{package_name}.py",
            f"""
            def test_package_imports() -> None:
                import {package_name}

                assert {package_name} is not None
            """,
        )

        temporary.rename(destination)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    print(f"Created algorithm project at {destination}")
    print("The approved ALGORITHM.md design and algorithm-specific tests are still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
