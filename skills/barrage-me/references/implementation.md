# Feature implementation

Use this reference only after the user confirms the build brief.

## Recheck before editing

- Re-read the applicable `AGENTS.md` or `CLAUDE.md` guidance and the confirmed brief.
- Inspect `git status` and preserve unrelated or pre-existing changes.
- Recheck the files and interfaces affected by the brief; the repository may have changed during the interview.
- Identify the smallest vertical slices that produce observable behavior.

The confirmed brief controls product behavior. Repository guidance controls how changes are made. If they conflict and the conflict was not already resolved, stop and ask before editing the affected area.

## Preserve the demonstrator architecture

Prefer the existing structure until a confirmed requirement creates a concrete reason to change it:

- Keep navigation, app identity, and theme colors in `frontend/src/config.ts`.
- Keep REST endpoints under `/api`.
- Keep backend application routes in `backend/main.py` until its responsibilities genuinely require a split.
- Reuse the current frontend patterns and CSS before adding frameworks or layers.
- Use the existing PostgreSQL and migration setup when persistence is already enabled.
- Do not add authentication, services, repositories, state libraries, dashboards, or generic abstractions unless the brief requires them.

Prefer a small complete path through UI, API, persistence, and tests over building one entire technical layer at a time.

## Implement against observable behavior

For each slice:

1. Identify the user-visible acceptance criterion and the public seam that proves it.
2. Add or update a test that fails for the missing behavior when practical.
3. Implement only the behavior required for that slice.
4. Run the narrowest relevant check.
5. Continue to the next slice.

Test through public boundaries: browser behavior, REST contracts, and stable domain interfaces. Avoid tests coupled to private functions or markup details unless those details are the promised behavior.

Handle the states resolved in the interview, including relevant loading, empty, validation, error, permission, and destructive-action states. Do not add speculative behavior that was excluded or never confirmed.

## Testing ownership

Inspect the existing tests and runner before adding coverage. Extend or adapt tests that already exercise the same behavior instead of creating equivalent assertions under a new name.

- Use pytest for Python calculations, backend rules, FastAPI contracts, and persistence behavior.
- Use Playwright for user-visible browser workflows.
- Permit small cross-layer overlap for critical workflows, but make each layer prove a different seam; do not mirror every backend assertion in Playwright.
- Keep `./test.sh` as the single full-project verification entry point. It must invoke every mandatory suite exactly once.
- When a feature introduces a new suite or mandatory check, update `test.sh` in the same change so the new coverage cannot be skipped.
- Do not add an empty test framework or change `test.sh` before there is a real test for it to run.

Targeted tests may run repeatedly during development and then run once more through the final `./test.sh`; that feedback loop is intentional and is not duplicate suite registration.

## Data and external effects

- Make schema changes through the repository's existing migration mechanism.
- Preserve existing data unless the confirmed brief explicitly authorizes a migration or deletion strategy.
- Never place secrets in source files or logs.
- Do not provision services, deploy, publish, modify external accounts, or send messages without separate authorization.
- Do not rewrite Git history. Do not commit unless requested.

## Keep repository guidance current

Update documentation as part of the same implementation, after the code's final shape is known.

Update the repository's agent-guidance source when the completed feature changes stable instructions that future agents must follow, such as canonical file locations, required commands, architectural constraints, or safety rules. Keep `AGENTS.md` and any `CLAUDE.md` bridge consistent. Make focused edits that preserve unrelated guidance. Do not place feature specifications, temporary status, implementation history, or one-off decisions in agent guidance, and do not weaken a rule merely to make the current implementation convenient. If the confirmed design conflicts with a current rule, resolve that conflict with the user before changing either the rule or the code.

Update `ARCHITECTURE.md` whenever the implemented system changes components, responsibilities, routes, data flow, persistence, external integrations, or important boundaries. Describe the system that now exists, not the proposed plan or a change log. Preserve still-correct information and remove statements made false by the implementation.

Update user/setup documentation when commands, environment variables, or operating steps change. Keep every Markdown file created or edited by this skill below 500 lines. Prefer concise guidance; if a file approaches the limit and genuinely needs more detail, move focused detail into a purpose-specific document and link to it rather than allowing an oversized catch-all file.

If neither agent guidance nor `ARCHITECTURE.md` needs a content change, leave it untouched and state why in the final report.

## Verification

Run focused checks during development and `./test.sh` after all changes, as required by the demonstrator contract. If a check fails, diagnose the failure, repair in-scope code, and rerun the affected check followed by the full suite. If an environmental or product blocker remains, report it precisely and do not claim success.

Before finishing, compare the implementation to every acceptance criterion and explicit non-goal in the confirmed brief. Report any deviation instead of silently shrinking scope.
