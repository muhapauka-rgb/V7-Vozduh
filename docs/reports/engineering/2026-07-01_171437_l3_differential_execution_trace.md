# L3 Differential Execution Trace

Status: `COMPLETE`
Mode: `READ_ONLY_DIFFERENTIAL_TRACE`
Code modified: `NO`
Runtime modified: `NO`
Architecture modified: `NO`
Production candidate regenerated: `NO`

## Summary

Compared paths:

- Good path: `tests/unit/test_v7_users_autoswitch_policy.py::test_l3_production_validation_envelope_reaches_switch_without_certifying_autonomy`, executed read-only with current code and fake switch.
- Production path: latest failed L3 Production Validation candidate from `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md` and `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md`.

Production candidate:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
current_failures: []
```

First executable divergence:

```text
current candidate service_suitability.per_service for the selected source
```

Good path contains a required service failure on current source:

```text
telegram: available=false, status=DOWN, truth_class=PERSISTENT_FAIL, freshness=FRESH
```

Production path does not contain any required-service failure rows for selected source `awg0`, so `_emergency_failover_move_evidence()` cannot produce `current_failures`.

## Differential Table

| Field | Good path value | Production path value | Same / different | First divergence? | Owner | Meaning |
| --- | --- | --- | --- | --- | --- | --- |
| `_decision_for_user()` | `switch`, `move_type=failover`, `reason=current_egress_not_eligible`, user `10.0.0.2`, source `1`, target `vless` | `switch`, `move_type=failover`, `reason=current_egress_not_eligible`, user `10.7.0.5`, source `awg0`, target `vless` | Same shape | No | `tools/v7-users-autoswitch::_decision_for_user` | Both paths produce a failover-shaped selected move. |
| Selected move after Planner | selected move exists; `source=1`, `target=vless` | selected move exists; `source=awg0`, `target=vless` | Same shape | No | Planner / Autoswitch | Identity differs by environment, not by contract. |
| `important_services` | `youtube, instagram, telegram, google, google_auth` | present/preserved; Runtime checks required services and finds no failures | Same enough to check | No | Planner / service profile | Missing services is not the blocker. |
| `candidates` | candidate list includes `vless` and current source `1` | candidate list exists after serialization fix; selected current source is `awg0` | Same shape | No | Planner / packet materialization | Candidate object survives. |
| Current candidate for source | `egress=1`, `eligible=false`, `blocked=[telegram_required_down]` | `egress=awg0`; no Runtime-verifiable required-service failure in `move_evidence` | Different | Partial | Planner / service suitability | Good path has explicit current-source service blocker. Production has broad current-not-eligible without current required-service failure. |
| Current candidate `service_suitability.per_service` | `telegram.available=false`, `status=DOWN`, `truth_class=PERSISTENT_FAIL`, `freshness=FRESH` | no row satisfying `available is false OR truth_class=PERSISTENT_FAIL OR status in DOWN/FAIL/ERROR/NOT_STARTED` for required services on `awg0` | Different | YES | Service suitability / Planner evidence | This is the first executable field that makes `current_failures` non-empty in A and empty in B. |
| Target candidate `service_suitability.per_service` | `vless` required services healthy; `telegram=OK/HEALTHY` | target `vless` selected as safe enough | Same functional outcome | No | Planner / service suitability | Target is not the first blocker. |
| `reason` list | Planner reason `current_egress_not_eligible`; gate later appends `emergency_failover_autonomy_authorized` | `current_egress_not_eligible` | Same base reason | No | Planner / Runtime gate | Reason alone is not sufficient for L3 wake. |
| `move_type` | `failover` | `failover` | Same | No | Planner / Runtime consumer | Label survives but does not prove L3 required-service failure. |
| `approved_plan_lock.selected_moves` | preserves `reason`, `important_services`, `candidates`, user/source/target/type | post-fix report confirms semantic fields preserved | Same shape | No | `admin_core/operator_execution.py` | Serialization is no longer the first divergence. |
| `restore_barrier.approved_plan_lock.selected_moves` | preserves lock selected move | post-fix report confirms lock valid and semantic fields present | Same shape | No | `admin_core/operator_execution.py` | Restore barrier carries the existing evidence; it does not create missing failures. |
| `_emergency_failover_move_evidence()` | `ok=true`, `blockers=[]` | `ok=false`, blockers include `required_service_failure_required` | Different | Downstream of first divergence | `tools/v7-users-autoswitch::_emergency_failover_move_evidence` | Runtime extracts failures only from current source required-service rows. |
| `current_failures` | `[telegram DOWN/PERSISTENT_FAIL/FRESH]` | `[]` | Different | Downstream | `_emergency_failover_move_evidence` | Direct outcome of current-source service suitability difference. |
| `failed_sources` | `[1]` | `[]` | Different | Downstream | `_emergency_failover_authority_gate` | Derived from non-empty `current_failures`. |
| `failed_services` | `[telegram]` | `[]` | Different | Downstream | `_emergency_failover_authority_gate` | Derived from non-empty `current_failures`. |
| `_l3_wake_decision()` | `ACCEPT_WAKE`; accepted sources `confirmed_service_failure`, `confirmed_current_channel_failure` | `REJECT_WAKE`; blocker `confirmed_l3_wake_required` | Different | Downstream | `tools/v7-users-autoswitch::_l3_wake_decision` | Wake is accepted only when failures can be inferred or externally proven. |
| `emergency_failover_authority_gate()` | `ok=true`; selected moves after gate `1`; decision `authorize_one_user_production_validation_envelope` | `ok=false`; selected moves after gate `0`; blockers include `required_service_failure_required`, `confirmed_l3_wake_required` | Different | Downstream | `tools/v7-users-autoswitch::_emergency_failover_authority_gate` | Gate correctly fails closed when move evidence lacks required-service failure. |

## Trace Point Detail

### Good Path Executable Values

From current-code execution of the existing test fixture:

```text
selected_move:
  user_ip: 10.0.0.2
  current_egress: 1
  recommended_egress: vless
  move_type: failover
  reason:
    - current_egress_not_eligible
  important_services:
    - youtube
    - instagram
    - telegram
    - google
    - google_auth

