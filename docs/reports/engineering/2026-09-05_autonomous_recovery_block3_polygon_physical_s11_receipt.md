# V7 Autonomous Recovery — Block 3 Polygon Physical-S11 Receipt

Date: 2026-09-05
Scope: existing `CAP-U06` Permanent Polygon / Future Scale / BDP / OMP owner path only.

## Outcome

The initial local receipt-assembler was rejected and disconnected from CAP-U06.
The corrected path extends the existing
`execute_routing_digital_twin_l3_l4_obligation` Docker Polygon owner only. It
is isolated L3/L4 engineering evidence, never a Production recovery claim.

## What was verified

- Existing Docker Polygon owner passed all 18 L3/L4 checks: internal labelled
  network, `tc` fault, real HTTP failure, route observation, rollback,
  recovery, containment, limits and orphan cleanup.
- The content-addressed immutable receipt
  `autonomous-recovery-docker-repair-95ed44e73d8a66f80fc0e488.json`
  binds one intentionally seeded CJS legacy-origin STOP_SAFE trace to its derived BDP
  candidate `BDP-ICI-8BBC01B30C464F526E532247`, admitted OMP mission
  `V7_OMP_AUTONOMOUS_RECOVERY_DOCKER_RECEIPT_REPAIR_V1`, actual current-ESM
  owner repair, cleanup, and a second same-contract current-ESM replay.
  Both repair and replay contain ordered 1K then 10K real HTTP receipt sets,
  successful `tc loss 100%` fault observation, rollback, kernel route
  observation, unique receipt hashes, a fail-closed seven-second terminal gate,
  and removal of containers, network, and disposable image. The repair/replay
  contract fingerprint equals the stored origin contract fingerprint. The
  existing `mission_completion_evidence_gate` is consumed with
  `COMPLETE_CONSUMED`; the OMP material-change consumer then records
  `mission_executed: true`.
  Its filename prefix and embedded `artifact_fingerprint`
  `95ed44e73d8a66f80fc0e48860ab3a681c6766102711e0ce5fbfa0038394abea`
  are the canonical semantic-payload identity defined by the owner; they are
  not a hash of the serialized JSON file.  The whole-file byte SHA-256 at
  verification time is
  `97fbc592d2616759778aaebfa43827521cb5efad40e381223a7c0d13db0e91b7`.
- `python3 -m unittest tests/unit/test_permanent_polygon_autonomous_program.py tests/unit/test_autonomous_recovery_agent_profile.py`
  completed: `Ran 17 tests ... OK`.
- `python3 tools/v7-truth-check --json --omp-permanent-polygon-repair-return`
  completed with PASS.  CAP-U06 retains its original read-only B8/B9/B10/A5
  contract; the local guard is not consumed by that result.

## Independent rejection and exact re-entry

The reviewer rejected the initial linkage for five concrete reasons:

1. `monotonic_ns()` was a process timestamp, not an isolated channel fault
   injection timestamp.
2. The loop fabricated `S11` records rather than consuming a required-service
   S11 / route-kernel owner.
3. BDP/OMP admission did not execute a real owner repair Mission.
4. The replay comparison omitted individual terminal-time/receipt identities.
5. The 10K loop was logical, not a capacity-bounded cohort recovery execution.

The earlier `POLYGON_SUBSTRATE_LIMIT` was a Reviewer sandbox artifact. Outside
that sandbox, Docker `28.4.0` is available and the existing probe returns L4.
The receipts remain limited to `ISOLATED_DOCKER_L3_L4_REQUIRED_SERVICE_HTTP_RECEIPT`:
they are not a normal V7 Runtime sample, not Production S11, and do not change
Runtime, Production, Authority or Maturity.

The final independent reviewer accepted the current-source artifact as bounded
Block 3 engineering evidence. A separate Codex CLI reviewer session returned
no final message or output artifact and is not counted as evidence.

