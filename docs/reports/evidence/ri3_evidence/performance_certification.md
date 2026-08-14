# RI.3 Performance Certification

## Measured Commands

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin_core/routing_brain.py admin_core/routing_intelligence.py tools/v7-users-autoswitch
```

Result:

```text
PASS
```

```text
python3 -m unittest tests.unit.test_routing_brain
```

Result:

```text
Ran 14 tests in 0.127s
OK
```

```text
python3 -m unittest discover tests/unit
```

Result:

```text
Ran 195 tests in 13.942s
OK
```

```text
python3 -m unittest discover tests/contracts
```

Result:

```text
Ran 5 tests in 0.265s
OK
```

## Runtime Path

RI.3 runs inside planner as a bounded in-process read model:

```text
service_matrix + quality_summary + service_preferences + audit records
-> RoutingBrain.candidate_advisory_scores
-> bounded score_part
-> existing planner ranking
```

The planner caches RI candidate scores per user/service/route-class set during one planner run.

No network lookup was added.

No runtime write was added.

No governance lookup mutation was added.

## Performance Verdict

Performance certified for current repo tests.

Recommended future optimization before very large user pools:

- pre-aggregate service history;
- cache user service weights;
- keep execution trust as compact summary;
- compute RI advisory context in background for admin UI where possible.

