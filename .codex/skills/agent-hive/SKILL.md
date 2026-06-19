---
name: agent-hive
description: Coordinate non-trivial work through a created goal, mandatory specialist subagent delegation, explicit verifier subagents, and a persistent .agent-hive/PLAN-PROGRESS-{context-id}.md file containing the full execution plan and progress state. Use when the user asks to orchestrate agents, run subagents, coordinate multi-step execution, delegate workstreams, execute a plan with verification, maintain agent progress state, or handle longer coding, research, analysis, migration, review, or implementation tasks where errors could compound across phases.
---

# Agent Hive

Use this skill to act as a coordinator, not the primary executor. Own the goal, context, sequencing, delegation, progress file, and final reporting. Delegate bounded execution to suitable agents and gate every phase with independent verifier agents before proceeding.

The pattern is intentionally narrow: clear goal, explicit stop conditions, delegated execution, pragmatic verification, and reproducible progress notes.

## Goal Activity Mode

Configure the goal as a checkpointed activity loop, not as one long uninterrupted execution. Optimize for throughput by making each activity a useful checkpointed batch, not a tiny serial step.

- Keep the goal active until all completion gates pass.
- In each Codex activity, read the progress file first, choose the next pending checkpointed batch, execute only that batch, update the progress file, then end the turn.
- Do not try to finish the whole goal in one activity unless the progress file shows only final reporting remains.
- Do not mark the goal complete after an intermediate activity. Mark it complete only when every `Execution Plan` phase is `Done`, `Accepted`, or `Not Applicable`; no `Activity Queue` item remains `Pending`, `In Progress`, `Retry Required`, or unresolved `Blocked`; all `Completion Gates` are checked; validation evidence is recorded; and residual risks are documented.
- Each activity must leave enough state in `.agent-hive/PLAN-PROGRESS-{context-id}.md` for the next continuation to resume without chat memory.
- Treat `.agent-hive/PLAN-PROGRESS-{context-id}.md` as the execution contract, not just a progress log. It must contain the user request, accepted plan, exploration findings, work breakdown, dependencies, validation gates, activity queue, and current progress needed to continue from a clean context.
- The next activity should decide what to do from the progress file, not from assumptions about the previous turn.

Use these activity types as the default queue:

1. Initialize goal and progress file.
2. Discover subagent tooling and specialists.
3. Spawn a batch of independent execution agents for the next bounded phases.
4. Collect available execution results and update progress.
5. Spawn verifier agents for completed phase batches.
6. Collect verifier results and either accept phases or create retry activities.
7. Run or delegate validation for accepted batches.
8. For multi-step work, attempt a checkpoint commit for accepted, validated, integrated code changes when the repository is versioned and commits are permitted.
9. Repeat for the next phase.
10. Perform final residual-risk review.
11. Final report and mark goal complete.

At the end of each non-final activity, explicitly stop after updating progress. Let the active goal continuation pick up the next activity.

## Checkpoint Commits

For multi-step work, after each checkpointed phase or batch has been executed, verified, and integrated, attempt to commit the completed code before moving to the next phase.

- Attempt checkpoint commits only when the requested work has more than one execution phase, checkpointed batch, or dependent next step.
- Do not create a checkpoint commit when all requested work is completed in a single accepted batch and the only remaining action is final reporting. Record the checkpoint commit status as `Not Applicable` in the progress file and continue to completion.
- Only attempt a commit when the affected code is in a versioned repository and the current environment, user instruction, and repository state allow commits.
- Treat checkpoint commits as best effort. If the repository is not versioned, commit permission is unavailable, Git identity is missing, hooks fail, the worktree contains unresolved unrelated changes, or any other commit attempt fails, record the reason in the progress file and continue the Agent Hive process.
- Do not block, retry indefinitely, or ask the user only because a checkpoint commit could not be created.
- Do not include unrelated user changes in a checkpoint commit. Commit only files intentionally changed for the accepted checkpoint, plus directly related generated artifacts when they are part of the agreed deliverable.
- Use a concise checkpoint commit message that names the completed phase or batch.
- Record every checkpoint commit attempt in `Checkpoint Commits` with status, commit SHA when available, files or scope, and any skip or failure reason.
- Make the checkpoint commit after verifier acceptance and required integration validation, before adding or starting the next dependent execution phase.

