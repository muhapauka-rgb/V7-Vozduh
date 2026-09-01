# OMP full consistency and failure-mode audit

Date: 2026-09-01  
Scope: complete read-only review of `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` (12,058 lines), its live-state pointers, the current CPS and the active Service Failure Program.  No Runtime, route, client, Matrix, timer, Authority or Program rule was changed.

## Verdict

`OMP_FULL_AUDIT = CONDITIONAL_PASS`.

The OMP's executable safety model is coherent.  It has no discovered document-to-Runtime path that can itself move a user, delete a route, bypass Authority, or silently weaken recovery.  The current machine-checked CPS/OMP projections agree on the active frontier:

```text
RECOVERY_STABILITY_FOUNDATION
-> existing Matrix/health reconciliation consumer
-> normal V7 Runtime remains the only recovery producer
```

`./tools/v7-truth-check --local` passed with `LOCAL_ALIGNED`.  The only warning is pre-existing unrelated untracked engineering reports.  Independent remote verification was not available in this audit because DNS could not resolve `github.com`; no publication claim is made.

## What is safe and should remain

1. CPS section 0 is explicitly the only authoritative volatile state.  Both OMP live pointer projections (`§20.2` and `§26`) agree with it and the checker verifies both.
2. A current recovery cannot be created from a report, a test, a manual route command or a historical event.  The only accepted recovery path remains the live V7 chain: health -> Matrix -> scope -> Authority -> Planner -> governed execution -> required-service S11.
3. Active safety conflicts fail closed.  Historical operations and advisory residue must not suppress a new current recovery; an exact re-entry condition is required.
4. The replacement/delete law requires migrated current consumers, regression evidence, a real fallback/rollback trigger and a named owner before old executable paths can be removed.
5. The new simplification-first law is bounded to affected components.  It does not add a Runtime hop, write, owner, state surface, queue or synchronous check.  Its `NOT_APPLICABLE` treatment for simple document edits prevents a global reporting ritual.

## Findings

### P1 — stale current-looking mission reference in the OMP header

The header still calls the August Atlas report the “Current active Mission report”, while OMP `§26` and CPS section 0 correctly identify `RECOVERY_STABILITY_FOUNDATION` and the 2026-09-01 foundation-admission report.

Impact: the parser and Runtime do not consume the header, so this cannot automatically switch or strand a client.  A human or future engineering agent reading only the header can nevertheless reopen a superseded Mission or reason from stale assumptions.

Required correction: make the header historical or reduce it to a pointer to CPS/OMP `§26`; it must never carry an independent volatile “current” field.

### P1 — V4.86 registration wording is now historically true but visually current

The V4.86 block says its registration “does not admit implementation” and that the first frontier will be selected later.  CPS now shows that the `RECOVERY_STABILITY_FOUNDATION` has been admitted.  This is correct as registration history, but it is not labelled as such near the document top.

Impact: no executable consumer uses this paragraph, but it can cause a false no-op decision or an unnecessary new admission cycle.

Required correction: label it `HISTORICAL_REGISTRATION` and add one short forward pointer to CPS section 0.  Do not alter the underlying safety or execution law.

### P2 — duplicated human navigation points for the single CPS pointer

OMP intentionally has two checked CPS projections (`§20.2` and `§26`).  They currently match and the source checker verifies both, so this is not a second truth source.  It is still a drift surface: any future manual edit can leave one readable projection stale even though the other remains correct.

Required correction: retain both only if generated/atomically updated by the existing reconciliation owner; otherwise make `§20.2` a one-line reference to `§26`/CPS.  The existing atomic writer already updates both, so no new owner is needed.

### P2 — simplification rules are semantically aligned but distributed

The same safety intent exists in V4.87, RT2 post-Reset contracts and RS7 physical-simplification gates: reuse first, consumer migration before deletion, hot-path protection, and no evergreen compatibility.  They do not select competing current frontiers because RT2/RS7 are explicitly `CONTRACT_READY_NOT_ADMITTED` and CPS controls the frontier.  The cost is comprehension: a future change author can overlook which clause is the controlling common law.

Required correction: add cross-references that name V4.87 as the common law and RT2/RS7 as specialized implementation gates.  Do not merge or delete the detailed RT2/RS7 safeguards.

### P2 — `REAL_WORLD_LIMIT` is easy to misread while the Foundation remains active

CPS legitimately records a global historical/natural-evidence boundary while also admitting an independent Recovery Stability Foundation.  The checker has an explicit allowed case and current pointers are consistent.  This is not a logical conflict, but a dashboard/operator reader may incorrectly interpret `REAL_WORLD_LIMIT` as “all work must stop”.

Required correction: present the stop as lane-scoped in the human-facing projection: natural-evidence lane blocked; Recovery Stability Foundation continues.  No relaxation of a true external safety boundary is allowed.

## Failure scenarios assessed

| Scenario | Current protection | Residual risk | Audit result |
| --- | --- | --- | --- |
| A historical report starts a recovery | CPS-only rule; reports cannot select a Mission or create an action | Human may follow the stale header manually | Protected in Runtime; P1 documentation repair |
| Simplification deletes a still-required route/recovery path | consumer migration, fallback trigger/exit, regression and residue gates | gate can be ignored only by an out-of-contract manual change | Protected by OMP; preserve gates |
| A temporary compatibility path becomes permanent | explicit cutover/removal condition required | existing old paths need a later bounded consumer audit | Protected prospectively; P2 cleanup backlog |
| A safety conflict causes an unsafe switch | fail-closed Matrix/Authority/route governance | may delay recovery, never authorizes an unsafe route mutation | Correct safety behavior |
| One finished operation blocks a new affected scope | current-truth and level-triggered re-entry law | active implementation proof is still the current Foundation work | Correctly identified current work, not an OMP contradiction |
| OMP modernization slows the hot path | V4.87 has no Runtime effect; hot-path gates require before/after measurement | a future implementer could over-apply reporting rules | No present slowdown; affected-scope rule must be retained |
| Global audit/RT2 contract pauses recovery work | RT2 is not admitted; no-unnecessary-waiting rule keeps independent ready work moving | human could confuse contract readiness with live frontier | P2 navigation risk only |

## Effect on modernization and optimization

The current modernization direction is sound: simplify current ownership and state/consumer edges before adding logic, while keeping fallback until real migration closure.  It improves long-term recovery reliability and does not add synchronous checks to the seven-second path.

The danger is not the law itself; it is over-broad reading of it.  The law must stay *affected-scope only*.  A recovery defect may receive one minimal existing-owner repair and affected regression; it must not be held up by a full repository simplification audit or by historical performance work.

## Exact next safe action

Run one document-only `OMP_CURRENT_HISTORICAL_PROJECTION_HYGIENE` correction:

1. retire/label the stale header “Current active Mission” field;
2. label V4.86 registration wording as historical and point to CPS;
3. make the two existing pointer projections visibly derived from CPS/atomic reconciliation;
4. add only cross-references between V4.87 and RT2/RS7;
5. run the existing truth check.

This is a documentation coherence repair only.  It must not modify Runtime, Matrix, Planner, health cadence, routes, clients, Authority, or the current Recovery Stability Foundation frontier.
