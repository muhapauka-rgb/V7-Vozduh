# V7 Code Optimization dominant UNKNOWN decomposition and Phase-2 entry gate (V1)

Date: 2026-09-04
Mode: read-only Engineering-plane audit; source changes `NONE`.

## Current truth and terminal

Current CPS/product frontier remains `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` / `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`, generation `cpsgen_SFA_RECOVERY_LATENCY_SLO_B95F8C5326E8`, transition `RECOVERY_LATENCY_SLO_PRODUCT_CONTRACT_REENTRY_V1`. It was not displaced or executed.

Terminal: `STOP_SAFE_NO_ISOLATED_COUNTERFACTUAL_CANDIDATE_AFTER_SEMANTIC_DECOMPOSITION`.

The existing Code Optimization CLI, evidence package, review binding and `mission_completion_evidence_gate` were reused unchanged. No owner, runner, schema, queue, registry or source behaviour was added.

## Decomposition finding

The prior 147-node / 434-edge shared bucket was not accepted as a semantic group. Fresh derivation showed the decisive structural cause: the domain seed is `tools/v7-truth-check:main`; its AST closure includes mutually exclusive branches for all command-line modes, including unrelated OMP, reconciliation and Runtime-adjacent command handlers. They are reachable from the monolithic parser/dispatcher source, but they are not proven consumers of `--omp-code-optimization-submit`.

This is not one generic dynamic-target issue. It is a localized branch-sensitivity gap in the existing derived-evidence producer.

| Cluster | Status | Exact missing fact / disposition | Re-entry |
| --- | --- | --- | --- |
| Actual submit CLI parse/dispatch/render | `OBSERVABILITY_ESSENTIAL` | Shell caller -> submit result -> JSON/exit terminal is observed | Repository fingerprint changes |
| Evidence/result/review/completion path | `SAFETY_ESSENTIAL` where owner-backed | Current completion consumer rejects mismatches | Repository fingerprint changes |
| Non-submit CLI branches | `OUT_OF_DOMAIN_WITH_REASON` | No argument-conditioned caller proof from `--omp-code-optimization-submit` | Existing producer derives a submit-flag branch slice |
| Transitive OMP/recovery handlers pulled from `main` | local `UNKNOWN` | Same branch-sensitive closure missing; no submit-mode consumer | Same slice, then fresh caller/consumer audit |
| Unresolved static calls | local `UNKNOWN` | 3199 exact unresolved/ambiguous call records, not a redundancy assertion | Resolve only the records inside the future submit slice |

The required quality gate therefore cannot pass: node/edge accounting is possible, but a large included set is demonstrably out of the submitted-result responsibility rather than semantically analysed. A Phase-2 candidate would be artificial.

## Actual CLI evidence

Executed through the existing non-test caller:

```text
tools/v7-truth-check --omp-code-optimization-submit - --json
```

- Mission/run: `V7_CODE_OPTIMIZATION_DOMINANT_UNKNOWN_DECOMPOSITION_AND_PHASE_2_ENTRY_GATE_V1` / `unknown-decomposition-v1`.
- Evidence fingerprint: `61cc441e8fcf25baefcc04863c1dc1dd0a5e745b14bb02af1ef6654200b01e00`.
- Result fingerprint: `c76a3452af21792394df747a9a73b8951abad1abbb498148edbdb655a0bdcf45`.
- Architecture/Evidence reviews: separate contexts, exact output binding, PASS.
- Submitted-run: `PASS`; completion `COMPLETE_WITH_LEGAL_TERMINAL`; execution-profile and subgraph bindings consumed; CLI exit code `0`.
- Result terminal: `INSUFFICIENT_EVIDENCE`, intentionally mapped by this Mission to the more precise outer STOP_SAFE above.

## Counterfactual / candidate gate

No hypothesis was ranked. Candidate `null`.

The actual CLI branch, evidence validation and completion gate each add an observed caller, a fail-closed safety boundary or a terminal consumer. Non-submit branches must not become deletion hypotheses because their inclusion is a static-dispatch artefact, not proof of current consumption or absence of contribution.

## Exact owner, action and re-entry

Missing capability: an argument-conditioned bounded slice within existing `derive_responsibility_subgraph`, for exactly `--omp-code-optimization-submit` dispatch. Existing owner: `tools/v7_sync_lib.py` responsibility-subgraph producer. Last proven output: complete read-only submitted run and a branch-insensitive static closure. Expected consumer: the existing Code Optimization submitted-result path. Minimal action: add a focused branch-slice derivation only after a reproduction test proves that non-submit branches contaminate this domain; do not add a graph service or registry. Re-entry condition: fresh submit-mode-only node/edge closure, followed by a new semantic decomposition and candidate gate.

Effects: CPS `NONE`, Runtime `NONE`, production `NONE`, route/user/Authority `NONE`; cleanup `NONE`.
