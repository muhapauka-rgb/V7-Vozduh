# V7 Vozduh - Non-Negotiables

Immutable Product, Routing, UX and Architecture Rules

This document is not a roadmap, feature list, or implementation plan.

It defines immutable architectural laws for V7 Vozduh.

If a change violates these laws, breaks the V7 philosophy, increases chaos, reduces predictability, reduces operator clarity, or weakens datapath safety, that change is forbidden even if it appears smart, powerful, modern, or technically attractive.

## Section A - Product Identity

### A1

V7 is not a VPN service.

V7 is:

- an internet access routing platform;
- a self-healing routing system;
- an anti-blocking access orchestrator.

### A2

VPN, WireGuard, AmneziaWG, VLESS, OpenVPN, and similar protocols are transport layer components only.

They are not the center of the product.

### A3

The primary goal of V7 is:

- stable internet access;
- minimal user friction;
- minimal operator firefighting.

### A4

The user must not be required to:

- understand routes;
- choose transports;
- diagnose channels;
- manually search for working servers.

### A5

The operator must be able to:

- observe;
- understand state;
- make bounded decisions.

The operator must not be forced to:

- constantly SSH-debug the platform;
- manually repair routing;
- manually rebalance users every hour.

## Section B - Routing And Safety

### B1

The kill switch is a mandatory foundation of the platform.

### B2

VPN traffic must never silently leak directly through the public interface.

### B3

Direct routing is only a controlled exception.

It is not bypass mode.

### B4

Routing must be:

- deterministic;
- explainable;
- verifiable.

### B5

The system must never:

- silently bypass policy;
- silently reroute traffic;
- silently disable protections.

### B6

Route classes are the authoritative routing abstraction.

Routing decisions must respect:

- `GLOBAL_FAST`;
- `GLOBAL_STABLE`;
- `DIRECT_RU`;
- `TRUSTED_RU_SENSITIVE`.

### B7

Trusted RU degradation must not silently fall back to unsafe routing.

### B8

Runtime state and UI state must not silently diverge.

## Section C - Autoswitch

### C1

Autoswitch is not a fastest-route optimizer.

Autoswitch is a stability preservation system.

### C2

Autoswitch must never:

- flap;
- oscillate users;
- panic-switch;
- endlessly chase latency.

### C3

Autoswitch must not react to transient spikes.

### C4

Mass user migration without high confidence is forbidden.

### C5

All switch decisions must be:

- explainable;
- auditable;
- bounded;
- reversible.

### C6

Stability is always more important than theoretical optimization.

## Section D - Observability

### D1

Observability is not a telemetry dump.

### D2

The operator must see:

- state;
- impact;
- causes;
- suggested actions.

The operator must not be shown endless raw metrics as the primary experience.

### D3

Diagnostics must be:

- grouped;
- contextual;
- compressed;
- progressively disclosed.

### D4

Alert spam is forbidden.

### D5

The system must not:

- silently degrade;
- silently fail;
- silently mismatch datapaths.

## Section E - UI And UX

### E1

The main UX philosophy is calm operator UX.

### E2

The UI must not:

- overload;
- make noise;
- blink unnecessarily;
- look like an engineering cockpit;
- look like a Grafana clone.

### E3

The interface must:

- hide complexity;
- show summary first;
- use progressive disclosure.

### E4

Giant dashboards are forbidden.

### E5

Metric walls are forbidden.

### E6

Topology spaghetti is forbidden.

### E7

Complex diagnostics must live in drill-down views only.

### E8

Every new feature must pass information architecture review and must not increase cognitive overload.

## Section F - Architecture

### F1

Rewrite-from-scratch behavior is forbidden.

### F2

The system must:

- stabilize;
- formalize;
- modularize gradually.

### F3

Backward compatibility is a priority.

### F4

Dangerous changes must be:

- reversible;
- bounded;
- auditable.

### F5

Incremental migration is always preferable to a giant rewrite.

### F6

Overengineering is forbidden.

### F7

Premature distributed complexity is forbidden.

### F8

Kubernetes for enterprise aesthetics is forbidden.

## Section G - Provisioning

### G1

A new egress must never instantly become production-active.

### G2

Provisioning must be:

- staged;
- quarantine-first;
- rollback-safe;
- runtime-verified.

### G3

Unverified routing changes are forbidden.

### G4

Unsafe auto-enable is forbidden.

### G5

Provisioning must not:

- silently modify datapath;
- silently override policies.

## Section H - AI And Intelligence

### H1

AI or intelligence must not become a black-box routing engine.

### H2

AI must not:

- silently reroute users;
- disable protections;
- override route classes;
- bypass policy;
- bypass the kill switch.

### H3

AI and intelligence may:

- recommend;
- forecast;
- explain;
- prioritize diagnostics.

### H4

The routing core must remain:

- deterministic;
- explainable;
- bounded.

### H5

Adaptive stealth must be:

- situational;
- bounded;
- performance-aware.

It must not be always-on heavy obfuscation.

## Section I - Operational Safety

### I1

All dangerous actions must:

- be logged;
- have an actor;
- have a reason;
- have rollback context.

### I2

System state must be:

- observable;
- verifiable;
- reconcilable.

### I3

The operator must always understand:

- what is happening;
- why it is happening;
- how serious it is;
- what to do.

### I4

The system must not depend on:

- administrator memory;
- undocumented tribal knowledge.

## Section J - Complexity Control

### J1

Every change must:

- reduce chaos;
- improve clarity;
- strengthen predictability.

### J2

Feature sprawl is forbidden.

### J3

Smartness for its own sake is forbidden.

### J4

The system must not become:

- harder to reason about;
- impossible to debug;
- opaque.

### J5

Complexity must be hidden inside the platform, not transferred to the operator or user.

## Final Non-Negotiable

If a solution worsens stability, datapath safety, predictability, operator clarity, calm UX, or creates hidden behavior, that solution is forbidden even if it seems technically advanced.

