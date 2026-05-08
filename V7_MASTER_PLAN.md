# V7 Master Plan

Date: 2026-05-06
Status: active working plan

## Standing Principle

V7 is not a single VPN server. V7 is a VPN aggregation and orchestration platform.

All future work must optimize for:

- correctness before speed
- no direct traffic leaks
- stable user experience
- sticky assignment instead of constant switching
- controlled failover
- controlled, gradual rebalance
- auditability
- rollback
- eventual 500+ user scale
- proven infrastructure patterns: control plane, data plane, reconciliation, immutable backups, audit logs, staged rollout

The current shell-core is valuable and must not be rewritten prematurely. The next architecture wraps it with safer provisioning, admin UI, and eventually a controller.

## What Is Already Done

Migration to new VPS is functionally complete.

Current VPS:

```text
IP: 195.2.79.116
OS: Ubuntu 26.04 x86_64
public interface: ens3
inbound: wg0
vless egress: tun0
awg egress: awg2
```

Completed:

- V7 scripts/config/state migrated.
- x86_64 `sing-box` installed.
- x86_64 AmneziaWG tooling installed.
- `wg0` works.
- `sing-box/tun0` works.
- `awg2` works.
- `v7-routing-sync.service` added for boot-time routing restore.
- V7 services enabled and active.
- `/health` returns OK.
- `/state` returns valid JSON.
- `v7-system-check` returns `V7_RESULT=OK`.
- iPhone client `10.0.0.3` works.
- NAT lesson fixed:
  - client subnet to `awg2`
  - client subnet to `tun0`
- First provisioning scripts added:
  - `/usr/local/bin/v7-user-create`
  - `/usr/local/bin/v7-user-disable`

## Immediate Priority

The next work must harden the current working core before building a large admin UI.

Priority order:

1. Kill switch engine.
2. Direct RU / whitelist routing design.
3. Safe mode and diagnostics.
4. User provisioning reconciliation.
5. Backup/restore/rollback.
6. Stale state detection.
7. Admin MVP, local-only.
8. Multi-egress generalization.
9. Installer.

## Phase 0C: Smart Client Profiles

Goal: make V7 usable through real client apps that support domain/geosite routing, not only raw WireGuard.

Primary targets:

- iPhone: Karing, Happ
- Android: Hiddify, Happ
- Desktop: Clash Verge Rev, Karing

The server remains the V7 orchestration core, but generated client profiles can decide whether selected domains should reach V7 or leave directly from the user's device.

Required route modes:

- `RU_LOCAL`: ordinary RU and sensitive RU go `DIRECT_CLIENT`; global/video goes through V7.
- `ABROAD_RU_VIA_V7`: ordinary RU goes through V7 server-side RU direct; government/sensitive portals go through a dedicated tested trusted RU path for users outside Russia.
- `AUTO_TRAVEL`: profile exposes a selector so user/operator can switch between client direct, V7 Russia, and trusted abroad.
- `STRICT_V7`: RU/global traffic reaches V7 for maximum server-side control.

Important travel case:

```text
User travels to Thailand.
If RU direct from phone is accepted, use RU_LOCAL.
If RU services reject foreign direct IP, switch to ABROAD_RU_VIA_V7.
Government portals must use RU_GOV_ABROAD, a separately tested route candidate.
```

`RU_GOV_ABROAD` must not be treated as solved until it passes real tests against Gosuslugi/ESIA/Nalog/government portals from the V7 server side.

## Phase 1: VPS Baseline Hardening

Goal: make the current VPS safe to run and recover.

Tasks:

- Create a post-migration audit snapshot.
- Add `v7-killswitch-check`.
- Add `v7-killswitch-enable`.
- Add `v7-killswitch-status`.
- Add `v7-killswitch-disable-temporary`.
- Ensure kill switch never locks out SSH.
- Deny direct user traffic from VPN subnet to `ens3`.
- Allow server control traffic via `ens3`.
- Allow egress tunnel endpoint traffic via `ens3`.
- Verify user traffic only exits through approved egress interfaces.
- Add stale-state warning if `v7-state.json` is old.
- Add journal/log size limits.
- Add disk checks before backup/install/heavy diagnostics.

Required invariant:

```text
10.0.0.0/24 must never exit directly via ens3.
```

Exception:

```text
10.0.0.0/24 may exit via ens3 only when destination is explicitly classified as direct/whitelisted.
```

## Phase 1B: Direct RU / Whitelist Routing

Goal: let users keep one V7 tunnel while Russian/whitelisted sites go directly from the V7 server without external VPN.

Required behavior:

```text
default traffic -> user's assigned egress, for example awg2 or tun0
.ru / whitelisted traffic -> direct via ens3
```

This is server-side destination policy routing, not client-side split tunnel.

Important implementation note:

Linux routes IPs, not domains. To route `.ru` domains directly, V7 needs a DNS classification layer.

Recommended MVP:

- run local DNS resolver for VPN clients
- set generated client configs to `DNS = 10.0.0.1`
- maintain domain whitelist
- resolve whitelisted domains into dynamic nftables set
- mark packets to whitelisted destination IPs
- send marked packets to direct table via `ens3`
- kill switch allows `ens3` only for whitelisted destinations

Do not allow generic user traffic from VPN subnet to `ens3`.

Important finding from testing:

```text
general RU sites may work via direct ens3, but sensitive RU services such as gosuslugi.ru may reject VPS/VPN-like IPs.
```

Therefore direct routing must support route classes:

- `VPN_DEFAULT`
- `DIRECT_RU`
- `TRUSTED_RU`
- `BLOCKED`
- `UNKNOWN`

