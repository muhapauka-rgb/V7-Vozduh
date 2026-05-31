# V7 Vozduh - Comprehensive Project Documentation

Дата: 2026-05-31.

Статус: актуальный рабочий справочник по проекту V7 Vozduh для операторов, разработчиков и Codex-сессий. Документ описывает текущий продукт, админку, runtime-слой, backend API, storage, governance, safety, Evidence/Proposal/Trust поверхности и основные инструменты репозитория.

Документ не является разрешением на live movement, autoswitch apply, routing mutation, canary/cohort execution или bypass governance. Любое runtime-действие остается под отдельным approval/recheck/rollback процессом.

## 1. Что такое V7

V7 Vozduh - это система управляемого доступа и маршрутизации, а не просто VPN-панель. Нижний транспортный слой может использовать WireGuard, AmneziaWG, VLESS, sing-box, OpenVPN и proxy-inbound сценарии, но продуктовая логика выше: V7 выбирает, проверяет, объясняет и безопасно меняет путь пользователя через каналы.

Главная продуктовая цепочка:

```text
Проблема
-> Доказательства
-> Предложение
-> Runtime Trust
-> Release Trust
-> Governance
-> Execution / Rollback
-> Audit / Closure
```

Основные возможности:

- пользователи и их текущие egress-назначения;
- каналы/egress с ролями, протоколами, capacity, health, speed и service matrix;
- маршруты и route classes для global, video, stable, low-latency, Direct RU и Trusted RU;
- сервисные предпочтения пользователя: YouTube, Instagram, Telegram, Google, Google Auth, ChatGPT, Claude и другие;
- channel suitability и service-aware routing;
- Evidence Bundle как операторское объяснение фактов;
- Proposal System как неавторитетная рекомендация;
- Runtime Trust и Release Trust как доверие к текущему состоянию и релизу;
- guarded mutation paths: preview, dry-run, confirmation, audit, rollback;
- governance lifecycle от 1-user movement до certified 10-user movement;
- production pool architecture tracks: Capacity, Batches, Policy, Concurrency.

## 2. Что V7 не должен делать

V7 не должен:

- silently reroute users;
- silently disable protections;
- выбирать канал только по скорости;
- игнорировать required services пользователя;
- применять autoswitch без governance;
- выполнять cohort movement вне approval packet;
- считать proposal authority;
- считать policy mutation authority;
- скрывать evidence, rollback или audit от оператора;
- показывать raw internals как главный UX, если оператору нужен вывод на человеческом языке.

## 3. Основная карта репозитория

```text
admin/v7-admin-api
```

Монолитный backend + embedded frontend текущей админки `/admin-v2`. Содержит HTTP API, auth/session/CSRF/RBAC, HTML/CSS/JS UI, Evidence/Proposal/Trust stores, runtime readers, guarded action endpoints и интеграцию с runtime tools.

```text
admin_core/
```

Переиспользуемые Python helpers:

- `registry_readers.py` - парсинг registry-файлов;
- `events.py` - JSONL events, severity, user extraction;
- `sanitize.py` - redaction secrets;
- `time.py` - UTC/time helpers;
- `operator_execution.py` - approval packet validation, runtime recheck, replay protection, audit append;
- `operator_observability.py` - evidence archive, audit search, operation lineage, approval preview, execution rehearsal preview.

```text
tools/
```

Repo-side и runtime-adjacent инструменты:

- autoswitch;
- readiness;
- restore-settle;
- route movement preview;
- service matrix;
- runtime/repo diff;
- governance checks;
- observability summary;
- client speed API;
- public gateway.

```text
tools/runtime-support/
```

Runtime support commands для admin actions и диагностики:

- admin auth/password;
- direct/trusted RU;
- proxy/public inbound;
- IPAM;
- backups/rollback;
- smart client profile;
- policy preview/rollback;
- capacity/readiness;
- log maintenance.

```text
tests/
```

Unit/contract tests for parser helpers, operator packets, observability, autoswitch policy, readiness, restore-settle and endpoint inventory.

```text
systemd/
```

Systemd services/timers for autoswitch, egress quality compaction, service matrix refresh, Telegram sentinel, OpenVPN egress templates and draft planner/health units.

```text
docs/track7/productization/
```

Большая productization/governance база: E25-E35, P1, Wave 1-4, capacity/batches/policy/concurrency architecture, audits and implementation reports.

```text
web/src/
```

