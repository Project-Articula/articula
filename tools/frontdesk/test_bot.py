"""Tests for the front-desk bot. Run: python3 -m unittest discover -s tools/frontdesk -p 'test_*.py'"""

import importlib.util
import json
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("frontdesk_bot", HERE / "bot.py")
bot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bot)

ITEMS = json.loads((HERE / "fixtures" / "sample_items.json").read_text(encoding="utf-8"))
BY_ID = {item["id"]: item for item in ITEMS}

EXPECTED_CATEGORY = {
    "issue:101": "question",
    "comment:102": "bug",
    "issue:103": "design_critique",
    "comment:104": "injection_attempt",
    "comment:105": "injection_attempt",
    "issue:106": "spam",
}


class HeuristicsTest(unittest.TestCase):
    def test_categories(self):
        for item_id, expected in EXPECTED_CATEGORY.items():
            brief = bot.build_brief(BY_ID[item_id], None)
            self.assertEqual(brief["classification"]["category"], expected, item_id)

    def test_injection_items_are_marked_untrusted_and_scored(self):
        for item_id in ("comment:104", "comment:105"):
            brief = bot.build_brief(BY_ID[item_id], None)
            self.assertTrue(brief["security"]["untrusted"])
            self.assertGreater(brief["security"]["injection_score"], 0.5)
            self.assertTrue(brief["security"]["injection_signals"])

    def test_spam_is_not_flagged_for_human(self):
        brief = bot.build_brief(BY_ID["issue:106"], None)
        self.assertFalse(brief["classification"]["needs_human"])
        self.assertEqual(brief["recommended_action"], "ignore_spam")


class ReplyPlanTest(unittest.TestCase):
    def brief(self, item_id):
        return bot.build_brief(BY_ID[item_id], None)

    def test_licence_question_gets_chinese_faq(self):
        plan = bot.plan_reply(self.brief("issue:101"))
        self.assertIsNotNone(plan)
        self.assertEqual(plan["topic"], "license")
        self.assertIn(bot.REPLY_MARKER, plan["body"])
        self.assertIn("AGPL", plan["body"])

    def test_injection_gets_silence(self):
        for item_id in ("comment:104", "comment:105"):
            self.assertIsNone(bot.plan_reply(self.brief(item_id)), item_id)

    def test_spam_gets_silence(self):
        self.assertIsNone(bot.plan_reply(self.brief("issue:106")))

    def test_non_question_comment_gets_silence(self):
        self.assertIsNone(bot.plan_reply(self.brief("comment:102")))

    def test_design_critique_issue_gets_acknowledgement(self):
        plan = bot.plan_reply(self.brief("issue:103"))
        self.assertIsNotNone(plan)
        self.assertEqual(plan["topic"], "ack")

    def test_bot_own_content_gets_silence(self):
        own = {"kind": "comment", "number": 1, "id": "comment:999", "author": bot.BOT_LOGIN,
               "created_at": "2026-01-01T00:00:00Z", "url": "https://example.invalid/1",
               "title": "x", "body": "hello"}
        self.assertIsNone(bot.plan_reply(bot.build_brief(own, None)))


class ModelParserTest(unittest.TestCase):
    def test_plain_summary(self):
        out = bot.parse_model_output("摘要：這是一個測試。")
        self.assertEqual(out["summary_zh"], "這是一個測試。")

    def test_empty_output_is_an_error(self):
        self.assertIsNotNone(bot.parse_model_output("   ")["error"])


if __name__ == "__main__":
    unittest.main()
