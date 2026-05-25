# V7 Phase 0 Experimental Areas

Purpose: identify areas that are exploratory, transitional, or not yet mature enough to be treated as core contracts.

## Experimental Or Transitional Areas

### Design Snapshots

Path: `design/`

Why experimental:

- multiple copies and alternatives;
- static HTML snapshots rather than a maintained frontend source tree;
- not yet a modular UI system.

Boundary: do not let snapshot complexity dictate product IA.

### Public Client Speed Flow

Paths:

- `tools/v7-client-speed-api`
- client speed links/state in `admin/v7-admin-api`
- `tools/v7-path-sample-ingest`

Why transitional:

- valuable for client-side datapath visibility;
- contracts need stronger documentation;
- public gateway/speed collection should remain bounded and abuse-aware.

### Proxy Public Runtime And Identity

Paths:

- proxy helpers inside `admin/v7-admin-api`
- `tools/v7-public-gateway`
- external `v7-proxy-*` commands

Why experimental:

- many external runtime commands are referenced but not in repo;
- public exposure changes carry high operational risk;
- should remain guarded, audited, and owner-level where applicable.

### Egress Import Expansion

Paths:

- `admin/v7-admin-api` egress parser/draft blocks;
- `tools/v7-egress-import-regression`.

Why transitional:

- supports many protocols and link formats;
- parsing complexity is high;
- should remain quarantine-first and preview-first.

### Adaptive/Intelligence Concepts

Status: roadmap only, not active Phase 0 implementation.

Boundary:

- no black-box routing;
- no uncontrolled experimentation;
- no production-wide adaptive routing changes.

## Experimental Area Rules

- Keep opt-in.
- Keep quarantined when possible.
- Add contracts before expanding behavior.
- Prefer preview/dry-run before apply.
- Preserve deterministic routing core.

