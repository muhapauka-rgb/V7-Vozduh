# V7 Vozduh — Wave 1 Evidence Foundation Implementation Report

wave1_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

## Implementation Result

evidence_store_implemented=true
evidence_api_implemented=true
evidence_ui_implemented=true
evidence_drawer_implemented=true
evidence_timeline_implemented=true
evidence_visible_in_admin=true

storage_backend_selected=JSONL

## Storage Decision

SQLite and JSONL were evaluated for the first Evidence Store.

SQLite advantages:
- stronger query model
- better indexing for large future evidence volume
- easier relational joins later

SQLite tradeoffs:
- requires schema/migration handling
- heavier operational surface for Wave 1
- less aligned with current V7 audit/log storage style

JSONL advantages:
- matches existing audit/event lineage patterns
- append-friendly for future evidence writers
- simple operational support
- no migration requirement for first read-only implementation
- easy to combine persisted bundles with generated runtime evidence

JSONL tradeoffs:
- limited indexing until a later store/index layer
- query performance is linear for now

Decision:
JSONL is selected for Wave 1 because it fits the current V7 architecture and keeps Evidence read-only, low-risk, and visible immediately. The store path is controlled by `V7_EVIDENCE_STORE_FILE` and defaults to:

`$V7_STATE_DIR/evidence-bundles.jsonl`

## Reality-First Mapping

Product Capability:
Evidence Foundation visible to operators.

Admin Surface:
Existing `/admin-v2` sections: `Главная`, `Пользователи`, `Каналы`, `Маршруты`, `Проверки`, `Логи`.

Runtime Service:
Existing `admin/v7-admin-api`; no new service.

Storage:
Read-only JSONL Evidence Store plus generated bundles from current checks, logs, registries, and overview data.

API:
- `GET /api/evidence`
- `GET /api/evidence/{id}`
- `GET /api/evidence/by-object/{type}/{id}`

UI Component:
- EvidenceChip
- EvidenceDrawer
- EvidenceTimeline
- EvidenceSummary

## Files Changed

- `admin/v7-admin-api`
- `BLOCK_WAVE_1_EVIDENCE_FOUNDATION_IMPLEMENTATION_REPORT.md`

## Endpoints Added

- `GET /api/evidence`
- `GET /api/evidence/{id}`
- `GET /api/evidence/by-object/{type}/{id}`

## New Storage Files/Tables

- `V7_EVIDENCE_STORE_FILE`
- default: `$V7_STATE_DIR/evidence-bundles.jsonl`

No database table was created in Wave 1.

## Seed Data

Initial evidence bundles are generated from real read-only sources:

- checks: state freshness, route reality
- logs: audit tail
- overview data: users, channels, route state
- registries: `users.registry`, `egress.registry`

No fake demo data was added.

## Admin Integration

Evidence chips/drawers were integrated without new top-level navigation:

- `Главная`: alert detail drawer can open related evidence
- `Пользователи`: user rows and user drawers expose evidence
- `Каналы`: channel rows and channel drawers expose evidence
- `Маршруты`: route drawer exposes evidence
- `Проверки`: visible Evidence chips on check cards and readiness table
- `Логи`: log event drawer links log/user/channel evidence

## Screenshots List

Captured during browser verification in Codex:

- `/admin-v2#checks` with visible Evidence chips in the existing `Проверки` workflow
- Evidence Drawer opened from the diagnostics chip
- Evidence bundle drawer showing Timeline and Evidence items

## Test Results

tests_passed=true

- backend starts: pass
- admin renders: pass
- evidence APIs return data: pass
- drawer opens: pass
- timeline renders: pass
- no runtime mutation scan: pass
- no user movement scan: pass
- no routing mutation scan: pass
- `py_compile`: pass
- `git diff --check`: pass

Observed command results:

- `python3 -m py_compile admin/v7-admin-api`: pass with `PYTHONPYCACHEPREFIX=/private/tmp/pycache-wave1`
- API function smoke test: `list_total=2`, `diagnostics_total=1`, `detail_found=true`, `read_only=true`
- dangerous diff scan for movement/routing/autoswitch/kill-switch mutation strings: no matches
- browser verification: Evidence chip visible, drawer opened, bundle detail showed Timeline and Evidence items

## Safety Statement

Evidence is read-only.

Evidence is non-authoritative.

Evidence does not execute proposals.

Evidence does not move users.

Evidence does not change routing.

Evidence does not apply actions.

## Remaining Notes

An existing admin render blocker was fixed during verification:

- `renderSettings()` referenced `rc` without declaring it.
- Added `const rc = p.reconnect || {};`.
- This is UI-only and does not mutate runtime.

## Recommended Next Wave

recommended_next_wave=WAVE_2_PROPOSAL_SYSTEM_IMPLEMENTATION

FINAL MUTATION STATEMENT

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
