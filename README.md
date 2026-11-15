# Agent skills

Portable skills shared by Codex and Claude Code.

## Install

Requirements: Git and Python 3.8 or newer.

Clone this repository anywhere, then run its installer:

```bash
git clone <repository-url> ~/agent-skills
python3 ~/agent-skills/install.py
```

The installer finds the repository from its own location and links every skill into
`~/.agents/skills` for Codex and `~/.claude/skills` for Claude Code. It can be run
from any working directory and never overwrites a real file or directory.

Verify the installation:

```bash
python3 ~/agent-skills/install.py --check
```

Restart Codex or Claude Code if a newly installed skill does not appear.

## Update

```bash
git -C ~/agent-skills pull --ff-only
python3 ~/agent-skills/install.py --check
```

## Symlink fallback

If the system cannot create symlinks, install managed copies instead:

```bash
python3 ~/agent-skills/install.py --copy
```

Copies do not update through their source automatically. Rerun `install.py --copy`
after every `git pull`. The installer updates only copies carrying its management
marker; it refuses unmanaged directories.

If an incorrect symlink is reported, inspect it first, then replace links only:

```bash
python3 ~/agent-skills/install.py --replace-links
```

Preview any installation without changing files with `install.py --dry-run`.

## Verify this repository

```bash
python3 verify.py
```

Verification uses only the Python standard library.
