# OpenVPN d2ad7c Live Evacuation Audit

Дата: 2026-06-29
Режим: read-only live audit
Канал: `openvpn-1779388847-d2ad7c`
Raw evidence: `docs/reports/engineering/live_openvpn_audit_2026-06-29/`
Compact summary: `docs/reports/engineering/live_openvpn_audit_2026-06-29/openvpn_live_audit_summary.json`

## Summary

Live production state confirmed:

- `openvpn-1779388847-d2ad7c` has 14 users assigned.
- Channel service matrix is `FAIL`.
- Service matrix reports `ok_count=0`, `total=14`.
- All checked user-relevant services fail through this channel.
- Route installation itself is OK: affected users route through `v7edb0c189291` with `route_ok=true`.
- Runtime readiness for the interface/profile is `READY`, but service suitability is not ready.
- Service recommendation read-model already identifies `SWITCH_AVAILABLE` / `manual_switch_available` for affected users.
- Autoswitch guarded plan does not materialize a selected evacuation move; current captured terminal reasons are restore-barrier related.

Conclusion:

This is not explained by "automation disabled" alone. V7 sees that the users are on an unusable service channel and knows safe alternate channels exist, but the governed evacuation proposal is not materialized as a selected autoswitch move.

## Live State

Channel registry:

- id: `openvpn-1779388847-d2ad7c`
- protocol: `openvpn`
- interface: `v7edb0c189291`
- enabled: `1`
- role: `GLOBAL_FAST`
- soft_limit: `1`
- hard_limit: `2`
- service_tags: `google,telegram,instagram,global`
- manual_only: `0`
- reserve_only: `0`

Affected users:

| User | Table | Current Channel | Route Reality |
|---|---:|---|---|
| `10.0.0.2` | 100 | `openvpn-1779388847-d2ad7c` | OK |
| `10.0.0.3` | 101 | `openvpn-1779388847-d2ad7c` | OK |
| `10.0.0.6` | 104 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.2` | 1000 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.3` | 1001 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.4` | 1002 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.6` | 1004 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.8` | 1006 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.9` | 1007 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.10` | 1008 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.11` | 1009 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.12` | 1010 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.13` | 1011 | `openvpn-1779388847-d2ad7c` | OK |
| `10.7.0.15` | 1013 | `openvpn-1779388847-d2ad7c` | OK |

Service state:

- channel verdict: `FAIL`
- services OK: `0/14`
- Telegram: timeout
- Google: timeout
- Google Auth: timeout
- YouTube: timeout
- Apple: timeout
- Instagram: timeout
- WhatsApp: timeout
- Facebook: timeout
- Spotify: timeout
- SoundCloud: timeout
- ChatGPT: timeout
- OpenAI Auth: timeout
- Claude: timeout
- Anthropic: timeout

Capacity/load:

- channel registry hard limit is `2`
- live assigned users are `14`
- overview capacity status is `FAIL`
- global capacity still has free capacity, so the issue is not lack of all possible capacity

## Per-User Why Cards

All 14 affected users have the same service pattern:

- current channel: `openvpn-1779388847-d2ad7c`
- required services: `youtube`, `instagram`, `telegram`, `google`, `google_auth`
- current service verdict: `current_ok=false`
- current failed services: all required services fail
- recommendation status: `SWITCH_AVAILABLE`
- recommendation action: `manual_review`
- common best target: `amneziawg-exec-20260528-10-8-1-14`
- other safe target candidates include `wireguard-1779454504-c43409`, `vless`, `awg3`, `awg0`

Per-user summary:

| User | Current OK | Best Target | Service Recommendation |
|---|---|---|---|
| `10.0.0.2` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.0.0.3` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.0.0.6` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.2` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.3` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.4` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.6` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.8` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.9` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.10` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.11` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.12` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.13` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |
| `10.7.0.15` | false | `amneziawg-exec-20260528-10-8-1-14` | `SWITCH_AVAILABLE` |

## Exact Blocker Reasons

Observed blockers:

1. Service recommendation read-model:
   - does not block detection;
   - correctly reports `SWITCH_AVAILABLE` and per-service `manual_switch_available`.

2. Autoswitch plan:
   - `/api/autoswitch-plan` returns `plan=null` in the API wrapper, because the command output is not being materialized as parsed plan JSON in the captured response.
   - global plan tail shows `selected_move_count=0`.
   - global plan terminal reason: `dry_run_restore_barrier_clearance_selected_moves_exceed_budget`.
   - target-scoped plan terminal reason: `dry_run_restore_barrier_clearance_generation_expired`.

