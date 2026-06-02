#!/usr/bin/env python3
"""Safe source-to-production sync helpers for V7.

The helpers in this module are fail-closed by design. They reuse
``tools/v7-truth-check`` for source-of-truth decisions and only model deployment
of explicitly approved binaries.
"""

from __future__ import annotations

import argparse
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
        "name": "v7-admin-api",
        "local_path": "admin/v7-admin-api",
        "remote_path": "/usr/local/bin/v7-admin-api",
        "mode": "0755",
        "service": "v7-admin-api.service",
    },
]

FORBIDDEN_USER_ARGS = {"--force", "-f", "--force-with-lease", "--delete", "--mirror"}
FORBIDDEN_RUNTIME_TOKENS = {
    "autoswitch_apply",
    "restore_barrier_mutation",
    "routing_mutation",
    "user_movement",
    "planner_mutation",
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
    return {
        "schema": "v7-deploy-manifest/v1",
        "project": "V7 Vozduh",
        "created_at": utc_now(),
        "deploy_id": deploy_id,
        "deploy_branch": branch,
        "deploy_commit": commit,
        "deployment_model": "copied_binaries_with_safe_sync_manifest",
        "approved_deploy_files": deploy_file_records(),
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
        "rollback_manifest_required": True,
        "service_restart_required": False,
    }


def production_hashes_from_snapshot() -> dict[str, str]:
    manifest = load_manifest()
    snapshot_path = ROOT / str(manifest.get("runtime_snapshot_path", ""))
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
    blockers: list[str] = []
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if truth.get("final_verdict") != "PASS":
        blockers.append("github_truth_check_failed")
    if any(not item["exists"] for item in deploy_file_records()):
        blockers.append("approved_deploy_file_missing")
    changed_admin = any(item["name"] == "v7-admin-api" and not item["matches"] for item in delta)
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
        "deployment_required": any(not item["matches"] for item in delta),
        "restart_admin_if_changed": restart_admin_if_changed,
        "planned_remote_paths": planned_remote_paths,
        "deploy_manifest": deploy_manifest,
        "runtime_linkage": runtime_linkage,
        "release_manifest": release_manifest,
        "blockers": blockers,
        "warnings": [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    ssh_target = os.environ.get("V7_PROD_SSH_TARGET", "root@195.2.79.116")
    payload = {
        "deploy_manifest": deploy_manifest,
        "runtime_linkage": runtime_linkage,
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
    restart_block = "systemctl restart v7-admin-api.service\n" if restart_admin_if_changed and changed_admin else ""
    script = (
        "set -eu\n"
        f"backup_root={planned_remote_paths['backup_root']}\n"
        f"release_dir={planned_remote_paths['release_dir']}\n"
        "mkdir -p \"$backup_root\" \"$release_dir\"\n"
        "for f in /usr/local/bin/v7-users-autoswitch /usr/local/bin/v7-audit-log /usr/local/bin/v7-admin-api; do "
        "if test -e \"$f\"; then cp -p \"$f\" \"$backup_root/$(basename \"$f\").pre-sync\"; fi; done\n"
        "python3 - <<'PY'\n"
        "import base64, json, os, pathlib\n"
        f"payload=json.loads(base64.b64decode('{payload_b64}').decode('utf-8'))\n"
        "for item in payload['files']:\n"
        "    if not item.get('replace'):\n"
        "        continue\n"
        "    remote=pathlib.Path(item['remote_path'])\n"
        "    tmp=remote.with_suffix(remote.suffix + '.v7-sync-new')\n"
        "    tmp.write_bytes(base64.b64decode(item['content_b64']))\n"
        "    os.chmod(tmp, int(item['mode'], 8))\n"
        "    tmp.replace(remote)\n"
        "pathlib.Path('/opt/v7/deploy-manifest.json').write_text(json.dumps(payload['deploy_manifest'], indent=2, ensure_ascii=False)+'\\n')\n"
        "pathlib.Path('/opt/v7/runtime-linkage.json').write_text(json.dumps(payload['runtime_linkage'], indent=2, ensure_ascii=False)+'\\n')\n"
        f"pathlib.Path('{planned_remote_paths['release_manifest']}').write_text(json.dumps(payload['release_manifest'], indent=2, ensure_ascii=False)+'\\n')\n"
        "PY\n"
        f"{restart_block}"
        f"ln -sfn {planned_remote_paths['release_dir']} /opt/v7/releases/current\n"
    )
    ssh_result = runner(["ssh", ssh_target, script], ROOT, 120)
    result["command_results"] = {"ssh_manifest_refresh": ssh_result}
    if not ssh_result.get("ok"):
        result["blockers"].append("production_manifest_refresh_failed")
    elif update_local_snapshot:
        update_snapshot_for_deploy(deploy_id=deploy_id, branch=branch, commit=commit)
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def update_snapshot_for_deploy(*, deploy_id: str, branch: str, commit: str) -> None:
    manifest = load_manifest()
    snapshot_path = ROOT / str(manifest.get("runtime_snapshot_path", ""))
    if not snapshot_path.exists():
        return
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
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
