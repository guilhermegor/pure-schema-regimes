# Ledger — #23 ruleset-no-strict

Branch: `fix/23-ruleset-no-strict` · Issue: #23 · Class: **ci**

## Goal

Port guilhermegor/blueprintx#1284 (issue #1283): `bin/enable_repo_rules.sh` creates the
`pr-quality-gate` ruleset with `strict_required_status_checks_policy=false`, and its verify
paths require strict to be off.

## Work

- [x] Create the ruleset with strict=false
- [x] Make the ruleset and classic-branch-protection verifies require strict=false
- [x] Update the failure and success messages to match
