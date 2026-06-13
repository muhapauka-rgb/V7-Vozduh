# WG.CAPACITY.1 - WireGuard Capacity Limit Ownership And Production Promotion Review

## 1. Capacity History

Channel:

```text
wireguard-1779454504-c43409
```

Historical canary-era metadata:

```text
soft_limit=1
hard_limit=2
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Evidence:

- `BLOCK_E11_11_POST_CLOSEOUT_GOVERNANCE_REVIEW_AND_PRODUCTION_HARDENING_REPORT.md`
- `BLOCK_E11_18_TWO_USER_MINI_COHORT_PROMOTION_CLEAN_GOVERNANCE_APPROVAL_REPORT.md`
- `WG_CANARY_ROOT_CAUSE_REPORT.md`
- `WG_CAPACITY_EVIDENCE/capacity_history_timeline.md`

Meaning at E11 time:

- one-user WireGuard canary was acceptable;
- two-user WireGuard mini-cohort became promotion-clean only under bounded governance;
- three-user WireGuard movement was explicitly not approved;
- the channel stayed `canary_reserved=true`.

Current production registry still carries `soft_limit=1 hard_limit=2`, but current planner code does not consume those registry fields as runtime capacity authority.

## 2. Capacity Owner Audit

Runtime planner capacity owner:

```text
tools/v7-users-autoswitch
```

Relevant runtime owners:

- `DEFAULT_LOAD_POLICY`
- `_dynamic_load_summary`
- `_load_limits_for_egress`
- `_capacity_decision`
- `_pick_moves_with_projected_load`

Current runtime load policy:

```text
mode=dynamic
reserve_ratio=0.15
soft_multiplier=1.15
hard_multiplier=1.45
failover_hard_multiplier=2.0
min_soft_limit=5
min_hard_limit=10
max_hard_limit=80
```

Target-specific runtime override owner:

```text
capacity_users
```

or legacy:

```text
capacity
```

Current WireGuard row does not define either override:

```text
capacity_users=absent
capacity=absent
```

Therefore current planner capacity is dynamic, not `1/2`.

Governance capacity owner:

```text
E32 capacity metadata/certification model
```

Governance rule:

```text
capacity_is_gate_not_authority=true
```

Forward movement above historical proof requires fresh certified capacity metadata.

Evidence:

- `WG_CAPACITY_EVIDENCE/capacity_owner_audit.md`
- `BLOCK_E32_1_1_CAPACITY_CLASS_MODEL_REPORT.md`
- `BLOCK_E32_1_2_CAPACITY_METADATA_MODEL_REPORT.md`
- `docs/track7/productization/e32_2_c-evidence/capacity-program-compatibility.md`

## 3. Conflict Analysis

Observed conflict:

| Source | Value |
| --- | --- |
| historical governance / registry metadata | `soft_limit=1 hard_limit=2` |
| current planner projection | `soft_limit=30 hard_limit=38` |

Why they differ:

`1/2` came from the E11 canary governance phase.

`30/38` is calculated by dynamic load policy:

```text
active_users=26
working_channels=1
avg_load=26.0
soft_limit=ceil(26.0 * 1.15)=30
hard_limit=ceil(26.0 * 1.45)=38
```

Current copied production load summary confirms:

```json
{
  "active_users": 26,
  "healthy_channels": 1,
  "working_channels": 1,
  "avg_load": 26.0,
  "soft_limit": 30,
  "hard_limit": 38,
  "failover_hard_limit": 52,
  "wireguard": {
    "users": 0,
    "soft_limit": 30,
    "hard_limit": 38,
    "capacity_users": 0,
    "status": "OK"
  }
}
```

Conclusion:

The conflict is not two equal truth sources disagreeing. It is a stale/historical canary metadata field being compared to the current dynamic load owner.

## 4. Capacity Reality

Current WireGuard health:

| Field | Value |
| --- | --- |
| service score | `100.0` |
| Telegram | `OK` |
| avg Mbps | `55.03` |
| min Mbps | `51.35` |
| stability | `0.933` |
| 1h stability | `0.9366` |
| current users | `0` |
| runtime capacity status | `OK` |
| required service missing | none |
| required service low | none |

Reality verdict:

WireGuard is healthy enough to be considered for production pool participation.

But capacity reality has two separate levels:

1. Runtime planner capacity: dynamic model says the channel can absorb load under current projection.
2. Governance certified capacity: evidence above two users is not freshly certified for this specific WireGuard channel.

Therefore actual safe capacity is not proven as `1/2`, but full normal production capacity is also not proven.

## 5. Counterfactual Review

Counterfactual performed only on copied local evidence:

```text
canary_reserved=true -> removed only in WG_CANARY_EVIDENCE/counterfactual_state/egress.registry
```

No runtime state was changed.

Result:

```text
healthy_egress_total: 1 -> 2
candidate_moves_total: 3 -> 26
selected_moves: 1 -> 1
```

Counterfactual WireGuard candidate:

```text
eligible=true
blocked=[]
best_available_pool=true
pool_rank=1
score=2234.66
```

Answer:

If canary flag is removed, planner assumes dynamic capacity and treats WireGuard as a strong production target. That would exceed old E11 assumptions and would make full unbounded promotion too wide without fresh capacity certification.

Evidence:

- `WG_CAPACITY_EVIDENCE/current_capacity_snapshot.json`
- `WG_CANARY_EVIDENCE/analysis/planner_impact_summary.json`

## 6. Promotion Readiness

Can WireGuard safely become a normal production channel?

Answer:

```text
not yet as FULL_PROMOTION
```

Can WireGuard safely move toward production pool?

Answer:

```text
yes, as LIMITED_PROMOTION
```

Required capacity model for promotion:

```text
capacity_mode=limited_production
runtime_capacity_source=dynamic_load_policy
governance_capacity_gate=fresh_capacity_certification
initial_effective_cap=2 or explicitly approved fresh capacity cap
```

The old `1/2` limit should not remain the permanent truth source, but it should not be replaced by implicit `30/38` full promotion. It should be retired only through a bounded promotion/capacity certification step.

## 7. Governance Verdict

Classification:

```text
LIMITED_PROMOTION
```

Why not `KEEP_CANARY`:

- channel is healthy;
- current production pool is narrow;
- canary purpose has been served;
- keeping a healthy channel permanently reserved harms pool resilience.

Why not `FULL_PROMOTION`:

- removing reservation makes WireGuard a strong best-pool target for many users;
- no fresh capacity-class certification above two users exists for this specific channel;
- old registry metadata and current dynamic model still need governance reconciliation.

## 8. Promotion Plan

No implementation performed.

Recommended next program:

```text
WG_CAPACITY_LIMITED_PRODUCTION_CERTIFICATION_AND_CANARY_DERESERVATION_PREP
```

Exact plan:

1. Keep production unchanged.
2. Create a fresh WireGuard limited-production capacity packet.
3. Revalidate current health, Telegram, service matrix, speed, and stability.
4. Set or bind explicit capacity metadata for first production phase:
   - either `capacity_users=2`;
   - or E32-style `capacity_class=CLASS_2`, `capacity_status=CERTIFIED`, `effective_batch_cap=2`.
5. Run planner dry-run with `canary_reserved=false` in copied state and explicit cap.
6. Verify:
   - WireGuard eligible;
   - healthy pool at least 2;
   - target users do not exceed cap;
   - no target substitution;
   - no governance bypass;
   - no restore-barrier bypass.
7. Only after dry-run certification, prepare the actual canary dereservation patch.
8. Deploy only through approved safe deploy.
9. Observe limited production.
10. Consider capacity expansion after evidence, not before.

## 9. Final Verdict

Final answer to the success question:

The `soft_limit=1 hard_limit=2` limit is a historical canary-era governance artifact as a runtime planner limit. It is not the current autoswitch capacity authority.

However, it still represents the last explicit WireGuard-specific movement certification. So it can be retired as the permanent capacity truth only if replaced by fresh capacity metadata/certification. It should not be silently replaced by implicit full dynamic capacity.

Final verdict:

```text
capacity_history_understood=true
capacity_owner_identified=true
capacity_conflict_explained=true
wireguard_runtime_capacity_source=dynamic_load_policy
wireguard_registry_1_2_runtime_authoritative=false
wireguard_1_2_historical_canary_artifact=true
wireguard_capacity_above_2_freshly_certified=false
production_capable=true
full_promotion_safe=false
limited_promotion_safe_to_prepare=true
governance_verdict=LIMITED_PROMOTION
runtime_changed=false
policy_changed=false
canary_removed=false
users_moved=0
autoswitch_apply_run=false
SAFE_NEXT_STEP=WG_CAPACITY_LIMITED_PRODUCTION_CERTIFICATION_AND_CANARY_DERESERVATION_PREP
```

