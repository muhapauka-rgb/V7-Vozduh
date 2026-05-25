# V7 Vozduh - Master Governance

Global Architecture, Product and Development Governance

This document is not a feature request, roadmap, or implementation task.

It is the global constitution of the V7 Vozduh project.

All architecture, product, UI, routing, and development decisions must comply with this document.

If a change contradicts governance, adds unnecessary complexity, breaks the V7 philosophy, or creates chaos, that change is wrong even if it appears technically smart.

## 1. Product Identity

V7 is not a VPN service.

V7 is:

- an internet access routing platform;
- a self-healing routing system;
- an anti-blocking internet access orchestrator.

VPN, WireGuard, AmneziaWG, VLESS, OpenVPN, and similar protocols are transport layer components only.

The main task of V7 is to:

- preserve stable internet access;
- hide routing complexity;
- adapt automatically to degradation;
- minimize operator firefighting.

## 2. Core Product Philosophy

The main priorities of V7 are:

1. stability;
2. speed;
3. datapath safety;
4. explainability;
5. observability;
6. adaptive stealth.

V7 must not optimize for:

- maximum obfuscation at any cost;
- endless protocol experimentation;
- feature overload.

## 3. User Experience Philosophy

The user must not be required to:

- understand routes;
- choose transports;
- analyze channels;
- manually search for working servers;
- understand networking.

For the user, the internet should simply work.

## 4. Operator Philosophy

The operator must be able to:

- observe;
- understand state;
- see degradations;
- make bounded decisions.

The operator must not be forced to:

- manually firefight everything;
- constantly repair routing;
- SSH-debug every incident;
- constantly rebalance users by hand.

The main operational goal of V7 is to automate operator routine.

## 5. Core Architectural Principles

V7 must remain:

- deterministic;
- observable;
- explainable;
- reconciliation-first;
- rollback-safe;
- staged;
- bounded;
- modularizing incrementally.

V7 must not become:

- chaotic;
- magical;
- opaque;
- overengineered;
- rewrite-driven.

## 6. Datapath Principles

Datapath is the foundation of the platform.

The main datapath principles are:

- deterministic routing;
- verifiable routing;
- mandatory kill switch;
- no silent leaks;
- no hidden routing;
- explicit route classes;
- controlled direct routing.

VPN subnets must not:

- accidentally bypass routing;
- directly leak to the public interface.

## 7. Kill Switch Governance

The kill switch is not a feature.

It is a fundamental invariant.

It is forbidden to:

- bypass the kill switch;
- disable safety silently;
- allow unsafe direct routing;
- enable unverified egress.

All routing changes must preserve no-leak guarantees.

## 8. Route Class Governance

Route classes are the authoritative routing abstraction.

The minimum route classes are:

- `GLOBAL_FAST`;
- `GLOBAL_STABLE`;
- `DIRECT_RU`;
- `TRUSTED_RU_SENSITIVE`.

Routing decisions must:

- respect route classes;
- be explainable;
- be policy-driven.

## 9. Autoswitch Governance

Autoswitch is not a fastest route selector.

Autoswitch is a stability preservation engine.

Autoswitch must not:

- flap;
- oscillate users;
- aggressively chase lower latency;
- mass-switch users;
- react to transient spikes.

Autoswitch must be:

- cautious;
- confidence-based;
- bounded;
- explainable;
- degradation-aware.

## 10. Observability Governance

Observability is not a telemetry dump.

The goal of observability is to:

- explain problems;
- reduce chaos;
- help the operator;
- show impact.

The system must not create:

- giant metric dashboards;
- noisy telemetry overload;
- engineering cockpit chaos.

## 11. UI/UX Governance

The main interface philosophy is calm operator UX.

The UI must be:

- calm;
- minimal;
- low-noise;
- summary-first;
- based on progressive disclosure.

The interface must not:

- show everything at once;
- overload the operator;
- look like a NOC or Grafana clone;
- create anxiety.

## 12. Information Architecture Principles

The information hierarchy must be:

1. state;
2. impact;
3. incidents;
4. grouped diagnostics;
5. deep telemetry.

It must not be the reverse.

## 13. Complexity Governance

V7 must not:

- grow uncontrollably;
- become a spaghetti platform;
- become a collection of unrelated features.

Every change must:

- reduce chaos;
- increase clarity;
- preserve architecture boundaries.

## 14. Modularization Principles

Monolith separation must be:

- gradual;
- compatibility-first;
- behavior-preserving.

It is forbidden to:

- perform giant rewrites;
- behave as if rewriting from scratch;
- break runtime compatibility.

## 15. Provisioning Governance

Provisioning must be:

- staged;
- quarantine-first;
- rollback-safe;
- runtime-verified;
- deterministic.

It is forbidden to:

- instantly production-enable unknown egress;
- silently modify routing;
- skip runtime verification.

## 16. Driver Governance

Protocols are drivers.

WireGuard, AmneziaWG, OpenVPN, VLESS, and similar transports must not create chaotic architecture branching.

Each transport must be:

- capability-based;
- bounded;
- explainable.

## 17. Stealth Governance

Stealth must be adaptive.

It must not be always-on heavy obfuscation.

The goal is to:

- preserve speed and stability;
- increase stealth only when needed.

## 18. AI And Intelligence Governance

AI and intelligence must not:

- silently reroute users;
- override policy;
- disable safeguards;
- become a black-box routing engine.

AI and intelligence may:

- recommend;
- explain;
- forecast;
- prioritize diagnostics.

The routing core must remain:

- deterministic;
- explainable;
- bounded.

## 19. Scaling Governance

Scaling must be:

- incremental;
- operationally safe;
- observable.

It is forbidden to introduce:

- premature Kubernetes;
- distributed complexity for fashion;
- overengineering.

## 20. Infrastructure Governance

Infrastructure must:

- survive failures;
- survive restart;
- survive degraded channels;
- support rollback;
- support reconciliation.

## 21. Development Governance

Any Codex work must follow this sequence:

1. Inspect.
2. Analyze.
3. Explain findings.
4. Propose bounded changes.
5. Apply a minimal safe patch.
6. Verify runtime safety.
7. Report exact results.

It is forbidden to introduce:

- giant uncontrolled rewrites;
- hidden behavior changes;
- runtime-breaking changes;
- silent architectural drift.

## 22. Safe Change Principles

Every change must be:

- bounded;
- reversible;
- observable;
- auditable;
- explainable;
- minimally invasive.

## 23. Auditability Principles

All dangerous actions must include:

- actor;
- reason;
- before and after state;
- timestamp;
- rollback context.

## 24. Future-Proofing Principles

V7 must:

- preserve simplicity;
- preserve operator clarity;
- hide complexity;
- modularize gradually;
- avoid feature sprawl.

## 25. Non-Negotiables

Never violate:

- no silent traffic leaks;
- no unsafe direct routing;
- no kill switch bypass;
- no chaotic autoswitch;
- no giant noisy dashboards;
- no hidden routing behavior;
- no black-box routing AI;
- no rewrite-from-scratch chaos;
- no uncontrolled complexity growth.

## 26. Global V7 Principle

V7 must:

- make complex routing invisible;
- preserve stable internet;
- reduce operator burden;
- be self-healing;
- be predictable;
- be trustworthy.

V7 must not become a magical VPN machine.

## 27. Final Governance Rule

If a solution makes the platform less understandable, increases chaos, worsens predictability, reduces operator clarity, violates calm UX, or breaks deterministic routing, that solution is wrong even if it seems technically powerful.

