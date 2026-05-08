# V7 Core Hardening Round 1

## Scope

This round intentionally does not refactor the admin UI/backend monolith.

It strengthens the core operational layer around:

- node configuration;
- safe registry parsing;
- operation locking;
- reconcile/drift detection;
- IPAM planning;
- kill-switch live rollout preview;
- isolated egress test readiness;
- secrets cleanup preview;
- local test checks.

## Added Commands

- `v7-node-env`
- `v7-node-config-check`
- `v7-reconcile-check`
- `v7-ipam-preview`
- `v7-policy-live-preview`
- `v7-policy-live-rollback`
- `v7-egress-namespace-check`
- `v7-secrets-cleanup-preview`
- `tests/run-local-checks.sh`

## Strengthened Existing Logic

- `v7-egress-lib`
  - added safe `key=value` helpers;
  - added node config loading;
  - added safe id/ip validators;
  - added lock helper.

- `v7-routing-sync`
  - added locking;
  - loads node config;
  - no longer uses `eval` for user registry rows.

- `v7-user-switch`
  - added locking;
  - validates IP, egress id, and table;
  - no longer uses `eval`;
  - rewrites registry through an awk temp file.

- `v7-user-disable`
  - added locking;
  - validates IP/table;
  - no longer uses `eval`.

- `v7-user-create`
  - added locking;
  - reads endpoint from node config;
  - supports configurable allocation window.

- `v7-users-autoswitch`
  - added locking;
  - no longer uses `eval` for users/egress registry rows.

## What Each New Layer Solves

### Node Config

`/etc/v7/node.env` becomes the place for node-specific facts:

- public IP;
- public interface;
- gateway;
- VPN subnet;
- WireGuard interface/port;
- DNS IP.

This reduces hardcoded server facts across scripts.

### Reconcile Check

`v7-reconcile-check` compares desired/runtime state:

- users registry;
- egress registry;
- assign files;
- live WireGuard allowed IPs;
- `ip rule`;
- route lookup result.

It is read-only and reports drift before it becomes a failure.

### IPAM Preview

`v7-ipam-preview` documents the migration path from current `/24` to future `/22`.

Current recommendation:

- keep existing users on `10.0.0.0/24`;
- allocate future users from a larger pool such as `10.7.0.0/22`;
- do not renumber active users automatically.

### Kill Switch Live Preview

`v7-policy-live-preview` shows what a future live service-aware rollout would need, but does not apply nftables/ip-rule changes.

`v7-policy-live-rollback` defines the future rollback interface and is intentionally blocked as a placeholder until live apply exists.

### Egress Runtime Isolation

`v7-egress-namespace-check` checks whether the server is ready for future namespace-isolated egress candidate tests.

The next implementation step is to run temporary candidates inside `v7rt-<draft-id>` network namespaces.

### Secrets Lifecycle

`v7-secrets-cleanup-preview` lists old generated profiles/QRs and private material without deleting anything.

It starts the lifecycle discipline:

generate -> deliver -> expire/revoke -> cleanup by confirmation.

### Test Contour

`tests/run-local-checks.sh` runs:

- bash syntax checks;
- Python syntax checks;
- `git diff --check`.

## Verification

Local:

```bash
tests/run-local-checks.sh
```

Expected:

```text
V7_LOCAL_CHECKS=OK
```

Server smoke after deployment:

```bash
v7-node-config-check
v7-reconcile-check
v7-ipam-preview
v7-policy-live-preview
v7-egress-namespace-check
v7-secrets-cleanup-preview /root/v7-clients
```

## Next Round

Recommended next hardening round:

1. Replace remaining `eval` usage in older auxiliary scripts.
2. Add `v7-reconcile-repair-preview`.
3. Add real IPAM state file and allocation command.
4. Implement namespace runtime test for WireGuard/AmneziaWG candidates.
5. Add CI or one-command pre-deploy check on every push.
