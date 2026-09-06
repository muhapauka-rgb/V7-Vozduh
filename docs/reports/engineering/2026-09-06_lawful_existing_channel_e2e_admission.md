# Lawful existing-channel E2E admission — 2026-09-06

## Decision

`STOP_SAFE_NO_LAWFUL_EXISTING_CONTROLLED_CHANNEL`

This terminal is not caused by VLESS. A new, controller-authorized discovery
through existing Matrix, topology and Authority owners found a viable existing
controlled source, but no current exact Authority/Product Contract permits the
five-certification-user transition into the shared healthy target. No new
channel, user, owner, infrastructure or architecture was created.

## Fresh evidence

The existing `v7-service-matrix-test` writer refreshed the only empty,
independently controllable source candidate:

- source: `amneziawg-exec-20260528-10-8-1-14`;
- timestamp: `2026-09-06T20:44:07.090755+00:00`;
- baseline: `OK`, `14/14` services;
- current source capability: zero ordinary identities, zero certification
  identities, capacity 9 after reserve, stable, empty-reservation eligible,
  and whole-source failure independently controllable.

The fresh topology owner therefore selected the source as
`OPTION_1_REBIND_EXISTING_EMPTY_EGRESS`. It is capable of the five-user stage
without affecting ordinary users.

| Existing channel | Health/stability | Ordinary / certification identities | Controlled-source result |
| --- | --- | --- | --- |
| `amneziawg-exec-20260528-10-8-1-14` | healthy / stable | 0 / 0 | viable empty source; requires existing rebind Authority action |
| `awg3` | healthy / stable | 29 / 24 | forbidden: whole-egress fault would affect ordinary users |
| `wireguard-1779454504-c43409` | healthy / stable | 46 / 1 | forbidden as source; viable shared destination only |
| `1` | unhealthy / unstable | 0 / 1 | no healthy baseline and occupied source |
| `awg0` | unhealthy / stable | 0 / 25 | no healthy baseline and occupied source |
| `openvpn-1779388847-d2ad7c` | unhealthy / stable | 0 / 1 | no healthy baseline, occupied and no remaining capacity |
| `vless` | unhealthy / unstable | 0 / 1 | independently blocked by external listener/profile repair |

## Exact blocker

The existing target-capacity owner proved that the healthy shared WireGuard
target has capacity for five certification users while preserving all 46
ordinary users and forbidding any target fault. Its exact boundary is
`EXACT_SHARED_PRODUCTION_TARGET_ACTION_CLASS_CONTRACT_REQUIRED`.

The existing source-topology Authority entrypoint was invoked only to prepare
the rebind request. It returned
`STOP_SAFE_PREDECESSOR_REQUIRED` with the same target-contract boundary; it
created no reservation, cohort binding, Candidate, Packet, Lease, route,
policy, fault or user movement. The old Authority preflight is stale, and the
standing policy does not delegate either this source rebind or the shared
target action class.

## Minimal lawful successor

The existing `admin_core/operator_execution.py` Engineering Authority/policy
owner must issue one fresh, immutable
`EXACT_SHARED_PRODUCTION_TARGET_ACTION_CLASS_CONTRACT` scoped to exactly five
existing certification/test users, source
`amneziawg-exec-20260528-10-8-1-14`, and the owner-selected shared WireGuard
target. It must explicitly preserve ordinary assignment and route fingerprints
and forbid target fault/restart.

Only after that contract exists may the existing source-reservation owner bind
the cohort, revalidate the target, and consider the already-prepared five-user
Runtime gate at `031b016f`. No deploy, physical fault, user movement, routing
change, latency claim, 1,000/10,000 campaign or production credit is currently
lawful.
