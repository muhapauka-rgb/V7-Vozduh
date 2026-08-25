# Polygon reseed and group-binding safety boundary

## Scope

This block continued the frozen HARD-path measurement work only far enough to
restore an isolated one-user controlled substrate.  No ordinary user was
selected, moved, or routed.

## Findings and applied fixes

The healthy execution-reserved Polygon source was excluded from empty-pool
reseed even though it already carried the explicit certification-source,
reservation, and ordinary-user fences.  The existing owner was corrected to
recognise that exact marked source as a source only, never as a controlled
destination or ordinary target.  The bootstrap request was also corrected to
read its existing compact candidate projection.  Finally, incremental identity
capacity is now calculated on the exact selected source rather than from a
different source's certification count.

Published and deployed commits:

- `79d9be20` — reserved certification Polygon source reseed;
- `5e385b32` — existing compact candidate projection consumed for reseed;
- `6b7197c5` — identity capacity bound to the exact source;
- `dc1b4840` — one-user provisioning uses the source-owned certification
  group and fails closed when that group is absent.

Focused regression checks passed for the source/target separation, empty
source reseed, exact-source capacity, source-group requirement and one-user
preflight.  Each commit passed `tools/v7-safe-deploy`; the final deployed
Runtime, local branch and GitHub `Updatesystem` aligned at `dc1b4840`.

## Production / Polygon observation

The existing provisioner created exactly one certification-only synthetic
identity on `amneziawg-exec-20260528-10-8-1-14` and recorded
`IDENTITY_POOL_PROVISIONED_AND_CLASSIFIED`.  Aggregated evidence after the
operation: one enabled certification identity on that source and zero ordinary
users moved.  No Candidate, Packet, Lease, routing mutation, or production
maturity change was created by the substrate operations.

The first historical provisioning had assigned a request-specific group while
the isolated source retained its prior group.  The deployed correction prevents
that mismatch for all future provisions.  The already-created synthetic identity
must be reconciled to the source's current reservation group before it can enter
the controlled hard-path transaction.

## Safety boundary

The existing `v7-egress-set-state certification-reserve` owner correctly
requires an exact current reservation id, expiry and egress fingerprint before
it may update the isolated source's certification group.  A subsequent attempt
to apply hard-coded values was rejected by the execution safety boundary:
the currently supplied id and expiry were not independently confirmed as the
current reservation contract.  No state was changed by that rejected attempt.

## Exact next step

Re-read the current source line through the existing reservation owner and
obtain an explicit approval for the current reservation id/expiry pair, then
use that owner to reconcile the source group with the one synthetic identity.
Re-run `--ct-m0f-standing-source-selection`; only if it returns ready, continue
with a single cold controlled HARD-path sample on the frozen implementation.

## Addendum: current group reconciliation and exact-client readiness

The source reservation was subsequently reconciled through the existing
`v7-egress-set-state certification-reserve` owner.  The single synthetic
identity `10.7.0.124` now belongs to the current certification-only group on
`amneziawg-exec-20260528-10-8-1-14`; the owner recorded zero user moves and
zero route changes.

The existing target-selection owner then chose `awg3` automatically from a
fresh one-shot diagnostic.  Its shared-target, one-synthetic-user policy was
explicitly admitted and records zero ordinary-user effect.  No target was
chosen manually.  A separate dedicated-draft attempt stopped safely because
the requested draft would duplicate an unhealthy interface configuration; no
draft, client or route was created from that stopped branch.

The governed controlled-condition owner next stopped before injecting a
failure: its isolated client-session handshake did not complete.  Diagnostics
proved two retained-profile mismatches in the runtime-only Polygon fixture:

- the client namespace was trying to reach the public endpoint from an
  isolated host-local veth; and
- the retained synthetic profile's peer public key did not match the live
  canonical `wg0` ingress key, so WireGuard correctly rejected the handshake.

