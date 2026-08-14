# RI.3 Test Results

## Targeted RI Tests

Command:

```text
python3 -m unittest tests.unit.test_routing_brain
```

Result:

```text
Ran 14 tests in 0.127s
OK
```

Coverage:

- RI cannot move users;
- RI cannot approve governance;
- missing RI data does not become pass;
- service weights affect advisory score;
- execution trust affects blast recommendation;
- bad service history lowers suitability;
- RI.3 candidate advisory contract emits bounded score parts;
- RI.3 user weight changes candidate advisory score;
- planner remains decision owner;
- missing RI data does not override planner gates;
- RI.3 influences ranking among eligible candidates;
- RI.3 does not bypass canary reservation or create candidates.

## Full Unit Suite

Command:

```text
python3 -m unittest discover tests/unit
```

Result:

```text
Ran 195 tests in 13.942s
OK
```

## Contract Suite

Command:

```text
python3 -m unittest discover tests/contracts
```

Result:

```text
Ran 5 tests in 0.265s
OK
```

