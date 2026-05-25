# Canary Candidate Selection

This document selects a conditional future candidate only. It does not approve or execute a live switch.

## Candidate

| Field | Value |
|---|---|
| User | `10.7.0.13` |
| Current egress | `awg0` |
| Route table | `1011` |
| Candidate target | `awg3` |
| Target interface | `awg3` |
| Rollback target | `awg0` |
| Expected blast radius | one user |

## Why This Candidate

- The user is enabled in `users.registry`.
- `v7-user-route-check` reported this user route as OK.
- `v7-reconcile-check` did not list table `1011` among missing rule errors.
- The current assignment is simple: `current=awg0 table=1011`.
- Target `awg3` exists, is enabled, has interface `awg3`, and has 0 assigned users in the sampled state.
- Rollback is clear in shape: `v7-user-switch 10.7.0.13 awg0`.

## Why This Is Still Not GO

- `10.7.0.13` is in autoswitch penalty state: `switches_1h=2`, `switches_24h=10`, `penalty_until=2026-05-25T02:05:31.440261+00:00`.
- `v7-users-autoswitch.timer` can run `v7-users-autoswitch --apply` every 20 seconds.
- Target `awg3` has 0 users and load capacity, but quality is below policy floor in the sampled quality summary.
- `v7-reconcile-check` has 11 errors for other users; broad route consistency is not clean.
- Trusted RU decision state is stale and Gosuslugi-sensitive.

## Skipped Candidate Patterns

- Disabled user `10.7.0.7`: skipped because disabled users are not suitable for a live canary.
- User `10.7.0.5`: skipped because it is already on high-quality egress `1`, and moving it would test a different risk class.
- Target `vless`: skipped because stability is below threshold and runtime state reports soft-full.
- Target `1`: skipped because it is already occupied, has tight per-egress limits in registry metadata, and excludes Trusted RU/Direct route classes.

## Selection Verdict

`10.7.0.13 -> awg3` is the best conditional planner candidate, but the live canary is **NO-GO** until the blockers are cleared.
