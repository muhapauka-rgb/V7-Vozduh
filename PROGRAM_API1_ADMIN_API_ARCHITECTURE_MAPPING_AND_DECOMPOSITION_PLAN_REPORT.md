# PROGRAM API.1 - Admin API Architecture Mapping, Truth Source Audit And Safe Decomposition Plan

Project: V7 Vozduh

Branch: `Updatesystem`

Mode: read-only audit

Primary target: `admin/v7-admin-api`

Evidence directory: `api1_evidence`

## Executive Verdict

`admin/v7-admin-api` can be decomposed safely only through a staged read-only-first program.

API.2 may begin if it is constrained to pure read-only helpers and view builders. It is not safe to begin with action handlers, auth/session/RBAC, `run_action`, execution handlers, rollback apply, governance mutation, audit writers, closure writers, or full UI separation.

## Files Created

Main report:

- `PROGRAM_API1_ADMIN_API_ARCHITECTURE_MAPPING_AND_DECOMPOSITION_PLAN_REPORT.md`

Evidence:

- `api1_evidence/endpoint_inventory.json`
- `api1_evidence/complete_endpoint_inventory.md`
- `api1_evidence/admin_api_static_map.json`
- `api1_evidence/endpoint_boundary_map.json`
- `api1_evidence/truth_source_map.json`
- `api1_evidence/largest_functions.json`
- `api1_evidence/discovery_summary.md`
- `api1_evidence/duplication_audit.md`
- `api1_evidence/truth_source_summary.md`
- `api1_evidence/dependency_graph.md`
- `api1_evidence/ownership_map.md`
- `api1_evidence/read_write_boundary_map.md`
- `api1_evidence/safe_extraction_candidates.md`
- `api1_evidence/performance_foundation_audit.md`
- `api1_evidence/decomposition_plan.md`
- `api1_evidence/risk_matrix.md`
- `api1_evidence/certification.md`

## Discovery Gate

The admin API was inventoried statically without importing or executing it.

| Metric | Value |
|---|---:|
| Source lines | 36,468 |
| Functions/classes detected | 657 |
| Endpoint branches detected | 264 |
| GET endpoints | 118 |
| HEAD endpoints | 8 |
| POST endpoints | 138 |
| Public endpoints | 19 |
| Auth-required endpoints | 245 |
| CSRF-required endpoints | 133 |
| Safe-mode blocked endpoints | 86 |

Risk counts:

| Risk | Count |
|---|---:|
| low | 118 |
| medium | 38 |
| high | 95 |
| critical | 13 |

Conclusion: the file is a combined admin server, operator UI, auth gate, runtime command wrapper, preview builder, execution/governance surface, audit writer, closure writer, identity/profile system, and public delivery path.

## Endpoint Inventory

Generated inventory:

- `api1_evidence/endpoint_inventory.json`
- `api1_evidence/complete_endpoint_inventory.md`

Boundary summary:

| Boundary | Count |
|---|---:|
| READ | 62 |
| UI | 19 |
| ACTION | 130 |
| WRITE | 2 |
| EXECUTION | 38 |
| GOVERNANCE | 7 |
| ROLLBACK | 6 |

Derived authority flags:

| Flag | Count |
|---|---:|
| read-only | 78 |
| runtime mutation possible | 183 |
| execution authority possible | 39 |
| governance mutation possible | 10 |
| rollback authority possible | 6 |

The classifier is conservative by design. Preview endpoints under POST/action areas are still treated as sensitive until contract tests prove exact behavior.

## Truth Source Map

Generated evidence:

- `api1_evidence/truth_source_map.json`
- `api1_evidence/truth_source_summary.md`

Authoritative stores:

| Area | Truth source |
|---|---|
| runtime users | `/opt/v7/egress/state/users.registry` |
| runtime egress/channels | `/opt/v7/egress/state/egress.registry` |
| runtime summary | `/opt/v7/egress/state/v7-state.json` |
| audit | `/opt/v7/audit/audit.jsonl` |
| events | `/opt/v7/events` |
| admin auth | `/etc/v7/admin/auth.json` |
| safe mode | `/etc/v7/admin/safe-mode.json` |
| maintenance | `/etc/v7/maintenance.conf` |
| egress drafts | `/etc/v7/egress-drafts` |
| egress draft tests | `/opt/v7/admin/egress-draft-tests` |
| egress runtime configs | `/etc/v7/egress-runtime` |
| identity | `/opt/v7/admin/v7-identity.db` |
| route policy | `/etc/v7/policy.json` |
| org egress policy | `/etc/v7/org-egress-policy.json` |
| route classes | `/opt/v7/policy/route-classes.registry` |
| profile delivery tokens | `/opt/v7/egress/state/profile-delivery-tokens.json` |
| service matrix | `/opt/v7/egress/state/service-matrix.json` |
| Trusted RU diagnostic | `/opt/v7/egress/state/trusted-ru-diagnostic.state` |
| Trusted RU decision | `/opt/v7/egress/state/trusted-ru-decision.state` |
| direct routing domains | `/etc/v7/direct/domains.conf` |
| policy domain files | `/etc/v7/policy` |
| traffic history | `/opt/v7/traffic/traffic.sqlite` |

