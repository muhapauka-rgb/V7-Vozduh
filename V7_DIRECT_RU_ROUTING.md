# V7 Direct RU / Whitelist Routing

Date: 2026-05-06
Status: required architecture addition

## Requirement

Some destinations must bypass external VPN egresses and leave directly from the V7 server.

Example:

```text
User phone/laptop -> wg0 -> V7 -> direct via ens3 -> .ru / whitelisted site
```

This means the user can keep a single VPN tunnel to V7, while V7 decides:

- normal traffic -> external egress, for example `awg2` or `tun0`
- whitelisted traffic -> direct VPS public interface `ens3`

This is not client-side split tunneling. The client still uses V7 as its single VPN endpoint.

## Updated Finding: Sensitive RU Sites

Testing on 2026-05-06 showed that general RU direct routing works for sites such as:

- ozon.ru
- lamoda.ru
- yandex.ru
- mos.ru
- nalog.gov.ru

But `gosuslugi.ru` / `www.gosuslugi.ru` / `esia.gosuslugi.ru` / `lk.gosuslugi.ru` timed out from:

- VPS direct public interface `ens3`
- current `awg2` egress
- current `vless` egress

Conclusion:

Some sensitive RU services may reject or blackhole datacenter/VPS/VPN-like source IPs even when routing is technically correct.

Therefore V7 needs another route class:

```text
trusted_ru
```

This should be a vetted RU egress channel with an IP accepted by sensitive Russian services.

Examples:

- residential RU ISP channel
- mobile RU channel
- trusted RU provider channel
- dedicated RU egress tested against sensitive services

Gosuslugi should not be treated as just generic `.ru direct` until the source path is proven.

## Important Distinction

V7 has two routing decisions:

1. User default egress assignment:

```text
10.0.0.3 -> table 101 -> awg2
```

2. Destination override:

```text
destination in direct whitelist -> ens3
```

The destination override must be more specific than default user egress routing.

## Why This Is Hard

Linux routing works on IP addresses, not domains.

The requirement says `.ru` sites, but packets contain destination IPs, not domain names. Therefore V7 needs a domain-to-IP classification layer.

Possible approaches:

### Option A: DNS-based nftables/ipset

Use local DNS resolver for VPN clients.

Flow:

```text
client DNS request -> V7 DNS resolver -> detects .ru / whitelist domain -> stores resolved IP in nft set -> packets to those IPs route direct
```

Pros:

- practical MVP
- fast
- works for normal browser/app DNS
- admin can manage domain whitelist

Cons:

- does not catch hardcoded IPs
- does not catch client DoH/DoT unless blocked or redirected
- CDN IPs may be shared by non-whitelisted domains

### Option B: sing-box/Xray routing rules

Route by domain inside a proxy/tun engine.

Pros:

- strong domain routing if traffic is handled by the engine
- good protocol ecosystem

Cons:

- current architecture uses Linux policy routing and external egress interfaces
- bigger architectural change
- must avoid rewriting current core prematurely

### Option C: Static IP lists

Maintain known IP ranges for government/bank/ru services.

Pros:

- no DNS dependency
- clear kill switch behavior

Cons:

- hard to keep current
- `.ru` as a TLD cannot be represented safely as static IP ranges

## Recommended MVP

Use DNS-based dynamic nftables sets.

Components:

- local DNS resolver for VPN clients, for example `dnsmasq` or `unbound`
- direct domain whitelist
- dynamic nftables set of resolved direct IPs
- policy routing or packet marking for direct destinations
- kill switch rule that only allows direct via `ens3` when destination is in direct whitelist set

Recommended client DNS:

```text
10.0.0.1
```

Current generated client configs should later use:

```text
DNS = 10.0.0.1
```

instead of public DNS, so V7 can classify domains.

## Whitelist Model

Do not treat all `.ru` blindly as the only rule forever. Use a managed whitelist model:

```text
direct_tld:
  - .ru
  - .рф

direct_domains:
  - gosuslugi.ru
  - nalog.gov.ru
  - mos.ru

direct_exceptions:
  - domains that should still use VPN if needed

trusted_ru_domains:
  - gosuslugi.ru
  - www.gosuslugi.ru
  - esia.gosuslugi.ru
  - lk.gosuslugi.ru
```

