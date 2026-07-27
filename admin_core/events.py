"""Pure event shaping helpers for V7 admin surfaces.

This module must stay side-effect free: no runtime paths, no file IO, no shell
commands, and no imports from the admin monolith.
"""

import hashlib
import json
import re


EVENT_SOURCE_CATALOG = {
    "telegram_sentinel": {
        "owner": "tools/v7-telegram-sentinel",
        "event_type": "service_regression",
        "default_confidence": 0.82,
        "event_class": "PRIMARY EVENT",
        "suitability": "autonomy_trigger_candidate_with_confirmation",
        "false_positive_risk": "medium",
        "false_negative_risk": "medium",
        "requires_confirmation": True,
    },
    "service_matrix": {
        "owner": "tools/v7-service-matrix-refresh-all / tools/v7-service-matrix-test",
        "event_type": "service_matrix_regression",
        "default_confidence": 0.86,
        "event_class": "PRIMARY EVENT",
        "suitability": "autonomy_trigger_candidate",
        "false_positive_risk": "medium",
        "false_negative_risk": "low",
        "requires_confirmation": True,
    },
    "quality_compact": {
        "owner": "tools/v7-egress-quality-compact",
        "event_type": "channel_quality_regression",
        "default_confidence": 0.78,
        "event_class": "PRIMARY EVENT",
        "suitability": "autonomy_trigger_candidate_with_freshness_gate",
        "false_positive_risk": "medium",
        "false_negative_risk": "medium",
        "requires_confirmation": True,
    },
    "capacity_signals": {
        "owner": "tools/runtime-support/v7-egress-load / tools/runtime-support/v7-capacity-readiness",
        "event_type": "capacity_or_load_regression",
        "default_confidence": 0.74,
        "event_class": "SECONDARY EVENT",
        "suitability": "planner_input_not_standalone_apply_trigger",
        "false_positive_risk": "medium",
        "false_negative_risk": "medium",
        "requires_confirmation": True,
    },
    "runtime_readiness": {
        "owner": "admin_core/runtime_read_views.py / tools/v7-truth-check",
        "event_type": "runtime_readiness_change",
        "default_confidence": 0.9,
        "event_class": "SECONDARY EVENT",
        "suitability": "hard_stop_or_readiness_gate",
        "false_positive_risk": "low",
        "false_negative_risk": "low",
        "requires_confirmation": False,
    },
    "route_readiness": {
        "owner": "admin_core/route_reality_views.py / tools/runtime-support/v7-policy-route-check",
        "event_type": "route_readiness_change",
        "default_confidence": 0.76,
        "event_class": "SECONDARY EVENT",
        "suitability": "planner_gate_with_confirmation",
        "false_positive_risk": "medium",
        "false_negative_risk": "medium",
        "requires_confirmation": True,
    },
    "planner_blocker_transitions": {
        "owner": "tools/v7-users-autoswitch",
        "event_type": "planner_blocker_transition",
        "default_confidence": 0.72,
        "event_class": "SECONDARY EVENT",
        "suitability": "planner_explanation_and_stop_reason",
        "false_positive_risk": "low",
        "false_negative_risk": "medium",
        "requires_confirmation": False,
    },
    "trust_evolution_changes": {
        "owner": "admin_core/intelligence_platform.py / trust-evolution-summaries",
        "event_type": "trust_evolution_change",
        "default_confidence": 0.7,
        "event_class": "SECONDARY EVENT",
        "suitability": "readiness_confidence_input",
        "false_positive_risk": "medium",
        "false_negative_risk": "medium",
        "requires_confirmation": False,
    },
    "prediction_signals": {
        "owner": "admin_core/intelligence_platform.py / prediction-summaries",
        "event_type": "prediction_signal_change",
        "default_confidence": 0.68,
        "event_class": "DIAGNOSTIC EVENT",
        "suitability": "advisory_until_matched_actuals_are_sufficient",
        "false_positive_risk": "medium",
        "false_negative_risk": "medium",
        "requires_confirmation": True,
    },
}


