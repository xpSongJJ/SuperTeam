---
name: solving-hard-problems
description: Use when Planner owns a cross-domain uncertainty, difficult algorithm, or escalation after repeated unsuccessful attempts.
---

# Solving hard problems

Planner owns investigation and, when necessary, critical implementation. Returning an unchanged vague task to a lead is not escalation handling.

1. Read the escalation: observed/expected behavior, contract/candidate revisions, reproduction, hypotheses, evidence and question. Preserve useful work and continue independent tasks.
2. State the invariant and uncertainty; trace relevant boundaries. For transaction ordering, enumerate retries, lost responses, competing requests and crash/recovery states before choosing a fix.
3. Compare explanations/designs and perform a bounded distinguishing experiment. Use research or architecture-challenge children when helpful, retaining ownership of the conclusion. Record disconfirmed hypotheses and stop conditions.
4. Produce an evidenced cause, concrete algorithm/design, executable regression or probe, and migration/compatibility consequences where relevant. When the hard kernel still requires substantial judgment, implement it as Planner with test-first verification; do not return only prose and leave the same unresolved difficulty to leads.
5. Obtain independent review of Planner-authored design/code from a capable reviewer. Convert remaining work into bounded lead tasks with exact contracts and examples. Record decisions and remaining risks.

If a probe cannot decide within budget, state the uncertainty and consequence. Planner may change approach or record a new bounded budget. Changes to explicit human requirements or actions outside authorization return to your human partner.

**Example:** Duplicate checkout after a lost response requires request identity, atomic persistence and replay semantics together. A longer frontend timeout cannot establish exactly-once business effects.
