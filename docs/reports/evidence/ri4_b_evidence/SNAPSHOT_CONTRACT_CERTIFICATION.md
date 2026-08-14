# Snapshot Contract Certification

## Extended Families

Added to `admin_core/intelligence_snapshots.py`:

| Family | File | Schema | Runtime requirement | Stale behavior |
|---|---|---|---|---|
| `candidate-suitability-summary` | `candidate-suitability-summary.json` | `v7.intelligence.candidate-suitability-summary.v1` | advisory_only | IGNORE |
| `best-available-pool` | `best-available-pool.json` | `v7.intelligence.best-available-pool.v1` | advisory_only | IGNORE |

Existing `user-service-scores` contract is now produced by workers.

## Compatibility

All new snapshots use the existing envelope:

- `schema`;
- `generated_at`;
- `expires_at`;
- `ttl_seconds`;
- `freshness_state`;
- `confidence`;
- `source_hashes`;
- `generator`;
- `item_count`;
- `warnings`;
- `items`.

No new snapshot root was created.

Canonical root remains:

```text
/opt/v7/egress/state/intelligence
```

## Runtime Compatibility

New RI4-B snapshots are advisory-only.

Low confidence behavior:

```text
candidate-suitability-summary LOW_CONFIDENCE=IGNORE
best-available-pool LOW_CONFIDENCE=IGNORE
```

Runtime STOP families remain unchanged:

- `risk-summaries`;
- `trust-summaries`;
- `blast-radius-summaries`.

## Certification

`tests.unit.test_intelligence_snapshots` verifies:

- families are registered;
- RI4-B advisory runtime families are exposed;
- stop matrix keeps new families advisory-only;
- worker recommendations do not mutate runtime state.