current_candidate:
  egress: 1
  eligible: false
  blocked:
    - telegram_required_down
  service_suitability.per_service.telegram:
    available: false
    status: DOWN
    truth_class: PERSISTENT_FAIL
    freshness: FRESH

target_candidate:
  egress: vless
  eligible: true
  blocked: []
  telegram: OK / HEALTHY

move_evidence:
  ok: true
  blockers: []
  current_failures:
    - service: telegram
      status: DOWN
      truth_class: PERSISTENT_FAIL
      freshness.state: FRESH

wake:
  decision: ACCEPT_WAKE
  accepted_wake_sources:
    - confirmed_service_failure
    - confirmed_current_channel_failure
  failed_sources:
    - 1
  failed_services:
    - telegram

authority_gate:
  ok: true
  decision: authorize_one_user_production_validation_envelope
  selected_moves_before_gate: 1
  selected_moves_after_gate: 1
```

### Production Path Executable Values

From latest production validation report:

```text
selected_move:
  user_ip: 10.7.0.5
  current_egress: awg0
  recommended_egress: vless
  move_type: failover
  reason:
    - current_egress_not_eligible

approved_plan_lock_validation.ok: true
approved_plan_lock.selected_moves contains semantic fields: true

move_evidence:
  current_failures: []

gate_blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required

wake:
  decision: REJECT_WAKE
  blocker: confirmed_l3_wake_required

authority_gate:
  selected_moves_after_gate: 0
  execution_blocker: emergency_failover_autonomy

terminal:
  final_verdict: STOP_SAFE
  apply_executed: false
  users_moved: 0