Commit `2062e171` corrected the first mismatch by directing only the temporary
namespace's outer UDP packet to the host-side veth gateway.  Its focused test
suite passed (19 checks) and the published/server checksum aligned.  Commit
`74b860b7` then made the temporary namespace copy use the current canonical
ingress public key.  The stored profile, service configuration, ordinary
clients, Matrix, Planner and routes were not modified.

That second deploy exposed one final fixture-only fault.  A five-second
packet trace proved that the server response was emitted, but was delivered
to a different, stale Polygon namespace because every fixture reused the same
`169.254.253.0/30` link.  The current pending correction assigns a stable,
different link-local /30 from each exact synthetic identity.  It therefore
prevents one stale prepared namespace from capturing another identity's reply;
it does not alter an ordinary-user route or any canonical runtime state.

## Current next step

Publish and safely deploy the tested per-identity fixture-link correction,
re-run the exact-client preparation, and only on a successful handshake issue
one governed cold controlled condition.  If preparation remains invalid, stop
before injecting a failure and record the new exact evidence.

## Terminal finding for this execution block

The per-identity fixture-link correction was published and safely deployed as
`f628fbe3`; focused verification passed 20/20.  Exact client preparation then
succeeded in 264.019 ms with no canonical state creation, route mutation or
ordinary-user effect.

The next governed step safely stopped before injecting the controlled failure.
The synthetic identity is registered on the isolated source with policy table
`1122`, but that Linux table does not exist and its route lookup falls back to
the public interface.  This is not a Matrix, target-selection or client-tunnel
failure.

The cause is an ownership gap in the current implementation: the existing
production-only `v7-user-create-from-ipam` owner creates and registers a
client, and explicitly leaves routing to V7, while the sole existing route
writer (`v7-user-switch`) correctly refuses any call without a complete
operation-scoped execution-control contract.  The current Program has no
admitted operation that binds an already-registered certification identity to
its initial source route.  Bypassing the route writer manually would violate
the Program's owner and safety rules.

No controlled failure was injected.  No Candidate, Packet, Lease, barrier or
ordinary-user route was created or changed in this block.  The certification
scope marker was refreshed only for the one synthetic identity.

### Required architectural decision

Add one bounded **initial certification source-binding** transition to the
existing governed certification/substrate lifecycle.  It must reuse the
existing `v7-user-switch` writer and its operation-scoped control/verification
contract, create the policy rule and default route only for the already marked
one-user certification identity, and fail closed/clean up on every failure.
It must not be a new route writer, timer, Planner, Matrix owner or direct shell
bypass.  After that transition is implemented and deployed, the exact next
action is one fresh cold governed HARD-path sample.

## Consumed bounded repair

The required transition is now implemented inside the existing governed
certification lifecycle as `INITIAL_CERTIFICATION_SOURCE_BINDING`.  It invokes
only the existing `v7-user-switch` route writer with an operation-scoped
execution-control window created by `admin_core/operator_execution.py`.
Before the writer runs it proves the exact one-user certification class,
group, isolated enabled source, zero ordinary occupants and both current
registry-row fingerprints; it re-reads the two rows immediately before apply.
The writer's normal post-apply route verifier remains mandatory, and the
operation window is always finalized back to its safe terminal state.

Focused tests cover the success path and prove that the only writer command is
`v7-user-switch <exact synthetic IP> <exact source>`.  The next live step is
safe deployment, runtime-alignment verification, one exact client preparation,
then one cold governed HARD-path transaction.

## Initial source binding: deployed evidence and self-contained cleanup

Commit `a53b57af` deployed the bounded binding through `tools/v7-safe-deploy`.
The local, GitHub and Runtime checksum of `v7-governed-canary-dry-run-cycle`
matched (`2649c95c…6141f`); `v7-health.service` remained active.  The focused
suite passed 161/161.  No standalone Matrix or Telegram timer was enabled.

The isolated certification identity `10.7.0.124` was then bound through the
sole route writer to its registered source `v7execwg0` / table `1122`.
The source was deliberately made unavailable through its existing owner; the
system selected `awg3` automatically and completed the governed Candidate →
Packet → Lease → Apply chain.  Exact route and target-bound required-service
verification passed.  The only moved identity was the synthetic certification
identity; ordinary-user delta was zero.

