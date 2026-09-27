---
name: delegating-work
description: Use when a top-level role assigns a bounded task to a temporary worker or coordinates parallel work.
---

# Delegating work

Delegate an independently checkable deliverable. Top-level roles remain accountable; workers have one task, a bounded lifetime and no children.

1. Read durable task records and reconcile live workers before dispatch. Do not repeat completed tasks after context loss. A pending run ID is not a result.
2. Write the [worker brief](templates/worker-brief.md): task/contract revisions, relevant inputs, deliverable, allowed paths, baseline, workspace, checks, output record, budget and escalation trigger. Give relevant context, not parent conversation history. Investigate unknown paths before assignment.
3. Reserve a slot under Planner's feature-wide allocation (defaults: four active children globally, two per role). Without atomic reservation, Planner serializes grants. Workers cannot spawn grandchildren, including reviewers; their top-level parent handles review. Slot exhaustion queues work instead of silently raising the cap.
4. Parallelize only dependency-independent work in isolated workspaces with disjoint ownership. Shared-checkout writers run serially. Give lockfiles, shared schemas and migration ordering one owner. Record source/target branches; do not guess the integration base.
5. Child returns artifact/commit, changed paths, actual checks/results, uncertainties and next action. Inspect real changes, then request independent review. Children cannot close the feature. Release the slot and preserve the report when a child ends.
6. After two unsuccessful repair/review rounds, stop repeating the attempt. A lead escalates hypotheses and evidence to Planner. Planner changes approach, decomposes or owns the difficult part. Recorded budget changes do not waive review or acceptance.

Without child-agent capability, implement inline and label the fallback. Route review to a separate agent, or leave IN_REVIEW/BLOCKED. Never fabricate parallel work or reviewer identities.

After interruption, check whether the prior child is still running and its commit already exists before retrying. Lead consolidation covers its own workers only; Planner owns cross-role integration.
