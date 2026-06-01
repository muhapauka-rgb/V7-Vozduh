# Block D2 Autoswitch Remediation And Shadow Retry Report

Date: 2026-06-01
Project: V7 Vozduh
Branch: `v7-next`
Mode: Remediation / Shadow Operation / Certification

## Final Verdict

Block D2 is certified as a repository/tooling remediation and shadow retry block.

The safety parser defect found in D1 is fixed in repository tooling. Enabled egress is now correctly detected from live KV registry rows. The shadow retry completed without `--apply`, and the new bounded proposal cap converted the broad raw shadow result into a one-move preview-only operator proposal while holding the execution cohort.

Runtime deploy was not performed, by rule.

## Report Files

- `BLOCK_D2_REALITY_AUDIT.md`
- `BLOCK_D2_IMPLEMENTATION_CONFLICT_AUDIT.md`
- `BLOCK_D2_TRUTH_SOURCE_AUDIT.md`
- `BLOCK_D2_RUNTIME_AUDIT.md`
- `BLOCK_D2_SAFETY_REMEDIATION.md`
- `BLOCK_D2_EGRESS_CERTIFICATION.md`
- `BLOCK_D2_PLANNER_CAP.md`
- `BLOCK_D2_HOLD_SEMANTICS.md`
- `BLOCK_D2_SHADOW_RETRY.md`
- `BLOCK_D2_SHADOW_QUALITY_REVIEW.md`
- `BLOCK_D2_FAIL_CLOSED_REVIEW.md`
- `BLOCK_D2_CERTIFICATION.md`

## Reality Audit

- Current branch: `v7-next`
- Local HEAD: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/v7-next`: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- Runtime user distribution stayed:
  - execution target: `10`
  - `awg0`: `3`
  - `awg3`: `3`
  - `vless`: `2`
- `v7-users-autoswitch.timer`: `inactive`
- No apply/movement/routing-sync process observed.

## Implementation Conflict Audit

Existing implementations were reused:

- `tools/v7-users-autoswitch` remains the only planner.
- `tools/v7-autoswitch-safety-review` was extended in place.
- Existing restore barrier semantics remain authoritative.
- No parallel runtime, planner, approval queue, routing engine, or apply path was introduced.

New helper:

- `tools/v7-autoswitch-proposal-cap`
- Role: read-only post-processor for existing shadow JSON.
- Authority: no execution authority.

## Safety Remediation

Fixed `tools/v7-autoswitch-safety-review` registry parsing:

- KV registry support added.
- Legacy two-column support retained.
- Enabled egress identity now resolves from `id/ip/name`.
- Enabled state now resolves from `enabled/value/state`.

Runtime certification using fixed repo script over SSH stdin:

- `status=ok`
- `enabled_egress=7`
- `users=18`
- `critical=0`
- `warning=0`

## Shadow Retry

Shadow retry summary:

- `apply_requested=false`
- `candidate_moves=12`
- `selected_moves=0`
- `healthy_egress_total=2`
- restore barrier still enforces zero selected movement

This confirms shadow mode ran but did not become execution.

## Planner Cap And Hold

Proposal cap input:

- raw candidate moves: `12`
- budget: `1`
- hold current egress: `amneziawg-exec-20260528-10-8-1-14`
- safety status: `ok`

Proposal cap output:

- held candidates: `10`
- eligible candidates: `2`
- proposal count: `1`
- ready for operator review: `true`
- proposed preview class: `vless -> awg0`

## Tests

Unit test command completed:

`65 tests OK`

Covered:

- safety-review KV parser
- legacy parser compatibility
- proposal budget cap
- hold semantics
- safety critical fail-closed
- invalid budget fail-closed
- `apply_requested=true` fail-closed
- existing autoswitch and operator packet tests

## Remaining Blockers

- Runtime-installed safety-review was not deployed because deploy is forbidden in D2.
- Admin API remains unavailable on `127.0.0.1:8017`.
- Raw shadow plan is still too broad for direct apply; bounded proposal cap must remain mandatory.

## Recommendation For Block E

Proceed only to a bounded operator-review block, not execution by default.

Minimum Block E gates:

1. Fresh runtime safety-review using the fixed parser or a deployed equivalent.
2. Fresh shadow sample without `--apply`.
3. Proposal cap budget `1`.
4. Hold execution cohort current egress.
5. Explicit operator approval for exact selected move.
6. Immediate pre-action registry hash recheck.
7. Separate stop condition if admin API is required and still unavailable.

## Required Verdicts

- safety_parser_fixed=true
- enabled_egress_certified=true
- planner_cap_working=true
- hold_semantics_working=true
- shadow_retry_completed=true
- shadow_quality_acceptable=true
- fail_closed_verified=true
- safe_to_continue_to_block_e=true

## Safety Verdicts

- users_moved=false
- autoswitch_apply_run=false
- routing_changed=false
- deploy_performed=false
- runtime_mutation_performed=false
- systemd_changed=false
- runtime_hooks_implemented=false

