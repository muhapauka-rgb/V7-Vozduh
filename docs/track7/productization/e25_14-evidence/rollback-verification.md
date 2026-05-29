# E25.14 Rollback Verification

## Result

`rollback_success=false`

`rollback_not_required=true`

`candidate_still_on_1=true`

## Verification

Rollback was not required because no forward movement occurred.

Fresh recheck evidence showed:

```text
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
table_1009=default dev v7e356a192b79 scope link
route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 cache iif wg0
```

Runtime checkers remained OK.
