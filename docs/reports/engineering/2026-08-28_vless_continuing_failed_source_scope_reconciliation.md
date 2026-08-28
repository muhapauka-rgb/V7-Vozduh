# V7 — reconciliation of the continuing failed-source scope

**Mission:** `V7_CONTINUING_FAILED_SOURCE_AFFECTED_SCOPE_RECONCILIATION`  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Date:** 2026-08-28  
**Result:** current live evidence does not reproduce a continuing failed VLESS
scope. The system correctly kept the two currently enabled VLESS users in
place because the source is presently degraded but usable and no governed
failover target is eligible.

## 1. Fresh current truth

The checks below were read through the existing Matrix and autoswitch owners;
no registry, route, reservation or user record was edited.

- `egress.registry`: `vless`, interface `tun0`, enabled.
- Fresh Matrix run completed at `2026-08-28T20:38:51Z`: `WARN`, `11/14`
  service checks passed.
- Required profile services passed: Telegram, Google, Apple, YouTube,
  WhatsApp, Instagram and Google Auth. ChatGPT and Anthropic were reachable
  with endpoint-limited responses (`403`/`404`). Facebook, OpenAI Auth and
  Claude timed out.
- Therefore `VLESS_CURRENT_STATE = DEGRADED_BUT_USABLE`, not an actionable
  whole-channel failure.
- Current enabled ordinary VLESS users are `10.7.0.126` (table `1124`) and
  `10.7.0.127` (table `1125`). `10.7.0.7` is disabled and is not affected
  scope. No current VLESS row is a certification identity.
- Current service-failure events are per-service episodes. No fresh
  owner-backed whole-channel incident covers users `126`/`127`.
- The older `v7-state.json` `FAIL`/`health_code_000` projection conflicts with
  the fresh Matrix result. It is stale evidence and is not allowed to trigger
  a move by itself.
- `autonomous-execution-control` is `OPEN`; the old restore barrier is
  expired; no active Candidate, Packet, Lease or conflicting operation was
  found.
- `v7-health.service` is active and runs the existing role-based health loop.
  The separate autoswitch unit remains bounded (`max-users=0`, L3 execution
  disabled), as required by the current production policy.

## 2. Why Liza moved and the current users did not

Liza (`10.7.0.125`) previously belonged to a distinct confirmed hard-failure
incident (`sfinc_cf3f65f71454a5ad2dbfa5f8e77b4b34`). The existing consumer
selected `awg0`, applied the change and verified the route and required
services. Its second invocation returned
`STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE`, proving exact-once behavior.

Users `10.7.0.126` and `10.7.0.127` were not in that incident. The current
Matrix observation says their source still passes all required services, so
there is no lawful failure event to consume. The observed `keep` decision is
therefore the safe result, not a lost affected-scope transition.

Even if VLESS became actionable at this moment, the existing planner reports
no eligible target for these users: every available alternative is blocked by
its current health, capacity, reservation or policy gates. The consumer must
remain fail-closed rather than inventing a target.

## 3. Causal hypothesis table (A–H)

| Hypothesis | Current evidence | Classification |
|---|---|---|
| A. Consumed incident never re-arms | Liza's old incident was consumed once; no current incident exists for `126`/`127`. | Not proven; exact-once is correct. |
| B. Stale affected-scope fingerprint | Current scope is read from `users.registry`; no active incident exists against which to bind it. | Not reproduced. |
| C. New users on an already-failed source are invisible | Current observe path enumerates both enabled VLESS rows; fresh Matrix does not mark the source actionably failed. | Not reproduced; existing Model-B coverage remains valid. |
| D. Role/policy blocks evacuation | Planner has no eligible target; VLESS itself carries stale hard-ineligible quality overlays. | Partly observed as a target/policy boundary, not a scope bug. |
| E. Wrong incident or Authority classification | Fresh Matrix is `WARN` with all required services healthy; no whole-channel failure is present. | Supported as the current explanation. |
| F. Expired lock/packet/barrier residue | Execution control is open and no current operation is active. | Not reproduced. |
| G. Stale snapshot prevents replan | Observe reports `stop_required=false`; no candidate exists because the failure/target preconditions are absent. | Not reproduced. |
| H. Health loop sees only edge failures | Role-based health loop refreshed Matrix successfully. The disabled oneshot autoswitch is a bounded production policy, not evidence of a continuing-scope defect. | Not proven as root cause. |

