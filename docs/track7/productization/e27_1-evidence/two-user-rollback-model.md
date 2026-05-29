# E27.1 Two User Rollback Model

## Rollback Manifest

```text
10.7.0.11 -> 1
10.7.0.12 -> 1
```

## Expected Route Restoration

```text
10.7.0.11 table=1009 default dev v7e356a192b79
10.7.0.12 table=1010 default dev v7e356a192b79
```

## Rollback Conditions

Rollback is safe if:

- both users still exist and remain enabled;
- both users moved only to `amneziawg-exec-20260528-10-8-1-14`;
- no third user moved;
- rollback executes exactly two approved commands or one governed batch with exactly two entries;
- route tables `1009` and `1010` restore to `v7e356a192b79`;
- target users count returns to 0;
- selected_moves remains 0;
- runtime checkers remain OK.

## Verdict

`two_user_rollback_safe=true`

This is a preparation-model verdict. The actual rollback proof still belongs to the future execution block.

