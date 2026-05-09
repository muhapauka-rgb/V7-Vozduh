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

## Rendered Disabled Runtime Config

Added command:

```bash
v7-proxy-inbound-render-disabled
```

Preview:

```bash
v7-proxy-inbound-render-disabled --inbound-id happ-test
```

Apply:

```bash
v7-proxy-inbound-render-disabled --inbound-id happ-test \
  --apply --confirm RENDER_PROXY_INBOUND_DISABLED
```

The command reads disabled identity bindings from:

```text
/etc/v7/inbound-runtime/happ-test/bindings/
```

Then it renders them into:

```text
/etc/v7/inbound-runtime/happ-test/sing-box.json
```

Security behavior:

- proxy UUID values are inserted into the root-only runtime config but never printed fully;
- `route.final` remains `block`;
- no service is started;
- no port is opened;
- no WireGuard users are moved;
- no routing, firewall, or kill switch state is changed;
- existing profile and binding files are backed up before apply;
- rendered binding files stay mode `600`.

Admin API currently exposes preview only:

```text
POST /api/actions/proxy-inbound-render-preview
```

There is intentionally no admin apply endpoint yet.

## Isolated Loopback Runtime Test

Added command:

```bash
v7-proxy-inbound-loopback-test --inbound-id happ-test
```

The command starts two temporary sing-box processes:

- loopback-only server from the rendered disabled profile;
- loopback-only SOCKS client that uses the first rendered proxy UUID.

Expected behavior:

- server listens only on `127.0.0.1`;
- client authentication path starts;
- outbound traffic stays blocked because `route.final = block`;
- no public port is opened;
- no systemd service is started;
- no firewall, kill switch, WireGuard, routing, or user state is changed;
- both temporary processes are stopped during cleanup.

Admin API endpoint:

```text
POST /api/actions/proxy-inbound-loopback-test
```

Role:

```text
operator
```

## Route Policy Mapping Dry Run

Added read-only command:

```bash
v7-proxy-route-policy-dry-run --inbound-id happ-test
```

The command builds a truth-check mapping:

```text
proxy UUID -> V7 user IP -> route table -> assigned egress/interface
```

It verifies:

- inbound runtime is still `rendered_disabled`;
- `route.final` is still `block`;
- the inbound listens only on `127.0.0.1`;
- each binding UUID is present in the rendered runtime config;
- the bound V7 user exists and is enabled in `users.registry`;
- the route table in the binding matches `users.registry`;
- the current egress exists and is enabled in `egress.registry`;
- the expected per-user `ip rule` is present;
- no public listener is open for the proxy inbound port.

Important limitation:

Proxy traffic does not naturally arrive as Linux source IP `10.0.0.x` like WireGuard traffic does. This dry-run intentionally does not claim live proxy routing is ready. It only proves the identity-to-route mapping is internally consistent. The next phase must implement a guarded runtime adapter before public enable.

Admin API endpoint:

```text
POST /api/actions/proxy-route-policy-dry-run
```

Role:

```text
viewer
```

## Policy Runtime Adapter Dry Run

Added read-only command:

```bash
v7-proxy-policy-runtime-adapter-dry-run --inbound-id happ-test
```

The command builds a temporary sing-box candidate config, but does not write it
to the live runtime path.

Current adapter candidate:

```text
proxy user name -> sing-box route rule -> direct outbound bound to V7 egress interface
```

For the current test binding this means:

```text
happ proxy identity -> 10.0.0.2 reference -> awg2 interface
```

Important:

- proxy traffic does not arrive as Linux source IP `10.0.0.x`;
- therefore the adapter does not directly use kernel table `100`;
- the table is kept as a reference to the V7 user assignment;
- the actual candidate runtime path uses sing-box `user` route matching and `bind_interface`;
- candidate `route.final` remains `block`;
- the generated candidate is validated with `sing-box check`;
- no file is written, no service is started, no public port is opened.

Admin API endpoint:

```text
POST /api/actions/proxy-policy-runtime-adapter-dry-run
```

Role:

```text
viewer
```

## VPS Result

On the VPS:

```text
V7_PROXY_INBOUND_PREFLIGHT=OK
V7_PROXY_INBOUND_DRAFT_CREATE=OK
draft_status=draft_disabled
V7_PROXY_IDENTITY_BIND=OK
binding_status=binding_disabled
V7_PROXY_INBOUND_RENDER_DISABLED=OK
runtime_status=rendered_disabled
rendered_bindings=1
binding_mode=600
included_in_runtime_config=True
route_final=block
V7_PROXY_INBOUND_LOOPBACK_TEST=OK
auth_path=temp_started
traffic_policy=blocked
V7_PROXY_ROUTE_POLICY_DRY_RUN=OK
proxy_mapping=10.0.0.2 -> table 100 -> awg2
V7_PROXY_POLICY_RUNTIME_ADAPTER_DRY_RUN=OK
adapter_mode=sing_box_user_rule_bind_interface
candidate_sing_box_check=OK
live_enable=BLOCKED
tcp_1443_listener=none
V7_RESULT=OK
```

## Next Step

After policy runtime adapter dry-run passes:

1. implement kill switch proxy identity guard dry-run;
2. verify proxy users cannot bypass approved egress interfaces;
3. design service-aware proxy routing for route classes;
4. only then expose Happ subscription generation.
