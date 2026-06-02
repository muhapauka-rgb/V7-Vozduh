# Z7.6-Z8 Evidence 03 - Test Results

## Commands

```text
python3 -m unittest tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
Ran 22 tests in 0.149s
OK
```

```text
python3 -m unittest tests/unit/test_operator_observability.py
```

Result:

```text
Ran 13 tests in 0.155s
OK
```

```text
python3 -m unittest tests/unit/test_operator_execution_packet.py
```

Result:

```text
Ran 7 tests in 0.011s
OK
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch
```

Result:

```text
OK
```

## Note

The first plain `py_compile` attempt failed because Python tried to write bytecode under the macOS user cache path outside the sandbox. The command was rerun with `PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache`, and syntax validation passed.

