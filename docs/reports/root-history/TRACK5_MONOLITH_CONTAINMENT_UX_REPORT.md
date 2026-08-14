# V7 Vozduh - Track 5 Monolith Containment & Calm Operator UX Evolution

Generated: 2026-05-23

Scope: begin controlled monolith containment and operator UX evolution without rewriting admin, changing runtime behavior, or touching routing/datapath.

No code extraction was applied in Track 5 because endpoint contracts are not frozen yet. This is intentional.

## 1. Monolith Subsystem Map

Created:

- `docs/track5/MONOLITH_BOUNDARY_MAP.md`

Observed monolith:

```text
admin/v7-admin-api: 30067 lines
```

Subsystems:

| Subsystem | Primary Responsibility | Runtime Risk |
|---|---|---|
| auth/session | login, sessions, cookies, throttling | Medium |
| RBAC/safe mode | role gates, action access, safe mode | High |
| state helpers | JSON/text IO, registries, validators | Critical |
| identity/onboarding | users, orgs, devices, connect sessions | Critical |
| profile delivery | public profile tokens, QR/download | Critical |
| provisioning | import, drafts, tests, quarantine, enable | High/critical |
| egress lifecycle | delete, pause, migrate, labels | Critical |
| observability | diagnostics, service matrix, traffic, events | Medium/high |
| autoswitch wrappers | plan, dry-run, apply wrapper | Critical |
| policy/routing summaries | route class, service-aware, policy | Critical |
| direct/RU + Trusted RU | direct policy, sensitive diagnostics | Critical/sensitive |
| UI rendering | embedded admin/public HTML and JS | Medium/high |
| Handler/router | all GET/POST endpoint dispatch | Critical |

## 2. Coupling Hotspots

Main hotspots:

1. `Handler` route dispatch is a single long chain for GET/POST.
2. Embedded JS calls many `/api/*` endpoints and assumes response shapes.
3. State helpers are global and used across identity, provisioning, routing, and UI.
4. Shell-coupled helpers call `/usr/local/bin/v7-*`; many production tools still lack repo lineage.
5. Identity/profile delivery crosses SQLite, token JSON, users registry, and profile files.
6. Provisioning writes draft/runtime/registry state and can run external processes.
7. Direct/RU and Trusted RU are mixed with policy, UI, diagnostics, and route class semantics.
8. Audit behavior exists but is not fully uniform as a contract across every risky action.

## 3. Extraction Risk Matrix

Created:

- `docs/track5/EXTRACTION_SAFETY_MATRIX.md`

Safest extraction candidates:

- redaction helpers;
- timestamp/age helpers;
- pure safe validators;
- registry read parsers after fixtures;
- event normalization readers;
- service matrix normalization;
- egress import parsers after regression fixtures.

Forbidden first extractions:

- user switching;
- autoswitch apply;
- policy apply;
- direct/RU or Trusted RU behavior;
- egress enable/apply/delete/pause;
- profile token consumption;
- Handler route dispatch.

## 4. Safe Extraction Candidates

Candidate modules:

| Module | Candidate Functions | Safety |
|---|---|---|
| `admin_core.sanitize` | `redact`, safe string/token validators | Safe read-only |
| `admin_core.time` | `now_iso`, `parse_ts`, `age_sec`, `file_age` | Safe read-only |
| `admin_core.registry_readers` | `parse_kv_line`, `parse_registry`, read-only maps | Low with fixtures |
| `admin_core.events` | `tail_jsonl`, severity inference, field inference | Low with fixtures |
| `admin_core.service_matrix` | row normalization, service state shaping | Low/medium |
| `admin_core.egress_parsers` | OpenVPN/Clash/Xray/Outline/share parsing | Low/medium with regression tests |

No extraction was done yet because contracts and fixtures must come first.

## 5. Endpoint Contract Freeze Plan

Created:

- `docs/track5/ENDPOINT_CONTRACT_FREEZE_PLAN.md`

Static scan observed:

```text
approx route branches: 186
```

Endpoint contract fields to freeze:

- method;
- path;
- auth role;
- CSRF requirement;
- safe mode behavior;
- request schema;
- response schema;
- error semantics;
- redaction behavior;
- state files read/written;
- shell commands called;
- audit event;
- rollback context.

Critical endpoint families:

- routing/user mutation;
- autoswitch;
- provisioning/egress lifecycle;
- policy/direct/RU;
- identity/profile delivery;
- public connect/profile delivery.

