# V7 Phase 7 Disaster Recovery

## Purpose

Disaster recovery must rebuild a safe routing platform from known state, not from administrator memory.

## Disaster Scenarios

- host reboot with stale runtime;
- corrupted registry;
- lost runtime profile;
- failed upgrade;
- accidental policy change;
- backup restore needed;
- egress pool partially unavailable;
- admin API unavailable.

## Recovery Order

1. secure host access;
2. preserve current state snapshot;
3. restore or validate persistent state;
4. verify dependencies;
5. verify kill switch;
6. run contract validation;
7. run lifecycle validation;
8. run provisioning reconciliation;
9. reconstruct runtime profiles if needed;
10. verify route classes and affected users.

## Safe Recovery Principle

Recovery should favor:

- no leaks;
- existing stable assignments;
- explicit degraded state;
- operator-visible blockers.

It must not favor:

- fastest restoration at the cost of datapath safety;
- silent direct routing;
- unsafe mass migration.

