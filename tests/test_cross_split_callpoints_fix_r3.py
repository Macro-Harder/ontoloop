"""Fix round 3 tests for the cross split call point region.

Charge pinned here, from design/steps/step-15-r3-triage.md
ruling 16, first limb (S15-R3-016, Low): both instruction item
call points, dataset.test_instruction_items_against_holdout at
candidate construction and promote.test_instruction_items_against_holdout
at promotion, present each item to the shared act
ontoloop.cross_split_audit.audit_instruction_item in a form the
act itself accepts. The shared act takes its instruction text
as a plain string or as a mapping carrying its text under the
instruction_text, text, or content key, through its own field
reading. Before this cure both call points read
item["instruction_text"] directly, so a plain string item
raised TypeError and a mapping carrying its text under a text
key or a content key raised KeyError, on forms the shared act
decides without error when called directly.

Each test below presents one item form at one occasion beside
the standing instruction_text mapping form, and compares the
call point outcome with a direct call of the shared act on the
same material, in the same comparison form the Fix round 2
call point tests use.
"""

import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def bundle_with(item, holdout_text=HOLDOUT_TEXT):
    return {
        "instruction_items": [item],
        "instruction_item_count": 1,
        "holdout_items": [{"text": holdout_text}],
    }


ITEM_FORMS = (
    ("plain string", HOLDOUT_TEXT),
    ("text key mapping", {"text": HOLDOUT_TEXT}),
    ("content key mapping", {"content": HOLDOUT_TEXT}),
    ("instruction_text mapping", {"instruction_text": HOLDOUT_TEXT}),
)


class CallPointItemFormTests(unittest.TestCase):
    """S15-R3-016: every form the shared act accepts decides at
    both call points exactly as a direct call decides."""

    def assert_matches_direct_call(self, result, direct):
        self.assertEqual(result["fired"], direct["fired"])
        self.assertEqual(result["fired_item"], direct["fired_item"])
        self.assertEqual(result["test_result"], direct["test_result"])
        self.assertEqual(result["audit_record"], direct["audit_record"])
        self.assertEqual(
            result["cross_split_audit_result"],
            direct["cross_split_audit_result"],
        )

    def check_occasion(self, module_name, occasion):
        module = harness.require(module_name)
        shared = harness.require("ontoloop.cross_split_audit")
        call_point = module.test_instruction_items_against_holdout
        for form_name, item in ITEM_FORMS:
            with self.subTest(occasion=occasion, form=form_name):
                bundle = bundle_with(item)
                result = call_point(bundle, occasion=occasion)
                direct = shared.audit_instruction_item(
                    item,
                    bundle["holdout_items"],
                    occasion=occasion,
                )
                self.assertTrue(direct["fired"])
                self.assertTrue(result["fired"])
                self.assertEqual(result["fired_item"], HOLDOUT_TEXT)
                self.assertEqual(result["items_tested"], 1)
                self.assert_matches_direct_call(result, direct)

    def test_item_forms_at_candidate_construction(self):
        self.check_occasion(
            "ontoloop.dataset", "candidate construction"
        )

    def test_item_forms_at_promotion(self):
        self.check_occasion("ontoloop.promote", "promotion")

    def test_clean_string_item_at_candidate_construction(self):
        dataset = harness.require("ontoloop.dataset")
        shared = harness.require("ontoloop.cross_split_audit")
        bundle = bundle_with(CLEAN_TEXT)
        result = dataset.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        direct = shared.audit_instruction_item(
            CLEAN_TEXT,
            bundle["holdout_items"],
            occasion="candidate construction",
        )
        self.assertFalse(direct["fired"])
        self.assertFalse(result["fired"])
        self.assertEqual(result["items_tested"], 1)

    def test_clean_text_key_item_at_promotion(self):
        promote = harness.require("ontoloop.promote")
        shared = harness.require("ontoloop.cross_split_audit")
        item = {"text": CLEAN_TEXT}
        bundle = bundle_with(item)
        result = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )
        direct = shared.audit_instruction_item(
            item, bundle["holdout_items"], occasion="promotion"
        )
        self.assertFalse(direct["fired"])
        self.assertFalse(result["fired"])
        self.assertEqual(result["items_tested"], 1)
        self.assertTrue(result["test_result_carried_on_promotion_record"])


if __name__ == "__main__":
    unittest.main()
