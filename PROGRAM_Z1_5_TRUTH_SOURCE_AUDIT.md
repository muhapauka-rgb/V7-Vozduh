# Program Z1.5 Truth Source Audit

Date: 2026-06-01

## Truth Source Map

| Domain | Canonical Source | Derived Source | Presentation Source |
| --- | --- | --- | --- |
| Approval | operator packet contract | approval fingerprint | approval UI/report |
| Proposal | `v7-users-autoswitch` shadow JSON | `v7-autoswitch-proposal-cap` output | proposal packet |
| Candidate | fresh proposal cap output | candidate fingerprint | approval preview |
| Target | fresh planner candidate ranking and eligibility | target class/substitution verdict | movement packet |
| Policy | `/etc/v7/policy.json`, `/etc/v7/org-egress-policy.json` | policy fingerprint | governance report |
| Runtime truth | `users.registry`, `egress.registry`, safety state, service/trust/capacity files | runtime fingerprint | runtime audit |

## Important Rule

Approval truth cannot override runtime truth.

If an approved target no longer matches the fresh policy/fingerprint constraints, execution must fail closed.

## Policy Approval Truth

For a policy approval, the approved object should be:

- user or candidate class
- budget
- route class
- target class
- hard safety constraints
- substitution constraints
- runtime fingerprint tolerance
- TTL

The target egress ID becomes a derived runtime decision, not the approval's primary truth.

