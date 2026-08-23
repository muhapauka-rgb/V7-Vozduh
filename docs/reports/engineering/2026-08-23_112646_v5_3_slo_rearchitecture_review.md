# V5.3 SLO rearchitecture review

**Date:** 2026-08-23  
**Scope:** review and in-place registration of the proposed role-based
Matrix/health amendment; no runtime, route, timer or client mutation was
performed.

## Decision

Adopt the direction as an **amendment of the existing V5.3 Program**, not as a
new Program or parallel health system.  Do not delete the current FAST/C8 or
Full Matrix code before a replacement has passed the same safety, consumer and
scale evidence.  Their roles change:

| Existing mechanism | New retained role |
| --- | --- |
| Matrix canonical writer | sole health/state writer |
| C8 / 30-second deadline loop | reconciliation backstop |
| Full Matrix | staggered deep refresh, disagreement and ambiguous-case fallback |
| Planner, Candidate, Packet, Lease, Barrier, apply and verification | governed recovery path |
| profile contracts, DNS semantics, dedup and rollback | mandatory safety contracts |

The new latency-critical lanes must precede those safeguards: hard/path
event-plus-liveness, Telegram-specific critical health, then moderate required
service sentinels.  Every fast signal still needs bounded, independent Matrix
confirmation before T0 and a current eligible target before any apply.

## Required corrections to the proposed order

1. Add an N0a runtime-envelope gate before N1: the current controlled
   Planner/Packet consumer reached roughly 1.7 GiB peak RAM and was killed by
   the kernel before Candidate creation.  A 3-second SLO is not admissible
   until the existing executor has a bounded memory profile and a successful
   controlled end-to-end run.
2. Treat `<=3 s` as a measured P95 target, not a promise.  It applies only to
   unambiguous hard/path and explicitly Telegram-critical failure classes.  It
   must have per-stage timing and resource budgets.
3. Keep `T11_CLIENT_TRAFFIC_RECOVERED` unchanged and introduce
   `S11_SERVER_SIDE_RECOVERY_VERIFIED` as the present measurable terminal:
   assignment changed, kernel route visible, and required service succeeds in
   that exact routing context.  S11 never claims client-side proof.
4. Telegram must be critical only where the active profile/product contract
   makes it required.  Optional-service failure stays degraded/background and
   cannot evacuate users.
5. “15-minute Full Matrix” becomes a freshness horizon only after a measured
   staggered implementation inside the existing Matrix owner is proven.  It
   may not introduce a queue, timer, state store or second writer.

## Legacy-code decision rule

Do not delete by age or by static caller search.  For each old branch first
record its caller, consumer, state effect, fallback and rollback role.  Then:

1. freeze it from the new critical path;
2. prove the replacement in Polygon and controlled Runtime under identical
   failure, stale/conflict and recovery scenarios;
3. retain it as backstop for one bounded release/evidence window;
4. remove only branches proved unreachable or fully redundant, with a tested
   rollback path.

This avoids both residual request storms and loss of the only conservative
fallback.  In particular, C8, Full fallback and governed apply safeguards are
not deletion candidates merely because a faster signal is introduced.

## Measured baseline and capacity implication

The current production host has 2 vCPU, 3.32 GiB RAM (about 2.12 GiB available
at observation) and no swap.  The normal Matrix service peaked around 101 MiB;
the controlled downstream consumer peaked at 1.70 GiB and was kernel-killed.
The current Full Matrix took 85.675 seconds of lifecycle time (87.192 seconds
wall time) for 7 egresses and 14 services; timer cadence adds up to 15 minutes
plus jitter where no early signal exists.

Consequently, adding 250-ms/500-ms probes to the present process model would
make the system worse.  Hardware alone cannot correct the broad
materialisation/OOM behaviour.  First prove a bounded lightweight execution
inside the existing owner, with no subprocess-per-probe and dedup by active
egress plus service contract, never by user count.

For planning only, after that proof: 4 vCPU / 8 GiB RAM is a reasonable lower
controlled tier for roughly 100 active egresses; 8 vCPU / 16 GiB RAM, fast NVMe
and 1 Gbit/s is the prudent initial tier for the 1,000-egress / 10,000-user
tournament.  This is not a production capacity verdict.  The tournament must
set the final limit from probes/sec, sockets, endpoint pressure, CPU, RAM,
network bytes and Matrix write rate.  At 1,000 active egresses, 1-second L1 is
1,000 probes/sec; 500 ms is 2,000/sec, before hot-target checks.  A 15-minute
deep horizon for 1,000 x 14 services averages only about 15.6 deep probes/sec
when genuinely staggered.

## Exact next action

Completed: the existing Program now contains the binding
`V5.3 current role-based recovery amendment (N0–N11)`.  It adds N0a, the four
SLO classes, S11, probe and data-plane contracts, automatic-consumption rules,
and consumer-proved deletion rules.  It explicitly reclassifies the former C8
and Full Matrix roles.  The reconciliation then removed the incompatible
L1–L12/A–H V5.3 execution text from the live Program rather than merely
labelling it historical.  Its evidence remains in the already referenced
Engineering Reports and Git history, so the Program now has one executable
V5.3 route only.

Program-only validation: `git diff --check` passed.  No application code was
changed, therefore no executable function, timer, request loop or Runtime
consumer was introduced, retained or removed in this block.

**Exact next action:** execute N0a: bounded Polygon profiling and reduction of
the existing governed downstream executor's memory envelope.  Do not change a
cadence, timer or health behaviour before that gate proves one controlled
causal path without OOM or unbounded retries.
