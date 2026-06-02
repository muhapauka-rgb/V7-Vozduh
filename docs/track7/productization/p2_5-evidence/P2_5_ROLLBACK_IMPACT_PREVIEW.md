# P2.5 Rollback Impact Preview

## Result

rollback_impact_preview_implemented=true

## Output

Rollback impact shows:

- rollback scope;
- rollback duration estimate;
- rollback risk;
- rollback confidence;
- rollback assumptions;
- rollback dependencies;
- embedded rollback preview.

## API

`GET /api/execution/rollback-impact`

## Boundary

Rollback impact is derived only. It does not prepare, trigger, or execute rollback.
