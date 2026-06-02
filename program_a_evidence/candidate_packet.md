# Program A Candidate Packet

Fresh state source: production runtime snapshot collected at `2026-06-02T16:08:50+03:00`.

Planner command class: local dry-run of `tools/v7-users-autoswitch` against freshly copied production state/config, with no production mutation.

Evidence:

- `program_a_evidence/phase1_fresh_runtime_reality.txt`
- `program_a_evidence/phase2_local_fresh_planner_plan.json`
- `program_a_evidence/phase3_restore_settle_local.txt`

## Runtime truth

- Host: `v3119922.hosted-by-vdsina.ru`
- Runtime branch: `Updatesystem`
- Runtime commit: `ddc7d1cf048277e8ffa7e7ef3d6a0c85f256e7ca`
- Deploy id: `deploy-z8-14-Updatesystem-ddc7d1c-20260602T154925`
- Admin API service: active
- Autoswitch service: inactive
- Autoswitch timer: inactive

## Planner output

- Operation owner: `tools/v7-users-autoswitch`
- Operation type: `runtime_autoswitch`
- Operation id: `runtime_autoswitch_487467573808ac6a11496c0c`
- Planner generation id: `6b1bf2bd3db4835bfc3c4e8d99ea2fe4506f96a7d6c4bfeb3667015cf7223d52`
- Runtime snapshot hash: `6573094d6a15875518bdfd94649b5f780bd19570aa84ede6f40afaa7087655db`
- Selected move count: `0`
- Selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- Terminal state: `DRY_RUN`
- Terminal reason: `dry_run_restore_barrier_clearance_generation_expired`

## Restore barrier state

- Enabled: `true`
- Clearance expected selected moves: `1`
- Approved selected moves hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- Approved generation id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- Current generation id: `6b1bf2bd3db4835bfc3c4e8d99ea2fe4506f96a7d6c4bfeb3667015cf7223d52`
- Clearance expires at: `2026-06-01T18:02:59.305408+00:00`
- Clearance generation ok: `false`
- Clearance guard reason: `restore_barrier_clearance_generation_expired`

## Candidate result

No executable candidate exists.

Reasons:

- Planner selected `0` moves.
- Healthy egress count is `0`.
- All users were kept on current egress because there was no eligible failover target.
- Target `1` is blocked by Telegram hard-block evidence: `telegram_required_telegram_down_14s`.
- `amneziawg-exec-20260528-10-8-1-14` is blocked by `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, and quality floors.
- `awg0` is blocked by `health_code_000` and quality floors.
- `awg3` is blocked by quality and stability floors.
- `openvpn-1779388847-d2ad7c` and `vless` are blocked by `severity_SUSPECT`.
- `wireguard-1779454504-c43409` is blocked by `canary_reserved_production_assignment_blocked`.

## Candidate verdict

candidate_available=false
selected_user=NONE
selected_forward_target=NONE
rollback_target=NONE
operation_created=false
execution_allowed=false
