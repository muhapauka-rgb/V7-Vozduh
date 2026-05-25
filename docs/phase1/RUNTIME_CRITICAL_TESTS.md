# V7 Phase 1 - Runtime Critical Tests

## Purpose

Phase 1 tests must be safe. They should detect mismatch and leak risk without rewriting routes, nftables, provisioning, or autoswitch behavior.

## Allowed Test Classes

### Read-Only Runtime Checks

Allowed:

- inspect interfaces;
- inspect `ip rule`;
- inspect route tables;
- inspect nftables;
- inspect systemd status;
- inspect registry and JSON state;
- run route verification commands that do not mutate runtime.

### Controlled Dry-Run Checks

Allowed:

- run existing tools in dry-run mode;
- generate repair plans without applying them;
- parse state files and report schema findings.

### Forbidden in Phase 1 Tests

Forbidden:

- rebuild nftables as part of test;
- change route tables;
- restart production interfaces;
- mutate registries;
- run autoswitch with `--apply`;
- enable unverified egress;
- perform mass user migration.

## Existing Safe Checks

Recommended read-only checks:

- `hardening/v7-killswitch-check`
- `hardening/v7-provisioning-reconcile-check`
- `tools/v7-service-matrix-test` only when used in controlled diagnostic mode
- `tools/v7-egress-set-state` without `--apply`

## New Contract Validation Check

Phase 1 adds:

- `tools/v7-runtime-contract-validate`

Purpose:

- parse state contracts safely;
- detect corrupt JSON;
- detect duplicate users/egresses;
- detect unknown egress references;
- detect missing critical files;
- report findings without writing runtime state.

Example production usage:

```bash
python3 tools/v7-runtime-contract-validate
```

Example local/sandbox usage when `/opt/v7` is absent:

```bash
python3 tools/v7-runtime-contract-validate --allow-missing
```

## Suggested Phase 1 Verification Bundle

Manual operator bundle:

1. run contract validator;
2. run kill switch check;
3. run provisioning reconcile check;
4. inspect direct/RU diagnostics;
5. inspect latest service matrix timestamp;
6. report summary first.

## Exit Semantics

Recommended:

- exit `0` when no blocker/corruption is found;
- exit `1` when critical contract corruption or unsafe missing required state is found.

Warnings should not automatically mutate runtime.
