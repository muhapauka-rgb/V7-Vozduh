# V7 Vozduh Live Runtime Verification Pass

Дата: 2026-05-22  
VPS: `195.2.79.116` / `v3119922.hosted-by-vdsina.ru`  
Mode: live read-only verification  
Важно: production routing/state не редактировались, сервисы не рестартились, nftables/routes не менялись.

## Important Note

Почти все действия были read-only. Исключение: был запущен `v7-trusted-ru-diagnostic`, который сам сообщает `state=/opt/v7/egress/state/trusted-ru-diagnostic.state` и, вероятно, обновляет этот diagnostic state file. Datapath/routing/nftables/users/provisioning не менялись.

## 1. Baseline / Git Status

На VPS не найден обычный git checkout в `/root`, `/opt`, `/srv`, `/var/www`.

`git -C /root status --short`:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Production deploy живёт как standalone executables в `/usr/local/bin` и state/config в `/opt/v7` + `/etc/v7`.

Deployed admin:

```text
/usr/local/bin/v7-admin-api 1747464 2026-05-22 18:39:40 +0300
sha256=f7fbb4234fa1d9a4cf4ef92f4b52bf30d315a9f818a235b7073a18c8a9ffb5d3
```

Old `/root/v7-admin-api` is not current:

```text
/root/v7-admin-api 36767 2026-05-06 19:52:28 +0300
sha256=2510f56d707c9f3e727772c07e5d87bc71f7c88dc9a85834f5bc0abeaea19cb4
```

Verdict:

- **No clean git baseline on VPS.**
- Current deploy is file-based with many backup executables.
- For production governance this is weak: rollback files exist, but source-of-truth deploy revision is not cleanly tied to git.

## 2. Timers / Autoswitch / Sentinel

Active services/timers:

```text
v7-users-autoswitch.timer=active
v7-users-autoswitch.service=inactive
v7-telegram-sentinel.timer=active
v7-telegram-sentinel.service=inactive
v7-service-matrix-refresh.timer=active
v7-egress-quality-compact.timer=active
v7-admin-api.service=active
v7-client-speed-api.service=active
```

Systemd definitions:

```text
v7-users-autoswitch.service:
ExecStart=/usr/local/bin/v7-users-autoswitch --apply

v7-users-autoswitch.timer:
OnBootSec=2min
OnUnitActiveSec=20s
AccuracySec=5s

v7-telegram-sentinel.service:
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1

v7-telegram-sentinel.timer:
OnBootSec=30s
OnUnitActiveSec=4s
AccuracySec=1s
```

Autoswitch policy:

```json
{
  "autoswitch_enabled": true,
  "autoswitch_mode": "guarded",
  "cooldown_seconds": 300,
  "autoswitch_max_planned_per_run": 3,
  "autoswitch_max_failover_per_run": 100
}
```

Live autoswitch journal showed:

- `apply_requested=true`;
- `selected_moves=0` at the checked moment;
- users frozen / cooldown active;
- recent history in autoswitch explanation included up to **5 switches in 1 hour** and **10 switches in 24 hours** for some users;
- `failed_verifications_1h=0`.

Verdict:

- Autoswitch is **really live in apply mode**, not mock/dry-run.
- Anti-flap is active and currently preventing further moves.
- However, recent failover volume is high. This is a real stability concern.
- `autoswitch_max_failover_per_run=100` is dangerously high for 16 users. It allows mass movement in one run if gates permit.

Recommended immediate safety change:

- Consider pausing `v7-users-autoswitch.timer` or reducing failover bounds only after explicit maintenance decision.
- At minimum, lower `autoswitch_max_failover_per_run` from `100` to a small bounded value.
- Review whether Telegram sentinel is allowed to trigger autoswitch apply. Its 4s timer is aggressive.

## 3. Kill Switch / No-Leak

Commands run:

- `v7-killswitch-status`
- `v7-killswitch-check`
- `v7-user-route-check`
- `v7-provisioning-reconcile-check`
- `ip rule show`
- filtered `nft list ruleset`

