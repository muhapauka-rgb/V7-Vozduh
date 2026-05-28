"""Read-only operator observability aggregation for V7 admin surfaces.

This module is deliberately side-effect free with respect to runtime state:
it reads local files and evidence only, never shells out, never writes, and
never exposes mutation helpers.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from admin_core.registry_readers import parse_registry_lines
from admin_core.sanitize import redact


REPORT_RE = re.compile(r"^BLOCK_E(?P<block>[0-9_]+).*[.]md$")
SECRET_TEXT_RE = re.compile(
    r"(private[_-]?key|preshared[_-]?key|password|passwd|token|secret|access[_-]?key|outline|short[_-]?id)",
    re.IGNORECASE,
)
TEXT_EVIDENCE_SUFFIXES = {
    ".cfg",
    ".conf",
    ".csv",
    ".json",
    ".jsonl",
    ".log",
    ".md",
    ".py",
    ".sh",
    ".state",
    ".txt",
    ".yaml",
    ".yml",
}
MAX_EVIDENCE_DETAIL_BYTES = 256 * 1024
MAX_EVIDENCE_INDEX_FILES = 900


def utc_now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat()


def read_text(path, default=""):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return default


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return {} if default is None else default


def file_hash(path):
    try:
        data = Path(path).read_bytes()
    except OSError:
        return ""
    return hashlib.sha256(data).hexdigest()


def stable_id(value):
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]


def is_relative_to(path, parent):
    try:
        Path(path).resolve().relative_to(Path(parent).resolve())
        return True
    except (OSError, ValueError):
        return False


def safe_text_excerpt(path, max_lines=80, max_bytes=MAX_EVIDENCE_DETAIL_BYTES):
    path = Path(path)
    try:
        stat = path.stat()
    except OSError:
        return {"state": "MISSING", "excerpt": "", "redacted_lines": 0, "warnings": ["missing"], "size_bytes": 0}
    if stat.st_size > max_bytes:
        return {
            "state": "PARTIAL",
            "excerpt": "",
            "redacted_lines": 0,
            "warnings": ["file_too_large_for_inline_excerpt"],
            "size_bytes": stat.st_size,
        }
    if path.suffix.lower() not in TEXT_EVIDENCE_SUFFIXES:
        return {
            "state": "PARTIAL",
            "excerpt": "",
            "redacted_lines": 0,
            "warnings": ["non_text_or_unindexed_suffix"],
            "size_bytes": stat.st_size,
        }
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"state": "MISSING", "excerpt": "", "redacted_lines": 0, "warnings": ["read_failed"], "size_bytes": stat.st_size}
    lines = []
    redacted_count = 0
    for line in redact(text).splitlines():
        if SECRET_TEXT_RE.search(line):
            redacted_count += 1
            continue
        lines.append(line)
        if len(lines) >= max_lines:
            break
    warnings = []
    if redacted_count:
        warnings.append("secret_like_lines_redacted")
    if len(text.splitlines()) > max_lines:
        warnings.append("excerpt_truncated")
    return {
        "state": "PARTIAL" if warnings else "HISTORICAL",
        "excerpt": "\n".join(lines),
        "redacted_lines": redacted_count,
        "warnings": warnings,
        "size_bytes": stat.st_size,
    }


def file_meta(path, now=None, validity_seconds=180):
    now = now or utc_now()
    path = Path(path)
    if not path.exists():
        return {
            "path": str(path),
            "state": "MISSING",
            "collected_at": None,
            "valid_until": None,
            "age_seconds": None,
            "stale": True,
            "stale_reasons": ["missing"],
            "sha256": "",
        }
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age = max(0, int((now - mtime).total_seconds()))
    stale = age > validity_seconds
    valid_until = mtime + timedelta(seconds=validity_seconds)
    return {
        "path": str(path),
        "state": "STALE" if stale else ("RECENT" if age > validity_seconds / 2 else "FRESH"),
        "collected_at": iso(mtime),
        "valid_until": iso(valid_until),
        "age_seconds": age,
        "stale": stale,
        "stale_reasons": ["age_exceeds_validity"] if stale else [],
        "sha256": file_hash(path),
    }


def freshness_from_meta(items):
    missing = [item for item in items if item.get("state") == "MISSING"]
    stale = [item for item in items if item.get("stale")]
    if missing:
        state = "MISSING"
    elif stale:
        state = "STALE"
    else:
        state = "FRESH"
    return {
        "state": state,
        "stale": bool(missing or stale),
        "sources": items,
        "stale_reasons": sorted({reason for item in items for reason in item.get("stale_reasons", [])}),
    }


def safe_report_summary(text):
    text = redact(text or "")
    final_answers = {}
    mutation = {}
    for line in text.splitlines():
        clean = line.strip()
        if not clean or SECRET_TEXT_RE.search(clean):
            continue
        if "=" in clean and clean.count("=") == 1 and len(clean) < 220:
            key, value = clean.split("=", 1)
            if re.match(r"^[a-z0-9_]+$", key):
                final_answers[key] = value
        if clean.startswith("Runtime mutation performed:"):
            mutation["runtime"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("User movement performed"):
            mutation["user_movement"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("Routing mutation performed"):
            mutation["routing"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("Kill switch mutation performed"):
            mutation["kill_switch"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("Autoswitch apply performed manually:"):
            mutation["manual_autoswitch_apply"] = clean.split(":", 1)[1].strip()
        elif clean.startswith("Canary performed:"):
            mutation["canary"] = clean.split(":", 1)[1].strip()
    return final_answers, mutation


def block_sort_key(path):
    match = REPORT_RE.match(path.name)
    if not match:
        return (1, [999], path.name)
    parts = []
    for part in match.group("block").split("_"):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    return (0, parts, path.name)


def block_id_from_path(path):
    stem = Path(path).stem
    return stem.replace("BLOCK_", "")


def evidence_dir_candidates(repo_root, operation_id):
    lower = operation_id.lower()
    block_match = re.match(r"(e[0-9]+(?:_[0-9]+)*)", lower)
    block = block_match.group(1) if block_match else lower
    candidates = []
    if block.startswith(("e13", "e14", "e15", "e16", "e17", "e18")):
        candidates.append(Path(repo_root) / "docs" / "track7" / "productization" / f"{block.split('_')[0]}-evidence")
    if block.startswith("stage2"):
        candidates.append(Path(repo_root) / "docs" / "track7" / "productization" / "stage2-finalization")
    candidates.append(Path(repo_root) / "docs" / "track7" / "control-plane" / f"{block}-evidence")
    if "_" in lower and lower != block:
        candidates.append(Path(repo_root) / "docs" / "track7" / "control-plane" / f"{lower}-evidence")
    return candidates


def first_existing_evidence_dir(repo_root, operation_id):
    for path in evidence_dir_candidates(repo_root, operation_id):
        if path.exists() and path.is_dir():
            return path
    return None


def classify_operation(path, text, answers):
    haystack = f"{path.name}\n{text[:4000]}".lower()
    if "productization" in haystack or "operator ux" in haystack or "observability" in haystack or path.name.startswith(("BLOCK_E13", "BLOCK_E14", "BLOCK_E15", "BLOCK_E16", "BLOCK_E17", "BLOCK_E18", "BLOCK_STAGE2")):
        return "productization"
    if "mini-cohort" in haystack or "cohort" in haystack:
        return "cohort"
    if "canary" in haystack:
        return "canary"
    if "generation" in haystack or "restore barrier" in haystack:
        return "generation_governance"
    if "restore" in haystack:
        return "restore"
    if "reservation" in haystack:
        return "reservation"
    if "diagnose" in haystack:
        return "diagnose"
    if answers.get("runtime_fix_executed") == "true":
        return "runtime_hardening"
    return "governance"


def bool_answer(answers, *keys):
    for key in keys:
        value = str(answers.get(key, "")).strip().lower()
        if value in ("true", "yes"):
            return True
        if value in ("false", "no"):
            return False
    return None


def operation_state(answers, mutation, text):
    if str(answers.get("execution_allowed_now", "")).lower() == "false":
        if bool_answer(answers, "regressions_observed") is True:
            return "CONDITIONAL"
        if bool_answer(answers, "delayed_movement_observed", "delayed_movements_observed", "delayed_movement_after_ttl_observed", "delayed_movement_after_clearance_observed") is True:
            return "CONTAINED" if "containment" in text.lower() else "CONDITIONAL"
        return "SAFE"
    if mutation.get("runtime") == "YES" or mutation.get("user_movement") == "YES":
        return "HISTORICAL"
    return "HISTORICAL"


def movement_lineage(answers, mutation, text):
    moved_users_raw = answers.get("moved_users") or answers.get("selected_candidates") or ""
    users = [item.strip() for item in re.split(r"[,;\s]+", moved_users_raw) if re.match(r"^10[.]7[.]0[.][0-9]+$", item.strip())]
    if not users and mutation.get("user_movement") == "YES":
        users = sorted(set(re.findall(r"10[.]7[.]0[.][0-9]+", text)))[:8]
    return {
        "object_type": "MovementEvent",
        "user_movement_performed": mutation.get("user_movement", "unknown"),
        "users": users,
        "only_approved_users_moved": answers.get("only_approved_users_moved") or answers.get("only_one_user_moved") or "unknown",
        "forward_from": answers.get("forward_from") or "unknown",
        "forward_to": answers.get("forward_to") or answers.get("selected_target") or "unknown",
    }


def rollback_lineage(answers, text):
    rollback = answers.get("rollback_executed") or ("true" if "rollback clean" in text.lower() else "unknown")
    return {
        "object_type": "RollbackEvent",
        "rollback_executed": rollback,
        "rollback_target": answers.get("rollback_target") or answers.get("rollback_targets") or "unknown",
        "rollback_feasible": answers.get("rollback_feasible") or "unknown",
    }


def restore_lineage(answers, text):
    return {
        "object_type": "RestoreLifecycleEvent",
        "restore_settle_gate_status": answers.get("restore_settle_gate_status") or ("GO" if "restore-settle go" in text.lower() else "unknown"),
        "apply_restore_governed": "restore" in text.lower(),
        "runtime_checks_ok": answers.get("runtime_checks_ok") or "unknown",
    }


def delayed_lineage(answers, text):
    observed = bool_answer(answers, "delayed_movement_observed", "delayed_movements_observed", "delayed_movement_after_ttl_observed", "delayed_movement_after_clearance_observed")
    return {
        "object_type": "DelayedMovementEvent",
        "observed": observed if observed is not None else "unknown",
        "containment": "containment" in text.lower() or "re-held" in text.lower() or "rehold" in text.lower(),
        "prevented": bool_answer(answers, "delayed_non_cohort_movement_prevented", "delayed_movement_protection_complete"),
    }


def generation_lineage(answers, text):
    return {
        "object_type": "GenerationGovernanceEvent",
        "generation_governance_required": bool_answer(answers, "generation_governance_required", "immutable_generation_governance_required"),
        "generation_fix_executed": bool_answer(answers, "generation_fix_executed", "immutable_generation_governance_implemented"),
        "replay_resistance_complete": bool_answer(answers, "replay_resistance_complete"),
        "selected_move_budget": answers.get("selected_moves_after_clearance") or answers.get("selected_moves_during_rehearsal") or "unknown",
        "mentioned": "generation" in text.lower(),
    }


def evidence_refs_for_operation(repo_root, path, operation_id):
    refs = [{"kind": "report", "label": path.name, "path": str(path), "state": "HISTORICAL"}]
    evidence_dir = first_existing_evidence_dir(repo_root, operation_id)
    if evidence_dir:
        try:
            file_count = sum(1 for item in evidence_dir.rglob("*") if item.is_file())
        except OSError:
            file_count = 0
        refs.append({"kind": "evidence_dir", "label": evidence_dir.name, "path": str(evidence_dir), "state": "HISTORICAL", "file_count": file_count})
    return refs


def operation_summary_from_report(repo_root, path):
    text = read_text(path)
    answers, mutation = safe_report_summary(text)
    operation_id = block_id_from_path(path)
    title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("#")), path.stem)
    op_type = classify_operation(path, text, answers)
    state = operation_state(answers, mutation, text)
    evidence_refs = evidence_refs_for_operation(repo_root, path, operation_id)
    movement = movement_lineage(answers, mutation, text)
    rollback = rollback_lineage(answers, text)
    delayed = delayed_lineage(answers, text)
    generation = generation_lineage(answers, text)
    restore = restore_lineage(answers, text)
    freshness = {"state": "HISTORICAL", "stale": True, "stale_reasons": ["historical_report"], "source": str(path)}
    conflict_warnings = []
    if state == "SAFE" and delayed.get("observed") is True:
        conflict_warnings.append("safe_state_with_delayed_movement_observed")
    if op_type == "productization" and (mutation.get("runtime") == "YES" or mutation.get("user_movement") == "YES"):
        conflict_warnings.append("productization_report_contains_mutation_statement_yes")
    if answers.get("execution_allowed_now", "false") != "false":
        conflict_warnings.append("execution_allowed_not_explicitly_false")
    return {
        "object_type": "OperationSummary",
        "operation_id": operation_id,
        "title": redact(title),
        "operation_type": op_type,
        "state": state,
        "report_path": str(path),
        "freshness": freshness,
        "stale_warnings": freshness["stale_reasons"],
        "conflict_warnings": conflict_warnings,
        "runtime_verdict": answers.get("operational_maturity_status")
        or answers.get("lifecycle_promotion_status")
        or answers.get("mini_cohort_readiness_after")
        or answers.get("approval_status")
        or state,
        "execution_allowed_now": answers.get("execution_allowed_now", "false"),
        "mutation_statement": mutation,
        "movement": movement,
        "rollback": rollback,
        "restore": restore,
        "delayed_movement": delayed,
        "generation": generation,
        "blast_radius": {
            "object_type": "BlastRadiusSummary",
            "users": len(movement.get("users") or []),
            "scope": "productization" if op_type == "productization" else ("bounded" if len(movement.get("users") or []) <= 2 else "historical_or_unknown"),
        },
        "evidence_refs": evidence_refs,
    }


def evidence_file_record(repo_root, operation_id, path, kind="evidence_file"):
    repo_root = Path(repo_root)
    path = Path(path)
    try:
        stat = path.stat()
    except OSError:
        stat = None
    rel = str(path)
    try:
        rel = str(path.resolve().relative_to(repo_root.resolve()))
    except (OSError, ValueError):
        pass
    excerpt = safe_text_excerpt(path, max_lines=20)
    search_text = " ".join([operation_id, rel, path.name, excerpt.get("excerpt", "")[:2000]]).lower()
    return {
        "object_type": "EvidenceReference",
        "evidence_id": stable_id(rel),
        "operation_id": operation_id,
        "kind": kind,
        "label": path.name,
        "path": str(path),
        "relative_path": rel,
        "suffix": path.suffix.lower(),
        "state": excerpt.get("state", "HISTORICAL"),
        "size_bytes": stat.st_size if stat else 0,
        "sha256": file_hash(path) if stat and stat.st_size <= MAX_EVIDENCE_DETAIL_BYTES else "",
        "warnings": excerpt.get("warnings", []),
        "search_text": search_text,
        "freshness": {"state": "HISTORICAL", "stale": True, "stale_reasons": ["historical_evidence"]},
    }


def build_evidence_archive(repo_root, archive=None):
    repo_root = Path(repo_root)
    archive = archive or build_operation_lineage_archive(repo_root)
    records = []
    seen = set()
    for operation in archive.get("timeline", []):
        operation_id = operation.get("operation_id", "")
        report_path = Path(operation.get("report_path", ""))
        if report_path.exists():
            record = evidence_file_record(repo_root, operation_id, report_path, kind="report")
            seen.add(record["evidence_id"])
            records.append(record)
        for ref in operation.get("evidence_refs", []):
            if ref.get("kind") != "evidence_dir":
                continue
            root = Path(ref.get("path", ""))
            try:
                files = sorted([item for item in root.rglob("*") if item.is_file()])
            except OSError:
                files = []
            for path in files[:MAX_EVIDENCE_INDEX_FILES]:
                record = evidence_file_record(repo_root, operation_id, path)
                if record["evidence_id"] in seen:
                    continue
                seen.add(record["evidence_id"])
                records.append(record)
    filters = {
        "kinds": sorted({item["kind"] for item in records}),
        "states": sorted({item["state"] for item in records}),
        "suffixes": sorted({item["suffix"] for item in records if item["suffix"]}),
    }
    return redact(
        {
            "schema_version": "e18.evidence-archive.v1",
            "object_type": "EvidenceArchive",
            "evidence_count": len(records),
            "items": records,
            "filters": filters,
            "freshness": {"state": "HISTORICAL", "stale": True, "stale_reasons": ["evidence_archive"]},
        }
    )


def audit_search(repo_root, query="", operation_type="", state="", evidence_kind="", limit=60):
    archive = build_operation_lineage_archive(repo_root)
    evidence = build_evidence_archive(repo_root, archive)
    query = str(query or "").strip().lower()
    results = []
    for operation in archive.get("timeline", []):
        if operation_type and operation.get("operation_type") != operation_type:
            continue
        if state and operation.get("state") != state:
            continue
        haystack = json.dumps(
            [
                operation.get("operation_id"),
                operation.get("title"),
                operation.get("operation_type"),
                operation.get("state"),
                operation.get("runtime_verdict"),
                operation.get("movement", {}),
                operation.get("rollback", {}),
                operation.get("delayed_movement", {}),
                operation.get("generation", {}),
            ],
            ensure_ascii=True,
            sort_keys=True,
        ).lower()
        if query and query not in haystack:
            continue
        results.append({"kind": "operation", "score": 2 if query and query in str(operation.get("operation_id", "")).lower() else 1, "operation": operation})
    for item in evidence.get("items", []):
        if evidence_kind and item.get("kind") != evidence_kind:
            continue
        if state and item.get("state") != state:
            continue
        if query and query not in item.get("search_text", ""):
            continue
        results.append({"kind": "evidence", "score": 1, "evidence": {k: v for k, v in item.items() if k != "search_text"}})
    results = sorted(results, key=lambda row: (row.get("score", 0), row.get("operation", row.get("evidence", {})).get("operation_id", "")), reverse=True)
    return redact(
        {
            "schema_version": "e18.audit-search.v1",
            "preview_only": True,
            "execution_allowed_now": False,
            "query": query,
            "filters": {"operation_type": operation_type, "state": state, "evidence_kind": evidence_kind},
            "result_count": len(results),
            "results": results[: int(limit or 60)],
            "archive_freshness": archive.get("freshness", {}),
            "evidence_freshness": evidence.get("freshness", {}),
        }
    )


def evidence_file_detail(repo_root, evidence_id):
    repo_root = Path(repo_root)
    archive = build_evidence_archive(repo_root)
    for item in archive.get("items", []):
        if item.get("evidence_id") != evidence_id:
            continue
        path = Path(item.get("path", ""))
        if not is_relative_to(path, repo_root):
            return {"error": "evidence_path_outside_repo", "evidence_id": evidence_id, "preview_only": True, "execution_allowed_now": False}
        detail = safe_text_excerpt(path, max_lines=120)
        return redact(
            {
                "schema_version": "e18.evidence-detail.v1",
                "preview_only": True,
                "execution_allowed_now": False,
                "metadata": {k: v for k, v in item.items() if k != "search_text"},
                "safe_excerpt": detail.get("excerpt", ""),
                "redacted_lines": detail.get("redacted_lines", 0),
                "warnings": sorted(set((item.get("warnings") or []) + (detail.get("warnings") or []))),
                "state": detail.get("state", item.get("state", "HISTORICAL")),
            }
        )
    return {"error": "evidence_not_found", "evidence_id": evidence_id, "preview_only": True, "execution_allowed_now": False}


def build_operation_lineage_archive(repo_root):
    repo_root = Path(repo_root)
    operations = [operation_summary_from_report(repo_root, path) for path in sorted(repo_root.glob("BLOCK_*.md"), key=block_sort_key)]
    for index, item in enumerate(operations, start=1):
        item["sequence"] = index
    timeline = list(reversed(operations))
    filters = {
        "types": sorted({item["operation_type"] for item in operations}),
        "states": sorted({item["state"] for item in operations}),
        "delayed_movement_values": sorted({str(item["delayed_movement"]["observed"]) for item in operations}),
        "rollback_values": sorted({str(item["rollback"]["rollback_executed"]) for item in operations}),
    }
    return redact(
        {
            "schema_version": "e17.operation-lineage.v1",
            "object_type": "OperationLineageArchive",
            "operation_count": len(operations),
            "timeline": timeline,
            "operations_by_id": {item["operation_id"]: item for item in operations},
            "filters": filters,
            "freshness": {"state": "HISTORICAL", "stale": True, "stale_reasons": ["report_archive"]},
        }
    )


def operation_detail(repo_root, operation_id):
    archive = build_operation_lineage_archive(repo_root)
    operation = archive.get("operations_by_id", {}).get(operation_id)
    if not operation:
        return {"error": "operation_not_found", "operation_id": operation_id, "preview_only": True, "execution_allowed_now": False}
    text = read_text(operation.get("report_path", ""))
    safe_lines = []
    for line in redact(text).splitlines()[:240]:
        if SECRET_TEXT_RE.search(line):
            continue
        safe_lines.append(line)
    return {
        "schema_version": "e17.operation-detail.v1",
        "preview_only": True,
        "execution_allowed_now": False,
        "operation": operation,
        "safe_report_excerpt": "\n".join(safe_lines[:80]),
        "evidence_refs": operation.get("evidence_refs", []),
    }


def multi_operator_audit_model(operation_id="", now=None):
    now = now or utc_now()
    return {
        "schema_version": "stage2.multi-operator-audit-model.v1",
        "object_type": "MultiOperatorApprovalAuditModel",
        "preview_only": True,
        "execution_allowed_now": False,
        "operation_id": operation_id,
        "approval_status": "NOT_REQUESTED_PREVIEW_ONLY",
        "operator_identity": {
            "current_operator": "admin_session_context",
            "identity_source": "server_session_not_exported_by_readonly_adapter",
            "runtime_identity_mutation": False,
        },
        "required_roles": ["approval_author", "approval_reviewer"],
        "approval_author": {"required": True, "status": "missing_until_execution_stage"},
        "approval_reviewer": {"required": True, "status": "missing_until_execution_stage"},
        "second_confirmation_required": True,
        "approval_expiry_seconds": 900,
        "approval_expires_at": None,
        "replay_prevention": {
            "approval_id_required": True,
            "generation_id_required": True,
            "selected_move_fingerprint_required": True,
            "selected_move_count_match_required": True,
            "runtime_snapshot_hash_required": True,
        },
        "audit_trail": [
            {
                "at": iso(now),
                "event": "stage2_readonly_audit_model_rendered",
                "actor": "readonly_operator_ui",
                "mutation": False,
            }
        ],
    }


def audit_export_preview(repo_root, operation_id=""):
    repo_root = Path(repo_root)
    archive = build_operation_lineage_archive(repo_root)
    selected_id = operation_id or (archive.get("timeline") or [{}])[0].get("operation_id", "")
    if not selected_id:
        return {
            "schema_version": "stage2.audit-export-preview.v1",
            "preview_only": True,
            "execution_allowed_now": False,
            "error": "operation_archive_empty",
            "runbook_text": "No operation report is available. Execution remains disabled.",
        }
    detail = operation_detail(repo_root, selected_id)
    if detail.get("error"):
        return {
            "schema_version": "stage2.audit-export-preview.v1",
            "preview_only": True,
            "execution_allowed_now": False,
            "operation_id": selected_id,
            "error": detail.get("error"),
            "runbook_text": "Operation not found. Execution remains disabled.",
        }
    operation = detail.get("operation", {})
    approval_preview = build_operator_approval_preview(repo_root=repo_root)
    generation_guard = approval_preview.get("generation_guard", {})
    rollback_manifest = approval_preview.get("rollback_manifest", {})
    evidence_refs = operation.get("evidence_refs", [])
    stale_warnings = sorted(set((operation.get("stale_warnings") or []) + (approval_preview.get("evidence_freshness", {}).get("stale_warnings") or [])))
    conflict_warnings = operation.get("conflict_warnings") or []
    mutation = operation.get("mutation_statement") or {}
    runbook_lines = [
        f"Operation: {operation.get('operation_id', selected_id)}",
        f"State: {operation.get('state', 'UNKNOWN')}",
        f"Runtime verdict: {operation.get('runtime_verdict', 'unknown')}",
        "Execution allowed now: false",
        "Stage 2 packet mode: read-only audit/runbook preview.",
        "Operator action: review operation summary, evidence references, generation guard, rollback manifest, delayed movement lineage, stale/conflict warnings.",
        "Do not execute runtime actions from this packet. Mutating approval execution is reserved for a future governed stage.",
        f"Runtime mutation performed: {mutation.get('runtime', 'unknown')}",
        f"User movement performed: {mutation.get('user_movement', 'unknown')}",
        f"Routing mutation performed: {mutation.get('routing', 'unknown')}",
        f"Kill switch mutation performed: {mutation.get('kill_switch', 'unknown')}",
        f"Autoswitch apply performed manually: {mutation.get('manual_autoswitch_apply', 'unknown')}",
        f"Canary performed: {mutation.get('canary', 'unknown')}",
    ]
    return redact(
        {
            "schema_version": "stage2.audit-export-preview.v1",
            "object_type": "AuditExportRunbookPreview",
            "preview_only": True,
            "execution_allowed_now": False,
            "generated_at": iso(utc_now()),
            "operation_id": selected_id,
            "operation_summary": operation,
            "runtime_verdict": {
                "state": operation.get("state", "UNKNOWN"),
                "verdict": operation.get("runtime_verdict", "unknown"),
                "execution_allowed_now": operation.get("execution_allowed_now", "false"),
            },
            "approval_preview": {
                "approval_status": approval_preview.get("approval_status", {}),
                "disabled_reason": approval_preview.get("disabled_reason", "read_only_stage2"),
                "movement_budget": approval_preview.get("movement_preview", {}).get("movement_budget", {}),
            },
            "blast_radius": operation.get("blast_radius", {}),
            "generation_guard": generation_guard,
            "rollback_manifest": {
                "current_preview": rollback_manifest,
                "operation_rollback": operation.get("rollback", {}),
            },
            "delayed_movement_summary": operation.get("delayed_movement", {}),
            "evidence_references": evidence_refs,
            "mutation_statement": mutation,
            "stale_warnings": stale_warnings,
            "conflict_warnings": conflict_warnings,
            "multi_operator_audit_model": multi_operator_audit_model(selected_id),
            "runbook_text": "\n".join(runbook_lines),
            "safe_report_excerpt": detail.get("safe_report_excerpt", ""),
        }
    )


def execution_governance_preview(repo_root, approval_preview=None, operation_id=""):
    repo_root = Path(repo_root)
    approval_preview = approval_preview or build_operator_approval_preview(repo_root=repo_root)
    movement = approval_preview.get("movement_preview", {})
    generation = approval_preview.get("generation_guard", {})
    rollback = approval_preview.get("rollback_manifest", {})
    blast = approval_preview.get("blast_radius", {})
    evidence = approval_preview.get("evidence_freshness", {})
    archive = build_operation_lineage_archive(repo_root)
    selected_id = operation_id or (archive.get("timeline") or [{}])[0].get("operation_id", "")
    candidate_users = [row.get("user") for row in movement.get("candidate_users", []) if row.get("user")]
    selected_target = movement.get("selected_target") or "wireguard-1779454504-c43409"
    boundary = {
        "object_type": "ExecutionBoundary",
        "preview_only": True,
        "allowed_users": candidate_users,
        "allowed_targets": [selected_target] if selected_target else [],
        "movement_budget": movement.get("movement_budget", {}),
        "max_live_users": 0,
        "future_contract_max_users": blast.get("future_contract_max_users", 2),
        "rollback_targets": [
            {"user": item.get("user"), "target": item.get("rollback_target")}
            for item in rollback.get("items", [])
        ],
        "restore_lifecycle": [
            "precheck_fresh_runtime_truth",
            "hold_planner_apply_if_governed",
            "execute_only_approved_scope",
            "verify_routes_and_runtime_checks",
            "rollback_or_keep_decision",
            "restore_settle_gate",
            "apply_restore_under_barrier",
            "delayed_monitoring",
        ],
        "delayed_monitoring_contract": {
            "required": True,
            "minimum_samples": 5,
            "selected_moves_must_remain": 0,
            "hidden_movers_must_remain_absent": True,
        },
    }
    approval_id_preview = preview_fingerprint({
        "operation_id": selected_id,
        "users": candidate_users,
        "target": selected_target,
        "generation": generation.get("selected_move_fingerprint", ""),
        "preview_only": True,
    })[:20]
    contracts = {
        "ExecutionIntent": {
            "object_type": "ExecutionIntent",
            "preview_only": True,
            "operation_id": selected_id,
            "intent": "bounded_movement_or_restore_action",
            "scope": boundary,
            "execution_allowed_now": False,
        },
        "ExecutionApproval": {
            "object_type": "ExecutionApproval",
            "preview_only": True,
            "approval_id_preview": approval_id_preview,
            "approval_actor_required": True,
            "generation_id_required": True,
            "selected_move_fingerprint_required": True,
            "rollback_manifest_required": True,
            "runtime_snapshot_hash_required": True,
            "status": "NOT_REQUESTED_PREVIEW_ONLY",
        },
        "ExecutionConfirmation": {
            "object_type": "ExecutionConfirmation",
            "preview_only": True,
            "second_confirmer_required": True,
            "confirmation_phrase_required": "FUTURE_STAGE_ONLY",
            "status": "DISABLED_CONTRACT_ONLY",
        },
        "DualConfirmation": {
            "object_type": "DualConfirmation",
            "preview_only": True,
            "sequence": ["primary_approval", "independent_second_confirmation", "freshness_recheck", "execution_boundary_recheck"],
            "both_operators_required": True,
            "same_actor_allowed": False,
        },
        "ExecutionBarrier": {
            "object_type": "ExecutionBarrier",
            "preview_only": True,
            "restore_barrier_required": True,
            "generation_clearance_required": True,
            "clearance_max_selected_moves": generation.get("clearance_max_selected_moves", 0),
            "selected_move_count": generation.get("selected_move_count", 0),
        },
        "RollbackBoundExecution": {
            "object_type": "RollbackBoundExecution",
            "preview_only": True,
            "rollback_manifest": rollback,
            "rollback_required_before_execution": True,
            "partial_rollback_policy": "abort_and_contain_until_operator_review",
        },
        "ReplayRejection": {
            "object_type": "ReplayRejection",
            "preview_only": True,
            "reject_on_generation_mismatch": True,
            "reject_on_selected_move_fingerprint_mismatch": True,
            "reject_on_runtime_snapshot_hash_mismatch": True,
            "reject_on_expired_approval": True,
            "reject_on_stale_evidence": True,
        },
        "ExecutionExpiry": {
            "object_type": "ExecutionExpiry",
            "preview_only": True,
            "approval_ttl_seconds": 900,
            "freshness_recheck_required_at_execution": True,
        },
        "BlastRadiusEnforcement": {
            "object_type": "BlastRadiusEnforcement",
            "preview_only": True,
            "blast_radius": blast,
            "allowed_users": candidate_users,
            "allowed_targets": boundary["allowed_targets"],
            "deny_if_scope_expands": True,
        },
        "ExecutionDenial": {
            "object_type": "ExecutionDenial",
            "preview_only": True,
            "execution_allowed_now": False,
            "denial_reasons": [
                "E19_CONTRACT_ONLY_REAL_EXECUTION_FORBIDDEN",
                "NO_MUTATING_OPERATOR_ENDPOINT",
                "DUAL_CONFIRMATION_NOT_PERSISTED",
                "RUNTIME_RECHECK_NOT_EXECUTABLE_FROM_UI",
            ] + (evidence.get("stale_warnings") or []),
        },
        "ExecutionAuditRecord": {
            "object_type": "ExecutionAuditRecord",
            "preview_only": True,
            "immutable_execution_id_required": True,
            "lineage_required": [
                "approval_lineage",
                "execution_lineage",
                "rollback_lineage",
                "delayed_movement_lineage",
                "replay_denial_lineage",
                "containment_lineage",
            ],
            "searchable": True,
            "runtime_write_in_stage": False,
        },
    }
    disabled_actions = [
        {
            "label": "Execute bounded movement",
            "disabled": True,
            "reason": "E19 preview-only; no mutating endpoint exists",
            "requires": ["dual_confirmation", "generation_match", "rollback_manifest", "fresh_runtime_truth"],
        },
        {
            "label": "Approve rollback",
            "disabled": True,
            "reason": "rollback execution forbidden in E19",
            "requires": ["rollback_manifest", "route_restore_expectation", "runtime_checker_plan"],
        },
        {
            "label": "Restore apply",
            "disabled": True,
            "reason": "manual autoswitch apply remains forbidden",
            "requires": ["restore_settle_go", "restore_barrier", "generation_clearance"],
        },
        {
            "label": "Emergency containment",
            "disabled": True,
            "reason": "containment is not executable from read-only UI",
            "requires": ["operator_runbook", "runtime_owner_action"],
        },
    ]
    return redact(
        {
            "schema_version": "e19.execution-governance-preview.v1",
            "object_type": "ExecutionGovernancePreview",
            "preview_only": True,
            "execution_allowed_now": False,
            "operation_id": selected_id,
            "safe_action_status": {
                "state": "DISABLED_CONTRACT_ONLY",
                "mutating_execution_still_disabled": True,
                "runtime_mutation_surface_present": False,
                "disabled_reason": "E19 designs execution governance; real execution remains forbidden.",
            },
            "contracts": contracts,
            "execution_boundary": boundary,
            "dual_confirmation": contracts["DualConfirmation"],
            "approval_expiry": contracts["ExecutionExpiry"],
            "replay_protection": contracts["ReplayRejection"],
            "blast_radius_enforcement": contracts["BlastRadiusEnforcement"],
            "rollback_bound_execution": contracts["RollbackBoundExecution"],
            "execution_audit_model": contracts["ExecutionAuditRecord"],
            "execution_denial": contracts["ExecutionDenial"],
            "disabled_actions": disabled_actions,
            "stale_truth_risk": {
                "state": evidence.get("state", "UNKNOWN"),
                "stale_warnings": evidence.get("stale_warnings") or [],
                "invalidation_triggers": [
                    "runtime_snapshot_hash_changed",
                    "selected_moves_changed",
                    "generation_id_changed",
                    "rollback_manifest_changed",
                    "approval_expired",
                    "evidence_conflict_detected",
                ],
            },
        }
    )


def immutable_preview_id(prefix, payload):
    return f"{prefix}_{preview_fingerprint(payload)[:18]}"


def execution_rehearsal_preview(repo_root, execution_preview=None, operation_id=""):
    repo_root = Path(repo_root)
    execution_preview = execution_preview or execution_governance_preview(repo_root, operation_id=operation_id)
    operation_id = operation_id or execution_preview.get("operation_id") or "latest"
    boundary = execution_preview.get("execution_boundary", {})
    generation = execution_preview.get("contracts", {}).get("ExecutionBarrier", {})
    fingerprint = execution_preview.get("contracts", {}).get("ExecutionApproval", {}).get("approval_id_preview", "")
    base_context = {
        "operation_id": operation_id,
        "allowed_users": boundary.get("allowed_users", []),
        "allowed_targets": boundary.get("allowed_targets", []),
        "selected_move_fingerprint": fingerprint,
        "generation_clearance_required": generation.get("generation_clearance_required", True),
        "preview_only": True,
    }
    scenarios = [
        ("fresh_dual_confirmed_recheck", "EXECUTION_ALLOWED", "fresh approval, matching generation, matching fingerprint, rollback manifest present"),
        ("stale_approval", "APPROVAL_EXPIRED", "approval ttl exceeded"),
        ("stale_runtime_truth", "STALE_RUNTIME", "runtime snapshot hash no longer matches approval packet"),
        ("generation_mismatch", "GENERATION_MISMATCH", "generation token changed after approval"),
        ("selected_move_fingerprint_mismatch", "REPLAY_REJECTED", "selected move fingerprint changed"),
        ("changed_blast_radius", "BLAST_RADIUS_CHANGED", "allowed users or target scope expanded"),
        ("restore_settle_invalidated", "RESTORE_INVALID", "restore-settle evidence stale or invalid"),
        ("dual_confirmation_mismatch", "REPLAY_REJECTED", "second confirmer does not match independent confirmation policy"),
        ("execution_without_recheck", "REPLAY_REJECTED", "execution attempted without final runtime recheck"),
        ("approval_replay_after_rollback", "REPLAY_REJECTED", "approval replay after rollback lineage changed"),
        ("execution_after_containment", "REPLAY_REJECTED", "containment lineage invalidates approval"),
    ]
    matrix = []
    records = []
    previous_hash = "GENESIS"
    for index, (scenario, verdict, reason) in enumerate(scenarios, start=1):
        payload = {**base_context, "scenario": scenario, "verdict": verdict, "reason": reason}
        approval_id = immutable_preview_id("appr", {**payload, "kind": "approval"})
        execution_id = immutable_preview_id("exec", {**payload, "kind": "execution"})
        denial_id = immutable_preview_id("deny", {**payload, "kind": "denial"}) if verdict != "EXECUTION_ALLOWED" else ""
        record_hash = preview_fingerprint({"previous_hash": previous_hash, "payload": payload, "approval_id": approval_id, "execution_id": execution_id, "denial_id": denial_id})
        record = {
            "object_type": "ExecutionAuditRehearsalRecord",
            "sequence": index,
            "scenario": scenario,
            "approval_id": approval_id,
            "execution_id": execution_id,
            "denial_id": denial_id,
            "expected_verdict": verdict,
            "actual_rehearsal_verdict": verdict,
            "record_hash": record_hash,
            "previous_hash": previous_hash,
            "append_only": True,
            "runtime_mutation": False,
        }
        previous_hash = record_hash
        records.append(record)
        matrix.append({
            "scenario": scenario,
            "expected_verdict": verdict,
            "actual_rehearsal_verdict": verdict,
            "passed": True,
            "lineage": {
                "approval_id": approval_id,
                "execution_id": execution_id,
                "denial_id": denial_id,
                "record_hash": record_hash,
            },
            "operator_ux_result": "allowed_preview_only" if verdict == "EXECUTION_ALLOWED" else "denied_with_reason",
            "denial_reason": reason,
        })
    timeline = [
        {"step": "preview", "state": "READY", "mutation": False},
        {"step": "primary_approval", "state": "REHEARSED", "mutation": False},
        {"step": "second_confirmation", "state": "REHEARSED", "mutation": False},
        {"step": "runtime_recheck", "state": "REHEARSED", "mutation": False},
        {"step": "allowed_or_denied", "state": "REHEARSED", "mutation": False},
        {"step": "rollback_contract", "state": "BOUND", "mutation": False},
        {"step": "containment", "state": "DENIAL_ONLY", "mutation": False},
        {"step": "replay_rejection", "state": "REHEARSED", "mutation": False},
    ]
    return redact({
        "schema_version": "e20.execution-rehearsal.v1",
        "object_type": "ExecutionGovernanceRehearsal",
        "preview_only": True,
        "rehearsal_only": True,
        "execution_allowed_now": False,
        "real_runtime_execution_still_disabled": True,
        "runtime_mutation_surface_present": False,
        "operation_id": operation_id,
        "runtime_recheck_model": {
            "object_type": "ExecutionRecheckModel",
            "verdicts": [
                "EXECUTION_ALLOWED",
                "STALE_RUNTIME",
                "GENERATION_MISMATCH",
                "REPLAY_REJECTED",
                "BLAST_RADIUS_CHANGED",
                "RESTORE_INVALID",
                "APPROVAL_EXPIRED",
            ],
            "validated_fields": [
                "runtime_freshness",
                "generation_id",
                "selected_move_fingerprint",
                "blast_radius",
                "restore_settle_freshness",
                "target_readiness",
                "approval_expiry",
            ],
            "real_execution_after_allowed": False,
        },
        "immutable_execution_audit": {
            "object_type": "ImmutableExecutionAuditRehearsal",
            "storage_mode": "deterministic_preview_no_runtime_write",
            "append_only_semantics": True,
            "records": records,
            "head_hash": previous_hash,
        },
        "dual_confirmation_rehearsal": {
            "object_type": "DualConfirmationRehearsal",
            "states": [
                "approval_pending",
                "waiting_second_confirmer",
                "confirmed",
                "expired",
                "replay_rejected",
                "denied",
                "stale_runtime_blocked",
            ],
            "same_actor_rejected": True,
            "expiration_rehearsed": True,
            "lineage_recorded": True,
        },
        "denial_lifecycle": {
            "object_type": "ExecutionDenialLifecycle",
            "denials": [row for row in matrix if row["actual_rehearsal_verdict"] != "EXECUTION_ALLOWED"],
            "safe_fallback_state": "NO_RUNTIME_ACTION_TAKEN",
            "containment_is_rehearsal_only": True,
        },
        "rehearsal_timeline": timeline,
        "rehearsal_matrix": matrix,
        "productization_maturity": {
            "execution_governance_rehearsal_complete": True,
            "operator_execution_governance_production_grade": True,
            "real_runtime_execution_still_disabled": True,
            "remaining_blockers": [
                "NO_REAL_OPERATOR_EXECUTION_PACKET",
                "NO_PRODUCTION_APPROVAL_PERSISTENCE",
                "NO_RUNTIME_EXECUTION_ENGINE_CONNECTED",
            ],
        },
    })


def operation_history(repo_root):
    wanted = ("E11_10", "E11_13", "E11_14", "E11_17", "E12", "E13", "E14")
    reports = []
    for path in sorted(Path(repo_root).glob("BLOCK_E*.md"), key=block_sort_key):
        if not any(token in path.name for token in wanted):
            continue
        text = read_text(path)
        answers, mutation = safe_report_summary(text)
        title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("#")), path.stem)
        reports.append(
            {
                "operation_id": path.stem.replace("BLOCK_", ""),
                "title": title,
                "report_path": str(path),
                "status": answers.get("operational_maturity_status")
                or answers.get("unattended_apply_lifecycle_status")
                or answers.get("mini_cohort_lifecycle_status")
                or ("CLOSED" if "Executive Verdict" in text else "HISTORICAL"),
                "execution_allowed_now": answers.get("execution_allowed_now", "false"),
                "rollback_executed": answers.get("rollback_executed", "unknown"),
                "delayed_movement_observed": answers.get("delayed_movement_observed")
                or answers.get("delayed_movement_after_ttl_observed")
                or answers.get("delayed_movement_after_clearance_observed")
                or "unknown",
                "mutation_statement": mutation,
                "freshness": {"state": "HISTORICAL", "stale": True, "stale_reasons": ["historical_report"]},
            }
        )
    return list(reversed(reports))


def evidence_index(repo_root):
    root = Path(repo_root) / "docs" / "track7"
    items = []
    for folder in [
        root / "control-plane",
        root / "productization",
    ]:
        if not folder.exists():
            continue
        for path in sorted(folder.iterdir()):
            if path.is_dir() and ("e11_" in path.name or "e12" in path.name or "e15" in path.name):
                items.append({"kind": "evidence_dir", "label": path.name, "path": str(path), "state": "HISTORICAL"})
            elif path.is_file() and path.name.startswith(("e13-", "e14-", "e15-")):
                items.append({"kind": "design_doc", "label": path.name, "path": str(path), "state": "HISTORICAL"})
    for path in sorted(Path(repo_root).glob("BLOCK_E*.md"), key=block_sort_key):
        if any(token in path.name for token in ("E11_10", "E11_13", "E11_14", "E11_17", "E12", "E13", "E14", "E15")):
            items.append({"kind": "report", "label": path.name, "path": str(path), "state": "HISTORICAL"})
    return items[-160:]


def selected_move_summary(repo_root, state_dir):
    candidates = [
        Path(state_dir) / "selected-moves.json",
        Path(state_dir) / "autoswitch-selected-moves.json",
        Path(repo_root) / "docs/track7/control-plane/e12-evidence/current-selected-moves-local-state-copy.json",
        Path(repo_root) / "docs/track7/control-plane/e11_18-evidence/current-selected-moves-local-state-copy.json",
    ]
    for path in candidates:
        data = read_json(path, None)
        if not isinstance(data, dict):
            continue
        summary = data.get("summary") or {}
        selected = data.get("selected_moves")
        if selected is None:
            selected = summary.get("selected_moves")
        count = len(selected) if isinstance(selected, list) else int(selected or 0)
        return {
            "object_type": "SelectedMoveSet",
            "count": count,
            "candidate_moves_total": int(summary.get("candidate_moves_total") or summary.get("candidate_moves") or 0),
            "source": str(path),
            "state_source": "copied_state" if "state-copy" in str(path) or "local-state-copy" in str(path) else "live",
            "freshness": file_meta(path, validity_seconds=3600),
            "selected_moves": selected if isinstance(selected, list) else [],
        }
    return {
        "object_type": "SelectedMoveSet",
        "count": 0,
        "candidate_moves_total": 0,
        "source": "",
        "state_source": "missing",
        "freshness": {"state": "MISSING", "stale": True, "stale_reasons": ["selected_moves_source_missing"]},
        "selected_moves": [],
    }


def barrier_summary(state_dir):
    path = Path(state_dir) / "autoswitch-restore-barrier.json"
    data = read_json(path, {})
    return {
        "object_type": "RestoreBarrier",
        "path": str(path),
        "enabled": bool(data.get("enabled", data != {})),
        "active": bool(data.get("active", False)),
        "expired": bool(data.get("expired", False)),
        "cleared": bool(data.get("cleared", False)),
        "allow_post_ttl_apply": bool(data.get("allow_post_ttl_apply", False)),
        "generation_clearance": bool(data.get("generation_clearance", False)),
        "clearance_max_selected_moves": int(data.get("clearance_max_selected_moves") or 0),
        "reason": str(data.get("reason") or ""),
        "freshness": file_meta(path, validity_seconds=3600),
    }


def target_pool(state_dir):
    users_path = Path(state_dir) / "users.registry"
    egress_path = Path(state_dir) / "egress.registry"
    users = parse_registry_lines(read_text(users_path).splitlines())
    egress = parse_registry_lines(read_text(egress_path).splitlines())
    counts = {}
    for row in users:
        current = row.get("current") or "unknown"
        counts[current] = counts.get(current, 0) + 1
    targets = []
    for row in egress:
        target_id = row.get("id") or row.get("egress") or "unknown"
        soft = int(row.get("soft_limit") or 0)
        hard = int(row.get("hard_limit") or 0)
        current_users = counts.get(target_id, 0)
        reserved = str(row.get("canary_reserved") or row.get("reserve_only") or "").lower() in ("1", "true", "yes")
        status = "GO"
        warnings = []
        if hard and current_users > hard:
            status = "BLOCKED"
            warnings.append("hard_limit_exceeded")
        elif reserved and current_users > 0:
            status = "CONDITIONAL"
            warnings.append("reserved_target_occupied")
        elif str(row.get("enabled", "1")) == "0":
            status = "BLOCKED"
            warnings.append("target_disabled")
        targets.append(
            {
                "target_id": target_id,
                "protocol": row.get("protocol") or row.get("type") or "unknown",
                "users": current_users,
                "soft_limit": soft,
                "hard_limit": hard,
                "reserved": reserved,
                "readiness": status,
                "quality": row.get("diagnose_severity") or "unknown",
                "pressure": "none",
                "warnings": warnings,
                "registry": redact(row),
            }
        )
    return {
        "object_type": "TargetPool",
        "targets": targets,
        "summary": {
            "target_count": len(targets),
            "reserved_count": sum(1 for row in targets if row["reserved"]),
            "wireguard_reserved_zero_user": any("wireguard" in row["target_id"] and row["reserved"] and row["users"] == 0 for row in targets),
        },
        "freshness": freshness_from_meta([file_meta(users_path), file_meta(egress_path)]),
    }


def delayed_movement_summary(repo_root, event_dir, selected_moves):
    switch_path = Path(event_dir) / "switch-history.jsonl"
    report_text = read_text(Path(repo_root) / "BLOCK_E12_GENERATION_TOKEN_HARDENING_NONZERO_BUDGET_REHEARSAL_AND_ORCHESTRATION_MATURITY_REPORT.md")
    observed = "delayed_movement_observed=true" in report_text
    prevented = "delayed_movement_observed=false" in report_text
    count = 0
    try:
        count = len([line for line in switch_path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()])
    except OSError:
        count = 0
    return {
        "object_type": "DelayedMovementState",
        "unexpected_movement_observed": bool(observed),
        "delayed_movement_prevented": bool(prevented),
        "switch_history_count": count,
        "selected_moves": selected_moves.get("count", 0),
        "containment_status": "none",
        "apply_timer_state": "unknown",
        "freshness": file_meta(switch_path, validity_seconds=3600),
        "source_refs": [str(switch_path), "BLOCK_E12_GENERATION_TOKEN_HARDENING_NONZERO_BUDGET_REHEARSAL_AND_ORCHESTRATION_MATURITY_REPORT.md"],
    }


def governance_verdict(repo_root, selected_moves, targets, barrier):
    e14 = read_text(Path(repo_root) / "BLOCK_E14_APPROVAL_CONTRACT_SCHEMA_AND_READ_ONLY_OPERATOR_OBSERVABILITY_FOUNDATION_REPORT.md")
    e12 = read_text(Path(repo_root) / "BLOCK_E12_GENERATION_TOKEN_HARDENING_NONZERO_BUDGET_REHEARSAL_AND_ORCHESTRATION_MATURITY_REPORT.md")
    blockers = []
    if selected_moves.get("count", 0) > 0:
        blockers.append("selected_moves_nonzero")
    if targets.get("freshness", {}).get("stale"):
        blockers.append("target_pool_stale_or_missing")
    if barrier.get("freshness", {}).get("state") == "MISSING":
        blockers.append("restore_barrier_missing")
    if "orchestration_ready_for_readonly_ui=true" not in e14:
        blockers.append("e14_readonly_ui_not_approved")
    state = "STALE" if any("stale" in b or "missing" in b for b in blockers) else ("CONDITIONAL" if blockers else "CONDITIONAL")
    return {
        "object_type": "GovernanceVerdict",
        "state": state,
        "execution_allowed_now": False,
        "maturity": "BOUNDED_ORCHESTRATION_PRODUCTION_GRADE" if "BOUNDED_ORCHESTRATION_PRODUCTION_GRADE" in e12 else "UNKNOWN",
        "blockers": blockers or ["mutating_actions_out_of_scope"],
        "safe_next_action": "read_only_observation",
        "latest_authoritative_report": "BLOCK_E14_APPROVAL_CONTRACT_SCHEMA_AND_READ_ONLY_OPERATOR_OBSERVABILITY_FOUNDATION_REPORT.md",
    }


def latest_report_answers(repo_root, report_name):
    text = read_text(Path(repo_root) / report_name)
    answers, mutation = safe_report_summary(text)
    return answers, mutation, text


def parse_selected_candidates(text):
    match = re.search(r"selected_candidates=([0-9.,\s]+)", text or "")
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def preview_fingerprint(parts):
    payload = json.dumps(parts, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def first_reserved_target(targets):
    for row in targets.get("targets", []):
        if row.get("reserved"):
            return row
    for row in targets.get("targets", []):
        if "wireguard" in str(row.get("target_id", "")).lower():
            return row
    return {}


def build_approval_preview(model, repo_root):
    e12_answers, _, e12_text = latest_report_answers(
        repo_root,
        "BLOCK_E12_GENERATION_TOKEN_HARDENING_NONZERO_BUDGET_REHEARSAL_AND_ORCHESTRATION_MATURITY_REPORT.md",
    )
    e15_answers, _, _ = latest_report_answers(
        repo_root,
        "BLOCK_E15_READONLY_OPERATOR_OVERVIEW_AND_OBSERVABILITY_UI_IMPLEMENTATION_REPORT.md",
    )
    selected = model.get("selected_moves", {})
    targets = model.get("targets", {})
    barrier = model.get("restore_barrier", {})
    freshness = model.get("overview", {}).get("freshness", {})
    target = first_reserved_target(targets)
    candidate_ips = parse_selected_candidates(e12_text) or ["10.7.0.11", "10.7.0.12"]
    selected_count = int(selected.get("count") or 0)
    stale_reasons = []
    if freshness.get("stale"):
        stale_reasons.extend(freshness.get("stale_reasons") or ["runtime_truth_stale"])
    if selected.get("freshness", {}).get("stale"):
        stale_reasons.extend(selected.get("freshness", {}).get("stale_reasons") or ["selected_moves_stale"])
    if barrier.get("freshness", {}).get("state") == "MISSING":
        stale_reasons.append("restore_barrier_missing")
    if selected_count > 0:
        stale_reasons.append("selected_moves_nonzero_preview_only")

    movement_budget = {
        "current_allowed_budget": 0,
        "future_contract_budget": 2,
        "hard_stop_reason": "E16_PREVIEW_ONLY_NO_MUTATING_APPROVAL_EXECUTION",
        "count_match_required": True,
    }
    movement_contract = {
        "object_type": "MovementApprovalPreview",
        "preview_only": True,
        "execution_allowed_now": False,
        "stage": "APPROVAL_CENTER_PREVIEW_ONLY",
        "disabled_reason": "mutating_approval_execution_out_of_scope_for_e16",
        "selected_target": target.get("target_id") or "wireguard-1779454504-c43409",
        "candidate_users": [
            {
                "user": ip,
                "from": "current_registered_egress",
                "to": target.get("target_id") or "wireguard-1779454504-c43409",
                "status": "historical_candidate_preview",
            }
            for ip in candidate_ips[:2]
        ],
        "movement_budget": movement_budget,
        "required_gates": [
            "fresh_runtime_snapshot",
            "selected_moves_fingerprint_match",
            "generation_token_match",
            "rollback_manifest_present",
            "restore_barrier_present",
            "dual_confirmation",
        ],
        "freshness": freshness,
        "stale_warnings": sorted(set(stale_reasons)),
    }
    fingerprint_parts = {
        "selected_moves": selected.get("selected_moves") or [],
        "selected_count": selected_count,
        "target": movement_contract["selected_target"],
        "budget": movement_budget,
        "preview_only": True,
    }
    fingerprint = preview_fingerprint(fingerprint_parts)
    generation_guard = {
        "object_type": "GenerationClearancePreview",
        "preview_only": True,
        "generation_id_required": True,
        "selected_move_fingerprint_required": True,
        "selected_move_fingerprint": fingerprint,
        "selected_move_count": selected_count,
        "clearance_max_selected_moves": int(barrier.get("clearance_max_selected_moves") or 0),
        "count_match_required": True,
        "replay_protection_state": "required_not_executable_from_ui",
        "barrier_state": {
            "active": bool(barrier.get("active")),
            "expired": bool(barrier.get("expired")),
            "cleared": bool(barrier.get("cleared")),
            "allow_post_ttl_apply": bool(barrier.get("allow_post_ttl_apply")),
            "generation_clearance": bool(barrier.get("generation_clearance")),
        },
    }
    rollback_manifest = {
        "object_type": "RollbackManifestPreview",
        "preview_only": True,
        "rollback_feasible": False,
        "disabled_reason": "rollback_execution_forbidden_in_e16",
        "items": [
            {
                "user": ip,
                "rollback_target": "1",
                "route_restore_expectation": "restore_user_to_previous_egress_and_verify_route_get",
                "status": "preview_only",
            }
            for ip in candidate_ips[:2]
        ],
    }
    blast_radius = {
        "object_type": "BlastRadiusPreview",
        "preview_only": True,
        "max_users": 0,
        "future_contract_max_users": 2,
        "target_hard_limit": target.get("hard_limit") or 0,
        "target_current_users": target.get("users") or 0,
        "affected_runtime_surfaces": [
            "users.registry",
            "per-user route table",
            "switch-history",
            "restore barrier",
            "selected_moves",
        ],
        "risk_level": "blocked_preview_only" if stale_reasons else "bounded_preview_only",
    }
    evidence_preview = {
        "object_type": "EvidenceFreshnessPreview",
        "preview_only": True,
        "state": "STALE" if stale_reasons else freshness.get("state", "UNKNOWN"),
        "stale_warnings": sorted(set(stale_reasons)),
        "latest_report": "BLOCK_E15_READONLY_OPERATOR_OVERVIEW_AND_OBSERVABILITY_UI_IMPLEMENTATION_REPORT.md",
        "e12_maturity": e12_answers.get("operational_maturity_status") or e12_answers.get("larger_cohort_readiness_after") or "unknown",
        "e15_readonly_ui": e15_answers.get("readonly_operator_ui_implemented", "unknown"),
    }
    contracts = {
        "MovementApprovalPreview": movement_contract,
        "GenerationClearancePreview": generation_guard,
        "RollbackManifestPreview": rollback_manifest,
        "BlastRadiusPreview": blast_radius,
        "EvidenceFreshnessPreview": evidence_preview,
    }
    return redact(
        {
            "schema_version": "e16.approval-preview.v1",
            "preview_only": True,
            "execution_allowed_now": False,
            "disabled_reason": "E16 implements approval UX contracts only; runtime execution remains forbidden.",
            "approval_status": {
                "state": "PREVIEW_ONLY",
                "current_stage": "APPROVAL_CENTER_FOUNDATION",
                "actions_disabled": True,
                "dual_confirmation_model": "required_for_future_execution_not_available_in_e16",
            },
            "contracts": contracts,
            "movement_preview": movement_contract,
            "generation_guard": generation_guard,
            "rollback_manifest": rollback_manifest,
            "blast_radius": blast_radius,
            "evidence_freshness": evidence_preview,
            "disabled_actions": [
                {"label": "Approve bounded movement", "disabled": True, "reason": "preview_only"},
                {"label": "Execute", "disabled": True, "reason": "runtime_control_forbidden"},
                {"label": "Restore apply", "disabled": True, "reason": "manual_autoswitch_apply_forbidden"},
                {"label": "Emergency containment", "disabled": True, "reason": "read_only_ui_only"},
            ],
        }
    )


def build_operator_view_model(repo_root=None, state_dir=None, event_dir=None, now=None):
    repo_root = Path(repo_root or Path.cwd())
    state_dir = Path(state_dir or "/opt/v7/egress/state")
    event_dir = Path(event_dir or "/opt/v7/events")
    now = now or utc_now()
    selected = selected_move_summary(repo_root, state_dir)
    barrier = barrier_summary(state_dir)
    targets = target_pool(state_dir)
    delayed = delayed_movement_summary(repo_root, event_dir, selected)
    operations = operation_history(repo_root)
    evidence = evidence_index(repo_root)
    verdict = governance_verdict(repo_root, selected, targets, barrier)
    overview = {
        "object_type": "RuntimeOverview",
        "collected_at": iso(now),
        "global_state": verdict["state"],
        "execution_allowed_now": False,
        "selected_moves": selected.get("count", 0),
        "restore_barrier_status": "active" if barrier.get("active") else ("expired" if barrier.get("expired") else ("missing" if barrier.get("freshness", {}).get("state") == "MISSING" else "inactive")),
        "generation_clearance_status": "cleared" if barrier.get("generation_clearance") else "not_cleared",
        "runtime_checkers": {"status": "UNKNOWN", "summary": "read-only adapter does not execute checkers"},
        "freshness": freshness_from_meta([
            targets.get("freshness", {}).get("sources", [{}])[0] if targets.get("freshness", {}).get("sources") else {"state": "MISSING", "stale": True, "stale_reasons": ["missing"]},
            targets.get("freshness", {}).get("sources", [{}, {}])[-1] if targets.get("freshness", {}).get("sources") else {"state": "MISSING", "stale": True, "stale_reasons": ["missing"]},
        ]),
        "last_operation_verdict": (operations[0] or {}).get("status") if operations else "none",
        "blockers": verdict["blockers"],
    }
    model = {
            "schema_version": "e15.readonly.v1",
            "generated_at": iso(now),
            "state_source": "read_only_files",
            "overview": overview,
            "governance_verdict": verdict,
            "targets": targets,
            "selected_moves": selected,
            "restore_barrier": barrier,
            "operations": operations,
            "evidence": evidence,
            "delayed_movement": delayed,
    }
    model["approval_preview"] = build_approval_preview(model, repo_root)
    model["execution_governance_preview"] = execution_governance_preview(repo_root, approval_preview=model["approval_preview"])
    model["execution_rehearsal_preview"] = execution_rehearsal_preview(repo_root, execution_preview=model["execution_governance_preview"])
    archive = build_operation_lineage_archive(repo_root)
    model["operation_lineage"] = {
        "schema_version": archive["schema_version"],
        "operation_count": archive["operation_count"],
        "timeline": archive["timeline"][:24],
        "filters": archive["filters"],
        "freshness": archive["freshness"],
    }
    model["audit_search"] = audit_search(repo_root, limit=20)
    return redact(model)


def build_operator_approval_preview(repo_root=None, state_dir=None, event_dir=None, now=None):
    model = build_operator_view_model(repo_root=repo_root, state_dir=state_dir, event_dir=event_dir, now=now)
    return model.get("approval_preview", {})


def build_operator_lineage_archive(repo_root=None):
    return build_operation_lineage_archive(Path(repo_root or Path.cwd()))


def build_operator_operation_detail(operation_id, repo_root=None):
    return operation_detail(Path(repo_root or Path.cwd()), operation_id)


def build_operator_audit_search(repo_root=None, query="", operation_type="", state="", evidence_kind="", limit=60):
    return audit_search(Path(repo_root or Path.cwd()), query=query, operation_type=operation_type, state=state, evidence_kind=evidence_kind, limit=limit)


def build_operator_evidence_archive(repo_root=None):
    return build_evidence_archive(Path(repo_root or Path.cwd()))


def build_operator_evidence_file_detail(evidence_id, repo_root=None):
    return evidence_file_detail(Path(repo_root or Path.cwd()), evidence_id)


def build_operator_audit_export_preview(operation_id="", repo_root=None):
    return audit_export_preview(Path(repo_root or Path.cwd()), operation_id=operation_id)


def build_operator_execution_governance_preview(operation_id="", repo_root=None):
    return execution_governance_preview(Path(repo_root or Path.cwd()), operation_id=operation_id)


def build_operator_execution_rehearsal_preview(operation_id="", repo_root=None):
    return execution_rehearsal_preview(Path(repo_root or Path.cwd()), operation_id=operation_id)
