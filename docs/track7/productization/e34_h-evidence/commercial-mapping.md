# E34.H Commercial Hardening Mapping

commercial_mapping_defined=true

## Reality-First Mapping

| Architecture entity | Product Meaning | Operator Meaning | Admin Surface | Runtime Service | Storage/API |
| --- | --- | --- | --- | --- | --- |
| Runtime / Repo Convergence | Know what version/config/runtime is actually running. | “Is this server running the certified thing?” | `Проверки`, `Безопасность`, `Логи`, `Главная` drift alert. | Convergence Service / runtime inventory collector. | Runtime Fingerprint Store, Release Store, `/api/runtime/*` future. |
| Release & Provenance | Certified deployable release identity and rollback lineage. | “What release is deployed, is it trusted, and what can we roll back to?” | `Безопасность` release drawer, `Проверки`, `Логи`. | Release Service / provenance verifier. | Release Store, Provenance Ledger, future `/api/releases/*`. |
| Backup / Restore | Verified backup and safe restore path. | “Can I recover and what will be restored?” | `Безопасность -> Бэкапы`, `Безопасность -> Действия`, `Логи`. | Backup Service / Restore Service. | Backup Store, backup manifests, audit ledger, existing backup APIs/actions. |
| Installer | Guided deployability and setup readiness. | “What is missing before this V7 instance is READY?” | Setup mode, `Безопасность`, `Проверки`, `Логи`. | Installer Service / preflight checker / health verifier. | Installer State Store, release store, backup store, future `/api/installer/*`. |
| Operator Independence | Guided runbooks and evidence-first problem closure. | “What happened, who is affected, what should I do next?” | `Что дальше`, `Сценарии`, drawers, info panels, `Логи`. | Runbook Service / Evidence Bundle Service. | Runbook Store, Evidence Bundle Store, Closure Record Store, future `/api/operator/*`. |

## Incomplete Runtime Work

- Release Store and Provenance Ledger need concrete backend.
- Runtime inventory collector needs implementation.
- Installer state and first-run entrypoint need implementation.
- Evidence Bundle Store and Closure Record Store need schema and APIs.

## Mapping Verdict

Commercial Hardening maps cleanly to product, operator, admin, runtime and storage/API paths, but several stores/services remain implementation backlog.
