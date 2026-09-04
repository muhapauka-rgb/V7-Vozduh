# V7 CODE_OPTIMIZATION FULL_BASELINE

Date: 2026-09-04
Terminal: `CODE_OPTIMIZATION_FULL_BASELINE_CONSUMED`

## Starting truth

CPS retained active Program
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`, active product frontier
`V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`, generation
`cpsgen_SFA_RECOVERY_LATENCY_SLO_B95F8C5326E8` and transition
`RECOVERY_LATENCY_SLO_PRODUCT_CONTRACT_REENTRY_V1`.

`FULL_BASELINE` did not previously exist as an execution command. OMP applied a
`LOCAL_EXECUTION_ADAPTATION`: “full” means every currently admitted bounded
responsibility domain, not an unbounded whole-repository graph. Objective,
owner/effect boundaries and Code Optimization Definition of Done were preserved.

## Consumed baseline

The existing responsibility-subgraph producer, `CODE_OPTIMIZATION` profile,
immutable submit/review binding and `mission_completion_evidence_gate` consumed
three current domains:

| Domain | Entry condition | Nodes | Edges | UNKNOWN refs | Completion |
| --- | --- | ---: | ---: | ---: | --- |
| `ORDINARY_SERVICE_FAILURE_GOVERNED_RECOVERY_EXECUTION` | `NONE` | 34 | 58 | 439 | `COMPLETE_WITH_LEGAL_TERMINAL` |
| `OMP_EXECUTION_PROFILE_COMPLETION_LIFECYCLE` | `CLI_FLAG:--omp-code-optimization-submit` | 15 | 20 | 736 | `COMPLETE_WITH_LEGAL_TERMINAL` |
| `OMP_CODE_OPTIMIZATION_MATERIAL_CHANGE_BRIDGE` | `CLI_FLAG:--continue-omp-change` | 110 | 301 | 1606 | `COMPLETE_WITH_LEGAL_TERMINAL` |

Baseline fingerprint:

`7e0c5f9c8360ab4429e93a8d6e0b56f5504670f6abd3718fc8342cec9c6f26b4`

Each domain passed Architecture, Safety Regression, Evidence and
Quality/Complexity review. The baseline is derived, disposable Engineering
evidence; no persistent graph or new truth owner was created.

## Structural signals

Recovery scope baseline: 5 files, 49,094 executable LOC, 721 functions, 3,609
branch nodes, one systemd surface. The largest hotspot is
`controlled_source_topology_diagnostic` at 2,312 LOC.

OMP completion/bridge source scope: 2 files, 31,750 executable LOC, 405
functions and 1,953 branch nodes. The largest hotspot is
`reconcile_active_standing_delegated_policy_to_cps` at 2,200 LOC; the current
OMP loop is 1,104 LOC.

These metrics are signals only. They do not prove redundancy or authorize a
refactor. State surfaces, locks/leases, process hops, durable/history reads,
compatibility paths and runtime behavior remain explicitly
`UNKNOWN_NOT_DERIVED` where the current producer cannot prove them.

## Actual caller and consumer

Executed command:

```text
tools/v7-truth-check --omp-code-optimization-full-baseline --json
```

All three profile results were consumed by the existing
`mission_completion_evidence_gate`. No candidate was selected because baseline
capture is structural evidence, not counterfactual semantic proof.

## Validation and effects

- Focused profile/subgraph/Mission-integrity suite: 55/55 PASS.
- Repeated actual command produced the same baseline fingerprint.
- CPS bytes unchanged.
- Runtime impact: NONE.
- Production impact: NONE.
- Authority impact: NONE.
- Product frontier displacement: NONE.

## Mission-owned files

- `tools/v7_sync_lib.py`
- `tools/v7-truth-check`
- `tests/unit/test_omp_code_optimization_profile.py`
- this Engineering Report

## Honest residual and successor

`FULL_BASELINE` is complete for the admitted domain set. It is not a claim of
full repository semantic understanding. The baseline intentionally ends with
zero selected candidates and preserved UNKNOWN facts.

The next Code Optimization action, when explicitly requested or triggered by a
qualifying material change, is bounded hypothesis and counterfactual work
inside one admitted responsibility domain. The active product successor remains
the existing CPS-owned
`V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`.
