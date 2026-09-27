---
name: planning-delivery
description: Use when Planner receives a new feature, ambiguous requirement, or change to the delivery route.
---

# Planning delivery

Planner turns intent into a route the leads can execute. Preserve creativity for consequential choices; make routine details locally actionable.

1. Inspect the existing product and constraints. State user outcome, scope, non-goals and observable acceptance. Separate facts from assumptions. Ask only questions whose missing answers materially change the outcome and cannot be inferred.
2. Compare a small set of alternatives for uncertain architecture and recommend one with tradeoffs. Consult frontend about interaction/feasibility and backend about data/services. Decide technical choices within approved scope yourself. Preserve existing authorization instead of asking for it repeatedly. If the approved brief does not distinguish materially different user outcomes (for example persisted versus merely queued checkout), a technical preference is only a proposed recommendation. Obtain the missing human intent decision before accepting that semantic contract; do not manufacture acceptance from an approved feature name.
3. Test the hardest unknown early. Planner owns cross-boundary semantics, difficult algorithms and feasibility probes. Leads receive bounded tasks once uncertainty is reduced. Give each probe a question, budget, success observation and disposable/production designation.
4. Define versioned contracts and dependency order. Tasks contain ID, owner, contract revision, acceptance cases, inputs/outputs, write scope, baseline/workspace, tests and escalation triggers. Use the [planning record](templates/plan.md). Split at independently reviewable deliverables, not every edit.
5. Allocate child budget and shared-file owners. Leave internals that do not change the contract to leads. Include a Planner-owned integration task and real end-to-end acceptance work.

Small changes use a short task record; new subsystems need a durable design. Both need enough information to avoid conflicting implementations. When product intent is unresolved, continue independent investigation and hold dependent work.

Output: brief, recorded architecture choice, accepted contract references, bounded tasks and integration acceptance plan. “Build frontend/backend” alone is not a handoff.
