"""Fix round 2 tests for the cross split call point region.

Charge pinned here, from design/steps/step-15-r2-triage.md
ruling 1 (CL-R2-1, the call point limb): both instruction item
call points, dataset.test_instruction_items_against_holdout at
candidate construction and promote.test_instruction_items_against_holdout
at promotion, delegate in full to the shared module act
ontoloop.cross_split_audit.audit_instruction_item. Each call
point presents every instruction item text, with the holdout
material the bundle carries, to that act, and takes fired, the
fired item, the test result, the audit record, and the charging
form after partial scoring solely from the module outcome. No
call point computes a firing condition of its own.

The disagreement probes use pairs where the two old formulas
disagree: the deleted local form divided the shared word count
by the holdout word count, and the module form divides by the
smaller of the two word counts. On an instruction text shorter
than the holdout text the local form misses a case the module
form fires on.
"""

import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
# Instruction words: sealed, holdout (2 distinct). Holdout
# words: 4 distinct. Shared words: 2. Module form: 2 / min(2, 4)
# = 1.0, at or above the near verbatim threshold, fires. Old
# local form: 2 / 4, below the threshold, does not fire.
SHORT_TEXT = "sealed holdout"
LONG_HOLDOUT_TEXT = (
    "sealed holdout instruction text alpha beta gamma delta"
)
# Instruction words: sealed, holdout, instruction, text, alpha,
# extra (6 distinct). Holdout words: 8 distinct. Shared words:
# 5. Module form: 5 / min(6, 8) = 5/6, fires. Old local form:
# 5 / 8, does not fire.
DISAGREEMENT_TEXT = "sealed holdout instruction text alpha extra"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def old_local_form_fires(instruction_text, holdout_text):
    """Recompute the deleted local formula, for the disagreement pin."""
    if instruction_text == holdout_text:
        return True
    holdout_words = set(holdout_text.split())
    item_words = set(instruction_text.split())
    if not holdout_words:
        return False
    return len(holdout_words & item_words) / len(holdout_words) >= 0.75


def bundle_with(instruction_text, holdout_text):
    return {
        "instruction_items": [
            {"instruction_text": instruction_text}
        ],
        "instruction_item_count": 1,
        "holdout_items": [{"text": holdout_text}],
    }


