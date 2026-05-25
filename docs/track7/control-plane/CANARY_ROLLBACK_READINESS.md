# Canary Rollback Readiness

## Candidate Rollback

Future forward canary:

```text
v7-user-switch 10.7.0.13 awg3
```

Rollback command:

```text
v7-user-switch 10.7.0.13 awg0
```

Rollback is also mutation and must not be executed without the same live approval boundary as the forward canary.

## Rollback Evidence Prepared

- Previous egress: `awg0`.
- Candidate target egress: `awg3`.
- Route table: `1011`.
- Rollback preview artifact: `docs/track7/control-plane/canary-previews/rollback-preview.json`.
- Expected rollback route: `ip route replace default dev awg0 table 1011`.

## Required Pre-Rollback Evidence During Future Canary

- Confirm current registry says `10.7.0.13 current=awg3`.
- Confirm table `1011` default route points to `awg3`.
- Confirm no autoswitch movement is active.
- Confirm kill switch is still OK before rollback.
- Confirm rollback operator approval is present.

## Required Post-Rollback Checks

- `users.registry` returns `10.7.0.13 current=awg0`.
- `user-10.7.0.13.assign` returns `awg0`.
- Table `1011` default route uses `awg0`.
- `v7-user-route-check` remains OK.
- `v7-killswitch-check` remains OK.
- Switch log/audit evidence exists if the live tools emit it.

## Partial Failure Handling

If rollback partially fails:

- do not run `v7-routing-sync` as an automatic fallback;
- capture `users.registry`, assignment file, table `1011`, and kill switch status;
- keep autoswitch held;
- escalate to manual operator review with one-user scope still preserved.

## Verdict

Rollback shape is understandable for this one-user candidate, but rollback is not yet operationally proven because no live canary or rollback has been executed.
