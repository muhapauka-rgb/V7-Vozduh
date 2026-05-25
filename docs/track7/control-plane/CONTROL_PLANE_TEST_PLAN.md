# Control Plane Test Plan

Only static tests and repo checks are allowed in the current governance block.

## 1. Static Tests

Run now:

```text
tools/v7-run-tests
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff tools/v7-control-plane-governance-check
bash -n copied shell evidence when available
python3 -m json.tool docs/track7/lineage/*.json
tools/v7-control-plane-governance-check --runtime-enumeration runtime-enumeration.json --pretty
python3 -m unittest tests.unit.test_v7_route_movement_preview
```

## 2. Read-Only Runtime Checks

Allowed later only with explicit read-only runtime approval:

```text
v7-killswitch-check
v7-killswitch-status
v7-user-route-check
systemctl --failed ...
```

Do not mix read-only checks with apply commands in the same runbook.

## 3. Dry-Run Checks

Allowed later only after each command is classified:

- autoswitch plan if reconnect/load-summary writes are accepted;
- policy apply dry-run if `v7-policy-resolve` state write is either disabled or accepted;
- proxy apply preview if temp config behavior is accepted.

## 4. One-User Canary Checks

Not allowed in this block.

Future prerequisites:

- route movement preview JSON exists;
- preview has `mutation=false`;
- preview has no `errors`;
- one named user;
- previous egress known;
- target egress verified;
- kill switch OK before;
- rollback command ready;
- post route check mandatory.

## 5. Full Apply Checks

Not allowed in this block.

Future prerequisites:

- successful static checks;
- successful read-only checks;
- successful dry-run;
- successful canary;
- explicit operator approval;
- rollback backup and owner present.

## Current Block Verification

This block verifies only:

- docs exist;
- JSON metadata parses;
- checker compiles and runs read-only;
- route movement preview planner compiles and is tested against fixtures;
- existing test gate stays green;
- lineage/release checkers still report partial governance honestly.
