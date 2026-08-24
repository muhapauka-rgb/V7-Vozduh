# V5.3 Post-HARD_PATH Reconciliation and Independent Frontier

Date: 2026-08-25
Scope: current `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`; existing
owners only. This block changes no Runtime behavior, configuration, cadence,
priority, verification semantics, Planner, Matrix, Authority, routes or
ordinary users.

## Fresh owner-backed state

* Local `Updatesystem` was clean at `be995a46`. Runtime is deployed from
  `dd9dd3d89f296be641651261fd16cd0a26fc20ca`; the local difference is two
  reports only. `v7-truth-check --runtime-readonly` returned
  `RUNTIME_ALIGNED` and `DOCS_ONLY_MISMATCH`.
* `v7-health.service` is active. Its role-based loop owns live Matrix and
  Telegram work. The standalone Matrix and Telegram timers are disabled and
  inactive; no timer was changed. A Matrix subprocess was live at observation,
  therefore disabled legacy timers do not mean absent Matrix work.
* Certification identity `10.7.0.92` is on Planner-selected `awg3`, remains
  `certification_user=1`, and no ordinary user was selected or moved.
* The latest lease is terminal (`APPLIED`, `finished_at` recorded); there is no
  active reservation, Candidate, Packet or Lease to reuse.

## N0–N11 compact map

| Phase | Status | Evidence / dependency |
| --- | --- | --- |
| N0 | DONE | N0–N11 contract exists; this report reconciles stale CPS live fields. |
| N0a | DONE | deployed bounded Runtime envelope (`f42e2908`). |
| N1–N4 | PARTIAL | predicates/tournament deployed; replacement retirement needs integrated proof. |
| N5–N6 | PARTIAL | prepared target/deep fallback exist; exact migration/retirement remains. |
| N7 | BLOCKED | frozen live HARD_PATH distribution fails P95 and max acceptance. |
| N8–N9 | PARTIAL | automatic controlled chain and scale proof exist; later homogeneous live HARD failure overrides SLO credit. |
| N10 | BLOCKED | completion consumes same unresolved post-T0 decision path. |
| N11 | READY_FOR_DISCOVERY | read-only inventory is lawful; deletion requires all replacement-closure proofs. |

`HARD_PATH_RUNTIME_SLO = BLOCKED_OWNER_ARCHITECTURAL_DECISION` remains open.
Frozen valid totals: 2947.173, 3133.279, 4987.290, 4992.034 and 8315.205 ms;
nearest-rank P95 is 8315.205 ms and one valid sample is over 5 s. Dominant
span: T0->decision, 2058.146–7310.806 ms. Apply, kernel and S11 are bounded by
comparison. Source: `2026-08-25_010000_hard_path_slo_architectural_convergence_blocked_frozen_series.md`.

## Independence gate

### Telegram-critical S11

`BLOCKED_BY_HARD_PATH_OWNER_DECISION`. The current Telegram path is Telegram
evidence -> Matrix T0 -> prepared target -> Candidate -> Packet -> Lease ->
Barrier -> Apply -> route-bound Telegram S11. It shares the unresolved
T0->decision boundary, so a new sample cannot prove an independent <=3 s / <=5
s SLO merely by changing failure class. No ordinary outage or ceremonial
controlled sample was created. Re-entry: owner decision on an executable
prepared decision; Telegram keeps its own route-bound verification.

### N10

`BLOCKED_BY_HARD_PATH_OWNER_DECISION`, not blocked by missing operator
approval. Standing policy can govern bounded selection but cannot make the
already failing common performance path acceptable. Ordinary-like/cohort moves
would add risk without resolving the architectural question; existing evidence
is retained without re-running it ceremonially.

## N11 read-only residue discovery

| Responsibility | Classification | Disposition |
| --- | --- | --- |
| `v7-health.service` / `v7-health-loop` | PRIMARY | active role-based producer; retain. |
| Matrix subprocess from health loop | PRIMARY | canonical Matrix path; retain. |
| `v7-telegram-sentinel` from health loop | PRIMARY | profile-required L1T producer; retain. |
| `v7-service-matrix-refresh.timer` | BACKSTOP / BLOCKED_BY_UNFINISHED_REPLACEMENT | disabled but still has tooling/recovery references. |
| `v7-telegram-sentinel.timer` | BLOCKED_BY_UNFINISHED_REPLACEMENT | disabled; repository/install/runtime references remain. |
| `v7-users-autoswitch.timer` | CURRENT_RECOVERY | installed, inactive, still named by governed recovery contracts. |
| draft autoswitch-planner units | BLOCKED_BY_UNFINISHED_REPLACEMENT | no-caller/no-consumer/deployment-state proof absent. |
| Full Matrix | FALLBACK / DEEP_BACKGROUND | ambiguity, stale/conflict and disagreement protection; retain. |
| `pre_planner_refresh` | CURRENT_RECOVERY | fail-closed freshness path and measured residual; retain. |
| prepared-decision projection | PRIMARY / INCOMPLETE_HANDOFF | N5 primitive; evaluate promotion, not deletion. |
| terminal Packet/Lease/reservation records | CURRENT_RECOVERY HISTORY | immutable closure evidence, not active state. |
| reports and fixtures | PRESERVED EVIDENCE | needed for decision; no Runtime caller claim. |

