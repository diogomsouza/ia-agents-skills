# Agent Hive Pattern

Use this reference when applying the `agent-hive` skill to longer tasks.

## Core idea

Separate control from execution. Agent Hive owns intent, context, sequencing, progress tracking, and stop conditions. Subagents perform bounded work. Separate verifier subagents decide whether a result is good enough for downstream steps.

## Principles from the source article

- Delegate, do not execute. Agent Hive should coordinate and report rather than silently doing the work. If subagent tooling is unavailable, report the blocker instead of continuing as a single-agent executor.
- Use specialists first. Prefer a domain-specific agent, skill, plugin, or verifier over a generic worker.
- Explore before action. Delegate exploration to an explorer or specialist before implementation when the codebase, data source, or problem surface is unclear.
- Require explicit verification. A phase does not complete because it looks plausible; it completes when a verifier accepts it against stated criteria.
- Keep stop conditions concrete. Every phase needs a definition of done that can be checked.
- Contain errors early. Verification gates prevent weak assumptions and incorrect outputs from contaminating later phases.
- Match verifier strictness to risk. Pragmatic verification is acceptable for decision-support analysis; production code, compliance, security, migrations, and data integrity require stricter checks.
- Optimize for throughput. Orchestration should reduce wall-clock time when work is independent; if it only serializes execution plus verification, the plan is too granular.

## Role boundaries

### Agent Hive

- Create or maintain the goal.
- Decompose work into phases.
- Choose specialists.
- Assign bounded tasks.
- Maintain `.agent-hive/PLAN-PROGRESS-{context-id}.md`.
- Decide whether to ask the user, retry, proceed, or stop.
- Integrate returned outputs and update status.
- Avoid doing execution or verification work locally unless the user explicitly approves a non-orchestrated fallback.

### Execution subagent

- Work only inside the assigned scope.
- Produce an inspectable artifact or concrete result.
- State assumptions, commands run, files touched, and any blockers.
- Stop at the requested boundary instead of expanding scope.

### Verifier

Answer this question:

> Is this result correct enough to support the decisions or steps that depend on it next?

The verifier must be separate from the execution subagent for the phase being checked. It should ignore polish unless polish is part of downstream correctness. If the result is not acceptable, it must provide specific correction guidance.

## Required subagent sequence

1. Discover available subagent tools and specialist capabilities.
2. Decompose work into independent batches with disjoint ownership.
3. Spawn or assign execution subagents for the current independent batch.
4. Wait for or collect execution results when needed for the next gate.
5. Spawn or assign separate verifier subagents with executor outputs and criteria.
6. Batch related verification when risk allows.
7. Proceed only after verifier acceptance.
8. If rejected, re-delegate execution with verifier feedback.

## Throughput guidance

Use orchestration where it buys either parallelism or correctness. If neither is happening, reduce overhead.

- Good batch boundaries: package, module, route area, feature folder, library, migration category, or test suite.
- Bad batch boundaries: one file at a time for repetitive edits, one tiny spawn per obvious change, or one verifier per trivial mechanical edit.
- For code migrations, run a strict verifier on the first representative slice, then use batch or sampled verification for repeated low-risk slices.
- Use strict verification on shared infrastructure, dependency updates, build configuration, data migrations, security-sensitive changes, and public APIs.
- Cap retries. After one failed retry, either change decomposition, tighten the prompt, or ask the user for a decision.
- Track runtime in the progress file. If orchestration exceeds the simple baseline by a large margin, increase batch size or reduce verification granularity.

## Waiting guidance

Wait for subagents when their result is needed for the next gate.

- Use the longest available wait window and repeat waits when a tool timeout returns no final status.
- Do not interrupt, shrink scope, or ask for status only because the subagent is slow.
- Treat long installs, builds, migrations, dependency resolution, and test suites as normal execution.
- Ask for status only when there is concrete evidence of a blocker, loop, or external input requirement.
- Do not end an activity with required subagents still running unless the platform prevents continued waiting.

## Final reporting

Final responses should synthesize the outcome instead of replaying agent activity. Include decomposition only when it explains validation, risk, deferred work, or blockers.

Include changed files, validation performed, completed activities, unresolved risks, blockers, next actions, and the progress file path when relevant. End with elapsed time and token usage when available. Format numeric token counts with `.` as the thousands separator, for example `877.647`, not `877647`:

```text
Objetivo Agent Hive concluído em ~{duration}; uso registrado: {token_count_with_dot_thousands_or_unavailable} tokens.
```

Do not invent token usage. If no goal/runtime usage data is available, say that usage is unavailable.

## Useful verifier prompts

Pragmatic verification:

```text
Verify the attached result for this phase. Answer only whether it is correct enough for the next dependent step, what evidence supports that answer, and what must change if it is not acceptable.
```

Production-code verification:

```text
Review this implementation against the stated completion criteria. Check correctness, regressions, missing tests, and validation evidence. Say whether it is safe to proceed, and list required fixes if not.
```

Research/report verification:

```text
Check whether this analysis supports the downstream decision. Focus on factual accuracy, assumptions, source quality, gaps, and whether the conclusion follows from the evidence.
```
