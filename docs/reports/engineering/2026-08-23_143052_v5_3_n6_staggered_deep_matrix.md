# V5.3 N6 — staggered deep Matrix refresh

Date: 2026-08-23 14:30 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Phase: `N6 STAGGERED_DEEP_MATRIX`  
Implementation: `c74db2c822ced8917a766501f6dc9a48dabb5418`  
Deploy: `deploy-z8-14-Updatesystem-c74db2c-20260823T142328`

## Result

N6 is complete as an implemented and deployed capability. The existing
`v7-service-matrix-refresh-all` Matrix owner now supports a deterministic
staggered DEEP observation mode. It does not create a cursor, queue, registry,
timer, state store or second Matrix writer.

The current sorted egress inventory is split across a 900-second horizon using
60-second restart-stable slots. A slot executes only its own bounded slice with
configured concurrency (`16`, hard maximum `128`). Missed work becomes stale;
it is never replayed as a catch-up burst. The explicit Full path is unchanged
and remains the fallback for stale, conflicting, ambiguous or disagreement
cases.

The existing `v7-health-loop` contains an inactive 60-second DEEP role command.
It remains under the same health owner and will be activated only in N8 after
N7 proves the integrated chain.

## Evidence

- Focused N5/N6/role/health/Routing Core suite: 34 tests passed in 10.349 s.
- 1,000 egress rows across 15 slots are covered exactly once; maximum slice is
  67 rows.
- A stale set of 100 rows does not create catch-up: one selected slot remains
  at most 7 rows.
- Current-state isolated Polygon used only copies of production
  `egress.registry` and `service-matrix.json`, with `/usr/bin/true` as a
  no-network/no-write checker:
  - current inventory: 7 egress rows;
  - selected slot: exactly one egress (`wireguard-1779454504-c43409`);
  - next slot: zero rows;
  - owner elapsed: 0.007 s; external elapsed: 0.13 s;
  - peak RSS: approximately 35 MiB;
  - Matrix writes, route changes and client movement: none.
- A first local attempt referenced absent macOS `/bin/true` and failed before
  any state or network effect. It was corrected to `/usr/bin/true`; this is
  retained as negative evidence rather than hidden.

## Runtime and production effect

Production hashes match local authoritative files for:

```text
v7-users-autoswitch              5580482c...47ec2
v7-service-matrix-refresh-all    2ed9d36c...e862
v7-health-loop                   8c679b52...e3a45a
```

`v7-health.service` is active, but its ExecStart still has no role-mode flag.
The predecessor Full Matrix timer and Telegram sentinel timer remain active.
This is intentional: N6 deploy supplies the replacement capability; N7/N8
must prove the integrated replacement, migrate the real caller and only then
retire the predecessor timers. No production route or client state changed.

## Limits and next step

N6 does not claim that FAST always outranks DEEP under real contention or that
the role loop is already the production caller. N7 must run both modes through
the same causal Polygon failure matrix, including restart, phase-offset,
stale/conflict and correlated-failure falsification. N8 then performs controlled
unattended activation and migration.
