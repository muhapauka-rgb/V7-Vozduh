# Block D Truth Source Audit

Project: V7 Vozduh

Block: D - Autoswitch Shadow And Operator Program

Date: 2026-06-01

## Autoswitch Candidate

Canonical source:

- `v7-users-autoswitch` dry-run output

Derived sources:

- Autoswitch safety state
- Policy file
- Quality summary
- Service matrix
- Users registry
- Egress registry

Presentation source:

- Block D reports

## Movement Recommendation

Canonical source:

- Shadow JSON decisions from `v7-users-autoswitch --mode guarded` without `--apply`

Derived source:

- Operator approval model

Presentation source:

- Shadow mode and shadow accuracy reports

## Approval

Canonical source:

- `v7-operator-execution-packet`
- Operator packet JSON

Derived source:

- Audit and recheck records

Presentation source:

- Operator execution report

## Verification

Canonical source:

- `v7-user-route-check`
- `v7-killswitch-check`
- `v7-provisioning-reconcile-check`

## Rollback

Canonical source:

- `v7-route-movement-preview`
- Existing `v7-user-switch` rollback path

## Verdict

Truth sources are identifiable. The blocker is not source ambiguity; it is unsafe recommendation quality and safety-review status.

