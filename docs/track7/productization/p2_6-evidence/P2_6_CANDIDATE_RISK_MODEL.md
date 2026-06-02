# P2.6 Candidate Risk Model

## Result

candidate_risk_model_implemented=true

## Risk Categories

- Authority Risk
- Capacity Risk
- Trust Risk
- Readiness Risk
- Service Risk
- Blast Radius Risk
- Rollback Risk

## Current Derivation

Candidate risks are derived from:

- blocking gates;
- review gates;
- blast radius risk categories;
- service impact at-risk services;
- rollback impact state;
- missing proposal lineage.

## API

`GET /api/execution/candidates/risks`
