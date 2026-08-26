# V5.3 Telegram critical latency: root cause and safe reduction

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_TELEGRAM_CRITICAL_LATENCY_ROOT_CAUSE_AND_SAFE_REDUCTION`  
**State:** implementation safely deployed; a live source-selection defect was repaired and the Telegram evidence is safely blocked until an actually empty, healthy certification source exists.

## Scope and guardrails

This work retained the existing Matrix, Planner, Authority, route writer, state files and service-verification semantics. No ordinary user, ordinary route, Matrix cadence, service timer, product SLO or HARD-path logic was changed. The only intended test effect is one certification-only identity on an isolated source.

## Baseline and causal finding

The valid Telegram controlled sample `f428` was functionally correct but too slow:

| Interval | Measured value |
| --- | ---: |
| failure -> decision | 18,163.325 ms |
| decision -> Apply | 240.232 ms |
| Apply -> assignment | 685.845 ms |
| assignment -> kernel | 17.853 ms |
| kernel -> reported S11 | 6,247.165 ms |
| total failure -> S11 | 25,354.419 ms |

The evidence isolates two avoidable synchronous contributors before/around decision:

1. Telegram failure publication woke `v7-autoswitch-planner.service` through a separate systemd process instead of the already-running health/Matrix owner. The observed earlier Telegram event was published at 14:22:20.925 UTC and the external planner start appeared about five seconds later.
2. A stale prepared target performed a 5,158.93 ms target-refresh attempt even though its only lawful consequence was the existing full controlled fallback. The complete prepared-validation span was 7,972.373 ms.

The reported 6,247.165 ms after kernel visibility must **not** be interpreted as a pure required-service check: the Matrix-required service evidence in that sample was 3,251.291 ms; the broader field includes additional transaction work.

## Implemented and deployed reduction

Published commit: `ac1d6c20b6ebbbf5073b917e27d1d51a9e6b1d3a` (`perf: remove telegram matrix process boundary`).  
Deployment: `deploy-z8-14-Updatesystem-ac1d6c2-20260826T182822`, final safe-deploy verdict `PASS`.

Changes:

- `tools/runtime-support/v7-health-loop` now consumes a Telegram Matrix T0 through the existing persistent health/Matrix consumer when that consumer is ready. HARD remains on its existing path.
- `tools/v7-telegram-sentinel` suppresses only the duplicate external systemd wake while the existing persistent consumer owns this exact Telegram event; it preserves the former wake as its fallback.
- `tools/v7-service-matrix-refresh-all` skips the known stale prepared-target refresh only on the runtime certification hot path and enters the existing full fallback directly. Non-hot behavior is unchanged.
- New focused tests cover exact current-assignment Telegram T0 selection and suppression of the duplicate external wake.

Validation passed:

- 153 focused health/sentinel/service-episode tests;
- 18 V5.3 role-based recovery tests;
- 7 fast-signal coverage tests;
- 10 N7 causal Polygon tournament tests.

The broader `test_service_failure_automation_evolution` contains one unrelated pre-existing failure in the unchanged `v7-users-autoswitch` standing-policy fixture (`STOP_SAFE_NO_SAFE_TARGET` versus the fixture's expected fresh-event revalidation state). It was not hidden or changed by this mission.

## Runtime state after deployment

- `v7-health.service`: `active`.
- Old standalone Matrix timer: absent/not found; standalone Telegram timer: `disabled`, as intended.
- Runtime hashes were accepted by the safe-deploy alignment gate.
- Certification identity currently selected by the lawful one-user topology preflight: `10.7.0.108`, currently on `awg0`, table `1106`, certification group `t48-d27d985e237c`.
- It has no Telegram service profile yet (`{}`), so the normal required-profile sentinel correctly has no basis to generate a Telegram controlled failure for it.

## Controlled-baseline reconciliation and authenticated source audit

The existing one-user topology owner originally selected the validated isolated draft `amneziawg-1779303737-a57ce8`, with an immutable contract:

- exactly one certification identity: `10.7.0.108`;
- expected assignment: `awg0 -> NEW_DEDICATED_SOURCE`;
- ordinary assignment and route deltas: `NONE`;
- no Candidate, Packet, Lease, routing or user move while requesting/deciding;
- bounded rollback and fresh Matrix/route verification required.

The existing Authority owner registered and approved this exact request:

- request `cstopauth_r1_10e2213949fe0f3afc3035b2`;
- decision `APPROVE_PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE`;
- decision record `cstopdec_23b1118726ebaf71cb7415be`.

Its first existing-owner consumer stopped safely before any mutation because the approved draft is not yet materialized into the existing disabled pool/runtime profile:

`approved_draft_not_materialized_to_existing_pool_source`, `approved_draft_pool_source_not_unique`, and `approved_draft_runtime_lifecycle_not_ready`.

The V7 Admin session was subsequently authenticated and the existing admin lifecycle was inspected through its UI.  It correctly rejected that AmneziaWG draft as a duplicate of existing channel `1` (`v7e356a192b79`).  No duplicate was created or enabled.

The next owner-selected OpenVPN candidate, `openvpn-1779388847-d2ad7c`, initially looked eligible because its historic admin lifecycle recorded `added_disabled`, `PASS` preflight/runtime/quarantine and one-identity capacity.  The live admin channel list and `users.registry` proved that the source is no longer empty:

| Live assignment class | Count |
| --- | ---: |
| ordinary users on `openvpn-1779388847-d2ad7c` | 2 |
| another certification identity / group | 1 |
| total assigned identities | 3 |

Its use as a purported dedicated source would violate the one-user contract.  The draft was not reserved, enabled, changed, or used for a controlled failure.

## Repair: live occupancy wins over historic draft lifecycle

The cause was narrow: `_controlled_source_draft_candidates` checked the historic draft state and duplicate configuration but did not check whether a previously materialized source had later acquired users.  Commit `5cbcbd0726516a4a25a8b7a18d5685dcaa1a364e` (`fix: require empty controlled source draft`) makes the existing topology owner read the existing `users.registry` alongside `egress.registry` and reject every materialized candidate with any current assignment.  It exposes only compact counts and a reason such as:

`draft_materialized_source_not_empty:openvpn-1779388847-d2ad7c`

This is not a new owner, state source, timer, route writer, Planner or Matrix path.  It closes a missing safety predicate in the existing owner.  It was published and deployed by `tools/v7-safe-deploy`; final verdict `PASS`, deployed commit `5cbcbd0726516a4a25a8b7a18d5685dcaa1a364e`.

This follows three earlier, separately deployed hardening commits from the same reconciliation: `c4a9fa7d` rejects an AmneziaWG draft duplicating an existing interface, `4ee4113b` applies the same rule to OpenVPN, and `230d397b` rejects a newly proposed source identifier already present in the registry.  The occupancy check is the final missing condition discovered by the authenticated live audit.

Focused verification after the repair passed:

- AmneziaWG duplicate rejection;
- OpenVPN duplicate rejection;
- occupied proposed-source-ID rejection;
- materialized-source-with-users rejection;
- existing safe-empty topology boundary test;
- Python syntax compilation and diff validation.

The live post-deploy topology diagnostic now reports `CONTROLLED_SOURCE_TOPOLOGY_PROVISIONING_REQUIRED`, not a false ready state.  It rejects the formerly selected OpenVPN source with three current assignments and also excludes the 49-user WireGuard source.  The new exact source request `cstopauth_r1_e04ee3039ad91f4dcf7943c7` is pending but no longer matches current preflight, therefore it cannot be consumed by the existing consumer.

## Existing safe-source attempts

Two remaining existing OpenVPN drafts were exercised only by the V7 Admin's normal isolated preparation flow.  That flow performs no user movement and does not add a source unless its field check, temporary runtime test and Matrix quarantine all pass.

| Draft | Result | Effect |
| --- | --- | --- |
| `openvpn-1779385423-2121b0` | stopped before temporary launch: the configuration contains unsupported `User`/`Group` directives and lacks safe allowlisted launch data | no pool entry, no runtime profile, no route or user effect |
| `openvpn-1779387408-c42bdf` | field and temporary runtime checks pass; Matrix quarantine remains `BLOCKED` / service-matrix `WARN` | no pool entry, no runtime profile, no route or user effect |

The panel's normalisation preview did not silently alter either configuration.  In particular, the incomplete first draft was not force-started without a safe credentials method.  No ordinary-client assignment or route fingerprint changed during these checks.

## Current external boundary and exact continuation

The only lawful materialization path remains the existing authenticated `v7-admin-api` lifecycle:

`egress-draft-pool-apply` (add disabled) -> `egress-draft-runtime-provision` -> guarded enable/validation -> existing topology consumer -> existing governed certification transaction.

It also owns `service-preferences-update`, the only discovered canonical writer for the temporary Telegram-required profile. It must later set that profile for the one certification identity and clear it during cleanup; direct JSON editing is not lawful.

Authentication is no longer a boundary: the authenticated UI was used.  The current boundary is an external source prerequisite: V7 has no existing source that is both (a) empty of all current identities, (b) healthy under the required Matrix quarantine, and (c) runnable from a complete safe configuration.  Reusing a shared source, fabricating credentials, weakening quarantine or manually overriding the source owner would break the controlled-test contract.

**Exact next action:** provide or import one distinct, complete source configuration through the existing V7 Admin draft lifecycle.  It must pass field validation, isolated runtime preparation and Matrix quarantine; it must be added disabled with zero assignments.  Then the existing topology owner can create a fresh manifest-bound request, reserve that one source, move only `10.7.0.108`, set the temporary Telegram requirement through `service-preferences-update`, and run the cold Telegram sample followed by the warm/final homogeneous evidence series.

## Current conclusion

The code-level causal reduction is live and ready to be measured. The mission has not claimed Telegram SLO success or failure because no post-deploy functionally valid Telegram sample exists.  The existing system now correctly prevents the previously hidden unsafe source reuse.  The remaining block is a real external source/configuration prerequisite; no safety contract needs to be weakened and no new owner is required.

## Fresh all-existing-egress reconciliation (2026-08-26 21:08–21:12 MSK)

The preceding external-source conclusion was re-opened rather than accepted from history.  The existing Matrix owner completed one observation-only refresh for every enabled egress.  It emitted no event, Candidate, Packet, Lease, route mutation or client movement.  The existing topology/reservation owner then evaluated every current egress against the one-user controlled-source contract.

The refresh changed material facts: VLESS Telegram itself is currently reachable, and the dedicated execution channel is actually empty.  A separate owner-state inconsistency was also found: the topology diagnostic used a stale `v7-state.json` assignment count (five) for the execution channel while the canonical current `users.registry` had zero enabled assignments.

Commit `ad9c1a9cd5e1728c774f8ae8cfd95b619e7b6833` (`fix: bind controlled topology to live assignments`) was published and safely deployed.  It makes the existing topology decision calculate present occupancy and free capacity from `users.registry`; the loaded Planner snapshot is retained only as an explicitly labelled diagnostic value.  It also closes a second safety hole found by the same reconciliation: an empty but actively reserved source cannot be rebound to a different certification group merely because it has no current users.  Both focused source/topology tests and Python compilation passed; `tools/v7-safe-deploy` returned `PASS`.

Final live owner-backed result after that deployment:

| Existing egress | Current state | Controlled-source decision |
| --- | --- | --- |
| `vless` | zero enabled current users; Telegram `OK`; overall Matrix `WARN` (12/14); quality/stability floor not met; old reservation expired | rejected: source baseline is not healthy and reservation is expired |
| `awg0` | healthy, but 13 ordinary + 25 certification identities | rejected: whole-source test would affect ordinary users |
| `awg3` | healthy, but 11 ordinary + 24 certification identities | rejected: whole-source test would affect ordinary users |
| `1` | empty but Matrix `FAIL`, Telegram `DOWN` | rejected: no healthy baseline |
| `openvpn-1779388847-d2ad7c` | 2 ordinary + 1 other certification identity; Matrix `FAIL` | rejected: occupied and unhealthy |
| `wireguard-1779454504-c43409` | healthy, but 46 ordinary + 3 certification identities | rejected: whole-source test would affect ordinary users |
| `amneziawg-exec-20260528-10-8-1-14` | healthy, empty, free capacity 9 | rejected for this Telegram campaign: it is actively reserved until `2026-08-31T00:00:00Z` for certification group `ctm0f-9765f296cbe9`, while the current Telegram identity belongs to `t48-d27d985e237c` |

The execution channel is therefore not a missed opportunity or a stale classification.  Its health and emptiness are valid, but its current reservation belongs to another controlled scope.  Reusing it would be an ungoverned cross-group takeover.  VLESS is likewise not rejected because of an old report: its current Telegram result is good, but the owner-backed whole-source baseline remains below the required health/stability floor.

Runtime confirmation after deployment: `v7-health.service` is `active`; the old standalone Matrix timer remains absent; the standalone Telegram timer remains `disabled`; the deployed and local `v7-users-autoswitch` hashes match.  There was no ordinary-user or route effect.

**Recomputed terminal:** `EXTERNAL_SOURCE_REQUIRED` is now evidence-backed for the current state of *all* existing egresses.  Re-entry is either (1) a new complete source through the existing Admin lifecycle, or (2) an explicit release/transfer by the current owner of the separately reserved execution channel.  The latter is a distinct cross-group authority decision and must not be inferred from the Telegram mission.

## Controlled execution-source reuse and Runtime boundary (2026-08-26 21:43–22:15 MSK)

The owner-decision to evaluate `amneziawg-exec-20260528-10-8-1-14` was consumed.  Read-only lineage reconciliation proved that its preceding CT-M0F operation was terminal: its execution lease was finished, the prior certification identity had no remaining assignment on the source, and no Candidate, Packet, Lease or rollback consumer was active.  The old controlled reservation was therefore released through `v7-egress-set-state`, first to its prior backup and then, under the new explicit base-release guard, to the matching clean base state.  No ordinary assignment, route or customer was changed.

Three narrow existing-owner repairs were needed and were focused-tested, published and safely deployed: `75afae88` added guarded release to an exact clean base; `35865aaf` normalised equivalent boolean registry spellings in that guard; `a8ad3d8c` and `549501a1` let an already auto-admitted, empty existing source be recorded and consumed by the existing topology/reservation owner.  The final owner-backed reservation was:

- source: `amneziawg-exec-20260528-10-8-1-14`;
- group: `t48-d27d985e237c`;
- reservation: `ctres_d899f66f641229141922acc7`;
- ordinary users: zero;
- free capacity after reservation: nine.

The initial-source transition then exposed one real hand-off defect: the controlled-condition owner required the certification identity to already be assigned to the newly reserved source before it invoked the sole route writer.  Commit `b1689e8e4d0c9d432b8f1b24ed2d32e32c147685` reorders only that existing transition.  It requires the exact source reservation and group, moves only the named certification identity through `v7-user-switch`, verifies its policy table and route, then permits the existing selector to read the resulting state.  Focused tests passed (`262` tests); safe deploy and local/GitHub/Runtime alignment passed.

Live proof of that bounded transition succeeded for `10.7.0.108`: its registered source, assignment and Linux table `1106` all resolved to `v7execwg0`.  The selected target remained owner-selected (`awg0`); no target was supplied manually, and no ordinary user moved.

The first Telegram condition was deliberately treated as invalid engineering setup, not SLO evidence: the temporary Telegram-required profile had not yet been set, so Matrix correctly did not bind the source failure to that profile.  The condition was removed through `v7-egress-set-state certification-telegram-recovery`.  The profile was then created through the authenticated canonical `service-preferences-update` owner, not by editing state files, and a new exact controlled condition was prepared.

That second attempt uncovered the current real blocker.  The ordinary Telegram health role itself remained running beyond its one-second cadence; successive deadline misses accumulated, `v7-health.service` reached an approximately 1 GiB memory peak and was OOM-killed, then restarted.  A manually started confirmation process was stopped; it is invalid and receives no evidence/SLO credit.  The source-level Telegram block was removed through the existing recovery owner.  Runtime later recovered (`v7-health.service` active), but the admin service was itself observed near 1 GiB (`MemoryCurrent=1050746880`), so additional profile/admin mutations were stopped as unsafe.

Current safety state:

- no ordinary client or route was changed;
- the artificial Telegram block is removed;
- the protected test identity remains isolated on the reserved execution source;
- the temporary Telegram profile is still present only for that identity because its canonical cleanup request became unsafe while the admin Runtime was memory-saturated;
- Admin Safe Mode was returned to `OPEN`/enabled after the failed cleanup attempt;
- the two pre-T0 transaction reservations expired without a Packet, Lease, Apply or recovery movement and must not be counted as a valid sample.

**Current terminal:** `TELEGRAM_CERTIFICATION_RUNTIME_MEMORY_CONVERGENCE_REQUIRED`.

**Exact next action:** first reconcile and bound the existing Telegram/Admin Runtime memory growth on Polygon or an isolated controlled run, prove that the health role completes and remains below the substrate limit, then use the existing canonical profile owner to clear the temporary profile and the existing governed cleanup owner to return `10.7.0.108` to its baseline.  Only after that clean baseline is proven may a fresh Telegram condition begin and be credited to the homogeneous Telegram evidence series.  No further source search or target-policy change is required.

## Runtime memory correction (2026-08-26 22:30–22:38 MSK)

The memory boundary was reproduced and reduced without changing Matrix, Planner, health cadence, route writing or Telegram semantics.  The primary cause was the shared Admin JSONL reader: it loaded an entire append-only closure store (`closure-records.jsonl.1`, 184 MB) into decoded text and a complete line list for every bounded-tail request.  Admin summary assembly can call that reader repeatedly through closure metadata, so a small requested history repeatedly materialised the archive.

Commit `de70f0fa797c682f2d97fce8663460bb4d602755` changes only `admin_core.summary_builders.bounded_jsonl_records`: it reads a capped trailing byte window, drops a partial first line, then parses the same requested latest rows.  The record limit and redaction contract are retained.  `272` focused regression tests passed.  GitHub/local/Runtime alignment and the safe-deploy gate passed; `v7-admin-api.service` was then restarted because the changed shared module is loaded by that long-running process.

Measured Runtime effect:

| Component | Before | After restart and bounded reader |
| --- | ---: | ---: |
| `v7-admin-api` current memory | about 1.1 GB | 118 MB |
| `v7-admin-api` peak after real cleanup response | about 1.17 GB | 155 MB |
| `v7-health` current memory | about 200 MB | remained active |

The canonical temporary Telegram profile for `10.7.0.108` was successfully cleared through `service-preferences-update`; the response-side client timed out, but owner-backed state proved `users[10.7.0.108] = null` and Admin Safe Mode returned to enabled/`OPEN`.  The controlled Telegram block had already been removed.  No ordinary client, route, Matrix rule or target policy changed.

**Next action:** consume the existing governed controlled-certification cleanup owner to return the isolated test identity from the now-expired execution reservation to its owner-recorded baseline, then prove the clean baseline.  Only then start a fresh Telegram failure condition and collect evidence.  The bounded JSONL repair removes the demonstrated administrative-memory obstacle; it does not itself credit a Telegram S11 sample.

## Expired reservation cleanup closure (2026-08-26 23:xx MSK)

Fresh owner-backed reconciliation found one real lifecycle gap after the interrupted Telegram setup.  The exact test identity `10.7.0.108` remained on the isolated execution source `amneziawg-exec-20260528-10-8-1-14`, while its only source reservation `ctres_d899f66f641229141922acc7` had expired at `19:17:05Z`.  The canonical operator lease was `OPERATOR_CANCELLED`; no active Candidate, Packet, Lease or operation remained.  The source was healthy and the Telegram condition had already been recovered, but the existing release owner correctly refuses to release any source with an assigned identity.

The consumed topology Authority record already contains the only lawful rollback: exact identity `10.7.0.108`, original source `awg0`, same group `t48-d27d985e237c`, and the exact backup required for release.  The missing part was not a new owner or route writer; it was the terminal composition of existing owners for the narrow **expired-before-credit** branch.

The new bounded command in the existing governed canary owner admits the operation only when all of the following are simultaneously true: one exact consumed provisioning record, immutable matching manifest/group/identity, an expired reservation, no active execution lease, exactly one certification identity on the source, no active source condition, and the original target still present.  It then invokes the existing governed Candidate/Packet/Lease/Barrier/Apply chain to return that identity, verifies it, calls only `v7-egress-set-state` to restore the exact owner backup, and records the one-use topology invalidation through `admin_core.operator_execution`.  It rejects every drift, active operation, group mismatch, unrelated occupant or changed backup without moving anybody.

Focused safety coverage now includes both the successful exact-owner path and refusal when an execution lease is active.  The relevant suite (`v7-egress lifecycle`, service-failure episode, governed canary) passed: **283 tests**.  Deployment and live consumption remain the next operation; this document update does not claim that the rollback has already occurred.

### Reconciliation correction

The first live attempt correctly created no Packet, Lease, route change or client movement, but it exposed a second narrow composition defect: a controlled **cleanup** was still evaluated against advisory prediction/trust snapshots.  Those snapshots are intentionally not part of the exact cleanup safety contract, so their normal refresh cadence could make a verified return permanently impossible.  The code now gives ordinary exact cleanup the same existing `CONTROLLED_CERTIFICATION_TOPOLOGY` current-state gate already used by controlled setup and standing reset, and refreshes the existing snapshot owner once before it builds the cleanup Packet.  This retains the required current service, risk, candidate, pool, route, target and rollback checks; it excludes only historical advisory model files from blocking a non-discretionary restoration.  Availability-first and standing resets retain their single existing refresh; no duplicate snapshot work was introduced.

Focused coverage now totals **284 passing tests**.  The exact next action is to deploy this correction and repeat the same owner-backed cleanup once.  No Telegram evidence is credited unless that cleanup completes and a new clean baseline is later established.

### Apply-boundary correction

After the current-state cleanup gate was applied, the fresh Packet, Lease and restore-barrier were built successfully for the exact identity and baseline.  The sole route writer still stopped before Apply because its ordinary incident-continuity guard saw an unrelated open VLESS incident and required the cleanup source to be VLESS.  This is a composition bug: an exact owner-recorded cleanup should not be reinterpreted as a new ordinary failover, but neither may it silently bypass the writer.

The existing `v7-users-autoswitch` owner now receives one explicit `controlled-engineering-cleanup` scope from the governed caller.  It proves one immutable Packet/Lease binding, one enabled registry-marked certification identity, its current reserved controlled source, and the already Packet-bound enabled baseline target.  It then suppresses only the unrelated-incident source comparison and keeps selected-user route verification.  It cannot be inferred by ordinary or emergency routing, cannot select a different user/source/target, and does not accept an ordinary identity.  A focused scope test confirms that a shared baseline with ordinary users does not widen the permitted move; the return still contains only the certification identity.

The previous two live attempts remain invalid setup/cleanup attempts: both stopped before route mutation.  The next operation is deploy → repeat the same exact cleanup once → verify source release and baseline route.  Telegram proof is still not started and receives no credit.

## Terminal cleanup consumed and program-frontier reconciliation (2026-08-26 23:00 MSK)

The exact cleanup has now completed.  This section supersedes the preceding
"next operation" paragraph; it is a lifecycle closure, not a new Telegram
experiment and not SLO evidence.

The final implementation retained the same existing owners.  Commit
`3801c24c` preserves the action class stored in the exact governed cleanup
window: it is one controlled user return, not a broad emergency action.  Commit
`3952b928` completes an interrupted terminal release safely.  It proves the
post-release source against the exact backup produced by the existing egress
owner and appends only the missing invalidation.  It never repeats a route
move.  This matters because execution-only properties such as
`execution_reserved` are permanent source attributes, whereas the removed
per-campaign reservation markers are temporary.

Both commits were published and safely deployed.  Focused tests: **487
passing** (148 governed-canary CLI, 202 autoswitch policy, 137
lifecycle/service-failure).  Local, GitHub and deployed code are aligned at
`3952b9286bf2def602ed91d59f924eb6cd9764b6`.

Live owner-backed terminal evidence:

| Item | Result |
| --- | --- |
| governed return | `GOVERNED_TRANSACTION_COMPLETED` |
| exact route/service verification | `PASS` |
| certification identity | `10.7.0.108`: execution source -> `awg0` |
| ordinary-user delta | `0` |
| source occupants after return | `0` |
| exact owner-backup match | `true` |
| old reservation invalidated | `cstopinv_a32b6ddde10fe43fb8563bc7` |
| Runtime health | `v7-health.service` active |

Direct Linux evidence for the returned identity is consistent: rule
`from 10.7.0.108 lookup 1106`, table `1106` default device `awg0`, and route
lookup from that identity selects `awg0`.

The legacy global `v7-user-route-check` utility emitted a global failure while
scanning every registry user, despite this direct exact policy-route evidence.
It has no single-user interface and is not the governed transaction verifier;
the discrepancy is retained as a diagnostic observation and was not used to
claim a pass.

### Current program frontier

This cleanup closes the interrupted source lifecycle, but it does not reopen
Telegram performance work.  Fresh CPS remains authoritative: Telegram
certification-only S11 is functionally proven at `25,354.419 ms`, above the
active 8-second ceiling.  The test client/profile are clean and ordinary-user
delta remains zero.

The exact remaining frontier is `N10_PRODUCT_AUTHORITY_COHORT_CONTRACT`.
It requires a separate, explicit product-owner ordinary-like cohort scope
before any ordinary identity can be selected, moved or counted as evidence.
Engineering deploy authority does not supply that product scope.  N11 remains
read-only; no safe deletion is admitted.