Truth-source rule: API decomposition must not introduce replacement stores or mirrored mutable state. It may only move read-only views over these sources.

## Dependency Graph

Generated evidence:

- `api1_evidence/dependency_graph.md`

High-level dependency:

```text
admin/v7-admin-api
  -> admin_core.events
  -> admin_core.operator_observability
  -> admin_core.registry_readers
  -> admin_core.sanitize
  -> admin_core.time
  -> /opt/v7 runtime state
  -> /etc/v7 policy/config/auth
  -> runtime-support tools through run_action
  -> read-only tools through run_readonly
  -> embedded /admin-v2 HTML/CSS/JS
```

Adjacent authoritative modules:

| Module/tool | Authority |
|---|---|
| `admin_core.operator_execution.py` | execution packet/governance contract model |
| `admin_core.operator_observability.py` | read-only operator timeline, audit, evidence, operation detail |
| `admin_core.registry_readers.py` | shared registry parsing |
| `admin_core.routing_brain.py` | RI advisory candidate scoring contract |
| `admin_core.routing_intelligence.py` | RI advisory signal model |
| `tools/v7-users-autoswitch` | planner/autoswitch dry-run and apply semantics |
| runtime-support tools | runtime execution mechanics |

## Ownership Map

Generated evidence:

- `api1_evidence/ownership_map.md`

| Responsibility | Owner | API.2 decision |
|---|---|---|
| HTTP routing | `Handler` in `admin/v7-admin-api` | do not touch first |
| auth/session/RBAC/CSRF | `admin/v7-admin-api` | do not touch first |
| safe mode | `admin/v7-admin-api` | do not touch first |
| runtime action execution | `run_action` plus runtime tools | do not touch first |
| audit writer | `audit_admin` | do not touch first |
| closure writer | admin closure functions | do not touch first |
| operator read-only observability | `admin_core.operator_observability.py` plus admin wrappers | extend |
| execution packet model | `admin_core.operator_execution.py` | reuse |
| registry parsing | `admin_core.registry_readers.py` and admin wrapper | extend |
| routing intelligence | `admin_core.routing_brain.py`, `admin_core.routing_intelligence.py` | reuse |
| embedded UI | `html_page_v2` | split late |

## Duplication Audit

Generated evidence:

- `api1_evidence/duplication_audit.md`

Material overlaps were found, but no safe reason exists to create parallel systems.

| Area | Finding | Decision |
|---|---|---|
| registry readers | admin wrapper plus tool-local parsers | reuse `admin_core.registry_readers` for admin read-only views first |
| audit writers | admin audit writer plus runtime audit writer | do not merge writers; extract read-only views only |
| closure | admin closure owner plus planner closure target metadata | keep admin closure owner |
| execution | admin `run_action`, runtime tools, execution packet models | no second executor |
| rollback | admin wrappers plus runtime rollback tools | preview views only first |
| governance | admin surfaces plus `operator_execution` packet model | reuse existing model |
| service readers | admin summaries plus service matrix tools | separate cache producer from view reader |
| routing intelligence | RI modules plus planner usage | admin displays; planner remains authority |

Duplication verdict: manageable overlap exists, but dangerous parallel systems should not be introduced.

## Read/Write Boundary

Generated evidence:

- `api1_evidence/read_write_boundary_map.md`

Safe early boundary:

- read-only GET payload builders;
- event/audit/evidence serializers;
- registry read views;
- service matrix summaries;
- route-class summaries;
- deterministic preview result formatters where command execution remains unmoved.

Forbidden as first extraction:

- action route dispatch;
- action execution;
- user movement;
- rollback apply;
- governance mutation;
- audit writes;
- closure writes;
- auth/RBAC/CSRF;
- whole UI split.

## Safe Extraction Candidates

Generated evidence:

- `api1_evidence/safe_extraction_candidates.md`

