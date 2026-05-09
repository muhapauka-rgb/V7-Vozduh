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

## Kill Switch Proxy Identity Guard Dry Run

Added read-only command:

```bash
v7-proxy-killswitch-guard-dry-run --inbound-id happ-test
```

Why this is needed:

- WireGuard users are protected in the Linux `forward` path.
- Proxy inbound traffic is generated by a local sing-box process.
- Local process traffic uses the Linux `output` path.
- Therefore the existing WireGuard kill switch is not enough for future public proxy inbound.

The dry-run builds a future guard plan:

```text
runtime user v7proxy -> allow approved egress interfaces -> drop public ens3 -> drop everything else
```

It checks:

- runtime is still disabled and loopback-only;
- `route.final` is still `block`;
- no public listener exists;
- bound egress interfaces are live;
- current nftables kill switch table exists;
- whether the future proxy runtime user exists;
- whether proxy-specific nft `output` guard rules already exist.

No nftables rules are changed in this phase.

Admin API endpoint:

```text
POST /api/actions/proxy-killswitch-guard-dry-run
```

Role:

```text
viewer
```

## Proxy Public Enable Guard Dry Run

Added final read-only public enable gate:

```bash
v7-proxy-public-enable-guard-dry-run --inbound-id happ-test
```

The command combines the staged checks:

- rendered runtime config exists;
- profile is still loopback-only;
- `route.final` is still `block`;
- identity bindings exist;
- no public listener is already open;
- route policy mapping dry-run is OK;
- policy runtime adapter dry-run is OK;
- proxy kill-switch guard dry-run is OK;
- live prerequisites are either satisfied or listed as blockers.

For the current system the correct result is `BLOCKED`, because this phase is
only a dry-run and the live prerequisites are not applied yet:

```text
create_runtime_user:v7proxy
add_nft_output_skuid_guard
add_nft_output_allow_rules_for_proxy_runtime_user
add_nft_output_drop_public_rule_for_proxy_runtime_user
```

Admin API endpoint:

```text
POST /api/actions/proxy-public-enable-guard-dry-run
```

Role:

```text
viewer
```

## Proxy Service-Aware Routing Dry Run

Added read-only command:

```bash
v7-proxy-service-aware-routing-dry-run --inbound-id happ-test
```

The command builds a temporary sing-box candidate config for service-aware
proxy routing:

```text
proxy user -> route class domains -> selected egress/interface
```

It validates the candidate with:

```bash
sing-box check
```

Current safety decisions:

- `GLOBAL_FAST`, `GLOBAL_STABLE`, `VIDEO_OPTIMIZED`, and `LOW_LATENCY` can be represented as sing-box `user + domain` route rules to approved egress interfaces.
- `DIRECT_RU` is blocked for server-side proxy until an output destination guard exists, or until the client handles RU split-routing locally.
- `TRUSTED_RU_SENSITIVE` stays blocked while the configured path is marked temporary.
- candidate `route.final` remains `block`;
- no runtime file is written;
- no service is started;
- no public port is opened;
- no nftables, routing, user, or registry state is changed.

Admin API endpoint:

```text
POST /api/actions/proxy-service-aware-routing-dry-run
```

Role:

```text
viewer
```

## Proxy Guarded Apply Design

Added read-only design command:

```bash
v7-proxy-guarded-apply-design --inbound-id happ-test
```

The command collects all staged proxy checks into one guarded apply design:

- route policy mapping;
- policy runtime adapter;
- proxy kill-switch output guard;
- public enable guard;
- proxy service-aware routing.

It does not apply anything. It only produces the future safe apply phases:

1. `apply_runtime_user`
   - create locked system user `v7proxy`;
   - audit required;
   - rollback only if no service uses it.

2. `apply_nft_output_guard`
   - add nft `output` rules for the proxy runtime user;
   - allow only approved egress interfaces;
   - drop public interface direct leak;
   - backup and rollback required.

3. `render_guarded_public_candidate`
   - render public candidate profile;
   - keep service stopped;
   - backup and rollback required.

4. `public_port_canary`
   - temporary one-identity public canary;
   - timeout controlled;
   - verify leak protection.

5. `operator_enable_action`
   - future final action only after canary and leak tests.

Admin API endpoint:

```text
POST /api/actions/proxy-guarded-apply-design
```

Role:

```text
viewer
```

## Proxy Runtime Guard Apply Preview

Added read-only apply preview:

```bash
v7-proxy-runtime-guard-apply-preview --inbound-id happ-test
```

The preview prepares the first future live prerequisite:

```text
runtime user v7proxy + nft output guard
```

It shows:

- whether `v7proxy` already exists;
- which egress interfaces would be allowed;
- which nft `output` rules would be added;
- where the nft ruleset backup would be written;
- rollback steps;
- required confirm token:

```text
APPLY_PROXY_RUNTIME_GUARD
```

It still does not:

