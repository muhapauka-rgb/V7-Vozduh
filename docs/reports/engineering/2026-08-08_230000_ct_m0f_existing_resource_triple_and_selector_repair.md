# CT-M0F: existing-resource triple и repair selector

Дата: `2026-08-08`  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1` (`CT-M0F`)

## Итог

`STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED` был неполной
selector-проекцией, а не доказательством отсутствия controlled substrate.
Read-only production disposition нашёл минимальный existing-resource путь:

```text
one fresh certification identity selected by existing owner
+ isolated failed source `vless`
+ distinct healthy shared Planner target (`awg0`; `awg3` is equivalent class)
= one certification-only CT-M0F triple after selector repair deploy.
```

Identity не захардкожен: existing owner выбирает fresh compatible identity.
Обычный пользователь, assignment, Candidate, Packet и lease не создавались.

## Disposition

| Ресурс | Вердикт |
| --- | --- |
| `vless` | isolated, 40 group-aligned certification identities, 0 ordinary, current service failure: `READY_SOURCE_TARGET_ADAPTER_REPAIR_REQUIRED` |
| `awg0` | healthy `14/14`, shared Planner target, reserve `66`: `TARGET_ADMISSION_REPAIR_REQUIRED_EXISTING_OWNER` |
| `awg3` | healthy `14/14`, shared Planner target, reserve `61`: `TARGET_ADMISSION_REPAIR_REQUIRED_EXISTING_OWNER` |
| `amneziawg-exec-*` | group/source-lineage conflict: `GROUP_BINDING_REPAIR_REQUIRED` |
| `wireguard-*` | ordinary-user overlap: `CONFLICTS_WITH_ORDINARY_USERS` |
| `1` | external peer/key is needed: `PHYSICALLY_UNAVAILABLE` |

The active CT-M0F contract is `ctm0fsdpc_208482a67dc4103e5f0ef7b6`, expires
`2026-09-05T09:32:42Z`, and is certification-only, max one user/concurrent
transaction. Existing `delegated_autonomy_policy` admits
`ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET` with zero ordinary identity and
route delta. Therefore Stage-48 `40 -> 48`, new identity provisioning and new
Authority are not prerequisites for this single sample.

## Repair and tests

`tools/v7-users-autoswitch` now admits a healthy shared target only in
`EXECUTE_CONTROLLED_FAILURE_CUTOVER`, only with current validated delegated
availability policy, capacity/verification/containment gates, and records:
`ACTIVE_AVAILABILITY_FIRST_SHARED_TARGET_ONE_USER`, zero ordinary delta,
forbidden shared-target fault injection, and zero Stage-48 credit.

Focused affected tests and `git diff --check` passed. The Python process emits
only the pre-existing invalid-escape `DeprecationWarning`.

## CPS/OMP and legal terminal

Source CPS still names the historical request-ready `ENGINEERING_AUTHORITY`
state despite the active audited contract. This is an existing
producer-to-consumer gap; it has not been falsified with a documentation-only
write. It must be consumed by the existing atomic CPS/OMP reconciliation owner
in the same deployable repair set.

The repository includes separately reviewed V3/Stage-48 runtime changes. The
actual `tools/v7-safe-deploy --apply` request was rejected before any write by
the independent safety reviewer: its accumulated delta contains the previously
rejected persistent V3 delegated-Authority/identity-provisioning expansion,
not only this CT-M0F selector repair. This cannot be bypassed by a different
deploy mechanism, a policy write or an indirect execution path. No policy
write, Matrix invocation, controlled condition, Candidate, Packet, lease,
route/user mutation, rollback, Authority expansion, L7/L8/Stage-48 credit or
Maturity change occurred.

```text
INDEPENDENT_DEPLOY_SCOPE_APPROVAL_REQUIRED_FOR_CT_M0F_SELECTOR_AND_CPS_RECONCILIATION
```

Re-entry: explicit independent approval of the accumulated deploy scope, or a
new materially smaller deployable package that excludes the V3 expansion.
Only after a passing `tools/v7-safe-deploy` and production caller/consumer
verification may ordinary Matrix create the first fresh CT-M0F sample.
