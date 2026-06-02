# P2.8.2 GitHub Admin API Provenance

Project: V7 Vozduh
Block: P2.8.2

## Remote Heads

Read-only `git ls-remote --heads origin`:

| Branch | SHA |
| --- | --- |
| `main` | `593619d494e215d11fd826086593527a4a555690` |
| `Updatesystem` | `b848fbf82f76f916b2fc6e5d04b24a1068e6048f` |
| `codex/dynamic-load-autoswitch` | `0ea6d4ef82abaad26b0609d254bb6cf297db6432` |
| `codex/dynamic-load-autoswitch-pr` | `3b0fab9b639a10d55e232a8d6320a12d97f0c34e` |
| `codex/integratsiya-tunelya` | `a0e689c67ef7d47e7f04e5c30e5430acd05752cb` |

## Admin API Hashes By Branch

| Branch/ref | Admin API hash | Size | Lines | Routes | Status vs runtime |
| --- | --- | ---: | ---: | ---: | --- |
| `origin/main` | `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` | 1292765 | 21624 | 165 | far behind runtime |
| `origin/Updatesystem` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | 1942053 | 33057 | 213 | closest committed baseline; missing runtime execution read APIs |
| `origin/codex/dynamic-load-autoswitch` | `7a1d133a9a4be1a5b4863248ae809c91788333432e69d1770b9f772843da3e26` | 1408178 | 23753 | 170 | behind runtime |
| `origin/codex/integratsiya-tunelya` | `34b64c9bd67ac2919df405f49413894ad95b9c9fa6b76a6bb673106b58fdca09` | 1703012 | 29184 | 180 | behind runtime |
| `codex/dynamic-load-autoswitch-pr` raw GitHub | `61b32bc43940b5ca9fd1249f921adab7dfd1897ffcec8f9c1dcf117c40e63da6` | 1359148 | 22733 | 170 | behind runtime |

## Recent GitHub History

### `origin/main`

| Commit | Date | Subject |
| --- | --- | --- |
| `593619d` | 2026-05-14 | Make admin routine actions quiet |
| `012436d` | 2026-05-14 | Wire import links into issued profiles |
| `130ac7f` | 2026-05-14 | Fix profile import QR delivery |
| `134897c` | 2026-05-14 | Compact quick config issue panel |

### `origin/Updatesystem`

| Commit | Date | Subject |
| --- | --- | --- |
| `b848fbf` | 2026-05-31 | Document V7 governance and admin trust surfaces |
| `736f035` | 2026-05-28 | Update V7 governance and operator execution state |
| `5de3007` | 2026-05-25 | Update V7 system governance snapshot |
| `a0e689c` | 2026-05-21 | Clarify import service limits |

## GitHub Interpretation

No inspected GitHub branch equals the runtime Admin API hash. `origin/Updatesystem` is the nearest committed source branch, but the runtime file contains additional execution read-only APIs not present in that branch.

github_admin_api_provenance_complete=true