## Progress File as Execution Contract

The progress file is the source of truth for both planning and execution. A future Agent Hive continuation must be able to read only the progress file plus the repository and know what to implement next.

- Record the original user request and any user-approved implementation plan before spawning execution workers.
- If the user previously asked for a plan and then asks Agent Hive to implement it, reconstruct the implementation plan into the progress file before executing. Do not rely on conversation memory, hidden window context, or a prior final answer.
- Convert the plan into concrete phases with scope, files or modules, dependencies, acceptance criteria, validation commands, verifier type, retry policy, and stop condition.
- Keep an explicit `Execution Plan` section separate from `Progress`. `Execution Plan` states what must be done and tracks each phase status; `Progress` records the audit trail of what happened.
- Keep an explicit `Explorer Findings` section. Every exploration agent result that changes scope, risks, file inventory, implementation order, or validation strategy must be summarized there before spawning workers that depend on it.
- Update the `Execution Plan` and `Activity Queue` when exploration or verification changes the work. Do not bury plan changes only in runtime notes.
- Record enough detail for each pending activity that a newly resumed agent can prompt a worker without consulting chat history.
- If the progress file does not contain enough information to continue, the next activity is to repair the progress file, not to implement code.
- Use `Execution Plan.Status` as the authoritative answer to "what has been implemented from the plan?" Use `Progress` only as evidence for why a status is correct.
- Use these phase statuses consistently: `Pending`, `In Progress`, `Done`, `Accepted`, `Rejected`, `Retry Required`, `Blocked`, and `Not Applicable`.
- Change a phase to `Done` only after execution work is complete. Change it to `Accepted` only after separate verifier gates pass. Use `Retry Required` when verification fails and a correction activity is needed.

## Throughput Rules

Preserve verification while avoiding unnecessary serialization.

- Prefer parallel batches over single-task sequencing. If work can be split by disjoint files, modules, packages, routes, libraries, test suites, or migration categories, spawn multiple execution agents in the same activity.
- Keep write scopes disjoint for parallel workers. If scopes overlap, serialize those specific scopes or assign one worker ownership.
- Default to 2-4 parallel execution agents for code changes. Use more only for read-only exploration or clearly isolated edits.
- Batch verification at the phase level, not per tiny edit. A verifier may review a coherent batch of related worker outputs when downstream risk is the same.
- Use strict verification for high-risk shared infrastructure, build configuration, migrations, security-sensitive code, data changes, or public APIs.
- Use pragmatic or sampled verification for repetitive low-risk mechanical edits after one representative strict check has passed.
- Set a retry budget per phase, usually one retry before escalating to the user or changing strategy. Do not loop indefinitely.
- Record elapsed time or rough duration per activity. If an activity takes much longer than the non-orchestrated baseline, reduce orchestration overhead by increasing batch size, lowering verifier granularity, or narrowing scope.
- Do not create agents that only restate obvious context. Agents should execute, inspect a distinct risk, or verify concrete output.

For migrations, prefer this structure:

1. Exploration batch: one or more agents map the migration surface by package/module and identify independent slices.
2. Planning checkpoint: Agent Hive records the explorer findings, slices, dependencies, validation approach, concurrency plan, and full execution plan in the progress file.
3. Execution batches: workers migrate independent slices in parallel with disjoint write ownership.
4. Verification batches: verifier agents review completed slices or a batch of related slices.
5. Integration validation: run build/test/lint after each meaningful batch, not after every file.

## Subagent Waiting Policy

When the next orchestration decision depends on a running subagent, wait for that subagent to finish.

- Use the longest available wait window for subagent waits. If the wait tool has a maximum timeout and returns no final status, immediately wait again.
- Do not interrupt, narrow scope, request status, or mark an activity as incomplete only because a subagent is taking a long time.
- Long-running work such as installs, builds, migrations, dependency resolution, or test suites is expected. Treat elapsed time as normal unless there is concrete evidence of failure or a reported blocker.
- Do not ask the subagent for status just to decide whether to keep waiting. Ask for status only when there is evidence that the agent is blocked, looping, or waiting for external input.
- Do not end the current activity while a spawned execution or verifier subagent is still needed for the next gate. Continue waiting until it completes, fails, or reports a blocker.
- Record long waits in `Runtime Notes`, but do not use runtime alone as a reason to change strategy.
- If multiple subagents are running and at least one finishes, process completed results that do not depend on still-running agents; keep waiting for the rest when their outputs are required.

