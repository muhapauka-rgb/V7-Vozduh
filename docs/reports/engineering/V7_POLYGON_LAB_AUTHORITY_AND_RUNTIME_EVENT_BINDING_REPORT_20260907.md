# Isolated Polygon Authority and runtime-event binding

Status: implementation/integration progress, Mission incomplete. No Production
deployment or user-route execution in this block. No S11, full E2E, seven-second
or 1,000/10,000-user claim.

## Changes and evidence

- Existing Authority owner now accepts an explicitly versioned `v2-polygon`
  standing contract. The fresh lab approval cannot reuse the production v1
  approval. Scope binds actual Docker preflight, Linux namespaces, root mount,
  GRE topology, finite CPU/memory, implementation hashes, exact certification
  registry and target inventory. Expiry is 120 seconds. Production v1 remains
  one member and one transaction; current lab scope is five members and one
  concurrent transaction.
- Actual source-down testing exposed an isolation-check defect: a vanished
  default route was misclassified as an external route. Absence is now allowed;
  an actual external-interface/gateway default still denies admission.
- Controlled health now passes the same audit store to Matrix and invokes the
  actual existing governed-canary executor, not the Planner executable in the
  executor position.
- Actual Matrix `V7_HEALTH_RUNTIME` events were rejected by the certification
  binder's external-only comparison. It now reuses the existing reconcilable
  provenance allowlist. Fresh incident/service/current-registry checks remain.
- Real replay: contract `ctm0fsdpc_5ca66ce13d1dded798657093` active before fault;
  source physical GRE-down detected, selector phase became
  `EXECUTE_CONTROLLED_FAILURE_CUTOVER`; five certification members, ordinary
  scope zero. Target still had 14/14 actual Matrix services. All owned
  containers, image and network were removed and their absence verified.
- Focused regression command covered new lab Authority tests, the complete
  health-fast-deadline test module, four existing standing-policy lifecycle
  tests and runtime-provenance binding denial cases: 50 tests passed in 17.246 s.
  Unit fixtures are not E2E evidence. Independent review was not performed in
  this block; Controller provided architectural direction, not a code-review PASS.
- Subsequent Controller decision admitted truthful COLD lab-only measurement,
  not invented 5m/1h history. Existing `v7-client-speed-api` now performs three
  waves of five concurrent TLS-verified 1 MiB downloads through each real GRE.
  Actual replay at 07:10:36Z: 30/30 payloads verified, 30 MiB total, target stream
  rates 330.004105–1071.062830 Mbps for this short offered load. Both long windows
  remain `NOT_OBSERVED`. This is target transport evidence only; not traffic
  from five switched clients, sustainable bandwidth or E2E. No measured-capacity
  evidence was consumed as a Planner/Authority admission grant in that first
  checkpoint; the subsequent integration below changes this boundary.

## Historical boundary at ae2d1b21

The existing target diagnostic returns `no_distinct_controlled_contract_admitted_target`:
the isolated target is reachable and its existing load-policy remaining bound
is nine, but quality current/5m/1h and throughput observations are absent, and
the production availability-first policy is not the new lab Authority. The new
raw prefault payload observations have not yet been bound to admission. These
are distinct missing inputs/coverage, not a failed target network.

Continue in the existing standing Matrix consumer and Planner. Obtain genuine
bounded pre-fault quality/capacity observations, bind approved lab semantics
without inventing history, and carry the entire approved cohort through existing
Candidate/Packet/Lease/Barrier/writer and last-member S11. Do not execute five
independently prepared one-user experiments or restart T0 per member. The source
must stay failed until the real terminal/rollback condition; teardown is not
recovery credit. Production quality floors and ordinary-user routing stay intact.

Actual scheduled re-entry in this same task occurred at 2026-09-07T06:39:26Z;
this proves the restored continuation heartbeat fired, not that the autonomous
engineering Mission or full campaign entry is complete. Architectural questions
and these measured boundaries were sent directly to «Агент Времени».

