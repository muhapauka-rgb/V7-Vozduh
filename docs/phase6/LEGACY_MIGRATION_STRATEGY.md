# V7 Phase 6 Legacy Migration Strategy

## Purpose

The embedded admin must remain available until the extracted platform proves compatibility.

## Migration Stages

Stage 0: document boundaries and create scaffold.

Stage 1: extract read-only API client and design tokens.

Stage 2: build read-only overview against existing `/api/overview`.

Stage 3: build workflow pages without dangerous actions.

Stage 4: add safe action preview components.

Stage 5: add guarded apply components behind backend validation.

Stage 6: enable new UI behind feature flag.

Stage 7: preserve embedded admin fallback.

## Compatibility Requirements

- endpoint paths unchanged;
- JSON shapes unchanged or versioned;
- old admin path available;
- auth/session/CSRF unchanged;
- no datapath mutation from frontend migration.

## Rollback

Rollback must be simple:

- disable new UI route/feature flag;
- keep `/admin-v2` operational;
- keep backend executable path unchanged.

