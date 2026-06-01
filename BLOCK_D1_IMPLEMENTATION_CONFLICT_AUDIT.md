# Block D1 Implementation Conflict Audit

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Inspected

- `v7-users-autoswitch`
- `v7-autoswitch-safety-review`
- `v7-second-canary-target-readiness`
- `v7-route-movement-preview`
- `v7-operator-execution-packet`
- `admin_core/operator_execution.py`
- `admin_core/operator_observability.py`
- autoswitch systemd units
- autoswitch policy files

## Existing Logic

Existing logic already covers:

- Shadow autoswitch planning
- Optional apply switch
- Anti-flap state
- Restore barrier state
- Read-only safety review
- Operator packet validation
- Replay rejection
- Runtime hash recheck
- Movement preview
- Execution-target readiness

## Conflict Decision

Do not create parallel systems.

The correct remediation path is to extend or fix existing components:

- Fix `v7-autoswitch-safety-review` parser to read KV registry format.
- Add packet-oriented cap/filtering around `v7-users-autoswitch` recommendations.
- Reuse `v7-operator-execution-packet` for approval and replay checks.
- Reuse readiness and movement preview tools.

## Verdict

No duplicate implementation is needed.