The staged equivalence re-entry subsequently bound the existing
`operator_execution` 1,000/10,000 app-level candidates to two real Docker
target representatives per stage. Each representative carries the exact class
generation, class and Packet fingerprints, target membership-subset identity,
namespace route fingerprint and required-service HTTP S11. Fresh measured
results were `2598.430 ms` for 1,000 and `4833.232 ms` for 10,000. The consumer
published engineering Polygon scopes `[1000, 10000]` while keeping Production
certification delta `0` and Authority/Runtime/Production `NONE`. Cleanup left
zero containers/networks and removed the temporary image. Four focused
negative tests cover missing target representative, forged fingerprint, stale
generation and shared-capacity breach; all passed.

The same owner now executes and consumes the complete bounded Program fault
catalog: channel off, tunnel/route loss, required-service failure, combined
delay/loss degradation, correlated and independent multi-channel failure,
process restart, stale generation, wrong target, insufficient capacity,
mid-switch interruption and rollback/re-entry. Four reproducible
coverage-directed combinations carry immutable scenario fingerprints. The
fresh catalog run passed all 12 classes; measured staged terminals were
`2706.796 ms` and `5335.418 ms`. Cleanup again left zero containers and
networks and removed the lab image.

The final local C-J repair/replay acceptance also passed. A real legacy
executor failure produced an existing BDP Candidate and accepted OMP Mission
`V7_OMP_AUTONOMOUS_RECOVERY_DOCKER_RECEIPT_REPAIR_V1`; the current owner repair
then passed at `2614.430 ms` / `5234.337 ms`, and exact replay passed at
`2834.335 ms` / `5142.990 ms`. Both repair and replay consumed the complete
fault catalog, the OMP material-change completion gate returned PASS, and both
Docker generations left zero containers/networks and removed their images.
The compact bundle now calls this real repair/replay owner instead of the old
read-only fixture and gives its fault-catalog certification to the independent
Reviewer. No daemon, watcher, queue, Production mutation or Authority expansion
was introduced.

The material-change/background gap is now entered only through the existing
`continue_omp_engineering_control_loop`, not through a watcher, daemon, or
direct bundle helper call. The loop derives comparable Git-HEAD/current byte
identities, captures the real CPS generation, rechecks it before and after the
bounded Polygon run, and selects the non-recursive Permanent Polygon runner.
It reuses the existing OMP external-reentry lease and historical-evidence
writer; there is no `.codex-build` journal or new registry. A duplicate is a
truthful no-execution receipt, not a fabricated lease/work claim. Malformed
history, stale generation, invalid budget, unavailable substrate, active lease
and runner failure all fail closed with `finally` lease cleanup.

The final `autonomous_recovery_section8_completion_binding` extends the
existing Mission Completion Evidence Gate. It rejects an interim
`CONTINUE_SAME_MISSION` profile unless every Section 8 outcome has its exact
packet, Docker/physical-S11, catalog, scale, BDP/OMP seed/replay,
native-review and OMP-continuation evidence fingerprint. It cannot close on a
boolean-only helper result. The compact bundle now calls Continue OMP exactly
once and supplies its resulting immutable material-change receipt to this
binding. Twenty focused profile/equivalence tests pass, including caller
reachability, duplicate/no-second-run, lease contention, stale reread,
malformed evidence, failure cleanup, and the assertion that an interim native
profile cannot be mistaken for Section 8 completion.

The compact bundle terminal was additionally corrected: only a final Section 8
`PASS` returns exit `0`; `CONTINUE_SAME_MISSION` and every failure remain
nonterminal/nonzero. The compact truth-check path has an isolated regression
test proving that it consumes bundle `PASS` and converts a nonzero continuation
result to `STOP_SAFE`. Twenty-one focused tests pass after this correction.

## Current residual

