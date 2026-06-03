"""Read-only registry view helpers for the V7 admin API.

This module owns pure loading and serialization helpers for users.registry and
egress.registry admin views. It must not import runtime action helpers, write
files, execute commands, or mutate runtime state.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from admin_core.registry_readers import parse_registry_lines
from admin_core.sanitize import redact


SAFE_EGRESS_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
SAFE_IP_RE = re.compile(r"^10\.(0\.0|7\.[0-3])\.[0-9]{1,3}$")


def read_text(path: Path | str, default: str = "") -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    except OSError as exc:
        return f"ERROR: {exc}"


def safe_egress_id(value: Any) -> str:
    value = str(value or "").strip()
    if not SAFE_EGRESS_RE.match(value):
        return ""
    return value


def safe_user_ip(value: Any) -> str:
    value = str(value or "").strip()
    if not SAFE_IP_RE.match(value):
        return ""
    try:
        last = int(value.rsplit(".", 1)[1])
    except (IndexError, ValueError):
        return ""
    if last < 2 or last > 254:
        return ""
    return value


def parse_registry(path: Path | str) -> list[dict[str, Any]]:
    return redact(parse_registry_lines(read_text(path).splitlines()))


def registry_rows(path: Path | str, *, enabled_only: bool = False) -> list[dict[str, Any]]:
    rows = parse_registry(path)
    if enabled_only:
        rows = [row for row in rows if str(row.get("enabled", "1")) == "1"]
    return rows


def registry_map(path: Path | str, *, key: str = "id", enabled_only: bool = False) -> dict[str, dict[str, Any]]:
    return {
        row.get(key): row
        for row in registry_rows(path, enabled_only=enabled_only)
        if row.get(key)
    }


def egress_registry_rows(state_dir: Path | str, *, enabled_only: bool = False) -> list[dict[str, Any]]:
    return registry_rows(Path(state_dir) / "egress.registry", enabled_only=enabled_only)


def egress_registry_map(state_dir: Path | str, *, enabled_only: bool = False) -> dict[str, dict[str, Any]]:
    return {
        row.get("id"): row
        for row in egress_registry_rows(state_dir, enabled_only=enabled_only)
        if row.get("id")
    }


def egress_exists(state_dir: Path | str, egress_id: Any, *, enabled_only: bool = False) -> bool:
    egress_id = safe_egress_id(egress_id)
    return bool(egress_id and egress_id in egress_registry_map(state_dir, enabled_only=enabled_only))


def default_egress_id(state_dir: Path | str) -> str:
    rows = egress_registry_rows(state_dir, enabled_only=True)
    return rows[0].get("id", "") if rows else ""


def egress_interface(state_dir: Path | str, egress_id: Any) -> str:
    row = egress_registry_map(state_dir).get(safe_egress_id(egress_id), {})
    return row.get("interface", "")


def users_registry_rows(state_dir: Path | str, *, enabled_only: bool = False) -> list[dict[str, Any]]:
    return registry_rows(Path(state_dir) / "users.registry", enabled_only=enabled_only)


def users_registry_map(state_dir: Path | str, *, enabled_only: bool = False) -> dict[str, dict[str, Any]]:
    return {
        row.get("ip"): row
        for row in users_registry_rows(state_dir, enabled_only=enabled_only)
        if row.get("ip")
    }


def default_active_user_ip(users: list[dict[str, Any]]) -> str:
    for user in users:
        ip = safe_user_ip(user.get("ip", ""))
        if ip and str(user.get("enabled", "1")) == "1":
            return ip
    return "10.0.0.3"


@dataclass
class AdminRegistrySnapshot:
    state_dir: Path
    users: list[dict[str, Any]]
    egress: list[dict[str, Any]]

    @classmethod
    def load(cls, state_dir: Path | str) -> "AdminRegistrySnapshot":
        root = Path(state_dir)
        return cls(
            state_dir=root,
            users=users_registry_rows(root),
            egress=egress_registry_rows(root),
        )

    def egress_rows(self, *, enabled_only: bool = False) -> list[dict[str, Any]]:
        if not enabled_only:
            return list(self.egress)
        return [row for row in self.egress if str(row.get("enabled", "1")) == "1"]

    def egress_map(self, *, enabled_only: bool = False) -> dict[str, dict[str, Any]]:
        return {
            row.get("id"): row
            for row in self.egress_rows(enabled_only=enabled_only)
            if row.get("id")
        }

    def users_rows(self, *, enabled_only: bool = False) -> list[dict[str, Any]]:
        if not enabled_only:
            return list(self.users)
        return [row for row in self.users if str(row.get("enabled", "1")) == "1"]

    def users_map(self, *, enabled_only: bool = False) -> dict[str, dict[str, Any]]:
        return {
            row.get("ip"): row
            for row in self.users_rows(enabled_only=enabled_only)
            if row.get("ip")
        }

    def default_egress_id(self) -> str:
        rows = self.egress_rows(enabled_only=True)
        return rows[0].get("id", "") if rows else ""

    def egress_interface(self, egress_id: Any) -> str:
        row = self.egress_map().get(safe_egress_id(egress_id), {})
        return row.get("interface", "")