_SOURCE_ALIASES = {
    "telegram": "telegram_sentinel",
    "telegram-sentinel": "telegram_sentinel",
    "telegram_sentinel": "telegram_sentinel",
    "service": "service_matrix",
    "service-matrix": "service_matrix",
    "service_matrix": "service_matrix",
    "matrix": "service_matrix",
    "quality": "quality_compact",
    "quality-compact": "quality_compact",
    "quality_compact": "quality_compact",
    "egress-quality": "quality_compact",
    "capacity": "capacity_signals",
    "load": "capacity_signals",
    "runtime": "runtime_readiness",
    "runtime-readiness": "runtime_readiness",
    "route": "route_readiness",
    "route-readiness": "route_readiness",
    "planner": "planner_blocker_transitions",
    "planner-blocker": "planner_blocker_transitions",
    "trust": "trust_evolution_changes",
    "trust-evolution": "trust_evolution_changes",
    "prediction": "prediction_signals",
}


def parse_jsonl_lines(lines, redact_value=None):
    redact_value = redact_value or (lambda value: value)
    out = []
    for line in lines:
        try:
            out.append(redact_value(json.loads(line)))
        except json.JSONDecodeError:
            out.append({"raw": redact_value(line)})
    return out


def stable_event_hash(payload):
    data = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:20]


def normalize_event_source(source):
    raw = str(source or "").strip().lower().replace(" ", "_")
    raw = raw.replace(".", "_")
    return _SOURCE_ALIASES.get(raw, raw if raw in EVENT_SOURCE_CATALOG else "unknown")


def event_source_profile(source):
    normalized = normalize_event_source(source)
    profile = dict(EVENT_SOURCE_CATALOG.get(normalized, {}))
    if not profile:
        profile = {
            "owner": "UNKNOWN",
            "event_type": "unknown_event",
            "default_confidence": 0.0,
            "event_class": "DIAGNOSTIC EVENT",
            "suitability": "not_suitable_until_source_is_mapped",
            "false_positive_risk": "unknown",
            "false_negative_risk": "unknown",
            "requires_confirmation": True,
        }
    profile["source"] = normalized
    return profile


def _event_timestamp(event):
    for key in ("updated_at", "timestamp", "time", "created_at", "observed_at"):
        value = event.get(key) if isinstance(event, dict) else None
        if value:
            return str(value)
    return ""


def _event_confidence(event, profile):
    for key in ("confidence", "score_confidence", "source_confidence"):
        try:
            value = float(event.get(key))
        except (TypeError, ValueError, AttributeError):
            continue
        if value > 1:
            value = value / 100.0
        return round(max(0.0, min(1.0, value)), 3)
    return round(float(profile.get("default_confidence", 0.0) or 0.0), 3)


def normalize_regression_event(event, source=""):
    event = event if isinstance(event, dict) else {"raw": event}
    inferred_source = source or event.get("source") or event.get("component") or event.get("tool") or event.get("owner")
    profile = event_source_profile(inferred_source)
    severity = infer_event_severity(event)
    event_type = str(event.get("event_type") or event.get("type") or profile["event_type"])
    # Preserve an already-normalized projection when an existing downstream
    # consumer receives it again.  Producers commonly use ``channel`` while
    # consumers use ``object``; losing the latter on a second normalization
    # would sever the source-bound safety check without changing the fact
    # itself.
    object_id = str(
        event.get("channel")
        or event.get("egress")
        or event.get("object")
        or event.get("user")
        or event.get("component")
        or ""
    )
    event_id = str(event.get("event_id") or "")
    normalized = {
        "event_id": event_id or stable_event_hash({
            "source": profile["source"],
            "event_type": event_type,
            "object": object_id,
            "timestamp": _event_timestamp(event),
            "message": event.get("message") or event.get("reason") or event.get("action") or event.get("raw") or "",
        }),
        "source": profile["source"],
        "owner": profile["owner"],
        "event_type": event_type,
        "event_class": profile["event_class"],
        "severity": severity,
        "object": object_id,
        "timestamp": _event_timestamp(event),
        "confidence": _event_confidence(event, profile),
        "freshness": "freshness_source_timestamp_present" if _event_timestamp(event) else "freshness_unknown",
        "suitability_for_autonomy": profile["suitability"],
        "requires_confirmation": bool(profile["requires_confirmation"]),
        "false_positive_risk": profile["false_positive_risk"],
        "false_negative_risk": profile["false_negative_risk"],
        "raw_reason": str(event.get("reason") or event.get("message") or event.get("action") or event.get("raw") or ""),
        "read_only": True,
        "preview_only": True,
        "synthetic_event": False,
        # Preserve the existing Service Matrix causal binding for downstream
        # bounded-delegated admission.  These are facts supplied by the
        # producer, not execution permission: the executor still verifies
        # freshness, source match, policy, Candidate, Packet and every live
        # safety gate independently.
        "source_incident_id": str(event.get("source_incident_id") or ""),
        "observation_generation": str(event.get("observation_generation") or ""),
        "failure_episode_id": str(event.get("failure_episode_id") or ""),
        "event_provenance": str(event.get("event_provenance") or event.get("provenance") or ""),
        "evidence_class": str(event.get("evidence_class") or ""),
        # Preserve the compact failed-source denominator across the generic
        # event boundary. It remains evidence only; packet and live gates
        # independently decide whether action is legal.
        "source_scope": (
            dict(event.get("source_scope") or {})
            if isinstance(event.get("source_scope"), dict) else {}
        ),
        "capture_only": str(event.get("capture_only") or "").strip().lower() in {"1", "true", "yes", "on"},
    }
    return normalized