3. Target scoped API semantics:
   - `--target-egress` is documented as "Limit selected autoswitch moves to users recommended for this egress."
   - Therefore `/api/autoswitch-plan?egress=openvpn-1779388847-d2ad7c` is not an evacuation-from-current query; it is a movements-to-target query.
   - This is not the correct query shape for "evacuate users currently on this bad channel."

## Is This Expected Behavior?

Partially.

Expected:

- Runtime must not apply movement automatically.
- Expired restore-barrier clearance must stop execution.
- The API must not move users during read-only planning.

Not expected:

- A channel with 14 assigned users, `0/14` service health, and known safe alternates should still produce an operator-visible governed evacuation proposal.
- Restore-barrier execution clearance should block apply, not hide or erase evacuation explanation.
- The channel UI should not rely on a target-only autoswitch query when the operator needs a "drain/evacuate current channel" why-card.

## Is This A Bug?

Yes: this is an existing-owner workflow/materialization defect, not a new architecture problem.

The service/evidence layer detects the issue correctly. The autoswitch/operator surface does not present a governed evacuation proposal for the current-channel failure case.

## Exact Existing Owners

Planner / switch decision:

- `tools/v7-users-autoswitch:4042-4058`
  - builds user decisions;
  - applies target-egress filtering;
  - selects moves.

Current eligibility and failover decision:

- `tools/v7-users-autoswitch:5254-5369`
  - computes current candidate;
  - if current is not eligible, attempts failover candidate selection;
  - emits `current_egress_not_eligible` when failover is selected.

Service suitability gate:

- `tools/v7-users-autoswitch:5544-5561`
  - constructs candidate and runs gates.
- `tools/v7-users-autoswitch:5734-5795`
  - applies service suitability and route-class service failure.

Load and current-channel handling:

- `tools/v7-users-autoswitch:5598-5606`
  - load gate is skipped for `purpose="current"`.
  - This is load-specific and does not explain service failure retention.

Target-only filter:

- `tools/v7-users-autoswitch:4046-4052`
  - `target_egress` filters moves recommended to that target.
- `tools/v7-users-autoswitch:6543`
  - help text confirms target semantics.

Restore-barrier selected-move clearance:

- `tools/v7-users-autoswitch:4980-5127`
  - validates restore-barrier generation, selected move hash/count and envelope.

Admin API autoswitch plan wrapper:

- `admin/v7-admin-api:15982-16005`
  - runs `v7-users-autoswitch --pre-planner-refresh write --pretty`.
- `admin/v7-admin-api:15953-15979`
  - parses command stdout as JSON; current captured response returned `plan=null`.

Authority / execution:

- current captured plan is read-only/dry-run;
- no `--apply` command was used;
- no runtime automation was enabled;
- no user movement occurred.

## Minimal Patch Proposal

Do not apply during this audit.

Existing owners only:

1. Extend `tools/v7-users-autoswitch` to expose a source/current-channel evacuation planning mode or query path for users currently assigned to a failing channel.
2. Preserve existing safety: expired restore-barrier clearance must block apply, but must not suppress the operator-visible evacuation why-card.
3. Ensure service failure on current channel produces a governed evacuation proposal when safe targets exist.
4. Add diagnostics distinguishing:
   - `proposal_available`;
   - `execution_blocked_by_restore_barrier`;
   - `target_filter_no_moves`;
   - `source_channel_evacuate_required`.
5. Fix/extend `admin/v7-admin-api` so autoswitch plan JSON is parsed and exposed reliably instead of returning `plan=null`.
6. Add regression test:
   - current channel has service matrix `FAIL`;
   - users are assigned to current;
   - safe targets exist;
   - read-only plan exposes governed evacuation proposal;
   - restore barrier blocks execution only.

## If Expected

If the existing product decides that only manual service recommendation is expected at this maturity stage, the required governed operator transaction is:

- select one affected user;
- choose a safe target from the service recommendation read-model;
- run governed transaction through existing authority;
- verify;
- rollback if verification fails;
- close outcome.

However, that would still leave an operator workflow gap: the channel UI should explicitly tell the operator that evacuation is available but execution requires governed approval.

## Canonical Knowledge Changes

NONE.

This audit did not discover a new product principle. It maps to existing Movement Protection, Runtime Eligibility, Operator Explainability, and governed transaction owners.

## Verdict

`EXISTING_OWNER_WORKFLOW_DEFECT`

The users remain on `openvpn-1779388847-d2ad7c` because V7 currently detects service-level unsuitability and manual switch availability, but the autoswitch/operator planning surface does not materialize a governed evacuation proposal for "users currently on this failed channel." The target-scoped autoswitch query is not an evacuation-from-current query, and restore-barrier execution clearance appears as the terminal blocker in the captured dry-run.

Need New Owner: FALSE
Need New Backlog Item: FALSE
Need New Architecture: FALSE
Runtime Changed: NO
Users Moved: NO
