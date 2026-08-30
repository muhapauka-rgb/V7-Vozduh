# V7 VLESS total-outage full-path 7 s acceptance

Date: 2026-08-30  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_VLESS_TOTAL_OUTAGE_FULL_PATH_7S_ACCEPTANCE`

## Result

`V7_VLESS_TOTAL_OUTAGE_FULL_PATH_7S_ACCEPTANCE` is **not yet credited**.
The current live state no longer contains an owner-admitted ordinary VLESS
cohort with required services that V7 may move.  Recreating such a cohort or
moving a user back to VLESS would violate the mission's strict automatic-origin
law, so no manual recovery or synthetic incident was used.

## Current VLESS facts

Fresh V7 Matrix observation at `2026-08-30T11:13:39Z` is source-bound to
`tun0` (`SO_BINDTODEVICE_OR_CURL_INTERFACE`), with matching current interface,
routing and identity fingerprints.

| Service | Current V7 result |
| --- | --- |
| Google / Google Auth / Instagram / YouTube | failed: TLS unexpected EOF |
| Telegram | healthy: all required Telegram samples connected |
| Channel liveness | local interface recovered |

Therefore the asserted **total** VLESS outage is not presently proven: the
current evidence is a real partial profile-service outage, not a Telegram-wide
channel failure.  This is not treated as a Matrix cache or default-route escape
because the current probe records its VLESS interface binding.

Current VLESS users:

- `10.7.0.13`: enabled ordinary user, but no declared required-service profile;
  it is not lawful to mark this user affected merely because other services fail.
- `10.7.0.125`, `10.7.0.126`, `10.7.0.127`: automatically recovered by V7 to
  `awg0` during this mission; each final route and required-service result was
  successful.

The only other currently assigned failed source found in the same read-only
reconciliation belongs to a certification identity, not an ordinary user.

## Existing live automatic recovery evidence

V7, not Codex, performed operation
`runtime_autoswitch_7bc963ba4b7b5ee1d4ee903f`:

- source: `vless`;
- members: `10.7.0.125`, `10.7.0.126`, `10.7.0.127`;
- target selected by V7: `awg0`;
- all three route and service receipts: success;
- Matrix record: `L3_PRODUCTION_PROVEN`;
- no route-writer, target, Candidate, Packet, Lease, Barrier or assignment was
  invoked or created by Codex.

That pre-fix transaction was valid functionally but failed the latency
acceptance.  Its measured critical spans were:

| Stage | Measured duration |
| --- | ---: |
| V7 governed execution process | 31.676 s |
| Three serial route-writer calls | 2.063 s, 1.970 s, 2.284 s |
| Three serial required-service checks | 4.617 s, 4.523 s, 4.551 s |
| Apply and verification total | 21.625 s |
| Post-success passive/learning tail | 8.500 s |

The governed action started at `10:58:56.515Z` and completed at
`10:59:30.836Z`.  It is not a 7-second result and receives no SLO credit.

## Repair deployed

Commit: `d28f28cab5ffd78f74845724439fb47794907253`  
Deploy: `deploy-z8-14-Updatesystem-d28f28c-20260830T141201`

The repair consumes only existing owners:

1. A bounded 2–4 member `EMERGENCY_FAILOVER` may use the already active
   Core-primary cohort commit, subject to the exact existing operation control.
   If Core-primary is unavailable, V7 retains the historical serial path.
2. Each user still receives an exact route verification.
3. For users with one selected target, the existing Matrix verifier checks the
   union of their declared required services once for that target, instead of
   repeating the same channel-level probe per user.
4. Any route, service or Core-primary failure retains the existing rollback and
   containment path.

No new owner, timer, queue, registry, source of truth, target-selection rule or
manual operational path was added.

Focused verification passed: 379 tests (`v7-user-switch`, autoswitch policy,
service-failure episode).  Safe deployment passed; GitHub, local commit and
installed Runtime hashes are aligned; `v7-health.service` is active.

## Exact remaining acceptance boundary

The next valid evidence must be produced by the normal live V7 caller when a
current ordinary user with declared required services is actually affected by a
fresh VLESS (or equivalent ordinary failed-source) observation.  The record
must include first valid observation, Matrix T0, automatic scope, V7-selected
target, governed apply, each member S11 and all-affected elapsed time.

Until that current owner-backed event exists, claiming `<= 7 s` would be false.
Codex must not manufacture it or move users to create it.