## Non-Negotiable Delegation Contract

When this skill is explicitly invoked or the user asks for agents, subagents, delegation, or orchestration, treat that as authorization to use subagents.

- The main process must not perform implementation, investigation, analysis, or verification work that can be delegated.
- The main process may create the goal, create and update the progress file, decompose work, prepare prompts, inspect returned results, integrate agent outputs, and communicate status.
- Every execution phase must be assigned to an execution subagent.
- Every completed execution phase must be checked by a separate verifier subagent before the next dependent phase starts.
- Do not use the same subagent as both executor and verifier for the same phase.
- If subagent tools are not visible, first search for them using the available tool discovery mechanism, with a query like `spawn subagent delegate task multi-agent agent verification`.
- If subagent tools are genuinely unavailable, stop and tell the user that orchestration cannot proceed as designed unless they enable subagent tooling. Record the blocker in the progress file. Do not silently continue as a single-agent executor.

## Required Start

1. Create or reuse a goal for the user-visible objective. If goal tools are available and no active matching goal exists, call the goal creation tool with a concrete objective.
2. Create `.agent-hive/PLAN-PROGRESS-{context-id}.md` directly before substantial work starts. Do not use a helper script for this.
3. When creating `.agent-hive` on Windows, make a best-effort attempt to mark it as hidden, for example by running `attrib +h .agent-hive` from the workspace root after the directory exists. If hiding fails or the platform does not support it, ignore and continue.
4. Build `context-id` as `YYYY-MM-DD-{short-task-slug}` using local time when known, otherwise UTC. The slug must be lowercase kebab-case, derived from three to six meaningful words from the task, and capped around 40 characters. If `.agent-hive/PLAN-PROGRESS-{context-id}.md` already exists, append a sequential suffix to the context id such as `-2`, `-3`, continuing until the filename is unique. Do not include a time component or random suffix.
5. Discover available subagent tooling and specialist capabilities before any execution work. Record the available execution and verifier options in the progress file.
6. Diagnose orchestration state before delegating. Record inventory, assumptions, risks, initial plan, and completion gates in the progress file. The diagnosis may identify files and tools, but substantive exploration must be delegated to an explorer or specialist agent.
7. Before any execution worker starts, ensure the progress file contains an `Execution Plan` with all phases, dependencies, validation gates, verifier assignments, and stop conditions. If exploration is required first, create a pending `Synthesize explorer findings into execution plan` activity and complete it after explorers return.

Use this initial file shape. In `Source Request and Plan` and `Inventory`, keep each field as a parent bullet and put all values on indented child bullets, even when there is only one value. Do not collapse these fields into single-line `- Field: value` bullets when creating or updating the progress file.

