# E11.9 Pre-Drain Investigation

Collected from live runtime on `v7-vps` at `2026-05-26T22:16:28Z`.

## Current WireGuard Truth

- `wireguard-1779454504-c43409` is `canary_reserved=true`.
- Runtime autoswitch hash is `5e3b1b479b8363cc9dfeb63bc8d0c87cc14de1ef9326912cea79086737734ec1`, the E11.8 reservation-enforcing build.
- WireGuard diagnose is `OK`.
- WireGuard interface is `v7e06a394c478`.
- WireGuard users before drain: `10`.

Current WireGuard users:

| user | table | route before |
|---|---:|---|
| `10.7.0.4` | `1002` | `v7e06a394c478` |
| `10.7.0.6` | `1004` | `v7e06a394c478` |
| `10.7.0.8` | `1006` | `v7e06a394c478` |
| `10.7.0.9` | `1007` | `v7e06a394c478` |
| `10.7.0.10` | `1008` | `v7e06a394c478` |
| `10.7.0.11` | `1009` | `v7e06a394c478` |
| `10.7.0.12` | `1010` | `v7e06a394c478` |
| `10.7.0.13` | `1011` | `v7e06a394c478` |
| `10.7.0.14` | `1012` | `v7e06a394c478` |
| `10.7.0.15` | `1013` | `v7e06a394c478` |

## Authority And Gates

- `v7-health.service`: active.
- `v7-autoswitch-planner.timer`: active.
- `v7-users-autoswitch.timer`: active before drain.
- `v7-users-autoswitch.service`: inactive before drain.
- Hidden `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply`: not observed.
- Autoswitch dry-run selected moves: `0`.
- Runtime checkers: reconcile OK, user-route OK, kill-switch OK, provisioning OK.

## Reservation Enforcement Evidence

Autoswitch dry-run showed:

- non-current WireGuard candidates blocked by `canary_reserved_production_assignment_blocked`;
- current WireGuard users held by `canary_reserved_current_hold_requires_separate_drain_approval`;
- `candidate_moves_total=0`;
- `selected_moves=0`.

This proves E11.8 enforcement prevents new production assignment but intentionally does not drain existing users.

## Drain Target Analysis

Target `1` was selected as the safe drain destination because:

- current users on target `1` before drain: `0`;
- runtime diagnose: `OK`;
- target interface: `v7e356a192b79`;
- autoswitch candidates for WireGuard users ranked `1` as the strongest non-reserved production alternative;
- dynamic capacity after moving 10 users would reach the soft limit, not the hard or failover hard limit;
- rollback is explicit per user through `v7-user-switch <user> wireguard-1779454504-c43409` if emergency containment requires it.

## Abort Conditions Checked

- `selected_moves > 0`: false.
- hidden movers: false.
- no healthy drain target: false.
- routing/checker failures: false.
- reservation enforcement uncertain: false.

Full raw evidence: `docs/track7/control-plane/e11_9-evidence/pre-drain-investigation.raw.txt`.
