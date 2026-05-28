# E25.1 Fresh Movement Approval Packet

Packet:

- `docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.json`

## Scope

- candidate user: `10.7.0.11`
- from egress: `1`
- to egress: `wireguard-1779454504-c43409`
- rollback target: `1`
- movement budget: `1`
- UI execution: disabled
- autoswitch apply: forbidden
- canary/cohort: forbidden

## Freshness

- created: `2026-05-28T10:33:31.168538+00:00`
- expires: `2026-05-28T12:33:31.168538+00:00`
- non-expired at creation: YES

Runtime hashes:

- users registry: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- egress registry: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Hashes:

- movement intent hash: `8e643a26d0645043a20c28a8037cef50416a48c3ae0587e8d0d2453fb822e785`
- live selected-moves empty hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `c5f58e490844e1ddb8cb29ba143a26a1479a45fc94cf08140ffb0931f199b2d5`

## Required E25.2 Rechecks

E25.2 must still recheck immediately before movement:

- packet not expired
- candidate still on `1`
- target readiness still `GO`
- restore-settle still `GO`
- selected_moves still `0`
- hidden movers absent
- runtime checkers OK
- WireGuard users count still `0`
- planner/apply timers held/inactive

## Execution Method

`APPROVED_RAW_FALLBACK_PREPARED`

Reason:

- current packet consumer is zero-move only.
- no movement-capable consumer was connected in E25.1.
- raw fallback is prepared for E25.2 only, under fresh GO gates.