Recommended first API.2 module:

`admin_core.admin_registry_views`

Allowed scope:

- registry snapshot loading;
- redacted users/egress rows;
- egress maps/default helpers;
- pure serialization;
- no writes;
- no `run_action`;
- no route movement;
- no new stores.

Other early candidates:

- event list serializers;
- audit/evidence/timeline read-only builders;
- safe value parsers;
- overview sub-builders after schema snapshots;
- service matrix read summaries;
- route-class read summaries.

## Performance Foundation Audit

Generated evidence:

- `api1_evidence/performance_foundation_audit.md`
- `api1_evidence/largest_functions.json`

Largest hotspots:

| Symbol | Lines | Concern |
|---|---:|---|
| `html_page_v2` | 12,370 | large embedded UI string and API/action coupling |
| `Handler` | 4,005 | routing/auth/actions/responses coupled in one class |
| `egress_draft_runtime_run` | 329 | preview/runtime preparation mixed |
| `egress_channel_add_pipeline` | 318 | provisioning pipeline risk |
| `egress_parse_proxy_share` | 316 | heavy import/parser logic |
| `egress_config_preview` | 270 | preview builder |

Performance-first plan:

- add request-scoped registry/state snapshots;
- introduce short TTL overview summaries;
- keep expensive probes out of automatic GET paths;
- use background/cache producers for service matrix, Trusted RU diagnostics, traffic summaries, backup verification, and speed/proxy checks;
- bound audit/event/JSONL reads;
- split read builders before action handlers.

## Decomposition Roadmap

Generated evidence:

- `api1_evidence/decomposition_plan.md`
- `api1_evidence/risk_matrix.md`

| Stage | Scope | Risk | Start now? |
|---|---|---|---|
| 1 | read-only extraction | LOW/MEDIUM | yes |
| 2 | shared builders and snapshots | MEDIUM | after schemas |
| 3 | routing intelligence views | MEDIUM | after RI fixtures |
| 4 | action handler preparation | HIGH | not first |
| 5 | governance handlers | HIGH | read-only only first |
| 6 | execution handlers | CRITICAL | no |
| 7 | UI separation | MEDIUM/HIGH | after endpoint contracts |

## What Must Remain Runtime Authority

- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- runtime-support tools for actual apply/rollback/systemd/proxy changes
- `tools/v7-users-autoswitch` for planner/autoswitch behavior
- `admin_core.operator_execution.py` for packet/governance contract model
- `admin_core.routing_brain.py` and `admin_core.routing_intelligence.py` for RI advisory contracts
- `admin/v7-admin-api` for auth, route dispatch, audit writes, closure writes, and action execution until later certified blocks

## API.2 Recommendation

Proceed to API.2 only with a narrow title such as:

`API.2 Read-Only Registry And Operator View Extraction`

Required API.2 gates:

1. Freeze before/after endpoint inventory.
2. Add or preserve `/api/overview` and operator read-only schema snapshots.
3. Extract one small read-only module at a time.
4. Keep `Handler`, auth, CSRF, `run_action`, audit writer, closure writer, and action bodies in place.
5. Run `py_compile`, unit tests, endpoint inventory, and diff safety scans.

## Verification Performed

Static verification artifacts were generated. No admin runtime process was started and no live server action was executed.

Commands used during audit:

```text
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out api1_evidence/endpoint_inventory.json
```

Additional static JSON/markdown evidence was derived from repository source and generated inventory.

## Safety

| Safety item | Value |
|---|---|
| runtime_behavior_changed | false |
| governance_behavior_changed | false |
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| autoswitch_apply_run | false |
| deploy_performed | false |
| systemd_changed | false |
| execution_engine_changed | false |
| runtime_hooks_changed | false |

## Final Verdicts

| Verdict | Value |
|---|---|
| endpoint_inventory_complete | true |
| truth_source_map_complete | true |
| dependency_graph_complete | true |
| ownership_map_complete | true |
| read_write_boundary_map_complete | true |
| safe_extraction_candidates_identified | true |
| performance_audit_complete | true |
| decomposition_plan_complete | true |
| performance_foundation_plan_complete | true |
| safe_to_begin_api2 | true, read-only scope only |

## Final Certification

API.1 is complete.

The safest decomposition path is:

1. extract read-only registry and operator view helpers;
2. introduce request snapshots and bounded read models;
3. add schema contracts before overview/service/policy builders;
4. postpone action/execution/governance/rollback/UI separation until later certified blocks.

No runtime behavior or governance behavior was changed.
