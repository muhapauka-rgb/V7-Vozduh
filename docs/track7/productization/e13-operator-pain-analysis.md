# E13 Operator Pain Analysis

## Purpose

E13 converts the proven bounded orchestration core into an operator-facing
product model. The problem is not missing runtime power. The problem is that
the safest actions still require the operator to mentally assemble truth from
reports, evidence folders, registry hashes, timers, journals, and dry-run
outputs.

## Current Operator Pain Map

| Area | Current pain | Unsafe moment | Product requirement |
|---|---|---|---|
| Runtime truth | Live state is spread across registry summaries, checkers, timer status, selected moves, target readiness, and restore-settle tools. | Operator can approve based on a stale or partial snapshot. | A single global operational truth layer with freshness, blockers, and action eligibility. |
| Evidence fragmentation | Each block writes strong evidence, but the chain is distributed across `BLOCK_*` reports and evidence directories. | Operator must know which report supersedes which historical state. | Evidence browser with canonical current decision, lineage, and superseded-state labeling. |
| Historical/live confusion | Earlier blocks proved stale fixture and historical NO-GO vs live GO confusion. | Historical target readiness can be mistaken for current target readiness. | Every displayed gate needs source, collected-at time, state directory, and staleness status. |
| Hidden movement risk | Delayed movement happened after apply timer restore even after restore-settle GO. | Apply timer can create non-obvious runtime mutation unless barrier/generation state is visible. | Apply lifecycle must show barrier, clearance, generation token, selected-move budget, and delayed monitor state together. |
| Approval burden | Approvals are currently tooling-driven and require reading selected moves, generation hashes, rollback targets, timers, and journals manually. | Operator may approve a movement without verifying exact fingerprint or rollback contract. | Approval Center with immutable preview fingerprint and explicit rollback/evidence contract. |
| Blast radius | Blast radius exists in reports, but it is not visually first-class. | Operator sees a target or move count but not the exact affected users and rollback scope. | Every movement preview must lead with affected users, targets, capacity delta, route delta, rollback delta, and maximum allowed movement budget. |
| Restore lifecycle | Planner restore, restore-settle, apply restore, barrier, TTL, clearance, and delayed monitoring are separate concepts. | Operator can believe restore is complete before delayed monitoring is clean. | Restore Lifecycle screen with phase rail and explicit "not complete until delayed monitor closed" semantics. |
| Generation-token opacity | E12 made generation ownership production-grade for bounded approvals, but the token is invisible to humans. | Operator may treat "token exists" as approval, or approve a different move set than the token owns. | Generation Governance screen showing token scope, selected-move fingerprint, budget, expiry, and mismatch reasons. |
| Rollback opacity | Rollback was proven, but rollback commands and verification are report-local. | Operator may approve forward movement without a validated rollback route and target state. | Rollback contract must be generated before approval and visible on the same approval surface. |
| Low-level tooling | Raw JSON, switch history, journal lines, hashes, and dry-runs are precise but cognitively expensive. | Important warnings can be buried inside verbose evidence. | Summarize first; raw evidence is a drawer, never the default. |
| Timer ownership | Planner/apply timer state changes are operationally critical. | Restoring apply without understanding barrier/generation state can reintroduce movement. | Timer state belongs in the global status band and every movement/restore approval. |
| Capacity clarity | WireGuard hard limit 2 drove governance decisions, but capacity is not encoded as an operator product concept. | Operator may reason in target names rather than load limits and reservation state. | Target Pool must show reserved/production eligibility, soft/hard caps, current users, and approval impact. |
| Language drift | Reports use precise block language, while future UI could drift into generic VPN/admin wording. | Generic labels hide bounded governance semantics. | Canonical vocabulary: movement, selected moves, generation token, restore barrier, rollback contract, delayed monitor. |

## Current Cognitive Overload Points

- Determining whether a state is live, copied, historical, or simulated.
- Comparing selected moves before and after barrier/clearance changes.
- Reconstructing who moved, why, and whether the movement was approved.
- Knowing whether apply timer is active, held, or safe to restore.
- Distinguishing "target readiness GO" from "approval allowed now".
- Understanding that two-user promotion-clean does not imply larger-cohort GO.
- Verifying that rollback is not just possible but already contracted.
- Finding the newest authoritative report for a governance decision.

## Unsafe Operator Moments

1. Approving a movement preview after the source registry hash has changed.
2. Clearing a restore barrier without seeing selected-move budget and generation token match.
3. Restoring apply timer before delayed monitoring is attached to the lifecycle.
4. Treating `selected_moves=0` as sufficient without checking hidden movers and switch-history delta.
5. Treating target readiness GO as capacity approval for a larger cohort.
6. Running broad autoswitch apply because the UI lacks a bounded approval primitive.
7. Missing a delayed movement because switch-history is not bound to the operation timeline.

## Productization Verdict

The orchestration core is mature enough for productization, but the operator
surface is not. The next risk is not missing runtime logic; it is approving the
right logic with stale, fragmented, or under-explained evidence.

