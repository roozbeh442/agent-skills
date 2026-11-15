---
name: demonstrator-skill
description: Bootstrap a minimal, independently maintained React and FastAPI demonstrator app with functional sidebar navigation, optional PostgreSQL, and automated verification.
---

# Demonstrator Skill v1

Use this skill ONLY to generate a new skeleton, not project-specific features. Target Linux (local, remote SSH, EC2) with VS Code and either Codex or Claude Code.

## Required interview
Ask for: (1) app name and destination, (2) sidebar menu names only, (3) theme selection from Navy/Gray, Teal/Slate, Graphite/Indigo, or Custom hex colors, (4) optional logo file path, (5) persistence choice: none (default), PostgreSQL now, or later. Do not ask for menu descriptions. Confirm destination before writing. Do not overwrite an existing directory or repository without explicit approval.

## Execution
1. Check `python3`, `node`, `npm`, `uv`, and `git` availability. For verification check `npx`/Playwright and browser dependencies. Report missing prerequisites accurately.
2. Resolve `<skill-dir>` as the directory containing this `SKILL.md`, then run `python3 <skill-dir>/scripts/scaffold.py --name '...' --destination '...' --menus 'Home,Results' --theme navy --database none` (or corresponding choices). For custom colors pass `--primary '#...' --accent '#...'`. Optionally `--logo /path/to/logo.png`.
3. Inspect generated files, then install dependencies (`cd frontend && npm install`; `cd backend && uv sync`). For database mode, provision PostgreSQL separately using `docker compose up -d db`, set `DATABASE_URL`, then run `uv run alembic upgrade head`.
4. Run `./test.sh` in the generated repository. This builds the frontend, checks Python compilation, exercises the FastAPI health endpoint, starts both services and runs Playwright browser checks for EVERY menu (including navigation, refresh and sidebar). If any test fails, diagnose and repair generated files, then rerun ALL checks. Limit to three repair cycles; never claim success if checks remain failing.
5. Only after mandatory checks pass, initialize local Git and make an initial commit. Never create a remote or alter existing Git history. If tests cannot run due to environment restrictions, report the unverified status and do not commit as verified.
6. Report created path, chosen options, exact test outcomes, prerequisites, and start commands. Never state that a live browser test passed unless it actually ran.

## Architectural constraints
- React + Vite + TypeScript, simple CSS and REST fetch, FastAPI with single `backend/main.py` for application routes. No Settings/About unless requested as menus.
- Separate demonstrator repository per app; minimal directories, no premature services, abstraction layers, authentication, dashboard, or feature code.
- One Home page and one working placeholder page per menu. If Home isn't named, add it as the first menu. Sidebar is collapsible, responsive; header shows app name and optional logo.
- Central theme and menu config; use one of three repeatable color sets or custom.
- Database optional: no database dependencies or folders in none mode. PostgreSQL mode uses SQLAlchemy, Alembic migrations and a Docker Compose database service. DB can be added later. Keep business logic separate from persistence as the app grows.
- Root README.md, ARCHITECTURE.md, AGENTS.md, GETTING_STARTED.md, .env.example, .gitignore, dev.sh, test.sh. Beginner guide explains every folder, adding a page, adding a FastAPI endpoint and calling it from React, remote SSH forwarding and troubleshooting.
- Prefer `uv` for Python dependency management. No AWS deployment automation. Run on Linux or remote EC2, access through VS Code Remote SSH and forwarded ports.