The cold sample is functionally valid but not an SLO pass:

| interval | measured |
|---|---:|
| failure evidence → decision | 4759.137 ms |
| decision → apply admission | 120.151 ms |
| apply → assignment | 932.421 ms |
| assignment → kernel path | 20.665 ms |
| target payload ready | 878.478 ms |
| total evidence → S11 | **6710.852 ms** |

It therefore exceeds both the 3-second goal and the 5-second single-sample
ceiling.  Per the frozen-series law, this evidence is retained and no
performance patch was derived from it.

Cleanup exposed one bounded lifecycle omission: re-enabling the isolated
source did not automatically consume the already-existing Matrix local
recovery writer, leaving the former `NOT_STARTED` liveness observation in
canonical state.  The existing recovery owner was used once to reconcile the
live transaction; it produced `CANONICAL_RECOVERY_WRITTEN`, and the existing
governed cleanup then returned the synthetic identity to `v7execwg0` with an
exact route check.

The same omission is now repaired in the controlled cleanup path: after a
successful source enable, it calls the existing
`v7-service-matrix-test --direct-local-recovery` owner, re-reads the canonical
Matrix and registry, and only then permits the existing governed return move.
It fails closed on either recovery-write or registry-reconciliation failure.
This introduces no owner, timer, Matrix architecture, Planner, route writer
or parallel truth source.

## Current frontier

Safely publish and deploy this cleanup-only repair, prove the deployed hashes,
then create at most two additional immutable-fingerprint controlled diagnostic
samples.  Since the first valid frozen cold sample already exceeds 3 seconds,
do not perform any further performance micro-patch.  After the bounded
diagnostic set, emit the full distribution and the smallest remaining
architectural choice.

### Post-deploy re-entry result

Cleanup repair `bf83e100` was published and deployed as
`deploy-z8-14-Updatesystem-bf83e10-20260825T184305`; safe deploy and truth
checks passed, `v7-health.service` is active, and the Runtime checksum of the
changed canary tool is `e31d6078…f17d`.  The synthetic identity is back on
its isolated source (`v7execwg0`, table `1122`).

The next sample was intentionally not injected.  The existing automatic
selection owner returned `STOP_SAFE`: it has no distinct admitted target while
the source is healthy, even though fresh Matrix rows show both `awg0` and
`awg3` healthy (14/14 required services).  Its current law requires an active
source-failure binding to admit a target, while the controlled transaction
requires an admitted target before it may create that failure.  This is a
deterministic preparation-cycle gap, not a channel-health failure and not an
external limitation.

The smallest safe next repair is therefore confined to the existing prepared
Matrix/Planner selection owner: for an already-authorized, one-identity
certification transaction only, consume its fresh prepared target contract
before failure injection.  It must retain automatic target choice, all
freshness/capacity checks and zero ordinary-user scope; no manual target
argument, general Planner widening or ordinary route change is admissible.

The root cause was narrowed further: the signed existing availability policy
stores its action scopes inside `policy`, while this one preparation reader
accepted only the normalized representation.  The repair accepts both forms
of the same validated decision; it does not grant, widen or write policy.

One final caller defect was also removed: without an explicitly supplied
prepared projection, the CLI passed an empty placeholder and thereby
suppressed its own existing target diagnostic.  It now passes no projection in
that case, so the selector obtains a fresh owner-backed diagnostic itself.

## Warm controlled evidence after target-preparation repair

The repaired selector automatically admitted `awg3` for the sole synthetic
identity.  A single shared fresh diagnostic was supplied to preparation, so
the source/target decision did not drift between selection and failure
creation.  The controlled failure, Matrix consumption, governed recovery and
baseline reset all completed with zero ordinary-user delta.