```markdown
# Agent Plan Progress: {context-id}

Task: {task}
Generated: {timestamp}

## Source Request and Plan

- User request:
  - `{original user request}`
- Prior user-approved plan or requested plan:
  - Pending capture, no prior detailed plan, or `{plan item}`.
- In-scope systems:
  - Pending scope confirmation.
- Out-of-scope systems:
  - Pending scope confirmation.
- Success definition:
  - Pending success definition.

## Diagnostic of Current State

- Pending initial diagnosis.

## Inventory

- Systems and tools:
  - Pending inventory.
- Available agents or specialists:
  - Pending discovery.
- Delegation tools:
  - Pending discovery.
- Execution mode:
  - Agent Hive coordinator delegates execution and verification.
- Parallelism plan:
  - Pending batching plan.
- Time budget:
  - Pending estimate.
- Assumptions:
  - Pending assumption review.
- Artifacts:
  - Progress file: `.agent-hive/PLAN-PROGRESS-{context-id}.md`.

## Identified Risks

- Pending risk review.

## Explorer Findings

| Time | Agent | Scope | Findings Integrated Into Plan |
| --- | --- | --- | --- |
| Pending | TBD | TBD | Pending exploration. |

## Execution Plan

| Phase | Status | Scope | Owner Type | Dependencies | Acceptance Criteria | Validation | Verifier | Stop Condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Pending | Discovery and plan synthesis | explorer + Agent Hive | Goal and inventory | Findings summarized and concrete phases created | Progress file review | Agent Hive | Execution plan is complete enough to resume without chat context. |

## Incremental Steps

1. Diagnose current state and constraints.
2. Capture the user request and any prior implementation plan in this progress file.
3. Delegate exploration when current code state is unclear.
4. Integrate explorer results into `Explorer Findings` and update `Execution Plan`.
5. Execute the next checkpointed batch from `Activity Queue`.
6. Update this progress file.
7. For multi-step work, attempt a checkpoint commit after a completed batch is accepted, validated, and integrated, when commits are possible.
8. Stop the current activity unless final completion gates are met.
9. On continuation, reread this file and choose the next pending activity.

## Completion Gates

- [ ] Goal is explicitly defined.
- [ ] Source request, accepted plan, scope, and success definition are captured.
- [ ] Delegation tools and specialists recorded.
- [ ] Initial diagnosis recorded.
- [ ] Inventory recorded.
- [ ] Risks recorded.
- [ ] Full execution plan recorded.
- [ ] Explorer findings recorded or explicitly not required.
- [ ] Every required execution phase is delegated to subagents.
- [ ] Every completed execution phase is verified by separate verifier subagents.
- [ ] Every `Execution Plan` phase is `Done`, `Accepted`, or `Not Applicable`.
- [ ] No `Activity Queue` item remains `Pending`, `In Progress`, `Retry Required`, or unresolved `Blocked`.
- [ ] Required validation has passed or validation gaps are documented.
- [ ] Required multi-step checkpoint commits were created for accepted code batches, or `Not Applicable`/skipped attempts are documented.
- [ ] Residual risks are documented.
- [ ] Final accounting is recorded before final response.

## Architectural Decisions

| Time | Decision | Rationale | Alternatives Considered |
| --- | --- | --- | --- |
| {timestamp} | Use orchestrated execution with verification gates. | Prevent unchecked errors from compounding across phases. | Single-agent execution. |

## Progress

| Time | Phase | Agent/Tool | Result | Verification |
| --- | --- | --- | --- | --- |
| {timestamp} | Initialization | Agent Hive | Progress file created. | Not applicable. |
| TBD | Delegation discovery | Agent Hive | Subagent tooling and specialists identified. | Not applicable. |

## Checkpoint Commits

| Time | Phase or Batch | Status | Commit | Scope | Notes |
| --- | --- | --- | --- | --- | --- |
| Pending | TBD | Pending | TBD | TBD | Attempt only for multi-step work after accepted, validated, integrated code changes; mark `Not Applicable` for single-batch completion. |

## Activity Queue

| Status | Activity | Owner | Stop Condition |
| --- | --- | --- | --- |
| Pending | Discover subagent tooling and specialists. | Agent Hive | Execution and verifier options recorded. |
| Pending | Capture source request and prior implementation plan. | Agent Hive | Progress file contains enough task context to continue without chat history. |
| Pending | Create parallelism and batching plan. | Agent Hive | Independent slices, dependencies, validation approach, and concurrency plan recorded in `Execution Plan`. |
| Pending | Spawn exploration batch when needed. | explorer subagents | Current code state and migration surface mapped. |
| Pending | Synthesize explorer findings into execution plan. | Agent Hive | `Explorer Findings`, `Execution Plan`, and `Activity Queue` updated from explorer output. |
| Pending | Spawn first execution batch. | execution subagents | Independent subagents spawned or assigned with disjoint scopes. |
| Pending | Collect first execution batch. | Agent Hive | Results recorded in Progress. |
| Pending | Spawn verifier batch. | verifier subagents | Verifiers spawned or assigned for completed batch. |
| Pending | Collect verifier batch. | Agent Hive | Phases accepted or retry activities added. |
| Pending | Decide or attempt checkpoint commit for accepted code batch. | Agent Hive | Commit created for multi-step work, or `Not Applicable`/skip/failure reason recorded in `Checkpoint Commits`. |

## Runtime Notes

| Activity | Started | Finished | Duration | Notes |
| --- | --- | --- | --- | --- |

## Final Accounting

- Started:
- Finished:
- Total duration:
- Token usage:
- Usage source:

## Residual Risks

- Pending final review.
```

