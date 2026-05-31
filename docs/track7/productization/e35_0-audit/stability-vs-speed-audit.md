# E35.0 Stability vs Speed Audit

## Scope

Audit question: what does V7 prefer today when selecting or recommending channels: speed, stability, load, manual preference, required services, or some mix.

## Policy Inputs

policy_inputs_found=true

Current policy update model includes:

- autoswitch mode: `observe`, `guarded`, `active`
- cooldown seconds
- max planned/failover/reconnect moves
- score improvement thresholds
- quality floors: `min_avg_mbps`, `min_floor_mbps`, `min_stability`
- load mode and limits
- rebalance controls
- reconnect controls
- safety/freeze/quarantine controls

## Selection / Suitability Inputs

The code does not use pure speed-only selection. Current scoring/recommendation can use:

- health code and diagnose severity
- role exact match
- route class/service tag match
- service matrix fitness
- Telegram hard/down or degraded status
- priority and weight
- speed sample (`server_v7_mbps`)
- reserve/manual flags
- load/capacity policy

## Required Services Interaction

Required services are evaluated by `service_recommendations()`.

If a user's current channel does not satisfy required services and another channel does, generated proposals can produce `MOVEMENT_PROPOSAL` with status `REVIEW_REQUIRED`.

This is advisory/proposal behavior, not automatic runtime mutation by itself.

## Stability Semantics

Stability exists in policy and prior tests. Quality floors include both average speed and minimum floor speed, plus stability. Test fixtures show Telegram hard block and persistent service failure can trigger failover, while one-off degraded service signals do not automatically force movement.

## Audit Verdict

stability_vs_speed_audit_complete=true
selection_is_speed_only=false
stability_considered=true
required_services_considered=true
manual_assignment_persists=true
automatic_required_service_guarantee=false

## E35 Implication

The current system prefers a guarded suitability model:

health + services + route class + stability + speed + capacity

not just "fastest channel". E35 should make this visible and explicit in admin language: speed is one signal, not the contract.
