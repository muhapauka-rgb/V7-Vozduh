# Reconcile Quiet-Window Experiment

This began as an experiment design. Block E8 attempted the bounded rehearsal and aborted before quiet samples because a non-systemd control-plane loop remained active after the timer/service hold.

## Question

Does `v7-reconcile-check=FAIL` persist when autoswitch authority is held and route/rule/registry snapshots are stable?

## Order

1. Capture `users.registry` hash.
2. Capture `ip -4 rule show`.
3. Capture `ip -4 route show table all`.
4. Confirm no autoswitch/user-switch/routing-sync process.
5. Wait quiet interval.
6. Run `v7-reconcile-check` sample 1.
7. Capture `ip -4 rule show`.
8. Run `v7-reconcile-check` sample 2.
9. Capture `ip -4 rule show`.
10. Run `v7-user-route-check`.
11. Run `v7-killswitch-check`.
12. Run `v7-provisioning-reconcile-check`.

## Samples

Minimum:

```text
2 reconcile samples
3 ip-rule snapshots
1 route-table snapshot before
1 route-table snapshot after if any mismatch appears
```

Optional third reconcile sample if sample 1 and 2 disagree.

## Stable

Stable means:

- registry hash unchanged;
- expected ip rules present in all snapshots;
- route tables unchanged;
- no switch-history movement;
- no autoswitch process;
- user-route/killswitch/provisioning checks OK.

## False-Positive Classification

Reconcile FAIL can be classified as false-positive/degraded if:

- stable snapshots contain all expected rules;
- candidate route table is correct;
- route-get checks are OK;
- kill switch OK;
- provisioning reconcile OK;
- no moving control-plane process exists.

## Dangerous Mismatch Classification

Reconcile FAIL is dangerous if:

- candidate rule missing in stable `ip -4 rule show`;
- table route missing or wrong;
- route-get uses wrong/public interface;
- kill switch fails;
- provisioning reconcile fails;
- registry/assignment mismatch appears.

## Canary Implication

Canary remains blocked unless this experiment either passes cleanly or produces an approved false-positive waiver.

## Block E8 Execution Result

```text
rehearsal_executed=true
autoswitch_hold_attempted=true
abort=true
abort_reason=active_control_plane_process_after_hold
quiet_window_verified=false
reconcile_under_quiet=NOT_SAMPLED_ABORTED
autoswitch_restored=true
```

Evidence files:

```text
docs/track7/control-plane/e8-evidence/pre-rehearsal.txt
docs/track7/control-plane/e8-evidence/hold-confirmation.txt
docs/track7/control-plane/e8-evidence/abort.txt
docs/track7/control-plane/e8-evidence/post-restore.txt
docs/track7/control-plane/e8-evidence/summary.txt
```

Pre-hold reconcile still reported:

```text
V7_RECONCILE_RESULT=FAIL
errors=11
```

The quiet-window reconcile experiment did not complete, because after stopping `v7-users-autoswitch.timer` and `v7-users-autoswitch.service`, `pgrep` still found an external loop process invoking `v7-users-autoswitch`.

Current conclusion:

```text
The original race/semantic false-positive hypothesis remains unproven.
The stronger finding is that autoswitch authority is not only systemd timer/service authority.
```
