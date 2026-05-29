# E32.2.1 Audit Lineage Model

batch_audit_lineage_defined=true

## Purpose

Audit lineage connects a batch plan to every approval, execution, rollback, denial, and evidence artifact.

## Required Lineage Fields

```text
audit_lineage_id
batch_id
approval_id
packet_id
forward_event_ids
rollback_event_ids
replay_event_ids
denial_event_ids
evidence_paths
registry_hashes
egress_hashes
capacity_evidence_ids
created_at
closed_at
```

## Event Model

### forward_event

Required when forward movement executes.

Must include:

- exact command or operation;
- user;
- source target;
- destination target;
- route table if applicable;
- exit code;
- before/after hash;
- timestamp.

### rollback_event

Required when rollback executes.

Must include:

- user;
- pre-rollback target;
- rollback target;
- route table if applicable;
- exit code;
- before/after hash;
- timestamp.

### replay_event

Required after executed packet replay validation.

Must include:

- packet id;
- replay verdict;
- no movement proof;
- no routing mutation proof.

### denial_event

Required when batch approval or execution is denied.

Must include:

- denied gate;
- observed value;
- expected value;
- next safe action.

## Evidence Paths

Evidence paths must include:

- approval packet;
- execution-time recheck;
- final authorization;
- forward execution;
- forward verification;
- observation samples;
- rollback execution;
- rollback verification;
- restore-settle;
- delayed monitoring;
- replay validation;
- tests.

## Lineage Verdict

Batch audit lineage is defined and supports proof, replay denial, incident review, and production-pool observability.