`gosuslugi.ru`, `www.gosuslugi.ru`, `esia.gosuslugi.ru`, and `lk.gosuslugi.ru` should be treated as `TRUSTED_RU_REQUIRED` until a vetted trusted RU egress passes real TCP/TLS tests.

Next required capability:

- add a trusted RU egress candidate
- test it against sensitive services
- only then map those domains to that egress

Future commands:

- `v7-direct-status`
- `v7-direct-list`
- `v7-direct-add-domain`
- `v7-direct-remove-domain`
- `v7-direct-test-domain`
- `v7-direct-sync`

Admin UI must show:

- why a domain goes direct or VPN
- last resolved direct IPs
- direct route hit counters
- warnings if client DNS bypasses V7
- warning when a domain requires trusted RU but no trusted RU egress exists

## Phase 2: Provisioning Layer

Goal: make user creation safe enough to become admin API logic later.

Already started:

- `v7-user-create`
- `v7-user-disable`

Next:

- Add `v7-users-sync`.
- Add `v7-user-status`.
- Add `v7-user-rotate-key`.
- Add `v7-user-export`.
- Add structured audit events for create/disable/rotate/switch.
- Add rollback for last provisioning operation.
- Stop treating `/etc/wireguard/wg0.conf` as the long-term source of truth.

For 500 users, manual config editing is not the model. The long-term source of truth should be a database and generated config/runtime state.

## Phase 3: Backup, Restore, Rollback

Goal: every risky change has an escape hatch.

Backup should include:

- `/usr/local/bin/v7-*`
- `/etc/systemd/system/v7-*.service`
- `/etc/wireguard`
- `/etc/amnezia`
- `/etc/amneziawg`
- `/etc/sing-box`
- `/opt/v7`
- provisioning client metadata, excluding avoidable log bulk

Add commands:

- `v7-backup-create`
- `v7-backup-list`
- `v7-backup-restore`
- `v7-rollback-last`

Rules:

- never overwrite without timestamped backup
- never restore secrets/configs without explicit confirmation
- always validate after restore

## Phase 4: Admin MVP

Goal: local-only control center that wraps existing V7 core.

Do not expose externally until auth is implemented.

First admin MVP pages:

- Dashboard
- Users
- Egress pool
- Diagnostics
- Rebalance preview
- Events/logs
- Backups
- Settings

First admin actions:

- run system check
- show `/state`
- show egress health
- show users and route status
- create user
- show/download QR
- disable user
- switch one user manually
- run rebalance dry-run
- apply one rebalance move

Auth/security:

- password setup
- sessions
- CSRF protection if forms are used
- local-only default binding
- secrets redaction
- audit log for every admin action

## Phase 5: User-Facing Page

Goal: simple page for non-technical users.

Two primary actions:

- Connect to VPN
- Reconnect

It may:

- show QR
- download config
- trigger server-side reassignment/reconnect
- show plain-language status

It must not pretend it can silently change iPhone/macOS VPN settings.

## Phase 6: Egress Pool And Protocol Adapters

Goal: support many external channels without hardcoding `vless` and `awg2`.

Adapter model required for:

- WireGuard
- AmneziaWG
- VLESS Reality / Xray / sing-box
- Outline
- OpenVPN
- IPsec
- SOCKS
- HTTP proxy
- 3proxy
- 3X-UI share links

Each adapter must define:

- detect
- validate
- install requirements
- bring up
- stop
- status
- direct IP test
- logs
- cleanup
- kill switch integration

Rule:

```text
Never add a new egress to active pool until it passes direct egress and leak tests.
```

## Phase 7: Service Matrix

Goal: measure real-world usability, not just raw speed.

Test layers:

- DNS
- TCP connect
- TLS handshake
- first byte
- optional small download

Services:

- YouTube
- Instagram
- Telegram
- WhatsApp
- Facebook
- Spotify
- SoundCloud
- Google
- Apple
- Cloudflare

This should influence quality scoring, but must not cause constant user switching.

## Phase 8: Installer

Goal: non-programmer can install V7 safely.

Installer steps:

- OS check
- architecture check
- root check
- disk/RAM/CPU check
- public IP detection
- default interface detection
- package install
- forwarding setup
- firewall/kill switch baseline
- inbound VPN setup
- first egress setup
- full validation
- admin access setup
- backup and final report

Installer must stop on critical failures and offer rollback.

## Scale Notes For 500+ Users

Current `/24` is a short-term MVP range.

Before real scale:

- move to larger VPN subnet, for example `/22`
- stop relying on one hand-edited config file
- introduce DB-backed IPAM
- introduce reconciliation worker
- measure cost of 500 `ip rule` entries
- evaluate nftables maps or fwmark routing after current model is automated

Do not optimize routing model prematurely. First automate and measure.

## Product And UX Direction

Admin UI should feel like a premium technical control center, not a decorative landing page.

Style:

- dark theme first
- calm surfaces
- compact cards
- clear status chips
- plain language first
- technical details expandable
- no visual noise
- no exposed secrets by default

The dashboard answers:

- Is V7 working?
- Are users online?
- Which egresses are healthy?
- Is kill switch safe?
- Any leak risk?
- What needs action?
- What would rebalance do?

## Non-Negotiables

- Do not destroy the old VM.
- Do not rewrite working V7 core prematurely.
- Do not enable automatic rebalance in health loop.
- Do not expose admin externally without auth.
- Do not print private keys in logs or chat.
- Do not add untested egress to active pool.
- Do not delete egress with users on it.
- Do not allow direct leak via public interface.
- Do not make mass user moves in one rebalance.
- Keep production cooldown at least 180 seconds.
