# Eligibility Root Cause Proof

Timestamp: 2026-07-01 19:19:23 Asia/Bangkok
Status: READ_ONLY_PROOF
Code modified: NO
Runtime modified: NO
Planner modified: NO
Production queried: NO

## Mission

Trace the exact birth of `current.eligible == false` for the historical production candidate:

```text
user: 10.7.0.5
source: awg0
target: vless
```

The requested proof target is not whether Runtime later rejected the move. The target is the first `_candidate()` gate that changed the current candidate from:

```text
eligible=true
```

to:

```text
eligible=false
```

## Inputs Read

- `docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md`
- `docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md`
- `docs/reports/engineering/2026-07-01_151234_formal_model_verification.md`
- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- pre-existing source version via `git show HEAD:tools/v7-users-autoswitch`
- persisted local artifacts matching `10.7.0.5`, `awg0`, and `vless`

## Source Code Trace

`_candidate()` creates a fresh candidate as eligible:

```text
c = Candidate(egress=egress, eligible=True)
```

Then it runs gates in this order:

```text
_gate_basic()
_gate_reservation()
_gate_org()
_gate_quality()
_gate_service()
_gate_load()
_gate_safety()
```

The only primitive that flips eligibility is:

```text
_block(candidate, reason):
  candidate.eligible = False
  candidate.blocked.append(reason)
```

Therefore the exact first gate can only be proven from an ordered gate trace or from a final candidate whose first inserted blocker is known to preserve insertion order for the target generation.

## Gate Possibility Table

| Gate | Inputs needed | Can flip current eligible? | Possible blockers | Source object / producer | Freshness |
| --- | --- | --- | --- | --- | --- |
| `_gate_basic()` | `Egress.enabled`, `state`, `manual_only`, `health_code`, severity classification, load mode | YES | `egress_disabled`, `egress_state_*`, `manual_only`, `health_code_*`, `severity_*`, `hard_full`, `reserve_only` | egress registry, `v7-state.json`, dynamic load policy | registry/state snapshot time required |
| `_gate_reservation()` | user current, `egress.canary_reserved` | YES except current canary path returns advisory | `canary_reserved_production_assignment_blocked` | egress registry meta | registry snapshot time required |
| `_gate_org()` | group policy, allowed/excluded pools, ACLs, exclusivity, current group usage | YES | `not_in_group_allowed_pool`, `excluded_by_group_policy`, `exclusive_to_*`, `not_in_egress_group_acl`, `egress_in_use_by_other_group` | org policy, user registry group usage | policy/registry snapshot time required |
| `_gate_quality()` | egress avg/min/stability, 1h quality window, service aggregate, severity exception | YES | `avg_mbps_below_floor`, `min_mbps_below_floor`, `stability_below_floor` | `v7-state.json`, `egress-quality-summary.json`, service suitability | quality window `updated` required |
| `_gate_service()` | route class, service matrix rows, telegram sentinel, explicit required services, route fitness | YES | `trusted_ru_required`, `service_*_evidence_unknown`, `telegram_required_*`, `service_multiple_critical_failed`, `service_*_persistent_failed`, `service_*_truth_stale`, `route_class_*_failed` | `service-matrix.json`, `telegram-sentinel.json`, service preferences/policy | service row freshness required |
| `_gate_load()` | purpose, target/current distinction, load limits, users count | For current purpose: NO, it returns immediately | `failover_full`, `planned_hard_full` for non-current only | dynamic load summary | load snapshot time required |
| `_gate_safety()` | purpose, user safety, egress safety, recent switches | For current purpose: NO, it returns immediately | `egress_safety_quarantine`, `egress_failed_verifications_limit`, `target_blocked_for_user`, `pair_reversal_stability_window` for non-current only | `autoswitch-safety.json` | safety state timestamp required |

For the requested current candidate (`purpose="current"`), `_gate_load()` and `_gate_safety()` cannot be the first flip because both return immediately for current purpose in the inspected source.

## Persisted Evidence Search

Searched local persisted artifacts for the exact structured tuple:

```text
user_ip/user/ip = 10.7.0.5
current_egress/source/from = awg0
recommended_egress/target/to = vless
```

Result:

```text
exact structured matches: 1
```

The single match is:

```text
docs/reports/evidence/trust_calibration_operator_certification_evidence/production_trust_inputs.json
switch_history[15]:
  user_ip: 10.7.0.5
  from: awg0
  to: vless
  reason: autoswitch_failover
  ts: 2026-05-27T03:18:01.952891+00:00
```

This is not the requested July L3 Production Validation Planner candidate. It is switch history only. It does not contain:

- `decisions[]`
- `candidates[]`
- current candidate `blocked[]`
- current candidate `reasons[]`
- `quality_decision`
- `service_suitability`
- `load`
- `safety`
- gate before/after eligibility

Other inspected planner artifacts containing `10.7.0.5` were not the target tuple:

- `docs/reports/evidence/authority_bridge_evidence/current_production_authority_dry_run.txt`: `10.7.0.5` had `current_egress=vless`, not `awg0`.
- `docs/channel_truth_1/evidence/autoswitch_planner_preview.json`: `10.7.0.5` had `current_egress=vless`, target `wireguard-1779454504-c43409`, not `awg0 -> vless`.
- numerous `awg0 -> vless` planner objects existed for other users such as `10.7.0.9`, `10.7.0.10`, and `10.7.0.13`, but not for the requested `10.7.0.5` target.

