# Observation to L3 Wake Bridge Implementation

Generated: 2026-07-02_083525

## Summary

Implemented the minimal Observation -> L3 Wake bridge inside the existing autoswitch owner.

When an existing planner candidate proves:

- current channel `diagnose_severity=FAIL`
- current channel `diagnose_reason=interface_down_or_missing`
- affected users remain assigned to the failed channel
- `v7-state.json` is fresh by the existing metrics freshness policy

`tools/v7-users-autoswitch` now produces a deterministic `confirmed_current_channel_failure` wake event from existing Observation facts.

No new Runtime, Planner, Authority, Restore Barrier, Wake owner, Event Bus, Truth Source, OMP, or architecture was created.

## Implementation

Changed:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

New local behavior:

- `_emergency_failover_move_evidence()` now records `current_channel_failure` evidence from the current candidate's existing severity classification.
- `_l3_wake_decision()` now consumes confirmed current-channel failure evidence and emits an inferred deterministic `confirmed_current_channel_failure` event.
- `_emergency_failover_authority_gate()` and `_l3_incident_context()` now allow an L3 incident key for pure current-channel failure using `service_family=["current_channel_failure"]` while keeping `failed_required_services=[]` unless service-matrix evidence proves a required-service failure.
- Summary diagnostics now include emergency failed sources from either required-service failure evidence or confirmed channel failure evidence.

## Owner Reuse Proof

| Stage | Existing owner reused | Result |
| --- | --- | --- |
| Observation | `v7-state.json` consumed by `tools/v7-users-autoswitch._load_egress()` | Reused |
| Candidate eligibility | `tools/v7-users-autoswitch._candidate()` and `_gate_basic()` | Reused |
| Wake | `tools/v7-users-autoswitch._l3_wake_decision()` | Extended in place |
| Incident | `tools/v7-users-autoswitch._l3_incident_context()` | Extended in place |
| Planner | `tools/v7-users-autoswitch._select_moves()` / `plan()` | Reused |
| Authority | `tools/v7-users-autoswitch._emergency_failover_authority_gate()` | Reused |
| Approved Plan Lock | `tools/v7-users-autoswitch._approved_plan_lock_validation()` | Reused |
| Restore Barrier | existing restore barrier status and gates | Reused |
| Runtime apply | `tools/v7-users-autoswitch.apply()` | Reused |
| Governed production validation owner | `tools/v7-governed-canary-dry-run-cycle` | Reused by existing tests |

## Continuity Proof

The bridge does not grant authority.

The bridge does not create packets.

The bridge does not create restore barriers.

The bridge does not bypass Planner.

The bridge does not bypass Runtime.

The bridge does not move users by itself.

The bridge only turns already-owned Observation evidence into the legal L3 wake source `confirmed_current_channel_failure`.

## Acceptance Results

Local tests prove:

- Timer wake remains `REJECT_WAKE`.
- Real `FAIL/interface_down_or_missing` with affected users produces `confirmed_current_channel_failure`.
- L3 incident state is not `NO_INCIDENT_DISABLED` or `NO_INCIDENT_NO_EVIDENCE` when confirmed current-channel failure exists.
- `selected_moves_before_restore_barrier > 0`.
- `selected_moves_after_gate == 1`.
- Selected move user is one of the affected users assigned to the failed source.
- Selected move source is the failed source.
- Selected move type is `failover`.
- No `confirmed_service_failure` is invented when service-matrix evidence is healthy.
- The inferred current-channel failure event id is deterministic across repeated planning.
- Broad automation remains disabled.

## Test Results

Commands run:

```bash
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Result:

```text
Ran 110 tests in 9.219s
OK
```

```bash
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Result: PASS.

```bash
python3 -m unittest tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 17 tests in 0.277s
OK
```

## Production Impact

Production impact: NONE.

Deploy performed: NO.

Users moved by this implementation task: 0.

Bounded production validation was not run after this local implementation because no deploy was performed.

## First Remaining Blocker

No local owner blocker remains for the bridge behavior.

Production still requires normal deployment and a bounded governed validation before this local change can affect live users.

## Next OMP Step

Run the existing safe deployment and bounded governed L3 production validation ladder with `max_users=1`.
