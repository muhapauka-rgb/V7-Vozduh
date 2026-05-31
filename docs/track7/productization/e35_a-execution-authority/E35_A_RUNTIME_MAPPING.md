# E35.A Runtime Mapping

## Mapping Table

| Concept | Runtime | Storage | Registry | API | Admin | Audit | Evidence / Proposal / Trust | Execution / Rollback |
|---|---|---|---|---|---|---|---|---|
| Current assignment | Route state | `users.registry` | `current`, `table` | existing overview/users APIs | Users/Routes | route/audit logs | Evidence can reference | Movement changes it only after authority and recheck |
| Authority state | Authority evaluator | `routing-authority.json` | not stored in registry | `/api/routing-authority/*` | Users/Channels/Settings | authority events | Evidence/Proposal refs | gates movement before execution |
| Authority event | Append-only event | `routing-authority-events.jsonl` | none | events API | Logs/Timeline | append-only | evidence linkage | no movement |
| AUTO | admission mode | authority store or group default | none | user authority API | Users drawer | events | proposals may recommend | autoswitch/governance may proceed if gates pass |
| OPERATOR_PINNED | admission lock | authority store | none | pin/unpin APIs later | Users/Channels | pin events | evidence/proposal optional | blocks normal movement away; emergency exception |
| MANUAL | operator-owned mode | authority store | none | set-mode API later | Users drawer | mode events | evidence optional | blocks autonomous forward; rollback allowed |
| Emergency authority | containment admission | authority event + active emergency state | none | emergency state API | Home/User/Logs | emergency event | evidence required | escape/return/rollback only |
| Governance | packet-bound authority | packet/audit stores | hash references | existing/future governance APIs | Proposal/Logs | packet audit | evidence required | exact scope only |
| Autoswitch | proposed movement source | selected moves/state files | reads registry | autoswitch plan APIs | Channels/Routes | autoswitch logs | proposals/evidence | cannot bypass authority |

## Runtime Evaluation Point

Authority evaluator should be called before:

- autoswitch selected moves are accepted for apply;
- admin manual switch confirms runtime movement;
- governed execution packet proceeds to execution-time recheck;
- future scheduler launches a batch.

## Evaluation Input

```json
{
  "actor": "AUTOSWITCH",
  "action": "FORWARD_MOVE",
  "user_ip": "10.7.0.11",
  "from_egress": "1",
  "to_egress": "awg2",
  "reason": "candidate_score_beats_current",
  "evidence_bundle_id": "",
  "proposal_id": ""
}
```

## Evaluation Output

```json
{
  "decision": "DENY",
  "reason": "operator_pinned",
  "routing_mode": "OPERATOR_PINNED",
  "routing_owner": "OPERATOR",
  "allowed_actions": ["rollback", "emergency_escape"],
  "admin_message": "Пользователь закреплён оператором"
}
```

## API Plan

Read-only first:

- `GET /api/routing-authority/users`
- `GET /api/routing-authority/users/{ip}`
- `GET /api/routing-authority/events`
- `POST /api/routing-authority/decision-preview`

Future mutation:

- `POST /api/routing-authority/users/{ip}/set-mode`
- `POST /api/routing-authority/users/{ip}/pin`
- `POST /api/routing-authority/users/{ip}/unpin`
- `POST /api/routing-authority/users/{ip}/emergency-return-preview`

Mutation APIs change only authority state unless explicitly part of later governed execution block.

## Storage Compatibility

Do not change:

- `users.registry` assignment semantics;
- `egress.registry` channel identity semantics;
- service preferences semantics;
- Evidence/Proposal/Trust non-authoritative behavior.

Extend:

- admin API with authority read/preview;
- autoswitch planner with authority gate;
- admin UI with authority visibility;
- logs/evidence links.

## Verdict

```text
runtime_mapping_defined=true
```
