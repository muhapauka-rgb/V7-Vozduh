# V7 Vozduh Full Platform Implementation Audit

Дата аудита: 2026-05-22  
Область аудита: локальный репозиторий `/Users/ponch/Documents/New project`  
Тип аудита: статический кодовый аудит + read-only локальные проверки  
Live production verification: не выполнялась

## Executive Verdict

V7 Vozduh сейчас нельзя честно назвать commercial-grade production-ready platform только на основании репозитория.

Правильная классификация:

- **advanced operational prototype**: да.
- **partially production-capable routing control plane**: да, вероятно, если production runtime уже настроен на сервере.
- **production-ready core**: не доказано.
- **commercial-grade multi-tenant platform**: нет.
- **fully implemented Phase 0-8 platform**: нет.
- **document-heavy platform foundation with real legacy/runtime components**: да.

Главная проблема: после Phase 0-8 в репозитории появилось много правильных governance-документов, contracts, review tools и safety models, но значительная часть фаз осталась **architecture/documentation foundation**, а не runtime implementation.

Главная сильная сторона: проект уже содержит реальный runtime control plane: giant admin API, autoswitch planner, service matrix, Telegram sentinel, egress state control, hardening scripts, systemd timers, profile/onboarding logic.

Главный риск: легко перепутать количество документации с фактической готовностью платформы. Документация стала намного сильнее, но production safety не доказана без live verification на сервере.

## Audit Method

Использованные проверки:

- `find . -maxdepth 3 -type f -print | sort`
- `git status --short`
- `git diff --stat`
- `wc -l admin/v7-admin-api tools/* hardening/* systemd/* docs/phase*/*.md V7_*.md web/src/*/*`
- `rg` по TODO/fake/stub/mock/hardcoded/future/default/fallback
- `tools/v7-runtime-contract-validate --allow-missing`
- `tools/v7-egress-lifecycle-validate --allow-missing`
- `tools/v7-identity-consistency-review --allow-missing --pretty`
- `tools/v7-observability-summary --allow-missing --pretty`
- `tools/v7-autoswitch-safety-review --allow-missing --pretty`
- `tools/v7-admin-platform-review`
- `tools/v7-admin-ux-review --pretty`
- `tools/v7-infrastructure-readiness-review --pretty`
- `tools/v7-intelligence-readiness-review --pretty`
- `tools/v7-egress-import-regression`
- `python3 -m py_compile` для admin/review tools

Важно: проверки выполнялись локально. Production paths `/opt/v7`, `/etc/v7`, `/usr/local/bin`, nftables, ip rules, interfaces, systemd units на VPS не проверялись.

## Repository Reality Snapshot

### Большие runtime-файлы

- `admin/v7-admin-api`: 30067 строк.
- `tools/v7-users-autoswitch`: 1546 строк.
- `tools/v7-autoswitch-safety-review`: 562 строки.
- `tools/v7-identity-consistency-review`: 469 строк.
- `tools/v7-egress-import-regression`: 385 строк.
- `tools/v7-observability-summary`: 368 строк.
- `tools/v7-egress-set-state`: 302 строки.
- `tools/v7-intelligence-readiness-review`: 296 строк.
- `tools/v7-runtime-contract-validate`: 277 строк.
- `tools/v7-egress-lifecycle-validate`: 249 строк.

### Dirty worktree status

В репозитории есть незакоммиченные изменения в runtime-critical файлах:

- `admin/v7-admin-api`
- `hardening/v7-killswitch-check`
- `hardening/v7-provisioning-reconcile-check`
- `systemd/v7-users-autoswitch.timer`
- `tools/v7-egress-import-regression`
- `tools/v7-egress-set-state`
- `tools/v7-service-matrix-test`
- `tools/v7-telegram-sentinel`
- `tools/v7-users-autoswitch`

Также есть много untracked Phase docs/tools/web scaffolding. Это значит: baseline не является clean git baseline. Для production-change governance это риск.

### Документация

Документация Phase 0-8 действительно создана:

- `docs/phase0/*`
- `docs/phase1/*`
- `docs/phase2/*`
- `docs/phase3/*`
- `docs/phase4/*`
- `docs/phase5/*`
- `docs/phase6/*`
- `docs/phase6a/*`
- `docs/phase7/*`
- `docs/phase8/*`

Но многие Phase reports прямо говорят: "No routing/nftables/autoswitch/provisioning/systemd/admin behavior was changed". Это честно, но означает: фазы часто были formalization, not implementation.

## Read-Only Verification Results

### Contract validation

`tools/v7-runtime-contract-validate --allow-missing`

Status: `warn`

Missing locally:

- `/opt/v7/egress/state/egress.registry`
- `/opt/v7/egress/state/users.registry`
- `/opt/v7/identity/v7-identity.db`

Interpretation: локально production state отсутствует. Runtime contracts не могут быть признаны verified.

### Egress lifecycle validation

`tools/v7-egress-lifecycle-validate --allow-missing`

Status: `warn`

Missing locally:

- egress registry
- users registry

Interpretation: lifecycle validator exists, but no local runtime proof.

### Identity consistency

`tools/v7-identity-consistency-review --allow-missing --pretty`

Status: `warn`

Findings:

- identity DB `/opt/v7/admin/v7-identity.db` missing locally;
- profile delivery token file missing locally;
- org policy `/etc/v7/org-egress-policy.json` missing locally.

Important mismatch: `v7-runtime-contract-validate` defaults identity DB to `/opt/v7/identity/v7-identity.db`, while admin and identity consistency review default to `/opt/v7/admin/v7-identity.db`.

### Observability summary

`tools/v7-observability-summary --allow-missing --pretty`

Status: `blocked`

Reasons:

- no enabled egress found locally;
- service matrix unavailable;
- path benchmark unavailable;
- trusted/direct RU diagnostics unavailable;
- autoswitch safety state unavailable.

Interpretation: observability tools exist, but local runtime state is absent. Production observability unknown.

### Autoswitch safety review

`tools/v7-autoswitch-safety-review --allow-missing --pretty`

Status: `warn`

Missing locally:

- `/etc/v7/policy.json`
- `autoswitch-safety.json`
- `service-matrix.json`
- org/reconnect/quality state files

The tool explicitly does not execute `v7-users-autoswitch`. Good for safety, not proof of runtime behavior.

### Admin platform review

`tools/v7-admin-platform-review`

Status: `warn`

Findings:

- monolith size: 30067 lines;
- action handlers: 132;
- `ACTION_MIN_ROLE` entries: 132;
- action handlers missing role mapping: 0;
- likely preview/read-only safe-mode exceptions: 43;
- action handlers requiring safe-mode classification review: 3.

Flagged endpoints:

- `/api/actions/egress-draft-clash-create-proxy-draft`
- `/api/actions/egress-draft-endpoint-create-managed-draft`
- `/api/actions/egress-draft-post-enable-validation`

### Admin UX review

`tools/v7-admin-ux-review --pretty`

Status: `warn`

Findings:

- 33 workspace states;
- 8 primary nav tabs;
- 50 render functions;
- 24 table shell references;
- 229 drawer-section references;
- topology token appears 42 times;
- logs can request up to 300 events.

Interpretation: admin tries to be calm, but density risk is real.

### Infrastructure readiness

`tools/v7-infrastructure-readiness-review --pretty`

Status: `warn`

Findings:

- `v7-telegram-sentinel.timer` runs every 4 seconds;
- `v7-egress-quality-compact.timer` lacks RandomizedDelaySec info;
- several systemd services lack explicit hardening directives;
- state files missing locally.

### Intelligence readiness

`tools/v7-intelligence-readiness-review --pretty`