Result:

```text
V7_KILLSWITCH_STATUS=enabled
V7_KILLSWITCH_CHECK=OK
V7_USER_ROUTE_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Kill switch nftables has:

- client source set:
  - `10.0.0.0/24`
  - `10.7.0.0/22`
- DNS capture for VPN clients;
- NAT for enabled egress:
  - `awg0`
  - `awg3`
  - `tun0`
  - `v7e06a394c478`
  - `v7e356a192b79`
  - `v7edb0c189291`
- explicit allow for direct whitelist;
- explicit drop:

```text
ip saddr @v7_client_src oifname "ens3" counter packets 0 bytes 0 drop comment "V7 block direct leak to public interface"
```

Per-user route checks:

- 16 enabled users checked.
- Every user matched registry assignment.
- Every user route table had default route via assigned egress.
- Every `route_get` with `iif wg0` used expected egress.

Manual `ip route get` without `iif wg0`:

```text
ip route get 1.1.1.1 from 10.0.0.2 -> Network is unreachable
ip route get 1.1.1.1 from 10.7.0.2 -> Network is unreachable
```

This is not the real forwarded-client path, but it does not indicate a public-interface leak.

Verdict:

- **Kill switch/no-leak is VERIFIED WORKING by live built-in checks.**
- Direct public leak counter is currently `0`.
- This is the strongest positive result of the pass.

Remaining caveat:

- This verifies current state, not future rebuild safety after restart/reconcile/provisioning.

## 4. Routing / Direct RU / Trusted RU

Current users:

- 16 enabled users.
- Assigned only to:
  - `awg0`
  - `awg3`

Current egress registry:

- `vless` enabled, interface `tun0`, role not shown in registry line.
- `awg0` enabled, role `GLOBAL_STABLE`.
- `awg3` enabled, role `GLOBAL_STABLE`.
- `1` enabled, role `GLOBAL_FAST`, excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU`.
- `openvpn-1779388847-d2ad7c` enabled, role `GLOBAL_FAST`, excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU`.
- `wireguard-1779454504-c43409` enabled, role `GLOBAL_FAST`, excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU`.

Direct status:

```text
dnsmasq=active
killswitch=active
fwmark 0x77 lookup table 70
table 70 default via 195.2.79.1 dev ens3
```

Direct/RU domain tests:

### `ya.ru`

- policy: `DIRECT_READY`
- direct HTTPS: `302`
- direct OpenSSL: `OK`
- vless HTTPS: `302`

### `vk.com`

- policy: `DIRECT_READY`
- direct HTTPS: `302`
- direct OpenSSL: `OK`
- vless HTTPS: `302`

### `www.gosuslugi.ru`

`v7-policy-test-domain`:

```text
route_class=TRUSTED_RU_SENSITIVE
mode=egress
active_egress=vless
mark=0x78
table=71
local_direct=TCP_TIMEOUT_BEFORE_TLS
decision=SERVICE_AWARE_SENSITIVE
desired_path=vless
reason=sensitive_app_overrides_broad_direct
```

`v7-direct-test-domain`:

```text
decision=VPN_PREFERRED_DIRECT_EXCLUDED
```

`v7-direct-diagnose-domain`:

```text
DIRECT_DNS=OK
DIRECT_ROUTE=FAIL
SERVER_HTTPS=TIMEOUT
V7_DIRECT_DOMAIN_RESULT=FAIL
```

`v7-trusted-ru-diagnostic`:

- for `www.gosuslugi.ru`:
  - direct timeout;
  - vless timeout;
  - openssl direct failed.
- for `ya.ru` and `vk.com`: OK.
- overall tool output still ended with:

```text
V7_TRUSTED_RU_DIAGNOSTIC=OK
```

Verdict:

- Direct/RU works for broad RU sites like `ya.ru` and `vk.com`.
- Trusted RU sensitive handling for `www.gosuslugi.ru` is **not actually working** in this live check.
- The diagnostic overall `OK` while one sensitive domain fails is a serious observability/semantics problem.

