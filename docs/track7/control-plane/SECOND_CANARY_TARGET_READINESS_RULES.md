# Second Canary Target Readiness Rules

Mode: read-only watcher design. These rules decide whether E9.3 can be considered. They do not authorize canary execution.

## Scope

The candidate is fixed for this watcher:

```text
candidate_user=10.7.0.14
expected_current_egress=vless
rollback_target=vless
strategy=different_user_same_mechanics
```

The watcher only selects a target. It must not run `v7-user-switch`, `v7-routing-sync`, `v7-users-autoswitch --apply`, policy apply, Direct/RU mutation, Trusted RU refresh, proxy apply, kill-switch mutation, route mutation, registry mutation, deploy, or systemd changes.

## GO Target Rules

A target is `GO` only when all of these are true:

| Rule | Required Value | Reason |
|---|---|---|
| enabled | `enabled=1` | disabled egress cannot be a canary target |
| registry users | `0` enabled users assigned | canary must remain a clean one-user proof |
| load-state users | `0` | load-state must agree target is empty |
| interface state | `UP,LOWER_UP` | route table preview must have a live interface |
| diagnose | `OK` | SUSPECT/FAIL means target health is not clean |
| manual_only | false | manual-only channels need separate approval |
| reserve_only | false | reserve-only channels should not be used for generic mechanics proof |
| route classes | excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU` | second canary must not test Direct/RU or Trusted RU behavior |
| average throughput | `>= 15 Mbps` | avoids low-quality targets for mechanics proof |
| minimum throughput | `>= 10 Mbps` | avoids unstable or weak datapath |
| stability | `>= 0.45` | avoids noisy egress during canary attribution |
| rollback | candidate can return to `vless` | rollback must stay simple and explicit |

## NO-GO Target Rules

A target is `NO-GO` if any of these are true:

| Condition | Reason |
|---|---|
| occupied by a real enabled user | canary would no longer isolate one-user blast radius |
| load-state users > 0 and registry confirms assignment | real load, not stale load, blocks clean target use |
| diagnose is `SUSPECT` or `FAIL` | health signal is not clean |
| below quality floor | canary result would mix user-switch mechanics with bad target quality |
| manual_only or reserve_only | separate approval needed |
| missing Direct/RU/Trusted RU exclusions | target could introduce policy-sensitive behavior |
| interface state unknown or not `UP,LOWER_UP` | route preview cannot be trusted |
| candidate is no longer `10.7.0.14 current=vless enabled=1` | candidate variable changed |

## Current E9.2.3 Baseline

The E9.2.2 snapshot is carried forward as a reproducible repo-side input for the manual checker:

```text
candidate_user=10.7.0.14
candidate_still_valid=true
target_1_current_user=10.7.0.5
clean_zero_user_target_exists=false
selected_target=NONE
approval_status=NO-GO
```

## Watcher Semantics

The manual checker `tools/v7-second-canary-target-readiness` reads local state snapshots only. Its no-argument mode uses `/opt/v7/egress/state` if available, otherwise the repo evidence snapshot in `docs/track7/control-plane/e9_2_3-evidence/current-state`.

Required output:

```text
candidate_user
candidate_still_valid
selected_target
target_candidates[]
target_1_current_user
zero_user_targets
rejected_targets
approval_status
second_canary_readiness
execution_allowed_now=false
```

`GO` from the watcher means a new E9.3 approval packet can be prepared. It does not execute or authorize the live canary.

## E9.2.4 Diagnostics Refinement

E9.2.4 reviewed the zero-user targets without changing watcher behavior:

```text
truly_no_clean_target=true
openvpn_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
wireguard_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
awg0_real_status=QUALITY_TOO_LOW
awg3_real_status=QUALITY_TOO_LOW
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

Default clean-target mode remains strict:

- diagnose `SUSPECT` still blocks `GO`;
- occupied target `1` still blocks `GO`;
- low-quality `awg0` / `awg3` still block `GO`.

Possible future extension, not implemented in E9.2.4:

- add a separate waiver-aware mode that can emit `CONDITIONAL` for idle/stale-handshake targets;
- keep default output `NO-GO` until a target is clean or an approval packet explicitly changes the experiment objective.

