# V5.3 — controlled Matrix observability and recovery-pool boundary

**Date:** 2026-08-22, 10:23 MSK  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Track:** `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
**Block:** controlled production-adjacent Matrix observation; no ordinary-customer effect

## Result

`CONTROLLED_MATRIX_FAILURE_OBSERVED; CONTROLLED_RECOVERY_POOL_NOT_ADMITTED`.

The existing Matrix writer now observes an intentionally disabled, already
reserved controlled-certification interface during its ordinary full refresh.
Before this repair, the refresh selected only enabled channels, therefore a
controlled source could be disabled correctly but remain invisible to the
canonical Matrix.  The minimal repair was deployed and verified by matching
local/Runtime SHA-256 fingerprints.

The controlled failure was then observed as a fresh `NOT_STARTED` Matrix row
and classified as certification-only.  The consumer correctly made no
ordinary-route decision and deferred to the existing controlled owner.  The
source was restored immediately.  No ordinary customer, ordinary route,
policy, timer, FAST admission or Matrix cadence changed.

The first attempted end-to-end recovery using the execution-only source could
not lawfully start because that source has five certification users while the
exact one-user controlled-failure contract permits one.  Its independent draft
reserve candidates duplicate the unhealthy legacy channel and were correctly
rejected.  This conclusion applies to that source only.

## Change and deployment

Commit `3f18ab5aeff24164229bd2169c0b67914f20387f`
(`fix: observe disabled controlled matrix sources`) changed only
`tools/v7-service-matrix-refresh-all`:

- a normal full refresh still selects all enabled channels;
- it additionally selects a disabled `interface` channel only when the
  existing registry already marks it `controlled_certification_source`;
- an explicit `--egresses` request still refuses disabled channels.

The focused regression
`test_full_refresh_includes_only_disabled_controlled_interface_source` proves
all three rules.  The affected unit module passed.  The broader legacy suite
has two unrelated fixture failures where old fixtures lack a now-required
live-registry scope fingerprint; these were not changed or masked.

Post-change Polygon regression also passed: `11/11` across the candidate
failure matrix and controlled Matrix comparison.  It re-proved full/subset
equivalence for the controlled healthy and required-service cases, full
fallback on disagreement, stale-state fail-closed behavior and the existing
bounded scale checks.  The temporary loopback response surface was local only.

`tools/v7-safe-deploy --json` and the apply both returned `PASS`:

- deploy: `deploy-z8-14-Updatesystem-3f18ab5-20260822T100910`;
- manifest blockers: none;
- local and `/usr/local/bin/v7-service-matrix-refresh-all` SHA-256:
  `50579aea49c30e9af6842380d92af252a302ae6cd03b8824d9e381645ba6f869`.

## Controlled evidence

| Step | Evidence | Result |
| --- | --- | --- |
| Precondition | Existing execution-only interface, five certification users, zero ordinary users | pass |
| Controlled source down | Existing `v7-egress-set-state ... maintenance --controlled-certification --apply` | interface disabled; guard scoped only certification users |
| Matrix refresh | Existing `v7-service-matrix-refresh-all` | fresh source row `NOT_STARTED`; current scope decision `RECONCILE_CONTROLLED_CERTIFICATION_SCOPE_ONLY` |
| Consumer | Existing Matrix passive projection | `DEFERRED_TO_EXISTING_CONTROLLED_OWNER`; no ordinary Runtime action |
| Restore | Existing `v7-egress-set-state ... enabled --controlled-certification --apply` | interface restored and kill-switch rebuilt |
| Recovery Matrix refresh | Existing `v7-service-matrix-refresh-all` after restore | fresh `OK`, `14/14` checks successful |
| Recovery preflight | Existing governed controlled-certification preflight | `STOP_SAFE`: no distinct enabled controlled target and no exact one-user source scope |

The full refresh also kept its normal work; the source-specific fresh row was
written at the controlled observation time.  A service limit response remains
distinct from a hard failure as before.

After restoration, a second ordinary full refresh produced a fresh `OK` row
with all `14/14` checks successful for the controlled source.  The remaining
certification-only reconciliation projection had no active source and no route
effect; it is historical-scope reconciliation, not a live failure.

## Recovery-pool disposition and correction

The existing topology owner found an approved one-user draft preparation, but
the admin draft owner rejected its materialization with
`duplicate_interface_config`: it duplicates legacy channel `1`, whose health
is currently unusable.  Read-only inventory confirmed that the two available
Amnezia drafts are both that duplicate.  They were not force-added.

An attempted Tier-48 request was immediately inspected and found to select a
different source and require an unnecessary 48-identity campaign.  It was
explicitly declined through the existing Authority audit owner.  This left
policy, registry, Runtime, routes and clients unchanged.

**Correction after the VLESS reuse audit (2026-08-23).**  The existing
`vless` source is a better real-failure input: it has eleven certification
users, zero ordinary users and a fresh Matrix `WARN` result with only `1/14`
checks passing.  It must not be used as a target, but it can safely be the
source of a one-user controlled recovery.  The existing selector currently
rejects it for two implementation reasons:

1. its certification-only Matrix event is represented with an ordinary
affected scope of zero, so the selector cannot bind one existing
certification identity to the fresh real incident;
2. existing healthy targets are presently classified `DEGRADED_USABLE`, while
the selector's one-user shared-target branch accepts only `HEALTHY` despite
the active availability-first policy already fencing a one-user,
certification-only degraded-target transition.

This is an existing-owner producer/consumer and admission-projection gap, not
an external-resource requirement.  The safe repair is limited to the existing
Matrix/controlled-selector path: expose an exact one-user certification
binding from the current canonical event, and admit only a fresh,
capacity-checked, verified `DEGRADED_USABLE` target when the existing standing
policy's one-user fences pass.  It must not change ordinary scope, target
fault injection, FAST admission or the full-Matrix fallback.

**Implemented selection repair (2026-08-23).**  The existing
`tools/v7-users-autoswitch` now reads a certification-only Matrix event only
when all of these independently current facts agree: VLESS remains failed in
Matrix, the Matrix observation and event are fresh, the source registry still
has no ordinary users, and the compact certification scope fingerprint equals
the live registry.  It chooses one group-aligned certification identity only.
For the destination it reuses the existing stage-1 availability allocation and
the already active policy semantic-coverage gate; it does not hand-pick a
server or relax the normal `HEALTHY` target floor.  In the observed inventory
that allocation selects `awg3` for one identity while retaining its ordinary
clients unchanged.  Stale, recovered, scope-mismatched, ordinary-mixed or
policy-incomplete inputs return `STOP_SAFE`.

Validation for this repair:

- two new focused tests prove exact VLESS-event binding and selection of the
  existing one-user degraded allocation;
- the previous healthy shared-target and execution-only-target selection tests
  remain green;
- the existing Polygon candidate-failure and Matrix full-vs-subset suites pass
  11/11.  Their local loopback server needs elevated test permission and has
  no production effect.

This closes discovery/selection only.  It deliberately does not yet move the
selected identity: the existing availability benchmark runner assumes a
healthy source and performs a reset back to that source, which is unsafe while
VLESS is actually failed.  The next implementation is therefore a narrow
one-way governed recovery consumer that reuses the same Packet, lease,
verification and rollback owners, leaves the one synthetic identity on the
verified reserve, and records the Matrix incident binding.  It must not reuse
the healthy-source benchmark semantics or reset a client onto the failed
VLESS channel.

**Runtime revalidation correction.**  The first deployed selector attempt was
terminated by the operating system before output.  The Matrix snapshot and
VLESS event themselves were fresh; the cause was ordering, not data: the
selector loaded the large ordinary L3 history before trying the stricter
certification-only event.  The binding is now tried first for a
certification-only source; the ordinary L3 binding remains its fail-closed
fallback.  This preserves the former path for ordinary incidents while keeping
the controlled real-failure path bounded.

**Stale-evidence selector hardening (2026-08-23).**  By the time the next
read-only Runtime invocation ran, the VLESS observation was no longer fresh.
That invocation was again killed before producing a result: after the strict
binding rejected stale evidence, it still fell through into the unrelated
ordinary L3-history and topology scans.  This was neither a reason to move a
client nor evidence that VLESS had recovered.  The selector now recognizes a
controlled certification-only source (zero ordinary identities) and, if its
strict Matrix evidence is not executable, returns to `STOP_SAFE` directly.
It neither looks for an ordinary passive cohort that cannot exist nor runs a
topology discovery which cannot make stale evidence fresh.  Ordinary or
mixed-scope sources retain their existing L3 fallback.  A focused regression
test proves both expensive fallbacks stay untouched; the strict binding and
stage-one allocation tests pass, and the existing Polygon suites pass 11/11
(timings by probe cap: 1=0.849 s, 2=0.838 s, 4=0.747 s).  No client, route,
Matrix cadence or policy was changed by this correction.

## Effects and limits

- Ordinary users moved: `0`.
- Certification users moved: `0`.
- Ordinary assignment/route delta: `0`.
- Automatic FAST admission: unchanged, held.
- Full Matrix fallback: unchanged.
- Production claim: none.  This is controlled observability evidence only.

Final `tools/v7-truth-check --all --json`: `PASS`, blockers none.  The only
warning is the expected documentation-only local/Runtime commit difference;
the deployed runtime binary remains the verified `3f18ab5` Matrix repair.

## Exact next step

Continue the admitted V5.3 plan without waiting for a Matrix timer:

1. Repair and Polygon-test the two existing-owner VLESS binding/admission
   gaps above. **Complete:** fresh VLESS event and existing one-user allocation
   now produce a single read-only selection.
2. Extend the existing governed Packet/lease/verification consumer for the
   exact *one-way* VLESS-failure sample.  It must retain the selected
   certification identity on the healthy reserve while VLESS is failed;
   resetting it to the known-failed source is forbidden.
3. Run the governed one-user recovery, measure VLESS failure → fresh Matrix →
   selection → client recovery and observe the client on the reserve.  A later
   VLESS recovery may use the existing reset lifecycle; duplicate draft
   rejection remains unchanged.
