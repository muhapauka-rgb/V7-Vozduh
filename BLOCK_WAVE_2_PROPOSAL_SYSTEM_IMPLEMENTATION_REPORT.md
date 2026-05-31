# V7 Vozduh — Wave 2 Proposal System Implementation Report

wave2_completed=true

## Result

Proposal System implemented as the read-only layer after Evidence:

Problem -> Evidence -> Proposal

Proposal remains non-authoritative and non-executing. It recommends, explains, prioritizes, and previews governance path only.

## Implementation Summary

proposal_store_implemented=true

proposal_api_implemented=true

proposal_ui_implemented=true

proposal_drawer_implemented=true

proposal_visible_in_admin=true

proposal_links_to_evidence=true

proposal_generation_working=true

storage_backend_selected=JSONL

Storage decision:
- SQLite: better future lifecycle/querying, higher operational weight for Wave 2.
- JSONL: matches Evidence Store, simple append/read model, low operational risk, enough for read-only generated/store records.
- Selected: JSONL, consistent with Wave 1 Evidence Foundation.

## Reality-First Mapping

Product Capability:
Read-only routing intelligence proposal layer linked to Evidence.

Admin Surface:
Existing V7 Admin `/admin-v2`, integrated into:
- Главная
- Пользователи
- Каналы
- Маршруты

Runtime Service:
`admin/v7-admin-api` generates proposals from existing checks, evidence bundles, service health, route reality, channel state, and overview data.

Storage:
`proposal-records.jsonl` through `V7_PROPOSAL_STORE_FILE`, defaulting under `STATE_DIR`.

API:
- `GET /api/proposals`
- `GET /api/proposals/{id}`
- `GET /api/proposals/by-object/{type}/{id}`

UI Component:
- Proposal chip
- Proposal list drawer
- Proposal detail drawer
- Proposal timeline
- Governance path explanation
- Evidence link button

## Files Changed

- `admin/v7-admin-api`
- `BLOCK_WAVE_2_PROPOSAL_SYSTEM_IMPLEMENTATION_REPORT.md`

## Endpoints Added

- `GET /api/proposals`
- `GET /api/proposals/{id}`
- `GET /api/proposals/by-object/{type}/{id}`

No mutation endpoint was added.

`POST /api/proposals` returns 404.

## Storage Files / Tables

storage_backend=jsonl

new_storage_file=proposal-records.jsonl

No database table was added.

## Generated Proposal Types

- MOVEMENT_PROPOSAL
- EVACUATION_PROPOSAL
- REBALANCE_PROPOSAL
- OBSERVATION

Every generated proposal requires `evidence_bundle_id`.

## Browser Verification

Verified surfaces:
- Главная: proposal chips visible in user/channel summaries.
- Пользователи: proposal chips visible in user rows.
- Каналы: proposal chips visible in channel rows.
- Маршруты: proposal chip visible in route toolbar.

Verified drawer behavior:
- Proposal list drawer opens.
- Proposal detail drawer opens.
- Detail shows confidence, affected users, evidence link, expected benefit, rollback hint, timeline, and governance path.
- No execution/apply controls are present.

Screenshots captured:
- `/private/tmp/v7-wave2-overview-proposals.png`
- `/private/tmp/v7-wave2-proposal-detail.png`

## Test Results

tests_passed=true

- backend starts: passed on `127.0.0.1:18083`
- proposal APIs return data: passed
- proposal detail links evidence: passed
- proposal drawer opens: passed
- proposal visible in admin: passed
- no mutation API added: passed
- `POST /api/proposals`: 404, passed
- `PYTHONPYCACHEPREFIX=/private/tmp/pycache-wave2 python3 -m py_compile admin/v7-admin-api`: passed
- `git diff --check`: passed
- dangerous-call scan for added diff: passed, no `v7-user-switch`, autoswitch apply, route mutation, kill-switch mutation, or POST action added

## Safety Statement

runtime_mutation_performed=false

user_movement_performed=false

routing_mutation_performed=false

autoswitch_apply_performed_manually=false

Proposal is read-only, non-authoritative, non-executing, and cannot move users, change routing, reserve capacity, lock users, create batch authority, or apply autoswitch.

## Recommended Next Wave

recommended_next_wave=WAVE_3_RUNTIME_AND_RELEASE_TRUST_IMPLEMENTATION

FINAL MUTATION STATEMENT

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