## E9.2.5 Waiver Packet Rule

E9.2.5 does not change strict watcher behavior. It creates a separate approval-packet path:

```text
waiver_name=openvpn_idle_suspect_mechanics_canary
target=openvpn-1779388847-d2ad7c
strict_watcher_result=NO-GO
approval_packet_status=CONDITIONAL
```

The strict checker should continue to reject diagnose `SUSPECT`. A future waiver-aware checker mode may report this as `CONDITIONAL`, but only if:

- target is zero-user by registry/load-state;
- target interface is `UP,LOWER_UP`;
- target quality floor passes;
- diagnose detail remains stale/idle only;
- all hard runtime checks pass immediately before execution;
- a human approval explicitly accepts the waiver.

## E9.3 Waiver Result

The OpenVPN waiver target passed mechanics but remains outside clean-target classification:

```text
target=openvpn-1779388847-d2ad7c
target_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
forward_result=OK
rollback_result=OK
```

Rule update:

```text
Idle-SUSPECT waiver can prove mechanics and target diversity, but it does not convert the target into CLEAN_READY.
```

Additional blocker before any future target readiness approval:

```text
post_restore_autoswitch_side_effect must be understood and bounded
```

## E9.3.1 Restore-Model Blocker

The side effect is now understood, but not yet bounded:

```text
classification=EXPECTED_BUT_UNSAFE_RESTORE_SEQUENCE
root_cause=timer_restore_immediate_apply_failover
additional_user_moved=10.7.0.5
second_canary_readiness=NO-GO
```

Target readiness now also requires a restore-model gate:

| Rule | Required Value |
|---|---|
| planner restore | planner restored and observed before apply restore |
| apply restore | separate explicit operator approval |
| pending movements | classified before apply authority resumes |
| restore blast radius | documented separately from canary blast radius |

A target can be technically suitable but still not executable if the restore model can trigger non-candidate autoswitch movement.

## E9.3.2 Target Readiness Restore Gate

The restore model is now defined but not yet executed:

```text
staged_restore_model_created=true
apply_restore_requires_separate_approval=true
target_readiness_execution_status=blocked_until_staged_restore_is_approved
```

Target readiness is no longer enough on its own. A future second canary target can move from `NO-GO` to approval discussion only when:

- candidate and target pass readiness gates;
- staged restore packet is part of the live approval;
- apply restore is excluded from automatic cleanup;
- operator separately accepts any post-canary autoswitch recovery movement.
# E9.3.3 Restore-Governance Dependency

Second canary target readiness is not sufficient by itself. Even if a target becomes acceptable, a future second canary remains blocked unless restore sequencing follows the staged model:

```text
restore planner first
observe selected moves
restore apply only by separate approval
```

E9.3.3 status:

```text
planner_only_stage_safe=true
apply_restore_status=HELD_REQUIRES_SEPARATE_APPROVAL
second_canary_readiness=CONDITIONAL_STAGED_RESTORE_PROVEN_APPLY_APPROVAL_REQUIRED
```

## E9.3.4 Apply Restore Readiness Dependency

E9.3.4 refreshed planner-only state and found no current selected moves, but apply authority remains held.

```text
pending_moves_visible=false
pending_moves_count=0_current
approval_status=CONDITIONAL
execution_allowed_now=false
```

## E11.3 Reserved WireGuard Metadata

WireGuard is now reserved in runtime metadata:

```text
target=wireguard-1779454504-c43409
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
wireguard_users_after=0
users.registry_changed=false
unrelated_egress_rows_changed=false
```

Strict readiness remains `NO-GO` because diagnose semantics are still strict:

```text
target_readiness_after=NO-GO
selected_target_after=NONE
waiver_required_after=true
second_canary_readiness_after=NO-GO
```

Reservation metadata is necessary but not sufficient. A future second canary
packet must include either a diagnose semantics fix that converts stale
handshake-only WireGuard evidence into acceptable target readiness, or an
explicit stale-handshake waiver that keeps the canary conditional and
one-user-scoped.

Fresh E9.3.4 copied runtime state also shows the old second-canary candidate baseline is no longer true:

```text
candidate_user=10.7.0.14
expected_current_egress=vless
actual_current_egress=1
candidate_still_valid=false
```

