# Block E9.3.2 — Staged Autoswitch Restore Governance Report

Mode: read-only / restore governance design only.

## Summary

E9.3.2 creates the staged restore governance model required after E9.3.1 showed that restoring `v7-users-autoswitch.timer` can immediately run `v7-users-autoswitch --apply` and move non-candidate users.

No live action was executed.

## Required Answers

| Field | Value |
|---|---|
| staged_restore_model_created | `true` |
| recommended_restore_model | `planner_first_apply_by_separate_approval` |
| apply_restore_requires_separate_approval | `true` |
| future_canary_restore_sequence_safe | `false` |
| second_canary_readiness | `CONDITIONAL_AFTER_STAGED_RESTORE_APPROVAL` |
| execution_allowed_now | `false` |
| exact_next_recommended_step | prepare an E9.3.3 staged-restore rehearsal approval packet or operator approval flow; do not run another canary yet |

## New Governance Artifacts

| Artifact | Purpose |
|---|---|
| `docs/track7/control-plane/STAGED_AUTOSWITCH_RESTORE_MODEL.md` | defines Stage A-F restore model |
| `docs/track7/control-plane/STAGED_RESTORE_EVIDENCE_REQUIREMENTS.md` | defines required evidence for each stage |
| `docs/track7/control-plane/APPLY_RESTORE_APPROVAL_RULES.md` | defines GO/NO-GO rules for apply restore |
| `docs/track7/control-plane/STAGED_CANARY_RESTORE_RUNBOOK.md` | future command sequence, explicitly not executed |
| `docs/track7/control-plane/e9_3_2-evidence/README.md` | evidence folder marker |

## Model

```text
Stage A: hold planner/apply; health active
Stage B: execute exactly one approved canary user movement and rollback/decision
Stage C: restore planner only
Stage D: observe planner-only pending movement
Stage E: request separate apply restore approval
Stage F: restore apply only if approved and classify post-apply movement separately
```

## Current Status

The restore model is now designed, but not live-proven:

```text
canary_window_status=not_running
restore_planner_status=design_only
apply_restore_status=requires_separate_approval
post_restore_movement_classification=previous_event_expected_but_unsafe
execution_allowed_now=false
```

## Why Future Canary Restore Is Not Yet Safe

The design removes ambiguity, but it does not itself prove runtime behavior. A future live block must validate planner-only restore before apply authority is restored. Until then, future canary execution remains blocked.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```

