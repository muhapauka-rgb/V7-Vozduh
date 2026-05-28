# E14 Freshness And Stale Evidence Model

## Purpose

Governed routing decisions must be made against current truth. E14 defines how
freshness, stale evidence, conflicts, and invalidation work for operator
objects and approvals.

## State Source Classes

| Source | Meaning | Approval use |
|---|---|---|
| `live` | Collected from current runtime or current read-only tool output. | Can support approval if fresh. |
| `copied_state` | Runtime state copied for local analysis or rehearsal. | Cannot directly approve live mutation. |
| `simulation` | Designed or computed scenario. | Planning only. |
| `historical` | Archived block report or evidence. | Audit only. |

## Freshness Fields

Every governance object carries:

- collected_at;
- valid_until;
- state_source;
- source_refs;
- registry hashes;
- generation id when applicable;
- confidence;
- stale boolean;
- stale reasons.

## Freshness Status

| Status | Meaning | UI behavior |
|---|---|---|
| `fresh` | Within validity window and no invalidation trigger. | Can support read-only summary and approval gates. |
| `aging` | Still valid but near expiry. | Show quiet warning; approval may require refresh soon. |
| `stale` | Expired or invalidated. | Disable approval; allow regenerate only. |
| `conflicting` | Two current sources disagree. | Mark operator state STALE or BLOCKED. |
| `historical_only` | No current live object exists. | Audit only; cannot approve. |

## Freshness Scoring

Freshness score is qualitative:

- high: live, recent, consistent hashes, matching generation;
- medium: live and recent but non-critical detail missing;
- low: old, copied-state, historical, or missing generation;
- invalid: conflicting, expired, or drifted.

The UI should show the status label, not a numeric score.

## Invalidation Triggers

Approvals and previews invalidate on:

- users registry hash drift;
- egress registry hash drift;
- switch-history count increase;
- selected-move fingerprint change;
- selected-move count exceeds budget;
- planner generation change;
- apply generation mismatch;
- restore barrier id/status change;
- target readiness changes from GO;
- rollback target becomes unhealthy;
- runtime checker fails;
- hidden mover detected;
- approval expiry;
- token expiry or consumption.

## Stale Selected Moves

SelectedMoveSet becomes stale when:

- planner generation changes;
- source registry hash changes;
- autoswitch pressure changes after validity window;
- selected-move fingerprint no longer matches generation token;
- barrier/clearance state changes;
- dry-run source is copied-state but approval is live.

Stale selected moves cannot be applied or used for nonzero clearance.

## Stale Restore-Settle

RestoreSettleState becomes stale when:

- sample window expires;
- switch-history changes;
- registry hash changes;
- selected_moves becomes nonzero;
- hidden mover appears;
- apply timer state changes unexpectedly;
- runtime checker fails.

Restore-settle GO does not close delayed monitoring.

## Conflicting Evidence Handling

When two sources conflict:

1. Prefer current live object over historical report.
2. Prefer machine-readable current object over pretty text.
3. Prefer newer object only if source is equally authoritative.
4. If conflict affects approval, block and request refresh.
5. Preserve conflict in evidence metadata.

## Historical Vs Live Labels

Every evidence item in UI must display:

- current live;
- copied-state;
- simulation;
- historical;
- superseded.

Historical evidence can explain why a rule exists; it cannot approve a current
movement.

## Auto-Expiring Approvals

Approval expiration is automatic and non-mutating. It changes the read model
status only. Expired approvals remain visible in history as expired, not
deleted.

## Operator Warnings

Stale warning format:

```text
approval disabled: users_registry_hash changed after preview
safe next action: regenerate movement preview
```

Warnings must name the failed gate and the safe next action.

## Freshness Verdict

Freshness is a safety primitive, not UI decoration. Any approval relying on
stale, conflicting, copied-state, or historical-only evidence is blocked.

