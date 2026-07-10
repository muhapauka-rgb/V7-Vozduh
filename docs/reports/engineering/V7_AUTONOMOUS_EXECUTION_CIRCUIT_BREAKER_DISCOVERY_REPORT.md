# V7 Autonomous Execution Circuit Breaker Discovery Report

Status: `DISCOVERY_COMPLETE`
Mission: `AUTONOMOUS_EXECUTION_CIRCUIT_BREAKER_KILL_SWITCH_DISCOVERY_AND_CERTIFICATION`
Date: `2026-07-11`
Mode: `READ_ONLY_DISCOVERY`
Final verdict: `IMPLEMENTATION_GAP`
OMP_CONTROLLED_RUN_ALLOWED: `NO`
Production controls changed: `NO`
Runtime apply, user movement, Authority change, rollback, deploy: `NO`
New owner, Engine, Runtime, Planner, lifecycle, capability, or truth source: `NO`

Exact safety reason:

```text
V7 has strong distributed STOP_SAFE, Authority, lease, packet, restore,
blast-radius, verification, rollback, policy, and operator controls, plus an
Admin Safe Mode. It does not have one executable fail-closed suspension state
consumed immediately before every production mutation. Admin Safe Mode is
API-only, missing/malformed state defaults to disabled, and direct systemd/CLI
autoswitch, rollback, and low-level v7-user-switch paths do not consume it.
Therefore a prepared or directly invoked mutation can bypass the current
operator stop state.
```

`OMP_CONTROLLED_RUN_ALLOWED = NO` applies to any OMP run capable of production mutation. Read-only OMP analysis, Discovery, preview, and certification runs remain allowed.

## 1. Existing Owner Discovery

No single new Circuit Breaker owner is required. The responsibility already maps to existing owners.

| Existing owner | Current responsibility | Circuit-breaker relevance | Current limitation |
| --- | --- | --- | --- |
| OMP | Suspension, downgrade, action-class state, certification and operator-control semantics. | Owns when autonomy must be suspended and when it may recover. | No current executable suspension state is consumed by every mutation path. |
| Runtime Model | Thin execute-or-stop lifecycle and final live-gate semantics. | Requires circuit breaker/suspension before execution. | Canonical contract exists; final executable consumption is missing. |
| Current Program State | Volatile program state and active blockers. | Canonical contract says active override/suspension is visible here. | No current circuit-breaker or operator-override field exists. CPS is not a Runtime truth source. |
| Authority / action-class / blast-radius owners | Permission, class scope, budgets, freeze/revoke and promotion. | Can deny or narrow specific execution authority. | Authority denial is not a global emergency stop and does not cover every direct mutation path. |
| `admin/v7-admin-api` | Operator surface, role/CSRF enforcement, audit, Admin Safe Mode. | Existing global operator control for Admin API mutations. | State is consumed only in the API dispatcher; missing/malformed state fails open. |
| `tools/v7-users-autoswitch` | Planner plus guarded Runtime movement owner. | Owns the final `_run_switch` call for autoswitch apply and automatic rollback. | Does not read Admin Safe Mode or another global suspension state before mutation. |
| `tools/v7-governed-canary-dry-run-cycle` | Governed L3 packet/lease/restore/apply/verification lifecycle. | Existing autonomous production entry path. | Invokes autoswitch `--apply` without circuit-breaker consumption. |
| `admin_core.operator_execution` | Packet, lease, identity, material-state recheck, restore barrier. | Strong fail-closed prepared-action validation. | No kill-switch/suspension field in packet or live pre-mutation recheck. |
| Verification / rollback / containment owners | Post-action proof, compensation and safe terminal state. | Must remain available when autonomy is suspended. | No explicit rollback-only mode tied to a global breaker. |
| Audit / Overview | Operator-visible events and status. | Admin Safe Mode changes and blocks are audited and visible. | Runtime CLI bypasses do not produce a breaker decision because they never read the state. |

Owner verdict:

```text
EXISTING_OWNERS_SUFFICIENT = YES
NEW_OWNER_REQUIRED = NO
```

## 2. Executable Control Inventory

