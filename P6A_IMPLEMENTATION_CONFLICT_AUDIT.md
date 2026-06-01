# P6.A Implementation Conflict Audit

Project: V7 Vozduh

Block: P6.A

## Inspected

Inspected:

- autoswitch
- rebalance
- routing selection
- candidate selection
- operator execution
- runtime action packet
- rollback preview
- verification

## Conflict Findings

Equivalent logic exists for most movement-design primitives:

- selection and safety scoring: `tools/v7-users-autoswitch`
- read-only movement preview: `tools/v7-route-movement-preview`
- target/candidate readiness: `tools/v7-second-canary-target-readiness`
- zero-move packet and replay primitives: `admin_core/operator_execution.py`
- bounded historical approval packets: `docs/track7/productization/e24-evidence/first-bounded-user-movement-approval-packet.json`, `e27_2-evidence/fresh-approval-packet.json`, `e28_2-evidence/fresh-approval-packet.json`
- verification artifacts: `v7-user-route-check`, `v7-killswitch-check`, `v7-provisioning-reconcile-check`

## Design Decision

P6.A defines a design that reuses these concepts.

No new movement engine, runtime hook, systemd unit, autoswitch apply path, routing apply path, or packet system is introduced.

The future P6.B certification should consume the existing preview/readiness/checker path and produce a fresh single-user movement packet. It must not bypass `v7-route-movement-preview`, `v7-second-canary-target-readiness`, or execution-time recheck.

## Do Not Duplicate

Do not duplicate:

- `v7-user-switch`
- autoswitch candidate scoring
- route movement preview
- target readiness checker
- replay/audit chain concepts
- rollback preview and verification checkers

## Verdict

- implementation_conflict_audit_complete=true
- equivalent_movement_logic_exists=true
- reuse_required=true
- duplicate_movement_logic_created=false
- execution_engine_implemented=false
- runtime_hooks_with_authority=false
