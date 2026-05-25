# V7 Phase 7 Runtime Persistence Model

## Purpose

The platform must know what is authoritative, what is rebuildable, and what should not be trusted after restart.

## Persistent State

Persistent state must survive restart and backup/restore:

- `users.registry`;
- `egress.registry`;
- `egress-flags.state`;
- policy files;
- org policy;
- identity DB;
- audit log;
- event history;
- egress draft metadata;
- runtime profile files;
- admin auth/safe-mode files.

## Ephemeral State

Ephemeral state may disappear after restart:

- temporary runtime test interfaces;
- temporary helper outputs;
- process PID files;
- in-flight command output;
- transient probe results.

## Rebuildable State

Rebuildable state can be regenerated from authoritative inputs:

- service matrix;
- compact quality summaries;
- route reality snapshots;
- direct/RU diagnostics;
- autoswitch plan previews;
- path optimizer advice.

## Cached State

Cached state is useful but not authoritative:

- speed samples;
- path samples;
- client agent snapshots;
- reconnect observations;
- Telegram sentinel state.

## Recovery Rule

After restart or restore:

1. validate persistent state;
2. reconstruct runtime from desired state;
3. run read-only reconciliation;
4. verify kill switch and route classes;
5. only then allow production-affecting actions.

