# V7 profile-failure immediate handoff repair — 2026-08-30

## Scope

This block repairs the existing automatic handoff from a fresh per-profile
failure observation to the existing Matrix consumer.  It does not move a user,
choose a target, write a route, create a Candidate/Packet/Lease/Barrier, or
change Authority.

## Fresh runtime diagnosis before the repair

The ordinary VLESS recovery scope was already discoverable by V7: two enabled
ordinary identities remained on the source and the existing Planner had an
owner-admitted healthy alternative.  The transaction did not reach an
automatic governed apply.

The generic cause was timing, not target selection:

1. the `other_required` health role ran for about 31–39 seconds;
2. a profile probe wrote a fresh source/profile observation while that role was
   still running;
3. the child deliberately suppressed its consumer wake because the health
   parent was expected to consume it after the complete probe batch;
4. when the parent eventually invoked the consumer, the bounded "current
   observation" handoff window had expired; and
5. the runtime then had no live source-bound incident to plan, although the
   Matrix retained the failure historically.

The subsequent autoswitch path also spent about 4.94 seconds on a historical
bounded-closure reconciliation before its first governed attempt.  That scan
does not change Candidate, Packet, Lease, Barrier, or apply validity for a
fresh exact profile handoff.

## Implemented repair

`tools/v7-egress-diagnose` now invokes the *existing* Matrix consumer inline
for an exact profile-source observation produced inside the existing V7 health
caller.  It passes only the exact source identifier and monotonic observation
time.  The consumer still derives affected users, target, Authority and all
execution objects, and still revalidates mutable state before any apply.  A
source-less interface-liveness event retains its parent-owned path.

`tools/v7-users-autoswitch` defers the historical closure scan only for that
fresh, source-bound runtime profile handoff.  The same reconciliation owner
remains available after the governed attempt and on later Matrix generations;
the deferment neither removes nor weakens executor safety checks.

## Verification before publication

- `bash -n tools/v7-egress-diagnose`: PASS.
- `PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m py_compile
  tools/v7-users-autoswitch`: PASS.
- `tests.unit.test_v7_egress_diagnose`: 35 PASS, including an exact
  source-binding wake test.
- Focused handoff regression test passes: it proves the historical scan is not
  called for a persistent-owner exact profile handoff.
- `git diff --check`: PASS.

The broader automation module did not complete within the local command
window and is therefore deliberately not counted as a passing suite.

## Safety and next evidence

After safe deployment, no Codex command may advance the live operation.  The
next evidence must come from the normal V7 health caller:

`fresh Matrix profile failure -> automatic affected scope -> automatic
Authority/Planner -> governed execution -> per-member S11`.

The next check records the exact automatic timestamps and compares the
all-affected interval with the binding seven-second product target.  If it
still stops, the next repair must be a newly measured generic runtime defect;
manual recovery remains invalid evidence.
