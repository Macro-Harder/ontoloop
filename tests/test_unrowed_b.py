"""F-C2 unrowed obligations, seat B range: plan subsections 19.17,
19.33, 19.34, 19.35, 19.36, 19.37, and 19.38.

Each subsection below is written as a suite test under its own
recorded transcription decision, homed at the subsection and counted
in the suite manifest under the subsection, under the F-C2 rulings
at design/steps/step-13-content-retrace.md section 5. No identifier
is stated in the plan for any of these obligations and none is
invented here. Each class carries a comment block naming its
subsection, the obligation as stated, and the transcription choice
this seat recorded for it.

Failure and boundary perspective: these tests prize the refusal,
firing boundary, and reporting only outcomes the subsections state.
"""

import unittest

from tests.harness import require, stage_carried


# ------------------------------------------------------------------
# Subsection 19.17, the purge preview.
# Obligation as stated: one OPS test row added at section 6.5,
# driving the purge preview: it shows all three contents, the
# identities affected, the datasets and promotions that would be
# marked, and the exports and backups presumed still to hold the
# material; it stands before any purge append in the driven
# sequence; and it fails where a purge act proceeds without the
# preview for that act.
# Transcription choice: one test case class in this file, exercised
# through the module ontoloop.ops, the OPS-MIGRATE surface named in
# the subsection heading, with the preview driven as an act in the
# purge sequence so its position before the purge append is checked
# in sequence order, not only in record content. The preview showing
# record home is the operator surface record for the purge occasion,
# kept with the purge records.
# ------------------------------------------------------------------
class TestUnrowed1917Preview(unittest.TestCase):
    """Subsection 19.17: the purge preview stands before the act."""

    def test_preview_shows_identities_affected(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertTrue(preview["identities_affected"])

    def test_preview_shows_datasets_and_promotions_to_be_marked(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertTrue(preview["datasets_to_be_marked"])
        self.assertTrue(preview["promotions_to_be_marked"])

    def test_preview_shows_exports_and_backups_presumed_holding(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertTrue(preview["exports_presumed_holding"])
        self.assertTrue(preview["backups_presumed_holding"])

    def test_preview_showing_stands_on_its_record_home(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertEqual(
            preview["record_home"],
            "operator surface record for the purge occasion",
        )
        self.assertEqual(preview["kept_with"], "purge records")

    def test_preview_stands_before_any_purge_append(self):
        module = require("ontoloop.ops")
        sequence = module.driven_purge_sequence()
        self.assertLess(
            sequence.index("purge preview"),
            sequence.index("purge append"),
        )

    def test_purge_without_preview_for_that_act_fails(self):
        module = require("ontoloop.ops")
        outcome = module.purge_without_preview()
        self.assertTrue(outcome["failed"])
        self.assertFalse(outcome["purge_proceeded"])

    def test_preview_reading_is_the_authorisation_timing_reading(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertEqual(
            preview["authorisation_timing_event"],
            "purge authorisation timing",
        )
        self.assertIs(
            preview["preview_reading_for_authorisation_timing"],
            True,
        )
        self.assertEqual(
            preview["authorisation_record_home"],
            "rehearsal register",
        )
        self.assertEqual(
            preview["authorisation_owning_seat"],
            "OPS-MIGRATE slice owner seat",
        )
        self.assertEqual(
            preview["authorisation_fallback_seat"],
            "Live-proof Owner",
        )
        real_preview = module.purge_preview(occasion="real")
        self.assertEqual(
            real_preview["authorisation_record_home"],
            "purge record",
        )
        self.assertIs(
            real_preview["preview_reading_for_authorisation_timing"],
            True,
        )


# ------------------------------------------------------------------
# Subsection 19.33, the declaration refusal.
# Obligation as stated: a CORE test row added under this subsection,
# refusing an unlisted declaration, a training technique under
# another name, and a case or spacing variant of a listed name, each
# in the named error declared training technique refused, with the
# shipped refused set the exact strings sft, dpo, and grpo matched
# after case folding and whitespace collapse, and no state change to
# the declared record.
# Transcription choice: one test case class in this file, exercised
# through the module ontoloop.core, with the three refusal cases
# driven as declaration presentations and the matching form checked
# on written variants of the exact strings, so the case folding and
# whitespace collapse limbs are exercised in fact.
# ------------------------------------------------------------------
class TestUnrowed1933DeclarationRefusal(unittest.TestCase):
    """Subsection 19.33: declared training technique refused."""

    ERROR = "declared training technique refused"

    def test_unlisted_declaration_is_refused_in_the_named_error(self):
        module = require("ontoloop.core")
        outcome = module.present_declaration("unlisted declaration")
        self.assertEqual(outcome["error"], self.ERROR)

    def test_training_technique_under_another_name_is_refused(self):
        module = require("ontoloop.core")
        outcome = module.present_declaration(
            "training technique under another name"
        )
        self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_of_listed_names_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("SFT", " dpo ", "g rpo"):
            outcome = module.present_declaration(variant)
            self.assertEqual(outcome["error"], self.ERROR)

    def test_the_shipped_refused_set_is_exactly_the_three_strings(self):
        module = require("ontoloop.core")
        self.assertEqual(module.refused_technique_set(),
                         {"sft", "dpo", "grpo"})

    def test_refusal_changes_no_state_of_the_declared_record(self):
        module = require("ontoloop.core")
        outcome = module.present_declaration("SFT")
        self.assertFalse(outcome["declared_record_changed"])
        self.assertTrue(outcome["journal_refusal_recorded"])


# ------------------------------------------------------------------
# Subsection 19.34, the grader calibration practice, governed at
# subsection 20.2.
# Obligation as stated: an EVAL test or stage row added under this
# subsection, drawing a sample across the graded runs of the dataset
# version, recording the agreement figure and the sample identities
# for the cycle, and raising the intake account flag on a sample
# below 8 of 10 at band level, at the cadence of 10 runs per dataset
# version or 30 days.
# Transcription choice: subsection 20.2 governs this subsection and
# states that a sample drawn by store sequence rotation is not a
# calibration sample, that the single record home is the calibration
# record, and that the flag blocks consumption of the flagged
# version in the form clause four of subsection 20.2 states, the
# rotation form and the no block form of subsection 19.34 carrying
# no reading. This class is therefore written in the governing
# subsection 20.2 form: keyed selection, the calibration record as
# the one home, and the consumption bar, with the cadence and the
# 8 of 10 bar as subsection 19.34 states them.
# ------------------------------------------------------------------
class TestUnrowed1934CalibrationPractice(unittest.TestCase):
    """Subsection 19.34 as governed at subsection 20.2."""

    def test_sample_is_drawn_by_keyed_selection(self):
        module = require("ontoloop.eval")
        sample = module.calibration_sample()
        self.assertEqual(sample["selection"], "keyed")
        self.assertFalse(sample["predictable_from_store_sequence_order"])

    def test_a_rotation_drawn_sample_is_not_a_calibration_sample(self):
        module = require("ontoloop.eval")
        sample = module.calibration_sample(drawn_by="store sequence rotation")
        self.assertFalse(sample["is_calibration_sample"])

    def test_agreement_and_sample_identities_stand_on_one_record(self):
        module = require("ontoloop.eval")
        record = module.calibration_record()
        self.assertTrue(record["agreement_figure"])
        self.assertTrue(record["sample_identities_under_key"])
        self.assertEqual(record["record_count_for_sample"], 1)
        runs_three = [
            {"id": "graded run %02d" % (index + 1),
             "agreed": index < 3}
            for index in range(10)
        ]
        record_three = module.calibration_record(runs=runs_three)
        self.assertEqual(record_three["agreement_figure"], "3 of 10")
        self.assertEqual(record_three["agreement_count"], 3)
        self.assertEqual(record_three["sample_size"], 10)
        runs_seven = [
            {"id": "graded run %02d" % (index + 1),
             "agreed": index < 7}
            for index in range(10)
        ]
        record_seven = module.calibration_record(runs=runs_seven)
        self.assertEqual(record_seven["agreement_figure"], "7 of 10")
        self.assertEqual(record_seven["agreement_count"], 7)
        self.assertEqual(record_seven["sample_size"], 10)
        self.assertNotEqual(
            record_three["agreement_figure"],
            record_seven["agreement_figure"],
        )

    def test_loop_report_prints_the_figure_drawn_from_that_record(self):
        module = require("ontoloop.eval")
        record = module.calibration_record()
        report = module.loop_report_for_cycle()
        self.assertEqual(
            report["agreement_figure"], record["agreement_figure"]
        )
        self.assertEqual(report["figure_source"], "calibration record")

    def test_below_8_of_10_raises_the_intake_flag(self):
        module = require("ontoloop.eval")
        outcome = module.calibration_outcome(agreement="7 of 10")
        self.assertTrue(outcome["intake_flag_raised"])
        self.assertTrue(outcome["already_consumed_marked_flagged"])

    def test_flag_bars_further_consumption_of_the_flagged_version(self):
        module = require("ontoloop.eval")
        outcome = module.calibration_outcome(agreement="7 of 10")
        self.assertTrue(outcome["consumption_barred"])
        for act in ("dataset build", "evaluation", "promotion"):
            self.assertIn(act, outcome["barred_acts"])

    def test_bar_lifts_only_on_fresh_pass_or_reasoned_decision(self):
        module = require("ontoloop.eval")
        outcome = module.calibration_outcome(agreement="7 of 10")
        self.assertEqual(
            set(outcome["bar_lifts_on"]),
            {"fresh sample passes", "reasoned operator decision"},
        )

    def test_at_or_above_8_of_10_no_flag_and_no_bar(self):
        module = require("ontoloop.eval")
        outcome = module.calibration_outcome(agreement="8 of 10")
        self.assertFalse(outcome["intake_flag_raised"])
        self.assertFalse(outcome["consumption_barred"])

    def test_cadence_is_10_runs_per_version_or_30_days(self):
        module = require("ontoloop.eval")
        cadence = module.calibration_cadence()
        self.assertEqual(cadence["runs_per_dataset_version"], 10)
        self.assertEqual(cadence["days"], 30)
        self.assertEqual(cadence["trigger"], "whichever comes first")

    def test_re_grade_conceals_the_original_grade(self):
        module = require("ontoloop.eval")
        re_grade = module.calibration_re_grade_case()
        self.assertFalse(re_grade["original_grade_shown"])
        self.assertTrue(re_grade["bundle_identity_visible"])

    def test_calibration_record_is_the_single_home_for_the_sample(self):
        module = require("ontoloop.eval")
        homes = module.calibration_record_homes()
        self.assertEqual(homes["sample_record_home"], "calibration record")
        self.assertFalse(homes["loop_report_is_second_home"])
        self.assertFalse(homes["intake_account_is_second_home"])

    def test_proceeding_decision_stands_on_the_calibration_record(self):
        module = require("ontoloop.eval")
        decision = module.proceeding_decision_for_flagged_version()
        self.assertTrue(decision["decision_recorded"])
        self.assertEqual(decision["record_home"], "calibration record")


# ------------------------------------------------------------------
# Subsection 19.35, the closed intake stamp set: DATASET attachment.
# Obligation as stated: a DATASET test row added under this
# subsection, attaching each stamp of the closed set, intake thin,
# high self reported share, and low confidence, on its trigger and
# attaching none off its trigger, in the trigger forms the
# subsection states: intake thin where a dataset has a failure share
# of zero, high self reported share where the channel share exceeds
# one third, and low confidence below 30 holdout groups.
# Transcription choice: the first of the two suite tests the F-C2
# ruling states for this subsection, exercised through the module
# ontoloop.dataset, one method per stamp trigger and one boundary
# method per stamp off its trigger, so each trigger is checked on
# both sides of its boundary.
# ------------------------------------------------------------------
class TestUnrowed1935DatasetStamps(unittest.TestCase):
    """Subsection 19.35, DATASET test: stamps attach on trigger."""

    def test_the_stamp_set_is_closed_at_three_stamps(self):
        module = require("ontoloop.dataset")
        self.assertEqual(
            module.intake_stamp_set(),
            {"intake thin", "high self reported share", "low confidence"},
        )

    def test_intake_thin_attaches_at_a_failure_share_of_zero(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(failure_share=0)
        self.assertIn("intake thin", stamps)

    def test_intake_thin_does_not_attach_above_zero_failure_share(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(failure_share=0.1)
        self.assertNotIn("intake thin", stamps)

    def test_high_self_reported_share_attaches_above_one_third(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(channel_share=0.5)
        self.assertIn("high self reported share", stamps)

    def test_high_self_reported_share_does_not_attach_at_one_third(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(channel_share=1 / 3)
        self.assertNotIn("high self reported share", stamps)

    def test_low_confidence_attaches_below_30_holdout_groups(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(holdout_groups=29)
        self.assertIn("low confidence", stamps)

    def test_low_confidence_does_not_attach_at_30_holdout_groups(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(holdout_groups=30)
        self.assertNotIn("low confidence", stamps)

    def test_no_stamp_attaches_off_every_trigger(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0.2, channel_share=0.2, holdout_groups=40
        )
        self.assertEqual(stamps, set())

    def test_no_later_slice_originates_a_stamp(self):
        module = require("ontoloop.dataset")
        self.assertEqual(module.stamp_origin_slice(), "DATASET")

    def test_attached_stamp_stands_on_the_dataset_record(self):
        module = require("ontoloop.dataset")
        outcome = module.attach_stamps_at_build(failure_share=0)
        self.assertEqual(outcome["record_home"], "dataset record")
        self.assertIn("intake thin", outcome["attached_stamps"])


# ------------------------------------------------------------------
# Subsection 19.35, the closed intake stamp set: REPORT travel.
# Obligation as stated: a REPORT test row added under this
# subsection, showing the attached stamp at every step of the travel
# chain, Dataset to Evaluation to Promotion Record to the bundle
# caveats block to the loop report, in the same view as the result.
# Transcription choice: the second of the two suite tests the F-C2
# ruling states for this subsection, exercised through the module
# ontoloop.report, checking the chain as an ordered list of steps
# with the stamp name unchanged at each step and the stamp standing
# in the same view as the result at the loop report step.
# ------------------------------------------------------------------
class TestUnrowed1935ReportTravel(unittest.TestCase):
    """Subsection 19.35, REPORT test: the stamp travel chain."""

    CHAIN = (
        "Dataset",
        "Evaluation",
        "Promotion Record",
        "bundle caveats block",
        "loop report",
    )

    def test_the_chain_has_the_five_steps_in_order(self):
        module = require("ontoloop.report")
        chain = module.stamp_travel_chain("intake thin")
        self.assertEqual(tuple(chain["steps"]), self.CHAIN)

    def test_the_stamp_stands_at_every_step_unchanged_in_name(self):
        module = require("ontoloop.report")
        chain = module.stamp_travel_chain("intake thin")
        for step in self.CHAIN:
            self.assertEqual(chain["stamp_at"][step], "intake thin")

    def test_the_stamp_stands_in_the_same_view_as_the_result(self):
        module = require("ontoloop.report")
        chain = module.stamp_travel_chain("intake thin")
        self.assertEqual(
            chain["loop_report_view"], chain["result_view"]
        )
        self.assertTrue(chain["stamp_in_result_view"])


# ------------------------------------------------------------------
# Subsection 19.36, the literal named error.
# Obligation as stated: a test row added under this subsection at
# each cross split audit call point, refusing in the literal name
# flagged material inside candidate bundle and in no other wording,
# recording the state change the subsection states, the candidate
# bundle refused, no promotion proceeding on it, and the evaluation
# recorded as not scored with its typed reason, and applying the
# charging form on both the scored and the unscored cases: charged
# as one completed evaluation where any case was scored before the
# refusal, and as no completed evaluation where no case was scored.
# Transcription choice: one test case class per call point, the
# dataset build call point of DATASET-T05, the evaluation call
# point, and the promotion call point, exercised through the module
# ontoloop.cross_split_audit, which the subsection names as the
# raising module at the evaluation and promotion call points, with
# the literal name asserted as an exact string in every class.
# ------------------------------------------------------------------
class TestUnrowed1936DatasetCallPoint(unittest.TestCase):
    """Subsection 19.36: literal name at the dataset build point."""

    NAME = "flagged material inside candidate bundle"

    def test_refusal_carries_the_literal_name_and_no_other(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build("flagged material in bundle")
        self.assertEqual(outcome["error"], self.NAME)
        self.assertEqual(outcome["wording_variants"], [])

    def test_the_candidate_bundle_is_refused(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build("flagged material in bundle")
        self.assertTrue(outcome["candidate_bundle_refused"])

    def test_no_promotion_proceeds_on_the_refused_bundle_at_build(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build("flagged material in bundle")
        self.assertFalse(outcome["promotion_proceeded"])

    def test_evaluation_recorded_not_scored_at_the_build_point(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build("flagged material in bundle")
        self.assertEqual(outcome["evaluation_state"], "not scored")
        self.assertTrue(outcome["typed_reason"])

    def test_record_home_at_the_build_point_is_evaluation_record(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build("flagged material in bundle")
        self.assertEqual(outcome["record_home"], "evaluation record")

    def test_charging_at_build_where_a_case_was_scored_first(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build(
            "flagged material in bundle", scored_before_refusal=True
        )
        self.assertEqual(outcome["completed_evaluations_charged"], 1)

    def test_charging_at_build_where_no_case_was_scored(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_build(
            "flagged material in bundle", scored_before_refusal=False
        )
        self.assertEqual(outcome["completed_evaluations_charged"], 0)


class TestUnrowed1936EvaluationCallPoint(unittest.TestCase):
    """Subsection 19.36: literal name at the evaluation point."""

    NAME = "flagged material inside candidate bundle"

    def test_refusal_carries_the_literal_name_and_no_other(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation("flagged material in bundle")
        self.assertEqual(outcome["error"], self.NAME)
        self.assertEqual(outcome["wording_variants"], [])

    def test_evaluation_recorded_not_scored_with_its_typed_reason(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation("flagged material in bundle")
        self.assertEqual(outcome["evaluation_state"], "not scored")
        self.assertTrue(outcome["typed_reason"])

    def test_the_candidate_bundle_is_refused_at_evaluation(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation("flagged material in bundle")
        self.assertTrue(outcome["candidate_bundle_refused"])

    def test_no_promotion_proceeds_on_the_refused_bundle_at_evaluation(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation("flagged material in bundle")
        self.assertFalse(outcome["promotion_proceeded"])

    def test_record_home_is_the_evaluation_record(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation("flagged material in bundle")
        self.assertEqual(outcome["record_home"], "evaluation record")

    def test_charging_form_where_a_case_was_scored_before_refusal(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation(
            "flagged material in bundle", scored_before_refusal=True
        )
        self.assertEqual(outcome["completed_evaluations_charged"], 1)

    def test_charging_form_where_no_case_was_scored(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_evaluation(
            "flagged material in bundle", scored_before_refusal=False
        )
        self.assertEqual(outcome["completed_evaluations_charged"], 0)


class TestUnrowed1936PromotionCallPoint(unittest.TestCase):
    """Subsection 19.36: literal name at the promotion point."""

    NAME = "flagged material inside candidate bundle"

    def test_refusal_carries_the_literal_name_and_no_other(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_promotion("flagged material in bundle")
        self.assertEqual(outcome["error"], self.NAME)
        self.assertEqual(outcome["wording_variants"], [])

    def test_no_promotion_proceeds_on_the_refused_bundle(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_promotion("flagged material in bundle")
        self.assertTrue(outcome["candidate_bundle_refused"])
        self.assertFalse(outcome["promotion_proceeded"])

    def test_record_home_is_the_promotion_record(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_promotion("flagged material in bundle")
        self.assertEqual(outcome["record_home"], "Promotion Record")

    def test_charging_at_promotion_where_a_case_was_scored_first(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_promotion(
            "flagged material in bundle", scored_before_refusal=True
        )
        self.assertEqual(outcome["completed_evaluations_charged"], 1)

    def test_charging_at_promotion_where_no_case_was_scored(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_promotion(
            "flagged material in bundle", scored_before_refusal=False
        )
        self.assertEqual(outcome["completed_evaluations_charged"], 0)


# ------------------------------------------------------------------
# Subsection 19.94, the dataset build audit bounding rule.
# Obligation as stated: pair comparisons grow with the square of
# the material compared; comparisons run over an index keyed on
# the group and signature relations, so pairs sharing neither
# relation are not compared; pairs the index selects carry the
# full comparison. Revisit volume: 20,000 runs in scope, guessed.
# Example E prices a cross split audit comparison per pair at
# 5 work units, guessed.
# Transcription choice: one test case class in this file,
# exercised through the module ontoloop.cross_split_audit, with
# candidate and holdout items presented as mappings carrying a
# group, a signature, and a text, so the index selection and the
# per pair cost counting are exercised in fact.
# ------------------------------------------------------------------
class TestUnrowed1994CrossSplitIndex(unittest.TestCase):
    """Subsection 19.94: comparisons over the keyed index only."""

    def _material(self, candidate, holdout):
        return {
            "candidate_items": candidate,
            "holdout_items": holdout,
        }

    def test_pairs_sharing_neither_relation_are_not_compared(self):
        module = require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(
            self._material(
                [{"group": "g1", "signature": "s1",
                  "text": "alpha beta gamma"}],
                [{"group": "g2", "signature": "s2",
                  "text": "delta epsilon zeta"}],
            )
        )
        self.assertEqual(result["comparisons"], 0)
        self.assertEqual(result["cost_units"], 0)

    def test_a_pair_sharing_a_group_is_compared_at_the_example_e_weight(self):
        module = require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(
            self._material(
                [{"group": "g1", "signature": "s1",
                  "text": "alpha beta gamma"}],
                [{"group": "g1", "signature": "s2",
                  "text": "delta epsilon zeta"}],
            )
        )
        self.assertEqual(result["comparisons"], 1)
        self.assertEqual(result["cost_weight_per_pair"], 5)
        self.assertEqual(result["cost_units"], 5)

    def test_cost_counts_every_selected_pair_and_no_other_pair(self):
        module = require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(
            self._material(
                [{"group": "g1", "signature": "s1",
                  "text": "alpha beta gamma"},
                 {"group": "g3", "signature": "s3",
                  "text": "eta theta iota"}],
                [{"group": "g1", "signature": "s9",
                  "text": "delta epsilon zeta"},
                 {"group": "g9", "signature": "s3",
                  "text": "kappa lambda mu"}],
            )
        )
        self.assertEqual(result["comparisons"], 2)
        self.assertEqual(result["cost_units"], 10)
        self.assertEqual(result["revisit_volume_runs"], 20000)
        self.assertFalse(result["all_pairs_compared"])


# ------------------------------------------------------------------
# Subsection 19.37, the warning act: count form.
# Obligation as stated: test rows added under this subsection for
# the two warning forms: the count form, firing the reuse warning
# at a count of 2 against a bound of 3 and not at a count of 1; and
# the age form, firing the stale warning at 75 percent of its 90 day
# bound; each warning naming the decision it informs on the surface
# that prints it, and neither firing changing a bound or blocking
# an act.
# Transcription choice: the first of the two suite tests the F-C2
# ruling states for this subsection, exercised through the module
# ontoloop.promote, the slice the subsection names as owner of the
# reuse warning, with counts 1 and 2 checked on both sides of the
# firing point and the bound and block limbs checked on the firing
# case itself.
# ------------------------------------------------------------------
class TestUnrowed1937CountForm(unittest.TestCase):
    """Subsection 19.37, count form: reuse warning at 2 of 3."""

    def test_the_warning_fires_at_a_count_of_2(self):
        module = require("ontoloop.promote")
        outcome = module.reuse_warning_at_count(2, bound=3)
        self.assertTrue(outcome["fired"])

    def test_the_warning_does_not_fire_at_a_count_of_1(self):
        module = require("ontoloop.promote")
        outcome = module.reuse_warning_at_count(1, bound=3)
        self.assertFalse(outcome["fired"])

    def test_the_warning_names_the_decision_it_informs(self):
        module = require("ontoloop.promote")
        outcome = module.reuse_warning_at_count(2, bound=3)
        self.assertTrue(outcome["decision_named"])
        self.assertTrue(outcome["surface_prints_decision_name"])

    def test_firing_changes_no_bound_and_blocks_no_act(self):
        module = require("ontoloop.promote")
        outcome = module.reuse_warning_at_count(2, bound=3)
        self.assertEqual(outcome["bound_after"], 3)
        self.assertFalse(outcome["act_blocked"])


class TestPromoteR2Pro1(unittest.TestCase):
    """R2-PRO-1: a reuse warning bound below 1 stands refused."""

    def test_bound_zero_stands_refused_naming_the_bound(self):
        module = require("ontoloop.promote")
        with self.assertRaises(ValueError) as caught:
            module.reuse_warning_at_count(0, bound=0)
        self.assertIn("bound", str(caught.exception))
        self.assertIn("0", str(caught.exception))

    def test_bound_below_one_stands_refused(self):
        module = require("ontoloop.promote")
        with self.assertRaises(ValueError):
            module.reuse_warning_at_count(0, bound=-2)

    def test_governed_bounds_behave_as_round_2_probed_them(self):
        module = require("ontoloop.promote")
        cases = [
            (3, 2, 1, 2),
            (4, 3, 2, 3),
            (8, 6, 5, 6),
        ]
        for bound, point, below, at in cases:
            under = module.reuse_warning_at_count(below, bound=bound)
            self.assertFalse(under["fired"])
            self.assertEqual(under["firing_point_count"], point)
            self.assertEqual(under["bound_after"], bound)
            self.assertFalse(under["act_blocked"])
            over = module.reuse_warning_at_count(at, bound=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_count"], point)
            self.assertEqual(over["bound_after"], bound)
            self.assertFalse(over["act_blocked"])


# ------------------------------------------------------------------
# Subsection 19.37, the warning act: age form.
# Obligation as stated: as the count form above, for the age form:
# the stale warning fires at 75 percent of its 90 day bound, each
# warning naming the decision it informs on the surface that prints
# it, and neither firing changing a bound or blocking an act.
# Transcription choice: the second of the two suite tests the F-C2
# ruling states for this subsection, exercised through the module
# ontoloop.dataset, the slice the subsection names as owner of the
# stale warning, with the firing point computed as 75 percent of
# 90 days and an age below that point checked as not firing.
# ------------------------------------------------------------------
class TestUnrowed1937AgeForm(unittest.TestCase):
    """Subsection 19.37, age form: stale warning at 75 percent."""

    def test_the_warning_fires_at_75_percent_of_the_90_day_bound(self):
        module = require("ontoloop.dataset")
        outcome = module.stale_warning_at_age(days=67.5, bound_days=90)
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["firing_point_fraction"], 0.75)

    def test_the_warning_does_not_fire_below_75_percent(self):
        module = require("ontoloop.dataset")
        outcome = module.stale_warning_at_age(days=60, bound_days=90)
        self.assertFalse(outcome["fired"])

    def test_the_warning_names_the_decision_it_informs(self):
        module = require("ontoloop.dataset")
        outcome = module.stale_warning_at_age(days=67.5, bound_days=90)
        self.assertTrue(outcome["decision_named"])
        self.assertTrue(outcome["surface_prints_decision_name"])

    def test_firing_changes_no_bound_and_blocks_no_act(self):
        module = require("ontoloop.dataset")
        outcome = module.stale_warning_at_age(days=67.5, bound_days=90)
        self.assertEqual(outcome["bound_after_days"], 90)
        self.assertFalse(outcome["act_blocked"])


# ------------------------------------------------------------------
# Subsection 19.38, the expected maximum times standard error
# figure.
# Obligation as stated: an EVAL test row added under this
# subsection, reporting the expected maximum times the standard
# error figure at the attempt count charged on a closing evaluation
# record, with its approximation and guess labelling and its
# replacing event, the first dataset version that exhausts its
# budget, and checking that the figure enters no gate figure, no
# verdict component, and no comparison in the same evaluation.
# Transcription choice: one test case class in this file, exercised
# through the module ontoloop.eval, with the reporting only limbs
# checked as absence assertions over the gate figures, the verdict
# components, and the comparisons of the same evaluation record, so
# a figure that leaked into any of them would fail in fact.
# ------------------------------------------------------------------
class TestUnrowed1938ExpectedMaximumFigure(unittest.TestCase):
    """Subsection 19.38: the reporting only figure on the record."""

    FIGURE = "expected maximum times standard error"

    def test_the_figure_stands_on_the_closing_evaluation_record(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        self.assertIn(self.FIGURE, record["figures"])
        self.assertEqual(
            record["figures"][self.FIGURE]["at"],
            "attempt count charged",
        )

    def test_the_figure_carries_approximation_and_guess_labelling(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        figure = record["figures"][self.FIGURE]
        self.assertTrue(figure["is_approximation"])
        self.assertEqual(figure["source_class"], "guess")
        self.assertFalse(figure["read_as_bias_measurement"])

    def test_the_replacing_event_is_named_on_the_record(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        self.assertEqual(
            record["figures"][self.FIGURE]["replacing_event"],
            "first dataset version that exhausts its budget",
        )

    def test_the_figure_enters_no_gate_figure(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        self.assertNotIn(self.FIGURE, record["gate_figures"])

    def test_the_figure_enters_no_verdict_component(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        self.assertNotIn(self.FIGURE, record["verdict_components"])

    def test_the_figure_enters_no_comparison_in_the_evaluation(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        self.assertNotIn(self.FIGURE, record["comparisons"])


if __name__ == "__main__":
    unittest.main()