Status: `ok`

But this is mostly a static readiness review. It confirms no black-box intelligence runtime was introduced. It does not prove adaptive routing exists.

### Import regression

`tools/v7-egress-import-regression`

Result: `egress_import_regression_ok`

Important caveat: this regression uses fakes/mocks for matrix/preflight/runtime/network calls. It is useful for parser/API regression, not runtime provisioning proof.

## Cross-Phase Implementation Audit

## PHASE 0 — Freeze / Archive / Baseline / Repository Cleanup

### 1. Implemented

Files and artifacts:

- `V7_NON_NEGOTIABLES.md`
- `V7_GOVERNANCE.md`
- `V7_MASTER_ROADMAP.md`
- `docs/phase0/PHASE0_BASELINE.md`
- `docs/phase0/RUNTIME_INVENTORY.md`
- `docs/phase0/STATE_CONTRACTS.md`
- `docs/phase0/RUNTIME_DEPENDENCIES.md`
- `docs/phase0/RISK_MAP.md`
- `docs/phase0/STABLE_RUNTIME.md`
- `docs/phase0/EXPERIMENTAL_AREAS.md`
- `docs/phase0/LEGACY_MAP.md`
- `docs/phase0/ADMIN_API_SPLIT_PLAN.md`
- `docs/phase0/UI_PHILOSOPHY.md`
- `docs/phase0/ROADMAP_FOUNDATION.md`

Runtime impact:

- Mostly none. This phase created documentation and classification.
- No confirmed runtime behavior change.

### 2. Partially Implemented

- Baseline exists in docs, but git worktree is dirty.
- Repository structure proposal exists, but runtime files are still mostly in old layout.
- Stable/experimental classification exists in docs, not enforced by tooling.
- Legacy was mapped, not archived or isolated in a repo-enforced way.

### 3. Documented Only

- Professional future structure `v7/admin_api`, `web`, `contracts`, `inventory`, `legacy`.
- Archive strategy.
- Module boundaries.
- Future extraction plan.

### 4. Fake / Stub / Mock

- No major fake runtime implementation in Phase 0 itself.
- Risk: documentation can be mistaken for completed cleanup.

### 5. Runtime Verification Status

- Baseline freeze: **PARTIALLY VERIFIED**.
- Runtime inventory: **PARTIALLY VERIFIED**.
- State contracts: **PARTIALLY VERIFIED**.
- Repository cleanup: **NOT FULLY VERIFIED**.

### 6. Governance Violations

- Dirty worktree contradicts the spirit of a stable baseline.
- No machine-enforced contract preventing unsafe edits to runtime-critical areas.

### 7. Technical Debt

- `admin/v7-admin-api` remains a giant monolith.
- Host-specific paths `/opt/v7`, `/etc/v7`, `/usr/local/bin` remain scattered.
- Runtime dependencies remain partially external and not packaged as one deployable contract.

### 8. UI/UX Audit

- UI philosophy documented.
- No actual UI simplification guaranteed in Phase 0.

### 9. Safety Audit

- Safe as documentation phase.
- Does not prove datapath safety.

### 10. Must Be Fixed Before Production

- Establish clean git baseline.
- Make runtime inventory executable/verifiable against VPS.
- Align identity DB path contract.

### 11. Should Be Refactored

- Repository layout needs gradual migration, but not before compatibility tests.

### 12. Should Not Be Touched

- Production routing files and hardening scripts should not be moved until path compatibility is proven.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 75% |
| Runtime completeness | 20% |
| Production readiness | 30% |
| Observability maturity | 40% |
| Operator UX maturity | 45% |
| Safety maturity | 45% |

Phase 0 is useful, but mostly documentary.

## PHASE 1 — Core Routing & Safety Stabilization

### 1. Implemented

Docs:

- `docs/phase1/ROUTING_STATE_MODEL.md`
- `docs/phase1/RECONCILIATION_PLAN.md`
- `docs/phase1/KILL_SWITCH_HARDENING.md`
- `docs/phase1/ROUTE_VERIFICATION.md`
- `docs/phase1/ROUTE_CLASSES.md`
- `docs/phase1/DIRECT_RU_SAFETY_MODEL.md`
- `docs/phase1/HEALTH_MODEL.md`
- `docs/phase1/RUNTIME_CRITICAL_TESTS.md`
- `docs/phase1/OPERATOR_VISIBILITY_FOUNDATION.md`
- `docs/phase1/STATE_CONTRACT_VALIDATION.md`
- `docs/phase1/AUDITABILITY.md`
- `docs/phase1/PHASE1_REPORT.md`

Tools and scripts:

- `tools/v7-runtime-contract-validate`
- `hardening/v7-killswitch-check`
- `hardening/v7-killswitch-enable`
- `hardening/v7-provisioning-reconcile-check`
- `hardening/v7-direct-*`
- `hardening/v7-path-guard-repair`

Runtime impact:

- There are real checks and hardening scripts.
- Actual production no-leak behavior was not verified in this audit.

### 2. Partially Implemented

- Routing state model is formalized in docs, not implemented as a single authoritative runtime engine.
- Reconciliation exists as checks, but full self-healing repair layer is limited.
- Route classes are documented and referenced by autoswitch/service matrix, but not proven as authoritative across all routing decisions.
- Kill switch scripts exist, but live nftables/ip-rule verification is not included here.

### 3. Documented Only

- Desired/observed/runtime/effective state hierarchy.
- Complete mismatch taxonomy.
- Full route verification system.
- Unified repair strategy.

### 4. Fake / Stub / Mock

- No obvious fake kill switch implementation found.
- But local contract validation with `--allow-missing` can produce non-fatal results even when state is missing. This is safe for audit, but not proof.

### 5. Runtime Verification Status

- Routing: **UNKNOWN**.
- Kill switch: **NOT VERIFIED LIVE**.
- Direct/RU: **UNKNOWN**.
- Trusted RU: **UNKNOWN**.
- Reconciliation: **PARTIALLY VERIFIED STATICALLY**.
- State contracts: **PARTIALLY VERIFIED STATICALLY**.

### 6. Governance Violations

- Governance requires no silent leaks. This cannot be claimed without live `nft`, `ip rule`, routing table and interface verification.
- Runtime/UI state divergence remains possible because local state and live runtime were not reconciled.

### 7. Technical Debt

- Shell-based hardening and repair scripts rely on external commands.
- Some repair actions call tools that are not in this repo or not proven installed:
  - `v7-routing-sync`
  - `v7-direct-auto-sync`
  - `v7-mss-clamp-enable`
  - `v7-sing-box-tun-mtu-set`
  - `v7-audit-log`

### 8. UI/UX Audit

- Operator visibility foundation exists conceptually.
- Admin still contains dense diagnostics and many direct runtime probes.

### 9. Safety Audit

Critical unknowns:

- no-leak guarantee for `10.0.0.0/24` and `10.7.0.0/22`;
- direct-mark isolation;
- table 70 correctness;
- trusted RU unsafe fallback prevention.

### 10. Must Be Fixed Before Production

- Run live no-leak tests.
- Run `v7-killswitch-check` on production and capture evidence.
- Verify `ip rule`, route tables, nft chains, NAT, DNS path, direct route isolation.
- Make route class enforcement observable in one source of truth.

### 11. Should Be Refactored

- Reconciliation should become a bounded service/tool with explicit mismatch classes and audit output.

### 12. Should Not Be Touched

- `hardening/v7-killswitch-enable`
- `hardening/v7-killswitch-check`
- direct/RU hardening scripts
- existing policy/routing scripts on production