Second canary target readiness remains dependent on restore readiness. Even a clean target is not executable until:

- apply restore status is resolved or explicitly kept outside the canary block;
- the operator approves any restore-time autoswitch recovery separately;
- a fresh planner-only sample immediately before apply restore is documented.

## E9.3.5 Apply Restore Dependency

Second-canary target readiness is not enough to authorize another canary while apply restore is unresolved. E9.3.5 showed that the planner-only state can change from zero selected moves to:

```text
selected_moves=3
candidate_moves_total=15
recommended_target=vless
reason=current_egress_not_eligible
```

Therefore second-canary readiness must remain blocked unless `apply_restore_status` is one of:

- `RESTORED_AND_SETTLED_WITH_BOUNDED_RECOVERY`; or
- `HELD_WITH_EXPLICIT_OPERATOR_ACCEPTANCE_FOR_NEXT_CANARY_WINDOW`.

Current status:

```text
apply_restore_status=HELD_ABORTED_BY_FINAL_PLANNER_SAMPLE
second_canary_readiness=NO-GO
execution_allowed_now=false
```

## E9.3.6 Root-Cause Dependency

E9.3.6 found that the held apply restore was blocked by transient service-gate failover logic:

```text
egress_1_ineligibility_root_cause=service_instagram_failed
candidate_moves_count=15
selected_moves_count=3
target=vless
```

Second-canary target selection must remain subordinate to apply-restore governance. A target can be valid and still not executable if restoring autoswitch apply authority could immediately move unrelated users.

## E9.3.7 Autoswitch Policy Dependency

Second-canary target readiness must also account for autoswitch service-signal policy.

Even if a target is valid, second canary remains NO-GO when:

- apply restore is held;
- autoswitch policy can convert one transient service failure into broad failover;
- final planner-only sample contains any selected moves not explicitly approved;
- service-signal persistence/confidence thresholds are not implemented.

Updated readiness rule:

```text
target_ready=true does not imply execution_allowed_now=true
```

Execution requires both:

1. target/candidate readiness; and
2. autoswitch restore governance either settled, explicitly waived, or protected by refined transient service signal policy.

## E10 Fresh Target Rules

E10 supersedes stale E9.2/E9.3 target packets with current runtime truth.

Strict fresh target GO now requires:

- zero users by registry and load state;
- interface present and UP/LOWER_UP;
- diagnose acceptable without stale waiver reuse;
- quality floor acceptable;
- Direct/RU and Trusted RU route-class exclusions present unless a separate explicit route-class waiver is approved;
- no active planner failover pressure;
- restore-settle gate GO from fresh samples.

E10 target verdict:

```text
selected_target=NONE
target_status=NO-GO
waiver_required=true
waiver_acceptable=false
second_canary_approval_status=NO-GO
execution_allowed_now=false
```

Rejected current targets:

- `1`: occupied by `10.7.0.14` and `10.7.0.15`;
- `awg0`: zero-user and diagnose OK, but missing Direct/RU and Trusted RU exclusions;
- `awg3`: zero-user and diagnose OK, but missing Direct/RU and Trusted RU exclusions;
- `openvpn-1779388847-d2ad7c`: zero-user but diagnose `SUSPECT`;
- `wireguard-1779454504-c43409`: zero-user but diagnose `SUSPECT`.

No stale waiver is reusable. The next target approval must be generated from fresh evidence.

## E10.1 Zero-User Target Remediation Rules

E10.1 found that `awg0` and `awg3` are no longer blocked by quality in the fresh runtime sample. Both are zero-user, UP/LOWER_UP, and diagnose OK. Their strict target-readiness blocker is missing route-class exclusions.

Fresh E10.1 comparison:

