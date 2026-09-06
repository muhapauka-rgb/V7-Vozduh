# V7 Engineering Report — in-process advisory runtime-args repair

Date: 2026-09-06  
Scope: existing Matrix → `v7-users-autoswitch` advisory handoff only

## Evidence

The fresh Runtime receipt at `2026-09-06T20:36:06.002019+00:00` recorded a
current ordinary failure on `wireguard-1779454504-c43409` (46 affected users,
incident `sfinc_f5a39c91cf97063a9e5fe77425dddd84`). The first source-bound
advisory did not complete in-process: `runtime_profile_advisory_diagnostic`
showed `advisory_status=FAILED`, `obligation_present=false`, and
`exact_obligation_match=false`. The same receipt then paid for passive work
(`5792.323 ms`) and a second advisory (`8846.256 ms`) before the governed
executor stopped safe with `ordinary_service_failure_selection_binding_invalid`.

Earlier fresh receipts exposed the underlying error in the subprocess fallback:
`AttributeError: 'Namespace' object has no attribute 'route_class'`. This proves
the normal in-process owner contract was incomplete; the fallback was not a
target-selection or route-governance decision.

## Repair

Extended only `in_process_autoswitch_args()` in
`tools/v7-service-matrix-refresh-all` with parser-equivalent defaults already
owned by the existing autoswitch CLI: `route_class`, `load_summary_file`,
`execution_control_file`, `allow_hard_full`, `rollback_on_verify_fail`, and the
approved bundle-hash fields. No owner, queue, timer, state source, Planner
semantics, Authority, route writer, or executor behavior was added or changed.

## Verification

- Focused handoff/profile tests: **4 PASS**.
- Full affected unit set: **297 run; 8 pre-existing CPS/fixture failures and
  2 pre-existing environment/setup errors**; none concerns this argument
  contract. The new regression test passes.
- No Candidate, Packet, Lease, Barrier, route mutation, or user movement was
  performed by Codex.

## Runtime status

The repair was published and deployed by the existing safe-deploy owner at
commit `254643beec60ed8e3408b9393ea364ccb16233b1` (deploy
`deploy-z8-14-Updatesystem-254643b-20260906T235853`). Production hashes for
the changed Matrix handoff and autoswitch files match the deployed commit;
`v7-health.service` is active.

## Post-deploy live confirmation

At `2026-09-07T00:02:33+03:00`, the live V7 health caller emitted
`V7_HEALTH_RECOVERY_CONSUMER_RECEIPT` with `action_completed=true`,
`advisory_diagnostic.status=PASS`, empty `in_process_error`, and no fallback
invocation. It automatically moved 4 ordinary users from the affected awg3
scope; required-service S11 was reached at 32,212.972 ms from consumer entry
and the governed consumer completed in 33,511 ms. No manual operational
transition was used.

Fresh current state after that operation contains 51 ordinary users on
`wireguard-1779454504-c43409` (Matrix `OK`) and 24 on `awg3` (Matrix `OK`),
with zero enabled ordinary users on `vless`, `1`, or
`openvpn-1779388847-d2ad7c`. VLESS remains unsafe for ordinary placement:
13 service rows are `FAIL`; awg0 has 4 failed service rows but its assigned
records are certification-only. There is no active recovery operation left
in the current lease/barrier state.
