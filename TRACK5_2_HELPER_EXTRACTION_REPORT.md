# V7 Vozduh - Track 5.2 First Tiny Helper Extraction: sanitize + time

Generated: 2026-05-23

Scope: first tiny monolith containment extraction.

Runtime deployed:

```text
no
```

Runtime behavior changed:

```text
no intended behavior change
```

## 1. Functions Extracted

Extracted from `admin/v7-admin-api` into side-effect-free helper modules:

| Function | New Module | Reason |
|---|---|---|
| `redact` | `admin_core.sanitize` | Pure recursive redaction helper; no file IO, no shell, no runtime state |
| `now_iso` | `admin_core.time` | Pure clock helper |
| `parse_ts` | `admin_core.time` | Pure timestamp parser |
| `age_sec` | `admin_core.time` | Pure clock delta helper; depends only on `parse_ts` and current time |

Imports added to monolith:

```python
from admin_core.sanitize import redact
from admin_core.time import age_sec, now_iso, parse_ts
```

The imported names preserve the same symbols in the monolith namespace, so existing call sites keep working unchanged.

## 2. Functions Intentionally Not Extracted

Not extracted:

- `read_text`
- `read_json`
- `write_json_atomic`
- `write_text_atomic`
- `deep_merge_defaults`
- `file_age`
- registry parsers;
- auth/session helpers;
- safe validators tied to route/policy/domain/global constants;
- identity helpers;
- provisioning helpers;
- autoswitch wrappers;
- direct/RU or Trusted RU helpers;
- Handler/router logic;
- embedded UI.

Why:

- `read_*` and `write_*` touch filesystem state.
- `file_age` reads actual file metadata.
- many `safe_*` validators depend on monolith globals such as supported modes, policy classes, route class sets, or runtime-specific regexes.
- moving validators broadly would increase the blast radius beyond a tiny first extraction.

## 3. Why Extracted Helpers Are Pure

`admin_core.sanitize`:

- imports only `re`;
- has no runtime path constants;
- performs no IO;
- performs no subprocess calls;
- does not import `admin/v7-admin-api`;
- does not mutate input objects.

`admin_core.time`:

- imports only standard library time/datetime;
- reads the clock only;
- performs no file IO;
- performs no subprocess calls;
- does not import `admin/v7-admin-api`;
- has no V7 runtime state dependency.

## 4. Files Created / Changed

Created:

- `admin_core/__init__.py`
- `admin_core/sanitize.py`
- `admin_core/time.py`
- `tests/unit/test_admin_core_sanitize.py`
- `tests/unit/test_admin_core_time.py`
- `TRACK5_2_HELPER_EXTRACTION_REPORT.md`

Changed:

- `admin/v7-admin-api`
  - exact imports added;
  - local definitions removed for `redact`, `now_iso`, `parse_ts`, `age_sec`.
- `docs/track5/endpoint-inventory.json`
  - regenerated after extraction; endpoint counts stayed unchanged.

## 5. Pre-Test Results

Pre-extraction contract test:

```text
python3 -m unittest tests.contracts.endpoint_inventory_test
.....
Ran 5 tests
OK
```

Pre-extraction direct compile command:

```text
python3 -m py_compile admin/v7-admin-api
```

Result:

```text
failed due macOS Python cache path outside sandbox:
PermissionError: /Users/ponch/Library/Caches/com.apple.python/Users/ponch/Documents
```

This was a local sandbox/cache issue, not a syntax failure.

Pre-extraction compile with allowed cache path:

```text
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api
```

Result:

```text
OK
```

## 6. Post-Test Results

Endpoint inventory regeneration:

```text
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/track5/endpoint-inventory.json
OK
```

Post-extraction contract tests:

```text
python3 -m unittest tests.contracts.endpoint_inventory_test
.....
Ran 5 tests in 0.185s
OK
```

Unit tests:

```text
python3 -m unittest tests.unit.test_admin_core_sanitize tests.unit.test_admin_core_time
........
Ran 8 tests in 0.001s
OK
```

Compile checks:

```text
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py
OK
```

Repository-wide unittest discovery:

```text
python3 -m unittest discover tests
Ran 0 tests
OK
```

Note: default discovery did not find the explicit test modules; explicit test commands above are authoritative for Track 5.2.

## 7. Endpoint Contract Test Result

Endpoint contract tests still pass.

Endpoint inventory after extraction:

| Metric | Count |
|---|---:|
| Endpoint branches | 192 |
| GET | 47 |
| HEAD | 8 |
| POST | 137 |
| Public | 19 |
| Auth required | 173 |
| CSRF-required | 132 |
| Safe-mode blocked actions | 86 |
| Critical risk | 13 |
| High risk | 95 |
| Medium risk | 37 |
| Low risk | 47 |

No endpoint path, method, auth requirement, CSRF requirement, or risk classification changed.

## 8. Py Compile Result

Post-extraction compile passed with local cache redirected:

```text
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py
OK
```

## 9. Diff Safety Review

Track 5.2 intended diff:

- added exact imports:
  - `from admin_core.sanitize import redact`
  - `from admin_core.time import age_sec, now_iso, parse_ts`
- removed local definitions for:
  - `now_iso`
  - `redact`
  - `parse_ts`
  - `age_sec`
- added pure helper modules and unit tests.

Important dirty-worktree note:

`admin/v7-admin-api` already had unrelated uncommitted changes before Track 5.2. A full `git diff` therefore includes older changes outside this extraction. Track 5.2 safety was reviewed by searching for the extraction-specific diff signatures; only the expected imports/removals were part of this block.

No changes were made to:

- Handler routing;
- endpoint paths;
- JSON payload construction;
- auth/session logic;
- RBAC/CSRF/safe mode;
- identity/provisioning/autoswitch/direct/RU/Trusted RU;
- shell command wrappers;
- embedded UI behavior.

## 10. Runtime Behavior Change Verdict

Runtime behavior change:

```text
none intended
```

Live deploy:

```text
not performed
```

Reason:

Track 5.2 is a repo/local containment step. It creates helper modules and validates contracts locally before any future deployment. Live VPS verification was not required because no production runtime file was changed.

## 11. Whether Next Extraction Step Is Safe

Safe next tiny step:

```text
admin_core.registry_readers only after fixtures are added
```

Before that:

- add fixtures for registry lines;
- assert exact parse behavior;
- keep writes in monolith;
- keep state paths in monolith;
- run endpoint inventory tests before/after.

Not safe yet:

- auth extraction;
- identity extraction;
- provisioning extraction;
- autoswitch extraction;
- direct/RU extraction;
- Handler route split;
- UI extraction.

Track 5.2 completed the first small containment step without broad refactor.

