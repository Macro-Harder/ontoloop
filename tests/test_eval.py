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
the fixed multiplier 2, with check values 2.365 at 8 groups, 2.262
at 10 groups, and 2.045 at 30 groups.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.eval, with function names taken from the behaviour wording
of each row. Fields a row does not state are not invented.
EVAL-T11 is a pointer row: its class states no second wording of
the behaviour and exercises the pass condition stated in the
central row DATASET-T05 at its evaluation call point only.
"""

import unittest

try:
    from tests.harness import require, stage_carried
except ImportError:
    from harness import require, stage_carried

MODULE = "ontoloop.eval"

STUDENT_T_CHECK_VALUES = {8: 2.365, 10: 2.262, 30: 2.045}
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

    def test_noise_uses_the_student_t_multiplier_by_group_count(self):
        module = require(MODULE)
        for groups, multiplier in STUDENT_T_CHECK_VALUES.items():
            taken = module.student_t_multiplier(groups)
            self.assertAlmostEqual(taken, multiplier, places=3)

    def test_noise_is_multiplier_times_standard_error_of_differences(self):
        module = require(MODULE)
        for groups, multiplier in STUDENT_T_CHECK_VALUES.items():
            result = module.margin_components(groups=groups)
            self.assertAlmostEqual(
                result["components"]["noise"],
                multiplier
                * result["standard_error_of_paired_differences"],
            )

    def test_the_fixed_multiplier_2_is_not_used(self):
        module = require(MODULE)
        for groups in STUDENT_T_CHECK_VALUES:
            self.assertNotAlmostEqual(
                module.student_t_multiplier(groups), 2.0, places=3
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


if __name__ == "__main__":
    unittest.main()
