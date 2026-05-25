# Quiet-Window Evidence Packet

This document defines the exact evidence required for a future quiet-window rehearsal. It was not collected in Block E7.

## Evidence Directory

All evidence for a future rehearsal must be written under:

```text
/root/v7-quiet-window-$V7_QW_TS
```

This evidence write is allowed only inside an approved rehearsal. It is not a runtime convergence or repair action.

## Required Pre-Hold Evidence

| Evidence | File |
|---|---|
| systemd active state | `systemctl-active.before.txt` |
| systemd enabled state | `systemctl-enabled.before.txt` |
| timer state | `timers.before.txt` |
| active control-plane processes | `processes.before.txt` |
| users registry hash | `users-registry.before.sha256` |
| IPv4 rules | `ip-rules.before.txt` |
| all route tables | `routes-all.before.txt` |
| switch history tail | `switch-history.before.txt` |
| autoswitch safety state | `autoswitch-safety.before.json` |
| reconnect state | `client-reconnect-state.before.json` |
| load state | `egress-load-summary.before.json` |

## Required Hold Evidence

| Evidence | File |
|---|---|
| timer/service inactive state | `systemctl-active.hold.txt` |
| timer list after hold | `timer.hold.txt` |
| no autoswitch/user-switch/routing-sync process | `processes.hold.txt` |

## Required Quiet Samples

Minimum samples:

```text
quiet_sample_count=2
quiet_sample_interval=45 seconds
minimum_quiet_duration=90 seconds
```

Required quiet files:

```text
users-registry.quiet.sha256
ip-rules.quiet.txt
routes-all.quiet.txt
switch-history.quiet.txt
processes.quiet.txt
```

## Required Reconcile Samples

Run two reconcile samples with route/rule evidence around them:

```text
reconcile.1.txt
ip-rules.after-reconcile-1.txt
reconcile.2.txt
ip-rules.after-reconcile-2.txt
```

Stable means:

- reconcile status and messages are consistent;
- `ip-rules.after-reconcile-1.txt` and `ip-rules.after-reconcile-2.txt` do not drift unexpectedly;
- reconcile does not trigger route/rule/user assignment changes.

## Required Datapath Checks

| Check | Evidence |
|---|---|
| user route check | `user-route-check.txt` |
| kill switch check | `killswitch-check.txt` |
| provisioning reconcile check | `provisioning-reconcile-check.txt` |

Any warning blocks canary promotion until reviewed.

## Required Restore Evidence

| Evidence | File |
|---|---|
| active state after restore | `systemctl-active.after.txt` |
| enabled state after restore | `systemctl-enabled.after.txt` |
| timers after restore | `timers.after.txt` |
| processes after restore | `processes.after.txt` |
| registry hash after restore | `users-registry.after.sha256` |
| rules after restore | `ip-rules.after.txt` |
| routes after restore | `routes-all.after.txt` |
| switch history after restore | `switch-history.after.txt` |

## Drift Classification

| Drift | Meaning | Rehearsal Result |
|---|---|---|
| No registry/route/rule/switch-history drift | quiet evidence | Candidate for success |
| Reconcile output changes but route/rule state stable | possible semantic false-positive | Needs review |
| Registry or switch-history changes | user movement evidence | Fail |
| Route/rule changes without approved action | hidden control-plane mutation | Fail |
| Autoswitch process reappears | hold failure | Fail |
| Kill switch warning | datapath risk | Fail |
