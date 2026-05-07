# V7 Phase 39: Direct-exclude routing for banking

Date: 2026-05-07

## Problem

After broad `.ru` direct routing was enabled, Alfa-Bank mobile traffic was sent
directly through the VPS public IP `195.2.79.116`.

Server-side test showed:

```text
curl direct to alfa-mobile.alfabank.ru: timeout
curl through vless: connection succeeds, HTTP 403 on root path
```

This indicates that direct via the datacenter VPS public IP is not a viable path
for this banking app, while the normal V7 egress path can reach the endpoint.

## Design Decision

V7 needs two domain groups, not one:

- `direct`: domains that should bypass external VPN and leave via VPS public IP.
- `direct_exclude` / `vpn_prefer`: domains that match broad direct rules such as
  `.ru`, but must stay on the user's assigned egress.

This preserves `.ru` direct routing for ordinary sites while allowing sensitive
apps such as banking to avoid a datacenter direct path.

## Added / Changed

### `/usr/local/bin/v7-killswitch-enable`

Added nft set:

```text
v7_direct_exclude_dst
```

Direct mark and direct public allow now apply only when destination is in
`v7_direct_dst` and not in `v7_direct_exclude_dst`.

### `/usr/local/bin/v7-direct-render-dnsmasq`

Now reads:

- `/etc/v7/direct/domains.conf`
- `/etc/v7/direct/exclude.conf`

and renders nftset rules for both direct and exclude sets.

### `/usr/local/bin/v7-direct-exclude-add-domain`

Adds a domain to `/etc/v7/direct/exclude.conf`, regenerates dnsmasq config, and
restarts dnsmasq.

### `/usr/local/bin/v7-direct-exclude-refresh`

Explicitly resolves exclude domains and writes their current IPs into
`v7_direct_exclude_dst`.

This is needed because overlapping dnsmasq `nftset` rules can populate the
direct set but not reliably populate a second exclude set for the same matched
domain.

### `/usr/local/bin/v7-direct-test-domain`

Now reports:

```text
direct_set=yes/no
direct_exclude=yes/no
decision=VPN_PREFERRED_DIRECT_EXCLUDED
```

### `/usr/local/bin/v7-direct-list`

Now shows both direct domains/IPs and direct-excluded domains/IPs.

## Banking Excludes Added

```text
alfabank.ru
edna.id
alfa-mobile.alfabank.ru
metrics.alfabank.ru
pushserver.edna.id
groupib-am.alfabank.ru
```

Observed app DNS domains included:

```text
alfa-mobile.alfabank.ru
metrics.alfabank.ru
pushserver.edna.id
groupib-am.alfabank.ru
```

`groupib-am.alfabank.ru` appears to be part of the bank anti-fraud/security
path and was added after a second trace.

## Validation

Commands run:

```bash
v7-direct-exclude-refresh
v7-direct-test-domain groupib-am.alfabank.ru 10.0.0.3
v7-direct-test-domain alfa-mobile.alfabank.ru 10.0.0.3
v7-direct-test-domain pushserver.edna.id 10.0.0.3
v7-killswitch-check
v7-system-check
```

Result:

- `groupib-am.alfabank.ru`: `VPN_PREFERRED_DIRECT_EXCLUDED`
- `alfa-mobile.alfabank.ru`: `VPN_PREFERRED_DIRECT_EXCLUDED`
- `pushserver.edna.id`: `VPN_PREFERRED_DIRECT_EXCLUDED`
- `v7-killswitch-check`: `OK`
- `v7-system-check`: `OK`

## Next If Still Failing

If the app still fails after full app restart, run another short trace:

```bash
v7-app-domain-trace 10.0.0.3 60 bank-after-exclude
```

Possible outcomes:

- Another bank/anti-fraud domain appears and should be added to
  `direct_exclude`.
- The assigned egress IP itself is blocked, in which case V7 needs a dedicated
  trusted RU/residential egress for banking and government services.
