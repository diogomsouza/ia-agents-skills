---
name: grill-with-docs
description: Interview mode for stress-testing a plan against the existing domain model, terminology, CONTEXT.md, and ADRs. Ask one question at a time and do not implement code unless explicitly approved after the grilling session.
---

<session-contract>

This skill is an interview and documentation mode, not an implementation mode.

Do not implement production code, change application behavior, add tests, refactor files, or make implementation commits while using this skill unless the user explicitly gives permission after the grilling session.

If the user's request mixes grilling with implementation, start with the grilling session and stop before implementation. Ask for explicit confirmation before making code changes.

Allowed actions before explicit implementation approval:
- inspect the codebase
- read existing documentation
- ask one question at a time
- recommend an answer for each question
- create or update `CONTEXT.md` after the user confirms a resolved term
- create `docs/adr/` and write an ADR after the user confirms an architectural decision that meets the ADR criteria below
- report exactly what was registered before asking the next question

Forbidden actions before explicit implementation approval:
- editing source code
- editing tests
- creating feature files
- changing configuration
- running broad refactors
- making implementation commits

Documentation writes are part of this skill's interview workflow. Creating or updating `CONTEXT.md` and ADR files is allowed and expected during the grilling session when the conditions below are met. These documentation writes do not count as implementation.

</session-contract>

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

Ask exactly one question at a time, waiting for feedback on each question before continuing.

For each question, provide your recommended answer, but do not proceed as if I accepted it until I confirm or correct it.

If a question can be answered by exploring the codebase, explore the codebase instead.

Whenever a term, boundary, invariant, responsibility, or domain relationship is resolved, immediately create or update the relevant `CONTEXT.md` before asking the next question.

Whenever an architectural decision is resolved and it meets the ADR criteria below, immediately create the ADR before asking the next question. If the decision does not meet the ADR criteria, say that no ADR is needed and continue.

After every documentation update, briefly report what was registered and in which file.

When you believe there are no more questions to ask, say that all doubts have been resolved and ask whether you may start implementation now. Do not start implementation until I explicitly confirm.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

</supporting-info>
