# V7 Autonomous Recovery Agent — Block 3 Product-Evidence Checkpoint

Status: `IMPLEMENTATION_BLOCK_3_COMPLETE_CONTINUE_SAME_MISSION`

## Implemented existing-owner extension

`tools/v7_sync_lib.py` now produces and fail-closed validates immutable
controlled Polygon recovery receipts. Every receipt binds:

- exact experiment, scenario, fault sequence, generation and fingerprints;
- authoritative Polygon `T_PHYSICAL_FAILURE` from the injected virtual event;
- complete affected scope frozen at onset;
- one receipt for every affected client with assignment, kernel/route and
  required-service S11 verification;
- `LAST_AFFECTED_REQUIRED_S11`, calculated duration and the seven-second
  verdict;
- actual Engineering execution wall time and process RSS envelope;
- explicit zero Runtime, Production and Authority effects.

The execution reuses the real existing isolated
`AutoswitchPlanner.plan`, `build_service_failure_adaptive_cohort_contract` and
`routing_digital_twin_virtual_apply` paths. It does not add a Planner, Apply
owner, Matrix, queue, registry, Runtime or truth source.

## Controlled evidence run

Campaign fingerprint:
`c231da24b3f5b226ad9090ab268f8f997b2aed8d3c174df8ecd4c1c65a09967d`.

| Scenario | Fault | Failed channels | Complete members | Onset to last S11 | Engineering wall | Peak RSS |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `AR-1K-HARD` | hard channel failure | 1 | 1,000/1,000 | 4,490 ms | 24.656 s | 735,312 KiB |
| `AR-10K-CORRELATED` | correlated multi-channel | 3 | 10,000/10,000 | 4,490 ms | 23.547 s | 749,712 KiB |

Both receipts passed exact-scope, last-member, identity and duration
validation. The 4,490 ms clock is deterministic controlled virtual-time
evidence, not Production latency or hardware-capacity evidence. Planner wall
time and RSS are reported separately and cannot be hidden inside the virtual
clock.

Executed coverage is deliberately bounded to hard single-channel and
correlated three-channel cases at the mandatory 1,000 then 10,000 scale gates.
The remaining declared fault classes are not reported as executed merely
because they exist in the catalog.

## Strict negative gates

- missing last affected member: `STOP_SAFE`;
- forged seven-second verdict: `STOP_SAFE`;
- stale member generation: `STOP_SAFE`;
- wrong member scenario identity: `STOP_SAFE`;
- incomplete assignment/kernel/required-service S11: `STOP_SAFE`.

## Disposable seeded defect proof

An isolated owner-path fixture deliberately selected `max(bounds)` instead of
the mandatory minimum across incident, capacity and Authority bounds. The
independent invariant test failed, the deterministic causal record localized
the exact error, one-line minimal repair restored `min(bounds)`, the exact
origin experiment replay passed, dependent regression passed, and all seeded
files were removed.

This record is explicitly
`DETERMINISTIC_CAUSAL_RECORD_NOT_NATIVE_ANALYST`; the invariant review is not
misrepresented as a native model Reviewer. Fresh native Analyst/Reviewer
acceptance remains owned by the compact runner.

## Verification

- Block 3 focused tests: `4/4 PASS` in `46.580 s`;
- controlled campaign: `PASS`;
- 1,000 then 10,000 ordering: `PASS`;
- seeded defect repair/return/cleanup: `PASS`;
- Production, CPS, Runtime, routing, real-user and Authority effects: `NONE`.

## Exact continuation

Block 4 must extend bounded coverage to the remaining service, partial,
stale/current, insufficient-capacity, mid-switch/rollback and restart/replay
branches, retain correct `STOP_SAFE` outcomes where recovery is not lawful,
and run the compact command with fresh native Analyst, Codex critical Executor
and independent Reviewer contexts. It must consume their artifacts through the
Block 2 gate and prove automatic same-Mission continuation. This checkpoint is
not the Program terminal.
