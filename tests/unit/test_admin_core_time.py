import unittest
from unittest import mock

from admin_core.time import age_sec, now_iso, parse_ts


class TimeHelperTest(unittest.TestCase):
    def test_now_iso_returns_timezone_aware_iso_string(self):
        value = now_iso()
        self.assertIn("+00:00", value)
        self.assertIsNotNone(parse_ts(value))

    def test_parse_ts_accepts_z_and_naive_values_as_utc(self):
        self.assertEqual(parse_ts("1970-01-01T00:00:00Z"), 0)
        self.assertEqual(parse_ts("1970-01-01T00:00:00"), 0)

    def test_parse_ts_returns_none_for_invalid_values(self):
        self.assertIsNone(parse_ts(""))
        self.assertIsNone(parse_ts(None))
        self.assertIsNone(parse_ts("not-a-date"))

    def test_age_sec_uses_clock_and_clamps_negative(self):
        with mock.patch("admin_core.time._time.time", return_value=100):
            self.assertEqual(age_sec("1970-01-01T00:01:30Z"), 10)
            self.assertEqual(age_sec("1970-01-01T00:02:30Z"), 0)
            self.assertIsNone(age_sec("bad"))


if __name__ == "__main__":
    unittest.main()

