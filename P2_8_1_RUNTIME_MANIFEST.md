# P2.8.1 Runtime Manifest

Project: V7 Vozduh
Block: P2.8.1
Generated from read-only runtime inspection on 2026-05-31.

## Directory Counts

| Runtime directory | File count, maxdepth 3 |
| --- | ---: |
| `/usr/local/bin` | 181 |
| `/etc/systemd/system` | 45 |
| `/etc/v7` | 90 |
| `/opt/v7` | 512 |

## Key Runtime Binary Hashes

| Runtime path | Size | SHA256 | Local analogue |
| --- | ---: | --- | --- |
| `/usr/local/bin/v7-admin-api` | 1983830 | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | `admin/v7-admin-api` |
| `/usr/local/bin/v7-public-gateway` | 6559 | `0ea593ad7bb8c79abe2fe3f1b3d518684b7211d571c994efbc481df9488bd123` | `tools/v7-public-gateway` |
| `/usr/local/bin/v7-api` | 1279 | `6b87927925b97125046a4e363f0d690d8997e3f13cd35701afeef4e9a27908fd` | UNKNOWN |
| `/usr/local/bin/v7-client-speed-api` | 20387 | `2d12e7f45f7e905a9b1d27abc1b3760b9edf347d5cbef007d87e58952c6531f0` | `tools/v7-client-speed-api` |
| `/usr/local/bin/v7-direct-auto-sync` | 4137 | `f58d3f845022ea6deadb999feddadc0ba55341198b7eb95f342639af363228c4` | `tools/runtime-support/v7-direct-auto-sync` |
| `/usr/local/bin/v7-users-autoswitch` | 95973 | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | `tools/v7-users-autoswitch` |
| `/usr/local/bin/v7-service-matrix-refresh-all` | 5524 | `1469f761e4c0da80a7823c04b9e993fb6771f3f9d7017f237d321ef86c4926ed` | `tools/v7-service-matrix-refresh-all` |
| `/usr/local/bin/v7-egress-quality-compact` | 8924 | `4c7c03aca4a597faf7943b1f86ea7e8f54b4b66616a8ef1ccb43a042f69c2375` | `tools/v7-egress-quality-compact` |
| `/usr/local/bin/v7-telegram-sentinel` | 18876 | `046d89f12e576edb1aeb38d4ed8ac32395098c97c83f01932aa87aa93e639127` | `tools/v7-telegram-sentinel` |
| `/usr/local/bin/v7-autoswitch-planner` | missing | UNKNOWN | no runtime binary; unit calls `v7-users-autoswitch` |
| `/usr/local/bin/v7-traffic-collector` | missing | UNKNOWN | unit calls `v7-traffic-snapshot` |
| `/usr/local/bin/v7-operator-execution-packet` | missing | UNKNOWN | `tools/v7-operator-execution-packet` |

## Key Systemd Unit Hashes

| Runtime path | SHA256 |
| --- | --- |
| `/etc/systemd/system/v7-admin-api.service` | `10708014b79bb2cd575802a3fd9345d2928e0a68c041764e5825330b96c410b9` |
| `/etc/systemd/system/v7-public-gateway.service` | `a30cea34f33681c17d09d763c19ae0f356d960024b27b9f496e82ad49e79dce7` |
| `/etc/systemd/system/v7-api.service` | `f99668a38eb3db3a0883c8f1e14db413b6989e58ce3d7838391c240b7977fdd0` |
| `/etc/systemd/system/v7-client-speed-api.service` | `4cbb19de11ead3b9ed72253b7afc35e39625b7c137f973b9d11d99d5d2134219` |
| `/etc/systemd/system/v7-users-autoswitch.service` | `7823869c890b24051b66ef990912ecbacd58a14882d35def317174e0d9d0f807` |
| `/etc/systemd/system/v7-service-matrix-refresh.service` | `a080187fe376c780596c968467bfaef8beaad9f120096a14a0827da081b0979c` |
| `/etc/systemd/system/v7-egress-quality-compact.service` | `cb2d1f5110475e99d57fc79a49a944d4c554b5c1157267a2bf0e799f11882313` |
| `/etc/systemd/system/v7-telegram-sentinel.service` | `e176f9791d5803faf4339d121507e011b38ea6a9b42ea29030b07068a6ed8027` |

runtime_manifest_complete=true