The origin is a deliberately seeded legacy executor fault, not a naturally
discovered Production defect. The chain is engineering-only and does not create Production S11, a V7 Runtime
sample, Authority credit, CPS projection, or maturity promotion. No fresh
`AUTONOMOUS_RECOVERY FULL_CAMPAIGN` was run after this contract change; that
fresh execution and its independent acceptance remain required. Any later
finding must retain this evidence boundary and cannot relabel a Docker receipt
as Production evidence.

## Fresh compact-command attempt — unaccepted infrastructure terminal

One fresh `tools/v7-truth-check --json AUTONOMOUS_RECOVERY FULL_CAMPAIGN`
was started after the terminal-contract audit. The first sandboxed invocation
stopped before Analyst dispatch because the native Codex CLI could not open its
local state DB. The same single command was then retried with the required
local native-context access. Its actual `v7-truth-check`, bundle, and one
read-only Analyst process remained active for the bundle's 900-second Analyst
budget, then exited before any Docker/BDP/repair phase.

The execution transport did not retain the completed command's stdout or exit
status. This report therefore does not infer an exact result beyond the
observed bounded native-Analyst failure: there is no new
`autonomous-recovery-docker-repair-*.json` artifact and no live campaign,
bundle, or native-context process. No Section 8 outcome is credited; no CPS,
Runtime, Production, Authority, or user effect occurred. The exact re-entry
condition is an existing native-context runner that returns and retains the
Analyst JSON/exit receipt; only then may the compact command be rerun through
the same OMP profile.

## Native transport repair and fresh smoke acceptance

The existing bounded OMP profile adapter was extended; no Agent System or new
owner was introduced. Native roles keep `read-only` project authority and use
the already authenticated local Codex runtime only as non-canonical transport
state. A clean disposable `CODEX_HOME` was rejected because it is not
authenticated and copying credentials is prohibited.

Each role now returns a `v7.native-context-attempt-envelope.v1`: command-policy
identity, immutable-packet fingerprint, exit/timeout, thread-start/final-message
observation, output fingerprints and redacted bounded excerpts. The outer
truth-check retains its own bundle envelope even if the bundle times out or
cannot emit JSON. The full outer budget is 1710 seconds, exceeding the bounded
role/Docker composition (1650 seconds); there is no hidden 900-second terminal.

The first real smoke exposed an invalid response schema after a valid native
thread start. The exact terminal was `STOP_SAFE_NATIVE_DISPATCH_EXIT`; the
envelope retained the API diagnostic. After correcting the schema, the real
compact command `tools/v7-truth-check --json AUTONOMOUS_RECOVERY NATIVE_SMOKE`
passed: `PASS_NATIVE_SMOKE`, fresh thread
`01a0710c-3ee1-7dc3-90b7-b0a643b24018`, exit `0`, observed final strict JSON,
native attempt fingerprint
`158361ea73fe5c5ab5349cd37a066f76816254a48ac1c0dfd3dc6a30f4868e81`, and
outer bundle-output fingerprint
`82fbed7556898526f9adb6ff098e69f222e4c1577a0eb92899c2cba9f026ef98`.
The smoke did not run Docker or mutate CPS, Runtime, Production or Authority.
It accepts only transport observability; Section 8 remains open.

The blocked acceptance-audit gaps were then closed through the real adapter,
bundle JSON and compact truth-check parser with bounded controlled subprocess
event streams. Eight negative paths now retain both envelopes and remain
`STOP_SAFE`: runtime access denial, timeout, missing `thread.started`, missing
final message, malformed final JSON, saved/event output mismatch, immutable
packet-fingerprint mismatch and strict-schema failure. No negative result has a
Section 8 completion field or terminal credit. The local parser now repeats the
strict response and packet binding validation after CLI transport parsing, so a
substituted stream cannot depend solely on remote schema enforcement.

