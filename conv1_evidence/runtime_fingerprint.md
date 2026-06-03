# CONV.1 Runtime Fingerprint Evidence

Canonical runtime fingerprint path:

`/opt/v7/runtime-fingerprint.json`

## Schema

`v7-runtime-fingerprint/v1`

## Contents

The fingerprint includes:

- branch;
- commit;
- deployment id;
- generated timestamp;
- runtime root;
- critical deployed file hashes;
- service/systemd unit names;
- snapshot subsystem root;
- snapshot refresh CLI path;
- snapshot refresh systemd units;
- required intelligence snapshot files.

## Required Snapshot Files

- `service-scores.json`
- `channel-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `overview-summary.json`

## Validation

CONV.1 adds `validate_runtime_fingerprint()` with schema:

`v7-runtime-fingerprint-validation/v1`

Local model validation returned:

```text
final_verdict=PASS
```

The runtime fingerprint is now embedded in:

- deploy manifest;
- release manifest;
- runtime linkage metadata;
- safe deploy payload.

