# V5.3 N1–N4 role signal and Matrix confirmation tournament

Date: 2026-08-23 14:05 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Current architecture: `V5.3 N0–N11 ROLE-BASED FAST RECOVERY ARCHITECTURE`  
Block: `N1–N4`  
Disposition: `IMPLEMENTED_REPLACEMENT_PENDING_N7_N8_RUNTIME_PROOF`

## Result

The current Matrix owner now has one explicit, fail-closed distinction:

```text
DEFINITIVE LOCAL HARD FAILURE
interface absent or administratively down
-> Matrix re-reads registry + interface + freshness + identity generation
-> MODE B direct canonical T0
-> no redundant source network probe

EVERY REMOTE OR SERVICE AMBIGUITY
timeout / tunnel-up-internet-down / Telegram / DNS / HTTP / partial / multi-service
-> SUSPECT
-> two independent producer observations where applicable
-> MODE A targeted Matrix confirmation
-> T0 only after Matrix confirmation

STALE / WRONG GENERATION / REPLAY / CONFLICT / CORRELATED FAILURE
-> STOP_SAFE or DEGRADED
-> no action
```

Matrix remains the only canonical state/event/T0 writer. The existing health
loop, egress diagnose, Telegram sentinel and Matrix test are reused. No owner,
timer, queue, watcher, registry, cache, Planner or truth source was added.

## Selected tournament values

| Role | Candidates | Selected | Why |
| --- | --- | --- | --- |
| N1 local hard liveness | 250/500/1000/2000 ms | 1000 ms | 1,000 active-source sysfs scan is 0.37 s; one second preserves margin for the downstream 3-second class without 2–4x needless reads |
| N2 Telegram-required profile | 250/500/1000 ms | 1000 ms, two failed samples on distinct rotating endpoints | lowest admitted endpoint rate; one socket per role-scoped source per cycle; single endpoint glitch cannot confirm failure |
| N3 other required service | 5/10/15/30 s | 5 s | only cadence that leaves room for two observations plus targeted Matrix confirmation inside the 15-second class |
| N3 global probe cap | 8/16/32/64/128 | 128 | 500 ms timeout-bound 1,000-contract pass is at most 4.0 s only at C128; healthy loopback pass is about 0.13 s |
| N4 definitive hard failure | MODE A repeat vs MODE B direct | MODE B only for `INTERFACE_DOWN_OR_MISSING` | Matrix independently revalidates the local kernel fact; direct T0 measured 0.28 s and is idempotent |
| N4 all ambiguous evidence | MODE A vs MODE B | MODE A retained | no remote timeout or service result is definitive enough to skip independent confirmation |

N3 fast work is limited to three non-Telegram required services per distinct
source/profile contract. A wider contract is `STOP_SAFE` for FAST and remains
eligible for DEEP/Full; `1000 x 14 x 1-second` probing is impossible by
construction. Telegram is owned by N2 and excluded from N3 batch work.

## Implementation

### Existing Matrix owner

`tools/v7-service-matrix-test` now:

- validates definitive local signals against current `egress.registry`, exact
  interface, identity generation and a three-second freshness ceiling;
- rejects all non-admitted classes, stale/future timestamps, wrong generation,
  missing/disabled sources, interface mismatch, current-UP conflicts and
  unknown interface state;
- writes the internal `__channel_liveness__` evidence row and canonical event
  atomically with `persistence_samples=1` only after validation;
- retains normal catalog totals and route-class service fitness separately;
- skips the expensive network-path projection on this exact critical path,
  because the local interface was already revalidated by Matrix;
- exposes a single-process, observation-only N3 batch executor with bounded
  contract/service/concurrency limits and no durable Matrix write.

### Existing signal producers

`tools/v7-egress-diagnose` now:

- joins active users to registry sources once and performs cheap local liveness
  reads; it never scans users in the incident consequence path;
- invokes direct Matrix validation only for a detected current-source local
  failure and wakes only the existing consumer for a newly emitted event;
- uses one ephemeral N3 work set and one Matrix process for lightweight batch
  TCP/DNS suspicion, instead of one Python/Matrix process per contract;
- retains the existing two-sample parent gate and targeted Matrix receiver for
  ambiguous N3 evidence;
- can emit hard-lane telemetry to stdout, so the lane adds no durable state.

`tools/v7-telegram-sentinel` now supports the N2 role contract:

- exact active sources only for profiles declaring Telegram required;
- one rotating endpoint per cycle;
- two failed samples on distinct endpoints;
- correlated all-source failure becomes `DEGRADED/STOP_SAFE`, not a fan-out of
  evacuations;
- C1–C128 bounded cross-source concurrency.

Legacy default flags remain unchanged until N8 controlled Runtime admission.
The existing 4-second Telegram timer and 30-second health behavior are still
the active production callers in this block.

### Existing health owner

`tools/runtime-support/v7-health-loop` contains a non-active role-based mode:

- HARD and Telegram schedules are independently due at one second;
- other-required service work is due at five seconds;
- long service work cannot block HARD deadlines;
- one invocation per role is allowed; overlap becomes a visible deadline miss,
  never a backlog or catch-up storm;
- every child belongs to and is reaped by the one foreground health owner.

`systemd/v7-health.service` was deliberately not changed in N1–N4. Runtime
activation, old-timer retirement and unattended caller proof belong to N8.