These are safety-critical and should only change with live verification and rollback.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 70% |
| Runtime completeness | 35% |
| Production readiness | 25% |
| Observability maturity | 45% |
| Operator UX maturity | 35% |
| Safety maturity | 55% |

Phase 1 has real safety tooling, but live datapath safety is unproven.

## PHASE 2 — Provisioning & Egress Lifecycle

### 1. Implemented

Docs:

- `docs/phase2/EGRESS_LIFECYCLE.md`
- `docs/phase2/DRIVER_MODEL.md`
- `docs/phase2/IMPORT_PIPELINE.md`
- `docs/phase2/QUARANTINE_MODEL.md`
- `docs/phase2/RUNTIME_ENABLE_GATES.md`
- `docs/phase2/MAINTENANCE_DRAIN_MODE.md`
- `docs/phase2/ROLLBACK_RECOVERY.md`
- `docs/phase2/RUNTIME_DEPENDENCY_SAFETY.md`
- `docs/phase2/REGISTRY_RUNTIME_RECONCILIATION.md`
- `docs/phase2/SAFE_STATE_PERSISTENCE.md`
- `docs/phase2/PROVISIONING_AUDITABILITY.md`
- `docs/phase2/PHASE2_REPORT.md`

Tools/runtime:

- `tools/v7-egress-lifecycle-validate`
- `tools/v7-egress-set-state`
- `tools/v7-egress-import-regression`
- provisioning/import/action code inside `admin/v7-admin-api`

Runtime impact:

- `v7-egress-set-state` is real and can mutate runtime with `--apply`.
- It backs up registry/flags and can start/stop OpenVPN runtime/systemd.
- It can call `v7-killswitch-enable` and `v7-egress-guard`.

### 2. Partially Implemented

- Formal lifecycle exists, but not all states are guaranteed enforced as one state machine.
- Driver architecture is mostly a contract, not a modular driver runtime.
- Quarantine is recognized by autoswitch and docs, but end-to-end enable gating is not live-verified.
- Rollback exists as backups and some admin actions, not proven as full runtime restore.

### 3. Documented Only

- Unified driver model for WireGuard/AWG/OpenVPN/VLESS/Hysteria2/TUIC/SOCKS/Shadowsocks.
- Full import pipeline stages.
- Full rollback/recovery model.
- Runtime enable gates as universal enforcement.

### 4. Fake / Stub / Mock

- `tools/v7-egress-import-regression` uses fakes:
  - fake matrix curl;
  - fake preflight;
  - fake runtime;
  - fake urlopen.

This is acceptable for unit/regression testing, but it is not runtime provisioning verification.

### 5. Runtime Verification Status

- Provisioning: **PARTIALLY VERIFIED**.
- Quarantine: **PARTIALLY VERIFIED STATICALLY**.
- Rollback: **NOT VERIFIED END-TO-END**.
- Driver lifecycle: **DOCUMENTED ONLY / PARTIAL**.
- Runtime dependency safety: **PARTIALLY VERIFIED STATICALLY**.

### 6. Governance Violations

- Unknown whether all admin provisioning paths prevent unsafe production enable.
- Three admin action endpoints need safe-mode classification review:
  - clash proxy draft;
  - endpoint managed draft;
  - post-enable validation.

### 7. Technical Debt

- Provisioning remains coupled to `admin/v7-admin-api`.
- Protocol-specific behavior is not cleanly modularized.
- External commands and production file paths are assumed.
- OpenVPN runtime handling is more concrete than other transport driver handling.

### 8. UI/UX Audit

- Operator workflow docs exist.
- Admin UI likely contains many provisioning controls in the monolith, increasing cognitive load.

### 9. Safety Audit

Risks:

- orphan interfaces;
- stale nftables/routes;
- registry says enabled while runtime dead;
- runtime alive while registry disabled;
- missing proof that quarantine always excludes autoswitch and route class eligibility.

### 10. Must Be Fixed Before Production

- Live test lifecycle for one new egress:
  - import;
  - draft;
  - quarantine;
  - runtime test;
  - enable proposal;
  - enable;
  - rollback;
  - disable;
  - stale cleanup.
- Prove no users move to unverified egress.

### 11. Should Be Refactored

- Extract driver contracts gradually from admin monolith.
- Keep current provisioning behavior stable until tests exist.

### 12. Should Not Be Touched

- Existing working import/provisioning paths in `admin/v7-admin-api`.
- `tools/v7-egress-set-state` without staging tests.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 75% |
| Runtime completeness | 45% |
| Production readiness | 35% |
| Observability maturity | 45% |
| Operator UX maturity | 45% |
| Safety maturity | 55% |

Phase 2 has real pieces, but driver/lifecycle architecture is not fully runtime-enforced.

## PHASE 3 — Observability & Diagnostics

### 1. Implemented

Docs:

- `docs/phase3/UNIFIED_HEALTH_MODEL.md`
- `docs/phase3/SERVICE_MATRIX_MATURITY.md`
- `docs/phase3/ROUTE_DIAGNOSTICS_ENGINE.md`
- `docs/phase3/INCIDENT_TIMELINE_MODEL.md`
- `docs/phase3/CLIENT_PATH_AWARENESS.md`
- `docs/phase3/DATAPATH_VISIBILITY.md`
- `docs/phase3/AUTOSWITCH_EXPLAINABILITY.md`
- `docs/phase3/TRUSTED_RU_OBSERVABILITY.md`
- `docs/phase3/COMPACT_OPERATOR_UX.md`
- `docs/phase3/ALERT_AND_HISTORY_MODEL.md`
- `docs/phase3/OBSERVABILITY_SUMMARY_TOOL.md`
- `docs/phase3/PHASE3_REPORT.md`

Tools/runtime:

- `tools/v7-observability-summary`
- `tools/v7-service-matrix-test`
- `tools/v7-service-matrix-refresh-all`
- `tools/v7-telegram-sentinel`
- `tools/v7-egress-quality-compact`
- `tools/v7-path-benchmark`
- `tools/v7-path-sample-ingest`
- `tools/v7-client-speed-api`
- admin diagnostics endpoints and overview cache

Systemd:

- `systemd/v7-service-matrix-refresh.service`
- `systemd/v7-service-matrix-refresh.timer`
- `systemd/v7-telegram-sentinel.service`
- `systemd/v7-telegram-sentinel.timer`
- `systemd/v7-egress-quality-compact.service`
- `systemd/v7-egress-quality-compact.timer`

### 2. Partially Implemented

- Service matrix exists but maturity is limited: Telegram/HTTP/TCP checks exist; "usable service quality" is not fully proven.
- Incident timeline exists in pieces via events and summaries, not as one mature event model.
- Client path awareness exists via speed/path sample tools, but bounded telemetry integration is partial.
- Observability summary can compress state, but depends on runtime state files missing locally.

### 3. Documented Only

- Full route diagnostics engine able to answer every "why".
- Unified event model with correlation id across all subsystems.
- Historical quality model as mature bounded summaries.
- AI-ready observability foundation.

### 4. Fake / Stub / Mock

- Local observability reports `blocked` because state is missing. That is not a fake, but it proves local state is absent.
- Some service matrix checks can degrade to basic reachability rather than true user experience.

### 5. Runtime Verification Status

- Observability: **PARTIALLY VERIFIED STATICALLY**.
- Diagnostics: **PARTIALLY VERIFIED**.
- Service matrix: **NOT VERIFIED LIVE**.
- Telegram sentinel: **NOT VERIFIED LIVE**.
- Client path telemetry: **UNKNOWN**.
- Incident model: **PARTIAL**.

### 6. Governance Violations

