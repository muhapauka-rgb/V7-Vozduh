# V5.3 T0–T11 — Stage C candidate failure-matrix Polygon result

Date: 2026-08-21 10:13 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Stage: **C — ordinary-failure path**  
Status: `POLYGON_DRY_RUN_CONTRACT_PROVEN; NO_APPLY`

## What was executed

The new test harness
`tests/unit/test_v5_3_candidate_failure_matrix.py` ran the same controlled
failure matrix for three neutral candidates:

- A: full Matrix;
- B: exact `telegram,google,google_auth` subset under the existing Matrix
  owner;
- C: the same subset with passive escalation through the existing Matrix
  event path.

The response surface was local and ephemeral. The existing Matrix CLI and the
existing pure governed pipeline were invoked. One synthetic ordinary-like
identity (`10.7.0.5`) was used; certification identities were explicitly
excluded by the existing ordinary-scope binder.

## Results

`python3 -m unittest -v tests.unit.test_v5_3_candidate_failure_matrix`:
**5/5 passed**.

For every candidate, the same path reached the existing authority boundary:

```text
T0 failure observation
→ Matrix result
→ existing Planner-bound source/target candidate
→ packet preview
→ restore/rollback preview
→ verification plan
→ outcome/closure plan
→ authority boundary
```

The boundary was intentionally not crossed: `apply_executed=false`,
`users_moved=0`, and no route or Runtime mutation occurred.

Healthy and required-service failure cases were equivalent at the decisive
service:

| Candidate | Healthy result | `google` failure | Selected probes |
| --- | --- | --- | ---: |
| A full Matrix | `OK` | `WARN`, `google=FAIL` | 14 |
| B FAST/DEEP | `OK` | `WARN`, `google=FAIL` | 3 |
| C passive escalation | `OK` | `WARN`, `google=FAIL` | 3 |

## Safety cases proven

1. **Short/full disagreement:** full Matrix failed `youtube` while the short
   subset remained `OK`; the harness marked the result as disagreement and
   required full Matrix as canonical fallback with action disallowed.
2. **Stale state:** stale service-scores produced
   `MISSING_STATE_TRANSITION` with `snapshot_mismatch:service-scores`; apply
   remained forbidden.
3. **Ordinary scope:** a certification identity in the Planner list was not
   selected by the ordinary-service-failure binder.
4. **Passive path:** Candidate C used an event only as an input to the same
   governed pipeline; it did not create a second event or route owner.
5. **Recovery/verification contract:** every candidate produced the existing
   restore/rollback and post-switch verification plans before the authority
   boundary.

## Interpretation

Stage C proves the ordinary-like causal contract and fail-closed behavior in
Polygon. It does **not** prove production client recovery, because the apply
boundary was not crossed and no artificial production failure was created.
It also does not yet choose a winner: A/B/C remain inputs to the scale
tournament.

## Exact next step

Consume this failure-matrix result in Stage D: run the same candidate contract
and metrics at 7, 50, 100 and 1,000 egresses, including probe budget,
resource/lock pressure, stale/conflict behavior and complexity. Then issue the
post-tournament architecture decision.

## Verification and safety

- Focused Stage C harness: `5/5 PASS`.
- Existing Matrix comparison + governed pipeline regression: `56/56 PASS`.
- Loopback listener was used only by the isolated Polygon response surface.
- No production timer, Matrix state, Runtime, route or client changed.