## Subsequent cold-admission and whole-cohort integration

Fresh lab Authority now binds the actual payload observation, including age,
monotonic time, verified bytes, simultaneous streams, three short rounds and
bounded memory observations. These do not establish CPU headroom, a sustained
load limit or missing 5m/1h history. Existing Candidate gates retain individual
services, organisation, load-policy and safety checks. Advisory snapshot and
alternate incident-Authority selection now recognise the distinct fresh lab
contract; they do not relabel certification identities as ordinary users.

Actual Planner selected all five moves. Strict lab selection binding accepts
only those actual moves and never manufactures them from recommendation rows.
The governed caller carries the same policy/audit paths and exact five-member
scope. Initial lab addresses use 10.7.254.1–5 inside the disposable namespace,
matching existing writer address semantics without changing production rules.
Existing state-json-save and intelligence-snapshot-refresh produce the actual
initial source/snapshot inputs at the consumer's real paths. The canonical
egress library is installed in the disposable image only, not Production.

The next real failure was missing transaction reservation at Packet/Lease bind.
Inspection confirmed the existing two-stage lifecycle: reserve prefault, bind
the actual target/Packet/Lease after T0. The same reservation owner now derives
and protects every member of the validated lab scope in one reservation. Its
lab source-reservation identity is bound to the immutable environment scope,
not a fabricated production provisioning receipt. Target remains unselected
prefault. The consumer compares exact contract/hash, implementation, members
and source fingerprint; duplicate reserve/bind remains idempotent. Guard and
release cover the whole cohort. Production single-user behavior is preserved.

Replay passed the former reservation failure and produced real Packet/Lease
identities. Its sample later closed with zero moved users; neither closure nor
internal sub-second timings establish recovery. Full owner audit rows are now
retained by the adapter to expose the exact downstream refusal before teardown.
Focused regressions: 15 PASS in 0.399 s (lab Authority/observation/cohort reserve,
strict selection, explicit owner paths, original production reservation and
Authority budget regressions). No independent code-review PASS is claimed.

Further live diagnosis found `committed_apply_policy_generation_changed`: the
Apply invocation omitted the selected policy path. It now passes that path;
the unchanged-generation check is retained. Another discovered safety issue
was the old operation-window builder falling back to global CLOSED for an
unsupported cohort. New lab calls require an exact operation scope bound to
fresh current v2 contract/audit/environment/member count and fail instead of
using global fallback. Ordinary/v1 limits are unchanged. Eight additional
existing execution-control/expiry/finalization and actual stale-policy/assignment
regressions passed (0.193 s).

The original Apply channel-evidence consumer understood old state severity or
service-majority failure, not the new HARD-only Matrix observation. In the
validated isolated scope it now consumes the actual certification Matrix
incident and corroborates current kernel IFF_UP down. It does not fabricate
service failures; recovered kernel, missing event, wrong incident and wrong
member deny. The existing L3 incident owner receives these actual move-evidence
rows and derives readiness itself. No READY status is hand-written.

Replay then reached the existing `v7-user-switch` invocation. The disposable
image lacked Runtime PATH/state-dir binding; that is now explicit, including
normal system sbin paths. No Production deployment is implied. The adapter
also waits for the exact transaction terminal, not an earlier healthy-cycle
consumer log, and does not restore the source while its consumer is running.
Actual exceptions retain bounded stack locations in existing diagnostic audit
so safe refusal cannot disappear behind sample-closure status. Final all-member
route execution, S11 and scale remain the required next proof, not a report
or commit terminal.

At the checkpoint, writer code still admits emergency groups only through its
old 2..4 fence. This is the next integration boundary, not permission to widen
Production. A subsequent learning-finalization `None` action-contract exception
also obscured the writer result; the absent-contract read is now safe and a
focused regression covers it. Existing diagnostic evidence retains actual
failed-writer rows. Latest changed-path run: 13 tests PASS in 0.365 s; previous
17-test and eight-test control/stale subsets also passed. No route/S11 success
has been established by any of these tests.
