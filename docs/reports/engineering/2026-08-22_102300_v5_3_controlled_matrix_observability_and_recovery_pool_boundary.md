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

The requested end-to-end recovery could not lawfully start because the actual
controlled source has five certification users while the exact one-user
controlled-failure contract permits one.  The inventory has no independent
ready controlled reserve: both eligible-looking draft records duplicate the
unhealthy legacy channel and were rejected by the existing draft lifecycle.
This is a real resource/topology boundary, not a stale-Matrix wait.

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
| Recovery preflight | Existing governed controlled-certification preflight | `STOP_SAFE`: no distinct enabled controlled target and no exact one-user source scope |

The full refresh also kept its normal work; the source-specific fresh row was
written at the controlled observation time.  A service limit response remains
distinct from a hard failure as before.

## Recovery-pool disposition

The existing topology owner found an approved one-user draft preparation, but
the admin draft owner rejected its materialization with
`duplicate_interface_config`: it duplicates legacy channel `1`, whose health
is currently unusable.  Read-only inventory confirmed that the two available
Amnezia drafts are both that duplicate.  They were not force-added.

An attempted Tier-48 request was immediately inspected and found to select a
different source and require an unnecessary 48-identity campaign.  It was
explicitly declined through the existing Authority audit owner.  This left
policy, registry, Runtime, routes and clients unchanged.

## Effects and limits

- Ordinary users moved: `0`.
- Certification users moved: `0`.
- Ordinary assignment/route delta: `0`.
- Automatic FAST admission: unchanged, held.
- Full Matrix fallback: unchanged.
- Production claim: none.  This is controlled observability evidence only.

## Exact next step

Continue the admitted V5.3 plan without waiting for a Matrix timer:

1. Use the already-consumed Polygon/scale results for the architecture track;
   they remain the valid evidence for candidate comparison and do not require
   a live client move.
2. For a new physical T0→T11 recovery proof, the existing controlled-source
   lifecycle needs one of two safe inputs: a genuinely independent ready
   draft from the external profile owner, **or** an explicitly admitted
   existing-owner operation that narrows the current five-user controlled
   source to one before its whole-interface failure.  Neither may be faked by
   overriding the duplicate-channel rejection.
3. Once that one-user source and a healthy target exist, reuse the already
   deployed Matrix observation and governed Packet/lease/verification path;
   measure source failure → fresh Matrix → decision → recovery and then reset.

