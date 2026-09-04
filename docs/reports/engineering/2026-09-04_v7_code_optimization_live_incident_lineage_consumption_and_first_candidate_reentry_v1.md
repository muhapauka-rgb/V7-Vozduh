# V7 Code Optimization: live incident lineage consumption and first candidate re-entry (V1)

Date: 2026-09-04
Mode: read-only incident lineage audit; no recovery, routing, CPS, OMP, source or deployment mutation.

## Outcome

`LIVE_INCIDENT_RECEIPT_BOUND_ZERO_CANDIDATES`

The fresh ordinary service-failure incident was not merely temporally adjacent to an autoswitch. Its immutable governed Packet, execution lease/barrier chain and canonical L3 cohort projection bind it to the same source incident and fresh failure scope. Both ordinary members reached `SUCCESS` with `apply_rc=0`, `verify_rc=0` and `service_verify_rc=0`. The controlled-certification member was outside the two-member execution cohort.

The first lawful Code Optimization gate was then re-entered once, read-only. It selected zero candidates: the live receipt proves recovery behaviour, but does not prove a counterfactual semantic redundancy in any responsibility subgraph. No cleanup phase was started.

## Live evidence ledger

| Required link | Current evidence | Verdict |
| --- | --- | --- |
| Incident -> affected scope | Fresh Matrix event at `2026-09-04T10:43:46.499165Z`; source `1`; `sfinc_d1f8e0179264449d1b9078e6e6df5916`; ordinary `2`, certification `1`, total `3`; scope fingerprint `b7eb6cd009aeb773760dcf8468baa651786976b8cac2946c52c873ab9b17e3f0`. | Bound |
| Authority / Planner -> Candidate / Packet | Immutable Packet `pkt_7dd3d6b3395e4e516cb2be96`, governed operation `govexec_9c327044947f42e13a05fa06`, planner generation `885108afa01f27b578572f632a3ce859ffc3b0d88220bc8ed5c290adf7db93c0`, selected-move hash `410e461c56069cd596c6ddf3ddd94652fa4f9181939eeba3aee3a4be09cb856a`. Its `service_failure_causal_binding` is `BOUND`, references the fresh incident/event and permits exactly two ordinary moves. | Bound |
| Packet -> Lease / Barrier -> Apply | Lease `execlease_496551ab38473632eb93c3d0` was execution-finished; the linked barrier and governance records show rollback binding and `execution_allowed_now=true`; operation terminal is `APPLIED`. | Bound |
| Apply -> per-member route -> required-service S11 | Canonical L3 projection for runtime operation `runtime_autoswitch_2a3c16b0ba365d16e93ddf94`: member count `2`, target `awg3`, `applied_successfully=2`, no contained failure. Each of its two subreceipts has `apply_rc=0`, `verify_rc=0`, `service_verify_rc=0`, `terminal=SUCCESS`. | Bound |
| Certification isolation | The source scope is mixed, but the immutable permitted cohort and canonical completed cohort are both two members; the certification member is not an execution member. No certification reclassification or movement was credited. | Bound |
| Last-member terminal / successor | Canonical cohort state is `SUCCESS`; terminal reason `core_primary_cohort_projection_verified`; durable successor published; next consumer is `tools/v7-users-autoswitch.reconcile_bounded_cohort_closure_obligations`, with re-entry `NEXT_MATRIX_OR_AUTOSWITCH_REENTRY`. | Bound |

The older passive L3 incident projection for the same source incident was deliberately **not** used as the outcome owner: it carried an earlier scope generation and said no Packet lineage had yet been projected. That was a stale/passive observation, not proof of absence of the later immutable Packet and completion receipt.

## Candidate gate after receipt completion

Executed existing read-only consumer:

```text
tools/v7-truth-check --omp-code-optimization-profile-proof --json
```

Result:

- Code-optimization profile admission: `PASS`.
- Canonical service-failure causal spine: revalidated.
- Candidate audit terminal: `INSUFFICIENT_EVIDENCE`.
- `ranked_candidates=[]`; `selected_first_candidate=null`.
- The gate explicitly refuses to infer semantic redundancy from static reachability or from this successful incident receipt.
- CPS, Runtime, production and source-product behaviour: no effect from this gate.

This is the required zero-or-one selection: **zero**, not a deferred refactor disguised as a candidate.

## Reviews

- Architecture review: the existing CPS/OMP/Packet/Lease/Barrier/L3 owners form the lawful recovery chain; no new agent, coordinator, queue, registry or truth owner is admitted.
- Evidence review: fresh incident identity, bounded ordinary scope, immutable Packet binding, governed execution, and both S11 subreceipts agree. Historical reports and passive older projections were not promoted to live truth.
- Safety self-check (local advisory): no runtime command, route change, user movement, restart, CPS/OMP mutation or deployment was issued.
- Self-review (local advisory): the conclusion distinguishes `APPLIED` from S11, and accepts S11 only from the two canonical per-member subreceipts.

## Verification and exact next action

`python3 -m unittest tests/unit/test_omp_code_optimization_profile.py` passed: 6 tests.
`git diff --check` passed.

Exact next action: leave the active Recovery Latency SLO product frontier with its existing successor unchanged; on a later independently evidenced responsibility-subgraph audit, submit at most one candidate only if counterfactual semantic evidence becomes sufficient. Do not run broad cleanup from this incident.
