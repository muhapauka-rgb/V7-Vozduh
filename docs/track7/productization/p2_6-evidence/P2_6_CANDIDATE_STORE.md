# P2.6 Candidate Store

## Result

candidate_store_implemented=true

## Store Type

P2.6 implements a derived candidate store.

Source of truth:

- Proposal Store;
- Evidence Store references;
- Contract Draft preview;
- Validation, Simulation, Forecast read models.

## Candidate Event Store

Candidate events are derived timeline rows:

- CANDIDATE_DERIVED
- CANDIDATE_VALIDATED_PREVIEW
- CANDIDATE_SIMULATED_PREVIEW
- CANDIDATE_READINESS_PREVIEW

## Retention

No new infinite JSONL store is introduced. Retention aligns with P2.5 log retention architecture.
