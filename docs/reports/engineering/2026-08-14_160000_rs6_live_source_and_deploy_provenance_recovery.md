# RS6 Live Source and Deploy Provenance Recovery

**Status:** `SOURCE_AND_DEPLOY_PROVENANCE_RECOVERED_PENDING_COMMIT_DEPLOY_RECONCILIATION`

**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`

## Result

Fresh read-only production observation at `2026-08-14T09:55:42+03:00`
proved that five live helpers and six unit definitions were absent from the
current source/deploy manifest. Exact production copies were recovered into
the existing `tools/runtime-support` and `systemd` owners and bound to the
existing `tools/v7_sync_lib.APPROVED_DEPLOY_FILES` manifest.

| Source owner | Production path | SHA-256 equality |
| --- | --- | --- |
| `tools/runtime-support/v7-state-merge` | `/usr/local/bin/v7-state-merge` | `216a8b9f46bd14c4c3168e14d4518def6a01e315b50857945400eb04a9a0bdfb` |
| `tools/runtime-support/v7-path-sanity-check` | `/usr/local/bin/v7-path-sanity-check` | `567adc602d769ea5e29a2ab4a339e2c6d6d81ead3176a59af45e92280ffbc890` |
| `tools/runtime-support/v7-egress-benchmark-all` | `/usr/local/bin/v7-egress-benchmark-all` | `f9d03e9edcc8d21e8cfb41c6c4bf4101a72d1b1edf196c711d9aa82f09746471` |
| `tools/runtime-support/v7-mss-clamp-enable` | `/usr/local/bin/v7-mss-clamp-enable` | `9c9031177de02f5838a3e5869bd30c1451d7e99be99bcf50a47f638ca9ea0bd6` |
| `tools/runtime-support/v7-api` | `/usr/local/bin/v7-api` | `6b87927925b97125046a4e363f0d690d8997e3f13cd35701afeef4e9a27908fd` |
| `systemd/v7-health.service` | `/etc/systemd/system/v7-health.service` | `5cdb974b88a40c8362d4944ab70a7b46a9eb41eb92f7daf702c42d1e26df00d3` |
| `systemd/v7-benchmark.service` | `/etc/systemd/system/v7-benchmark.service` | `176b08155843218d4cfcb760ec06006d43a9baba9b563b3530893143577e52a9` |
| `systemd/v7-mss-clamp.service` | `/etc/systemd/system/v7-mss-clamp.service` | `206cc6278f4cab98ebb810b4d0b9ec0363973c9eb06e2f753e1387e4fa134daa` |
| `systemd/v7-api.service` | `/etc/systemd/system/v7-api.service` | `f99668a38eb3db3a0883c8f1e14db413b6989e58ce3d7838391c240b7977fdd0` |
| `systemd/v7-killswitch.service` | `/etc/systemd/system/v7-killswitch.service` | `db1a1a4fabe48b160d17fee6337d7a841594f997584b75261378bb1717cb4d0c` |
| `systemd/v7-public-gateway.service` | `/etc/systemd/system/v7-public-gateway.service` | `a30cea34f33681c17d09d763c19ae0f356d960024b27b9f496e82ad49e79dce7` |

No production file was written. The source additions reproduce already-live
content; they introduce no new behavior. Manifest validation passed, shell
syntax passed, Python compile passed with an isolated cache, and existing sync
and RS7 lifecycle focused tests passed.

## Remaining RS6 condition

Fresh `v7-path-sanity-check` still reports
`user_policy_routes=FAIL reason=desired_state_unknown` and
`egress_service_matrix=FAIL`. Source/deploy provenance is closed for this
bounded set, but the desired-state/Matrix owner condition remains independent.

## Effects and successor

- Runtime/Production/Authority effects before deploy: `NONE`;
- recovered owner files: `11`;
- new owner/Program/registry: `NONE`;
- exact successor: commit/push, safe-deploy manifest reconciliation, then
  return to the existing RS6 desired-state/Matrix consumer.
