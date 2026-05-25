# V7 Phase 1 - Kill Switch Hardening Model

## Purpose

Kill switch is a platform invariant, not a feature. Phase 1 hardening focuses on verification and documentation first.

No Phase 1 change may allow VPN client traffic to silently leak through the public interface.

## Protected Client Subnets

The following VPN client ranges are safety-critical:

- `10.0.0.0/24`
- `10.7.0.0/22`

These subnets must not reach the public interface directly unless traffic is explicitly marked and routed through the controlled direct/RU exception path.

## Runtime Surfaces

Kill switch safety depends on:

- nftables table `inet v7`;
- client source subnet sets;
- forward chain policy;
- direct/RU allow sets;
- DNS capture rules;
- fwmark-based policy routing;
- NAT rules for valid egress;
- MSS clamp where required by transport/runtime.

## Direct Exception Boundary

Direct routing is allowed only as a controlled exception.

Expected direct path properties:

- fwmark is explicit;
- direct mark is isolated from general VPN traffic;
- table `70` is used for direct exception routing;
- direct table default points to the expected public interface;
- direct DNS behavior is explicit;
- trusted RU failure becomes degraded/blocker, not silent unsafe fallback.

## Verification Requirements

The kill switch check must verify at minimum:

- nftables table exists;
- protected client subnets exist in nft sets or equivalent rules;
- forward path cannot leak protected subnets to public interface;
- direct mark rule exists only for controlled exception;
- direct table `70` is correct;
- NAT/MSS state exists for egress paths that need it;
- DNS capture is present for direct/RU policy when enabled;
- per-user table default routes match assigned egress.

Existing read-only checks:

- `hardening/v7-killswitch-check`
- `hardening/v7-provisioning-reconcile-check`

## Failure Handling

If kill switch verification fails:

1. mark routing safety as blocker;
2. do not infer that tunnel health is safe;
3. do not silently enable direct routing;
4. do not silently fallback trusted RU to global/public route;
5. show operator an exact bounded repair recommendation.

## Runtime Rebuild Safety

Kill switch rebuild is a dangerous action.

Required before rebuild:

- desired state parsed successfully;
- egress registry parsed successfully;
- public interface known;
- rollback context available;
- actor/reason captured.

Required after rebuild:

- run kill switch verification again;
- verify protected subnets;
- verify direct exception;
- verify per-user route table defaults;
- write audit event.

## Phase 1 Boundary

Phase 1 adds verification rules and safety model only. It does not change nftables behavior, route tables, or direct routing behavior.