```text
awg0 zero_user=true diagnose=OK avg_mbps=26.8167 min_mbps=22.43 stability=0.836419
awg3 zero_user=true diagnose=OK avg_mbps=23.9337 min_mbps=16.0 stability=0.668513
missing_exclusions=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Remediation candidate:

```text
remediation_candidate=awg0
remediation_approval_status=GO
mutation_required=true
mutation_scope=/opt/v7/egress/state/egress.registry awg0 metadata only
policy_apply_required=false
execution_allowed_now=false
```

Expected readiness after a separately approved bounded metadata mutation:

```text
expected_target_after_remediation=awg0
expected_second_canary_readiness_after_remediation=GO_if_restore_settle_gate_remains_GO_and_runtime_checks_remain_OK
```

This is not approval to mutate. It is approval to prepare a future bounded metadata mutation packet.

## E10.2 Fresh Metadata Remediation Gate Result

E10.2 rechecked target readiness immediately before the approved metadata mutation and found that the E10.1 zero-user assumption was stale.

```text
candidate_user=10.7.0.11
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
metadata_mutation_executed=false
abort_reason=awg0_no_longer_zero_user
execution_allowed_now=false
```

Fresh target statuses:

```text
awg0: NO-GO; zero_user=false; registry_users=4; load_state_users=4; diagnose=OK; load_status=HARD_FULL
awg3: NO-GO; zero_user=false; registry_users=2; load_state_users=2; diagnose=OK; load_status=HARD_FULL
1: NO-GO; zero_user=false; registry_users=2; load_state_users=2; diagnose=OK
openvpn-1779388847-d2ad7c: NO-GO; zero_user=true; diagnose=SUSPECT
wireguard-1779454504-c43409: NO-GO; zero_user=true; diagnose=SUSPECT
```

Rule update:

- a previously approved metadata remediation packet is invalid if the target stops being zero-user before mutation;
- route-class metadata remediation on an occupied egress must be treated as a broader production metadata change and needs a new approval packet;
- E10.2 did not change target rules or runtime metadata.

## E10.3 Fresh Target Pool Truth Refresh

E10.3 supersedes the stale E10.2 occupancy snapshot for target selection. The E10.2 abort remains valid, but the current target pool changed again.

Fresh E10.3 result:

```text
restore_settle_gate_status=GO
clean_zero_user_target_exists=false
selected_target=NONE
second_canary_readiness=NO-GO
execution_allowed_now=false
```

Fresh target statuses:

```text
awg0: NO-GO; zero_user=true; diagnose=OK; min_mbps=1.78; stability=0.0650188; missing_exclusions=TRUSTED_RU_SENSITIVE,DIRECT_RU
awg3: NO-GO; zero_user=true; diagnose=OK; min_mbps=1.13; stability=0.0322427; missing_exclusions=TRUSTED_RU_SENSITIVE,DIRECT_RU
1: NO-GO; zero_user=false; registry_users=6; load_state_users=6
openvpn-1779388847-d2ad7c: NO-GO; zero_user=true; diagnose=SUSPECT; min_mbps=8.83; stability=0.1641
wireguard-1779454504-c43409: NO-GO clean; zero_user=true; diagnose=SUSPECT; quality_ok=true
```

Rule update:

- do not resume E10.2 metadata mutation from the old approval packet;
- `awg0`/`awg3` metadata exclusions are not sufficient while quality floor fails;
- `wireguard-1779454504-c43409` is the only plausible conditional waiver path, but it needs a separate waiver packet;
- second canary remains `NO-GO` until a clean target exists or a fresh waiver is explicitly approved.

## E10.4 Target Reservation Strategy

E10.4 did not change runtime or target readiness. It added governance strategy for obtaining a clean target.

Current status remains:

```text
clean_zero_user_target_exists=false
second_canary_readiness=NO-GO
execution_allowed_now=false
```

New design rule:

```text
canary_reserved=true
```

must mean that autoswitch cannot assign production users to the reserved target. A reserved target is still not clean unless it is zero-user, diagnose OK or explicitly waived, quality OK, Direct/RU and Trusted RU excluded, rollback clear, and restore-settle gate GO.

Recommended next block:

```text
E10.5_WIREGUARD_STALE_HANDSHAKE_DIAGNOSTIC_AND_RESERVATION_FEASIBILITY_PACKET
```

Reason: WireGuard is zero-user, quality OK, and already has required exclusions. Its remaining blocker is `diagnose=SUSPECT` / stale handshake.

## E10.5 WireGuard Diagnostic Rule

E10.5 found that WireGuard's persisted diagnose state can be stale relative to live WireGuard reality:

```text
target=wireguard-1779454504-c43409
persisted_diagnose=SUSPECT
persisted_reason=curl_ok_but_handshake_stale
persisted_handshake_age_seconds=999999
live_latest_handshake=3 seconds ago
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
```

Strict target readiness still rejects `SUSPECT`, but a future waiver-aware approval packet may treat this as `CONDITIONAL` when all are true:

- live handshake is fresh;
- interface is `UP,LOWER_UP`;
- route evidence is sane;
- target is zero-user by registry and load-state;
- quality floor passes;
- Direct/RU and Trusted RU exclusions are present;
- restore-settle gate is `GO`;
- runtime checks are OK.

Reservation feasibility:

```text
wireguard_reservation_feasible=true
reservation_requires_mutation=true
expected_second_canary_readiness_after_reservation=CONDITIONAL_GO_WITH_STALE_HANDSHAKE_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
execution_allowed_now=false
```

## E11.1 WireGuard Readiness Simulation

E11.1 keeps strict readiness at `NO-GO` until WireGuard is reserved and the stale-handshake blocker is handled:

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
wireguard_reservation_feasible=true
waiver_required=true
expected_second_canary_readiness_after_reservation=CONDITIONAL_OR_GO_IF_DIAGNOSE_SEMANTICS_FIXED
```

