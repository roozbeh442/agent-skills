# Algorithm design phase

Use this reference before any project files or implementation code are created. The objective is to make the algorithm understandable and testable without silently choosing scientific or product behavior for the user.

## Select and confirm the side-project root

Ask for the project name and exact project root. Treat the root as the final project directory, not merely an unspecified workspace. Resolve `~`, relative components, and symbolic links where possible, then show the resulting absolute path.

Confirm that:

- the user intends this as a separate side project;
- the path is not the main application repository unless deliberately chosen;
- a new destination does not already exist; or
- an existing destination may be inspected and extended without overwriting unrelated work.

Do not create a temporary design file in the main application. Keep the pre-approval design in the conversation until the user approves it.

## Resolve the algorithm contract

Explore only branches relevant to the requested algorithm:

- purpose, success conditions, users, and explicit non-goals;
- normalized distribution/package name and target Python compatibility, including the main application's version when known;
- input and output types, shapes, ranges, units, precision, and missing-data behavior;
- reference frames, coordinate systems, sign conventions, boundary and initial conditions;
- governing equations, physical laws, empirical correlations, or statistical assumptions;
- constants and their source, units, uncertainty, and expected update policy;
- candidate analytical, numerical, optimization, stochastic, or approximation methods;
- validity domain and behavior outside it;
- acceptable error, convergence, repeatability, complexity, and performance;
- expected failure modes and diagnostic information;
- trusted examples, datasets, measurements, analytical solutions, or existing implementations.

Ask the user for decisions that change behavior. Inspect supplied materials and calculate technical facts rather than asking the user to rediscover them.

When more than one credible method exists, present the meaningful alternatives, their assumptions, accuracy, stability, complexity, dependencies, and limitations. Recommend one based on the stated needs, but let the user choose or explicitly delegate the choice.

Record citations or provenance for equations, constants, correlations, and validation data when sources are available. Distinguish model uncertainty, input uncertainty, discretization error, solver error, and floating-point error when relevant.

## Create a testable flowchart

Use Mermaid. Assign stable IDs such as `A01`, `A02`, and `A03` to every substantive processing or decision section. Do not assign IDs to purely visual start/end connectors. A useful section has an observable contract and can be validated independently or through a clearly identified integration test.

Design for a close one-to-one correspondence between chart and code:

- map every stable-ID section to exactly one primary function, class, or class method;
- give the orchestration section its own function or method that composes the other mapped symbols;
- do not map several substantive sections to one large function or class;
- if one class owns several substantive steps, show each step as a separate section mapped to a method;
- do not hide meaningful calculations, physics, method choices, validation, or branching in an uncharted helper;
- allow an uncharted helper only when it is trivial and contains no independent algorithm behavior.

For every node define:

- responsibility and chosen method;
- inputs, outputs, types, shapes, and units;
- preconditions, postconditions, and invariants;
- failure and diagnostic behavior;
- proposed primary function, class, or class method;
- validation oracle and planned tests;
- dependencies on other nodes.

Break large calculations into coherent units, not arbitrary line-count chunks. Prefer functions when behavior can be expressed as input to output. Propose a class only for meaningful state, shared configuration, enforced invariants, resource ownership, or an iterative lifecycle. The one-to-one rule is a troubleshooting boundary, not a reason to create one-line wrappers or speculative abstraction layers; combine trivial presentation-only actions within the nearest substantive section.

Include a clear orchestration node that shows how the smaller units compose. Identify iteration, branching, convergence, fallback, and termination explicitly.

## Approval brief

Present the complete design in a concise reviewable form with:

1. Algorithm contract and non-goals.
2. Chosen methods and alternatives considered.
3. Equations, assumptions, units, constants, and validity limits.
4. Mermaid flowchart with stable IDs.
5. One-to-one flowchart-to-function/class/method decomposition.
6. Validation plan mapped to every flowchart ID.
7. Public import interface, target Python version, and expected dependencies.
8. Known limitations and difficult-to-reverse decisions.

Ask for explicit approval. If the user revises a parent decision, revisit affected flowchart nodes, interfaces, and tests before asking for approval again.
