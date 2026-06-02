# P2.8.2 Local Admin API Provenance

Project: V7 Vozduh
Block: P2.8.2

## Local File

| Field | Value |
| --- | --- |
| Path | `admin/v7-admin-api` |
| Hash | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` |
| Size | `2129821` bytes |
| mtime | `May 31 18:28:22 2026` |
| Mode | `755` |
| Owner | local user |

## Git State

| Field | Value |
| --- | --- |
| Branch | `Updatesystem` |
| HEAD | `b848fbf82f76f916b2fc6e5d04b24a1068e6048f` |
| Upstream | `origin/Updatesystem` |
| Status | dirty |
| File status | `M admin/v7-admin-api` |

## Uncommitted Modification Summary

`git diff --numstat -- admin/v7-admin-api`:

| Insertions | Deletions | File |
| ---: | ---: | --- |
| 3432 | 20 | `admin/v7-admin-api` |

## Recent File History

| Commit | Date | Subject |
| --- | --- | --- |
| `b848fbf` | 2026-05-31 | Document V7 governance and admin trust surfaces |
| `736f035` | 2026-05-28 | Update V7 governance and operator execution state |
| `5de3007` | 2026-05-25 | Update V7 system governance snapshot |
| `a0e689c` | 2026-05-21 | Clarify import service limits |
| `6941898` | 2026-05-21 | Complete channel import pipeline |
| `14217af` | 2026-05-21 | Fix admin add-channel JavaScript syntax |
| `fc8f3d1` | 2026-05-21 | Add managed OpenVPN egress pipeline |
| `ca1b96d` | 2026-05-21 | Implement egress import and Telegram-aware channel checks |

## Structural Summary

| Metric | Value |
| --- | ---: |
| Lines | 36469 |
| Python functions | 681 |
| Detected routes | 252 |
| GET role entries | 232 |
| JS functions | 799 |
| API fetch calls in UI | 30 |

## Local Interpretation

Local Admin API is the broadest implementation candidate and includes P2.1-P2.7 execution, validation, simulation, candidate, approval, governance, rehearsal, and dry-run preview read paths. It is not authoritative because it is uncommitted and not deployed.

local_admin_api_provenance_complete=true
