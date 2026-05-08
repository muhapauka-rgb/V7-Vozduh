# V7 Phase 103-105 — Service-Aware Onboarding, QR Preview, Result Cards

Date: 2026-05-08

## What Changed

This step continues the safe egress onboarding flow after roles and usage policy.

It adds:

- broader service matrix coverage;
- route-class fitness summaries;
- QR upload preview endpoint/UI;
- clearer result cards for quarantine/runtime checks;
- route-class fitness in egress details.

## Phase 103 — Service-Aware Onboarding

The service matrix now understands service groups instead of only generic OK/FAIL.

Route classes:

- `GLOBAL_FAST`
- `GLOBAL_STABLE`
- `VIDEO_OPTIMIZED`
- `LOW_LATENCY`
- `DIRECT_RU`
- `TRUSTED_RU_SENSITIVE`

Services now tracked in the catalog:

- Cloudflare
- Google
- YouTube
- Telegram
- Apple
- Instagram
- WhatsApp
- Facebook
- Spotify
- SoundCloud
- Yandex
- VK
- Ozon
- Lamoda
- Alfa Bank
- T-Bank
- Sber
- Gosuslugi
- ESIA
- nalog.gov.ru

The matrix produces per-class fitness:

- `OK`
- `WARN`
- `FAIL`
- `UNKNOWN`

This means a channel can be acceptable for one purpose and bad for another. For example, it can be `OK` for `GLOBAL_FAST` and `FAIL` for `TRUSTED_RU_SENSITIVE`.

## Phase 104 — QR Upload Preview

The Add Egress wizard now has QR image upload.

Safety behavior:

- QR is preview-only.
- QR does not create a draft automatically.
- QR does not add anything to the pool.
- QR does not enable a channel.
- Decoded secret text is not returned to the UI.
- If the local decoder is missing, the UI gets a clear `DECODER_MISSING` result.

Current decoder hook:

- `zbarimg`

If `zbarimg` is not installed, operators can still paste the URI/config manually.

## Phase 105 — Better Result Cards

The onboarding result card now shows:

- external IP when available;
- service matrix status;
- selected role fit;
- route-class fitness table;
- service-by-service details;
- usage policy;
- pool preview.

The egress details modal also shows route-class fitness for already tested active channels.

## Safety Preserved

- No routing changes.
- No user movement.
- No kill switch changes.
- No automatic enable.
- No secrets printed.
- QR upload never activates a channel.
- Service matrix runs only during explicit test actions.

## Verification

Local:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -W error -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
git diff --check
```

Functional smoke test:

- route-class fitness returns `WARN` for mixed video results;
- sensitive RU returns `FAIL` when Gosuslugi/ESIA fail;
- QR endpoint returns `DECODER_MISSING` safely if no local decoder exists.

## Manual Admin Checks

1. Open `http://127.0.0.1:7080/login`.
2. Go to `Egress`.
3. Click `Add Egress Draft`.
4. Confirm QR upload input is visible.
5. Paste a supported URI/config.
6. Run `Detect`.
7. Run quarantine/runtime checks on a safe draft.
8. Confirm result card shows:
   - `Usage Policy`;
   - `Route-Class Fitness`;
   - `Service Matrix`.

## Next Work

The next layer is making service-aware routing consume these role/fitness fields when choosing route classes. That must still remain staged: dry-run first, then preview, then guarded apply.
