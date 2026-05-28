# E9.3.6 Autoswitch Policy Analysis

Mode: source/static analysis plus read-only runtime evidence.

## Source References

- `tools/v7-users-autoswitch` lines 873-904: per-user decision path.
- `tools/v7-users-autoswitch` lines 1149-1174: service/route-class eligibility gates.
- `tools/v7-users-autoswitch` lines 1352-1367: selected move grouping and failover limit.
- `tools/v7-users-autoswitch` lines 1369-1407: projected movement picker.
- `tools/v7-users-autoswitch` lines 1442-1451: no mutation without `--apply` and no selected moves.

## Eligibility Logic

For each user, the tool computes candidates and the current egress candidate. If the current egress candidate is absent or not eligible, the failover path is entered and `current_egress_not_eligible` is appended to the decision reason.

Non-Telegram service failures are hard gates:

```text
if service row ok is false -> block candidate as service_<service>_failed
```

Telegram is treated differently:

- hard-blocked Telegram blocks candidate;
- degraded Telegram adds a reason and score penalty;
- degraded Telegram alone is not the hard blocker seen in E9.3.5.

## Why Egress 1 Was Blocked

The E9.3.5 planner sample included `blocked=["service_instagram_failed"]` for egress `1`. That made `current.eligible=false` for users currently on `1`, so the failover path selected the best eligible alternative.

This is expected under current code. It is not a routing-sync or route-table issue.

## Why VLESS Was Selected

`vless` was the best eligible failover target in the E9.3.5 sample:

- services OK;
- load OK;
- route class OK;
- no hard service block;
- `1` was ineligible;
- AWG/OpenVPN/WireGuard alternatives were blocked or lower quality under the planner scoring/gates.

## Why 15 Candidates But 3 Selected

The planner reports both total candidate decisions and selected moves:

```text
candidate_moves_total=sum(all decisions where recommended != current)
selected_moves=len(selected after policy limits)
```

The selected set is limited by `autoswitch_max_failover_per_run`. Current policy evidence from earlier governance blocks and planner output shows:

```text
autoswitch_max_failover_per_run=3
```

Therefore 15 candidate decisions and 3 selected moves is expected behavior: the signal applied to all enabled users on egress `1`, while the per-run failover limit capped the immediate apply blast radius at 3.

## Canary Watcher vs Autoswitch Eligibility

There is no conflict in this specific E9.3.5 sample:

- E9.3.3 previously saw pending `1 -> awg3`.
- E9.3.5 final sample selected `1 -> vless`.
- E9.3.6 current snapshot shows `selected_moves=[]` in later planner evidence.

The target changed because the input service/quality state changed. This confirms the planner-only state is volatile and must be sampled immediately before any apply restore.

## Policy Risk

Current policy behavior is operationally plausible but governance-sensitive:

- It protects users from a current egress with a failed important service.
- It can convert one transient service failure into many candidate movements.
- It caps immediate failover to 3, but repeated timer runs could continue moving users if the signal persists.

## Conclusion

```text
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
policy_too_aggressive=conditional
max_failover_behavior_expected=true
apply_restore_safe_now=false
```

Apply should remain held until either the planner shows stable zero selected moves immediately before restore or an operator explicitly approves the exact selected movement list and max movement count.
