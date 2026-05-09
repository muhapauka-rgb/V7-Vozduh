# V7 Phase: Proxy Two-Identity Live Probe

Date: 2026-05-09

## Goal

Prove that sing-box can distinguish two VLESS proxy identities before V7
scales happ/Karing proxy inbound to many users.

## Implemented

Added:

- `hardening/v7-proxy-two-identity-live-probe`

Updated:

- `admin/v7-admin-api`

## Probe Model

The probe starts only temporary loopback processes:

```text
identity A -> direct via awg2
identity B -> block
```

The test passes only if:

- identity A reaches the expected `awg2` external IP;
- identity B cannot reach the internet;
- no public port is opened;
- no persistent service is touched;
- no routing or kill-switch rule is changed.

## Admin API

```text
POST /api/actions/proxy-two-identity-live-probe
```

Required confirm token:

```text
RUN_PROXY_TWO_IDENTITY_PROBE
```

Role:

```text
owner
```

## Why This Matters

The previous canary had a single-egress fallback. That was fine for proving the
first public path, but it is not enough for a 500-user system. This probe tests
real identity-based routing before we remove fallback in the multi-user
candidate.

## Current Finding

The first live probe showed that sing-box route field `user` matches the local
Linux process user, not the authenticated VLESS user. V7 now uses `auth_user`
for proxy identity routing and removes the single-egress inbound fallback from
new public candidates. The next validation must prove:

- identity A can exit via `awg2`;
- identity B is blocked;
- the public candidate has `auth_user` rules;
- the public candidate has no inbound fallback.

## Validation Result

Validated on the VPS:

- two-identity live probe: OK;
- identity A external IP through `awg2`: `94.241.139.241`;
- identity B blocked: OK;
- public candidate route rule uses `auth_user`;
- public candidate inbound fallback: disabled;
- public-port canary: OK;
- direct `ens3` leak test: blocked;
- persistent public service restored: active/enabled on port `1443`;
- `v7-system-check`: `V7_RESULT=OK`.

Remaining expected limitation:

- only one proxy identity binding exists today, so full multi-user readiness is
  still `no` until V7 creates separate proxy identities for additional users.