| Mechanism | State source / producer | Consumer | Scope | Fail behavior | Persistence / audit | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| Admin Safe Mode | `/etc/v7/admin/safe-mode.json`; owner-only `/api/actions/safe-mode-set` with explicit confirmation. | Admin API dispatcher checks `SAFE_MODE_BLOCKED_ACTIONS`. | Global across 86 listed Admin mutation endpoints. | Enabled state blocks with HTTP 423. Missing, unreadable, malformed, or absent `enabled` becomes `false`: fail-open. | Atomic file, backup, mode `0600`; operator-visible Overview; set/block events audited. | `EXISTS_PARTIALLY` |
| `switch.autoswitch_enabled` | Policy/org-policy; planner reads at process start. | Planner and `apply(plan)`. | Autoswitch capability. | Disabled blocks; missing policy inherits default `true`. Not reread immediately before `_run_switch`. | Policy-file persistence; ordinary execution evidence. | `EXISTS_PARTIALLY` |
| Autoswitch mode | CLI/policy: observe, guarded, active. | `apply(plan)`. | One invocation. | Observe blocks apply; direct CLI may select guarded/active. | Process-local. | `ALREADY_IMPLEMENTED_AND_COVERED`, not a kill switch |
| Authority budget lifecycle | Policy: class, certified class, frozen/revoked. | Planner selection and authority-budget gate. | Action class / batch scope. | Disabled, frozen, revoked or over-budget states stop selected moves. | Policy persistence; tests and plan evidence. | `IMPLEMENTED_DISTRIBUTED` |
| A6 Runtime Eligibility | Existing read model over freshness, authority, blast, rollback, verification, recovery and runtime_apply. | Certification/read-model consumers. | Runtime eligibility model. | Produces `STOP_SAFE`. | Read-only evidence. | `EXISTS_PARTIALLY`; not consumed as the final live gate by all apply paths |
| L3 execution eligibility | Plan, incident, wake, Authority, identity and live source/target/service evidence. | Autoswitch L3 apply path immediately before movement loop. | L3 emergency failover only. | Unknown/mismatch produces `STOP_SAFE`. | Plan/audit/terminal evidence; extensive tests. | `ALREADY_IMPLEMENTED_AND_COVERED` for L3 eligibility, not global suspension |
| Packet / execution lease / atomic envelope | Packet and lease owners, source hashes, generation and identity. | Governed execution and autoswitch apply validation. | Approved operation/action scope. | Missing, expired, changed or mismatched identity stops. | Durable lease/packet stores and audit. | `IMPLEMENTED_DISTRIBUTED` |
| Restore barrier / rollback readiness | Existing restore and rollback owners. | Governed execution and planner/apply gates. | Operation / selected movement scope. | Missing or mismatched clearance blocks governed movement. | Durable state and audit evidence. | `IMPLEMENTED_DISTRIBUTED` |
| User/channel/policy gates | Registry, egress state, org policy, anti-flap, quarantine, cooldown. | Planner and live L3 checks. | User / channel / target / policy. | Invalid or blocked scope stops that candidate. | Registry/policy/state persistence. | `IMPLEMENTED_DISTRIBUTED` |
| systemd service/timer state | systemd. | Starts governed L3 production-validation command. | Process scheduling. | Inactive prevents scheduled execution only. Enabling service bypasses Admin Safe Mode. | Persistent unit enablement; runtime status visible. | Operational containment only, not a circuit breaker |
| Network `v7-killswitch` | nftables/network tooling. | Data-plane leak prevention and diagnostics. | Network egress safety. | Protects traffic leakage. | Runtime network state and checks. | `NOT_THE_EXECUTION_KILL_SWITCH` |
| `v7-safe-run` | Static allowlist wrapper. | Admin diagnostic calls. | Diagnostic command execution. | Unknown command is blocked. | Audit event when available. | Diagnostic safe mode only; does not wrap autoswitch apply |

## 3. Mutation Entry Point Inventory

