# V7 Phase 8 Adaptive Autoswitch Hooks

## Purpose

Autoswitch may use intelligence as a bounded modifier, never as black-box authority.

## Allowed Hooks

- degradation prediction increases confidence;
- historical survivability reduces or increases confidence;
- transport reliability adjusts candidate ranking;
- stealth capability marks a candidate eligible for scoped fallback;
- overload prediction blocks target selection.

## Required Gates

Autoswitch still requires:

- route class compatibility;
- policy compatibility;
- kill switch compatibility;
- target not quarantined;
- target not maintenance;
- bounded move count;
- cooldown/freeze checks;
- audit and explanation.

## Forbidden Hooks

- AI-only migration;
- mass user movement from forecast alone;
- ignoring route classes;
- silent stealth escalation;
- fallback to unsafe direct path.

