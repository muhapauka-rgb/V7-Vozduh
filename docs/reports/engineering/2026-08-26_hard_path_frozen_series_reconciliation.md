# HARD_PATH frozen-series reconciliation

**Date:** 2026-08-26  
**Purpose:** reconcile the current Program/CPS/OMP pointers after the accepted bounded existing-owner corrections and before further evidence collection.

## Reconciled fact

The former `HARD_PATH_SLO_ARCHITECTURAL_CONVERGENCE_BLOCKED` pointer described the superseded fingerprint with an 8.269 s cold result.  It no longer described the deployed Runtime after the accepted persistent-consumer and prepared-projection freshness corrections.

The current deployed performance fingerprint is:

```text
ba7161f5f0eeb959fb193b7ec94370185f686e6ba0fe7d80b695c6727a926cd3
```

Its first valid cold certification-only sample retained the exact route/kernel and required-service checks and recorded:

| Measure | Current result |
| --- | ---: |
| control-plane/kernel cutover | 2696.992 ms |
| failure to decision | 1746.435 ms |
| prepared target validation | 41.150 ms |

This is insufficient for the 3 s P95 conclusion because only one valid cold sample exists.  It is sufficient to replace the historical architecture-blocked pointer with a frozen homogeneous-series frontier.

## State change

- CPS state: `FROZEN_HARD_PATH_SERIES_PENDING`.
- No code, configuration, cadence, priority, verifier, Matrix, Planner, Authority, or route change is permitted during the series.
- Existing owner budget: one valid cold sample, zero warm samples, one owner-backed Matrix generation, zero active reservations and four valid samples remaining.
- Telegram-critical and N10 remain blocked by this evidence gate, not by the superseded architectural blocker.

## Safety and Runtime

`v7-health.service` is active. Standalone Matrix and Telegram timers remain intentionally inactive. The sole certification identity is back on its isolated source; no ordinary identity moved.

## Exact next action

Run four additional functionally valid certification-only samples on the same fingerprint, including at least two warm samples and a second owner-backed Matrix generation. Retain every valid slow sample. Then calculate nearest-rank P95 and either consume the HARD_PATH evidence gate or return a single measured terminal decision.
