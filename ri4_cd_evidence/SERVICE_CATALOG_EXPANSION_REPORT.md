# SERVICE_CATALOG_EXPANSION_REPORT

## Current Services

Discovered current default catalog in `admin_core/routing_intelligence.py`:

- `telegram`
- `youtube`
- `instagram`
- `chatgpt`
- `google`
- `google_auth`

## Current Production Signals

Existing reports and code references show service matrix, quality summary, Telegram sentinel, and admin service views.

## Recommendation

Do not blindly add new services in RI4.CD.

Recommended later additions after explicit probe ownership is mapped:

- WhatsApp
- TikTok
- X
- Facebook
- Gmail
- Google Meet
- Zoom
- Discord
- Netflix
- Spotify
- Apple Services

## Classification

| Service | Status |
| --- | --- |
| Telegram | IMPLEMENTED_PRIMARY_MODEL |
| YouTube | IMPLEMENTED_PRIMARY_MODEL |
| Instagram | IMPLEMENTED_PRIMARY_MODEL |
| ChatGPT | IMPLEMENTED_PRIMARY_MODEL |
| Google | KEEP_GENERIC_MODEL |
| Google Auth | KEEP_GENERIC_MODEL |
| Additional services | DEFER_UNTIL_PROBE_OWNERSHIP_AUDIT |

