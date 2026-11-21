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
        self.assertEqual(
            preview["identities_affected"],
            ["tombstoned identity a", "tombstoned identity b"],
        )

    def test_preview_shows_datasets_and_promotions_to_be_marked(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertTrue(preview["datasets_to_be_marked"])
        self.assertTrue(preview["promotions_to_be_marked"])
        self.assertEqual(
            preview["datasets_to_be_marked"],
            [
                "dataset holding tombstoned identity a",
                "dataset holding tombstoned identity b",
            ],
        )
        self.assertEqual(
            preview["promotions_to_be_marked"],
            [
                "promotion holding tombstoned identity a",
                "promotion holding tombstoned identity b",
            ],
        )

    def test_preview_shows_exports_and_backups_presumed_holding(self):
        module = require("ontoloop.ops")
        preview = module.purge_preview()
        self.assertTrue(preview["exports_presumed_holding"])
        self.assertTrue(preview["backups_presumed_holding"])
        self.assertEqual(
            preview["exports_presumed_holding"],
            [
                "export presumed holding tombstoned identity a",
                "export presumed holding tombstoned identity b",
            ],
        )
        self.assertEqual(
            preview["backups_presumed_holding"],
            [
                "backup presumed holding tombstoned identity a",
                "backup presumed holding tombstoned identity b",
            ],
        )

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
        for variant in ("SFT", " dpo ", "g rpo", "s f t", "DPO",
                        "\tgrpo\n", "G r p o", "SfT", "d  p  o",
                        "GRPO ", "S F T", "dPo", "\nDPO\t",
                        "g  r  p  o", "GrPo", " sft ", "D P O",
                        "g r p o ", "SF T", "D PO", "GR PO",
                        "gRpo", "dp o", "s fT", " SFT ",
                        "d\tp\to", "sFt", "DpO", "GRpO",
                        "s  f  t", "\tSFT\t", "DP O",
                        "G RPO", "sf t", "sFT", "Dpo", "gRPO",
                        "s f  t", "\nSFT ", "D  PO", "GR  PO",
                        "sf  t", "Sf t", "d PO", "gR po",
                        "S f t", "dpO ", "\nGRPO", "sF t",
                        "DPo "):
            outcome = module.present_declaration(variant)
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_fifty_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("gRpO", "Dp o", "s fT ", "\tDPO", "GR PO ",
                        "Sf  t", "dP O", "grPO"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_fifty_eight_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("GRp o", "sF  t", "\nDPO ", "Dp  o", "gRP o",
                        "SFt ", "\tgrpo ", "D pO"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_sixty_six_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("GRpo\t", "sFt ", "Dp o ", "G R P O", "dP  o",
                        "\nsfT", "gr Po", "S F t"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_seventy_four_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("\tGRPO", "DPO\t", "GrPo ", " dpo", "SFT\n",
                        "gR pO", "D P O ", "sF T"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_eighty_two_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("\tSFT", "DPO\n", "sFt\t", " G RPO",
                        "gr  po", "dPo\t", "sft ", " G R P O"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_ninety_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("\nSFT", "GRPO\t", "gRPo ", " D P O",
                        "\tDPO ", "GR PO\n", "dpo\t", "sFt\n"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
            self.assertEqual(outcome["error"], self.ERROR)

    def test_case_and_spacing_variants_beyond_the_ninety_eight_presented_are_refused(self):
        module = require("ontoloop.core")
        for variant in ("\t\tSFT", "\nGRPO ", "g rpo ", " DPO\t",
                        "\nDPO", "GRPO\t\n", "sft\t\t", " G RPO\n"):
            outcome = module.present_declaration(variant)
            self.assertTrue(outcome["refused"])
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
        self.assertEqual(record["agreement_figure"], "9 of 10")
        self.assertEqual(record["agreement_count"], 9)
        self.assertEqual(record["sample_size"], 10)
        self.assertEqual(
            record["sample_identities_under_key"],
            ["graded run 07", "graded run 10", "graded run 03",
             "graded run 01", "graded run 05", "graded run 06",
             "graded run 04", "graded run 09", "graded run 08",
             "graded run 02"],
        )
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
        self.assertEqual(
            record_three["sample_identities_under_key"],
            ["graded run 07", "graded run 10", "graded run 03",
             "graded run 01", "graded run 05", "graded run 06",
             "graded run 04", "graded run 09", "graded run 08",
             "graded run 02"],
        )
        self.assertEqual(
            record_seven["sample_identities_under_key"],
            ["graded run 07", "graded run 10", "graded run 03",
             "graded run 01", "graded run 05", "graded run 06",
             "graded run 04", "graded run 09", "graded run 08",
             "graded run 02"],
        )
        self.assertNotEqual(
            record_three["agreement_figure"],
            record_seven["agreement_figure"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "run alpha", "agreed": True},
            {"id": "run beta", "agreed": True},
            {"id": "run gamma", "agreed": True},
            {"id": "run delta", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["run delta", "run gamma", "run alpha", "run beta"],
        )
        runs_six = [
            {"id": "sample k%d" % (index + 1),
             "agreed": index < 5}
            for index in range(6)
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["sample k3", "sample k4", "sample k1",
             "sample k5", "sample k6", "sample k2"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_still_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_three = [
            {"id": "case one", "agreed": True},
            {"id": "case two", "agreed": True},
            {"id": "case three", "agreed": False},
        ]
        record_three = module.calibration_record(runs=runs_three)
        self.assertEqual(record_three["agreement_figure"], "2 of 3")
        self.assertEqual(record_three["agreement_count"], 2)
        self.assertEqual(record_three["sample_size"], 3)
        self.assertEqual(record_three["record_count_for_sample"], 1)
        self.assertEqual(
            record_three["sample_identities_under_key"],
            ["case one", "case three", "case two"],
        )
        runs_five = [
            {"id": "item a", "agreed": True},
            {"id": "item b", "agreed": True},
            {"id": "item c", "agreed": True},
            {"id": "item d", "agreed": True},
            {"id": "item e", "agreed": False},
        ]
        record_five = module.calibration_record(runs=runs_five)
        self.assertEqual(record_five["agreement_figure"], "4 of 5")
        self.assertEqual(record_five["agreement_count"], 4)
        self.assertEqual(record_five["sample_size"], 5)
        self.assertEqual(record_five["record_count_for_sample"], 1)
        self.assertEqual(
            record_five["sample_identities_under_key"],
            ["item a", "item c", "item d",
             "item b", "item e"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_yet_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_two = [
            {"id": "north one", "agreed": True},
            {"id": "north two", "agreed": True},
        ]
        record_two = module.calibration_record(runs=runs_two)
        self.assertEqual(record_two["agreement_figure"], "2 of 2")
        self.assertEqual(record_two["agreement_count"], 2)
        self.assertEqual(record_two["sample_size"], 2)
        self.assertEqual(record_two["record_count_for_sample"], 1)
        self.assertEqual(
            record_two["sample_identities_under_key"],
            ["north two", "north one"],
        )
        runs_four = [
            {"id": "wave a", "agreed": True},
            {"id": "wave b", "agreed": True},
            {"id": "wave c", "agreed": True},
            {"id": "wave d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["wave d", "wave b", "wave c", "wave a"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_next_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_three = [
            {"id": "cedar one", "agreed": True},
            {"id": "cedar two", "agreed": True},
            {"id": "cedar three", "agreed": False},
        ]
        record_three = module.calibration_record(runs=runs_three)
        self.assertEqual(record_three["agreement_figure"], "2 of 3")
        self.assertEqual(record_three["agreement_count"], 2)
        self.assertEqual(record_three["sample_size"], 3)
        self.assertEqual(record_three["record_count_for_sample"], 1)
        self.assertEqual(
            record_three["sample_identities_under_key"],
            ["cedar two", "cedar one", "cedar three"],
        )
        runs_six = [
            {"id": "orbit a", "agreed": True},
            {"id": "orbit b", "agreed": True},
            {"id": "orbit c", "agreed": True},
            {"id": "orbit d", "agreed": True},
            {"id": "orbit e", "agreed": True},
            {"id": "orbit f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["orbit b", "orbit e", "orbit a",
             "orbit f", "orbit d", "orbit c"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_further_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "birch a", "agreed": True},
            {"id": "birch b", "agreed": True},
            {"id": "birch c", "agreed": True},
            {"id": "birch d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["birch a", "birch c", "birch d", "birch b"],
        )
        runs_five = [
            {"id": "comet a", "agreed": True},
            {"id": "comet b", "agreed": True},
            {"id": "comet c", "agreed": True},
            {"id": "comet d", "agreed": True},
            {"id": "comet e", "agreed": False},
        ]
        record_five = module.calibration_record(runs=runs_five)
        self.assertEqual(record_five["agreement_figure"], "4 of 5")
        self.assertEqual(record_five["agreement_count"], 4)
        self.assertEqual(record_five["sample_size"], 5)
        self.assertEqual(record_five["record_count_for_sample"], 1)
        self.assertEqual(
            record_five["sample_identities_under_key"],
            ["comet d", "comet b", "comet a",
             "comet c", "comet e"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_still_further_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "hazel a", "agreed": True},
            {"id": "hazel b", "agreed": True},
            {"id": "hazel c", "agreed": True},
            {"id": "hazel d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["hazel b", "hazel c", "hazel d", "hazel a"],
        )
        runs_six = [
            {"id": "willow a", "agreed": True},
            {"id": "willow b", "agreed": True},
            {"id": "willow c", "agreed": True},
            {"id": "willow d", "agreed": True},
            {"id": "willow e", "agreed": True},
            {"id": "willow f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["willow f", "willow e", "willow a",
             "willow d", "willow b", "willow c"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_next_further_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "maple a", "agreed": True},
            {"id": "maple b", "agreed": True},
            {"id": "maple c", "agreed": True},
            {"id": "maple d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["maple c", "maple b", "maple d", "maple a"],
        )
        runs_six = [
            {"id": "juniper a", "agreed": True},
            {"id": "juniper b", "agreed": True},
            {"id": "juniper c", "agreed": True},
            {"id": "juniper d", "agreed": True},
            {"id": "juniper e", "agreed": True},
            {"id": "juniper f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["juniper c", "juniper d", "juniper f",
             "juniper a", "juniper b", "juniper e"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_still_next_further_other_run_sets(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "ash a", "agreed": True},
            {"id": "ash b", "agreed": True},
            {"id": "ash c", "agreed": True},
            {"id": "ash d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["ash c", "ash d", "ash a", "ash b"],
        )
        runs_six = [
            {"id": "rowan a", "agreed": True},
            {"id": "rowan b", "agreed": True},
            {"id": "rowan c", "agreed": True},
            {"id": "rowan d", "agreed": True},
            {"id": "rowan e", "agreed": True},
            {"id": "rowan f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["rowan b", "rowan a", "rowan f",
             "rowan c", "rowan d", "rowan e"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_next_further_other_run_sets_past_still_next_further(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "alder a", "agreed": True},
            {"id": "alder b", "agreed": True},
            {"id": "alder c", "agreed": True},
            {"id": "alder d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["alder a", "alder d", "alder c", "alder b"],
        )
        runs_six = [
            {"id": "larch a", "agreed": True},
            {"id": "larch b", "agreed": True},
            {"id": "larch c", "agreed": True},
            {"id": "larch d", "agreed": True},
            {"id": "larch e", "agreed": True},
            {"id": "larch f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["larch c", "larch d", "larch f",
             "larch e", "larch b", "larch a"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_other_run_sets_past_next_further_still_next_further(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "beech a", "agreed": True},
            {"id": "beech b", "agreed": True},
            {"id": "beech c", "agreed": True},
            {"id": "beech d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["beech c", "beech d", "beech a", "beech b"],
        )
        runs_six = [
            {"id": "elm a", "agreed": True},
            {"id": "elm b", "agreed": True},
            {"id": "elm c", "agreed": True},
            {"id": "elm d", "agreed": True},
            {"id": "elm e", "agreed": True},
            {"id": "elm f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["elm d", "elm e", "elm a",
             "elm c", "elm b", "elm f"],
        )

    def test_agreement_and_sample_identities_stand_on_records_with_other_run_sets_past_next_further_still_next_further_next(self):
        module = require("ontoloop.eval")
        runs_four = [
            {"id": "aspen a", "agreed": True},
            {"id": "aspen b", "agreed": True},
            {"id": "aspen c", "agreed": True},
            {"id": "aspen d", "agreed": False},
        ]
        record_four = module.calibration_record(runs=runs_four)
        self.assertEqual(record_four["agreement_figure"], "3 of 4")
        self.assertEqual(record_four["agreement_count"], 3)
        self.assertEqual(record_four["sample_size"], 4)
        self.assertEqual(record_four["record_count_for_sample"], 1)
        self.assertEqual(
            record_four["sample_identities_under_key"],
            ["aspen a", "aspen b", "aspen c", "aspen d"],
        )
        runs_six = [
            {"id": "poplar a", "agreed": True},
            {"id": "poplar b", "agreed": True},
            {"id": "poplar c", "agreed": True},
            {"id": "poplar d", "agreed": True},
            {"id": "poplar e", "agreed": True},
            {"id": "poplar f", "agreed": False},
        ]
        record_six = module.calibration_record(runs=runs_six)
        self.assertEqual(record_six["agreement_figure"], "5 of 6")
        self.assertEqual(record_six["agreement_count"], 5)
        self.assertEqual(record_six["sample_size"], 6)
        self.assertEqual(record_six["record_count_for_sample"], 1)
        self.assertEqual(
            record_six["sample_identities_under_key"],
            ["poplar d", "poplar c", "poplar e",
             "poplar a", "poplar b", "poplar f"],
        )

    def test_loop_report_prints_the_figure_drawn_from_that_record(self):
        module = require("ontoloop.eval")
        record = module.calibration_record()
        report = module.loop_report_for_cycle()
        self.assertEqual(
            report["agreement_figure"], record["agreement_figure"]
        )
        self.assertEqual(report["figure_source"], "calibration record")
        runs_seven = [
            {"id": "graded run %02d" % (index + 1),
             "agreed": index < 7}
            for index in range(10)
        ]
        record_seven = module.calibration_record(runs=runs_seven)
        report_seven = module.loop_report_for_cycle(runs=runs_seven)
        self.assertEqual(report_seven["agreement_figure"], "7 of 10")
        self.assertEqual(
            report_seven["agreement_figure"],
            record_seven["agreement_figure"])
        self.assertEqual(report_seven["figure_source"], "calibration record")

    def test_sample_identities_stand_in_keyed_digest_order(self):
        import hashlib

        module = require("ontoloop.eval")
        probe_key = "probe key r5"
        identities = [
            "graded run 04", "graded run 01",
            "graded run 03", "graded run 02",
        ]
        runs = [{"id": identity, "agreed": True}
                for identity in identities]
        sample = module.calibration_sample(
            runs=runs, operator_key=probe_key)
        expected = sorted(
            identities,
            key=lambda identity: hashlib.sha256(
                ("%s\n%s" % (probe_key, identity)).encode("utf-8")
            ).hexdigest(),
        )
        self.assertNotEqual(expected, identities)
        self.assertNotEqual(expected, sorted(identities))
        self.assertEqual(
            sample["sample_identities_under_key"], expected)

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
        self.assertEqual(
            outcome["barred_acts"],
            ["dataset build", "evaluation", "promotion"],
        )

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
        self.assertEqual(stamps, {"intake thin"})

    def test_intake_thin_does_not_attach_above_zero_failure_share(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(failure_share=0.1)
        self.assertNotIn("intake thin", stamps)
        self.assertEqual(stamps, set())

    def test_high_self_reported_share_attaches_above_one_third(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(channel_share=0.5)
        self.assertIn("high self reported share", stamps)
        self.assertEqual(stamps, {"high self reported share"})

    def test_high_self_reported_share_does_not_attach_at_one_third(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(channel_share=1 / 3)
        self.assertNotIn("high self reported share", stamps)
        self.assertEqual(stamps, set())

    def test_low_confidence_attaches_below_30_holdout_groups(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(holdout_groups=29)
        self.assertIn("low confidence", stamps)
        self.assertEqual(stamps, {"low confidence"})

    def test_low_confidence_does_not_attach_at_30_holdout_groups(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(holdout_groups=30)
        self.assertNotIn("low confidence", stamps)
        self.assertEqual(stamps, set())

    def test_no_stamp_attaches_off_every_trigger(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0.2, channel_share=0.2, holdout_groups=40
        )
        self.assertEqual(stamps, set())

    def test_combined_triggers_attach_the_whole_stamp_set(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.5, holdout_groups=29
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.5
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=29
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.5, holdout_groups=29
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})

    def test_combined_triggers_attach_the_whole_stamp_set_at_further_values(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.9, holdout_groups=10
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.9
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=10
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.9, holdout_groups=10
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.34, holdout_groups=29
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_still_further_values(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.8, holdout_groups=5
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.8
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=5
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.8, holdout_groups=5
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.75, holdout_groups=20
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_yet_further_values(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.6, holdout_groups=10
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.6
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=12
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.6, holdout_groups=10
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.5, holdout_groups=15
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.6, holdout_groups=10
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_next_further_values(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.7, holdout_groups=20
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.7
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=25
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.7, holdout_groups=20
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.45, holdout_groups=18
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.7, holdout_groups=20
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_still_next_further_values(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.62, holdout_groups=14
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.62
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=14
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.62, holdout_groups=14
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.41, holdout_groups=22
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.62, holdout_groups=14
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_further_values_past_still_next(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.55, holdout_groups=17
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.55
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=17
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.55, holdout_groups=17
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.38, holdout_groups=26
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.55, holdout_groups=17
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_further_values_past_still_next_further(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.52, holdout_groups=19
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.52
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=19
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.52, holdout_groups=19
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.36, holdout_groups=24
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.52, holdout_groups=19
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_further_values_beyond_past_still_next_further(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.49, holdout_groups=27
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.49
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=27
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.49, holdout_groups=27
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.35, holdout_groups=28
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.49, holdout_groups=27
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_still_further_values_beyond_past_still_next_further(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.44, holdout_groups=21
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.44
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=21
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.44, holdout_groups=21
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.39, holdout_groups=23
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.44, holdout_groups=21
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_still_further_values_beyond_past_still_next_further_next(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.51, holdout_groups=16
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.51
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=16
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.51, holdout_groups=16
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.47, holdout_groups=13
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.51, holdout_groups=16
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_values_beyond_past_still_next_further_next_still_further(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.53, holdout_groups=11
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.53
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=11
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.53, holdout_groups=11
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.57, holdout_groups=11
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.53, holdout_groups=11
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_combined_triggers_attach_the_whole_stamp_set_at_values_beyond_past_still_next_further_next_still_further_next(self):
        module = require("ontoloop.dataset")
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.59, holdout_groups=9
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.59
        )
        self.assertEqual(
            stamps, {"intake thin", "high self reported share"})
        stamps = module.stamps_attached(
            failure_share=0, holdout_groups=9
        )
        self.assertEqual(stamps, {"intake thin", "low confidence"})
        stamps = module.stamps_attached(
            channel_share=0.59, holdout_groups=9
        )
        self.assertEqual(
            stamps, {"high self reported share", "low confidence"})
        stamps = module.stamps_attached(
            failure_share=0, channel_share=0.63, holdout_groups=9
        )
        self.assertEqual(
            stamps,
            {"intake thin", "high self reported share",
             "low confidence"},
        )
        outcome = module.attach_stamps_at_build(
            failure_share=0, channel_share=0.59, holdout_groups=9
        )
        self.assertEqual(
            outcome["attached_stamps"],
            {"intake thin", "high self reported share",
             "low confidence"},
        )

    def test_no_later_slice_originates_a_stamp(self):
        module = require("ontoloop.dataset")
        self.assertEqual(module.stamp_origin_slice(), "DATASET")

    def test_attached_stamp_stands_on_the_dataset_record(self):
        module = require("ontoloop.dataset")
        outcome = module.attach_stamps_at_build(failure_share=0)
        self.assertEqual(outcome["record_home"], "dataset record")
        self.assertIn("intake thin", outcome["attached_stamps"])
        self.assertEqual(outcome["attached_stamps"], {"intake thin"})


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
        self.assertEqual(
            outcome["typed_reason"],
            "refused on its presentation as flagged material",
        )

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
        self.assertEqual(
            outcome["typed_reason"],
            "refused on its presentation as flagged material",
        )

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

    def test_evaluation_recorded_not_scored_with_its_typed_reason_at_promotion(self):
        module = require("ontoloop.cross_split_audit")
        outcome = module.audit_at_promotion("flagged material in bundle")
        self.assertEqual(outcome["evaluation_state"], "not scored")
        self.assertEqual(
            outcome["typed_reason"],
            "refused on its presentation as flagged material",
        )

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
        self.assertEqual(
            outcome["decision"],
            "whether the bundle is reused for a further promotion",
        )

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
        self.assertEqual(
            str(caught.exception), "unknown reuse warning bound: 0")

    def test_bound_below_one_stands_refused(self):
        module = require("ontoloop.promote")
        with self.assertRaises(ValueError) as caught:
            module.reuse_warning_at_count(0, bound=-2)
        self.assertEqual(
            str(caught.exception), "unknown reuse warning bound: -2")

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

    def test_refusal_at_bounds_beyond_the_presented_pair(self):
        module = require("ontoloop.promote")
        cases = [
            (-1, "unknown reuse warning bound: -1"),
            (0.5, "unknown reuse warning bound: 0.5"),
            (-100, "unknown reuse warning bound: -100"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_bounds_beyond_the_presented_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (2, 1, 0, 1),
            (6, 4, 3, 4),
            (10, 7, 6, 7),
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

    def test_refusal_at_further_bounds_beyond_the_presented_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.9, "unknown reuse warning bound: 0.9"),
            (-1.5, "unknown reuse warning bound: -1.5"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_further_bounds_beyond_the_presented_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (7, 5, 4, 5),
            (12, 9, 8, 9),
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

    def test_refusal_at_domain_bounds_beyond_the_presented_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.99, "unknown reuse warning bound: 0.99"),
            (-3, "unknown reuse warning bound: -3"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_presented_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (13, 9, 8, 9),
            (100, 75, 74, 75),
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

    def test_refusal_at_outer_bounds_beyond_the_domain_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.999, "unknown reuse warning bound: 0.999"),
            (-4, "unknown reuse warning bound: -4"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_outer_bounds_beyond_the_domain_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (20, 15, 14, 15),
            (101, 75, 74, 75),
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

    def test_refusal_at_remaining_domain_bounds_beyond_the_outer_values(self):
        module = require("ontoloop.promote")
        cases = [
            (-0.5, "unknown reuse warning bound: -0.5"),
            (-50, "unknown reuse warning bound: -50"),
            (0.1, "unknown reuse warning bound: 0.1"),
            (0.98, "unknown reuse warning bound: 0.98"),
            (0.9999, "unknown reuse warning bound: 0.9999"),
            (-5, "unknown reuse warning bound: -5"),
            (0.99999, "unknown reuse warning bound: 0.99999"),
            (-1000, "unknown reuse warning bound: -1000"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_remaining_domain_bounds_beyond_the_outer_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (1, 1, 0, 1),
            (5, 3, 2, 3),
            (9, 6, 5, 6),
            (11, 8, 7, 8),
            (14, 10, 9, 10),
            (15, 11, 10, 11),
            (16, 12, 11, 12),
            (17, 12, 11, 12),
            (18, 13, 12, 13),
            (19, 14, 13, 14),
            (21, 15, 14, 15),
            (22, 16, 15, 16),
            (50, 37, 36, 37),
            (99, 74, 73, 74),
            (102, 76, 75, 76),
            (200, 150, 149, 150),
            (1000, 750, 749, 750),
            (10000, 7500, 7499, 7500),
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

    def test_refusal_at_domain_bounds_beyond_the_remaining_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.999999, "unknown reuse warning bound: 0.999999"),
            (-10000, "unknown reuse warning bound: -10000"),
            (0.001, "unknown reuse warning bound: 0.001"),
            (0.9999999, "unknown reuse warning bound: 0.9999999"),
            (-6, "unknown reuse warning bound: -6"),
            (-9999, "unknown reuse warning bound: -9999"),
            (0.2, "unknown reuse warning bound: 0.2"),
            (0.75, "unknown reuse warning bound: 0.75"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_remaining_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (23, 17, 16, 17),
            (24, 18, 17, 18),
            (25, 18, 17, 18),
            (30, 22, 21, 22),
            (40, 30, 29, 30),
            (60, 45, 44, 45),
            (75, 56, 55, 56),
            (98, 73, 72, 73),
            (103, 77, 76, 77),
            (150, 112, 111, 112),
            (500, 375, 374, 375),
            (999, 749, 748, 749),
            (1001, 750, 749, 750),
            (2000, 1500, 1499, 1500),
            (9999, 7499, 7498, 7499),
            (10001, 7500, 7499, 7500),
            (100000, 75000, 74999, 75000),
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

    def test_refusal_at_domain_bounds_beyond_the_next_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.99999999, "unknown reuse warning bound: 0.99999999"),
            (-100000, "unknown reuse warning bound: -100000"),
            (0.000001, "unknown reuse warning bound: 1e-06"),
            (0.999999999, "unknown reuse warning bound: 0.999999999"),
            (-7, "unknown reuse warning bound: -7"),
            (-99999, "unknown reuse warning bound: -99999"),
            (0.3, "unknown reuse warning bound: 0.3"),
            (0.6, "unknown reuse warning bound: 0.6"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_next_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (26, 19, 18, 19),
            (27, 20, 19, 20),
            (29, 21, 20, 21),
            (31, 23, 22, 23),
            (33, 24, 23, 24),
            (250, 187, 186, 187),
            (100001, 75000, 74999, 75000),
            (1000000, 750000, 749999, 750000),
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

    def test_refusal_at_domain_bounds_beyond_the_further_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.9999999999, "unknown reuse warning bound: 0.9999999999"),
            (-1000000, "unknown reuse warning bound: -1000000"),
            (0.0000001, "unknown reuse warning bound: 1e-07"),
            (0.99999999999, "unknown reuse warning bound: 0.99999999999"),
            (-8, "unknown reuse warning bound: -8"),
            (-999999, "unknown reuse warning bound: -999999"),
            (0.4, "unknown reuse warning bound: 0.4"),
            (0.7, "unknown reuse warning bound: 0.7"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_further_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (28, 21, 20, 21),
            (32, 24, 23, 24),
            (34, 25, 24, 25),
            (35, 26, 25, 26),
            (36, 27, 26, 27),
            (100002, 75001, 75000, 75001),
            (1000001, 750000, 749999, 750000),
            (10000000, 7500000, 7499999, 7500000),
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

    def test_refusal_at_domain_bounds_beyond_the_further_ring_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.999999999999, "unknown reuse warning bound: 0.999999999999"),
            (-10000000, "unknown reuse warning bound: -10000000"),
            (0.00000001, "unknown reuse warning bound: 1e-08"),
            (0.9999999999999, "unknown reuse warning bound: 0.9999999999999"),
            (-9, "unknown reuse warning bound: -9"),
            (-9999999, "unknown reuse warning bound: -9999999"),
            (0.8, "unknown reuse warning bound: 0.8"),
            (0.15, "unknown reuse warning bound: 0.15"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_further_ring_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (37, 27, 26, 27),
            (38, 28, 27, 28),
            (39, 29, 28, 29),
            (41, 30, 29, 30),
            (100003, 75002, 75001, 75002),
            (1000002, 750001, 750000, 750001),
            (10000001, 7500000, 7499999, 7500000),
            (100000000, 75000000, 74999999, 75000000),
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

    def test_refusal_at_domain_bounds_beyond_the_next_ring_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.99999999999999, "unknown reuse warning bound: 0.99999999999999"),
            (-100000000, "unknown reuse warning bound: -100000000"),
            (0.000000001, "unknown reuse warning bound: 1e-09"),
            (0.999999999999999, "unknown reuse warning bound: 0.999999999999999"),
            (-10, "unknown reuse warning bound: -10"),
            (-99999999, "unknown reuse warning bound: -99999999"),
            (0.85, "unknown reuse warning bound: 0.85"),
            (0.25, "unknown reuse warning bound: 0.25"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_next_ring_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (42, 31, 30, 31),
            (43, 32, 31, 32),
            (44, 33, 32, 33),
            (45, 33, 32, 33),
            (100004, 75003, 75002, 75003),
            (1000003, 750002, 750001, 750002),
            (10000002, 7500001, 7500000, 7500001),
            (1000000000, 750000000, 749999999, 750000000),
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

    def test_refusal_at_domain_bounds_beyond_the_following_ring_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.9999999999999994, "unknown reuse warning bound: 0.9999999999999994"),
            (-1000000000, "unknown reuse warning bound: -1000000000"),
            (0.0000000001, "unknown reuse warning bound: 1e-10"),
            (0.9999999999999997, "unknown reuse warning bound: 0.9999999999999997"),
            (-11, "unknown reuse warning bound: -11"),
            (-999999999, "unknown reuse warning bound: -999999999"),
            (0.95, "unknown reuse warning bound: 0.95"),
            (0.35, "unknown reuse warning bound: 0.35"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_following_ring_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (46, 34, 33, 34),
            (47, 35, 34, 35),
            (48, 36, 35, 36),
            (49, 36, 35, 36),
            (100005, 75003, 75002, 75003),
            (1000004, 750003, 750002, 750003),
            (10000003, 7500002, 7500001, 7500002),
            (10000000000, 7500000000, 7499999999, 7500000000),
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

    def test_refusal_at_domain_bounds_beyond_the_succeeding_ring_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.9999999999999998, "unknown reuse warning bound: 0.9999999999999998"),
            (-10000000000, "unknown reuse warning bound: -10000000000"),
            (0.00000000001, "unknown reuse warning bound: 1e-11"),
            (0.9999999999999996, "unknown reuse warning bound: 0.9999999999999996"),
            (-12, "unknown reuse warning bound: -12"),
            (-9999999999, "unknown reuse warning bound: -9999999999"),
            (0.96, "unknown reuse warning bound: 0.96"),
            (0.45, "unknown reuse warning bound: 0.45"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_succeeding_ring_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (51, 38, 37, 38),
            (52, 39, 38, 39),
            (53, 39, 38, 39),
            (54, 40, 39, 40),
            (100006, 75004, 75003, 75004),
            (1000005, 750003, 750002, 750003),
            (10000004, 7500003, 7500002, 7500003),
            (100000000000, 75000000000, 74999999999, 75000000000),
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

    def test_refusal_at_domain_bounds_of_the_next_ring_out_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.97, "unknown reuse warning bound: 0.97"),
            (0.55, "unknown reuse warning bound: 0.55"),
            (-13, "unknown reuse warning bound: -13"),
            (-99999999999, "unknown reuse warning bound: -99999999999"),
            (0.000000000001, "unknown reuse warning bound: 1e-12"),
            (0.9999999999999992, "unknown reuse warning bound: 0.9999999999999992"),
            (-100000000000, "unknown reuse warning bound: -100000000000"),
            (0.9999999999999999, "unknown reuse warning bound: 0.9999999999999999"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_of_the_next_ring_out_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (55, 41, 40, 41),
            (56, 42, 41, 42),
            (57, 42, 41, 42),
            (59, 44, 43, 44),
            (100007, 75005, 75004, 75005),
            (1000006, 750004, 750003, 750004),
            (10000005, 7500003, 7500002, 7500003),
            (1000000000000, 750000000000, 749999999999, 750000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_next_ring_out_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.965, "unknown reuse warning bound: 0.965"),
            (0.65, "unknown reuse warning bound: 0.65"),
            (-14, "unknown reuse warning bound: -14"),
            (-999999999999, "unknown reuse warning bound: -999999999999"),
            (0.0000000000001, "unknown reuse warning bound: 1e-13"),
            (0.9999999999999993, "unknown reuse warning bound: 0.9999999999999993"),
            (-1000000000000, "unknown reuse warning bound: -1000000000000"),
            (0.125, "unknown reuse warning bound: 0.125"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_next_ring_out_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (58, 43, 42, 43),
            (64, 48, 47, 48),
            (65, 48, 47, 48),
            (66, 49, 48, 49),
            (100009, 75006, 75005, 75006),
            (1000008, 750006, 750005, 750006),
            (10000007, 7500005, 7500004, 7500005),
            (10000000000000, 7500000000000, 7499999999999, 7500000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_further_ring_out_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.955, "unknown reuse warning bound: 0.955"),
            (0.58, "unknown reuse warning bound: 0.58"),
            (-15, "unknown reuse warning bound: -15"),
            (-9999999999999, "unknown reuse warning bound: -9999999999999"),
            (0.00000000000001, "unknown reuse warning bound: 1e-14"),
            (0.9999999999999991, "unknown reuse warning bound: 0.9999999999999991"),
            (-10000000000000, "unknown reuse warning bound: -10000000000000"),
            (0.0625, "unknown reuse warning bound: 0.0625"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_further_ring_out_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (61, 45, 44, 45),
            (62, 46, 45, 46),
            (63, 47, 46, 47),
            (67, 50, 49, 50),
            (100010, 75007, 75006, 75007),
            (1000009, 750006, 750005, 750006),
            (10000008, 7500006, 7500005, 7500006),
            (100000000000000, 75000000000000, 74999999999999, 75000000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_outermost_ring_out_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.945, "unknown reuse warning bound: 0.945"),
            (0.52, "unknown reuse warning bound: 0.52"),
            (-16, "unknown reuse warning bound: -16"),
            (-99999999999999, "unknown reuse warning bound: -99999999999999"),
            (0.000000000000001, "unknown reuse warning bound: 1e-15"),
            (0.999999999999998, "unknown reuse warning bound: 0.999999999999998"),
            (-100000000000000, "unknown reuse warning bound: -100000000000000"),
            (0.03125, "unknown reuse warning bound: 0.03125"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_outermost_ring_out_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (68, 51, 50, 51),
            (69, 51, 50, 51),
            (70, 52, 51, 52),
            (71, 53, 52, 53),
            (100011, 75008, 75007, 75008),
            (1000010, 750007, 750006, 750007),
            (10000009, 7500006, 7500005, 7500006),
            (1000000000000000, 750000000000000, 749999999999999, 750000000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_next_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.94, "unknown reuse warning bound: 0.94"),
            (0.51, "unknown reuse warning bound: 0.51"),
            (-17, "unknown reuse warning bound: -17"),
            (-999999999999999, "unknown reuse warning bound: -999999999999999"),
            (0.0000000000000001, "unknown reuse warning bound: 1e-16"),
            (0.999999999999997, "unknown reuse warning bound: 0.999999999999997"),
            (-1000000000000000, "unknown reuse warning bound: -1000000000000000"),
            (0.015625, "unknown reuse warning bound: 0.015625"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_next_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (72, 54, 53, 54),
            (73, 54, 53, 54),
            (74, 55, 54, 55),
            (76, 57, 56, 57),
            (100012, 75009, 75008, 75009),
            (1000011, 750008, 750007, 750008),
            (10000010, 7500007, 7500006, 7500007),
            (10000000000000000, 7500000000000000, 7499999999999999, 7500000000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_second_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.93, "unknown reuse warning bound: 0.93"),
            (0.49, "unknown reuse warning bound: 0.49"),
            (-18, "unknown reuse warning bound: -18"),
            (-9999999999999999, "unknown reuse warning bound: -9999999999999999"),
            (0.00000000000000001, "unknown reuse warning bound: 1e-17"),
            (0.999999999999996, "unknown reuse warning bound: 0.999999999999996"),
            (-10000000000000000, "unknown reuse warning bound: -10000000000000000"),
            (0.0078125, "unknown reuse warning bound: 0.0078125"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_second_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (77, 57, 56, 57),
            (78, 58, 57, 58),
            (79, 59, 58, 59),
            (81, 60, 59, 60),
            (100013, 75009, 75008, 75009),
            (1000012, 750009, 750008, 750009),
            (10000011, 7500008, 7500007, 7500008),
            (100000000000000000, 75000000000000000, 74999999999999999, 75000000000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_third_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.92, "unknown reuse warning bound: 0.92"),
            (0.48, "unknown reuse warning bound: 0.48"),
            (-19, "unknown reuse warning bound: -19"),
            (-99999999999999999, "unknown reuse warning bound: -99999999999999999"),
            (0.000000000000000001, "unknown reuse warning bound: 1e-18"),
            (0.999999999999995, "unknown reuse warning bound: 0.999999999999995"),
            (-100000000000000000, "unknown reuse warning bound: -100000000000000000"),
            (0.00390625, "unknown reuse warning bound: 0.00390625"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_third_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (82, 61, 60, 61),
            (83, 62, 61, 62),
            (84, 63, 62, 63),
            (86, 64, 63, 64),
            (100014, 75010, 75009, 75010),
            (1000013, 750009, 750008, 750009),
            (10000012, 7500009, 7500008, 7500009),
            (1000000000000000000, 750000000000000000, 749999999999999999, 750000000000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_fourth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.91, "unknown reuse warning bound: 0.91"),
            (0.47, "unknown reuse warning bound: 0.47"),
            (-20, "unknown reuse warning bound: -20"),
            (-999999999999999999, "unknown reuse warning bound: -999999999999999999"),
            (0.0000000000000000001, "unknown reuse warning bound: 1e-19"),
            (0.999999999999994, "unknown reuse warning bound: 0.999999999999994"),
            (-1000000000000000000, "unknown reuse warning bound: -1000000000000000000"),
            (0.001953125, "unknown reuse warning bound: 0.001953125"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_fourth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (87, 65, 64, 65),
            (88, 66, 65, 66),
            (89, 66, 65, 66),
            (91, 68, 67, 68),
            (100015, 75011, 75010, 75011),
            (1000014, 750010, 750009, 750010),
            (10000013, 7500009, 7500008, 7500009),
            (10000000000000000000, 7500000000000000000, 7499999999999999999, 7500000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_fifth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.89, "unknown reuse warning bound: 0.89"),
            (0.31, "unknown reuse warning bound: 0.31"),
            (-23, "unknown reuse warning bound: -23"),
            (-123456789012345678, "unknown reuse warning bound: -123456789012345678"),
            (0.0000000000000000002, "unknown reuse warning bound: 2e-19"),
            (0.9999995, "unknown reuse warning bound: 0.9999995"),
            (-999999998, "unknown reuse warning bound: -999999998"),
            (0.001953124, "unknown reuse warning bound: 0.001953124"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_fifth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (92, 69, 68, 69),
            (93, 69, 68, 69),
            (95, 71, 70, 71),
            (97, 72, 71, 72),
            (200015, 150011, 150010, 150011),
            (2000014, 1500010, 1500009, 1500010),
            (20000013, 15000009, 15000008, 15000009),
            (100000000000000000000, 75000000000000000000, 74999999999999999999, 75000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_sixth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.87, "unknown reuse warning bound: 0.87"),
            (0.29, "unknown reuse warning bound: 0.29"),
            (-29, "unknown reuse warning bound: -29"),
            (-987654321098765432, "unknown reuse warning bound: -987654321098765432"),
            (0.00000000000000000005, "unknown reuse warning bound: 5e-20"),
            (0.9999993, "unknown reuse warning bound: 0.9999993"),
            (-888888887, "unknown reuse warning bound: -888888887"),
            (0.0009765623, "unknown reuse warning bound: 0.0009765623"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_sixth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (113, 84, 83, 84),
            (117, 87, 86, 87),
            (119, 89, 88, 89),
            (123, 92, 91, 92),
            (400015, 300011, 300010, 300011),
            (4000014, 3000010, 3000009, 3000010),
            (40000013, 30000009, 30000008, 30000009),
            (300000000000000000000, 225000000000000000000, 224999999999999999999, 225000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_seventh_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.86, "unknown reuse warning bound: 0.86"),
            (0.33, "unknown reuse warning bound: 0.33"),
            (-31, "unknown reuse warning bound: -31"),
            (-777777777, "unknown reuse warning bound: -777777777"),
            (0.000000000000000000005, "unknown reuse warning bound: 5e-21"),
            (0.9999992, "unknown reuse warning bound: 0.9999992"),
            (-555555553, "unknown reuse warning bound: -555555553"),
            (0.0004882813, "unknown reuse warning bound: 0.0004882813"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_seventh_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (127, 95, 94, 95),
            (131, 98, 97, 98),
            (137, 102, 101, 102),
            (141, 105, 104, 105),
            (500021, 375015, 375014, 375015),
            (5000017, 3750012, 3750011, 3750012),
            (50000019, 37500014, 37500013, 37500014),
            (7000000000000000000000, 5250000000000000000000, 5249999999999999999999, 5250000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_eighth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.71, "unknown reuse warning bound: 0.71"),
            (0.625, "unknown reuse warning bound: 0.625"),
            (-47, "unknown reuse warning bound: -47"),
            (-888888888, "unknown reuse warning bound: -888888888"),
            (1e-22, "unknown reuse warning bound: 1e-22"),
            (0.9999996, "unknown reuse warning bound: 0.9999996"),
            (-444444441, "unknown reuse warning bound: -444444441"),
            (0.000244140625, "unknown reuse warning bound: 0.000244140625"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_eighth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (149, 111, 110, 111),
            (157, 117, 116, 117),
            (163, 122, 121, 122),
            (173, 129, 128, 129),
            (600011, 450008, 450007, 450008),
            (6000013, 4500009, 4500008, 4500009),
            (60000023, 45000017, 45000016, 45000017),
            (8000000000000000000000, 6000000000000000000000, 5999999999999999999999, 6000000000000000000000),
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

    def test_refusal_at_domain_bounds_beyond_the_ninth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.53, "unknown reuse warning bound: 0.53"),
            (0.375, "unknown reuse warning bound: 0.375"),
            (-63, "unknown reuse warning bound: -63"),
            (-777777776, "unknown reuse warning bound: -777777776"),
            (1e-23, "unknown reuse warning bound: 1e-23"),
            (0.9999991, "unknown reuse warning bound: 0.9999991"),
            (-333333331, "unknown reuse warning bound: -333333331"),
            (0.0001220703125, "unknown reuse warning bound: 0.0001220703125"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_ninth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (181, 135, 134, 135),
            (191, 143, 142, 143),
            (199, 149, 148, 149),
            (211, 158, 157, 158),
            (700011, 525008, 525007, 525008),
            (7000013, 5250009, 5250008, 5250009),
            (70000027, 52500020, 52500019, 52500020),
            (9000000000000000000000, 6750000000000000000000, 6749999999999999999999, 6750000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_tenth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.41, "unknown reuse warning bound: 0.41"),
            (0.3125, "unknown reuse warning bound: 0.3125"),
            (-71, "unknown reuse warning bound: -71"),
            (-666666665, "unknown reuse warning bound: -666666665"),
            (1e-24, "unknown reuse warning bound: 1e-24"),
            (0.9999989, "unknown reuse warning bound: 0.9999989"),
            (-222222221, "unknown reuse warning bound: -222222221"),
            (0.00006103515625, "unknown reuse warning bound: 6.103515625e-05"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_tenth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (223, 167, 166, 167),
            (239, 179, 178, 179),
            (251, 188, 187, 188),
            (263, 197, 196, 197),
            (800011, 600008, 600007, 600008),
            (8000013, 6000009, 6000008, 6000009),
            (80000029, 60000021, 60000020, 60000021),
            (10000000000000000000000, 7500000000000000000000, 7499999999999999999999, 7500000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_eleventh_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.21875, "unknown reuse warning bound: 0.21875"),
            (0.15625, "unknown reuse warning bound: 0.15625"),
            (-83, "unknown reuse warning bound: -83"),
            (-555555554, "unknown reuse warning bound: -555555554"),
            (1e-25, "unknown reuse warning bound: 1e-25"),
            (0.9999987, "unknown reuse warning bound: 0.9999987"),
            (-111111110, "unknown reuse warning bound: -111111110"),
            (0.000030517578125, "unknown reuse warning bound: 3.0517578125e-05"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_eleventh_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (272, 204, 203, 204),
            (288, 216, 215, 216),
            (312, 234, 233, 234),
            (336, 252, 251, 252),
            (900012, 675009, 675008, 675009),
            (9000016, 6750012, 6750011, 6750012),
            (90000032, 67500024, 67500023, 67500024),
            (12000000000000000000000, 9000000000000000000000, 8999999999999999999999, 9000000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_twelfth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.109375, "unknown reuse warning bound: 0.109375"),
            (0.078125, "unknown reuse warning bound: 0.078125"),
            (-97, "unknown reuse warning bound: -97"),
            (-444444443, "unknown reuse warning bound: -444444443"),
            (1e-26, "unknown reuse warning bound: 1e-26"),
            (0.9999985, "unknown reuse warning bound: 0.9999985"),
            (-666666664, "unknown reuse warning bound: -666666664"),
            (0.0000152587890625, "unknown reuse warning bound: 1.52587890625e-05"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_twelfth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (352, 264, 263, 264),
            (376, 282, 281, 282),
            (408, 306, 305, 306),
            (440, 330, 329, 330),
            (1000020, 750015, 750014, 750015),
            (1000016, 750012, 750011, 750012),
            (10000036, 7500027, 7500026, 7500027),
            (14000000000000000000000, 10500000000000000000000, 10499999999999999999999, 10500000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_thirteenth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.0546875, "unknown reuse warning bound: 0.0546875"),
            (0.0390625, "unknown reuse warning bound: 0.0390625"),
            (-127, "unknown reuse warning bound: -127"),
            (-333333332, "unknown reuse warning bound: -333333332"),
            (1e-27, "unknown reuse warning bound: 1e-27"),
            (0.9999983, "unknown reuse warning bound: 0.9999983"),
            (-777777773, "unknown reuse warning bound: -777777773"),
            (0.00000762939453125, "unknown reuse warning bound: 7.62939453125e-06"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_thirteenth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (472, 354, 353, 354),
            (504, 378, 377, 378),
            (544, 408, 407, 408),
            (584, 438, 437, 438),
            (1100020, 825015, 825014, 825015),
            (1100024, 825018, 825017, 825018),
            (11000040, 8250030, 8250029, 8250030),
            (16000000000000000000000, 12000000000000000000000, 11999999999999999999999, 12000000000000000000000),
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


    def test_refusal_at_domain_bounds_beyond_the_fourteenth_ring_beyond_outermost_values(self):
        module = require("ontoloop.promote")
        cases = [
            (0.02734375, "unknown reuse warning bound: 0.02734375"),
            (0.01953125, "unknown reuse warning bound: 0.01953125"),
            (-157, "unknown reuse warning bound: -157"),
            (-222222223, "unknown reuse warning bound: -222222223"),
            (1e-28, "unknown reuse warning bound: 1e-28"),
            (0.9999981, "unknown reuse warning bound: 0.9999981"),
            (-888888883, "unknown reuse warning bound: -888888883"),
            (0.000003814697265625, "unknown reuse warning bound: 3.814697265625e-06"),
        ]
        for bound, message in cases:
            with self.assertRaises(ValueError) as caught:
                module.reuse_warning_at_count(bound, bound=bound)
            self.assertEqual(str(caught.exception), message)

    def test_firing_at_domain_bounds_beyond_the_fourteenth_ring_beyond_outermost_bounds(self):
        module = require("ontoloop.promote")
        cases = [
            (624, 468, 467, 468),
            (664, 498, 497, 498),
            (712, 534, 533, 534),
            (760, 570, 569, 570),
            (1200020, 900015, 900014, 900015),
            (1200032, 900024, 900023, 900024),
            (12000044, 9000033, 9000032, 9000033),
            (18000000000000000000000, 13500000000000000000000, 13499999999999999999999, 13500000000000000000000),
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
        self.assertEqual(
            outcome["decision"],
            "whether the stale holdout material is reaffirmed "
            "or retired before the act in hand proceeds",
        )

    def test_firing_changes_no_bound_and_blocks_no_act(self):
        module = require("ontoloop.dataset")
        outcome = module.stale_warning_at_age(days=67.5, bound_days=90)
        self.assertEqual(outcome["bound_after_days"], 90)
        self.assertFalse(outcome["act_blocked"])

    def test_the_warning_fires_at_75_percent_of_bounds_other_than_90(self):
        module = require("ontoloop.dataset")
        cases = [
            (30, 22.5, 22.49),
            (7, 5.25, 5.24),
            (120, 90, 89.99),
            (365, 273.75, 273.74),
            (1, 0.75, 0.74),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])

    def test_the_warning_fires_at_75_percent_of_further_bounds(self):
        module = require("ontoloop.dataset")
        cases = [
            (45, 33.75, 33.74),
            (60, 45, 44.99),
            (14, 10.5, 10.49),
            (180, 135, 134.99),
            (2, 1.5, 1.49),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])

    def test_the_warning_fires_at_75_percent_of_still_further_bounds(self):
        module = require("ontoloop.dataset")
        cases = [
            (21, 15.75, 15.74),
            (28, 21, 20.99),
            (50, 37.5, 37.49),
            (75, 56.25, 56.24),
            (200, 150, 149.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_yet_further_bounds(self):
        module = require("ontoloop.dataset")
        cases = [
            (33, 24.75, 24.74),
            (40, 30, 29.99),
            (64, 48, 47.99),
            (150, 112.5, 112.49),
            (500, 375, 374.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])



    def test_the_warning_fires_at_75_percent_of_next_further_bounds(self):
        module = require("ontoloop.dataset")
        cases = [
            (17, 12.75, 12.74),
            (26, 19.5, 19.49),
            (55, 41.25, 41.24),
            (110, 82.5, 82.49),
            (300, 225, 224.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_still_next_further_bounds(self):
        module = require("ontoloop.dataset")
        cases = [
            (19, 14.25, 14.24),
            (34, 25.5, 25.49),
            (72, 54.0, 53.99),
            (140, 105.0, 104.99),
            (420, 315.0, 314.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_bounds_past_still_next_further(self):
        module = require("ontoloop.dataset")
        cases = [
            (23, 17.25, 17.24),
            (41, 30.75, 30.74),
            (88, 66.0, 65.99),
            (160, 120.0, 119.99),
            (640, 480.0, 479.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])

    def test_the_warning_fires_at_75_percent_of_bounds_beyond_past_still_next_further(self):
        module = require("ontoloop.dataset")
        cases = [
            (29, 21.75, 21.74),
            (47, 35.25, 35.24),
            (96, 72.0, 71.99),
            (175, 131.25, 131.24),
            (700, 525.0, 524.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_still_further_bounds_beyond_past_still_next_further(self):
        module = require("ontoloop.dataset")
        cases = [
            (31, 23.25, 23.24),
            (53, 39.75, 39.74),
            (104, 78.0, 77.99),
            (190, 142.5, 142.49),
            (750, 562.5, 562.49),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_further_bounds_beyond_past_still_next_further_still_next(self):
        module = require("ontoloop.dataset")
        cases = [
            (37, 27.75, 27.74),
            (61, 45.75, 45.74),
            (122, 91.5, 91.49),
            (215, 161.25, 161.24),
            (800, 600.0, 599.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_bounds_beyond_past_still_next_further_still_next_further(self):
        module = require("ontoloop.dataset")
        cases = [
            (43, 32.25, 32.24),
            (67, 50.25, 50.24),
            (133, 99.75, 99.74),
            (240, 180.0, 179.99),
            (900, 675.0, 674.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_bounds_beyond_past_still_next_further_still_next_further_next(self):
        module = require("ontoloop.dataset")
        cases = [
            (49, 36.75, 36.74),
            (73, 54.75, 54.74),
            (149, 111.75, 111.74),
            (260, 195.0, 194.99),
            (950, 712.5, 712.49),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


    def test_the_warning_fires_at_75_percent_of_bounds_beyond_past_still_next_further_still_next_further_next_next(self):
        module = require("ontoloop.dataset")
        cases = [
            (57, 42.75, 42.74),
            (83, 62.25, 62.24),
            (167, 125.25, 125.24),
            (290, 217.5, 217.49),
            (1000, 750.0, 749.99),
        ]
        for bound, point, below in cases:
            under = module.stale_warning_at_age(
                days=below, bound_days=bound)
            self.assertFalse(under["fired"])
            over = module.stale_warning_at_age(
                days=point, bound_days=bound)
            self.assertTrue(over["fired"])
            self.assertEqual(over["firing_point_fraction"], 0.75)
            self.assertEqual(over["bound_after_days"], bound)
            self.assertFalse(over["act_blocked"])


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

    def test_the_figure_value_counts_from_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record(
            attempt_count=5, standard_error=2.0)
        figure = record["figures"][self.FIGURE]
        expected_maximum = NormalDist().inv_cdf((5 - 0.375) / (5 + 0.25))
        self.assertEqual(figure["attempt_count_charged"], 5)
        self.assertEqual(figure["standard_error"], 2.0)
        self.assertEqual(figure["expected_maximum"], expected_maximum)
        self.assertEqual(figure["value"], expected_maximum * 2.0)

    def test_the_figure_value_counts_from_further_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (6, 2.0),
            (10, 3.0),
            (1, 0.5),
            (100, 1.0),
            (2, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_even_further_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (8, 1.25),
            (9, 0.5),
            (15, 2.0),
            (30, 1.5),
            (200, 0.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_still_further_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (3, 1.0),
            (7, 2.5),
            (20, 0.75),
            (50, 4.0),
            (4, 0.25),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_yet_further_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (11, 1.0),
            (12, 3.0),
            (25, 1.25),
            (40, 2.0),
            (150, 0.75),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_next_further_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (13, 1.0),
            (18, 2.5),
            (35, 0.5),
            (60, 1.5),
            (120, 2.0),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_still_next_inputs_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (14, 1.0),
            (22, 2.0),
            (45, 0.75),
            (80, 1.25),
            (250, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_past_still_next_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (16, 1.0),
            (28, 2.0),
            (55, 0.75),
            (95, 1.25),
            (300, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_beyond_past_still_next_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (19, 1.0),
            (32, 2.0),
            (65, 0.75),
            (110, 1.25),
            (350, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_beyond_past_still_next_further_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (23, 1.0),
            (38, 2.0),
            (78, 0.75),
            (130, 1.25),
            (420, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_beyond_past_still_next_further_next_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (27, 1.0),
            (44, 2.0),
            (92, 0.75),
            (155, 1.25),
            (500, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_beyond_past_still_next_further_next_further_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (31, 1.0),
            (52, 2.0),
            (108, 0.75),
            (180, 1.25),
            (600, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_beyond_past_still_next_further_next_further_next_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (36, 1.0),
            (61, 2.0),
            (125, 0.75),
            (210, 1.25),
            (700, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_value_counts_from_inputs_beyond_past_still_next_further_next_further_next_next_passed_in(self):
        from statistics import NormalDist
        module = require("ontoloop.eval")
        cases = [
            (42, 1.0),
            (73, 2.0),
            (145, 0.75),
            (245, 1.25),
            (820, 1.5),
        ]
        for attempt_count, standard_error in cases:
            record = module.closing_evaluation_record(
                attempt_count=attempt_count,
                standard_error=standard_error)
            figure = record["figures"][self.FIGURE]
            expected_maximum = NormalDist().inv_cdf(
                (attempt_count - 0.375) / (attempt_count + 0.25))
            self.assertEqual(
                figure["attempt_count_charged"], attempt_count)
            self.assertEqual(figure["standard_error"], standard_error)
            self.assertEqual(
                figure["expected_maximum"], expected_maximum)
            self.assertEqual(
                figure["value"], expected_maximum * standard_error)

    def test_the_figure_enters_no_comparison_in_the_evaluation(self):
        module = require("ontoloop.eval")
        record = module.closing_evaluation_record()
        self.assertNotIn(self.FIGURE, record["comparisons"])


if __name__ == "__main__":
    unittest.main()
