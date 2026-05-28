# Target Reservation Policy

Mode: governance design. Not deployed.

## Purpose

V7 can now prove canary mechanics, quiet-window behavior, restore sequencing, and restore-settle windows. The remaining blocker is target-pool governance: there is no guaranteed clean target that autoswitch cannot occupy before a canary.

This policy defines a future reservation model for clean test targets.

## Reservation Field

Proposed egress metadata:

```text
canary_reserved=true
```

Optional companion fields:

```text
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
reservation_expires_at=<iso8601-or-empty>
reservation_allowed_users=<candidate-ip-or-empty>
```

## Required Semantics

When `canary_reserved=true`:

- autoswitch planner must not select the egress for normal production users;
- autoswitch apply must not move users onto the egress unless the movement belongs to an approved canary window;
- target readiness may prefer the egress if it is zero-user and clean;
- manual `v7-user-switch` still requires separate explicit approval;
- reservation must be reversible with a documented rollback.

## Clean Reserved Target Requirements

A reserved target is clean only when all are true:

```text
enabled=1
canary_reserved=true
users_count_from_registry=0
users_count_from_load_state=0
interface=UP/LOWER_UP
diagnose=OK
quality_floor=OK
exclude_route_classes includes DIRECT_RU
exclude_route_classes includes TRUSTED_RU_SENSITIVE
manual_only/reserve semantics understood
route table preview possible
rollback target clear
restore_settle_gate_status=GO
runtime checks OK
```

## Conditional Reserved Target

A reserved target is conditional if:

- diagnose is `SUSPECT` only for a classified stale/idle reason;
- quality passes floor;
- operator explicitly approves a waiver;
- rollback is clear;
- target is zero-user by registry and load-state;
- no hidden autoswitch/user-switch/routing-sync process is observed.

`CONDITIONAL` does not authorize canary by itself. It authorizes a separate waiver approval packet.

## NO-GO Conditions

Reservation or target use is NO-GO if any are true:

- target has production users;
- load-state users disagree in a way that implies hidden occupancy;
- diagnose is `FAIL` or unclassified `SUSPECT`;
- quality floor fails;
- Direct/RU or Trusted RU exclusions are missing;
- route table preview is unavailable;
- autoswitch can still assign production users to the target;
- restore-settle gate is not `GO`;
- runtime checks fail.

## Lifecycle

1. Read-only target selection identifies candidate target.
2. Reservation approval packet defines exact metadata/policy changes.
3. Bounded mutation block applies reservation only.
4. Read-only verification proves target remains zero-user and clean.
5. Canary approval packet references reservation evidence.
6. Canary execution uses staged restore lifecycle.
7. Reservation is removed or promoted only by separate approval.

## Governance Status

```text
target_reservation_policy_created=true
runtime_policy_deployed=false
metadata_mutation_performed=false
execution_allowed_now=false
```

## E11.5 Repo-Side Diagnose Fix Prepared

E11.5 added a repo-side `tools/v7-egress-diagnose` implementation with
protocol-aware handshake semantics:

```text
wireguard -> wg show
amneziawg/awg -> awg show
repo_diagnose_fix_implemented=true
runtime_deploy_executed=false
diagnose_fix_executed=false
wireguard_reserved=true
target_readiness_after=NO-GO_RUNTIME_UNCHANGED_GO_IN_REPO_FIXED_FIXTURE
recommended_next_block=E11.6_BOUNDED_RUNTIME_DEPLOY_OF_WIREGUARD_DIAGNOSE_FIX
```

Reservation remains valid and runtime remains unchanged. WireGuard becomes a
strict clean target only after the diagnose fix is deployed to runtime and fresh
target readiness selects the reserved WireGuard target.

## E11.4 WireGuard Diagnose Semantics Decision

E11.4 completed the post-reservation diagnose semantics review and found that
WireGuard reservation is structurally correct, but strict readiness is still
blocked by a diagnose producer bug:

```text
target=wireguard-1779454504-c43409
wireguard_reserved=true
wireguard_users=0
strict_readiness=NO-GO
blocker=diagnose SUSPECT
wireguard_root_cause_classification=DIAGNOSE_REFRESH_BUG
best_strategy=FIX_FIRST_WITH_WAIVER_AS_FALLBACK
recommended_next_block=E11.5_BOUNDED_WIREGUARD_DIAGNOSE_SEMANTICS_FIX_PACKET
execution_allowed_now=false
```

Reservation remains valid, but it is not enough to make WireGuard a clean target.
Clean target status requires a protocol-aware diagnose fix so the runtime uses
`wg show` for WireGuard handshake freshness instead of the AWG-specific command
path. A one-user stale-handshake waiver remains possible only as a conditional
fallback with fresh live handshake, route, quality, restore-settle, and runtime
checker evidence.

