---
name: code-planner
description: Run a conversational Plan Mode for code implementation work before editing code. Use when the user asks for "/plan", plan mode, Code Planner, an implementation plan, planning before coding, or a pre-edit technical approach. The skill requires non-mutating environment exploration, mandatory questions for unresolved material ambiguity, intent clarification, implementation clarification, risks, assumptions, verification checkpoints, and a final decision-complete Markdown plan. Also use before substantial or risky codebase changes where execution should wait for a complete plan.
---

# Code Planner

## Overview

Operate as a conversational planning mode for implementation work. Explore first, chat toward a decision-complete plan, and do not mutate repo-tracked state while planning.

## Mode Rules

- Stay in Plan Mode until the user explicitly asks to leave planning and implement.
- Treat execution requests during Plan Mode as requests to plan execution, not perform it.
- Do not use checklist/progress tools as a substitute for Plan Mode. If an `update_plan` tool is unavailable or disallowed in a plan-only context, do not try to use it.
- Produce at most one final plan per turn, and only when presenting a complete plan.
- Do not guess or choose silently when an unresolved ambiguity changes behavior, data contracts, identifiers, permissions, persistence, user experience, or implementation ownership.

## Implementation Handoff Principles

Shape the final plan so another engineer or agent can implement it without re-planning.

- Preserve existing architecture, terminology, ownership boundaries, and local coding style.
- Keep the implementation sequence surgical: start with the smallest behavior-enabling change, then directly related tests, then any narrow cleanup made necessary by the change.
- Avoid speculative abstractions, broad refactors, unrelated formatting, and feature expansion.
- Name affected subsystems, public interfaces, data contracts, migrations, or user-visible behavior when they matter for implementation safety.
- Define exact verification checkpoints tied to requirements and risks, starting with the smallest relevant check.
- Call out dependencies, ordering constraints, rollback or migration concerns, and compatibility risks when they affect execution.
- Make handoff details concrete enough that the implementer knows what to change, what not to change, and how to prove the work is complete.

## Mutation Boundary

Allowed non-mutating actions:

- Read or search files, configs, schemas, types, manifests, docs, and existing tests.
- Inspect repository structure, static code relationships, project instructions, and build scripts.
- Run dry-run commands when they do not edit repo-tracked files.
- Run tests, builds, or checks when their only writes are ordinary caches or build artifacts and their purpose is to validate feasibility.

Forbidden mutating actions:

- Edit, create, delete, or write repo-tracked files.
- Apply patches, migrations, code generation, or formatters that update repo-tracked files.
- Run commands whose purpose is to carry out the implementation rather than refine the plan.
- Commit, push, open pull requests, deploy, or mutate external systems.

When in doubt, if the action would reasonably be described as doing the work rather than planning the work, do not do it.

## Phase 1: Ground In The Environment

Begin with targeted non-mutating exploration. Resolve unknowns by discovering facts before asking the user.

- Inspect likely entry points, relevant files, configs, tests, schemas, types, and project instructions.
- Identify current behavior, existing conventions, adjacent implementation patterns, and realistic constraints.
- Ask before exploring only when the prompt itself contains an obvious contradiction or ambiguity that exploration cannot resolve.
- Do not ask questions that can be answered from the repo or system.

## Phase 2: Intent Chat

Clarify what the user actually wants before finalizing a plan.

- Establish the goal, success criteria, audience or user impact, in-scope and out-of-scope behavior, constraints, current state, and important preferences.
- Ask when a question materially changes the spec, confirms a meaningful assumption, or chooses between real tradeoffs.
- Ask instead of guessing when high-impact ambiguity remains.
- Do not finalize a plan that says "anchor on X or Y", "decide whether", "choose between", or otherwise leaves a material choice to the implementer.

## Phase 3: Implementation Chat

Clarify how the work should be built until the plan is decision complete.

- Lock down approach, interfaces, APIs, schemas, data flow, edge cases, failure modes, testing, acceptance criteria, rollout, monitoring, migrations, and compatibility constraints when they are relevant.
- Prefer the smallest implementation that satisfies the request and matches the existing architecture.
- Avoid inventing detailed schema, fallback, precedence, validation, or wire-shape policies unless the request establishes them or they prevent a concrete implementation mistake.
- Keep adjacent issues separate instead of silently expanding scope.

## Unknowns

Treat unknowns differently based on whether they are discoverable.

- Discoverable facts: inspect first. Ask if multiple plausible candidates remain, nothing can be found, or the ambiguity is product intent.
- Preferences and tradeoffs: ask early when they cannot be derived from exploration. Offer 2-4 mutually exclusive options and, when useful, a recommended option clearly labeled as a recommendation.
- Assumptions are allowed only for non-material defaults that do not change behavior, contracts, identifiers, data selection, rollout, or validation. If the assumption would affect how the implementation is written, ask.

## Asking Questions

Ask as many questions as needed to make the plan decision complete, but each question must:

- Materially change the spec or implementation plan.
- Confirm or reject an important assumption.
- Choose between meaningful tradeoffs.
- Not be answerable by non-mutating exploration.

Prefer the available user-input mechanism for important questions when the environment provides one. Offer only meaningful multiple-choice options; do not include filler choices that are obviously wrong or irrelevant. If the question cannot be expressed with reasonable choices, ask it directly and concisely.

Before asking, include the relevant facts discovered through exploration. When asking about remaining alternatives, present concrete candidates and recommend one only as a recommendation, not as a silent decision.

Do not proceed to the final plan while any question needed for a decision-complete plan is unanswered. If a question turns out to be non-material, remove it from the plan instead of treating it as an unresolved decision.

## Final Plan

Only output the official plan when it is decision complete and leaves no implementation decisions unresolved. Use plain Markdown with this compact structure:

```markdown
## Title

### Summary
- Briefly state the outcome and chosen approach.

### Key Changes
- Group implementation work by behavior or subsystem.
- Mention files only when needed to prevent ambiguity.

### Test Plan
- List concrete tests, checks, or manual scenarios tied to the risks and requirements.

### Assumptions
- Record only facts, constraints, and decisions already established by the user or discovered environment.
```

Do not ask "should I proceed?" inside the final plan. The user can leave Plan Mode or request implementation after receiving the final Markdown plan.

## Plan Quality Bar

- Make the plan human and agent digestible.
- Make it decision complete enough that another engineer or agent can implement it without making product or architecture decisions.
- Ask instead of planning around alternatives when a material fact or preference is unknown.
- Prefer compact plans with 3-5 short sections.
- Prefer grouped implementation bullets by subsystem or behavior over file-by-file inventories.
- Mention public APIs, interfaces, types, schemas, migrations, and compatibility concerns when affected.
- Tie every verification step to a requirement or risk.
- Mention tradeoffs only when they change the implementation choice.
- Avoid vague steps such as "update logic" or "add tests"; name the target behavior or test scope.
- For straightforward refactors, keep the plan to summary, key edits, tests, and assumptions.
- If the user asks for revisions after a prior final plan, produce a complete replacement plan.
