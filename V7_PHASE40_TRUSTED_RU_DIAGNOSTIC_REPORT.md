# V7 Phase 40: Trusted RU direct-path diagnostic

Date: 2026-05-07

## Constraint

The project must stay within the current single Russian V7 VPS:

```text
195.2.79.116
```

No second VPS, no mobile/residential/home egress, no additional external
trusted server.

## Goal

Check whether sensitive RU services can be made to work directly from the
existing VPS by local behavior changes, or whether the failure happens before
TLS/HTTP.

This evaluates the proposed `TRUSTED_RU_TLS` idea as an isolated diagnostic
experiment.

## Added

### `/usr/local/bin/v7-trusted-ru-diagnostic`

Read-only diagnostic command.

It checks each domain through:

- direct VPS public interface `ens3`;
- VLESS SOCKS `127.0.0.1:1080`;
- AWG interface `awg2`;
- direct OpenSSL TLS handshake;
- current V7 policy decision via `v7-direct-test-domain`;
- DNS resolution through V7 DNS.

It writes:

```text
/opt/v7/egress/state/trusted-ru-diagnostic.state
```

## Domains Tested

```text
www.gosuslugi.ru
gosuslugi.ru
esia.gosuslugi.ru
alfa-mobile.alfabank.ru
groupib-am.alfabank.ru
```

## Key Results

### Gosuslugi

`www.gosuslugi.ru`, `gosuslugi.ru`, `esia.gosuslugi.ru`:

```text
direct_http=000
direct_tls=0
direct_err=Connection timed out
direct_openssl=FAIL timeout_or_connect_failed
vless_http=000 timeout
awg_http=000 timeout
```

Pinned-IP tcpdump for `www.gosuslugi.ru`:

```text
195.2.79.116 > 109.207.1.118.443: Flags [S]
195.2.79.116 > 109.207.1.118.443: Flags [S]
195.2.79.116 > 109.207.1.118.443: Flags [S]
195.2.79.116 > 109.207.1.118.443: Flags [S]
```

No SYN-ACK was observed.

### Alfa-Bank

`alfa-mobile.alfabank.ru`:

```text
direct_http=000 timeout
direct_openssl=FAIL timeout_or_connect_failed
vless_http=404
awg_http=404
```

tcpdump for direct Alfa:

```text
195.2.79.116 > 217.12.98.151.443: Flags [S]
195.2.79.116 > 217.12.98.151.443: Flags [S]
195.2.79.116 > 217.12.98.151.443: Flags [S]
195.2.79.116 > 217.12.98.151.443: Flags [S]
```

No SYN-ACK was observed on direct path.

`groupib-am.alfabank.ru`:

```text
direct_http=000 timeout
vless_tls=0.392278 then unexpected EOF
awg_tls=0.088444 then reset by peer
```

This means the direct path fails before TLS, while egress paths at least reach
the remote TLS stage.

## Conclusion

For the tested sensitive RU targets, direct traffic from `195.2.79.116` fails
before TLS.

Therefore, browser-like TLS/uTLS/local gateway behavior on the same public IP
cannot fix these direct paths, because the connection does not reach TLS
handshake.

The failure class is:

```text
DIRECT_PATH_TCP_TIMEOUT_BEFORE_TLS
```

This does not prove the exact remote reason, but it proves that local TLS
fingerprint changes are not the first viable fix for these targets.

## Architectural Impact

V7 still needs service-aware policy:

```text
ordinary_ru -> DIRECT_RU
bank/government sensitive -> TRUSTED_RU_SENSITIVE
video/global -> appropriate global egress
default -> user sticky egress
```

Within the user's stated constraint of a single VPS, `TRUSTED_RU_SENSITIVE`
cannot be guaranteed if the remote service refuses the VPS public IP before TLS.

The system must represent this honestly in state/admin:

```text
route_class=TRUSTED_RU_SENSITIVE
local_direct_status=TCP_TIMEOUT_BEFORE_TLS
local_tls_gateway_viable=false
```

## Validation

After diagnostics:

```text
v7-killswitch-check = OK
v7-system-check = OK
```

No user route mutation was performed.
