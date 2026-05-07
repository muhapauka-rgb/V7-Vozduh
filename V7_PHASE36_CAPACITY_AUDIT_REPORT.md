# V7 Phase 36: Capacity audit for 500 users

Date: 2026-05-07

## Goal

Check whether the current WireGuard/V7 address plan can scale to the target of
500 users without changing the live network blindly.

## Added

### `/usr/local/bin/v7-capacity-check`

Read-only capacity check:

- Reads current `wg0` address/CIDR.
- Calculates usable client capacity.
- Counts registered and active V7 users.
- Lists remaining `/24` references that must be handled before expanding the
  subnet.
- Returns:
  - `V7_CAPACITY_RESULT=OK`
  - `V7_CAPACITY_RESULT=WARN`
  - `V7_CAPACITY_RESULT=FAIL`

### Admin dashboard

`v7-admin-api` now runs:

```bash
v7-capacity-check 500
```

Dashboard summary now includes a `Capacity` card. Diagnostics include the full
capacity output.

## Findings

Current VPS:

```text
wg_address=10.0.0.1/24
current_client_capacity=253
target_users=500
recommended_min_cidr=/23
recommended_client_capacity=509
registered_users=2
active_users=2
V7_CAPACITY_RESULT=FAIL
```

Important `/24` dependencies found:

- `/etc/wireguard/wg0.conf`
- `/usr/local/bin/v7-killswitch-enable`
- `/usr/local/bin/v7-killswitch-check`
- `/usr/local/bin/v7-user-create`

## Decision Needed Later

To support 500 users, V7 should move from `10.0.0.0/24` to at least
`10.0.0.0/23`.

This should be done as a maintenance step because it touches:

- `wg0` server address.
- NAT rules.
- kill switch subnet rules.
- user creation IP allocator.
- admin validation regex.
- route/direct diagnostics defaults.
- generated client config assumptions.

No live subnet expansion was performed in this phase.

## Validation

Commands run:

```bash
bash -n /usr/local/bin/v7-capacity-check
v7-capacity-check 500
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api
curl -sS -o /tmp/v7-admin-root.html -w "%{http_code} %{size_download}\n" http://127.0.0.1:7080/
```

Result:

- `v7-capacity-check` works and reports `/23` as minimum for 500 users.
- `v7-admin-api`: active.
- Admin root returned `303`, expected redirect to login.
