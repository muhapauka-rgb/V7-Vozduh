# P2.6 Retention Model

## Result

retention_model_defined=true

## Model

P2.6 introduces no persistent candidate JSONL growth.

Candidate store is derived from retained sources:

- proposal store;
- evidence store;
- contract draft preview;
- execution preview state;
- P2.5 simulation previews.

## Alignment With P2.5

Candidate timeline events are derived summary views. If future P2 stages persist candidate events, they must follow P2.5 retention requirements:

- rotate JSONL stores;
- compact resolved events;
- preserve unresolved reviews;
- preserve active emergencies;
- preserve latest authority state;
- keep audit lineage provable.

## Safe Cleanup

P2.6 performs no cleanup, compaction, archive write, or deletion.
