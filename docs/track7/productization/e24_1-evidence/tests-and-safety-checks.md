# E24.1 Tests and Safety Checks

## Local Static/Syntax/Unit Tests

- `PYTHONPYCACHEPREFIX=.pycache-e24_1 python3 -m py_compile tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate`
  - result: PASS
- `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate`
  - result: PASS
  - count: `19` tests
- `python3 -m unittest discover tests`
  - result: PASS
  - count: `116` tests
- Local JSON smoke:
  - `tools/v7-second-canary-target-readiness --json`: JSON parse PASS
  - `tools/v7-restore-settle-gate --json`: JSON parse PASS
- `git diff --check`
  - result: PASS
- Credential scan on touched/generated E24.1 artifacts:
  - result: PASS, no credential patterns found

## Dangerous Call Scan

Result:

- No executable mutation calls found.
- No registry write calls found.
- No route/ip/nft mutation calls found.
- No service restart calls found.
- No autoswitch apply calls found.
- No user-switch calls found.

## VPS Runtime Safety Checks

Runtime checkers after deploy:

- `v7-reconcile-check`: PASS
- `v7-user-route-check`: PASS
- `v7-killswitch-check`: PASS
- `v7-provisioning-reconcile-check`: PASS

Runtime hashes after deploy/helper execution:

- `users.registry` unchanged: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` unchanged: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Hidden mover scan:

- No `v7-user-switch`.
- No `v7-routing-sync`.
- No `v7-users-autoswitch --apply`.

## Helper Output Checks

- `v7-second-canary-target-readiness --pretty`: PASS, live GO for WireGuard target.
- `v7-second-canary-target-readiness --json`: PASS, JSON valid.
- `v7-restore-settle-gate --pre-restore --pretty`: PASS executable, output NO-GO due missing default samples.
- `v7-restore-settle-gate --pre-restore --json`: PASS executable, JSON valid.
- `v7-restore-settle-gate --pre-restore --state-dir /opt/v7/egress/state --json`: PASS executable, output CONDITIONAL due insufficient samples.

## Tests Not Fully Run

- Endpoint inventory: not applicable; E24.1 did not touch admin/API routes.
- Frontend/static render: not applicable; E24.1 did not touch UI.

## Safety Verdict

- Deployment did not perform user movement.
- Deployment did not mutate routing.
- Deployment did not run autoswitch apply.
- Deployment did not restart services.
- Deployment mutated only the two approved helper tool paths.
