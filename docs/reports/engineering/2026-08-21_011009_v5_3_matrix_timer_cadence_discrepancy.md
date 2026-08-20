# V5.3: Matrix timer cadence discrepancy

Дата: 2026-08-21 01:10 MSK  
Класс: read-only operational discrepancy.

## FACTS

* Unit configuration: `OnUnitActiveSec=15min`, `RandomizedDelaySec=60s`.
* Runtime read-only status: `v7-service-matrix-refresh.timer` is `active (waiting)`.
* Last visible runtime convergence snapshot: `2026-08-20 22:07:15 MSK`.
* At that snapshot Autoswitch reported `DRY_RUN`, `selected_move_count=0`, `dry_run_intelligence_snapshot_stop_required`.
* No newer successful Matrix generation, `service-matrix.json` freshness, service exit status or next-trigger timestamp is exposed by the current approved read-only command set.

## CONCLUSION

Cadence is configured, but successful execution every 15 minutes is **not proven**. The timer can remain active while the oneshot service is failing, stale, or not producing a new canonical Matrix state. Therefore the missing generation is now an operational-observation gap, not evidence that the Matrix cadence is working.

`STOP_SAFE` remains. No clients, routes, Matrix, Runtime or timers were changed.

## EXACT NEXT ACTION

Existing Runtime/Matrix owner must provide read-only evidence for one cycle:

1. last successful `v7-service-matrix-refresh.service` start/finish and exit code;
2. next timer trigger;
3. current `service-matrix.json` modification/freshness time;
4. service failure/log reason if the cycle is overdue.

Only after a fresh canonical Matrix generation appears should CT-M0F exact-context revalidation and the one-client governed dry-run proceed. Heartbeat continues waiting, but it must treat the timer as **configured-only** until this evidence is available.

