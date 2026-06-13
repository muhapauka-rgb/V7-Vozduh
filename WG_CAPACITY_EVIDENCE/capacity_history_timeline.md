# WG Capacity History Timeline

## E11 Canary Era

`wireguard-1779454504-c43409` was held as a clean second canary target.

Evidence:

- `BLOCK_E11_3_BOUNDED_WIREGUARD_RESERVATION_METADATA_MUTATION_REPORT.md`
- `BLOCK_E11_11_POST_CLOSEOUT_GOVERNANCE_REVIEW_AND_PRODUCTION_HARDENING_REPORT.md`
- `BLOCK_E11_18_TWO_USER_MINI_COHORT_PROMOTION_CLEAN_GOVERNANCE_APPROVAL_REPORT.md`

Observed metadata:

```text
soft_limit=1
hard_limit=2
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Meaning:

- one user was safe for canary;
- two users became promotion-clean only under E11 governance;
- larger WireGuard cohort was not approved.

## Dynamic Load Policy

Commit:

```text
152c1ce Add guarded VPN autoswitch dynamic load policy
```

The autoswitch runtime introduced `DEFAULT_LOAD_POLICY` and dynamic load calculation.

Current code path:

- `tools/v7-users-autoswitch::_dynamic_load_summary`
- `tools/v7-users-autoswitch::_load_limits_for_egress`
- `tools/v7-users-autoswitch::_capacity_decision`

Important finding:

`soft_limit` and `hard_limit` from `egress.registry` are not loaded into the `Egress` capacity model. The runtime reads only:

```text
capacity_users
capacity
```

for target-specific capacity overrides.

## E30/E32 Capacity Program

Later capacity certification work formalized capacity as evidence-bound.

Evidence:

- `BLOCK_E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION_REPORT.md`
- `BLOCK_E32_1_1_CAPACITY_CLASS_MODEL_REPORT.md`
- `BLOCK_E32_1_2_CAPACITY_METADATA_MODEL_REPORT.md`
- `docs/track7/productization/e32_2_c-evidence/capacity-program-compatibility.md`

Important distinction:

E30/E32 certified `amneziawg-exec-20260528-10-8-1-14`, not `wireguard-1779454504-c43409`.

Therefore WireGuard has:

- good current health;
- dynamic planner capacity projection;
- historical two-user canary evidence;
- no fresh formal capacity-class certification above two users.

