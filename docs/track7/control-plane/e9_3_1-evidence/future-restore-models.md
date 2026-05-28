# E9.3.1 Future Restore Models

Mode: design analysis only. No implementation or runtime mutation is authorized here.

## Model A — Restore Planner First, Observe, Restore Apply Later

Sequence:

1. Keep `v7-health.service` active.
2. Restore `v7-autoswitch-planner.timer`.
3. Observe at least two planner periods.
4. Inspect planner output, safety state, selected moves, and registry stability.
5. Restore `v7-users-autoswitch.timer` only after explicit operator approval.

Pros:

- Separates advisory planner state from mutation authority.
- Exposes pending failovers before apply is re-enabled.
- Keeps health/state loop active.

Cons:

- Requires an extra approval checkpoint.
- Planner itself can still write planner/reconnect/load state.
- Does not prevent future apply movement after approval.

Verdict:

```text
recommended_minimum_future_model=true
```

## Model B — Restore Planner Only; Separate Approval Before Apply Restore

Sequence:

1. Restore planner timer only.
2. Leave apply timer held.
3. Collect a formal post-canary planner-only evidence packet.
4. Decide separately whether to restore apply authority, continue hold, or perform a controlled autoswitch recovery.

Pros:

- Strongest attribution boundary.
- Prevents immediate hidden post-restore user movement.
- Makes pending autoswitch movements visible before they mutate runtime.

Cons:

- Leaves autoswitch apply unavailable until separate approval.
- Operator must explicitly own the interim control-plane state.

Verdict:

```text
recommended=true
future_restore_model_recommended=planner_first_apply_by_separate_approval
```

## Model C — Restore Apply in Paused/Drain Mode

This would require product/tooling support that does not currently exist in the proven runtime model.

Potential behavior:

- apply service starts but suppresses user movement;
- planned/failover moves are written to a pending queue;
- operator approves or rejects each move.

Pros:

- Durable long-term model if implemented.

Cons:

- Requires code/systemd changes.
- Not available for immediate governance.

Verdict:

```text
design_future_only=true
```

## Model D — Restore Apply but Suppress Immediate Migrations

This would require an explicit autoswitch guard such as:

```text
--restore-grace-period
--preview-after-hold
--no-immediate-apply
```

No such live-proven mechanism exists in the current evidence.

Verdict:

```text
not_available_now=true
```

## Model E — Snapshot Desired State Before Hold and Compare Before Apply Restore

Sequence:

1. Snapshot `users.registry`, route tables, planner state, safety state, and desired state before hold.
2. After canary rollback, restore planner only.
3. Compare desired moves against pre-hold baseline.
4. If selected moves exist, classify them before restoring apply.

Pros:

- Provides explicit pending-move detection.
- Explains whether restore movement is recovery, stale state, or newly caused by the canary.

Cons:

- Does not itself stop apply unless paired with Model A or B.

Verdict:

```text
recommended_as_evidence_layer=true
```

## Recommended Future Model

Use Model B with Model E evidence:

```text
1. restore planner timer only;
2. observe planner-only selected moves and state deltas;
3. keep apply timer held;
4. require explicit operator approval to restore apply;
5. if pending movements exist, treat apply restore as a separate controlled autoswitch recovery stage, not part of the canary.
```

This model preserves one-user canary attribution and makes post-restore autoswitch movement explicit before mutation authority returns.

