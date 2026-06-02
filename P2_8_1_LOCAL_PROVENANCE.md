# P2.8.1 Local Provenance

Project: V7 Vozduh
Block: P2.8.1

## Local Repository State

| Field | Value |
| --- | --- |
| Worktree | `/Users/ponch/Documents/New project` |
| Branch | `Updatesystem` |
| HEAD | `b848fbf82f76f916b2fc6e5d04b24a1068e6048f` |
| Upstream | `origin/Updatesystem` |
| Tracked file count | 4031 |
| Current repository files under audited roots | 3858 |
| Dirty state | dirty |
| Modified tracked file | `admin/v7-admin-api` |
| Untracked entries | 41 |

## Local Dirty Work

`git diff --stat` reports:

| File | Change |
| --- | --- |
| `admin/v7-admin-api` | 3432 insertions, 20 deletions |

Untracked local reports/evidence include P2.1-P2.8 reports, P2.7 docs/evidence, and `tests/unit/test_p2_7_candidate_workflow.py`.

## Local Key Hashes

| Local path | SHA256 |
| --- | --- |
| `admin/v7-admin-api` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` |
| `tools/v7-public-gateway` | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` |
| `tools/v7-client-speed-api` | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` |
| `tools/runtime-support/v7-direct-auto-sync` | `f58d3f845022ea6deadb999feddadc0ba55341198b7eb95f342639af363228c4` |
| `tools/v7-users-autoswitch` | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` |
| `tools/v7-service-matrix-refresh-all` | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` |
| `tools/v7-egress-quality-compact` | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` |
| `tools/v7-telegram-sentinel` | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` |
| `tools/v7-operator-execution-packet` | `9cf153a1869c4d3d72c418d74b49300995b3f5621c78cb523eef50ad39a301bf` |

## Local Gaps

| Runtime artifact | Local status |
| --- | --- |
| `/usr/local/bin/v7-api` | no local path found by exact basename search |
| `/usr/local/bin/v7-traffic-snapshot` | no local path found by exact basename search |
| Several runtime systemd units | no local systemd source found by exact path search |

local_provenance_complete=true
