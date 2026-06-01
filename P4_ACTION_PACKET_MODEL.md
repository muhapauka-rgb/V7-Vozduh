# P4 Action Packet Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Purpose

The Action Packet is the planning unit that binds dry-run trust to a future governed action path without executing it.

## Required Fields

| Field | Requirement |
| --- | --- |
| `action_id` | Stable id derived from canonical refs and scope. |
| `scope` | Exact action boundary. |
| `target` | Exact runtime target. |
| `candidate` | Candidate id, lifecycle state and lineage refs. |
| `evidence` | Runtime refs, hashes, freshness and dry-run verification. |
| `decision` | Planning decision, never direct execution. |
| `confidence` | Confidence with reasons and limits. |
| `verification_plan` | Pre-action, during-action and post-action checks. |
| `rollback_plan` | Preview-only rollback scope and triggers. |
| `observation_window` | Before/during/after monitoring windows and checkpoints. |
| `expiry` | Short TTL; expired packets abort. |
| `authority_state` | `PLANNING_ONLY` in P4. |
| `approval_state` | Proposed/review/approved/rejected/expired lifecycle. |

## Packet Lifecycle

1. `PROPOSED`
2. `REVIEW_REQUIRED`
3. `APPROVED_FOR_DESIGN`
4. `RECHECK_REQUIRED`
5. `READY_FOR_FUTURE_EXECUTION_BLOCK`
6. `REJECTED`
7. `EXPIRED`
8. `ABORTED`

## Non-Executable Flags

Every P4 Action Packet must include:

- `execution_allowed_now=false`
- `runtime_mutation_allowed=false`
- `routing_mutation_allowed=false`
- `user_movement_allowed=false`
- `autoswitch_apply_allowed=false`
- `rollback_execution_allowed=false`

## Verdict

`action_packet_defined=true`

