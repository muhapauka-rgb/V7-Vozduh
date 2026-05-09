# V7 Happ / Proxy Inbound Preflight

Date: 2026-05-09

## Goal

Prepare V7 for future Happ support without changing current production routing.

Happ cannot use the current V7 WireGuard user profile directly. It expects proxy/share/subscription formats such as:

- `vless://`
- `vmess://`
- `trojan://`
- `ss://`
- `socks://`
- standard subscription URL

Therefore the next safe architectural step is a dedicated V7 proxy inbound, not immediate Happ profile generation.

## Implemented

Added read-only preflight command:

```bash
v7-proxy-inbound-preflight [port]
```

Default port:

```text
1443
```

The command does not:

- open ports;
- write configs;
- restart services;
- move users;
- change firewall or kill switch;
- change WireGuard or routing tables.

It only checks whether the server is ready to host a future proxy inbound.

## Checks

The preflight inspects:

- OS/kernel/architecture;
- root access;
- required commands: `systemctl`, `ss`, `ip`, `nft`, `iptables`, `curl`, `jq`, `python3`, `sing-box`;
- default route and public interface;
- public IP;
- `net.ipv4.ip_forward`;
- current `wg0` visibility;
- candidate TCP/UDP port conflicts;
- V7 services;
- runtime directories;
- policy requirements for user identity binding and kill switch.

## Admin API

Added read-only endpoint:

```text
GET /api/proxy-inbound-preflight?port=1443
```

Role:

```text
viewer
```

Response includes:

- parsed summary;
- raw command output;
- purpose;
- next step.

## Important Architecture Note

WireGuard naturally gives V7 a per-user source IP, for example `10.0.0.6`.

A proxy inbound does not automatically preserve that same Linux source-IP model. V7 must bind proxy authentication to V7 identity:

```text
proxy UUID/password -> V7 user/device -> route policy -> egress
```

This must be implemented before Happ users are allowed into the active pool.

## Disabled Draft Profile

Added command:

```bash
v7-proxy-inbound-draft-create
```

The command has two modes:

```bash
v7-proxy-inbound-draft-create --id happ-test --port 1443 --listen 127.0.0.1
```

Preview only.

```bash
v7-proxy-inbound-draft-create --id happ-test --port 1443 --listen 127.0.0.1 \
  --apply --confirm CREATE_PROXY_INBOUND_DRAFT
```

Writes a disabled validation-only profile:

```text
/etc/v7/inbound-runtime/happ-test/sing-box.json
/etc/v7/inbound-runtime/happ-test/metadata.json
```

The generated profile:

- listens on `127.0.0.1` by default;
- is not started;
- does not open firewall ports;
- does not move users;
- does not change routing;
- has `route.final = block` until identity binding and policy routing are implemented.

Admin API currently exposes preview only:

```text
POST /api/actions/proxy-inbound-draft-preview
```

There is intentionally no admin apply endpoint yet.

## Disabled Identity Binding

Added command:

```bash
v7-proxy-identity-bind
```

Preview:

```bash
v7-proxy-identity-bind --inbound-id happ-test --user-ip 10.0.0.2 --client happ
```

Apply:

```bash
v7-proxy-identity-bind --inbound-id happ-test --user-ip 10.0.0.2 --client happ \
  --apply --confirm CREATE_PROXY_IDENTITY_BINDING
```

The command writes a root-only disabled binding:

```text
/etc/v7/inbound-runtime/happ-test/bindings/user-10.0.0.2.json
```

The binding maps:

```text
proxy UUID -> V7 user IP -> route table -> current egress
```

Security behavior:

- UUID is stored in the root-only binding file.
- UUID is never printed fully in command output.
- binding status is `binding_disabled`.
- binding is not included in runtime sing-box config yet.
- no listener is started.
- no route/firewall/user state is changed.

Admin API currently exposes preview only:

```text
POST /api/actions/proxy-identity-bind-preview
```

There is intentionally no admin apply endpoint yet.

## VPS Result

On the VPS:

```text
V7_PROXY_INBOUND_PREFLIGHT=OK
V7_PROXY_INBOUND_DRAFT_CREATE=OK
draft_status=draft_disabled
V7_PROXY_IDENTITY_BIND=OK
binding_status=binding_disabled
binding_mode=600
included_in_runtime_config=False
tcp_1443_listener=none
V7_RESULT=OK
```

## Next Step

After disabled identity binding exists, render a disabled runtime config that includes the binding:

```text
binding -> sing-box inbound users[] -> still route.final=block
```

Then:

1. validate rendered config with `sing-box check`;
2. start isolated loopback-only test instance;
3. verify auth works but traffic remains blocked;
4. implement route policy mapping;
5. run leak tests;
6. only then expose Happ subscription generation.
