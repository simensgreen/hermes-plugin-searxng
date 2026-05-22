"""Unit tests for hermes-plugin-searxng (no network)."""
import json
import unittest
from unittest.mock import patch

from tools import (
    _dedupe_and_rank,
    _max_results_per_query,
    searxng_handler,
)


class TestMaxResultsPerQuery(unittest.TestCase):
    def test_explicit_override(self):
        self.assertEqual(_max_results_per_query({"max_results": 7}, 4), 7)

    def test_defaults_by_query_count(self):
        self.assertEqual(_max_results_per_query({}, 1), 12)
        self.assertEqual(_max_results_per_query({}, 2), 7)
        self.assertEqual(_max_results_per_query({}, 4), 5)

    def test_minimum_one(self):
        self.assertEqual(_max_results_per_query({"max_results": 0}, 2), 1)


class TestDedupeAndRank(unittest.TestCase):
    def test_caps_per_bucket_merge(self):
        buckets = [
            [{"url": "https://a", "title": "A"}],
            [{"url": "https://b", "title": "B"}],
        ]
        merged = _dedupe_and_rank(buckets, 2)
        self.assertEqual(len(merged), 2)
        urls = {r["url"] for r in merged}
        self.assertEqual(urls, {"https://a", "https://b"})

    def test_dedupes_same_url(self):
        buckets = [
            [{"url": "https://a/", "title": "A1"}],
            [{"url": "https://a", "title": "A2"}],
        ]
        merged = _dedupe_and_rank(buckets, 5)
        self.assertEqual(len(merged), 1)


class TestSearxngHandler(unittest.TestCase):
    @patch("tools._search_base_url", return_value="")
    def test_missing_url(self, _mock_url):
        out = json.loads(searxng_handler({}))
        self.assertIn("error", out)

    @patch("tools._search_once")
    @patch("tools._search_base_url", return_value="https://search.example/search")
    def test_by_query_structure(self, _mock_base, mock_search):
        def fake_search(_b, q, _l, _c, cap):
            return [
                {
                    "title": f"{q}-{i}",
                    "url": f"https://example/{q}/{i}",
                    "snippet": "",
                    "engine": "t",
                }
                for i in range(cap)
            ]

        mock_search.side_effect = fake_search
        out = json.loads(searxng_handler({
            "queries": ["alpha", "beta"],
            "max_results": 2,
        }))
        self.assertEqual(out["max_results_per_query"], 2)
        self.assertEqual(len(out["by_query"]), 2)
        self.assertEqual(out["by_query"][0]["query"], "alpha")
        self.assertEqual(out["by_query"][0]["total"], 2)
        self.assertEqual(out["by_query"][1]["query"], "beta")
        self.assertEqual(out["total"], 4)
        self.assertNotIn("results", out)


if __name__ == "__main__":
    unittest.main()
