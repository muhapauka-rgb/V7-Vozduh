# WG.PROMOTE.APPLY — WireGuard Production Pool Enablement Report

## 1. Executive Summary

Final verdict: **WIREGUARD_PROMOTED_SUCCESSFULLY**.

Channel `wireguard-1779454504-c43409` was removed from obsolete canary reservation and became a normal production-pool candidate. No users were moved. No autoswitch apply was run. No routing mutation was performed.

The registry mutation was limited to removing:

- `canary_reserved=true`
- `reservation_reason=second_canary_target`
- `reservation_owner=control_plane_governance`

No artificial capacity caps were introduced.

## 2. Pre-Mutation Audit

Production host: `v3119922.hosted-by-vdsina.ru`.

Pre-mutation WireGuard state:

- channel: `wireguard-1779454504-c43409`
- protocol: `wireguard`
- enabled: `1`
- role: `GLOBAL_FAST`
- soft_limit: `1`
- hard_limit: `2`
- manual_only: `0`
- reserve_only: `0`
- canary_reserved: `true`
- reservation_reason: `second_canary_target`
- reservation_owner: `control_plane_governance`

Pre-mutation registry hash:

`f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`

Evidence:

- `WG_PROMOTE_APPLY_EVIDENCE/pre/production_pre_audit.txt`
- `WG_PROMOTE_APPLY_EVIDENCE/pre/production_pre_planner.json`

## 3. Backup

A production backup was created before the successful mutation:

`/opt/v7/egress/state/egress.registry.wg_promote_apply_backup.20260613T153350Z`

Rollback command:

```bash
cp -p /opt/v7/egress/state/egress.registry.wg_promote_apply_backup.20260613T153350Z /opt/v7/egress/state/egress.registry
```

Important safety note: an earlier mutation attempt was detected as unsafe because it joined the WireGuard line with the next registry row. That attempt was immediately rolled back from its backup, and the registry hash returned to the original pre-mutation value before the safe field-based mutation was executed.

Evidence:

- `WG_PROMOTE_APPLY_EVIDENCE/mutation/production_mutation_rollback_from_failed_attempt.txt`
- `WG_PROMOTE_APPLY_EVIDENCE/mutation/wg_promote_apply_remote.sh`
- `WG_PROMOTE_APPLY_EVIDENCE/mutation/production_mutation_success.txt`

## 4. Canary Dereservation

The successful mutation used a bounded field-based registry rewrite against the target row only.

Post-mutation WireGuard row:

```text
id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Validation:

- line count unchanged: `PASS`
- reservation fields removed: `PASS`
- neighbor row preserved: `PASS`
- audit log attempted: `true`

Post-mutation registry hash:

`05d8118c43888d046e8fe3aa3cca906db1603b15e478fd0e7eaf282797d13a78`

## 5. Post-Mutation Truth Gate

Runtime/local truth results:

- runtime truth: `PASS`
- local truth: `PASS`
- GitHub direct check: `0f0ffbac09cfe5107a73668d78931131826c5c24`
- local HEAD: `0f0ffbac09cfe5107a73668d78931131826c5c24`
- production status in convergence output: `PASS`
- deploy delta mismatches: `[]`

The local `truth-check --all` command returned `NO-GO` only because its internal GitHub remote read failed inside the restricted execution environment:

- `github_remote_unreadable`
- `canonical_branch_missing_on_remote`

This was counterchecked with direct `git ls-remote`, which confirmed GitHub and local branch match.

Evidence:

- `WG_PROMOTE_APPLY_EVIDENCE/post/truth_check_after.json`
- `WG_PROMOTE_APPLY_EVIDENCE/post/convergence_status_after.json`
- `WG_PROMOTE_APPLY_EVIDENCE/post/github_ls_remote_updatesystem.txt`

## 6. Planner Reality Validation

Fresh production planner dry-run after dereservation:

- `users_total`: `26`
- `egress_total`: `7`
- `healthy_egress_total`: `2`
- `candidate_moves_total`: `26`
- `rebalance_candidates`: `23`
- `selected_moves`: `0`
- terminal reason: `dry_run_intelligence_snapshot_stop_required`

WireGuard planner state:

- eligible: `true`
- blocked: `[]`
- canary_reserved: `false`
- score: `2230.92`
- stability: `0.901`
- 1h stability: `0.9383`
- min stability floor: `0.45`

Comparison:

- WireGuard score: `2230.92`
- vless score: `1871.93`

WireGuard became the ranked winner in the post-mutation planner view.

Evidence:

- `WG_PROMOTE_APPLY_EVIDENCE/planner/production_post_planner.json`
- `WG_PROMOTE_APPLY_EVIDENCE/analysis/planner_reality_summary.json`

## 7. Pool Impact Review

The production pool expanded from one healthy planner channel to two healthy planner channels:

- before: effectively `vless`
- after: `wireguard-1779454504-c43409` + `vless`

WireGuard does not merely become eligible; it dominates the current pool ranking because it has:

- stronger service score
- strong stability
- strong latency/load/capacity score parts
- no canary/reserve penalty

Other channels remain blocked:

- `awg0`: `stability_below_floor`
- `awg3`: `stability_below_floor`
- `amneziawg-exec-20260528-10-8-1-14`: `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `stability_below_floor`
- `openvpn-1779388847-d2ad7c`: health/speed/Telegram failures

## 8. Autonomy Impact

BA.3 and future autonomy now have a second healthy channel in planner reality. That improves pool diversity and recovery options.

However, BA.3 is not automatically execution-ready from this program because the fresh dry-run still stopped on snapshot source mismatches:

- `channel-service-scores`
- `service-scores`

This program intentionally stopped before apply. The next execution program must run the canonical snapshot refresh / pre-planner refresh path and regenerate fresh packet and restore barrier before any movement.

## 9. Stop Before Apply

Confirmed:

- users moved: `0`
- autoswitch apply run: `false`
- routing changed: `false`
- autonomy expanded: `false`
- selected moves executed: `0`

The `users.registry` hash stayed unchanged:

`ad8f3a24d9bf3b709b8ca3a66de9c0c7100da37d2eb23b1a9277d59b71598e0e`

## 10. Final Verdict

Final verdict: **WIREGUARD_PROMOTED_SUCCESSFULLY**

Final flags:

- wireguard_promoted: `true`
- canary_reserved_removed: `true`
- reservation_reason_removed: `true`
- reservation_owner_removed: `true`
- artificial_cap_added: `false`
- healthy_egress_total_after: `2`
- candidate_moves_total_after: `26`
- wireguard_eligible_after: `true`
- wireguard_pool_rank: `1`
- users_moved: `0`
- apply_executed: `false`
- routing_mutation_executed: `false`
- ba3_improved: `true`
- ba3_execution_ready_now: `false`

Safe next step:

`BA3_REFRESH_PACKET_RESTORE_BARRIER_AND_EXECUTION_RECHECK`

