# E34.E Evidence Collection Model

evidence_collection_defined=true

## Purpose

Operators need automatic evidence collection so diagnosis does not depend on memory or manual scavenging.

Evidence collection must be read-only by default.

## Evidence Domains

| Domain | Evidence examples | Source of truth |
| --- | --- | --- |
| Logs | Service logs, installer logs, release logs, scheduler logs, operator action logs. | Append-only log store. |
| Runtime state | Runtime fingerprint, config fingerprint, service status, health checks. | Runtime inventory collector. |
| Release state | Release object, manifest, certification status, rollback release, provenance. | Release/provenance store. |
| Policy state | Active policies, evaluation trace, conflicts, review requirements. | Policy engine metadata. |
| Capacity state | Capacity class, status, confidence, validation age, effective batch cap. | Capacity metadata and validation evidence. |
| Scheduler state | Scheduled batches, blocked reasons, queue state, lock/reservation conflicts. | Scheduler metadata. |
| Routing state | Required services, target health, routing proposals, route tables, route_get. | Routing Intelligence plus runtime route inventory. |
| Audit lineage | Approval packets, forward records, rollback records, replay denials, recovery records. | Audit ledger. |

## Evidence Bundle

Every problem should produce an evidence bundle:

```text
evidence_bundle_id
created_at
problem_id
scope
collected_sources
fingerprints
lineage_refs
redaction_status
operator_notes
```

## Redaction and Safety

Evidence bundles must redact:

- private keys;
- tokens;
- passwords;
- raw provider credentials;
- user secrets.

Evidence may include hashes, fingerprints, timestamps, paths, and redacted diffs.

## Completeness Rule

If required evidence is unavailable, the diagnostic flow must mark:

```text
evidence_complete=false
forward_action_allowed=false
rollback_or_containment_allowed=true
```
