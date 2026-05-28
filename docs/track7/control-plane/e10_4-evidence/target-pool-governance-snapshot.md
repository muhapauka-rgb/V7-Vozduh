# E10.4 Target Pool Governance Snapshot

Mode: read-only strategy input.

## Evidence Base

E10.4 uses the current E10.3 truth artifacts:

- `docs/track7/control-plane/e10_3-evidence/target-pool-matrix.md`
- `docs/track7/control-plane/e10_3-evidence/current-target-readiness.json`
- `docs/track7/control-plane/e10_3-evidence/current-restore-settle.json`
- `docs/track7/control-plane/e10_3-evidence/awg-occupation-history.md`
- `docs/track7/control-plane/e10_3-evidence/openvpn-wireguard-suspect-review.md`
- `docs/track7/control-plane/SECOND_CANARY_TARGET_READINESS_RULES.md`
- `docs/track7/control-plane/AUTOSWITCH_TRANSIENT_SERVICE_SIGNAL_POLICY.md`

No live mutation or live runtime command was required for this strategy block.

## Current Restore Governance

Fresh E10.3 settle evidence:

```text
restore_settle_gate_status=GO
selected_moves_by_sample=[0,0,0]
telegram_hard_blocked_by_sample=[false,false,false]
egress_1_eligible_by_sample=[true,true,true]
users.registry_stable=true
egress.registry_stable=true
runtime_checks_ok=true
hidden_movers_observed=false
```

Restore governance is not the active blocker. Target-pool availability is the active blocker.

## Current Target Pool

| Egress | Users | Diagnose | Quality | Exclusions | Governance status |
|---|---:|---|---|---|---|
| `1` | 6 | OK | OK | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | occupied production egress, not clean target |
| `awg0` | 0 | OK | below floor | none | zero-user but NO-GO |
| `awg3` | 0 | OK | below floor | none | zero-user but NO-GO |
| `openvpn-1779388847-d2ad7c` | 0 | SUSPECT | below floor in E10.3 readiness | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | zero-user but NO-GO |
| `wireguard-1779454504-c43409` | 0 | SUSPECT | OK | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | zero-user conditional waiver candidate only |
| `vless` | 10 registry / 11 load-state | OK | baseline proxy path | none | rollback/default pool, not canary target |

## Current Metadata Signals

From E10.3 egress registry snapshot:

- `awg0`: no `manual_only`, no `reserve_only`, no `exclude_route_classes`, no canary/test label.
- `awg3`: no `manual_only`, no `reserve_only`, no `exclude_route_classes`, no canary/test label.
- `1`: `manual_only=0`, `reserve_only=0`, exclusions present.
- OpenVPN: `manual_only=0`, `reserve_only=0`, exclusions present.
- WireGuard: `manual_only=0`, `reserve_only=0`, exclusions present.

There is no existing explicit canary reservation model in the observed egress metadata.

## Autoswitch Interaction

E10.3 AWG history shows `awg0` and `awg3` are production autoswitch candidates. They can become occupied without manual action. A target can be zero-user at one snapshot and still be unsuitable for canary if autoswitch can assign production users to it before the approval packet is executed.

## Governance Gap

The current platform can prove canary mechanics and restore discipline, but it lacks a reserved clean target pool. Target readiness is therefore unstable because targets are either:

- occupied by production users;
- zero-user but below quality floor;
- zero-user but `SUSPECT`;
- zero-user but not protected from autoswitch occupation.

The missing governance concept is an explicit `canary_reserved` / test-egress lifecycle.

