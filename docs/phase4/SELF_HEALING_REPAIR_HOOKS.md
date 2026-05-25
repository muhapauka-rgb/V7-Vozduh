# V7 Phase 4 - Self-Healing Repair Hooks

## Purpose

Autoswitch may request repair, but must not become an uncontrolled repair engine.

## Allowed Hook Types

Autoswitch may:

- quarantine unstable egress;
- request reconcile;
- request repair;
- suggest maintenance;
- trigger safe restart when policy allows.

## Required Boundaries

Hooks must be:

- bounded;
- audited;
- verified;
- reversible where possible;
- explicit in operator summary.

## Forbidden Hooks

Autoswitch must not:

- silently rebuild nftables;
- silently bypass kill switch;
- silently enable unverified egress;
- silently direct-route trusted RU;
- perform mass migrations without confidence.

## Recommended Hook Flow

1. detect persistent issue;
2. classify repair type;
3. emit recommendation;
4. dry-run repair when available;
5. apply only through guarded tool;
6. verify datapath;
7. audit and update safety state.
