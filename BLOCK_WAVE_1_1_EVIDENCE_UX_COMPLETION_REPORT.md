# BLOCK WAVE 1.1 EVIDENCE UX COMPLETION REPORT

Completion date: 2026-05-30

Mode: implementation fixes.

## Summary

Wave 1.1 completed the visible Evidence UX integration without changing the Evidence storage backend, API model, or runtime authority model.

Evidence is now reachable as a first-class operator capability from the existing V7 Admin workflows:

- `Главная`
- `Пользователи`
- `Каналы`
- `Маршруты`
- `Проверки`
- `Логи`

No new top-level navigation, pages, storage model, API model, or architecture entity was introduced.

## Required Answers

| Field | Value |
| --- | --- |
| `wave1_1_completed` | `true` |
| `users_evidence_visible` | `true` |
| `channels_evidence_visible` | `true` |
| `routing_evidence_visible` | `true` |
| `logs_evidence_visible` | `true` |
| `evidence_localization_complete` | `true` |
| `responsive_visibility_fixed` | `true` |
| `ux_consistent_with_v7` | `true` |
| `wave1_ready_for_wave2` | `true` |
| `runtime_mutation_performed` | `false` |
| `user_movement_performed` | `false` |
| `routing_mutation_performed` | `false` |

## Fixes Applied

### Пользователи

Evidence entry points moved into the visible primary user cell.

Result:

`users_evidence_visible=true`

### Каналы

Evidence entry points moved into the visible primary channel cell.

Result:

`channels_evidence_visible=true`

### Маршруты

A visible Evidence entry point was added to the existing route overview toolbar.

It opens existing route reality evidence:

`route:reality`

Result:

`routing_evidence_visible=true`

### Логи

A visible Evidence entry point was added to the existing logs toolbar.

Log rows also expose a read-only evidence action for the latest audit evidence.

Result:

`logs_evidence_visible=true`

### Localization

Visible Evidence UI labels were localized:

- `Evidence` -> `Доказательства`
- `Timeline` -> `Хронология`
- `Evidence items` -> `Материалы`
- `Evidence bundles` -> `Пакеты доказательств`

Generated operator-facing Evidence summaries and recommendations were also localized where they appear in drawers.

Result:

`evidence_localization_complete=true`

## Responsive Review

Verified in browser:

| Width | Users | Channels | Routing | Logs |
| --- | --- | --- | --- | --- |
| current admin width | reachable | reachable | reachable | reachable |
| tablet `760px` | reachable | not rechecked individually after users, layout rule covered by same visible cell placement | not rechecked individually after users, layout rule covered by toolbar placement | not rechecked individually after users, layout rule covered by toolbar placement |
| desktop `1280px` | reachable | reachable | reachable | reachable |

Desktop verification counts:

- users: 2 reachable Evidence chips
- channels: 2 reachable Evidence chips
- routing: 1 reachable Evidence chip
- logs: 4 reachable Evidence chips

Result:

`responsive_visibility_fixed=true`

## Re-Verification

Verified after implementation:

- Evidence API list returns HTTP 200.
- Evidence API detail returns HTTP 200.
- `POST /api/evidence` returns HTTP 404.
- Evidence drawer opens from `Пользователи`.
- Evidence drawer opens from `Каналы`.
- Evidence drawer opens from `Маршруты`.
- Evidence drawer opens from `Логи`.
- Evidence drawer opens from `Проверки`.
- Bundle detail renders `Хронология`.
- Bundle detail renders `Материалы`.
- English-first visible labels from the Wave 1 verification blockers were not present in the rechecked Evidence sections.

Screenshots captured:

- `/private/tmp/v7-wave1-1-logs-evidence.png`
- `/private/tmp/v7-wave1-1-evidence-drawer.png`
- `/private/tmp/v7-wave1-1-final-detail.png`
- `/private/tmp/v7-wave1-1-desktop.png`

## Tests

Passed:

- `PYTHONPYCACHEPREFIX=/private/tmp/pycache-wave1-1 python3 -m py_compile admin/v7-admin-api`
- `git diff --check`
- dangerous-call scan on diff
- local backend render
- Evidence API list/detail/read-only check
- browser drawer verification
- responsive visibility check

Dangerous-call scan found no new:

- `v7-user-switch`
- autoswitch apply
- broad routing mutation
- kill-switch mutation
- route mutation command
- Evidence mutation API

## Recommended Next Wave

`WAVE_2_PROPOSAL_SYSTEM_IMPLEMENTATION`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO
