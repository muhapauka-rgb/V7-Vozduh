"""Pure time helpers for V7 admin surfaces.

This module must stay side-effect free: it may read the clock, but it must not
read files, runtime state, or admin monolith globals.
"""

import time as _time
from datetime import datetime, timezone


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def parse_ts(value):
    if not value:
        return None
    try:
        text = str(value).replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:
        return None


def age_sec(value):
    ts = parse_ts(value)
    if ts is None:
        return None
    return max(0, int(_time.time() - ts))

