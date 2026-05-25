# Canary GO / NO-GO Criteria

## Current Verdict

```text
NO-GO
```

## Block E8 Rehearsal Result

```text
quiet_window_rehearsal=aborted_restored
quiet_window_verified=false
reconcile_under_quiet=NOT_SAMPLED_ABORTED
canary_status=NO-GO
```

## GO Criteria

All must be true before any future one-user canary:

- `tools/v7-route-movement-preview` forward preview exists with `mutation=false`, `runtime_commands_executed=false`, and `errors=[]`.
- Rollback preview exists and exact rollback command is known.
- Candidate user is explicitly named.
- Target egress is healthy, enabled, not overloaded, and acceptable under policy thresholds.
- `v7-killswitch-check` is OK immediately before canary.
- `v7-user-route-check` is OK immediately before canary.
- Provisioning reconcile is OK immediately before canary.
- `v7-reconcile-check` failure is either resolved or explicitly explained as non-blocking.
- Quiet-window rehearsal succeeded.
- Reconcile is clean under quiet-window, or an approved false-positive waiver exists.
- Autoswitch apply authority is held or otherwise proven unable to interfere.
- No anti-flap penalty/freeze applies to the candidate user.
- Trusted RU stale state is confirmed irrelevant to the candidate route class, or refreshed in a separately approved governance flow.
- Operator approval is explicit and bounded to one user.

## HARD BLOCKERS

Hard blockers cannot be ignored by the planner. They require resolution or a separately documented operator waiver where noted.

- autoswitch active authority can still run `v7-users-autoswitch --apply`;
- non-systemd autoswitch loop authority can still invoke `v7-users-autoswitch`;
- quiet-window rehearsal has not succeeded;
- `v7-reconcile-check=FAIL` is unresolved;
- target egress is below quality floor and no explicit one-user waiver exists;
- rollback command or rollback verification is unclear;
- kill switch is not OK;
- user route check is not OK;
- provisioning reconcile is not OK;
- Trusted RU/Gosuslugi-sensitive state is stale and relevant to the canary path;
- candidate user is in anti-flap/penalty state;
- any plan requires `v7-routing-sync` as the first live action.

## CONDITIONAL WAIVERS

Waivers must be explicit, time-bounded, and one-user scoped. A waiver does not turn the platform green.

- Target egress quality floor waiver: allowed only if the canary purpose is routing mechanics, not customer experience, and rollback is immediate.
- Reconcile false-positive waiver: allowed only after full read-only route/rule evidence proves candidate table consistency.
- Quiet-window rehearsal waiver: not allowed for canary; rehearsal success is mandatory.
- Trusted RU stale-state waiver: allowed only if the candidate path and target egress do not affect Trusted RU/Gosuslugi-sensitive route classes.
- Anti-flap waiver: allowed only when autoswitch is held and the operator accepts that the candidate was recently unstable.

## NO-GO Criteria

Any one of these blocks canary:

- autoswitch timer can still run `v7-users-autoswitch --apply`;
- candidate user is in anti-flap penalty/freeze;
- target egress is below policy quality floor or overloaded;
- kill switch warning/failure;
- user route check warning/failure;
- provisioning reconcile warning/failure;
- unexplained route consistency errors;
- rollback command or post-checks unclear;
- plan requires `v7-routing-sync` as first live action;
- Trusted RU/Gosuslugi-sensitive state is relevant and stale;
- operator approval is missing.

## Current Blockers

- Autoswitch apply timer is active.
- Block E8 found an external loop process that still invokes `v7-users-autoswitch` after the systemd timer/service hold.
- Candidate user `10.7.0.13` is in penalty until 2026-05-25T02:05:31Z.
- `v7-reconcile-check` reports 11 missing ip rule lookup table errors.
- Target `awg3` has capacity but quality below threshold.
- Trusted RU decision evidence is stale and sensitive.

## Recommendation

Continue governance. Do not run live canary yet.
