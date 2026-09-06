import importlib.machinery
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "v7-users-autoswitch"


def load_tool():
    loader = importlib.machinery.SourceFileLoader("polygon_only_route_truth_test", str(TOOL))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class PolygonOnlyRouteTruthTest(unittest.TestCase):
    def test_timestamp_is_not_route_truth_but_route_fact_is(self):
        module = load_tool()
        first = "===== V7 ROUTE CHECK =====\n2026-09-07T10:00:00+00:00\nUSER=10.0.0.1 TABLE=100 EXPECTED_DEV=awg0\nOK: route_get uses awg0\nV7_SCOPED_USER_ROUTE_CHECK=OK\n"
        same_route_later = first.replace("10:00:00", "10:05:00")
        changed_route = same_route_later.replace("uses awg0", "uses wg0")
        self.assertEqual(
            module.polygon_only_route_truth_fingerprint(first),
            module.polygon_only_route_truth_fingerprint(same_route_later),
        )
        self.assertNotEqual(
            module.polygon_only_route_truth_fingerprint(first),
            module.polygon_only_route_truth_fingerprint(changed_route),
        )

    def test_warn_or_probe_failure_is_not_admissible_route_truth(self):
        module = load_tool()
        self.assertTrue(module.polygon_only_route_truth_probe_valid(0, "V7_USER_ROUTE_CHECK=OK\n"))
        self.assertFalse(module.polygon_only_route_truth_probe_valid(0, "V7_USER_ROUTE_CHECK=WARN\n"))
        self.assertFalse(module.polygon_only_route_truth_probe_valid(1, "V7_USER_ROUTE_CHECK=OK\n"))
        self.assertFalse(module.polygon_only_route_truth_probe_valid(0, ""))
