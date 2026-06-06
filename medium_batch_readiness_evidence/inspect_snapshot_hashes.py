import json
from datetime import datetime, timezone
from pathlib import Path

from admin_core.routing_intelligence import sha256_json


state = Path("/opt/v7/egress/state")
root = state / "intelligence"
files = {
    "service_matrix": state / "service-matrix.json",
    "quality_summary": state / "egress-quality-summary.json",
    "service_preferences": state / "service-preferences.json",
    "service_scores": root / "service-scores.json",
    "channel_service_scores": root / "channel-service-scores.json",
    "user_service_scores": root / "user-service-scores.json",
    "risk_summaries": root / "risk-summaries.json",
}

out = {}
for name, path in files.items():
    info = {"path": str(path), "exists": path.exists()}
    if path.exists():
        st = path.stat()
        info.update(
            {
                "mtime": st.st_mtime,
                "mtime_iso": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
                "size": st.st_size,
            }
        )
        try:
            data = json.loads(path.read_text())
            info["sha256_json"] = sha256_json(data)
            if isinstance(data, dict):
                info["schema"] = data.get("schema") or data.get("schema_version")
                info["generated_at"] = data.get("generated_at")
                info["source_hashes"] = data.get("source_hashes")
                info["freshness_state"] = data.get("freshness_state")
                info["confidence"] = data.get("confidence")
        except Exception as exc:
            info["error"] = repr(exc)
    out[name] = info

print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
