# E29 Risk Matrix

date_utc=2026-05-29T11:17:46Z
runtime_mutation_performed=false

| Risk | Occurred | Status | Severity Now | Notes |
|---|---:|---|---|---|
| Registry drift | yes | proven mitigated | low | E25.14 failed closed; E25.15 refreshed packet and documented out-of-scope drift user. |
| Target quality drift | yes | partially mitigated | medium | Existing spiky WG target rejected; execution target quality recovered and requalified. Larger scales still require fresh capacity proof. |
| Capacity limits | yes | partially mitigated | medium | Limits increased only after E27.1 and E28.1 validation. Capacity above 4 remains unproven. |
| Rollback complexity | yes | proven mitigated up to 4 users | medium | One, two, and four-user rollback certified; larger rollback sets unproven. |
| Audit complexity | yes | proven mitigated up to 4 users | medium | Audit chain valid; E27.2 contains append-only replay nuance but final DENY_REPLAY is present. |
| Replay complexity | yes | proven mitigated up to 4 users | medium | Replay denial certified at 1, 2, and 4 users. Bulk replay volume remains unproven. |
| Restore-settle complexity | yes | proven mitigated up to 4 users | low | Restore-settle GO after rollback with stable registry, checkers OK, hidden movers absent. |
| Delayed movement risk | yes | proven mitigated up to 4 users | low | Delayed monitoring clean at certified scales. |
| Hidden mover risk | yes | proven mitigated | low | Hidden mover scans absent during critical windows. |
| Autoswitch interference | yes | proven mitigated | low | selected_moves=0 and target autoswitch_allowed=false/rebalance_allowed=false. |

remaining_risks=capacity_and_operational_complexity_above_4_users
risk_level_for_current_certified_scale=LOW
risk_level_for_10_user_next_scale=MEDIUM_UNTIL_CAPACITY_PREPARATION
