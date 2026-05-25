# V7 Track 5 - Extraction Safety Matrix

Purpose: decide what can be extracted first without breaking runtime compatibility.

## Risk Classes

| Class | Meaning |
|---|---|
| `SAFE_READ_ONLY` | Pure formatting/parsing/read-only code; no writes, no shell mutation |
| `LOW_RISK_WITH_TESTS` | Can move after snapshot tests and endpoint schema capture |
| `MEDIUM_RISK` | State-coupled or shell-read coupled; extraction needs contract tests |
| `HIGH_RISK` | Writes runtime state, calls mutation tools, or affects operator safety |
| `DO_NOT_EXTRACT_YET` | Datapath, Trusted RU, autoswitch apply, provisioning enable, route mutation |

## Extraction Risk Matrix

| Subsystem | Read/Write | Coupling | Risk | Track 5 Verdict |
|---|---|---|---|---|
| redaction helpers | read-only | low | `SAFE_READ_ONLY` | candidate |
| timestamp/age helpers | read-only | low | `SAFE_READ_ONLY` | candidate |
| bounded/safe value parsers | read-only | low | `SAFE_READ_ONLY` | candidate |
| registry parsing | read-only, broad use | state-coupled | `LOW_RISK_WITH_TESTS` | candidate after fixtures |
| JSON/text atomic IO | writes state | global | `MEDIUM_RISK` | do not move first unless heavily tested |
| audit event normalization | read-only | audit files | `LOW_RISK_WITH_TESTS` | candidate |
| audit writer | writes audit | shell-coupled to `v7-audit-log` | `MEDIUM_RISK` | later |
| service matrix normalization | read-only | state schema | `LOW_RISK_WITH_TESTS` | candidate |
| observability summary adapters | read-only | multiple state files | `MEDIUM_RISK` | candidate after schema freeze |
| identity read models | read-only DB | SQLite schema | `MEDIUM_RISK` | candidate after DB fixtures |
| identity writers | writes DB/profile/users | high | `HIGH_RISK` | later |
| egress import parsers | pure-ish parsing | config formats | `LOW_RISK_WITH_TESTS` | good candidate |
| egress draft writes | writes `/etc/v7/egress-drafts` | lifecycle | `HIGH_RISK` | later |
| egress runtime tests | shell/process coupled | interfaces/proxies | `HIGH_RISK` | do not move first |
| egress enable/apply | writes runtime registry | production impact | `DO_NOT_EXTRACT_YET` | freeze only |
| traffic summaries | read-only | SQLite/runtime files | `MEDIUM_RISK` | later |
| policy readers | read-only | policy schemas | `MEDIUM_RISK` | candidate after contract freeze |
| policy writers | writes `/etc/v7` | route behavior | `HIGH_RISK` | later |
| autoswitch dry-run wrapper | shell-read/planning | autoswitch tool | `MEDIUM_RISK` | later |
| autoswitch apply wrapper | mutates routing assignment | high | `DO_NOT_EXTRACT_YET` | no |
| direct/RU readers | read-only but sensitive | policy/direct files | `HIGH_RISK` | no Track 5 extraction |
| Trusted RU diagnostics | shell/policy sensitive | route class semantics | `DO_NOT_EXTRACT_YET` | no |
| embedded UI JS | frontend-only but schema-coupled | huge | `MEDIUM_RISK` | no rewrite; carve after endpoint contracts |
| Handler router | all endpoints | critical | `DO_NOT_EXTRACT_YET` | no |

## Safest-First Extraction Order

1. `admin_core.sanitize`
   - `redact`
   - `safe_*` validators that do not touch state
   - bounded int/float helpers
2. `admin_core.time`
   - `now_iso`
   - `parse_ts`
   - `age_sec`
   - `file_age`
3. `admin_core.registry_readers`
   - `parse_kv_line`
   - `parse_registry`
   - read-only registry maps
   - fixtures required before moving
4. `admin_core.events`
   - `tail_jsonl`
   - `infer_event_severity`
   - `infer_admin_audit_fields`
   - no writer movement yet
5. `admin_core.service_matrix`
   - `normalize_service_matrix_row`
   - service matrix read adapters
6. `admin_core.egress_parsers`
   - OpenVPN/Clash/Xray/Outline/share parser helpers
   - regression fixtures required

## Extraction Blockers

Before moving code:

- freeze endpoint contracts;
- add import compatibility wrapper;
- add fixtures for registry, service matrix, identity DB, and egress configs;
- verify old executable still starts;
- run read-only endpoint smoke tests;
- run runtime safety checks if deployed.

## Explicitly Forbidden First Extractions

- `user-switch` and user route mutation;
- `autoswitch_apply_guarded`;
- `policy_update`;
- `org_egress_policy_update`;
- direct/RU and Trusted RU apply/refresh actions;
- egress enable/apply/delete/pause;
- profile token consumption;
- Handler route dispatch.

