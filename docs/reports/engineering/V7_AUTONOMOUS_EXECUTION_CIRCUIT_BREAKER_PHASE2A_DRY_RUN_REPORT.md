# V7 Autonomous Execution Circuit Breaker / Kill Switch Phase 2A Dry Run Report

Status: `ENGINEERING_REPORT`

Mission: `AUTONOMOUS EXECUTION CIRCUIT BREAKER / KILL SWITCH PHASE 2A — IMPLEMENTATION PLAN + DRY RUN`

Date: `2026-07-11`

Repository baseline: `b93adab6`

Source Discovery: `docs/reports/engineering/V7_AUTONOMOUS_EXECUTION_CIRCUIT_BREAKER_DISCOVERY_REPORT.md`

## Executive Result

```text
DISCOVERY_REVALIDATION = GAP_MATCHES_DISCOVERY
EXISTING_OWNERS_SUFFICIENT = YES
NEW_OWNER_REQUIRED = NO
NEW_STATE_OWNER_REQUIRED = NO
PRODUCTION_MUTATION_PERFORMED = NO
PRODUCTION_STATE_CHANGED = NO
AUTHORITY_CHANGED = NO
DRY_RUN_VERDICT = SAFE_TO_APPLY
OMP_CONTROLLED_RUN_ALLOWED = NO
```

The implementation gap is confirmed at code level. V7 already has canonical `CLOSED`, `HALF_OPEN`, `OPEN`, suspension, rollback, verification, closure, learning, Production Maturity, and CPS responsibilities. The missing implementation is one fail-closed operator control state consumed immediately before every autonomous production mutation.

The approved plan reuses Admin Safe Mode as the only operator-controlled stop state. It does not create a Circuit Breaker Engine, second Runtime, second Planner, second state owner, new lifecycle, new OMP capability, new authority, or new execution path.

This report is a dry run. No proposed patch was applied.

## 1. Discovery Revalidation

### 1.1 Revalidation verdict

```text
GAP_MATCHES_DISCOVERY
```

| Object | Actual implementation | Current fail behavior | Immediate pre-mutation control check | Bypass | Missing handoff |
| --- | --- | --- | --- | --- | --- |
| Admin Safe Mode state | `admin/v7-admin-api::admin_safe_mode_state`, `set_admin_safe_mode`; `/etc/v7/admin/safe-mode.json` | Missing, unreadable, malformed, or non-dict state becomes `enabled=false` | API dispatcher only | CLI/systemd/runtime paths | Safe Mode producer -> Runtime consumers |
| Safe Mode API/audit | `/api/actions/safe-mode-set`; owner role, CSRF, exact confirmation, audit, Overview | Active state blocks 86 listed Admin actions with HTTP 423 | Before Admin handler dispatch | Already-started process and non-API paths | Audit state -> final Runtime decision |
| Autoswitch apply | `tools/v7-users-autoswitch::apply` | Distributed gates generally stop safely; no global operator suspension gate | Envelope and L3 gates, but no breaker | Direct `--apply` | Breaker state -> apply and each `_run_switch` |
| Governed L3 | `tools/v7-governed-canary-dry-run-cycle::execute_l3_production_validation` | Packet/lease/restore failures STOP_SAFE | No breaker before plan, lease, clearance, or apply | Direct CLI and systemd | Breaker generation -> packet/lease/apply |
| Batch movement | `tools/v7-users-autoswitch::apply` loop | Stops on command/verification outcomes, not on newly enabled breaker | No reread between items | Remaining prepared moves continue | Live generation -> every item |
| Rollback packet | `execute_rollback_packet` | Invalid packet denies; valid packet may call `_run_switch` | Packet validation only | No global rollback-only classification | Breaker state -> certified compensation decision |
| Automatic rollback | verification-failure branch in `apply` | Executes through `_run_switch` when configured | No breaker semantics | No forward/rollback distinction | Breaker -> certified containment exception |
| Authority promotion | `promote_authority` | Confirmation, evidence and truth gates fail closed | No global operator stop | Direct CLI | Breaker -> production-affecting policy mutation |
| Low-level movement | production `/usr/local/bin/v7-user-switch` | Validates user/egress then directly runs `ip route replace` | No breaker check | Direct invocation | Existing execution-control contract -> primitive |
| systemd entry | `systemd/v7-users-autoswitch.service` | Scheduler state controls invocation only | No breaker | Enabling unit starts governed apply path | Breaker -> governed command |

