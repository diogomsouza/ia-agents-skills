# IA Agents Skills

A collection of Codex agents and skills. The project organizes reusable instructions under `.codex/agents` and `.codex/skills`, with global guidelines in `.codex/AGENTS.md`.

## Agents

- `code-reviewer`: reviews changed code against project guidelines, style rules, relevant bugs, and quality concerns before commits or pull requests.
- `code-reviewer-max`: reviews complex changes with an advanced focus on architecture, maintainability, branching, abstractions, contracts, and structural quality.
- `code-reviewer-security`: reviews high-risk changes with a focus on security, authorization, privacy, data integrity, feature gates, and critical regressions.
- `code-simplifier`: simplifies newly written or modified code while preserving behavior and prioritizing clarity, consistency, and maintainability.
- `code-worker`: implements features, bug fixes, refactors, and migrations with a strict focus on clarity, architectural boundaries, and low incidental complexity.
- `comment-analyzer`: analyzes comments, docstrings, and technical documentation for accuracy, completeness, and long-term maintainability.
- `csharp-expert`: supports .NET/C# development with a focus on platform conventions, clean design, security, testing, performance, and maintainability.
- `optimizing-dotnet-performance`: analyzes .NET code for bottlenecks, recommends concrete optimizations, and guides benchmark validation.
- `pr-test-analyzer`: evaluates pull request test coverage quality, focusing on critical paths, edge cases, and tests that prevent real regressions.
- `silent-failure-hunter`: audits error handling, fallbacks, and `catch` blocks to find silent failures, insufficient logging, and weak actionable feedback.
- `type-design-analyzer`: reviews type design, invariants, encapsulation, and validation to improve model robustness and clarity.
- `win-forms-expert`: supports creation and maintenance of Designer-compatible WinForms apps, including layout, binding, DPI, dark mode, and `.designer` file rules.

## Skills

- `agent-hive`: coordinates larger work with persistent planning, subagent delegation, independent verifiers, conditional checkpoint commits, and a progress file.
- `analyzing-dotnet-performance`: scans .NET code for performance anti-patterns in async, memory, strings, collections, LINQ, regex, serialization, and I/O.
- `architecture-blueprint-generator`: generates an architecture blueprint from codebase analysis, documenting the stack, patterns, components, dependencies, and diagrams.
- `angular-developer`: guides and generates Angular code using modern best practices for components, services, reactivity, forms, routing, accessibility, testing, and CLI usage.
- `angular-new-app`: creates new Angular applications with the Angular CLI, including CLI checks, appropriate flags, and AI assistant configuration.
- `code-planner`: runs a conversational planning mode for implementation work before editing code, with non-mutating exploration, required questions, and a complete final plan.
- `dotnet-webapi`: guides creation and modification of ASP.NET Core Web API endpoints with HTTP semantics, OpenAPI metadata, DTOs, and error handling.
- `gpt-image-2`: generates or edits bitmap images through the OpenAI Images API using `gpt-image-2`, saving project-ready assets.
- `grill-code`: runs a technical interview about a plan using context, ADRs, and versioned documents, without implementing code until explicitly approved.
- `grill-me`: interviews the user about a plan or design one question at a time until ambiguities and decision dependencies are resolved.
- `optimizing-ef-core-queries`: guides Entity Framework Core query optimization, covering N+1 issues, tracking modes, compiled queries, and common database-load traps.
- `thermo-nuclear-code-quality-review`: runs an extremely strict maintainability review focused on abstractions, large files, and complex conditional growth.
- `thermo-nuclear-review`: runs a deep security and correctness audit of branch changes, focusing on bugs, breakages, developer-experience regressions, and feature-gate leaks.

## Structure

```text
.codex/
  AGENTS.md
  agents/
  skills/
```

## Recommended Operational Flow

Use these skills when the work carries decision, domain, or implementation risk:

```text
grill-code -> code-planner -> agent-hive
```

