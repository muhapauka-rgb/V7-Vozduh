# V7 Admin Phase 47: Policy domain rollback

Date: 2026-05-07

## Goal

Add rollback tooling for service-aware policy domain files.

This protects the operator workflow:

```text
add/remove domain -> detect bad classification -> preview diff -> restore class file
```

## Added

Scripts:

```text
/usr/local/bin/v7-policy-domain-backups
/usr/local/bin/v7-policy-domain-restore
```

`v7-policy-domain-backups <CLASS>` lists class-file backups created by policy
domain add/remove/restore actions.

`v7-policy-domain-restore <CLASS> <backup>` defaults to dry-run and prints a
unified diff. It only restores when `--apply` is passed.

Safety:

- class id is validated;
- backup name must match the class file backup prefix;
- path traversal is rejected;
- current file is backed up before restore apply;
- policy resolve/apply preview/matrix/state JSON are refreshed after apply;
- audit log is written when available.

## Admin API

Added:

```text
POST /api/actions/policy-domain-backups
POST /api/actions/policy-domain-restore-preview
POST /api/actions/policy-domain-restore-apply
```

Roles:

```text
backups: viewer
restore-preview: viewer
restore-apply: admin
```

Restore apply requires:

```text
RESTORE_POLICY_DOMAIN
```

Admin Safe Mode blocks restore apply.

## Admin UI

The `Service-aware Policy` section now includes:

- list class backups;
- restore preview;
- restore class file.

This keeps policy changes operationally reversible from the control center.

## Validation

Commands run on VPS:

```bash
v7-policy-domain-backups LOW_LATENCY
v7-policy-domain-restore LOW_LATENCY low_latency_domains.conf.backup.v7-policy-domain-add.20260507-150235
systemctl is-active v7-admin-api
curl -sS -I http://127.0.0.1:7080/login
v7-killswitch-check
v7-system-check
```

Results:

- backup list returned existing policy-domain backups;
- restore preview ran in dry-run mode;
- no restore apply was performed;
- `v7-admin-api`: active;
- `HTTP /login`: `200 OK`;
- `v7-killswitch-check`: `OK`;
- `v7-system-check`: `OK`;
- live user routes stayed unchanged.

## Next Phase

Before enabling any live service-aware marks, add a readiness checklist:

- class has domains;
- class DNS resolve is fresh;
- class active egress exists;
- route table plan is valid;
- kill switch rule ordering is valid;
- rollback path exists;
- one test user can be selected for rollout.
