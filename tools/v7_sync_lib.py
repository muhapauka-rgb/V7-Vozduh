#!/usr/bin/env python3
"""Safe source-to-production sync helpers for V7.

The helpers in this module are fail-closed by design. They reuse
``tools/v7-truth-check`` for source-of-truth decisions and only model deployment
of explicitly approved binaries.
"""

from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "track7" / "runtime-convergence" / "V7_TRUTH_MANIFEST.json"
TRUTH_CHECK_PATH = ROOT / "tools" / "v7-truth-check"
CANONICAL_BRANCH = "Updatesystem"
REMOTE_NAME = "origin"
DEPLOY_CONFIRMATION = "DEPLOY_V7_APPROVED"
RELEASE_SYNC_CONFIRMATION = "RELEASE_SYNC_APPROVED"

APPROVED_DEPLOY_FILES = [
    {
        "name": "admin_core/__init__.py",
        "local_path": "admin_core/__init__.py",
        "remote_path": "/usr/local/bin/admin_core/__init__.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "v7-users-autoswitch",
        "local_path": "tools/v7-users-autoswitch",
        "remote_path": "/usr/local/bin/v7-users-autoswitch",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-audit-log",
        "local_path": "tools/runtime-support/v7-audit-log",
        "remote_path": "/usr/local/bin/v7-audit-log",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-truth-check",
        "local_path": "tools/v7-truth-check",
        "remote_path": "/usr/local/bin/v7-truth-check",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-admin-api",
        "local_path": "admin/v7-admin-api",
        "remote_path": "/usr/local/bin/v7-admin-api",
        "mode": "0755",
        "service": "v7-admin-api.service",
    },
    {
        "name": "v7-operator-execution-packet",
        "local_path": "tools/v7-operator-execution-packet",
        "remote_path": "/usr/local/bin/v7-operator-execution-packet",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-intelligence-snapshot-refresh",
        "local_path": "tools/v7-intelligence-snapshot-refresh",
        "remote_path": "/usr/local/bin/v7-intelligence-snapshot-refresh",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-service-matrix-refresh-all",
        "local_path": "tools/v7-service-matrix-refresh-all",
        "remote_path": "/usr/local/bin/v7-service-matrix-refresh-all",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-service-matrix-test",
        "local_path": "tools/v7-service-matrix-test",
        "remote_path": "/usr/local/bin/v7-service-matrix-test",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-egress-quality-compact",
        "local_path": "tools/v7-egress-quality-compact",
        "remote_path": "/usr/local/bin/v7-egress-quality-compact",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-telegram-sentinel",
        "local_path": "tools/v7-telegram-sentinel",
        "remote_path": "/usr/local/bin/v7-telegram-sentinel",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-autoswitch-planner.service",
        "local_path": "systemd/drafts/v7-autoswitch-planner.service",
        "remote_path": "/etc/systemd/system/v7-autoswitch-planner.service",
        "mode": "0644",
        "service": "v7-autoswitch-planner.service",
    },
    {
        "name": "admin_core/admin_registry_views.py",
        "local_path": "admin_core/admin_registry_views.py",
        "remote_path": "/usr/local/bin/admin_core/admin_registry_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/diagnostic_views.py",
        "local_path": "admin_core/diagnostic_views.py",
        "remote_path": "/usr/local/bin/admin_core/diagnostic_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/events.py",
        "local_path": "admin_core/events.py",
        "remote_path": "/usr/local/bin/admin_core/events.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/intelligence_snapshots.py",
        "local_path": "admin_core/intelligence_snapshots.py",
        "remote_path": "/usr/local/bin/admin_core/intelligence_snapshots.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/intelligence_workers.py",
        "local_path": "admin_core/intelligence_workers.py",
        "remote_path": "/usr/local/bin/admin_core/intelligence_workers.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/intelligence_platform.py",
        "local_path": "admin_core/intelligence_platform.py",
        "remote_path": "/usr/local/bin/admin_core/intelligence_platform.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_execution.py",
        "local_path": "admin_core/operator_execution.py",
        "remote_path": "/usr/local/bin/admin_core/operator_execution.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_execution_feedback.py",
        "local_path": "admin_core/operator_execution_feedback.py",
        "remote_path": "/usr/local/bin/admin_core/operator_execution_feedback.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_execution_pipeline.py",
        "local_path": "admin_core/operator_execution_pipeline.py",
        "remote_path": "/usr/local/bin/admin_core/operator_execution_pipeline.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_observability.py",
        "local_path": "admin_core/operator_observability.py",
        "remote_path": "/usr/local/bin/admin_core/operator_observability.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_decision_surface.py",
        "local_path": "admin_core/operator_decision_surface.py",
        "remote_path": "/usr/local/bin/admin_core/operator_decision_surface.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/shadow_autonomy.py",
        "local_path": "admin_core/shadow_autonomy.py",
        "remote_path": "/usr/local/bin/admin_core/shadow_autonomy.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_views.py",
        "local_path": "admin_core/operator_views.py",
        "remote_path": "/usr/local/bin/admin_core/operator_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/overview_views.py",
        "local_path": "admin_core/overview_views.py",
        "remote_path": "/usr/local/bin/admin_core/overview_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/performance_summaries.py",
        "local_path": "admin_core/performance_summaries.py",
        "remote_path": "/usr/local/bin/admin_core/performance_summaries.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/registry_readers.py",
        "local_path": "admin_core/registry_readers.py",
        "remote_path": "/usr/local/bin/admin_core/registry_readers.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/route_reality_views.py",
        "local_path": "admin_core/route_reality_views.py",
        "remote_path": "/usr/local/bin/admin_core/route_reality_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/route_views.py",
        "local_path": "admin_core/route_views.py",
        "remote_path": "/usr/local/bin/admin_core/route_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/routing_brain.py",
        "local_path": "admin_core/routing_brain.py",
        "remote_path": "/usr/local/bin/admin_core/routing_brain.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/routing_intelligence.py",
        "local_path": "admin_core/routing_intelligence.py",
        "remote_path": "/usr/local/bin/admin_core/routing_intelligence.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/runtime_read_views.py",
        "local_path": "admin_core/runtime_read_views.py",
        "remote_path": "/usr/local/bin/admin_core/runtime_read_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/sanitize.py",
        "local_path": "admin_core/sanitize.py",
        "remote_path": "/usr/local/bin/admin_core/sanitize.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/service_views.py",
        "local_path": "admin_core/service_views.py",
        "remote_path": "/usr/local/bin/admin_core/service_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/summary_builders.py",
        "local_path": "admin_core/summary_builders.py",
        "remote_path": "/usr/local/bin/admin_core/summary_builders.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/time.py",
        "local_path": "admin_core/time.py",
        "remote_path": "/usr/local/bin/admin_core/time.py",
        "mode": "0644",
        "service": None,
    },
]

