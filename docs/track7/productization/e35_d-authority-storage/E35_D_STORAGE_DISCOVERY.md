# E35.D Storage Discovery

## Scope

E35.D defines where Authority state, events, read models and admin visibility live.

No implementation or runtime mutation is performed.

## Existing Stores

| Store | Purpose | Owner | Truth Source | Retention | Read APIs/Admin Usage | Classification |
|---|---|---|---|---|---|---|
| `users.registry` | Current user assignment and route table | runtime | yes for current route | runtime managed | overview/users/routes | Reuse, Do Not Duplicate |
| `egress.registry` | Channel identity/static metadata | runtime | yes for channel identity | runtime managed | overview/channels | Reuse, Do Not Duplicate |
| Identity DB `v7-identity.db` | users/groups/org identity | admin | yes for identity | long-lived | users/settings | Reuse |
| Org policy JSON | group/channel routing policy | admin/runtime policy | yes for group/channel constraints | config lifecycle | settings/channels/autoswitch | Extend |
| Evidence Store | evidence bundles | admin read model | no for authority | JSONL active/archive | `/api/evidence` | Link Only |
| Proposal Store | non-authoritative recommendations | admin read model | no for authority | JSONL active/archive | `/api/proposals` | Link Only |
| Runtime Trust Store | runtime convergence/drift | admin trust surface | trust input | JSONL | `/api/runtime/*` | Reuse as Input |
| Release Trust Store | release lineage/rollback | admin trust surface | trust input | JSONL | `/api/release/*` | Reuse as Input |
| Audit logs | operator/admin action audit | admin/security | audit truth | append/archive | logs | Reuse |
| Switch history | route movement history | runtime/events | movement history | append/archive | operator/logs | Reuse |
| Operator execution records | approval/denial/replay records | governance | governance audit truth | JSONL append | operator views | Reuse |
| Approval packet records | bounded execution contract | governance | execution authority | packet TTL + audit | operator/governance | Reuse |
| Closure Store | closure workflow | admin ops | closure status | JSONL | evidence/proposal/trust | Link Only |

## Reuse Conclusions

Authority must not be stored in:

- `users.registry`: this is current runtime assignment, not intent.
- `egress.registry`: this is channel identity, not per-user authority.
- Evidence/Proposal stores: these explain and recommend, but are non-authoritative.
- Runtime/Release Trust stores: these are trust inputs, not authority truth.

Authority should use:

- a dedicated state store for current authority truth;
- an append-only event store for audit and timelines;
- read adapters that combine authority with registries, Evidence, Proposal and Trust.

## Verdict

```text
storage_discovery_complete=true
existing_stores_classified=true
single_authority_store_required=true
```
