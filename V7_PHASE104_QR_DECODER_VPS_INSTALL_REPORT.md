# V7 Phase 104 — QR Decoder Installed On VPS

Date: 2026-05-08

## What Was Done

Installed local QR decoding support on the VPS for the Add Egress wizard.

Package installed:

```text
zbar-tools
```

Runtime tool:

```text
/usr/bin/zbarimg
```

## Why

The admin UI and backend endpoint already support QR upload preview. Without a local decoder, the endpoint safely returns `DECODER_MISSING`.

After installing `zbar-tools`, QR images can be decoded locally on the V7 server. No external QR decoding service is used.

## Safety

- QR upload remains preview-only.
- QR does not create a draft automatically.
- QR does not add a channel to the pool.
- QR does not enable a channel.
- Decoded secret text is not returned to the UI.
- The operator still needs to proceed through the staged onboarding flow.

## Verification

On the VPS:

```bash
command -v zbarimg
curl -fsS http://127.0.0.1:7080/health
```

Observed:

```text
/usr/bin/zbarimg
admin health: OK
```