## Polygon evidence

### Current server shape

On a copy of current production registry/user state, the local HARD scan saw
six active sources, all locally UP, emitted zero T0 events and requested zero
consumer wakes. Duration was `0.596 s`. Matrix and event files were impossible
in this read-only run because the Matrix command was replaced with `/bin/false`.

### 1,000-source HARD scale

The first 1,000-source attempt exposed an O(n²) shell join (one registry/user
search per source). It exceeded 30 seconds and was rejected. The owner was
repaired to perform one in-memory join and one bounded sysfs read per source.

Accepted same-server Polygon after repair:

| Measure | Result |
| --- | ---: |
| active sources | 1,000 |
| local failure observations | 0 |
| canonical writes | 0 |
| elapsed | 0.37 s |
| peak RSS | 12,332 KiB |
| user CPU | 0.19 s |
| system CPU | 0.09 s |

### MODE B direct T0

An isolated temporary Matrix/event directory and a synthetic missing interface
produced exactly one canonical T0 event:

| Measure | Result |
| --- | --- |
| disposition | `MODE_B_DIRECT_T0` |
| Matrix result | `CANONICAL_T0_WRITTEN` |
| source network probe | skipped |
| event count | 1 |
| repeat behavior | same episode, no duplicate new event |
| elapsed | 0.28 s |
| peak RSS | 27,704 KiB |

Stale, wrong-generation and every ambiguous class produced `STOP_SAFE` and no
Matrix file/event in focused falsification tests.

### N2 current role scope

Two isolated cycles against the current server interfaces selected exactly one
active Telegram-required source (`wireguard-1779454504-c43409`). Both cycles
were healthy, used one rotating target and emitted no failure/event/action.

| Cycle | elapsed | probe time | checked sources | blocked |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0.32 s | 0.060 s | 1 | 0 |
| 2 | 0.30 s | 0.056 s | 1 | 0 |

State, Matrix and events were temporary. A PATH-scoped fake `systemctl` made a
production consumer wake impossible even if the Polygon had failed.

### N3 current role scope and scale

Current copied profiles produced two distinct contracts, but only one had N3
services; it performed two lightweight probes (`google`, `youtube`), made zero
Matrix writes/receiver calls and completed in `0.75 s`, peak RSS `27,932 KiB`.

The local 1,000-contract real loopback TCP tournament completed:

| Cap | owner probe wall | external wall | probes | failures |
| ---: | ---: | ---: | ---: | ---: |
| 32 | 129.437 ms | 0.1368 s | 1,000 | 0 |
| 64 | 130.121 ms | 0.1380 s | 1,000 | 0 |
| 128 | 127.667 ms | 0.1355 s | 1,000 | 0 |

Healthy throughput alone did not select C128; the selection comes from the
physical-timeout bound: `ceil(1000/128) * 0.5 s = 4.0 s`. C64 can require
8.0 s and cannot reliably sustain a five-second phase under full timeout.

## Verification

- New N1–N4 focused suite: PASS.
- Existing health-loop, egress-diagnose, Telegram-sentinel and fast-signal
  regression suites: PASS.
- Existing Matrix full/subset and candidate failure-matrix loopback suites:
  `11/11 PASS`.
- Combined non-loopback focused suites: `61/61 PASS`.
- Existing broad service-failure baseline retains only the three previously
  recorded CT-M0F fixture-contract failures; no new failure was introduced.
- shell syntax, Python compile and `git diff --check`: PASS.

## Publication and deployment

- implementation commit: `c6024218`;
- O(n²) repair commit: `92064629`;
- truthful batch-concurrency telemetry and causal scheduler-test repair:
  `3acd13e0`;
- all three published to `origin/Updatesystem`;
- safe deploys:
  - `deploy-z8-14-Updatesystem-c602421-20260823T135239`;
  - `deploy-z8-14-Updatesystem-9206462-20260823T135713`;
  - `deploy-z8-14-Updatesystem-3acd13e-20260823T140714`;
- final deployed tool hashes match local source;
- full GitHub/CPS/Runtime/state truth check after the final deploy:
  `FULLY_ALIGNED`, `PASS`, blockers `0`.

## Runtime and production effect

The capabilities are deployed but not activated. Production still runs:

- `/usr/local/bin/v7-health-loop` without `--role-based-fast`;
- the existing 4-second Telegram timer;
- the existing 15-minute Full Matrix timer.

No production Matrix cadence, failure threshold, consumer policy, route,
Packet, lease, client or interface was changed. No client moved.

## Replacement closure and exact next step

N1–N4 design, implementation and tournament are complete. Responsibility
retirement is intentionally pending N7/N8 integrated/unattended proof. The old
30-second/4-second callers, shadow names and compatibility persistence cannot
be removed before that evidence exists.

Exact next block: **N5–N6**.

```text
N5: existing Planner/Matrix/capacity owners
-> bounded top-H pre-ready targets
-> fact-specific freshness + compatible-target dedup
-> prepared data plane for 1/10/100/1000 compatible clients

N6: existing Matrix writer
-> staggered fair DEEP horizon
-> bounded rate/concurrency
-> FAST priority, no catch-up storm
-> Full fallback for disagreement/stale/conflict/ambiguity
```

Overall Program progress after this block: **30%**.
