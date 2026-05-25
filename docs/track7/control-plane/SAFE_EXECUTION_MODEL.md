# Safe Execution Model

This is the future control-plane execution model. It does not authorize running live mutations now.

## 1. Inspect

Allowed:

- read lineage metadata;
- read `runtime-enumeration.json`;
- read registry/state snapshots;
- run static syntax checks;
- run read-only governance checker.

Forbidden:

- any command that writes state;
- any route/nft/ip/systemctl mutation.

## 2. Preview

Allowed only when the preview is confirmed non-mutating. Some V7 dry-runs still write summaries or reconnect state, so preview commands must be classified first.

Required checks:

- command source inspected;
- write paths known;
- output redaction known;
- stale-state handling clear.

## 3. Dry-Run

Allowed only after explicit confirmation that low-risk state writes are acceptable. Examples that need caution:

- autoswitch planning can write load summary and reconnect state;
- policy apply `--apply` writes preview state even though live marks are blocked.

## 4. Canary One User

Only for user movement. Required:

- `tools/v7-route-movement-preview user-switch ...` generated with `mutation=false`;
- preview has no `errors`;
- previous egress captured;
- target egress health/capacity OK;
- kill switch OK before switch;
- one user only;
- post route check;
- rollback command prepared.

Routing-sync cannot be the first live mutation. The first canary must be a single explicit user switch after preview tests pass.

## 5. Bounded Apply

Allowed only after canary success. Required:

- max planned moves explicit;
- max failover moves explicit;
- target egress projected load below hard limit;
- anti-flap state readable;
- Telegram/Trusted RU signals not stale;
- admin approval recorded.

## 6. Post-Check

Mandatory after any datapath mutation:

```text
v7-killswitch-check
v7-user-route-check
ip route get samples for changed users
service status for changed service layer
audit/switch log verification
```

## 7. Rollback

Rollback must be defined before apply:

| Mutation | Rollback |
|---|---|
| User switch | switch same user back to previous egress |
| Autoswitch | automatic rollback on failed route verify plus manual switch-back plan |
| Routing sync | restore registry backup, rerun sync only with approval |
| Direct/RU config | restore config backup, render/restart only with approval |
| Proxy guard | `v7-proxy-runtime-guard-rollback` with backup dir |
| Kill switch | restore known-good nft/ip route state or rerun known-good enable |
| Trusted RU state | restore/remove diagnostic and decision state snapshot |

Commands forbidden until separate approval:

```text
v7-trusted-ru-refresh-missing
v7-trusted-ru-diagnostic
v7-routing-sync
v7-user-switch
v7-users-autoswitch --apply
v7-policy-apply --apply
v7-policy-apply-systemd --apply
v7-proxy-runtime-guard-apply
v7-killswitch-enable
v7-killswitch-disable-temporary
```

Preview commands allowed in repo/local tests:

```text
tools/v7-route-movement-preview user-switch --users-registry <fixture> --egress-registry <fixture> --user-ip <ip> --to-egress <egress>
tools/v7-route-movement-preview routing-sync --users-registry <fixture> --egress-registry <fixture>
```

The preview planner is read-only and does not call runtime commands.
