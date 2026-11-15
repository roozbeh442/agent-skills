---
name: algorithm-design
description: Design, implement, and validate standalone Python algorithm side projects with user-approved flowcharts, explicit mathematical or physical assumptions, uv dependency management, and traceable tests. Use for algorithms that will later be imported into an application; exclude UI, API, database, and application-feature development.
---

# Algorithm Design

Develop an algorithm in a separate, importable Python project so its behavior, mathematics, physics, and numerical methods can be understood and validated before application integration.

## Boundary

- Do not use or extend `demonstrator-skill`; this is an independent side project.
- Do not modify the main application or integrate the algorithm into it unless the user separately requests that work.
- Keep application frameworks, UI, APIs, databases, and storage concerns out of the algorithm project.
- Use uv for project creation, dependencies, locking, and command execution.
- Keep every Markdown file created or edited by this skill below 500 lines.

## 1. Establish the destination and problem

Before designing:

1. Ask for the algorithm project name and the exact project root where the side project should be created or developed.
2. Resolve and repeat the full destination path. Confirm it before any write.
3. Inspect the destination if it already exists. Preserve its files and Git history; do not overwrite it or rerun the initializer there.
4. Confirm that the destination is separate from the main application. If the user deliberately chooses a path inside the main application, explain the coupling and obtain explicit confirmation before proceeding.
5. Inspect available requirements, reference calculations, datasets, and existing algorithm code. Ask for decisions rather than facts that can be discovered.

Read [references/design-phase.md](references/design-phase.md) completely, then conduct the design phase. Do not create the project or write implementation code during this phase.

## 2. Present the algorithm design

Present one reviewable design containing:

- purpose, users, inputs, outputs, units, target Python version, and public interface;
- selected physical, mathematical, empirical, or numerical methods;
- alternatives considered and material tradeoffs;
- equations, constants, coordinate systems, sign conventions, assumptions, and validity limits;
- error behavior, tolerances, convergence criteria, performance needs, and explicit non-goals;
- a Mermaid flowchart split into meaningful, testable sections with stable IDs;
- one primary function, class, or class method for every substantive flowchart section;
- validation sources and planned tests for every section;
- expensive or difficult-to-reverse choices.

Ask the user to approve the design or revise it. Do not scaffold or implement until the user explicitly approves it.

## 3. Implement only the approved design

After approval, read [references/implementation-validation.md](references/implementation-validation.md) completely.

For a new destination, resolve `<skill-dir>` as the directory containing this `SKILL.md`, then run:

```bash
python3 <skill-dir>/scripts/init_algorithm_project.py --name '<project-name>' --destination '<confirmed-project-root>' --python '<approved-version>'
```

Then replace the generated `ALGORITHM.md` design placeholder with the approved design before implementing calculations. For an existing project, adapt its current structure rather than running the initializer.

Implement the flowchart as a close structural map of the code. Every substantive section with a stable flowchart ID must correspond to exactly one primary function, class, or class method, including the orchestration section. Do not collapse several approved sections into one large symbol. A helper may remain outside the chart only when it is trivial and contains no algorithmic, physical, mathematical, validation, or decision behavior; otherwise add it as an approved flowchart section.

Prefer pure functions for calculations and transformations. Use a class only when persistent state, configuration, invariants, or a lifecycle makes it clearer. If a class owns several substantive algorithm steps, map those steps to separate methods and flowchart sections. Keep one module until separate responsibilities create a concrete need to split it.

A post-approval change to equations, physical models, numerical methods, constants, units, coordinate systems, validity limits, acceptance tolerances, or the flowchart-to-symbol decomposition requires user approval before dependent implementation continues. Ordinary refactoring that preserves both approved behavior and the approved section mapping does not.

## 4. Validate and finish with evidence

- Test each section through its mapped function, class, or method, and cover the composed algorithm end to end.
- Validate against independent analytical results, trusted data, invariants, convergence behavior, or another suitable oracle where practical.
- Maintain a traceability table in `ALGORITHM.md` mapping each flowchart ID to implementation symbols and tests. Tests prove behavior; the table proves design coverage.
- Keep `./test.sh` as the single full-project verification entry point and have it invoke each mandatory suite exactly once.
- Run focused checks while developing and `./test.sh` after all changes. Never claim an unrun check passed.
- Do not initialize Git, commit, publish, or integrate with the main application unless separately requested.

Report the project path, approved methods and non-goals, public import interface, traceability result, exact checks and outcomes, limitations, and any remaining validation or integration work.