### 1.2 Low-level primitive evidence

The deployed `v7-user-switch` is not currently release-owned in the repository. Its production body performs:

```bash
ip route replace default dev "$dev" table "$table"
```

before assignment persistence and audit. No Admin Safe Mode, circuit-breaker generation, packet, lease, or execution-owner check precedes that mutation.

Read-only source-adoption baseline:

```text
/usr/local/bin/v7-user-switch
sha256 = fd90a9763a8393c066c904514162d17264b4accd5040d332fa12f07debf39c16
```

Phase 2B must stop on a hash mismatch and revalidate the production source instead of silently adopting drift.

`tools/v7-runtime-tool-enumerate` classifies a repository-missing datapath-critical primitive as release ownership debt. The existing safe-deploy allowlist also has no `/usr/local/bin/v7-user-switch` entry.

### 1.3 Existing test baseline

Phase 2A executed a read-only baseline subset:

```text
python3 -m unittest -q \
  tests.unit.test_operator_execution_packet \
  tests.unit.test_governed_canary_cli \
  tests.contracts.endpoint_inventory_test

Ran 70 tests
OK
```

The Discovery baseline remains `256 passed`. No test was weakened or changed.

## 2. Existing Owner Reuse Map

| Responsibility | Existing owner | Reuse decision | New owner |
| --- | --- | --- | --- |
| Suspension/downgrade semantics | OMP | Reuse existing suspension and recovery laws | `NO` |
| Circuit-breaker states and final execute-or-stop law | Autonomous Runtime Model / Runtime Model | Reuse `CLOSED`, `HALF_OPEN`, `OPEN`, `SUSPENDED`, `STOP_SAFE` | `NO` |
| Operator stop state and state-change audit | Admin Safe Mode / `admin/v7-admin-api` | Keep as sole writer and sole operator stop state | `NO` |
| State validation, generation and packet/lease binding | `admin_core/operator_execution.py` | Extend existing packet/lease owner with shared control-state validation | `NO` |
| Shared command-line validation | `tools/v7-operator-execution-packet` | Reuse existing wrapper; add a validation mode in its existing owner | `NO` |
| Final forward mutation consumer | `tools/v7-users-autoswitch` | Consume shared decision before apply and each movement | `NO` |
| Governed pre-lease/pre-apply consumer | `tools/v7-governed-canary-dry-run-cycle` | Consume and bind current generation | `NO` |
| Low-level mutation boundary | existing production `v7-user-switch` primitive | Bring existing primitive under repository/release ownership and consume existing validator | `NO` |
| Rollback/containment | existing rollback packet, automatic rollback, B15/C5 owners | Preserve certified rollback-only path | `NO` |
| Operator visibility/history | Admin Overview and audit | Surface state, generation, reason and block decisions | `NO` |
| Volatile program visibility | CPS | Mirror implementation/certification and active program blocker only; never Runtime truth | `NO` |
| Health/maturity impact | Production Maturity | Consume certified implementation and real outcomes later | `NO` |

## 3. Existing Closure Law Mapping

No new closure law is required.

