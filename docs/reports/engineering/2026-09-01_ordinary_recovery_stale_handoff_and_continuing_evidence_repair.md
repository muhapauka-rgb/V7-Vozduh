# Ordinary recovery stale-handoff and continuing-evidence repair — 2026-09-01

## Result

Two independent generic blockers were preventing the ordinary automatic
recovery path from acting even though current Matrix evidence and the existing
Planner had a suitable target.

Both repairs are deployed.  The normal `v7-health.service` caller then moved
two ordinary users from failed `vless` to `awg0`, and later moved the remaining
ordinary user from failed source `1` to `awg0`.  No user was moved by Codex;
the normal V7 chain produced the actions.

## Causes and repairs

1. A historical ordinary obligation with `NO_SAFE_TARGET` and zero selected
   users was treated as a ready direct handoff forever.  That suppressed the
   existing advisory owner even after a new Matrix generation made `awg0`
   eligible.  Commit `a009cca2cd8629fe066ede56751cbbbe9833cbaa` makes an
   ordinary direct handoff usable only when it carries the current actionable
   revalidation classification and at least one selected user.  A stale
   no-target result therefore returns control to the existing advisory owner.

2. A continuing Matrix failure was rejected after ten seconds when the latest
   health wake did not equal the incident's original hard-failure timestamp.
   On the contended Runtime this made freshly re-probed, still-failed services
   disappear before recovery.  Commit `724a1129abc2ed70ecae8a98b3f12d0ecf9f8990`
   accepts only `OBSERVED_CONTINUING` evidence refreshed within 30 seconds;
   all older, new, unknown and conflicting evidence retains the prior exact
   timestamp rule.  Matrix scope plus governed Candidate, Packet, Lease,
   Barrier, Apply and required-service checks remain mandatory.

## Verification and production observation

Focused unit tests for both causal cases and Python compilation passed.  The
broader legacy bundle still has one pre-existing static fixture assertion
failure unrelated to these files; it was not changed or hidden.

Each deployment passed the existing allowlist, GitHub/local/Runtime alignment
and truth gate, and `v7-health.service` remained active.

Live owner-backed receipts:

| Source | Automatic result | Users moved | Matrix T0 to complete |
| --- | --- | ---: | ---: |
| `vless` | `ACTION_COMPLETED` | 2 | 19.710 s |
| `1` | `ACTION_COMPLETED` | 1 | 27.568 s |

The timing does **not** meet the seven-second product limit.  This block
restores correctness and proves the automatic caller resumes recovery.  The
next frontier is measured reduction of the now-visible 19–27 second governed
execution path, without returning to manual user operations.
