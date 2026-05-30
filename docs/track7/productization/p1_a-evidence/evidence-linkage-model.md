# P1.A Evidence Linkage Model

evidence_linkage_defined=true

## Linkage Principle

Evidence bundles are object-linked. A bundle must be discoverable from the object the operator is already inspecting.

## Supported Object Types

| Object type | Link purpose |
| --- | --- |
| `User` | Explain user issue, route state, required services, movement recommendation, verification result. |
| `Channel` | Explain channel health, service support, capacity, readiness, failures. |
| `Proposal` | Explain why a proposal exists and what proof supports or blocks it. |
| `Alert` | Explain alert root cause, severity and next safe action. |
| `Route` | Explain route class, route reality, service routing and route checks. |
| `Release` | Explain release provenance, validation, deployment and rollback readiness. |
| `Backup` | Explain backup freshness, scope, integrity and restore suitability. |
| `Restore` | Explain restore plan, execution proof and post-restore verification. |

## Link Cardinality

One object can have many bundles.

One bundle can link to multiple objects, but it must have one primary object:

```text
primary_object = where the operator should start
related_objects = supporting context
```

## Query Requirements

Evidence must support lookup by:

- `bundle_id`;
- `object_type + object_id`;
- `status`;
- `severity`;
- `source`;
- `time range`;
- `tag`;
- `correlation_id`.

## Required Link Metadata

Each link should include:

- `object_type`;
- `object_id`;
- `relationship`;
- `display_label`;
- `admin_surface`;
- `created_at`;
- `confidence`.

## Linkage Verdict

Evidence linkage makes proof available in context without creating new navigation. The same bundle can support checks, logs, proposals, recovery and release verification.