Recommended immediate fix:

- Treat per-domain sensitive failures as degraded/blocker, not overall OK.
- Do not silently present Trusted RU as healthy when `TRUSTED_RU_SENSITIVE` target fails.

## 5. State Contracts / Identity DB Path

State directory exists and is active:

```text
/opt/v7/egress/state
```

Important files present:

- `users.registry`
- `egress.registry`
- `v7-state.json`
- `autoswitch-safety.json`
- `service-matrix.json`
- `egress-quality-summary.json`
- `telegram-sentinel.json`
- `client-reconnect-state.json`
- `profile-delivery-tokens.json`
- `trusted-ru-diagnostic.state`

Runtime summary:

```text
v7-state.json: users=16 egress=6
autoswitch-safety.json: users_tracked=16 egress_tracked=5
telegram-sentinel.json: checked=6 blocked=[] healthy=['awg0','awg3','openvpn-...','wireguard-...']
service-matrix.json: dict_items=6 statuses={'WARN': 5, 'OK': 1}
egress-quality-summary.json: tracked=8
client-reconnect-state.json: users=16
```

Identity DB:

```text
/opt/v7/admin/v7-identity.db exists
/opt/v7/identity/v7-identity.db missing
```

Identity DB counts via read-only SQLite URI:

```text
organizations 3
groups 1
identity_users 11
devices 20
allowed_users 6
connect_sessions 8
pending_profiles 3
provisioning_jobs 8
onboarding_attempts 41
access_settings 1
user_metadata 2
```

Verdict:

- Live identity DB path is `/opt/v7/admin/v7-identity.db`.
- Any tooling expecting `/opt/v7/identity/v7-identity.db` is wrong for this VPS.
- State contracts exist and are active.
- State is scattered but operational.

## 6. External `v7-*` Commands

There are many installed `v7-*` commands in `/usr/local/bin`, including critical ones:

- `v7-user-switch`
- `v7-user-route-check`
- `v7-users-autoswitch`
- `v7-killswitch-check`
- `v7-killswitch-enable`
- `v7-routing-sync`
- `v7-provisioning-reconcile-check`
- `v7-direct-*`
- `v7-policy-*`
- `v7-trusted-ru-*`
- `v7-egress-*`
- `v7-service-matrix-*`
- `v7-telegram-sentinel`
- `v7-backup-*`
- `v7-rollback-last-change`

But `/usr/local/bin` also contains many executable backups:

- `v7-admin-api.backup-*`
- `v7-admin-api.bak.*`
- `v7-users-autoswitch.backup.*`
- several `.bak.*` variants for tools.

Verdict:

- External command dependency is mostly satisfied on this VPS.
- Operational clutter is high.
- Backup executables in `/usr/local/bin` should not be on executable PATH forever.

Recommended cleanup:

- Move old executable backups to a non-PATH archive directory after a safe backup.
- Keep only current command names executable in `/usr/local/bin`.

## 7. Observability / Quality Contradictions

Service matrix:

```text
1: OK, telegram=DEGRADED, some AI services HTTP_LIMITED
awg0: WARN, most core services OK, AI services HTTP_LIMITED
awg3: WARN, most core services OK, AI services HTTP_LIMITED
openvpn: WARN, most core services OK, AI services HTTP_LIMITED
vless: WARN, most core services OK, AI services HTTP_LIMITED
wireguard: WARN, several HTTP_LIMITED
```

Quality summary:

```text
1: strong quality, stable
awg0: moderate quality, stability around 0.43-0.49
awg3: degrading/weak, min below floor, stability below floor
vless: low stability, min below floor
openvpn: high speed/stability but fail_rate ~0.9999
wireguard new: high speed/stability but fail_rate ~0.9999
```

Load summary conflict:

- `summary.state` says:
  - `awg0_load_status=HARD_FULL`
  - `awg3_load_status=HARD_FULL`
  - because static soft/hard limits are `1/2`.
- autoswitch dynamic load logs show:
  - `awg0`/`awg3` load `8/24`, status `OK`.

Verdict:

- Observability is rich but not fully coherent.
- Multiple subsystems produce different health semantics.
- This can confuse operator decisions.

Must fix:

- One authoritative operator health summary.
- Separate "service-specific WARN" from "route unusable".
- Fix/load-align static summary vs dynamic autoswitch capacity.

## 8. Admin Runtime

`v7-admin-api.service`:

```text
Active: active (running)
Main PID: python3 /usr/local/bin/v7-admin-api
Listening: http://127.0.0.1:7080
Memory: 85.2M
CPU: 23min over 4h56m uptime
```

`/` redirects to `/admin-v2`.

`/admin-v2` redirects to `/login`.

`/api/overview` returns unauthorized without auth.

`/admin` returns 404.

Verdict:

- Admin runtime is active and protected by login for admin-v2/api overview.
- `/admin` is not the active path; active UI is `/admin-v2`.
- Service sandboxing includes `NoNewPrivileges`, `PrivateTmp`, `ProtectHome=read-only`, and limited `ReadWritePaths`, which is good.

## 9. What Really Works

Verified working live:

- VPS reachable.
- V7 runtime state exists and is fresh.
- Admin service running.
- Client speed service running.
- Kill switch enabled.
- No-leak guard present.
- User route checks pass for all 16 users.
- Provisioning reconcile check passes.
- Direct/RU path works for `ya.ru` and `vk.com`.
- External v7 commands are installed.
- Autoswitch is active and bounded by cooldown/freeze at the checked moment.
- Identity DB exists and is readable at `/opt/v7/admin/v7-identity.db`.

## 10. What Is Dangerous

1. **Autoswitch is live in apply mode every 20s.**
2. **Telegram sentinel runs every 4s.**
3. **Recent users had up to 5 switches/hour and 10 switches/day.**
4. **`autoswitch_max_failover_per_run=100` is too high for the current 16-user platform.**
5. **Trusted RU diagnostic says overall OK while `www.gosuslugi.ru` fails.**
6. **Observability health semantics conflict between service matrix, quality summary, sentinel, and load summary.**
7. **No git baseline on VPS.**
8. **Many executable backups live in `/usr/local/bin`.**
9. **Identity DB path mismatch remains real: admin path exists, alternate path missing.**

## 11. What To Disable / Pause

I did not disable anything.

Candidates to consider in a maintenance window:

1. Pause or reduce `v7-users-autoswitch.timer` if user-visible instability continues.
2. Disable autoswitch apply from Telegram sentinel or add stronger persistence threshold.
3. Lower `autoswitch_max_failover_per_run`.

Do not disable kill switch.

## 12. What To Fix First

Priority fixes:

1. Trusted RU: make per-domain failure visible as degraded/blocker.
2. Autoswitch: reduce failover bounds and investigate why users switched 5/hour.
3. Observability: align health semantics.
4. State contracts: standardize identity DB path to `/opt/v7/admin/v7-identity.db` or migrate explicitly.
5. Deployment: create git-linked release baseline for `/usr/local/bin` deploy.
6. Cleanup: remove executable backups from PATH into archive storage.
7. UI: show "autoswitch frozen users / high recent switch rate" as operator incident.

## Final Verdict

The live VPS is **not broken** and has a working datapath safety foundation.

The strongest verified result is:

- kill switch enabled;
- no-leak guard present;
- route checks OK for all users;
- provisioning reconcile OK.

The biggest production risks are:

- autoswitch instability history;
- too-high failover limit;
- Telegram sentinel aggressiveness;
- Trusted RU sensitive failure hidden behind an overall OK;
- inconsistent observability health semantics.

The platform is operational, but not calm or fully mature yet. It is closer to "working production prototype with real safety controls" than to "commercial-grade predictable platform".

