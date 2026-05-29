# E32.1.4 Evidence Catalog

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

evidence_catalog_defined=true

## Evidence Types

| Evidence Type | Purpose | Authority | Freshness | Mandatory | Certification Impact |
| --- | --- | --- | --- | --- | --- |
| `TARGET_LOCAL_PROBE` | Measures class-sized target pressure without moving users. | Validation tooling plus evidence review. | Expires with capacity freshness. | Mandatory for promotion. | Required for MEDIUM confidence. |
| `LONG_WINDOW` | Measures sustained quality and readiness. | Validation tooling plus evidence review. | Expires with capacity freshness. | Mandatory for promotion. | Required for MEDIUM confidence. |
| `READINESS` | Confirms target is GO. | Readiness helper. | Immediate / packet-time. | Mandatory. | Blocks execution if not GO. |
| `RESTORE_SETTLE` | Confirms runtime is quiet. | Restore-settle helper. | Immediate / packet-time. | Mandatory. | Blocks execution if not GO. |
| `RUNTIME_CHECKERS` | Confirms platform health. | Runtime checker suite. | Immediate / packet-time. | Mandatory. | Blocks execution if failing. |
| `FORWARD_PROOF` | Proves exact approved users moved. | Audit + registry/route diffs. | Historical proof. | Mandatory for certification. | Required for HIGH confidence. |
| `ROLLBACK_PROOF` | Proves exact approved users returned. | Audit + registry/route diffs. | Historical proof. | Mandatory for certification. | Required for HIGH confidence. |
| `DELAYED_MONITORING` | Detects delayed/unapproved movement. | Observation samples. | Historical proof. | Mandatory for certification. | Required for HIGH confidence. |
| `REPLAY_PROOF` | Proves packet replay denial. | Replay helper + audit. | Historical proof. | Mandatory for certification. | Required for HIGH confidence. |
| `AUDIT_PROOF` | Proves append-only lineage and ordering. | Audit store validation. | Historical proof. | Mandatory for certification. | Required for production-grade claim. |

## Optional Evidence

Optional evidence can increase confidence or explain failures but cannot replace mandatory proof:

- packet loss;
- latency;
- jitter;
- CPU/load;
- interface errors/drops;
- external endpoint health;
- provider diagnostics.

## Evidence Authority

Evidence is authoritative only when:

- collected by approved helper or documented command;
- linked to a block report;
- redacted when secrets are present;
- bound to hashes where available;
- reviewed by `OPERATOR_PLUS_EVIDENCE` authority.

## Evidence Freshness

Operational evidence has TTL:

- readiness: immediate / same execution-time recheck;
- restore-settle: immediate / same execution-time recheck;
- runtime checkers: immediate / same execution-time recheck;
- target-local probe: class freshness TTL;
- long-window: class freshness TTL;
- movement/rollback/replay/audit proof: historical proof, but operational eligibility still expires.

