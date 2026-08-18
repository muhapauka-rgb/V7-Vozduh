# V5.3 target-architecture decision ordering repair

Time: `2026-08-18 13:47 MSK`

Summary: `DECISION_ORDERING_REPAIRED; MODEL_B_NOT_PREDECIDED`

## Ambiguity and reused evidence

Before this repair, commit `643077b4` correctly identified the dominant Matrix
delay and recommended Model B, but V5.3 could be read as if that recommendation
had already selected the final implementation architecture. Phase C had a
comparison terminal, but the A/B/C/D -> E decision dependency and the gate in
front of the first implementation candidate were not machine-explicit.

Reused without repetition:

- read-only Mission `V7_FAILURE_DETECTION_AND_HEALTH_MODEL_OPTIMIZATION_V1`;
- `RECOMMEND_MODEL_B_FAST_PLUS_DEEP_USING_EXISTING_MATRIX_OWNER`;
- existing Phase C commercial benchmark contract and evidence dispositions;
- existing V5.3 owner, lane-independence, lifecycle, Definition of Done and
  retirement contracts.

No evidence shows Phase C/D/E or
`V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1` was admitted, executed or
consumed after the current Program revision.

## Exact correction

- Model B: previous effective meaning `leading recommendation with ambiguous
  finality` -> `STRONG_STANDING_ARCHITECTURAL_HYPOTHESIS` -> not final until
  Phase C/D/E are consumed.
- Added `V5_3_DECISION_ORDERING_LAW`:
  `A -> B -> C -> D -> E -> F/G -> H -> implementation -> measurement`.
- Phase A is a compact reusable comparison baseline, not broad archaeology.
- Phase C rows now require `TARGET_ARCHITECTURE_CONSEQUENCE` and Phase D/E
  consumption.
- Phase D must synthesize V7 reality, failure semantics and mature/commercial
  evidence into one role/stability health-model candidate.
- Phase E is the formal decision gate and emits exactly one bounded model
  verdict plus `V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED`.
- Phase F/G validate the selected architecture and return contradictions to
  Phase E through exact invalidation rather than redesigning silently.
- Phase H starts only after the architecture and relevant scale constraints
  are consumed.
- First candidate is retained but becomes admission-eligible only after the
  Phase E terminal, `FIRST_IMPLEMENTATION_RESIDUAL_CONFIRMED` and matching CPS
  Mission identity.
- Existing terminal criteria now require evidence-backed architecture,
  implementation parity and prohibition of post-hoc benchmark justification.

## Current state and effects

- Program version: `5.3`.
- V5.3: `REGISTERED_BOUNDED_WORKSTREAM`; registration disposition
  `NOT_ADMITTED`; CPS owns live state.
- CPS generation: `cpsgen_RS7_ADMIN_COMPLETE_2A5DA0F2`.
- Current CPS Mission: `V7_OMP_BDP_65CB2232971BC224D937140C_V1`.
- Current successor: `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
- Current V5.3 frontier: no CPS-admitted Phase C/D/E or implementation Mission.
- First candidate: `V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1`,
  retained as leading pending candidate, not executable.
- Next executable action: `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
- Canonical Reference / SYSTEM_MAP changes: `NONE`.
- Runtime / Production / Authority effects: `NONE / NONE / NONE`.

Validation: `git diff --check` PASS; focused RS7 lifecycle, OMP program
reconciliation and truth-check suites: `73 tests, OK`.

## Invalidation and re-entry

Reconcile forward rather than repeat evidence if CPS later consumes any gate.
Re-open an earlier decision only on its named source/owner/consumer drift,
commercial-mechanism contradiction, role/stability mismatch, scale/probe-budget
invalidation, Matrix subset/target-freshness/anti-flap/writer failure or a real
ordinary failover contradiction.

Terminal: `V5_3_TARGET_ARCHITECTURE_DECISION_ORDERING_CONTRACT_REPAIRED`.
