# V7 Phase 7 Graceful Degradation

## Purpose

V7 must continue core routing when non-core systems degrade.

## Degradation Priority

Preserve in order:

1. kill switch and no-leak guarantees;
2. existing stable user routing;
3. route class policy;
4. operator visibility;
5. autoswitch/provisioning automation;
6. advanced diagnostics.

## Degraded Mode Examples

If service matrix is stale:

- keep existing assignments;
- mark service visibility stale;
- avoid service-aware autoswitch until refreshed.

If autoswitch safety state is missing:

- freeze autoswitch apply;
- allow read-only diagnostics;
- require operator review.

If one egress is unstable:

- quarantine or maintenance candidate;
- avoid mass movement;
- preserve unaffected egress.

If backup destination is unavailable:

- block dangerous writes;
- allow read-only operations;
- surface explicit warning.

## Forbidden Degradation

Never degrade by:

- disabling kill switch;
- silently falling back to unsafe direct routing;
- enabling unverified egress;
- hiding mismatch from operator.

