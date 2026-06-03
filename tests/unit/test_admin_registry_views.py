import inspect
import tempfile
import unittest
from pathlib import Path

from admin_core import admin_registry_views as views


class AdminRegistryViewsTest(unittest.TestCase):
    def write_state(self, root: Path):
        state = root / "state"
        state.mkdir()
        (state / "users.registry").write_text(
            "\n".join(
                [
                    "ip=10.7.0.2 current=awg0 enabled=1 password=secret",
                    "ip=10.7.0.3 current=vless enabled=0 token=hidden",
                    "malformed",
                    "ip=10.7.0.4 current=awg3 enabled=1",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (state / "egress.registry").write_text(
            "\n".join(
                [
                    "id=awg0 interface=awg0 enabled=1 role=GLOBAL_STABLE private_key=secret",
                    "id=vless interface=tun0 enabled=0 role=GLOBAL_FAST",
                    "broken",
                    "id=awg3 interface=awg3 enabled=1 role=GLOBAL_FAST",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return state

    def test_user_registry_view_parity_and_redaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(Path(tmp))
            rows = views.users_registry_rows(state)
            self.assertEqual(rows[0]["ip"], "10.7.0.2")
            self.assertEqual(rows[0]["password"], "[REDACTED]")
            self.assertEqual(rows[1]["token"], "[REDACTED]")
            self.assertEqual(rows[2], {})
            enabled = views.users_registry_rows(state, enabled_only=True)
            self.assertEqual([row.get("ip") for row in enabled], ["10.7.0.2", None, "10.7.0.4"])

    def test_egress_registry_view_parity_and_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(Path(tmp))
            rows = views.egress_registry_rows(state)
            self.assertEqual(rows[0]["private_key"], "[REDACTED]")
            self.assertEqual(rows[2], {})
            self.assertEqual(views.egress_registry_rows(state, enabled_only=True)[0]["id"], "awg0")
            self.assertEqual(views.egress_registry_map(state)["vless"]["interface"], "tun0")
            self.assertTrue(views.egress_exists(state, "awg0", enabled_only=True))
            self.assertFalse(views.egress_exists(state, "vless", enabled_only=True))
            self.assertEqual(views.default_egress_id(state), "awg0")
            self.assertEqual(views.egress_interface(state, "awg3"), "awg3")
            self.assertEqual(views.egress_interface(state, "../../bad"), "")

    def test_missing_file_and_malformed_row_handling(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"
            state.mkdir()
            self.assertEqual(views.users_registry_rows(state), [])
            self.assertEqual(views.egress_registry_rows(state), [])
            registry = state / "custom.registry"
            registry.write_text("not-a-kv\nid=x key=value\n", encoding="utf-8")
            self.assertEqual(views.parse_registry(registry), [{}, {"id": "x", "key": "value"}])

    def test_request_snapshot_foundation_reuses_loaded_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = self.write_state(Path(tmp))
            snapshot = views.AdminRegistrySnapshot.load(state)
            self.assertEqual(len(snapshot.users_rows()), 4)
            self.assertEqual(snapshot.default_egress_id(), "awg0")
            self.assertEqual(snapshot.egress_interface("vless"), "tun0")
            (state / "egress.registry").write_text("id=new interface=new0 enabled=1\n", encoding="utf-8")
            self.assertNotIn("new", snapshot.egress_map())
            self.assertIn("new", views.egress_registry_map(state))

    def test_no_write_or_action_api_exposed(self):
        public = {name for name in dir(views) if not name.startswith("_")}
        forbidden_names = {"run_action", "write_json_atomic", "write_text_atomic", "audit_admin", "append_record"}
        self.assertTrue(public.isdisjoint(forbidden_names))
        source = inspect.getsource(views)
        self.assertNotIn("subprocess", source)
        self.assertNotIn("os.replace", source)
        self.assertNotIn("write_text(", source)
        self.assertNotIn("run_action", source)


if __name__ == "__main__":
    unittest.main()
