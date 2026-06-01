# Program Z2 Autonomy Certification

Date: 2026-06-01

## Verdict

autonomy_certified=false

## Certified

The governance contract is certified for:

- hybrid approval validation
- policy approval with budget `1`
- target substitution validation
- policy/proposal/runtime fingerprints
- runtime recheck
- replay protection
- append-only governance record
- fail-closed denial paths

## Not Certified

Live bounded autonomy is not fully certified because real user movement was not executed under this Z2 contract.

Blocker:

- live runtime state path unavailable in this workspace
- movement executor not invoked

## Quality

Targeted unit tests passed:

- `tests.unit.test_v7_hybrid_approval`
- `tests.unit.test_v7_autoswitch_proposal_cap`
- `tests.unit.test_operator_execution_packet`

Result:

- `14 tests OK`

Full unit discovery:

- `175 tests OK`

## Safety

- scope_expanded=false
- autonomous_budget=1
- users_moved=false
- routing_changed=false
- deploy_performed=false
