# V7 Phase 2 - Driver Model

## Purpose

Protocols are drivers. They must not create chaotic branching in provisioning, routing, UI, or autoswitch.

Drivers describe capabilities and hooks. Routing policy remains authoritative.

## Supported Driver Families

Phase 2 model covers:

- WireGuard;
- AmneziaWG;
- OpenVPN;
- VLESS;
- Hysteria2;
- TUIC;
- SOCKS;
- Shadowsocks;
- future transports.

Current runtime code already groups drivers into:

- interface-backed egress: WireGuard, AmneziaWG, OpenVPN;
- proxy/sing-box egress: VLESS, VMess, Trojan, Shadowsocks/Outline, Hysteria/Hysteria2, TUIC, AnyTLS, SOCKS, HTTP, wireguard URI wrappers;
- container sources: subscriptions, Xray JSON, Clash YAML, provider bundles that must produce one concrete managed outbound.

## Driver Contract

Every driver must define:

- `id`;
- `protocol_aliases`;
- `runtime_mode`;
- `capabilities`;
- `required_tools`;
- `config_normalizer`;
- `static_validator`;
- `runtime_test_hook`;
- `quarantine_hook`;
- `runtime_profile_writer`;
- `enable_guard`;
- `health_hook`;
- `cleanup_hook`;

## Capability Model

Capabilities are descriptive. They do not bypass route classes.

Common capabilities:

- `supports_direct`;
- `supports_trusted_ru`;
- `supports_stealth`;
- `supports_high_bandwidth`;
- `supports_low_latency`;
- `supports_udp`;
- `supports_tcp_fallback`;
- `supports_mobile_clients`;
- `supports_fast_reconnect`;
- `supports_temporary_runtime`;
- `supports_interface_runtime`;
- `supports_proxy_runtime`;

## Runtime Requirements

### WireGuard

Required:

- `wg`;
- `wg-quick`;
- `ip`;
- `curl`.

Provisioning constraints:

- runtime copy must be V7-managed;
- `Table = off` is required in managed runtime;
- hooks are forbidden;
- DNS must remain under V7 control.

### AmneziaWG

Required:

- `awg`;
- `awg-quick` or compatible runtime;
- `ip`;
- `curl`.

Provisioning constraints:

- preserve AmneziaWG obfuscation options;
- normalize routing ownership to V7;
- hooks are forbidden.

### OpenVPN

Required:

- `openvpn`;
- `curl`;
- optional `systemd` unit `v7-egress-openvpn@.service`.

Provisioning constraints:

- force V7-managed interface;
- force `route-nopull`;
- block executable hooks;
- ignore pushed DNS;
- keep routing under V7 control.

### Sing-box Proxy Drivers

Drivers:

- VLESS;
- VMess;
- Trojan;
- Shadowsocks/Outline;
- Hysteria/Hysteria2;
- TUIC;
- AnyTLS;
- SOCKS;
- HTTP.

Required:

- `sing-box`;
- `curl`.

Provisioning constraints:

- run isolated local profile for tests;
- do not mutate current sing-box service;
- only one selected outbound becomes a managed egress.

## Validation Hooks

Driver validation must answer:

- can the source be parsed;
- are secrets present and safely stored;
- can runtime config be normalized;
- are unsafe hooks absent;
- can temporary runtime test run;
- can quarantine service matrix pass;
- can cleanup be verified.

## Health Hooks

Driver health should produce common signals:

- interface/process alive;
- external IP reachable;
- service matrix pass;
- packet loss/reconnect trends when available;
- MTU/MSS warnings;
- restart frequency;
- cleanup failures.

## Phase 2 Boundary

This document describes the future driver contract. It does not refactor current protocol code into separate modules.
