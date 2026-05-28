# E25 Pre-Execution Live Snapshot

Collected: 2026-05-28T10:16:05Z and follow-up samples through 2026-05-28T10:18:43Z on `v3119922.hosted-by-vdsina.ru`.

## Scope

E25 approved movement:

- candidate: `10.7.0.11`
- expected current egress: `1`
- forward target: `wireguard-1779454504-c43409`
- rollback target: `1`
- movement budget: `1`

No movement was executed during this snapshot.

## Runtime Identity

- `hostname=v3119922.hosted-by-vdsina.ru`
- initial `date -u=Thu May 28 10:16:05 UTC 2026`
- follow-up readiness sample 2: `Thu May 28 10:17:08 UTC 2026`
- follow-up readiness sample 3: `Thu May 28 10:18:43 UTC 2026`

## Tool Availability

Observed on VPS:

- `v7-user-switch=/usr/local/bin/v7-user-switch`
- `v7-operator-execution-packet`: not present in PATH

Local packet consumer capability review:

- `tools/v7-operator-execution-packet` delegates to `admin_core/operator_execution.py`.
- Current implementation validates only E22/E23 zero-movement packets.
- It explicitly rejects movement packets, nonzero movement budget, non-empty allowed users, and non-empty allowed targets.

## Registry Hashes

Initial precheck:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Final immutable precheck:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Registry drift: NO.

## Candidate State

Candidate row:

- `ip=10.7.0.11 current=1 table=1009 enabled=1`

Candidate route table:

- `default dev v7e356a192b79 scope link`

Candidate route_get:

- `8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009`

Candidate drift:

- candidate moved since E24.2: NO

## Users Per Egress

Initial precheck:

- `1=4`
- `awg0=3`
- `awg3=9`
- `wireguard-1779454504-c43409=0`

WireGuard users:

- none observed.

## Target Readiness

Command:

- `v7-second-canary-target-readiness --json`

Initial precheck result at 2026-05-28T10:16:05Z:

- `approval_status=NO-GO`
- `second_canary_readiness=NO-GO`
- `selected_target=NONE`
- WireGuard rejection reason: `stability below floor (0.422735)`

Follow-up sample 2 at 2026-05-28T10:17:08Z:

- `approval_status=NO-GO`
- WireGuard rejection reason: `stability below floor (0.431723)`

Follow-up sample 3 at 2026-05-28T10:18:43Z:

- `approval_status=NO-GO`
- WireGuard rejection reason: `stability below floor (0.438413)`

Quality floor:

- required stability: `0.45`

WireGuard remained:

- zero-user: YES
- load status OK: YES
- diagnose OK: YES
- interface inferred UP from diagnose: YES

But the readiness helper gate was hard NO-GO because `stability.state` remained below floor.

Abort gate:

- target readiness not GO: TRUE

## Target Readiness Source Divergence

Direct source data at 2026-05-28T10:17:08Z:

`stability.state`:

- `wireguard-1779454504-c43409_avg_mbps=39.4003`
- `wireguard-1779454504-c43409_min_mbps=17.01`
- `wireguard-1779454504-c43409_stability=0.431723`
- `wireguard-1779454504-c43409_samples=30`

`egress-quality-summary.json` for WireGuard:

- `5m.stability=0.5197`
- `1h.stability=0.5718`
- `24h.stability=0.7159`
- `7d.stability=0.8215`

Classification:

- `READINESS_SOURCE_DIVERGENCE`

Operational decision:

- E25 must honor the deployed readiness helper because E24.1/E24.2 made it the movement-critical gate.
- No movement is allowed while `v7-second-canary-target-readiness` returns `NO-GO`, even if another quality summary is more favorable.

## Restore-Settle Gate

Command:

- `tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e24_2-evidence/restore-settle-samples --json`

Result:

- `gate_status=GO`
- `sample_count=3`
- `apply_timer_intervals_covered=5.75`
- `selected_moves_by_sample=[0,0,0]`
- `registry_stable=true`
- `egress_registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`

Restore-settle stale/invalid: NO for the E24.2 sample dir.

## Selected Moves

Observed:

- no `/opt/v7/egress/state/*selected*` files.

Selected moves:

- `0`

## Restore Barrier

`autoswitch-restore-barrier.json`:

- `enabled=true`
- `block=E11.17`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`
- `clearance_max_selected_moves=0`
- `expires_at=2000-01-01T00:00:00+00:00`

## Timers

- `planner timer=inactive`
- `apply timer=inactive`

No hold action was performed because timers were already inactive and execution aborted before movement.

## Hidden Mover Scan

No active processes observed for:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`

## Runtime Checkers

Precheck:

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`

## Audit Store Tail

Audit store paths inspected:

- `/opt/v7/audit/operator-execution-audit.jsonl`
- `/opt/v7/audit/operator-runtime-governance-actions.jsonl`

Latest observed records were E23 zero-move governance records/denials. No E25 audit record was written because execution aborted before movement.

## Pre-Execution Verdict

`pre_execution_abort=true`

Blocking reasons:

1. `target_readiness_not_go`
2. `approval_packet_expired`
3. `operator_packet_consumer_not_movement_capable`

No user movement was performed.
