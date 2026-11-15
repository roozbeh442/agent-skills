# Implementation and validation

Use this reference only after the user approves the algorithm design.

## Create or inspect the project

For a new project, run the bundled initializer against the exact confirmed project root. It creates an atomic, standalone uv library project and refuses an existing destination. Inspect its output before editing it.

For an existing project:

- read its guidance, documentation, `pyproject.toml`, source, tests, and Git status;
- preserve unrelated changes and current public interfaces;
- use uv without replacing a working package layout merely for consistency;
- add only missing structure required by the approved design.

Write the approved design into `ALGORITHM.md` before implementing it. Keep every Markdown file below 500 lines. If a complex design approaches the limit, split focused validation details into `VALIDATION.md` and link it from `ALGORITHM.md`; do not create extra documents preemptively.

## Implement small observable units

Implement a narrow vertical path at a time:

1. Select one approved flowchart ID and its observable contract.
2. Add or update a focused test that would fail without that behavior when practical.
3. Implement the single primary function, class, or method assigned to that section.
4. Run the focused test.
5. Record that primary implementation symbol and its tests in the traceability table.

Preserve the approved one-to-one mapping. A primary symbol implements one substantive section; an orchestration symbol coordinates mapped sections without absorbing their calculations. If implementation reveals that a section should be split, combined, or mapped differently, revise the flowchart and obtain approval before changing that boundary.

Prefer pure functions and explicit parameters. Avoid hidden global state. Keep units visible in names, types, documentation, or a units library when the approved design requires one. Keep constants centralized with provenance and units.

Use a class only for justified shared state, configuration, invariants, or lifecycle. Separate numerical iteration from domain calculations when that makes convergence and failure easier to test. Expose useful diagnostics such as status, iterations, residual, tolerance, and warnings when applicable.

Keep the public interface small and framework-independent so the package can later be imported by the main application. Do not add adapters for that application during this workflow.

## Protect the approved method

Implementation discoveries may reveal a missing product or scientific decision. Stop dependent work and ask the smallest necessary question when a change would affect:

- governing equations or physical model;
- numerical, statistical, optimization, or approximation method;
- constants, units, coordinate systems, or sign conventions;
- validity range, convergence, precision, or acceptance tolerances;
- public input/output behavior.

Continue independent work when safe. Behavior-preserving refactoring does not need renewed approval when it preserves the approved section mapping. Renaming a mapped symbol requires a traceability update; splitting, combining, or moving substantive behavior across mapped sections requires a revised flowchart and user approval.

## Build meaningful validation

Choose tests that fit the algorithm rather than applying every category mechanically:

- unit tests for each flowchart section;
- end-to-end tests for the orchestration path;
- known-answer or analytical solutions;
- independent reference calculations or trusted datasets;
- mathematical and physical invariants;
- dimensional, range, and conservation checks;
- boundary, invalid-input, and failure cases;
- convergence order, stability, and termination tests;
- sensitivity or uncertainty checks;
- reproducibility with explicit random seeds;
- regression baselines only after independent validation;
- performance limits only when performance is an acceptance requirement.

Use explicit tolerances with a documented rationale. Avoid using outputs from the implementation under test as the sole expected result. Software tests alone do not establish scientific validity; state the achieved validation level accurately.

## Trace the design to evidence

Maintain a table in `ALGORITHM.md` with at least:

| Flow ID | Responsibility | Primary function/class/method | Unit tests | Integration or reference tests | Status |
|---|---|---|---|---|---|

Every approved flowchart ID must map to exactly one primary implementation symbol and validation evidence, or be marked incomplete with a reason. Every substantive implementation symbol must map back to a flowchart ID. Do not test Mermaid wording or claim that parsing the chart proves algorithm correctness.

Before finishing:

1. Compare code and tests against every approved flowchart node and non-goal.
2. Run `./test.sh` from the project root.
3. Confirm the package imports through the documented public interface.
4. Confirm `uv.lock` reflects the final dependencies.
5. Report deviations, limitations, unvalidated assumptions, and remaining integration work.
