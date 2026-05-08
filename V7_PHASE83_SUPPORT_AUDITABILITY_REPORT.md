# V7 Phase 83 - Support Auditability

Date: 2026-05-08

## Goal

Improve auditability around operator support actions in Identity / Onboarding.

## Implemented

- Allowed Phone details:
  - phone rows now open a detail modal;
  - detail modal shows state, name, organization, group, operator note, update time;
  - recent connect attempts for that phone are shown.
- Identity User details:
  - operator note is now visible in the user detail modal;
  - recent connect attempts for the user's phone are shown.
- Security Audit shortcuts:
  - added `Identity Changes` quick filter.
- Events shortcuts:
  - added `Identity Events` quick filter.
- Audit wording:
  - identity user updates now include `notes_updated=true/false`;
  - allowed phone updates include `note_present=true/false`.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Local admin HTML smoke test:
  - allowed phone details: present;
  - user note detail: present;
  - security identity filter: present;
  - events identity filter: present.
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- Live admin check:
  - POST `/login`: HTTP `303`
  - admin page: HTTP `200`
  - Phase83 UI elements present.

## Next

Phase 84 should return to platform-level hardening:

- backup/restore operator UX;
- bounded logs and backup retention visibility;
- safe restore preview;
- confirm that Identity DB is included in backups.
