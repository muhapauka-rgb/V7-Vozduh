# V7 Track 4 - Release Lineage Foundation

Purpose: create release truth without introducing CI/CD, containers, Kubernetes, or a deployment rewrite.

## Current State

The platform now has runtime evidence:

- deploy baseline manifest:
  `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`
- stale executable archive:
  `/root/v7-backups/usr-local-bin-archive/20260523T122936Z/`
- suspicious executable archive:
  `/root/v7-backups/usr-local-bin-archive/20260523T124646Z/`
- current PATH after cleanup:
  - `/usr/local/bin/v7*`: `141`
  - `v7*.tmp`: `0`
  - known suspicious executables: `0`

But there is still no release lineage. Deploy truth is cleaner, yet still mostly "live filesystem plus manifests".

## Release ID Model

Use a simple release ID first:

```text
v7-runtime-YYYYMMDDTHHMMSSZ
```

Each release ID should point to:

- source commit or source snapshot;
- runtime manifest;
- executable hash list;
- systemd unit summary;
- state contract summary;
- migration notes;
- rollback material;
- verification result.

## Release Manifest Structure

Recommended minimal file:

```json
{
  "release_id": "v7-runtime-YYYYMMDDTHHMMSSZ",
  "generated_at": "...",
  "source": {
    "repo_url": "...",
    "commit": "...",
    "dirty": true,
    "production_only_tools": []
  },
  "runtime": {
    "host": "...",
    "executables_manifest": "...",
    "systemd_summary": "...",
    "state_contract_summary": "..."
  },
  "changes": [],
  "verification": {
    "systemctl_failed": "PASS",
    "v7_killswitch_check": "PASS",
    "v7_user_route_check": "PASS",
    "v7_provisioning_reconcile_check": "PASS",
    "v7_observability_summary": "PASS"
  },
  "rollback": {
    "available": true,
    "material": []
  },
  "warnings": []
}
```

## Provenance Rules

Every runtime deploy should answer:

1. What changed?
2. Who changed it?
3. Why was it changed?
4. Which source file produced the runtime file?
5. Which release manifest owns it?
6. How do we rollback?
7. Which safety checks passed after deploy?

## Production-Only Tool Handling

There are still `103` production-only unknown tools from Block 3.3.

Do not delete them. Instead:

- import into repo with provenance notes, or
- mark as `runtime_local` with owner and purpose, or
- mark as `archive_candidate` after workflow verification.

No tool should remain indefinitely in the state:

```text
production-only, executable, in PATH, unknown owner
```

## Runtime Reproducibility Model

Classify runtime files as:

| Class | Definition | Rebuild Strategy |
|---|---|---|
| `source_owned` | Generated from repo files | Rebuild from commit |
| `runtime_local` | Created on server, intentional | Preserve in release manifest |
| `state_authoritative` | Live state that must survive deploy | Backup and validate |
| `state_generated` | Rebuildable cache/summary | Rebuild from authoritative state |
| `rollback_material` | Archived previous runtime files | Preserve with manifest |
| `legacy_unknown` | Not yet owned | Govern before touching |

## First Practical Step

Do not build CI/CD yet.

Next bounded step:

1. Create a new release manifest from the current clean runtime.
2. Add a `release_id`.
3. Link it to:
   - Block 3.1 baseline;
   - Block 3.2 archive;
   - Block 3.4 archive;
   - current verification result.
4. Mark all production-only tools as `runtime_local_pending_lineage`.