| Required responsibility | Existing law/owner | Application to this Mission |
| --- | --- | --- |
| Producer/consumer continuity | OMP producer-consumer continuity and Legal Terminal Consumer rule | State writer must feed validator; validator must feed every mutation boundary. |
| Automation Gap Closure | OMP Automation Gap Closure | API-only state with unconsumed Runtime output remains incomplete. |
| Intent Gap Detection | OMP Intent Gap Detection | Original intent is immediate, global, fail-closed suspension of autonomous mutation. |
| Engineering Intent Closure Validation | OMP closure validation | Local function/test PASS cannot close the Mission until all mutation consumers are covered. |
| Freshness/stale mutation blocking | B17, B18, C1, C6; Runtime Model | Missing, unknown, expired, or generation-stale control cannot authorize mutation. |
| Verification | Runtime/Verification owners | Every allowed mutation still requires existing verification. |
| Rollback/Closure | B15/C5 and rollback owners | Breaker blocks forward mutation while certified compensation remains separately bounded. |
| Learning | existing feedback/learning owners | Block, success, rollback and failure remain separate terminal outcomes. |
| Production Maturity | Production Maturity Model | Implementation evidence alone does not certify production autonomy. |
| CPS synchronization | CPS | Records current program/certification state; does not become executable breaker truth. |

## 4. Target State Contract

### 4.1 Single state source

Path remains:

```text
/etc/v7/admin/safe-mode.json
```

Writer remains Admin Safe Mode. Runtime consumers never write this state.

Proposed schema:

```json
{
  "schema_version": "v7.autonomous-execution-control.v2",
  "enabled": true,
  "state": "OPEN",
  "scope": "global",
  "generation": "aec_<owner-issued-id>",
  "updated_at": "<RFC3339 UTC>",
  "valid_until": "",
  "updated_by": "<operator>",
  "reason": "<operator reason>",
  "rollback_policy": "CERTIFIED_ROLLBACK_ONLY"
}
```

Contract rules:

1. `enabled=true` means `OPEN`; all autonomous forward mutation is denied.
2. `OPEN` does not expire into permission. A stale/old `OPEN` remains deny-safe across restart.
3. `enabled=false` means `CLOSED` only while `valid_until` is fresh.
4. `CLOSED.valid_until` reuses `DEFAULT_EXECUTION_LEASE_TTL_SECONDS = 900`; no new duration owner or threshold is introduced.
5. Missing file, unreadable file, malformed JSON, wrong schema, missing generation, invalid timestamps, unknown state/scope/action class, expired `CLOSED`, or generation mismatch returns `STOP_SAFE`.
6. `HALF_OPEN` remains an existing canonical state but is not newly automated by this implementation. Unsupported `HALF_OPEN` execution returns `STOP_SAFE` until an existing OMP certification path explicitly admits one bounded validation action.
7. The state never grants Authority, changes Planner output, expands blast radius, or certifies an action class.

### 4.2 Fail-closed decision output

Existing `admin_core.operator_execution` produces a structured decision:

```text
allowed_forward_mutation
rollback_only_allowed
state
scope
generation
valid_until
reason
blockers
audit_fields
```

Only `allowed_forward_mutation=true` can pass the breaker. Every existing Authority, freshness, packet, lease, blast-radius, rollback, verification and eligibility gate still applies afterward.

### 4.3 Generation binding

`breaker_generation` is added to:

- packet identity;
- `APPROVED_PACKET_BINDING_FIELDS`;
- `MATERIAL_STATE_FIELDS`;
- execution lease immutable identity/material state;
- governed-cycle apply arguments;
- autoswitch approved identity and final live checks.

A state change after plan/packet/lease creation invalidates prepared work. The current file is reread before apply and before every forward `_run_switch`.

## 5. Mutation Coverage Matrix

