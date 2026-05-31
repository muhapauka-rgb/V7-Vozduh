# P1.B Proposal API Model

proposal_api_defined=true

## API Surface

Required read APIs:

```text
GET /api/proposals
GET /api/proposals/{id}
GET /api/proposals/by-object/{type}/{id}
```

Future mutation APIs may create, refresh, close or submit proposals to governance, but must be role-gated and audited.

## `GET /api/proposals`

Purpose: list proposals for overview, routing, users and channels.

Query filters:

- `proposal_type`;
- `status`;
- `confidence`;
- `severity`;
- `object_type`;
- `object_id`;
- `user`;
- `current_target`;
- `proposed_target`;
- `required_service`;
- `from`;
- `to`;
- `q`;
- `limit`;
- `cursor`.

Response shape:

```json
{
  "items": [],
  "next_cursor": null,
  "summary": {
    "active": 0,
    "review_required": 0,
    "expired": 0
  }
}
```

## `GET /api/proposals/{id}`

Purpose: return full drawer data for one proposal.

Response includes:

- proposal header;
- confidence and severity;
- affected objects/users;
- current/proposed targets;
- required services;
- evidence link;
- expected benefit;
- rollback hint;
- lifecycle timeline;
- governance path;
- advanced details allowed for caller role.

## `GET /api/proposals/by-object/{type}/{id}`

Purpose: show proposals linked to the object currently inspected by the operator.

Examples:

```text
GET /api/proposals/by-object/user/10.7.0.11
GET /api/proposals/by-object/channel/amneziawg-exec-20260528-10-8-1-14
```

## Security Model

API must:

- enforce role visibility;
- redact secret-bearing evidence summaries;
- clearly label preview-only vs executable state;
- never expose private profile material;
- never execute movement or autoswitch as a side effect of read APIs.

## API Verdict

Proposal API is a read-first product API for recommendations. It connects admin surfaces to stored proposals without runtime mutation.
