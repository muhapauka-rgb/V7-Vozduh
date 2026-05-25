# V7 Phase 1 - Unified Health Model

## Purpose

V7 needs one shared health language for routing, observability, autoswitch, provisioning, and operator UX.

Health must explain platform state without becoming a noisy metric dump.

## Health States

### healthy

Meaning:

- desired, runtime, observed, and effective state agree;
- datapath verifies against policy;
- no active safety warning.

Operator view:

- show as normal summary state.

### degraded

Meaning:

- service or egress works but has measurable quality or consistency issues;
- safety is not violated;
- operator should know impact.

Examples:

- latency drift;
- packet loss trend;
- stale quality summary;
- partial service instability.

### unstable

Meaning:

- repeated failures or oscillation risk;
- autoswitch must be cautious;
- user impact may be intermittent.

Examples:

- reconnect spikes;
- flapping interface;
- inconsistent service matrix results.

### blocked

Meaning:

- service/egress/route class cannot currently satisfy policy;
- routing may be unavailable or unsafe for that target.

Examples:

- trusted RU path unavailable with no safe fallback;
- kill switch verification failure;
- route table points to wrong egress.

### quarantined

Meaning:

- egress or route is intentionally excluded from production use;
- it may be observed or tested but not silently assigned to users.

Examples:

- new egress after provisioning;
- failed verification;
- unstable egress removed from autoswitch pool.

### overloaded

Meaning:

- resource pressure creates user-impact risk;
- routing may still be safe but performance/stability is reduced.

Examples:

- bandwidth saturation;
- high active users;
- CPU pressure affecting transport.

### maintenance

Meaning:

- operator or platform intentionally removed component from normal service.

Rules:

- autoswitch must not assign new users to maintenance egress;
- UI must make intentional state clear.

### recovering

Meaning:

- component is returning from degraded/blocked/quarantined state;
- verification is in progress or grace period applies.

Rules:

- no panic migration back;
- require stability window before healthy.

### unknown

Meaning:

- state cannot be verified.

Rules:

- unknown must not be shown as healthy;
- unknown can be warning or blocker depending on datapath safety.

## Inputs

Health can use:

- registry desired state;
- Linux runtime;
- route verification;
- service matrix;
- egress quality summary;
- autoswitch safety file;
- direct/RU diagnostics;
- systemd/process status;
- audit and recent repair events.

## Severity Projection

Health state should project to operator severity:

- blocker: unsafe or unverifiable datapath;
- critical: user-impacting mismatch;
- warning: degraded but safe;
- info: context or stale optional diagnostics.

## Autoswitch Guidance

Autoswitch may act on:

- persistent `blocked`;
- persistent `unstable`;
- verified `quarantined` exclusion;
- sustained degradation with confidence.

Autoswitch must not act on:

- one transient spike;
- unknown state without safety classification;
- noisy optional metric;
- unverified direct/RU fallback.

## UI Guidance

Show:

- overall health summary;
- impacted users/egresses;
- cause group;
- suggested bounded action.

Hide until drill-down:

- raw metric walls;
- full command output;
- per-rule dumps;
- long diagnostic tables.

## Phase 1 Boundary

This model standardizes terminology. It does not change health computations or autoswitch behavior by itself.
