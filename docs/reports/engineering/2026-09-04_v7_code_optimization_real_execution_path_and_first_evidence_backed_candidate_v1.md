# V7 Code Optimization real execution path and first evidence-backed candidate (V1)

Date: 2026-09-04
Mode: Engineering-plane source contract extension and read-only verification. No CPS, Runtime, production, route, user, Authority or deployment effect.

## Current state and terminal

Current CPS: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`; generation `cpsgen_SFA_RECOVERY_LATENCY_SLO_B95F8C5326E8`; transition `RECOVERY_LATENCY_SLO_PRODUCT_CONTRACT_REENTRY_V1`; active frontier and safe next action remain `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE` / normal health-caller S11 sample.

Terminal: `STOP_SAFE_NO_ISOLATED_EVIDENCE_RICH_DOMAIN`.

This Mission did not alter or execute that product frontier. The previously proved incident receipt remains an owner-backed control receipt, not a general semantic-optimization input.

## AS-IS and proven gap

`bounded_code_optimization_contract_proof` is retained as an explicit negative contract self-test: it derives the recovery pilot subgraph, deliberately publishes an empty hypothesis/candidate list and proves the completion guard accepts the legal `INSUFFICIENT_EVIDENCE` terminal. It is not an actual optimization execution.

Existing OMP owners already provide admission (`admit_execution_profile_contract`), result identity, Architecture/Evidence review binding (`execution_profile_completion_binding`), responsibility-subgraph binding and the existing `mission_completion_evidence_gate`. The missing capability was a disposable, immutable evidence package and a submitted-result path which verifies evidence references before that existing gate consumes the result.

## Minimal extension

Changed only existing owners:

- `tools/v7_sync_lib.py`
  - added a bounded second subgraph configuration for `OMP_EXECUTION_PROFILE_COMPLETION_LIFECYCLE`; this is an explicit fixed branch, not a domain registry or graph service;
  - added `code_optimization_evidence_package` and fail-closed `validate_code_optimization_evidence_package`;
  - added `submit_code_optimization_result`: Codex/external reasoning supplies classifications and hypotheses; deterministic code validates identity, freshness, evidence IDs, mandatory candidate Control/Counterfactual fields, reviews and the existing completion consumer;
  - evidence classes distinguish static source, caller/consumer, state/process, replay, controlled/production receipt, compatibility and historical evidence. The package is disposable and creates no store.
- `tests/unit/test_omp_code_optimization_profile.py`
  - adds an honest-zero submitted-result fixture through the new path, and confirms a changed expiry/fingerprint fails closed.

The actual submitted path refuses non-`UNKNOWN` classifications without evidence IDs, candidates without caller/consumer/Control/Counterfactual/proof plan, and an honest zero without considered mechanisms. It grants no cleanup authority.

## First-domain discovery and stop-safe boundary

The active recovery pilot remains excluded: it conflicts with the active Recovery Latency WIP and static source is insufficient to treat its live receipt as a refactoring conclusion.

The only new isolated OMP-domain producer configuration that can currently satisfy the bounded static generator is `tools/v7-truth-check:selected_mode`. It has no independently proven current caller, consumer, state effect or meaningful Control/Counterfactual cleanup path. It is therefore neither an evidence-rich repository domain nor a legitimate first candidate. The positive unit fixture proves schema/validator mechanics only and is explicitly not counted as the requested real run.

Missing fact: an existing-owner-produced, bounded responsibility subgraph for one non-recovery current domain containing proven caller and consumer evidence plus a reviewable counterfactual. Responsible owner: existing `derive_responsibility_subgraph` / OMP engineering-evidence owner. Last proven output: a bounded source-only OMP CLI seed. Expected next consumer: this submitted-result entrypoint. Minimal next action: extend that existing producer for exactly one chosen non-recovery domain after its concrete callers and consumers are discovered; no registry, background scan or new owner. Re-entry condition: the derived package has fresh, owner-backed caller/consumer evidence and a bounded reversible counterfactual.

## Reviews and verification

- Architecture: no new Agent System, Coordinator, Program, Planner, queue, Runtime or durable evidence registry; existing OMP completion gate remains terminal consumer.
- Safety: package expiry, identity/fingerprint mismatch and unsupported candidate fields fail closed; source analysis cannot grant Runtime or cleanup authority.
- Evidence: static evidence is labelled static and does not establish Runtime/production semantics; historical reports were not used as current truth.
- Self-review: old zero self-test remains separately named; no fixture was presented as a repository candidate; no file size became a verdict.

`python3 -m unittest tests/unit/test_omp_code_optimization_profile.py`: PASS (7 tests).
`git diff --check`: PASS.

Effects: source contract only; CPS `NONE`, Runtime `NONE`, production `NONE`, Authority `NONE`, routes `NONE`, users `NONE`. No candidate selected; no cleanup executed.
