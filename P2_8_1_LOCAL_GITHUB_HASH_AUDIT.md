# P2.8.1 Local GitHub Hash Audit

Project: V7 Vozduh
Block: P2.8.1

## Result

The local branch tip equals `origin/Updatesystem`, but the working tree is dirty. Therefore the local worktree is not fully verified against GitHub.

## Local Working Tree vs `origin/Updatesystem`

| Component | Local worktree hash | `origin/Updatesystem` hash | Verdict |
| --- | --- | --- | --- |
| Admin API | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | DIFFERENT |
| Public gateway | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | MATCH |
| Client speed API | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | MATCH |
| Users autoswitch | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | MATCH |
| Service matrix refresh | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | MATCH |
| Egress quality compactor | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | MATCH |
| Telegram sentinel | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | MATCH |
| Operator execution packet | `9cf153a1869c4d3d72c418d74b49300995b3f5621c78cb523eef50ad39a301bf` | `9cf153a1869c4d3d72c418d74b49300995b3f5621c78cb523eef50ad39a301bf` | MATCH |

## Local vs `origin/main`

`origin/main` is not an implementation peer for the current audited work. It lacks most audited `tools/v7-*` files and has a different Admin API hash.

local_github_hashes_verified=false
