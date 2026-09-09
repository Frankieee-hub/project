import importlib.util
import pathlib
import unittest
from datetime import date
from unittest.mock import patch

MODULE_PATH = pathlib.Path(__file__).with_name("fetch_tenders.py")
spec = importlib.util.spec_from_file_location("fetch_tenders", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class BidSignalTests(unittest.TestCase):
    def test_normalize_multilingual_values(self):
        value = {"eng": "Website design", "fra": ["Conception", "numérique"]}
        text = mod.normalize_text(value)
        self.assertIn("Website design", text)
        self.assertIn("Conception", text)
        self.assertIn("numérique", text)

    def test_flatten_and_score_notice(self):
        raw = {
            "publication-number": "123456-2026",
            "notice-title": {"eng": "Website redesign and digital marketing services"},
            "buyer-name": {"eng": "Example City"},
            "place-of-performance": ["France"],
            "description-proc": {"eng": "Branding, social media and website services"},
            "classification-cpv": ["72413000"],
            "publication-date": "2026-09-08",
            "deadline-receipt-tender-date-lot": "2026-10-01",
            "estimated-value-proc": "250000",
            "estimated-value-cur-proc": "EUR",
            "sme-lot": True,
        }
        notice = mod.flatten_notice(raw)
        profile = {
            "include": ["website", "digital marketing", "branding"],
            "exclude": ["printing equipment"],
            "countries": ["France"],
        }
        score, hits = mod.score_notice(notice, profile)
        self.assertGreaterEqual(score, 10)
        self.assertIn("website", hits)
        self.assertEqual(notice["currency"], "EUR")
        self.assertTrue(notice["sme_suitable"])

    def test_exclude_terms_penalize_match(self):
        notice = {
            "title": "Hardware supply and software development",
            "place": "Belgium",
            "sme_suitable": False,
            "search_text": "hardware supply and software development belgium",
        }
        profile = {
            "include": ["software development"],
            "exclude": ["hardware supply"],
            "countries": [],
        }
        score, _ = mod.score_notice(notice, profile)
        self.assertLess(score, 0)

    def test_iteration_fetch_deduplicates_and_reaches_empty_terminal_page(self):
        responses = [
            {
                "notices": [
                    {"publication-number": "A-2026"},
                    {"publication-number": "B-2026"},
                ],
                "iterationNextToken": "next-1",
                "totalNoticeCount": 3,
                "timedOut": False,
            },
            {
                "notices": [
                    {"publication-number": "B-2026"},
                    {"publication-number": "C-2026"},
                ],
                "iterationNextToken": "next-2",
                "timedOut": False,
            },
            {
                "notices": [],
                "iterationNextToken": None,
                "timedOut": False,
            },
        ]
        with patch.object(mod, "post_json", side_effect=responses):
            notices, timed_out = mod.fetch_publication_day(date(2026, 9, 8))
        self.assertEqual(len(notices), 3)
        self.assertFalse(timed_out)

    def test_live_request_disables_syntax_only_mode(self):
        payload = mod.request_for_date(date(2026, 9, 8))
        self.assertIn("estimated-value-proc", payload["fields"])
        self.assertIn("estimated-value-cur-proc", payload["fields"])
        self.assertIn("dispatch-date", payload["fields"])
        self.assertNotIn("estimated-value", payload["fields"])
        self.assertNotIn("document-sent-date", payload["fields"])
        self.assertEqual(payload["paginationMode"], "ITERATION")
        self.assertTrue(payload["onlyLatestVersions"])
        self.assertFalse(payload["checkQuerySyntax"])

    def test_validation_request_is_syntax_only(self):
        payload = mod.validation_request_for_date(date(2026, 9, 8))
        self.assertTrue(payload["checkQuerySyntax"])
        self.assertEqual(payload["limit"], 1)
        self.assertEqual(payload["paginationMode"], "PAGE_NUMBER")

    def test_expert_query_format(self):
        self.assertEqual(mod.expert_query_for_date(date(2026, 9, 8)), "publication-date=20260908")


if __name__ == "__main__":
    unittest.main()
