# P2.8.4 Migration Waves

Project: V7 Vozduh
Block: P2.8.4

## Wave 0: Baseline Capture

- Record branch SHA and Admin API hash.
- Record runtime hash.
- Generate route/function inventory.
- No code changes in P2.8.4; this is a future wave.

## Wave 1: Runtime-Only Read APIs

- Preserve execution summary/contracts/events/timeline/verification/rollback/explain.
- Add tests proving read-only and non-executable behavior.
- Verify no runtime-specific secret/config is copied.

## Wave 2: Draft + Validation Preview

- Add execution draft contract model.
- Add validation gates and preview APIs.
- Ensure fail-closed behavior.

## Wave 3: Simulation + Rollback Preview

- Add outcome, blast radius, service impact, readiness forecast.
- Add rollback preview/impact.
- Verify all outputs remain preview-only.

## Wave 4: Candidate Workflow

- Add candidate list/detail/readiness/risks/explain/timeline.
- Add approval, governance, rehearsal, workflow views.
- Align retention and archive behavior.

## Wave 5: UI Integration

- Integrate drawers/cards/tabs with existing `/admin-v2` patterns.
- Avoid new top-level admin sections unless approved.
- Verify no overlapping or dead UI hooks.

## Wave 6: Tests + Documentation

- Add unit tests.
- Add route inventory evidence.
- Add convergence report and deploy manifest draft.

migration_waves_defined=true
