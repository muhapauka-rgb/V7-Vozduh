# Инженерный отчет: Business Intent Model Semantic Audit

## Кратко

V7 уже содержит Business Intent Model, но не под отдельным названием.
Семантически он живет в `V7_PRODUCT_SPECIFICATION.md` как Product Mission, Product Principles, Ideal User Experience, Product Success, Evolution Domains, Action-Class Authority, Delegated Autonomy Policy, SLA/service/user fit и final product behavior.

Вердикт: `EXTEND_EXISTING`.
Need New Owner: `FALSE`.
Need New Document: `FALSE`.

## Выполненное действие

- Выполнен semantic audit по OMP, Product Specification, Runtime Model, Canonical Reference, System Architecture, Production Maturity Model, Current Program State, SYSTEM_MAP, Policy Library и ADRs.
- Runtime не изменялся.
- OMP не изменялся.
- Product Specification не изменялся.
- Код не изменялся.
- Canonical Reference обновлен только durable conclusion о владельце Business Intent.

## Объективные наблюдения

Business Intent уже представлен в V7 через существующие понятия:

- Product Mission: keep users connected, choose safe routes, avoid unnecessary movement, recover from failure, learn from reality.
- Ideal User Experience: user uses Telegram, YouTube, ChatGPT, browser, and never thinks about VPN.
- Product Success: users stay online, failures recover, switches are invisible, operator workload shrinks.
- Product Principles: Reality First, User Connectivity First, Minimal Operator Work, Safety Before Movement, Learning From Reality, Event-Driven Operation, Simple Authority.
- Delegated Autonomy Policy: operator approves policy boundaries; Runtime acts only inside them.
- Service/user/SLA fit: existing read-only model for whether a channel fits this user and service need.
- Evolution Domains: Runtime Intelligence, Knowledge Evolution, Progressive Autonomy, Scale Evolution, Operational Excellence, Platform Evolution.

## Semantic Findings

### 1. Does V7 already define business intent?

Yes.
It defines business intent as product-level outcomes rather than a separate technical object:

- stable access;
- safe routing;
- verified learning;
- lower operator burden;
- maximum continuity for users;
- bounded safety;
- progressive autonomy;
- policy-bound execution.

### 2. Where is it owned?

Primary owner:

```text
docs/product/V7_PRODUCT_SPECIFICATION.md
```

Supporting consumers / translators:

- OMP: turns product intent into implementation priority, maturity, backlog, and authority recommendations.
- Policies: translate intent into operational constraints.
- Runtime Model: executes or stops using already translated policies and gates.
- Service/user/SLA fit: translates intent into read-only routing suitability evidence.
- Current Program State: stores current volatile operational need and stop/authority state.

### 3. Is Product Specification already the owner?

Yes.
Canonical Reference already says Product Specification is the highest-level product specification and that architecture, OMP, Runtime, implementation, research, reports, and ADRs derive product meaning from it.

### 4. Does OMP already consume business goals?

Yes, indirectly.
OMP consumes business goals as:

- production leverage;
- maturity progress;
- backlog priority;
- authority recommendations;
- autonomy promotion;
- operator workload reduction;
- current highest leverage action.

OMP does not need a new owner.
If a visible Business Intent field is needed later, OMP and Current Program State should reference Product Specification and policy outputs.

### 5. Does Runtime already consume business goals indirectly?

Yes.
Runtime consumes business intent only after translation into:

- policies;
- action classes;
- runtime eligibility gates;
- SLA/service/user fit;
- safety gates;
- rollback/no-rollback requirements;
- freshness;
- blast radius;
- authority bounds;
- verification and learning requirements.

Runtime must not consume raw Product Owner preferences directly.

### 6. Is Business Intent represented under another name?

Yes.
Equivalent existing names:

