# V7 Track 5 Extraction Gate

This gate is mandatory before any future admin monolith extraction.

Track 5 containment must remain:

- behavior-preserving;
- fixture-backed;
- endpoint-contract-safe;
- reversible;
- local-first;
- non-runtime-changing unless explicitly approved.

## Required Commands

Run before any extraction:

```bash
python3 -m unittest discover tests
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py
```

Or use:

```bash
tools/v7-run-tests
```

## Endpoint Inventory Gate

After any extraction, regenerate endpoint inventory:

```bash
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/track5/endpoint-inventory.json
```

Then rerun:

```bash
python3 -m unittest discover tests
```

The endpoint inventory guard must stay green unless an endpoint contract change was intentional and documented.

Current frozen counts:

- `endpoint_count`: 192
- `GET`: 47
- `HEAD`: 8
- `POST`: 137
- `public`: 19
- `required`: 173
- `csrf_required_count`: 132
- `safe_mode_blocked_count`: 86

## Diff Gate

Before accepting an extraction, confirm there are no accidental changes to:

- Handler dispatch;
- endpoint paths;
- JSON response payload construction;
- auth/session/RBAC/CSRF/safe-mode;
- identity;
- provisioning;
- autoswitch;
- Direct/RU or Trusted RU/Gosuslugi;
- shell command wrappers;
- runtime paths;
- embedded UI.

## Live Deploy Gate

Default policy:

- no live deploy for helper extraction;
- no production runtime changes;
- no VPS checks required for repo-local containment steps.

Live deploy requires explicit approval, backup plan, and post-deploy runtime verification.

## Allowed Future Extraction Shape

Allowed:

- tiny pure helpers;
- read-only parsers with fixtures;
- no IO;
- no subprocess;
- no runtime path ownership.

Not allowed without a new gate:

- state layer extraction;
- registry writer extraction;
- auth/session extraction;
- identity extraction;
- provisioning extraction;
- autoswitch extraction;
- routing/Direct/RU/Trusted RU extraction;
- Handler extraction;
- UI extraction.
