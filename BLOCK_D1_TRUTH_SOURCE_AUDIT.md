# Block D1 Truth Source Audit

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Planner

Canonical source:

- `v7-users-autoswitch` shadow JSON

Derived sources:

- users registry
- egress registry
- policy
- org policy
- service matrix
- quality summary
- safety state

## Safety Review

Canonical source:

- `v7-autoswitch-safety-review`

Problem:

- It currently parses registry rows as two-column rows and treats token two as `value`.
- Current registry is KV format, so token two is usually `protocol=...`, not `enabled=...`.

## Capacity

Canonical source:

- `egress.registry` for per-target hard guardrails
- `/etc/v7/policy.json` for dynamic autoswitch load policy

Conflict:

- Dynamic autoswitch load reported broad capacity as OK.
- Governance execution target is still hard-limited at `10` by registry.

## Execution Targets

Canonical source:

- `egress.registry`

Current result:

- One execution-only target exists.
- No second execution-only target exists.

## Trust

Canonical source:

- trusted RU decision/diagnostic state files

Current status:

- `overall=NEEDS_ATTENTION`
- trusted route class still needs a trusted path.

## Health

Canonical source:

- runtime checker outputs

Presentation source:

- reports and admin API

Admin API is unavailable and cannot be treated as authoritative health while down.

## Verdict

Truth sources are known. The main mismatch is safety-review parsing, not runtime registry truth.

