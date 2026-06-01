# Program Z3.1 Safe Remediation

Date: 2026-06-01

## Verdict

safe_remediation_possible=true

## Remediation Chosen

Z3.1 refreshed restore barrier clearance for exactly:

- user: `10.7.0.16`
- target: `awg3`
- budget: `1`
- expected selected moves: `1`

## Why This Is Safe

- It uses the existing planner barrier model.
- It is generation-bound.
- It is selected-hash-bound.
- It is selected-count-bound.
- It expires quickly.
- It does not call movement authority.
- It keeps unfiltered planner blocked.

## Runtime Mutation

Governance-only mutation performed:

- wrote `/opt/v7/egress/state/autoswitch-restore-barrier.json`

Backups:

- `/opt/v7/egress/state/z3_1-backups/autoswitch-restore-barrier.20260601T174520Z.json`
- `/opt/v7/egress/state/z3_1-backups/autoswitch-restore-barrier.refresh.20260601T174715Z.json`

## Not Performed

- no `v7-users-autoswitch --apply`
- no `v7-user-switch`
- no systemd change
- no deploy