After that parser change, fresh real smoke passed again: `PASS_NATIVE_SMOKE`,
native thread `01a07112-d01b-7732-809a-46e58912063b`, exit `0`, native attempt
fingerprint `a2142102ccbe965ca7e97d58f1664402e1800a6c4544af33431b23de140b1e3e`,
and outer output fingerprint
`2ca865d6d9a029ab5e9dd79d7a8f4f3c7378a944bbc340f0537561ca2b2cebb4`.
This remains transport-only evidence; it authorizes neither a Section 8 claim
nor Docker/Production/Runtime/Authority action.

## One fresh full campaign — reviewer STOP_SAFE

Exactly one fresh `tools/v7-truth-check --json AUTONOMOUS_RECOVERY
FULL_CAMPAIGN` was then executed through the accepted transport. The outer
command exited `2` after `137867 ms` with
`STOP_SAFE_AUTONOMOUS_RECOVERY_ARTIFACT_CONSUMPTION`; no deploy, commit, push,
CPS, Runtime, Production or Authority effect occurred.

All three native roles completed with observed fresh contexts and exit `0`.
The existing isolated owner chain also produced valid physical receipts:
`1000` members completed in `2595.312 ms` and `10000` in `5086.439 ms` from
`T_PHYSICAL_FAILURE` to last required-service S11. The result marks the
multi-fault catalog, distinct seeded repair/cleanup/replay, owner-consumed
material continuation, compact contract, no-user-relay, physical S11 clock and
scale/capacity law as passed. It gives no Production or ordinary-failover
credit.

Section 8 is nevertheless `STOP_SAFE`: the only unmet outcome is
`NATIVE_ANALYST_CRITICAL_EXECUTOR_AND_INDEPENDENT_REVIEW_CONSUMED`. The
independent Reviewer rejected all four sections with exact invariants:

- Architecture: fingerprints/asserted verdicts are not inspectable proof of
  owner, caller, consumer or closure path.
- Safety: read-only authority and missing safety-regression evidence cannot
  substantiate a repair PASS.
- Evidence: fingerprints alone do not prove execution, Runtime/Production
  state, latency-SLO observations, convergence or user effect.
- Mission integrity: `CONTINUE_SAME_MISSION` explicitly forbids a final closure
  claim.

The full command's complete raw result was captured by the local Codex command
record, but its large historical display aggregation is not a parseable project
artifact. This is an output-retention limitation to repair through the existing
profile adapter before another full campaign; it does not invalidate the exact
`STOP_SAFE` terminal above.

## Reviewer evidence-contract correction — not a new campaign

The `STOP_SAFE` identified a real contract gap: an independent Reviewer had
only fingerprints and asserted outcome labels, so it could not inspect the
current producer, current consumer, or execution path.  The existing
`AUTONOMOUS_RECOVERY` execution profile now supplies a compact immutable
`v7.autonomous-recovery-engineering-review-evidence.v1` contract.  It binds the
current OMP consumer (`continue_omp_engineering_control_loop`), material-change
trigger, Docker-origin/BDP/repair/replay states, material receipt and seeded
repair/replay.  A documented capability without that current caller/consumer
path remains `STOP_SAFE`.

The Reviewer receives this exact evidence contract, must echo its fingerprint
and the sole lawful scope `ISOLATED_POLYGON_ENGINEERING_ONLY`, and is still
required to reject missing owner/caller/consumer proof.  Its strict schema and
the Section 8 binding reject a missing or tampered fingerprint/scope.  The
scope expressly forbids claims of Runtime, Production, user effect, or Section
8 closure; those were invalid requirements for the isolated engineering
Polygon, not evidence gaps to be fabricated.

The existing historical evidence writer also now persists, on a later campaign,
a bounded redacted `v7.autonomous-recovery-campaign-evidence.v1` artifact under
`docs/reports/evidence/`.  It contains terminal state, compact Section 8
receipts, review bindings and native attempt identities, but never prompts,
agent-message excerpts, or complete raw native output.  This is an immutable
historical receipt, not a new registry, OMP/CPS writer, Runtime writer, or
Agent System.