```

## Primary Questions

### 1. In the good path, what exact field causes `current_failures` to be non-empty?

This exact field:

```text
selected_move.candidates[current_source].service_suitability.per_service.telegram
```

with values:

```text
available: false
status: DOWN
truth_class: PERSISTENT_FAIL
freshness.state: FRESH
```

The Runtime extraction rule in `tools/v7-users-autoswitch::_emergency_failover_move_evidence()` appends a current failure when any required service row satisfies:

```text
available is false
OR truth_class == PERSISTENT_FAIL
OR status in DOWN / FAIL / ERROR / NOT_STARTED
```

### 2. In production, why is `current_failures` empty?

Chosen answer:

```text
E. Planner selected a non-L3 candidate as failover.
```

Executable reason:

The production selected move has:

```text
reason: current_egress_not_eligible
move_type: failover
source: awg0
```

but Runtime cannot find any required-service failure row on `awg0` for the selected user's required services. Therefore `current_failures` remains empty and `_l3_wake_decision()` has no `failed_sources` or `failed_services`.

This is not:

- `B`: required services are not missing; Runtime checks them.
- `C`: candidate evidence exists after the serialization fix.
- `D`: the interpreter is not too narrow; the good path proves `DOWN`, `PERSISTENT_FAIL`, and `available=false` are accepted.
- `F`: Runtime extraction is not too strict; it accepts the good path.
- `G`: production data shape is no longer the first issue after serialization was fixed.

It is also compatible with:

```text
A. awg0 has no required-service failure
```

at the Runtime evidence boundary. But the first executable cause is `E`, because Planner still emitted `move_type=failover` even though the selected source did not carry the L3-required failure evidence.

### 3. Does production Planner legally emit `move_type=failover` for `awg0`?

```text
NO
```

Not as an L3-executable failover.

It may emit a movement candidate or explanation that current egress is not eligible, but it must not produce an L3-executable `FAILOVER` selected move unless same-subject current-channel failure and required-service failure are present for `10.7.0.5 / awg0`.

### 4. If NO, what should it emit instead?

Best fit:

```text
PROBE_ONLY
```

Reason:

The system has enough concern to investigate or refresh evidence, but not enough same-subject L3 failure proof to execute emergency failover.

Acceptable fail-closed alternatives depending on local vocabulary wiring:

```text
WAIT
ASK_OPERATOR
NO_ACTION
```

It should not emit L3-executable `FAILOVER`.

### 5. If YES, what evidence must be added or preserved so Runtime can derive `current_failures`?

Not applicable to current production candidate because answer 3 is `NO`.

If a future candidate is legitimately L3 failover, it must carry current-source required-service failure evidence equivalent to the good path:

```text
selected_move.candidates[current_source].service_suitability.per_service[required_service]:
  available: false
  status: DOWN | FAIL | ERROR | NOT_STARTED
  or truth_class: PERSISTENT_FAIL
  freshness.state: FRESH | AGING
```

## Regression Tests

Existing tests already cover:

| Requirement | Existing coverage |
| --- | --- |
| Good L3 path where `current_failures` is non-empty | `tests/unit/test_v7_users_autoswitch_policy.py::test_l3_production_validation_envelope_reaches_switch_without_certifying_autonomy` |
| Runtime keeps STOP_SAFE when `current_failures` is empty | `tests/unit/test_v7_users_autoswitch_policy.py::test_l3_production_validation_blocks_two_users_and_source_recovered` second subcase |
| Serialization preserves evidence | `tests/unit/test_operator_execution_packet.py::test_nonzero_packet_generation_and_clearance_lifecycle` |
| Approved plan lock carries semantic fields | `tests/unit/test_v7_users_autoswitch_policy.py::approved_plan_lock_from_plan` helper plus production validation envelope tests |

Missing explicit regression test:

```text
Planner must not emit L3-executable failover when current_egress_not_eligible exists
but required-service failure is absent for the same user/source.
```

That test should assert the Planner output is not an L3-executable `move_type=failover` for the production-shaped case.

## First Divergence

```text
field: selected_move.candidates[current_source].service_suitability.per_service[required_service]
function: tools/v7-users-autoswitch::_emergency_failover_move_evidence
root executable reason: production selected source awg0 has no Runtime-verifiable required-service failure row, while the good path has telegram DOWN/PERSISTENT_FAIL/FRESH.
minimal correction direction: Planner must not emit L3-executable `failover` from broad `current_egress_not_eligible` unless the selected current source carries same-subject required-service failure evidence.
```

## Final Verdict

```text
FIRST_DIVERGENCE_FOUND
```
