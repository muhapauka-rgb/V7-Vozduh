# V7 Hot-Path Advisory Planner Deep Profile Report

**Mission:** `V7_HOT_PATH_ADVISORY_PLANNER_DEEP_PROFILE_V1`  
**Mode:** read-only source and normal-cycle profile  
**Verdict:** `OMP_SERIAL_EDGE_CONFIRMED; FRESH_OBLIGATION_OMP_DECOUPLING_REQUIRES_ADMISSION`

## Architectural conclusion

OMP is an Engineering Plane receipt/evidence consumer. It must not be a
synchronous prerequisite for the execution part of:

```text
failure → decision → governed execution → apply → verify
```

The current code already treats OMP as non-authoritative for Candidate,
Packet, lease and apply. However the Matrix refresh service invokes it
serially before the bounded delegated executor, so it is presently a real
blocking order edge even when no OMP work is required.

## Measured and mapped sequence

```text
passive event consumer                    14.402 sec
→ advisory: reconcile → plan → prepared   23.726 sec to prepared decision
→ advisory post-decision materialization  ~38.012 sec
→ OMP receipt consumer                     3.473 sec
→ bounded delegated executor
```

The observed OMP call returned `NO_PENDING_OBLIGATION`; no Candidate, Packet,
lease, route mutation or user movement occurred. The complete systemd cycle
was about 85 seconds wall time, but it was an advisory/certification-only
cycle, not evidence of route-apply latency.

## Exact dependency result

| Edge | Existing evidence | Hot-path classification |
| --- | --- | --- |
| Matrix event → passive consumer | source/current-scope owner | required observation/re-entry edge |
| Advisory → fresh service-failure obligation | existing Autoswitch owner | current decision/preparation edge |
| Fresh obligation → bounded delegated executor | executor receives it directly | OMP is not its data producer |
| OMP consumer → receipt | `v7-truth-check --consume-service-failure-automation-only` | Engineering/receipt edge |
| Existing OMP receipt → later receipt-bound handoff | closure owner | may be required for a later generation; not yet decoupled |

For a fresh advisory obligation, the executor is passed the materialized
obligation directly. The preceding OMP call does not transform it. For the
separate receipt-bound handoff path, however, an existing OMP receipt may be
the owner-backed predecessor; that path must remain unchanged until separately
proven.

## Non-negotiable target boundary

```text
DATA / CONTROL PATH
failure → current state → decision → governed executor → apply → verify

ENGINEERING PATH
OMP receipt → reports / evidence / learning / replay
```

OMP may observe and consume a durable receipt, but it may not delay fresh
governed execution. This is a boundary rule, not permission to bypass Packet,
lease, barrier, validation, recovery or the receipt-bound handoff path.

## Exact next bounded Mission

`V7_HOT_PATH_FRESH_OBLIGATION_OMP_DECOUPLING_ADMISSION_V1` must prove whether
the existing fresh-obligation branch can call the existing governed executor
before the OMP receipt consumer while preserving:

1. identical obligation identity and scope;
2. Packet / lease / barrier / validation contracts;
3. exact-once OMP receipt consumption after execution;
4. unchanged receipt-bound handoff for later generations;
5. rollback by one commit; and
6. before/after measurement from event to executor start.

It must not create an async worker, queue, OMP replacement, new truth source
or parallel lifecycle. It is an admission only; implementation remains blocked
until these conditions are proven.

Runtime effects = `NONE`. Production effects = `NONE`. Authority effects =
`NONE`. CPS is unchanged.
