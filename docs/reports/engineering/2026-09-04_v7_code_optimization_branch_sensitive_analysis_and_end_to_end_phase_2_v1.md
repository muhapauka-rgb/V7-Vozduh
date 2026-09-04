# V7 Code Optimization branch-sensitive analysis and end-to-end Phase 2 (V1)

Date: 2026-09-04
Terminal: `REDUNDANT_LINK_PROVEN_AND_BOUNDED_CLEANUP_COMPLETE`.

## Starting truth and reused owners

The active CPS/product frontier remains `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` / `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`, generation `cpsgen_SFA_RECOVERY_LATENCY_SLO_B95F8C5326E8`. It was neither displaced nor executed.

Reused: existing responsibility-subgraph producer, `tools/v7-truth-check --omp-code-optimization-submit - --json`, evidence/result/review bindings and `mission_completion_evidence_gate`. No owner, Runtime, queue, registry, service, state store or parallel execution path was introduced.

## Reproduced gap and minimal producer extension

Before: the OMP completion domain seeded `tools/v7-truth-check:main`; static closure included all mutually exclusive CLI modes: 179 nodes, 552 edges and 3199 unresolved calls. This contaminated submit-path analysis with non-submit OMP/recovery handlers.

`tools/v7_sync_lib.py` now accepts only the bounded, explicit entry condition `CLI_FLAG:--omp-code-optimization-submit` for this existing domain. It statically selects exactly one matching `if args.omp_code_optimization_submit` body, does not execute code, fails closed if it cannot resolve exactly one branch, and preserves legacy behaviour when no condition is supplied.

After submit-mode slice: 12 nodes, 16 direct edges and 595 local unresolved calls. Non-submit branches are excluded by entry condition, not classified dead or redundant. Focused existing tests plus deterministic repeat passed.

## Semantic clusters and localized uncertainty

| Cluster | Contribution | Classification / disposition |
| --- | --- | --- |
| CLI submit dispatch and stdin/file input | Receives disposable payload and returns JSON/exit terminal | `OBSERVABILITY_ESSENTIAL` |
| Evidence/result/review validation | Rejects unsupported, stale or mismatched submission | `SAFETY_ESSENTIAL` |
| Completion gate | Produces existing legal completion verdict | `SAFETY_ESSENTIAL` |
| File-input path construction | Needed only for file mode | `ESSENTIAL` for file mode; redundant on stdin link below |
| Dynamic calls inside selected slice | Exact dynamic targets not statically resolved | local `UNKNOWN`; re-entry is resolution only for a future proposed mechanism |

There is no dominant aggregate bucket in the selected slice. Every unresolved reference remains local and is not a candidate assertion.

## Candidate, Phase 2 and cleanup

Selected candidate: eager `Path(args.omp_code_optimization_submit)` construction on the stdin (`-`) branch.

Control: valid stdin submitted payload under the original implementation.
Counterfactual: construct `Path` only in the file-input branch.
Required invariants: stdin payload parsing, result/review binding, completion terminal, exit status, file-input missing-path STOP_SAFE and no CPS/Runtime effect.

The eager object had no consumer in the stdin branch; file mode retains its consumer. Control and counterfactual produced equivalent admissible submit behaviour. The link is therefore `REDUNDANT_LINK_PROVEN` only for stdin eager construction, not for file-path validation.

Cleanup: moved `Path(...)` construction under the existing non-stdin branch. This is the only cleanup. It creates no abstraction or state and preserves missing-file handling.

SUBGRAPH BEFORE/AFTER for the responsibility boundary remains 12 nodes / 16 edges: the removed relation was an intra-branch empty construction, not a new architectural edge. Terminal, callers, consumers and local unknowns are unchanged.

## Post-cleanup execution and reviews

Actual non-test CLI execution after cleanup:

```text
tools/v7-truth-check --omp-code-optimization-submit - --json
```

Submitted run `PASS`; completion `COMPLETE_WITH_LEGAL_TERMINAL`; profile and subgraph bindings consumed; result fingerprint `f78d217bd008d65d102df88967b43839d5e5f91c03973bc4086939d089ad797a`; exit code `0`.

- Architecture review: PASS — existing owner only; bounded slice; no infrastructure.
- Safety review: PASS — no Runtime/Authority inference; file and stdin contracts isolated.
- Evidence review: PASS — branch condition, candidate, counterfactual and completion are exact-fingerprint bound.

Focused suites: 28 tests PASS. `git diff --check` PASS.

Mission-owned changed files: `tools/v7_sync_lib.py`, `tools/v7-truth-check`, `tests/unit/test_omp_code_optimization_profile.py`, and this report. Existing unrelated dirty worktree changes were not included.

Effects: CPS `NONE`, Runtime `NONE`, production `NONE`, routes `NONE`, users `NONE`, Authority `NONE`. Source change is one narrowed construction in existing CLI plus the bounded producer extension.

Successor toward repeatable Phase 3: repeat the same branch-sensitive selection only when a new localized, evidence-backed counterfactual hypothesis exists; no broad cleanup campaign is admitted.
