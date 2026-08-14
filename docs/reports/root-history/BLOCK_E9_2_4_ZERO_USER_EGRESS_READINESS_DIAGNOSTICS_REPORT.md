# BLOCK E9.2.4 - Zero-User Egress Readiness Diagnostics

Mode: read-only / egress diagnostics only.

## Summary

E9.2.4 did not find a clean second-canary target. It did refine the reason:

```text
truly_no_clean_target=true
best_current_target=1
best_zero_user_waiver_candidate=openvpn-1779388847-d2ad7c
occupied_target_acceptable_with_waiver=true
openvpn_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
wireguard_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
awg0_real_status=QUALITY_TOO_LOW
awg3_real_status=QUALITY_TOO_LOW
watcher_too_conservative=false
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

No runtime mutation, canary, user movement, routing mutation, autoswitch apply, policy apply, Direct/RU mutation, Trusted RU refresh, proxy apply, kill-switch mutation, deploy, restart, chmod/chown, or registry edit was performed.

## Evidence

| Artifact | Path |
|---|---|
| current snapshot | `docs/track7/control-plane/e9_2_4-evidence/current-egress-snapshot.txt` |
| SUSPECT analysis | `docs/track7/control-plane/e9_2_4-evidence/suspect-analysis.md` |
| quality floor analysis | `docs/track7/control-plane/e9_2_4-evidence/quality-floor-analysis.md` |

This block used repo-side E9.2.2/E9.2.3 evidence. It did not run live VPS read-only commands.

## Target Truth

| Target | Zero User | Diagnose | Quality | Classification | Readiness |
|---|---:|---|---|---|---|
| `1` | no | OK | strong | occupied production target | conditional with explicit mechanics waiver only |
| `awg0` | yes | OK | weak | `QUALITY_TOO_LOW` | NO-GO |
| `awg3` | yes | OK | weak | `QUALITY_TOO_LOW` | NO-GO |
| `openvpn-1779388847-d2ad7c` | yes | SUSPECT | strong | `IDLE_BUT_HEALTHY` / `DIAGNOSE_TOO_STRICT` | conditional waiver candidate |
| `wireguard-1779454504-c43409` | yes | SUSPECT | strong | `IDLE_BUT_HEALTHY` / `DIAGNOSE_TOO_STRICT` | conditional waiver candidate |

## OpenVPN / WireGuard SUSPECT Finding

Both targets are zero-user, interface-up, have strong avg/min/stability, and exclude `TRUSTED_RU_SENSITIVE,DIRECT_RU`.

Observed blocker:

```text
diagnose=SUSPECT
detail=handshake_age_seconds=999999
```

This looks like idle/stale handshake semantics, not proven datapath failure. However, current clean-target rules correctly reject them because `SUSPECT` means the target is not cleanly attributable without a waiver or fresh OK diagnose.

## AWG0 / AWG3 Finding

`awg0` and `awg3` are zero-user and diagnose OK, but below canary quality floor:

```text
awg0 avg=11.909 min=4.17 stability=0.350155
awg3 avg=5.62633 min=4.39 stability=0.78026
floor avg>=15 min>=10 stability>=0.45
```

They are real quality-floor failures for a mechanics reproducibility canary.

## Is There Truly No Clean Target?

Yes.

`truly_no_clean_target=true` because no enabled non-vless target is simultaneously:

- zero-user by registry and load-state;
- interface `UP,LOWER_UP`;
- diagnose OK;
- quality-floor acceptable;
- non-sensitive by route-class exclusions.

## Target 1 Waiver Question

`target 1` is still the best operational target by quality and diagnose, but it is occupied by `10.7.0.5`.

A second canary to target `1` would still mutate only one candidate user if executed through the bounded `v7-user-switch 10.7.0.14 1` path, but attribution would no longer be clean isolation because the target already carries a real user. It is acceptable only as a separate **mechanics-with-production-load waiver**, not as the clean zero-user E9.3 target.

## Watcher Review

`tools/v7-second-canary-target-readiness` is not too conservative for clean-target mode. It correctly blocks:

- occupied target `1`;
- low-quality AWG targets;
- `SUSPECT` OpenVPN/WireGuard targets.

Proposed future enhancement, not implemented in this block:

- add a separate `--allow-idle-suspect-waiver` or `CONDITIONAL` mode that distinguishes stale idle handshake from real target failure;
- keep default mode strict and `NO-GO`.

## Second Canary Strategy

Future second canary strategy should be explicit about objective:

| Objective | Preferred Target Strategy |
|---|---|
| clean isolation | wait for a true clean zero-user target |
| target diversity | consider OpenVPN first, but only with stale-handshake waiver and fresh read-only evidence |
| production-load realism | consider target `1`, but only with occupied-target waiver and hard-limit/load acceptance |

Safest next step:

```text
Prepare a waiver-aware E9.3 approval packet only if the operator accepts either:
1. openvpn idle-SUSPECT waiver, or
2. occupied target-1 mechanics-with-production-load waiver.

Otherwise wait and rerun tools/v7-second-canary-target-readiness until selected_target != NONE.
```

## Final Answers

```text
truly_no_clean_target=true
best_current_target=1
occupied_target_acceptable_with_waiver=true
openvpn_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
wireguard_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
awg0_real_status=QUALITY_TOO_LOW
awg3_real_status=QUALITY_TOO_LOW
watcher_too_conservative=false
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
exact_safest_next_step=choose waiver path explicitly or wait for clean target and rerun watcher
```

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