RUNTIME_ENTRYPOINTS = (
    "tools/v7-users-autoswitch",
    "tools/v7-intelligence-snapshot-refresh",
    "tools/v7-service-matrix-refresh-all",
    "tools/v7-service-matrix-test",
    "tools/v7-egress-quality-compact",
    "tools/v7-telegram-sentinel",
    "admin/v7-admin-api",
    "tools/v7-operator-execution-packet",
)

SNAPSHOT_REQUIRED_FILES = (
    "service-scores.json",
    "channel-service-scores.json",
    "risk-summaries.json",
    "trust-summaries.json",
    "blast-radius-summaries.json",
    "overview-summary.json",
)

SNAPSHOT_SYSTEMD_UNITS = (
    "v7-intelligence-snapshot-refresh.service",
    "v7-intelligence-snapshot-refresh.timer",
)

FORBIDDEN_USER_ARGS = {"--force", "-f", "--force-with-lease", "--delete", "--mirror"}
FORBIDDEN_RUNTIME_TOKENS = {
    "autoswitch_apply",
    "restore_barrier_mutation",
    "routing_mutation",
    "user_movement",
    "planner_mutation",
}

DEPLOYABLE_CHANGE_PREFIXES = (
    "admin/",
    "admin_core/",
    "tools/",
    "systemd/",
)

DOCS_ONLY_CHANGE_PREFIXES = (
    "docs/",
    "canary_expansion_execution_evidence/",
    "service_matrix_lineage_evidence/",
    "version_convergence_guard_evidence/",
)

ALLOWLISTED_RUNTIME_HASH_COMMAND_PATHS = {
    "/usr/local/bin/v7-users-autoswitch",
    "/usr/local/bin/v7-audit-log",
    "/usr/local/bin/v7-admin-api",
    "/usr/local/bin/v7-intelligence-snapshot-refresh",
    "/usr/local/bin/v7-service-matrix-refresh-all",
    "/usr/local/bin/v7-service-matrix-test",
    "/usr/local/bin/v7-egress-quality-compact",
}

ALLOWLISTED_RUNTIME_EXECUTABLE_TEST_PATHS = {
    "/usr/local/bin/v7-users-autoswitch",
    "/usr/local/bin/v7-audit-log",
    "/usr/local/bin/v7-admin-api",
    "/usr/local/bin/v7-intelligence-snapshot-refresh",
    "/usr/local/bin/v7-service-matrix-refresh-all",
    "/usr/local/bin/v7-service-matrix-test",
    "/usr/local/bin/v7-egress-quality-compact",
}

CommandRunner = Callable[[list[str], Optional[Path], int], dict[str, Any]]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_command(cmd: list[str], cwd: Optional[Path] = None, timeout: int = 30) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "rc": 127, "stdout": "", "stderr": str(exc), "cmd": cmd}
    return {
        "ok": proc.returncode == 0,
        "rc": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "cmd": cmd,
    }


def run_command_stdin(cmd: list[str], stdin: str, cwd: Optional[Path] = None, timeout: int = 30) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "rc": 127, "stdout": "", "stderr": str(exc), "cmd": cmd}
    return {
        "ok": proc.returncode == 0,
        "rc": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "cmd": cmd,
    }


