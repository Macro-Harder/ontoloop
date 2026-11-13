"""Unrowed F-C2 obligations, seat A: plan subsections 19.5 and 19.6.

These tests carry no row identifier. The plan states no identifier
for either obligation, and none is invented here. Each test is
homed at its plan subsection and counted in the suite manifest
under that subsection, under the F-C2 ruling at section 5 of
design/steps/step-13-content-retrace.md.
"""

import unittest

try:
    from tests.harness import require, stage_carried
except ImportError:
    from harness import require, stage_carried


# ------------------------------------------------------------------
# Transcription decision, subsection 19.5
#
# Subsection: plan subsection 19.5, the incident entry point and
# the incident loading stop.
#
# Obligation as the subsection states it: one OPS test row added
# at plan section 6.5, covering the three questions asked and
# recorded in order at incident entry (first whether sealed or
# secret material is involved, second whether the store is
# suspect, third whether a bundle is wrongly loadable, all three
# asked and recorded even where an earlier answer is yes), the
# consequence of a yes at each question, the recorder first rule
# (where a discrepancy is disputed, the journal is reconstructed
# and read before any recollection is relied on), the joint
# precedence of repair verification over purge and stop appends,
# and the incident loading stop taking effect on loading before
# its journal record lands.
#
# Transcription choice: written as one suite case,
# TestUnrowed195IncidentEntryPoint, with one test method per
# limb of the obligation, against the product surface the suite
# names ontoloop.ops. The exact question order and the exact
# precedence order are asserted as ordered tuples, because this
# seat prizes exact value forms. The consequence of a yes at each
# question is asserted at its brief passage value: a yes at the
# first question opens the redaction miss and purge path, a yes
# at the second takes the suspect path with evaluation and
# promotion refused until it clears, and a yes at the third stops
# the bundle loading at the next run boundary. The entry point
# record home is the incident record. The loading stop limbs are
# asserted in full: recorded on the operator surface at the
# moment it is taken, effect at the next run boundary, and its
# record written into the journal when the journal next accepts
# an append. Counted in the manifest under subsection 19.5,
# under no row identifier.
# ------------------------------------------------------------------


class TestUnrowed195IncidentEntryPoint(unittest.TestCase):
    """Subsection 19.5: the incident entry point, in full."""

    QUESTIONS_IN_ORDER = (
        "sealed or secret material involved",
        "store suspect",
        "bundle wrongly loadable",
    )

    EXPECTED_CONSEQUENCES = {
        "sealed or secret material involved": (
            "redaction miss and purge path"
        ),
        "store suspect": (
            "suspect path, evaluation and promotion refused"
        ),
        "bundle wrongly loadable": (
            "bundle loading stopped at the next run boundary"
        ),
    }

    def test_three_questions_asked_and_recorded_in_order(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("no", "no", "no"))
        self.assertEqual(tuple(record["questions"]), self.QUESTIONS_IN_ORDER)
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(len(record["answers"]), 3)

    def test_all_three_recorded_even_where_an_earlier_answer_is_yes(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("yes", "no", "no"))
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(record["answers"]["sealed or secret material involved"],
                         "yes")

    def test_consequence_of_a_yes_at_each_question(self):
        module = require("ontoloop.ops")
        for question in self.QUESTIONS_IN_ORDER:
            answers = tuple(
                "yes" if item == question else "no"
                for item in self.QUESTIONS_IN_ORDER
            )
            record = module.incident_entry(answers=answers)
            self.assertIn(question, record["consequences"])
            self.assertEqual(
                record["consequences"][question],
                self.EXPECTED_CONSEQUENCES[question],
            )

    def test_entry_point_record_stands_in_the_incident_record(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("no", "no", "no"))
        self.assertEqual(record["record_home"], "incident record")

    def test_recorder_first_rule(self):
        module = require("ontoloop.ops")
        result = module.resolve_dispute(disputed=True)
        self.assertEqual(result["first_act"], "journal reconstruction")
        self.assertIs(result["recollection_relied_on"], False)

    def test_joint_precedence_of_repair_verification(self):
        module = require("ontoloop.ops")
        order = module.incident_append_order()
        self.assertEqual(
            tuple(order),
            ("repair verification", "purge append", "stop append"),
        )

    def test_loading_stop_takes_effect_before_its_journal_record(self):
        module = require("ontoloop.ops")
        stop = module.take_loading_stop()
        self.assertIs(stop["effective_on_loading"], True)
        self.assertIs(stop["journal_record_landed"], False)
        discovery = module.discovery_after_stop(stop)
        self.assertEqual(discovery["promotion"], None)

    def test_loading_stop_record_boundary_and_journal_landing(self):
        module = require("ontoloop.ops")
        stop = module.take_loading_stop()
        self.assertEqual(stop["recorded_on"], "operator surface")
        self.assertEqual(stop["effective_at"], "next run boundary")
        self.assertIs(stop["journal_record_landed"], False)
        landed = module.journal_record_after_append(stop)
        self.assertIs(landed["journal_record_landed"], True)


