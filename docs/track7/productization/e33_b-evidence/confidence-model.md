# E33.B Confidence Model

confidence_model_defined=true

## Confidence Levels

| Level | Meaning | Allowed Output |
| --- | --- | --- |
| LOW | Evidence missing, stale, contradictory, or single-sample only. | OBSERVE or REVIEW_REQUIRED. |
| MEDIUM | Evidence is recent but limited, or improvement is plausible with some uncertainty. | REVIEW_REQUIRED, OBSERVATION, or low-risk proposal requiring operator review. |
| HIGH | Recent repeated evidence supports current degradation and candidate improvement. | Proposal may enter governance path. |
| VERY_HIGH | Multiple fresh evidence sources agree, prior history supports target, and no safety conflicts exist. | Proposal may enter governance path with lower review burden, still no direct execution. |

## Inputs

Confidence is derived from:

- service health freshness;
- required_services completeness;
- current target quality;
- candidate target quality;
- degradation evidence count;
- repeated observations;
- operator feedback;
- incident history;
- flapping history;
- rollback certainty;
- governance path completeness.

## Confidence Computation Model

Start from LOW.

Increase confidence when:

- all required_services are known and fresh;
- current degradation repeats across samples;
- candidate target is user-specific OK;
- service affinity is positive and fresh;
- no unresolved incidents exist;
- rollback manifest is deterministic;
- governance path is complete.

Decrease confidence when:

- any required service is UNKNOWN;
- service evidence is stale;
- target quality is stale or noisy;
- incident history is unresolved;
- flapping risk is present;
- proposed blast radius is larger than recent certified practice;
- operator feedback conflicts with telemetry.

## Minimum Confidence Rules

- MOVEMENT_PROPOSAL requires HIGH unless human review is mandatory.
- EVACUATION_PROPOSAL may be MEDIUM when current target is failing, but must require human review if candidate evidence is incomplete.
- REBALANCE_PROPOSAL requires HIGH or VERY_HIGH.
- OBSERVE is the correct output for LOW confidence.

## Product Decision Required

```text
ARCHITECTURE_DECISION_REQUIRED:
decision_needed=exact_confidence_scoring_formula
options=weighted_numeric_score, rule_based_level, hybrid_score_plus_rules
pros=weighted score is tunable; rule model is auditable; hybrid balances both
cons=weighted score can hide safety issues; rule model can be rigid; hybrid needs careful documentation
recommended_option=hybrid_score_plus_rules
```

confidence_model_defined=true
