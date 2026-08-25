# HARD_PATH SLO architectural convergence — blocked

Date: 2026-08-25

## Result

`HARD_PATH_SLO_ARCHITECTURAL_CONVERGENCE_BLOCKED`.

The frozen controlled path was functionally valid, including Matrix confirmation, automatic target selection, Candidate, Packet, Lease, Barrier, Apply, route/kernel visibility and required-service S11. It did not meet the performance contract, so no automatic performance patch or further SLO sample was started.

## Frozen implementation and verification

- Source commit: `35a2836f1da2758c6a8175b904a32cd5df4031ac` (`Allow CT-M0F source-only substrate reuse`).
- Focused and V5.3 regression verification: `480` tests passed.
- Actual safe deployment: `deploy-z8-14-Updatesystem-35a2836-20260825T104533`.
- Runtime file checksum equals source: `a89ec6b0204b153194502c637173661c979b9082b9a2af0166f99b0c11d4bb2d`.
- `v7-health.service` is active. Legacy standalone Matrix and Telegram timers are inactive as intended.
- Frozen implementation fingerprint: `3523043275ac5d3c122ed866b7cc8e64bfa64c6a4b7333343fe61c44a46693e2`.

## Controlled Polygon preparation

The isolated execution channel had one stale local-liveness failure row although all 14 service probes passed. The existing Matrix recovery operation closed that row without changing routes. The existing cleanup owner then restored synthetic `10.7.0.92` to the isolated source. A narrowly scoped source-only reuse correction was necessary because CT-M0F deliberately chooses its destination later, while the existing reuse preflight still required a pre-bound destination.

The user-approved Authority record admitted exactly `IDENTITY_PROVISIONING` and `CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT`; it created no identity. The reuse receipt confirms one existing certification identity, zero ordinary users, zero route changes and zero user moves during preparation. Matrix later chose `awg3` itself for the controlled transaction.

## New cold sample

Sample: `ctm0fsample_37d70c26e0f7ac667ae0f61b`  
Generation: `ctm0fgen_f51972cf6ca096b2c57399e6`  
Kind: cold  
Classification: `FUNCTIONALLY_VALID_PERFORMANCE_FAIL`

| Interval | Measured time |
| --- | ---: |
| controlled onset → T0 | 0.000 ms |
| T0 → decision | 7096.819 ms |
| decision → Apply admission | 124.650 ms |
| Apply → assignment | 524.874 ms |
| assignment → kernel path visible | 17.691 ms |
| kernel visible → required-service S11 | 504.575 ms |
| onset → S11 | **8268.609 ms** |

The required acceptance is nearest-rank P95 `<= 3000 ms` and no functionally valid sample `> 5000 ms`. With the first frozen valid sample at `8268.609 ms`, both conditions fail. The path has been safely restored; the synthetic identity is again on `awg3`. No ordinary user was moved.

## Diagnosis

The dominant residual is deterministic failure-to-decision work (`7096.819 ms`, about 86% of the total), with the precomputed-target mutable validation taking `3962.740 ms` and falling back to a safe rejection of both candidate targets before the later governed transaction completes. Apply, route visibility and required-service verification together are below 1.2 seconds. The current record does not establish a CPU/load variance explanation; this single valid cold sample cannot separate stochastic substrate effects from that deterministic validation path.

## Boundary and next step

No further automatic micro-optimization is permitted. The smallest remaining architectural choice is whether the fresh controlled target validation must continue to synchronously perform the observed multi-second fallback/rejection work on the hard path, or whether an existing owner-backed prepared target proof can be consumed with a bounded current-data check that preserves the same S11 safety semantics. The owner must choose and authorize that architecture before a new immutable implementation and a fresh homogeneous five-sample series can begin.

Telegram-critical proof, N10 rollout and N11 work remain blocked by this result.
