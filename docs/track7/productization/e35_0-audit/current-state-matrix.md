# E35.0 Current State Matrix

| Capability | Exists Today | Storage | API/Admin Surface | Runtime Authority | Notes |
|---|---:|---|---|---|---|
| Organization | Yes | Identity DB `organizations` | Пользователи -> Организации | Partial | Identity/admin metadata; links to group. |
| Group | Yes | Identity DB `groups` | Пользователи -> Организации | Partial | Has `route_policy` used for smart mode default. |
| Group route policy | Yes | `groups.route_policy` | Identity controls | Partial | Affects identity/connect smart mode, not full channel constraint. |
| Per-user required services | Yes | `SERVICE_PREFS_FILE` | Пользователи -> Приоритеты | Advisory/partial | Drives service recommendations/proposals. |
| Service matrix | Yes | `SERVICE_MATRIX_FILE` | Каналы -> Сервисная матрица | Partial | Evaluates service availability by channel. |
| Channel suitability | Yes | egress registry + matrix + state | Channels/routes/proposals | Partial | Scoring and guarded flows exist. |
| User current channel | Yes | `users.registry current=` | Users/routes | Yes as current truth | Persistent assignment, not explicit pin. |
| Preferred channel | No clear model | None found | None found | No | Needs E35 design/implementation. |
| User pinning | No clear model | None found | None found | No | `current` is not a pin contract. |
| Per-user AUTO/PINNED/MANUAL | No | None found | None found | No | Existing modes are client/global/channel level. |
| Org channel allowlist/denylist | Partial | `org-egress-policy.json`, egress `organization_scope` | Settings/channel onboarding | Not universal | Needs hard enforcement definition. |
| Autoswitch quality policy | Yes | `POLICY_FILE` | Настройки | Yes for autoswitch tooling | Guarded by policy, safety, restore barrier. |
| Proposal from service mismatch | Yes | generated/store proposals | Главная/Users/Channels/Routes | Non-authoritative | Proposal does not execute. |
| Direct guarantee of service access after selecting required services | No | N/A | N/A | No | Current behavior is recommendation/precheck, not guarantee. |

## Summary

current_state_matrix_complete=true

The system already has many building blocks, but E35 must close the gap between admin expectation and runtime guarantee.