Admin UI should show this as:

- Direct websites
- VPN websites
- Exceptions

Plain language:

```text
Russian/government sites go directly through V7 server.
Other sites go through selected VPN channel.
Sensitive government sites may require a trusted Russian channel.
```

## Route Classes

V7 should classify destinations into route classes:

```text
VPN_DEFAULT
DIRECT_RU
TRUSTED_RU
BLOCKED
UNKNOWN
```

Meaning:

- `VPN_DEFAULT`: use user's sticky assigned egress.
- `DIRECT_RU`: go directly through VPS public interface `ens3`.
- `TRUSTED_RU`: use a special trusted Russian egress, not generic VPN.
- `BLOCKED`: block intentionally.
- `UNKNOWN`: fallback to VPN default unless policy says otherwise.

For now:

```text
.ru general -> DIRECT_RU
gosuslugi/esia -> TRUSTED_RU required
```

Until a trusted RU egress exists, admin should show:

```text
Gosuslugi requires action: no trusted RU route configured.
```

## Routing Design

Short-term design:

1. Client sends DNS to V7.
2. Resolver detects direct domains.
3. Resolver adds returned IPs to nft set:

```text
v7_direct_dst
```

4. nftables marks packets from VPN subnet to those IPs:

```text
source 10.0.0.0/24 destination @v7_direct_dst -> mark DIRECT
```

5. policy rule sends marked packets to direct table:

```text
fwmark DIRECT lookup 70
table 70 default via 195.2.79.1 dev ens3
```

6. NAT allows marked direct traffic through `ens3`.

## Kill Switch Interaction

Kill switch must not block approved direct traffic, but must block leaks.

Allowed:

```text
10.0.0.0/24 -> @v7_direct_dst -> ens3
10.0.0.0/24 -> awg2
10.0.0.0/24 -> tun0
```

Denied:

```text
10.0.0.0/24 -> ens3 when destination not in direct whitelist
```

This is the key safety invariant:

```text
User traffic may go direct only if destination is explicitly classified as direct.
```

## Admin Requirements

Admin must support:

- view direct whitelist
- add domain
- remove domain
- add exception
- test domain route
- show whether a domain goes direct or VPN
- show last resolved IPs
- show direct route hit counters
- warn if client DNS is not V7 DNS
- show route class: VPN_DEFAULT / DIRECT_RU / TRUSTED_RU
- warn when a domain requires trusted RU but no trusted RU egress is healthy

Example admin test:

```text
Domain: gosuslugi.ru
Decision: TRUSTED_RU_REQUIRED
Route: none
Leak risk: none
Reason: generic direct path tested but TCP 443 timed out
```

## Testing Requirements

Add future commands:

- `v7-direct-list`
- `v7-direct-add-domain`
- `v7-direct-remove-domain`
- `v7-direct-test-domain`
- `v7-direct-sync`
- `v7-direct-status`

Tests:

```bash
dig @10.0.0.1 gosuslugi.ru
v7-direct-test-domain gosuslugi.ru
ip route get <resolved_ip> from 10.0.0.3 iif wg0
```

Expected for direct domains:

```text
dev ens3
```

Expected for non-whitelisted domains:

```text
dev awg2 or tun0 according to user assignment
```

## Risks

- Client may use DoH/DoT and bypass V7 DNS classification.
- CDN IPs may be shared.
- `.ru` is broad and may include sites that should not go direct.
- Direct route exposes VPS IP, not external VPN IP.
- This must be visible in admin UI to avoid confusion.

## Roadmap Placement

This belongs after kill switch baseline and before large-scale admin rollout.

Reason:

- direct whitelist changes leak model
- kill switch must know direct exceptions
- user provisioning should set client DNS to V7 resolver
- admin must explain direct/VPN route decisions clearly

Next practical step:

1. Add or obtain one trusted RU egress.
2. Test sensitive services through it before adding to active pool:

```bash
curl --interface <trusted_ru_if> -4 -I -L --connect-timeout 8 --max-time 20 https://gosuslugi.ru
curl --interface <trusted_ru_if> -4 -I -L --connect-timeout 8 --max-time 20 https://esia.gosuslugi.ru
```

3. Only after success, map Gosuslugi/ESIA domains to `TRUSTED_RU`.