## E10.5 WireGuard Feasibility Addendum

E10.5 classified `wireguard-1779454504-c43409` as the best current conditional reservation target:

```text
target=wireguard-1779454504-c43409
zero_user=true
quality_ok=true
Direct_RU_exclusion_present=true
Trusted_RU_exclusion_present=true
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
```

Reservation remains design-only until a bounded metadata/tooling approval block explicitly applies it. A `canary_reserved=true` field must not be treated as a hard guard unless autoswitch/readiness tooling is confirmed to honor it.

## E11.1 WireGuard Reservation Decision

E11.1 refreshed the live target truth and confirmed WireGuard remains reservation-feasible:

```text
target=wireguard-1779454504-c43409
wireguard_zero_user=true
wireguard_quality_ok=true
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
expected_second_canary_readiness_after_reservation=CONDITIONAL_OR_GO_IF_DIAGNOSE_SEMANTICS_FIXED
```

Next reservation approval must include:

- exact `egress.registry` metadata diff;
- proof that autoswitch/readiness honors `canary_reserved=true`;
- stale-handshake waiver or diagnose semantics fix;
- kill-switch/user-route/reconcile/provisioning rechecks.

## E11.2 WireGuard Reservation Approval Packet

E11.2 prepared the bounded approval packet for WireGuard reservation without
mutating runtime state:

```text
target=wireguard-1779454504-c43409
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
secondary_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
reservation_approval_status=GO_FOR_SEPARATE_BOUNDED_METADATA_MUTATION_PACKET
recommended_next_block=E11.3_BOUNDED_WIREGUARD_RESERVATION_METADATA_MUTATION
```

Reservation metadata remains preview-only until a separate bounded mutation
block:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

No canary may use this target until either diagnose semantics are fixed or the
explicit stale-handshake waiver is carried into a fresh second-canary approval
packet.

## E11.3 WireGuard Reservation Metadata Applied

E11.3 executed the bounded metadata mutation for WireGuard only:

```text
target=wireguard-1779454504-c43409
runtime_file=/opt/v7/egress/state/egress.registry
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
rollback_performed=false
users.registry_changed=false
unrelated_egress_rows_changed=false
```

This reserves the target in metadata, but it does not make the target clean by
itself. Strict target readiness remains `NO-GO` until `diagnose=SUSPECT` is
resolved by a diagnose semantics fix or accepted through a fresh bounded
stale-handshake waiver approval packet.

Current reservation state:

```text
wireguard_reserved_after=true
wireguard_users_after=0
target_readiness_after=NO-GO
selected_target_after=NONE
waiver_required_after=true
second_canary_readiness_after=NO-GO
execution_allowed_now=false
```

## E11.6 WireGuard Diagnose Runtime Deploy

E11.6 deployed the protocol-aware runtime diagnose tool. The reserved WireGuard
target now clears strict diagnose:

```text
target=wireguard-1779454504-c43409
wireguard_reserved_after=true
wireguard_users_after=0
wireguard_diagnose_after=OK
wireguard_blocker_after=NONE
selected_target_after=wireguard-1779454504-c43409
target_readiness_after=GO
waiver_required_after=false
```

Reservation policy remains unchanged: a reserved target is not canary-approved
by metadata alone. A fresh approval packet must still select the current
candidate, current egress, rollback target, and staged restore lifecycle from
live runtime truth.

## E11.7 Reservation Enforcement Gap

E11.7 found that the reserved WireGuard target is occupied:

```text
target=wireguard-1779454504-c43409
canary_reserved=true
users_from_registry=12
users_from_load_state=12
target_readiness=NO-GO
```

Policy implication:

- reservation metadata must be enforced by autoswitch eligibility before it can
  protect canary isolation;
- a reserved target with production users is not a clean canary target;
- the next governance block should investigate reservation enforcement and
  target-pool reconciliation before any canary approval.

## E11.8 Reservation Enforcement Runtime Rule

E11.8 proved that `canary_reserved=true` was metadata-only until production
autoswitch consumed it. Runtime `v7-users-autoswitch` now enforces reservation
as a production destination hard-block:

- `canary_reserved=true` is parsed from egress metadata;
- reserved targets are excluded from the production dynamic load pool;
- non-current production users cannot be assigned to a reserved target;
- existing users already on a reserved target are held with
  `canary_reserved_current_hold_requires_separate_drain_approval`;
- draining existing users requires a separate bounded approval packet.

Reservation enforcement is active for new assignments, but target cleanliness
still requires `users_count=0`.

## E11.11 Reservation Enforcement Review

E11.11 rechecked reservation enforcement after E11.10 closeout.

```text
reservation_enforcement_complete=true
```

Coverage:

