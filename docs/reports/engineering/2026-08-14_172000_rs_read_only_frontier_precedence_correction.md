# RS Read-Only Frontier Precedence Correction

**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`
**Scope:** existing `Continue OMP` selection only
**Runtime / Production / Authority effects:** `NONE / NONE / NONE`

## Problem

The authoritative CPS named the admitted
`RS6_RUNTIME_PACKAGE_MINIMIZATION` frontier and successor
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. A read-only `Continue OMP` run
nevertheless selected an unrelated Polygon product-action obligation because
the generic reconciliation projection did not materialize the RS frontier.
No CPS write occurred in that run.

## Change

`tools/v7_sync_lib.py` now recognizes an existing CPS-admitted RS0–RS6
read-only Mission before generic OMP selection. It returns the exact current
successor to the existing phase owner and ignores `persist_cps`; it neither
changes CPS nor consumes Polygon, product, Runtime, routing or Authority work.

The Program now states the same precedence law. No owner, Program, lifecycle,
truth source, Runtime component or registry was added.

## Validation

`test_omp_program_execution_reconciliation` proves that an RS6 admitted
frontier returns `RS_READ_ONLY_FRONTIER_PREEMPTS_GENERIC_OMP`, preserves the
exact successor and leaves CPS byte-identical even when persistence is
requested.

The existing safe-deploy preflight found only `tools/v7_sync_lib.py` different
from the deployed approved copy. It correctly refused deployment because the
canonical GitHub branch was not readable/aligned for the uncommitted source
candidate. No `--apply` deployment, service restart, Runtime mutation or
Production mutation was performed.

## Before / after / delta

```text
BEFORE: generic Continue OMP could select unrelated Polygon work.
AFTER:  existing RS read-only frontier is acknowledged first.
DELTA:  one precedence guard; one regression test; no state, Runtime or
        production edge changed.
```

## Next frontier

`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION` remains the only current action.
This correction does not complete RS6 or admit a physical simplification
Mission.
