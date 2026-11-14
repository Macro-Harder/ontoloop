"""Fix round 4 tests for the cross split call point region.

Charge pinned here, from design/steps/step-15-r4-triage.md
ruling 21 (N-03, R4-CORE-1, Medium, with the Lead Engineer
B-4 collection forms counted there): at both instruction
item call points, dataset.test_instruction_items_against_holdout
at candidate construction and
promote.test_instruction_items_against_holdout at promotion,
the instruction_items collection stands checked as a list
of items before any iteration. A collection given as a
plain string, as a single mapping, or as None returns the
governed refusal form in one stated form, instead of the
silent clearance the Round 4 CORE paper probed: a string
equal to the holdout text returned fired False with
items_tested standing at 31 by character split, a single
mapping returned fired False over its key string, and None
raised an ungoverned TypeError.

The governed refusal form chosen, stated in the region
paper at design/steps/step-15-r4-fix-cross-split-callpoints.md,
stands in the surfaces own standing refusal vocabulary:
the firing return form of these same surfaces, holding
fired standing True, refusal_form standing at the string
cross split audit refusal, field_scope standing at
instruction text field, wider_material_compared standing
False, and the occasion proceeds flag standing False
(bundle_proceeds at candidate construction,
promotion_proceeds at promotion). No items_tested count
and no instruction_item_count stands in the refusal,
because no item was ever presented to the shared act,
and no fired item, test result, audit record, or cross
split audit result stands in it, because those values
stand carried solely from a shared act outcome and no
act ran. Every other non list form, a tuple among them,
refuses in the same form, per ruling 21.

A genuine list keeps the standing behaviour exactly: a
list holding the holdout text as its one item fires as
the standing pins hold, a clean list returns fired False
with its items_tested count, and the empty list returns
fired False with items_tested standing at 0.
"""

import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def bundle_with_collection(collection):
    return {
        "instruction_items": collection,
        "holdout_items": [{"text": HOLDOUT_TEXT}],
    }


def expected_refusal(occasion):
    result = {
        "fired": True,
        "refusal_form": "cross split audit refusal",
        "field_scope": "instruction text field",
        "wider_material_compared": False,
    }
    if occasion == "promotion":
        result["promotion_proceeds"] = False
    else:
        result["bundle_proceeds"] = False
    return result


CALL_POINTS = (
    ("ontoloop.dataset", "candidate construction"),
    ("ontoloop.promote", "promotion"),
)

ALL_OCCASIONS = ("candidate construction", "promotion")


class CollectionFormRefusalTests(unittest.TestCase):
    """Ruling 21: a non list collection refuses in the
    governed form at both call points, in one stated form."""

    def check_refusal(self, module_name, occasion, collection):
        module = harness.require(module_name)
        bundle = bundle_with_collection(collection)
        result = module.test_instruction_items_against_holdout(
            bundle, occasion=occasion
        )
        self.assertEqual(result, expected_refusal(occasion))
        self.assertNotIn("items_tested", result)
        self.assertNotIn("instruction_item_count", result)

    def test_string_collection_refuses_at_both_call_points(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                self.check_refusal(module_name, occasion, HOLDOUT_TEXT)

    def test_mapping_collection_refuses_at_both_call_points(self):
        collection = {"instruction_text": HOLDOUT_TEXT}
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                self.check_refusal(module_name, occasion, collection)

    def test_none_collection_refuses_at_both_call_points(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                self.check_refusal(module_name, occasion, None)

    def test_refusal_form_is_one_form_at_every_occasion(self):
        for module_name in ("ontoloop.dataset", "ontoloop.promote"):
            for occasion in ALL_OCCASIONS:
                with self.subTest(module=module_name, occasion=occasion):
                    self.check_refusal(module_name, occasion, HOLDOUT_TEXT)
                    self.check_refusal(module_name, occasion, None)

    def test_tuple_collection_refuses_at_both_call_points(self):
        collection = ({"instruction_text": HOLDOUT_TEXT},)
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                self.check_refusal(module_name, occasion, collection)


class GenuineListBehaviourTests(unittest.TestCase):
    """Ruling 21: a genuine list keeps the standing
    behaviour exactly, beside the collection refusal."""

    def test_list_holding_holdout_text_fires_at_both_call_points(self):
        collection = [{"instruction_text": HOLDOUT_TEXT}]
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                module = harness.require(module_name)
                bundle = bundle_with_collection(collection)
                result = module.test_instruction_items_against_holdout(
                    bundle, occasion=occasion
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 1)
                self.assertEqual(result["fired_item"], HOLDOUT_TEXT)
                self.assertEqual(
                    result["refusal_form"], "cross split audit refusal"
                )

    def test_clean_list_clears_at_both_call_points(self):
        collection = [{"instruction_text": CLEAN_TEXT}]
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                module = harness.require(module_name)
                bundle = bundle_with_collection(collection)
                result = module.test_instruction_items_against_holdout(
                    bundle, occasion=occasion
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)

    def test_empty_list_clears_with_zero_tested_at_both_call_points(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                module = harness.require(module_name)
                bundle = bundle_with_collection([])
                result = module.test_instruction_items_against_holdout(
                    bundle, occasion=occasion
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 0)
                self.assertEqual(result["instruction_item_count"], 0)


if __name__ == "__main__":
    unittest.main()
