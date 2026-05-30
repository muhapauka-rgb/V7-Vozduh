# E34.H Governance Mapping

governance_mapping_defined=true

## Reality-First Mapping

| Architecture entity | Product Meaning | Operator Meaning | Admin Surface | Runtime Service | Storage/API |
| --- | --- | --- | --- | --- | --- |
| Capacity | Certified safe size for a target or channel. | “Can this channel safely take this many users/batch?” | `Каналы` readiness/load, `Проверки` readiness, `Настройки -> Влияние`, `Главная` alerts. | Capacity Service / readiness helper / quality validator. | Capacity Store, egress registry metadata, `/api/overview`, future `/api/capacity/*`. |
| Execution Batches | Governed group movement unit. | “This proposed action affects these users and has rollback.” | `Главная` proposals, `Проверки`, `Логи`, action drawers. | Batch Service / Proposal Service / execution-time recheck. | Batch Store, Packet Store, Audit Ledger, future `/api/batches/*`. |
| Policy | Admission logic for whether an action is allowed. | “Allowed, denied, review required, or additional gates required.” | `Настройки -> Политика V7`, `Настройки -> Влияние`, `Маршруты -> Проверка`, `Логи`. | Policy Service / admission evaluator. | Policy Store, policy config files, `/api/actions/policy-update`, `/api/actions/org-egress-policy-update`. |
| Concurrency | Locking and reservation guardrails. | “Action is blocked because a user/channel/batch is already reserved.” | Action result drawers, `Проверки`, `Логи`, `Главная` blockers. | Lock Service / Reservation Service. | Lock Store, Reservation Ledger, Audit Ledger, future `/api/locks/*`. |
| Scheduling | Safe timing and queueing of future actions. | “What is planned, blocked, waiting, or safe to run next?” | `Главная`, `Настройки -> Автосвитч`, `Логи`, future scheduler drawer. | Scheduler Service / autoswitch planner integration. | Schedule Store, Batch Store, Audit Ledger, future `/api/schedule/*`. |

## Incomplete Runtime Work

- Capacity needs a formal API beyond current overview/registry-derived data.
- Batch Store and Packet Store need implementation-level schemas.
- Lock/Reservation ledger needs a concrete storage backend.
- Scheduler needs a production queue model distinct from existing autoswitch/planner state.

## Mapping Verdict

Governance architecture maps to product capability, admin surface, runtime service and storage/API.