- create the user;
- change nftables;
- start a service;
- open port `1443`;
- change routing;
- move users;
- render a public runtime profile.

Admin API endpoint:

```text
POST /api/actions/proxy-runtime-guard-apply-preview
```

Role:

```text
viewer
```

## Proxy Runtime Guard Apply

Added guarded apply:

```bash
v7-proxy-runtime-guard-apply \
  --inbound-id happ-test \
  --runtime-user v7proxy \
  --confirm APPLY_PROXY_RUNTIME_GUARD
```

This is the first live prerequisite for future public proxy/happ ingress.

It does:

- run the preview first and refuse to continue if preview is not `OK`;
- create a locked system user `v7proxy` if missing;
- backup the current nft ruleset;
- add nft `output` rules for the proxy runtime user:
  - allow approved egress interfaces;
  - drop direct public-interface output;
  - drop every other non-approved output;
- verify the guard after apply;
- write an audit event.

It still does not:

- start a service;
- open port `1443`;
- change routing;
- move users;
- change the runtime profile;
- add direct/DIRECT_RU proxy behavior.

Rollback command:

```bash
v7-proxy-runtime-guard-rollback \
  --backup-dir /root/v7-install-backups/proxy-runtime-guard-happ-test-YYYYMMDD-HHMMSS \
  --confirm ROLLBACK_PROXY_RUNTIME_GUARD
```

Admin API endpoints:

```text
POST /api/actions/proxy-runtime-guard-apply
POST /api/actions/proxy-runtime-guard-rollback
```

Role:

```text
owner
```

## Proxy Public Candidate Preview

Added read-only public runtime candidate preview:

```bash
v7-proxy-public-candidate-preview \
  --inbound-id happ-test \
  --runtime-user v7proxy \
  --public-listen 0.0.0.0
```

It builds a temporary sing-box config with:

- public listen address preview;
- existing authenticated users;
- `user -> egress interface` rules;
- direct outbounds bound to approved egress interfaces;
- final route action `block`.

It validates the candidate with:

```bash
sing-box check -c <temporary-candidate>
```

It still does not:

- write the runtime profile;
- start sing-box;
- open a public port;
- change nftables;
- change routing;
- move users.

Admin API endpoint:

```text
POST /api/actions/proxy-public-candidate-preview
```

Role:

```text
viewer
```

## Proxy Public Candidate Render

Added guarded render for the public candidate profile:

```bash
v7-proxy-public-candidate-render \
  --inbound-id happ-test \
  --runtime-user v7proxy \
  --public-listen 0.0.0.0 \
  --confirm RENDER_PROXY_PUBLIC_CANDIDATE
```

It writes:

```text
/etc/v7/inbound-runtime/happ-test/public-candidate/sing-box.json
/etc/v7/inbound-runtime/happ-test/public-candidate/metadata.json
```

It keeps the current loopback runtime untouched:

```text
/etc/v7/inbound-runtime/happ-test/sing-box.json
```

It still does not:

- start sing-box;
- open port `1443`;
- change nftables;
- change routing;
- move users.

Admin API endpoint:

```text
POST /api/actions/proxy-public-candidate-render
```

Role:

```text
owner
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
V7_PROXY_KILLSWITCH_GUARD_DRY_RUN=OK
allowed_egress_interfaces=awg2
required_before_live=create_runtime_user:v7proxy,add_nft_output_skuid_guard,add_nft_output_allow_rules_for_proxy_runtime_user,add_nft_output_drop_public_rule_for_proxy_runtime_user
V7_PROXY_PUBLIC_ENABLE_GUARD_DRY_RUN=BLOCKED
V7_PROXY_SERVICE_AWARE_ROUTING_DRY_RUN=OK
candidate_sing_box_check=OK
blocked_classes=DIRECT_RU,TRUSTED_RU_SENSITIVE
V7_PROXY_GUARDED_APPLY_DESIGN=OK
apply_phases=apply_runtime_user,apply_nft_output_guard,render_guarded_public_candidate,public_port_canary,operator_enable_action
V7_PROXY_RUNTIME_GUARD_APPLY_PREVIEW=OK
confirm_required=APPLY_PROXY_RUNTIME_GUARD
V7_PROXY_RUNTIME_GUARD_APPLY=OK
runtime_user_created=yes
proxy_output_guard_present=yes
V7_PROXY_PUBLIC_ENABLE_GUARD_DRY_RUN=READY
V7_PROXY_PUBLIC_CANDIDATE_PREVIEW=OK
candidate_sing_box_check=OK
V7_PROXY_PUBLIC_CANDIDATE_RENDER=OK
service_started=no
port_opened=no
live_enable=BLOCKED
tcp_1443_listener=none
V7_RESULT=OK
```

## Next Step

After public candidate render exists:

1. run a bounded public port canary from the candidate profile;
2. verify auth, egress binding, no direct leak, and cleanup;
3. then create final operator enable action;
4. only then expose Happ subscription generation.
