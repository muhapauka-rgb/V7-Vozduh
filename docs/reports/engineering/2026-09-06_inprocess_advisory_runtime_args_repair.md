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

The repair is local and not yet deployed in this report revision. The next
lawful step is the existing safe-deploy owner, followed by fresh Runtime
health evidence. A live V7 health caller must originate any recovery; no
manual replay or target injection is valid evidence.
