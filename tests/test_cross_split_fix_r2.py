"""Fix round 2 tests for the cross split module region.

Charges pinned here, from design/steps/step-15-r2-triage.md
ruling 1 (CL-R2-1, the module limb) and section 3 (CSA-R2-2):

1. The shared module ontoloop.cross_split_audit carries the
one instruction item firing act, audit_instruction_item. Given
an instruction text and the holdout material, the act computes
verbatim and near verbatim firing over the instruction text
field only, by the module relation form (word overlap dividing
by the smaller of the two word counts), and returns the firing
decision and, on firing, its refusal form.

2. The module single item form returns its refusal stating
presentation as its ground, carrying no firing pair and no
comparison count.
"""

import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text alpha beta gamma delta"
# Instruction words: sealed, holdout, instruction, text, alpha,
# extra (6 distinct). Holdout words: 8 distinct. Shared words: 5.
# Module form: 5 / min(6, 8) = 5/6, at or above 0.75, fires.
# Old local form: 5 / 8, below 0.75, does not fire.
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


class InstructionItemFiringActTests(unittest.TestCase):
    """CL-R2-1 module limb: the one instruction item firing act."""

    def module(self):
        return harness.require("ontoloop.cross_split_audit")

    def test_the_act_stands_exported_on_the_shared_module(self):
        module = self.module()
        self.assertIn("audit_instruction_item", module.__all__)
        self.assertTrue(callable(module.audit_instruction_item))

    def test_disagreement_case_is_decided_by_the_module_form(self):
        module = self.module()
        self.assertFalse(
            old_local_form_fires(DISAGREEMENT_TEXT, HOLDOUT_TEXT)
        )
        result = module.audit_instruction_item(
            DISAGREEMENT_TEXT, HOLDOUT_TEXT
        )
        self.assertTrue(result["fired"])
        self.assertEqual(result["fired_item"], DISAGREEMENT_TEXT)
        self.assertEqual(result["field_scope"], "instruction text field")
        self.assertFalse(result["wider_material_compared"])
        self.assertEqual(result["comparisons"], 1)
        self.assertEqual(
            result["firing_pairs"],
            [
                {
                    "candidate_position": 0,
                    "holdout_position": 0,
                    "relations": ["near verbatim cluster"],
                }
            ],
        )
        shared = result["cross_split_audit_result"]
        self.assertTrue(shared["candidate_bundle_refused"])
        self.assertEqual(shared["record_home"], "evaluation record")
        self.assertEqual(shared["comparisons"], 1)

    def test_disagreement_case_at_the_promotion_occasion(self):
        module = self.module()
        result = module.audit_instruction_item(
            DISAGREEMENT_TEXT, HOLDOUT_TEXT, occasion="promotion"
        )
        self.assertTrue(result["fired"])
        self.assertEqual(result["fired_item"], DISAGREEMENT_TEXT)
        shared = result["cross_split_audit_result"]
        self.assertTrue(shared["candidate_bundle_refused"])
        self.assertEqual(shared["record_home"], "Promotion Record")

    def test_verbatim_case_fires(self):
        module = self.module()
        result = module.audit_instruction_item(HOLDOUT_TEXT, HOLDOUT_TEXT)
        self.assertTrue(result["fired"])
        self.assertTrue(result["verbatim"])
        self.assertEqual(result["fired_item"], HOLDOUT_TEXT)
        self.assertEqual(
            result["test_result"],
            "holdout content found in instruction item",
        )
        self.assertEqual(
            result["refusal_form"], "cross split audit refusal"
        )
        record = result["audit_record"]
        self.assertEqual(
            record["home"], "cross split audit record for the candidate"
        )
        self.assertEqual(record["fired_item"], HOLDOUT_TEXT)
        self.assertTrue(record["test_result_recorded"])
        self.assertEqual(record["test_result"], result["test_result"])

    def test_clean_case_does_not_fire(self):
        module = self.module()
        result = module.audit_instruction_item(CLEAN_TEXT, HOLDOUT_TEXT)
        self.assertFalse(result["fired"])
        self.assertIsNone(result["fired_item"])
        self.assertIsNone(result["test_result"])
        self.assertEqual(result["firing_pairs"], [])
        shared = result["cross_split_audit_result"]
        self.assertFalse(shared["candidate_bundle_refused"])
        self.assertIsNone(shared["error"])

    def test_only_the_instruction_text_field_is_compared(self):
        module = self.module()
        item = {
            "instruction_text": CLEAN_TEXT,
            "content": HOLDOUT_TEXT,
            "group": "shared group",
            "signature": "shared signature",
        }
        holdout = [
            {
                "group": "shared group",
                "signature": "shared signature",
                "text": HOLDOUT_TEXT,
            }
        ]
        result = module.audit_instruction_item(item, holdout)
        self.assertFalse(result["fired"])
        self.assertEqual(result["firing_pairs"], [])

    def test_holdout_bundle_material_fires_on_a_later_item(self):
        module = self.module()
        holdout = {
            "holdout_items": [
                {"text": "entirely separate holdout wording"},
                {"text": HOLDOUT_TEXT},
            ]
        }
        result = module.audit_instruction_item(HOLDOUT_TEXT, holdout)
        self.assertTrue(result["fired"])
        self.assertEqual(result["comparisons"], 2)
        self.assertEqual(
            result["firing_pairs"][0]["holdout_position"], 1
        )

    def test_charging_form_after_partial_scoring(self):
        module = self.module()
        result = module.audit_instruction_item(
            HOLDOUT_TEXT, HOLDOUT_TEXT, after_partial_scoring=True
        )
        self.assertTrue(result["fired"])
        self.assertEqual(result["completed_evaluations_charged"], 1)
        self.assertEqual(
            result["charging_form"],
            "standing charging form for a refusal after partial scoring",
        )
        self.assertTrue(
            result["charged_under_the_standing_charging_rules"]
        )
        shared = result["cross_split_audit_result"]
        self.assertEqual(shared["completed_evaluations_charged"], 1)

    def test_no_charging_form_where_no_case_was_scored(self):
        module = self.module()
        result = module.audit_instruction_item(HOLDOUT_TEXT, HOLDOUT_TEXT)
        self.assertTrue(result["fired"])
        self.assertEqual(result["completed_evaluations_charged"], 0)
        self.assertIsNone(result["charging_form"])
        self.assertFalse(
            result["charged_under_the_standing_charging_rules"]
        )
        shared = result["cross_split_audit_result"]
        self.assertEqual(shared["completed_evaluations_charged"], 0)

    def test_an_unknown_occasion_raises_value_error(self):
        module = self.module()
        with self.assertRaises(ValueError) as caught:
            module.audit_instruction_item(
                HOLDOUT_TEXT, HOLDOUT_TEXT, occasion="somewhere else"
            )
        self.assertEqual(
            str(caught.exception),
            "unknown instruction test occasion: 'somewhere else'")


