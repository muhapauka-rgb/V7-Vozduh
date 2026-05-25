# V7 Phase 8 Transport Intelligence Layer

## Purpose

V7 should understand transport behavior without making transport the product center.

Transport intelligence is metadata for explainable routing and diagnostics.

## Transport Signals

Track:

- stability;
- blockage;
- performance;
- reconnect quality;
- DPI sensitivity;
- MTU sensitivity;
- UDP/TCP behavior;
- mobile reconnect behavior;
- quarantine history;
- maintenance history.

## Transport Classes

Transport families may include:

- WireGuard;
- AmneziaWG;
- OpenVPN;
- VLESS;
- Hysteria2;
- TUIC;
- SOCKS;
- Shadowsocks;
- future proxy drivers.

## Decision Use

Transport intelligence may:

- explain why a channel is risky;
- rank diagnostics priority;
- influence recommendation confidence;
- support route forecasting;
- support adaptive stealth suggestions.

It must not:

- override route classes;
- override org policy;
- enable unverified channels;
- become protocol-centered UI.

