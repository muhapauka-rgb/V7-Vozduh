# E25.7 Rollback / Removal Plan

## Executed Removal

- `rollback_removal_executed=true`
- `wg_quick_down_exit=0`
- `interface_removed=true`
- `normalized_config_removed_from_active_path=true`
- `config_archived_to=/root/e25_7_v7execwg0.conf.removed.20260528T121350Z`

## Verification

- default route unchanged;
- DNS resolver hash unchanged;
- users registry hash unchanged;
- egress registry hash unchanged;
- candidate route table unchanged;
- candidate `route_get` unchanged;
- hidden movers absent.

## Future Removal Steps

If a future activation leaves the interface up:

1. `wg-quick down v7execwg0`
2. archive `/etc/wireguard/v7execwg0.conf`
3. remove any active execution-only metadata row if it was written;
4. verify default route and DNS unchanged;
5. verify `users.registry` unchanged;
6. verify selected_moves remains zero;
7. run runtime checkers.

