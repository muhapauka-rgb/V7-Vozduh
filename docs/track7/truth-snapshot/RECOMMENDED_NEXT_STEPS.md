# Recommended Next Steps

## What Is Actually Stable

- Host and core V7 services are up.
- Datapath checks are currently OK.
- Kill switch check is currently OK.
- User route check is currently OK.
- Provisioning reconcile is currently OK.
- Public/admin/proxy services are active.
- Runtime inventory is named and partially governed.

## What Only Looks Stable

- Routing looks operational, but `v7-reconcile-check` still fails and has not been tested under a true quiet window.
- Autoswitch timer/service state looks governable, but Block E8 proved a non-systemd autoswitch loop also exists.
- Trusted RU/Direct RU have state files, but Trusted RU decision state is stale/sensitive and cannot be treated as solved.
- Release object exists, but release provenance remains incomplete.

## What Is Dangerous

- Autoswitch can move users and has more than one authority.
- `v7-routing-sync` can mutate route/rule state across enabled users.
- `v7-user-switch` mutates live assignment and route table state.
- Policy/Direct/RU/proxy apply tools can affect runtime path decisions.
- Kill switch enable/disable/rebuild affects datapath safety.
- Broad rollback apply can restore sensitive runtime files and services.

## What Is Blocked

- Any one-user canary.
- Any routing-sync execution.
- Any autoswitch apply.
- Any Trusted RU refresh or policy apply.
- Any proxy runtime apply.
- Any kill switch mutation.

## Safe Next Steps

- Map the non-systemd autoswitch loop owner and launch mechanism.
- Add governance docs for non-systemd autoswitch authority.
- Prepare a second quiet-window rehearsal model that can hold all autoswitch authorities.
- Continue repo-side lineage resolution for remaining high-risk tools.
- Keep running static checks and read-only snapshots.

## Conditional Steps

- A second quiet-window rehearsal may be proposed only after non-systemd autoswitch hold/restore is modeled and separately approved.
- Canary discussion may start only after a successful quiet-window rehearsal and evidence review.
- Reconcile false-positive waiver may be discussed only with stable quiet-window route/rule evidence.

## Forbidden Steps Without Separate Approval

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`
- `v7-policy-apply`
- `v7-direct-*` mutation
- `v7-trusted-ru-refresh-missing`
- `v7-proxy-runtime-guard-apply`
- `v7-killswitch-enable`
- `v7-killswitch-disable-temporary`
- rollback apply
- service restart/deploy/cleanup/chmod/chown
