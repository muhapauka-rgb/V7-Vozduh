# P1.B Proposal Storage Model

proposal_storage_defined=true

## Storage Ownership

Proposal Store owns recommendation metadata, lifecycle state, evidence linkage, timeline and closure records.

It does not own runtime registry state and does not mutate users, routes or channels.

## Storage Objects

Minimum entities:

- `proposals`;
- `proposal_timeline_events`;
- `proposal_evidence_links`;
- `proposal_object_links`;
- `proposal_closure_records`;
- `proposal_governance_refs`.

## Retention

Recommended retention:

| Proposal type | Retention |
| --- | --- |
| active/review-required | until closure plus policy retention |
| closed operational proposals | 180 days minimum |
| proposals that entered governance | match audit/packet retention |
| recovery/security proposals | 365 days minimum |

## Expiration

Proposal expiration is required because evidence and runtime truth age.

Expiration should be based on:

- evidence bundle freshness;
- target readiness freshness;
- service health freshness;
- capacity freshness;
- policy/version freshness;
- explicit proposal TTL.

Expired proposals cannot enter execution. They must be refreshed or closed.

## Lineage

Proposal lineage must preserve:

- creating source;
- evidence bundle id;
- related object links;
- current/proposed targets;
- lifecycle transitions;
- governance references if created;
- closure record.

## Evidence Linkage

`evidence_bundle_id` is mandatory.

Additional evidence links may exist for supporting proof, but one primary Evidence Bundle must explain the proposal.

## Storage Verdict

Proposal Store is the durable recommendation layer between evidence and governance. It must be searchable, auditable and freshness-aware.