def build_event_source_inventory(events_by_source=None, now=""):
    events_by_source = events_by_source if isinstance(events_by_source, dict) else {}
    rows = []
    for source in EVENT_SOURCE_CATALOG:
        profile = event_source_profile(source)
        rows_for_source = events_by_source.get(source, [])
        if isinstance(rows_for_source, dict):
            rows_for_source = [rows_for_source]
        rows_for_source = rows_for_source if isinstance(rows_for_source, list) else []
        timestamps = [_event_timestamp(row) for row in rows_for_source if isinstance(row, dict) and _event_timestamp(row)]
        rows.append({
            "source": source,
            "owner": profile["owner"],
            "event_type": profile["event_type"],
            "event_class": profile["event_class"],
            "event_count": len(rows_for_source),
            "freshness": max(timestamps) if timestamps else "unknown",
            "confidence": profile["default_confidence"],
            "suitability_for_autonomy": profile["suitability"],
            "false_positive_risk": profile["false_positive_risk"],
            "false_negative_risk": profile["false_negative_risk"],
            "requires_confirmation": profile["requires_confirmation"],
            "last_inventory_at": now,
        })
    return rows


def build_readonly_event_consumer_trace(events=None, *, now=""):
    events = events if isinstance(events, list) else []
    normalized_events = [normalize_regression_event(event) for event in events]
    primary = [event for event in normalized_events if event["event_class"] == "PRIMARY EVENT"]
    secondary = [event for event in normalized_events if event["event_class"] == "SECONDARY EVENT"]
    diagnostic = [event for event in normalized_events if event["event_class"] == "DIAGNOSTIC EVENT"]
    planner_events = primary + secondary
    return {
        "schema_version": "v7.event-consumer-readonly.v1",
        "generated_at": now,
        "read_only": True,
        "preview_only": True,
        "execution_allowed_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "autonomy_enabled": False,
        "synthetic_events_created": False,
        "new_truth_source_created": False,
        "event_count": len(normalized_events),
        "primary_event_count": len(primary),
        "secondary_event_count": len(secondary),
        "diagnostic_event_count": len(diagnostic),
        "planner_preview_event_count": len(planner_events),
        "event_source_inventory": build_event_source_inventory(
            {
                event["source"]: [row for row in normalized_events if row["source"] == event["source"]]
                for event in normalized_events
            },
            now=now,
        ),
        "events": normalized_events,
        "planner_trigger_candidates": planner_events,
        "diagnostic_events": diagnostic,
        "certification_state": "CERTIFIED_READONLY_CONSUMER" if planner_events else "WAITING_FOR_REAL_REGRESSION_EVENT",
        "links": [
            {"from": "observed_outcome", "to": "event", "state": "present" if normalized_events else "waiting_for_event"},
            {"from": "event", "to": "planner_preview", "state": "present" if planner_events else "waiting_for_primary_or_secondary_event"},
            {"from": "planner_preview", "to": "packet_preview", "state": "delegated_to_existing_pipeline"},
            {"from": "packet_preview", "to": "restore_barrier_preview", "state": "delegated_to_existing_pipeline"},
            {"from": "restore_barrier_preview", "to": "rollback_preview", "state": "delegated_to_existing_pipeline"},
            {"from": "rollback_preview", "to": "feedback_preview", "state": "delegated_to_existing_pipeline"},
            {"from": "feedback_preview", "to": "learning_preview", "state": "delegated_to_existing_pipeline"},
        ],
    }


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
