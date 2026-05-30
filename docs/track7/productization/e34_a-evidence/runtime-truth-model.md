# E34.A Runtime Truth Model

runtime_truth_model_defined=true

## Definition

runtime_truth is the observed state of what is actually executing and what configuration it is using.

It is not inferred only from the repository. It must be collected from the running environment.

## Runtime Truth Components

| Component | Meaning | Example Evidence |
| --- | --- | --- |
| running_services | Processes and service units currently active. | process list, service manager state, container state. |
| runtime_configuration | Config files and environment values loaded by services. | file hashes, env fingerprints, service unit hashes. |
| runtime_version | Version or commit identity reported by running service. | `/version`, CLI version output, embedded commit. |
| runtime_state | Mutable state that affects behavior. | registries, ledgers, quality summaries, locks, reservations. |
| runtime_lineage | How this runtime was deployed. | release id, deployment id, deploy actor, timestamp. |

## Authority

runtime_truth is authoritative for safety checks because it describes live behavior.

repo_truth is authoritative for source provenance, but cannot prove what is running without convergence evidence.

## Required Runtime Snapshot

Each convergence snapshot should include:

```text
snapshot_id
collected_at
host_id
service_inventory
process_fingerprints
config_fingerprints
state_fingerprints
runtime_reported_version
deployment_lineage_ref
drift_status
```

## Fail-Closed Rule

If runtime truth cannot be collected, deployment status is UNKNOWN and production promotion must be denied.

runtime_truth_model_defined=true
