# Autoswitch / User Movement Snapshot

Evidence source:

```text
docs/track7/truth-snapshot/evidence/section-systemd-v7.txt
docs/track7/truth-snapshot/evidence/section-processes.txt
docs/track7/truth-snapshot/evidence/section-autoswitch-state.txt
docs/track7/control-plane/e8-evidence/*
```

## Authority

Systemd authority:

```text
v7-users-autoswitch.timer active/enabled
v7-users-autoswitch.service inactive/static
```

Non-systemd authority:

```text
/bin/bash -c while true; do v7-egress-history; v7-egress-stability; v7-egress-load; v7-egress-diagnose; v7-state-merge; v7-user-desired-state-save; v7-state-json-save; v7-users-autoswitch; sleep 30; done
```

This loop is the most important autoswitch truth. Block E8 proved timer/service hold is insufficient.

## State

```text
users.registry sha256=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
egress.registry sha256=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
autoswitch-safety.json present
client-reconnect-state.json present
```

Switch history tail shows repeated `autoswitch_failover` events on 2026-05-25 across many users.

## Stability

```text
moving_now=not proven at the exact snapshot instant
control_plane_quiet=false
quiet_window_verified=false
rehearsal_result=aborted_restored
```

## Risk Verdict

Autoswitch is operationally dangerous for canary attribution. It can move multiple users and has at least two authorities: systemd timer/service and a separate long-running shell loop. No canary should run until all autoswitch authorities are mapped and held under a separately approved model.
