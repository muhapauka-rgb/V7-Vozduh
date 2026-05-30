# E34.H Routing Intelligence Mapping

routing_mapping_defined=true

## Reality-First Mapping

| Architecture entity | Product Meaning | Operator Meaning | Admin Surface | Runtime Service | Storage/API |
| --- | --- | --- | --- | --- | --- |
| Signal Model | Inputs used to decide route/channel suitability. | “Why does V7 prefer or reject this channel?” | `Маршруты`, user/channel drawers, `Проверки`. | Routing Signal Service / route preview helper. | Routing state files, `/api/overview`, `/api/actions/policy-route-preview`. |
| Required Services | User/company-specific service needs. | “This user must have Telegram/Google/YouTube/etc working.” | `Пользователи` priority column/drawer, `Каналы -> Сервисная матрица`, `Маршруты`. | Required Services Resolver / service preference evaluator. | Service Preferences Store, identity/user metadata, `/api/actions/service-preferences-update`. |
| Service Health | Per-channel service availability. | “Does this channel currently support the services we need?” | `Каналы -> Сервисная матрица`, channel drawer, `Проверки`. | Service Health Service / service matrix tester. | Service health state, `/api/actions/service-matrix-test`, `/api/overview`. |
| Target Quality | Throughput/stability/readiness quality. | “Is this channel fast/stable enough?” | `Каналы -> Готовность и скорость`, `Главная`, `Проверки`. | Quality Service / benchmark/readiness helper. | Quality history state, egress diagnose state, `/api/overview`, speedtest actions. |
| User-Specific Health | Whether a specific user is healthy on route/channel. | “Is this person connected, routed and leak-safe?” | `Пользователи`, user drawer, `Проверки`. | User Readiness Service / route checker. | User readiness state, users registry, `/api/overview`, user check actions. |
| Proposal Engine | Produces route/movement/observation proposals. | “Here is the safe next action and why.” | `Главная`, `Маршруты -> Проверка`, drawers. | Proposal Service / routing decision engine. | Proposal Store, Audit Ledger, future `/api/proposals/*`. |
| Confidence | Operator trust level for a decision. | “Can I trust this proposal or does it need review?” | Proposal card/drawer, `Проверки`, `Логи`. | Confidence Evaluator. | Proposal Store, evidence bundle store, future confidence fields in proposal API. |
| Flapping Protection | Prevents unstable repeated switching. | “Do not move users back and forth because of noise.” | `Настройки -> Ограничители`, proposal denial, `Логи`. | Flap Guard / cooldown guard / history evaluator. | Switch history, cooldown state, policy store, `/api/overview`. |

## Incomplete Runtime Work

- Proposal Store is not yet a first-class implemented store.
- Confidence needs a shared schema across routing, capacity, policy and batch proposals.
- Required services need a clearer user/company-level admin editor and API contract.

## Mapping Verdict

Routing Intelligence maps to current admin surfaces and runtime concepts, with proposal/confidence/required-service storage requiring implementation hardening.
