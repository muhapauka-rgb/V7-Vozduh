# V7 Phase 4 Degradation Persistence Logic

## Purpose

Transient spikes must not trigger routing movement. Autoswitch acts only when degradation is persistent enough to threaten user experience.

## Evidence Classes

Degradation evidence is grouped into:

- service evidence: service matrix failures, Telegram sentinel state, DNS/HTTPS failures;
- datapath evidence: route verification mismatch, MTU instability, packet loss;
- egress evidence: quality summary, failed runtime checks, load overload;
- client evidence: reconnect loops, unstable sessions, client-side throughput collapse;
- policy evidence: direct routing or trusted RU safety state.

## Persistence Requirements

A switch should generally require at least one of:

- sustained degradation over a configured window;
- repeated failures across multiple samples;
- multi-signal degradation affecting the same route class;
- high-severity safety issue with verified alternate path.

## Non-Switch Conditions

Autoswitch should avoid switching when:

- only one probe failed;
- latency changed slightly but service quality remains usable;
- evidence is stale;
- degradation is client-local and target egress would not help;
- route-class compatibility is unclear;
- alternate path is not verified.

## Severity Mapping

- warning: degradation observed but not persistent enough for movement;
- degraded: persistent quality loss with user impact;
- unstable: repeated quality changes or reconnect loops;
- blocked: service or route class unusable;
- safety_blocked: policy or kill switch rules prevent safe movement.

## Operator Output

The operator should see the compressed reason first:

`Telegram degraded for 42s; reconnects increased; alternate GLOBAL_STABLE path verified; confidence high.`

Raw samples belong only in drill-down diagnostics.

