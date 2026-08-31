# VLESS ordinary recovery: Packet-cohort revalidation repair

## Scope

Live Runtime evidence showed a real VLESS required-service failure for ordinary
users.  V7 correctly created the governed recovery transaction and selected
locked healthy targets, but stopped before any route mutation.

## Root cause

The Packet retained full candidate diagnostics for only the representative of a
homogeneous multi-user cohort.  Later locked members therefore reached final
execution revalidation with an empty local candidate list.  That final check
mistook absent duplicate diagnostics for absent current Matrix proof and
returned `STOP_SAFE`, even though it was not permitted to select a new target.

The normal health process then remembered the unchanged Matrix incident as
consumed, so it could not retry the repaired generic path until a new incident
appeared.

## Repair

- The existing Packet remains the only target selector.
- Final revalidation now reconstructs only the already locked source/target
  evidence from the current Matrix and registry owners when compact cohort rows
  omit duplicate candidate diagnostics.  It does not rerank, select, or widen
  eligibility.
- The health owner retains normal deduplication for every completed or safety
  stop.  It leaves only the exact pre-route downstream-validation stop
  retryable, allowing the existing Runtime caller to reconsume the same live
  incident after this generic repair.

## Verification

- Focused sparse-cohort revalidation test: pass.
- Autoswitch policy suite: 236 pass.
- Focused health-owner deduplication and retry tests: pass.
- The combined health-loop suite has three pre-existing scheduling-fixture
  failures unrelated to this path; they occur while the persistent Matrix is
  unavailable in those fixtures and concern background role preemption.

## Production result

After safe deployment and restart of only the existing `v7-health.service`,
the normal Runtime itself reconsumed the still-live VLESS incident and
completed the governed recovery for three ordinary users.  It recorded Matrix
to Candidate, Packet, Lease, Barrier, Apply and required-service verification;
no manual route or user-specific recovery command was used.

The governed transaction started at 18:04:56 UTC and completed at 18:05:41
UTC on 2026-08-31: 41.827 seconds total.  The largest measured interval was
Apply and verification at 39.037 seconds.  This is valid functional recovery,
but it does **not** meet the seven-second product limit.

## Exact successor

Instrument and reduce the existing Apply-and-verification interval without
weakening route or required-service proof.  The automatic source-detection and
governed target-selection path must remain untouched; the live Runtime must
continue to be the operational actor.
