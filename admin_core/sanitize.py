"""Pure redaction helpers for V7 admin surfaces.

This module must stay side-effect free: no runtime paths, no file IO, no shell
commands, and no imports from the admin monolith.
"""

import re


SECRET_RE = re.compile(
    r"(private[_-]?key|preshared[_-]?key|password|passwd|token|secret|access[_-]?key|outline|short[_-]?id)",
    re.IGNORECASE,
)


def redact(value):
    if value is None:
        return value
    if isinstance(value, dict):
        return {k: ("[REDACTED]" if SECRET_RE.search(str(k)) else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if not isinstance(value, str):
        return value
    value = re.sub(r"(PrivateKey|PresharedKey|private_key|preshared_key|password|token|short_id)\s*=\s*\S+", r"\1=[REDACTED]", value, flags=re.I)
    value = re.sub(r'("(?:private_key|preshared_key|password|token|short_id)"\s*:\s*")[^"]+(")', r"\1[REDACTED]\2", value, flags=re.I)
    value = re.sub(r"(?is)<(key|tls-auth|tls-crypt|auth-user-pass)>\s*.*?\s*</\1>", r"<\1>[REDACTED]</\1>", value)
    return value

