# P6.A Observation Plan

Project: V7 Vozduh

Block: P6.A

## Samples

Future P6.B certification should collect:

- before sample
- authorization sample
- immediate after-forward sample
- short delayed sample
- final delayed sample
- rollback samples if rollback is triggered

## Checkpoints

Each sample must record:

- users registry hash
- egress registry hash
- candidate row
- destination users count
- route table `1009`
- ip rule snapshot
- selected moves count/hash
- autoswitch timer/apply state
- admin health
- route/user/killswitch/provisioning checker outputs
- audit/switch-history counts

## Evidence Collection

Evidence should include:

- movement packet
- route preview
- target readiness
- pre-movement recheck
- forward verification
- observation samples
- rollback preview
- fail-closed matrix

## Retention

Keep compact reports and hashes in the repository. Keep large raw runtime captures in bounded evidence directories with cleanup/compaction consistent with existing retention practice.

## Verdict

- observation_plan_defined=true
- fully_observable=true
