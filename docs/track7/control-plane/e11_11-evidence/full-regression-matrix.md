# E11.11 Full Regression Matrix

regression_matrix_completed=true

| Check | Evidence | Result |
|---|---|---|
| WireGuard target still clean | `current-target-readiness.txt`: WireGuard zero-user and selected target | YES |
| No reassignment | `current-autoswitch-plan.pretty.json`: `selected_moves=0` | YES |
| No delayed movement | `current-restore-settle-gate.txt`: movement counts `[0,0,0]` | YES |
| No hidden movers | `full-governance-snapshot.txt`: hidden process scan empty | YES |
| No restore regression | restore-settle default after fix returns `GO` | YES |
| No diagnose regression | targeted diagnose tests pass; live diagnose state has WireGuard and AWG OK | YES |
| No AWG regression | runtime checkers OK for AWG routes; targeted diagnose tests pass | YES |
| No target readiness regression | default target readiness returns WireGuard `GO` with execution disabled | YES |
| No autoswitch regression | targeted autoswitch policy tests pass; current plan selected moves zero | YES |
| No runtime checker regression | reconcile, route, kill switch, provisioning all rc=0 | YES |
| Runtime/repo lineage unchanged risk | runtime/repo diff remains `partial` with lineage gaps | NO_REGRESSION_EXISTING_PARTIAL_LINEAGE |

regressions_observed=false
