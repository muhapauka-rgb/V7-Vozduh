# Block A Reality Audit

Project: V7 Vozduh

Block: A - Single User Completion Program

Date: 2026-06-01

Mode: single-user lifecycle completion

## Scope

Approved user:

- `10.7.0.11`

Approved rollback:

- From: `amneziawg-exec-20260528-10-8-1-14`
- To: `1`
- Route table: `1009`
- Rollback interface: `v7e356a192b79`

## Repository State

- Branch: `v7-next`
- Local working tree before Block A reports: clean
- No deploy performed
- No systemd unit changes performed
- No routing changes outside table `1009` performed

## Runtime Truth Source

Runtime movement truth source is registry based:

- Users registry: `/opt/v7/egress/state/users.registry`
- Egress registry: `/opt/v7/egress/state/egress.registry`
- Assignment file: `/opt/v7/egress/state/user-10.7.0.11.assign`
- Switch history: `/opt/v7/events/switch-history.jsonl`
- Operator audit: `/opt/v7/audit/operator-execution-audit.jsonl`

SQLite `/opt/v7/v7.db` exists but has no runtime user tables and is not the user movement truth source.

## Pre-Rollback Runtime Snapshot

Captured from `/tmp/block-a-single-user-completion-20260601T104148Z`.

- `before_current=amneziawg-exec-20260528-10-8-1-14`
- `before_source_count=9`
- `before_target_count=1`
- `before_users_hash=0f280f338deec97d7ffb8bb3d7e945b9f3d9c969cb5495f4df40c3aa55b2cf1d`
- `before_outside_users_hash=d4a727db73f70e6f5a2a98747ed640c9a4c3edf6c1f0a9c89363c4499487ad8e`
- `before_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `before_selected_count=0`
- `before_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `before_routes_outside_hash=eeb83c6bc224a46f8682821148b360a2e76234e7587e023a050ae82103604eef`
- `before_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`
- `autoswitch_timer=inactive`

Route table `1009` before rollback:

```text
default dev v7execwg0 scope link
```

## Reality Verdict

- Exactly one user was in rollback scope.
- The execution egress contained exactly one target user before rollback.
- Existing registry state matched the approved rollback path.
- Autoswitch was inactive.
- No selected move queue was present.

