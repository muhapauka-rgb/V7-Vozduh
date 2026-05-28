# E9.3.3 Pending Move Analysis

Mode: live restore-governance rehearsal evidence analysis.
Runtime mutation scope used in this block: temporary planner/apply hold and planner-only restore.

## Evidence Inputs

- `pre-rehearsal.txt`
- `hold-confirmation.txt`
- `quiet-baseline.txt`
- `planner-restore-confirmation.txt`
- `planner-only-sample-A.txt`
- `planner-only-sample-B.txt`
- `planner-only-sample-C.txt`
- `final-authority-status.txt`
- `latest-planner-journal.jsonl`

## Authority State Observed

Planner-only restore was achieved:

- `v7-health.service`: active/running.
- `v7-autoswitch-planner.timer`: active.
- `v7-autoswitch-planner.service`: transient, inactive/dead between runs.
- `v7-users-autoswitch.timer`: inactive/dead.
- `v7-users-autoswitch.service`: inactive/dead.

The apply timer was not restored in this block.

## Registry And Routing Stability

The baseline registry hashes stayed stable across quiet baseline and planner-only samples:

- `users.registry`: `045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222`
- `egress.registry`: `67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f`

The runtime checkers stayed OK:

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

No `v7-user-switch` process was observed. No `v7-routing-sync` process was observed. No manual or timer-driven autoswitch apply execution was observed.

## Planner Output

Planner-only output was visible in the planner journal. During samples A/B/C, planner results were dry-run/non-apply:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=dry_run
```

In the final authority status sample, the latest captured planner output showed pending failover recommendations while apply authority remained held. The observed selected moves were:

| User | Current | Recommended | Move Type | Reason Class |
|---|---|---|---|---|
| `10.7.0.5` | `1` | `awg3` | `failover` | current egress not eligible under transient Telegram/down signal |
| `10.0.0.2` | `1` | `awg3` | `failover` | current egress not eligible under transient Telegram/down signal |
| `10.0.0.3` | `1` | `awg3` | `failover` | current egress not eligible under transient Telegram/down signal |

The journal output was too large for a fully clean JSON parse in the final sample because journald line splitting occurred, but the captured evidence exposes at least these three selected moves. No selected move was applied because `v7-users-autoswitch.timer` remained inactive.

## Classification

```text
pending_moves_visible=true
pending_moves_count=3_observed
pending_moves_summary=10.7.0.5,10.0.0.2,10.0.0.3 -> awg3 failover recommendations
apply_restore_status=HELD_REQUIRES_SEPARATE_APPROVAL
```

This confirms the staged restore model is useful: planner-only restore can reveal autoswitch recovery/failover intent before apply authority is restored.

## Governance Verdict

Planner-only stage was safe during this rehearsal:

- no user movement;
- no routing drift;
- no registry drift;
- no apply process;
- runtime checkers OK.

Apply restore is not safe to perform automatically. The planner identified possible non-canary user movements; therefore `v7-users-autoswitch.timer` must remain held until a separate operator approval names the accepted movement count and accepted movement reasons.
