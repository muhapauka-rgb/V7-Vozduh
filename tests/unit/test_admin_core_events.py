import json
import unittest
from pathlib import Path

from admin_core.events import (
    build_event_source_inventory,
    build_readonly_event_consumer_trace,
    event_source_profile,
    extract_user_ip,
    infer_event_severity,
    normalize_regression_event,
    parse_jsonl_lines,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "events"


def fixture_lines(name):
    return (FIXTURE_DIR / name).read_text(encoding="utf-8").splitlines()


class EventsHelperTest(unittest.TestCase):
    def test_parse_jsonl_lines_parses_valid_rows(self):
        rows = parse_jsonl_lines(fixture_lines("simple_events.jsonl"))
        self.assertEqual(rows[0]["action"], "admin_login")
        self.assertEqual(rows[1]["message"], "verify ok")

    def test_parse_jsonl_lines_preserves_malformed_rows_as_raw(self):
        rows = parse_jsonl_lines(fixture_lines("malformed_events.jsonl"))
        self.assertEqual(rows[0]["action"], "ok")
        self.assertEqual(rows[1], {"raw": "not json at all"})
        self.assertEqual(rows[2], {"raw": '{"action":"truncated",'})
        self.assertEqual(rows[3], {"raw": ""})
        self.assertEqual(rows[4]["action"], "after")

    def test_parse_jsonl_lines_accepts_redactor_callback(self):
        rows = parse_jsonl_lines(['{"token":"secret","safe":"ok"}'], redact_value=lambda value: {"redacted": value})
        self.assertEqual(rows, [{"redacted": {"token": "secret", "safe": "ok"}}])

    def test_tail_behavior_is_preserved_by_calling_code_slicing(self):
        lines = fixture_lines("large_tail.jsonl")
        rows = parse_jsonl_lines(lines[-3:])
        self.assertEqual([row["idx"] for row in rows], [8, 9, 10])

    def test_infer_event_severity_preserves_current_priority(self):
        rows = parse_jsonl_lines(fixture_lines("mixed_severity.jsonl"))
        self.assertEqual([infer_event_severity(row) for row in rows], ["error", "warning", "info", "warning", "info"])

    def test_missing_fields_default_to_info_or_keyword_based_severity(self):
        rows = parse_jsonl_lines(fixture_lines("missing_fields.jsonl"))
        self.assertEqual([infer_event_severity(row) for row in rows], ["info", "error", "warning"])

    def test_unicode_and_user_ip_extraction(self):
        rows = parse_jsonl_lines(fixture_lines("unicode_events.jsonl"))
        self.assertEqual(rows[0]["message"], "проверка прошла ok")
        self.assertEqual(extract_user_ip(rows[0]["message"]), "")
        self.assertEqual(extract_user_ip(rows[1]["message"]), "10.0.0.7")

    def test_extract_user_ip_uses_current_vpn_subnet_pattern_only(self):
        self.assertEqual(extract_user_ip("client 10.0.0.255 failed"), "10.0.0.255")
        self.assertEqual(extract_user_ip("client 10.7.0.2 failed"), "")
        self.assertEqual(extract_user_ip(None), "")

    def test_event_source_inventory_covers_autonomy_sources(self):
        inventory = build_event_source_inventory(
            {
                "telegram_sentinel": [{"source": "telegram_sentinel", "status": "DOWN", "updated_at": "2026-06-23T00:00:00Z"}],
                "service_matrix": [{"source": "service_matrix", "message": "youtube failed"}],
            },
            now="2026-06-23T00:01:00Z",
        )
        sources = {row["source"]: row for row in inventory}

        for source in (
            "telegram_sentinel",
            "service_matrix",
            "quality_compact",
            "capacity_signals",
            "runtime_readiness",
            "route_readiness",
            "planner_blocker_transitions",
            "trust_evolution_changes",
            "prediction_signals",
        ):
            self.assertIn(source, sources)
            self.assertIn(sources[source]["event_class"], {"PRIMARY EVENT", "SECONDARY EVENT", "DIAGNOSTIC EVENT"})

        self.assertEqual(sources["telegram_sentinel"]["event_count"], 1)
        self.assertEqual(sources["service_matrix"]["event_count"], 1)
        self.assertEqual(sources["telegram_sentinel"]["owner"], event_source_profile("telegram")["owner"])

    def test_regression_event_survives_refresh_rebuild_and_reread(self):
        source_event = {
            "source": "service_matrix",
            "channel": "vless",
            "message": "Telegram failed",
            "updated_at": "2026-06-23T00:00:00Z",
            "confidence": 0.91,
        }

        first = normalize_regression_event(source_event)
        refreshed = normalize_regression_event(dict(source_event))
        reread = normalize_regression_event(parse_jsonl_lines([json.dumps(source_event)])[0])

        self.assertEqual(first["event_id"], refreshed["event_id"])
        self.assertEqual(first["event_id"], reread["event_id"])
        self.assertEqual(first["event_class"], "PRIMARY EVENT")
        self.assertTrue(first["read_only"])
        self.assertTrue(first["preview_only"])
        self.assertFalse(first["synthetic_event"])

    def test_readonly_event_consumer_routes_real_events_to_planner_preview_candidates(self):
        trace = build_readonly_event_consumer_trace(
            [
                {"source": "service_matrix", "channel": "vless", "message": "service failed", "updated_at": "2026-06-23T00:00:00Z"},
                {"source": "prediction_signals", "message": "prediction drift", "updated_at": "2026-06-23T00:00:00Z"},
            ],
            now="2026-06-23T00:01:00Z",
        )

        self.assertTrue(trace["read_only"])
        self.assertTrue(trace["preview_only"])
        self.assertFalse(trace["execution_allowed_now"])
        self.assertEqual(trace["event_count"], 2)
        self.assertEqual(trace["primary_event_count"], 1)
        self.assertEqual(trace["diagnostic_event_count"], 1)
        self.assertEqual(trace["planner_preview_event_count"], 1)
        self.assertEqual(trace["certification_state"], "CERTIFIED_READONLY_CONSUMER")
        self.assertFalse(trace["synthetic_events_created"])
        self.assertFalse(trace["new_truth_source_created"])


if __name__ == "__main__":
    unittest.main()