| Business Intent concept | Existing V7 name |
| --- | --- |
| Maximum Stability | Movement Protection, Anti-Flap, Recovery Admission, State Change Cost |
| Fastest Recovery | Hard Failure, Rollback, Recovery Admission, Runtime Eligibility |
| Lowest User Disruption | User Connectivity First, Stickiness, Minimum Improvement Threshold, Movement Protection |
| Highest Service Availability | Service/user/SLA fit, Soft Degradation, Hard Failure, Freshness |
| Lowest Business Risk | Safety Before Movement, Blast Radius, Authority Evolution |
| SLA Priorities | Service/user/SLA fit, cohort/SLA views, policy gates |
| Business Risk Appetite | Delegated Autonomy Policy, Authority, Blast Radius, production maturity gates |
| Desired User Outcome | Ideal User Experience, Product Success |
| Product Constraints | Product Principles, Canonical Policy Library, Runtime forbidden actions |

## Responsibility Model

| Level | Responsibility |
| --- | --- |
| Product Owner | Defines business goals, desired user outcomes, SLA priorities, risk appetite, product policy direction, and product constraints. |
| Operator | Supervises production, approves policy/authority boundaries, handles exceptions, rejects unsafe/unclear requests, approves authority expansion. |
| OMP | Converts product intent into production leverage, backlog priority, maturity tracking, authority recommendations, and stop classification. |
| Policies | Translate intent into operational rules: freshness, rollback, blast radius, anti-flap, recovery, authority, promotion, hard/soft failure. |
| Runtime | Executes certified decisions inside approved policy or stops safely; it does not interpret business strategy directly. |
| Users | Experience stable connectivity and should not manage routes, packets, or policy. |

## Target Model

```text
Product Owner
  -> Business Intent
  -> Policies
  -> OMP
  -> Runtime
  -> Users
```

Expanded:

```text
Product Owner
  -> Maximum Stability / Fastest Recovery / Lowest User Disruption
  -> Highest Service Availability / Lowest Business Risk / SLA Priorities
  -> Product Policy and Risk Appetite
  -> Canonical Policies and Action Classes
  -> OMP priority, certification, promotion, authority recommendation
  -> Runtime eligibility and certified execution
  -> Users stay online
```

## Product Owner Model

Product Owner should define:

- Maximum Stability;
- Fastest Recovery;
- Lowest User Disruption;
- Highest Service Availability;
- Lowest Business Risk;
- SLA Priorities;
- Business Risk Appetite;
- policy direction;
- product success criteria.

Product Owner must not be required to understand:

- packets;
- routing algorithms;
- blast-radius internals;
- rollback internals;
- planner implementation;
- runtime implementation;
- protocol engineering.

## Runtime Model

Runtime translates Business Intent only after Product/Policy/OMP have turned it into executable constraints.

Runtime should see:

- allowed action class;
- approved policy;
- max users / blast radius;
- freshness requirements;
- rollback/no-rollback requirements;
- verification requirements;
- anti-flap status;
- service/user/SLA fit;
- stop conditions.

Runtime should not see:

- raw business strategy;
- subjective product priorities;
- operator preference text;
- unapproved policy expansion.

## Reuse Analysis

Existing owner:

```text
docs/product/V7_PRODUCT_SPECIFICATION.md
```

Existing sections:

- Product Mission;
- The Ideal User Experience;
- Product Principles;
- What Success Looks Like;
- The Final Product;
- Autonomy Promotion Engine;
- Delegated Autonomy Policy;
- Evolution Domains;
- Technical Appendix: Knowledge, Runtime, Autonomy, Scalability.

Fields to extend if a visible Business Intent section is later requested:

- `stability_goal`;
- `recovery_goal`;
- `user_disruption_goal`;
- `service_availability_goal`;
- `business_risk_appetite`;
- `sla_priorities`;
- `policy_constraints`;
- `operator_authority_boundary`;
- `runtime_translation_path`.

Implementation path if later approved:

1. Extend existing Product Specification in place.
2. Keep OMP as consumer of product intent through production leverage and backlog priority.
3. Keep policies as translation layer from business language to operational gates.
4. Keep Runtime as executor of policy-bound certified decisions only.
5. Expose read-only Business Intent mapping through existing operator/policy/read-model surfaces if needed.

No new owner is needed.
No new document is needed.

## Comparison With ADRs And Policies

Relevant ADRs confirm reuse:

- `ADR-V7-DELEGATED-AUTONOMY-POLICY`: operator approves policy boundaries; V7 acts inside them.
- `ADR-V7-ACTION-CLASS-AUTHORITY`: durable approval object is Action Class, not packet.
- `ADR-EVENT-DRIVEN-AUTONOMY`: product intent rejects timer-only movement.
- `ADR-V7-SERVICE-USER-SLA-FIT-MODEL`: service/user/SLA fit exists as read-only routing foundation.

Relevant policies confirm translation:

- hard failure protects availability;
- soft degradation handles quality/SLA impairment;
- recovery admission protects stability after recovery;
- authority separates execution from expansion;
- action-class promotion reduces repetitive approval;
- blast radius controls business risk;
- rollback protects reversibility;
- freshness prevents stale mutation;
- anti-flap protects stability.

## Почему система приняла именно такое решение

Product Specification already owns product meaning, and Business Intent is product meaning.
Creating a new Business Intent owner would duplicate the product specification and weaken the existing Product -> Policy -> OMP -> Runtime chain.

## Почему решение считается безопасным

This audit changes no Runtime behavior, no OMP behavior, no Product Specification text, no code, no authority, no apply path, and no users.
The canonical update only prevents future duplicate-owner creation.

## Почему решение считается полезным

It makes clear that V7 should not ask Product Owner to reason about packets, routing algorithms, rollback internals, or protocol details.
Business goals must be translated into policies and certified runtime gates.

## Почему система НЕ выбрала альтернативные варианты

`CREATE_NEW` was rejected because Product Specification already owns product intent.
New owner was rejected because OMP, Policies, Runtime Model, Service/user/SLA fit, and Current Program State already cover the translation path.
New document was rejected because the correct durable location is the existing Product Specification if future extension is needed.

## Влияние на Runtime

No Runtime change.
Target rule clarified: Runtime consumes Business Intent only after it is translated into policies, action classes, eligibility, safety, rollback, freshness, blast-radius, verification, learning, and authority gates.

## Влияние на OMP

No OMP change.
OMP already consumes product/business intent as production leverage, maturity, backlog priority, authority recommendation, and autonomy progression.

## Влияние на Backlog

No backlog change.
Future implementation may add read-only mapping if needed, but no new backlog item was created in this audit.

## Влияние на Capability

Relevant capabilities:

- Authority Evolution;
- Runtime Eligibility;
- Production Autonomy;
- Movement Protection;
- Decision Explainability;
- Observability;
- Production Readiness.

## Влияние на Production

No production action.
No runtime automation enabled.
No authority expanded.
No users moved.

## Capability Progress

No progress changed.
This audit is semantic only.

## Backlog Progress

No backlog progress changed.

## Production Maturity

No Production Maturity change.

## Canonical Knowledge

Canonical Reference updated:

Business Intent is semantic reuse of Product Specification ownership.
OMP, policies, and Runtime are consumers/translators/executors, not new business-intent owners.

## Evidence

Read sources:

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`;
- `docs/product/V7_PRODUCT_SPECIFICATION.md`;
- `docs/reference/V7_RUNTIME_MODEL.md`;
- `docs/reference/V7_CANONICAL_REFERENCE.md`;
- `docs/reference/V7_SYSTEM_ARCHITECTURE.md`;
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`;
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`;
- `docs/reference/SYSTEM_MAP.md`;
- `docs/policies/POLICY_001_HARD_FAILURE.md` through `POLICY_009_ANTI_FLAP.md`;
- `docs/decisions/`.

Runtime mutation: no.
OMP modification: no.
Product Specification modification: no.
Apply: no.
User movement: no.

## Next Step

Continue OMP from current A3 state.
If future work requires explicit Business Intent display, extend the existing Product Specification in place and expose a read-only mapping through existing policy/OMP/operator surfaces.

## Re-audit Rule

Do not re-audit Business Intent unless Product Specification ownership changes, Product Owner responsibilities change, policy translation semantics materially change, Runtime starts consuming raw business goals directly, or the operator explicitly requests a new audit.