def emit(result: dict[str, Any], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(human_summary(result))
    return 0 if result.get("final_verdict") == "PASS" else 1


def human_summary(result: dict[str, Any]) -> str:
    lines = [
        f"{result.get('tool', 'v7-sync')}: {result.get('final_verdict', 'UNKNOWN')}",
        f"status: {result.get('status', result.get('convergence_status', 'UNKNOWN'))}",
    ]
    for key in ("branch", "commit", "remote_commit", "runtime_commit", "mode"):
        if result.get(key):
            lines.append(f"{key}: {result[key]}")
    blockers = result.get("blockers") or []
    warnings = result.get("warnings") or []
    if blockers:
        lines.append("blockers: " + ", ".join(blockers))
    if warnings:
        lines.append("warnings: " + ", ".join(warnings))
    return "\n".join(lines)


def load_truth_module() -> Any:
    loader = importlib.machinery.SourceFileLoader("v7_truth_check_for_sync", str(TRUTH_CHECK_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def configured_runtime_snapshot_path(manifest: dict[str, Any]) -> Path:
    return ROOT / str(manifest.get("runtime_snapshot_path", ""))


def runtime_snapshot_seed_path(manifest: dict[str, Any]) -> Path:
    return ROOT / str(manifest.get("runtime_snapshot_seed_path", manifest.get("runtime_snapshot_path", "")))


def production_ssh_target(manifest: dict[str, Any] | None = None) -> str:
    manifest = manifest or load_manifest()
    return os.environ.get("V7_PROD_SSH_TARGET") or str(manifest.get("production_ssh_target") or "root@195.2.79.116")


def command_stdout(cmd: list[str], *, cwd: Path = ROOT, timeout: int = 30) -> str:
    return str(run_command(cmd, cwd=cwd, timeout=timeout).get("stdout") or "").strip()


def truth_check(mode: str = "all", *, runner: CommandRunner = run_command) -> dict[str, Any]:
    truth = load_truth_module()
    manifest = truth.load_manifest(MANIFEST_PATH)
    return truth.combine_results(manifest, mode=mode, runner=runner, cwd=ROOT)


def git_status() -> str:
    return command_stdout(["git", "status", "--short"])


def current_branch() -> str:
    return command_stdout(["git", "branch", "--show-current"])


def current_commit() -> str:
    return command_stdout(["git", "rev-parse", "HEAD"])


def origin_url() -> str:
    return command_stdout(["git", "remote", "get-url", REMOTE_NAME])


def remote_commit(remote_url: str, branch: str, *, runner: CommandRunner = run_command) -> str:
    result = runner(["git", "ls-remote", remote_url, f"refs/heads/{branch}"], ROOT, 30)
    if not result.get("ok"):
        return ""
    truth = load_truth_module()
    return truth.parse_ls_remote(str(result.get("stdout") or ""), branch)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deploy_file_records() -> list[dict[str, Any]]:
    records = []
    for item in APPROVED_DEPLOY_FILES:
        local_path = ROOT / item["local_path"]
        exists = local_path.exists()
        records.append(
            {
                **item,
                "local_abs_path": str(local_path),
                "exists": exists,
                "sha256": sha256_file(local_path) if exists else "MISSING",
            }
        )
    return records


def approved_local_paths() -> set[str]:
    return {str(item["local_path"]) for item in APPROVED_DEPLOY_FILES}


def admin_core_imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return set()
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name.startswith("admin_core."):
                    imports.add(name.split(".", 2)[1])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "admin_core":
                for alias in node.names:
                    imports.add(alias.name)
            elif module.startswith("admin_core."):
                imports.add(module.split(".", 2)[1])
    return imports


def required_admin_core_paths_for_runtime() -> set[str]:
    pending = [ROOT / path for path in RUNTIME_ENTRYPOINTS if (ROOT / path).exists()]
    seen_files: set[Path] = set()
    required: set[str] = set()
    while pending:
        path = pending.pop()
        if path in seen_files or not path.exists():
            continue
        seen_files.add(path)
        for module in admin_core_imports(path):
            module_path = ROOT / "admin_core" / f"{module}.py"
            if not module_path.exists():
                continue
            local = str(module_path.relative_to(ROOT))
            if local not in required:
                required.add(local)
                pending.append(module_path)
    if required:
        init_path = ROOT / "admin_core" / "__init__.py"
        if init_path.exists():
            required.add(str(init_path.relative_to(ROOT)))
    return required


def deploy_allowlist_validation() -> dict[str, Any]:
    approved = approved_local_paths()
    required_runtime = set(RUNTIME_ENTRYPOINTS)
    required_admin = required_admin_core_paths_for_runtime()
    required = required_runtime | required_admin
    missing = sorted(path for path in required if path not in approved)
    extra = sorted(path for path in approved if path.startswith("admin_core/") and path not in required)
    records = deploy_file_records()
    missing_local_files = sorted(item["local_path"] for item in records if not item["exists"])
    duplicate_remote_paths = sorted(
        path
        for path in {item["remote_path"] for item in APPROVED_DEPLOY_FILES}
        if sum(1 for item in APPROVED_DEPLOY_FILES if item["remote_path"] == path) > 1
    )
    return {
        "schema": "v7-deploy-allowlist-validation/v1",
        "owner": "tools/v7_sync_lib.APPROVED_DEPLOY_FILES",
        "runtime_entrypoints": list(RUNTIME_ENTRYPOINTS),
        "required_admin_core_paths": sorted(required_admin),
        "approved_local_paths": sorted(approved),
        "missing_required_paths": missing,
        "documentation_extra_paths": extra,
        "missing_local_files": missing_local_files,
        "duplicate_remote_paths": duplicate_remote_paths,
        "final_verdict": "PASS" if not missing and not missing_local_files and not duplicate_remote_paths else "NO-GO",
    }


def build_runtime_fingerprint(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    records = deploy_file_records()
    return {
        "schema": "v7-runtime-fingerprint/v1",
        "created_at": utc_now(),
        "branch": branch,
        "commit": commit,
        "deploy_id": deploy_id,
        "runtime_root": "/opt/v7",
        "critical_files": [
            {
                "name": item["name"],
                "local_path": item["local_path"],
                "remote_path": item["remote_path"],
                "sha256": item["sha256"],
                "mode": item["mode"],
            }
            for item in records
        ],
        "systemd_units": [
            "v7-autoswitch-planner.service",
            "v7-autoswitch-planner.timer",
            "v7-users-autoswitch.service",
            "v7-users-autoswitch.timer",
            "v7-admin-api.service",
            *SNAPSHOT_SYSTEMD_UNITS,
        ],
        "snapshot_subsystem": {
            "root": "/opt/v7/egress/state/intelligence",
            "refresh_cli": "/usr/local/bin/v7-intelligence-snapshot-refresh",
            "required_files": list(SNAPSHOT_REQUIRED_FILES),
            "systemd_units": list(SNAPSHOT_SYSTEMD_UNITS),
        },
        "authority": {
            "canonical_truth_gate": "tools/v7-truth-check",
            "canonical_deploy_tool": "tools/v7-safe-deploy",
            "canonical_status_command": "tools/v7-convergence-status",
        },
    }


def validate_runtime_fingerprint(fingerprint: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if fingerprint.get("schema") != "v7-runtime-fingerprint/v1":
        errors.append("schema_mismatch")
    if not fingerprint.get("commit"):
        errors.append("commit_missing")
    files = fingerprint.get("critical_files")
    if not isinstance(files, list) or not files:
        errors.append("critical_files_missing")
    else:
        for row in files:
            if not isinstance(row, dict):
                errors.append("critical_file_row_invalid")
                continue
            for key in ("local_path", "remote_path", "sha256"):
                if not row.get(key):
                    errors.append(f"critical_file_{key}_missing")
    snapshot = fingerprint.get("snapshot_subsystem")
    if not isinstance(snapshot, dict):
        errors.append("snapshot_subsystem_missing")
    else:
        if not snapshot.get("refresh_cli"):
            errors.append("snapshot_refresh_cli_missing")
        if not snapshot.get("required_files"):
            errors.append("snapshot_required_files_missing")
    return {
        "schema": "v7-runtime-fingerprint-validation/v1",
        "errors": sorted(set(errors)),
        "final_verdict": "PASS" if not errors else "NO-GO",
    }


def classify_status(status: str) -> dict[str, Any]:
    truth = load_truth_module()
    return truth.classify_git_status(status)


def reject_forbidden_args(argv: Iterable[str]) -> list[str]:
    seen = [arg for arg in argv if arg in FORBIDDEN_USER_ARGS]
    return [f"forbidden_arg:{arg}" for arg in seen]


def dirty_requires_runtime_approval(dirty: dict[str, Any]) -> bool:
    return bool(dirty.get("counts", {}).get("runtime_critical") or dirty.get("counts", {}).get("unknown"))


def safe_commit_plan(
    *,
    message: str,
    apply: bool,
    allow_runtime_critical: bool,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    status = git_status()
    dirty = classify_status(status)
    blockers: list[str] = []
    warnings: list[str] = []

    if str(manifest.get("canonical_branch")) != CANONICAL_BRANCH:
        blockers.append("manifest_authoritative_branch_unexpected")
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if not message.strip():
        blockers.append("commit_message_required")
    if dirty.get("clean"):
        blockers.append("nothing_to_commit")
    if dirty.get("blocking") and not allow_runtime_critical:
        blockers.append("runtime_or_unknown_dirty_requires_explicit_allowance")
    if dirty.get("warning"):
        warnings.append("runtime_relevant_dirty")
    if dirty.get("info_paths"):
        warnings.append("documentation_dirty_present")

    commands = [
        ["git", "status", "--short"],
        ["git", "add", "--", "."],
        ["git", "commit", "-m", message],
    ]
    result = {
        "tool": "v7-safe-commit",
        "schema": "v7-safe-commit/v1",
        "mode": "apply" if apply else "dry-run",
        "branch": branch or "UNKNOWN",
        "commit_before": current_commit() or "UNKNOWN",
        "dirty_classification": dirty,
        "planned_commands": commands,
        "warnings": warnings,
        "blockers": blockers,
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    add_result = runner(["git", "add", "--", "."], ROOT, 30)
    commit_result = runner(["git", "commit", "-m", message], ROOT, 60)
    result["command_results"] = {"git_add": add_result, "git_commit": commit_result}
    if not add_result.get("ok"):
        result["blockers"].append("git_add_failed")
    if not commit_result.get("ok"):
        result["blockers"].append("git_commit_failed")
    result["commit_after"] = current_commit() or "UNKNOWN"
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def safe_push_plan(*, apply: bool, argv: Iterable[str] = (), runner: CommandRunner = run_command) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    commit = current_commit()
    remote = origin_url()
    expected_remote = str(manifest.get("canonical_remote"))
    blockers = reject_forbidden_args(argv)
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if remote != expected_remote:
        blockers.append("remote_mismatch")
    status = git_status()
    dirty = classify_status(status)
    if dirty.get("blocking"):
        blockers.append("blocking_dirty_workspace")
    before = remote_commit(remote, branch, runner=runner) if remote and branch else ""
    if before and before != commit and apply:
        ancestor = runner(["git", "merge-base", "--is-ancestor", before, commit], ROOT, 30)
        if not ancestor.get("ok"):
            blockers.append("remote_commit_not_ancestor_of_local")

    commands = [["git", "push", REMOTE_NAME, f"HEAD:{branch}"]]
    result = {
        "tool": "v7-safe-push",
        "schema": "v7-safe-push/v1",
        "mode": "apply" if apply else "dry-run",
        "branch": branch or "UNKNOWN",
        "commit": commit or "UNKNOWN",
        "remote": remote or "UNKNOWN",
        "remote_commit_before": before or "UNKNOWN",
        "planned_commands": commands,
        "blockers": blockers,
        "warnings": ["documentation_dirty_present"] if dirty.get("info_paths") else [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    push_result = runner(["git", "push", REMOTE_NAME, f"HEAD:{branch}"], ROOT, 120)
    after = remote_commit(remote, branch, runner=runner) if push_result.get("ok") else ""
    result["command_results"] = {"git_push": push_result}
    result["remote_commit_after"] = after or "UNKNOWN"
    if not push_result.get("ok"):
        result["blockers"].append("git_push_failed")
    if after and after != commit:
        result["blockers"].append("remote_commit_after_mismatch")
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def deployment_id(branch: str, commit: str) -> str:
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    return f"deploy-z8-14-{branch}-{commit[:7]}-{stamp}"


def build_deploy_manifest(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    fingerprint = build_runtime_fingerprint(branch=branch, commit=commit, deploy_id=deploy_id)
    return {
        "schema": "v7-deploy-manifest/v1",
        "project": "V7 Vozduh",
        "created_at": utc_now(),
        "deploy_id": deploy_id,
        "deploy_branch": branch,
        "deploy_commit": commit,
        "deployment_model": "copied_binaries_with_safe_sync_manifest",
        "approved_deploy_files": deploy_file_records(),
        "allowlist_validation": deploy_allowlist_validation(),
        "runtime_fingerprint": fingerprint,
        "runtime_fingerprint_validation": validate_runtime_fingerprint(fingerprint),
        "safety": {
            "autoswitch_apply_executed": False,
            "user_movement_executed": False,
            "routing_mutation_executed": False,
            "restore_barrier_modified": False,
            "planner_modified": False,
            "policy_modified": False,
        },
    }


def build_runtime_linkage(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    return {
        "schema": "v7-runtime-linkage/v1",
        "updated_at": utc_now(),
        "runtime_identity_model": "copied_binaries_from_deploy_manifest",
        "runtime_root_is_git_checkout": False,
        "deploy_id": deploy_id,
        "deploy_branch": branch,
        "deploy_commit": commit,
        "runtime_fingerprint_schema": "v7-runtime-fingerprint/v1",
        "authoritative_workspace": str(ROOT),
        "authoritative_branch": branch,
    }


def build_release_manifest(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    return {
        "schema": "v7-release-manifest/v1",
        "created_at": utc_now(),
        "release_id": deploy_id,
        "branch": branch,
        "commit": commit,
        "deploy_manifest": "/opt/v7/deploy-manifest.json",
        "runtime_linkage": "/opt/v7/runtime-linkage.json",
        "runtime_fingerprint": "/opt/v7/runtime-fingerprint.json",
        "rollback_manifest_required": True,
        "service_restart_required": False,
    }


def production_hashes_from_snapshot() -> dict[str, str]:
    manifest = load_manifest()
    snapshot_path = configured_runtime_snapshot_path(manifest)
    if not snapshot_path.exists():
        snapshot_path = runtime_snapshot_seed_path(manifest)
    if not snapshot_path.exists():
        return {}
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    command_results = snapshot.get("command_results") if isinstance(snapshot.get("command_results"), dict) else {}
    hashes: dict[str, str] = {}
    for command, value in command_results.items():
        if not command.startswith("sha256sum "):
            continue
        stdout = str((value or {}).get("stdout") or "")
        parts = stdout.split()
        if len(parts) >= 2:
            hashes[parts[1]] = parts[0]
    additional = (
        snapshot.get("additional_readonly_findings")
        if isinstance(snapshot.get("additional_readonly_findings"), dict)
        else {}
    )
    safe_deploy_hashes = (
        additional.get("safe_deploy_runtime_hashes")
        if isinstance(additional.get("safe_deploy_runtime_hashes"), dict)
        else {}
    )
    for remote_path, sha256 in safe_deploy_hashes.items():
        if remote_path and sha256:
            hashes[str(remote_path)] = str(sha256)
    return hashes


def deploy_delta() -> list[dict[str, Any]]:
    production = production_hashes_from_snapshot()
    delta = []
    for item in deploy_file_records():
        remote_hash = production.get(item["remote_path"], "UNKNOWN")
        delta.append(
            {
                "name": item["name"],
                "local_path": item["local_path"],
                "remote_path": item["remote_path"],
                "local_sha256": item["sha256"],
                "production_sha256": remote_hash,
                "matches": remote_hash == item["sha256"],
                "exists": item["exists"],
            }
        )
    return delta


def is_docs_only_change(path: str) -> bool:
    normalized = path.strip()
    if not normalized:
        return False
    first = normalized.split("/", 1)[0]
    return (
        normalized.startswith(DOCS_ONLY_CHANGE_PREFIXES)
        or first.endswith("_evidence")
        or (normalized.startswith("PROGRAM_") and normalized.endswith(".md"))
        or normalized.endswith("_REPORT.md")
    )


def is_deployable_change(path: str) -> bool:
    normalized = path.strip()
    if not normalized:
        return False
    return normalized in approved_local_paths() or normalized.startswith(DEPLOYABLE_CHANGE_PREFIXES)


def classify_deployable_changes(paths: Iterable[str]) -> dict[str, Any]:
    deploy_required: list[str] = []
    docs_only: list[str] = []
    unknown: list[str] = []
    for raw in paths:
        path = str(raw).strip()
        if not path:
            continue
        if is_docs_only_change(path):
            docs_only.append(path)
        elif is_deployable_change(path):
            deploy_required.append(path)
        else:
            unknown.append(path)
    if deploy_required:
        classification = "DEPLOY_REQUIRED"
    elif unknown:
        classification = "UNKNOWN"
    elif docs_only:
        classification = "DOCS_ONLY_MISMATCH"
    else:
        classification = "NO_CHANGES"
    return {
        "schema": "v7-deployable-change-classification/v1",
        "classification": classification,
        "deploy_required_paths": sorted(deploy_required),
        "docs_only_paths": sorted(docs_only),
        "unknown_paths": sorted(unknown),
        "deployment_required": bool(deploy_required),
        "docs_only_mismatch": bool(docs_only and not deploy_required and not unknown),
        "final_verdict": "PASS" if not unknown else "NO-GO",
    }


def changed_files_between_commits(
    base_commit: str,
    head_commit: str,
    *,
    runner: CommandRunner = run_command,
) -> list[str]:
    if not base_commit or not head_commit or "UNKNOWN" in {base_commit, head_commit}:
        return []
    if base_commit == head_commit:
        return []
    result = runner(["git", "diff", "--name-only", f"{base_commit}..{head_commit}"], ROOT, 30)
    if not result.get("ok"):
        return []
    return [line.strip() for line in str(result.get("stdout") or "").splitlines() if line.strip()]


def runtime_action_guard_for_status(
    status: dict[str, Any],
    *,
    changed_files: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    local_commit = str(status.get("local", {}).get("commit") or status.get("commit") or "UNKNOWN")
    github_commit = str(status.get("github", {}).get("commit") or status.get("remote_commit") or "UNKNOWN")
    production_commit = str(status.get("production", {}).get("commit") or status.get("runtime_commit") or "UNKNOWN")
    diagnosis = [str(item) for item in (status.get("diagnosis") or status.get("blockers") or [])]
    deploy_delta_rows = status.get("deploy_delta_mismatches") or []
    if not deploy_delta_rows and isinstance(status.get("deploy_delta"), list):
        deploy_delta_rows = [row for row in status["deploy_delta"] if isinstance(row, dict) and not row.get("matches")]
    classification = classify_deployable_changes(changed_files or [])
    deploy_required_by_delta = bool(deploy_delta_rows)
    deploy_required_by_changes = classification.get("classification") == "DEPLOY_REQUIRED"
    deployment_required = deploy_required_by_delta or deploy_required_by_changes
    docs_only_mismatch = (
        classification.get("classification") == "DOCS_ONLY_MISMATCH"
        and not deploy_required_by_delta
        and not deploy_required_by_changes
    )
    safe_deploy_command = (
        "tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED "
        "--update-local-snapshot --restart-admin-if-changed --json"
    )

    if status.get("final_verdict") == "PASS" and not deployment_required:
        guard_status = "READY_FOR_RUNTIME_ACTION"
        reason = "local_github_production_aligned"
        runtime_action_safe = True
        safe_next_command = "tools/v7-truth-check --all --json"
        final_verdict = "PASS"
    elif docs_only_mismatch and local_commit == github_commit and production_commit != "UNKNOWN":
        guard_status = "DOCS_ONLY_MISMATCH"
        reason = "production_commit_behind_only_docs_or_evidence_changes"
        runtime_action_safe = True
        safe_next_command = "tools/v7-convergence-status --json"
        final_verdict = "PASS"
    elif deployment_required or any("runtime_local_commit_mismatch" in item for item in diagnosis):
        guard_status = "DEPLOY_REQUIRED"
        reason = "production_runtime_not_at_deployable_current_truth"
        runtime_action_safe = False
        safe_next_command = safe_deploy_command
        final_verdict = "NO-GO"
    else:
        guard_status = "NO_GO"
        reason = "unclassified_convergence_blocker"
        runtime_action_safe = False
        safe_next_command = "tools/v7-convergence-status --json"
        final_verdict = "NO-GO"

    if classification.get("classification") == "UNKNOWN":
        guard_status = "NO_GO"
        reason = "changed_files_include_unknown_paths"
        runtime_action_safe = False
        safe_next_command = "STOP_REVIEW_CHANGED_FILES"
        final_verdict = "NO-GO"

    return {
        "schema": "v7-runtime-action-deploy-guard/v1",
        "status": guard_status,
        "reason": reason,
        "local_commit": local_commit,
        "github_commit": github_commit,
        "production_commit": production_commit,
        "deployment_required": deployment_required,
        "docs_only_mismatch": docs_only_mismatch,
        "runtime_action_safe": runtime_action_safe,
        "safe_next_command": safe_next_command,
        "deploy_delta_mismatches": deploy_delta_rows,
        "changed_files_since_production": sorted(str(path) for path in (changed_files or [])),
        "deployable_change_classification": classification,
        "diagnosis": diagnosis,
        "final_verdict": final_verdict,
    }


def safe_deploy_plan(
    *,
    apply: bool,
    confirm: str,
    update_local_snapshot: bool,
    restart_admin_if_changed: bool = False,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    commit = current_commit()
    deploy_id = deployment_id(branch, commit)
    truth = truth_check("github", runner=runner)
    delta = deploy_delta()
    allowlist = deploy_allowlist_validation()
    blockers: list[str] = []
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if truth.get("final_verdict") != "PASS":
        blockers.append("github_truth_check_failed")
    if allowlist.get("final_verdict") != "PASS":
        blockers.append("deploy_allowlist_validation_failed")
    if any(not item["exists"] for item in deploy_file_records()):
        blockers.append("approved_deploy_file_missing")
    changed_admin = any(item["name"] == "v7-admin-api" and not item["matches"] for item in delta)
    changed_systemd = any(
        item["remote_path"].startswith("/etc/systemd/system/")
        and not item["matches"]
        for item in delta
    )
    if apply and confirm != DEPLOY_CONFIRMATION:
        blockers.append("deploy_confirmation_required")
    if apply and changed_admin and not restart_admin_if_changed:
        blockers.append("admin_binary_changed_requires_explicit_restart_flag")

    deploy_manifest = build_deploy_manifest(branch=branch, commit=commit, deploy_id=deploy_id)
    runtime_linkage = build_runtime_linkage(branch=branch, commit=commit, deploy_id=deploy_id)
    release_manifest = build_release_manifest(branch=branch, commit=commit, deploy_id=deploy_id)
    planned_remote_paths = {
        "backup_root": f"/root/v7-deploy-backups/{deploy_id}",
        "release_dir": f"/opt/v7/ops/{deploy_id}",
        "deploy_manifest": "/opt/v7/deploy-manifest.json",
        "runtime_linkage": "/opt/v7/runtime-linkage.json",
        "runtime_fingerprint": "/opt/v7/runtime-fingerprint.json",
        "release_manifest": f"/opt/v7/ops/{deploy_id}/release-manifest.json",
    }
    result = {
        "tool": "v7-safe-deploy",
        "schema": "v7-safe-deploy/v1",
        "mode": "apply" if apply else "dry-run",
        "branch": branch or "UNKNOWN",
        "commit": commit or "UNKNOWN",
        "deploy_id": deploy_id,
        "truth_check": truth,
        "deploy_delta": delta,
        "allowlist_validation": allowlist,
        "deployment_required": any(not item["matches"] for item in delta),
        "restart_admin_if_changed": restart_admin_if_changed,
        "planned_remote_paths": planned_remote_paths,
        "deploy_manifest": deploy_manifest,
        "runtime_linkage": runtime_linkage,
        "runtime_fingerprint": deploy_manifest["runtime_fingerprint"],
        "release_manifest": release_manifest,
        "blockers": blockers,
        "warnings": [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    ssh_target = production_ssh_target(manifest)
    payload = {
        "deploy_manifest": deploy_manifest,
        "runtime_linkage": runtime_linkage,
        "runtime_fingerprint": deploy_manifest["runtime_fingerprint"],
        "release_manifest": release_manifest,
        "update_local_snapshot": update_local_snapshot,
        "restart_admin_if_changed": restart_admin_if_changed,
        "files": [],
    }
    delta_by_path = {item["remote_path"]: item for item in delta}
    for item in deploy_file_records():
        replacement_required = not delta_by_path[item["remote_path"]]["matches"]
        file_payload = {
            "name": item["name"],
            "remote_path": item["remote_path"],
            "mode": item["mode"],
            "service": item["service"],
            "replace": replacement_required,
        }
        if replacement_required:
            file_payload["content_b64"] = base64.b64encode(Path(item["local_abs_path"]).read_bytes()).decode("ascii")
        payload["files"].append(file_payload)
    payload_b64 = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode("utf-8")).decode("ascii")
    daemon_reload_block = "systemctl daemon-reload\n" if changed_systemd else ""
    restart_block = "systemctl restart v7-admin-api.service\n" if restart_admin_if_changed and changed_admin else ""
    script = (
        "set -eu\n"
        f"backup_root={planned_remote_paths['backup_root']}\n"
        f"release_dir={planned_remote_paths['release_dir']}\n"
        "mkdir -p \"$backup_root\" \"$release_dir\"\n"
        "for f in /usr/local/bin/v7-users-autoswitch /usr/local/bin/v7-audit-log /usr/local/bin/v7-admin-api; do "
        "if test -e \"$f\"; then cp -p \"$f\" \"$backup_root/$(basename \"$f\").pre-sync\"; fi; done\n"
        "python3 - <<'PY'\n"
        "import base64, json, os, pathlib, shutil\n"
        f"payload=json.loads(base64.b64decode('{payload_b64}').decode('utf-8'))\n"
        f"backup_root=pathlib.Path('{planned_remote_paths['backup_root']}')\n"
        "for item in payload['files']:\n"
        "    if not item.get('replace'):\n"
        "        continue\n"
        "    remote=pathlib.Path(item['remote_path'])\n"
        "    remote.parent.mkdir(parents=True, exist_ok=True)\n"
        "    if remote.exists():\n"
        "        backup_name=str(remote).strip('/').replace('/', '__') + '.pre-sync'\n"
        "        shutil.copy2(remote, backup_root / backup_name)\n"
        "    tmp=remote.with_suffix(remote.suffix + '.v7-sync-new')\n"
        "    tmp.write_bytes(base64.b64decode(item['content_b64']))\n"
        "    os.chmod(tmp, int(item['mode'], 8))\n"
        "    tmp.replace(remote)\n"
        "pathlib.Path('/opt/v7/deploy-manifest.json').write_text(json.dumps(payload['deploy_manifest'], indent=2, ensure_ascii=False)+'\\n')\n"
        "pathlib.Path('/opt/v7/runtime-linkage.json').write_text(json.dumps(payload['runtime_linkage'], indent=2, ensure_ascii=False)+'\\n')\n"
        "pathlib.Path('/opt/v7/runtime-fingerprint.json').write_text(json.dumps(payload['runtime_fingerprint'], indent=2, ensure_ascii=False)+'\\n')\n"
        f"pathlib.Path('{planned_remote_paths['release_manifest']}').write_text(json.dumps(payload['release_manifest'], indent=2, ensure_ascii=False)+'\\n')\n"
        "PY\n"
        f"{daemon_reload_block}"
        f"{restart_block}"
        f"ln -sfn {planned_remote_paths['release_dir']} /opt/v7/releases/current\n"
    )
    if runner is run_command:
        ssh_result = run_command_stdin(["ssh", ssh_target, "bash", "-s"], script, ROOT, 120)
    else:
        ssh_result = runner(["ssh", ssh_target, "bash", "-s"], ROOT, 120)
    result["command_results"] = {"ssh_manifest_refresh": ssh_result}
    if not ssh_result.get("ok"):
        result["blockers"].append("production_manifest_refresh_failed")
    elif update_local_snapshot:
        update_snapshot_for_deploy(deploy_id=deploy_id, branch=branch, commit=commit)
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def update_snapshot_for_deploy(*, deploy_id: str, branch: str, commit: str) -> None:
    manifest = load_manifest()
    snapshot_path = configured_runtime_snapshot_path(manifest)
    seed_path = runtime_snapshot_seed_path(manifest)
    source_path = snapshot_path if snapshot_path.exists() else seed_path
    if not source_path.exists():
        return
    snapshot = json.loads(source_path.read_text(encoding="utf-8"))
    snapshot["collected_at"] = utc_now()
    snapshot["collection_mode"] = "z8_14_safe_deploy_provenance_refresh"
    additional = snapshot.setdefault("additional_readonly_findings", {})
    additional["z8_14_safe_sync"] = {
        "commit": commit,
        "deploy_id": deploy_id,
        "binary_replacement_performed": False,
        "autoswitch_apply_executed": False,
        "user_movement_executed": False,
        "routing_mutation_executed": False,
        "restore_barrier_modified": False,
        "service_restart_performed": False,
    }
    derived = snapshot.setdefault("derived", {})
    derived["deployment_model"] = "copied_binaries_from_safe_sync_manifest"
    derived["runtime_identity_model"] = "copied_binaries_from_safe_sync_manifest"
    derived["deploy_branch"] = branch
    derived["deploy_commit"] = commit
    derived["deploy_id"] = deploy_id
    fingerprint = build_runtime_fingerprint(branch=branch, commit=commit, deploy_id=deploy_id)
    command_results = snapshot.get("command_results") if isinstance(snapshot.get("command_results"), dict) else {}
    for command, value in list(command_results.items()):
        if isinstance(value, dict) and value.get("source") == "v7-safe-deploy-runtime-fingerprint":
            command_results.pop(command, None)
    runtime_hashes: dict[str, str] = {}
    for item in fingerprint.get("critical_files", []):
        remote_path = str(item.get("remote_path") or "")
        sha256 = str(item.get("sha256") or "")
        if not remote_path or not sha256:
            continue
        runtime_hashes[remote_path] = sha256
        if remote_path in ALLOWLISTED_RUNTIME_HASH_COMMAND_PATHS:
            command_results[f"sha256sum {remote_path}"] = {
                "ok": True,
                "rc": 0,
                "stdout": f"{sha256}  {remote_path}",
                "stderr": "",
                "cmd": ["sha256sum", remote_path],
                "source": "v7-safe-deploy-runtime-fingerprint",
            }
        if remote_path in ALLOWLISTED_RUNTIME_EXECUTABLE_TEST_PATHS:
            command_results[f"test -x {remote_path}"] = {
                "ok": True,
                "rc": 0,
                "stdout": "",
                "stderr": "",
                "cmd": ["test", "-x", remote_path],
                "source": "v7-safe-deploy-runtime-fingerprint",
            }
    additional["safe_deploy_runtime_hashes"] = runtime_hashes
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_status(*, runner: CommandRunner = run_command) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    commit = current_commit()
    remote = origin_url()
    remote_head = remote_commit(remote, branch, runner=runner) if remote and branch else ""
    local_truth = truth_check("local", runner=runner)
    all_truth = truth_check("all", runner=runner)
    delta = deploy_delta()
    runtime = all_truth.get("runtime", {}) if isinstance(all_truth.get("runtime"), dict) else {}
    blockers: list[str] = []
    if local_truth.get("final_verdict") != "PASS":
        blockers.append("local_truth_failed")
    if remote_head and remote_head != commit:
        blockers.append("github_not_at_local_commit")
    if all_truth.get("final_verdict") != "PASS":
        blockers.extend([f"truth:{item}" for item in all_truth.get("blockers", [])])
    return {
        "tool": "v7-sync-status",
        "schema": "v7-sync-status/v1",
        "status": "SYNCED" if not blockers else "NO-GO",
        "branch": branch or "UNKNOWN",
        "commit": commit or "UNKNOWN",
        "remote": remote or "UNKNOWN",
        "remote_commit": remote_head or "UNKNOWN",
        "runtime_commit": runtime.get("runtime_commit", "UNKNOWN"),
        "local_truth": local_truth,
        "truth_check_all": all_truth,
        "deploy_delta": delta,
        "blockers": blockers,
        "warnings": all_truth.get("warnings", []),
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }


def convergence_status(*, runner: CommandRunner = run_command) -> dict[str, Any]:
    status = sync_status(runner=runner)
    truth_all = status.get("truth_check_all") if isinstance(status.get("truth_check_all"), dict) else {}
    local = truth_all.get("local") if isinstance(truth_all.get("local"), dict) else {}
    github = truth_all.get("github") if isinstance(truth_all.get("github"), dict) else {}
    runtime = truth_all.get("runtime") if isinstance(truth_all.get("runtime"), dict) else {}
    deploy_delta_rows = status.get("deploy_delta") if isinstance(status.get("deploy_delta"), list) else []
    mismatched = [row for row in deploy_delta_rows if isinstance(row, dict) and not row.get("matches")]
    result = {
        "tool": "v7-convergence-status",
        "schema": "v7-convergence-status/v1",
        "canonical_truth_model": {
            "canonical_branch": CANONICAL_BRANCH,
            "canonical_deploy_source": "origin/Updatesystem plus tools/v7-safe-deploy approved package",
            "canonical_truth_gate": "tools/v7-truth-check",
            "canonical_deploy_tool": "tools/v7-safe-deploy",
            "canonical_runtime_fingerprint": "/opt/v7/runtime-fingerprint.json",
        },
        "local": {
            "commit": local.get("current_commit", status.get("commit", "UNKNOWN")),
            "status": local.get("final_verdict", "UNKNOWN"),
        },
        "github": {
            "commit": github.get("remote_branch_commit", status.get("remote_commit", "UNKNOWN")),
            "status": github.get("final_verdict", "UNKNOWN"),
        },
        "production": {
            "commit": runtime.get("runtime_commit", "UNKNOWN"),
            "status": runtime.get("final_verdict", "UNKNOWN"),
            "runtime_access_status": runtime.get("runtime_access_status", "UNKNOWN"),
            "runtime_truth_status": runtime.get("runtime_truth_status", "UNKNOWN"),
        },
        "deploy_allowlist": deploy_allowlist_validation(),
        "deploy_delta_mismatches": mismatched,
        "status": "ALIGNED" if status.get("final_verdict") == "PASS" else "NOT_ALIGNED",
        "diagnosis": status.get("blockers", []),
        "source_status": status,
        "final_verdict": status.get("final_verdict", "NO-GO"),
    }
    changed_files = changed_files_between_commits(
        str(result["production"].get("commit") or ""),
        str(result["local"].get("commit") or ""),
        runner=runner,
    )
    guard = runtime_action_guard_for_status(result, changed_files=changed_files)
    result["runtime_action_guard"] = guard
    result["runtime_action_status"] = guard["status"]
    result["runtime_action_safe"] = guard["runtime_action_safe"]
    result["safe_next_command"] = guard["safe_next_command"]
    return result


def convergence_owner_status(*, runner: CommandRunner = run_command) -> dict[str, Any]:
    status = convergence_status(runner=runner)
    source = status.get("source_status") if isinstance(status.get("source_status"), dict) else {}
    truth_all = source.get("truth_check_all") if isinstance(source.get("truth_check_all"), dict) else {}
    local_truth = truth_all.get("local") if isinstance(truth_all.get("local"), dict) else {}
    dirty = local_truth.get("dirty_classification") if isinstance(local_truth.get("dirty_classification"), dict) else {}
    diagnosis = list(status.get("diagnosis") or [])
    ssh_target = production_ssh_target()

    if status.get("final_verdict") == "PASS":
        next_action = "NONE_MONITOR"
        safe_command = "tools/v7-truth-check --all"
        explanation = "local_github_production_aligned"
    elif any("github_not_at_local_commit" in item or "local_remote_commit_mismatch" in item for item in diagnosis):
        next_action = "PUSH_CANONICAL_BRANCH"
        safe_command = "tools/v7-safe-push --apply --json"
        explanation = "github_is_not_at_local_commit"
    elif any("runtime_local_commit_mismatch" in item for item in diagnosis):
        next_action = "RUN_APPROVED_SAFE_DEPLOY"
        safe_command = (
            f"V7_PROD_SSH_TARGET={ssh_target} "
            "tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json"
        )
        explanation = "production_is_not_at_local_commit"
    elif any("github_remote_unreadable" in item for item in diagnosis):
        next_action = "RETRY_WITH_NETWORK_ACCESS"
        safe_command = "tools/v7-truth-check --all"
        explanation = "github_read_failed"
    else:
        next_action = "STOP_REVIEW_BLOCKERS"
        safe_command = "tools/v7-convergence-status --json"
        explanation = "unclassified_blocker"

    return {
        "tool": "v7-convergence-owner",
        "schema": "v7-convergence-owner/v1",
        "status": status.get("status", "UNKNOWN"),
        "final_verdict": status.get("final_verdict", "NO-GO"),
        "local_commit": status.get("local", {}).get("commit", "UNKNOWN"),
        "github_commit": status.get("github", {}).get("commit", "UNKNOWN"),
        "production_commit": status.get("production", {}).get("commit", "UNKNOWN"),
        "runtime_access_status": status.get("production", {}).get("runtime_access_status", "UNKNOWN"),
        "runtime_truth_status": status.get("production", {}).get("runtime_truth_status", "UNKNOWN"),
        "workspace_runtime_clean": not bool(dirty.get("blocking") or dirty.get("warning")),
        "documentation_dirty_ignored": bool(dirty.get("documentation_only")),
        "next_required_action": next_action,
        "safe_command": safe_command,
        "explanation": explanation,
        "diagnosis": diagnosis,
        "source_status": status,
    }


def run_unit_tests() -> dict[str, Any]:
    cmd = [sys.executable, "-m", "unittest", "tests/unit/test_v7_sync_tools.py", "tests/unit/test_v7_truth_check.py"]
    return run_command(cmd, ROOT, 120)


def release_sync_plan(
    *,
    apply: bool,
    message: str,
    confirm: str,
    allow_runtime_critical: bool,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    blockers: list[str] = []
    if apply and confirm != RELEASE_SYNC_CONFIRMATION:
        blockers.append("release_sync_confirmation_required")
    initial = sync_status(runner=runner)
    tests = run_unit_tests()
    commit_result = safe_commit_plan(
        message=message,
        apply=apply,
        allow_runtime_critical=allow_runtime_critical,
        runner=runner,
    )
    push_result = safe_push_plan(apply=apply, runner=runner)
    deploy_result = safe_deploy_plan(
        apply=apply,
        confirm=DEPLOY_CONFIRMATION if apply else "",
        update_local_snapshot=apply,
        restart_admin_if_changed=False,
        runner=runner,
    )
    final_truth = truth_check("all", runner=runner) if not apply else truth_check("all", runner=runner)
    if not tests.get("ok"):
        blockers.append("unit_tests_failed")
    for name, section in (
        ("commit", commit_result),
        ("push", push_result),
        ("deploy", deploy_result),
        ("truth", final_truth),
    ):
        if section.get("final_verdict") != "PASS":
            blockers.append(f"{name}_stage_no_go")
    return {
        "tool": "v7-release-sync",
        "schema": "v7-release-sync/v1",
        "mode": "apply" if apply else "dry-run",
        "initial_status": initial,
        "test_result": tests,
        "commit_result": commit_result,
        "push_result": push_result,
        "deploy_result": deploy_result,
        "final_truth_check": final_truth,
        "blockers": blockers,
        "warnings": [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }


def add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")


def add_apply_flags(parser: argparse.ArgumentParser, *, confirmation: str) -> None:
    parser.add_argument("--apply", action="store_true", help="perform the planned safe action")
    parser.add_argument("--confirm", default="", help=f"required confirmation token: {confirmation}")


def ensure_no_unsafe_tool_body(paths: Iterable[Path]) -> dict[str, Any]:
    findings = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "git push --force" in text or "--force-with-lease" in text:
            findings.append({"path": str(path), "issue": "force_push_token"})
        if "/usr/local/bin/v7-users-autoswitch --apply" in text:
            findings.append({"path": str(path), "issue": "autoswitch_apply_token"})
    return {
        "schema": "v7-sync-source-safety-scan/v1",
        "findings": findings,
        "final_verdict": "PASS" if not findings else "NO-GO",
    }


def executable_installed(path: Path) -> bool:
    return path.exists() and os.access(path, os.X_OK)


def copy_available() -> bool:
    return shutil.which("ssh") is not None
