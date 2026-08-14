# CTR.I4 No-Bypass And Validation Evidence

## No-bypass flags

`ctr_shadow_comparison.no_bypass` explicitly reports:

- `selected_moves_changed=false`
- `planner_ranking_changed=false`
- `runtime_behavior_changed=false`
- `routing_changed=false`
- `governance_authority_changed=false`
- `packet_authority_changed=false`

## Validation

Targeted tests passed:

- CTR.I3 simulation parity test
- CTR.I4 shadow comparison test assertions
- CTR.I1 no-bypass tests
- CTR.I2 review-required tests

Command result:

- 10 tests OK

Additional validation performed:

- `py_compile tools/v7-users-autoswitch`

Full suite and diff check are recorded in the final report after validation.

