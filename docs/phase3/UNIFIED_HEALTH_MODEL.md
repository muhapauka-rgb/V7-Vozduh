# V7 Phase 3 - Unified Health Model

## Purpose

Phase 3 turns the Phase 1 health vocabulary into an observability contract across platform objects.

Health must explain state and impact. It must not become a metric dump.

## Health States

Minimum states:

- `healthy`;
- `degraded`;
- `unstable`;
- `recovering`;
- `blocked`;
- `overloaded`;
- `maintenance`;
- `quarantined`;
- `unknown`.

## Health Domains

Health must exist for:

- users;
- egress;
- route classes;
- services;
- datapaths;
- transports;
- trusted RU;
- autoswitch.

## Severity Projection

Every health state maps to operator severity:

- `blocker`: safety cannot be verified, no safe fallback, route leak risk, trusted RU unsafe fallback prevented;
- `critical`: user-impacting outage or route mismatch;
- `warning`: degraded but policy-safe;
- `info`: context, stale optional diagnostics, or planned maintenance;
- `ok`: verified healthy.

## Required Fields

Each health item should expose:

- object type;
- object id;
- health state;
- severity;
- reason;
- impact;
- suggested action;
- verification state;
- timestamp.

## Unknown Rule

Unknown is not healthy.

Unknown may be a warning or blocker depending on whether datapath safety is affected.

## Phase 3 Boundary

This model does not alter autoswitch or routing decisions. It defines a shared state language for diagnostics.
