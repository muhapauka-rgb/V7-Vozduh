# Simulation And Tests

Targeted simulations were implemented as unit tests.

Certified scenarios:

- default canary caps a large request to one selected move;
- prepared small batch allows two selected moves;
- canary cannot be raised above one by policy;
- disabled authority gate fails closed;
- pool distribution tests use explicit prepared large-batch authority.

Test results:

- `PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m py_compile tools/v7-users-autoswitch`: PASS
- `PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`: 30 tests OK
- `PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m unittest tests.unit.test_best_available_pool_policy tests.unit.test_v7_users_autoswitch_policy`: 36 tests OK
- `PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m unittest discover tests`: 315 tests OK