The warm sample is functionally valid and remains a performance failure:
`control_plane_and_kernel_path_cutover_latency_ms = 6064.355`; the dominant
interval is `failure_to_decision_latency_ms = 5096.479`.  In contrast,
decision-to-apply was 72.831 ms, assignment commit 442.656 ms, kernel
visibility 19.270 ms, and target payload 433.119 ms.  It is therefore retained
in the frozen distribution and no micro-patch is inferred from it.

## Admitted decision-path acceleration

The measured dominant interval is before decision binding, while route apply
and kernel visibility are already short.  The existing Matrix prepared-decision
handoff is now consumed automatically only for an exact one-user governed
synthetic transaction with source, target and one-user budget already bound.
It still re-reads the fresh Matrix projection and falls back to the unchanged
full Planner on any missing or stale handoff.  No normal customer path, target
selection rule, policy or route writer changes.

## 2026-08-25 — prepared-decision hot-path reconciliation and freeze frontier

### Scope and safety

This logical block continued the already admitted one-user HARD-path mission.
All live exercises used only certification identity `10.7.0.124` on its
isolated source `amneziawg-exec-20260528-10-8-1-14`; target `awg3` was always
selected by the existing owner.  Every exercise returned the identity to the
same isolated source.  `v7-health.service` remained `active`; ordinary-user
delta stayed `0`; no timer, owner, Planner, queue, registry, route writer or
parallel state source was created.

### Changes, evidence and deployment

The initial prepared-decision integration reduced one valid cold
failure-to-decision interval from `5096.479 ms` to `2566.188 ms`.  Exact
timeline instrumentation then identified an avoidable post-T0 cost: the
already-read Matrix Authority lineage was copied and subsequently rejected by
an inconsistent JSON-hash law between Matrix and Planner.

The bounded repair:

- passes the existing append-only lineage by reference inside the same
  governed process;
- binds it to the freshly reread current policy contract;
- uses the Planner's canonical hash law for that binding;
- retains the existing fresh-owner fallback on any absent, mismatched or stale
  handoff;
- records whether the handoff was actually reused.

Focused suites (`test_service_failure_episode`,
`test_governed_canary_cli`, `test_v7_users_autoswitch_policy`) passed
`456/456` after the final repair.  The deployed Runtime and GitHub were
aligned by `tools/v7-safe-deploy` at code commit `d16db6b4` for the final
measurement instrumentation (the preceding functional hash-law repair is
`345cb41c`).

### Measured result

The final valid controlled sample proved that the Matrix lineage handoff is
actually consumed: both planner-side lineage reads were
`REUSED_CURRENT_MATRIX_LINEAGE` and took `0.027 ms` and `0.026 ms`, replacing
earlier `~0.75–0.92 s` fresh append-only reads.  Current policy and handed-off
contract hashes matched exactly; no relaxed verification was introduced.

The remaining variable interval is Matrix prepared-target validation.  Its
latest decomposition is:

| interval | latest measurement |
|---|---:|
| current prepared-projection owner validation | 793.116 ms |
| summary read | 0.811 ms |
| target intersection / capacity / path check | 9.754 ms |
| final Planner initialization | 162.060 ms |
| decision → Apply admission | 110.699 ms |
| route writer | 427.725 ms |

An isolated read-only measurement of the existing Planner import plus its
prepared-projection validator was `158.839 ms`.  The larger live values are
therefore not evidence of another duplicated full Matrix/Planner reconstruction;
they include process scheduling contention on the current two-vCPU substrate.
The required fresh target/path and final mutable checks remain intact.

### Current exact frontier

Implementation is frozen after `d16db6b4`.  The next action is a homogeneous
controlled HARD-path series on that single fingerprint: at least five valid
samples, including at least one cold, two warm and two Matrix generations.
No code, configuration, cadence, priority or verifier change is permitted
during this series.  Pass requires nearest-rank P95 `<= 3000 ms` and no valid
sample above `5000 ms`; otherwise the mission emits
`HARD_PATH_3S_FEASIBILITY_EXHAUSTED` with the full distribution and smallest
remaining architectural choice.