Documentation skeleton for future frontend modularization: app, api, components, hooks, layouts, pages, stores, styles and status semantics.

## 4. Runtime модель

V7 runtime держит состояние в `/opt/v7`, `/etc/v7`, system networking paths и runtime-support tool outputs.

Ключевые сущности:

- `users.registry` - пользователи, IP, текущий egress, route table, enabled state;
- `egress.registry` - каналы, protocol, interface, role, capacity, autoswitch eligibility, state;
- `v7-state.json` - aggregated runtime state;
- `egress-speed.json` - server-side speed measurements;
- `client-speed.json` / `client-speed-links.json` - client-side speed samples and commands;
- `service matrix` - доступность сервисов на egress/route class;
- `autoswitch-selected-moves.json` - selected moves state;
- `autoswitch-restore-barrier.json` - restore-settle and delayed movement barrier;
- `audit/switch/event logs` - append-only event history;
- evidence/proposal/trust JSONL stores - operator-facing product layer.

Runtime truth всегда сильнее assumptions. Любое approval или execution block должен проверять live registry hashes, target readiness, restore-settle, selected moves, hidden movers and runtime checkers.

## 5. Текущая админка

Админка открывается на:

```text
/admin-v2
```

Backend:

```text
admin/v7-admin-api
```

Существующие top-level разделы, которые нельзя плодить без причины:

- `Главная`;
- `Пользователи`;
- `Каналы`;
- `Маршруты`;
- `Проверки`;
- `Безопасность`;
- `Настройки`;
- `Логи`.

UX принципы:

- спокойный операторский интерфейс;
- низкий шум;
- evidence-first;
- drawer-first;
- progressive disclosure;
- сначала человеческое объяснение, raw internals только в advanced/details;
- существующие паттерны таблиц, drawers, chips, status badges;
- не создавать новую админку и не создавать новые top-level sections для локальных возможностей.

## 6. Разделы админки

### 6.1 Главная

Назначение: executive/operator overview.

Показывает:

- общий runtime status;
- users/channels/routes summaries;
- Evidence chips;
- Proposal cards;
- Runtime Trust;
- Release Trust;
- quick risk/attention signals;
- recent events.

Оператор должен понять:

- работает ли система;
- есть ли проблемы;
- есть ли предложения;
- можно ли доверять runtime/release;
- куда идти за деталями.

### 6.2 Пользователи

Назначение: user-centric operations.

Показывает:

- список пользователей;
- IP, current egress, route table, enabled;
- service preferences / required services;
- route reality;
- traffic summary;
- Evidence entry point;
- Proposal entry point;
- user detail drawer;
- profile delivery and identity surfaces where available.

Важное правило: выбор обязательных сервисов в админке пока является входом в service-aware logic и proposal/suitability слой, но не абсолютной гарантией автоматического live movement без governance. Гарантия возникает только когда service health, suitability, policy, capacity, execution-time recheck и movement governance сходятся.

### 6.3 Каналы

Назначение: egress/channel operations.

Показывает:

- egress registry;
- protocol/interface/role/state;
- speed tests;
- service matrix;
- capacity and limits;
- health/readiness;
- Evidence and Proposal entry points;
- channel details and config export under role gates;
- draft/import/provisioning workflows.

Канал может быть:

- обычным egress;
- execution-only target;
- reserve/manual-only;
- Direct/Trusted RU related path;
- proxy/public candidate.

### 6.4 Маршруты

Назначение: route classes and route behavior.

Показывает:

- route classes;
- Direct RU and Trusted RU state;
- service-aware route preview/apply;
- route reality;
- policy domain classes;
- route movement preview;
- Evidence/Proposal entry points for route objects.

Маршрут не должен быть изменен broad sync без отдельного разрешения. Preview/dry-run surfaces are preferred.

### 6.5 Проверки

Назначение: diagnostics and validation.

Показывает:

- system check;
- route check;
- kill switch;
- direct routing diagnostics;
- stale state check;
- readiness helpers;
- restore-settle helpers;
- service matrix refresh/test;
- Runtime Trust and Release Trust surfaces;
- Evidence/Proposal context.

### 6.6 Безопасность

Назначение: safety, auth, recovery, trust.

Показывает:

- auth/session/RBAC state;
- admin accounts;
- security audit;
- backups and backup download;
- rollback;
- safe mode;
- kill switch status;
- Runtime Trust;
- Release Trust;
- advanced details behind roles.

