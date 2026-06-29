# Continue OMP C6 Bounded Stale Allowance

Status: `COMPLETE`
Date: `2026-06-29T19:00:00+0700`
Task: `C6_DECIDE_BOUNDED_STALE_ALLOWANCE_BY_ACTION_CLASS`

## Discovery

Existing owners reused:

- Freshness actionability.
- Action-class freshness windows.
- B17 stale-read mutation blocking.
- B18 owner-issued version/lease pattern.
- C1 fail-open/fail-closed action-class behavior.
- A6 runtime eligibility arbitration.
- OMP stop rules.

No new Runtime, Planner, owner, truth source, roadmap, authority, automation, synthetic evidence, or user movement was created.

## Implementation

Implemented `bounded_stale_allowance_by_action_class` in `admin_core.autonomy_trust_acceleration`.

Decision:

- stale/unknown evidence may be observed, diagnosed, and reported;
- stale/unknown evidence has `0` mutation allowance;
- fresh evidence inside existing action-class windows is required before mutation review;
- owner-issued version/lease evidence is preferred where already available;
- no freshness windows, thresholds, formulas, lease behavior, Runtime behavior, or authority changed.

## Canonical Updates

Updated:

- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/policies/POLICY_008_FRESHNESS.md`

Current OMP step is now `C7_MAP_POOL_MAX_EJECTION_MINIMUM_HEALTH_SEMANTICS_TO_V7_CAPACITY_AND_BLAST_BOUNDS`.

## Verification

Passed:

- `python3 -m py_compile admin_core/autonomy_trust_acceleration.py`
- targeted C6 unit tests
- canonical consistency scan for stale C6-current metrics

## Result

Production Maturity: `66.0 / 100`.
Backlog: `33 / 34 actionable complete`.
Tier C: `6 / 7 complete`.

Final verdict: `CONTINUE_OMP_C6_COMPLETE`
