# E8.3 Evidence Index

Block: E8.3.

Mode: repo-side design only.

No live runtime inspection or mutation was performed in this block. E8.3 uses
the E8.1 authority evidence and E8.2 approval packet to prepare a deployable
design proposal.

## Created Design Artifacts

```text
docs/track7/control-plane/HEALTH_AUTOSWITCH_PLANNER_SPLIT_DESIGN.md
docs/track7/control-plane/HEALTH_AUTOSWITCH_SPLIT_MIGRATION_PLAN.md
systemd/drafts/v7-health.service
systemd/drafts/v7-autoswitch-planner.service
systemd/drafts/v7-autoswitch-planner.timer
BLOCK_E8_3_HEALTH_AUTOSWITCH_PLANNER_SPLIT_DESIGN_REPORT.md
```

## Source Evidence

The design is based on:

```text
docs/track7/control-plane/e8_1-evidence/process-truth.txt
docs/track7/control-plane/e8_1-evidence/systemd-login-authority.txt
docs/track7/control-plane/NON_SYSTEMD_AUTOSWITCH_AUTHORITY_MAP.md
BLOCK_E8_2_FULL_AUTHORITY_QUIET_WINDOW_APPROVAL_PACKET.md
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed: NO
Deploy performed: NO
```
