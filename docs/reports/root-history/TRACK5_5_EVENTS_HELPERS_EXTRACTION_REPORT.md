# V7 Vozduh — Track 5.5 Events Read-Only Helpers Extraction Report

Generated: 2026-05-23

## Scope

Track 5.5 performed one tiny read-only event helper extraction.

No audit writer behavior was moved.
No event persistence behavior was moved.
No endpoint logic was changed.
No live deploy was performed.

## 1. Functions Extracted

Extracted into `admin_core/events.py`:

- `parse_jsonl_lines(lines, redact_value=None)`
- `infer_event_severity(event)`
- `extract_user_ip(text)`

`parse_jsonl_lines(...)` contains the pure JSONL row-shaping behavior formerly embedded in `tail_jsonl(...)`.

## 2. Functions Intentionally Not Extracted

Not extracted:

- `tail_jsonl(path, limit=30)`
- `audit_admin(...)`
- `infer_admin_audit_fields(...)`
- `normalized_events(...)`
- `security_audit(...)`
- `security_audit_csv(...)`

Reasons:

- `tail_jsonl(path)` reads a filesystem path and remains the monolith IO boundary.
- `audit_admin(...)` calls `v7-audit-log` and is explicitly runtime mutation/audit writer behavior.
- `normalized_events(...)` owns runtime path selection through `AUDIT_FILE` and `EVENT_DIR`.
- `security_audit(...)` owns audit-specific filtering and runtime audit file reads.
- CSV export and API response shaping were not part of this tiny extraction.

## 3. Fixture Cases Created

Created under `tests/unit/fixtures/events/`:

- `simple_events.jsonl`
- `mixed_severity.jsonl`
- `malformed_events.jsonl`
- `missing_fields.jsonl`
- `large_tail.jsonl`
- `unicode_events.jsonl`

Covered cases:

- valid JSONL rows;
- malformed JSON rows;
- empty/truncated lines;
- missing fields;
- explicit and inferred severity;
- unknown severity fallback;
- unicode messages;
- VPN user IP extraction;
- tail behavior by preserving caller-side slicing semantics.

## 4. Exact Behavior Preserved

Previous behavior inside `tail_jsonl(...)`:

```python
lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]
out = []
for line in lines:
    try:
        out.append(redact(json.loads(line)))
    except json.JSONDecodeError:
        out.append({"raw": redact(line)})
return out
```

New behavior:

```python
lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]
return parse_jsonl_lines(lines, redact_value=redact)
```

`tail_jsonl(path)` still:

- converts input to `Path`;
- checks `exists()`;
- reads the file;
- applies tail slicing;
- applies redaction.

The extracted helper does not own runtime paths and does not write anything.

## 5. Pre-Test Results

Command:

```bash
tools/v7-run-tests
```

Result:

- unittest discovery: OK, 20 tests;
- py_compile: OK.

## 6. Post-Test Results

Command:

```bash
tools/v7-run-tests
```

Result:

- unittest discovery: OK, 28 tests;
- py_compile: OK.

Additional check:

```bash
python3 -m unittest tests.unit.test_admin_core_events
```

Result:

- OK, 8 tests.

Additional compile:

```bash
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py admin_core/events.py
```

Result:

- OK.

## 7. Endpoint Inventory Before/After Counts

Endpoint inventory was regenerated:

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

Note: the old `source_line_count >= 30000` assertion was relaxed to `source_line_count > 0` because successful extraction reduced the monolith below 30000 lines. Endpoint contract counts remain exact-frozen.

## 8. Diff Safety Review

Track 5.5 intended changes:

- added `admin_core/events.py`;
- added event fixtures/tests;
- imported exact event helpers in `admin/v7-admin-api`;
- kept `tail_jsonl(path)` as local IO wrapper;
- removed duplicate local definitions of `infer_event_severity(...)` and `extract_user_ip(...)`;
- updated `tools/v7-run-tests` to compile `admin_core/events.py`;
- regenerated endpoint inventory with unchanged endpoint counts;
- adjusted source-line-count sanity assertion.

No Track 5.5 changes were made to:

- Handler dispatch;
- endpoint paths;
- JSON response schemas;
- auth/session/RBAC/CSRF/safe-mode;
- identity;
- provisioning;
- autoswitch;
- Direct/RU or Trusted RU/Gosuslugi;
- shell command wrappers;
- runtime paths;
- audit writer behavior;
- embedded UI;
- production runtime.

Note: the working tree contains prior Track 5 and earlier V7 changes, so full `git diff` for `admin/v7-admin-api` includes older unrelated changes. Track 5.5-specific symbol checks confirm only the event helper import/wrapper delta.

## 9. Runtime Behavior Change Verdict

Expected runtime behavior change: none.

Reason:

- audit writer was not moved;
- event file reads remain in `tail_jsonl(path)`;
- runtime paths remain in the monolith;
- redaction still occurs in the same `tail_jsonl(...)` path;
- endpoint inventory counts are unchanged;
- local gate passes.

## 10. Live Deploy Verdict

No live deploy was performed.

This was a repo-local containment step only.

## 11. Whether Next Tiny Extraction Is Safe

Next tiny extraction is allowed only if it is:

- fixture-backed before move;
- read-only or pure;
- covered by `tools/v7-run-tests`;
- followed by endpoint inventory regeneration;
- endpoint-count-stable;
- free of runtime path ownership and side effects.

Still not allowed:

- audit/runtime layer extraction;
- state writers;
- auth/session;
- identity;
- provisioning;
- autoswitch;
- routing/Direct/RU/Trusted RU;
- Handler;
- UI.
