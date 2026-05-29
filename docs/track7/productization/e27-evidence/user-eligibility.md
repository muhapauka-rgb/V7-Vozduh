# E27 User Eligibility

`candidate_user_A=10.7.0.11`

`candidate_user_B=10.7.0.12`

## Candidate Pool

The current egress `1` pool is:

```text
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1
ip=10.7.0.14 current=1 table=1012 enabled=1
ip=10.7.0.15 current=1 table=1013 enabled=1
```

All four have sane route tables and route_get through `v7e356a192b79`.

## Selected Pair

`10.7.0.11` and `10.7.0.12` are selected for preparation because:

- both are enabled;
- both are currently on rollback target `1`;
- both have known route tables;
- both route through the expected device `v7e356a192b79`;
- both were stable across the E27 restore-settle sample window;
- `10.7.0.11` is the already-proven one-user candidate from E25.15;
- `10.7.0.12` is adjacent in the same source egress pool and provides a minimal second-user expansion.

## Eligibility Verdict

`candidate_user_A_eligible=true`

`candidate_user_B_eligible=true`

The pair is eligible as a candidate pair, but final two-user readiness depends on target capacity.

