---
name: engineering-evidence
description: Use when implementing a behavioral change, investigating a failure, recovering work, or reporting verification results.
---

# Engineering evidence

Preserve Superpowers' test-first loop, root-cause investigation and evidence-before-claims for the current task and candidate.

## Implement and debug

Derive expected behavior from the requirement or contract. Add a regression/acceptance test, observe its intended failure, implement the smallest change, observe it pass, then refactor with checks green. A missing dependency or syntax error is not the intended failing assertion. Do not delete inherited code to manufacture a test-first history; record its baseline and demonstrate that the regression detects the defect.

Tests exercise real behavior. Independently derive expected values; never compute both sides with the implementation under test or merely search source text. Mocks isolate unavailable/expensive boundaries and follow the contract; they cannot prove real integration. Pure prose/static configuration needs proportionate inspection, not meaningless unit tests. Evaluate behavior-shaping skills with consuming agents.

For failures: reproduce and read errors; inspect changes and trace failing boundaries; compare working cases; state one hypothesis; run a distinguishing experiment. Fix the evidenced cause and verify its regression. Redact credentials/personal data. After two unsuccessful rounds, a lead escalates the record to Planner rather than stacking guesses.

## Verify and recover

Run task checks and relevant project suite/build/type/integration gates before claiming success. Read output and exit status, including skipped tests and pre-existing failures. If a required check is unavailable, record NOT_RUN and its blocker; do not infer a result from another passing check.

Use the [evidence record](templates/evidence.md): command, environment, exact candidate, result and retrievable artifacts. Reuse evidence only after verifying tree and relevant environment are unchanged; otherwise rerun affected checks. A child's success message is a lead to inspect, not proof.

On restart, reconcile records, revisions, actual changes, live runs and unfinished findings. Preserve unrelated changes. Reconstruct missing identity/evidence and resume from the last verified gate. Record PASS, FAIL, SKIPPED or NOT_RUN per check; omissions cannot become success.
