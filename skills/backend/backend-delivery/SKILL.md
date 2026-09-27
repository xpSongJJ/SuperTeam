---
name: backend-delivery
description: Use when Backend Lead implements or verifies a bounded API, service, data or migration task against an accepted contract.
---

# Backend delivery

Deliver service behavior and data guarantees, not just happy-path responses. Planner owns uncertain cross-domain algorithms and integration; the lead owns bounded implementation and domain verification.

1. Verify task/contract revision and ownership. Confirm durability, units, validation, errors, authorization and retries. Choose internals within those constraints. Shared schemas or business meaning change through a Planner-owned contract decision.
2. Derive tests from outcomes and failure modes: applicable tenant isolation, malformed inputs, concurrency/idempotency, transaction boundaries and recovery. Use representative storage when a double would hide the relevant defect.
3. Implement the smallest compliant change. Coordinate shared schemas/lockfiles/migration ordering with their owner. For migrations, describe compatibility and ordering and validate forward behavior and the chosen rollback or forward-recovery strategy on test data. Never infer permission for production migrations.
4. Run domain suite, contract and relevant service/database integration checks. Record candidate/environment. Passing happy paths cannot waive observed duplicates or cross-tenant disclosure. Missing required migration/recovery evidence remains a blocker.
5. Diagnose with evidence. Escalate cross-domain uncertainty or two unsuccessful rounds to Planner with reproduction/hypotheses; do not keep workers guessing or change frontend semantics locally.
6. Obtain independent spec and quality review. Deliver candidate, contract revision, checks, schema/migration needs, configuration names and limitations to Planner. Set READY_FOR_INTEGRATION only after domain gates pass; otherwise record blocker and next action. Planner owns the combined candidate and acceptance.