### 6.7 Настройки

Назначение: operator-controlled policy/config.

Показывает:

- V7 policy;
- autoswitch guarded settings;
- quality floors;
- load/capacity policy;
- service preferences defaults;
- organization/egress policy;
- systemd interval settings;
- direct/trusted route class settings.

Mutating settings require CSRF, role checks, confirmations and audit.

### 6.8 Логи

Назначение: auditability and historical diagnosis.

Показывает:

- audit events;
- switch events;
- normalized events;
- security audit;
- evidence archive/search;
- proposal/trust history;
- closure/freshness/retention signals from Wave 4.

## 7. Admin API карта

### 7.1 Auth and session

- `GET /login` - login page;
- `POST /login` - session creation;
- `POST /logout` - session revoke;
- `GET /api/session` - current session, role, CSRF, access;
- `GET /health` - local health, auth configured flag.

Security model:

- sessions;
- CSRF for mutating actions;
- role levels: viewer/operator/admin style;
- endpoint role mapping;
- safe mode blocks risky actions;
- audit is appended for sensitive operations.

### 7.2 Core read APIs

- `GET /api/overview`;
- `GET /api/state`;
- `GET /api/users`;
- `GET /api/user-detail?ip=...`;
- `GET /api/user-history?ip=...`;
- `GET /api/egress`;
- `GET /api/egress-detail?id=...`;
- `GET /api/egress-config?id=...`;
- `GET /api/traffic/summary`;
- `GET /api/traffic/user?ip=...`;
- `GET /api/traffic/channel?id=...`;
- `GET /api/traffic/live/user?ip=...`;
- `GET /api/traffic/live/channel?id=...`;
- `GET /api/diagnostics`;
- `GET /api/killswitch`;
- `GET /api/direct-routing`;
- `GET /api/events`;
- `GET /api/policy`;
- `GET /api/org-egress-policy`;
- `GET /api/autoswitch-plan`;
- `GET /api/backups`;
- `GET /api/log-maintenance`;
- `GET /api/admin-accounts`;
- `GET /api/security-audit`;
- `GET /api/profile-delivery-status`;
- `GET /api/identity`.

### 7.3 Evidence APIs

- `GET /api/evidence`;
- `GET /api/evidence/{bundle_id}`;
- `GET /api/evidence/by-object/{type}/{id}`.

Evidence is:

- read-only;
- non-authoritative;
- non-executing;
- linkable to User, Channel, Route, Alert, Proposal, Release, Backup, Restore;
- designed for operator explanation.

Typical fields:

- `bundle_id`;
- `object_type`;
- `object_id`;
- `status`;
- `severity`;
- `summary`;
- `timeline`;
- `evidence_items`;
- `recommendation`;
- `verification_state`;
- `closure_state`.

### 7.4 Proposal APIs

- `GET /api/proposals`;
- `GET /api/proposals/{proposal_id}`;
- `GET /api/proposals/by-object/{type}/{id}`.

Proposal is:

- read-only;
- non-authoritative;
- always evidence-linked;
- never a movement command;
- never an autoswitch apply.

Typical fields:

- `proposal_id`;
- `proposal_type`;
- `status`;
- `confidence`;
- `severity`;
- `reason`;
- `affected_users`;
- `current_target`;
- `proposed_target`;
- `required_services`;
- `evidence_bundle_id`;
- `expected_benefit`;
- `rollback_hint`;
- `created_at`.

Proposal types:

- `MOVEMENT_PROPOSAL`;
- `EVACUATION_PROPOSAL`;
- `REBALANCE_PROPOSAL`;
- `OBSERVATION`.

### 7.5 Runtime Trust APIs

- `GET /api/runtime/convergence`;
- `GET /api/runtime/fingerprint`;
- `GET /api/runtime/drift`.

Operator statuses:

- `RUNTIME_OK` - система соответствует ожидаемому состоянию;
- `RUNTIME_WARNING` - требуется внимание;
- `RUNTIME_DRIFT` - обнаружено расхождение;
- `RUNTIME_UNKNOWN` - недостаточно данных;
- `RUNTIME_BLOCKING` - доверие к системе отсутствует.

Runtime Trust is read-only and not authority.

### 7.6 Release Trust APIs

- `GET /api/release/current`;
- `GET /api/release/history`;
- `GET /api/release/{id}`.

Answers:

