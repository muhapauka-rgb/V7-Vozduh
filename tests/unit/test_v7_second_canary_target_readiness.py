import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-second-canary-target-readiness"


def load_tool_module():
    loader = importlib.machinery.SourceFileLoader("v7_second_canary_target_readiness", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class SecondCanaryTargetReadinessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = load_tool_module()

    def write_state(
        self,
        root: Path,
        *,
        users_extra: str = "",
        egress_extra: str = "",
        load_extra: str = "",
        diagnose_extra: str = "",
        stability_extra: str = "",
        interface_extra: str = "",
    ) -> None:
        (root / "users.registry").write_text(
            "ip=10.7.0.14 current=vless table=1012 enabled=1\n" + users_extra,
            encoding="utf-8",
        )
        (root / "egress.registry").write_text(
            "id=vless interface=tun0 enabled=1 role=baseline\n" + egress_extra,
            encoding="utf-8",
        )
        (root / "egress-load.state").write_text(load_extra, encoding="utf-8")
        (root / "egress-diagnose.state").write_text(diagnose_extra, encoding="utf-8")
        (root / "egress-stability.state").write_text(stability_extra, encoding="utf-8")
        (root / "interface-state.state").write_text(interface_extra, encoding="utf-8")

    def test_occupied_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                users_extra="ip=10.7.0.5 current=1 table=1003 enabled=1\n",
                egress_extra="id=1 interface=v7target enabled=1 role=GLOBAL_FAST exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU\n",
                load_extra="1_users=1 1_load_status=SOFT_FULL\n",
                diagnose_extra="1_severity=OK\n",
                stability_extra="1_avg_mbps=60 1_min_mbps=50 1_stability=0.9\n",
                interface_extra="v7target=UP,LOWER_UP\n",
            )
            report = self.checker.readiness_report(root, "10.7.0.14", "vless")
            target = report["target_candidates"][0]
            self.assertEqual(target["egress_id"], "1")
            self.assertEqual(target["status"], "NO-GO")
            self.assertIn("occupied by registry users: 10.7.0.5", target["rejection_reasons"])
            self.assertEqual(report["selected_target"], "NONE")

    def test_low_quality_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                egress_extra="id=awg0 interface=awg0 enabled=1 role=GLOBAL_STABLE exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU\n",
                load_extra="awg0_users=0 awg0_load_status=OK\n",
                diagnose_extra="awg0_severity=OK\n",
                stability_extra="awg0_avg_mbps=11 awg0_min_mbps=4 awg0_stability=0.35\n",
                interface_extra="awg0=UP,LOWER_UP\n",
            )
            target = self.checker.readiness_report(root, "10.7.0.14", "vless")["target_candidates"][0]
            self.assertEqual(target["status"], "NO-GO")
            self.assertIn("avg_mbps below floor (11.0)", target["rejection_reasons"])
            self.assertIn("min_mbps below floor (4.0)", target["rejection_reasons"])

    def test_suspect_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                egress_extra="id=ovpn interface=v7ovpn enabled=1 role=GLOBAL_FAST exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU\n",
                load_extra="ovpn_users=0 ovpn_load_status=OK\n",
                diagnose_extra="ovpn_severity=SUSPECT\n",
                stability_extra="ovpn_avg_mbps=60 ovpn_min_mbps=50 ovpn_stability=0.9\n",
                interface_extra="v7ovpn=UP,LOWER_UP\n",
            )
            target = self.checker.readiness_report(root, "10.7.0.14", "vless")["target_candidates"][0]
            self.assertEqual(target["status"], "NO-GO")
            self.assertIn("diagnose SUSPECT", target["rejection_reasons"])

    def test_diagnose_severity_suffix_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                egress_extra="id=fast2 interface=v7fast2 enabled=1 role=GLOBAL_FAST exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU\n",
                load_extra="fast2_users=0 fast2_load_status=OK\n",
                diagnose_extra="fast2_diagnose_severity=OK fast2_diagnose_detail=handshake_age_seconds=12\n",
                stability_extra="fast2_avg_mbps=70 fast2_min_mbps=55 fast2_stability=0.95\n",
                interface_extra="v7fast2=UP,LOWER_UP\n",
            )
            target = self.checker.readiness_report(root, "10.7.0.14", "vless")["target_candidates"][0]
            self.assertEqual(target["diagnose_status"], "OK")
            self.assertEqual(target["status"], "GO")

    def test_clean_zero_user_ok_target_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                egress_extra="id=fast2 interface=v7fast2 enabled=1 role=GLOBAL_FAST exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU\n",
                load_extra="fast2_users=0 fast2_load_status=OK\n",
                diagnose_extra="fast2_severity=OK\n",
                stability_extra="fast2_avg_mbps=70 fast2_min_mbps=55 fast2_stability=0.95\n",
                interface_extra="v7fast2=UP,LOWER_UP\n",
            )
            report = self.checker.readiness_report(root, "10.7.0.14", "vless")
            self.assertEqual(report["approval_status"], "GO")
            self.assertEqual(report["selected_target"], "fast2")

    def test_reserved_wireguard_ok_target_selected_after_diagnose_fix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                egress_extra=(
                    "id=wireguard-1779454504-c43409 interface=v7wg enabled=1 role=GLOBAL_FAST "
                    "exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true\n"
                ),
                load_extra="wireguard-1779454504-c43409_users=0 wireguard-1779454504-c43409_load_status=OK\n",
                diagnose_extra=(
                    "wireguard-1779454504-c43409_diagnose_severity=OK "
                    "wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=8\n"
                ),
                stability_extra=(
                    "wireguard-1779454504-c43409_avg_mbps=52 "
                    "wireguard-1779454504-c43409_min_mbps=48 "
                    "wireguard-1779454504-c43409_stability=0.93\n"
                ),
                interface_extra="v7wg=UP,LOWER_UP\n",
            )
            report = self.checker.readiness_report(root, "10.7.0.14", "vless")
            target = report["target_candidates"][0]
            self.assertEqual(target["egress_id"], "wireguard-1779454504-c43409")
            self.assertEqual(target["status"], "GO")
            self.assertEqual(report["selected_target"], "wireguard-1779454504-c43409")

    def test_live_quality_summary_and_diagnose_can_replace_stale_state_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                egress_extra=(
                    "id=wireguard-1779454504-c43409 interface=v7wg enabled=1 role=GLOBAL_FAST "
                    "exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true\n"
                ),
                load_extra="wireguard-1779454504-c43409_users=0 wireguard-1779454504-c43409_load_status=OK\n",
                diagnose_extra=(
                    "wireguard-1779454504-c43409_diagnose_severity=OK "
                    "wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=103\n"
                ),
                stability_extra="",
                interface_extra="",
            )
            (root / "egress-quality-summary.json").write_text(
                json.dumps(
                    {
                        "items": {
                            "wireguard-1779454504-c43409": {
                                "windows": {
                                    "1h": {
                                        "avg_mbps": 32.314,
                                        "min_mbps": 24.826,
                                        "stability": 0.7586,
                                    }
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            report = self.checker.readiness_report(root, "10.7.0.14", "vless")
            target = report["target_candidates"][0]
            self.assertEqual(target["egress_id"], "wireguard-1779454504-c43409")
            self.assertEqual(target["status"], "GO")
            self.assertEqual(target["avg_mbps"], 32.314)
            self.assertTrue(target["interface_up_lower_up"])
            self.assertIn("interface_state_inferred_from_diagnose", target["warnings"])

    def test_no_target_is_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(root)
            report = self.checker.readiness_report(root, "10.7.0.14", "vless")
            self.assertEqual(report["approval_status"], "NO-GO")
            self.assertEqual(report["selected_target"], "NONE")

    def test_candidate_invalid_is_no_go_even_with_clean_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(
                root,
                users_extra="ip=10.7.0.14 current=1 table=1012 enabled=1\n",
                egress_extra="id=fast2 interface=v7fast2 enabled=1 role=GLOBAL_FAST exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU\n",
                load_extra="fast2_users=0 fast2_load_status=OK\n",
                diagnose_extra="fast2_severity=OK\n",
                stability_extra="fast2_avg_mbps=70 fast2_min_mbps=55 fast2_stability=0.95\n",
                interface_extra="v7fast2=UP,LOWER_UP\n",
            )
            report = self.checker.readiness_report(root, "10.7.0.14", "vless")
            self.assertFalse(report["candidate_still_valid"])
            self.assertEqual(report["approval_status"], "NO-GO")
            self.assertEqual(report["selected_target"], "NONE")

    def test_cli_json_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_state(root)
            proc = subprocess.run(
                [sys.executable, str(TOOL), "--state-dir", str(root), "--json"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertFalse(payload["mutation"])
            self.assertFalse(payload["runtime_commands_executed"])


if __name__ == "__main__":
    unittest.main()
