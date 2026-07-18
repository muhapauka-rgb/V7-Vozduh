Mission ID: `V7_PERMANENT_POLYGON_BOUNDED_REAL_SOURCE_REPAIR_RETURN_V1`
Run Nonce: `V7_PPDT_M5_20260718T173004Z`

# Permanent Polygon Design-Time — Mission 5

Verdict: `PASS_AUTOMATION_PATH_CERTIFIED_REAL_DEFECT_RESIDUAL_PRESERVED`

The bounded chain is installed and checked: minimized counterexample -> classification -> existing BDP admission -> existing OMP Mission -> selective source invalidation -> focused/full tests -> `tools/v7-safe-deploy` -> production caller -> truth/convergence -> same/affected replay.

Certification-only input remains `AUTOMATION_PATH_CERTIFICATION_EVIDENCE` and cannot become a product candidate. A real repair closes only with all required commit/deploy/consumer/replay identities. No current Polygon run found a reproducible natural V7 source defect, so `NATURAL_REPRODUCIBLE_V7_REAL_SOURCE_DEFECT_REPAIR_RETURN` remains an event-driven criterion and did not block Missions 6-8.

Next: `V7_PERMANENT_POLYGON_HISTORICAL_REPLAY_AND_CALIBRATION_V1`.
