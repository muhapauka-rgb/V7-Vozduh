# Matrix-confirmed current-channel failover candidate repair

Date: 2026-09-01

## Live finding

The canonical Matrix currently shows source `1` with 14/14 failed services,
fresh observations and two ordinary assigned users. The existing Planner's
source-scope reader independently confirmed the same source as a fresh
whole-channel failure and exposed three healthy eligible targets.

Nevertheless its decision for an affected user was `keep` on source `1`.
The current-route comparison candidate used the ordinary sticky-placement
semantics and was not explicitly made ineligible from the already confirmed
Matrix channel evidence. The downstream governed consumer therefore received
no Planner-selected move and stopped before Candidate/Packet/Lease/Apply.

## Repair

`AutoswitchPlanner._decision_for_user` now reads the existing Matrix
whole-channel evidence for its current candidate. If that evidence is
confirmed, it marks only that current candidate ineligible before normal
failover selection. The existing Planner still selects the target; existing
Authority, Packet, Lease, Barrier, route writer and required-service S11
remain unchanged.

No manual user movement, target injection, event creation, Matrix change or
new owner was used.

## Verification

- New regression: a fresh Matrix-majority failure turns a source-bound
  ordinary decision into a failover instead of a sticky `keep`.
- Focused tests: 4 passed.
- Full `test_v7_users_autoswitch_policy`: 239 passed.
- Live read-only diagnostic confirmed source `1` is currently failed and
  healthy targets `awg0`, `awg3` and `wireguard-1779454504-c43409` are
  eligible for the affected profile.

## Deployment and observation frontier

The repair must be safe-deployed. After that, only the normal V7 health caller
may consume the current Matrix failure and create the recovery transaction.
The next valid evidence must show automatic Matrix T0 through required-service
S11; no Codex-initiated recovery is admissible.
