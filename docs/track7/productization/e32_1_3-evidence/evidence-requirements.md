# E32.1.3 Evidence Requirements

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

evidence_requirements_defined=true

## Evidence Categories

- target-local probes;
- throughput and minimum Mbps samples;
- long-window readiness;
- runtime checker health;
- restore-settle;
- exact candidate set;
- approval packet;
- execution-time recheck;
- forward proof;
- rollback proof;
- delayed monitoring;
- replay denial;
- audit chain validation;
- metadata diff and registry hashes.

## Per-Class Requirements

| Class | Candidate Pool | Target-Local Validation | Long Window | Governed Movement Proof | Rollback Proof | Replay Proof | Confidence After Certification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLASS_1 | 1 user | Required or inherited from target readiness | Required | 1-user exact proof | Required | Required | HIGH |
| CLASS_2 | 2 users | Required | Required | 2-user exact proof | Required | Required | HIGH |
| CLASS_4 | 4 users | Required | Required | 4-user exact proof | Required | Required | HIGH |
| CLASS_10 | 10 users | Required | Required | 10-user exact proof | Required | Required | HIGH |
| CLASS_20 | 20 users | Required | Required | 20-user exact proof | Required | Required | HIGH after proof |
| CLASS_50 | 50 users | Required | Required | Exact or approved staged proof | Required | Required | HIGH after proof |
| CLASS_100 | 100 users | Required | Required | Exact or approved staged proof | Required | Required | HIGH after proof |

## Metadata Evidence

Every certification decision must record:

- target id;
- old capacity class;
- new capacity class;
- old hard limit;
- new hard limit;
- evidence paths;
- evidence hashes where available;
- registry hashes;
- packet ids;
- audit record ids or hashes;
- validation timestamp;
- schema version.

## Minimum Evidence For CERTIFIED

`CERTIFIED` requires:

```text
target_local_capacity_safe=true
long_window_go=true
no_sample_below_floor=true
restore_settle_gate_status=GO
runtime_checkers_ok=true
exact_forward_proof=true
exact_rollback_proof=true
replay_denial=true
delayed_movement_observed=false
audit_chain_valid=true
```

## Evidence Insufficiency

If any required evidence is missing:

- status cannot be CERTIFIED for the requested class;
- status becomes CANDIDATE, VALIDATING, STALE, or EXPIRED depending on context;
- forward execution remains denied.

