# E35.0.1 Autonomy Impact Review

## Scope

Audit question: if E35 autonomous execution started today, what would it inherit.

autonomy_impact_assessed=true

## What Is Safe to Inherit

Safe building blocks:

- hard-gate-before-score candidate model
- explicit blocked reasons
- required service matrix integration
- Telegram hard/degraded distinction
- speed and stability floors
- group allow/exclude/exclusive checks
- capacity hard limits and projected capacity selection
- anti-flap, quarantine, blocked-target and pair-reversal safety
- current-channel sticky threshold
- bounded move type limits
- read-only plan generation

## What Is Dangerous to Inherit Blindly

Risk areas:

- multiple channel-selection paths exist and are not unified.
- proposal logic is not the same as autoswitch hard-gate logic.
- admin required-service expectations may imply guarantee, while enforcement is not centralized.
- default required services may apply when per-user preferences are missing.
- ChatGPT/Claude are known services, but no special business semantics beyond normal service handling were found.
- group/org constraints exist in autoswitch/org policy but are not yet a single product-level contract across all flows.
- current channel persistence is not the same as explicit pinning.
- service-aware route apply can mutate route-class registry when explicitly confirmed; it is separate from per-user movement.

## What Should Change Before E35 Autonomy

recommended_changes_before_e35:

1. Centralize suitability into one reusable evaluator used by proposals, approval packets, execution-time recheck, autoswitch, and admin preview.
2. Make required-service guarantee explicit: advisory, hard gate, or execution precondition.
3. Add explicit per-user routing control mode: AUTO / PINNED / MANUAL.
4. Separate current channel from preferred/pinned channel.
5. Define group/org constraints as authoritative or advisory, not mixed.
6. Expose hard vs soft suitability reasons in admin before any autonomous decision.
7. Require execution-time recheck to recompute the same suitability verdict.
8. Ensure proposal ranking and autoswitch ranking cannot disagree silently.

## Audit Verdict

autonomy_can_reuse_current_selector=true
autonomy_should_not_execute_directly_on_current_selector_without_unification=true
e35_requires_suitability_contract=true