- `grill-code`: validates understanding, terms, domain boundaries, and architectural decisions.
- `code-planner`: turns the validated understanding into a closed implementation plan.
- `agent-hive`: executes the plan with subagents, checkpoints, and independent verification.

Not every case needs all three. For simple changes, direct execution with review is usually enough. For complex changes, use the full flow.

## code-planner

Use when you want to plan before editing code.

Ideal cases:

- non-trivial feature;
- bug with uncertain cause;
- change that affects APIs, contracts, schemas, permissions, or persistence;
- refactor with regression risk;
- migration between patterns or libraries;
- when you want a plan another agent can implement without re-planning.

Workflow:

1. Explore the code without modifying files.
2. Identify current behavior, local patterns, and risks.
3. Ask questions only about material ambiguities.
4. Define scope, out-of-scope items, and expected success.
5. Produce a final plan with summary, main changes, test plan, and assumptions.

When not to use:

- obvious one-line fix;
- purely textual change;
- task where the user already provided a closed plan and asked for direct execution.

## grill-code

Use when the problem needs to be questioned before becoming a plan or code.

Ideal cases:

- poorly defined domain;
- ambiguous names such as `account`, `order`, `cancellation`, or `session`;
- business rule with exceptions;
- change that may require an ADR;
- plan that looks correct but depends on undocumented invariants;
- before implementing something that changes responsibilities across modules.

Workflow:

1. Explore existing code and documentation.
2. Ask exactly one question at a time.
3. Recommend an answer, but wait for confirmation.
4. When a term, boundary, or invariant is resolved, record it in `docs/CONTEXT-{context-id}.md`.
5. When there is a relevant architectural decision, create an ADR in `docs/adr/`.
6. At the end, ask whether implementation may begin.

When not to use:

- when the domain is already clear;
- when the user only wants a review;
- when the change is purely mechanical.

## agent-hive

Use when work needs orchestration with subagents, persistent progress, and independent verification.

Ideal cases:

- long or multi-step implementation;
- large migration;
- refactor across several modules;
- feature that crosses layers;
- fix with high regression risk;
- work that can be divided among agents;
- when you want execution with checkpoints, review, and phase-by-phase validation.

Workflow:

1. Create or reuse a goal.
2. Create `.agent-hive/PLAN-PROGRESS-{context-id}.md`.
3. Discover available agents.
4. Record the original request, scope, risks, execution plan, validations, and activity queue.
5. Delegate exploration when needed.
6. Delegate execution to `code-worker`.
7. Collect the result.
8. Delegate verification to a separate reviewer.
9. If approved, run validation.
10. For multi-step work, attempt a checkpoint commit.
11. Repeat until all phases are accepted.
12. Record residual risks and finish.

Agent usage:

- `code-worker`: execution agent. Implements code, fixes bugs, performs refactors, and runs proportional validations.
- `code-reviewer`: standard verification for small or medium changes, focused on guidelines, obvious bugs, and ordinary maintainability.
- `code-reviewer-max`: advanced verification for architecture, complexity, branching, abstractions, contracts, and maintainability.
- `code-reviewer-security`: verification focused on security, authorization, privacy, data integrity, feature gates, and critical regressions.

## Quick Choice

- I want to think before coding: `code-planner`
- I want to be questioned about the domain or plan: `grill-code`
- I want to execute a complex plan with agents: `agent-hive`

## Recommended Flows

For a feature with uncertain domain:

```text
grill-code
-> agent-hive
   -> code-worker
   -> code-reviewer-max
```

For a change in authentication, authorization, billing, or feature flags:

```text
code-planner
-> agent-hive
   -> code-worker
   -> code-reviewer-security
   -> code-reviewer-max if there is also structural risk
```

For a large refactor:

```text
code-planner
-> agent-hive
   -> multiple code-worker agents by module
   -> code-reviewer-max by batch
```

For an already written but suspicious plan:

```text
grill-code
-> agent-hive if execution is large
```

## Usage

Copy or keep the `.codex` folder at the root of a workspace that should load these agents and skills. Adjust the instructions as needed for each project.
