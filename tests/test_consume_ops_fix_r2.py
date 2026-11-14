"""Fix round 2 region 5 pinning tests: consume and ops surfaces.

Written test first for triage sections 9.4 (OPS N-1), 9.5
(Consume N-1), beside the deletion check at section 9.6
(Consume N-2), which owes no test of its own.
"""

import unittest

from tests import harness


class ConsumeHashMismatchComparisonTests(unittest.TestCase):
    """Consume N-1: the mismatch surface follows its comparison."""

    def test_agreeing_digests_return_the_loadable_form(self):
        mod = harness.require("ontoloop.consumption")
        before = len(mod.load_refusal_records())
        result = mod.load_with_hash_mismatch(
            material="same content", tool_material="same content"
        )
        self.assertEqual(result["position"], "loadable")
        self.assertTrue(result["loaded"])
        self.assertTrue(result["content_presented"])
        self.assertEqual(result["tool_side_hash"], result["presented_hash"])
        self.assertEqual(result["computed_hash"], result["presented_hash"])
        self.assertNotIn("load_refusal_record", result)
        self.assertEqual(len(mod.load_refusal_records()), before)

    def test_agreeing_digests_match_the_hash_check_loadable_form(self):
        mod = harness.require("ontoloop.consumption")
        checked = mod.load_with_hash_check(
            "same content",
            expected_hash=mod.load_with_hash_mismatch(
                material="same content", tool_material="same content"
            )["presented_hash"],
        )
        agreed = mod.load_with_hash_mismatch(
            material="same content", tool_material="same content"
        )
        self.assertEqual(agreed["loaded"], checked["loaded"])
        self.assertEqual(agreed["position"], checked["position"])
        self.assertEqual(
            agreed["content_presented"], checked["content_presented"]
        )

    def test_differing_digests_return_unloadable_and_write_the_refusal(self):
        mod = harness.require("ontoloop.consumption")
        before = len(mod.load_refusal_records())
        result = mod.load_with_hash_mismatch(
            material="presented content", tool_material="tool content"
        )
        self.assertEqual(result["position"], "unloadable")
        self.assertFalse(result["content_presented"])
        self.assertNotEqual(
            result["tool_side_hash"], result["presented_hash"]
        )
        self.assertEqual(len(mod.load_refusal_records()), before + 1)
        record = result["load_refusal_record"]
        self.assertEqual(record["checked_side_hash"], result["tool_side_hash"])
        self.assertEqual(
            record["against_side_hash"], result["presented_hash"]
        )
        self.assertEqual(mod.load_refusal_records()[-1], record)


class OpsPurgeWithoutPreviewShownFormTests(unittest.TestCase):
    """OPS N-1: the shown position takes the preview form or the flag."""

    def assert_failed(self, outcome):
        self.assertTrue(outcome["failed"])
        self.assertFalse(outcome["purge_proceeded"])

    def assert_proceeded(self, outcome):
        self.assertFalse(outcome["failed"])
        self.assertTrue(outcome["purge_proceeded"])

    def test_junk_preview_values_fail(self):
        module = harness.require("ontoloop.ops")
        junk_values = (
            False,
            0,
            [],
            {},
            "not a preview",
            {"unrelated": "mapping"},
            {"record_home": "operator surface record for the purge occasion"},
            {"identities_affected": ["identity a"]},
            42,
            ["purge preview"],
        )
        for junk in junk_values:
            outcome = module.purge_without_preview(preview=junk)
            self.assert_failed(outcome)

    def test_no_preview_and_no_flag_fails(self):
        module = harness.require("ontoloop.ops")
        self.assert_failed(module.purge_without_preview())
        self.assert_failed(module.purge_without_preview(preview=None))

    def test_a_real_preview_mapping_proceeds(self):
        module = harness.require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertIn("record_home", preview)
        self.assertIn("identities_affected", preview)
        self.assert_proceeded(module.purge_without_preview(preview=preview))

    def test_a_minimal_preview_form_mapping_proceeds(self):
        module = harness.require("ontoloop.ops")
        preview = {
            "record_home": "operator surface record for the purge occasion",
            "identities_affected": ["identity a"],
        }
        self.assert_proceeded(module.purge_without_preview(preview=preview))

    def test_the_shown_flag_alone_proceeds(self):
        module = harness.require("ontoloop.ops")
        self.assert_proceeded(
            module.purge_without_preview(preview_shown=True)
        )
        self.assert_proceeded(
            module.purge_without_preview(preview=False, preview_shown=True)
        )


if __name__ == "__main__":
    unittest.main()
