# E17 Report And Evidence Survey

## Purpose

E17 creates a read-only operation lineage archive so the operator can answer
what happened without manually opening scattered reports and evidence folders.

## Current Artifact Inventory

| Source | Current role | E17 treatment |
|---|---|---|
| `BLOCK_E*.md` reports | Primary historical operation truth, final answers, mutation statements, verdicts. | Canonical operation backbone. |
| `docs/track7/control-plane/e*-evidence/` | Raw and summarized operational evidence for canary, cohort, restore, generation, delayed movement, reservation, diagnose, and target readiness blocks. | Linked as `EvidenceReference` by operation id prefix. |
| `docs/track7/productization/e*-evidence/` | Productization evidence for E15/E16 and later UI blocks. | Linked for productization operation detail. |
| `docs/track7/productization/e13-*` and `e14-*` | UX, approval contract, observability, lineage, freshness, and API design source. | Historical design evidence. |
| mutation statements | Runtime/user/routing/kill-switch/manual-apply/canary declarations. | Parsed into operation summaries. |
| final answer key/value lines | Readiness, rollback, delayed movement, generation, test, and execution status. | Parsed into lineage fields. |

## Lineage Gaps Found

| Gap | Impact | E17 mitigation |
|---|---|---|
| Reports use different final answer keys across E8-E16. | A single rigid parser would miss old truth. | Parser accepts multiple delayed/rollback/generation key variants and falls back to text classification. |
| Evidence folder naming is not identical to report filenames. | Operation detail could miss evidence. | Evidence lookup extracts block prefix such as `E11_13` and links matching `e11_13-evidence`. |
| Productization evidence lives separately from control-plane evidence. | UI/product blocks could disappear from archive. | Productization evidence path is searched for E13+. |
| Older reports are historical by nature. | Operator might treat old evidence as live truth. | Timeline labels report-backed entries as `HISTORICAL`. |
| Some reports have partial/missing final fields. | Detail view must not crash or invent certainty. | Missing values render as `unknown`. |

## Operation Grouping Rules

1. Operation id is derived deterministically from the report filename without
   the `BLOCK_` prefix.
2. Operation type is inferred from filename/report content:
   - productization;
   - cohort;
   - canary;
   - generation governance;
   - restore;
   - reservation;
   - diagnose;
   - runtime hardening;
   - governance.
3. Evidence folder is linked by block prefix, for example:
   - `E11_13...` -> `docs/track7/control-plane/e11_13-evidence`;
   - `E16...` -> `docs/track7/productization/e16-evidence`.
4. Timeline ordering follows report block order and renders newest first.

## Stale Archive Risk

All report/evidence archive entries are historical. The UI must not display
them as live GO/NO-GO runtime truth. Live status remains in the E15 read-only
runtime overview; E17 provides audit-grade lineage.

## Survey Verdict

The current artifact set is sufficient for a read-only operation lineage archive
if the UI clearly labels report-backed data as historical and missing fields as
unknown.

