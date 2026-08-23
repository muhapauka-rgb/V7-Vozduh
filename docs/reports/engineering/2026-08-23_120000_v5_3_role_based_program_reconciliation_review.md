# V5.3 role-based Program reconciliation review

**Date:** 2026-08-23  
**Scope:** read-only comparison of the restored V5.3 Program with the proposed
role-based recovery plan and the supplied independent review.  No Runtime,
route, timer, Matrix or client change was performed.

## Verdict

The new N0–N11 contract contains the intended architecture, but the restored
Program is not yet a fully unambiguous executable contract.  The required
repair is surgical: preserve the prior V5.3/CT/V4 evidence and contracts, but
add narrow precedence and semantic-mapping laws where old wording could be
misread as a prohibition or alternate requirement for N0–N11.  Do not delete
the broader Program again.

## Required amendments

1. Use two clocks.  Polygon measures controlled failure/outage onset -> S11;
   production records first failed observation -> S11 plus last-success ->
   first-failure cadence delay.  Never pass a 3-second target by starting the
   clock after a long unnoticed outage.
2. For HARD/PATH and Telegram require P95 `<=3s` **and** no valid controlled
   sample above `5s`, including immediately-before/after/mid-interval failure
   placement.  A budget miss is a failed performance sample and open residual,
   even if STOP_SAFE/fallback was safe.
3. Require class-specific S11 and confirmation max-wall/timeout/retry budgets:
   lightweight route payload for HARD/PATH, Telegram payload for Telegram,
   and exact service-X for other-required classes.
4. Add correlated-failure suppression: source Telegram failure is failover
   eligible only when compatible hot target evidence passes; widespread
   independent target failure is a correlated-service incident, not a switch
   storm.  Apply the equivalent rule to shared path-probe failure.
5. Define hot-target freshness by fact type, deduplicate by compatible target
   fingerprint, and require at least one pre-ready eligible hot target for a
   source to claim the 3-second class.  Otherwise record
   `NO_3S_TARGET_CAPACITY`.
6. Bind N5 to the existing V4 constant-time cohort/data-plane invariants.
   The SLO applies to an eligible compatible affected routing class, not only
   the first moved identity.  Exception identities retain an explicit slower
   path.
7. Make N6 scheduling measurable: fast lanes always win; bounded global deep
   rate/concurrency and fairness; no catch-up burst; missed horizon becomes
   stale rather than a probe storm.
8. Change N0a from a global research blocker to a prerequisite for N8 and
   production activation only.  N1–N7/N9 Polygon, profiling and scale work may
   continue independently under existing owners.
9. Add a narrow V5.3 fast-wake precedence law: L0/L1P/L1T/L2 may legally wake
   targeted Matrix confirmation.  Old “timer is sole wake producer” wording
   remains limited to the named CT-M0F sample-generation contract and cannot
   delay N1–N4.
10. Distinguish allowed controlled evidence from forbidden manufacture:
    Polygon fault injection and exact-owner-authorized controlled
    certification are allowed where existing policy admits them; manufactured
    ordinary production failure and repeated production action merely to fill
    samples remain forbidden.
11. Map historical server-bound `CLIENT_TRAFFIC_RECOVERY_*` receipts to S11
    for N0–N11 consumption.  They cannot prove T11 without independent client
    telemetry.
12. N3 must select one measured other-required observation SLO after its
    tournament, including cadence phase, timeout and confirmation—not retain a
    permanent `10–15s` range.

## Product decision required

The supplied review correctly identifies an ambiguity that cannot be resolved
by engineering: whether Telegram’s 1–3-second class applies to every active
source serving enabled clients, or only to profiles that declare Telegram
required.  The Program currently uses the latter.  This choice changes which
outage may move clients and therefore needs explicit product direction before
the text is changed.

## Exact next action

After that one decision, amend the existing N0–N11 section and the few named
legacy statements in place; retain all unrelated Program contracts.  Then N0a
and N1–N7/N9 continue in parallel according to their independent gates.