Readiness can become `GO` only if:

- reservation is applied and enforced by autoswitch/readiness tooling;
- diagnose semantics are fixed/refreshed so WireGuard is no longer `SUSPECT`;
- restore-settle gate remains `GO`;
- runtime checks remain OK.

If diagnose remains `SUSPECT`, readiness can only be `CONDITIONAL` with an explicit stale-handshake waiver approval.

## E11.2 Reservation And Stale-Handshake Semantics

E11.2 did not execute canary and did not reserve the target. It approved the
next bounded packet shape:

```text
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
wireguard_quality_ok=true
wireguard_zero_user=true
reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness=CONDITIONAL_AFTER_RESERVATION_WITH_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
```

Readiness interpretation:

- `GO` requires reservation plus diagnose semantics that clear stale persisted
  handshake state using live WireGuard evidence.
- `CONDITIONAL` is possible after reservation if an explicit stale-handshake
  waiver is accepted for one bounded canary window.
- Direct canary remains `NO-GO` until reservation and a fresh second-canary
  approval packet exist.

## E11.4 WireGuard Diagnose Semantics Gate

After E11.3 reservation, E11.4 keeps strict second-canary readiness at `NO-GO`
until the WireGuard diagnose semantics are fixed or explicitly waived:

```text
wireguard_root_cause_classification=DIAGNOSE_REFRESH_BUG
strict_target_readiness=NO-GO
wireguard_blocker=diagnose SUSPECT
diagnose_affects_real_runtime=false
diagnose_affects_target_readiness_only=false
fix_required=true
waiver_acceptable=true
best_strategy=FIX_FIRST_WITH_WAIVER_AS_FALLBACK
expected_second_canary_readiness=GO_AFTER_DIAGNOSE_FIX_AND_FRESH_GATES_OR_CONDITIONAL_WITH_EXPLICIT_STALE_HANDSHAKE_WAIVER
```

Readiness interpretation:

- `GO`: allowed only after the diagnose producer is fixed/deployed and a fresh
  target readiness run sees WireGuard as clean.
- `CONDITIONAL`: allowed only through an explicit one-user stale-handshake
  waiver packet with fresh live `wg show`, route, zero-user, quality,
  restore-settle, and checker evidence.
- `NO-GO`: remains the default while `diagnose=SUSPECT` is unresolved.

## E11.5 Diagnose Fix Readiness Rule

E11.5 proves the desired readiness outcome in repo-side fixtures but does not
change runtime readiness:

```text
repo_fixed_fixture_selected_target=wireguard-1779454504-c43409
repo_fixed_fixture_second_canary_readiness=GO
runtime_selected_target=NONE
runtime_second_canary_readiness=NO-GO
runtime_deploy_executed=false
```

Therefore the readiness rule is:

- `GO` only after the fixed diagnose tool is deployed and a fresh runtime target
  readiness run selects the reserved WireGuard target.
