import unittest
from datetime import date

from scripts.update_dataset_from_amfi import parse_history_export, parse_latest_export


class ParseAmfiExportTests(unittest.TestCase):
    def test_parses_current_latest_format(self) -> None:
        text = """Scheme Code;ISIN Div Payout/ ISIN Growth;ISIN Div Reinvestment;Scheme Name;Plan;Option;Net Asset Value;Date
135762;INF846K01WO1;-;Axis Children's Fund;Direct Plan;Growth Option;30.5165;31-Aug-2026
"""

        rows = parse_latest_export(text)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].scheme_code, "135762")
        self.assertEqual(rows[0].scheme_name, "Axis Children's Fund")
        self.assertEqual(rows[0].nav, "30.5165")
        self.assertEqual(rows[0].nav_date, date(2026, 8, 31))

    def test_parses_current_history_format(self) -> None:
        text = """Scheme Code;NAV Name;Plan;Option;ISIN Div Payout/ISIN Growth;ISIN Div Reinvestment;Net Asset Value;Date
139619;Taurus Investor Education Pool - Unclaimed Dividend - Growth;;;;;10.0000;31-Aug-2026
"""

        rows = parse_history_export(text)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].scheme_code, "139619")
        self.assertEqual(rows[0].scheme_name, "Taurus Investor Education Pool - Unclaimed Dividend - Growth")
        self.assertEqual(rows[0].nav, "10.0000")

    def test_remains_compatible_with_legacy_latest_format(self) -> None:
        text = """Scheme Code;ISIN Div Payout/ ISIN Growth;ISIN Div Reinvestment;Scheme Name;Net Asset Value;Date
100001;;;Example Fund;12.34;21-Aug-2026
"""

        rows = parse_latest_export(text)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].nav, "12.34")

    def test_fails_loudly_when_header_changes_again(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "header was not found"):
            parse_latest_export("unexpected response")

    def test_history_allows_unpublished_date_without_header(self) -> None:
        self.assertEqual(parse_history_export(""), [])


if __name__ == "__main__":
    unittest.main()