- current release;
- certification state;
- rollback availability;
- release/runtime match;
- attention required.

Raw hashes/manifests/signatures should stay hidden until advanced view.

### 7.7 Operator governance APIs

- `GET /api/operator/overview`;
- `GET /api/operator/targets`;
- `GET /api/operator/operations`;
- `GET /api/operator/evidence`;
- `GET /api/operator/delayed-movement`;
- `GET /api/operator/approval-preview`;
- `GET /api/operator/approval-contracts`;
- `GET /api/operator/rollback-preview`;
- `GET /api/operator/timeline`;
- `GET /api/operator/lineage`;
- `GET /api/operator/runtime-verdicts`;
- `GET /api/operator/operation-detail`;
- `GET /api/operator/evidence-detail`;
- `GET /api/operator/audit-search`;
- `GET /api/operator/evidence-archive`;
- `GET /api/operator/audit-export-preview`;
- `GET /api/operator/execution-governance-preview`;
- `GET /api/operator/execution-rehearsal-preview`;
- `GET /api/operator/evidence-file-detail`.

These surfaces are preview/read-only by design unless a separate execution packet path is explicitly used.

## 8. Mutating action families

Mutating endpoints live under `/api/actions/...` and must use auth, CSRF, safe-mode constraints where applicable, confirmations and audit.

Important action families:

- backup create/download/verify;
- rollback apply;
- safe mode toggle;
- maintenance cleanup/settings;
- password/admin account operations;
- egress draft create/preflight/runtime/quarantine/pool apply/enable/delete;
- egress speedtest;
- client speed request;
- autoswitch dry-run and guarded apply;
- service preferences update;
- service-aware apply guarded;
- Direct RU and Trusted RU diagnostics/refresh/decision;
- policy systemd apply;
- proxy/public inbound dry-runs, guarded previews, guarded render/apply/rollback;
- smart client profile generation/reissue/rotate/revoke;
- user flow trace.

Hard rule: mutating action exists in API does not mean it is safe to run in a given product block. Product block boundaries override generic endpoint availability.

## 9. Service catalog and route classes

Known service catalog in the current admin backend:

- `google`;
- `google_auth`;
- `youtube`;
- `telegram`;
- `apple`;
- `instagram`;
- `whatsapp`;
- `facebook`;
- `spotify`;
- `soundcloud`;
- `chatgpt`;
- `openai_auth`;
- `claude`;
- `anthropic`.

Default user priority services:

```text
youtube, instagram, telegram, google, google_auth
```

Route classes:

- `GLOBAL_FAST` - Google, Google Auth, Telegram, Facebook, ChatGPT, OpenAI Auth, Claude, Anthropic;
- `GLOBAL_STABLE` - Google, Google Auth, Telegram, Apple, WhatsApp, ChatGPT, OpenAI Auth, Claude, Anthropic;
- `VIDEO_OPTIMIZED` - YouTube, Instagram, Spotify, SoundCloud;
- `LOW_LATENCY` - Google, Google Auth, Telegram;
- `DIRECT_RU` - ordinary Russian domains that should bypass external VPN;
- `TRUSTED_RU_SENSITIVE` - Gosuslugi, ESIA, banks and sensitive Russian services;
- `RESERVE`;
- `MANUAL_ONLY`.

Telegram has special hard/soft states:

- hard: `NOT_STARTED`, `DOWN`;
- soft: `DEGRADED`, `DOWN_GRACE`, `GRACE`.

Required services participate through service preferences, service matrix, route fitness, suitability and proposals. They must not be treated as cosmetic admin checkboxes.

## 10. Channel selection and autoswitch logic

Current selection is not pure speed.

Actual priority model from E35.0.1 audit:

```text
hard eligibility
-> service suitability / route fitness
-> stability and safety
-> capacity/load
-> score and speed preference
-> governance/approval before real movement
```

Quality floors currently exposed in admin policy:

```text
min_avg_mbps = 15.0
min_floor_mbps = 10.0
min_stability = 0.45
```

Switch preference thresholds:

```text
min_score_improvement_pct = 0.2
min_score_delta = 50
```

Important nuance:

- A direct "best channel is x2 faster, therefore switch" hard rule was not found as a single literal policy.
- There is a score-improvement model and quality floor model.
- Speed cannot override hard suitability, unsafe target, capacity conflict, restore barrier, selected moves or hidden movers.
- Required services can influence route fitness and proposal reasoning, but a full autonomous hard-block guarantee for every per-user required service still needs explicit E35 design before autonomous execution.