- `NO-GO` remains active while runtime `diagnose=SUSPECT` persists.
- Waiver remains possible only as a separate conditional approval path.

## E11.6 Runtime Diagnose Fix Deployed

After E11.6, the runtime diagnose producer is protocol-aware:

```text
WireGuard=wg show
AWG/AmneziaWG=awg show
wireguard_diagnose_after=OK
wireguard_blocker_after=NONE
awg_regression_observed=false
```

With current runtime truth, the reserved WireGuard target is a strict target
readiness `GO`:

```text
selected_target_after=wireguard-1779454504-c43409
target_readiness_after=GO
waiver_required_after=false
```

The old candidate expectation `current_egress=vless` is stale. Any executable
second-canary packet must use a fresh candidate/current-egress/rollback model.

## E11.7 Fresh Readiness After Runtime Drift

E11.7 shows a separate blocker after the diagnose fix:

```text
wireguard_diagnose=OK
wireguard_reserved=true
wireguard_users_from_registry=12
wireguard_users_from_load_state=12
wireguard_zero_user=false
target_readiness_status=NO-GO
selected_target=NONE
```

Readiness rule update:

- `canary_reserved=true` is not sufficient unless the target is actually
  zero-user by both registry and load-state.
- A reserved target with production users is `NO-GO`, even if diagnose and
  quality are OK.
- Future approval requires either reservation enforcement/drain by separate
  approval or a different clean zero-user target.

## E11.8 Reservation Enforcement After Occupancy

E11.8 fixed production autoswitch enforcement for `canary_reserved=true`, but it
does not automatically make an occupied reserved target clean.

Readiness remains `NO-GO` when:

- a reserved target has any production users;
- users arrived before the enforcement fix;
- no separate bounded drain packet has been approved.

Reserved-target readiness can become `GO` only after reservation enforcement
remains active, the target has zero users in both registry and load-state,
diagnose/quality remain OK, and restore-settle governance remains GO.

## E11.11 Live-State Default Rules

E11.11 fixed stale default behavior in the readiness checker. The checker now
prefers current E11.11/E11.10 state before historical fixtures and defaults to
the closed E11.10 candidate truth:

```text
candidate_user=10.7.0.3
current_egress=awg0
```

The checker may use `egress-quality-summary.json` when token stability state is
absent, and may infer interface readiness from diagnose `OK` with a fresh
`handshake_age_seconds=` detail. This prevents historical fixture NO-GO from
masking current live GO.

This is a readiness signal only:

```text
execution_allowed_now=false
```

## E11.12 Mini-Cohort Readiness Binding

E11.12 proved that readiness defaults must be treated as block-scoped evidence,
not standing approval. The old `10.7.0.3 current=awg0` assumption became stale
after runtime drift; the first mini-cohort packet is bound to fresh candidates:

```text
candidate_1=10.7.0.11 current_egress=1 target_readiness=GO
candidate_2=10.7.0.12 current_egress=1 target_readiness=GO
selected_target=wireguard-1779454504-c43409
execution_allowed_now=false
```

Readiness for E11.12 means the target is a clean reserved target for a future
governed cohort packet. It does not authorize execution, does not override the
WireGuard `hard_limit=2`, and must be re-run immediately before any E11.13 live
movement.

## E11.13 Readiness After Mini-Cohort

After E11.13 rollback and containment, the readiness signal remains target-only:

```text
wireguard_users_after=0
target_readiness_after=GO
candidate_10.7.0.11_current=1
candidate_10.7.0.12_current=1
execution_allowed_now=false
```

This does not approve another cohort. E11.13 proved target readiness can remain
GO while the broader restore lifecycle is not promotion-clean. Future readiness
must include both target readiness and delayed apply-restore movement status.
## E11.14 Readiness Addendum

Target readiness GO is not sufficient by itself to approve cohort promotion after E11.14. WireGuard can remain clean and reserved while apply restore still risks non-cohort movement on other targets.

Additional promotion gate:

- apply_timer_must_be_held_or_restore_barrier_active=true
- delayed_apply_restore_non_cohort_movement_absent=true
- restore_barrier_or_generation_rehearsal_required=true

WireGuard target readiness remains a target-local condition; apply-restore governance is now a separate global lifecycle gate.