- Telegram sentinel can trigger autoswitch with `--apply`. This is no longer purely observability.
- `v7-telegram-sentinel.timer` every 4 seconds risks high-noise/high-load behavior as egress count grows.

### 7. Technical Debt

- Observability state is spread across many JSON files.
- Timers/probes may grow linearly with egress count.
- Some systemd services lack hardening directives.

### 8. UI/UX Audit

- Admin review reports density risks:
  - 33 workspace states;
  - 50 render functions;
  - logs up to 300 events;
  - topology references.
- This can violate calm UX if not compressed.

### 9. Safety Audit

Observability should not mutate datapath. But Telegram sentinel can call autoswitch apply:

`v7-users-autoswitch --mode guarded --apply --service telegram --route-class GLOBAL_STABLE --pretty`

This must be treated as control-plane action, not passive monitoring.

### 10. Must Be Fixed Before Production

- Separate passive sentinel from autoswitch trigger or prove bounded behavior live.
- Add rate/capacity model for probes.
- Prove service matrix does not produce false confidence.

### 11. Should Be Refactored

- Consolidate event model.
- Group diagnostics by incident/channel/user rather than raw metrics.

### 12. Should Not Be Touched

- Existing observability scripts should not be aggressively rewritten until live expected outputs are captured.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 70% |
| Runtime completeness | 45% |
| Production readiness | 35% |
| Observability maturity | 60% |
| Operator UX maturity | 45% |
| Safety maturity | 45% |

Phase 3 has real observability tools, but live signal quality and UI calmness are not proven.

## PHASE 4 — Autoswitch Intelligence & Self-Healing

### 1. Implemented

Docs:

- `docs/phase4/AUTOSWITCH_DECISION_MODEL.md`
- `docs/phase4/ANTI_FLAPPING_MODEL.md`
- `docs/phase4/ANTI_FLAPPING_SYSTEM.md`
- `docs/phase4/DEGRADATION_PERSISTENCE.md`
- `docs/phase4/SERVICE_ROUTE_CLASS_SWITCHING.md`
- `docs/phase4/CONFIDENCE_AND_BOUNDED_MIGRATION.md`
- `docs/phase4/GRACEFUL_RECOVERY_MODEL.md`
- `docs/phase4/SELF_HEALING_REPAIR_HOOKS.md`
- `docs/phase4/HISTORICAL_RELIABILITY_SCORING.md`
- `docs/phase4/AUTOSWITCH_SAFETY_AUDIT.md`
- `docs/phase4/COMPACT_AUTOSWITCH_UX.md`
- `docs/phase4/ADAPTIVE_STEALTH_FOUNDATION.md`
- `docs/phase4/FUTURE_INTELLIGENCE_FOUNDATION.md`
- `docs/phase4/PHASE4_REPORT.md`

Runtime:

- `tools/v7-users-autoswitch`
- `tools/v7-autoswitch-safety-review`
- `systemd/v7-users-autoswitch.service`
- `systemd/v7-users-autoswitch.timer`
- Telegram sentinel autoswitch hook
- admin autoswitch dry-run/apply endpoints

Actual autoswitch implementation contains:

- guarded mode defaults;
- cooldown;
- max planned/failover/reconnect moves;
- quality policy;
- load policy;
- reconnect policy;
- safety policy;
- route-class/service gates;
- org policy gates;
- quarantine/maintenance/disabled/manual-only exclusion;
- score improvement threshold;
- post-switch verification via `v7-user-route-check`;
- rollback attempt via `v7-user-switch` on verification failure;
- event/audit-oriented safety state.

### 2. Partially Implemented

- Confidence scoring exists as deterministic scoring/gates, but "confidence" is not necessarily a mature explicit model everywhere.
- Self-healing repair hooks are limited; autoswitch mostly moves users, not a full repair engine.
- Historical reliability exists via quality/safety/reconnect files, but live history maturity unknown.
- Regional/operator awareness is foundation only.

### 3. Documented Only

- Full adaptive stealth behavior.
- Future predictive route forecasting.
- Mature client experience awareness.
- Operator-specific regional degradation models.

### 4. Fake / Stub / Mock

- No fake autoswitch planner found; `tools/v7-users-autoswitch` is real.
- But autoswitch depends on external commands not in repo:
  - `v7-user-switch`
  - `v7-user-route-check`
- If those are missing or behave unexpectedly on production, autoswitch safety collapses.

### 5. Runtime Verification Status

- Autoswitch dry-run: **NOT RUN IN THIS AUDIT** because it may write reconnect observation state.
- Autoswitch apply: **NOT VERIFIED**.
- Anti-flapping: **PARTIALLY VERIFIED BY CODE INSPECTION**.
- Bounded migration: **PARTIALLY VERIFIED BY CODE INSPECTION**.
- Rollback after failed verification: **PARTIALLY VERIFIED BY CODE INSPECTION**.

### 6. Governance Violations

Potential violation, not proven:

- `systemd/v7-users-autoswitch.service` runs `/usr/local/bin/v7-users-autoswitch --apply`.
- Telegram sentinel can also run autoswitch `--apply`.

This can comply with governance only if policy/cooldown/safety state is correct in production. Without live verification, it is a governance risk.

### 7. Technical Debt

- Autoswitch is a single 1546-line script.
- Planner mixes state loading, scoring, gating, move selection, external command execution, verification, rollback.
- External command contracts are implicit.
- Some dry-run state writes are acknowledged by safety review.

### 8. UI/UX Audit

- Admin has autoswitch UI/endpoints.
- Risk: scoring/gates can become too complex for operator without grouped explanation.

### 9. Safety Audit

Key risks:

- moving users based on stale/missing service matrix;
- verification command missing or weak;
- rollback command failing;
- sentinel-triggered apply too frequent;
- policy missing causing defaults to enable autoswitch.

Default policy in `v7-users-autoswitch` has `autoswitch_enabled: True` and `autoswitch_mode: guarded`. That is reasonable but dangerous if production policy file is missing and defaults are used unintentionally.

### 10. Must Be Fixed Before Production

- Verify production policy file exists and disables/enables exact intended behavior.
- Prove cooldown and max move limits under systemd timer.
- Run dry-run and apply in staging with controlled users.
- Verify `v7-user-switch` and `v7-user-route-check` contracts.
- Decide whether Telegram sentinel is allowed to call `--apply`.

### 11. Should Be Refactored

- Split autoswitch into planner, state reader, scorer, safety ledger, executor.
- Keep CLI behavior backward compatible.

### 12. Should Not Be Touched

- `tools/v7-users-autoswitch` apply logic without staging.
- `systemd/v7-users-autoswitch.*` in production.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 75% |
| Runtime completeness | 55% |
| Production readiness | 40% |
| Observability maturity | 55% |
| Operator UX maturity | 50% |
| Safety maturity | 60% |

Phase 4 is one of the most real phases. It is also one of the riskiest.

## PHASE 5 — Identity, Users & Multi-Tenant

### 1. Implemented

Docs:

- `docs/phase5/MULTITENANT_MODEL.md`
- `docs/phase5/ORGANIZATION_ISOLATION.md`
- `docs/phase5/USER_LIFECYCLE.md`
- `docs/phase5/DEVICE_LIFECYCLE.md`
- `docs/phase5/PROFILE_DELIVERY_MODEL.md`
- `docs/phase5/ONBOARDING_RECOVERY_UX.md`
- `docs/phase5/POLICY_BASED_ACCESS.md`
- `docs/phase5/SAFE_USER_OPERATIONS.md`
- `docs/phase5/DEVICE_TRUST_FOUNDATION.md`
- `docs/phase5/OPERATOR_IDENTITY_UX.md`
- `docs/phase5/USER_READINESS_MODEL.md`
- `docs/phase5/COMMERCIAL_ENTERPRISE_FOUNDATION.md`
- `docs/phase5/IDENTITY_RUNTIME_CONSISTENCY.md`
- `docs/phase5/PHASE5_REPORT.md`

