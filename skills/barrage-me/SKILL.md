---
name: barrage-me
description: Turn an app or feature description into resolved requirements, then implement and verify it in an existing React/FastAPI repository created by demonstrator-skill. Use for a thorough requirements interview followed by feature development; do not use to create a new skeleton or for interview-only planning.
---

# Barrage Me

Convert a rough description into a shared, testable implementation without silently choosing product behavior for the user.

## Boundary

This skill extends an existing `demonstrator-skill` application. It does not rerun the scaffold or overwrite a repository. If the current repository is not a demonstrator-style React/Vite frontend with a FastAPI backend, explain the mismatch and ask the user whether to continue with the repository as-is or create a skeleton separately.

The interview and implementation are one workflow, separated by an explicit confirmation gate. Do not edit application files during the interview.

## 1. Establish the starting point

Treat the user's description as the root of the requirements tree. Do not ask them to repeat it.

Before asking product questions:

- Read the applicable `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`, and repository status when present.
- Inspect the current navigation/config, frontend entry points, `backend/main.py`, persistence setup, and existing tests.
- Resolve discoverable facts with repository inspection. Ask the user for decisions, not facts available in files or tools.
- Preserve uncommitted work and call out any conflict between the request and repository guidance.

Then read [references/interview.md](references/interview.md) completely and conduct the interview.

## 2. Confirm the build brief

When the decision frontier is empty, present one concise build brief containing:

- desired outcome and users;
- in-scope workflows and explicit non-goals;
- UI states and navigation changes;
- domain rules and data lifecycle;
- API and persistence behavior;
- failure, authorization, and integration behavior where relevant;
- acceptance criteria and verification approach;
- expected agent-guidance and `ARCHITECTURE.md` changes, or why neither needs to change;
- important assumptions accepted by the user.

State any consequence that is expensive or difficult to reverse. Ask the user to confirm that this is the application or feature they want built. When native option controls are available, offer `Build this brief (Recommended)` and `Revise the brief` as buttons, with the interface's free-form Other option. If they revise anything, reopen the affected branches of the requirements tree and continue interviewing. Do not implement until they explicitly confirm the brief.

## 3. Implement after confirmation

After confirmation, read [references/implementation.md](references/implementation.md) completely. Implement the confirmed brief in the current repository, following its instructions and the repository's `AGENTS.md`.

If new information exposes a product decision that was not resolved, pause only that dependent work, ask the smallest necessary follow-up question, and continue independent work when safe. Do not reinterpret the confirmation as permission for deployment, external account changes, destructive data operations, Git history rewrites, or publishing.

## 4. Finish with evidence

Report:

- what was built and any confirmed non-goals;
- material files and architecture changes;
- how agent guidance and `ARCHITECTURE.md` were kept current, including when no update was necessary;
- exact checks run and their outcomes;
- anything not verified or still requiring user action.

Never claim a check passed unless it ran successfully. Do not commit unless the user asked for a commit.