The required July target appears in engineering reports as a reconstructed candidate, not as a raw persisted Planner plan object.

## What The Reports Prove

The required reports prove:

```text
Planner emitted:
  user: 10.7.0.5
  source: awg0
  target: vless
  move_type: failover
  reason: current_egress_not_eligible
```

Runtime later derived:

```text
current_failures: []
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
```

They do not persist the raw current candidate object at `_candidate(user=10.7.0.5, egress=awg0, purpose=current)` birth.

Specifically absent:

```text
decisions[].candidates[] row where:
  decision.user_ip == 10.7.0.5
  decision.current_egress == awg0
  decision.recommended_egress == vless
  candidate.egress == awg0
```

and absent within that row:

```text
candidate.blocked[]
candidate.reasons[]
candidate.quality_decision
candidate.service_suitability
candidate.load
candidate.safety
ordered gate transition trace
```

## Question Answers

### 1. Which gate FIRST changed eligible=true -> false?

Not provable from persisted historical evidence.

Possible gates for current purpose are:

- `_gate_basic()`
- `_gate_reservation()`
- `_gate_org()`
- `_gate_quality()`
- `_gate_service()`

Not possible for current purpose:

- `_gate_load()`
- `_gate_safety()`

The exact first gate cannot be selected because the July `10.7.0.5 / awg0 / vless` raw Planner candidate and ordered gate trace were not persisted.

### 2. What exact blocker was inserted?

Not provable for the target July candidate.

Runtime proved the blocker was not a Runtime-verifiable required-service failure row for `awg0`, because `current_failures` was empty. But Runtime did not prove whether the Planner-side ineligibility blocker was:

- quality, such as `min_mbps_below_floor` or `stability_below_floor`;
- basic, such as `health_code_*` or `severity_*`;
- service freshness/unknown/stale evidence;
- org/reservation policy;
- another Planner hard blocker.

### 3. Was it required service failure, quality, freshness, load, safety, policy, or another gate?

Not exactly provable.

What can be excluded:

- load for current candidate: `_gate_load()` returns immediately when `purpose == "current"`;
- safety for current candidate: `_gate_safety()` returns immediately when `purpose == "current"`;
- L3-required service failure as consumed by Runtime: Runtime found `current_failures: []`.

What remains possible:

- basic;
- reservation;
- org policy;
- quality;
- service freshness/unknown/stale or non-L3 service gate.

### 4. Was current.blocked[] preserved historically?

For the requested July candidate: NO evidence found.

The code path can serialize `candidate.blocked[]` via `_candidate_json()` when the full plan is persisted. Other artifacts demonstrate planner objects can include `blocked[]`. But the requested July target's full `decisions[].candidates[]` object was not found in persisted local artifacts or required reports.

### 5. If not, where was it lost?

No source-code loss is proven.

The loss is an evidence-capture/persistence gap:

```text
The raw full Planner plan for the July L3PV candidate was not persisted in the available artifact set.
```

The reports retained only the reconstructed selected move identity and later Runtime gate result. That is enough to prove `current_egress_not_eligible` reached selected move birth and `current_failures` was empty later. It is not enough to prove the exact `_candidate()` gate that first flipped `eligible`.

### 6. Can Planner legally emit L3 failover from this blocker?

Not answerable for the exact unknown blocker.

Canonical rule:

Planner may emit L3-executable failover only from same-subject current-channel failure plus required-service failure evidence for the affected user/current source.

If the missing blocker was quality, basic, org/reservation, freshness unknown, or non-L3 service degradation, then Planner cannot legally emit L3 failover from it.

If the missing blocker was a required-service failure with fresh same-subject current-source evidence, then it could be L3-compatible. But that case conflicts with downstream `current_failures: []` unless the failure evidence was lost before Runtime. Existing reports say semantic payload preservation was fixed and not the first divergence, but the raw July candidate is still missing, so this cannot be proven at gate-birth depth.

### 7. Is Planner wrong, or is the upstream gate producing an incorrect blocker?

Not provable at the requested gate-birth depth.

The earlier broader conclusion that Planner overclassified broad `current_egress_not_eligible` remains plausible, but this task asked for stricter proof of the exact first gate. That stricter proof requires historical data that is not present.

No evidence proves an upstream gate produced an incorrect blocker. No evidence proves the exact upstream blocker was correct either.

## Required Missing Historical Object

The exact missing object is:

```text
Full raw Planner plan JSON for the July L3 Production Validation attempt,
including the decision:
  user_ip: 10.7.0.5
  current_egress: awg0
  recommended_egress: vless
and its current candidate row:
  candidates[].egress == awg0
  candidates[].eligible
  candidates[].blocked[]
  candidates[].reasons[]
  candidates[].quality_decision
  candidates[].service_suitability
  candidates[].load
  candidates[].quality_history
  candidates[].severity_classification
```

To prove the first gate, an even stronger missing object is needed:

```text
ordered gate trace for that same candidate:
  gate name
  input values
  eligible before
  eligible after
  blocker/reason appended
  source object
  producer
  freshness
  owner
```

Without at least the final raw candidate row, the exact blocker is unknown. Without ordered gate tracing, multiple blockers in `blocked[]` would still require code-order reconstruction to infer the first flip.

## Final Verdict

INSUFFICIENT_HISTORICAL_EVIDENCE
