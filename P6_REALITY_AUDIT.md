# P6 Reality Audit

Project: V7 Vozduh

Program: P6

Block: P6

Mode: Certification / Execution / Observation / Verification

## Scope

Approved maximum scope:

- user: `10.7.0.11`
- source egress: `1`
- target egress: `amneziawg-exec-20260528-10-8-1-14`
- target interface: `v7execwg0`
- route table: `1009`
- rollback target: `1`

## Fresh Runtime Truth

Collected from:

`/opt/v7/egress/state`

Runtime host work directory:

`/tmp/p6-first-user-movement-20260601T102011Z`

## Verified Sources

- users registry: present
- egress registry: present
- selected moves: `missing_treated_as_empty`
- admin health: `OK`
- capacity: acceptable, target users before movement `0`
- trust: trusted RU state present, movement avoids trusted/direct route classes
- candidate state: `10.7.0.11 current=1 table=1009 enabled=1`
- target readiness: `GO`

## Existing Runtime Tools

Existing tools were present and reused:

- `/usr/local/bin/v7-user-switch`
- `/usr/local/bin/v7-route-movement-preview`
- `/usr/local/bin/v7-second-canary-target-readiness`
- `/usr/local/bin/v7-user-route-check`
- `/usr/local/bin/v7-killswitch-check`
- `/usr/local/bin/v7-provisioning-reconcile-check`
- `/usr/local/bin/v7-restore-settle-gate`

## Verdict

- reality_audit_complete=true
- fresh_runtime_truth_available=true
- candidate_state_verified=true
- target_readiness_verified=true
- scope_limited_to_one_user=true