Compatibility constraints:

- no silent endpoint path changes;
- no silent JSON top-level key changes;
- no silent auth/role changes;
- no silent confirmation token changes;
- no shell argument drift.

## 6. Operator UX Maturity Analysis

Created:

- `docs/track5/CALM_OPERATOR_UX_EVOLUTION.md`

Current positives:

- Phase 6A information hierarchy exists;
- grouped diagnostics model exists;
- status semantics exist;
- operator block contract exists;
- autoswitch and health semantics are calmer after stabilization.

Current UX risks:

- UI is still embedded in monolith;
- dangerous actions are numerous;
- endpoint response shapes are implicit;
- runtime governance status is not yet first-class in UI;
- sensitive-state warnings are not yet calmly surfaced;
- direct/RU and Trusted RU can be semantically nuanced and must not be forced green.

## 7. Information Architecture Map

Level 1 - Platform state:

- overall state;
- incidents;
- affected users/orgs;
- degraded channels;
- autoswitch guard state;
- capacity imbalance;
- sensitive-state warnings;
- runtime baseline/release status.

Level 2 - Grouped diagnostics:

- Channels;
- Routing;
- Services;
- Users;
- Trusted RU;
- Autoswitch;
- Provisioning;
- Security;
- Runtime governance.

Level 3 - Deep evidence:

- raw command output;
- route reality rows;
- service matrix rows;
- MTU/path diagnostics;
- raw JSON;
- event streams.

Rule:

Level 3 must never be the default page state.

## 8. Workflow Risk Analysis

| Workflow | Risk | Recommended UX Control |
|---|---|---|
| user switch | can worsen instability | show anti-flap/capacity context |
| autoswitch apply | high impact | guarded confirm + confidence/cooldown |
| egress enable | production impact | lifecycle gate summary |
| egress delete/pause | user migration risk | affected users + rollback |
| profile delivery | token sensitivity | expiry/revoke visibility |
| direct/RU changes | policy/routing sensitivity | separate diagnostic context |
| policy update | broad behavior impact | before/after + backup |
| runtime cleanup | deploy ambiguity | manifest/archive status |
| sensitive hardening | can break access | dry-run access map before chmod |

## 9. Exact Changes Applied

Local foundation files added:

- `docs/track5/MONOLITH_BOUNDARY_MAP.md`
- `docs/track5/EXTRACTION_SAFETY_MATRIX.md`
- `docs/track5/ENDPOINT_CONTRACT_FREEZE_PLAN.md`
- `docs/track5/CALM_OPERATOR_UX_EVOLUTION.md`
- `TRACK5_MONOLITH_CONTAINMENT_UX_REPORT.md`

Runtime changes:

- None.

Code extraction:

- None. Not justified before endpoint contract freeze.

## 10. Runtime Verification Results

Track 5 did not modify live runtime. Mandatory read-only verification should remain the deployment gate for any future extraction.

Last live safety verification during Track 4/5 inspection showed:

| Check | Result |
|---|---|
| `systemctl --failed` | PASS |
| `v7-killswitch-check` | PASS |
| `v7-user-route-check` | PASS |
| `v7-provisioning-reconcile-check` | PASS |
| `v7-observability-summary --pretty` | PASS |

Because Track 5 only added local documentation, no runtime regression path was introduced.

## 11. Remaining Architecture Blockers

Critical:

- endpoint contracts are not machine-frozen;
- no snapshot tests for `/api/*` response shapes;
- embedded UI and backend are still in one executable;
- production-only runtime tools remain a coupling risk;
- sensitive profile-token state still needs hardening.

High:

- shell command dependencies need explicit contracts;
- provisioning lifecycle needs operator-visible gate truth;
- identity/profile delivery must be protected before extraction;
- audit must become a uniform contract for dangerous actions.

## 12. Recommended Next Containment Steps

1. Generate endpoint inventory JSON from current monolith.
2. Add read-only contract tests for:
   - `/health`;
   - `/api/session`;
   - `/api/overview`;
   - `/api/events`;
   - `/api/diagnostics`.
3. Add schema fixtures for critical previews:
   - autoswitch dry-run;
   - egress enable preview;
   - egress set-state preview;
   - policy route preview.
4. Extract only `admin_core.sanitize` and `admin_core.time` after tests pass.
5. Keep all routing, direct/RU, autoswitch apply, provisioning apply, and profile delivery logic in place until contracts are enforced.

