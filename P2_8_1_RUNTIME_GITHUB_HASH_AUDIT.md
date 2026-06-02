# P2.8.1 Runtime GitHub Hash Audit

Project: V7 Vozduh
Block: P2.8.1

## GitHub Branches Compared

Runtime hashes were compared against committed objects in `origin/Updatesystem` and `origin/main` where local remote-tracking refs match live `git ls-remote` heads.

## Runtime vs `origin/Updatesystem`

| Component | Runtime hash | `origin/Updatesystem` hash | Verdict |
| --- | --- | --- | --- |
| Admin API | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | DIFFERENT |
| Public gateway | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | MATCH |
| Client speed API | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | MATCH |
| Users autoswitch | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | MATCH |
| Service matrix refresh | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | MATCH |
| Egress quality compactor | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | MATCH |
| Telegram sentinel | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | MATCH |

## Runtime vs `origin/main`

`origin/main` lacks most audited `tools/v7-*` and `systemd/v7-*` artifacts. Its `admin/v7-admin-api` hash is `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977`, which does not match runtime.

## Interpretation

The runtime is closer to `origin/Updatesystem` than to `origin/main`, but Admin API is not equal to either audited GitHub branch. A runtime deploy manifest is absent.

runtime_github_hashes_verified=false
