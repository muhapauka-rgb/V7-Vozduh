"""Read-only operator view facade for admin API handlers."""

from __future__ import annotations

from pathlib import Path

from admin_core import operator_observability


def operator_view_model(*, repo_root: Path, state_dir: Path, event_dir: Path) -> dict:
    return operator_observability.build_operator_view_model(
        repo_root=repo_root,
        state_dir=state_dir,
        event_dir=event_dir,
    )


def approval_preview(*, repo_root: Path, state_dir: Path, event_dir: Path) -> dict:
    return operator_observability.build_operator_approval_preview(
        repo_root=repo_root,
        state_dir=state_dir,
        event_dir=event_dir,
    )


def lineage_archive(*, repo_root: Path) -> dict:
    return operator_observability.build_operator_lineage_archive(repo_root=repo_root)


def operation_detail(operation_id: str, *, repo_root: Path) -> dict:
    return operator_observability.build_operator_operation_detail(operation_id, repo_root=repo_root)


def audit_search(
    *,
    repo_root: Path,
    query: str = "",
    operation_type: str = "",
    state: str = "",
    evidence_kind: str = "",
    limit: int = 60,
) -> dict:
    return operator_observability.build_operator_audit_search(
        repo_root=repo_root,
        query=query,
        operation_type=operation_type,
        state=state,
        evidence_kind=evidence_kind,
        limit=limit,
    )


def audit_export_preview(operation_id: str = "", *, repo_root: Path) -> dict:
    return operator_observability.build_operator_audit_export_preview(operation_id, repo_root=repo_root)


def execution_governance_preview(operation_id: str = "", *, repo_root: Path) -> dict:
    return operator_observability.build_operator_execution_governance_preview(operation_id, repo_root=repo_root)


def execution_rehearsal_preview(operation_id: str = "", *, repo_root: Path) -> dict:
    return operator_observability.build_operator_execution_rehearsal_preview(operation_id, repo_root=repo_root)


def approved_execution_controller_preview(decision: str = "DRAFT", *, repo_root: Path) -> dict:
    return operator_observability.build_operator_approved_execution_controller_preview(decision, repo_root=repo_root)


def evidence_archive(*, repo_root: Path) -> dict:
    return operator_observability.build_operator_evidence_archive(repo_root=repo_root)


def evidence_file_detail(evidence_id: str, *, repo_root: Path) -> dict:
    return operator_observability.build_operator_evidence_file_detail(evidence_id, repo_root=repo_root)
