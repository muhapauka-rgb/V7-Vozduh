# Program Z1.5 Reality Audit

Date: 2026-06-01
Mode: Discovery / Governance / Autonomy Design

## Scope

Analysis only.

No movement, rollback execution, autoswitch apply, policy apply, deploy, systemd change, or runtime mutation was performed.

## Runtime Evidence

Fresh read-only evidence was collected in:

`/private/tmp/v7-program-z1-5`

Files:

- `users.registry`
- `egress.registry`
- `runtime-guard.txt`
- `observability.txt`
- `safety.json`
- `current-runtime-summary.json`
- `drift-history.json`

## Current Runtime Summary

- registry rows: `19`
- enabled users by current egress:
  - `amneziawg-exec-20260528-10-8-1-14`: `10`
  - `awg0`: `3`
  - `awg3`: `3`
  - `vless`: `2`

## Current Safety

- safety-review status: `ok`
- enabled egress: `7`
- active users: `18`
- critical findings: `0`
- warning findings: `0`

## Current Observability

- autoswitch: healthy
- capacity: warm
- users: healthy
- security: healthy
- channels: unstable
- routing: degraded
- services: blocked
- direct routing: unknown
- trusted RU: unknown

## Drift History

Program F2:

- approved/stale target: `awg3`
- fresh target: `awg0`
- candidate: `10.7.0.16`
- raw candidates: `12`
- healthy egress total: `2`

Program Z1:

- approved/stale target: `awg0`
- fresh canonical candidate: `10.7.0.10`
- fresh target: `awg3`
- raw candidates: `15`
- healthy egress total: `1`

## Reality Conclusion

Target drift is not a rare edge case. It is caused by live health, stability, capacity, and candidate ordering changes. Pure target-specific approval is safe because it fails closed, but it is operationally brittle for bounded autonomy.

