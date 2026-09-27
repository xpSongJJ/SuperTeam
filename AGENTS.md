# SuperTeam contributor instructions

This is a user-authorized team-specific derivative of Superpowers. Planner owns direction, difficult work and cross-role integration. Frontend and Backend Leads own bounded execution and domain tests. Read README.md, team.json, agents/common.md and the relevant skill before changing behavior.

Preserve the original MIT license and attribution. Do not submit this fork-specific redesign to the upstream project. No automatic publishing, deployment or upstream PR is implied by local development. Preserve unrelated human changes.

## Skill maintenance

Skills shape behavior. Keep role responsibility in agents/ and reusable workflows in skills/. Maintain shared content once and package it for all bound roles. Every skill must be self-contained with its referenced resources. Do not make the runtime depend on this repository's other directories being present.

For behavior changes use the writing-skills methodology: define realistic pressure scenarios, run a no-new-guidance baseline, inspect actual responses, change the relevant guidance, rerun in fresh contexts and record outcomes/limitations. Use independent agents for forward evaluation and review when available. The upstream authoring method is available in Git history at the baseline recorded in docs/migration.md. Static validators cannot establish agent compliance. Never fabricate evals, transcripts, model information or test results.

Keep descriptions specific to triggers. Avoid unnecessary universal rules and repeated instructions. An explicit user constraint takes precedence over inherited skill conventions. Run the bundled skill-creator validator when available, plus the repository checks below.

## Verification

- python scripts/team.py check
- python -m unittest discover -s tests -v
- python scripts/team.py build --out <new-output-directory>
- git diff --check

For changes to behavior, also run the relevant evals described in evals/README.md. Retain raw scenario responses and record model/harness/settings. Do not claim a Multica integration is validated without a real session there. Model/CLI evaluations are optional authoring tools, not runtime dependencies.

For code changes add meaningful tests of observable behavior, not exact prose, headings or implementation text. Keep packaging zero-dependency and portable across Python 3.10+ environments. Report which checks actually ran and any unavailable environments.
