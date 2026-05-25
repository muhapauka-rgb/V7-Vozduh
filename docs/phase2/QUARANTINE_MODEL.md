# V7 Phase 2 - Quarantine Model

## Purpose

Quarantine prevents unverified egress from affecting production.

It is not a label. It is an isolation contract.

## Quarantine Guarantees

While quarantined, an egress has:

- no users;
- no autoswitch participation;
- no route-class eligibility;
- no production routing impact;
- no silent registry enable;
- no kill switch bypass;
- no direct/RU exception usage unless specifically tested as policy-safe.

## Entry Conditions

An egress enters quarantine when:

- imported but not verified;
- runtime test is pending;
- service matrix is unknown;
- MTU/DNS/path is not verified;
- dependency is missing;
- duplicate conflict exists;
- route/rule conflict is possible;
- health history is not established.

## Exit Conditions

Quarantine can exit only when:

- preflight passed;
- temporary runtime test passed;
- service matrix passed for intended route class;
- runtime profile is ready;
- kill switch compatibility is verified;
- no duplicate/conflicting route exists;
- operator explicitly proceeds to disabled pool or enable flow.

## Blocked Quarantine

Blocked quarantine must be shown when:

- runtime did not start;
- external IP failed;
- cleanup failed;
- service matrix failed;
- dependency is missing;
- trusted RU route has no safe fallback;
- duplicate was found and not explicitly resolved.

## Autoswitch Rule

Autoswitch must ignore quarantined egress.

Quarantine evidence may inform readiness, but it must not cause automatic user migration.

## Operator View

Summary labels:

- `testing`;
- `quarantine`;
- `ready`;
- `blocked`;
- `degraded`;
- `rollback available`.

Details on drill-down:

- dependency check;
- temporary interface/proxy result;
- service matrix details;
- cleanup result;
- duplicate evidence;
- policy/route-class fit.
