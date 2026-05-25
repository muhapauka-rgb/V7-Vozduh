# Canary Blast Radius Review

## Intended Forward Action

```text
v7-user-switch 10.7.0.13 awg3
```

The planner classifies the intended blast radius as:

```text
one_user
```

## Directly Affected Runtime Objects If Approved Later

- `users.registry` entry for `10.7.0.13`.
- `user-10.7.0.13.assign`.
- Route table `1011` default route.
- Switch log and audit log if available.

## Shared Dependencies

- egress interface `awg3`;
- shared kill switch/nft leak guard;
- `wg0` client ingress path;
- autoswitch timer and safety state;
- route-check/provisioning reconciliation checks.

## Largest Observed Risks

- Autoswitch can move users concurrently, expanding the effective blast radius beyond one user.
- `v7-routing-sync` preview would touch all enabled users, so it must not be used as the first correction step.
- Shared kill switch state protects all users; any failure there is platform-wide.
- Target `awg3` is enabled and empty, but quality is below configured floor in the sampled state.
- Reconcile check failure indicates route consistency ambiguity outside the selected candidate.

## Blast Radius Verdict

The planned user-switch action can be scoped to one user only if autoswitch is held and no routing-sync fallback is used. Current live conditions do not satisfy that requirement.
