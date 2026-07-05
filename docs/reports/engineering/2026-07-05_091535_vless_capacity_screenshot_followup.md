# VLESS Capacity Screenshot Follow-Up

## Summary

Screenshot shows:

```text
channel=vless
decision=Перевести пользователей
reason=Лимит назначений достигнут
load detail=59 пользователей назначено; жёсткий предел 2
```

This is the old production UI/read-model behavior.

## Why VLESS Still Shows Limit

The previous local patch has not been deployed to the live admin UI shown in the screenshot.

The live UI is still using the old fallback:

```javascript
hard = reg.hard_limit || policy.hard_limit || 2
```

and/or the old legacy load state produced by:

```bash
V7_LOAD_HARD_LIMIT default = 2
```

Therefore `vless` with 59 assigned users becomes:

```text
59 >= 2 -> capacity problem
```

This does not prove that `vless` has a real canonical two-user capacity.

## Why Other Channels May Not Show It

This condition appears only when the channel drawer/read-model decides Capacity is the active problem for that channel.

`vless` has many assigned users, so old fallback `hard=2` is highly visible there. Other channels may be showing a different primary decision/reason, or may not be opened in the same capacity drawer path.

The defect is not vless-specific. It is the same artificial fallback/default capacity issue.

## Current Local Fix Status

Local workspace already changes:

- `admin/v7-admin-api` no longer materializes blank limits as `1/2`;
- UI placeholders now show `pool default` / `not capped`;
- missing registry hard limit no longer becomes fallback `2`;
- `tools/runtime-support/v7-egress-load` no longer defaults to `hard=2`;
- tests prove no artificial cap is created when no real policy exists.

## Required Production Step

To remove this from the live UI:

1. Deploy the current local patch through the existing safe deploy process.
2. Restart/reload admin UI if required by safe deploy.
3. Rerun or wait for the load-state producer so legacy `egress-load.state` is refreshed.
4. If live `egress.registry` contains explicit `soft_limit=1 hard_limit=2` for `vless`, remove those fields through the existing production/admin registry owner.

No users need to move.

No runtime automation needs to be enabled.

No authority expansion is required.

## Verdict

VLESS_SCREENSHOT_SHOWS_OLD_PRODUCTION_CAPACITY_FALLBACK