Runtime/admin:

- SQLite identity DB logic inside `admin/v7-admin-api`.
- `/connect` onboarding surface.
- public gateway allowlist in `tools/v7-public-gateway`.
- identity consistency review tool.
- profile delivery token concepts and admin logic.
- org policy file referenced by admin/autoswitch.

### 2. Partially Implemented

- Organizations/groups/users/devices exist in admin DB logic, but live DB missing locally.
- Multi-tenant isolation is not proven under production data.
- Org policy is referenced but local policy file missing.
- Commercial hooks exist; billing/subscription not implemented.
- Device trust is foundation only.

### 3. Documented Only

- Full enterprise lifecycle.
- SSO/delegated admins.
- Commercial readiness.
- Managed deployments.
- Formal org diagnostics visibility.

### 4. Fake / Stub / Mock

- No obvious fake identity DB runtime found.
- But local identity verification is impossible because DB is missing.
- Profile delivery maturity cannot be proven without live token files.

### 5. Runtime Verification Status

- Onboarding: **UNKNOWN**.
- Identity DB: **NOT VERIFIED LOCALLY**.
- Org isolation: **NOT VERIFIED**.
- Device lifecycle: **PARTIALLY IMPLEMENTED / NOT VERIFIED**.
- Profile delivery: **PARTIALLY IMPLEMENTED / NOT VERIFIED**.

### 6. Governance Violations

- Identity DB path mismatch is a governance issue:
  - admin: `/opt/v7/admin/v7-identity.db`;
  - runtime validator: `/opt/v7/identity/v7-identity.db`.

This can lead to false validation or wrong migration if not fixed carefully.

### 7. Technical Debt

- Identity logic is embedded in admin monolith.
- Runtime registry and SQLite DB can diverge.
- Multi-tenant boundaries are not backed by a dedicated service/module.

### 8. UI/UX Audit

- Risk of giant user tables and identity overload.
- Docs emphasize grouped identity UX, but real admin remains monolithic and dense.

### 9. Safety Audit

Risks:

- revoked-but-active profiles;
- stale devices;
- orphan users in registry;
- org policy not applied to autoswitch/provisioning consistently;
- profile delivery token leakage if not verified.

### 10. Must Be Fixed Before Production

- Align identity DB path contract.
- Run identity consistency review against live DB.
- Verify revoked devices cannot remain active.
- Verify org policies constrain routing and visibility.

### 11. Should Be Refactored

- Extract identity DB access and lifecycle transitions from admin monolith.
- Add explicit migration/versioning for identity schema.

### 12. Should Not Be Touched

- Live identity DB and profile token files without backup/migration.
- Existing onboarding/profile delivery code without compatibility tests.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 65% |
| Runtime completeness | 35% |
| Production readiness | 25% |
| Observability maturity | 35% |
| Operator UX maturity | 45% |
| Safety maturity | 45% |

Phase 5 has real foundation, but commercial multi-tenant readiness is not proven.

## PHASE 6 — New Admin Platform & Operator Experience

### 1. Implemented

Docs:

- `docs/phase6/ADMIN_PLATFORM_ARCHITECTURE.md`
- `docs/phase6/BACKEND_MODULE_BOUNDARIES.md`
- `docs/phase6/FRONTEND_ARCHITECTURE.md`
- `docs/phase6/CALM_OPERATOR_UX.md`
- `docs/phase6/OVERVIEW_FIRST_UX.md`
- `docs/phase6/WORKFLOW_NAVIGATION.md`
- `docs/phase6/PROGRESSIVE_DISCLOSURE.md`
- `docs/phase6/SAFE_ACTION_UX.md`
- `docs/phase6/DIAGNOSTICS_INCIDENT_UX.md`
- `docs/phase6/ROUTING_VISUALIZATION.md`
- `docs/phase6/OPERATOR_USER_UX_SEPARATION.md`
- `docs/phase6/MOBILE_OPERATOR_UX.md`
- `docs/phase6/DESIGN_SYSTEM_FOUNDATION.md`
- `docs/phase6/LEGACY_MIGRATION_STRATEGY.md`
- `docs/phase6/PERFORMANCE_SCALABILITY_UX.md`
- `docs/phase6/FUTURE_OPERATOR_FOUNDATION.md`
- `docs/phase6/PHASE6_REPORT.md`

Runtime/admin:

- Existing `/admin-v2` embedded UI in `admin/v7-admin-api`.
- RBAC maps:
  - `ACTION_MIN_ROLE`;
  - `GET_MIN_ROLE`.
- safe-mode blocked action set.
- CSRF checks and confirm tokens.
- `tools/v7-admin-platform-review`.

Frontend scaffold:

- `web/src/app/README.md`
- `web/src/pages/README.md`
- `web/src/components/README.md`
- `web/src/layouts/README.md`
- `web/src/api/README.md`
- `web/src/hooks/README.md`
- `web/src/stores/README.md`
- `web/src/styles/README.md`
- `web/src/styles/status-semantics.css`
- `web/src/app/information-architecture.json`
- `web/src/components/OPERATOR_BLOCK_CONTRACT.md`

### 2. Partially Implemented

- Admin platform is not split. Backend, API, HTML, CSS, JS remain in `admin/v7-admin-api`.
- Web scaffold is not wired into runtime.
- Frontend architecture exists as docs/README/scaffold only.
- Design system exists as CSS semantics and docs, not as implemented component library.

### 3. Documented Only

- Modular backend packages.
- Modular frontend application.
- Safe migration strategy.
- Mobile operator UX beyond existing embedded UI.

### 4. Fake / Stub / Mock

- `web/` is a scaffold, not a working admin platform.
- Design HTML files in `design/` are prototypes/artifacts, not production UI.
- Hardcoded example in admin:
  - `vless://uuid@example.com:443?...#v7-egress`

### 5. Runtime Verification Status

- Existing admin monolith: **PARTIALLY VERIFIED STATICALLY**.
- New web frontend: **NOT IMPLEMENTED / NOT VERIFIED**.
- RBAC action mapping: **STATICALLY VERIFIED**.
- Safe mode: **PARTIALLY VERIFIED STATICALLY**.

### 6. Governance Violations

- Giant monolith violates modularization direction.
- 30k-line file increases hidden coupling and operator platform risk.
- UI density may violate calm operator UX.

### 7. Technical Debt

- `admin/v7-admin-api` is the biggest technical debt in the repo.
- 132 action handlers in one file.
- 50 render functions in one file.
- Embedded JS/CSS/HTML coupled to backend state.
- Many external commands called directly from admin actions.

### 8. UI/UX Audit

Risks:

- 8 primary tabs;
- 33 workspace states;
- logs up to 300 events;
- topology references;
- many drawers;
- large tables.

The UI likely tries to be calm, but structural density is high.

### 9. Safety Audit

Risks:

- admin can trigger dangerous runtime actions;
- safe-mode classification gaps;
- viewer role for post-enable validation endpoint needs review;
- direct action shell coupling.

### 10. Must Be Fixed Before Production

- Review flagged safe-mode endpoints.
- Add regression coverage for critical admin actions.
- Decide admin modularization cut points.
- Do not pretend `web/` is production.

### 11. Should Be Refactored

Extraction order:

1. pure state readers;
2. audit/event helpers;
3. identity DB helpers;
4. provisioning adapters;
5. autoswitch API wrappers;
6. frontend components.