## 4. Runtime and regression evidence

- Existing `v7-users-autoswitch --mode observe --source-egress vless` returned
  `keep` for both enabled users, `candidate_moves=0`, `selected_moves=0`,
  `users_moved_by_read_model=0`, and `authority_expanded=false`.
- No Candidate, Packet, Lease, Barrier or Apply was created; no route changed;
  no ordinary user moved.
- Focused policy regression: **219 tests passed**.
- A broader evolution/health selection was started but stopped after it
  entered a long AST-consistency test; it made no repository or Runtime
  changes. The focused owner suite is the relevant executable regression for
  this no-mutation reconciliation.

## 5. Changes and deployment

No implementation defect was proven, so no code or configuration change was
made. There was no commit, deploy, route mutation, registry edit, or client
movement. This preserves fail-closed behavior and avoids turning stale
`v7-state` evidence into an unsafe automatic switch.

## 6. Conclusion and re-entry

The alleged continuing-failure inconsistency is not present in the current
world. Liza's earlier automatic recovery and the current users' `keep`
decisions are consistent with two different incident states. The current
blocking fact is not affected-scope discovery; it is the absence of both an
actionable VLESS failure and an eligible failover target.

The next executable frontier in the Program is:

```text
fresh Matrix actionable VLESS failure
→ current enabled users bound from users.registry
→ eligible target admitted by existing Planner/Authority
→ existing Candidate/Packet/Lease/Barrier/Apply consumer
→ exact route + required-service verification
```

Do not fabricate a cohort, manually move a client, or promote the stale
`v7-state` projection. If the product requirement is instead “move a client
when any individual service fails,” that is a separate product-contract
decision; it is not justified by this reconciliation.

## 7. Follow-up live observation (2026-08-28 20:53–20:55 UTC)

The owner-backed probe was rerun after the previous report because the
operator expected VLESS to be unavailable. The new result is materially
different from the earlier `11/14` observation:

- first follow-up: `1/14`, `WARN`; only Telegram passed;
- second follow-up: `1/14`, `WARN`; Telegram passed, while Google,
  Google Auth, Instagram, YouTube, WhatsApp, Facebook, OpenAI Auth, Spotify,
  SoundCloud, Claude, Anthropic and ChatGPT failed;
- the failures are mostly TLS EOF or five-second connection timeouts to the
  VLESS path. `sing-box` logs show intermittent successful and timed-out
  connections to `77.110.103.131:443`, confirming instability rather than a
  clean process shutdown.

The label `WARN` is a presentation/aggregation weakness: the Matrix status
code is computed as `WARN` whenever at least one service is reachable, even
when `13/14` checks fail. The detailed service rows contain the failures,
but the headline can look healthy in the admin view. The local interface and
process are also still `UP`, which is not equivalent to end-to-end service
availability.

After the two observations, the existing autoswitch consumer still produced
`selected_moves=0` and `NO_INCIDENT_DISABLED`. Its current production policy
is explicitly bounded (`emergency_failover_enabled=false`, L3 execution
disabled, `max-users=0`), and the intelligence snapshot refresh timed out,
so it failed closed. No client or route changed.

This follow-up identifies two separate issues, neither repaired in this
diagnostic turn:

1. VLESS is currently operationally unstable, but the Matrix headline should
   expose `13/14` failure more clearly instead of saying only `WARN`.
2. Automatic ordinary-user movement is currently disabled by the existing
   L3 production policy and also has no admitted target in the present
   planner inventory. Enabling or changing that policy is a separate
   product/Authority decision, not a safe inference from this observation.
