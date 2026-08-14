# Admin Parse Registry Consumer Split Mapping Report

**Discovery:** `ADMIN_PARSE_REGISTRY_CONSUMER_SPLIT_MAPPING_V1`  
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**Type / Layer:** `READ_ONLY_BOUNDARY_DISCOVERY / MANAGEMENT_PLANE`  
**Runtime / Production / Authority effects:** `NONE / NONE / NONE`

## 1. Scope and current responsibility

Only `admin/v7-admin-api:parse_registry(path)` was analyzed. It is a
transparent delegation to the existing
`admin_core.admin_registry_views.parse_registry(path)` owner. Every current
call passes one explicit input: `STATE_DIR/users.registry` or
`STATE_DIR/egress.registry`.

The shared output contract is a redacted `list[dict]`; absent/empty input
produces an empty list through the existing reader path. The wrapper has no
state write, Runtime effect, action effect or special error handling. Security
context comes from the caller: output is already redacted by the existing owner.

## 2. Complete consumer inventory

The AST map found `41` direct calls. Each entry below is
`caller:line (registry input)`; each caller consumes the redacted row list.

| Context | Consumers | Classification | State / side effect |
| --- | --- | --- | --- |
| Detail, overview and display | `user_detail:18787 (users)`, `egress_detail:19248,19253 (egress,users)`, `overview:19589,19590 (users,egress)`, `do_GET:37660,37665 (users,egress)` | `READ_ONLY` | reads registry; response/display only |
| Diagnostics and read-only previews | `traffic_summary_state:15785,15792`, `direct_routing_freshness:19399`, `direct_routing_quick:19413`, `direct_routing_full:19538`, `service_aware_route_dry_run:16464`, `users_registry_map:13598`, `egress_assigned_user_rows:18925` | `READ_ONLY` | reads registry; no writer in caller path mapped here |
| Engineering evidence/read models | `generated_evidence_bundles:10596,10599`, `generated_user_evidence_bundles:10726`, `runtime_drift_records:12242,12306`, `operator_decision_surface_response:11817,11818` | `DIAGNOSTIC` | read inputs feed evidence/decision presentation; output lifecycle needs separate proof |
| Provisioning, identity and egress action-bound helpers | `identity_update_user_metadata:3884`, `egress_draft_post_enable_validation:9283,9297`, `save_public_client_speed_sample:17249`, `egress_delete_migration_plan:18946`, `proxy_runtime_egress_for_user:9663` | `ADMIN_ACTION` or `CONTROL_PATH` | wrapper reads only; enclosing caller may validate, write or trigger later work |
| Proposal generators requiring behavior trace | `generated_proposals:11064,11067`, `generated_user_proposals:11242` | `UNKNOWN` | evidence/proposal naming alone does not prove action or read-only semantics |
| Guarded POST handlers | `do_POST:39866,39898,40020,40141,40165,40177,40189,40831,40910,40982` | `ADMIN_ACTION` | registry data participates in authenticated guarded operation paths |

The table accounts for all 41 calls: `15 READ_ONLY`, `7 DIAGNOSTIC`,
`16 ADMIN_ACTION`, and `3 UNKNOWN` classification units. The
`CONTROL_PATH`-sensitive `proxy_runtime_egress_for_user` call remains within
the action-bound cohort until its Product Contract trace is analyzed.

## 3. Behavior contracts by cohort

| Cohort | Current input / output | Error and security contract | Migration risk |
| --- | --- | --- | --- |
| Read-only | explicit registry path -> redacted row list -> display, detail, diagnostic payload | existing parser handles missing/empty input; no caller write | low only after endpoint/payload baseline per isolated cohort |
| Diagnostic | explicit registry path -> redacted row list -> evidence/decision data | existing redaction retained; downstream evidence consumer must be proven | medium: output may be persisted or used for decision explanation |
| Action-bound | explicit registry path -> redacted row list -> validation/provision/delete/POST input | caller auth, RBAC, CSRF and safe-mode remain outside wrapper | high: direct migration must preserve guarded operation behavior |
| Unknown | explicit registry path -> redacted row list -> proposal construction | no hidden effect was assumed | blocked pending producer/consumer lifecycle trace |

## 4. Responsibility analysis

`parse_registry` itself has one responsibility and one existing owner:
redacted parsing of a caller-selected registry path. The mixed meaning exists in
its consumers, not in the function. Therefore a broad deletion would conflate
read-only display paths with guarded actions and evidence/proposal flows.

Possible future splits are consumer cohorts, not a split of the parser:

1. a fully baselined read-only cohort;
2. an evidence/proposal cohort after its producer and durable consumer are mapped;
3. action-bound cohorts only after individual Product Contract and rollback proof.

## 5. Candidate disposition and next safe boundary

| Disposition | Candidate | Reason |
| --- | --- | --- |
| `READY_FOR_FUTURE_MISSION` | none | no complete isolated cohort has direct-owner migration and endpoint baseline yet |
| `NEEDS_MORE_EVIDENCE` | read-only display/detail cohort | prove exact endpoint payloads and all direct owner call-site arguments |
| `NEEDS_MORE_EVIDENCE` | diagnostic/evidence cohort | prove producer -> durable consumer and retention behavior |
| `KEEP_CURRENT_BOUNDARY` | all action-bound calls | `parse_registry` has no side effect, but callers are security/operation contexts |
| `KEEP_CURRENT_BOUNDARY` | proposal callers | classification is still unknown |

No implementation Mission was created. No code, owner, state handling, Admin
API, CPS, Runtime, Production or Authority was changed.

**NEXT_SAFE_BOUNDARY:** a read-only admission packet for one endpoint-neutral
display/detail cohort, but only after direct-owner argument and response
equivalence are proved. The global CPS successor remains:

```text
EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION
```
