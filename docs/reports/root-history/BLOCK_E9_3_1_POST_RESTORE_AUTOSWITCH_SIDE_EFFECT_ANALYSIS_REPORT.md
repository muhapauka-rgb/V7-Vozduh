# Block E9.3.1 — Post-Restore Autoswitch Side-Effect Analysis Report

Mode: read-only / restore-sequence analysis only.

## Summary

E9.3 mechanically succeeded as a waiver-based one-user canary:

```text
10.7.0.14: vless -> openvpn-1779388847-d2ad7c -> vless
quiet_window_preserved=true
candidate_blast_radius=one_user
checks_OK=true
```

However, after restoring autoswitch timers, the restored apply authority immediately moved another user:

```text
10.7.0.5: 1 -> vless
table_1003: v7e356a192b79 -> tun0
```

This was not manual apply and not manual user-switch. It was timer-driven autoswitch behavior after restore.

## Required Findings

| Question | Answer |
|---|---|
| restore_side_effect_classification | `EXPECTED_BUT_UNSAFE_RESTORE_SEQUENCE` |
| autoswitch_root_cause | `timer_restore_immediate_apply_failover` |
| blast_radius_during_canary | `one_user` |
| blast_radius_after_restore | `broader_than_canary` |
| restore_sequence_safe | `false` |
| restore_sequence_governance_gap | `true` |
| future_restore_model_recommended | `planner_first_apply_by_separate_approval` |
| second_canary_readiness | `NO-GO` |
| execution_allowed_now | `false` |

## Exact Restore Chain

```text
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

Immediately after that, evidence showed:

```text
python3 /usr/local/bin/v7-users-autoswitch
python3 /usr/local/bin/v7-users-autoswitch --apply
```

The apply service was triggered by `v7-users-autoswitch.timer`, whose unit executes:

```text
/usr/local/bin/v7-users-autoswitch --apply
```

## Why 10.7.0.5 Moved

The saved safety state classified the movement as:

```text
user_ip=10.7.0.5
move_type=failover
updated=2026-05-25T18:28:50.345236+00:00
```

The autoswitch source classifies failover when the current egress is not eligible, then selects the best eligible failover target. Runtime policy allowed failover movements:

```text
autoswitch_enabled=true
autoswitch_mode=guarded
autoswitch_max_failover_per_run=3
```

The most precise supported root cause is:

```text
restored apply timer fired immediately;
autoswitch saw 10.7.0.5 on egress 1;
egress 1 was considered not eligible at that moment;
vless was selected as failover target;
autoswitch invoked v7-user-switch under timer authority.
```

## Expected or Governance Failure?

This behavior is expected from the current timer/service design but unsafe for canary attribution:

- expected: the apply timer is designed to run `v7-users-autoswitch --apply`;
- expected: failover is allowed by guarded policy;
- unsafe: restoring apply authority can move users outside the approved canary user;
- governance gap: the restore phase was not bounded separately from the canary phase.

## Future Restore Model

Recommended:

```text
restore planner first;
observe planner-only state and selected moves;
keep apply timer held;
restore apply only under separate explicit approval;
treat apply restore as a separate autoswitch recovery stage.
```

This keeps the canary result interpretable. It also makes any pending autoswitch movement visible before mutation authority resumes.

## Second Canary Implication

Second canary mechanics remain possible in principle, but the current restore model is not acceptable for another live canary because post-restore can widen blast radius automatically.

```text
second_canary_readiness=NO-GO
blocked_by=restore_sequence_governance_gap
```

Next step should not be a third canary or another second-canary execution. The next step should be an E9.3.2-style restore governance packet that implements or approves staged restore semantics.

## Artifacts

| Artifact | Purpose |
|---|---|
| `docs/track7/control-plane/e9_3_1-evidence/read-only-runtime-snapshot.txt` | read-only runtime snapshot after side effect |
| `docs/track7/control-plane/e9_3_1-evidence/restore-timeline.md` | restore event timeline |
| `docs/track7/control-plane/e9_3_1-evidence/autoswitch-root-cause.md` | root-cause analysis |
| `docs/track7/control-plane/e9_3_1-evidence/blast-radius-analysis.md` | canary vs restore blast-radius boundary |
| `docs/track7/control-plane/e9_3_1-evidence/future-restore-models.md` | restore alternatives |

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```

