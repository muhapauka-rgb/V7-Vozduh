# Canary Promotion Rules

This document defines when a quiet-window rehearsal is successful enough to start discussing a future one-user canary. It does not approve canary execution.

## Promotion Is Discussion Only

A successful rehearsal permits canary discussion. It does not permit:

- `v7-user-switch`;
- `v7-routing-sync`;
- autoswitch apply;
- route/rule/nft mutation;
- customer movement.

## Rehearsal Success Requirements

All must be true:

- autoswitch timer and service were held for the approved window;
- no autoswitch/user-switch/routing-sync process appeared during quiet observation;
- registry hash stayed stable;
- switch-history showed no user movement;
- route/rule snapshots stayed stable or any drift is fully explained as read-only observation noise;
- reconcile output is stable across repeated samples;
- user-route, kill-switch, and provisioning checks do not warn or fail in a new way;
- autoswitch authority was restored and verified;
- evidence packet is complete.

## Reconcile Outcomes

| Outcome | Meaning | Canary Promotion |
|---|---|---|
| Reconcile passes repeatedly | Race hypothesis supported | Promotion discussion allowed. |
| Reconcile fails identically while route/rule/user checks are clean | Possible semantic false-positive | Requires explicit waiver before canary discussion. |
| Reconcile fails with changing output | Control-plane instability | No promotion. |
| Reconcile failure corresponds to missing route/rule state | Real routing risk | No promotion. |

## Still Blocking Canary After Successful Rehearsal

Even after rehearsal success, canary remains blocked if any are true:

- candidate user is still in anti-flap/penalty state;
- target egress is below quality floor without waiver;
- Trusted RU state is stale and relevant to candidate route class;
- rollback preview is stale or incomplete;
- autoswitch restore is uncertain;
- operator approval for canary is missing;
- canary command would require `v7-routing-sync` as first live mutation.

## Promotion Decision

Possible states:

```text
not_rehearsed
rehearsal_aborted_restored
rehearsal_failed
rehearsal_success_canary_still_blocked
rehearsal_success_canary_discussion_allowed
```

Current state:

```text
rehearsal_aborted_restored
```

## Block E8 Promotion Decision

Block E8 does not permit canary discussion.

Reason:

```text
The systemd timer/service hold was not sufficient to create a quiet window.
An external loop process continued to invoke v7-users-autoswitch.
Quiet samples were not collected.
Reconcile under quiet window was not measured.
```

Required before promotion can be reconsidered:

- map the non-systemd autoswitch loop owner;
- define a bounded hold model for that loop;
- repeat quiet-window rehearsal with all autoswitch authorities held;
- collect quiet samples A/B/C;
- prove registry/rule/route stability under quiet observation;
- re-evaluate reconcile under quiet window.
