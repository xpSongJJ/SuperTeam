---
name: independent-review
description: Use when an implementation or design needs acceptance, or review feedback needs resolution.
---

# Independent review

Author is not Reviewer, including Planner or the strongest model. The coordinator dispatches an independent context with appropriate capability. Self-check prepares the artifact; it cannot approve it.

1. Freeze an identifiable candidate. Provide the requirement, accepted contract, task scope, baseline-to-candidate diff, surrounding code and evidence. Use the actual baseline, not HEAD~1 for multi-commit work. For designs, provide their revision and source constraints.
2. Reviewer reads the artifact directly and gives two verdicts: specification compliance and quality. Inspect error paths and test adequacy. Findings need location, trigger, consequence and severity. Uncertainty is cannot-verify, not a pass. Use the [review report](templates/review.md).
3. Verify feedback against code/contract. Fix valid blockers and request scoped re-review of the changed candidate. Reject incorrect findings with evidence and a recorded resolution. Do not weaken tests or suppress findings by appealing to Planner's authority.
4. A reviewer editing the candidate becomes an author for that edit; use a different reviewer. Earlier-commit reviews cannot approve later changes. Record when scoped re-review extends approval to a new candidate.
5. After two unsuccessful rounds, leads escalate to Planner. Correctness, authorization, data-loss or acceptance failures remain blockers; an exhausted budget is not approval. Defer only nonblocking findings with owner and rationale.

Without an independent reviewer, keep review pending. No renamed self-review or fictional identity. Final cross-role acceptance requires independent review covering the integrated candidate, including Planner's conflict resolutions and difficult code.
