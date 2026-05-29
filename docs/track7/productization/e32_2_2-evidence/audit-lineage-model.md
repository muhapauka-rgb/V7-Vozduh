# E32.2.2 Audit And Lineage Model

metadata_audit_lineage_defined=true

## Principle

Batch metadata must bind every approval, packet, runtime event, denial, and evidence artifact into one auditable lineage.

## Lineage Objects

### Batch Ledger

Stores:

- authoritative batch fields;
- status transitions;
- parent/child relationships;
- operator context;
- audit lineage id.

### Approval Record

Stores:

- approval id;
- approver or authority;
- batch id;
- movement budget;
- blast radius;
- freshness hashes;
- capacity state.

### Packet Record

Stores:

- packet id;
- packet generation;
- packet hash;
- allowed users;
- allowed target;
- expiration;
- execution-time recheck contract.

### Forward Event

Stores:

- per-user forward action;
- source target;
- destination target;
- route table when applicable;
- exit code;
- before/after hashes.

### Rollback Event

Stores:

- per-user rollback action;
- rollback target;
- route table when applicable;
- exit code;
- before/after hashes.

### Replay Denial

Stores:

- packet id;
- replay verdict;
- consumed forward record reference;
- proof of no movement and no routing mutation.

### Evidence Paths

Stores file paths for:

- precheck;
- approval packet;
- authorization;
- forward proof;
- observation;
- rollback proof;
- restore-settle;
- delayed monitoring;
- replay validation;
- tests.

## Binding Rule

Every event must reference:

```text
batch_id
audit_lineage_id
packet_id_or_denial_reason
```

## Conflict Behavior

If audit lineage conflicts:

```text
forward_allowed=false
replay_allowed=false
operator_next_action=human_review
```

Rollback containment remains allowed only if exact rollback scope is known.

## Audit Verdict

Metadata audit lineage is defined and production-pool compatible.