class CallPointDelegationTests(unittest.TestCase):
    """CL-R2-1 call point limb: full delegation at both occasions."""

    def assert_matches_direct_call(self, result, direct):
        self.assertEqual(result["fired"], direct["fired"])
        self.assertEqual(result["fired_item"], direct["fired_item"])
        self.assertEqual(result["test_result"], direct["test_result"])
        self.assertEqual(result["audit_record"], direct["audit_record"])
        self.assertEqual(
            result["cross_split_audit_result"],
            direct["cross_split_audit_result"],
        )

    def test_short_instruction_disagreement_at_candidate_construction(self):
        dataset = harness.require("ontoloop.dataset")
        module = harness.require("ontoloop.cross_split_audit")
        self.assertFalse(old_local_form_fires(SHORT_TEXT, HOLDOUT_TEXT))
        bundle = bundle_with(SHORT_TEXT, HOLDOUT_TEXT)
        result = dataset.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        direct = module.audit_instruction_item(
            SHORT_TEXT, HOLDOUT_TEXT, occasion="candidate construction"
        )
        self.assertTrue(direct["fired"])
        self.assertTrue(result["fired"])
        self.assertEqual(result["fired_item"], SHORT_TEXT)
        self.assertEqual(
            result["refusal_form"], "cross split audit refusal"
        )
        self.assertFalse(result["bundle_proceeds"])
        self.assert_matches_direct_call(result, direct)

    def test_short_instruction_disagreement_at_promotion(self):
        promote = harness.require("ontoloop.promote")
        module = harness.require("ontoloop.cross_split_audit")
        self.assertFalse(old_local_form_fires(SHORT_TEXT, HOLDOUT_TEXT))
        bundle = bundle_with(SHORT_TEXT, HOLDOUT_TEXT)
        result = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )
        direct = module.audit_instruction_item(
            SHORT_TEXT, HOLDOUT_TEXT, occasion="promotion"
        )
        self.assertTrue(direct["fired"])
        self.assertTrue(result["fired"])
        self.assertEqual(result["fired_item"], SHORT_TEXT)
        self.assertEqual(
            result["refusal_form"], "cross split audit refusal"
        )
        self.assertFalse(result["promotion_proceeds"])
        self.assert_matches_direct_call(result, direct)

    def test_long_holdout_disagreement_at_candidate_construction(self):
        dataset = harness.require("ontoloop.dataset")
        module = harness.require("ontoloop.cross_split_audit")
        self.assertFalse(
            old_local_form_fires(DISAGREEMENT_TEXT, LONG_HOLDOUT_TEXT)
        )
        bundle = bundle_with(DISAGREEMENT_TEXT, LONG_HOLDOUT_TEXT)
        result = dataset.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        direct = module.audit_instruction_item(
            DISAGREEMENT_TEXT,
            LONG_HOLDOUT_TEXT,
            occasion="candidate construction",
        )
        self.assertTrue(direct["fired"])
        self.assertTrue(result["fired"])
        self.assert_matches_direct_call(result, direct)

    def test_long_holdout_disagreement_at_promotion(self):
        promote = harness.require("ontoloop.promote")
        module = harness.require("ontoloop.cross_split_audit")
        self.assertFalse(
            old_local_form_fires(DISAGREEMENT_TEXT, LONG_HOLDOUT_TEXT)
        )
        bundle = bundle_with(DISAGREEMENT_TEXT, LONG_HOLDOUT_TEXT)
        result = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )
        direct = module.audit_instruction_item(
            DISAGREEMENT_TEXT, LONG_HOLDOUT_TEXT, occasion="promotion"
        )
        self.assertTrue(direct["fired"])
        self.assertTrue(result["fired"])
        self.assert_matches_direct_call(result, direct)

    def test_clean_case_at_candidate_construction(self):
        dataset = harness.require("ontoloop.dataset")
        module = harness.require("ontoloop.cross_split_audit")
        bundle = bundle_with(CLEAN_TEXT, HOLDOUT_TEXT)
        result = dataset.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        direct = module.audit_instruction_item(
            CLEAN_TEXT, HOLDOUT_TEXT, occasion="candidate construction"
        )
        self.assertFalse(direct["fired"])
        self.assertFalse(result["fired"])
        self.assertEqual(result["items_tested"], 1)
        self.assertEqual(
            result["field_scope"], "instruction text field"
        )
        self.assertFalse(result["wider_material_compared"])

    def test_clean_case_at_promotion(self):
        promote = harness.require("ontoloop.promote")
        module = harness.require("ontoloop.cross_split_audit")
        bundle = bundle_with(CLEAN_TEXT, HOLDOUT_TEXT)
        result = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )
        direct = module.audit_instruction_item(
            CLEAN_TEXT, HOLDOUT_TEXT, occasion="promotion"
        )
        self.assertFalse(direct["fired"])
        self.assertFalse(result["fired"])
        self.assertEqual(result["items_tested"], 1)
        self.assertTrue(result["test_result_carried_on_promotion_record"])

    def test_charging_form_after_partial_scoring_at_candidate_construction(self):
        dataset = harness.require("ontoloop.dataset")
        module = harness.require("ontoloop.cross_split_audit")
        bundle = bundle_with(HOLDOUT_TEXT, HOLDOUT_TEXT)
        result = dataset.test_instruction_items_against_holdout(
            bundle,
            occasion="candidate construction",
            after_partial_scoring=True,
        )
        direct = module.audit_instruction_item(
            HOLDOUT_TEXT,
            HOLDOUT_TEXT,
            occasion="candidate construction",
            after_partial_scoring=True,
        )
        self.assertTrue(result["fired"])
        self.assert_matches_direct_call(result, direct)
        self.assertEqual(result["charging_form"], direct["charging_form"])
        self.assertEqual(
            result["charging_form"],
            "standing charging form for a refusal after partial scoring",
        )
        self.assertTrue(result["charged_under_the_standing_charging_rules"])
        self.assertEqual(
            result["cross_split_audit_result"][
                "completed_evaluations_charged"
            ],
            1,
        )

    def test_charging_form_after_partial_scoring_at_promotion(self):
        promote = harness.require("ontoloop.promote")
        module = harness.require("ontoloop.cross_split_audit")
        bundle = bundle_with(HOLDOUT_TEXT, HOLDOUT_TEXT)
        result = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion", after_partial_scoring=True
        )
        direct = module.audit_instruction_item(
            HOLDOUT_TEXT,
            HOLDOUT_TEXT,
            occasion="promotion",
            after_partial_scoring=True,
        )
        self.assertTrue(result["fired"])
        self.assert_matches_direct_call(result, direct)
        self.assertEqual(result["charging_form"], direct["charging_form"])
        self.assertEqual(
            result["charging_form"],
            "standing charging form for a refusal after partial scoring",
        )
        self.assertTrue(result["charged_under_the_standing_charging_rules"])
        self.assertEqual(
            result["cross_split_audit_result"][
                "completed_evaluations_charged"
            ],
            1,
        )

    def test_every_instruction_item_is_presented(self):
        dataset = harness.require("ontoloop.dataset")
        bundle = {
            "instruction_items": [
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": SHORT_TEXT},
            ],
            "instruction_item_count": 2,
            "holdout_items": [{"text": HOLDOUT_TEXT}],
        }
        result = dataset.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(result["fired"])
        self.assertEqual(result["fired_item"], SHORT_TEXT)
        self.assertEqual(result["items_tested"], 2)


if __name__ == "__main__":
    unittest.main()
