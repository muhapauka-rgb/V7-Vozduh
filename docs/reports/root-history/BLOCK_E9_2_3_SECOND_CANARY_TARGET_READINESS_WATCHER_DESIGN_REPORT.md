# BLOCK E9.2.3 - Second Canary Target Readiness Watcher Design

Mode: read-only / watcher design only.

## Summary

E9.2.3 created a manual read-only target-readiness checker for the second one-user canary path.

```text
manual_checker_created=true
current_second_canary_readiness=NO-GO
selected_target=NONE
target_1_status=occupied_by_10.7.0.5
clean_zero_user_target_exists=false
candidate_10.7.0.14_valid=true
should_E9_3_execute_now=false
execution_allowed_now=false
```

No daemon, timer, systemd unit, deploy, route mutation, registry mutation, user movement, autoswitch apply, or canary execution was performed.

## Artifacts

| Artifact | Path |
|---|---|
| rules doc | `docs/track7/control-plane/SECOND_CANARY_TARGET_READINESS_RULES.md` |
| manual checker | `tools/v7-second-canary-target-readiness` |
| checker tests | `tests/unit/test_v7_second_canary_target_readiness.py` |
| current state snapshot fixture | `docs/track7/control-plane/e9_2_3-evidence/current-state/` |
| pretty evidence | `docs/track7/control-plane/e9_2_3-evidence/readiness-current.txt` |
| JSON evidence | `docs/track7/control-plane/e9_2_3-evidence/readiness-current.json` |

## Checker Contract

`tools/v7-second-canary-target-readiness` is read-only by construction:

- reads `users.registry`, `egress.registry`, `egress-load.state`, `egress-diagnose.state`, `egress-stability.state`, and `interface-state.state`;
- does not call `v7-user-switch`;
- does not call `v7-routing-sync`;
- does not call `v7-users-autoswitch`;
- does not call `ip`, `nft`, `systemctl`, SSH, or runtime mutation commands;
- emits JSON or pretty text only.

Default input resolution:

1. `--state-dir`, if supplied;
2. `V7_STATE_DIR`, if supplied;
3. `/opt/v7/egress/state`, if readable;
4. repo evidence snapshot `docs/track7/control-plane/e9_2_3-evidence/current-state`.

## Current Watcher Result

The current reproducible repo-side snapshot returns:

```text
candidate_user=10.7.0.14
candidate_still_valid=true
current_egress=vless
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
target_1_current_user=10.7.0.5
```

Zero-user targets exist, but none is safe:

| Target | Zero User | Status | Reason |
|---|---:|---|---|
| `awg0` | true | NO-GO | below avg/min/stability floor; missing Direct/RU and Trusted RU exclusions |
| `awg3` | true | NO-GO | below avg/min floor; missing Direct/RU and Trusted RU exclusions |
| `openvpn-1779388847-d2ad7c` | true | NO-GO | diagnose `SUSPECT` |
| `wireguard-1779454504-c43409` | true | NO-GO | diagnose `SUSPECT` |
| `1` | false | NO-GO | occupied by `10.7.0.5`; load-state users=1 |

## Rules Added

A target is `GO` only if it is enabled, empty by registry and load-state, interface `UP,LOWER_UP`, diagnose `OK`, not manual/reserve-only, excludes Direct/RU and Trusted RU route classes, meets the quality floor, and has a clean rollback path to `vless`.

A target is `NO-GO` if occupied, stale/unclean by load-state, diagnose `SUSPECT/FAIL`, below floor, manual/reserve-only, policy-sensitive, or interface state is unknown.

## Test Coverage

Added unit coverage for:

- occupied target rejected;
- low-quality target rejected;
- `SUSPECT` target rejected;
- clean zero-user OK target selected;
- no target -> `NO-GO`;
- invalid candidate -> `NO-GO`;
- CLI JSON output remains read-only.

## Governance Effect

E9.2.3 does not make E9.3 executable. It makes target readiness repeatable.

```text
current_canary_status=SECOND_CANARY_TARGET_WATCHER_NO_GO
second_canary_readiness=NO-GO
execution_allowed_now=false
```

## Next Recommended Step

Wait for a clean target state, then rerun:

```bash
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
```

If the checker returns `GO`, prepare a new E9.3 bounded live approval packet naming the selected target. Do not execute E9.3 from this report alone.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
