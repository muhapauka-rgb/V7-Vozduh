# E34.H Gap Analysis

implementation_gaps_defined=true

## Unimplemented Services

- Proposal Service as first-class runtime service.
- Batch Service as durable runtime service.
- Concurrency Lock/Reservation Service.
- Release Service and Provenance verifier.
- Installer Service.
- Runbook Service.
- Evidence Bundle Service.
- Closure Record Service.

## Missing Storage

- Proposal Store.
- Batch Store.
- Packet Store.
- Lock Store.
- Reservation Ledger.
- Release Store.
- Provenance Ledger.
- Installer State Store.
- Evidence Bundle Store.
- Closure Record Store.

## Missing APIs

- `/api/proposals/*`
- `/api/batches/*`
- `/api/packets/*`
- `/api/locks/*`
- `/api/reservations/*`
- `/api/releases/*`
- `/api/provenance/*`
- `/api/installer/*`
- `/api/evidence/*`
- `/api/closure/*`

## Missing UI Surfaces

Not missing as new top-level nav.

Missing as components/workspaces:

- proposal card/drawer;
- evidence bundle drawer section;
- release/provenance drawer;
- runtime convergence status card;
- role-gated expert diagnostics;
- installer first-run/checklist flow;
- scheduler queue/blocked reason drawer;
- closure verdict component.

## Missing Integrations

- Required Services editor to channel/service matrix recommendations.
- Policy admission trace to proposal UI.
- Capacity status to batch/proposal admission.
- Locks/reservations to action drawers.
- Release provenance to backup/restore/recovery.
- Evidence bundles to logs and checks.

## Gap Verdict

Architecture is mapped to implementation. Several implementation gaps remain, but none are unmapped architecture-only entities.
