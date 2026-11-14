"""Slice EVAL, list section 2.12, plan section 6.5 plus rows
supplied at subsection 16.37 and the Amendment 1 owing rows at
section 13.3.

Failure and boundary perspective: these tests prize the boundary
outcomes the rows state: zero paired groups and one paired group,
the perfect baseline case, cost refusal over the D-7 cap, voided
comparisons on pointer movement, zero tolerance spend disagreement
named as a defect, and the closed verdict vocabulary of four terms.

EVAL-T04 stands in its subsection 20.78 adopted form: the noise
component takes a Student t multiplier by group count in place of
a fixed multiplier, with check values held in the EVAL module and
at plan subsection 20.78.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.eval, with function names taken from the behaviour wording
of each row. Fields a row does not state are not invented.
EVAL-T11 is a pointer row: its class states no second wording of
the behaviour and exercises the pass condition stated in the
central row DATASET-T05 at its evaluation call point only.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.eval"

THREE_RELATIONS = ("group", "signature", "near verbatim cluster")


class TestEvalT01(unittest.TestCase):
    """EVAL-T01: aggregation is the equal weighted group mean."""

    def test_aggregation_is_the_mean_of_per_group_scores(self):
        module = require(MODULE)
        result = module.aggregate_example("B")
        scores = result["per_group_scores"]
        self.assertAlmostEqual(
            result["aggregate"], sum(scores) / len(scores)
        )

    def test_groups_are_weighted_equally(self):
        module = require(MODULE)
        result = module.aggregate_example("B")
        weights = result["group_weights"]
        self.assertEqual(len(set(weights)), 1)

    def test_paired_differences_are_taken_group_by_group(self):
        module = require(MODULE)
        result = module.aggregate_example("D")
        self.assertEqual(
            len(result["paired_differences"]),
            len(result["per_group_scores"]),
        )

    def test_rounding_is_applied_once_at_the_group_score(self):
        module = require(MODULE)
        result = module.aggregate_example("D")
        self.assertEqual(result["rounding_points"], ["group score"])


class TestEvalT02(unittest.TestCase):
    """EVAL-T02: zero paired groups, and the one paired group case."""

    def test_zero_paired_groups_returns_not_scored(self):
        module = require(MODULE)
        result = module.evaluate_example_d("zero paired groups")
        self.assertEqual(result["verdict"], "not scored")

    def test_typed_reason_is_no_complete_pair(self):
        module = require(MODULE)
        result = module.evaluate_example_d("zero paired groups")
        self.assertEqual(result["typed_reason"], "no complete pair")

    def test_zero_case_charged_as_no_completed_evaluation(self):
        module = require(MODULE)
        result = module.evaluate_example_d("zero paired groups")
        self.assertEqual(result["completed_evaluations_charged"], 0)

    def test_one_paired_group_carries_the_comparison_with_limits(self):
        module = require(MODULE)
        result = module.evaluate_example_d("one paired group")
        self.assertTrue(result["comparison_carried"])
        self.assertTrue(result["limits_stated"])

    def test_one_group_prints_no_noise_figure_as_a_number(self):
        module = require(MODULE)
        result = module.evaluate_example_d("one paired group")
        self.assertNotIsInstance(result["noise_figure"], (int, float))


class TestEvalT03(unittest.TestCase):
    """EVAL-T03: the perfect baseline case."""

    def test_no_candidate_gain_can_clear_the_practical_component(self):
        module = require(MODULE)
        result = module.evaluate_example_d("perfect baseline")
        self.assertTrue(
            result["records_no_gain_can_clear_practical_margin"]
        )

    def test_perfect_baseline_charges_one_completed_evaluation(self):
        module = require(MODULE)
        result = module.evaluate_example_d("perfect baseline")
        self.assertEqual(result["completed_evaluations_charged"], 1)

    def test_no_short_circuit_before_scoring(self):
        module = require(MODULE)
        result = module.evaluate_example_d("perfect baseline")
        self.assertTrue(result["scoring_ran"])
        self.assertFalse(result["short_circuited"])


class TestEvalT04(unittest.TestCase):
    """EVAL-T04: margin components and the sufficiency conjunction."""

    def test_the_three_components_compute_in_their_one_home(self):
        module = require(MODULE)
        result = module.margin_components()
        self.assertEqual(
            set(result["components"]),
            {"practical", "noise", "absolute floor"},
        )
        self.assertEqual(len(set(result["computed_in"])), 1)

    def test_practical_component_is_the_smaller_of_the_two_values(self):
        module = require(MODULE)
        result = module.margin_components()
        practical = result["components"]["practical"]
        self.assertAlmostEqual(
            practical,
            min(
                result["d1_value"],
                result["d2_share"] * result["remaining_error"],
            ),
        )

    def _implied_multiplier(self, module, groups):
        result = module.margin_components(groups=groups)
        standard_error = result[
            "standard_error_of_paired_differences"
        ]
        return result["components"]["noise"] / standard_error, result

    def test_noise_uses_the_student_t_multiplier_by_group_count(self):
        module = require(MODULE)
        implied = {}
        for groups in (8, 10, 30):
            value, result = self._implied_multiplier(module, groups)
            implied[groups] = value
            self.assertGreater(value, 0)
            self.assertGreater(value, 2)
            self.assertLess(value, 3)
            self.assertNotAlmostEqual(value, 2.0, places=3)
        self.assertEqual(len(set(implied.values())), 3)
        self.assertGreater(implied[8], implied[10])
        self.assertGreater(implied[10], implied[30])

    def test_noise_is_multiplier_times_standard_error_of_differences(self):
        module = require(MODULE)
        for groups in (8, 10, 30):
            value, result = self._implied_multiplier(module, groups)
            self.assertAlmostEqual(
                result["components"]["noise"],
                value
                * result["standard_error_of_paired_differences"],
            )

    def test_the_fixed_multiplier_2_is_not_used(self):
        module = require(MODULE)
        for groups in (8, 10, 30):
            value, result = self._implied_multiplier(module, groups)
            self.assertNotAlmostEqual(value, 2.0, places=3)

    def test_default_margin_result_matches_the_8_group_case(self):
        module = require(MODULE)
        default = module.margin_components()
        eight = module.margin_components(groups=8)
        self.assertAlmostEqual(
            default["components"]["noise"],
            eight["components"]["noise"],
        )

    def test_sufficiency_conjunction_requires_every_component(self):
        module = require(MODULE)
        result = module.margin_components()
        conjunction = result["sufficiency_conjunction"]
        self.assertEqual(
            conjunction["form"], "all components must be cleared"
        )
        self.assertEqual(
            set(conjunction["components"]),
            {"practical", "noise", "absolute floor"},
        )


class TestEvalT05(unittest.TestCase):
    """EVAL-T05: cost estimation refusal and abort records."""

    def test_a_start_over_the_d7_cap_is_refused(self):
        module = require(MODULE)
        outcome = module.estimate_and_start("over cap")
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["started"])

    def test_the_cap_is_checked_before_each_costly_step(self):
        module = require(MODULE)
        outcome = module.estimate_and_start("within cap")
        for step in outcome["costly_steps"]:
            self.assertTrue(step["cap_checked_before"])

    def test_abort_records_land(self):
        module = require(MODULE)
        outcome = module.estimate_and_start("abort during run")
        self.assertTrue(outcome["abort_records_landed"])

    def test_example_e_weights_are_labelled_guessed(self):
        module = require(MODULE)
        for weight in module.example_e_weights():
            self.assertEqual(weight["source_class"], "guessed")


class TestEvalT06(unittest.TestCase):
    """EVAL-T06: pointer movement voids the comparison."""

    def test_pointer_movement_voids_the_comparison(self):
        module = require(MODULE)
        outcome = module.move_pointer_between_evaluation_and_promotion()
        self.assertTrue(outcome["comparison_voided"])

    def test_partial_scores_stand_recorded_as_not_promotable(self):
        module = require(MODULE)
        outcome = module.move_pointer_between_evaluation_and_promotion()
        self.assertEqual(
            outcome["partial_scores_state"], "not promotable"
        )


class TestEvalT07(unittest.TestCase):
    """EVAL-T07: spend reconciliation with zero tolerance."""

    def test_spend_reconciles_to_the_journal_counted_figure(self):
        module = require(MODULE)
        result = module.reconcile_spend()
        self.assertEqual(result["difference"], 0)

    def test_a_disagreement_is_a_named_defect_not_absorbed(self):
        module = require(MODULE)
        result = module.reconcile_spend(varied_by="disagreement")
        self.assertTrue(result["named_defect"])
        self.assertFalse(result["absorbed"])
        self.assertNotEqual(result["difference"], 0)


class TestEvalT08(unittest.TestCase):
    """EVAL-T08: the closed verdict vocabulary of four terms."""

    def test_the_vocabulary_has_exactly_four_terms(self):
        module = require(MODULE)
        vocabulary = module.verdict_vocabulary()
        self.assertEqual(len(vocabulary), 4)
        for verdict in module.all_recorded_verdicts():
            self.assertIn(verdict, vocabulary)

    def test_gate_refusal_stands_beside_not_inside_the_vocabulary(self):
        module = require(MODULE)
        vocabulary = module.verdict_vocabulary()
        self.assertNotIn("gate refusal", vocabulary)
        self.assertIn(
            "gate refusal", module.forms_beside_the_vocabulary()
        )

    def test_not_scored_reasons_distinguished_from_cannot_judge(self):
        module = require(MODULE)
        reasons = module.not_scored_reasons()
        self.assertTrue(reasons)
        self.assertNotIn("cannot judge only", reasons)
        result = module.evaluate_example_d("zero paired groups")
        self.assertNotEqual(result["verdict"], "cannot judge")


class TestEvalT09(unittest.TestCase):
    """EVAL-T09, Amendment 1: forms owed in the evaluation record."""

    def test_simple_figure_without_advanced_counterpart_fails(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        varied = dict(record)
        varied["advanced"] = {}
        defects = module.check_evaluation_record(varied)
        self.assertTrue(defects)
        self.assertTrue(all(d["artifact"] == "evaluation record"
                            for d in defects))

    def test_derivation_stated_in_summary_only_fails_the_row(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        varied = dict(record)
        advanced = dict(record["advanced"])
        figures = dict(advanced["figures"])
        first = sorted(figures)[0]
        entry = dict(figures[first])
        entry["derivation"] = "summary only"
        figures[first] = entry
        advanced["figures"] = figures
        varied["advanced"] = advanced
        self.assertTrue(module.check_evaluation_record(varied))

    def test_label_missing_from_the_record_fails_the_row(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        varied = dict(record)
        simple = dict(record["simple"])
        simple["grader_awareness_label"] = None
        varied["simple"] = simple
        self.assertTrue(module.check_evaluation_record(varied))

    def test_owed_forms_stand_in_the_record_as_built(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        self.assertEqual(module.check_evaluation_record(record), [])
        self.assertTrue(record["simple"]["grader_awareness_label"])
        self.assertTrue(record["simple"]["verdict_wording"])
        for section in ("figures", "paired_per_group_scores",
                        "margin_components"):
            self.assertIn(section, record["advanced"])

    def test_the_label_owing_is_discharged_jointly_with_protocol(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        self.assertEqual(
            record["label_discharge"],
            "joint with the protocol record",
        )

    def test_no_load_claim_is_printed_in_agentic_form(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        self.assertNotIn("agentic", record)

    def test_owed_form_with_a_different_value_fails_the_row(self):
        module = require(MODULE)
        record = module.evaluation_record_example_d()
        varied = dict(record)
        advanced = dict(record["advanced"])
        figures = dict(advanced["figures"])
        first = sorted(figures)[0]
        entry = dict(figures[first])
        entry["value"] = "a different value"
        figures[first] = entry
        advanced["figures"] = figures
        varied["advanced"] = advanced
        self.assertTrue(module.check_evaluation_record(varied))


class TestEvalT10(unittest.TestCase):
    """EVAL-T10, Amendment 1: protocol record checked before scoring."""

    def test_label_missing_in_agentic_form_blocks_scoring(self):
        module = require(MODULE)
        record = module.protocol_record_example_d(missing="agentic label")
        outcome = module.score_against_protocol_record(record)
        self.assertFalse(outcome["scoring_proceeded"])
        self.assertEqual(outcome["defect_artifact"], "protocol record")

    def test_label_missing_in_simple_form_blocks_scoring(self):
        module = require(MODULE)
        record = module.protocol_record_example_d(missing="simple label")
        outcome = module.score_against_protocol_record(record)
        self.assertFalse(outcome["scoring_proceeded"])
        self.assertEqual(outcome["defect_artifact"], "protocol record")

    def test_figure_without_advanced_counterpart_blocks_scoring(self):
        module = require(MODULE)
        record = module.protocol_record_example_d(
            missing="advanced counterpart"
        )
        outcome = module.score_against_protocol_record(record)
        self.assertFalse(outcome["scoring_proceeded"])
        self.assertEqual(outcome["defect_artifact"], "protocol record")

    def test_a_complete_protocol_record_allows_scoring(self):
        module = require(MODULE)
        record = module.protocol_record_example_d()
        outcome = module.score_against_protocol_record(record)
        self.assertTrue(outcome["scoring_proceeded"])
        self.assertEqual(
            record["agentic"]["grader_awareness_label"],
            module.grader_awareness_label_agentic(),
        )


class TestEvalT11(unittest.TestCase):
    """EVAL-T11: pointer row, subsection 16.37.

    This row states no second wording of the behaviour. The tests
    below exercise the pass condition stated in the central row
    DATASET-T05 at its evaluation call point only: refusal at
    evaluation, and no verdict recorded for a refused evaluation.
    """

    def test_spanning_pair_over_each_relation_is_refused(self):
        module = require(MODULE)
        for relation in THREE_RELATIONS:
            outcome = module.evaluate_with_spanning_pair(relation)
            self.assertTrue(outcome["refused_at_evaluation"])

    def test_no_verdict_is_recorded_for_a_refused_evaluation(self):
        module = require(MODULE)
        for relation in THREE_RELATIONS:
            outcome = module.evaluate_with_spanning_pair(relation)
            self.assertTrue(outcome["refused_at_evaluation"])
            self.assertIsNone(outcome["verdict_recorded"])

    def test_the_audit_at_this_call_point_uses_three_relations_only(self):
        module = require(MODULE)
        outcome = module.evaluate_with_spanning_pair("paraphrase only")
        self.assertFalse(outcome["refused_at_evaluation"])
        self.assertEqual(set(outcome["relations"]), set(THREE_RELATIONS))


class TestEvalKeyCustody(unittest.TestCase):
    """Subsection 20.2 clause two: the calibration key custody limb.

    The key is held by the operator. It stands printed on no
    export, no file presentation, and no record the graded party
    reads. These tests pin that position over the calibration
    surfaces and the records this module returns: sample
    identities stand under the key, while no key value, and no
    field carrying a key, stands on any of those returns.
    """

    KEY_FIELD_NAMES = (
        "key",
        "operator_key",
        "calibration_key",
        "selection_key",
        "secret",
    )

    def _assert_no_key_carried(self, value):
        if isinstance(value, dict):
            for name, entry in value.items():
                self.assertNotIn(name, self.KEY_FIELD_NAMES)
                self._assert_no_key_carried(entry)
        elif isinstance(value, (list, tuple)):
            for entry in value:
                self._assert_no_key_carried(entry)

    def test_calibration_sample_carries_no_key(self):
        module = require(MODULE)
        sample = module.calibration_sample()
        self.assertEqual(sample["selection"], "keyed")
        self.assertTrue(sample["sample_identities_under_key"])
        self._assert_no_key_carried(sample)

    def test_calibration_record_carries_no_key(self):
        module = require(MODULE)
        record = module.calibration_record()
        self.assertTrue(record["sample_identities_under_key"])
        self._assert_no_key_carried(record)

    def test_no_key_on_records_the_graded_party_reads(self):
        module = require(MODULE)
        for record in (
            module.calibration_record(),
            module.loop_report_for_cycle(),
            module.evaluation_record_example_d(),
            module.protocol_record_example_d(),
            module.closing_evaluation_record(),
        ):
            self._assert_no_key_carried(record)

    def test_no_key_surface_stands_on_the_module(self):
        module = require(MODULE)
        for name in self.KEY_FIELD_NAMES:
            self.assertNotIn(name, module.__all__)


class TestEvalFixR6(unittest.TestCase):
    """Fix round 6, Region 3: eval scalar lookups, rulings 99 and 100.

    Written test first for S15-R6-EVAL-1 and S15-R6-EVAL-2.
    Each pin states the stated ValueError form of its surface,
    beside the standing forms the cure preserves. No pin states
    any table value.
    """

    # Ruling 99: margin_components meets an unhashable group
    # count in its stated ValueError form.
    def test_margin_components_unhashable_count_raises_value_error(self):
        module = require(MODULE)
        for count in ([8], {"count": 8}, {8}):
            with self.assertRaises(ValueError, msg=repr(count)):
                module.margin_components(groups=count)

    def test_margin_components_standing_counts_still_return(self):
        module = require(MODULE)
        for count in (8, 10, 30):
            result = module.margin_components(groups=count)
            self.assertEqual(
                set(result["components"]),
                {"practical", "noise", "absolute floor"},
            )
        default = module.margin_components()
        self.assertIn("components", default)
        for count in (7, "8", (8,)):
            with self.assertRaises(ValueError, msg=repr(count)):
                module.margin_components(groups=count)

    # Ruling 100: aggregate_example meets an unhashable example
    # letter in its stated ValueError form.
    def test_aggregate_example_unhashable_letter_raises_value_error(self):
        module = require(MODULE)
        for letter in (["B"], {"letter": "B"}):
            with self.assertRaises(ValueError, msg=repr(letter)):
                module.aggregate_example(letter)

    def test_aggregate_example_standing_letters_still_return(self):
        module = require(MODULE)
        for letter in ("B", "D"):
            result = module.aggregate_example(letter)
            scores = result["per_group_scores"]
            self.assertAlmostEqual(
                result["aggregate"], sum(scores) / len(scores))
        with self.assertRaises(ValueError):
            module.aggregate_example("X")


if __name__ == "__main__":
    unittest.main()