class SingleItemPresentationFormTests(unittest.TestCase):
    """CSA-R2-2: the single item refusal states presentation as ground."""

    PRESENTATION_REASON = "refused on its presentation as flagged material"

    def module(self):
        return harness.require("ontoloop.cross_split_audit")

    def assert_presentation_form(self, outcome):
        self.assertEqual(
            outcome["error"], "flagged material inside candidate bundle"
        )
        self.assertEqual(outcome["wording_variants"], [])
        self.assertTrue(outcome["candidate_bundle_refused"])
        self.assertFalse(outcome["promotion_proceeded"])
        self.assertEqual(outcome["evaluation_state"], "not scored")
        self.assertEqual(outcome["typed_reason"], self.PRESENTATION_REASON)
        self.assertEqual(outcome["firing_pairs"], [])
        self.assertEqual(outcome["comparisons"], 0)
        self.assertEqual(outcome["comparison_cost_units"], 0)
        self.assertNotIn(
            "near verbatim", outcome["typed_reason"]
        )

    def test_a_clean_single_string_returns_the_presentation_form(self):
        module = self.module()
        outcome = module.audit_at_build(
            "totally unrelated clean guidance"
        )
        self.assert_presentation_form(outcome)

    def test_a_flagged_single_string_still_refuses_in_presentation_form(self):
        module = self.module()
        outcome = module.audit_at_build("flagged material in bundle")
        self.assert_presentation_form(outcome)
        self.assertEqual(outcome["record_home"], "evaluation record")

    def test_the_presentation_form_at_evaluation_and_promotion(self):
        module = self.module()
        outcome = module.audit_at_evaluation("flagged material in bundle")
        self.assert_presentation_form(outcome)
        self.assertEqual(outcome["record_home"], "evaluation record")
        outcome = module.audit_at_promotion("flagged material in bundle")
        self.assert_presentation_form(outcome)
        self.assertEqual(outcome["record_home"], "Promotion Record")

    def test_a_single_mapping_with_no_text_returns_presentation_form(self):
        module = self.module()
        outcome = module.audit_at_build(
            {"group": None, "signature": None, "text": None}
        )
        self.assert_presentation_form(outcome)

    def test_a_single_mapping_with_text_returns_presentation_form(self):
        module = self.module()
        outcome = module.audit_at_build(
            {
                "group": "g1",
                "signature": "s1",
                "text": "some presented wording",
            }
        )
        self.assert_presentation_form(outcome)

    def test_single_item_charging_follows_the_scored_argument(self):
        module = self.module()
        outcome = module.audit_at_build(
            "flagged material in bundle", scored_before_refusal=True
        )
        self.assert_presentation_form(outcome)
        self.assertEqual(outcome["completed_evaluations_charged"], 1)
        outcome = module.audit_at_build(
            "flagged material in bundle", scored_before_refusal=False
        )
        self.assert_presentation_form(outcome)
        self.assertEqual(outcome["completed_evaluations_charged"], 0)


if __name__ == "__main__":
    unittest.main()
