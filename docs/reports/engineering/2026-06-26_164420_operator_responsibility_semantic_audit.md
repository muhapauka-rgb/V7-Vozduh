# Инженерный отчет: Operator Responsibility Semantic Audit

## Кратко

Аудит определил финальную роль человека-оператора в V7.
Текущая обязанность approve/reject exact packet существует из-за незавершенной производственной зрелости и должна исчезнуть для сертифицированных классов до Production Autonomy.
Постоянная роль оператора: supervision, exception handling, approval of authority/policy boundaries, approval of authority expansion, and accountable override/rejection when V7 stops outside policy.

## Выполненное действие

- Прочитаны OMP, Product Specification, Runtime Model, Canonical Reference, Current Program State и capability framework внутри OMP.
- Выполнено semantic comparison с уже сохраненным world-practice знанием по Google SRE, Cloudflare, Cisco/network operations и Kubernetes.
- Runtime, OMP и код не изменялись.
- Canonical Reference обновлен только durable conclusion о финальной роли оператора.

## Объективные наблюдения

Текущее состояние V7:

- текущий stop: `OPERATIONAL_AUTHORITY`;
- текущий операторский action: approve/reject exact packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc`;
- runtime automation: `NO`;
- current mode: governed TIER_1;
- packet approval: transitional governed fallback;
- target model: Action-Class Authority -> Delegated Autonomy Policy -> Production Autonomy.

## Текущая модель оператора

Сегодня оператор отвечает за:

1. approve/reject exact governed packet while action class remains `GOVERNED_ONLY`;
2. approval before restore-barrier write, runtime apply, user movement, rollback apply, or exact production action;
3. approval or rejection of authority expansion;
4. supervision of OMP stops;
5. exceptional decisions when evidence, safety, policy, rollback, verification, or authority is insufficient;
6. policy and authority decisions that Runtime may not grant to itself.

## Какие обязанности переходные

These exist only because V7 is not fully mature:

- exact packet approval;
- repetitive approval of the same action class;
- manual acceptance of routine one-user governed candidate movement;
- manual review of runtime eligibility for certified low-risk classes;
- manual decision on routine rollback/no-rollback only while rollback class evidence is incomplete;
- repeated operator involvement caused by packet staleness before class/policy authority is certified.

## Какие обязанности должны исчезнуть до Production Autonomy

Before Production Autonomy:

- packet-level approval must disappear for certified classes;
- routine class-level operational decisions must move to Runtime inside approved policy;
- operator should not inspect raw route/probe/packet details for routine certified work;
- operator should not repeatedly approve identical low-risk actions after evidence and authority are certified;
- operator should not be the normal rollback trigger for certified automatic rollback paths.

## Какие обязанности остаются навсегда

Permanent operator responsibilities:

- supervise product operation;
- approve or reject authority expansion;
- approve durable policy boundaries when not already certified by policy process;
- handle exceptions outside policy;
- handle ambiguous or novel failure modes;
- reject unsafe recommendations;
- approve break-glass / emergency policy if such policy becomes explicitly defined;
- remain accountable for business-risk decisions that cannot be inferred from runtime evidence alone.

## Что принадлежит Runtime

Runtime should own:

- consume prepared decisions;
- verify fresh packet/class/policy match;
- check runtime eligibility;
- execute certified actions inside approved policy;
- stop safely outside policy;
- verify results;
- rollback when certified and authorized;
- close outcomes;
- feed learning;
- update Current Program State through existing owners;
- notify OMP.

Runtime must not own:

- product policy expansion;
- authority expansion;
- blast-radius expansion;
- new action-class approval;
- lowering gates;
- business risk appetite;
- operator supervision.

## Что принадлежит Product Owner

Product Owner should own:

- business goals;
- product mission and success criteria;
- SLA and user-priority direction;
- risk appetite;
- durable policy direction;
- approval of product-level changes that alter user/business meaning;
- prioritization when policies conflict at product level;
- decision whether new business scopes belong to V7.

## Сравнение с mature production systems

| System family | Mature pattern | V7 target match |
| --- | --- | --- |
| Google SRE | Humans set SLOs, error budgets, release policies, escalation practice, and incident accountability; automation handles routine deployment/rollback inside guardrails when metrics are reliable. | Matches: operator approves authority/policy; Runtime executes certified bounded work; escalation remains human. |
| Cloudflare | Edge automation operates at scale through health checks, traffic steering, rollout controls, and fast rollback; humans supervise policy, incidents, and exceptional risk. | Matches: V7 target reduces per-action operator work and keeps human review for policy/exception boundaries. |
| Cisco / network operations | Operators define routing policy, device authority, change controls, and rollback safeguards; protocols/controllers act inside declared policy and stop/escalate when authority or safety is missing. | Matches: Runtime acts inside approved policy; operator owns authority and exceptions. |
| Kubernetes | Humans declare desired state and policy; controllers reconcile routine state; RBAC/admission/policy constrain execution; humans intervene for policy, admission failures, or incidents. | Matches: Product Owner/operator set boundaries; Runtime reconciles certified actions or stops safely. |

## Целевая модель

```text
Product Owner
  -> Business Goals
  -> Product Policy / Risk Appetite / SLA Direction
  -> Operator
  -> Authority Boundaries / Exception Decisions / Supervision
  -> OMP
  -> Capability Maturity / Backlog / Promotion Recommendations
  -> Policies
  -> Approved Action Classes / Delegated Autonomy Policy
  -> Runtime
  -> Certified execution or safe stop
  -> Users