| Mutation entry point | Owner / primitive | Current route | Current status |
| --- | --- | --- | --- |
| Scheduled autonomous L3 validation | `systemd/v7-users-autoswitch.service` -> `tools/v7-governed-canary-dry-run-cycle` | Explicit production confirmation embedded in unit -> packet/lease/restore -> autoswitch `--apply` -> `v7-user-switch`. | Scheduler currently inactive, but no circuit-breaker state is consumed if started. |
| Direct governed L3 CLI | `tools/v7-governed-canary-dry-run-cycle --execute-l3-production-validation` | Same governed production path as systemd. | Strong packet/lease/restore gates; no global suspension gate. |
| Direct autoswitch CLI | `tools/v7-users-autoswitch --apply` | Plan -> apply -> `_run_switch` -> `v7-user-switch`. | Can bypass Admin Safe Mode. Policy missing defaults autoswitch enabled. |
| Admin guarded autoswitch | `/api/actions/autoswitch-apply-guarded` | Role + CSRF + confirmation + Admin Safe Mode -> direct autoswitch CLI. | Safe Mode blocks before process launch, but there is no final recheck after launch or before each mutation. |
| Admin direct user switch | `/api/actions/user-switch` | Current handler returns governed-pipeline blocker. | Hard-blocked; no current mutation. |
| Low-level movement primitive | `v7-user-switch` | Direct CLI or called by autoswitch. | No repository-visible global breaker consumer; direct invocation is a bypass. |
| Batch movement | Autoswitch selected moves inside authority/blast bounds. | One process may call `_run_switch` repeatedly. | No breaker reread between moves; operator cannot stop remaining prepared moves through Admin Safe Mode. |
| Recovery candidate movement | B8/B9/B10 -> A6 -> existing autoswitch owner. | Read-only integration only. | No current mutation, but future apply would inherit the same final-gate gap. |
| Operation-scoped rollback packet | `v7-users-autoswitch --rollback-packet ... --apply`. | Packet validation -> `_run_switch` per rollback item. | No global breaker consumption; rollback may need an explicit safety exemption/rollback-only state. |
| Automatic rollback after verification failure | Autoswitch apply owner. | Verification failure -> `_run_switch` to previous target. | Existing safety path; should remain available under defined containment rules. No explicit breaker semantics. |
| Authority promotion | `v7-users-autoswitch --promote-authority-to`. | Confirmation + evidence + truth check -> policy update. | Not user movement, but it changes future execution authority and does not consume Admin Safe Mode on direct CLI. |

## 4. Gate Coverage Matrix

| Mutation Entry Point | Existing Gate | Gate Source | Checked Immediately Before Mutation | Fail-Closed | Bypass Possible | Tests |
| --- | --- | --- | --- | --- | --- | --- |
| Admin guarded autoswitch | Admin Safe Mode + auth/CSRF/confirm + planner gates | Safe-mode file and request/session state | Safe Mode: no, only before CLI launch; planner live gates: partial | Safe Mode missing state: no | Direct CLI; state change after launch | Endpoint inventory count only for Safe Mode; autoswitch gates extensively tested |
| Direct autoswitch CLI | apply flag, policy enabled, mode, selected moves, envelope, optional L3 gate | CLI, policy, plan, runtime sources | Envelope/L3: yes; global suspension: no | Distributed gates: mostly yes; policy missing: no | Yes | Extensive apply/envelope/L3/restore tests; no breaker tests |
| Scheduled governed L3 | packet, lease, restore barrier, L3 eligibility | systemd command plus governed-cycle state | Live L3 checks occur before autoswitch movement; global suspension absent | L3 unknowns: yes | Safe Mode and direct process control | Governed canary and autoswitch L3 tests; no service-to-breaker test |
| Direct governed L3 CLI | same as scheduled path | CLI + execution owners | Same as above | Same as above | Safe Mode bypass | Governed canary tests; no breaker tests |
| Low-level `v7-user-switch` | Primitive-local validation unknown in repository | Deployed primitive | No proven breaker check | Not proven | Yes, direct CLI | No circuit-breaker contract test found |
| Batch movement | authority/blast/envelope before loop | Plan/policy/runtime state | Global state is not reread before each `_run_switch` | No for emergency stop | State can change during loop without stopping remaining moves | Batch/authority tests exist; in-flight stop test missing |
| Recovery movement | No live mutation yet | Read-only B8/B9/B10/A6 | Not applicable today | Read-only STOP_SAFE | Future apply would inherit autoswitch gap | Recovery read-only tests pass |
| Rollback packet | packet validation and apply flag | Rollback packet/current user state | Packet validation before loop; no global suspension semantics | Packet invalid: yes | Direct CLI and no scoped breaker | Rollback packet tests exist; breaker/rollback-only tests missing |
| Automatic rollback | Verification failure and rollback policy | Apply result and policy | Immediately after failed verification | Safety-path dependent | No explicit breaker distinction | Rollback success/failure tests exist |
| Authority promotion | confirmation, transition, evidence, truth | CLI and existing records | Before policy write | Yes for existing checks | No global operator stop on direct CLI | Promotion denial/evidence/truth tests exist |

## 5. Fail-Closed And Bypass Audit

### Mandatory final gate

```text
ONE_REQUIRED_FINAL_MUTATION_GATE = NO
DISTRIBUTED_EQUIVALENT_COVERAGE = NO
```

Distributed controls are strong for eligibility and identity, but they are not equivalent to a circuit breaker because none represents an operator-controlled suspension state that all mutation paths must consume.

### Confirmed bypass classes

