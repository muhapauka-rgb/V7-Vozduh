# V7 Phase 34: Registry-driven system check and admin actions

Date: 2026-05-07

## Goal

Continue N-egress hardening after Phase 33.

The next risky hardcodes were in:

- `v7-system-check`
- `v7-admin-api`
- `v7-client-speed-api`

The target behavior is that checks and admin actions use
`/opt/v7/egress/state/egress.registry` as the source of truth instead of
assuming only `vless` and `awg2`.

## Changed

### `/usr/local/bin/v7-system-check`

- Decision validation now checks whether `DECISION` exists and is enabled in
  `egress.registry`.
- Per-user route expected interface now comes from each egress `interface=...`
  field.
- Direct egress tests now loop over enabled registry entries:
  - `test=socks5://...` uses SOCKS curl.
  - `type=interface`, `type=tun`, or `test=interface` uses curl by interface.
- The check no longer hardcodes expected route devices for only `vless/awg2`.

### `/usr/local/bin/v7-admin-api`

- Added registry helpers for enabled egresses, egress existence, default egress,
  interface lookup, and config path lookup.
- User route reality in the admin overview now uses registry interface mapping.
- Create-user egress selector is generated from enabled registry rows.
- User switch button chooses the first enabled alternative egress from registry.
- Backend validation for user create/switch now accepts enabled registry egresses
  instead of only `awg2` and `vless`.
- Egress speed/matrix/state actions now verify the egress exists in registry.

### `/usr/local/bin/v7-client-speed-api`

- The phone direct-speed page now populates egress options from
  `egress.registry`.

## Backups

Before installation, VPS backups were created under `/root/v7-backups/`:

- `v7-system-check.20260507-105003.bak`
- `v7-admin-api.20260507-105406.bak`
- `v7-client-speed-api.20260507-105406.bak`

## Validation

Commands run on VPS:

```bash
bash -n /usr/local/bin/v7-system-check
python3 -m py_compile /usr/local/bin/v7-admin-api /usr/local/bin/v7-client-speed-api
systemctl restart v7-admin-api v7-client-speed-api
systemctl is-active v7-admin-api v7-client-speed-api v7-api v7-health v7-benchmark
v7-system-check
curl -sS http://10.0.0.1:7090/ | grep -E "option value|V7 Speed" | head
curl -sS http://127.0.0.1:7077/health
jq -r ".egress|keys|join(\",\")" /opt/v7/egress/state/v7-state.json
```

Result:

- `v7-admin-api`: active
- `v7-client-speed-api`: active
- `v7-api`: active
- `v7-health`: active
- `v7-benchmark`: active
- `v7-system-check`: `V7_RESULT=OK`
- Direct egress tests:
  - `vless_ip=77.110.103.131`
  - `awg2_ip=94.241.139.241`
- Phone speed page shows registry-driven options:
  - `vless`
  - `awg2`
- V7 state API health: `OK`
- JSON egress keys: `awg2,vless`

## Notes

- Existing users stayed on `vless`; no user routing mutation was performed in
  this phase.
- Manual rebalance remains manual.
- `v7-decide-egress` may prefer a faster candidate, but `v7-users-autoswitch`
  keeps the current assignment when current quality is still OK.
- `EGRESS_CONFIG_PATHS` remains as a fallback for existing known config paths.
  Future uploaded egresses should add `config=` or `config_path=` to registry
  so config details can be shown without code changes.