| Mutation Entry Point | Existing Owner | Proposed existing gate consumer | Check location | Generation | Rollback semantics | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Admin guarded autoswitch | Admin + autoswitch | shared control decision + autoswitch live recheck | API dispatch, apply entry, before `_run_switch` | live + expected | forward only | `COVERED_BY_PLAN` |
| Direct autoswitch CLI | autoswitch | shared control decision | apply entry and every move | live; expected when prepared | direct rollback requires certified packet | `COVERED_BY_PLAN` |
| Scheduled/systemd governed L3 | governed cycle | shared control decision | before plan/lease and immediately before autoswitch apply | bound to packet/lease | rollback remains operation-scoped | `COVERED_BY_PLAN` |
| Direct governed L3 CLI | governed cycle | same as scheduled path | same two boundaries | bound | operation-scoped | `COVERED_BY_PLAN` |
| Every forward `_run_switch` | autoswitch | shared control decision | directly before subprocess invocation | live equality | not rollback | `COVERED_BY_PLAN` |
| Batch between items | autoswitch | shared control decision | top of every loop iteration | live equality | remaining forward items stop | `COVERED_BY_PLAN` |
| Recovery movement | recovery owners + autoswitch | inherited autoswitch final gate | before future recovery apply and movement | live/bound | existing recovery containment | `COVERED_BY_PLAN` |
| Rollback packet | autoswitch rollback owner | rollback-only decision after packet validation | before loop and each rollback item | current state recorded; forward permission not required | certified rollback packet only | `COVERED_BY_PLAN` |
| Automatic rollback | autoswitch verification/rollback owner | rollback-only decision tied to current failed operation | immediately before compensation `_run_switch` | operation/generation evidence | allowed only after attempted forward mutation and failed verification | `COVERED_BY_PLAN` |
| Low-level `v7-user-switch` | existing movement primitive | existing `v7-operator-execution-packet` validation mode | immediately before `ip route replace` | mandatory owner-issued context | rollback context mandatory | `COVERED_BY_PLAN` |
| Authority promotion | autoswitch Authority mutation owner | shared control decision | immediately before policy backup/write | live current generation | not rollback | `COVERED_BY_PLAN` |
| Admin Safe Mode state change | Admin owner | not blocked by itself | owner-only endpoint | creates new generation | emergency stop/clear control | `NOT_APPLICABLE_WITH_REASON`: this is the control producer |
| Read-only diagnostics, preview, Verification, evidence, Learning | respective existing owners | no mutation denial | unchanged | visible only | available while OPEN | `NOT_APPLICABLE_WITH_REASON`: permanent breaker rule preserves them |

### 5.1 Eight Admin actions outside the existing block set

The current Admin platform review reports eight handlers outside `SAFE_MODE_BLOCKED_ACTIONS`. They are classified here so they are not an unknown mutation family:

| Endpoint family | Classification | Reason |
| --- | --- | --- |
| `closure-set`, `execution-feedback-materialize` | `NOT_APPLICABLE_WITH_REASON` | Closure/learning evidence; must remain available while autonomy is suspended. |
| `recommendation-approve`, `recommendation-ignore`, `shadow-autonomy-compare` | `NOT_APPLICABLE_WITH_REASON` | Recommendation/shadow state; non-authorizing and non-runtime. |
| two egress draft creation endpoints | `NOT_APPLICABLE_WITH_REASON` | Draft-only configuration preparation; no production apply. |
| `egress-draft-post-enable-validation` | `NOT_APPLICABLE_WITH_REASON` | Post-action verification evidence; no enable/apply mutation. |

Their names should receive explicit static classification tests, but they are not autonomous production mutation bypasses.

## 6. File-by-file Diff Preview

All previews below are proposals only.

### CB-01 — `admin_core/operator_execution.py`

Existing owner: packet/lease/material-state/fail-closed execution validation.

Current behavior: no autonomous execution control reader or generation field.

Proposed behavior:

```diff
+AUTONOMOUS_EXECUTION_CONTROL_SCHEMA = "v7.autonomous-execution-control.v2"
+DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE = Path("/etc/v7/admin/safe-mode.json")
+
+def autonomous_execution_control_state(path=..., *, now=None):
+    # strict schema/timestamp/generation/scope validation
+    # missing/invalid/expired CLOSED => STOP_SAFE
+    # OPEN always denies forward mutation
+
+def autonomous_execution_control_decision(...):
+    # structured allow/deny/rollback-only result; never grants Authority
+
 MATERIAL_STATE_FIELDS = [
+    "breaker_generation",
     ...
 ]
 APPROVED_PACKET_BINDING_FIELDS = [
+    "breaker_generation",
     ...
 ]
+parser.add_argument("--check-autonomous-execution-control", action="store_true")
+parser.add_argument("--expected-breaker-generation", default="")
+parser.add_argument("--mutation-kind", choices=("forward", "rollback"), ...)
```

Reason: one existing validation owner must expose identical semantics to Admin, Python Runtime and the shell primitive.

