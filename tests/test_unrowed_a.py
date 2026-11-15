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
        second = module.incident_entry(answers=("no", "no", "no"))
        self.assertIsNot(record["questions"], second["questions"])
        self.assertIsNot(record["answers"], second["answers"])
        self.assertIsNot(record["consequences"], second["consequences"])
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
        second_tuple_yes = module.incident_entry(
            answers=("yes", "no", "no"))
        self.assertIsNot(record, second_tuple_yes)
        self.assertIsNot(record["questions"], second_tuple_yes["questions"])
        self.assertIsNot(record["answers"], second_tuple_yes["answers"])
        self.assertIsNot(
            record["consequences"], second_tuple_yes["consequences"])
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

        second_question_yes = module.incident_entry(
            answers=("no", "yes", "no"))
        second_second_question_yes = module.incident_entry(
            answers=("no", "yes", "no"))
        self.assertIsNot(second_question_yes, second_second_question_yes)
        self.assertIsNot(
            second_question_yes["questions"],
            second_second_question_yes["questions"])
        self.assertIsNot(
            second_question_yes["answers"],
            second_second_question_yes["answers"])
        self.assertIsNot(
            second_question_yes["consequences"],
            second_second_question_yes["consequences"])
        third_question_yes = module.incident_entry(
            answers=("no", "no", "yes"))
        second_third_question_yes = module.incident_entry(
            answers=("no", "no", "yes"))
        self.assertIsNot(third_question_yes, second_third_question_yes)
        self.assertIsNot(
            third_question_yes["questions"],
            second_third_question_yes["questions"])
        self.assertIsNot(
            third_question_yes["answers"],
            second_third_question_yes["answers"])
        self.assertIsNot(
            third_question_yes["consequences"],
            second_third_question_yes["consequences"])

        all_yes_tuple = module.incident_entry(
            answers=("yes", "yes", "yes"))
        second_all_yes_tuple = module.incident_entry(
            answers=("yes", "yes", "yes"))
        self.assertIsNot(all_yes_tuple, second_all_yes_tuple)
        self.assertIsNot(
            all_yes_tuple["questions"], second_all_yes_tuple["questions"])
        self.assertIsNot(
            all_yes_tuple["answers"], second_all_yes_tuple["answers"])
        self.assertIsNot(
            all_yes_tuple["consequences"],
            second_all_yes_tuple["consequences"])

    def test_answers_presented_as_a_mapping_stand_recorded_in_question_order(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers={
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })
        second = module.incident_entry(answers={
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })
        self.assertIsNot(record["questions"], second["questions"])
        self.assertIsNot(record["answers"], second["answers"])
        self.assertIsNot(record["consequences"], second["consequences"])
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(record["answers"], {
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })
        self.assertIn(
            "sealed or secret material involved", record["consequences"])

        second_question_mapping = module.incident_entry(answers={
            "sealed or secret material involved": "no",
            "store suspect": "yes",
            "bundle wrongly loadable": "no",
        })
        second_second_question_mapping = module.incident_entry(answers={
            "sealed or secret material involved": "no",
            "store suspect": "yes",
            "bundle wrongly loadable": "no",
        })
        self.assertIsNot(
            second_question_mapping, second_second_question_mapping)
        self.assertIsNot(
            second_question_mapping["questions"],
            second_second_question_mapping["questions"])
        self.assertIsNot(
            second_question_mapping["answers"],
            second_second_question_mapping["answers"])
        self.assertIsNot(
            second_question_mapping["consequences"],
            second_second_question_mapping["consequences"])
        third_question_mapping = module.incident_entry(answers={
            "sealed or secret material involved": "no",
            "store suspect": "no",
            "bundle wrongly loadable": "yes",
        })
        second_third_question_mapping = module.incident_entry(answers={
            "sealed or secret material involved": "no",
            "store suspect": "no",
            "bundle wrongly loadable": "yes",
        })
        self.assertIsNot(
            third_question_mapping, second_third_question_mapping)
        self.assertIsNot(
            third_question_mapping["questions"],
            second_third_question_mapping["questions"])
        self.assertIsNot(
            third_question_mapping["answers"],
            second_third_question_mapping["answers"])
        self.assertIsNot(
            third_question_mapping["consequences"],
            second_third_question_mapping["consequences"])


    def test_undisputed_form_stands_in_its_governed_form(self):
        module = require("ontoloop.ops")
        result = module.resolve_dispute(disputed=False)
        second_result = module.resolve_dispute(disputed=False)
        self.assertIsNot(result, second_result)
        self.assertIsNot(
            result["reconstructed_material"],
            second_result["reconstructed_material"])
        self.assertIsNot(
            result["material_read"], second_result["material_read"])
        self.assertIsNone(result["first_act"])
        self.assertIs(result["recollection_relied_on"], False)
        self.assertIs(result["journal_reconstructed"], False)
        self.assertIs(result["journal_read"], False)
        self.assertEqual(result["reconstructed_material"], [])
        self.assertEqual(result["material_read"], [])
        self.assertIsNot(
            result["reconstructed_material"], result["material_read"])
        with_records = module.resolve_dispute(
            disputed=False,
            journal_records=["journal record one", "journal record two"])
        second_with_records = module.resolve_dispute(
            disputed=False,
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(with_records, second_with_records)
        self.assertIsNot(
            with_records["reconstructed_material"],
            second_with_records["reconstructed_material"])
        self.assertIsNot(
            with_records["material_read"],
            second_with_records["material_read"])
        self.assertEqual(with_records["reconstructed_material"], [])
        self.assertEqual(with_records["material_read"], [])
        self.assertIsNot(
            with_records["reconstructed_material"],
            with_records["material_read"])
        with_tuple_records = module.resolve_dispute(
            disputed=False,
            journal_records=("journal record one", "journal record two"))
        second_with_tuple_records = module.resolve_dispute(
            disputed=False,
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(with_tuple_records, second_with_tuple_records)
        self.assertIsNot(
            with_tuple_records["reconstructed_material"],
            second_with_tuple_records["reconstructed_material"])
        self.assertIsNot(
            with_tuple_records["material_read"],
            second_with_tuple_records["material_read"])
        self.assertIsNone(with_tuple_records["first_act"])
        self.assertIs(with_tuple_records["recollection_relied_on"], False)
        self.assertIs(with_tuple_records["journal_reconstructed"], False)
        self.assertIs(with_tuple_records["journal_read"], False)
        self.assertEqual(with_tuple_records["reconstructed_material"], [])
        self.assertEqual(with_tuple_records["material_read"], [])
        self.assertIsNot(
            with_tuple_records["reconstructed_material"],
            with_tuple_records["material_read"])
        falsy_result = module.resolve_dispute(
            disputed=0,
            journal_records=["journal record one", "journal record two"])
        second_falsy_result = module.resolve_dispute(
            disputed=0,
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(falsy_result, second_falsy_result)
        self.assertIsNot(
            falsy_result["reconstructed_material"],
            second_falsy_result["reconstructed_material"])
        self.assertIsNot(
            falsy_result["material_read"],
            second_falsy_result["material_read"])
        no_argument_result = module.resolve_dispute()
        second_no_argument_result = module.resolve_dispute()
        self.assertIsNot(no_argument_result, second_no_argument_result)
        self.assertIsNot(
            no_argument_result["reconstructed_material"],
            second_no_argument_result["reconstructed_material"])
        self.assertIsNot(
            no_argument_result["material_read"],
            second_no_argument_result["material_read"])


        none_records_result = module.resolve_dispute(
            disputed=False, journal_records=None)
        second_none_records_result = module.resolve_dispute(
            disputed=False, journal_records=None)
        self.assertIsNot(none_records_result, second_none_records_result)
        self.assertIsNot(
            none_records_result["reconstructed_material"],
            second_none_records_result["reconstructed_material"])
        self.assertIsNot(
            none_records_result["material_read"],
            second_none_records_result["material_read"])
        zero_tuple_result = module.resolve_dispute(
            disputed=0,
            journal_records=("journal record one", "journal record two"))
        second_zero_tuple_result = module.resolve_dispute(
            disputed=0,
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(zero_tuple_result, second_zero_tuple_result)
        self.assertIsNot(
            zero_tuple_result["reconstructed_material"],
            second_zero_tuple_result["reconstructed_material"])
        self.assertIsNot(
            zero_tuple_result["material_read"],
            second_zero_tuple_result["material_read"])
        zero_no_records_result = module.resolve_dispute(disputed=0)
        second_zero_no_records_result = module.resolve_dispute(disputed=0)
        self.assertIsNot(
            zero_no_records_result, second_zero_no_records_result)
        self.assertIsNot(
            zero_no_records_result["reconstructed_material"],
            second_zero_no_records_result["reconstructed_material"])
        self.assertIsNot(
            zero_no_records_result["material_read"],
            second_zero_no_records_result["material_read"])
        zero_none_records_result = module.resolve_dispute(
            disputed=0, journal_records=None)
        second_zero_none_records_result = module.resolve_dispute(
            disputed=0, journal_records=None)
        self.assertIsNot(
            zero_none_records_result, second_zero_none_records_result)
        self.assertIsNot(
            zero_none_records_result["reconstructed_material"],
            second_zero_none_records_result["reconstructed_material"])
        self.assertIsNot(
            zero_none_records_result["material_read"],
            second_zero_none_records_result["material_read"])
        none_disputed_result = module.resolve_dispute(
            disputed=None,
            journal_records=["journal record one", "journal record two"])
        second_none_disputed_result = module.resolve_dispute(
            disputed=None,
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(none_disputed_result, second_none_disputed_result)
        self.assertIsNot(
            none_disputed_result["reconstructed_material"],
            second_none_disputed_result["reconstructed_material"])
        self.assertIsNot(
            none_disputed_result["material_read"],
            second_none_disputed_result["material_read"])
        empty_disputed_result = module.resolve_dispute(
            disputed="",
            journal_records=["journal record one", "journal record two"])
        second_empty_disputed_result = module.resolve_dispute(
            disputed="",
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(empty_disputed_result, second_empty_disputed_result)
        self.assertIsNot(
            empty_disputed_result["reconstructed_material"],
            second_empty_disputed_result["reconstructed_material"])
        self.assertIsNot(
            empty_disputed_result["material_read"],
            second_empty_disputed_result["material_read"])
        ops_empty_result = module.resolve_dispute(disputed="")
        second_ops_empty_result = module.resolve_dispute(disputed="")
        self.assertIsNot(ops_empty_result, second_ops_empty_result)
        self.assertIsNot(
            ops_empty_result["reconstructed_material"],
            second_ops_empty_result["reconstructed_material"])
        self.assertIsNot(
            ops_empty_result["material_read"],
            second_ops_empty_result["material_read"])
        ops_none_disputed_result = module.resolve_dispute(disputed=None)
        second_ops_none_disputed_result = module.resolve_dispute(
            disputed=None)
        self.assertIsNot(
            ops_none_disputed_result, second_ops_none_disputed_result)
        self.assertIsNot(
            ops_none_disputed_result["reconstructed_material"],
            second_ops_none_disputed_result["reconstructed_material"])
        self.assertIsNot(
            ops_none_disputed_result["material_read"],
            second_ops_none_disputed_result["material_read"])
        ops_zero_tuple_result = module.resolve_dispute(
            disputed=0,
            journal_records=("journal record one", "journal record two"))
        second_ops_zero_tuple_result = module.resolve_dispute(
            disputed=0,
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(ops_zero_tuple_result, second_ops_zero_tuple_result)
        self.assertIsNot(
            ops_zero_tuple_result["reconstructed_material"],
            second_ops_zero_tuple_result["reconstructed_material"])
        self.assertIsNot(
            ops_zero_tuple_result["material_read"],
            second_ops_zero_tuple_result["material_read"])

        tuple_none_disputed_result = module.resolve_dispute(
            disputed=None,
            journal_records=("journal record one", "journal record two"))
        second_tuple_none_disputed_result = module.resolve_dispute(
            disputed=None,
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(
            tuple_none_disputed_result, second_tuple_none_disputed_result)
        self.assertIsNot(
            tuple_none_disputed_result["reconstructed_material"],
            second_tuple_none_disputed_result["reconstructed_material"])
        self.assertIsNot(
            tuple_none_disputed_result["material_read"],
            second_tuple_none_disputed_result["material_read"])
        tuple_empty_disputed_result = module.resolve_dispute(
            disputed="",
            journal_records=("journal record one", "journal record two"))
        second_tuple_empty_disputed_result = module.resolve_dispute(
            disputed="",
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(
            tuple_empty_disputed_result, second_tuple_empty_disputed_result)
        self.assertIsNot(
            tuple_empty_disputed_result["reconstructed_material"],
            second_tuple_empty_disputed_result["reconstructed_material"])
        self.assertIsNot(
            tuple_empty_disputed_result["material_read"],
            second_tuple_empty_disputed_result["material_read"])
        none_records_none_disputed_result = module.resolve_dispute(
            disputed=None, journal_records=None)
        second_none_records_none_disputed_result = module.resolve_dispute(
            disputed=None, journal_records=None)
        self.assertIsNot(
            none_records_none_disputed_result,
            second_none_records_none_disputed_result)
        self.assertIsNot(
            none_records_none_disputed_result["reconstructed_material"],
            second_none_records_none_disputed_result[
                "reconstructed_material"])
        self.assertIsNot(
            none_records_none_disputed_result["material_read"],
            second_none_records_none_disputed_result["material_read"])
        none_records_empty_disputed_result = module.resolve_dispute(
            disputed="", journal_records=None)
        second_none_records_empty_disputed_result = module.resolve_dispute(
            disputed="", journal_records=None)
        self.assertIsNot(
            none_records_empty_disputed_result,
            second_none_records_empty_disputed_result)
        self.assertIsNot(
            none_records_empty_disputed_result["reconstructed_material"],
            second_none_records_empty_disputed_result[
                "reconstructed_material"])
        self.assertIsNot(
            none_records_empty_disputed_result["material_read"],
            second_none_records_empty_disputed_result["material_read"])
        float_zero_disputed_result = module.resolve_dispute(
            disputed=0.0,
            journal_records=["journal record one", "journal record two"])
        second_float_zero_disputed_result = module.resolve_dispute(
            disputed=0.0,
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(
            float_zero_disputed_result, second_float_zero_disputed_result)
        self.assertIsNot(
            float_zero_disputed_result["reconstructed_material"],
            second_float_zero_disputed_result["reconstructed_material"])
        self.assertIsNot(
            float_zero_disputed_result["material_read"],
            second_float_zero_disputed_result["material_read"])
        empty_list_disputed_result = module.resolve_dispute(
            disputed=[],
            journal_records=["journal record one", "journal record two"])
        second_empty_list_disputed_result = module.resolve_dispute(
            disputed=[],
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(
            empty_list_disputed_result, second_empty_list_disputed_result)
        self.assertIsNot(
            empty_list_disputed_result["reconstructed_material"],
            second_empty_list_disputed_result["reconstructed_material"])
        self.assertIsNot(
            empty_list_disputed_result["material_read"],
            second_empty_list_disputed_result["material_read"])
        empty_tuple_disputed_result = module.resolve_dispute(
            disputed=(),
            journal_records=["journal record one", "journal record two"])
        second_empty_tuple_disputed_result = module.resolve_dispute(
            disputed=(),
            journal_records=["journal record one", "journal record two"])
        self.assertIsNot(
            empty_tuple_disputed_result, second_empty_tuple_disputed_result)
        self.assertIsNot(
            empty_tuple_disputed_result["reconstructed_material"],
            second_empty_tuple_disputed_result["reconstructed_material"])
        self.assertIsNot(
            empty_tuple_disputed_result["material_read"],
            second_empty_tuple_disputed_result["material_read"])
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
        first_none = module.incident_entry(answers=None)
        second_none = module.incident_entry(answers=None)
        self.assertIsNot(first_none["questions"], second_none["questions"])
        self.assertIsNot(first_none["answers"], second_none["answers"])
        self.assertIsNot(
            first_none["consequences"], second_none["consequences"])
        first_no_argument = module.incident_entry()
        second_no_argument = module.incident_entry()
        self.assertIsNot(first_no_argument, second_no_argument)
        self.assertIsNot(
            first_no_argument["questions"],
            second_no_argument["questions"])
        self.assertIsNot(
            first_no_argument["answers"], second_no_argument["answers"])
        self.assertIsNot(
            first_no_argument["consequences"],
            second_no_argument["consequences"])
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
            ({"sealed or secret material involved": "maybe",
              "store suspect": "no",
              "bundle wrongly loadable": "no"},
             "each answer must be yes or no"),
            ({"store suspect": "no", "bundle wrongly loadable": "no"},
             "answers lacks the question: 'sealed or secret material involved'"),
            ({"sealed or secret material involved": "yes",
              "store suspect": "no"},
             "answers lacks the question: 'bundle wrongly loadable'"),
        )
        for answers, message in refused_forms:
            with self.assertRaises(ValueError, msg=repr(answers)) as caught:
                module.incident_entry(answers=answers)
            self.assertEqual(str(caught.exception), message)

    def test_answers_presented_as_a_list_stand_recorded_in_question_order(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=["yes", "no", "no"])
        second = module.incident_entry(answers=["yes", "no", "no"])
        self.assertIsNot(record["questions"], second["questions"])
        self.assertIsNot(record["answers"], second["answers"])
        self.assertIsNot(record["consequences"], second["consequences"])
        self.assertEqual(tuple(record["questions"]),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(tuple(record["answers"].keys()),
                         self.QUESTIONS_IN_ORDER)
        self.assertEqual(record["answers"], {
            "sealed or secret material involved": "yes",
            "store suspect": "no",
            "bundle wrongly loadable": "no",
        })

        second_question_list = module.incident_entry(
            answers=["no", "yes", "no"])
        second_second_question_list = module.incident_entry(
            answers=["no", "yes", "no"])
        self.assertIsNot(second_question_list, second_second_question_list)
        self.assertIsNot(
            second_question_list["questions"],
            second_second_question_list["questions"])
        self.assertIsNot(
            second_question_list["answers"],
            second_second_question_list["answers"])
        self.assertIsNot(
            second_question_list["consequences"],
            second_second_question_list["consequences"])
        third_question_list = module.incident_entry(
            answers=["no", "no", "yes"])
        second_third_question_list = module.incident_entry(
            answers=["no", "no", "yes"])
        self.assertIsNot(third_question_list, second_third_question_list)
        self.assertIsNot(
            third_question_list["questions"],
            second_third_question_list["questions"])
        self.assertIsNot(
            third_question_list["answers"],
            second_third_question_list["answers"])
        self.assertIsNot(
            third_question_list["consequences"],
            second_third_question_list["consequences"])
        all_yes_list = module.incident_entry(answers=["yes", "yes", "yes"])
        second_all_yes_list = module.incident_entry(
            answers=["yes", "yes", "yes"])
        self.assertIsNot(all_yes_list, second_all_yes_list)
        self.assertIsNot(
            all_yes_list["questions"], second_all_yes_list["questions"])
        self.assertIsNot(
            all_yes_list["answers"], second_all_yes_list["answers"])
        self.assertIsNot(
            all_yes_list["consequences"], second_all_yes_list["consequences"])

    def test_answers_value_in_no_governed_form_raises_value_error(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError) as caught:
            module.incident_entry(answers="yes")
        self.assertEqual(
            str(caught.exception), "answers must be a list, tuple, mapping, or None")

    def test_journal_records_value_in_no_governed_form_raises(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError) as caught:
            module.resolve_dispute(disputed=True,
                                   journal_records="journal record one")
        self.assertEqual(
            str(caught.exception), "journal records must be a list or None")

    def test_journal_records_value_in_no_governed_form_raises_on_undisputed_call(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError) as caught:
            module.resolve_dispute(disputed=False,
                                   journal_records="journal record one")
        self.assertEqual(
            str(caught.exception), "journal records must be a list or None")

    def test_entry_point_record_stands_in_the_incident_record(self):
        module = require("ontoloop.ops")
        record = module.incident_entry(answers=("no", "no", "no"))
        self.assertEqual(record["record_home"], "incident record")

    def test_recorder_first_rule(self):
        module = require("ontoloop.ops")
        result = module.resolve_dispute(disputed=True)
        second_no_records = module.resolve_dispute(disputed=True)
        self.assertIsNot(
            result["reconstructed_material"],
            second_no_records["reconstructed_material"])
        self.assertIsNot(
            result["material_read"], second_no_records["material_read"])
        self.assertEqual(result["first_act"], "journal reconstruction")
        self.assertIs(result["recollection_relied_on"], False)
        self.assertIs(result["journal_reconstructed"], True)
        self.assertIs(result["journal_read"], True)
        self.assertEqual(result["reconstructed_material"], [])
        self.assertEqual(result["material_read"], [])
        self.assertIsNot(
            result["reconstructed_material"], result["material_read"])
        records = ["journal record one", "journal record two"]
        read_result = module.resolve_dispute(
            disputed=True, journal_records=records)
        second_read_result = module.resolve_dispute(
            disputed=True, journal_records=records)
        self.assertIsNot(
            read_result["reconstructed_material"],
            second_read_result["reconstructed_material"])
        self.assertIsNot(
            read_result["material_read"],
            second_read_result["material_read"])
        self.assertEqual(
            read_result["reconstructed_material"], records)
        self.assertEqual(read_result["material_read"], records)
        self.assertIs(read_result["journal_read"], True)
        self.assertIsNot(
            read_result["reconstructed_material"],
            read_result["material_read"])
        self.assertIsNot(read_result["reconstructed_material"], records)
        self.assertIsNot(read_result["material_read"], records)
        truthy_result = module.resolve_dispute(
            disputed=1, journal_records=records)
        second_truthy_result = module.resolve_dispute(
            disputed=1, journal_records=records)
        self.assertIsNot(truthy_result, second_truthy_result)
        self.assertIsNot(
            truthy_result["reconstructed_material"],
            second_truthy_result["reconstructed_material"])
        self.assertIsNot(
            truthy_result["material_read"],
            second_truthy_result["material_read"])
        truthy_tuple_result = module.resolve_dispute(
            disputed=1,
            journal_records=("journal record one", "journal record two"))
        second_truthy_tuple_result = module.resolve_dispute(
            disputed=1,
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(truthy_tuple_result, second_truthy_tuple_result)
        self.assertIsNot(
            truthy_tuple_result["reconstructed_material"],
            second_truthy_tuple_result["reconstructed_material"])
        self.assertIsNot(
            truthy_tuple_result["material_read"],
            second_truthy_tuple_result["material_read"])
        truthy_no_records_result = module.resolve_dispute(disputed=1)
        second_truthy_no_records_result = module.resolve_dispute(
            disputed=1)
        self.assertIsNot(
            truthy_no_records_result, second_truthy_no_records_result)
        self.assertIsNot(
            truthy_no_records_result["reconstructed_material"],
            second_truthy_no_records_result["reconstructed_material"])
        self.assertIsNot(
            truthy_no_records_result["material_read"],
            second_truthy_no_records_result["material_read"])
        none_records_result = module.resolve_dispute(
            disputed=True, journal_records=None)
        second_none_records_result = module.resolve_dispute(
            disputed=True, journal_records=None)
        self.assertIsNot(none_records_result, second_none_records_result)
        self.assertIsNot(
            none_records_result["reconstructed_material"],
            second_none_records_result["reconstructed_material"])
        self.assertIsNot(
            none_records_result["material_read"],
            second_none_records_result["material_read"])


        string_disputed_result = module.resolve_dispute(
            disputed="a disputed value standing as a string",
            journal_records=records)
        second_string_disputed_result = module.resolve_dispute(
            disputed="a disputed value standing as a string",
            journal_records=records)
        self.assertIsNot(
            string_disputed_result, second_string_disputed_result)
        self.assertIsNot(
            string_disputed_result["reconstructed_material"],
            second_string_disputed_result["reconstructed_material"])
        self.assertIsNot(
            string_disputed_result["material_read"],
            second_string_disputed_result["material_read"])
        self.assertEqual(
            string_disputed_result["first_act"], "journal reconstruction")

        string_tuple_result = module.resolve_dispute(
            disputed="a disputed value standing as a string",
            journal_records=("journal record one", "journal record two"))
        second_string_tuple_result = module.resolve_dispute(
            disputed="a disputed value standing as a string",
            journal_records=("journal record one", "journal record two"))
        self.assertIsNot(string_tuple_result, second_string_tuple_result)
        self.assertIsNot(
            string_tuple_result["reconstructed_material"],
            second_string_tuple_result["reconstructed_material"])
        self.assertIsNot(
            string_tuple_result["material_read"],
            second_string_tuple_result["material_read"])
        string_no_records_result = module.resolve_dispute(
            disputed="a disputed value standing as a string")
        second_string_no_records_result = module.resolve_dispute(
            disputed="a disputed value standing as a string")
        self.assertIsNot(
            string_no_records_result, second_string_no_records_result)
        self.assertIsNot(
            string_no_records_result["reconstructed_material"],
            second_string_no_records_result["reconstructed_material"])
        self.assertIsNot(
            string_no_records_result["material_read"],
            second_string_no_records_result["material_read"])
        string_none_records_result = module.resolve_dispute(
            disputed="a disputed value standing as a string",
            journal_records=None)
        second_string_none_records_result = module.resolve_dispute(
            disputed="a disputed value standing as a string",
            journal_records=None)
        self.assertIsNot(
            string_none_records_result, second_string_none_records_result)
        self.assertIsNot(
            string_none_records_result["reconstructed_material"],
            second_string_none_records_result["reconstructed_material"])
        self.assertIsNot(
            string_none_records_result["material_read"],
            second_string_none_records_result["material_read"])
        one_none_records_result = module.resolve_dispute(
            disputed=1, journal_records=None)
        second_one_none_records_result = module.resolve_dispute(
            disputed=1, journal_records=None)
        self.assertIsNot(
            one_none_records_result, second_one_none_records_result)
        self.assertIsNot(
            one_none_records_result["reconstructed_material"],
            second_one_none_records_result["reconstructed_material"])
        self.assertIsNot(
            one_none_records_result["material_read"],
            second_one_none_records_result["material_read"])
        two_disputed_result = module.resolve_dispute(
            disputed=2, journal_records=records)
        second_two_disputed_result = module.resolve_dispute(
            disputed=2, journal_records=records)
        self.assertIsNot(two_disputed_result, second_two_disputed_result)
        self.assertIsNot(
            two_disputed_result["reconstructed_material"],
            second_two_disputed_result["reconstructed_material"])
        self.assertIsNot(
            two_disputed_result["material_read"],
            second_two_disputed_result["material_read"])
        bytes_disputed_result = module.resolve_dispute(
            disputed=b"a disputed value standing as bytes",
            journal_records=records)
        second_bytes_disputed_result = module.resolve_dispute(
            disputed=b"a disputed value standing as bytes",
            journal_records=records)
        self.assertIsNot(
            bytes_disputed_result, second_bytes_disputed_result)
        self.assertIsNot(
            bytes_disputed_result["reconstructed_material"],
            second_bytes_disputed_result["reconstructed_material"])
        self.assertIsNot(
            bytes_disputed_result["material_read"],
            second_bytes_disputed_result["material_read"])
        list_disputed_result = module.resolve_dispute(
            disputed=["a disputed value standing as a list"],
            journal_records=records)
        second_list_disputed_result = module.resolve_dispute(
            disputed=["a disputed value standing as a list"],
            journal_records=records)
        self.assertIsNot(list_disputed_result, second_list_disputed_result)
        self.assertIsNot(
            list_disputed_result["reconstructed_material"],
            second_list_disputed_result["reconstructed_material"])
        self.assertIsNot(
            list_disputed_result["material_read"],
            second_list_disputed_result["material_read"])
    def test_recorder_first_rule_with_journal_records_as_a_tuple(self):
        module = require("ontoloop.ops")
        records = ("journal record one", "journal record two")
        result = module.resolve_dispute(
            disputed=True, journal_records=records)
        second_result = module.resolve_dispute(
            disputed=True, journal_records=records)
        self.assertIsNot(
            result["reconstructed_material"],
            second_result["reconstructed_material"])
        self.assertIsNot(
            result["material_read"], second_result["material_read"])
        self.assertEqual(result["first_act"], "journal reconstruction")
        self.assertEqual(
            result["reconstructed_material"],
            ["journal record one", "journal record two"])
        self.assertEqual(
            result["material_read"],
            ["journal record one", "journal record two"])
        self.assertIsNot(
            result["reconstructed_material"],
            result["material_read"])

    def test_loading_stop_stands_as_a_named_act(self):
        module = require("ontoloop.ops")
        self.assertIn("take_loading_stop", module.__all__)
        stop = module.take_loading_stop()
        second_stop = module.take_loading_stop()
        self.assertIsNot(stop, second_stop)
        none_bundle_stop = module.take_loading_stop(bundle=None)
        second_none_bundle_stop = module.take_loading_stop(bundle=None)
        self.assertIsNot(none_bundle_stop, second_none_bundle_stop)
        self.assertEqual(stop["act"], "incident loading stop")
        self.assertIsNone(stop["bundle"])


        empty_bundle_stop = module.take_loading_stop(bundle="")
        second_empty_bundle_stop = module.take_loading_stop(bundle="")
        self.assertIsNot(empty_bundle_stop, second_empty_bundle_stop)
        self.assertEqual(empty_bundle_stop["bundle"], "")
        zero_bundle_stop = module.take_loading_stop(bundle=0)
        second_zero_bundle_stop = module.take_loading_stop(bundle=0)
        self.assertIsNot(zero_bundle_stop, second_zero_bundle_stop)

        false_bundle_stop = module.take_loading_stop(bundle=False)
        second_false_bundle_stop = module.take_loading_stop(bundle=False)
        self.assertIsNot(false_bundle_stop, second_false_bundle_stop)
        float_zero_bundle_stop = module.take_loading_stop(bundle=0.0)
        second_float_zero_bundle_stop = module.take_loading_stop(bundle=0.0)
        self.assertIsNot(
            float_zero_bundle_stop, second_float_zero_bundle_stop)
        empty_list_bundle_stop = module.take_loading_stop(bundle=[])
        second_empty_list_bundle_stop = module.take_loading_stop(bundle=[])
        self.assertIsNot(
            empty_list_bundle_stop, second_empty_list_bundle_stop)
        empty_mapping_bundle_stop = module.take_loading_stop(bundle={})
        second_empty_mapping_bundle_stop = module.take_loading_stop(
            bundle={})
        self.assertIsNot(
            empty_mapping_bundle_stop, second_empty_mapping_bundle_stop)
        empty_tuple_bundle_stop = module.take_loading_stop(bundle=())
        second_empty_tuple_bundle_stop = module.take_loading_stop(bundle=())
        self.assertIsNot(
            empty_tuple_bundle_stop, second_empty_tuple_bundle_stop)
    def test_joint_precedence_of_repair_verification(self):
        module = require("ontoloop.ops")
        first_return = module.incident_append_order()
        second_return = module.incident_append_order()
        self.assertIsNot(first_return, second_return)
        first_tuple_return = module.incident_append_order(
            acts=("stop append", "purge append", "repair verification"))
        second_tuple_return = module.incident_append_order(
            acts=("stop append", "purge append", "repair verification"))
        self.assertIsNot(first_tuple_return, second_tuple_return)
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
        first_none_return = module.incident_append_order(acts=None)
        second_none_return = module.incident_append_order(acts=None)
        self.assertIsNot(first_none_return, second_none_return)

    def test_incident_append_order_unknown_act_raises_value_error(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError) as caught:
            module.incident_append_order(acts=("bogus act",))
        self.assertEqual(
            str(caught.exception), "unknown append act: 'bogus act'")

    def test_incident_append_order_acts_value_in_no_governed_form(self):
        module = require("ontoloop.ops")
        with self.assertRaises(ValueError) as caught:
            module.incident_append_order(acts="stop append")
        self.assertEqual(
            str(caught.exception), "acts must be a list, tuple, or None")

    def test_incident_append_order_acts_presented_as_a_list(self):
        module = require("ontoloop.ops")
        first_return = module.incident_append_order(
            acts=["stop append", "purge append", "repair verification"])
        second_return = module.incident_append_order(
            acts=["stop append", "purge append", "repair verification"])
        self.assertIsNot(first_return, second_return)
        order = list(module.incident_append_order(
            acts=["stop append", "purge append", "repair verification"]))
        self.assertEqual(
            order,
            ["repair verification", "stop append", "purge append"])
        self.assertEqual(
            list(module.incident_append_order(
                acts=["purge append", "stop append",
                      "repair verification"])),
            ["repair verification", "purge append", "stop append"])
        self.assertEqual(
            set(order),
            {"repair verification", "purge append", "stop append"})
        self.assertLess(
            order.index("repair verification"),
            order.index("purge append"))
        self.assertLess(
            order.index("repair verification"),
            order.index("stop append"))
        first_repeated_return = module.incident_append_order(
            acts=["purge append", "purge append", "stop append"])
        second_repeated_return = module.incident_append_order(
            acts=["purge append", "purge append", "stop append"])
        self.assertIsNot(first_repeated_return, second_repeated_return)


        first_tuple_repeated_return = module.incident_append_order(
            acts=("purge append", "purge append", "stop append"))
        second_tuple_repeated_return = module.incident_append_order(
            acts=("purge append", "purge append", "stop append"))
        self.assertIsNot(
            first_tuple_repeated_return, second_tuple_repeated_return)
        self.assertEqual(
            list(first_tuple_repeated_return),
            ["purge append", "purge append", "stop append"])
        first_ops_tuple_repeated_return = module.incident_append_order(
            acts=("purge append", "purge append", "stop append"))
        second_ops_tuple_repeated_return = module.incident_append_order(
            acts=("purge append", "purge append", "stop append"))
        self.assertIsNot(
            first_ops_tuple_repeated_return,
            second_ops_tuple_repeated_return)
        first_repair_repeated_return = module.incident_append_order(
            acts=["repair verification", "repair verification",
                  "stop append"])
        second_repair_repeated_return = module.incident_append_order(
            acts=["repair verification", "repair verification",
                  "stop append"])
        self.assertIsNot(
            first_repair_repeated_return, second_repair_repeated_return)

        first_tuple_repair_return = module.incident_append_order(
            acts=("repair verification", "repair verification"))
        second_tuple_repair_return = module.incident_append_order(
            acts=("repair verification", "repair verification"))
        self.assertIsNot(
            first_tuple_repair_return, second_tuple_repair_return)
        self.assertEqual(
            list(first_tuple_repair_return),
            ["repair verification", "repair verification"])
        first_stop_list_return = module.incident_append_order(
            acts=["stop append", "stop append"])
        second_stop_list_return = module.incident_append_order(
            acts=["stop append", "stop append"])
        self.assertIsNot(first_stop_list_return, second_stop_list_return)
        self.assertEqual(
            list(first_stop_list_return), ["stop append", "stop append"])
        first_stop_tuple_return = module.incident_append_order(
            acts=("stop append", "stop append"))
        second_stop_tuple_return = module.incident_append_order(
            acts=("stop append", "stop append"))
        self.assertIsNot(first_stop_tuple_return, second_stop_tuple_return)
        self.assertEqual(
            list(first_stop_tuple_return), ["stop append", "stop append"])
    def test_incident_append_order_on_a_proper_subset_of_the_acts(self):
        module = require("ontoloop.ops")
        order = list(module.incident_append_order(
            acts=("stop append", "repair verification")))
        self.assertEqual(order, ["repair verification", "stop append"])
        self.assertEqual(
            list(module.incident_append_order(acts=("purge append",))),
            ["purge append"])
        purge_order = list(module.incident_append_order(
            acts=("purge append", "repair verification")))
        self.assertEqual(
            purge_order, ["repair verification", "purge append"])
        list_purge_order = list(module.incident_append_order(
            acts=["purge append", "repair verification"]))
        self.assertEqual(
            list_purge_order, ["repair verification", "purge append"])
        list_stop_order = list(module.incident_append_order(
            acts=["stop append", "repair verification"]))
        self.assertEqual(
            list_stop_order, ["repair verification", "stop append"])
        self.assertEqual(
            list(module.incident_append_order(
                acts=("purge append", "stop append"))),
            ["purge append", "stop append"])
        self.assertEqual(
            list(module.incident_append_order(
                acts=("stop append", "purge append"))),
            ["stop append", "purge append"])
        self.assertEqual(
            list(module.incident_append_order(
                acts=["purge append", "stop append"])),
            ["purge append", "stop append"])
        self.assertEqual(
            list(module.incident_append_order(
                acts=["stop append", "purge append"])),
            ["stop append", "purge append"])
        first_single_list = module.incident_append_order(
            acts=["purge append"])
        second_single_list = module.incident_append_order(
            acts=["purge append"])
        self.assertIsNot(first_single_list, second_single_list)
        first_pair_list = module.incident_append_order(
            acts=["stop append", "purge append"])
        second_pair_list = module.incident_append_order(
            acts=["stop append", "purge append"])
        self.assertIsNot(first_pair_list, second_pair_list)
        first_pair_tuple = module.incident_append_order(
            acts=("stop append", "repair verification"))
        second_pair_tuple = module.incident_append_order(
            acts=("stop append", "repair verification"))
        self.assertIsNot(first_pair_tuple, second_pair_tuple)
        first_single_tuple = module.incident_append_order(
            acts=("purge append",))
        second_single_tuple = module.incident_append_order(
            acts=("purge append",))
        self.assertIsNot(first_single_tuple, second_single_tuple)
        first_empty_list = module.incident_append_order(acts=[])
        second_empty_list = module.incident_append_order(acts=[])
        self.assertIsNot(first_empty_list, second_empty_list)
        first_empty_tuple = module.incident_append_order(acts=())
        second_empty_tuple = module.incident_append_order(acts=())
        self.assertIsNot(first_empty_tuple, second_empty_tuple)

    def test_loading_stop_takes_effect_before_its_journal_record(self):
        module = require("ontoloop.ops")
        bundle = "named wrongly loadable bundle"
        stop = module.take_loading_stop(bundle=bundle)
        second_stop = module.take_loading_stop(bundle=bundle)
        self.assertIsNot(stop, second_stop)
        self.assertIs(stop["effective_on_loading"], True)
        self.assertIs(stop["journal_record_landed"], False)
        self.assertEqual(stop["bundle"], bundle)
        discovery = module.discovery_after_stop(stop, bundle=bundle)
        second_discovery = module.discovery_after_stop(stop, bundle=bundle)
        self.assertIsNot(discovery, second_discovery)
        self.assertEqual(discovery["promotion"], None)
        self.assertEqual(discovery["bundle"], bundle)
        companion_stop = dict(stop)
        companion_stop["effective_on_loading"] = False
        companion = module.discovery_after_stop(
            companion_stop, bundle=bundle)
        second_companion = module.discovery_after_stop(
            companion_stop, bundle=bundle)
        self.assertIsNot(companion, second_companion)
        self.assertEqual(companion["promotion"], bundle)
        self.assertEqual(companion["bundle"], bundle)
        differing = module.discovery_after_stop(
            stop, bundle="another bundle passed to the call")
        second_differing = module.discovery_after_stop(
            stop, bundle="another bundle passed to the call")
        self.assertIsNot(differing, second_differing)
        self.assertEqual(differing["bundle"], bundle)
        no_bundle_stop = module.take_loading_stop()
        none_bundle_discovery = module.discovery_after_stop(
            no_bundle_stop, bundle=bundle)
        second_none_bundle_discovery = module.discovery_after_stop(
            no_bundle_stop, bundle=bundle)
        self.assertIsNot(
            none_bundle_discovery, second_none_bundle_discovery)
        none_bundle_companion_stop = dict(no_bundle_stop)
        none_bundle_companion_stop["effective_on_loading"] = False
        none_bundle_companion = module.discovery_after_stop(
            none_bundle_companion_stop, bundle=bundle)
        second_none_bundle_companion = module.discovery_after_stop(
            none_bundle_companion_stop, bundle=bundle)
        self.assertIsNot(
            none_bundle_companion, second_none_bundle_companion)
        no_argument_discovery = module.discovery_after_stop(stop)
        second_no_argument_discovery = module.discovery_after_stop(stop)
        self.assertIsNot(
            no_argument_discovery, second_no_argument_discovery)
        no_argument_companion = module.discovery_after_stop(companion_stop)
        second_no_argument_companion = module.discovery_after_stop(
            companion_stop)
        self.assertIsNot(
            no_argument_companion, second_no_argument_companion)
        no_key_stop = {
            key: value for key, value in stop.items() if key != "bundle"
        }
        no_key_discovery = module.discovery_after_stop(
            no_key_stop, bundle=bundle)
        second_no_key_discovery = module.discovery_after_stop(
            no_key_stop, bundle=bundle)
        self.assertIsNot(no_key_discovery, second_no_key_discovery)
        no_key_companion_stop = dict(no_key_stop)
        no_key_companion_stop["effective_on_loading"] = False
        no_key_companion = module.discovery_after_stop(
            no_key_companion_stop, bundle=bundle)
        second_no_key_companion = module.discovery_after_stop(
            no_key_companion_stop, bundle=bundle)
        self.assertIsNot(no_key_companion, second_no_key_companion)
        no_mapping_discovery = module.discovery_after_stop(
            None, bundle=bundle)
        second_no_mapping_discovery = module.discovery_after_stop(
            None, bundle=bundle)
        self.assertIsNot(
            no_mapping_discovery, second_no_mapping_discovery)
        other_no_mapping_discovery = module.discovery_after_stop(
            "a stop standing as no mapping", bundle=bundle)
        second_other_no_mapping_discovery = module.discovery_after_stop(
            "a stop standing as no mapping", bundle=bundle)
        self.assertIsNot(
            other_no_mapping_discovery, second_other_no_mapping_discovery)
        express_none_discovery = module.discovery_after_stop(
            stop, bundle=None)
        second_express_none_discovery = module.discovery_after_stop(
            stop, bundle=None)
        self.assertIsNot(
            express_none_discovery, second_express_none_discovery)
        no_effective_key_stop = {
            key: value for key, value in stop.items()
            if key != "effective_on_loading"
        }
        no_effective_key_discovery = module.discovery_after_stop(
            no_effective_key_stop, bundle=bundle)
        second_no_effective_key_discovery = module.discovery_after_stop(
            no_effective_key_stop, bundle=bundle)
        self.assertIsNot(
            no_effective_key_discovery,
            second_no_effective_key_discovery)
        truthy_effective_stop = dict(stop)
        truthy_effective_stop["effective_on_loading"] = 1
        truthy_effective_discovery = module.discovery_after_stop(
            truthy_effective_stop, bundle=bundle)
        second_truthy_effective_discovery = module.discovery_after_stop(
            truthy_effective_stop, bundle=bundle)
        self.assertIsNot(
            truthy_effective_discovery,
            second_truthy_effective_discovery)


        zero_effective_stop = dict(stop)
        zero_effective_stop["effective_on_loading"] = 0
        zero_effective_discovery = module.discovery_after_stop(
            zero_effective_stop, bundle=bundle)
        second_zero_effective_discovery = module.discovery_after_stop(
            zero_effective_stop, bundle=bundle)
        self.assertIsNot(
            zero_effective_discovery, second_zero_effective_discovery)
        self.assertEqual(zero_effective_discovery["promotion"], bundle)
        self.assertEqual(zero_effective_discovery["bundle"], bundle)
        companion_none_bundle_discovery = module.discovery_after_stop(
            companion_stop, bundle=None)
        second_companion_none_bundle_discovery = (
            module.discovery_after_stop(companion_stop, bundle=None))
        self.assertIsNot(
            companion_none_bundle_discovery,
            second_companion_none_bundle_discovery)
        no_bundle_none_bundle_discovery = module.discovery_after_stop(
            no_bundle_stop, bundle=None)
        second_no_bundle_none_bundle_discovery = (
            module.discovery_after_stop(no_bundle_stop, bundle=None))
        self.assertIsNot(
            no_bundle_none_bundle_discovery,
            second_no_bundle_none_bundle_discovery)
        no_mapping_no_argument_discovery = module.discovery_after_stop(
            None)
        second_no_mapping_no_argument_discovery = (
            module.discovery_after_stop(None))
        self.assertIsNot(
            no_mapping_no_argument_discovery,
            second_no_mapping_no_argument_discovery)
        no_mapping_none_bundle_discovery = module.discovery_after_stop(
            None, bundle=None)
        second_no_mapping_none_bundle_discovery = (
            module.discovery_after_stop(None, bundle=None))
        self.assertIsNot(
            no_mapping_none_bundle_discovery,
            second_no_mapping_none_bundle_discovery)
        truthy_none_bundle_discovery = module.discovery_after_stop(
            truthy_effective_stop, bundle=None)
        second_truthy_none_bundle_discovery = (
            module.discovery_after_stop(truthy_effective_stop, bundle=None))
        self.assertIsNot(
            truthy_none_bundle_discovery,
            second_truthy_none_bundle_discovery)
        truthy_no_argument_discovery = module.discovery_after_stop(
            truthy_effective_stop)
        second_truthy_no_argument_discovery = (
            module.discovery_after_stop(truthy_effective_stop))
        self.assertIsNot(
            truthy_no_argument_discovery,
            second_truthy_no_argument_discovery)
        no_key_none_bundle_discovery = module.discovery_after_stop(
            no_effective_key_stop, bundle=None)
        second_no_key_none_bundle_discovery = (
            module.discovery_after_stop(no_effective_key_stop, bundle=None))
        self.assertIsNot(
            no_key_none_bundle_discovery,
            second_no_key_none_bundle_discovery)
        no_key_no_argument_discovery = module.discovery_after_stop(
            no_effective_key_stop)
        second_no_key_no_argument_discovery = (
            module.discovery_after_stop(no_effective_key_stop))
        self.assertIsNot(
            no_key_no_argument_discovery,
            second_no_key_no_argument_discovery)
        empty_mapping_discovery = module.discovery_after_stop(
            {}, bundle=bundle)
        second_empty_mapping_discovery = module.discovery_after_stop(
            {}, bundle=bundle)
        self.assertIsNot(
            empty_mapping_discovery, second_empty_mapping_discovery)
        self.assertEqual(empty_mapping_discovery["promotion"], bundle)
        self.assertEqual(empty_mapping_discovery["bundle"], bundle)
        ops_no_mapping_no_argument_discovery = (
            module.discovery_after_stop(None))
        second_ops_no_mapping_no_argument_discovery = (
            module.discovery_after_stop(None))
        self.assertIsNot(
            ops_no_mapping_no_argument_discovery,
            second_ops_no_mapping_no_argument_discovery)
        ops_string_none_bundle_discovery = module.discovery_after_stop(
            "a stop standing as no mapping", bundle=None)
        second_ops_string_none_bundle_discovery = (
            module.discovery_after_stop(
                "a stop standing as no mapping", bundle=None))
        self.assertIsNot(
            ops_string_none_bundle_discovery,
            second_ops_string_none_bundle_discovery)
        ops_no_key_none_bundle_discovery = module.discovery_after_stop(
            no_key_stop, bundle=None)
        second_ops_no_key_none_bundle_discovery = (
            module.discovery_after_stop(no_key_stop, bundle=None))
        self.assertIsNot(
            ops_no_key_none_bundle_discovery,
            second_ops_no_key_none_bundle_discovery)
        string_effective_stop = dict(stop)
        string_effective_stop["effective_on_loading"] = (
            "a truthy string value")
        string_effective_discovery = module.discovery_after_stop(
            string_effective_stop, bundle=bundle)
        second_string_effective_discovery = module.discovery_after_stop(
            string_effective_stop, bundle=bundle)
        self.assertIsNot(
            string_effective_discovery, second_string_effective_discovery)
        self.assertEqual(string_effective_discovery["promotion"], bundle)

        zero_none_bundle_discovery = module.discovery_after_stop(
            zero_effective_stop, bundle=None)
        second_zero_none_bundle_discovery = module.discovery_after_stop(
            zero_effective_stop, bundle=None)
        self.assertIsNot(
            zero_none_bundle_discovery, second_zero_none_bundle_discovery)
        self.assertEqual(zero_none_bundle_discovery["promotion"], None)
        self.assertEqual(zero_none_bundle_discovery["bundle"], bundle)
        zero_no_argument_discovery = module.discovery_after_stop(
            zero_effective_stop)
        second_zero_no_argument_discovery = module.discovery_after_stop(
            zero_effective_stop)
        self.assertIsNot(
            zero_no_argument_discovery, second_zero_no_argument_discovery)
        self.assertEqual(zero_no_argument_discovery["promotion"], None)
        self.assertEqual(zero_no_argument_discovery["bundle"], bundle)
        string_none_bundle_discovery = module.discovery_after_stop(
            string_effective_stop, bundle=None)
        second_string_none_bundle_discovery = module.discovery_after_stop(
            string_effective_stop, bundle=None)
        self.assertIsNot(
            string_none_bundle_discovery,
            second_string_none_bundle_discovery)
        self.assertEqual(string_none_bundle_discovery["promotion"], None)
        string_no_argument_discovery = module.discovery_after_stop(
            string_effective_stop)
        second_string_no_argument_discovery = module.discovery_after_stop(
            string_effective_stop)
        self.assertIsNot(
            string_no_argument_discovery,
            second_string_no_argument_discovery)
        self.assertEqual(string_no_argument_discovery["promotion"], None)
        empty_none_bundle_discovery = module.discovery_after_stop(
            {}, bundle=None)
        second_empty_none_bundle_discovery = module.discovery_after_stop(
            {}, bundle=None)
        self.assertIsNot(
            empty_none_bundle_discovery, second_empty_none_bundle_discovery)
        self.assertEqual(empty_none_bundle_discovery["promotion"], None)
        self.assertEqual(empty_none_bundle_discovery["bundle"], None)
        empty_no_argument_discovery = module.discovery_after_stop({})
        second_empty_no_argument_discovery = module.discovery_after_stop({})
        self.assertIsNot(
            empty_no_argument_discovery, second_empty_no_argument_discovery)
        self.assertEqual(empty_no_argument_discovery["promotion"], None)
        self.assertEqual(empty_no_argument_discovery["bundle"], None)
        string_no_argument_discovery = module.discovery_after_stop(
            "a stop standing as no mapping")
        second_string_no_argument_discovery = module.discovery_after_stop(
            "a stop standing as no mapping")
        self.assertIsNot(
            string_no_argument_discovery,
            second_string_no_argument_discovery)
        no_key_no_argument_discovery = module.discovery_after_stop(
            no_key_stop)
        second_no_key_no_argument_discovery = module.discovery_after_stop(
            no_key_stop)
        self.assertIsNot(
            no_key_no_argument_discovery,
            second_no_key_no_argument_discovery)
        companion_differing = module.discovery_after_stop(
            companion_stop, bundle="another bundle passed to the call")
        second_companion_differing = module.discovery_after_stop(
            companion_stop, bundle="another bundle passed to the call")
        self.assertIsNot(companion_differing, second_companion_differing)
        self.assertEqual(
            companion_differing["promotion"],
            "another bundle passed to the call")
        self.assertEqual(companion_differing["bundle"], bundle)
        list_stop_discovery = module.discovery_after_stop(
            ["a stop standing as a list"], bundle=bundle)
        second_list_stop_discovery = module.discovery_after_stop(
            ["a stop standing as a list"], bundle=bundle)
        self.assertIsNot(list_stop_discovery, second_list_stop_discovery)
        self.assertEqual(list_stop_discovery["promotion"], bundle)
        self.assertEqual(list_stop_discovery["bundle"], bundle)
        tuple_stop_discovery = module.discovery_after_stop(
            ("a stop standing as a tuple",), bundle=bundle)
        second_tuple_stop_discovery = module.discovery_after_stop(
            ("a stop standing as a tuple",), bundle=bundle)
        self.assertIsNot(tuple_stop_discovery, second_tuple_stop_discovery)
        self.assertEqual(tuple_stop_discovery["promotion"], bundle)
        self.assertEqual(tuple_stop_discovery["bundle"], bundle)
        empty_string_effective_stop = dict(stop)
        empty_string_effective_stop["effective_on_loading"] = ""
        empty_string_effective_discovery = module.discovery_after_stop(
            empty_string_effective_stop, bundle=bundle)
        second_empty_string_effective_discovery = (
            module.discovery_after_stop(
                empty_string_effective_stop, bundle=bundle))
        self.assertIsNot(
            empty_string_effective_discovery,
            second_empty_string_effective_discovery)
        self.assertEqual(
            empty_string_effective_discovery["promotion"], bundle)
        float_zero_effective_stop = dict(stop)
        float_zero_effective_stop["effective_on_loading"] = 0.0
        float_zero_effective_discovery = module.discovery_after_stop(
            float_zero_effective_stop, bundle=bundle)
        second_float_zero_effective_discovery = (
            module.discovery_after_stop(
                float_zero_effective_stop, bundle=bundle))
        self.assertIsNot(
            float_zero_effective_discovery,
            second_float_zero_effective_discovery)
        self.assertEqual(float_zero_effective_discovery["promotion"], bundle)
        empty_list_effective_stop = dict(stop)
        empty_list_effective_stop["effective_on_loading"] = []
        empty_list_effective_discovery = module.discovery_after_stop(
            empty_list_effective_stop, bundle=bundle)
        second_empty_list_effective_discovery = (
            module.discovery_after_stop(
                empty_list_effective_stop, bundle=bundle))
        self.assertIsNot(
            empty_list_effective_discovery,
            second_empty_list_effective_discovery)
        self.assertEqual(empty_list_effective_discovery["promotion"], bundle)
    def test_loading_stop_record_boundary_and_journal_landing(self):
        module = require("ontoloop.ops")
        stop = module.take_loading_stop()
        self.assertEqual(stop["recorded_on"], "operator surface")
        self.assertEqual(stop["effective_at"], "next run boundary")
        self.assertIs(stop["journal_record_landed"], False)
        landed = module.journal_record_after_append(stop)
        second_landed = module.journal_record_after_append(stop)
        self.assertIsNot(landed, second_landed)
        self.assertIsNot(landed["stop"], second_landed["stop"])
        self.assertIs(landed["journal_record_landed"], True)
        self.assertEqual(landed["stop"], stop)
        self.assertIsNot(landed["stop"], stop)
        none_store_landed = module.journal_record_after_append(
            stop, store=None)
        second_none_store_landed = module.journal_record_after_append(
            stop, store=None)
        self.assertIsNot(none_store_landed, second_none_store_landed)
        self.assertIsNot(
            none_store_landed["stop"], second_none_store_landed["stop"])
        string_stop_landed = module.journal_record_after_append(
            "a stop standing as no mapping")
        second_string_stop_landed = module.journal_record_after_append(
            "a stop standing as no mapping")
        self.assertIsNot(string_stop_landed, second_string_stop_landed)


        named_stop = module.take_loading_stop(bundle="named bundle")
        named_none_store_landed = module.journal_record_after_append(
            named_stop, store=None)
        second_named_none_store_landed = (
            module.journal_record_after_append(named_stop, store=None))
        self.assertIsNot(
            named_none_store_landed, second_named_none_store_landed)
        self.assertIsNot(
            named_none_store_landed["stop"],
            second_named_none_store_landed["stop"])
        none_stop_no_store_landed = module.journal_record_after_append(
            None)
        second_none_stop_no_store_landed = (
            module.journal_record_after_append(None))
        self.assertIsNot(
            none_stop_no_store_landed, second_none_stop_no_store_landed)
        none_stop_none_store_landed = module.journal_record_after_append(
            None, store=None)
        second_none_stop_none_store_landed = (
            module.journal_record_after_append(None, store=None))
        self.assertIsNot(
            none_stop_none_store_landed,
            second_none_stop_none_store_landed)
        string_stop_none_store_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=None))
        second_string_stop_none_store_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=None))
        self.assertIsNot(
            string_stop_none_store_landed,
            second_string_stop_none_store_landed)
        no_bundle_key_stop = {
            key: value for key, value in stop.items() if key != "bundle"
        }
        no_bundle_key_landed = module.journal_record_after_append(
            no_bundle_key_stop)
        second_no_bundle_key_landed = (
            module.journal_record_after_append(no_bundle_key_stop))
        self.assertIsNot(no_bundle_key_landed, second_no_bundle_key_landed)
        self.assertIsNot(
            no_bundle_key_landed["stop"],
            second_no_bundle_key_landed["stop"])
        ops_none_stop_no_store_landed = (
            module.journal_record_after_append(None))
        second_ops_none_stop_no_store_landed = (
            module.journal_record_after_append(None))
        self.assertIsNot(
            ops_none_stop_no_store_landed,
            second_ops_none_stop_no_store_landed)

        no_bundle_key_none_store_landed = (
            module.journal_record_after_append(
                no_bundle_key_stop, store=None))
        second_no_bundle_key_none_store_landed = (
            module.journal_record_after_append(
                no_bundle_key_stop, store=None))
        self.assertIsNot(
            no_bundle_key_none_store_landed,
            second_no_bundle_key_none_store_landed)
        self.assertIsNot(
            no_bundle_key_none_store_landed["stop"],
            second_no_bundle_key_none_store_landed["stop"])
        empty_stop_landed = module.journal_record_after_append({})
        second_empty_stop_landed = module.journal_record_after_append({})
        self.assertIsNot(empty_stop_landed, second_empty_stop_landed)
        self.assertIsNot(
            empty_stop_landed["stop"], second_empty_stop_landed["stop"])
        self.assertIs(empty_stop_landed["journal_record_landed"], True)
        list_stop_landed = module.journal_record_after_append(
            ["a stop standing as a list"])
        second_list_stop_landed = module.journal_record_after_append(
            ["a stop standing as a list"])
        self.assertIsNot(list_stop_landed, second_list_stop_landed)
    def test_loading_stop_journal_landing_with_a_store_passed(self):
        module = require("ontoloop.ops")
        stop = module.take_loading_stop(bundle="named bundle")
        landed = module.journal_record_after_append(stop, store={})
        second_landed = module.journal_record_after_append(stop, store={})
        self.assertIsNot(landed, second_landed)
        self.assertIsNot(landed["stop"], second_landed["stop"])
        self.assertIs(landed["journal_record_landed"], False)
        self.assertEqual(landed["stop"], stop)
        self.assertIsNot(landed["stop"], stop)
        standing_store = {"standing entry": "standing value"}
        no_landing_landed = module.journal_record_after_append(
            stop, store=standing_store)
        second_no_landing_landed = module.journal_record_after_append(
            stop, store=standing_store)
        self.assertIsNot(no_landing_landed, second_no_landing_landed)
        self.assertIsNot(
            no_landing_landed["stop"], second_no_landing_landed["stop"])
        no_bundle_stop = module.take_loading_stop()
        no_bundle_landed = module.journal_record_after_append(
            no_bundle_stop, store={})
        second_no_bundle_landed = module.journal_record_after_append(
            no_bundle_stop, store={})
        self.assertIsNot(no_bundle_landed, second_no_bundle_landed)
        self.assertIsNot(
            no_bundle_landed["stop"], second_no_bundle_landed["stop"])
        crossed_landed = module.journal_record_after_append(
            no_bundle_stop, store=standing_store)
        second_crossed_landed = module.journal_record_after_append(
            no_bundle_stop, store=standing_store)
        self.assertIsNot(crossed_landed, second_crossed_landed)
        self.assertIsNot(
            crossed_landed["stop"], second_crossed_landed["stop"])
        string_stop_landed = module.journal_record_after_append(
            "a stop standing as no mapping", store={})
        second_string_stop_landed = module.journal_record_after_append(
            "a stop standing as no mapping", store={})
        self.assertIsNot(string_stop_landed, second_string_stop_landed)


        none_stop_empty_store_landed = (
            module.journal_record_after_append(None, store={}))
        second_none_stop_empty_store_landed = (
            module.journal_record_after_append(None, store={}))
        self.assertIsNot(
            none_stop_empty_store_landed,
            second_none_stop_empty_store_landed)
        none_stop_standing_store_landed = (
            module.journal_record_after_append(
                None, store=standing_store))
        second_none_stop_standing_store_landed = (
            module.journal_record_after_append(
                None, store=standing_store))
        self.assertIsNot(
            none_stop_standing_store_landed,
            second_none_stop_standing_store_landed)
        string_stop_standing_store_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=standing_store))
        second_string_stop_standing_store_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=standing_store))
        self.assertIsNot(
            string_stop_standing_store_landed,
            second_string_stop_standing_store_landed)
        ops_none_stop_empty_store_landed = (
            module.journal_record_after_append(None, store={}))
        second_ops_none_stop_empty_store_landed = (
            module.journal_record_after_append(None, store={}))
        self.assertIsNot(
            ops_none_stop_empty_store_landed,
            second_ops_none_stop_empty_store_landed)

        journal_no_bundle_key_stop = {
            key: value for key, value in stop.items() if key != "bundle"
        }
        no_bundle_key_empty_store_landed = (
            module.journal_record_after_append(
                journal_no_bundle_key_stop, store={}))
        second_no_bundle_key_empty_store_landed = (
            module.journal_record_after_append(
                journal_no_bundle_key_stop, store={}))
        self.assertIsNot(
            no_bundle_key_empty_store_landed,
            second_no_bundle_key_empty_store_landed)
        self.assertIsNot(
            no_bundle_key_empty_store_landed["stop"],
            second_no_bundle_key_empty_store_landed["stop"])
        no_bundle_key_standing_store_landed = (
            module.journal_record_after_append(
                journal_no_bundle_key_stop, store=standing_store))
        second_no_bundle_key_standing_store_landed = (
            module.journal_record_after_append(
                journal_no_bundle_key_stop, store=standing_store))
        self.assertIsNot(
            no_bundle_key_standing_store_landed,
            second_no_bundle_key_standing_store_landed)
        self.assertIsNot(
            no_bundle_key_standing_store_landed["stop"],
            second_no_bundle_key_standing_store_landed["stop"])
        empty_stop_empty_store_landed = (
            module.journal_record_after_append({}, store={}))
        second_empty_stop_empty_store_landed = (
            module.journal_record_after_append({}, store={}))
        self.assertIsNot(
            empty_stop_empty_store_landed,
            second_empty_stop_empty_store_landed)
        self.assertIsNot(
            empty_stop_empty_store_landed["stop"],
            second_empty_stop_empty_store_landed["stop"])
    def test_loading_stop_journal_landing_with_an_appending_store(self):
        module = require("ontoloop.ops")
        store_module = require("ontoloop.store")
        stop = module.take_loading_stop(bundle="named bundle")
        appending_store = store_module.golden_record_store()
        landed = module.journal_record_after_append(
            stop, store=appending_store)
        second_landed = module.journal_record_after_append(
            stop, store=appending_store)
        self.assertIsNot(landed, second_landed)
        self.assertIsNot(landed["stop"], second_landed["stop"])
        self.assertIs(landed["journal_record_landed"], True)
        self.assertEqual(landed["stop"], stop)
        self.assertIsNot(landed["stop"], stop)
        no_bundle_stop = module.take_loading_stop()
        no_bundle_landed = module.journal_record_after_append(
            no_bundle_stop, store=appending_store)
        second_no_bundle_landed = module.journal_record_after_append(
            no_bundle_stop, store=appending_store)
        self.assertIsNot(no_bundle_landed, second_no_bundle_landed)
        self.assertIsNot(
            no_bundle_landed["stop"], second_no_bundle_landed["stop"])
        none_stop_landed = module.journal_record_after_append(
            None, store=appending_store)
        second_none_stop_landed = module.journal_record_after_append(
            None, store=appending_store)
        self.assertIsNot(none_stop_landed, second_none_stop_landed)


        string_stop_appending_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=appending_store))
        second_string_stop_appending_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=appending_store))
        self.assertIsNot(
            string_stop_appending_landed,
            second_string_stop_appending_landed)
        ops_string_stop_appending_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=appending_store))
        second_ops_string_stop_appending_landed = (
            module.journal_record_after_append(
                "a stop standing as a string", store=appending_store))
        self.assertIsNot(
            ops_string_stop_appending_landed,
            second_ops_string_stop_appending_landed)

        journal_no_bundle_key_stop = {
            key: value for key, value in stop.items() if key != "bundle"
        }
        no_bundle_key_appending_landed = (
            module.journal_record_after_append(
                journal_no_bundle_key_stop, store=appending_store))
        second_no_bundle_key_appending_landed = (
            module.journal_record_after_append(
                journal_no_bundle_key_stop, store=appending_store))
        self.assertIsNot(
            no_bundle_key_appending_landed,
            second_no_bundle_key_appending_landed)
        self.assertIsNot(
            no_bundle_key_appending_landed["stop"],
            second_no_bundle_key_appending_landed["stop"])
        empty_stop_appending_landed = (
            module.journal_record_after_append({}, store=appending_store))
        second_empty_stop_appending_landed = (
            module.journal_record_after_append({}, store=appending_store))
        self.assertIsNot(
            empty_stop_appending_landed, second_empty_stop_appending_landed)
        self.assertIsNot(
            empty_stop_appending_landed["stop"],
            second_empty_stop_appending_landed["stop"])
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
        self.assertEqual(
            store["records"][-1]["record_type"], "incident loading stop")
        self.assertEqual(
            store["records"][-1]["record_type"], stop["act"])


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
        unsealed_without_material = module.retire(
            self.CHECK_POINT,
            replacement_sealed=False,
            replacement_sealed_without_retiring_material=True,
        )
        self.assertEqual(
            unsealed_without_material["check_point"], self.CHECK_POINT)
        self.assertIs(unsealed_without_material["accepted"], False)
        self.assertIsNone(
            unsealed_without_material["lifecycle_record"]["transition"])
        self.assertEqual(
            unsealed_without_material["lifecycle_record"]["record_home"],
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
        with self.assertRaises(ValueError) as caught:
            module.retire_unspent_sealed(
                "dataset build", occasion="bogus")
        self.assertEqual(
            str(caught.exception), "unknown retirement occasion: 'bogus'")


    def test_no_retirement_occasion_raises_value_error(self):
        module = require("ontoloop.dataset")
        with self.assertRaises(ValueError) as caught:
            module.retire_unspent_sealed("dataset build")
        self.assertEqual(
            str(caught.exception), "unknown retirement occasion: None")

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
        self.assertEqual(outcome["record_home"], "dataset record")

    def test_no_claim_limit_effect_where_low_confidence_does_not_attach(self):
        module = require("ontoloop.dataset")
        outcome = module.attach_stamps_at_build(holdout_groups=30)
        self.assertNotIn("low confidence", outcome["attached_stamps"])
        self.assertIs(outcome["claim_limit_effect"], False)
        self.assertIs(outcome["gate_blocked"], False)
        self.assertEqual(outcome["record_home"], "dataset record")


if __name__ == "__main__":
    unittest.main()
