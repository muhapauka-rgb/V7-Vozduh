# P2.5 Blast Radius Preview

## Result

blast_radius_preview_implemented=true

## Output

Blast radius preview shows:

- users affected;
- groups affected;
- channels affected;
- services affected;
- capacity affected;
- policy affected;
- routing domains affected;
- risk categories.

## API

`GET /api/execution/blast-radius`

## Boundary

The preview only reads contract draft scope, users registry-derived metadata, capacity adapter output, and service impact output.