1. Direct `v7-users-autoswitch --apply` bypasses Admin Safe Mode.
2. systemd/governed L3 execution bypasses Admin Safe Mode.
3. direct low-level `v7-user-switch` is an independent primitive bypass unless externally constrained.
4. rollback packet apply does not consume a shared suspension/rollback-only state.
5. a process accepted by the Admin API before Safe Mode is enabled does not recheck Safe Mode before `_run_switch` or between batch moves.
6. direct Authority promotion does not consume the operator stop state.

### Missing, unknown and stale state

- missing/unreadable/malformed Admin Safe Mode data becomes `enabled = false`;
- Safe Mode has no enforced schema, generation, TTL, freshness or stale-state handling;
- missing autoswitch policy inherits `autoswitch_enabled = true`;
- Runtime has no breaker generation bound to packet/lease/authority identity;
- process restart reloads policy and runtime sources, but does not load a circuit-breaker state;
- Admin Safe Mode file persists across Admin restart, yet persistence does not protect non-API execution paths.

This fails the required rule `unknown/missing state = STOP`.

## 6. Operator Control And Persistence Audit

Admin Safe Mode is the correct existing operator surface to reuse:

- owner role required;
- CSRF required;
- exact confirmation required for enable and disable;
- reason, actor and update time persisted;
- previous file backed up;
- state shown in Overview;
- state changes and blocked API attempts audited;
- read-only diagnostics remain available.

Remaining gaps:

- API-only consumption;
- missing state fails open;
- no stale/generation semantics;
- no action-class/channel/user scope;
- no explicit rollback-only/containment exemption;
- no Runtime-facing final check;
- no CPS mirror of active override/suspension;
- no OMP-controlled recovery/clearance lifecycle;
- no proof that direct CLI, systemd or primitive paths cannot bypass it.

The current inactive autoswitch service/timer is a valid temporary containment condition, not a certified kill switch. Read-only truth on 2026-07-11 confirms both inactive and approved manual mode. Runtime/repository convergence is `NO-GO` because Runtime remains at deployed commit `faba686f` while the repository is at `cf1cba0a`; no deploy was performed by this Mission.

## 7. Existing Tests And Missing Tests

Executed without modifying code or state:

| Test set | Result |
| --- | --- |
| Autoswitch, packet/lease, execution pipeline, endpoint inventory | `227 passed` |
| Governed canary CLI | `29 passed` |
| Total | `256 passed` |
| `tools/v7-admin-platform-review --pretty` | `WARN`: 86 Safe Mode blocked actions; 8 action handlers require classification/review |

Existing tests prove Authority budget/freeze, blast bounds, restore barrier, atomic envelope, stale source/lease denial, L3 `STOP_SAFE`, retry limits, packet identity, rollback, verification, and promotion denial.

Missing circuit-breaker tests:

- Safe Mode enabled denies Admin autoswitch apply;
- missing, malformed, unknown and stale breaker state deny mutation;
- direct autoswitch CLI cannot bypass breaker;
- systemd/governed L3 cannot bypass breaker;
- low-level mover cannot be invoked outside the existing execution owner;
- breaker enabled after plan/packet preparation blocks apply;
- breaker change during batch stops remaining mutations;
- restart preserves suspension safely;
- rollback/containment remains available only under explicit safety rules;
- breaker state changes are bound to audit and operator-visible generation;
- every mutation endpoint/CLI is included in an executable coverage test.

## 8. World Responsibility Mapping

Existing V7 world research already establishes the relevant responsibilities; no new external research was required.

| Mature production pattern | Required responsibility | V7 mapping | Status |
| --- | --- | --- | --- |
| SRE emergency stop / automation suspension | Operator can stop automation while preserving diagnosis and learning. | Admin Safe Mode plus OMP/Runtime suspension contract. | `EXISTS_PARTIALLY` |
| Progressive-delivery rollout abort | Abort is consumed before the next mutation, including already prepared rollout work. | STOP_SAFE and verification/rollback exist; no shared final abort state. | `INTEGRATION_GAP` |
| Kubernetes/admission or maintenance controls | Mutation admission defaults closed under unknown policy/state. | Admin API admission exists; missing Safe Mode defaults open and CLI bypasses. | `IMPLEMENTATION_GAP_WITHIN_EXISTING_OWNER` |
| Cloud administrative disable | Durable operator state is visible, auditable and survives restart. | Admin Safe Mode provides visibility/audit/persistence. | `EXISTS_PARTIALLY` |
| Envoy-style circuit breaking | Closed/open/half-open state bounds unsafe action and recovery. | Canonical Runtime Model defines these states; executable state machine is absent. | `IMPLEMENTATION_GAP_WITHIN_EXISTING_OWNER` |
| Network change-control freeze | Policy/Authority can deny or narrow changes independently of planning. | Authority freeze/revoke and action-class bounds exist. | `IMPLEMENTED_DISTRIBUTED` |
| Rollback-only containment | Forward mutation stops while certified compensation remains possible. | Rollback/containment owners exist; shared rollback-only breaker semantics are absent. | `INTEGRATION_GAP` |

