# P6.A Approval Design

Project: V7 Vozduh

Block: P6.A

## Approval Scope

Approval scope for P6.B must be exactly:

- user: `10.7.0.11`
- from: `1`
- to: `amneziawg-exec-20260528-10-8-1-14`
- movement budget: `1`
- route table: `1009`
- rollback target: `1`

## Approval TTL

Recommended TTL:

- 30 minutes maximum
- shorter if runtime health/capacity/trust is volatile

Approval expires immediately if any required runtime hash or readiness fact changes.

## Approval Invalidation

Invalidate approval if:

- user current egress is no longer `1`
- destination no longer has zero users
- destination readiness is not `GO`
- selected moves count is not `0`
- users registry hash changes
- egress registry hash changes
- route table `1009` baseline changes
- admin health is not OK
- autoswitch timer/apply becomes active unexpectedly
- trust/capacity gates change to blocked
- replay is detected

## Approval Renewal

Renewal requires a fresh packet, fresh dual approval, fresh recheck, and fresh movement preview.

## Approval Rejection

Reject if packet is unknown, missing, stale, expired, invalid, mismatched, replayed, or broader than the single-user scope.

## Verdict

- approval_defined=true
- approval_scope_single_user=true
- approval_ttl_required=true
