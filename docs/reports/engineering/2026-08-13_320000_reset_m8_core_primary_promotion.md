# RESET-M8 Core-primary Production Promotion Engineering Report

Status: `RESET_M8_CORE_PRIMARY_PRODUCTION_PROMOTION_WITH_SAFE_FALLBACK_PASS`

## Result

The existing `v7-routing-sync` writer now consumes the exact owner-issued `routing_core_primary_promotion` contract and installs one generation-bound class dataplane for all `124` compatible enabled production users across `6` current egress classes. The legacy per-user routes remain installed solely as the required fallback.

## Evidence

- Authority: request `rcppreq_68c41377b6a7c1f2a97d5a4a`; contract `rcpp_6bfcaa2063bd7567c9554b6d`; scope `ALL_COMPATIBLE_PRODUCTION_USERS`; `legacy_fallback_required=true`.
- Source/deploy: commits `18b3683f` and `46ab4891`; safe deploy `deploy-z8-14-Updatesystem-46ab489-20260813T134054`; GitHub/runtime convergence PASS.
- Apply/verify: `CORE_PRIMARY_APPLY_PASS`, `CORE_PRIMARY_VERIFY_PASS`; membership generation `ef76812d6d3d2d9e0e72702123cd80f3ad55e94af0a80e09c863d3fcb8466147`; class generation `177eef6d073399f77a98de89fd2c0765fdd878b9f2bbe15d91b70f7043bb34dd`.
- Real production consumer path: nft prerouting hook on `wg0` maps source address to class mark; six fwmark rules select six class route tables. Representative `10.7.0.114` maps to `0x202`; marked route lookup consumes table `202` and resolves `awg3`.
- Recovery: exact fallback removed the Core table/rules, regenerated all `124` legacy per-user routes, and the representative unmarked route still resolved table `1112 -> awg3`.
- Restart/crash recovery: ordinary `v7-routing-sync.service` restart re-read the active Authority contract and rebuilt Core-primary. Two further restarts remained idempotent: one nft table, two hook rules, six mark rules, no duplicate effect.
- Observability: the two production nft hook rules carry packet/byte counters. No natural client packet was observed during the bounded evidence window; no synthetic client event was manufactured. This does not invalidate installed production authority, marked route consumption, recovery, or fallback proof.
- Capacity/blast radius: the promoted membership is exactly the enabled compatible registry set; unresolved users/egresses fail closed during class derivation; the legacy fallback remains available.

## Closure

- Intent closed: Core-primary production routing authority is installed for the authorized compatible population with exact fallback and restart recovery.
- Owners affected: existing policy/Authority owner, `v7-routing-sync` writer, nft/ip-rule kernel owners, users/egress registries, CPS and OMP projections. No new owner was created.
- Residual: legacy primary orchestration and removable duplicate timer/package surfaces are owned by RESET-M9; fallback semantics remain protected.
- Exact successor: `EXECUTE_RESET_M9_LEGACY_RETIREMENT_SYSTEM_SHRINK_AND_PROGRAM_CLEANUP`.
- Runtime effects: `CORE_PRIMARY_CLASS_DATAPLANE_ACTIVE`.
- Production effects: `124_COMPATIBLE_USERS_CORE_PRIMARY_WITH_LEGACY_FALLBACK`.
- Authority effects: `EXACT_USER_AUTHORIZED_M8_SCOPE_CONSUMED; NO_SCOPE_EXPANSION`.

Terminal: `RESET_M8_CORE_PRIMARY_PRODUCTION_PROMOTION_WITH_SAFE_FALLBACK_PASS`.
