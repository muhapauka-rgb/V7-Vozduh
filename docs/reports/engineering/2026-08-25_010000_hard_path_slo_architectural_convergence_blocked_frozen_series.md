# HARD_PATH_SLO_ARCHITECTURAL_CONVERGENCE_BLOCKED

Date: 2026-08-25  
Terminal: `HARD_PATH_SLO_ARCHITECTURAL_CONVERGENCE_BLOCKED`  
Scope: frozen implementation only; no code, configuration, cadence, priority,
verification, Planner, Matrix or Authority change was made during this series.

## Frozen basis

* Deployed runtime implementation fingerprint:
  `0cef0edf758f504eab000ecd2e5e68118819817aa4585fcd331360531f4e5735`.
* Runtime was independently `RUNTIME_ALIGNED` before the series.  The newer
  local Git commit contained this report documentation only and did not alter
  deployed code.
* One certification-only Polygon identity was used: `10.7.0.92`.
* The existing owners selected the controlled source and each target; no
  target was substituted manually.  Every selected target was `awg3`.
* Each sample completed the existing automatic governed chain:
  controlled condition -> Matrix-backed selection -> Candidate -> Packet ->
  Lease -> Apply -> exact assignment/kernel verification -> required-service
  S11.
* No ordinary identity was used or moved.  Matrix timer state, cadence and
  service configuration were not changed.  Health remained active.

## Valid frozen HARD_PATH distribution

All five rows are functionally valid and remain in the distribution.
`generation` is the distinct owner-backed controlled Matrix/validation
generation bound to the Packet/Lease operation.

| # | generation | kind | T0->decision | decision->Apply | Apply->assignment | assignment->kernel | kernel->S11 | onset->S11 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `ctm0fgen_7a6cbe49b5573330c07bebbd` | cold | 2058.146 ms | 121.361 ms | 362.619 ms | 22.150 ms | 382.897 ms | **2947.173 ms** |
| 2 | `ctm0fgen_3ad8e79b9ab8e432218a3619` | warm | 4137.878 ms | 99.013 ms | 336.666 ms | 16.536 ms | 397.197 ms | **4987.290 ms** |
| 3 | `ctm0fgen_63b5c055e5161d9ab088f42a` | warm | 7310.806 ms | 94.327 ms | 431.251 ms | 21.501 ms | 457.319 ms | **8315.205 ms** |
| 4 | `ctm0fgen_f78be373dd4a6f0b1aceb615` | warm | 2257.431 ms | 82.283 ms | 381.836 ms | 18.217 ms | 393.513 ms | **3133.279 ms** |
| 5 | `ctm0fgen_559060a67f4bbc3b876b7b7d` | warm | 3767.602 ms | 114.798 ms | 564.956 ms | 26.424 ms | 518.254 ms | **4992.034 ms** |

The controlled onset and T0 are the same hard-failure observation in this
contract, therefore onset->T0 is `0.000 ms` for every sample.  The five
bound Matrix-generation fingerprints were also distinct, satisfying the
multi-generation condition without creating a new Matrix owner.

## Acceptance result

Sorted onset->S11 values:

```text
2947.173, 3133.279, 4987.290, 4992.034, 8315.205 ms
```

For five samples, nearest-rank P95 is rank `ceil(0.95 * 5) = 5`:

```text
P95 = 8315.205 ms
```

Result: **FAIL**.

* Required P95 <= 3000 ms: failed.
* Required no valid sample > 5000 ms: failed; sample 3 was 8315.205 ms.
* All samples remained functionally valid and all required S11 semantics
  remained intact.

## Dominant residual and decision boundary

The dominant remaining interval is **T0 -> decision**:

```text
min 2058.146 ms, max 7310.806 ms, range 5252.660 ms
```

All downstream intervals together were comparatively bounded:

```text
decision -> Apply:        82.283..121.361 ms
Apply -> assignment:     336.666..564.956 ms
assignment -> kernel:     16.536..26.424 ms
kernel -> required S11:  382.897..518.254 ms
```

Thus the remaining architectural choice is not a route-write or service-S11
change.  It is whether the failure-confirmed Matrix/Planner decision handoff
must be made precomputed and directly consumable on T0, or whether its
current multi-second generation/reconciliation work is deliberately retained
for safety.  This decision cannot be inferred from one fast run and must not
be replaced by another automatic micro-patch.

## Final runtime state

The final sample closed its transaction and lease; no active controlled
transaction reservation remained.  The controlled source interface was up.
The synthetic identity remained on the Planner-selected recovery target
`awg3`, as expected after the final governed failover.  No ordinary-client
effect was observed.

## Required next action

Stop automatic performance changes.  Owner decision is required on the
smallest architectural question above.  Do not begin Telegram-critical proof,
N10 rollout or N11 until that decision is recorded.
