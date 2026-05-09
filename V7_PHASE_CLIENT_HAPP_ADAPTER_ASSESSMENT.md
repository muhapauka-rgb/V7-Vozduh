# V7 Happ Client Adapter Assessment

Date: 2026-05-09

## Summary

Happ is not enabled as an automatic V7 user client yet.

Reason: current V7 user ingress is WireGuard. Happ documentation describes import support for proxy-style configurations and subscriptions:

- `vless://`
- `vmess://`
- `trojan://`
- `ss://`
- `socks://`
- standard subscription URL
- encrypted `happ://crypto...` subscription

That means Happ needs a V7-compatible proxy ingress or subscription endpoint before V7 can safely issue Happ profiles.

## Current Decision

Keep Happ visible in admin capability matrix, but mark it blocked:

- status: `blocked`
- blocker: `current_v7_user_inbound_is_wireguard`
- required V7 inbound: `VLESS or Trojan or Shadowsocks subscription endpoint on V7`
- delivery: `not_available`
- automatic generation: disabled

This avoids issuing a misleading profile that would not connect through the current V7 architecture.

## Why Karing/Hiddify Are Different

Karing and Hiddify can consume sing-box-style profiles that include a WireGuard endpoint to V7.

Happ is Xray/proxy-oriented, so a full V7 Happ adapter should be implemented as a separate phase:

1. Add a dedicated V7 proxy ingress, such as VLESS Reality or Trojan.
2. Bind it to the same V7 user identity/routing model.
3. Generate Happ-compatible subscription/share links.
4. Test that user traffic still enters V7 and follows V7 policy/failover.
5. Only then mark Happ as `ready`.

## Safe Next Step

Do not enable Happ profile generation until a tested V7 proxy ingress exists.

