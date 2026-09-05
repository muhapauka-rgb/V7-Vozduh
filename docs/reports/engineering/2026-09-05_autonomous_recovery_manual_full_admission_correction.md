# Autonomous Recovery — manual FULL admission correction

Date: 2026-09-05
Scope: existing OMP execution profile and isolated Permanent Polygon only
Status: `PASS — SECTION8_FULL_COMPLETION_CONSUMED`

## Cause and correction

The preceding post-acceptance `FULL_CAMPAIGN` returned
`STOP_SAFE_AUTONOMOUS_RECOVERY_ARTIFACT_CONSUMPTION` solely because there was
no new qualifying source-diff receipt. That was an unlawful terminal for an
explicit manual full command: a material change is an admission trigger, not a
manual-full prerequisite.

OMP remains the sole owner of this connection. Its existing bounded
continuation flow now admits exactly three trigger kinds:

- `MATERIAL_CHANGE`: unchanged bytes remain a no-op for this trigger only;
- `MANUAL_FULL`: every compact full command supplies a unique frozen-snapshot
  identity and consumes one bounded Polygon experiment from current CPS;
- `BOUNDED_CADENCE`: an external existing-OMP caller may consume one
  resource-limited cadence slot; a lease and slot identity suppress duplicates.

No coordinator, scheduler, self-wake loop, queue, registry, Runtime owner or
Authority was added. Invalid snapshot identity, invalid cadence budget, stale
CPS, unavailable substrate, active lease, incomplete evidence or failed
background run remain `STOP_SAFE`.

## Verification

- `python3 -m unittest tests.unit.test_autonomous_recovery_agent_profile tests.unit.test_autonomous_recovery_equivalence_certification`
  -> `29` tests `OK`.
- Fresh one-time `tools/v7-truth-check --json AUTONOMOUS_RECOVERY FULL_CAMPAIGN`
  -> artifact
  `docs/reports/evidence/autonomous-recovery-campaign-33349a849d0eb34bc4a30aa8.json`.
- Artifact terminal: `AUTONOMOUS_RECOVERY_SECTION8_FULL_COMPLETION_CONSUMED`;
  all Section 8 outcomes are `true`.
- Existing owner chain observed:
  `tools/v7-truth-check -> tools/v7-autonomous-recovery-bundle ->
  continue_omp_engineering_control_loop ->
  autonomous_recovery_qualifying_material_change_continuation ->
  run_permanent_polygon_bounded_soak`.
  The consumed trigger is `Continue OMP explicit Autonomous Recovery
  frozen-snapshot experiment`.
- Native Analyst, critical Executor and independent Reviewer each returned
  `PASS`. Provenance is correctly limited to
  `ORCHESTRATOR_OBSERVED_NOT_CRYPTOGRAPHIC`.
- Isolated physical Polygon receipts passed at `1,000` and `10,000` members.

## Effect boundary

`runtime_impact=NONE`, `production_impact=NONE`, `authority_impact=NONE`.
This is not proof of Runtime, Production, natural L8 or user effect.

## Next action

No manual re-wake is required after a no-diff full command. A later compact
`FULL_CAMPAIGN` lawfully creates its own frozen snapshot; an external OMP
cadence caller may re-enter only under its bounded slot and single-flight
contract. No commit, push or deploy was performed in this correction turn.
