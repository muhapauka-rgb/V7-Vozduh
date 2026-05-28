# E9.3.1 Blast Radius Analysis

Mode: read-only governance analysis.

## During Canary Window

The held canary window respected the intended one-user blast radius:

```text
candidate_user=10.7.0.14
forward=vless -> openvpn-1779388847-d2ad7c
rollback=openvpn-1779388847-d2ad7c -> vless
only_candidate_moved=true
routing_table_changed=1012 only
autoswitch_process_observed=false
v7-routing-sync_observed=false
checks_OK=true
```

During this phase, the blast radius was one user.

## After Restore

The restore phase widened the practical blast radius:

```text
restored_timer=v7-users-autoswitch.timer
restored_service=v7-users-autoswitch.service
apply_authority_resumed=true
timer_driven_autoswitch_movement=true
additional_user_moved=10.7.0.5
additional_table_changed=1003
```

After restore, the blast radius was no longer limited to the canary user because apply authority resumed and acted on current autoswitch policy state.

## Classification

Primary classification:

```text
EXPECTED_BUT_UNSAFE_RESTORE_SEQUENCE
```

Secondary governance classification:

```text
RESTORE_SEQUENCE_GOVERNANCE_GAP
```

This was expected in the narrow sense that restored `v7-users-autoswitch.timer` is designed to trigger `v7-users-autoswitch --apply`, and policy allowed failover. It was unsafe for canary attribution because the restore sequence did not separate "canary proof complete" from "autoswitch apply authority resumed and may move other users."

## Did Restore Violate the Intended Blast-Radius Model?

Yes, if the canary operation is defined as including restore. The quiet-window canary itself was one-user bounded, but the full operational sequence ended with another timer-driven user movement.

Future reports must distinguish:

| Stage | Blast Radius |
|---|---|
| held canary window | one user |
| rollback window | one user |
| restore observation window | potentially broader if apply timer resumes |

## Governance Verdict

```text
blast_radius_during_canary=one_user
blast_radius_after_restore=broader_than_canary
restore_sequence_safe=false
restore_sequence_governance_gap=true
```

