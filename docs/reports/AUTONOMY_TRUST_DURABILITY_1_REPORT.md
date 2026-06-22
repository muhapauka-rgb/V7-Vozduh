# AUTONOMY.TRUST.DURABILITY.1 Report

Status: implementation complete  
Date: 2026-06-22  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Base commit: `602280a5a2d2e695dd64982abf5f43eec112261c`  
Runtime apply: none  
Users moved: `0`  
Daemon/autoswitch enabled: no  

## 1. Root Cause

Branch 1B proved blast recovery in production with real governed evidence:

- `blast_radius_evidence_count=11`
- `blast_radius_confidence=100.0`
- `trust_score=54.684`
- `users_moved=0`

AUTONOMY.TRUST.BUILDOUT.1 later found the current consumed dry-run had reverted to:

- `blast_radius_confidence=0.0`
- `trust_score=39.582`

The root cause is the normal snapshot refresh input lifecycle, not the blast model. The default refresh path consumed only active JSONL files such as `execution-events.jsonl`, `runtime-trust.jsonl`, `proposal-records.jsonl`, `closure-records.jsonl`, `switch-history.jsonl`, and `rollback-history.jsonl`. Real recovered evidence can live in rotated numeric files such as `execution-events.jsonl.1`. After normal refresh, the active files could be empty while real governed evidence remained in the same store family but outside the consumed path.

Certified interpretation:

```text
Existing governed evidence survived in rotated JSONL stores.
Normal refresh did not consume the full JSONL family.
Recovered blast trust was therefore not durable across refresh/rebuild cycles.
```

## 2. Implementation

Changed existing owner only:

- `tools/v7-intelligence-snapshot-refresh`

Implemented:

- `jsonl_family_paths(path)`
- `read_jsonl_family(path)`
- normal `load_inputs()` now reads active JSONL plus numeric rotated family stores for:
  - audit logs
  - feedback logs
  - switch history
  - rollback history

Ordering is oldest to newest:

```text
execution-events.jsonl.2
execution-events.jsonl.1
execution-events.jsonl
```

This is not a new truth source. It is the same existing evidence store family.

## 3. Changed Files

| File | Change |
| --- | --- |
| `tools/v7-intelligence-snapshot-refresh` | Normal refresh now consumes JSONL family rotations, not only active files. |
| `tests/unit/test_intelligence_workers.py` | Added durability tests for rotated store ordering and refresh/rebuild/reread preservation. |
| `docs/reports/AUTONOMY_TRUST_DURABILITY_1_EVIDENCE/local_rotated_family_durability.json` | Local verification evidence. |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Added canonical trust durability rules. |
| `docs/reference/SYSTEM_MAP.md` | Updated blast-radius materialization owner and evidence lifecycle. |
| `docs/reference/V7_PROJECT_MAP.md` | Updated readiness deltas and changelog. |
| `docs/reference/V7_AUTONOMY_BLUEPRINT.md` | Updated autonomy blueprint with fixed durability path and next phase. |

## 4. Tests

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.unit.test_intelligence_workers` | PASS, 37 tests |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-intelligence-snapshot-refresh admin_core/intelligence_workers.py` | PASS |

Note: `python3 -m pytest tests/unit/test_intelligence_workers.py -q` could not run because `pytest` is not installed in this local environment. The equivalent built-in `unittest` suite passed.

## 5. Verification

Evidence file:

`docs/reports/AUTONOMY_TRUST_DURABILITY_1_EVIDENCE/local_rotated_family_durability.json`

Local lifecycle verification:

| Stage | Blast Confidence | Overall Confidence | Prediction Confidence | Suitability Confidence | Blast Rows | Source Records | Bounded Records |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| after refresh | 100.0 | 53.055 | 47.487 | 62.597 | 1 | 1001 | 1000 |
| after rebuild | 100.0 | 53.055 | 47.487 | 62.597 | 1 | 1001 | 1000 |
| after reread | 100.0 | 53.055 | 47.487 | 62.597 | 1 | 1001 | 1000 |

The test fixture intentionally leaves the active feedback file empty and places the real blast evidence in `execution-events.jsonl.1`. The refresh rebuilds snapshots, writes them, and rereads them. The recovered blast evidence remains visible.

## 6. Metrics

| Metric | Before | After Code Fix |
| --- | ---: | ---: |
| Current consumed blast confidence | 0.0 | local refresh lifecycle preserves 100.0 |
| Branch 1B proven blast confidence | 100.0 | preserved by normal JSONL family refresh |
| Current consumed trust | 39.582 | expected to recover after deployed refresh consumes rotations |
| Branch 1B proven trust | 54.684 | no formula change |
| Users moved | 0 | 0 |
| Runtime apply | false | false |

The code fix does not change thresholds, floors, formulas, planner output, governance, execution, or daemon state.

## 7. Remaining Blockers

| Blocker | State |
| --- | --- |
| Production runtime has not been changed by this report | Runtime deploy/snapshot regeneration is the next operational phase if live API reread is required. |
| Trust floor | Even Branch 1B recovered trust `54.684` remains below `70.0`. |
| Prediction confidence | Still below floor; previous evidence showed the blocker is low forecast/source confidence, not missing matches. |
| Operator comparison evidence | Existing path is present but underfed; comparison count remains below autonomy floor. |
| Event-driven consumer | Still not certified for live apply. |
| Daemon/autoswitch runtime | Still disabled by design. |

## 8. Final Verdict

`TRUST_DURABILITY_FIXED`

Recovered blast evidence now has durable code behavior in the normal snapshot refresh owner: active JSONL plus numeric rotated stores are consumed together, bounded processing still applies, and reread snapshots preserve recovered blast confidence.
