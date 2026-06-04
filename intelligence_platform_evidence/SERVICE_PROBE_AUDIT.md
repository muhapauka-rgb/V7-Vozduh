# SERVICE_PROBE_AUDIT

Implemented in:

- `admin_core/intelligence_platform.py::service_probe_audit`

## Classification

| Service | Classification | Evidence |
| --- | --- | --- |
| Telegram | EXISTS | `v7-telegram-sentinel`, service matrix |
| YouTube | PARTIAL | service matrix logical checks |
| Instagram | PARTIAL | service matrix logical checks |
| ChatGPT | PARTIAL | service matrix logical checks |
| Google | EXISTS | service matrix |
| Google Auth | PARTIAL | service matrix |

## Missing Probe Classes

- service-specific YouTube playback probe;
- Instagram media probe;
- ChatGPT streaming probe.

## Verdict

```text
service_probe_audit_completed=true
```