## Delegation Rules

- Delegate execution; do not silently implement, investigate, analyze, test, or fix substantial work yourself.
- Check available specialist agents, skills, plugins, or tools before using a generic worker. Prefer specialists for code implementation, code review, testing, security, data analysis, design, documents, GitHub, or domain-specific work.
- Use an explorer or specialist subagent before implementation when repository structure, conventions, requirements, or failure modes are unclear.
- Require explorer outputs to be structured for direct insertion into `Explorer Findings` and `Execution Plan`: affected files/modules, required phases, dependencies, risks, validation commands, and recommended worker scopes.
- Give each subagent a narrow task, the minimum relevant context, expected artifact, constraints, and stop condition.
- Keep Agent Hive responsible for sequencing, tracking, re-delegation, and user-facing status.
- If a phase seems too small to delegate, merge it into a larger delegated phase or ask the user whether to continue without orchestration. Do not default to doing it locally.
- Prefer one checkpointed batch per Codex activity. A batch may spawn several workers, collect available results, spawn verifiers for completed results, and update progress if that fits cleanly in the activity.
- Avoid turning every spawn, wait, or result collection into its own activity unless the system itself naturally ends the activity there.

## Subagent Prompt Pattern

Execution subagent prompt:

```text
You are the execution agent for phase {phase}. You are not alone in the codebase; do not revert unrelated edits and adapt to existing changes. Scope: {bounded scope}. Context: {minimal context}. Deliverable: {artifact/result}. Stop condition: {checkable done state}. Report files changed, commands run, assumptions, blockers, and evidence.
```

Explorer subagent prompt:

```text
You are the explorer for phase {phase}. Do not implement changes. Scope: {bounded scope}. Context: {minimum context from the progress file}. Deliverable: structured findings for the Agent Hive progress file, including affected files/modules, current behavior, recommended execution phases, dependencies, risks, validation commands, and open questions. Stop condition: enough evidence for Agent Hive to update `Explorer Findings`, `Execution Plan`, and `Activity Queue` without relying on chat history.
```

Verifier subagent prompt:

```text
You are the verifier for phase {phase}. Review the executor output and evidence. Do not perform the implementation yourself. Answer: Is this result correct enough to support the next dependent step? If no, list specific corrections required. Check against: {phase acceptance criteria and completion gates}. Also report validation evidence that supports your conclusion.
```

## Execution Loop

For every phase or subtask, advance through one checkpointed batch per Codex activity:

1. **Execute activity**: Do the next pending batch from `Activity Queue`.
2. **Record**: Append the result, artifacts, commands, and open questions to the progress file.
3. **Plan update**: If the result is exploration, verification feedback, or a scope change, update `Explorer Findings`, `Execution Plan`, and `Activity Queue`, not only `Progress`.
4. **Checkpoint commit**: For multi-step work, after accepted, validated, integrated code changes, create a best-effort commit when possible. For single-batch completion, record `Not Applicable`; otherwise record why it was skipped or failed.
5. **Stop or finish**: If completion gates are not fully met, end the current activity. If they are met, produce final report and mark the goal complete.

For a full phase, the required state transitions are:

1. **Execute**: Spawn or assign bounded tasks to the best available execution subagents, using parallel workers for independent scopes.
2. **Collect**: Record executor results, artifacts, commands, and open questions.
3. **Verify**: Spawn or assign verification to separate verifier subagents. Verify coherent batches when risk allows.
4. **Gate**: Collect the verifier answer to: "Is this result correct enough to support the decisions or steps that depend on it next?"
5. **Retry if needed**: If the answer is no, add a retry execution activity with the verifier's specific correction guidance. Do not proceed past the gate.
6. **Integrate and validate**: Run or delegate the required integration validation for the accepted phase or batch.
7. **Commit checkpoint**: If the answer is yes and validation passes or documented validation gaps are accepted, attempt the checkpoint commit before adding or starting the next dependent phase only when there is more than one execution phase, checkpointed batch, or dependent next step. If this accepted batch completes the entire request in one step, record the checkpoint commit as `Not Applicable` and proceed to final reporting.
8. **Advance**: Update `Execution Plan.Status`, update completion gates when applicable, and add the next phase activity.

