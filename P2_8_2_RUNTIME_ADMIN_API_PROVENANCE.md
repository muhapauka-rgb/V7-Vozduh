# P2.8.2 Runtime Admin API Provenance

Project: V7 Vozduh
Block: P2.8.2
Mode: Audit / Discovery / Lineage Verification
Date: 2026-05-31

## Collection Mode

Runtime was inspected through read-only SSH and a read-only copy of `/usr/local/bin/v7-admin-api` was copied to `/private/tmp/p2_8_2-runtime-v7-admin-api` for diffing.

No runtime mutation, systemd change, deploy, routing change, user movement, autoswitch apply, policy apply, killswitch mutation, trusted/direct RU mutation, execution engine, or runtime hook was performed.

## File Provenance

| Field | Value |
| --- | --- |
| Runtime path | `/usr/local/bin/v7-admin-api` |
| Runtime hash | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` |
| Size | `1983830` bytes |
| mtime | `2026-05-31 16:50:08.428754394 +0300` |
| Mode | `755` |
| Owner | `root:root` |
| Shebang | `#!/usr/bin/env python3` |
| Local audit copy hash | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` |

## Runtime Location

| Field | Value |
| --- | --- |
| Host | `v3119922.hosted-by-vdsina.ru` |
| Kernel | `Linux v3119922.hosted-by-vdsina.ru 7.0.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC Mon Apr 13 11:09:53 UTC 2026 x86_64 GNU/Linux` |
| Listener | `127.0.0.1:7080` |
| Public admin surface | proxied through public TLS host from prior P2.8 evidence |

## Interpreter

| Field | Value |
| --- | --- |
| Interpreter path | `/usr/bin/python3` through env shebang |
| Python version | `Python 3.14.4` |

## Systemd Linkage

| Field | Value |
| --- | --- |
| Unit | `v7-admin-api.service` |
| State | `active/running` |
| Fragment | `/etc/systemd/system/v7-admin-api.service` |
| Drop-in | `/etc/systemd/system/v7-admin-api.service.d/profile-public-base.conf` |
| ExecStart | `/usr/local/bin/v7-admin-api` |
| User | `root` |
| Group | `root` |
| Environment | `V7_ADMIN_HOST=127.0.0.1`, `V7_ADMIN_PORT=7080`, profile public base URL |

## Runtime Command Line

`python3 /usr/local/bin/v7-admin-api`

## Runtime Dependencies

Top-level imports:

`admin_core.events`, `admin_core.operator_observability`, `admin_core.registry_readers`, `admin_core.sanitize`, `admin_core.time`, `base64`, `csv`, `datetime`, `hashlib`, `hmac`, `html`, `http`, `http.server`, `io`, `ipaddress`, `json`, `os`, `pathlib`, `queue`, `re`, `secrets`, `shutil`, `socket`, `sqlite3`, `subprocess`, `tempfile`, `threading`, `time`, `urllib.parse`, `urllib.request`, `uuid`.

## Structural Summary

| Metric | Value |
| --- | ---: |
| Lines | 33800 |
| Python functions | 585 |
| Classes | `ConnectRequestSnapshot`, `Handler` |
| Detected routes | 221 |
| GET role entries | 204 |
| JS functions | 776 |
| API fetch calls in UI | 16 |

## Lineage Result

Runtime hash was searched against local Git history for `admin/v7-admin-api`. No matching commit was found.

runtime_admin_api_provenance_complete=true
