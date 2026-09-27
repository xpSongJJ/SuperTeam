---
name: frontend-delivery
description: Use when Frontend Lead implements or verifies a bounded UI task against an accepted design and contract.
---

# Frontend delivery

Deliver interaction and frontend behavior matching the accepted flow. Component tests and a polished mock are intermediate evidence.

1. Verify task/contract revision, data meaning, success/errors, session behavior and write ownership. Map applicable loading, empty, success, validation, failure and retry states. Choose visual/component details within the brief; escalate material UX or business changes to Planner.
2. Plan independently testable components and API boundaries. Use accessible semantics, keyboard operation and responsive behavior. Fixtures follow the accepted contract revision.
3. Implement with behavioral tests: visible outcomes, focus/input behavior, error recovery and relevant request races. Do not merely check that a mocked component mounted. Use children for substantial independent work and a different reviewer for acceptance.
4. Run component/type/build and browser interaction checks. Exercise the real API when available. Record actual viewport/input/environment observations for visual/accessibility claims. Unavailable browser/backend means explicitly unverified cases and a Planner dependency; a mock preview is not feature completion.
5. Fix frontend failures; provide reproduction for cross-domain faults. After two unsuccessful rounds or when shared semantics must change, escalate evidence to Planner.
6. Obtain independent spec and quality review. Hand off candidate/contract revision, evidence, environment needs and limitations. Use READY_FOR_INTEGRATION only after domain requirements pass. Known keyboard failures block domain delivery even with green component tests. Planner owns combined acceptance.

Do not silently normalize a backend contract violation to hide it. Report observed response and expected contract so Planner can choose the compatible correction.