Verification after the correction: 27 focused Autonomous Recovery profile and
equivalence tests passed, including the old fingerprint-only rejection,
positive owner/caller/consumer evidence, tampered evidence/scope rejection,
strict Reviewer schema, and redacted artifact idempotency. `py_compile` and
`git diff --check` passed. A broad existing product-evidence/Polygon batch was
stopped after one test process remained nonresponsive for more than four
minutes; it supplies no acceptance credit and is not represented as passing.

The required actual read-only `NATIVE_SMOKE` then passed through the corrected
transport: `PASS_NATIVE_SMOKE`, native context
`01a0712a-e7a9-7e12-bb83-15708305f34c`, inner attempt fingerprint
`dd0ee7b51cce6ce36ffc9fee5832d7db806aa465a37c1e1b8d00a3588890dad2`, and
outer stdout fingerprint
`67203d081a7e97013c34cc91719389adaf529ebf3abce92b16af7c79061285f9`.
The first sandboxed smoke correctly stopped safe because the Codex CLI could
not write its own state DB; the same read-only smoke in its required local
transport state passed. Neither attempt changed CPS, Runtime, Production,
Authority, or user state.

No second `AUTONOMOUS_RECOVERY FULL_CAMPAIGN` was run. The exact re-entry is a
fresh independently accepted campaign through this corrected existing OMP
profile, with its resulting bounded historical evidence artifact. Until that
run, Section 8 and every Runtime/Production/user conclusion remain unaccepted.

## Fresh corrected FULL CAMPAIGN — Section 8 accepted in engineering scope

One fresh `tools/v7-truth-check --json AUTONOMOUS_RECOVERY FULL_CAMPAIGN` was
then run through the corrected profile. It exited `0` with
`AUTONOMOUS_RECOVERY_SECTION8_FULL_COMPLETION_CONSUMED`. Its bounded immutable
historical receipt is
`docs/reports/evidence/autonomous-recovery-campaign-4fbf83c55a97cfa4f6712c18.json`
with artifact fingerprint
`4fbf83c55a97cfa4f6712c1872445468b907108268c06fd005b86937f0b73ff5`.

All ten Section 8 outcomes are `PASS`: compact contract, exact current
obligation, isolated multi-fault Polygon, native Analyst/Critical
Executor/independent Reviewer, existing-owner seeded repair, automatic origin
replay, physical S11 bound, scale/capacity law, no manual relay, and
owner-consumed successor/terminal. The Reviewer artifact is bound to evidence
fingerprint `5748d3a72ac4cbe28e735025acd5aa784a749375cf9af8b8b9a5edfa18fd8a36`
and scope `ISOLATED_POLYGON_ENGINEERING_ONLY`; Architecture,
Safety/Regression, Evidence and Mission Integrity all returned `PASS`.

The isolated Docker repair receipts measured `2753.913 ms` for 1K and
`5019.917 ms` for 10K from physical fault onset to final required-service S11;
same-contract replay measured `2741.123 ms` and `5094.389 ms`. Each is under
seven seconds. These are isolated engineering receipts only, not Runtime or
Production SLO samples.

Native contexts were observed and completed with exit `0`: Analyst
`01a07130-e7fc-7ad2-baec-caafba1f63e2`, Critical Executor
`01a07131-9bea-7f52-a2f2-b2fb9be38713`, and independent Reviewer
`01a07133-41a2-7be0-8a52-9af08af4fecc`. The campaign records
`runtime_impact=NONE`, `production_impact=NONE`, and `authority_impact=NONE`.
There was no commit, push, deploy, CPS projection, Production action, or user
effect.

The next acceptance action is a fresh independent read-only review of this
campaign artifact and its referenced isolated receipt identities. It must
confirm the artifact-to-owner chain and scope boundary before any publication;
it must not reinterpret this engineering acceptance as Runtime, Production or
user acceptance.
