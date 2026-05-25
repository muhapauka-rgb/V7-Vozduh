# V7 Phase 7 Upgrade Safety

## Purpose

Upgrades must be staged, reversible, and validated before runtime-affecting actions resume.

## Upgrade Stages

1. preflight inventory;
2. backup/snapshot;
3. compatibility validation;
4. staged file update;
5. contract validation;
6. runtime reconciliation;
7. post-upgrade verification;
8. rollback window.

## Preflight Checks

- required commands available;
- supported Linux/systemd/nft/iproute2;
- state files parse;
- identity DB opens;
- backup destination writable;
- disk space sufficient;
- safe mode status known.

## Post-Upgrade Checks

- admin API starts;
- validators pass or show explicit blockers;
- kill switch check passes;
- provisioning reconcile check passes;
- route classes are present;
- autoswitch safety state is readable;
- service matrix can be refreshed manually.

## Rollback Rule

If post-upgrade verification fails, V7 should remain in safe/maintenance posture and expose rollback context before any autoswitch or provisioning action continues.

