# Requirements interview

Use this reference only during the requirements phase. The goal is to eliminate product ambiguity before application files are changed.

## Build a decision tree

Represent the request as a tree of decisions. A parent decision determines which child decisions matter. The **frontier** is the set of unanswered decisions whose prerequisites are already settled.

Work in rounds:

1. Recompute the frontier from the user's latest answers.
2. Ask all useful frontier questions that can be answered independently.
3. Wait for the user's answers before asking dependent questions.
4. Record the answers and reopen any downstream decisions invalidated by a changed parent.

Do not ask a question whose meaning depends on another unanswered question in the same round. If the full frontier would be exhausting to answer, group it into a small number of coherent sections without hiding or skipping branches.

## Separate facts from decisions

Inspect the repository and available tools for facts such as existing routes, menu configuration, database choice, schemas, dependencies, and test commands. Do not turn repository archaeology into questions for the user.

Ask the user when a choice changes product behavior, scope, cost, risk, or user experience. When repository guidance conflicts with the requested behavior, explain the conflict and ask which outcome should prevail; do not quietly edit the guidance.

## Prefer native option buttons

Use the interface's structured choice tool, such as `request_user_input`, whenever it is available and permitted in the current mode. Do not render a prose copy of questions that are already displayed by the tool.

For a native choice prompt:

- send one to three independent frontier questions per call;
- give each question two or three mutually exclusive options;
- put the recommended option first and end its label with `(Recommended)`;
- use each option's description to explain its effect or tradeoff in one short sentence;
- rely on the interface-provided Other/free-form option instead of adding a duplicate;
- continue with another button round when unresolved frontier questions remain.

If native choice controls are unavailable, say so briefly once and use the text fallback below. A skill cannot manufacture clickable controls in a surface that does not expose them.

## Ask actionable questions

Number questions continuously across rounds. For each question:

- give it a short title;
- explain why the decision matters when that is not obvious;
- provide two or three concrete, mutually exclusive choices when possible;
- put the recommended choice first and label it `(Recommended)`;
- explain the recommendation based on the description and current repository;
- in the text fallback, include `Other — describe your preferred answer` as the final choice so the user can enter free-form instructions;
- allow `yes` to accept the recommendation, a choice label to select an option, or free-form text to supply the Other answer.

If a question genuinely cannot be expressed as useful choices, ask for a short free-form answer and still offer a recommended default when one exists.

Use this compact shape only as the fallback when native buttons are unavailable:

```text
Q7 — Empty results: How should an empty search help the user recover?
A. Show guidance and a reset action. (Recommended)
B. Show an empty table with no guidance.
C. Other — describe your preferred answer.

Recommendation: A, because it prevents an empty screen from looking broken.
Reply A, B, or C with your own text. You can also reply “yes” to accept A.
```

Do not ask broad prompts such as “anything else?” while known branches remain. Do not repeat settled questions unless a later answer invalidates them.

## Explore only relevant branches

Use this list as coverage guidance, not as a questionnaire. Open a branch only when it could affect the requested feature.

- Outcome: user problem, success condition, and explicit non-goals.
- Actors: user types, ownership, visibility, and permissions.
- Workflow: entry points, sequence, navigation, and completion behavior.
- Domain rules: terminology, calculations, validation, state transitions, and edge cases.
- Data: fields, identifiers, relationships, history, retention, seed/import needs, and concurrency.
- Interface: desktop/mobile behavior, loading, empty, error, destructive, and confirmation states.
- API: request/response behavior, filtering, pagination, idempotency, and error semantics.
- Persistence: existing-data compatibility, migrations, deletion, and rollback expectations.
- Security: authentication, authorization, sensitive data, audit needs, and abuse limits.
- Integrations: ownership, credentials, failure handling, retries, and offline behavior.
- Operations: observability, configuration, deployment constraints, and support workflow.
- Acceptance: observable examples, critical test seams, and completion criteria.

Prefer worked examples for complicated rules. Ask the user to supply business examples only when they are the source of truth; calculate or inspect technical facts yourself.

## Handle uncertainty

If the user says “you decide” or “I don't care,” adopt the recommendation and record it as an accepted assumption. If two answers conflict, describe the contradiction and resolve it before proceeding.

A branch is resolved when the user has chosen an answer, accepted the recommendation, explicitly delegated the choice, or marked it out of scope.

## Completion test

The interview is complete only when:

- every relevant branch is resolved or explicitly excluded;
- acceptance criteria describe observable behavior;
- no known answer contradicts another answer or repository guidance;
- the implementation can proceed without inventing product behavior;
- expensive or difficult-to-reverse choices are visible in the build brief.

Then return to `SKILL.md` and present the build brief for explicit confirmation.
