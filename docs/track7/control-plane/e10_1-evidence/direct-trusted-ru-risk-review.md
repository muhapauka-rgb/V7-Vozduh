# E10.1 Direct/RU And Trusted RU Risk Review

Mode: read-only analysis only. No Direct/RU or Trusted RU mutation was performed.

## What The Missing Exclusions Mean

`tools/v7-second-canary-target-readiness` requires canary target egresses to carry:

```text
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

This metadata means the egress should not be considered a clean target for Direct/RU or Trusted RU sensitive route classes. It is a safety marker for target selection and policy-aware routing. It is not a domain-list mutation, not a Trusted RU diagnostic refresh, and not an nft/ip route change by itself.

## Direct/RU Exclusion

`DIRECT_RU` covers Russian direct-routing domains and resolved IP classes. Current evidence shows Direct/RU state exists and is active:

```text
/etc/v7/direct/domains.conf
/opt/v7/egress/state/direct-ru-autosync.state
/opt/v7/egress/state/route-classes.state
DIRECT_RU_domains=17
```

Adding `DIRECT_RU` to `awg0` exclusions would mean `awg0` should not be used as a canary target for Direct/RU route-class traffic. It does not remove domains, change dnsmasq, or alter route tables by itself.

## Trusted RU Sensitive Exclusion

`TRUSTED_RU_SENSITIVE` covers Gosuslugi/Alfabank/related sensitive routing decisions. Current evidence shows stale but relevant state:

```text
trusted-ru-diagnostic.updated=2026-05-22T23:36:03+03:00
trusted-ru-decision.updated=2026-05-07T20:18:37+03:00
trusted-ru-decision.overall=NEEDS_ATTENTION
trusted-ru-decision.route_class_status=NEEDS_TRUSTED_PATH
```

Adding `TRUSTED_RU_SENSITIVE` to `awg0` exclusions would prevent treating `awg0` as a clean target for Gosuslugi-sensitive canary semantics. It should reduce sensitive-route ambiguity, not expand it.

## Risk Questions

| Question | Answer |
|---|---|
| Would adding exclusions prevent Gosuslugi-sensitive routing through this egress? | It prevents `awg0` from being treated as eligible for `TRUSTED_RU_SENSITIVE` route-class selection by metadata-aware tooling. |
| Could exclusions accidentally break normal global routing? | Not for normal one-user global canary mechanics; `GLOBAL_STABLE/GLOBAL_FAST` are not excluded by this metadata. |
| Would exclusions affect current users? | No current users are on `awg0`; no user movement is part of E10.1. |
| Would exclusions affect only target readiness? | Immediately, yes for the checker. Downstream policy-aware tools may also avoid `awg0` for Direct/RU/Trusted RU classes. |
| Is this safe as metadata-only egress policy? | Yes, with separate bounded runtime approval and backup, because it narrows sensitive route eligibility. |
| Is policy apply needed for exclusions to take effect? | No policy apply is needed for target-readiness evaluation. A future registry metadata mutation would be enough for the readiness checker. |
| Would kill switch need re-check? | Yes after any future mutation, but kill-switch mutation is not expected; only read-only `v7-killswitch-check` should run. |

## Risk Classification

```text
direct_ru_risk=LOW_METADATA_EXCLUSION_ONLY
trusted_ru_risk=LOW_METADATA_EXCLUSION_ONLY_WITH_STALE_STATE_AWARENESS
kill_switch_risk=LOW_RECHECK_REQUIRED_AFTER_MUTATION
policy_apply_required=false
runtime_route_mutation_required=false
```

The main risk is operational: editing `egress.registry` is still runtime metadata mutation and must be done only in a bounded mutation block with backup and rollback.