Tests: strict schema; missing/malformed/unknown/expired; OPEN persistence; generation mismatch; scope/action-class unknown; forward/rollback separation; no Authority output.

### CB-02 — `admin/v7-admin-api`

Existing owner: sole operator state writer, authentication, confirmation, audit and Overview.

Current fragment:

```python
data = read_json(SAFE_MODE_FILE, {})
...
"enabled": bool(data.get("enabled", False))
```

Proposed preview:

```diff
-def admin_safe_mode_state():
-    ... bool(data.get("enabled", False)) ...
+def admin_safe_mode_state():
+    return operator_execution.autonomous_execution_control_state(SAFE_MODE_FILE)

 def set_admin_safe_mode(actor, enabled, reason=""):
     data = {
-        "schema_version": 1,
+        "schema_version": AUTONOMOUS_EXECUTION_CONTROL_SCHEMA,
         "enabled": bool(enabled),
+        "state": "OPEN" if enabled else "CLOSED",
+        "scope": "global",
+        "generation": owner_issued_generation,
+        "updated_at": now_iso(),
+        "valid_until": "" if enabled else now_plus_existing_900_second_lease_window,
         "updated_by": actor,
         "reason": reason,
+        "rollback_policy": "CERTIFIED_ROLLBACK_ONLY",
     }
```

The API block response and Overview add state, generation, validity, reason and fail-closed blockers. State changes remain owner-role + CSRF + exact confirmation + audit.

Compatibility: current schema v1/missing state becomes STOP_SAFE for autonomous mutation until an operator writes valid v2. It never becomes an implicit allow.

Tests: writer schema/generation; enabled blocks; disabled fresh window; state-change audit; Overview fields; blocked mutation audit.

### CB-03 — `tools/v7-users-autoswitch`

Existing owner: planner plus bounded routing apply, rollback and Authority promotion.

Current fragments:

```python
for move in plan["selected_moves"]:
    proc = self._run_switch(ip, target, move.get("move_type", "planned"))
```

```python
env["V7_SWITCH_REASON"] = f"autoswitch_{reason}"
return subprocess.run(["v7-user-switch", ip, egress], ...)
```

Proposed preview:

```diff
+control = self._autonomous_execution_control_decision(mutation_kind="forward", expected_generation=...)
+if not control["allowed_forward_mutation"]:
+    return STOP_SAFE("autonomous_execution_control_denied", control)
 for move in plan["selected_moves"]:
+    control = self._autonomous_execution_control_decision(...)
+    if not control["allowed_forward_mutation"]:
+        break_with_stop_safe_for_remaining_moves()
     proc = self._run_switch(..., execution_control=control)
```

`_run_switch` passes mandatory existing-owner context to `v7-user-switch`: mutation kind, breaker generation, action class, operation id, packet/rollback identity. Missing context is denied by the primitive.

`execute_rollback_packet` first validates the existing rollback packet, then requests `rollback-only` consumption. Automatic rollback receives rollback eligibility only from the current failed verified operation. A caller cannot obtain rollback-only behavior by setting `reason=rollback` alone.

`promote_authority` performs a live forward-mutation decision immediately before policy backup/write. The breaker never creates, promotes or expands Authority.

Tests: direct CLI denial; prepared-state change; batch interruption; Authority promotion denial; Planner output equality; rollback packet and automatic rollback distinction.

### CB-04 — `tools/v7-governed-canary-dry-run-cycle`

Existing owner: governed packet/lease/restore/apply lifecycle.

Current behavior: creates packet and lease, then invokes autoswitch apply without breaker state.

Proposed preview:

```diff
+preflight_control = operator_execution.autonomous_execution_control_decision(...)
+if not preflight_control["allowed_forward_mutation"]:
+    return transaction_stop("autonomous_execution_control_denied_pre_lease")
 packet = operator_execution.packet_from_plan(..., breaker_generation=preflight_control["generation"])
 lease = operator_execution.create_execution_lease_from_packet(...)
 ...
+pre_apply_control = operator_execution.autonomous_execution_control_decision(
+    expected_generation=packet_identity["breaker_generation"], ...)
+if not pre_apply_control["allowed_forward_mutation"]:
+    finish lease OPERATOR_CANCELLED and STOP_SAFE
 apply_run = run_autoswitch_apply(..., breaker_generation=...)
```