World mapping conclusion: V7 already has the correct owner structure and most safety primitives. The missing element is executable final consumption, not a new architecture or Circuit Breaker Engine.

## 9. Gap Certification

| Gap | Certified status | Existing owner route |
| --- | --- | --- |
| No shared suspension state consumed immediately before every production mutation. | `IMPLEMENTATION_GAP_WITHIN_EXISTING_OWNER` | Runtime Model + existing execution/autoswitch owners + Admin Safe Mode. |
| Admin Safe Mode is not consumed by systemd/CLI/runtime apply. | `INTEGRATION_GAP` | Admin operator-control owner -> governed cycle/autoswitch final gate. |
| Missing/malformed state fails open. | `IMPLEMENTATION_GAP_WITHIN_EXISTING_OWNER` | Existing Safe Mode state reader/consumer. |
| No stale/generation/restart contract for breaker state. | `IMPLEMENTATION_GAP_WITHIN_EXISTING_OWNER` | Existing packet/lease/generation owners plus Safe Mode state. |
| No explicit rollback-only semantics. | `INTEGRATION_GAP` | Existing rollback/containment owners and Runtime Model. |
| No direct bypass prevention for low-level mover. | `IMPLEMENTATION_GAP_WITHIN_EXISTING_OWNER` | Existing autoswitch Runtime owner and low-level primitive. |
| Operator visibility exists but CPS suspension state is absent. | `OPERATOR_SURFACE_GAP` | Existing Admin Overview + CPS mirror through OMP; CPS remains non-Runtime. |
| No executable breaker behavior tests. | `TEST_GAP` | Existing autoswitch, governed-cycle, Admin API and packet test owners. |
| Previous report-level suspension wording could be mistaken for executable coverage. | `KNOWLEDGE_GAP` | This report records the implementation distinction; canonical update is deferred. |
| Fundamental architecture gap. | `NO` | Existing owners can legally close every gap. |

Overall certification:

```text
IMPLEMENTATION_GAP
```

## 10. Existing Owner Reuse Plan

This is a Discovery output, not implementation approval.

The minimal next Mission must reuse:

1. OMP for suspension, recovery and scope semantics.
2. Existing Admin Safe Mode as the operator-controlled state and audit surface; no second state owner.
3. Runtime Model and `tools/v7-users-autoswitch` for mandatory fail-closed consumption immediately before each `_run_switch`.
4. `tools/v7-governed-canary-dry-run-cycle` for pre-lease and pre-apply consumption without creating a second execution path.
5. Existing packet/lease/generation contracts to bind prepared work to current breaker generation.
6. Existing rollback/containment owners for explicit rollback-only behavior.
7. Current Program State only as the volatile visibility mirror, never as Runtime truth.
8. Existing Admin/audit/read-model owners for operator-visible state and change history.
9. Existing test owners for deny, unknown, stale, restart, in-flight, bypass and rollback cases.

No new owner, Engine, Runtime, Planner, policy system, truth source, lifecycle, or OMP capability is justified.

## 11. OMP First-Run Safety Verdict

```text
OMP_CONTROLLED_RUN_ALLOWED = NO
```

Exact reason: current scheduler inactivity prevents unattended scheduled movement, but it is process state rather than a mandatory fail-closed execution gate. If the service is enabled or the governed/autoswitch CLI is invoked directly, no operator-controlled breaker is checked immediately before mutation. Admin Safe Mode cannot stop those paths and unknown state fails open. Therefore mutation-capable controlled OMP runs are not certifiable yet.

Read-only OMP runs remain safe because they do not invoke Runtime mutation.

## 12. Next Minimal Step

Prepare a bounded Phase 2 implementation plan and dry run for an existing-owner extension that:

- makes the existing operator stop state fail-closed for missing/unknown/stale data;
- consumes it in governed execution and autoswitch immediately before every forward mutation;
- prevents direct CLI/primitive bypass;
- preserves explicitly certified rollback/containment;
- binds prepared work to breaker generation;
- provides operator-visible/audited state;
- adds complete mutation-path coverage tests;
- performs no production apply until separately authorized.

## 13. Final Verdict

`IMPLEMENTATION_GAP`

`OMP_CONTROLLED_RUN_ALLOWED = NO`