# ------------------------------------------------------------------
# Transcription decision, subsection 19.6
#
# Subsection: plan subsection 19.6, the holdout freshness
# lifecycle acts.
#
# Obligation as the subsection states it: three test rows added
# at plan section 6.5, one for the freshness check at each of its
# three points, dataset build, evaluation start, and promotion,
# covering the stale flag, the exclusion of stale material, the
# reaffirmation, the retirement transition with its replacement
# first condition, and the supersession refusal.
#
# Transcription choice: written as three suite cases, one per
# check point, TestUnrowed196DatasetBuild,
# TestUnrowed196EvaluationStart, and TestUnrowed196Promotion,
# each with one test method per limb of the obligation, against
# the product surface the suite names ontoloop.dataset, the
# DATASET slice owning the freshness clock, the stale flag, and
# the lifecycle transitions under the subsection. The subsection
# names two record homes at its clause five: a reaffirmation is
# recorded on the dataset record of the dataset version it
# reaffirms for, while retirement transitions, the Retired
# transition of unspent sealed material at supersession or
# withdrawal, and the stale flag and its clearing stand on the
# holdout lifecycle record. Both homes are asserted in those
# terms. Counted in the manifest under subsection 19.6, under no
# row identifier.
# ------------------------------------------------------------------


class _FreshnessCheckPoint:
    """Shared limbs for one freshness check point."""

    CHECK_POINT = None
    MODULE = "ontoloop.dataset"

    def _fresh(self):
        module = require(self.MODULE)
        return module.freshness_check(self.CHECK_POINT)

    def test_stale_flag_stands_on_the_lifecycle_record(self):
        check = self._fresh()
        record = check["lifecycle_record"]
        self.assertIn("stale_flag", record)
        self.assertIn("stale_flag_cleared", record)

    def test_stale_material_is_excluded_from_the_act_in_hand(self):
        check = self._fresh()
        stale = check["stale_material"]
        self.assertTrue(stale)
        included = check["included_material"]
        self.assertEqual(set(stale) & set(included), set())

    def test_reaffirmation_restores_inclusion(self):
        module = require(self.MODULE)
        result = module.reaffirm(self.CHECK_POINT)
        self.assertIn("reaffirmation", result["dataset_record"])
        self.assertTrue(result["dataset_record"]["reaffirmation"])
        self.assertIs(result["lifecycle_record"]["stale_flag_cleared"], True)
        stale = set(result["stale_material"])
        included = set(result["included_material"])
        self.assertTrue(stale <= included or not stale)

    def test_unspent_sealed_material_retires_at_supersession_or_withdrawal(self):
        module = require(self.MODULE)
        for occasion in ("supersession", "withdrawal"):
            result = module.retire_unspent_sealed(
                self.CHECK_POINT, occasion=occasion
            )
            self.assertEqual(
                result["lifecycle_record"]["transition"], "Retired"
            )
            self.assertTrue(
                result["lifecycle_record"]["unspent_sealed_material"]
            )

    def test_retirement_only_after_a_replacement_has_sealed(self):
        module = require(self.MODULE)
        refused = module.retire(self.CHECK_POINT, replacement_sealed=False)
        self.assertIs(refused["accepted"], False)
        allowed = module.retire(self.CHECK_POINT, replacement_sealed=True)
        self.assertIs(allowed["accepted"], True)
        self.assertEqual(
            allowed["lifecycle_record"]["transition"], "Retired"
        )

    def test_promotion_from_a_superseded_version_is_refused(self):
        module = require(self.MODULE)
        result = module.supersession_refusal(self.CHECK_POINT)
        self.assertIs(result["accepted"], False)
        named = module.error_catalogue()["superseded version"]["error"]
        self.assertEqual(result["error"], named)
        self.assertIn("superseded", result["error"])


class TestUnrowed196DatasetBuild(_FreshnessCheckPoint, unittest.TestCase):
    """Subsection 19.6: freshness check at dataset build."""

    CHECK_POINT = "dataset build"


class TestUnrowed196EvaluationStart(_FreshnessCheckPoint, unittest.TestCase):
    """Subsection 19.6: freshness check at evaluation start."""

    CHECK_POINT = "evaluation start"


class TestUnrowed196Promotion(_FreshnessCheckPoint, unittest.TestCase):
    """Subsection 19.6: freshness check at promotion."""

    CHECK_POINT = "promotion"


if __name__ == "__main__":
    unittest.main()
