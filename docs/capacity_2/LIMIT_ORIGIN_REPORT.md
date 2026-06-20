# LIMIT ORIGIN REPORT

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Origin Summary

| Limit | Origin evidence | Current purpose | Still valid? |
| --- | --- | --- | --- |
| `soft_limit` | Present since early admin/egress metadata; dynamic load policy added in `152c1ce5 Add guarded VPN autoswitch dynamic load policy`; semantics locked in `3f699567 Establish capacity semantics reference` | Warn before broad new assignment | Yes, as assignment safety. No, as real tunnel capacity. |
| `hard_limit` | Present since early admin/egress metadata; planner hard gate strengthened by dynamic load policy in `152c1ce5`; semantics locked in CAPACITY.1 / ADR-009 | Block planned new assignment when channel is full by policy | Yes, as assignment safety. No, as observed physical limit. |
| `capacity_users` | Added as explicit egress capacity metadata; visible in planner dynamic load cap logic and committed by `152c1ce5` / later capacity semantics work | Cap soft/hard/failover limits when a bounded production or manual limit is known | Conditional. Valid only when the metadata is intentionally certified and fresh. |
| `failover_hard_limit` | Dynamic/failover safety policy added with guarded autoswitch dynamic load policy | Block emergency failover beyond safe assignment pressure | Yes, as failover guard. |

## Git Evidence

Relevant history found by `git log -S`:

- `152c1ce5 Add guarded VPN autoswitch dynamic load policy`
- `3b894b86 Complete autoswitch quality safety UI`
- `9c36f0f6 Add POOL promotion equivalence rule`
- `bcca20e6 Audit channel decision pipeline alignment`
- `3f699567 Establish capacity semantics reference`

`152c1ce5` added the major dynamic-load implementation in `tools/v7-users-autoswitch` and admin support. `3f699567` created CAPACITY.1 and ADR-009, locking the current semantics.

## Why They Exist

The limits exist to prevent unsafe user movement:

- avoid dumping too many users into one egress;
- preserve failover headroom;
- keep reserve/canary/manual channels from being treated as ordinary capacity;
- block planned assignments when a target is already full;
- keep current users distinct from new movement.

## Historical vs Production Purpose

| Context | Purpose |
| --- | --- |
| Early channel onboarding | Provide simple visible per-channel limits and policy settings. |
| Guarded autoswitch | Protect planner decisions from over-concentrating users. |
| Canary / pool promotion | Keep unproven channels bounded until enough evidence exists. |
| Current production | Assignment safety and operator explanation. |

## Caveats

Some explicit `soft_limit: 1` / `hard_limit: 2` values are historical or bounded rollout metadata. CAPACITY.1 already established that they must not be read as measured tunnel throughput.

`capacity_users=0` means no explicit per-egress cap is known. It does not mean unlimited real capacity.

## Audit Verdict

Limits remain necessary as safety rails. They should not be removed or automatically replaced. However, V7 should not rely on static limits alone when it wants to understand practical third-party tunnel capacity.
