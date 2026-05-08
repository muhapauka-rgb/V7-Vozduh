# V7 Phase89 Egress Draft Preview Report

Date: 2026-05-08

## Goal

Start the egress onboarding wizard safely.

The first step must not add anything to the pool. It should only detect the config type, validate required fields, redact sensitive material, and tell the operator what the next safe step is.

## Changes

- Added Admin action:
  - `POST /api/actions/egress-config-preview`
- Added `Add Egress Draft` button in the Egress panel.
- Preview supports first-pass detection for:
  - WireGuard `.conf`
  - AmneziaWG `.conf`
  - sing-box JSON
  - VLESS / VMess / Trojan share links
  - Shadowsocks / Outline-like access keys
- Preview response never adds the draft to active pool.
- Preview does not persist the pasted config.
- Required sensitive fields are reported as present/missing without returning secret values.

## Live VPS Validation

Authenticated preview with a fake WireGuard config:

```text
protocol=wireguard
runtime_mode=interface
Interface.PrivateMaterial=present
Interface.Address=present
Peer.PublicKey=present
Peer.Endpoint=present
missing=[]
sensitive_material=yes
pool_action=draft_only_not_added
validation=detected_required_fields
```

## Safety Notes

- No egress was created.
- No config was saved.
- No service was started.
- No routing or nftables rules were changed.