No item has all six deletion preconditions (replacement, migrated consumers,
fallback window, no caller, no consumer, no state dependency). N11 therefore
performed no destructive change.

The direct unit inventory confirms the classification: the standalone Matrix
and Telegram timers are disabled, while `v7-health.service` is enabled and
active and invokes both tools as role children. The install script and the
freshness/diagnostic contracts still name the disabled timer family; deleting
the unit files would therefore leave executable-looking reinstatement and
truth-check consumers inconsistent. The exact N11 result for this block is
`NO_SAFE_DELETION_ADMITTED`.

## Verification

* `v7-truth-check --runtime-readonly`: `RUNTIME_ALIGNED`; deployed Runtime
  commit `dd9dd3d89f296be641651261fd16cd0a26fc20ca`; documentation changes do
  not require deploy.
* Direct read-only Runtime observation: health active, standalone Matrix and
  Telegram timers disabled/inactive, no active governed transaction, and only
  the certification identity in the observed controlled result.
* Focused owner-bound regression set: 54 passed:
  `tests.unit.test_v7_health_fast_deadline_loop`,
  `tests.unit.test_telegram_sentinel_lock_scope`, and
  `tests.unit.test_v7_truth_check`.
* Remote branch verification: `Updatesystem` contains
  `41626c0d8c5871c65498cb8f853a876fc6fb559e`.

## HARD_PATH owner-decision package

### A. Executable N5 handoff

Potentially, but not with the present path. `AutoswitchPlanner.plan` looks up
the prepared projection, yet still constructs the Planner and performs owner
discovery, snapshot refresh, policy/capacity resolution and per-user decision
construction. Prepared lookup is about 5 ms, while T0->decision is 2058–7311
ms. A future admitted change must make a fresh exact prepared handoff an
existing-owner executable input without rebuilding the world.

### B. Mandatory synchronous checks

Keep fail-closed Matrix provenance/freshness/generation, source/identity
scope, immutable Packet/Lease/Barrier identity, current assignment,
policy/Authority generation, target role/capacity/service freshness, and
route/kernel plus failure-class-specific S11. Broad inventory/history and
candidate reselection are candidates for removal only after an admitted proof.

### C–E. Measured envelope

Potentially precomputable work: stable snapshot construction, broad inventory
reads and policy/capacity projection, each guarded by generation invalidators.
Never precompute stale health truth, target freshness, Authority, assignment or
final safety gates. Existing downstream spans: decision->Apply 82–121 ms,
Apply->assignment 337–565 ms, assignment->kernel 16–26 ms, kernel->S11
383–518 ms; combined observed envelope 0.82–1.23 s. The 2-vCPU substrate does
not disprove <=3 s (one cold sample was 2947.173 ms), but the 8315.205 ms warm
sample means it is not currently a credible SLO. Compute expansion must not be
assumed to cure a semantic handoff.

### F. Required choice

Choose explicitly: (1) admit a bounded existing-owner prepared-decision to
Apply architecture and remeasure on 2 vCPU; (2) retain current architecture
and accept the blocker; (3) assess more compute only after (1); or (4) change
the product SLO through an owner decision. No option was selected here.

## Legal frontier

1. Owner decision on the executable prepared-decision handoff.
2. Continue N11 discovery; remove only an independently closed responsibility.
3. After decision, run separate Telegram S11 and N10 proof; never reuse
   HARD_PATH samples as Telegram evidence.

## Independent-frontier reconciliation terminal

Terminal for this block:
`HARD_PATH_OWNER_DECISION_REQUIRED_AFTER_INDEPENDENT_FRONTIER_CONSUMED`.

All presently lawful independent work in this prompt has been consumed:

* HARD_PATH has been frozen and packaged rather than patched;
* Telegram and N10 have a demonstrated shared dependency and cannot receive
  misleading independent credit;
* N11 discovery found no responsibility eligible for deletion;
* final Runtime read-only reconciliation remains `RUNTIME_ALIGNED` with a
  docs-only local mismatch and no deploy requirement;
* health is active, legacy standalone Matrix and Telegram timers remain
  disabled, the observed lease is terminal, and the only affected identity is
  the certification identity on `awg3`.

The exact next action is the owner architectural decision in section F. No
further safe implementation, rollout, Telegram proof, N10 progression or N11
deletion exists without that decision.
