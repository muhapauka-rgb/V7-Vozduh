# Dirty Workspace Map

Date: 2026-06-02

## Modified Files

| Path | Classification | Decision |
| --- | --- | --- |
| `admin/v7-admin-api` | KEEP_COMMIT | Large read-only execution visibility/admin API integration; py_compile passed with `PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache`; no autoswitch apply or runtime mutation performed |

## Untracked Files

`git ls-files --others --exclude-standard` returned 213 paths.

| Group | Count / Examples | Classification | Decision |
| --- | --- | --- | --- |
| Root convergence/productization reports | `BLOCK_*`, `CONVERGENCE_*`, `P2_*`, `PROGRAM_Z8_*`, `RUNTIME_ORCHESTRATOR_REALITY_AUDIT_REPORT.md`, `EXISTING_IMPLEMENTATION_REPORT.md` | KEEP_COMMIT | Project evidence and reports; do not discard |
| Productization evidence docs | `docs/track7/productization/e35_f-autonomous-execution/`, `p2_1-evidence` through `p2_6-evidence` | KEEP_COMMIT | Program evidence; do not discard |
| Runtime convergence truth tooling | `docs/track7/runtime-convergence/V7_TRUTH_MANIFEST.json`, `tools/v7-truth-check`, `tests/unit/test_v7_truth_check.py` | KEEP_COMMIT | Z8.8/Z8.9 truth protocol |
| Candidate workflow test | `tests/unit/test_p2_7_candidate_workflow.py` | KEEP_COMMIT | Covers read-only candidate workflow |
| Z8.5/Z8.7 evidence | `z8_5-evidence/`, `z8_7-evidence/` | KEEP_COMMIT | Required historical convergence evidence |
| Z8.9 evidence/report | `z8_9-evidence/`, `PROGRAM_Z8_9_...` | KEEP_COMMIT | Current remediation evidence |

## Secret Scan

Targeted scan for the supplied password and obvious secret markers did not find the supplied password in dirty files. Matches were limited to public IPs, `root` ownership text, UI labels such as `Пароль`, and code/test terms such as `token`.

## Tests

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7-truth-check admin/v7-admin-api
  PASS

python3 -m unittest tests/unit/test_v7_truth_check.py tests/unit/test_p2_7_candidate_workflow.py
  PASS, 15 tests
```
