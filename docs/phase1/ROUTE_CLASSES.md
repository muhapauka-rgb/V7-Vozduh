# V7 Phase 1 - Route Classes

## Purpose

Route classes are the authoritative abstraction for routing intent. Transport names are implementation details.

Phase 1 minimum route classes:

- `GLOBAL_FAST`
- `GLOBAL_STABLE`
- `DIRECT_RU`
- `TRUSTED_RU_SENSITIVE`

Existing secondary classes can remain for compatibility, but they must not bypass these safety semantics.

## Global Rules

All route classes must be:

- deterministic;
- explainable;
- policy-driven;
- verifiable through runtime/effective checks;
- bounded by kill switch safety.

Route class selection must not silently override user/org policy.

## GLOBAL_FAST

Intent:

- default fast global access where stability and safety are verified.

Expected behavior:

- prefer healthy performant egress;
- avoid quarantined, blocked, overloaded, or maintenance egress;
- allow failover only when effective datapath remains policy-safe;
- do not chase transient latency spikes.

Allowed transports:

- any production-verified global transport supported by current registry and driver behavior.

Safety rules:

- no direct public leak;
- no unverified egress auto-enable;
- no silent migration to unsafe route.

## GLOBAL_STABLE

Intent:

- conservative global access for sensitive or degradation-prone services.

Expected behavior:

- prefer lower incident history and stable datapath over raw speed;
- tolerate moderate latency if packet path is safer;
- switch only on persistent degradation or blocker.

Allowed transports:

- verified transports with stable health history and working route verification.

Safety rules:

- anti-flapping must dominate speed optimization;
- mass migration requires high confidence;
- degraded state must be visible.

## DIRECT_RU

Intent:

- controlled direct/RU exception for explicitly allowed Russian/local destinations.

Expected behavior:

- use explicit fwmark and direct routing table;
- apply only to policy-approved destinations;
- keep VPN user subnet isolation intact;
- expose degraded/direct blockers clearly.

Allowed transports:

- direct path only when policy and kill switch allow it.

Safety rules:

- never behave as general bypass mode;
- never catch unmarked VPN traffic;
- never silently fallback sensitive routes through unsafe direct path.

## TRUSTED_RU_SENSITIVE

Intent:

- conservative handling for trusted Russian sensitive destinations where unsafe fallback is unacceptable.

Expected behavior:

- require explicit trusted policy;
- require verification of direct/RU path and DNS behavior;
- prefer degraded/blocker state over unsafe fallback.

Allowed transports:

- trusted direct/RU path only when verified;
- global fallback only when policy explicitly permits and safety is verified.

Safety rules:

- degradation must be surfaced;
- no silent downgrade to normal direct bypass;
- no policy bypass under failure.

## Failover Rules

General failover order:

1. keep current verified path if healthy;
2. degrade status if signals are uncertain;
3. switch only with persistent evidence and bounded impact;
4. verify effective datapath after switch;
5. audit risky action.

Forbidden failover:

- switching because one metric briefly improved;
- moving users to unverified egress;
- direct fallback for trusted routes without explicit policy;
- bypassing kill switch for recovery.

## Compatibility Notes

Older or secondary classes should be mapped to the four authoritative classes when used for safety decisions. Compatibility mapping must be explicit and documented before behavior changes.