The same function is used by direct CLI and systemd, so neither route can bypass the gate.

Tests: enabled/missing/invalid state before lease; generation change after lease; enabled after packet preparation; apply never launched on denial; lease terminalized safely.

### CB-05 — `tools/runtime-support/v7-user-switch` (repository adoption of existing primitive)

Existing owner: deployed low-level user routing primitive. This is source adoption, not a new owner or execution path.

Current production behavior:

```bash
ip route replace default dev "$dev" table "$table"
```

Proposed preview immediately before that line:

```diff
+v7-operator-execution-packet \
+  --check-autonomous-execution-control \
+  --expected-breaker-generation "$V7_EXECUTION_CONTROL_GENERATION" \
+  --mutation-kind "$V7_EXECUTION_MUTATION_KIND" \
+  --operation-id "$V7_EXECUTION_OPERATION_ID" \
+  --json >/tmp_or_pipe_result
+[ validator_verdict = ALLOW ] || { echo "STOP_SAFE: execution control denied"; exit 2; }
 ip route replace default dev "$dev" table "$table"
```

The actual implementation must avoid an unsafe reusable temporary result and parse the validator result from the same invocation. Missing owner context, direct invocation, unknown mutation kind, invalid rollback identity, OPEN state, stale `CLOSED`, or generation mismatch denies before `ip route replace`.

Tests use temporary registries and a fake `ip` command. They prove `ip route replace` is never reached on denial and is reached only with a valid owner-issued context.

### CB-06 — `tools/v7_sync_lib.py`

Current behavior: safe-deploy allowlist does not own `/usr/local/bin/v7-user-switch`.

Proposed preview:

```diff
 APPROVED_DEPLOY_FILES = [
+  {
+    "name": "v7-user-switch",
+    "local_path": "tools/runtime-support/v7-user-switch",
+    "remote_path": "/usr/local/bin/v7-user-switch",
+    "mode": "0755",
+    "service": None,
+  },
 ]
```

Reason: the final mutation primitive must be release-owned, fingerprinted and convergence-auditable with its caller and validator.

Tests: allowlist coverage, deploy delta, runtime fingerprint/hash coverage, no production deploy in Phase 2B unless separately authorized.

### CB-07 — tests

Proposed test changes only:

| File | Planned coverage |
| --- | --- |
| `tests/unit/test_operator_execution_packet.py` | schema, fail-closed parsing, TTL, generation, scope, CLI validator, packet/lease binding |
| `tests/unit/test_v7_users_autoswitch_policy.py` | apply, batch, direct CLI, rollback-only, automatic rollback, promotion, Planner invariance |
| `tests/unit/test_governed_canary_cli.py` | pre-lease/pre-apply denial, generation invalidation, safe lease terminalization |
| `tests/contracts/endpoint_inventory_test.py` | Admin state delegation, audit/visibility fields, explicit classification of eight Safe Mode exceptions |
| `tests/unit/test_v7_sync_tools.py` | release ownership and fingerprint for `v7-user-switch` |
| `tests/unit/test_v7_user_switch.py` | low-level deny/allow boundary with fake system commands; no real routing mutation |

### CB-08 — CPS/OMP synchronization after Phase 2B certification

No canonical document change is proposed before implementation and verification.

After a successful Phase 2B only:

- Engineering Report records implementation/test evidence;
- CPS records the current blocker/certification result and whether a controlled run remains blocked;
- OMP consumes the certification result and selects the next legal step;
- Production Maturity remains unchanged unless its existing owner accepts sufficient evidence;
- no runtime process writes markdown CPS/OMP files;
- Admin Safe Mode remains Runtime truth; CPS remains visibility only.

## 7. Safety Matrix For Every Proposed Change

