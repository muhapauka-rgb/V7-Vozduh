# V7 Track 6 Sensitive-State Access Map

Track 6 is a dry run. No permission changes are applied here.

## Sensitive-State Inventory Model

| File | Sensitivity | Runtime Criticality | Primary Readers | Primary Writers | Initial Target |
|---|---|---|---|---|---|
| `/opt/v7/egress/state/profile-delivery-tokens.json` | High | profile delivery/onboarding | admin API, public delivery/import handlers through admin process, identity consistency review | admin API profile delivery create/consume/revoke/prune | `0600` or `0640` after service ownership confirmation |
| `/opt/v7/admin/v7-identity.db` | High | identity/users/devices/onboarding | admin API, identity consistency review | admin API identity lifecycle | keep `0600` |
| `/etc/v7/policy.json` | Medium | autoswitch hard policy | admin API, autoswitch, safety review, observability summary | admin API/operator maintenance | `0640` after service group confirmation |
| `/etc/v7/org-egress-policy.json` | Medium | org/egress eligibility | admin API, autoswitch, observability, identity consistency review | admin API/operator maintenance | `0640` after service group confirmation |
| `/opt/v7/egress/state/users.registry` | Medium | active user routing assignments | admin API, autoswitch, kill switch check, reconcile check, observability, identity consistency, client speed API | admin/provisioning/user switch flows | `0640` after service group confirmation |
| `/opt/v7/egress/state/egress.registry` | Medium | egress lifecycle/routing | admin API, autoswitch, service matrix, sentinel, kill switch/reconcile checks, observability | admin/provisioning/egress lifecycle tools | `0640` after service group confirmation |
| `/opt/v7/egress/state/autoswitch-safety.json` | Medium | anti-flap/freeze/quarantine memory | autoswitch, safety review, observability, admin diagnostics | autoswitch | `0640` after autoswitch writer confirmation |
| `/opt/v7/egress/state/client-reconnect-state.json` | Medium | client experience/autoswitch support signal | autoswitch, safety review, observability, admin diagnostics | autoswitch/client telemetry tools if enabled | `0640` after writer confirmation |

## Current Known Live Baseline

Track 4 previously observed:

- `profile-delivery-tokens.json`: `0644 root:root`, high commercial risk.
- `v7-identity.db`: `0600 root:root`, controlled.
- policies, registries, autoswitch safety and reconnect state: mostly `0644 root:root`, legacy-operational but commercially weak.

Track 6 adds `tools/v7-sensitive-state-check` so the same metadata can be checked read-only on the runtime host before any hardening.

## Runtime Access Notes

The repository systemd units do not specify a `User=` field, so the file-based deployment is currently assumed root-run unless live unit overrides differ.

Important: this assumption must be verified on the VPS before applying any chmod/chown.

## Dry-Run Breakage Model

### `profile-delivery-tokens.json -> 0600`

Likely safe only if the same owner runs:

- admin API;
- public profile delivery/import handlers;
- profile delivery create/consume/revoke flows.

Breakage risk:

- public delivery fails if served by a separate non-root process;
- profile issuing fails if admin API cannot write token state;
- stale token pruning fails if admin API cannot update the file.

### `policy.json` and `org-egress-policy.json -> 0640`

Potentially safe with a shared service group.

Breakage risk:

- autoswitch cannot read policy;
- observability summary cannot explain health/policy gates;
- admin policy update cannot write unless owner/group model is correct.

### `users.registry` and `egress.registry -> root-only`

Not currently safe to apply blindly.

Breakage risk:

- autoswitch planning/apply cannot read assignments;
- kill switch/reconcile checks may fail;
- service matrix/sentinel may lose egress inventory;
- provisioning and admin lifecycle flows may fail.

### `autoswitch-safety.json` and `client-reconnect-state.json -> 0640`

Potentially safe only after confirming autoswitch timer writer identity.

Breakage risk:

- anti-flap/freeze/quarantine memory cannot update;
- reconnect signal updates fail;
- operator health summary becomes misleading.

## Safe Hardening Sequence

Stage 1: read-only validation.

- Run `tools/v7-sensitive-state-check --pretty` on the runtime host.
- Confirm live modes/owners/groups.
- Confirm systemd `User=`/drop-ins for admin API, autoswitch, sentinel, quality compactor, service matrix refresh, public gateway.

Stage 2: single-file dry-run review.

- Start with `profile-delivery-tokens.json`.
- Confirm all profile delivery readers/writers run as owner or agreed group.
- Prepare metadata backup and rollback command.

Stage 3: bounded apply with rollback.

- Change one file class only.
- Verify admin API profile delivery create/download/revoke paths.
- Verify `tools/v7-run-tests` locally and live runtime checks separately.

Stage 4: policy/registry group model.

- Only after service users and group model are explicit.
- Avoid recursive chmod/chown.

## Calm Operator UX Summary

Recommended summary shape:

```text
Sensitive-state warnings: 2
Commercial exposure: medium/high
Profile token exposure: high
Runtime-safe hardening candidate: profile delivery tokens, pending service-user confirmation
Identity DB: controlled
Policy/registry hardening: staged only
```

Do not expose raw tokens or full file contents in UI.
