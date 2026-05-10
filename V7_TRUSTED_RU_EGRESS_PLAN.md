# V7 Trusted RU Egress Plan

Date: 2026-05-06
Status: required after Gosuslugi testing

## Problem

`gosuslugi.ru` and related domains timed out from all currently available paths:

- direct VPS public interface `ens3`
- `awg2`
- `vless`

Meanwhile other RU services worked:

- ozon.ru
- lamoda.ru
- yandex.ru
- mos.ru
- nalog.gov.ru

This indicates that sensitive RU services may reject the current source IP classes.

## Required Route Class

Add a route class:

```text
TRUSTED_RU
```

This is separate from:

- `DIRECT_RU`: direct via VPS `ens3`
- `VPN_DEFAULT`: user's assigned external VPN egress

## Candidate Requirements

A trusted RU egress candidate must:

- be physically/geographically suitable for Russian services
- have an IP accepted by Gosuslugi/ESIA
- be stable enough for auth flows
- support routing integration with V7
- pass direct service tests before being added to active routing

Possible sources:

- residential RU ISP connection
- mobile RU connection
- trusted RU VPS/provider if accepted by target services
- WireGuard/AmneziaWG/OpenVPN tunnel from a known-good RU endpoint

## Validation Before Pool Admission

A candidate must pass:

```bash
curl --interface <ifname> -4 -I -L --connect-timeout 8 --max-time 20 https://gosuslugi.ru
curl --interface <ifname> -4 -I -L --connect-timeout 8 --max-time 20 https://www.gosuslugi.ru
curl --interface <ifname> -4 -I -L --connect-timeout 8 --max-time 20 https://esia.gosuslugi.ru
curl --interface <ifname> -4 -I -L --connect-timeout 8 --max-time 20 https://lk.gosuslugi.ru
```

Expected:

- TCP connect succeeds
- TLS handshake succeeds
- HTTP response is received

The response can be redirect or login page. It does not have to be `200`, but it must not timeout.

## Integration Model

Once a trusted RU egress exists:

1. Add it to `egress.registry` with a route class:

```text
id=trusted_ru protocol=<protocol> type=interface interface=<ifname> test=interface class=trusted_ru enabled=1
```

2. Add sensitive domains to a separate list:

```text
/etc/v7/direct/trusted-ru-domains.conf
```

3. DNS resolver fills a separate nft set:

```text
v7_trusted_ru_dst
```

4. nft marks those destinations:

```text
mark 0x78
```

5. policy routing sends mark `0x78` to trusted RU table:

```text
fwmark 0x78 lookup 71
table 71 default dev <trusted_ru_if>
```

6. kill switch allows:

```text
10.0.0.0/24 -> <trusted_ru_if>
```

7. kill switch continues blocking:

```text
10.0.0.0/24 -> ens3 generic leak
```

## Admin Behavior

For `gosuslugi.ru`, admin should show:

```text
Route class: TRUSTED_RU
Status: Requires trusted RU egress
Current result: unavailable, no working trusted RU route
```

After candidate passes:

```text
Route class: TRUSTED_RU
Egress: trusted_ru
Status: Working
```

## Do Not Do

- Do not force Gosuslugi through generic `DIRECT_RU` if direct tests fail.
- Do not silently fall back to foreign VPN for sensitive RU services.
- Do not mark all `.ru` as `TRUSTED_RU`; this class is for sensitive services.
- Do not add a trusted RU egress to active pool without real service test.