Speed data sources:

- server-side speed test state;
- client-speed API samples;
- path samples;
- egress quality compact summaries;
- target-local probes during capacity certification.

## 11. Autoswitch policy

Default policy includes:

- cooldown 180s;
- guarded autoswitch mode;
- max planned per run 1;
- max failover per run 25;
- max reconnect per run 10;
- dynamic load mode;
- reserve ratio 0.15;
- hard/soft load multipliers;
- failover capacity multiplier;
- anti-flap user freezes;
- target block/quarantine windows;
- reconnect rotation cooldown.

Autoswitch may plan or propose, but live apply must respect block-specific approvals. In newer governance/product layers, autonomous execution is not considered ready until required services, suitability, capacity, policy, concurrency and approval packet semantics are explicit.

## 12. Governance and certified movement history

Certified capabilities from E25-E31:

- one-user governed execution certified;
- two-user governed execution certified;
- four-user small cohort governed execution certified;
- ten-user governed execution certified.

Proven properties:

- approval packet system;
- execution-time recheck;
- rollback;
- replay rejection;
- restore-settle;
- delayed movement monitoring;
- routing mutation limited to approved candidates;
- execution-only target model;
- governance isolation.

Current strategic direction after E31:

```text
SHIFT_TO_PRODUCTION_POOL_GOVERNANCE
```

Architecture tracks after E32:

- Capacity Classes;
- Execution Batches;
- Policy Engine;
- Concurrency Controls;
- Scheduler/Production Pool future work.

## 13. Capacity program

Capacity classes:

- `CLASS_1`;
- `CLASS_2`;
- `CLASS_4`;
- `CLASS_10`;
- `CLASS_20_CANDIDATE`;
- `CLASS_50_CANDIDATE`;
- `CLASS_100_CANDIDATE`;
- `PRODUCTION_POOL`.

Current certified target:

```text
amneziawg-exec-20260528-10-8-1-14
```

Current certified class:

```text
CLASS_10
```

Runtime capacity rule:

```text
effective_batch_cap = min(certified_capacity, hard_limit, active_policy_cap)
```

Capacity is a forward-execution gate, not authority. Rollback remains allowed under stale/degraded/expired capacity when needed for containment.

## 14. Execution batch architecture

Batch status model:

- `DRAFT`;
- `PRECHECKED`;
- `APPROVED`;
- `SCHEDULED`;
- `EXECUTING`;
- `OBSERVING`;
- `ROLLBACK_READY`;
- `ROLLING_BACK`;
- `COMPLETED`;
- `FAILED_CLOSED`;
- `REPLAY_DENIED`;
- `CANCELLED`;
- `EXPIRED`.

Batch must bind:

- exact users;
- exact target;
- rollback manifest;
- approval packet;
- capacity status;
- policy decision;
- concurrency locks/reservations;
- evidence lineage;
- audit lineage.

Batch failure modes include stale/expired packet, replay attempt, runtime drift, capacity conflict, partial forward, partial rollback, audit inconsistency and unknown rollback scope.

## 15. Policy engine architecture

Policy is:

```text
policy_is_authority = false
policy_is_runtime_mutation = false
policy_is_admission_logic = true
```

Policy can:

- allow;
- deny;
- require review;
- require additional gates.

Policy cannot:

- move users;
- mutate runtime;
- execute proposal;
- bypass governance.

Policy combines with capacity, batch, approval packet, runtime gates and execution-time recheck to form admission, not execution.

## 16. Concurrency architecture

Locks:

- `USER_LOCK`;
- `TARGET_LOCK`;
- `BATCH_LOCK`;
- `PACKET_LOCK`;
- `AUDIT_LOCK`.

Reservations:

- `CAPACITY_RESERVATION`;
- `TARGET_RESERVATION`;
- `BATCH_RESERVATION`.

Lock order:

```text
BATCH_LOCK
-> PACKET_LOCK
-> USER_LOCKS
-> TARGET_LOCK
-> AUDIT_LOCK
```

Concurrency protects from:

- double execution;
- replay race;
- reservation conflicts;
- user/target collisions;
- audit conflicts;
- stale locks/reservations.

## 17. Evidence, Proposal and Trust implementation

Wave 1 implemented:

- Evidence Store;
- Evidence API;
- Evidence UI;
- Evidence Drawer;
- Evidence Timeline;
- Evidence Chips.

Wave 1.1 completed UX native integration:

- visible in users/channels/routes/logs/checks/main;
- localized labels: `Доказательства`, `Хронология`, `Материалы`;
- responsive visibility.

Wave 2 implemented:

- Proposal Store;
- Proposal API;
- Proposal UI;
- Proposal Drawer;
- Proposal Timeline;
- proposal links to evidence.

Wave 3 implemented:

- Runtime Trust Store/API/UI;
- Release Trust Store/API/UI;
- cross-links in operator chain.

Wave 4 implemented:

- search/filtering;
- freshness;
- retention;
- role-gated details;
- closure workflow;
- auditability;
- daily operation hardening.

## 18. Backend function map

### 18.1 `admin_core.registry_readers`

- `parse_kv_line` - parses `key=value` registry row fragments;
- `parse_registry_lines` - parses registry lines while skipping comments/empty lines.

### 18.2 `admin_core.events`

- `parse_jsonl_lines` - robust JSONL event parsing;
- `infer_event_severity` - normalizes severity;
- `extract_user_ip` - extracts user IP from event text.

### 18.3 `admin_core.sanitize`

- `redact` - recursively redacts secrets, private keys, wireguard/json-style secrets and sensitive strings.

### 18.4 `admin_core.time`

- `now_iso`;
- `parse_ts`;
- `age_sec`.

### 18.5 `admin_core.operator_execution`

- `PacketError`;
- `validate_packet`;
- `runtime_recheck`;
- `selected_moves_state`;
- `read_audit_records`;
- `replay_seen`;
- `append_record`;
- `append_runtime_governance_action`;
- `execute_packet`;
- `load_packet`.

These functions implement packet safety, bounded movement checks, replay denial and audit append semantics.

### 18.6 `admin_core.operator_observability`

Important functions:

- file/read helpers: `read_text`, `read_json`, `file_hash`, `file_meta`;
- evidence helpers: `evidence_dir_candidates`, `evidence_refs_for_operation`, `evidence_file_record`, `build_evidence_archive`, `evidence_file_detail`, `evidence_index`;
- operation helpers: `operation_summary_from_report`, `operation_detail`, `operation_history`;
- search/export: `audit_search`, `audit_export_preview`;
- governance previews: `execution_governance_preview`, `execution_rehearsal_preview`, `build_approval_preview`;
- runtime summaries: `selected_move_summary`, `barrier_summary`, `target_pool`, `delayed_movement_summary`, `governance_verdict`;
- public wrappers: `build_operator_view_model`, `build_operator_approval_preview`, `build_operator_lineage_archive`, `build_operator_audit_search`, `build_operator_evidence_archive`.

## 19. Runtime tools reference

### 19.1 Autoswitch and route movement

- `tools/v7-users-autoswitch` - guarded autoswitch planner/apply logic, candidate scoring, cooldowns, safety, load, stability and policy evaluation;
- `tools/v7-route-movement-preview` - read-only movement/route diff preview;
- `tools/v7-autoswitch-safety-review` - safety/freeze/quarantine review;
- `tools/v7-autoswitch-install-systemd` - systemd install helper.

### 19.2 Readiness and restore

- `tools/v7-second-canary-target-readiness` - read-only target readiness checker with quality floors and execution-only validation;
- `tools/v7-restore-settle-gate` - restore-settle gate, selected moves, hidden movement and delayed movement checks;
- `tools/v7-control-plane-governance-check` - broad governance check;
- `tools/v7-runtime-contract-validate` - runtime contract validation.

### 19.3 Service and routing

- `tools/v7-service-matrix-test`;
- `tools/v7-service-matrix-refresh-all`;
- `tools/v7-telegram-sentinel`;
- `tools/v7-path-benchmark`;
- `tools/v7-path-sample-ingest`;
- `tools/v7-path-optimizer-advice`;
- `tools/v7-egress-diagnose`;
- `tools/v7-egress-quality-compact`;
- `tools/v7-egress-lifecycle-validate`.

### 19.4 Observability and release/repo truth

