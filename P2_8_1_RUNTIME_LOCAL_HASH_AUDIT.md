# P2.8.1 Runtime Local Hash Audit

Project: V7 Vozduh
Block: P2.8.1

## Result

Runtime and local are partially aligned. They are not fully verified.

| Component | Runtime hash | Local hash | Verdict |
| --- | --- | --- | --- |
| Admin API | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | DIFFERENT |
| Public gateway | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | MATCH |
| Client speed API | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | MATCH |
| Direct auto sync | `f58d3f845022ea6deadb999feddadc0ba55341198b7eb95f342639af363228c4` | `f58d3f845022ea6deadb999feddadc0ba55341198b7eb95f342639af363228c4` | MATCH |
| Users autoswitch | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | MATCH |
| Service matrix refresh | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | MATCH |
| Egress quality compactor | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | MATCH |
| Telegram sentinel | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | MATCH |
| Local operator execution packet | runtime missing | `9cf153a1869c4d3d72c418d74b49300995b3f5621c78cb523eef50ad39a301bf` | LOCAL_ONLY |
| Runtime API | `6b87927925b97125046a4e363f0d690d8997e3f13cd35701afeef4e9a27908fd` | local exact basename missing | RUNTIME_ONLY |

## Interpretation

Most audited operational tools match local source. The admin API does not. Because Admin API is the active admin surface and the local file is dirty, runtime/local hashes are not verified as a complete set.

runtime_local_hashes_verified=false
