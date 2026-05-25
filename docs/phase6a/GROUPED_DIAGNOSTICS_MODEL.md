# V7 Phase 6A Grouped Diagnostics Model

## Purpose

Diagnostics should be grouped by operator meaning, not by raw implementation detail.

## Groups

Channels:

- egress lifecycle;
- service quality;
- health/degradation;
- readiness;
- quarantine/maintenance.

Routing:

- route classes;
- policy alignment;
- route reality;
- direct/RU isolation;
- kill switch compatibility.

Services:

- Telegram;
- YouTube;
- WhatsApp;
- DNS;
- HTTPS;
- sensitive RU services.

Users:

- affected users;
- readiness;
- reconnect issues;
- profile mismatch;
- org impact.

Trusted RU:

- availability;
- policy blockers;
- unsafe fallback prevention;
- route mismatch;
- service denial risk.

Autoswitch:

- mode;
- cooldown/freeze state;
- decision summary;
- confidence;
- blocked or deferred switches.

Security:

- kill switch;
- safe mode;
- RBAC;
- backups;
- audit trail.

Provisioning:

- imported;
- quarantine;
- runtime tested;
- staged;
- rollback available.

## Compression Rule

Prefer:

- `unstable quality observed on awg2`

over:

- 50 individual packet loss alerts.

