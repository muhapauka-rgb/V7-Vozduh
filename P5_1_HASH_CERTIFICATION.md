# P5.1 Hash Certification

## Authoritative Hashes

For a future P5 retry, the authoritative hashes must be computed from live files at execution time:

- `users_registry_hash`: SHA-256 of `/opt/v7/egress/state/users.registry`
- `egress_registry_hash`: SHA-256 of `/opt/v7/egress/state/egress.registry`
- `selected_move_hash`: canonical JSON SHA-256 of current selected moves
- `runtime_snapshot_hash`: canonical JSON SHA-256 over the three hashes above

## Stale Hashes

Hashes in old reports, evidence folders, fixtures, or previous audits are stale for P5.1 and cannot authorize P5.

## Current Certification Result

No live hashes were certified because current runtime files were not accessible in this environment.

## Verdicts

- hashes_certified=false
- authoritative_hash_algorithm_identified=true
- stale_hashes_rejected=true
- live_users_registry_hash_certified=false
- live_egress_registry_hash_certified=false
- live_selected_moves_hash_certified=false
- live_runtime_snapshot_hash_certified=false
