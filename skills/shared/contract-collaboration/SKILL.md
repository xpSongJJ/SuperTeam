---
name: contract-collaboration
description: Use when a task consumes or changes a shared interface, data meaning, or cross-role acceptance condition.
---

# Contract collaboration

Make producer and consumer agree on observable behavior before dependent implementation. Planner owns the decision record; both leads supply feasibility and impact evidence. An implementation already written does not redefine the contract.

1. Read the accepted revision and related business requirement. Identify producer, consumers and affected tasks. Distinguish confirmed requirements from assumptions.
2. Specify relevant boundaries: request/response schemas, units and nullability, success meaning and durability, errors, authorization, retry/idempotency, pagination or events. Include valid/invalid examples and observable acceptance cases. API schema alone cannot settle business semantics.
3. Resolve open technical choices with Planner and affected leads. Planner chooses within approved intent; only a material unresolved user requirement goes back to your human partner.
4. Record a revision and producer/consumer acknowledgments. Dependent tasks reference that exact revision. Independent work can continue. Mocks and generated clients use the same accepted contract.
5. For a change, record reason, compatibility, affected implementation/tests/mocks/migrations and rollout order. Planner decides; both leads acknowledge impact. Update the revision and task records together before resuming affected work. Superseded tests and reviews cannot establish current acceptance.

Deliver or update the [contract record](templates/contract.md). Link unchanged accepted records instead of duplicating them.

**Example:** A success response meaning “queued” does not satisfy checkout requiring a persisted order, even when both contain an ID. Resolve durability and UI behavior explicitly.

**Common mistake:** Silently changing integer cents to floating dollars because backend code exists. Preserve the accepted contract or use a versioned change; sunk cost is not approval.