- `tools/v7-observability-summary`;
- `tools/v7-runtime-repo-diff`;
- `tools/v7-runtime-tool-enumerate`;
- `tools/v7-release-lineage-check`;
- `tools/v7-sensitive-state-check`;
- `tools/v7-admin-endpoint-inventory`;
- `tools/v7-admin-platform-review`;
- `tools/v7-admin-ux-review`;
- `tools/v7-intelligence-readiness-review`;
- `tools/v7-identity-consistency-review`;
- `tools/v7-infrastructure-readiness-review`.

### 19.5 Public/client surfaces

- `tools/v7-public-gateway` - public gateway proxy/allowlist;
- `tools/v7-client-speed-api` - client speed measurement page/API, commands, samples and user agent tracking.

### 19.6 Runtime support commands

Representative groups:

- Auth: `v7-admin-auth-init`, `v7-admin-auth-status`, `v7-admin-password-rotate`;
- Audit/logs: `v7-audit-log`, `v7-switch-log`, `v7-log-maintenance-status`;
- Capacity: `v7-capacity-check`, `v7-capacity-readiness`;
- Direct RU: `v7-direct-add-domain`, `v7-direct-auto-sync`, `v7-direct-diagnose-domain`, `v7-direct-list`, `v7-direct-remove-domain`, `v7-direct-status`, `v7-direct-test-domain`;
- Trusted RU: `v7-trusted-ru-decision`, `v7-trusted-ru-diagnostic`, `v7-trusted-ru-refresh-missing`;
- Proxy: `v7-proxy-*` dry-runs, guards, identity, public candidate and route policy tools;
- Profiles: `v7-smart-client-profile-generate`, `v7-user-reissue-config`, `v7-user-rotate-key`;
- IPAM: `v7-ipam-preview`, `v7-ipam-allocate`;
- Maintenance: `v7-maintenance-cleanup-preview`, `v7-secrets-cleanup-preview`, `v7-rollback-last-change`, `v7-safe-run`.

## 20. Data and storage model

Registry-like:

- `users.registry`;
- `egress.registry`;
- route class/domain registries;
- policy registry files.

JSON state:

- overview/runtime state;
- speed and client-speed;
- autoswitch safety;
- selected moves;
- restore barrier;
- service matrix outputs;
- trust/fingerprint/drift/release summaries.

JSONL:

- audit logs;
- switch logs;
- evidence bundles;
- proposal records;
- trust/drift histories where implemented.

SQLite where present/needed:

- traffic summaries;
- identity/profile stores;
- future stores may use SQLite if queryability and lifecycle demand it.

Storage rule: operator-facing product state must be appendable/auditable, linkable by object, searchable enough for daily use and redacted before UI display.

## 21. Security and safety model

Core protections:

- login/session;
- CSRF for POST actions;
- role-gated endpoints;
- safe mode blocked actions;
- no-store cache headers for sensitive downloads;
- safe path resolution for downloads/artifacts;
- secret redaction;
- audit append on admin actions;
- preview/dry-run before apply;
- confirmations for risky operations;
- runtime checks before movement;
- rollback manifest and delayed monitoring after movement.

Mutation safety statement:

```text
Evidence is not authority.
Proposal is not authority.
Policy is not authority.
Capacity is not authority.
Execution requires governance.
Rollback remains containment.
```

## 22. Testing model

Current test families:

- parser helpers;
- event parsing;
- sanitize/redaction;
- time helpers;
- operator execution packet/replay/path traversal;
- operator observability;
- autoswitch policy design;
- users autoswitch policy;
- egress diagnose;
- reconcile check;
- restore-settle gate;
- route movement preview;
- second canary target readiness;
- endpoint inventory contracts.

Common required checks in governance blocks:

- `py_compile`;
- unit/contract tests;
- runtime checkers;
- hidden mover scan;
- readiness helper;
- restore-settle helper;
- credential scan;
- dangerous-call scan;
- `git diff --check`.

## 23. Operator workflows

### 23.1 Diagnose user problem

```text
Пользователи
-> select user
-> Evidence chip/drawer
-> Proposal if exists
-> service preferences
-> route reality
-> traffic and events
```

Expected result: operator sees problem, evidence, suggested next action and whether runtime/release trust is sufficient.

### 23.2 Check channel suitability

```text
Каналы
-> channel detail
-> service matrix
-> speed/quality
-> capacity
-> Evidence
-> Proposal
```

Expected result: operator sees whether channel is healthy for required services and whether it can be used.

### 23.3 Review routing/service behavior

```text
Маршруты
-> route class
-> service-aware preview
-> Direct/Trusted RU diagnostics
-> Evidence/Proposal
```

