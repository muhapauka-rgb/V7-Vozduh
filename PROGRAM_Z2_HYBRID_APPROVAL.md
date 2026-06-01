# Program Z2 Hybrid Approval

Date: 2026-06-01

## Verdict

hybrid_approval_implemented=true

## Implementation

Implemented in:

- `admin_core/hybrid_approval.py`
- `tools/v7-hybrid-approval-contract`
- `tests/unit/test_v7_hybrid_approval.py`

## Contract

Hybrid approval supports two paths:

1. Target approval
   - Required for execution-only targets.
   - Required for manual-only or reserved targets.
   - Required for trust class changes.
   - Required for route class changes.
   - Required for budget above `1`.

2. Policy approval
   - Allowed only for budget `1`.
   - Allowed only for one selected move.
   - User must be explicitly allowed.
   - Route class must match policy.
   - Trust class must match policy.
   - Policy class must match policy.
   - Target must not be `HARD_FULL`.
   - Rollback target must match current egress.

## Z2 Packet

Packet:

- `docs/track7/productization/z2-evidence/hybrid-approval-packet.json`

Policy:

- approval mode: `HYBRID`
- budget: `1`
- allowed user: `10.7.0.16`
- route class: `GLOBAL_STABLE`
- target class: `BEST_HEALTHY`
- trust class: `RU_SENSITIVE_EXCLUDED`
- policy class: `AUTOSWITCH_ALLOWED`
- rollback: `10.7.0.16 -> vless`

## Validation Result

- verdict: `ALLOW_HYBRID_BOUNDED_AUTONOMY`
- target approval required: `false`
- runtime mutation performed: `false`
- users moved: `false`

## Safety

- autonomous_budget=1
- scope_expanded=false
- autoswitch_apply_run=false
- routing_changed=false

