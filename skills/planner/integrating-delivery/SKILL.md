---
name: integrating-delivery
description: Use when Planner receives reviewed domain handoffs or a cross-role integration failure.
---

# Integrating delivery

Planner owns the combined result: merge order, conflicts, real-system validation and business acceptance. Lead completion is readiness for integration.

1. Verify handoff contracts, dependencies, base/head commits, actual artifacts, domain evidence and independent review coverage. A ready message without evidence is not a gate. Identify the intended integration branch/workspace.
2. Freeze inputs. Integrate in dependency order in Planner's workspace, preserving source branches and unrelated work. Leads consolidate their own workers; Planner owns cross-role integration. Resolve semantic conflicts against the contract with both leads. Contract changes reopen affected tasks, clients/mocks and evidence.
3. Record the candidate and run relevant suite/build checks and real frontend-to-backend acceptance flows, including failures/retries/authentication/persistence where required. Frontend mocks plus backend unit tests do not prove real integration. Validate required migrations/recovery in a safe test environment.
4. Route local defects to leads; retain cross-boundary diagnosis and difficult fixes. Each integrated edit changes the candidate and invalidates affected evidence/review. Pre-merge tests cannot establish a changed merged result.
5. Obtain independent review covering the combined candidate, especially conflict resolutions and Planner-authored code. Reuse valid domain evidence without implying it covers new integration behavior. Unresolved correctness and acceptance failures block acceptance.
6. Produce the [integration record](templates/integration.md) mapping every acceptance case to evidence, component/integration revisions, review coverage and remaining risks. Set ACCEPTED only when required gates pass; otherwise INTEGRATING or BLOCKED with owner and next action.

Acceptance is a verified local delivery state, not permission to deploy, publish, push or delete workspaces. Apply existing authorization separately. Preserve handoff and review records for recovery.
