# P3.C Retention

Project: V7 Vozduh
Block: P3.C First Runtime Dry-Run

## Retention Model

P3.C uses derived-on-demand reports.

- No persistent dry-run store.
- No copied source payloads.
- No infinite JSONL.
- No hook-local queue.
- Source refs and hashes only.
- Report expiry is included.
- Retention class: `P3C_DERIVED_PREVIEW`.

## Verdict

`retention_safe=true`

