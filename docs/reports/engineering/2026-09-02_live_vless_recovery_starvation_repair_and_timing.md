# Live VLESS recovery: starvation repair and timing

Date: 2026-09-02 (MSK)  
Scope: existing `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`; ordinary live recovery only.

## Purpose

Verify a current ordinary client placed on `vless`, repair only a generic Runtime defect if the normal automatic chain did not progress, and attribute the outcome to the V7 Runtime rather than to an operator or Codex route action.

## Current evidence and diagnosis

- The active ordinary identity `10.7.0.127` was on `vless` and required Google, Google Auth, Instagram and Telegram.
- Matrix independently recorded fresh continuing failures on `vless` for Google, Google Auth and Instagram.
- The Runtime did reach the source-bound automatic consumer (`other_required:vless`).  Therefore the defect was not lack of Matrix evidence, Authority or a manual-target requirement.
- An unrelated source whose governed attempt ended in `l3_production_validation_downstream_proof_failed` was retried for the same unchanged Matrix binding.  Each repeat was synchronous and took tens of seconds, starving newer source bindings.

## Repair

Changed the existing `tools/runtime-support/v7-health-loop` exact-once scheduling behavior:

- every terminal `STOP_SAFE` result is now remembered for the same exact Matrix binding;
- Matrix can re-enter only after a changed source incident, affected profile/service scope, or source assignment;
- no new owner, timer, queue, registry, truth source, Planner, Authority or route writer was added;
- no client was moved by Codex.

Commit and deployed Runtime fingerprint:

`0ed5b22f12957e0d73030d44b77b2eb41e9c875d` — `fix: prevent stale recovery retry starvation`.

## Verification

- focused health-loop tests: `33 PASS`;
- safe deploy: passed, GitHub/local/Runtime aligned;
- `v7-health.service`: active after deployment;
- independent remote branch check: GitHub contains `0ed5b22f12957e0d73030d44b77b2eb41e9c875d`;
- a pre-existing broad test outside the changed path still fails because it expects an obsolete literal call shape in `test_source_bounded_planning_filters_before_decision_construction`; it was not altered or hidden.

## Live automatic outcome

The live Runtime subsequently completed its own source-bound transaction:

```text
fresh Matrix profile binding for vless
-> V7 health caller
-> Matrix / Authority / Planner / Candidate / Packet / Lease / Barrier
-> governed Apply
-> required-service S11
-> 10.7.0.127: vless -> awg0
```

The corresponding Runtime receipt recorded:

- role: `other_required:vless`;
- `action_completed=true`;
- `runtime_mutation_performed=true`;
- `users_moved=1`;
- `stop_reason=""`;
- Matrix T0 to consumer start: `428 ms`;
- Matrix T0 to terminal required-service result: `16,453 ms`.

After the transition, Matrix showed Google, Google Auth, Instagram and Telegram all `OK` on `awg0` for the profile's requirements.  This is valid automatic provenance: no user-specific route command, target injection, Candidate, Packet, Lease, Barrier or registry mutation was issued by Codex.

## Timing conclusion

This is a successful automatic recovery, but **not** a 7-second success.  The governed receipt attributes about 7.0 seconds to Planner, Packet/Lease, Barrier, Apply/verification and feedback; the remaining elapsed time is earlier work inside the existing governed process.  The live bound remains `T0 -> all affected users recovered <= 7 s`; the measured `16.453 s` is failure evidence, not acceptance credit.

## Next frontier

Keep the implementation and safety semantics intact, instrument the existing governed-process pre-transaction interval, identify the remaining synchronous span above 100 ms, then make one bounded generic repair and validate it only through a new live V7-originated Matrix event.  No manual user recovery is admissible as proof.
