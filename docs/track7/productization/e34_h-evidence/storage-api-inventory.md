# E34.H Storage / API Inventory

storage_api_inventory_defined=true

| State | Storage | API Surface | Consumers |
| --- | --- | --- | --- |
| Capacity metadata | Capacity Store / egress registry metadata | `/api/overview`, future `/api/capacity/*` | Channels, Checks, Proposals, Policy |
| Proposals | Proposal Store | future `/api/proposals/*` | Overview, Users, Channels, Routing, Checks |
| Batches | Batch Store | future `/api/batches/*` | Scheduler, Logs, Checks, Governance |
| Approval packets | Packet Store | future `/api/packets/*` | Batch Service, Execution-Time Recheck, Replay Protection |
| Locks | Lock Store | future `/api/locks/*` | Concurrency, Scheduler, Action Drawers |
| Reservations | Reservation Ledger | future `/api/reservations/*` | Capacity, Scheduler, Batch Service |
| Policy | Policy Store / config files | existing policy actions plus future `/api/policy/*` | Settings, Routing, Proposal Engine |
| Service preferences | Service Preferences Store / identity metadata | `/api/actions/service-preferences-update`, future `/api/service-preferences/*` | Users, Routing, Channels |
| Service health | Service health state / matrix cache | `/api/overview`, service matrix actions | Channels, Routing, Checks |
| Quality history | Egress diagnose/benchmark state | `/api/overview`, speedtest actions | Channels, Capacity, Proposals |
| User readiness | User readiness state | `/api/overview`, user check actions | Users, Checks, Proposals |
| Release objects | Release Store | future `/api/releases/*` | Security, Checks, Convergence |
| Provenance | Provenance Ledger | future `/api/provenance/*` | Release, Logs, Recovery |
| Backups | Backup Store / manifests | existing backup actions/download, future `/api/backups/*` | Security, Restore, Recovery |
| Installer state | Installer State Store | future `/api/installer/*` | Setup mode, Security, Checks |
| Evidence bundles | Evidence Bundle Store | future `/api/evidence/*` | Drawers, Checks, Logs, Support |
| Closure records | Closure Record Store | future `/api/closure/*` | Operator Independence, Logs |
| Audit events | Audit Ledger / event stream | `/api/events`, security audit APIs | Logs, Drawers, Certification |

## Storage/API Verdict

Storage/API inventory is defined. Existing admin already exposes part of the model through `/api/overview`, `/api/actions/*`, logs, backup actions and policy actions. Formal first-class APIs are still needed for proposals, batches, locks, releases, installer state, evidence bundles and closure records.
