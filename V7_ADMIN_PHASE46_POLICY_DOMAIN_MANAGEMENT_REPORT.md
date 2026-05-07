# V7 Admin Phase 46: Policy domain management

Date: 2026-05-07

## Goal

Make service-aware policy classes manageable from the admin panel, instead of
editing `/etc/v7/policy/*.conf` manually over SSH.

This is required for scaling from a few known domains to many apps and service
groups.

## Added

Scripts:

```text
/usr/local/lib/v7-policy-domain-lib
/usr/local/bin/v7-policy-domain-list
/usr/local/bin/v7-policy-domain-add
/usr/local/bin/v7-policy-domain-remove
```

Supported classes:

```text
TRUSTED_RU_SENSITIVE
DIRECT_RU
VIDEO_OPTIMIZED
GLOBAL_FAST
GLOBAL_STABLE
LOW_LATENCY
```

Behavior:

- add/remove default to dry-run unless `--apply` is passed;
- domain and class are validated;
- config file is backed up before mutation;
- duplicate add is idempotent;
- missing remove is idempotent;
- after apply, V7 refreshes policy resolve/apply preview/matrix/state JSON;
- audit log is written when available.

## Admin API

Added:

```text
POST /api/actions/policy-domain-add
POST /api/actions/policy-domain-remove
```

Both require:

```text
role >= admin
CSRF token
explicit confirmation
```

Confirm strings:

```text
ADD_POLICY_DOMAIN
REMOVE_POLICY_DOMAIN
```

Admin Safe Mode blocks both mutation actions.

## Admin UI

The `Service-aware Policy` section now shows:

- current domains per route class;
- add domain to class;
- remove domain from class;
- existing domain test;
- policy matrix;
- policy apply preview.

This keeps the operator workflow in one place:

```text
observe -> classify -> test -> preview -> apply config change
```

No live service-aware route marks are enabled by this phase.

## Validation

Commands run on VPS:

```bash
v7-policy-domain-list TRUSTED_RU_SENSITIVE
v7-policy-domain-add LOW_LATENCY v7-policy-test.invalid --apply
v7-policy-domain-remove LOW_LATENCY v7-policy-test.invalid --apply
v7-policy-test-domain yandex.ru 10.0.0.3
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
curl -sS -I http://127.0.0.1:7080/login
v7-killswitch-check
v7-system-check
```

Results:

- test domain was added and removed successfully;
- `yandex.ru` remains `DIRECT_RU`, desired path `ens3`;
- admin login endpoint returned `200 OK`;
- final `v7-killswitch-check`: `OK`;
- final `v7-system-check`: `OK`;
- live user routes stayed unchanged.

During the immediate restart/rebuild window, one killswitch check reported a
transient partial nft view, but a follow-up check seconds later returned `OK`
and confirmed the expected direct/DNS rules were present. User route checks did
not show public-interface leakage during that window.

## Next Phase

Add policy change history/rollback at the policy-domain level:

- show recent backups for each class file;
- show who changed what;
- preview diff before restore;
- restore one class file with confirmation;
- refresh policy state after restore.