```text
NEW_OWNER ............... NO
NEW_ENGINE .............. NO
NEW_RUNTIME ............. NO
NEW_PLANNER ............. NO
NEW_LIFECYCLE ........... NO
NEW_OMP_CAPABILITY ...... NO
SECOND_STATE_OWNER ...... NO
AUTHORITY_EXPANSION ..... NO
BLAST_RADIUS_EXPANSION .. NO
PRODUCTION_APPLY ........ NO
EXISTING_OWNER_REUSE .... YES
FAIL_CLOSED ............. YES
CHAIN_CLOSED ............ YES
```

This matrix applies to CB-01 through CB-08. Any Phase 2B diff that changes one answer is not approved by this Dry Run and must stop as `MANUAL_REVIEW_REQUIRED`.

## 8. Fail-Closed And Generation Model

| Condition | Required result |
| --- | --- |
| State file missing/unreadable | `STOP_SAFE` |
| JSON malformed/non-object | `STOP_SAFE` |
| Unknown/legacy schema | `STOP_SAFE` for autonomous mutation |
| Missing generation/actor/reason/timestamp/scope | `STOP_SAFE` |
| Unknown state/scope/action class | `STOP_SAFE` |
| `OPEN` | deny forward mutation without expiry |
| `CLOSED` expired after existing 900-second lease window | `STOP_SAFE` |
| Packet/lease expected generation differs from live generation | invalidate prepared work and `STOP_SAFE` |
| Breaker enabled after planning | pre-apply recheck denies |
| Breaker enabled during batch | next iteration denies remaining forward mutations |
| Process restart | reload durable file; missing/invalid remains deny-safe; `OPEN` stays deny |
| Breaker decision passes | continue to existing Authority/safety/packet/lease/verification gates; no authority created |

## 9. Rollback-Only Semantics

Breaker state does not convert every `reason=rollback` invocation into permission.

Rollback-only is allowed only when one of these existing contracts proves compensation ownership:

1. a valid operation-scoped rollback packet has passed `_validate_rollback_packet`; or
2. the current autoswitch operation performed a forward mutation, immediate verification failed, and the existing `rollback_on_verify_fail` contract requests compensation for that same user/source/target.

Required fields include operation identity, source operation, selected-move identity, current user location, rollback target, and breaker decision audit fields. Unknown, direct, stale, unbound, or reason-only rollback requests are denied.

When `OPEN`:

- new forward mutations stop;
- existing certified compensation may continue one item at a time;
- the breaker is reread before each compensation item;
- rollback failure remains a separate terminal state and may never be reported as success;
- diagnostics, Verification, audit, closure and Learning remain available.

## 10. Test Plan

| Required scenario | Planned executable assertion |
| --- | --- |
| Enabled breaker denies Admin autoswitch | handler returns 423 and emits block audit |
| Enabled breaker denies direct autoswitch | `apply_result.applied=false`, `STOP_SAFE`, `_run_switch` not called |
| Enabled breaker denies systemd/governed L3 | transaction stops before lease/apply |
| Enabled breaker denies low-level forward mutation | fake `ip` records no `route replace` |
| Missing/malformed/unknown schema | structured deny; no mutation subprocess |
| Stale state | expired `CLOSED` denies; old generation denies prepared work |
| Generation changes after packet/lease | packet/lease invalidated and apply not launched |
| Breaker enabled after plan | live pre-apply deny |
| Breaker enabled during batch | first completed item preserved; remaining forward items not invoked |
| Restart preserves suspension | fresh process reads durable `OPEN` and denies |
| Direct bypass | low-level invocation without owner context denies |
| No Authority creation | decision has no grant/promote output; existing Authority tests unchanged |
| No Planner change | identical plan output for same inputs whether breaker is OPEN or CLOSED; only apply result differs |
| Read-only remains available | plan/preview/diagnostics/verification/report calls succeed while OPEN |
| Certified rollback-only | validated packet or immediate operation-scoped compensation reaches primitive |
| Uncertified rollback | reason-only/direct request denied |
| Audit/visibility | state changes and blocked decisions contain generation/state/reason/actor |
| Mutation inventory | static contract asserts every classified entry point has a consumer or reason |
| Compatibility | existing read-only, non-autonomous, packet, lease, rollback and endpoint suites remain green |

