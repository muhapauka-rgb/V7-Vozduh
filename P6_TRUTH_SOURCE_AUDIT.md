# P6 Truth Source Audit

Project: V7 Vozduh

Block: P6

## Truth Source Map

| Domain | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| Movement packet | `/tmp/p6-first-user-movement-20260601T102011Z/packet.json` | packet hash and markdown summary | `P6_PACKET.md` |
| Approval | packet approval fields and TTL | approval validation JSON | `P6_APPROVAL_VALIDATION.md` |
| Movement preview | `v7-route-movement-preview` output | gate result | `P6_TARGET_READINESS.md`, `P6_PREMOVEMENT_RECHECK.md` |
| Rollback | rollback preview to `1` | rollback readiness report | `P6_ROLLBACK_READINESS.md` |
| Verification | live checkers and route/registry facts | final snapshot | `P6_FINAL_VERIFICATION.md` |
| Observation | live before/after/delayed/final snapshots | observation report | `P6_OBSERVATION_WINDOW.md` |

## Canonical Runtime Sources

- users: `/opt/v7/egress/state/users.registry`
- egress: `/opt/v7/egress/state/egress.registry`
- selected moves: selected-move files or canonical empty `[]`
- admin health: `http://127.0.0.1:7080/health`
- switch history: `/opt/v7/events/switch-history.jsonl`
- audit: `/opt/v7/audit/operator-execution-audit.jsonl`

## Conflict Review

No truth-source conflict was found.

Historical reports were used only for implementation precedent. The action used fresh runtime truth from `/opt/v7/egress/state`.

## Verdict

- truth_source_audit_complete=true
- truth_sources_clean=true
- stale_report_used_for_execution=false