Expected result: route change is previewed/explained before any guarded apply.

### 23.4 Governed movement

```text
Evidence
-> Proposal
-> approval packet
-> execution-time recheck
-> exact approved users
-> exact target
-> forward movement
-> verification
-> observation
-> rollback
-> delayed monitoring
-> replay denial
-> final report
```

Expected result: movement is bounded, audited and reversible.

### 23.5 Daily closure

```text
Evidence/Proposal/Trust finding
-> verify current state
-> close with reason
-> audit closure
-> retention/freshness visible
```

Expected result: operator is not flooded with stale historical records.

## 24. Current implementation status

Implemented and documented:

- admin `/admin-v2`;
- Evidence Foundation;
- Proposal System;
- Runtime Trust;
- Release Trust;
- Wave 4 hardening;
- service preferences;
- service matrix and route class model;
- governed movement up to 10 users;
- capacity classes and batch/policy/concurrency architecture;
- E35.0/E35.0.1 audits for required services/channel selection.

Still important before autonomous execution:

- formalize exact autonomous channel selection authority;
- convert per-user required services into explicit admission gates;
- define user mode semantics: AUTO / PINNED / MANUAL;
- finish concurrency/scheduler integration in implementation, not only architecture;
- ensure no proposal can become execution without packet/governance;
- make service guarantee language precise in admin UX.

## 25. Glossary

- Evidence Bundle - evidence object explaining facts behind a problem or state.
- Proposal - non-authoritative recommendation linked to evidence.
- Runtime Trust - whether current runtime matches expected trusted state.
- Release Trust - whether current release/provenance/rollback state is trusted.
- Required Services - services selected for a user that must inform suitability and proposals.
- Suitability - whether a channel can serve a user/route/service safely.
- Capacity Class - certified target capacity level.
- Execution Batch - bounded set of users, target, rollback and governance metadata.
- Approval Packet - movement contract bound to runtime hashes and exact scope.
- Execution-time Recheck - final pre-mutation validation.
- Restore-settle - post-restore stability gate.
- Selected Moves - autoswitch-selected movement state; must be zero for many governed actions.
- Hidden Movers - unexpected user/routing movement outside approved scope.
- Replay Denial - old packet cannot be used twice.
- Fail-closed - deny forward movement when evidence/trust/capacity/policy is missing or unsafe.

## 26. Canonical docs to read next

For current product implementation:

- `BLOCK_WAVE_1_EVIDENCE_FOUNDATION_IMPLEMENTATION_REPORT.md`;
- `BLOCK_WAVE_1_1_EVIDENCE_UX_COMPLETION_REPORT.md`;
- `BLOCK_WAVE_2_PROPOSAL_SYSTEM_IMPLEMENTATION_REPORT.md`;
- `BLOCK_WAVE_3_RUNTIME_AND_RELEASE_TRUST_IMPLEMENTATION_REPORT.md`;
- `BLOCK_WAVE_4_PRODUCTION_HARDENING_IMPLEMENTATION_REPORT.md`.

For channel selection and services:

- `docs/track7/productization/e35_0-audit/required-services-audit.md`;
- `docs/track7/productization/e35_0-audit/channel-suitability-audit.md`;
- `docs/track7/productization/e35_0_1-audit/current-priority-chain.md`;
- `docs/track7/productization/e35_0_1-audit/speed-policy-audit.md`;
- `docs/track7/productization/e35_0_1-audit/speed-switching-rules-documentation.md`.

For governance:

- `BLOCK_E31_POST_TEN_USER_GOVERNANCE_REVIEW_REPORT.md`;
- `BLOCK_E32_1_8_CAPACITY_CLASSES_CERTIFICATION_REPORT.md`;
- `BLOCK_E32_2_C_EXECUTION_BATCHES_CERTIFICATION_REPORT.md`;

For old historical baseline:

- `V7_FULL_PROJECT_DOCUMENTATION.md`;
- `V7_PROJECT_DOCUMENTATION.md`;
- `V7_GOVERNANCE.md`;
- `V7_NON_NEGOTIABLES.md`.

## 27. Working rule for future Codex sessions

Before changing code, Codex should map every requested capability through:

```text
Product Capability
-> Admin Surface
-> Runtime Service
-> Storage
-> API
-> UI Component
-> Safety/Governance
-> Tests
```

If any layer is missing, implementation is incomplete.
