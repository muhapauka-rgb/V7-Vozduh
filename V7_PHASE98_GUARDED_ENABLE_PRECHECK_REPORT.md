# V7 Phase98: Guarded enable precheck

## Human Meaning

V7 now refuses to enable a channel if it cannot prove the channel has a runtime
profile ready.

This protects the operator from a dangerous mistake: adding a channel to the pool
and then enabling it while the actual interface/proxy config is missing.

## Terms

- Enable: allow V7 to route users through an egress channel.
- Runtime readiness: proof that the channel has the required runtime profile.
- Backend guard: server-side refusal, even if a request bypasses the UI.

## What Changed

Updated:

- `admin/v7-admin-api`

The egress state preview now returns:

```text
runtime_readiness
```

The egress state apply action now blocks:

```text
state=enabled
```

when:

```text
runtime_readiness.enable_ready=false
```

The UI also stops before asking for final confirmation if the readiness check is
blocked.

## Safety Model

This phase does not change routing logic.

It only adds a refusal path before an existing mutation:

- `disabled` and `maintenance` actions still use the existing user-assignment
  guard;
- `enabled` now additionally requires runtime readiness;
- blocked attempts are written to audit log as warning events.

## Local Validation

Compile:

```text
python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
```

Result:

```text
OK
```

Whitespace check:

```text
git diff --check
```

Result:

```text
OK
```

## VPS Validation

Deployed to:

```text
/usr/local/bin/v7-admin-api
```

Backup created before replacement:

```text
/usr/local/bin/v7-admin-api.bak.phase98.<timestamp>
```

Validation:

```text
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api
curl -fsS http://127.0.0.1:7080/health
```

Result:

```text
active
status=OK
```

Runtime-readiness blocked case:

```json
{
  "blocked_enable": false,
  "blocked_status": "BLOCKED",
  "would_block_enable": true
}
```

## Current Status

Phase98 is complete.

V7 now has both:

- visibility before enable;
- backend enforcement before enable.

## Next Step

Phase99 should add runtime profile provisioning for disabled drafts.

Human meaning:

- when an operator adds a tested draft to the pool, V7 should also prepare the
  disabled runtime profile in the correct managed path;
- the channel should still remain disabled;
- after that, readiness should become `READY`, and the next explicit `Enable`
  can be allowed.