```

Responsibility by level:

| Level | Responsibilities |
| --- | --- |
| Product Owner | Business goals, product meaning, SLA priorities, risk appetite, durable policy direction. |
| Operator | Supervision, exception handling, authority expansion approval, policy boundary approval, rejection of unsafe or unclear requests. |
| OMP | Maturity management, backlog selection, certification, authority recommendations, stop classification. |
| Policies | Define allowed classes, safety gates, blast radius, freshness, rollback, verification, learning, stop conditions. |
| Runtime | Execute certified decisions inside approved authority or stop safely. |
| Users | Receive stable connectivity; users do not manage routing. |

## Почему система приняла именно такое решение

Existing product and runtime documents already define packet approval as temporary and delegated policy as the target.
Therefore the correct conclusion is reuse/extend existing owners, not create a new operator-governance model.

## Почему решение считается безопасным

The audit does not change runtime behavior.
It preserves the existing rule that Runtime may not expand authority or act outside approved policy.
The human remains responsible for expansion and exceptions.

## Почему решение считается полезным

It prevents V7 from optimizing the wrong human role.
The product goal is not faster packet approval; it is removing repetitive packet approval through certification, action-class authority, and delegated autonomy.

## Почему система НЕ выбрала альтернативные варианты

No new owner was created because OMP, Product Specification, Runtime Model, Authority Policy, Action-Class Promotion, Current Program State, and Canonical Reference already contain the needed semantics.
No new document was created because this engineering report is historical evidence, not a permanent owner.
No implementation was performed because the task is semantic analysis only.

## Влияние на Runtime

No runtime change.
Target responsibility clarified: Runtime should own routine certified execution inside approved policy and safe stops outside policy.

## Влияние на OMP

No OMP change.
OMP remains the owner for maturity, authority recommendations, and stop classification.

## Влияние на Backlog

No backlog change.
Existing gaps remain in Authority Evolution, Runtime Eligibility, Production Autonomy, Decision Explainability, and related backlog items.

## Влияние на Capability

Relevant capabilities:

- Authority Evolution;
- Production Autonomy;
- Runtime Eligibility;
- Decision Explainability;
- Observability;
- Production Readiness.

## Влияние на Production

No production action occurred.
No runtime automation was enabled.
No users moved.

## Capability Progress

No numeric progress changed.
The audit clarifies that operator-load reduction must come from certified runtime capability, not from repeated manual approvals.

## Backlog Progress

No backlog item was completed.

## Production Maturity

No Production Maturity change.
The conclusion is canonical knowledge, not implementation evidence.

## Canonical Knowledge

Canonical Reference updated:

- final operator role is supervision, policy/authority boundary approval, exception handling, and explicit approval for authority expansion;
- per-packet and per-routine-action approval are transitional maturity constraints;
- Runtime owns routine certified execution inside approved policy;
- Product Owner owns business goals, durable policy direction, risk appetite, and SLA priorities.

## Evidence

Local sources:

- `docs/product/V7_PRODUCT_SPECIFICATION.md`;
- `docs/reference/V7_RUNTIME_MODEL.md`;
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`;
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`;
- `docs/reference/V7_CANONICAL_REFERENCE.md`;
- `docs/policies/POLICY_004_AUTHORITY.md`;
- `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md`;
- `docs/reference/V7_SYSTEM_ARCHITECTURE.md`;
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`.

Runtime mutation: no.
Apply: no.
User movement: no.

## Next Step

Continue OMP from the current A3 `OPERATIONAL_AUTHORITY` state.
If future approval is requested, Decision Explainability should make clear whether the operator is approving a transitional packet, durable class, policy boundary, or authority expansion.

## Re-audit Rule

Do not re-audit operator responsibility unless Product Specification, Runtime authority semantics, Delegated Autonomy Policy, Action-Class Authority, or Production Autonomy target materially changes, or the operator explicitly requests it.