### 12. Should Not Be Touched

- Admin action endpoint names and JSON shapes until clients/tests exist.
- Existing `/admin-v2` runtime until replacement is working.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 55% |
| Runtime completeness | 45% |
| Production readiness | 35% |
| Observability maturity | 45% |
| Operator UX maturity | 55% |
| Safety maturity | 45% |

Phase 6 is mostly migration foundation. The monolith remains.

## PHASE 6A — Minimal Operator UX Integration

### 1. Implemented

Docs:

- `docs/phase6a/INFORMATION_HIERARCHY.md`
- `docs/phase6a/PROGRESSIVE_DISCLOSURE_ARCHITECTURE.md`
- `docs/phase6a/SUMMARY_FIRST_UX.md`
- `docs/phase6a/GROUPED_DIAGNOSTICS_MODEL.md`
- `docs/phase6a/INCIDENT_CENTRIC_INTERFACE.md`
- `docs/phase6a/VISUAL_NOISE_REDUCTION.md`
- `docs/phase6a/DRILLDOWN_AND_CONTEXTUAL_DETAILS.md`
- `docs/phase6a/ROUTING_VISUALIZATION_SIMPLICITY.md`
- `docs/phase6a/STATUS_SEMANTICS.md`
- `docs/phase6a/FUTURE_COMPLEXITY_PROTECTION.md`
- `docs/phase6a/PHASE6A_REPORT.md`

Scaffold:

- `web/src/app/information-architecture.json`
- `web/src/styles/status-semantics.css`
- `web/src/components/OPERATOR_BLOCK_CONTRACT.md`

Tool:

- `tools/v7-admin-ux-review`

### 2. Partially Implemented

- Information architecture exists as docs/scaffold, not active UI.
- Existing admin may already have overview/drawers, but Phase 6A did not refactor it.
- UX review reports density risks, not resolved issues.

### 3. Documented Only

- Full layered diagnostics UX.
- Summary-first enforcement.
- Future feature IA review gate.

### 4. Fake / Stub / Mock

- `web/src` is non-production scaffold.
- No functional Phase 6A UI app exists.

### 5. Runtime Verification Status

- UX readability: **STATICALLY REVIEWED ONLY**.
- Actual browser/UI verification: **NOT PERFORMED IN THIS AUDIT**.
- New UI runtime: **NOT IMPLEMENTED**.

### 6. Governance Violations

- Existing admin density remains a risk against Calm Operator UX.
- No enforced IA review gate exists for future features.

### 7. Technical Debt

- UX rules live in docs, not component constraints.
- Admin monolith can continue to accumulate UI complexity.

### 8. UI/UX Audit

Primary risks:

- too many tabs/workspaces;
- too many raw diagnostics exposed;
- logs and topology can become engineering cockpit;
- giant table growth possible.

### 9. Safety Audit

UI can accidentally encourage unsafe actions if it shows action buttons before impact/rollback context.

### 10. Must Be Fixed Before Production

- Define a live overview screen acceptance test.
- Cap or group logs/diagnostics.
- Ensure dangerous actions always show impact and rollback.

### 11. Should Be Refactored

- Move UI toward reusable summary/drilldown blocks.

### 12. Should Not Be Touched

- Existing operational admin UX should not be replaced until new UI proves compatibility.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 70% |
| Runtime completeness | 10% |
| Production readiness | 20% |
| Observability maturity | 50% |
| Operator UX maturity | 65% |
| Safety maturity | 35% |

Phase 6A is useful IA work, but not runtime UI implementation.

## PHASE 7 — Scaling, Reliability & Infrastructure Maturity

### 1. Implemented

Docs:

- `docs/phase7/INFRASTRUCTURE_MATURITY_MODEL.md`
- `docs/phase7/MULTI_EGRESS_SCALING.md`
- `docs/phase7/CAPACITY_AND_RESOURCE_MODEL.md`
- `docs/phase7/RUNTIME_PERSISTENCE_MODEL.md`
- `docs/phase7/BACKUP_RESTORE_MATURITY.md`
- `docs/phase7/UPGRADE_SAFETY.md`
- `docs/phase7/FAILURE_DOMAIN_ISOLATION.md`
- `docs/phase7/GRACEFUL_DEGRADATION.md`
- `docs/phase7/RUNTIME_SELF_HEALING_MATURITY.md`
- `docs/phase7/LARGE_SCALE_OPERATOR_UX.md`
- `docs/phase7/MULTI_REGION_AND_ENDPOINT_FOUNDATION.md`
- `docs/phase7/DISASTER_RECOVERY.md`
- `docs/phase7/OPERATIONAL_RUNBOOKS.md`
- `docs/phase7/INFRASTRUCTURE_AUDITABILITY.md`
- `docs/phase7/LONG_TERM_STABILITY_TRACKING.md`
- `docs/phase7/INFRASTRUCTURE_COMPATIBILITY.md`
- `docs/phase7/FUTURE_CLUSTER_FOUNDATION.md`
- `docs/phase7/PHASE7_REPORT.md`

Tool:

- `tools/v7-infrastructure-readiness-review`

Runtime components already present:

- systemd timers/services for autoswitch, sentinel, quality compact, service matrix refresh.
- backup-related admin actions exist in monolith.

### 2. Partially Implemented

- Capacity awareness exists in autoswitch load policy, but not full infra resource model.
- Backup/restore admin hooks exist, but disaster recovery not proven.
- Runtime persistence model is documented, not enforced.
- Large-scale UX is documented, not implemented.

### 3. Documented Only

- Multi-region foundation.
- Endpoint redundancy.
- Disaster recovery runbooks.
- Upgrade safety gates.
- Failure domain isolation as a full platform guarantee.

### 4. Fake / Stub / Mock

- No fake infra tool found; `v7-infrastructure-readiness-review` is honest static review.
- But Phase 7 outcomes are mostly docs/tooling, not runtime infrastructure.

### 5. Runtime Verification Status

- Scaling: **NOT VERIFIED**.
- Backup/restore: **NOT VERIFIED**.
- Upgrade safety: **NOT VERIFIED**.
- Disaster recovery: **DOCUMENTED ONLY**.
- Resource management: **PARTIAL / STATIC**.

### 6. Governance Violations

- Timer/service hardening gaps.
- High-frequency sentinel timer may not scale.
- Infrastructure maturity is not enough for commercial reliability.

### 7. Technical Debt

- No unified deploy/package model visible.
- Systemd install script writes to `/usr/local/bin` and enables timers.
- Runtime state scattered across registries, JSON, SQLite, systemd, interfaces.

### 8. UI/UX Audit

- Large-scale UI grouping is not implemented beyond current admin.

### 9. Safety Audit

Risks:

- backup restore can silently break datapath if not verified;
- scaling can overload probes/autoswitch;
- one egress/org failure could propagate if isolation is only conceptual.

### 10. Must Be Fixed Before Production

- Perform backup/restore drill.
- Run upgrade rollback drill.
- Verify timers under N egress.
- Add service hardening directives where safe.

### 11. Should Be Refactored

- Package runtime dependencies.
- Add environment compatibility checker as deployment gate.

### 12. Should Not Be Touched

- Production systemd timers/services without maintenance window.
- Backup/restore scripts without test restore environment.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 65% |
| Runtime completeness | 10% |
| Production readiness | 20% |
| Observability maturity | 40% |
| Operator UX maturity | 40% |
| Safety maturity | 45% |

Phase 7 is mostly maturity documentation and static review.

## PHASE 8 — Advanced Intelligence & Adaptive Stealth

### 1. Implemented

Docs:

- `docs/phase8/INTELLIGENCE_SAFETY_BOUNDARIES.md`
- `docs/phase8/ADAPTIVE_STEALTH_ARCHITECTURE.md`
- `docs/phase8/TRANSPORT_INTELLIGENCE_LAYER.md`
- `docs/phase8/PREDICTIVE_DEGRADATION_DETECTION.md`
- `docs/phase8/REGIONAL_OPERATOR_INTELLIGENCE.md`
- `docs/phase8/ROUTE_FORECASTING_FOUNDATION.md`
- `docs/phase8/CONFIDENCE_RECOMMENDATION_MODEL.md`
- `docs/phase8/OPERATOR_ASSISTANCE_LAYER.md`
- `docs/phase8/ADAPTIVE_AUTOSWITCH_HOOKS.md`
- `docs/phase8/CONTROLLED_EXPERIMENTATION.md`
- `docs/phase8/LONG_TERM_LEARNING_FOUNDATION.md`
- `docs/phase8/CALM_INTELLIGENCE_UX.md`
- `docs/phase8/ADAPTIVE_TRANSPORT_STRATEGY.md`
- `docs/phase8/INTELLIGENCE_AUDITABILITY.md`
- `docs/phase8/FUTURE_DISTRIBUTED_INTELLIGENCE.md`
- `docs/phase8/PRESERVE_DETERMINISTIC_CORE.md`
- `docs/phase8/PHASE8_REPORT.md`

Tool:

- `tools/v7-intelligence-readiness-review`

Existing intelligence-adjacent runtime:

- service matrix;
- Telegram sentinel;
- quality summary;
- path benchmark;
- path optimizer advice;
- autoswitch safety review.

### 2. Partially Implemented

- Transport intelligence exists indirectly via quality/service/autoswitch signals.
- Predictive degradation exists as documentation/foundation, not live prediction.
- Operator assistance exists as summaries/advice in tools, not mature UI workflow.
- Adaptive autoswitch hooks exist conceptually and partially through autoswitch scoring.

### 3. Documented Only

- Adaptive stealth modes:
  - normal fast;
  - elevated stealth;
  - severe blocking fallback.
- Predictive degradation.
- Route forecasting.
- Controlled experimentation framework.
- Long-term learning foundation.
- Distributed intelligence foundation.

### 4. Fake / Stub / Mock

- No black-box AI implementation found.
- No adaptive stealth runtime implementation found.
- Intelligence readiness is static review, not adaptive intelligence.
- `v7-path-optimizer-advice --write` can persist recommendations, but not route; still must not be mistaken for authority.

### 5. Runtime Verification Status

- Adaptive intelligence: **DOCUMENTED ONLY / STATIC REVIEW**.
- Adaptive stealth: **DOCUMENTED ONLY**.
- Predictive degradation: **DOCUMENTED ONLY**.
- Transport intelligence: **PARTIAL SIGNAL FOUNDATION**.
- Controlled experimentation: **DOCUMENTED ONLY**.

### 6. Governance Violations

- No black-box AI violation found.
- Main risk is semantic: calling Phase 8 "implemented" would be misleading.

### 7. Technical Debt

- Recommendations/advice/state are not one unified model.
- No mature confidence/evidence contract enforced in UI.
- Stealth strategy not connected to transport runtime.

### 8. UI/UX Audit

- Calm intelligence UX is documented.
- No live UI integration verified.

### 9. Safety Audit

Good:

- Phase 8 did not add uncontrolled AI routing.

Risk:

- future intelligence output can influence operator/autoswitch decisions before confidence/evidence contracts are enforced.

### 10. Must Be Fixed Before Production

- Label all intelligence outputs as recommendation/advice unless deterministic policy applies.
- Add explicit confidence/evidence/safety bounds to any UI recommendation.
- Prevent `--write` advice from becoming hidden routing authority.

### 11. Should Be Refactored

- Build one recommendation schema reused by observability/autoswitch/admin.

### 12. Should Not Be Touched

- Deterministic routing core.
- Kill switch.
- Route class authority.

### 13. Scores

| Metric | Score |
|---|---:|
| Architecture completeness | 65% |
| Runtime completeness | 10% |
| Production readiness | 15% |
| Observability maturity | 40% |
| Operator UX maturity | 45% |
| Safety maturity | 45% |

Phase 8 is safe because it did not implement dangerous AI routing. It is not functionally complete.

## Subsystem Runtime Verification Matrix

| Subsystem | Status | Evidence | Notes |
|---|---|---|---|
| Routing | UNKNOWN | No live `ip route/ip rule` verification | Must verify on VPS |
| Kill switch | NOT VERIFIED LIVE | Scripts exist | No-leak cannot be claimed |
| nftables | UNKNOWN | Not inspected live | Critical |
| Autoswitch planner | PARTIALLY VERIFIED BY CODE | Real script exists | Apply not tested |
| Autoswitch systemd | NOT VERIFIED LIVE | Timer/service files exist | Runs `--apply` |
| Telegram sentinel | PARTIALLY VERIFIED BY CODE | Real script exists | Can trigger autoswitch apply |
| Provisioning | PARTIAL | Admin/tooling exists | E2E not verified |
| Quarantine | PARTIAL | Docs + state handling | Runtime gating not proven |
| Rollback | PARTIAL | Backups/actions exist | Disaster restore not proven |
| Driver lifecycle | DOCUMENTED/PARTIAL | Driver docs | No modular driver runtime |
| Onboarding | UNKNOWN | Admin code exists | Live flow not tested |
| Identity DB | NOT VERIFIED LOCALLY | DB missing locally | Path mismatch risk |
| Direct/RU | UNKNOWN | Scripts exist | Safety not proven |
| Trusted RU | UNKNOWN | Docs/actions exist | Fallback safety not proven |
| Observability | PARTIAL | Tools exist | Local state missing |
| Diagnostics | PARTIAL | Admin/tools exist | Quality/actionability unknown |
| Service matrix | PARTIAL | Tool exists | Live signal not verified |
| Backup/restore | NOT VERIFIED | Admin actions/docs | Needs drill |
| New web frontend | NOT IMPLEMENTED | Scaffold only | Not runtime |
| Adaptive intelligence | DOCUMENTED ONLY | Static review tool | No runtime intelligence |

## Fake / Stub / Mock Implementations

### Confirmed mocks/fakes

- `tools/v7-egress-import-regression`
  - fake runtime;
  - fake preflight;
  - fake matrix;
  - fake network/urlopen.

These are valid test fakes, but they must not be used as proof of production provisioning.

### Scaffolds not runtime

- `web/src/*`
- `web/src/app/information-architecture.json`
- `web/src/styles/status-semantics.css`
- `web/src/components/OPERATOR_BLOCK_CONTRACT.md`

These are not a working admin platform.

### Design artifacts not runtime

- `design/*.html`

These are UI artifacts/prototypes/snapshots.

### Hardcoded/demo values

- `admin/v7-admin-api` has example VLESS URL:
  - `vless://uuid@example.com:443?encryption=none&security=tls&type=tcp#v7-egress`

### Documentation-only hooks

Most Phase 7 and Phase 8 capabilities are explicit future foundation, not runtime implementation.

## Governance / Non-Negotiables Audit

### No silent traffic leaks

Status: **UNKNOWN**

Reason: no live kill switch/nftables/ip-rule verification performed.

### No unsafe direct routing

Status: **UNKNOWN**

Reason: direct/RU scripts exist, but live table/fwmark/DNS behavior was not verified.

### Kill switch mandatory

Status: **PARTIAL**

Reason: kill switch scripts exist; runtime guarantee not proven.

### Route classes authoritative

