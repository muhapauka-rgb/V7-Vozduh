# E11.4 Fix Vs Waiver Decision

## Path A - Diagnose Semantics Fix

Required logic:

```text
if protocol=wireguard:
  use wg show <iface> for latest handshake
elif protocol=amneziawg/awg:
  use awg show <iface>
else:
  do not manufacture stale handshake for non-WireGuard transports
```

Additional requirements:

- preserve real hard-failure behavior;
- keep `SUSPECT` for truly missing/down interfaces;
- distinguish zero-user idle from a broken datapath;
- update repo-side source/lineage for `v7-egress-diagnose`;
- add fixture tests for `wg show` fresh, `wg show` stale, AWG fresh, missing handshake, and zero-user idle behavior;
- deploy in a separate bounded block with apply timer/control-plane protections unchanged;
- rerun target readiness after deploy.

Benefits:

- turns WireGuard into a clean target if live evidence remains good;
- removes the repeated waiver burden;
- aligns target readiness and autoswitch planner with real protocol semantics;
- reduces future false `SUSPECT` decisions for reserved zero-user WireGuard targets.

Risk:

- requires runtime policy/diagnose deploy in a future bounded mutation block;
- needs careful tests so real stale/down WireGuard remains blocked.

## Path B - Explicit Stale-Handshake Waiver

Waiver can be operationally acceptable only if all conditions are freshly true:

```text
target=wireguard-1779454504-c43409
scope=one_user_only
wireguard_zero_user=true
interface_up=true
live_wg_handshake_fresh=true
route_get_ok=true
quality_ok=true
exclusions_present=true
restore_settle_gate=GO
runtime_checks_ok=true
hidden_user_switch=false
hidden_routing_sync=false
rollback_clear=true
```

Not waived:

- kill-switch failure;
- reconcile failure;
- user-route failure;
- provisioning failure;
- interface down/missing;
- stale or missing live `wg show` handshake;
- target no longer zero-user;
- restore-settle gate not `GO`;
- any broad autoswitch movement pressure;
- rollback uncertainty.

Benefits:

- allows a faster second canary under explicit conditional governance.

Risk:

- leaves the underlying diagnose bug unresolved;
- canary remains `CONDITIONAL`, not clean `GO`;
- every future use needs fresh waiver evidence.

## Decision

```text
final_recommendation=FIX_FIRST
fix_required=true
waiver_acceptable=true
waiver_status=CONDITIONAL_FALLBACK_ONLY
best_strategy=FIX_FIRST_WITH_WAIVER_AS_FALLBACK
recommended_next_block=E11.5_BOUNDED_WIREGUARD_DIAGNOSE_SEMANTICS_FIX_PACKET
```

The waiver is acceptable as a fallback because the risk is control-plane attribution rather than proven datapath failure. It is not the best primary path because E11.4 identified a concrete diagnose semantics bug that can and should be fixed before declaring WireGuard a clean target.

