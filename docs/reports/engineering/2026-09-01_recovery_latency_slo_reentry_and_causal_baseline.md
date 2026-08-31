Mission ID: `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`
Run Nonce: `V7_PHASE6_PHASE7_BOUNDARY_20260827_01`

# Recovery-latency SLO re-entry and causal baseline

Date: 2026-09-01

## Purpose

Functional automatic recovery remains historical evidence, but the active
product contract is not consumed until V7 itself proves:

```text
T_FIRST_VALID_FAILURE_OBSERVATION
-> T_GLOBAL_ALL_AFFECTED_RECOVERED
P95 <= 7000 ms
MAX <= 8000 ms
```

This report re-enters that single unfinished V5.3 contract. It does not create
a Program, owner, Matrix, Planner, timer, queue, state source or operational
recovery action.

## Current Runtime provenance (read-only)

| Surface | Observed state |
| --- | --- |
| Local source | `Updatesystem` at `dc14856373fd478417efd877774beae3bb49e610`; one pre-existing untracked historical report was left untouched. |
| Deployed runtime model | manifest deploy `deploy-z8-14-Updatesystem-2de1542-20260901T005009`; source/runtime commit difference is documentation-only. |
| Health owner | `v7-health.service` active; role-based health loop is running. |
| Admin owner | `v7-admin-api.service` active. |
| Matrix | canonical `service-matrix.json` was freshly written at 2026-09-01T01:10:17+03:00. |
| VLESS current evidence | canonical Matrix reports correlated continuing required-service failure; current ordinary affected scope is three users. |

Remote GitHub inspection and the truth gate's broad runtime-hash read were
unavailable in the local sandbox. This is a provenance observation, not a
reason to change Runtime; the safe deploy path remains the only deploy owner.

## Immutable fail baseline

Previously measured samples remain fail evidence and were not relabelled:

| Segment | Measured residual |
| --- | ---: |
| first valid failure -> obligation ready | about 9.648 s |
| first valid failure -> execution lease | about 14.205 s |
| three-user Apply + verification | about 39.037 s |
| three-user total | about 41.827 s |
| observed historical bad placement | about 8 minutes |

## Fresh causal baseline

| Stage | Current evidence | Duration / state | Owner | Classification |
| --- | --- | --- | --- | --- |
| Detector dispatch | `other_required` cadence | 3500 ms | existing `v7-health-loop` | recovery-critical |
| Detector execution | recent cycles | 1835–4732 ms; repeated `PREVIOUS_INVOCATION_RUNNING` misses | existing Matrix producer | P0, material and variable |
| Matrix confirmation | VLESS current required services | continuing confirmed incident and fresh source scope of 3 | existing Matrix | current evidence exists |
| Matrix -> Runtime consumer | live parent observes new profile binding | a new binding was consumed by the normal health owner at 01:11:17; result was not logged in sufficient detail | existing health owner | observability gap |
| Prepared target | live health output | typically 48–216 ms | existing target-preparation owner | not current dominant residual |
| Planner / Authority / Packet / Lease / Barrier / Apply / S11 | current ongoing incident | no exact current timing/result receipt exposed by the health owner | existing governed owners | unmeasured; no conclusion permitted |

The immediate repair frontier is therefore not a manual VLESS recovery. It is
bounded instrumentation of the already-running health owner so every
normal-runtime consumer attempt emits its current Matrix/Planner/Authority/
execution outcome and timing. The first subsequent automatic V7 event will
then establish the complete causal table before a performance repair is made.

## Execution law

Codex may repair code, test, deploy through `tools/v7-safe-deploy`, and read
evidence. Codex must not invoke a user recovery, choose a target, create an
incident/Candidate/Packet/Lease/Barrier, mutate assignments or run the normal
consumer in place of V7. A valid acceptance sample must originate solely from
the live V7 health -> Matrix -> governed execution path.

## Exact next action

Activate this residual through the existing CPS/OMP atomic owner, deploy only
the bounded health-owner timing/result instrumentation after focused tests, and
let the existing live Runtime process the current or next fresh eligible
ordinary failure. Then build the full causal table and repair only the measured
generic P0/P1 residual.
