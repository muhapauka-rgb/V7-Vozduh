# P6 Final Verification

Project: V7 Vozduh

Block: P6

## Movement Outcome

- did movement occur: true
- moved user: `10.7.0.11`
- final egress: `amneziawg-exec-20260528-10-8-1-14`
- target correct: true
- route table `1009`: `default dev v7execwg0 scope link`
- target users: `1`

## Scope Verification

- users moved count: `1`
- users outside scope untouched: true
- routing outside scope changed: false
- egress registry unchanged: true
- selected moves unchanged: true
- autoswitch apply run: false
- deploy performed: false
- rollback executed: false

## Final Hashes

- users registry hash: `256c20b85442caea1de7bd7501b95c22bd39f2ee7eb92241c304458d2f76afcc`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `cf0d6a3be5d4d17166dd610f2d288b419945b319def6a2daef015f12bd97c1c9`

## Checkers

- user route check: `OK`
- kill switch check: `OK`
- provisioning reconcile check: `OK`
- admin health: `OK`

## Required Verdicts

- target_ready=true
- packet_created=true
- approval_valid=true
- runtime_recheck_passed=true
- movement_executed=true
- observation_completed=true
- rollback_ready=true
- replay_protection_verified=true
- fail_closed_verified=true
- first_user_movement_successful=true

## Safety Verdict

- scope_expanded=false
- users_moved_count=1
- routing_changed_outside_scope=false
- autoswitch_apply_run=false
- deploy_performed=false
- rollback_executed=false
