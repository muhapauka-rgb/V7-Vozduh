# E11.6 Diagnose Regression Matrix

Runtime mutation scope: `/usr/local/bin/v7-egress-diagnose` only.

| Egress | Diagnose Before | Diagnose After | Route/Interface State | Quality | Blocker Before | Blocker After | Regression |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `wireguard-1779454504-c43409` | `SUSPECT`, `curl_ok_but_handshake_stale`, `handshake_age_seconds=999999` | `OK`, `handshake_age_seconds=60` in focused check; `handshake_age_seconds=101` in readiness fixture | `v7e06a394c478` `UP,LOWER_UP`; `wg show` fresh handshake; `route_get` OK | avg `59.1643`, min `58.43`, stability `0.987589` | false stale handshake from AWG command path | none | no |
| `awg0` | `OK` | `OK`, `handshake_age_seconds=104` in focused check | `awg show awg0` readable; interface up | avg `26.8043`, min `18.71`, stability `0.698022` | occupied and missing Direct/RU + Trusted RU exclusions for canary readiness | unchanged non-diagnose blockers | no |
| `awg3` | `OK` | `OK`, `handshake_age_seconds=80` in focused check | `awg show awg3` readable; interface up | avg `23.693`, min `16.53`, stability `0.697674` | occupied and missing Direct/RU + Trusted RU exclusions for canary readiness | unchanged non-diagnose blockers | no |
| `1` | `OK` before deploy; one immediate post-refresh sample showed stale `SUSPECT` | `OK`, `handshake_age_seconds=8` in focused follow-up | registry says `protocol=amneziawg`; `wg show` unsupported as expected; `awg show v7e356a192b79` fresh handshake; interface `UP,LOWER_UP` | avg `50.3747`, min `45.8`, stability `0.909187` | occupied by production users | occupied by production users | no sustained regression |
| `openvpn-1779388847-d2ad7c` | `SUSPECT`, `protocol=openvpn` | `SUSPECT`, `protocol=openvpn` | interface present/up in readiness fixture | avg `65.6883`, min `62.98`, stability `0.95877` | unsupported/non-WireGuard diagnose semantics | unchanged | no |

Conclusion:

```text
wireguard_false_stale_handshake_cleared=true
awg_regression_observed=false
target_1_sustained_regression_observed=false
openvpn_unchanged=true
```
