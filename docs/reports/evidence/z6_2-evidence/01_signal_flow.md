# Signal Flow Evidence

## Runtime Signal Owners

| Signal / State | Writers | Readers | Scheduler / Trigger | Runtime Authority |
|---|---|---|---|---|
| `policy.json` | Operator/Admin policy paths | `v7-users-autoswitch`, Admin, observability | Manual/Admin | Hard policy authority. |
| `org-egress-policy.json` | Operator/Admin policy paths | `v7-users-autoswitch`, Admin, observability | Manual/Admin | Tenant policy authority. |
| `service-matrix.json` / refresh summary | `v7-service-matrix-test`, `v7-service-matrix-refresh-all`, `v7-telegram-sentinel` | `v7-users-autoswitch`, Admin, observability | `v7-service-matrix-refresh.timer`, sentinel timer, ad hoc | Live service health signal. |
| `telegram-sentinel.json` | `v7-telegram-sentinel` | `v7-users-autoswitch`, Admin, observability | `v7-telegram-sentinel.timer` every 4s | Fast Telegram advisory/block signal. |
| `egress-quality-summary.json` | `v7-egress-quality-compact` | `v7-users-autoswitch`, Admin, observability | `v7-egress-quality-compact.timer` every 5m | Historical quality signal. |
| `autoswitch-safety.json` | `v7-users-autoswitch` | `v7-users-autoswitch`, Admin, observability | Autoswitch apply cycle | Anti-flap/safety state. |
| `client-reconnect-state.json` | `v7-users-autoswitch`; client observers per catalog | `v7-users-autoswitch`, Admin, observability | Planner/apply observation and external observers | Reconnect/client-experience signal. |
| `egress-load-summary.json` | `v7-users-autoswitch` dynamic load summary; future/optional capacity writers per catalog | `v7-users-autoswitch`, Admin, observability | Planner cycle | Capacity signal. |
| `v7-state.json` | Health/state tooling | `v7-users-autoswitch`, quality compact, Admin | Health/runtime tooling | Current user/egress routing truth snapshot. |
| `egress-speed.json` / `client-speed.json` | Speed/health tooling | `v7-users-autoswitch`, quality compact, Admin | Health/runtime tooling | Performance evidence. |
| `autoswitch-restore-barrier.json` | Historical/manual/governance flows; no single active writer found in current code scan | `v7-users-autoswitch`, Admin restore-settle gate adapters | Restore-governance operations | Restore barrier authority, enforced by autoswitch. |

## Scheduler Evidence

| Unit | Trigger | ExecStart | Role |
|---|---|---|---|
| `systemd/v7-users-autoswitch.timer` | `OnBootSec=2min`, `OnUnitActiveSec=20s` | `v7-users-autoswitch.service` | Starts autonomous runtime plan/apply cycle. |
| `systemd/v7-users-autoswitch.service` | timer | `/usr/local/bin/v7-users-autoswitch --apply` | Primary autonomous execution service. |
| `systemd/v7-telegram-sentinel.timer` | `OnBootSec=30s`, `OnUnitActiveSec=4s` | `v7-telegram-sentinel.service` | Fast Telegram health sampling. |
| `systemd/v7-telegram-sentinel.service` | timer | `/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch` | Writes sentinel state; production unit disables sentinel-triggered autoswitch. |
| `systemd/v7-service-matrix-refresh.timer` | `OnBootSec=2min`, `OnUnitActiveSec=15min`, randomized delay | `v7-service-matrix-refresh.service` | Refreshes service-matrix evidence. |
| `systemd/v7-egress-quality-compact.timer` | `OnBootSec=3min`, `OnUnitActiveSec=5min` | `v7-egress-quality-compact.service` | Compacts historical quality evidence. |
| `systemd/drafts/v7-autoswitch-planner.timer` | `OnBootSec=2min`, `OnUnitActiveSec=30s` | draft planner service | Draft path; not classified as active production owner. |

## Signal Flow Summary

1. Health, service, Telegram, quality, safety, capacity, policy, reconnect, and restore-barrier state are written by multiple specialized tools.
2. `v7-users-autoswitch` ingests these files at planner initialization.
3. `v7-observability-summary` catalogs the intended authority hierarchy:
   hard policy, safety, live service, fast service signal, capacity, client experience, historical quality, runtime verification.
4. Signal ownership is intentionally distributed, but runtime execution authority concentrates inside `v7-users-autoswitch --apply` and manual Admin action endpoints.

## Signal Risks

- Duplicate scheduler risk: live autoswitch timer plus draft planner timer path.
- Duplicate signal-writer risk: service matrix can be influenced by refresh tooling and Telegram sentinel.
- Governance bypass risk: signal files can influence autonomous planner decisions without passing through Admin execution-contract approval.
- Restore barrier writer risk: autoswitch enforces the barrier, but no singular active writer/closer was found.