- planner destination selection blocks `canary_reserved=true` targets;
- apply selection receives no reserved-target production moves from the planner;
- failover, planned movement, reconnect rotation, and rebalance all pass through
  the same candidate reservation gate;
- dynamic load excludes canary-reserved targets from the working production pool;
- an existing user already on a reserved target is held and requires a separate
  drain approval;
- target readiness may select a reserved target only for explicitly governed
  canary/cohort use, not production assignment.

Manual `v7-user-switch` remains a privileged explicit-governance path and must
be driven only by an approved movement manifest.

## E11.12 Two-User Cohort Reservation Use

E11.12 keeps the production reservation rule unchanged:

- `canary_reserved=true` blocks production autoswitch assignment to
  `wireguard-1779454504-c43409`;
- target readiness may select that target only for an explicit governed packet;
- E11.12 itself is read-only and performed no movement;
- the first mini-cohort may name at most two users because WireGuard has
  `hard_limit=2`;
- a three-user cohort is forbidden.

Current approved packet scope:

```text
selected_target=wireguard-1779454504-c43409
selected_candidates=10.7.0.11,10.7.0.12
wireguard_users_before=0
wireguard_hard_limit=2
target_capacity_safe=true
execution_allowed_now=false
```

Future E11.13 execution must re-verify zero-user reserved target state before
using the explicit-governance movement path.

## E11.13 Reservation Result

E11.13 used the reserved WireGuard target only for the approved two users and
then rolled both users back.

```text
approved_users=10.7.0.11,10.7.0.12
max_wireguard_users_observed=2
wireguard_hard_limit=2
wireguard_users_after=0
reservation_enforced_after=true
production_assignment_to_reserved_target=blocked
```

The reservation policy held: delayed post-apply movement did not reassign any
production user to WireGuard. The blocker after E11.13 is restore/apply churn,
not reserved-target leakage.
## E11.14 Reservation Interaction

E11.14 delayed movement did not violate WireGuard reservation. During the 13:18 apply-timer movement, WireGuard remained ineligible for production assignment with `canary_reserved_production_assignment_blocked`.

Reservation verdict:

- reservation_enforcement_regression=false
- wireguard_reserved_target_used_by_delayed_apply=false
- delayed_movement_target=awg0

The remaining issue is apply-restore service-signal governance, not reserved-target enforcement.

## E11.15 Reservation Interaction

E11.15 did not move any user and did not use the reserved WireGuard target. The
bounded apply timer rehearsal preserved reservation enforcement:

```text
wireguard_users=0
production_assignment_to_reserved_target=false
selected_moves_during_rehearsal=0
reservation_enforced_after=true
```

The timer-triggered apply generation still treated
`wireguard-1779454504-c43409` as blocked for production assignment via
`canary_reserved_production_assignment_blocked`. The remaining E11.15 condition
is barrier TTL/generation governance, not target reservation.

## E11.16 Reservation Interaction

The post-TTL generation fix did not change target reservation semantics.
WireGuard remained clean and reserved:

```text
wireguard_users=0
canary_reserved_production_assignment_blocked=true
selected_moves_after_fix=0
reservation_regression=false
```

The E11.16 issue and fix are apply-generation governance, not reservation
enforcement.

## E11.17 Clearance Budget Interaction

E11.17 did not change reservation semantics. WireGuard remains
`canary_reserved=true` and production assignment remains blocked.

The new generation-clearance budget guard is orthogonal to reservation:

- reservation blocks production assignment to reserved targets;
- clearance budget blocks apply-timer movement above the governed budget after
  an expired barrier is explicitly cleared.

E11.17 live rehearsal used `clearance_max_selected_moves=0`; WireGuard users
remained `0` and no production user was assigned to the reserved target.

## E11.18 Promotion-Clean Reservation Decision

The two-user promotion-clean approval is constrained by WireGuard reservation
and capacity:

```text
selected_target=wireguard-1779454504-c43409
wireguard_users_current=0
wireguard_hard_limit=2
two_user_promotion_clean=true
three_user_wireguard_cohort_forbidden=true
```

Reservation enforcement remains complete for the bounded two-user lifecycle.
It does not authorize production assignment to the reserved target outside the
explicit governed cohort manifest.

## E12 Generation-Token Interaction

E12 did not change target reservation semantics. WireGuard remains
`canary_reserved=true`, zero-user, and blocked from production autoswitch
assignment.

Generation-token governance is orthogonal:

- reservation blocks unapproved assignment to reserved targets;
- generation tokens block stale or unowned nonzero selected-move clearance;
- WireGuard `hard_limit=2` still forbids a 3-user WireGuard cohort.

```text
wireguard_reserved=true
wireguard_users=0
larger_cohort_readiness_after=CONDITIONAL_NO_GO
execution_allowed_now=false
```
