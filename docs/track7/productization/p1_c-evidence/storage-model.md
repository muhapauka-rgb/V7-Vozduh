# P1.C Storage Model

runtime_convergence_storage_defined=true

## Store Ownership

Runtime Convergence Store owns runtime trust snapshots, drift state, verification history and lineage references.

It does not own release artifacts, backups or runtime registries. It stores references to those sources.

## Storage Objects

Minimum entities:

- `runtime_convergence_snapshots`;
- `runtime_fingerprints`;
- `runtime_drift_records`;
- `runtime_verification_events`;
- `runtime_lineage_refs`;
- `runtime_convergence_closure_records`.

## Runtime Fingerprint Storage

Fingerprint storage should include:

- fingerprint id;
- captured timestamp;
- runtime version/build label;
- release reference;
- hash summary;
- redaction state;
- source checker;
- evidence bundle id.

Raw fingerprint internals can be role-gated or stored as referenced payloads.

## Drift State Storage

Drift records should include:

- drift id;
- drift type;
- severity;
- affected surface;
- summary;
- detected at;
- verification state;
- recommended action;
- closure state.

## Verification History

Verification history should preserve:

- check source;
- input release reference;
- output status;
- drift findings;
- runtime checker result;
- evidence bundle id;
- actor/source.

## Lineage References

Lineage references link convergence to:

- release id;
- provenance record;
- backup manifest;
- restore event;
- audit record;
- evidence bundle.

## Storage Verdict

Runtime Convergence Store is an audit-friendly trust snapshot store. It presents operator meaning while preserving advanced technical lineage behind role-gated details.
