"""Pure event shaping helpers for V7 admin surfaces.

This module must stay side-effect free: no runtime paths, no file IO, no shell
commands, and no imports from the admin monolith.
"""

import json
import re


def parse_jsonl_lines(lines, redact_value=None):
    redact_value = redact_value or (lambda value: value)
    out = []
    for line in lines:
        try:
            out.append(redact_value(json.loads(line)))
        except json.JSONDecodeError:
            out.append({"raw": redact_value(line)})
    return out


def infer_event_severity(event):
    explicit = str(event.get("severity", "")).lower()
    if explicit in ("error", "warning", "info"):
        return explicit
    text = " ".join(str(event.get(k, "")) for k in ("severity", "action", "component", "message", "reason")).lower()
    if any(word in text for word in ("fail", "failed", "error", "down", "leak", "blocked")):
        return "error"
    if any(word in text for word in ("warn", "stale", "quarantine", "rollback", "disable", "rotate")):
        return "warning"
    if any(word in text for word in ("ok", "create", "verify", "preview", "switch", "enable", "reissue")):
        return "info"
    return "info"


def extract_user_ip(text):
    match = re.search(r"\b10\.0\.0\.[0-9]{1,3}\b", str(text or ""))
    return match.group(0) if match else ""