Status: **PARTIAL**

Reason: route classes are documented and referenced, but not proven authoritative across all runtime paths.

### Autoswitch stability over speed

Status: **PARTIAL**

Reason: autoswitch code has guarded scoring/cooldown/bounds, but systemd and sentinel apply paths need live verification.

### Calm Operator UX

Status: **AT RISK**

Reason: admin is dense and monolithic. Static UX review reports significant complexity.

### No black-box AI routing

Status: **COMPLIANT**

Reason: Phase 8 did not add AI routing.

### No rewrite-from-scratch

Status: **COMPLIANT**

Reason: changes are mostly docs/tools/scaffold; no giant rewrite.

### No uncontrolled complexity growth

Status: **AT RISK**

Reason: docs and tools expanded significantly while monolith remained. Complexity is better described but not reduced.

## Technical Debt Register

### Critical

- `admin/v7-admin-api` is 30067 lines and mixes:
  - API routing;
  - auth/RBAC;
  - identity DB;
  - provisioning;
  - routing actions;
  - diagnostics;
  - HTML;
  - CSS;
  - JavaScript.

- Autoswitch/sentinel can execute runtime moves through external commands.
- Live datapath safety not verified.
- Identity DB path mismatch.
- External commands not fully packaged/verified.

### High

- State scattered across:
  - `users.registry`;
  - `egress.registry`;
  - JSON state files;
  - SQLite identity DB;
  - systemd state;
  - Linux runtime;
  - nftables/routes.

- Many hardcoded host paths:
  - `/opt/v7`;
  - `/etc/v7`;
  - `/usr/local/bin`;
  - `/root/v7-*`.

- Systemd timer frequency and hardening need review.
- Web frontend is scaffold only.

### Medium

- Documentation is ahead of implementation.
- Regression tests use fakes.
- UI density risk.
- Many runtime commands are shell-coupled.

## UI/UX Audit

Current admin likely has useful operator surfaces, but risks violating Calm Operator UX:

- too many tabs/workspaces;
- many drawers;
- logs up to 300 events;
- topology language appears frequently;
- multiple diagnostics surfaces;
- provisioning/user/routing/security all embedded in one file.

What must change:

- summary first;
- incidents first;
- group diagnostics;
- cap raw telemetry visibility;
- hide route internals until drilldown;
- show action impact and rollback before dangerous actions.

What is good:

- `/admin-v2` exists;
- safe-mode and RBAC exist;
- overview cache exists;
- progressive disclosure via drawers appears to exist.

What is not good enough:

- new modular UI is not wired;
- design system is not enforced;
- density is growing inside monolith.

## Safety Audit

### Leak risks

Cannot be ruled out without live:

- `nft list ruleset`;
- `ip rule`;
- `ip route show table ...`;
- public interface route checks;
- VPN subnet route checks;
- direct-mark verification.

### Autoswitch risks

- systemd service runs `--apply`;
- Telegram sentinel can run `--apply`;
- default autoswitch policy enables guarded autoswitch if policy file missing;
- external switch/verify commands must be trusted.

### Provisioning risks

- unverified egress enable path unknown;
- rollback not proven;
- stale runtime cleanup not proven;
- three admin endpoints need safe-mode classification review.

### Identity risks

- identity DB path mismatch;
- revoked devices/profiles not verified live;
- org isolation not verified.

### Observability risks

- service matrix can be too shallow;
- sentinel frequency can create load/noise;
- UI can overexpose raw diagnostics.

## What Must Be Fixed Before Production

1. Establish clean baseline.
2. Run full live datapath verification on VPS.
3. Prove kill switch no-leak behavior.
4. Verify direct/RU and trusted RU do not unsafe fallback.
5. Verify autoswitch policy, cooldown, timers, and rollback.
6. Decide whether Telegram sentinel may trigger `--apply`.
7. Verify provisioning lifecycle end-to-end with quarantine and rollback.
8. Align identity DB path contract.
9. Verify org/device/profile lifecycle against live DB.
10. Review three admin safe-mode flagged endpoints.
11. Package/verify all external commands.
12. Run backup/restore drill.
13. Add production acceptance tests for admin dangerous actions.
14. Reduce or contain admin UI density.
15. Stop treating docs-only Phase 7/8 capabilities as implemented features.

## What Should Be Refactored

Priority refactors:

1. Extract read-only state readers from `admin/v7-admin-api`.
2. Extract audit/event helpers.
3. Extract identity DB module.
4. Extract provisioning adapters.
5. Extract autoswitch wrapper/API layer.
6. Extract UI components only after endpoint contracts are stable.
7. Split autoswitch into planner/scorer/executor/safety ledger.
8. Create one runtime dependency manifest.
9. Create one state contract validator with aligned DB paths.

Do not start with a full rewrite. That would violate governance.

## What Should Not Be Touched

Do not touch casually:

- `hardening/v7-killswitch-enable`
- `hardening/v7-killswitch-check`
- direct/RU routing scripts
- `tools/v7-users-autoswitch`
- `tools/v7-egress-set-state`
- production systemd timers/services
- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- `/etc/v7/policy.json`
- `/etc/v7/org-egress-policy.json`
- live SQLite identity DB
- admin action endpoint names/JSON shapes

These areas are either stable runtime or dangerous-to-modify. Any change needs backup, staging, explicit verification, and rollback.

## Final Platform Assessment

V7 is currently a **serious advanced prototype with operational runtime components**, not merely a toy.

It has:

- real admin monolith;
- real autoswitch planner;
- real service matrix/sentinel tooling;
- real hardening scripts;
- real provisioning actions;
- real identity/onboarding foundations;
- real systemd integration.

But it also has:

- large documentation/runtime gap;
- unverified live datapath safety;
- unverified kill switch no-leak guarantee;
- unverified provisioning rollback;
- unverified commercial multi-tenant isolation;
- unfinished modular admin platform;
- Phase 7/8 mostly documentation/static review;
- significant monolith debt;
- unsafe assumptions around external commands and host paths.

Best honest label:

**Partially production-capable operational routing platform prototype with strong governance documents and real control-plane components, but not yet a proven commercial-grade production platform.**

The platform may be running in production on the server, but this audit cannot certify it as production-safe without live runtime verification.

## Next Real Engineering Priorities

These are not roadmap phases. These are the real blockers.

1. **Live no-leak verification**
   - Kill switch, direct/RU, trusted RU, nftables, route tables, DNS path.

2. **Autoswitch safety proof**
   - Policy loaded;
   - cooldown active;
   - bounded moves;
   - verify/rollback works;
   - sentinel apply behavior intentionally approved.

3. **Provisioning end-to-end proof**
   - Import to quarantine to runtime test to staged enable to rollback.

4. **State contract cleanup**
   - Align identity DB path;
   - classify authoritative state;
   - validate registry/JSON/SQLite consistency live.

5. **Admin safety review**
   - Safe-mode flagged endpoints;
   - dangerous actions;
   - viewer/admin/owner roles;
   - impact/rollback previews.

6. **Backup/restore drill**
   - Restore into staging;
   - verify routing not corrupted;
   - verify registry/identity/policy recovery.

7. **Monolith containment**
   - Do not rewrite;
   - extract read-only modules first;
   - preserve endpoint contracts.

8. **UI density control**
   - Summary-first overview;
   - grouped incidents;
   - raw diagnostics behind drilldown;
   - no giant metric wall.

9. **Runtime dependency packaging**
   - Confirm every `v7-*` command exists on production;
   - document version/owner;
   - add deployment check.

10. **Stop marking docs as implementation**
    - Phase 7 and 8 must be treated as foundation, not completed runtime.

