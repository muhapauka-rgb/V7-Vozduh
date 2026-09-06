---
name: v7-autonomous-recovery
description: Run the V7 autonomous recovery engineering campaign when the user says `AUTONOMOUS_RECOVERY FULL_CAMPAIGN`. Use only in this V7 repository.
---

# V7 Autonomous Recovery

## Persistent compact-command contract

On `AUTONOMOUS_RECOVERY FULL_CAMPAIGN`, read the current CPS, OMP, SYSTEM_MAP,
Service Failure Program and
`docs/programs/V7_AUTONOMOUS_RECOVERY_ENGINEERING_AGENT_PROGRAM.md`. Invoke
`tools/v7-truth-check --json AUTONOMOUS_RECOVERY FULL_CAMPAIGN` and retain the
same Mission until Program Section 8 is behaviorally accepted or an exact
legal boundary is consumed. Packet-ready, a test, report, commit, repair or one
experiment is never a terminal.

If a real `STOP_SAFE`, stale packet, missing proof, conflicting contract or
external boundary occurs, emit one `CONTROLLER_ESCALATION` directly to the
active controlling Codex task: exact condition, evidence, affected owner,
safe independent work and the smallest required decision. Do not ask the user
to relay it. This is orchestration transport, not a V7 Runtime component; hold
only the dependent branch and continue independent safe work.

`FULL_CAMPAIGN` is always one explicit manual admission to the existing OMP
flow: it must create one new frozen-snapshot Polygon experiment from current
CPS even when no source diff exists. A missing material diff may suppress only
the `MATERIAL_CHANGE` trigger; it is never a legal terminal for `FULL_CAMPAIGN`.
The same OMP flow may also be entered by a bounded cadence slot, with one
single-flight lease and duplicate suppression per slot. It must not self-wake,
spin, or add a scheduler; an existing OMP caller supplies that bounded re-entry.

Before a first full campaign after native-transport changes, invoke
`tools/v7-truth-check --json AUTONOMOUS_RECOVERY NATIVE_SMOKE`. It is one fresh
read-only Analyst transport acceptance, not a Polygon campaign: require an
observed `thread.started`, a strict final JSON object, and a complete native
attempt envelope. A failed smoke is an exact `STOP_SAFE`; do not start Docker,
repair or the full campaign until the existing native-context adapter has a
diagnosable lawful re-entry.

## Native role flow

1. Dispatch one fresh native `ANALYST` context with the immutable packet and
   current owner evidence. It performs causal/semantic analysis and recommends
   only an existing-owner change.
2. Codex checks repository and Runtime facts. It may record a bounded
   `LOCAL_EXECUTION_ADAPTATION`; it may not narrow the objective, Definition of
   Done, Authority or safety boundary.
3. Freeze the Analyst result and dispatch a distinct fresh
   `INDEPENDENT_REVIEWER` context. The Reviewer checks Architecture,
   Safety/Regression, Evidence and Mission Integrity and does not rewrite the
   proposal. Its immutable packet must include the current producer, current
   caller/consumer and existing-owner execution path for the isolated Polygon;
   it must echo that evidence fingerprint and
   `ISOLATED_POLYGON_ENGINEERING_ONLY`. A documented capability without a
   current execution consumer does not satisfy this role. The Reviewer must
   reject missing/tampered owner evidence, but must not require or infer
   Runtime, Production, user-effect or Section 8 closure evidence from this
   engineering-only packet.
4. One rejected item permits at most one targeted Analyst re-entry. A second
   rejection is `STOP_SAFE_EXACT_GAP` with owner and re-entry condition.
5. An admitted repair uses the existing owner and normal OMP workflow. Preserve
   the origin experiment identity, return automatically, replay the same
   obligation, then run dependent selective regression.
6. Continue the next independent safe obligation automatically. Never ask the
   user to copy packets, checkpoints, reviews or continuation commands.

## Boundaries

The agent is an OMP execution profile, not a Matrix, Planner, Authority,
route/S11 writer, coordinator, queue, registry, scheduler or truth source.
Destructive faults are confined to a proven isolated Polygon. Production
faults are never fabricated. Python may package, fingerprint and validate; it
may not manufacture semantic analysis or Reviewer PASS.

Campaign results are persisted only through the existing immutable historical
evidence owner. The artifact is bounded and redacted: retain identities,
fingerprints, terminal, compact Section 8 receipts and review bindings; never
retain prompts, full agent messages, or turn a report into a new truth source.
