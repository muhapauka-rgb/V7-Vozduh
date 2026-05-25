# V7 Vozduh — Track 5.3 Registry Readers Fixtures & Read-Only Extraction Report

Generated: 2026-05-23

## Scope

Track 5.3 performed a second tiny monolith containment step:

- extracted only read-only registry parsing helpers;
- added fixture-backed parser contract tests;
- preserved endpoint inventory counts;
- preserved the monolith `parse_registry(path)` as the runtime IO/redaction boundary.

No live deploy was performed.

## Functions Extracted

Extracted into `admin_core/registry_readers.py`:

- `parse_kv_line(line)`
- `parse_registry_lines(lines)`

`parse_registry_lines(lines)` is the pure parsing part of the old `parse_registry(path)` loop. It accepts already-loaded lines and does not know runtime paths.

## Functions Intentionally Not Extracted

Not extracted:

- `parse_registry(path)`

Reason:

- reads registry contents through `read_text(path)`;
- accepts runtime `Path` values;
- applies `redact(...)` to parsed output;
- remains part of the monolith state IO boundary.

Also not extracted:

- registry writers;
- atomic write helpers;
- runtime path readers;
- assignment mutators;
- provisioning helpers;
- autoswitch helpers;
- Direct/RU or Trusted RU logic;
- Handler methods;
- auth/session/RBAC/CSRF/safe-mode logic;
- shell command wrappers.

## Fixture Cases Created

Created under `tests/unit/fixtures/registry/`:

- `simple.registry`
- `comments_empty.registry`
- `malformed_lines.registry`
- `duplicate_keys.registry`
- `quoted_values.registry`
- `whitespace.registry`

The fixtures lock current behavior, including parser quirks:

- whitespace splitting is not shell-like;
- malformed rows are preserved as `{}`;
- malformed parts without `=` are ignored;
- duplicate keys keep the last value;
- values containing `=` keep the suffix after the first `=`;
- quoted values are not parsed as quoted strings;
- full-line comments are skipped after `.strip()`;
- inline `#` does not start a comment, so later `key=value` tokens are still parsed.

## Exact Behavior Preserved

Old behavior:

```python
def parse_kv_line(line):
    item = {}
    for part in line.strip().split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        item[key] = value
    return item

def parse_registry(path):
    items = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        items.append(parse_kv_line(line))
    return redact(items)
```

New behavior:

```python
from admin_core.registry_readers import parse_kv_line, parse_registry_lines

def parse_registry(path):
    return redact(parse_registry_lines(read_text(path).splitlines()))
```

The runtime wrapper still owns file IO and redaction.

## Pre-Test Results

Command:

```bash
python3 -m unittest tests.contracts.endpoint_inventory_test
python3 -m unittest tests.unit.test_admin_core_sanitize tests.unit.test_admin_core_time
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py
```

Results:

- endpoint inventory contracts: OK, 5 tests;
- existing helper unit tests: OK, 8 tests;
- py_compile: OK.

## Post-Test Results

Command:

```bash
python3 -m unittest tests.contracts.endpoint_inventory_test
python3 -m unittest tests.unit.test_admin_core_sanitize tests.unit.test_admin_core_time tests.unit.test_admin_core_registry_readers
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py
```

Results:

- endpoint inventory contracts: OK, 5 tests;
- helper unit tests: OK, 15 tests;
- py_compile: OK.

Repository-wide default discovery was also checked:

```bash
python3 -m unittest discover tests
```

Result:

- OK, but discovered 0 tests because the current test layout is explicit-module based.

## Endpoint Inventory Before/After Counts

After regeneration with:

```bash
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/track5/endpoint-inventory.json
```

Counts remained unchanged:

```json
{
  "endpoint_count": 192,
  "by_method": {
    "GET": 47,
    "HEAD": 8,
    "POST": 137
  },
  "by_auth": {
    "public": 19,
    "required": 173
  },
  "by_family": {
    "action": 132,
    "page": 14,
    "public_api": 3,
    "public_delivery": 5,
    "read_api": 38
  },
  "by_risk": {
    "critical": 13,
    "high": 95,
    "medium": 37,
    "low": 47
  },
  "csrf_required_count": 132,
  "safe_mode_blocked_count": 86
}
```

## Files Created

- `admin_core/registry_readers.py`
- `tests/unit/test_admin_core_registry_readers.py`
- `tests/unit/fixtures/registry/simple.registry`
- `tests/unit/fixtures/registry/comments_empty.registry`
- `tests/unit/fixtures/registry/malformed_lines.registry`
- `tests/unit/fixtures/registry/duplicate_keys.registry`
- `tests/unit/fixtures/registry/quoted_values.registry`
- `tests/unit/fixtures/registry/whitespace.registry`
- `TRACK5_3_REGISTRY_READERS_EXTRACTION_REPORT.md`

## Files Changed

- `admin/v7-admin-api`
- `docs/track5/endpoint-inventory.json`

## Diff Safety Review

Track 5.3 changes in `admin/v7-admin-api` are limited to:

- adding exact import:
  - `from admin_core.registry_readers import parse_kv_line, parse_registry_lines`
- removing the local `parse_kv_line(...)` definition;
- changing `parse_registry(path)` to call `parse_registry_lines(read_text(path).splitlines())`.

No intentional Track 5.3 changes were made to:

- Handler dispatch;
- endpoint paths;
- JSON response payload construction;
- auth/session/RBAC/CSRF/safe-mode;
- shell command wrappers;
- registry write logic;
- runtime paths;
- embedded UI.

Note: `admin/v7-admin-api` already contains prior uncommitted changes from earlier V7 work, so full `git diff` includes unrelated historical edits. The Track 5.3-specific delta was verified by symbol and import search.

## Runtime Behavior Change Verdict

Expected runtime behavior change: none.

Reason:

- file IO remains in the monolith wrapper;
- redaction remains in the monolith wrapper;
- parser logic is byte-for-byte equivalent in behavior;
- endpoint inventory counts are stable;
- contract tests and py_compile pass;
- no live deployment was performed.

## Live Deploy Verdict

No live deploy was performed.

This was a repo-local containment step. Production runtime files were not changed.

## Whether Next Extraction Step Is Safe

Safe only for another tiny, fixture-backed, read-only extraction.

Still unsafe:

- state layer extraction;
- registry writer extraction;
- auth/session extraction;
- identity extraction;
- provisioning extraction;
- autoswitch extraction;
- routing/Direct/RU/Trusted RU extraction;
- Handler extraction;
- UI extraction.

Recommended next gate:

1. Add fixture-backed tests for any proposed helper before moving it.
2. Avoid helpers that read runtime paths or invoke commands.
3. Keep endpoint inventory contract tests mandatory after every extraction.