Use pragmatic verification for reports, investigations, prototypes, and decision-support work. Use stricter verification for production code, security, compliance, migrations, data integrity, or user-impacting behavior; require relevant tests, builds, lint, review checks, or reproducible validation.

## Progress File Requirements

Keep the progress file current. It must include:

- Source request, in-scope/out-of-scope boundaries, and success definition
- Prior user-approved plan or a reconstructed implementation plan when the user asks to implement a plan
- Diagnostic of the current state
- Inventory of relevant files, systems, agents, tools, assumptions, and artifacts
- Identified risks
- Explorer findings, including raw enough summaries of subagent analysis to guide execution
- Full execution plan with phases, dependencies, acceptance criteria, validation, verifier, and stop conditions
- Incremental steps
- Completion gates
- Architectural decisions
- Activity queue with all known required activities, not just the immediate next step
- Progress log
- Checkpoint commit attempts, including successful commit SHAs, `Not Applicable` single-batch decisions, or skip/failure reasons
- Residual risks

Update the file after every meaningful phase, verification result, decision, or scope change. Treat it as the durable state that lets the work resume without relying on chat memory.

Before spawning an execution worker, verify the progress file answers:

- What exactly is being implemented?
- Which files or modules are in scope?
- What phases are required and in what order?
- What did explorers discover that changes the plan?
- What validation and verifier gates prove completion?
- What remains pending?

If any answer is missing, update the progress file first.

## Decision Points

- If requirements are unclear enough to materially change decomposition, ask the user before splitting the work.
- If several agents can do the work, prefer the specialist with the closest domain fit.
- If a verifier cannot evaluate a phase, tighten the phase output and stop condition, then retry.
- If verification fails, do not patch around it in Agent Hive. Re-delegate with concrete feedback.
- If a risk is accepted instead of fixed, record it under residual risks with the reason.

## Completion

Finish only when all completion gates pass: every `Execution Plan` phase is `Done`, `Accepted`, or `Not Applicable`; no `Activity Queue` item remains `Pending`, `In Progress`, `Retry Required`, or unresolved `Blocked`; verification gates have passed; validation evidence is recorded; and residual risks are documented. Final reporting should summarize:

- Goal outcome
- Phases completed
- Verifications run and results
- Files or artifacts changed
- Residual risks or follow-up work

If goal tools are available, mark the goal complete only after the objective is genuinely achieved. Never call `update_goal(status=complete)` while any required `Execution Plan` phase is unfinished or any `Activity Queue` item still requires action.

## Final Response

Report the synthesized outcome, not a transcript of agent activity. Mention decomposition only when it helps explain verification, risk, deferred work, or remaining blockers.

Before final response:

- Update `Final Accounting` in the progress file with start time, finish time, total duration, token usage, and the source of the usage number.
- If goal status or usage tools are available, inspect them before finalizing and use their elapsed-time/token values.
- If token usage is not available from tools or the runtime, do not estimate it. Report it as unavailable.
- If marking a goal complete returns usage data, include that exact usage in the final response.
- Format numeric token counts with `.` as the thousands separator, for example `877.647`, not `877647`.

When relevant, include changed files, validation performed, completed activities, deferred post-run analysis items, unresolved risks, blockers, next actions, and the progress file path used for the run. Do not claim success if validation failed or was not run.

End the final response with this accounting line, adjusted to the real status:

```text
Objetivo Agent Hive concluído em ~{duration}; uso registrado: {token_count_with_dot_thousands_or_unavailable} tokens.
```

## Reference

Read `references/agent-hive-pattern.md` when you need the rationale behind the orchestration pattern or need to tune verifier strictness and delegation boundaries.
