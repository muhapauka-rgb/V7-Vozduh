# E34.H Runtime Service Inventory

runtime_service_inventory_defined=true

| Service Name | Purpose | Owner | Inputs | Outputs | Dependencies |
| --- | --- | --- | --- | --- | --- |
| Capacity Service | Certify and expose target capacity/effective batch cap. | Governance runtime | quality, target users, hard limit, policy cap, validation evidence | capacity status, available capacity, blockers | Quality Service, Policy Service, egress registry |
| Policy Service | Evaluate admission decisions. | Governance runtime | policy config, batch/proposal, runtime gates, scope | ALLOW/DENY/REVIEW/ADDITIONAL_GATES | Capacity Service, Runtime Checkers, Audit |
| Scheduling Service | Queue and time safe future execution. | Governance runtime | approved batches, locks, reservations, windows | scheduled/blocked/expired state | Batch Service, Concurrency Service, Policy Service |
| Proposal Service | Create operator-readable proposals. | Routing/Governance bridge | signals, service health, user health, capacity, policy | movement/evacuation/rebalance/observation proposals | Routing Intelligence, Capacity, Policy |
| Batch Service | Manage execution batch lifecycle. | Governance runtime | approval packets, user set, target, rollback manifest | batch status, verification status, audit refs | Packet Store, Audit, Concurrency |
| Concurrency Service | Manage locks and reservations. | Governance runtime | user/target/batch/packet/audit lock requests | lock granted/denied, reservation status | Lock Store, Reservation Ledger |
| Service Health Service | Measure per-channel service availability. | Routing runtime | service probes, egress channels, service catalog | service matrix, health blockers | Channel registry, probe tools |
| Quality Service | Measure channel throughput/stability/readiness. | Routing runtime | benchmark, diagnose, target-local probes | avg/min Mbps, stability, readiness | Benchmark service, egress diagnose |
| User Readiness Service | Evaluate specific user connection/routing health. | Admin/runtime bridge | users registry, client state, route_get, profile status | user readiness, next action | Client agent state, route checker |
| Backup Service | Create, verify, expose backups. | Commercial hardening | backup scope, runtime/config/release/audit data | backup object, verification result | Backup Store, Audit |
| Restore Service | Preview and apply controlled restore. | Commercial hardening | backup object, restore scope, release/config expectations | restore preview/result | Backup Service, Release Service, Runtime Checkers |
| Release Service | Track release identity/certification/provenance. | Commercial hardening | release manifest, commit, artifacts, signatures | release status, rollback release | Release Store, Provenance Ledger |
| Convergence Service | Compare runtime truth to repo/release truth. | Commercial hardening | runtime fingerprint, config fingerprint, release fingerprint | drift status, blockers | Runtime Inventory, Release Service |
| Installer Service | Guide deployment readiness and setup. | Commercial hardening | host discovery, preflight, release, config, backup readiness | CHECK/READY status, blockers | Release, Backup, Convergence |
| Runbook Service | Provide operator procedures. | Operator independence | problem type, context, role | next safe steps, closure criteria | Evidence Bundle Service |
| Evidence Bundle Service | Collect supportable evidence for diagnosis. | Operator independence | logs, runtime, release, policy, capacity, routing, audit | evidence bundle, redacted detail | All runtime services, Audit |

## Inventory Verdict

Runtime service inventory is defined, with several services currently architectural/future rather than implemented.
