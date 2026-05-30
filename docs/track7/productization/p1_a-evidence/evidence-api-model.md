# P1.A Evidence API Model

evidence_api_defined=true

## API Surface

Required read APIs:

```text
GET /api/evidence
GET /api/evidence/{id}
GET /api/evidence/by-object/{type}/{id}
```

These APIs are read-oriented. Mutation endpoints for closure or annotation can be added later behind role and audit controls.

## `GET /api/evidence`

Purpose: list evidence bundles for tables, dashboards, logs and checks.

Query filters:

- `object_type`;
- `object_id`;
- `status`;
- `severity`;
- `source`;
- `tag`;
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
  "filters": {},
  "summary": {
    "open": 0,
    "warn": 0,
    "bad": 0
  }
}
```

## `GET /api/evidence/{id}`

Purpose: return complete drawer data for one bundle.

Response includes:

- bundle header;
- linked objects;
- summary;
- timeline;
- evidence items;
- recommendation;
- verification state;
- closure state;
- advanced details allowed for caller role.

## `GET /api/evidence/by-object/{type}/{id}`

Purpose: return bundles linked to the object currently visible in admin.

Example:

```text
GET /api/evidence/by-object/user/10.7.0.11
```

## Security Model

API must:

- redact secrets by default;
- enforce role visibility for advanced payloads;
- avoid exposing raw profile keys, tokens, passwords or private configs;
- include `redaction_state` for each item;
- log access to sensitive evidence when policy requires it.

## API Verdict

The Evidence API is a read-first product API that gives the current admin enough structured data for chips, drawers, logs, check results and future proposal cards.