No test may invoke the real production `ip`, deploy, systemd, Authority promotion, or user movement.

## 11. Closed Engineering Chain Validation

Future Phase 2B chain:

```text
Operator sets suspension/clearance
  -> Admin Safe Mode writes durable v2 state and generation
  -> Admin audit/Overview consumes the state
  -> packet/lease owner consumes and binds generation
  -> governed cycle consumes before lease and before apply
  -> autoswitch consumes at apply and before every item
  -> low-level primitive consumes immediately before route mutation
  -> mutation or STOP_SAFE is recorded
  -> Verification consumes executed outcome
  -> certified rollback/containment consumes failed outcome when required
  -> Closure records legal terminal classification
  -> Learning consumes terminal outcome
  -> Engineering Report preserves evidence
  -> Production Maturity accepts/blocks/no-changes evidence
  -> CPS mirrors current program/certification state
  -> OMP consumes CPS/maturity/report and selects next legal step
  -> Engineering Intent Closure verifies no autonomous mutation bypass remains
```

Producer/consumer validation:

| Producer output | Required next consumer | Orphan risk after plan |
| --- | --- | --- |
| Admin control state/generation | shared validator | none |
| Validator decision | Admin, governed cycle, autoswitch, primitive | none |
| Packet/lease generation binding | governed pre-apply and autoswitch | none |
| Apply/deny result | Verification/audit/closure | none |
| Verification outcome | rollback/closure | none |
| Rollback/containment outcome | closure/learning | none |
| Closure/learning evidence | report/Production Maturity | none |
| Maturity/program result | CPS/OMP | none |

Legal Terminal Consumer: OMP consumes the CPS/maturity/certification result after Engineering Intent Closure Validation. A local validator PASS, test PASS, report, or one blocked path is not terminal completion.

## 12. SAFE_TO_APPLY List

```text
CB-01 shared fail-closed control contract in existing packet/lease owner
CB-02 Admin Safe Mode v2 sole-writer schema and operator visibility
CB-03 autoswitch apply/batch/rollback/promotion consumers
CB-04 governed pre-lease/pre-apply generation consumption
CB-05 repository ownership and final gate for existing v7-user-switch primitive
CB-06 safe-deploy allowlist/fingerprint coverage
CB-07 executable unit/contract regression coverage
CB-08 post-certification Engineering Report -> Production Maturity -> CPS -> OMP synchronization
```

## 13. MANUAL_REVIEW_REQUIRED List

```text
NONE
```

No owner, lifecycle, policy threshold, Authority expansion, blast-radius expansion, or architectural decision is missing. The 900-second fresh `CLOSED` window reuses the current execution-lease owner and constant. `OPEN` remains durable and deny-safe.

## 14. OMP Controlled Run Safety Status

```text
OMP_CONTROLLED_RUN_ALLOWED = NO
```

Reason: this Dry Run changes no executable consumer. Current Admin Safe Mode remains API-only and fail-open on missing/malformed state; direct CLI, systemd/governed apply, batch, rollback, Authority promotion and low-level movement do not yet consume the shared final gate.

Read-only OMP analysis, Discovery, preview, test planning and certification preparation remain allowed.

## 15. Next Minimal Step

Run a separate Phase 2B implementation/certification Mission that:

1. revalidates repository baseline `b93adab6` or explicitly reconciles drift;
2. applies only CB-01 through CB-08 as approved here;
3. performs no deploy, production mutation, Authority change or user movement;
4. runs the complete targeted and regression suites;
5. proves every mutation path consumes the final gate;
6. creates a Phase 2B Engineering Report;
7. updates CPS/OMP only after verified implementation evidence;
8. keeps `OMP_CONTROLLED_RUN_ALLOWED = NO` unless Phase 2B certification explicitly proves the implementation complete and no bypass remains.

## Final Verdict

```text
SAFE_TO_APPLY
OMP_CONTROLLED_RUN_ALLOWED = NO
```
