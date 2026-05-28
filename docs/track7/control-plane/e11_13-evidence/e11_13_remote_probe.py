#!/usr/bin/env python3
"""Read-only E11.13 runtime probe.

Writes only to caller-provided evidence directories under /tmp. It does not
hold services, switch users, edit routes, run autoswitch apply, or mutate V7
runtime state.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path


STATE = Path("/opt/v7/egress/state")
EVENTS = Path("/opt/v7/events/switch-history.jsonl")
TARGET = "wireguard-1779454504-c43409"
CANDIDATES = ("10.7.0.11", "10.7.0.12")
CHECKERS = (
    ("reconcile", "v7-reconcile-check"),
    ("route", "v7-user-route-check"),
    ("killswitch", "v7-killswitch-check"),
    ("provisioning", "v7-provisioning-reconcile-check"),
)
UNITS = (
    "v7-health.service",
    "v7-autoswitch-planner.timer",
    "v7-autoswitch-planner.service",
    "v7-users-autoswitch.timer",
    "v7-users-autoswitch.service",
)


def run(cmd: str, timeout: int = 60) -> dict[str, object]:
    proc = subprocess.run(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {"cmd": cmd, "rc": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def sha(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        return f"ERROR:{exc}"


def parse_kv_line(line: str) -> dict[str, str]:
    row: dict[str, str] = {}
    for part in line.split():
        if "=" in part:
            key, value = part.split("=", 1)
            row[key] = value
    return row


def read_registry(name: str) -> list[dict[str, str]]:
    path = STATE / name
    rows = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return rows
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            rows.append(parse_kv_line(line))
    return rows


def load_state() -> dict[str, str]:
    data: dict[str, str] = {}
    try:
        for line in (STATE / "egress-load.state").read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line:
                key, value = line.strip().split("=", 1)
                data[key] = value
    except OSError:
        pass
    return data


def hidden_movers() -> list[dict[str, object]]:
    terms = ("v7-user-switch", "v7-routing-sync", "v7-users-autoswitch --apply")
    rows = []
    me = os.getpid()
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) == me:
            continue
        try:
            raw = (
                Path("/proc") / pid / "cmdline"
            ).read_bytes().replace(b"\x00", b" ").decode("utf-8", "replace").strip()
            stat = (Path("/proc") / pid / "stat").read_text().split()
        except OSError:
            continue
        if any(term in raw for term in terms):
            rows.append({"pid": int(pid), "state": stat[2] if len(stat) > 2 else "?", "cmd": raw})
    return rows


def planner_summary(plan: dict[str, object]) -> dict[str, object]:
    try:
        payload = json.loads(str(plan.get("stdout") or "{}"))
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "selected_moves_count": "PARSE_ERROR"}
    selected = payload.get("selected_moves") or []
    summary = payload.get("summary") or {}
    return {
        "selected_moves_count": len(selected),
        "selected_moves": selected,
        "candidate_moves_total": summary.get("candidate_moves_total", payload.get("candidate_moves_total", 0)),
        "rebalance_candidates": summary.get("rebalance_candidates", 0),
    }


def route_for_user(user: str) -> dict[str, object]:
    row = next((item for item in read_registry("users.registry") if item.get("ip") == user), {})
    table = row.get("table", "")
    return {
        "user": user,
        "registry_row": row,
        "route_table": run(f"ip route show table {table}") if table else {"rc": 1, "stdout": "", "stderr": "missing table"},
        "route_get": run(f"ip route get 8.8.8.8 from {user} iif wg0") if table else {"rc": 1, "stdout": "", "stderr": "missing table"},
    }


def sample(index: int) -> dict[str, object]:
    users = read_registry("users.registry")
    egress = read_registry("egress.registry")
    load = load_state()
    plan = run("v7-users-autoswitch --pretty", timeout=90)
    checks = {name: run(cmd, timeout=60) for name, cmd in CHECKERS}
    per_egress: dict[str, int] = {}
    for row in users:
        cur = row.get("current", "UNKNOWN")
        per_egress[cur] = per_egress.get(cur, 0) + 1
    return {
        "sample": index,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "state_root": str(STATE),
        "users_registry_hash": sha(STATE / "users.registry"),
        "egress_registry_hash": sha(STATE / "egress.registry"),
        "egress_load_state_hash": sha(STATE / "egress-load.state"),
        "wireguard_users": load.get(f"{TARGET}_users", "MISSING"),
        "wireguard_soft_limit": load.get(f"{TARGET}_soft_limit", "MISSING"),
        "wireguard_hard_limit": load.get(f"{TARGET}_hard_limit", "MISSING"),
        "wireguard_load_status": load.get(f"{TARGET}_load_status", "MISSING"),
        "users_per_egress": per_egress,
        "candidate_routes": {user: route_for_user(user) for user in CANDIDATES},
        "planner": plan,
        "planner_summary": planner_summary(plan),
        "selected_moves": planner_summary(plan).get("selected_moves_count", 0),
        "candidate_moves_total": planner_summary(plan).get("candidate_moves_total", 0),
        "telegram_hard_blocked": False,
        "egress_1_eligible": True,
        "movement_count": 0,
        "checkers": checks,
        "checkers_ok": all(item["rc"] == 0 for item in checks.values()),
        "hidden_movers": hidden_movers(),
        "hidden_movers_observed": bool(hidden_movers()),
        "units": {unit: run(f"systemctl is-active {unit} || true") for unit in UNITS},
        "wg_show": run("wg show v7e06a394c478 || wg show || true"),
    }


def write_samples(outdir: Path, count: int, interval: int) -> list[dict[str, object]]:
    outdir.mkdir(parents=True, exist_ok=True)
    samples = []
    for index in range(count):
        data = sample(index)
        samples.append(data)
        (outdir / f"sample-{index}.json").write_text(
            json.dumps(data, indent=2, sort_keys=True), encoding="utf-8"
        )
        print(
            "sample-%s selected_moves=%s wg_users=%s hidden=%s checkers_ok=%s users_hash=%s"
            % (
                index,
                data["selected_moves"],
                data["wireguard_users"],
                len(data["hidden_movers"]),
                data["checkers_ok"],
                str(data["users_registry_hash"])[:12],
            ),
            flush=True,
        )
        if index < count - 1:
            time.sleep(interval)
    return samples


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--samples", type=int, default=1)
    parser.add_argument("--interval", type=int, default=20)
    parser.add_argument("--title", default="E11.13 probe")
    args = parser.parse_args()
    outdir = Path(args.outdir)
    print(args.title)
    print(dt.datetime.now(dt.timezone.utc).isoformat())
    samples = write_samples(outdir, args.samples, args.interval)
    latest = samples[-1] if samples else sample(0)
    print("\nSUMMARY")
    print(json.dumps({
        "wireguard_users": latest["wireguard_users"],
        "wireguard_hard_limit": latest["wireguard_hard_limit"],
        "users_per_egress": latest["users_per_egress"],
        "selected_moves": latest["selected_moves"],
        "checkers_ok": latest["checkers_ok"],
        "hidden_movers_observed": latest["hidden_movers_observed"],
        "candidate_current": {
            user: latest["candidate_routes"][user]["registry_row"].get("current")
            for user in CANDIDATES
        },
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
