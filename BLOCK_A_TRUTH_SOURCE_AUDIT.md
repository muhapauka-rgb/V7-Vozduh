# Block A Truth Source Audit

Project: V7 Vozduh

Block: A - Single User Completion Program

Date: 2026-06-01

## User Movement Truth Source

Primary truth source:

- `/opt/v7/egress/state/users.registry`

The approved user row before rollback:

```text
ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
```

The approved user row after rollback:

```text
ip=10.7.0.11 current=1 table=1009 enabled=1
```

## Egress Truth Source

Primary egress truth source:

- `/opt/v7/egress/state/egress.registry`

Rollback egress:

- `id=1`
- `interface=v7e356a192b79`
- `enabled=1`

Execution egress:

- `id=amneziawg-exec-20260528-10-8-1-14`
- `interface=v7execwg0`
- `manual_only=1`
- `reserve_only=1`
- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`

## Hash Continuity

Unaffected user rows:

- Before: `d4a727db73f70e6f5a2a98747ed640c9a4c3edf6c1f0a9c89363c4499487ad8e`
- Final: `d4a727db73f70e6f5a2a98747ed640c9a4c3edf6c1f0a9c89363c4499487ad8e`

Egress registry:

- Before: `09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- Final: `09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`

IP rules:

- Before: `200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`
- Final: `200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

Routes outside table `1009`:

- Before: `eeb83c6bc224a46f8682821148b360a2e76234e7587e023a050ae82103604eef`
- Final: `eeb83c6bc224a46f8682821148b360a2e76234e7587e023a050ae82103604eef`

## Truth Source Verdict

- Truth source clean: true
- Registry source used: true
- SQLite runtime assumption rejected: true
- User outside scope unchanged: true
- Egress registry unchanged: true

