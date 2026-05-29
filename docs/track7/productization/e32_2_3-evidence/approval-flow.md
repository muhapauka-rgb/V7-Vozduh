# E32.2.3 Approval Flow

approval_flow_defined=true

## Purpose

Approval flow moves a batch from modeled scope to approved scope without making it executable yet.

Approval does not authorize immediate runtime mutation.

## Required Metadata

Before approval:

```text
batch_id_present=true
batch_type_valid=true
allowed_users_exact=true
source_targets_present=true
destination_target_present_for_forward=true
rollback_manifest_complete=true
movement_budget_valid=true
blast_radius_valid=true
capacity_requirements_present=true
execution_window_valid=true
audit_lineage_id_present=true
```

## Required Packet

Approval creates or binds:

```text
approval_packet_id
approval_id
packet_generation
packet_hash
packet_expires_at
```

The packet must bind:

- exact user set;
- exact target;
- rollback manifest;
- capacity requirements;
- registry hashes;
- selected moves hash;
- restore-settle status;
- runtime checker status.

## Required Gates

Approval requires:

- metadata validation;
- capacity eligibility at approval time;
- rollback completeness;
- audit lineage allocation;
- no known hidden movers;
- no selected moves;
- operator confirmation where required.

## Required Operator Actions

For operator movement batches:

- review exact users;
- review target and rollback target;
- review blast radius;
- confirm rollback manifest;
- confirm execution window;
- confirm no autoswitch/cohort expansion.

## Approval Output

Successful approval transitions:

```text
PRECHECKED -> APPROVED
```

The batch remains non-executable until execution-time recheck.

## Approval Failure

Any approval mismatch transitions to:

```text
FAILED_CLOSED
```

or:

```text
EXPIRED
```

if the approval window has lapsed.

## Approval Verdict

Approval flow is defined and preserves `execution_allowed_now=false` until execution-time recheck.

