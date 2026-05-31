# E35.B Boundary Matrix

| Domain | May Control | May Influence | May Override | May Block | Cannot Override | Cannot Bypass | Must Audit | Must Explain | Must Roll Back |
|---|---|---|---|---|---|---|---|---|---|
| Safety | Forward permission | All movement admission | Everyone for forward denial | All forward movement | none | n/a | Yes | Yes | No, but can require rollback/containment |
| Containment | Emergency escape/rollback scope | Return plan | Operator/Group/User/Autoswitch in emergency | Normal forward action | Safety, kill switch, invalid governance | Safety | Yes | Yes | Yes |
| Governance | Packet-scoped execution | Operator review | Autoswitch, Group, Operator only with explicit override | Out-of-scope movement | Safety | Replay/expiry/hash checks | Yes | Yes | Yes |
| Operator | Pins/manual mode | Group defaults through settings | Autoswitch, User preference | Autoswitch movement | Safety, hard governance deny | Runtime trust | Yes | Yes | If action moved user |
| Group | Allowed/excluded channels, required services | Defaults and preferences | Autoswitch | Group-incompatible movement | Safety, Governance, Containment | Required service/safety | Yes | Yes | No |
| User | Required-service needs/request | Proposals/suitability | none | none directly | all authority domains | n/a | If user input exists | Yes | No |
| Autoswitch | AUTO movement proposals | Candidate ranking | none | Its own selected moves | Safety, Governance, Operator, Group, Containment | hard gates | Yes | Yes | Yes when it moved user |
| Scheduler | Timing/reservation | Execution timing | none | stale/expired scheduled work | all authority domains | execution-time recheck | Yes | Yes | No direct rollback; invokes governed rollback |

## Matrix Verdict

```text
boundary_model_defined=true
boundary_matrix_defined=true
```
