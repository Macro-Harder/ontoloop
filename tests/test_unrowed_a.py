"""Unrowed F-C2 obligations, seat A: plan subsections 19.5 and 19.6.

These tests carry no row identifier. The plan states no identifier
for either obligation, and none is invented here. Each test is
homed at its plan subsection and counted in the suite manifest
under that subsection, under the F-C2 ruling at section 5 of
design/steps/step-13-content-retrace.md.
"""

import unittest

from tests.harness import require, stage_carried


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
# names ontoloop.ops. The question order is asserted as an
# ordered tuple, because the subsection states the three
# questions in order. The precedence form stands relaxed under
# the Step 15 Round 1 triage ruling for UA-L1: the subsection
# states only that repair verification precedes each of the
# purge append and the stop append, and states no order between
# those two appends, so the precedence test asserts that
# partial order and no more. The consequence of a yes at each
# question is asserted only in the limbs the subsection
# states: a consequence stands recorded for the question
# answered yes, and the bundle consequence carries the next
# run boundary form the subsection states for the loading
# stop. The exact consequence strings of the brief passage,
# which the subsection incorporates by reference and does not
# reproduce, stand unpinned. The entry point
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

    def test_three_questions_asked_and_recorded_in_order(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("no", "no", "no"))
        self.assertEqual(tuple(record["questions"]), self.QUESTIONS_IN_ORDER)
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(len(record["answers"]), 3)
        self.assertEqual(record["answers"], {
            "sealed or secret material involved": "no",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })

    def test_all_three_recorded_even_where_an_earlier_answer_is_yes(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("yes", "no", "no"))
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(record["answers"]["sealed or secret material involved"],
                         "yes")
        self.assertEqual(record["answers"]["store suspect"], "no")
        self.assertEqual(record["answers"]["bundle wrongly loadable"], "no")
        self.assertEqual(record["answers"], {
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })

    def test_answers_presented_as_a_mapping_stand_recorded_in_question_order(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers={
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(record["answers"], {
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })
        self.assertIn(
            "sealed or secret material involved", record["consequences"])

    def test_undisputed_form_stands_in_its_governed_form(self):
        module = require("ontoloop.ops")
        result = module.resolve_dispute(disputed=False)
        self.assertIsNone(result["first_act"])
        self.assertIs(result["recollection_relied_on"], False)
        self.assertIs(result["journal_reconstructed"], False)
        self.assertIs(result["journal_read"], False)
        self.assertEqual(result["reconstructed_material"], [])
        self.assertEqual(result["material_read"], [])
        with_records = module.resolve_dispute(
            disputed=False,
            journal_records=["journal record one", "journal record two"])
        self.assertEqual(with_records["reconstructed_material"], [])
        self.assertEqual(with_records["material_read"], [])

    def test_consequence_of_a_yes_at_each_question(self):
        module = require("ontoloop.ops")
        for question in self.QUESTIONS_IN_ORDER:
            answers = tuple(
                "yes" if item == question else "no"
                for item in self.QUESTIONS_IN_ORDER
            )
            record = module.incident_entry(answers=answers)
            self.assertIn(question, record["consequences"])
            consequence = record["consequences"][question]
            self.assertIsInstance(consequence, str)
            self.assertTrue(consequence)
            for other in self.QUESTIONS_IN_ORDER:
                if other != question:
                    self.assertNotIn(other, record["consequences"])
        record = module.incident_entry(
            answers=("no", "no", "yes"))
        self.assertIn(
            "next run boundary",
            record["consequences"]["bundle wrongly loadable"],
        )

    def test_no_answers_and_none_answers_stand_as_three_no_answers(self):
        module = require("ontoloop.ops")
        for record in (module.incident_entry(),
                       module.incident_entry(answers=None)):
            self.assertEqual(tuple(record["questions"]),
                             self.QUESTIONS_IN_ORDER)
            self.assertEqual(record["answers"], {
                "sealed or secret material involved": "no",
                "store suspect": "no",
                "bundle wrongly loadable": "no",
            })
            self.assertEqual(record["consequences"], {})

    def test_refused_answer_forms_raise_value_error(self):
        module = require("ontoloop.ops")
        refused_forms = (
            (("maybe", "no", "no"), "each answer must be yes or no"),
            (("yes", "no"), "answers must hold three answers"),
            (("yes", "no", "no", "no"), "answers must hold three answers"),
            ({"sealed or secret material involved": "yes"},
             "answers lacks the question: 'store suspect'"),
        )
        for answers, message in refused_forms:
            with self.assertRaises(ValueError, msg=repr(answers)) as caught:
                module.incident_entry(answers=answers)
            self.assertEqual(str(caught.exception), message)

    def test_answers_presented_as_a_list_stand_recorded_in_question_order(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=["yes", "no", "no"])
        self.assertEqual(tuple(record["questions"]),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(record["answers"], {
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })

    def test_answers_value_in_no_governed_form_raises_value_error(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError):
            module.incident_entry(answers="yes")

    def test_entry_point_record_stands_in_the_incident_record(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("no", "no", "no"))
        self.assertEqual(record["record_home"], "incident record")

    def test_recorder_first_rule(self):
        module = require("ontoloop.ops")
        result = module.resolve_dispute(disputed=True)
        self.assertEqual(result["first_act"], "journal reconstruction")
        self.assertIs(result["recollection_relied_on"], False)
        self.assertIs(result["journal_reconstructed"], True)
        self.assertIs(result["journal_read"], True)
        self.assertEqual(result["reconstructed_material"], [])
        self.assertEqual(result["material_read"], [])
        records = ["journal record one", "journal record two"]
        read_result = module.resolve_dispute(
            disputed=True, journal_records=records)
        self.assertEqual(
            read_result["reconstructed_material"], records)
        self.assertEqual(read_result["material_read"], records)
        self.assertIs(read_result["journal_read"], True)
        self.assertIsNot(
            read_result["reconstructed_material"],
            read_result["material_read"])

    def test_recorder_first_rule_with_journal_records_as_a_tuple(self):
        module = require("ontoloop.ops")
        records = ("journal record one", "journal record two")
        result = module.resolve_dispute(
            disputed=True, journal_records=records)
        self.assertEqual(result["first_act"], "journal reconstruction")
        self.assertEqual(
            result["reconstructed_material"],
            ["journal record one", "journal record two"])
        self.assertEqual(
            result["material_read"],
            ["journal record one", "journal record two"])

    def test_loading_stop_stands_as_a_named_act(self):
        module = require("ontoloop.ops")
        self.assertIn("take_loading_stop", module.__all__)
        stop = module.take_loading_stop()
        self.assertEqual(stop["act"], "incident loading stop")
        self.assertIsNone(stop["bundle"])

    def test_joint_precedence_of_repair_verification(self):
        module = require("ontoloop.ops")
        order = list(module.incident_append_order())
        self.assertEqual(
            set(order),
            {"repair verification", "purge append", "stop append"},
        )
        self.assertLess(
            order.index("repair verification"),
            order.index("purge append"),
        )
        self.assertLess(
            order.index("repair verification"),
            order.index("stop append"),
        )
        swapped = list(module.incident_append_order(
            acts=("stop append", "purge append", "repair verification"),
        ))
        self.assertEqual(
            set(swapped),
            {"repair verification", "purge append", "stop append"},
        )
        self.assertLess(
            swapped.index("repair verification"),
            swapped.index("stop append"),
        )
        self.assertLess(
            swapped.index("repair verification"),
            swapped.index("purge append"),
        )
        self.assertLess(
            swapped.index("stop append"),
            swapped.index("purge append"),
        )
        reordered = list(module.incident_append_order(
            acts=("purge append", "stop append", "repair verification"),
        ))
        self.assertEqual(
            set(reordered),
            {"repair verification", "purge append", "stop append"},
        )
        self.assertLess(
            reordered.index("repair verification"),
            reordered.index("purge append"),
        )
        self.assertLess(
            reordered.index("repair verification"),
            reordered.index("stop append"),
        )
        self.assertLess(
            reordered.index("purge append"),
            reordered.index("stop append"),
        )

    def test_incident_append_order_unknown_act_raises_value_error(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError):
            module.incident_append_order(acts=("bogus act",))

    def test_incident_append_order_acts_presented_as_a_list(self):
        module = require("ontoloop.ops")
        order = list(module.incident_append_order(
            acts=["stop append", "purge append", "repair verification"]))
        self.assertEqual(
            set(order),
            {"repair verification", "purge append", "stop append"})
        self.assertLess(
            order.index("repair verification"),
            order.index("purge append"))
        self.assertLess(
            order.index("repair verification"),
            order.index("stop append"))

    def test_loading_stop_takes_effect_before_its_journal_record(self):
        module = require("ontoloop.ops")
        bundle = "named wrongly loadable bundle"
        stop = module.take_loading_stop(bundle=bundle)
        self.assertIs(stop["effective_on_loading"], True)
        self.assertIs(stop["journal_record_landed"], False)
        self.assertEqual(stop["bundle"], bundle)
        discovery = module.discovery_after_stop(stop, bundle=bundle)
        self.assertEqual(discovery["promotion"], None)
        self.assertEqual(discovery["bundle"], bundle)
        companion_stop = dict(stop)
        companion_stop["effective_on_loading"] = False
        companion = module.discovery_after_stop(
            companion_stop, bundle=bundle)
        self.assertEqual(companion["promotion"], bundle)
        self.assertEqual(companion["bundle"], bundle)
        differing = module.discovery_after_stop(
            stop, bundle="another bundle passed to the call")
        self.assertEqual(differing["bundle"], bundle)

    def test_loading_stop_record_boundary_and_journal_landing(self):
        module = require("ontoloop.ops")
        stop = module.take_loading_stop()
        self.assertEqual(stop["recorded_on"], "operator surface")
        self.assertEqual(stop["effective_at"], "next run boundary")
        self.assertIs(stop["journal_record_landed"], False)
        landed = module.journal_record_after_append(stop)
        self.assertIs(landed["journal_record_landed"], True)
        self.assertEqual(landed["stop"], stop)

    def test_loading_stop_journal_landing_with_a_store_passed(self):
        module = require("ontoloop.ops")
        stop = module.take_loading_stop(bundle="named bundle")
        landed = module.journal_record_after_append(stop, store={})
        self.assertIs(landed["journal_record_landed"], False)
        self.assertEqual(landed["stop"], stop)

    def test_loading_stop_journal_landing_with_an_appending_store(self):
        module = require("ontoloop.ops")
        store_module = require("ontoloop.store")
        stop = module.take_loading_stop(bundle="named bundle")
        landed = module.journal_record_after_append(
            stop, store=store_module.golden_record_store())
        self.assertIs(landed["journal_record_landed"], True)
        self.assertEqual(landed["stop"], stop)

    def test_loading_stop_journal_landing_records_the_append_content(self):
        module = require("ontoloop.ops")
        store_module = require("ontoloop.store")
        store = store_module.golden_record_store()
        stop = module.take_loading_stop(bundle="named bundle")
        landed = module.journal_record_after_append(stop, store=store)
        self.assertIs(landed["journal_record_landed"], True)
        self.assertEqual(landed["stop"], stop)
        content = store["records"][-1]["content"]
        self.assertEqual(content["act"], stop["act"])
        self.assertEqual(content["act"], "incident loading stop")
        self.assertEqual(content["recorded_on"], stop["recorded_on"])
        self.assertEqual(content["recorded_on"], "operator surface")
        self.assertEqual(content["effective_at"], stop["effective_at"])
        self.assertEqual(content["effective_at"], "next run boundary")
        self.assertEqual(content["bundle"], stop["bundle"])
        self.assertEqual(content["bundle"], "named bundle")


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
        self.assertEqual(check["check_point"], self.CHECK_POINT)
        record = check["lifecycle_record"]
        self.assertIn("stale_flag", record)
        self.assertIn("stale_flag_cleared", record)
        self.assertIs(record["stale_flag"], True)
        self.assertIs(record["stale_flag_cleared"], False)
        self.assertEqual(record["record_home"], "holdout lifecycle record")

    def test_stale_material_is_excluded_from_the_act_in_hand(self):
        check = self._fresh()
        stale = check["stale_material"]
        self.assertTrue(stale)
        included = check["included_material"]
        self.assertEqual(set(stale) & set(included), set())

    def test_reaffirmation_restores_inclusion(self):
        module = require(self.MODULE)
        before = module.freshness_check(self.CHECK_POINT)
        formerly_stale = set(before["stale_material"])
        self.assertTrue(formerly_stale)
        result = module.reaffirm(self.CHECK_POINT)
        self.assertEqual(result["check_point"], self.CHECK_POINT)
        self.assertIn("reaffirmation", result["dataset_record"])
        self.assertTrue(result["dataset_record"]["reaffirmation"])
        self.assertEqual(
            result["dataset_record"]["reaffirmation"]["actor"], "operator"
        )
        self.assertIs(result["lifecycle_record"]["stale_flag_cleared"], True)
        self.assertIs(result["lifecycle_record"]["stale_flag"], False)
        self.assertEqual(
            result["lifecycle_record"]["record_home"],
            "holdout lifecycle record")
        self.assertEqual(
            result["dataset_record"]["record_home"], "dataset record")
        self.assertEqual(
            set(result["stale_material"]), formerly_stale)
        self.assertEqual(result["reaffirming_actor"], "operator")
        self.assertEqual(
            result["dataset_record"]["reaffirmation"]["check_point"],
            self.CHECK_POINT)
        included = set(result["included_material"])
        self.assertTrue(formerly_stale <= included)

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
            self.assertEqual(
                result["lifecycle_record"]["record_home"],
                "holdout lifecycle record")
            self.assertEqual(result["occasion"], occasion)
            self.assertEqual(result["check_point"], self.CHECK_POINT)

    def test_retirement_only_after_a_replacement_has_sealed(self):
        module = require(self.MODULE)
        refused = module.retire(self.CHECK_POINT, replacement_sealed=False)
        self.assertEqual(refused["check_point"], self.CHECK_POINT)
        self.assertIs(refused["accepted"], False)
        self.assertIsNone(refused["lifecycle_record"]["transition"])
        self.assertEqual(
            refused["lifecycle_record"]["record_home"],
            "holdout lifecycle record")
        with_material = module.retire(
            self.CHECK_POINT,
            replacement_sealed=True,
            replacement_sealed_without_retiring_material=False,
        )
        self.assertIs(with_material["accepted"], False)
        allowed = module.retire(
            self.CHECK_POINT,
            replacement_sealed=True,
            replacement_sealed_without_retiring_material=True,
        )
        self.assertIs(allowed["accepted"], True)
        self.assertEqual(allowed["check_point"], self.CHECK_POINT)
        self.assertEqual(
            allowed["lifecycle_record"]["transition"], "Retired"
        )
        self.assertEqual(
            allowed["lifecycle_record"]["record_home"],
            "holdout lifecycle record")

    def test_promotion_from_a_superseded_version_is_refused(self):
        module = require(self.MODULE)
        result = module.supersession_refusal(self.CHECK_POINT)
        self.assertEqual(result["check_point"], self.CHECK_POINT)
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], "superseded version")
        self.assertIn("superseded", result["error"])


class TestUnrowed196UnknownCheckPoint(unittest.TestCase):
    """Subsection 19.6: an unknown check point stands refused."""

    def test_unknown_check_point_raises_value_error_on_each_surface(self):
        module = require("ontoloop.dataset")
        calls = (
            lambda: module.freshness_check("unknown point"),
            lambda: module.reaffirm("unknown point"),
            lambda: module.retire(
                "unknown point", replacement_sealed=False),
            lambda: module.retire_unspent_sealed(
                "unknown point", occasion="supersession"),
            lambda: module.supersession_refusal("unknown point"),
        )
        for call in calls:
            with self.assertRaises(ValueError) as caught:
                call()
            self.assertEqual(
                str(caught.exception),
                "unknown freshness check point: 'unknown point'")

    def test_unknown_retirement_occasion_raises_value_error(self):
        module = require("ontoloop.dataset")
        with self.assertRaises(ValueError):
            module.retire_unspent_sealed(
                "dataset build", occasion="bogus")


class TestUnrowed196DatasetBuild(_FreshnessCheckPoint, unittest.TestCase):
    """Subsection 19.6: freshness check at dataset build."""

    CHECK_POINT = "dataset build"


class TestUnrowed196EvaluationStart(_FreshnessCheckPoint, unittest.TestCase):
    """Subsection 19.6: freshness check at evaluation start."""

    CHECK_POINT = "evaluation start"


class TestUnrowed196Promotion(_FreshnessCheckPoint, unittest.TestCase):
    """Subsection 19.6: freshness check at promotion."""

    CHECK_POINT = "promotion"

    def test_freshness_check_at_promotion_delegates_to_the_dataset_home(self):
        promote = require("ontoloop.promote")
        dataset = require("ontoloop.dataset")
        result = promote.freshness_check_at_promotion()
        self.assertEqual(result, dataset.freshness_check("promotion"))
        self.assertEqual(result["check_point"], "promotion")


# ------------------------------------------------------------------
# Test act, subsection 19.35 point two, claim limit limb.
#
# Subsection 19.35 point two states that the low confidence stamp
# fires below 30 holdout groups, with a claim limit effect and no
# gate block. This pinning test stands in this file because the
# DAT fix seat owns this file; its natural home beside the stamp
# attachment tests in test_unrowed_b.py stands outside that
# ownership, and that position is recorded in the fix paper.
# No claim limit figure stands stated in the governing text, and
# none is pinned here: the test pins the effect standing present
# where the stamp attaches, absent where it does not, and no gate
# blocked in either case.
# ------------------------------------------------------------------


class TestUnrowed1935ClaimLimitDataset(unittest.TestCase):
    """Subsection 19.35 point two: low confidence claim limit."""

    def test_low_confidence_carries_a_claim_limit_and_no_gate_block(self):
        module = require("ontoloop.dataset")
        outcome = module.attach_stamps_at_build(holdout_groups=29)
        self.assertIn("low confidence", outcome["attached_stamps"])
        self.assertIs(outcome["claim_limit_effect"], True)
        self.assertIs(outcome["gate_blocked"], False)

    def test_no_claim_limit_effect_where_low_confidence_does_not_attach(self):
        module = require("ontoloop.dataset")
        outcome = module.attach_stamps_at_build(holdout_groups=30)
        self.assertNotIn("low confidence", outcome["attached_stamps"])
        self.assertIs(outcome["claim_limit_effect"], False)
        self.assertIs(outcome["gate_blocked"], False)


if __name__ == "__main__":
    unittest.main()
