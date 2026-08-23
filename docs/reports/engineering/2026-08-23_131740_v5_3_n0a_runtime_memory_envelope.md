# V5.3 N0a — Runtime memory envelope

**Date:** 2026-08-23 13:17 MSK  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Block:** `N0a`  
**Outcome:** `PASS_MEMORY_ENVELOPE`; automatic Runtime trigger remains disabled until N8.

## Current owners and boundary

No owner, Runtime, queue, registry, timer or state source was added. Matrix
remains the canonical service-health writer. The existing downstream chain is
still `v7-service-matrix-refresh-all` -> `v7-users-autoswitch` -> governed
Candidate/Packet/Lease/Barrier/apply owners. All profiling that could reach
selection used a copied Polygon state under `/tmp`, `PrivateNetwork=yes`, no
`CAP_NET_ADMIN`, no access to `/opt/v7/egress/state`, and no `apply` against
production.

## Root cause

The production `service-failure-events.jsonl` is **466,785,289 bytes**
(approximately 446 MiB, 179,344 rows at discovery). Three Runtime reads in the
existing autoswitch owner materialized that complete append-only journal even
though their contracts need only a recent event window. The earlier automatic
consumer reached **1,823,195,136 bytes** peak and was killed by the kernel
before Candidate materialization (`Result=oom-kill`). Matrix itself had peaked
near 101 MiB and was not the memory root cause.

## Minimal correction

Commit `f42e29080c79bbe690833a87738877daa3e90a56` adds one bounded read projection
inside the existing owner:

- at most 20,000 recent rows;
- 4–32 MB byte window depending on requested row limit;
- same canonical journal and event schema;
- missing evidence remains fail-closed;
- no cache, persistence, alternate truth or new consumer.

The full-journal reads used by current incident binding, immutable-event
backfill, external wake classification and passive event consumption now reuse
that projection.

## Verification

### Source and tests

- focused causal/Matrix tests: **5/5 PASS**;
- combined autoswitch plus service-failure modules: **280 PASS**, **3 known
  pre-existing fixture-contract failures** identical to the earlier baseline;
- syntax compilation and `git diff --check`: PASS;
- GitHub branch independently resolved to exact commit `f42e2908`;
- safe deploy `deploy-z8-14-Updatesystem-f42e290-20260823T130921`: PASS;
- deployed executable SHA-256 equals local manifest:
  `e89de61aec3b629d7ff2db96a51f582c77b90b2980593cc5d427ecdb6f9744e2`.

### Runtime-size Polygon

The current 466.8 MB production journal and current state were copied to an
isolated server-local Polygon. Results under `MemoryMax=512 MiB`:

| Path | Result | Wall time | Peak memory | Effect |
| --- | --- | ---: | ---: | --- |
| bounded passive-event owner | PASS | 1.84 s | 171.5 MiB | no Candidate/Packet/apply; 0 users |
| full legacy Planner observe, one exact certification user | DRY_RUN with one selected move | 7.90 s | 179.5 MiB (process 183,832 KiB) | no apply; 0 users |
| governed Matrix/CT-M0F consumer | bounded STOP_SAFE at target admission | 27.17 s | 150.1 MiB | source and exact Matrix incident resolved; no target admitted; 0 users |

This proves the previous OOM/unbounded-materialisation defect is removed. The
governed consumer now stops for the independent current target-eligibility
contract (`no_distinct_controlled_contract_admitted_target`), not memory. It
did not repeatedly retry.

## Production effect

- production `users.registry` mtime remains `2026-08-15 01:01:59 +0300`;
- production `egress.registry` mtime remains `2026-08-22 10:14:20 +0300`;
- no route or client movement was performed;
- ordinary Matrix timer remains active/enabled;
- the old 30-second autoswitch timer remains disabled and was not recreated;
- the failed service result remains historical evidence of the old OOM and is
  not re-enabled as a recurring trigger.

## Closure and next step

`N0a` is complete for its stated memory/retry prerequisite. It does not claim
T11 or target admission. The independent target result belongs to later
selection/readiness work and remains fail-closed.

**Exact next step:** execute N1–N4 as one role-based detection block: inventory
the already deployed hard/path, Telegram-critical and moderate required-service
signals; implement only missing Matrix-owned definitive-vs-ambiguous handling;
then run the common MODE A/MODE B Polygon tournament before selecting direct
T0 for any failure class.
