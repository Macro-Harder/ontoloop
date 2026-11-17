"""Unrowed F-C2 obligations, seat A: plan subsections 19.5 and 19.6.

These tests carry no row identifier. The plan states no identifier
for either obligation, and none is invented here. Each test is
homed at its plan subsection and counted in the suite manifest
under that subsection, under the F-C2 ruling at section 5 of
design/steps/step-13-content-retrace.md.
"""

import unittest
import re
from decimal import Decimal
from array import array
from collections import Counter, OrderedDict, deque
from collections import ChainMap, UserDict, UserList, UserString, defaultdict
from datetime import timedelta
from fractions import Fraction
from collections import namedtuple
from datetime import date
from enum import Enum
from enum import IntEnum
from pathlib import Path
from types import MappingProxyType
from datetime import datetime
from datetime import timezone
from enum import Flag, IntFlag, StrEnum
from uuid import UUID
from ipaddress import IPv4Address
from weakref import WeakKeyDictionary, WeakSet, WeakValueDictionary
from xml.etree.ElementTree import Element

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

        r803_tuple_0 = module.incident_entry(answers=('yes', 'yes', 'no'))
        r803_tuple_0_second = module.incident_entry(answers=('yes', 'yes', 'no'))
        self.assertIsNot(r803_tuple_0, r803_tuple_0_second)
        self.assertIsNot(
            r803_tuple_0["questions"], r803_tuple_0_second["questions"])
        self.assertIsNot(
            r803_tuple_0["answers"], r803_tuple_0_second["answers"])
        self.assertIsNot(
            r803_tuple_0["consequences"], r803_tuple_0_second["consequences"])
        r803_tuple_1 = module.incident_entry(answers=('yes', 'no', 'yes'))
        r803_tuple_1_second = module.incident_entry(answers=('yes', 'no', 'yes'))
        self.assertIsNot(r803_tuple_1, r803_tuple_1_second)
        self.assertIsNot(
            r803_tuple_1["questions"], r803_tuple_1_second["questions"])
        self.assertIsNot(
            r803_tuple_1["answers"], r803_tuple_1_second["answers"])
        self.assertIsNot(
            r803_tuple_1["consequences"], r803_tuple_1_second["consequences"])
        r803_tuple_2 = module.incident_entry(answers=('no', 'yes', 'yes'))
        r803_tuple_2_second = module.incident_entry(answers=('no', 'yes', 'yes'))
        self.assertIsNot(r803_tuple_2, r803_tuple_2_second)
        self.assertIsNot(
            r803_tuple_2["questions"], r803_tuple_2_second["questions"])
        self.assertIsNot(
            r803_tuple_2["answers"], r803_tuple_2_second["answers"])
        self.assertIsNot(
            r803_tuple_2["consequences"], r803_tuple_2_second["consequences"])

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


        r803_mapping_0 = module.incident_entry(answers={"sealed or secret material involved": "yes", "store suspect": "yes", "bundle wrongly loadable": "no"})
        r803_mapping_0_second = module.incident_entry(answers={"sealed or secret material involved": "yes", "store suspect": "yes", "bundle wrongly loadable": "no"})
        self.assertIsNot(r803_mapping_0, r803_mapping_0_second)
        self.assertIsNot(
            r803_mapping_0["questions"], r803_mapping_0_second["questions"])
        self.assertIsNot(
            r803_mapping_0["answers"], r803_mapping_0_second["answers"])
        self.assertIsNot(
            r803_mapping_0["consequences"], r803_mapping_0_second["consequences"])
        r803_mapping_1 = module.incident_entry(answers={"sealed or secret material involved": "yes", "store suspect": "no", "bundle wrongly loadable": "yes"})
        r803_mapping_1_second = module.incident_entry(answers={"sealed or secret material involved": "yes", "store suspect": "no", "bundle wrongly loadable": "yes"})
        self.assertIsNot(r803_mapping_1, r803_mapping_1_second)
        self.assertIsNot(
            r803_mapping_1["questions"], r803_mapping_1_second["questions"])
        self.assertIsNot(
            r803_mapping_1["answers"], r803_mapping_1_second["answers"])
        self.assertIsNot(
            r803_mapping_1["consequences"], r803_mapping_1_second["consequences"])
        r803_mapping_2 = module.incident_entry(answers={"sealed or secret material involved": "no", "store suspect": "yes", "bundle wrongly loadable": "yes"})
        r803_mapping_2_second = module.incident_entry(answers={"sealed or secret material involved": "no", "store suspect": "yes", "bundle wrongly loadable": "yes"})
        self.assertIsNot(r803_mapping_2, r803_mapping_2_second)
        self.assertIsNot(
            r803_mapping_2["questions"], r803_mapping_2_second["questions"])
        self.assertIsNot(
            r803_mapping_2["answers"], r803_mapping_2_second["answers"])
        self.assertIsNot(
            r803_mapping_2["consequences"], r803_mapping_2_second["consequences"])
        r803_mapping_3 = module.incident_entry(answers={"sealed or secret material involved": "yes", "store suspect": "yes", "bundle wrongly loadable": "yes"})
        r803_mapping_3_second = module.incident_entry(answers={"sealed or secret material involved": "yes", "store suspect": "yes", "bundle wrongly loadable": "yes"})
        self.assertIsNot(r803_mapping_3, r803_mapping_3_second)
        self.assertIsNot(
            r803_mapping_3["questions"], r803_mapping_3_second["questions"])
        self.assertIsNot(
            r803_mapping_3["answers"], r803_mapping_3_second["answers"])
        self.assertIsNot(
            r803_mapping_3["consequences"], r803_mapping_3_second["consequences"])

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
        r805_float_zero_tuple = module.resolve_dispute(disputed=0.0, journal_records=("journal record one", "journal record two"))
        r805_float_zero_tuple_second = module.resolve_dispute(disputed=0.0, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r805_float_zero_tuple, r805_float_zero_tuple_second)
        self.assertIsNot(
            r805_float_zero_tuple["reconstructed_material"], r805_float_zero_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r805_float_zero_tuple["material_read"], r805_float_zero_tuple_second["material_read"])
        r805_float_zero_omitted = module.resolve_dispute(disputed=0.0)
        r805_float_zero_omitted_second = module.resolve_dispute(disputed=0.0)
        self.assertIsNot(r805_float_zero_omitted, r805_float_zero_omitted_second)
        self.assertIsNot(
            r805_float_zero_omitted["reconstructed_material"], r805_float_zero_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r805_float_zero_omitted["material_read"], r805_float_zero_omitted_second["material_read"])
        r805_float_zero_none = module.resolve_dispute(disputed=0.0, journal_records=None)
        r805_float_zero_none_second = module.resolve_dispute(disputed=0.0, journal_records=None)
        self.assertIsNot(r805_float_zero_none, r805_float_zero_none_second)
        self.assertIsNot(
            r805_float_zero_none["reconstructed_material"], r805_float_zero_none_second["reconstructed_material"])
        self.assertIsNot(
            r805_float_zero_none["material_read"], r805_float_zero_none_second["material_read"])
        r805_empty_list_tuple = module.resolve_dispute(disputed=[], journal_records=("journal record one", "journal record two"))
        r805_empty_list_tuple_second = module.resolve_dispute(disputed=[], journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r805_empty_list_tuple, r805_empty_list_tuple_second)
        self.assertIsNot(
            r805_empty_list_tuple["reconstructed_material"], r805_empty_list_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r805_empty_list_tuple["material_read"], r805_empty_list_tuple_second["material_read"])
        r805_empty_list_omitted = module.resolve_dispute(disputed=[])
        r805_empty_list_omitted_second = module.resolve_dispute(disputed=[])
        self.assertIsNot(r805_empty_list_omitted, r805_empty_list_omitted_second)
        self.assertIsNot(
            r805_empty_list_omitted["reconstructed_material"], r805_empty_list_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r805_empty_list_omitted["material_read"], r805_empty_list_omitted_second["material_read"])
        r805_empty_list_none = module.resolve_dispute(disputed=[], journal_records=None)
        r805_empty_list_none_second = module.resolve_dispute(disputed=[], journal_records=None)
        self.assertIsNot(r805_empty_list_none, r805_empty_list_none_second)
        self.assertIsNot(
            r805_empty_list_none["reconstructed_material"], r805_empty_list_none_second["reconstructed_material"])
        self.assertIsNot(
            r805_empty_list_none["material_read"], r805_empty_list_none_second["material_read"])
        r805_empty_tuple_tuple = module.resolve_dispute(disputed=(), journal_records=("journal record one", "journal record two"))
        r805_empty_tuple_tuple_second = module.resolve_dispute(disputed=(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r805_empty_tuple_tuple, r805_empty_tuple_tuple_second)
        self.assertIsNot(
            r805_empty_tuple_tuple["reconstructed_material"], r805_empty_tuple_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r805_empty_tuple_tuple["material_read"], r805_empty_tuple_tuple_second["material_read"])
        r805_empty_tuple_omitted = module.resolve_dispute(disputed=())
        r805_empty_tuple_omitted_second = module.resolve_dispute(disputed=())
        self.assertIsNot(r805_empty_tuple_omitted, r805_empty_tuple_omitted_second)
        self.assertIsNot(
            r805_empty_tuple_omitted["reconstructed_material"], r805_empty_tuple_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r805_empty_tuple_omitted["material_read"], r805_empty_tuple_omitted_second["material_read"])
        r805_empty_tuple_none = module.resolve_dispute(disputed=(), journal_records=None)
        r805_empty_tuple_none_second = module.resolve_dispute(disputed=(), journal_records=None)
        self.assertIsNot(r805_empty_tuple_none, r805_empty_tuple_none_second)
        self.assertIsNot(
            r805_empty_tuple_none["reconstructed_material"], r805_empty_tuple_none_second["reconstructed_material"])
        self.assertIsNot(
            r805_empty_tuple_none["material_read"], r805_empty_tuple_none_second["material_read"])
        r807_empty_mapping = module.resolve_dispute(disputed={}, journal_records=["journal record one", "journal record two"])
        r807_empty_mapping_second = module.resolve_dispute(disputed={}, journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r807_empty_mapping, r807_empty_mapping_second)
        self.assertIsNot(
            r807_empty_mapping["reconstructed_material"], r807_empty_mapping_second["reconstructed_material"])
        self.assertIsNot(
            r807_empty_mapping["material_read"], r807_empty_mapping_second["material_read"])
        r807_empty_bytes = module.resolve_dispute(disputed=b"", journal_records=["journal record one", "journal record two"])
        r807_empty_bytes_second = module.resolve_dispute(disputed=b"", journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r807_empty_bytes, r807_empty_bytes_second)
        self.assertIsNot(
            r807_empty_bytes["reconstructed_material"], r807_empty_bytes_second["reconstructed_material"])
        self.assertIsNot(
            r807_empty_bytes["material_read"], r807_empty_bytes_second["material_read"])
        r807_empty_set = module.resolve_dispute(disputed=set(), journal_records=["journal record one", "journal record two"])
        r807_empty_set_second = module.resolve_dispute(disputed=set(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r807_empty_set, r807_empty_set_second)
        self.assertIsNot(
            r807_empty_set["reconstructed_material"], r807_empty_set_second["reconstructed_material"])
        self.assertIsNot(
            r807_empty_set["material_read"], r807_empty_set_second["material_read"])
        r864_bytearray = module.resolve_dispute(disputed=bytearray(), journal_records=["journal record one", "journal record two"])
        r864_bytearray_second = module.resolve_dispute(disputed=bytearray(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r864_bytearray, r864_bytearray_second)
        self.assertIsNot(
            r864_bytearray["reconstructed_material"], r864_bytearray_second["reconstructed_material"])
        self.assertIsNot(
            r864_bytearray["material_read"], r864_bytearray_second["material_read"])
        r864_complex = module.resolve_dispute(disputed=0j, journal_records=["journal record one", "journal record two"])
        r864_complex_second = module.resolve_dispute(disputed=0j, journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r864_complex, r864_complex_second)
        self.assertIsNot(
            r864_complex["reconstructed_material"], r864_complex_second["reconstructed_material"])
        self.assertIsNot(
            r864_complex["material_read"], r864_complex_second["material_read"])
        r864_decimal = module.resolve_dispute(disputed=Decimal(0), journal_records=["journal record one", "journal record two"])
        r864_decimal_second = module.resolve_dispute(disputed=Decimal(0), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r864_decimal, r864_decimal_second)
        self.assertIsNot(
            r864_decimal["reconstructed_material"], r864_decimal_second["reconstructed_material"])
        self.assertIsNot(
            r864_decimal["material_read"], r864_decimal_second["material_read"])
        r864_frozenset = module.resolve_dispute(disputed=frozenset(), journal_records=["journal record one", "journal record two"])
        r864_frozenset_second = module.resolve_dispute(disputed=frozenset(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r864_frozenset, r864_frozenset_second)
        self.assertIsNot(
            r864_frozenset["reconstructed_material"], r864_frozenset_second["reconstructed_material"])
        self.assertIsNot(
            r864_frozenset["material_read"], r864_frozenset_second["material_read"])
        r864_range = module.resolve_dispute(disputed=range(0), journal_records=["journal record one", "journal record two"])
        r864_range_second = module.resolve_dispute(disputed=range(0), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r864_range, r864_range_second)
        self.assertIsNot(
            r864_range["reconstructed_material"], r864_range_second["reconstructed_material"])
        self.assertIsNot(
            r864_range["material_read"], r864_range_second["material_read"])
        r871_empty_mapping_tuple = module.resolve_dispute(disputed={}, journal_records=("journal record one", "journal record two"))
        r871_empty_mapping_tuple_second = module.resolve_dispute(disputed={}, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r871_empty_mapping_tuple, r871_empty_mapping_tuple_second)
        self.assertIsNot(
            r871_empty_mapping_tuple["reconstructed_material"], r871_empty_mapping_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_mapping_tuple["material_read"], r871_empty_mapping_tuple_second["material_read"])
        r871_empty_mapping_omitted = module.resolve_dispute(disputed={})
        r871_empty_mapping_omitted_second = module.resolve_dispute(disputed={})
        self.assertIsNot(r871_empty_mapping_omitted, r871_empty_mapping_omitted_second)
        self.assertIsNot(
            r871_empty_mapping_omitted["reconstructed_material"], r871_empty_mapping_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_mapping_omitted["material_read"], r871_empty_mapping_omitted_second["material_read"])
        r871_empty_mapping_none = module.resolve_dispute(disputed={}, journal_records=None)
        r871_empty_mapping_none_second = module.resolve_dispute(disputed={}, journal_records=None)
        self.assertIsNot(r871_empty_mapping_none, r871_empty_mapping_none_second)
        self.assertIsNot(
            r871_empty_mapping_none["reconstructed_material"], r871_empty_mapping_none_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_mapping_none["material_read"], r871_empty_mapping_none_second["material_read"])
        r871_empty_bytes_tuple = module.resolve_dispute(disputed=b"", journal_records=("journal record one", "journal record two"))
        r871_empty_bytes_tuple_second = module.resolve_dispute(disputed=b"", journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r871_empty_bytes_tuple, r871_empty_bytes_tuple_second)
        self.assertIsNot(
            r871_empty_bytes_tuple["reconstructed_material"], r871_empty_bytes_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_bytes_tuple["material_read"], r871_empty_bytes_tuple_second["material_read"])
        r871_empty_bytes_omitted = module.resolve_dispute(disputed=b"")
        r871_empty_bytes_omitted_second = module.resolve_dispute(disputed=b"")
        self.assertIsNot(r871_empty_bytes_omitted, r871_empty_bytes_omitted_second)
        self.assertIsNot(
            r871_empty_bytes_omitted["reconstructed_material"], r871_empty_bytes_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_bytes_omitted["material_read"], r871_empty_bytes_omitted_second["material_read"])
        r871_empty_bytes_none = module.resolve_dispute(disputed=b"", journal_records=None)
        r871_empty_bytes_none_second = module.resolve_dispute(disputed=b"", journal_records=None)
        self.assertIsNot(r871_empty_bytes_none, r871_empty_bytes_none_second)
        self.assertIsNot(
            r871_empty_bytes_none["reconstructed_material"], r871_empty_bytes_none_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_bytes_none["material_read"], r871_empty_bytes_none_second["material_read"])
        r871_empty_set_tuple = module.resolve_dispute(disputed=set(), journal_records=("journal record one", "journal record two"))
        r871_empty_set_tuple_second = module.resolve_dispute(disputed=set(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r871_empty_set_tuple, r871_empty_set_tuple_second)
        self.assertIsNot(
            r871_empty_set_tuple["reconstructed_material"], r871_empty_set_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_set_tuple["material_read"], r871_empty_set_tuple_second["material_read"])
        r871_empty_set_omitted = module.resolve_dispute(disputed=set())
        r871_empty_set_omitted_second = module.resolve_dispute(disputed=set())
        self.assertIsNot(r871_empty_set_omitted, r871_empty_set_omitted_second)
        self.assertIsNot(
            r871_empty_set_omitted["reconstructed_material"], r871_empty_set_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_set_omitted["material_read"], r871_empty_set_omitted_second["material_read"])
        r871_empty_set_none = module.resolve_dispute(disputed=set(), journal_records=None)
        r871_empty_set_none_second = module.resolve_dispute(disputed=set(), journal_records=None)
        self.assertIsNot(r871_empty_set_none, r871_empty_set_none_second)
        self.assertIsNot(
            r871_empty_set_none["reconstructed_material"], r871_empty_set_none_second["reconstructed_material"])
        self.assertIsNot(
            r871_empty_set_none["material_read"], r871_empty_set_none_second["material_read"])

        r922_memoryview = module.resolve_dispute(disputed=memoryview(b""), journal_records=["journal record one", "journal record two"])
        r922_memoryview_second = module.resolve_dispute(disputed=memoryview(b""), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r922_memoryview, r922_memoryview_second)
        self.assertIsNot(
            r922_memoryview["reconstructed_material"], r922_memoryview_second["reconstructed_material"])
        self.assertIsNot(
            r922_memoryview["material_read"], r922_memoryview_second["material_read"])
        r922_fraction = module.resolve_dispute(disputed=Fraction(0), journal_records=["journal record one", "journal record two"])
        r922_fraction_second = module.resolve_dispute(disputed=Fraction(0), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r922_fraction, r922_fraction_second)
        self.assertIsNot(
            r922_fraction["reconstructed_material"], r922_fraction_second["reconstructed_material"])
        self.assertIsNot(
            r922_fraction["material_read"], r922_fraction_second["material_read"])
        r922_deque = module.resolve_dispute(disputed=deque(), journal_records=["journal record one", "journal record two"])
        r922_deque_second = module.resolve_dispute(disputed=deque(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r922_deque, r922_deque_second)
        self.assertIsNot(
            r922_deque["reconstructed_material"], r922_deque_second["reconstructed_material"])
        self.assertIsNot(
            r922_deque["material_read"], r922_deque_second["material_read"])
        r922_counter = module.resolve_dispute(disputed=Counter(), journal_records=["journal record one", "journal record two"])
        r922_counter_second = module.resolve_dispute(disputed=Counter(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r922_counter, r922_counter_second)
        self.assertIsNot(
            r922_counter["reconstructed_material"], r922_counter_second["reconstructed_material"])
        self.assertIsNot(
            r922_counter["material_read"], r922_counter_second["material_read"])
        r922_ordered = module.resolve_dispute(disputed=OrderedDict(), journal_records=["journal record one", "journal record two"])
        r922_ordered_second = module.resolve_dispute(disputed=OrderedDict(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r922_ordered, r922_ordered_second)
        self.assertIsNot(
            r922_ordered["reconstructed_material"], r922_ordered_second["reconstructed_material"])
        self.assertIsNot(
            r922_ordered["material_read"], r922_ordered_second["material_read"])
        r930_bytearray_tuple = module.resolve_dispute(disputed=bytearray(), journal_records=("journal record one", "journal record two"))
        r930_bytearray_tuple_second = module.resolve_dispute(disputed=bytearray(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r930_bytearray_tuple, r930_bytearray_tuple_second)
        self.assertIsNot(
            r930_bytearray_tuple["reconstructed_material"], r930_bytearray_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r930_bytearray_tuple["material_read"], r930_bytearray_tuple_second["material_read"])
        r930_bytearray_omitted = module.resolve_dispute(disputed=bytearray())
        r930_bytearray_omitted_second = module.resolve_dispute(disputed=bytearray())
        self.assertIsNot(r930_bytearray_omitted, r930_bytearray_omitted_second)
        self.assertIsNot(
            r930_bytearray_omitted["reconstructed_material"], r930_bytearray_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r930_bytearray_omitted["material_read"], r930_bytearray_omitted_second["material_read"])
        r930_bytearray_none = module.resolve_dispute(disputed=bytearray(), journal_records=None)
        r930_bytearray_none_second = module.resolve_dispute(disputed=bytearray(), journal_records=None)
        self.assertIsNot(r930_bytearray_none, r930_bytearray_none_second)
        self.assertIsNot(
            r930_bytearray_none["reconstructed_material"], r930_bytearray_none_second["reconstructed_material"])
        self.assertIsNot(
            r930_bytearray_none["material_read"], r930_bytearray_none_second["material_read"])
        r930_complex_tuple = module.resolve_dispute(disputed=0j, journal_records=("journal record one", "journal record two"))
        r930_complex_tuple_second = module.resolve_dispute(disputed=0j, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r930_complex_tuple, r930_complex_tuple_second)
        self.assertIsNot(
            r930_complex_tuple["reconstructed_material"], r930_complex_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r930_complex_tuple["material_read"], r930_complex_tuple_second["material_read"])
        r930_complex_omitted = module.resolve_dispute(disputed=0j)
        r930_complex_omitted_second = module.resolve_dispute(disputed=0j)
        self.assertIsNot(r930_complex_omitted, r930_complex_omitted_second)
        self.assertIsNot(
            r930_complex_omitted["reconstructed_material"], r930_complex_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r930_complex_omitted["material_read"], r930_complex_omitted_second["material_read"])
        r930_complex_none = module.resolve_dispute(disputed=0j, journal_records=None)
        r930_complex_none_second = module.resolve_dispute(disputed=0j, journal_records=None)
        self.assertIsNot(r930_complex_none, r930_complex_none_second)
        self.assertIsNot(
            r930_complex_none["reconstructed_material"], r930_complex_none_second["reconstructed_material"])
        self.assertIsNot(
            r930_complex_none["material_read"], r930_complex_none_second["material_read"])
        r930_decimal_tuple = module.resolve_dispute(disputed=Decimal(0), journal_records=("journal record one", "journal record two"))
        r930_decimal_tuple_second = module.resolve_dispute(disputed=Decimal(0), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r930_decimal_tuple, r930_decimal_tuple_second)
        self.assertIsNot(
            r930_decimal_tuple["reconstructed_material"], r930_decimal_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r930_decimal_tuple["material_read"], r930_decimal_tuple_second["material_read"])
        r930_decimal_omitted = module.resolve_dispute(disputed=Decimal(0))
        r930_decimal_omitted_second = module.resolve_dispute(disputed=Decimal(0))
        self.assertIsNot(r930_decimal_omitted, r930_decimal_omitted_second)
        self.assertIsNot(
            r930_decimal_omitted["reconstructed_material"], r930_decimal_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r930_decimal_omitted["material_read"], r930_decimal_omitted_second["material_read"])
        r930_decimal_none = module.resolve_dispute(disputed=Decimal(0), journal_records=None)
        r930_decimal_none_second = module.resolve_dispute(disputed=Decimal(0), journal_records=None)
        self.assertIsNot(r930_decimal_none, r930_decimal_none_second)
        self.assertIsNot(
            r930_decimal_none["reconstructed_material"], r930_decimal_none_second["reconstructed_material"])
        self.assertIsNot(
            r930_decimal_none["material_read"], r930_decimal_none_second["material_read"])
        r930_frozenset_tuple = module.resolve_dispute(disputed=frozenset(), journal_records=("journal record one", "journal record two"))
        r930_frozenset_tuple_second = module.resolve_dispute(disputed=frozenset(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r930_frozenset_tuple, r930_frozenset_tuple_second)
        self.assertIsNot(
            r930_frozenset_tuple["reconstructed_material"], r930_frozenset_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r930_frozenset_tuple["material_read"], r930_frozenset_tuple_second["material_read"])
        r930_frozenset_omitted = module.resolve_dispute(disputed=frozenset())
        r930_frozenset_omitted_second = module.resolve_dispute(disputed=frozenset())
        self.assertIsNot(r930_frozenset_omitted, r930_frozenset_omitted_second)
        self.assertIsNot(
            r930_frozenset_omitted["reconstructed_material"], r930_frozenset_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r930_frozenset_omitted["material_read"], r930_frozenset_omitted_second["material_read"])
        r930_frozenset_none = module.resolve_dispute(disputed=frozenset(), journal_records=None)
        r930_frozenset_none_second = module.resolve_dispute(disputed=frozenset(), journal_records=None)
        self.assertIsNot(r930_frozenset_none, r930_frozenset_none_second)
        self.assertIsNot(
            r930_frozenset_none["reconstructed_material"], r930_frozenset_none_second["reconstructed_material"])
        self.assertIsNot(
            r930_frozenset_none["material_read"], r930_frozenset_none_second["material_read"])
        r930_range_tuple = module.resolve_dispute(disputed=range(0), journal_records=("journal record one", "journal record two"))
        r930_range_tuple_second = module.resolve_dispute(disputed=range(0), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r930_range_tuple, r930_range_tuple_second)
        self.assertIsNot(
            r930_range_tuple["reconstructed_material"], r930_range_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r930_range_tuple["material_read"], r930_range_tuple_second["material_read"])
        r930_range_omitted = module.resolve_dispute(disputed=range(0))
        r930_range_omitted_second = module.resolve_dispute(disputed=range(0))
        self.assertIsNot(r930_range_omitted, r930_range_omitted_second)
        self.assertIsNot(
            r930_range_omitted["reconstructed_material"], r930_range_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r930_range_omitted["material_read"], r930_range_omitted_second["material_read"])
        r930_range_none = module.resolve_dispute(disputed=range(0), journal_records=None)
        r930_range_none_second = module.resolve_dispute(disputed=range(0), journal_records=None)
        self.assertIsNot(r930_range_none, r930_range_none_second)
        self.assertIsNot(
            r930_range_none["reconstructed_material"], r930_range_none_second["reconstructed_material"])
        self.assertIsNot(
            r930_range_none["material_read"], r930_range_none_second["material_read"])
        r978_array = module.resolve_dispute(disputed=array("i", []), journal_records=["journal record one", "journal record two"])
        r978_array_second = module.resolve_dispute(disputed=array("i", []), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r978_array, r978_array_second)
        self.assertIsNot(
            r978_array["reconstructed_material"], r978_array_second["reconstructed_material"])
        self.assertIsNot(
            r978_array["material_read"], r978_array_second["material_read"])
        r978_chainmap = module.resolve_dispute(disputed=ChainMap(), journal_records=["journal record one", "journal record two"])
        r978_chainmap_second = module.resolve_dispute(disputed=ChainMap(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r978_chainmap, r978_chainmap_second)
        self.assertIsNot(
            r978_chainmap["reconstructed_material"], r978_chainmap_second["reconstructed_material"])
        self.assertIsNot(
            r978_chainmap["material_read"], r978_chainmap_second["material_read"])
        r978_defaultdict = module.resolve_dispute(disputed=defaultdict(int), journal_records=["journal record one", "journal record two"])
        r978_defaultdict_second = module.resolve_dispute(disputed=defaultdict(int), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r978_defaultdict, r978_defaultdict_second)
        self.assertIsNot(
            r978_defaultdict["reconstructed_material"], r978_defaultdict_second["reconstructed_material"])
        self.assertIsNot(
            r978_defaultdict["material_read"], r978_defaultdict_second["material_read"])
        r978_timedelta = module.resolve_dispute(disputed=timedelta(0), journal_records=["journal record one", "journal record two"])
        r978_timedelta_second = module.resolve_dispute(disputed=timedelta(0), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r978_timedelta, r978_timedelta_second)
        self.assertIsNot(
            r978_timedelta["reconstructed_material"], r978_timedelta_second["reconstructed_material"])
        self.assertIsNot(
            r978_timedelta["material_read"], r978_timedelta_second["material_read"])
        r978_userdict = module.resolve_dispute(disputed=UserDict(), journal_records=["journal record one", "journal record two"])
        r978_userdict_second = module.resolve_dispute(disputed=UserDict(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r978_userdict, r978_userdict_second)
        self.assertIsNot(
            r978_userdict["reconstructed_material"], r978_userdict_second["reconstructed_material"])
        self.assertIsNot(
            r978_userdict["material_read"], r978_userdict_second["material_read"])
        r985_memoryview_tuple = module.resolve_dispute(disputed=memoryview(b""), journal_records=("journal record one", "journal record two"))
        r985_memoryview_tuple_second = module.resolve_dispute(disputed=memoryview(b""), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r985_memoryview_tuple, r985_memoryview_tuple_second)
        self.assertIsNot(
            r985_memoryview_tuple["reconstructed_material"], r985_memoryview_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r985_memoryview_tuple["material_read"], r985_memoryview_tuple_second["material_read"])
        r985_memoryview_omitted = module.resolve_dispute(disputed=memoryview(b""))
        r985_memoryview_omitted_second = module.resolve_dispute(disputed=memoryview(b""))
        self.assertIsNot(r985_memoryview_omitted, r985_memoryview_omitted_second)
        self.assertIsNot(
            r985_memoryview_omitted["reconstructed_material"], r985_memoryview_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r985_memoryview_omitted["material_read"], r985_memoryview_omitted_second["material_read"])
        r985_memoryview_none = module.resolve_dispute(disputed=memoryview(b""), journal_records=None)
        r985_memoryview_none_second = module.resolve_dispute(disputed=memoryview(b""), journal_records=None)
        self.assertIsNot(r985_memoryview_none, r985_memoryview_none_second)
        self.assertIsNot(
            r985_memoryview_none["reconstructed_material"], r985_memoryview_none_second["reconstructed_material"])
        self.assertIsNot(
            r985_memoryview_none["material_read"], r985_memoryview_none_second["material_read"])
        r985_fraction_tuple = module.resolve_dispute(disputed=Fraction(0), journal_records=("journal record one", "journal record two"))
        r985_fraction_tuple_second = module.resolve_dispute(disputed=Fraction(0), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r985_fraction_tuple, r985_fraction_tuple_second)
        self.assertIsNot(
            r985_fraction_tuple["reconstructed_material"], r985_fraction_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r985_fraction_tuple["material_read"], r985_fraction_tuple_second["material_read"])
        r985_fraction_omitted = module.resolve_dispute(disputed=Fraction(0))
        r985_fraction_omitted_second = module.resolve_dispute(disputed=Fraction(0))
        self.assertIsNot(r985_fraction_omitted, r985_fraction_omitted_second)
        self.assertIsNot(
            r985_fraction_omitted["reconstructed_material"], r985_fraction_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r985_fraction_omitted["material_read"], r985_fraction_omitted_second["material_read"])
        r985_fraction_none = module.resolve_dispute(disputed=Fraction(0), journal_records=None)
        r985_fraction_none_second = module.resolve_dispute(disputed=Fraction(0), journal_records=None)
        self.assertIsNot(r985_fraction_none, r985_fraction_none_second)
        self.assertIsNot(
            r985_fraction_none["reconstructed_material"], r985_fraction_none_second["reconstructed_material"])
        self.assertIsNot(
            r985_fraction_none["material_read"], r985_fraction_none_second["material_read"])
        r985_deque_tuple = module.resolve_dispute(disputed=deque(), journal_records=("journal record one", "journal record two"))
        r985_deque_tuple_second = module.resolve_dispute(disputed=deque(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r985_deque_tuple, r985_deque_tuple_second)
        self.assertIsNot(
            r985_deque_tuple["reconstructed_material"], r985_deque_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r985_deque_tuple["material_read"], r985_deque_tuple_second["material_read"])
        r985_deque_omitted = module.resolve_dispute(disputed=deque())
        r985_deque_omitted_second = module.resolve_dispute(disputed=deque())
        self.assertIsNot(r985_deque_omitted, r985_deque_omitted_second)
        self.assertIsNot(
            r985_deque_omitted["reconstructed_material"], r985_deque_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r985_deque_omitted["material_read"], r985_deque_omitted_second["material_read"])
        r985_deque_none = module.resolve_dispute(disputed=deque(), journal_records=None)
        r985_deque_none_second = module.resolve_dispute(disputed=deque(), journal_records=None)
        self.assertIsNot(r985_deque_none, r985_deque_none_second)
        self.assertIsNot(
            r985_deque_none["reconstructed_material"], r985_deque_none_second["reconstructed_material"])
        self.assertIsNot(
            r985_deque_none["material_read"], r985_deque_none_second["material_read"])
        r985_counter_tuple = module.resolve_dispute(disputed=Counter(), journal_records=("journal record one", "journal record two"))
        r985_counter_tuple_second = module.resolve_dispute(disputed=Counter(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r985_counter_tuple, r985_counter_tuple_second)
        self.assertIsNot(
            r985_counter_tuple["reconstructed_material"], r985_counter_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r985_counter_tuple["material_read"], r985_counter_tuple_second["material_read"])
        r985_counter_omitted = module.resolve_dispute(disputed=Counter())
        r985_counter_omitted_second = module.resolve_dispute(disputed=Counter())
        self.assertIsNot(r985_counter_omitted, r985_counter_omitted_second)
        self.assertIsNot(
            r985_counter_omitted["reconstructed_material"], r985_counter_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r985_counter_omitted["material_read"], r985_counter_omitted_second["material_read"])
        r985_counter_none = module.resolve_dispute(disputed=Counter(), journal_records=None)
        r985_counter_none_second = module.resolve_dispute(disputed=Counter(), journal_records=None)
        self.assertIsNot(r985_counter_none, r985_counter_none_second)
        self.assertIsNot(
            r985_counter_none["reconstructed_material"], r985_counter_none_second["reconstructed_material"])
        self.assertIsNot(
            r985_counter_none["material_read"], r985_counter_none_second["material_read"])
        r985_ordered_tuple = module.resolve_dispute(disputed=OrderedDict(), journal_records=("journal record one", "journal record two"))
        r985_ordered_tuple_second = module.resolve_dispute(disputed=OrderedDict(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r985_ordered_tuple, r985_ordered_tuple_second)
        self.assertIsNot(
            r985_ordered_tuple["reconstructed_material"], r985_ordered_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r985_ordered_tuple["material_read"], r985_ordered_tuple_second["material_read"])
        r985_ordered_omitted = module.resolve_dispute(disputed=OrderedDict())
        r985_ordered_omitted_second = module.resolve_dispute(disputed=OrderedDict())
        self.assertIsNot(r985_ordered_omitted, r985_ordered_omitted_second)
        self.assertIsNot(
            r985_ordered_omitted["reconstructed_material"], r985_ordered_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r985_ordered_omitted["material_read"], r985_ordered_omitted_second["material_read"])
        r985_ordered_none = module.resolve_dispute(disputed=OrderedDict(), journal_records=None)
        r985_ordered_none_second = module.resolve_dispute(disputed=OrderedDict(), journal_records=None)
        self.assertIsNot(r985_ordered_none, r985_ordered_none_second)
        self.assertIsNot(
            r985_ordered_none["reconstructed_material"], r985_ordered_none_second["reconstructed_material"])
        self.assertIsNot(
            r985_ordered_none["material_read"], r985_ordered_none_second["material_read"])
        r1048_proxy = module.resolve_dispute(disputed=MappingProxyType({}), journal_records=["journal record one", "journal record two"])
        r1048_proxy_second = module.resolve_dispute(disputed=MappingProxyType({}), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1048_proxy, r1048_proxy_second)
        self.assertIsNot(
            r1048_proxy["reconstructed_material"], r1048_proxy_second["reconstructed_material"])
        self.assertIsNot(
            r1048_proxy["material_read"], r1048_proxy_second["material_read"])
        r1048_namedtuple = module.resolve_dispute(disputed=namedtuple("R1048Tuple", [])(), journal_records=["journal record one", "journal record two"])
        r1048_namedtuple_second = module.resolve_dispute(disputed=namedtuple("R1048Tuple", [])(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1048_namedtuple, r1048_namedtuple_second)
        self.assertIsNot(
            r1048_namedtuple["reconstructed_material"], r1048_namedtuple_second["reconstructed_material"])
        self.assertIsNot(
            r1048_namedtuple["material_read"], r1048_namedtuple_second["material_read"])
        r1048_keys = module.resolve_dispute(disputed={}.keys(), journal_records=["journal record one", "journal record two"])
        r1048_keys_second = module.resolve_dispute(disputed={}.keys(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1048_keys, r1048_keys_second)
        self.assertIsNot(
            r1048_keys["reconstructed_material"], r1048_keys_second["reconstructed_material"])
        self.assertIsNot(
            r1048_keys["material_read"], r1048_keys_second["material_read"])
        r1048_values = module.resolve_dispute(disputed={}.values(), journal_records=["journal record one", "journal record two"])
        r1048_values_second = module.resolve_dispute(disputed={}.values(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1048_values, r1048_values_second)
        self.assertIsNot(
            r1048_values["reconstructed_material"], r1048_values_second["reconstructed_material"])
        self.assertIsNot(
            r1048_values["material_read"], r1048_values_second["material_read"])
        r1048_intenum = module.resolve_dispute(disputed=IntEnum("R1048Enum", {"member": 0}).member, journal_records=["journal record one", "journal record two"])
        r1048_intenum_second = module.resolve_dispute(disputed=IntEnum("R1048Enum", {"member": 0}).member, journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1048_intenum, r1048_intenum_second)
        self.assertIsNot(
            r1048_intenum["reconstructed_material"], r1048_intenum_second["reconstructed_material"])
        self.assertIsNot(
            r1048_intenum["material_read"], r1048_intenum_second["material_read"])
        r1061_userlist_empty = module.resolve_dispute(disputed=UserList([]), journal_records=["journal record one", "journal record two"])
        r1061_userlist_empty_second = module.resolve_dispute(disputed=UserList([]), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1061_userlist_empty, r1061_userlist_empty_second)
        self.assertIsNot(
            r1061_userlist_empty["reconstructed_material"], r1061_userlist_empty_second["reconstructed_material"])
        self.assertIsNot(
            r1061_userlist_empty["material_read"], r1061_userlist_empty_second["material_read"])
        r1061_userstring_empty = module.resolve_dispute(disputed=UserString(""), journal_records=["journal record one", "journal record two"])
        r1061_userstring_empty_second = module.resolve_dispute(disputed=UserString(""), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1061_userstring_empty, r1061_userstring_empty_second)
        self.assertIsNot(
            r1061_userstring_empty["reconstructed_material"], r1061_userstring_empty_second["reconstructed_material"])
        self.assertIsNot(
            r1061_userstring_empty["material_read"], r1061_userstring_empty_second["material_read"])
        r1055_array_tuple = module.resolve_dispute(disputed=array("i", []), journal_records=("journal record one", "journal record two"))
        r1055_array_tuple_second = module.resolve_dispute(disputed=array("i", []), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1055_array_tuple, r1055_array_tuple_second)
        self.assertIsNot(
            r1055_array_tuple["reconstructed_material"], r1055_array_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1055_array_tuple["material_read"], r1055_array_tuple_second["material_read"])
        r1055_array_omitted = module.resolve_dispute(disputed=array("i", []))
        r1055_array_omitted_second = module.resolve_dispute(disputed=array("i", []))
        self.assertIsNot(r1055_array_omitted, r1055_array_omitted_second)
        self.assertIsNot(
            r1055_array_omitted["reconstructed_material"], r1055_array_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1055_array_omitted["material_read"], r1055_array_omitted_second["material_read"])
        r1055_array_none = module.resolve_dispute(disputed=array("i", []), journal_records=None)
        r1055_array_none_second = module.resolve_dispute(disputed=array("i", []), journal_records=None)
        self.assertIsNot(r1055_array_none, r1055_array_none_second)
        self.assertIsNot(
            r1055_array_none["reconstructed_material"], r1055_array_none_second["reconstructed_material"])
        self.assertIsNot(
            r1055_array_none["material_read"], r1055_array_none_second["material_read"])
        r1055_chainmap_tuple = module.resolve_dispute(disputed=ChainMap(), journal_records=("journal record one", "journal record two"))
        r1055_chainmap_tuple_second = module.resolve_dispute(disputed=ChainMap(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1055_chainmap_tuple, r1055_chainmap_tuple_second)
        self.assertIsNot(
            r1055_chainmap_tuple["reconstructed_material"], r1055_chainmap_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1055_chainmap_tuple["material_read"], r1055_chainmap_tuple_second["material_read"])
        r1055_chainmap_omitted = module.resolve_dispute(disputed=ChainMap())
        r1055_chainmap_omitted_second = module.resolve_dispute(disputed=ChainMap())
        self.assertIsNot(r1055_chainmap_omitted, r1055_chainmap_omitted_second)
        self.assertIsNot(
            r1055_chainmap_omitted["reconstructed_material"], r1055_chainmap_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1055_chainmap_omitted["material_read"], r1055_chainmap_omitted_second["material_read"])
        r1055_chainmap_none = module.resolve_dispute(disputed=ChainMap(), journal_records=None)
        r1055_chainmap_none_second = module.resolve_dispute(disputed=ChainMap(), journal_records=None)
        self.assertIsNot(r1055_chainmap_none, r1055_chainmap_none_second)
        self.assertIsNot(
            r1055_chainmap_none["reconstructed_material"], r1055_chainmap_none_second["reconstructed_material"])
        self.assertIsNot(
            r1055_chainmap_none["material_read"], r1055_chainmap_none_second["material_read"])
        r1055_defaultdict_tuple = module.resolve_dispute(disputed=defaultdict(int), journal_records=("journal record one", "journal record two"))
        r1055_defaultdict_tuple_second = module.resolve_dispute(disputed=defaultdict(int), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1055_defaultdict_tuple, r1055_defaultdict_tuple_second)
        self.assertIsNot(
            r1055_defaultdict_tuple["reconstructed_material"], r1055_defaultdict_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1055_defaultdict_tuple["material_read"], r1055_defaultdict_tuple_second["material_read"])
        r1055_defaultdict_omitted = module.resolve_dispute(disputed=defaultdict(int))
        r1055_defaultdict_omitted_second = module.resolve_dispute(disputed=defaultdict(int))
        self.assertIsNot(r1055_defaultdict_omitted, r1055_defaultdict_omitted_second)
        self.assertIsNot(
            r1055_defaultdict_omitted["reconstructed_material"], r1055_defaultdict_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1055_defaultdict_omitted["material_read"], r1055_defaultdict_omitted_second["material_read"])
        r1055_defaultdict_none = module.resolve_dispute(disputed=defaultdict(int), journal_records=None)
        r1055_defaultdict_none_second = module.resolve_dispute(disputed=defaultdict(int), journal_records=None)
        self.assertIsNot(r1055_defaultdict_none, r1055_defaultdict_none_second)
        self.assertIsNot(
            r1055_defaultdict_none["reconstructed_material"], r1055_defaultdict_none_second["reconstructed_material"])
        self.assertIsNot(
            r1055_defaultdict_none["material_read"], r1055_defaultdict_none_second["material_read"])
        r1055_timedelta_tuple = module.resolve_dispute(disputed=timedelta(0), journal_records=("journal record one", "journal record two"))
        r1055_timedelta_tuple_second = module.resolve_dispute(disputed=timedelta(0), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1055_timedelta_tuple, r1055_timedelta_tuple_second)
        self.assertIsNot(
            r1055_timedelta_tuple["reconstructed_material"], r1055_timedelta_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1055_timedelta_tuple["material_read"], r1055_timedelta_tuple_second["material_read"])
        r1055_timedelta_omitted = module.resolve_dispute(disputed=timedelta(0))
        r1055_timedelta_omitted_second = module.resolve_dispute(disputed=timedelta(0))
        self.assertIsNot(r1055_timedelta_omitted, r1055_timedelta_omitted_second)
        self.assertIsNot(
            r1055_timedelta_omitted["reconstructed_material"], r1055_timedelta_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1055_timedelta_omitted["material_read"], r1055_timedelta_omitted_second["material_read"])
        r1055_timedelta_none = module.resolve_dispute(disputed=timedelta(0), journal_records=None)
        r1055_timedelta_none_second = module.resolve_dispute(disputed=timedelta(0), journal_records=None)
        self.assertIsNot(r1055_timedelta_none, r1055_timedelta_none_second)
        self.assertIsNot(
            r1055_timedelta_none["reconstructed_material"], r1055_timedelta_none_second["reconstructed_material"])
        self.assertIsNot(
            r1055_timedelta_none["material_read"], r1055_timedelta_none_second["material_read"])
        r1055_userdict_tuple = module.resolve_dispute(disputed=UserDict(), journal_records=("journal record one", "journal record two"))
        r1055_userdict_tuple_second = module.resolve_dispute(disputed=UserDict(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1055_userdict_tuple, r1055_userdict_tuple_second)
        self.assertIsNot(
            r1055_userdict_tuple["reconstructed_material"], r1055_userdict_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1055_userdict_tuple["material_read"], r1055_userdict_tuple_second["material_read"])
        r1055_userdict_omitted = module.resolve_dispute(disputed=UserDict())
        r1055_userdict_omitted_second = module.resolve_dispute(disputed=UserDict())
        self.assertIsNot(r1055_userdict_omitted, r1055_userdict_omitted_second)
        self.assertIsNot(
            r1055_userdict_omitted["reconstructed_material"], r1055_userdict_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1055_userdict_omitted["material_read"], r1055_userdict_omitted_second["material_read"])
        r1055_userdict_none = module.resolve_dispute(disputed=UserDict(), journal_records=None)
        r1055_userdict_none_second = module.resolve_dispute(disputed=UserDict(), journal_records=None)
        self.assertIsNot(r1055_userdict_none, r1055_userdict_none_second)
        self.assertIsNot(
            r1055_userdict_none["reconstructed_material"], r1055_userdict_none_second["reconstructed_material"])
        self.assertIsNot(
            r1055_userdict_none["material_read"], r1055_userdict_none_second["material_read"])

        r1120_items = module.resolve_dispute(disputed={}.items(), journal_records=["journal record one", "journal record two"])
        r1120_items_second = module.resolve_dispute(disputed={}.items(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1120_items, r1120_items_second)
        self.assertIsNot(
            r1120_items["reconstructed_material"], r1120_items_second["reconstructed_material"])
        self.assertIsNot(
            r1120_items["material_read"], r1120_items_second["material_read"])
        r1120_intflag = module.resolve_dispute(disputed=IntFlag("R1120Flag", {"member": 0}).member, journal_records=["journal record one", "journal record two"])
        r1120_intflag_second = module.resolve_dispute(disputed=IntFlag("R1120Flag", {"member": 0}).member, journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1120_intflag, r1120_intflag_second)
        self.assertIsNot(
            r1120_intflag["reconstructed_material"], r1120_intflag_second["reconstructed_material"])
        self.assertIsNot(
            r1120_intflag["material_read"], r1120_intflag_second["material_read"])
        r1120_strenum = module.resolve_dispute(disputed=StrEnum("R1120StrEnum", {"member": ""}).member, journal_records=["journal record one", "journal record two"])
        r1120_strenum_second = module.resolve_dispute(disputed=StrEnum("R1120StrEnum", {"member": ""}).member, journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1120_strenum, r1120_strenum_second)
        self.assertIsNot(
            r1120_strenum["reconstructed_material"], r1120_strenum_second["reconstructed_material"])
        self.assertIsNot(
            r1120_strenum["material_read"], r1120_strenum_second["material_read"])
        r1120_flag = module.resolve_dispute(disputed=Flag("R1120PlainFlag", {"member": 0}).member, journal_records=["journal record one", "journal record two"])
        r1120_flag_second = module.resolve_dispute(disputed=Flag("R1120PlainFlag", {"member": 0}).member, journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1120_flag, r1120_flag_second)
        self.assertIsNot(
            r1120_flag["reconstructed_material"], r1120_flag_second["reconstructed_material"])
        self.assertIsNot(
            r1120_flag["material_read"], r1120_flag_second["material_read"])
        r1129_proxy_tuple = module.resolve_dispute(disputed=MappingProxyType({}), journal_records=("journal record one", "journal record two"))
        r1129_proxy_tuple_second = module.resolve_dispute(disputed=MappingProxyType({}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1129_proxy_tuple, r1129_proxy_tuple_second)
        self.assertIsNot(
            r1129_proxy_tuple["reconstructed_material"], r1129_proxy_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1129_proxy_tuple["material_read"], r1129_proxy_tuple_second["material_read"])
        r1129_proxy_omitted = module.resolve_dispute(disputed=MappingProxyType({}))
        r1129_proxy_omitted_second = module.resolve_dispute(disputed=MappingProxyType({}))
        self.assertIsNot(r1129_proxy_omitted, r1129_proxy_omitted_second)
        self.assertIsNot(
            r1129_proxy_omitted["reconstructed_material"], r1129_proxy_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1129_proxy_omitted["material_read"], r1129_proxy_omitted_second["material_read"])
        r1129_proxy_none = module.resolve_dispute(disputed=MappingProxyType({}), journal_records=None)
        r1129_proxy_none_second = module.resolve_dispute(disputed=MappingProxyType({}), journal_records=None)
        self.assertIsNot(r1129_proxy_none, r1129_proxy_none_second)
        self.assertIsNot(
            r1129_proxy_none["reconstructed_material"], r1129_proxy_none_second["reconstructed_material"])
        self.assertIsNot(
            r1129_proxy_none["material_read"], r1129_proxy_none_second["material_read"])
        r1129_namedtuple_tuple = module.resolve_dispute(disputed=namedtuple("R1129Tuple", [])(), journal_records=("journal record one", "journal record two"))
        r1129_namedtuple_tuple_second = module.resolve_dispute(disputed=namedtuple("R1129Tuple", [])(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1129_namedtuple_tuple, r1129_namedtuple_tuple_second)
        self.assertIsNot(
            r1129_namedtuple_tuple["reconstructed_material"], r1129_namedtuple_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1129_namedtuple_tuple["material_read"], r1129_namedtuple_tuple_second["material_read"])
        r1129_namedtuple_omitted = module.resolve_dispute(disputed=namedtuple("R1129Tuple", [])())
        r1129_namedtuple_omitted_second = module.resolve_dispute(disputed=namedtuple("R1129Tuple", [])())
        self.assertIsNot(r1129_namedtuple_omitted, r1129_namedtuple_omitted_second)
        self.assertIsNot(
            r1129_namedtuple_omitted["reconstructed_material"], r1129_namedtuple_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1129_namedtuple_omitted["material_read"], r1129_namedtuple_omitted_second["material_read"])
        r1129_namedtuple_none = module.resolve_dispute(disputed=namedtuple("R1129Tuple", [])(), journal_records=None)
        r1129_namedtuple_none_second = module.resolve_dispute(disputed=namedtuple("R1129Tuple", [])(), journal_records=None)
        self.assertIsNot(r1129_namedtuple_none, r1129_namedtuple_none_second)
        self.assertIsNot(
            r1129_namedtuple_none["reconstructed_material"], r1129_namedtuple_none_second["reconstructed_material"])
        self.assertIsNot(
            r1129_namedtuple_none["material_read"], r1129_namedtuple_none_second["material_read"])
        r1129_keys_tuple = module.resolve_dispute(disputed={}.keys(), journal_records=("journal record one", "journal record two"))
        r1129_keys_tuple_second = module.resolve_dispute(disputed={}.keys(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1129_keys_tuple, r1129_keys_tuple_second)
        self.assertIsNot(
            r1129_keys_tuple["reconstructed_material"], r1129_keys_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1129_keys_tuple["material_read"], r1129_keys_tuple_second["material_read"])
        r1129_keys_omitted = module.resolve_dispute(disputed={}.keys())
        r1129_keys_omitted_second = module.resolve_dispute(disputed={}.keys())
        self.assertIsNot(r1129_keys_omitted, r1129_keys_omitted_second)
        self.assertIsNot(
            r1129_keys_omitted["reconstructed_material"], r1129_keys_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1129_keys_omitted["material_read"], r1129_keys_omitted_second["material_read"])
        r1129_keys_none = module.resolve_dispute(disputed={}.keys(), journal_records=None)
        r1129_keys_none_second = module.resolve_dispute(disputed={}.keys(), journal_records=None)
        self.assertIsNot(r1129_keys_none, r1129_keys_none_second)
        self.assertIsNot(
            r1129_keys_none["reconstructed_material"], r1129_keys_none_second["reconstructed_material"])
        self.assertIsNot(
            r1129_keys_none["material_read"], r1129_keys_none_second["material_read"])
        r1129_values_tuple = module.resolve_dispute(disputed={}.values(), journal_records=("journal record one", "journal record two"))
        r1129_values_tuple_second = module.resolve_dispute(disputed={}.values(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1129_values_tuple, r1129_values_tuple_second)
        self.assertIsNot(
            r1129_values_tuple["reconstructed_material"], r1129_values_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1129_values_tuple["material_read"], r1129_values_tuple_second["material_read"])
        r1129_values_omitted = module.resolve_dispute(disputed={}.values())
        r1129_values_omitted_second = module.resolve_dispute(disputed={}.values())
        self.assertIsNot(r1129_values_omitted, r1129_values_omitted_second)
        self.assertIsNot(
            r1129_values_omitted["reconstructed_material"], r1129_values_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1129_values_omitted["material_read"], r1129_values_omitted_second["material_read"])
        r1129_values_none = module.resolve_dispute(disputed={}.values(), journal_records=None)
        r1129_values_none_second = module.resolve_dispute(disputed={}.values(), journal_records=None)
        self.assertIsNot(r1129_values_none, r1129_values_none_second)
        self.assertIsNot(
            r1129_values_none["reconstructed_material"], r1129_values_none_second["reconstructed_material"])
        self.assertIsNot(
            r1129_values_none["material_read"], r1129_values_none_second["material_read"])
        r1129_intenum_tuple = module.resolve_dispute(disputed=IntEnum("R1129Enum", {"member": 0}).member, journal_records=("journal record one", "journal record two"))
        r1129_intenum_tuple_second = module.resolve_dispute(disputed=IntEnum("R1129Enum", {"member": 0}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1129_intenum_tuple, r1129_intenum_tuple_second)
        self.assertIsNot(
            r1129_intenum_tuple["reconstructed_material"], r1129_intenum_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1129_intenum_tuple["material_read"], r1129_intenum_tuple_second["material_read"])
        r1129_intenum_omitted = module.resolve_dispute(disputed=IntEnum("R1129Enum", {"member": 0}).member)
        r1129_intenum_omitted_second = module.resolve_dispute(disputed=IntEnum("R1129Enum", {"member": 0}).member)
        self.assertIsNot(r1129_intenum_omitted, r1129_intenum_omitted_second)
        self.assertIsNot(
            r1129_intenum_omitted["reconstructed_material"], r1129_intenum_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1129_intenum_omitted["material_read"], r1129_intenum_omitted_second["material_read"])
        r1129_intenum_none = module.resolve_dispute(disputed=IntEnum("R1129Enum", {"member": 0}).member, journal_records=None)
        r1129_intenum_none_second = module.resolve_dispute(disputed=IntEnum("R1129Enum", {"member": 0}).member, journal_records=None)
        self.assertIsNot(r1129_intenum_none, r1129_intenum_none_second)
        self.assertIsNot(
            r1129_intenum_none["reconstructed_material"], r1129_intenum_none_second["reconstructed_material"])
        self.assertIsNot(
            r1129_intenum_none["material_read"], r1129_intenum_none_second["material_read"])
        r1135_userlist_tuple = module.resolve_dispute(disputed=UserList([]), journal_records=("journal record one", "journal record two"))
        r1135_userlist_tuple_second = module.resolve_dispute(disputed=UserList([]), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1135_userlist_tuple, r1135_userlist_tuple_second)
        self.assertIsNot(
            r1135_userlist_tuple["reconstructed_material"], r1135_userlist_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userlist_tuple["material_read"], r1135_userlist_tuple_second["material_read"])
        r1135_userlist_omitted = module.resolve_dispute(disputed=UserList([]))
        r1135_userlist_omitted_second = module.resolve_dispute(disputed=UserList([]))
        self.assertIsNot(r1135_userlist_omitted, r1135_userlist_omitted_second)
        self.assertIsNot(
            r1135_userlist_omitted["reconstructed_material"], r1135_userlist_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userlist_omitted["material_read"], r1135_userlist_omitted_second["material_read"])
        r1135_userlist_none = module.resolve_dispute(disputed=UserList([]), journal_records=None)
        r1135_userlist_none_second = module.resolve_dispute(disputed=UserList([]), journal_records=None)
        self.assertIsNot(r1135_userlist_none, r1135_userlist_none_second)
        self.assertIsNot(
            r1135_userlist_none["reconstructed_material"], r1135_userlist_none_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userlist_none["material_read"], r1135_userlist_none_second["material_read"])
        r1135_userstring_tuple = module.resolve_dispute(disputed=UserString(""), journal_records=("journal record one", "journal record two"))
        r1135_userstring_tuple_second = module.resolve_dispute(disputed=UserString(""), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1135_userstring_tuple, r1135_userstring_tuple_second)
        self.assertIsNot(
            r1135_userstring_tuple["reconstructed_material"], r1135_userstring_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userstring_tuple["material_read"], r1135_userstring_tuple_second["material_read"])
        r1135_userstring_omitted = module.resolve_dispute(disputed=UserString(""))
        r1135_userstring_omitted_second = module.resolve_dispute(disputed=UserString(""))
        self.assertIsNot(r1135_userstring_omitted, r1135_userstring_omitted_second)
        self.assertIsNot(
            r1135_userstring_omitted["reconstructed_material"], r1135_userstring_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userstring_omitted["material_read"], r1135_userstring_omitted_second["material_read"])
        r1135_userstring_none = module.resolve_dispute(disputed=UserString(""), journal_records=None)
        r1135_userstring_none_second = module.resolve_dispute(disputed=UserString(""), journal_records=None)
        self.assertIsNot(r1135_userstring_none, r1135_userstring_none_second)
        self.assertIsNot(
            r1135_userstring_none["reconstructed_material"], r1135_userstring_none_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userstring_none["material_read"], r1135_userstring_none_second["material_read"])

        r1213_element = module.resolve_dispute(disputed=Element("tag"), journal_records=["journal record one", "journal record two"])
        r1213_element_second = module.resolve_dispute(disputed=Element("tag"), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1213_element, r1213_element_second)
        self.assertIsNot(
            r1213_element["reconstructed_material"], r1213_element_second["reconstructed_material"])
        self.assertIsNot(
            r1213_element["material_read"], r1213_element_second["material_read"])
        r1213_weakset = module.resolve_dispute(disputed=WeakSet(), journal_records=["journal record one", "journal record two"])
        r1213_weakset_second = module.resolve_dispute(disputed=WeakSet(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1213_weakset, r1213_weakset_second)
        self.assertIsNot(
            r1213_weakset["reconstructed_material"], r1213_weakset_second["reconstructed_material"])
        self.assertIsNot(
            r1213_weakset["material_read"], r1213_weakset_second["material_read"])
        r1213_weakkey = module.resolve_dispute(disputed=WeakKeyDictionary(), journal_records=["journal record one", "journal record two"])
        r1213_weakkey_second = module.resolve_dispute(disputed=WeakKeyDictionary(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1213_weakkey, r1213_weakkey_second)
        self.assertIsNot(
            r1213_weakkey["reconstructed_material"], r1213_weakkey_second["reconstructed_material"])
        self.assertIsNot(
            r1213_weakkey["material_read"], r1213_weakkey_second["material_read"])
        r1213_weakvalue = module.resolve_dispute(disputed=WeakValueDictionary(), journal_records=["journal record one", "journal record two"])
        r1213_weakvalue_second = module.resolve_dispute(disputed=WeakValueDictionary(), journal_records=["journal record one", "journal record two"])
        self.assertIsNot(r1213_weakvalue, r1213_weakvalue_second)
        self.assertIsNot(
            r1213_weakvalue["reconstructed_material"], r1213_weakvalue_second["reconstructed_material"])
        self.assertIsNot(
            r1213_weakvalue["material_read"], r1213_weakvalue_second["material_read"])

        r1222_items_tuple = module.resolve_dispute(disputed={}.items(), journal_records=("journal record one", "journal record two"))
        r1222_items_tuple_second = module.resolve_dispute(disputed={}.items(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1222_items_tuple, r1222_items_tuple_second)
        self.assertIsNot(
            r1222_items_tuple["reconstructed_material"], r1222_items_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1222_items_tuple["material_read"], r1222_items_tuple_second["material_read"])
        r1222_items_omitted = module.resolve_dispute(disputed={}.items())
        r1222_items_omitted_second = module.resolve_dispute(disputed={}.items())
        self.assertIsNot(r1222_items_omitted, r1222_items_omitted_second)
        self.assertIsNot(
            r1222_items_omitted["reconstructed_material"], r1222_items_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1222_items_omitted["material_read"], r1222_items_omitted_second["material_read"])
        r1222_items_none = module.resolve_dispute(disputed={}.items(), journal_records=None)
        r1222_items_none_second = module.resolve_dispute(disputed={}.items(), journal_records=None)
        self.assertIsNot(r1222_items_none, r1222_items_none_second)
        self.assertIsNot(
            r1222_items_none["reconstructed_material"], r1222_items_none_second["reconstructed_material"])
        self.assertIsNot(
            r1222_items_none["material_read"], r1222_items_none_second["material_read"])
        r1222_intflag_tuple = module.resolve_dispute(disputed=IntFlag("R1222Flag", {"member": 0}).member, journal_records=("journal record one", "journal record two"))
        r1222_intflag_tuple_second = module.resolve_dispute(disputed=IntFlag("R1222Flag", {"member": 0}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1222_intflag_tuple, r1222_intflag_tuple_second)
        self.assertIsNot(
            r1222_intflag_tuple["reconstructed_material"], r1222_intflag_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1222_intflag_tuple["material_read"], r1222_intflag_tuple_second["material_read"])
        r1222_intflag_omitted = module.resolve_dispute(disputed=IntFlag("R1222Flag", {"member": 0}).member)
        r1222_intflag_omitted_second = module.resolve_dispute(disputed=IntFlag("R1222Flag", {"member": 0}).member)
        self.assertIsNot(r1222_intflag_omitted, r1222_intflag_omitted_second)
        self.assertIsNot(
            r1222_intflag_omitted["reconstructed_material"], r1222_intflag_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1222_intflag_omitted["material_read"], r1222_intflag_omitted_second["material_read"])
        r1222_intflag_none = module.resolve_dispute(disputed=IntFlag("R1222Flag", {"member": 0}).member, journal_records=None)
        r1222_intflag_none_second = module.resolve_dispute(disputed=IntFlag("R1222Flag", {"member": 0}).member, journal_records=None)
        self.assertIsNot(r1222_intflag_none, r1222_intflag_none_second)
        self.assertIsNot(
            r1222_intflag_none["reconstructed_material"], r1222_intflag_none_second["reconstructed_material"])
        self.assertIsNot(
            r1222_intflag_none["material_read"], r1222_intflag_none_second["material_read"])
        r1222_strenum_tuple = module.resolve_dispute(disputed=StrEnum("R1222StrEnum", {"member": ""}).member, journal_records=("journal record one", "journal record two"))
        r1222_strenum_tuple_second = module.resolve_dispute(disputed=StrEnum("R1222StrEnum", {"member": ""}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1222_strenum_tuple, r1222_strenum_tuple_second)
        self.assertIsNot(
            r1222_strenum_tuple["reconstructed_material"], r1222_strenum_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1222_strenum_tuple["material_read"], r1222_strenum_tuple_second["material_read"])
        r1222_strenum_omitted = module.resolve_dispute(disputed=StrEnum("R1222StrEnum", {"member": ""}).member)
        r1222_strenum_omitted_second = module.resolve_dispute(disputed=StrEnum("R1222StrEnum", {"member": ""}).member)
        self.assertIsNot(r1222_strenum_omitted, r1222_strenum_omitted_second)
        self.assertIsNot(
            r1222_strenum_omitted["reconstructed_material"], r1222_strenum_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1222_strenum_omitted["material_read"], r1222_strenum_omitted_second["material_read"])
        r1222_strenum_none = module.resolve_dispute(disputed=StrEnum("R1222StrEnum", {"member": ""}).member, journal_records=None)
        r1222_strenum_none_second = module.resolve_dispute(disputed=StrEnum("R1222StrEnum", {"member": ""}).member, journal_records=None)
        self.assertIsNot(r1222_strenum_none, r1222_strenum_none_second)
        self.assertIsNot(
            r1222_strenum_none["reconstructed_material"], r1222_strenum_none_second["reconstructed_material"])
        self.assertIsNot(
            r1222_strenum_none["material_read"], r1222_strenum_none_second["material_read"])
        r1222_flag_tuple = module.resolve_dispute(disputed=Flag("R1222PlainFlag", {"member": 0}).member, journal_records=("journal record one", "journal record two"))
        r1222_flag_tuple_second = module.resolve_dispute(disputed=Flag("R1222PlainFlag", {"member": 0}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1222_flag_tuple, r1222_flag_tuple_second)
        self.assertIsNot(
            r1222_flag_tuple["reconstructed_material"], r1222_flag_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1222_flag_tuple["material_read"], r1222_flag_tuple_second["material_read"])
        r1222_flag_omitted = module.resolve_dispute(disputed=Flag("R1222PlainFlag", {"member": 0}).member)
        r1222_flag_omitted_second = module.resolve_dispute(disputed=Flag("R1222PlainFlag", {"member": 0}).member)
        self.assertIsNot(r1222_flag_omitted, r1222_flag_omitted_second)
        self.assertIsNot(
            r1222_flag_omitted["reconstructed_material"], r1222_flag_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1222_flag_omitted["material_read"], r1222_flag_omitted_second["material_read"])
        r1222_flag_none = module.resolve_dispute(disputed=Flag("R1222PlainFlag", {"member": 0}).member, journal_records=None)
        r1222_flag_none_second = module.resolve_dispute(disputed=Flag("R1222PlainFlag", {"member": 0}).member, journal_records=None)
        self.assertIsNot(r1222_flag_none, r1222_flag_none_second)
        self.assertIsNot(
            r1222_flag_none["reconstructed_material"], r1222_flag_none_second["reconstructed_material"])
        self.assertIsNot(
            r1222_flag_none["material_read"], r1222_flag_none_second["material_read"])
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

        r803_list_0 = module.incident_entry(answers=['yes', 'yes', 'no'])
        r803_list_0_second = module.incident_entry(answers=['yes', 'yes', 'no'])
        self.assertIsNot(r803_list_0, r803_list_0_second)
        self.assertIsNot(
            r803_list_0["questions"], r803_list_0_second["questions"])
        self.assertIsNot(
            r803_list_0["answers"], r803_list_0_second["answers"])
        self.assertIsNot(
            r803_list_0["consequences"], r803_list_0_second["consequences"])
        r803_list_1 = module.incident_entry(answers=['yes', 'no', 'yes'])
        r803_list_1_second = module.incident_entry(answers=['yes', 'no', 'yes'])
        self.assertIsNot(r803_list_1, r803_list_1_second)
        self.assertIsNot(
            r803_list_1["questions"], r803_list_1_second["questions"])
        self.assertIsNot(
            r803_list_1["answers"], r803_list_1_second["answers"])
        self.assertIsNot(
            r803_list_1["consequences"], r803_list_1_second["consequences"])
        r803_list_2 = module.incident_entry(answers=['no', 'yes', 'yes'])
        r803_list_2_second = module.incident_entry(answers=['no', 'yes', 'yes'])
        self.assertIsNot(r803_list_2, r803_list_2_second)
        self.assertIsNot(
            r803_list_2["questions"], r803_list_2_second["questions"])
        self.assertIsNot(
            r803_list_2["answers"], r803_list_2_second["answers"])
        self.assertIsNot(
            r803_list_2["consequences"], r803_list_2_second["consequences"])

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
        r804_two_tuple = module.resolve_dispute(disputed=2, journal_records=("journal record one", "journal record two"))
        r804_two_tuple_second = module.resolve_dispute(disputed=2, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r804_two_tuple, r804_two_tuple_second)
        self.assertIsNot(
            r804_two_tuple["reconstructed_material"], r804_two_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r804_two_tuple["material_read"], r804_two_tuple_second["material_read"])
        r804_two_omitted = module.resolve_dispute(disputed=2)
        r804_two_omitted_second = module.resolve_dispute(disputed=2)
        self.assertIsNot(r804_two_omitted, r804_two_omitted_second)
        self.assertIsNot(
            r804_two_omitted["reconstructed_material"], r804_two_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r804_two_omitted["material_read"], r804_two_omitted_second["material_read"])
        r804_two_none = module.resolve_dispute(disputed=2, journal_records=None)
        r804_two_none_second = module.resolve_dispute(disputed=2, journal_records=None)
        self.assertIsNot(r804_two_none, r804_two_none_second)
        self.assertIsNot(
            r804_two_none["reconstructed_material"], r804_two_none_second["reconstructed_material"])
        self.assertIsNot(
            r804_two_none["material_read"], r804_two_none_second["material_read"])
        r804_bytes_tuple = module.resolve_dispute(disputed=b"a disputed value standing as bytes", journal_records=("journal record one", "journal record two"))
        r804_bytes_tuple_second = module.resolve_dispute(disputed=b"a disputed value standing as bytes", journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r804_bytes_tuple, r804_bytes_tuple_second)
        self.assertIsNot(
            r804_bytes_tuple["reconstructed_material"], r804_bytes_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r804_bytes_tuple["material_read"], r804_bytes_tuple_second["material_read"])
        r804_bytes_omitted = module.resolve_dispute(disputed=b"a disputed value standing as bytes")
        r804_bytes_omitted_second = module.resolve_dispute(disputed=b"a disputed value standing as bytes")
        self.assertIsNot(r804_bytes_omitted, r804_bytes_omitted_second)
        self.assertIsNot(
            r804_bytes_omitted["reconstructed_material"], r804_bytes_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r804_bytes_omitted["material_read"], r804_bytes_omitted_second["material_read"])
        r804_bytes_none = module.resolve_dispute(disputed=b"a disputed value standing as bytes", journal_records=None)
        r804_bytes_none_second = module.resolve_dispute(disputed=b"a disputed value standing as bytes", journal_records=None)
        self.assertIsNot(r804_bytes_none, r804_bytes_none_second)
        self.assertIsNot(
            r804_bytes_none["reconstructed_material"], r804_bytes_none_second["reconstructed_material"])
        self.assertIsNot(
            r804_bytes_none["material_read"], r804_bytes_none_second["material_read"])
        r804_list_tuple = module.resolve_dispute(disputed=["a disputed value standing as a list"], journal_records=("journal record one", "journal record two"))
        r804_list_tuple_second = module.resolve_dispute(disputed=["a disputed value standing as a list"], journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r804_list_tuple, r804_list_tuple_second)
        self.assertIsNot(
            r804_list_tuple["reconstructed_material"], r804_list_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r804_list_tuple["material_read"], r804_list_tuple_second["material_read"])
        r804_list_omitted = module.resolve_dispute(disputed=["a disputed value standing as a list"])
        r804_list_omitted_second = module.resolve_dispute(disputed=["a disputed value standing as a list"])
        self.assertIsNot(r804_list_omitted, r804_list_omitted_second)
        self.assertIsNot(
            r804_list_omitted["reconstructed_material"], r804_list_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r804_list_omitted["material_read"], r804_list_omitted_second["material_read"])
        r804_list_none = module.resolve_dispute(disputed=["a disputed value standing as a list"], journal_records=None)
        r804_list_none_second = module.resolve_dispute(disputed=["a disputed value standing as a list"], journal_records=None)
        self.assertIsNot(r804_list_none, r804_list_none_second)
        self.assertIsNot(
            r804_list_none["reconstructed_material"], r804_list_none_second["reconstructed_material"])
        self.assertIsNot(
            r804_list_none["material_read"], r804_list_none_second["material_read"])
        r806_float = module.resolve_dispute(disputed=1.5, journal_records=records)
        r806_float_second = module.resolve_dispute(disputed=1.5, journal_records=records)
        self.assertIsNot(r806_float, r806_float_second)
        self.assertIsNot(
            r806_float["reconstructed_material"], r806_float_second["reconstructed_material"])
        self.assertIsNot(
            r806_float["material_read"], r806_float_second["material_read"])
        r806_tuple = module.resolve_dispute(disputed=("a disputed value standing as a tuple",), journal_records=records)
        r806_tuple_second = module.resolve_dispute(disputed=("a disputed value standing as a tuple",), journal_records=records)
        self.assertIsNot(r806_tuple, r806_tuple_second)
        self.assertIsNot(
            r806_tuple["reconstructed_material"], r806_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r806_tuple["material_read"], r806_tuple_second["material_read"])
        r806_mapping = module.resolve_dispute(disputed={"a disputed key": "a disputed value"}, journal_records=records)
        r806_mapping_second = module.resolve_dispute(disputed={"a disputed key": "a disputed value"}, journal_records=records)
        self.assertIsNot(r806_mapping, r806_mapping_second)
        self.assertIsNot(
            r806_mapping["reconstructed_material"], r806_mapping_second["reconstructed_material"])
        self.assertIsNot(
            r806_mapping["material_read"], r806_mapping_second["material_read"])
        r806_set = module.resolve_dispute(disputed={"a disputed value standing as a set"}, journal_records=records)
        r806_set_second = module.resolve_dispute(disputed={"a disputed value standing as a set"}, journal_records=records)
        self.assertIsNot(r806_set, r806_set_second)
        self.assertIsNot(
            r806_set["reconstructed_material"], r806_set_second["reconstructed_material"])
        self.assertIsNot(
            r806_set["material_read"], r806_set_second["material_read"])
        r863_bytearray = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"), journal_records=records)
        r863_bytearray_second = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"), journal_records=records)
        self.assertIsNot(r863_bytearray, r863_bytearray_second)
        self.assertIsNot(
            r863_bytearray["reconstructed_material"], r863_bytearray_second["reconstructed_material"])
        self.assertIsNot(
            r863_bytearray["material_read"], r863_bytearray_second["material_read"])
        r863_complex = module.resolve_dispute(disputed=1j, journal_records=records)
        r863_complex_second = module.resolve_dispute(disputed=1j, journal_records=records)
        self.assertIsNot(r863_complex, r863_complex_second)
        self.assertIsNot(
            r863_complex["reconstructed_material"], r863_complex_second["reconstructed_material"])
        self.assertIsNot(
            r863_complex["material_read"], r863_complex_second["material_read"])
        r863_decimal = module.resolve_dispute(disputed=Decimal(1), journal_records=records)
        r863_decimal_second = module.resolve_dispute(disputed=Decimal(1), journal_records=records)
        self.assertIsNot(r863_decimal, r863_decimal_second)
        self.assertIsNot(
            r863_decimal["reconstructed_material"], r863_decimal_second["reconstructed_material"])
        self.assertIsNot(
            r863_decimal["material_read"], r863_decimal_second["material_read"])
        r863_frozenset = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}), journal_records=records)
        r863_frozenset_second = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}), journal_records=records)
        self.assertIsNot(r863_frozenset, r863_frozenset_second)
        self.assertIsNot(
            r863_frozenset["reconstructed_material"], r863_frozenset_second["reconstructed_material"])
        self.assertIsNot(
            r863_frozenset["material_read"], r863_frozenset_second["material_read"])
        r863_range = module.resolve_dispute(disputed=range(1), journal_records=records)
        r863_range_second = module.resolve_dispute(disputed=range(1), journal_records=records)
        self.assertIsNot(r863_range, r863_range_second)
        self.assertIsNot(
            r863_range["reconstructed_material"], r863_range_second["reconstructed_material"])
        self.assertIsNot(
            r863_range["material_read"], r863_range_second["material_read"])
        r870_float_tuple = module.resolve_dispute(disputed=1.5, journal_records=("journal record one", "journal record two"))
        r870_float_tuple_second = module.resolve_dispute(disputed=1.5, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r870_float_tuple, r870_float_tuple_second)
        self.assertIsNot(
            r870_float_tuple["reconstructed_material"], r870_float_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r870_float_tuple["material_read"], r870_float_tuple_second["material_read"])
        r870_float_omitted = module.resolve_dispute(disputed=1.5)
        r870_float_omitted_second = module.resolve_dispute(disputed=1.5)
        self.assertIsNot(r870_float_omitted, r870_float_omitted_second)
        self.assertIsNot(
            r870_float_omitted["reconstructed_material"], r870_float_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r870_float_omitted["material_read"], r870_float_omitted_second["material_read"])
        r870_float_none = module.resolve_dispute(disputed=1.5, journal_records=None)
        r870_float_none_second = module.resolve_dispute(disputed=1.5, journal_records=None)
        self.assertIsNot(r870_float_none, r870_float_none_second)
        self.assertIsNot(
            r870_float_none["reconstructed_material"], r870_float_none_second["reconstructed_material"])
        self.assertIsNot(
            r870_float_none["material_read"], r870_float_none_second["material_read"])
        r870_tuple_tuple = module.resolve_dispute(disputed=("a disputed value standing as a tuple",), journal_records=("journal record one", "journal record two"))
        r870_tuple_tuple_second = module.resolve_dispute(disputed=("a disputed value standing as a tuple",), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r870_tuple_tuple, r870_tuple_tuple_second)
        self.assertIsNot(
            r870_tuple_tuple["reconstructed_material"], r870_tuple_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r870_tuple_tuple["material_read"], r870_tuple_tuple_second["material_read"])
        r870_tuple_omitted = module.resolve_dispute(disputed=("a disputed value standing as a tuple",))
        r870_tuple_omitted_second = module.resolve_dispute(disputed=("a disputed value standing as a tuple",))
        self.assertIsNot(r870_tuple_omitted, r870_tuple_omitted_second)
        self.assertIsNot(
            r870_tuple_omitted["reconstructed_material"], r870_tuple_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r870_tuple_omitted["material_read"], r870_tuple_omitted_second["material_read"])
        r870_tuple_none = module.resolve_dispute(disputed=("a disputed value standing as a tuple",), journal_records=None)
        r870_tuple_none_second = module.resolve_dispute(disputed=("a disputed value standing as a tuple",), journal_records=None)
        self.assertIsNot(r870_tuple_none, r870_tuple_none_second)
        self.assertIsNot(
            r870_tuple_none["reconstructed_material"], r870_tuple_none_second["reconstructed_material"])
        self.assertIsNot(
            r870_tuple_none["material_read"], r870_tuple_none_second["material_read"])
        r870_mapping_tuple = module.resolve_dispute(disputed={"a disputed key": "a disputed value"}, journal_records=("journal record one", "journal record two"))
        r870_mapping_tuple_second = module.resolve_dispute(disputed={"a disputed key": "a disputed value"}, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r870_mapping_tuple, r870_mapping_tuple_second)
        self.assertIsNot(
            r870_mapping_tuple["reconstructed_material"], r870_mapping_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r870_mapping_tuple["material_read"], r870_mapping_tuple_second["material_read"])
        r870_mapping_omitted = module.resolve_dispute(disputed={"a disputed key": "a disputed value"})
        r870_mapping_omitted_second = module.resolve_dispute(disputed={"a disputed key": "a disputed value"})
        self.assertIsNot(r870_mapping_omitted, r870_mapping_omitted_second)
        self.assertIsNot(
            r870_mapping_omitted["reconstructed_material"], r870_mapping_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r870_mapping_omitted["material_read"], r870_mapping_omitted_second["material_read"])
        r870_mapping_none = module.resolve_dispute(disputed={"a disputed key": "a disputed value"}, journal_records=None)
        r870_mapping_none_second = module.resolve_dispute(disputed={"a disputed key": "a disputed value"}, journal_records=None)
        self.assertIsNot(r870_mapping_none, r870_mapping_none_second)
        self.assertIsNot(
            r870_mapping_none["reconstructed_material"], r870_mapping_none_second["reconstructed_material"])
        self.assertIsNot(
            r870_mapping_none["material_read"], r870_mapping_none_second["material_read"])
        r870_set_tuple = module.resolve_dispute(disputed={"a disputed value standing as a set"}, journal_records=("journal record one", "journal record two"))
        r870_set_tuple_second = module.resolve_dispute(disputed={"a disputed value standing as a set"}, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r870_set_tuple, r870_set_tuple_second)
        self.assertIsNot(
            r870_set_tuple["reconstructed_material"], r870_set_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r870_set_tuple["material_read"], r870_set_tuple_second["material_read"])
        r870_set_omitted = module.resolve_dispute(disputed={"a disputed value standing as a set"})
        r870_set_omitted_second = module.resolve_dispute(disputed={"a disputed value standing as a set"})
        self.assertIsNot(r870_set_omitted, r870_set_omitted_second)
        self.assertIsNot(
            r870_set_omitted["reconstructed_material"], r870_set_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r870_set_omitted["material_read"], r870_set_omitted_second["material_read"])
        r870_set_none = module.resolve_dispute(disputed={"a disputed value standing as a set"}, journal_records=None)
        r870_set_none_second = module.resolve_dispute(disputed={"a disputed value standing as a set"}, journal_records=None)
        self.assertIsNot(r870_set_none, r870_set_none_second)
        self.assertIsNot(
            r870_set_none["reconstructed_material"], r870_set_none_second["reconstructed_material"])
        self.assertIsNot(
            r870_set_none["material_read"], r870_set_none_second["material_read"])

        r921_memoryview = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"), journal_records=records)
        r921_memoryview_second = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"), journal_records=records)
        self.assertIsNot(r921_memoryview, r921_memoryview_second)
        self.assertIsNot(
            r921_memoryview["reconstructed_material"], r921_memoryview_second["reconstructed_material"])
        self.assertIsNot(
            r921_memoryview["material_read"], r921_memoryview_second["material_read"])
        r921_fraction = module.resolve_dispute(disputed=Fraction(1, 2), journal_records=records)
        r921_fraction_second = module.resolve_dispute(disputed=Fraction(1, 2), journal_records=records)
        self.assertIsNot(r921_fraction, r921_fraction_second)
        self.assertIsNot(
            r921_fraction["reconstructed_material"], r921_fraction_second["reconstructed_material"])
        self.assertIsNot(
            r921_fraction["material_read"], r921_fraction_second["material_read"])
        r921_deque = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]), journal_records=records)
        r921_deque_second = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]), journal_records=records)
        self.assertIsNot(r921_deque, r921_deque_second)
        self.assertIsNot(
            r921_deque["reconstructed_material"], r921_deque_second["reconstructed_material"])
        self.assertIsNot(
            r921_deque["material_read"], r921_deque_second["material_read"])
        r921_counter = module.resolve_dispute(disputed=Counter({"a disputed key": 1}), journal_records=records)
        r921_counter_second = module.resolve_dispute(disputed=Counter({"a disputed key": 1}), journal_records=records)
        self.assertIsNot(r921_counter, r921_counter_second)
        self.assertIsNot(
            r921_counter["reconstructed_material"], r921_counter_second["reconstructed_material"])
        self.assertIsNot(
            r921_counter["material_read"], r921_counter_second["material_read"])
        r921_ordered = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]), journal_records=records)
        r921_ordered_second = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]), journal_records=records)
        self.assertIsNot(r921_ordered, r921_ordered_second)
        self.assertIsNot(
            r921_ordered["reconstructed_material"], r921_ordered_second["reconstructed_material"])
        self.assertIsNot(
            r921_ordered["material_read"], r921_ordered_second["material_read"])
        r929_bytearray_tuple = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"), journal_records=("journal record one", "journal record two"))
        r929_bytearray_tuple_second = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r929_bytearray_tuple, r929_bytearray_tuple_second)
        self.assertIsNot(
            r929_bytearray_tuple["reconstructed_material"], r929_bytearray_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r929_bytearray_tuple["material_read"], r929_bytearray_tuple_second["material_read"])
        r929_bytearray_omitted = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"))
        r929_bytearray_omitted_second = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"))
        self.assertIsNot(r929_bytearray_omitted, r929_bytearray_omitted_second)
        self.assertIsNot(
            r929_bytearray_omitted["reconstructed_material"], r929_bytearray_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r929_bytearray_omitted["material_read"], r929_bytearray_omitted_second["material_read"])
        r929_bytearray_none = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"), journal_records=None)
        r929_bytearray_none_second = module.resolve_dispute(disputed=bytearray(b"a disputed value standing as a bytearray"), journal_records=None)
        self.assertIsNot(r929_bytearray_none, r929_bytearray_none_second)
        self.assertIsNot(
            r929_bytearray_none["reconstructed_material"], r929_bytearray_none_second["reconstructed_material"])
        self.assertIsNot(
            r929_bytearray_none["material_read"], r929_bytearray_none_second["material_read"])
        r929_complex_tuple = module.resolve_dispute(disputed=1j, journal_records=("journal record one", "journal record two"))
        r929_complex_tuple_second = module.resolve_dispute(disputed=1j, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r929_complex_tuple, r929_complex_tuple_second)
        self.assertIsNot(
            r929_complex_tuple["reconstructed_material"], r929_complex_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r929_complex_tuple["material_read"], r929_complex_tuple_second["material_read"])
        r929_complex_omitted = module.resolve_dispute(disputed=1j)
        r929_complex_omitted_second = module.resolve_dispute(disputed=1j)
        self.assertIsNot(r929_complex_omitted, r929_complex_omitted_second)
        self.assertIsNot(
            r929_complex_omitted["reconstructed_material"], r929_complex_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r929_complex_omitted["material_read"], r929_complex_omitted_second["material_read"])
        r929_complex_none = module.resolve_dispute(disputed=1j, journal_records=None)
        r929_complex_none_second = module.resolve_dispute(disputed=1j, journal_records=None)
        self.assertIsNot(r929_complex_none, r929_complex_none_second)
        self.assertIsNot(
            r929_complex_none["reconstructed_material"], r929_complex_none_second["reconstructed_material"])
        self.assertIsNot(
            r929_complex_none["material_read"], r929_complex_none_second["material_read"])
        r929_decimal_tuple = module.resolve_dispute(disputed=Decimal(1), journal_records=("journal record one", "journal record two"))
        r929_decimal_tuple_second = module.resolve_dispute(disputed=Decimal(1), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r929_decimal_tuple, r929_decimal_tuple_second)
        self.assertIsNot(
            r929_decimal_tuple["reconstructed_material"], r929_decimal_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r929_decimal_tuple["material_read"], r929_decimal_tuple_second["material_read"])
        r929_decimal_omitted = module.resolve_dispute(disputed=Decimal(1))
        r929_decimal_omitted_second = module.resolve_dispute(disputed=Decimal(1))
        self.assertIsNot(r929_decimal_omitted, r929_decimal_omitted_second)
        self.assertIsNot(
            r929_decimal_omitted["reconstructed_material"], r929_decimal_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r929_decimal_omitted["material_read"], r929_decimal_omitted_second["material_read"])
        r929_decimal_none = module.resolve_dispute(disputed=Decimal(1), journal_records=None)
        r929_decimal_none_second = module.resolve_dispute(disputed=Decimal(1), journal_records=None)
        self.assertIsNot(r929_decimal_none, r929_decimal_none_second)
        self.assertIsNot(
            r929_decimal_none["reconstructed_material"], r929_decimal_none_second["reconstructed_material"])
        self.assertIsNot(
            r929_decimal_none["material_read"], r929_decimal_none_second["material_read"])
        r929_frozenset_tuple = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}), journal_records=("journal record one", "journal record two"))
        r929_frozenset_tuple_second = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r929_frozenset_tuple, r929_frozenset_tuple_second)
        self.assertIsNot(
            r929_frozenset_tuple["reconstructed_material"], r929_frozenset_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r929_frozenset_tuple["material_read"], r929_frozenset_tuple_second["material_read"])
        r929_frozenset_omitted = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}))
        r929_frozenset_omitted_second = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}))
        self.assertIsNot(r929_frozenset_omitted, r929_frozenset_omitted_second)
        self.assertIsNot(
            r929_frozenset_omitted["reconstructed_material"], r929_frozenset_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r929_frozenset_omitted["material_read"], r929_frozenset_omitted_second["material_read"])
        r929_frozenset_none = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}), journal_records=None)
        r929_frozenset_none_second = module.resolve_dispute(disputed=frozenset({"a disputed value standing as a frozenset"}), journal_records=None)
        self.assertIsNot(r929_frozenset_none, r929_frozenset_none_second)
        self.assertIsNot(
            r929_frozenset_none["reconstructed_material"], r929_frozenset_none_second["reconstructed_material"])
        self.assertIsNot(
            r929_frozenset_none["material_read"], r929_frozenset_none_second["material_read"])
        r929_range_tuple = module.resolve_dispute(disputed=range(1), journal_records=("journal record one", "journal record two"))
        r929_range_tuple_second = module.resolve_dispute(disputed=range(1), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r929_range_tuple, r929_range_tuple_second)
        self.assertIsNot(
            r929_range_tuple["reconstructed_material"], r929_range_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r929_range_tuple["material_read"], r929_range_tuple_second["material_read"])
        r929_range_omitted = module.resolve_dispute(disputed=range(1))
        r929_range_omitted_second = module.resolve_dispute(disputed=range(1))
        self.assertIsNot(r929_range_omitted, r929_range_omitted_second)
        self.assertIsNot(
            r929_range_omitted["reconstructed_material"], r929_range_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r929_range_omitted["material_read"], r929_range_omitted_second["material_read"])
        r929_range_none = module.resolve_dispute(disputed=range(1), journal_records=None)
        r929_range_none_second = module.resolve_dispute(disputed=range(1), journal_records=None)
        self.assertIsNot(r929_range_none, r929_range_none_second)
        self.assertIsNot(
            r929_range_none["reconstructed_material"], r929_range_none_second["reconstructed_material"])
        self.assertIsNot(
            r929_range_none["material_read"], r929_range_none_second["material_read"])
        r977_array = module.resolve_dispute(disputed=array("i", [1]), journal_records=records)
        r977_array_second = module.resolve_dispute(disputed=array("i", [1]), journal_records=records)
        self.assertIsNot(r977_array, r977_array_second)
        self.assertIsNot(
            r977_array["reconstructed_material"], r977_array_second["reconstructed_material"])
        self.assertIsNot(
            r977_array["material_read"], r977_array_second["material_read"])
        r977_chainmap = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}), journal_records=records)
        r977_chainmap_second = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}), journal_records=records)
        self.assertIsNot(r977_chainmap, r977_chainmap_second)
        self.assertIsNot(
            r977_chainmap["reconstructed_material"], r977_chainmap_second["reconstructed_material"])
        self.assertIsNot(
            r977_chainmap["material_read"], r977_chainmap_second["material_read"])
        r977_defaultdict = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}), journal_records=records)
        r977_defaultdict_second = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}), journal_records=records)
        self.assertIsNot(r977_defaultdict, r977_defaultdict_second)
        self.assertIsNot(
            r977_defaultdict["reconstructed_material"], r977_defaultdict_second["reconstructed_material"])
        self.assertIsNot(
            r977_defaultdict["material_read"], r977_defaultdict_second["material_read"])
        r977_timedelta = module.resolve_dispute(disputed=timedelta(days=1), journal_records=records)
        r977_timedelta_second = module.resolve_dispute(disputed=timedelta(days=1), journal_records=records)
        self.assertIsNot(r977_timedelta, r977_timedelta_second)
        self.assertIsNot(
            r977_timedelta["reconstructed_material"], r977_timedelta_second["reconstructed_material"])
        self.assertIsNot(
            r977_timedelta["material_read"], r977_timedelta_second["material_read"])
        r977_userdict = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}), journal_records=records)
        r977_userdict_second = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}), journal_records=records)
        self.assertIsNot(r977_userdict, r977_userdict_second)
        self.assertIsNot(
            r977_userdict["reconstructed_material"], r977_userdict_second["reconstructed_material"])
        self.assertIsNot(
            r977_userdict["material_read"], r977_userdict_second["material_read"])
        r984_memoryview_tuple = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"), journal_records=("journal record one", "journal record two"))
        r984_memoryview_tuple_second = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r984_memoryview_tuple, r984_memoryview_tuple_second)
        self.assertIsNot(
            r984_memoryview_tuple["reconstructed_material"], r984_memoryview_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r984_memoryview_tuple["material_read"], r984_memoryview_tuple_second["material_read"])
        r984_memoryview_omitted = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"))
        r984_memoryview_omitted_second = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"))
        self.assertIsNot(r984_memoryview_omitted, r984_memoryview_omitted_second)
        self.assertIsNot(
            r984_memoryview_omitted["reconstructed_material"], r984_memoryview_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r984_memoryview_omitted["material_read"], r984_memoryview_omitted_second["material_read"])
        r984_memoryview_none = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"), journal_records=None)
        r984_memoryview_none_second = module.resolve_dispute(disputed=memoryview(b"a disputed value standing as a memoryview"), journal_records=None)
        self.assertIsNot(r984_memoryview_none, r984_memoryview_none_second)
        self.assertIsNot(
            r984_memoryview_none["reconstructed_material"], r984_memoryview_none_second["reconstructed_material"])
        self.assertIsNot(
            r984_memoryview_none["material_read"], r984_memoryview_none_second["material_read"])
        r984_fraction_tuple = module.resolve_dispute(disputed=Fraction(1, 2), journal_records=("journal record one", "journal record two"))
        r984_fraction_tuple_second = module.resolve_dispute(disputed=Fraction(1, 2), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r984_fraction_tuple, r984_fraction_tuple_second)
        self.assertIsNot(
            r984_fraction_tuple["reconstructed_material"], r984_fraction_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r984_fraction_tuple["material_read"], r984_fraction_tuple_second["material_read"])
        r984_fraction_omitted = module.resolve_dispute(disputed=Fraction(1, 2))
        r984_fraction_omitted_second = module.resolve_dispute(disputed=Fraction(1, 2))
        self.assertIsNot(r984_fraction_omitted, r984_fraction_omitted_second)
        self.assertIsNot(
            r984_fraction_omitted["reconstructed_material"], r984_fraction_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r984_fraction_omitted["material_read"], r984_fraction_omitted_second["material_read"])
        r984_fraction_none = module.resolve_dispute(disputed=Fraction(1, 2), journal_records=None)
        r984_fraction_none_second = module.resolve_dispute(disputed=Fraction(1, 2), journal_records=None)
        self.assertIsNot(r984_fraction_none, r984_fraction_none_second)
        self.assertIsNot(
            r984_fraction_none["reconstructed_material"], r984_fraction_none_second["reconstructed_material"])
        self.assertIsNot(
            r984_fraction_none["material_read"], r984_fraction_none_second["material_read"])
        r984_deque_tuple = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]), journal_records=("journal record one", "journal record two"))
        r984_deque_tuple_second = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r984_deque_tuple, r984_deque_tuple_second)
        self.assertIsNot(
            r984_deque_tuple["reconstructed_material"], r984_deque_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r984_deque_tuple["material_read"], r984_deque_tuple_second["material_read"])
        r984_deque_omitted = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]))
        r984_deque_omitted_second = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]))
        self.assertIsNot(r984_deque_omitted, r984_deque_omitted_second)
        self.assertIsNot(
            r984_deque_omitted["reconstructed_material"], r984_deque_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r984_deque_omitted["material_read"], r984_deque_omitted_second["material_read"])
        r984_deque_none = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]), journal_records=None)
        r984_deque_none_second = module.resolve_dispute(disputed=deque(["a disputed value standing as a deque"]), journal_records=None)
        self.assertIsNot(r984_deque_none, r984_deque_none_second)
        self.assertIsNot(
            r984_deque_none["reconstructed_material"], r984_deque_none_second["reconstructed_material"])
        self.assertIsNot(
            r984_deque_none["material_read"], r984_deque_none_second["material_read"])
        r984_counter_tuple = module.resolve_dispute(disputed=Counter({"a disputed key": 1}), journal_records=("journal record one", "journal record two"))
        r984_counter_tuple_second = module.resolve_dispute(disputed=Counter({"a disputed key": 1}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r984_counter_tuple, r984_counter_tuple_second)
        self.assertIsNot(
            r984_counter_tuple["reconstructed_material"], r984_counter_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r984_counter_tuple["material_read"], r984_counter_tuple_second["material_read"])
        r984_counter_omitted = module.resolve_dispute(disputed=Counter({"a disputed key": 1}))
        r984_counter_omitted_second = module.resolve_dispute(disputed=Counter({"a disputed key": 1}))
        self.assertIsNot(r984_counter_omitted, r984_counter_omitted_second)
        self.assertIsNot(
            r984_counter_omitted["reconstructed_material"], r984_counter_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r984_counter_omitted["material_read"], r984_counter_omitted_second["material_read"])
        r984_counter_none = module.resolve_dispute(disputed=Counter({"a disputed key": 1}), journal_records=None)
        r984_counter_none_second = module.resolve_dispute(disputed=Counter({"a disputed key": 1}), journal_records=None)
        self.assertIsNot(r984_counter_none, r984_counter_none_second)
        self.assertIsNot(
            r984_counter_none["reconstructed_material"], r984_counter_none_second["reconstructed_material"])
        self.assertIsNot(
            r984_counter_none["material_read"], r984_counter_none_second["material_read"])
        r984_ordered_tuple = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]), journal_records=("journal record one", "journal record two"))
        r984_ordered_tuple_second = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r984_ordered_tuple, r984_ordered_tuple_second)
        self.assertIsNot(
            r984_ordered_tuple["reconstructed_material"], r984_ordered_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r984_ordered_tuple["material_read"], r984_ordered_tuple_second["material_read"])
        r984_ordered_omitted = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]))
        r984_ordered_omitted_second = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]))
        self.assertIsNot(r984_ordered_omitted, r984_ordered_omitted_second)
        self.assertIsNot(
            r984_ordered_omitted["reconstructed_material"], r984_ordered_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r984_ordered_omitted["material_read"], r984_ordered_omitted_second["material_read"])
        r984_ordered_none = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]), journal_records=None)
        r984_ordered_none_second = module.resolve_dispute(disputed=OrderedDict([("a disputed key", "a disputed value")]), journal_records=None)
        self.assertIsNot(r984_ordered_none, r984_ordered_none_second)
        self.assertIsNot(
            r984_ordered_none["reconstructed_material"], r984_ordered_none_second["reconstructed_material"])
        self.assertIsNot(
            r984_ordered_none["material_read"], r984_ordered_none_second["material_read"])
        r1047_proxy = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}), journal_records=records)
        r1047_proxy_second = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}), journal_records=records)
        self.assertIsNot(r1047_proxy, r1047_proxy_second)
        self.assertIsNot(
            r1047_proxy["reconstructed_material"], r1047_proxy_second["reconstructed_material"])
        self.assertIsNot(
            r1047_proxy["material_read"], r1047_proxy_second["material_read"])
        r1047_namedtuple = module.resolve_dispute(disputed=namedtuple("R1047Tuple", ["field"])(1), journal_records=records)
        r1047_namedtuple_second = module.resolve_dispute(disputed=namedtuple("R1047Tuple", ["field"])(1), journal_records=records)
        self.assertIsNot(r1047_namedtuple, r1047_namedtuple_second)
        self.assertIsNot(
            r1047_namedtuple["reconstructed_material"], r1047_namedtuple_second["reconstructed_material"])
        self.assertIsNot(
            r1047_namedtuple["material_read"], r1047_namedtuple_second["material_read"])
        r1047_keys = module.resolve_dispute(disputed={"k": "v"}.keys(), journal_records=records)
        r1047_keys_second = module.resolve_dispute(disputed={"k": "v"}.keys(), journal_records=records)
        self.assertIsNot(r1047_keys, r1047_keys_second)
        self.assertIsNot(
            r1047_keys["reconstructed_material"], r1047_keys_second["reconstructed_material"])
        self.assertIsNot(
            r1047_keys["material_read"], r1047_keys_second["material_read"])
        r1047_values = module.resolve_dispute(disputed={"k": "v"}.values(), journal_records=records)
        r1047_values_second = module.resolve_dispute(disputed={"k": "v"}.values(), journal_records=records)
        self.assertIsNot(r1047_values, r1047_values_second)
        self.assertIsNot(
            r1047_values["reconstructed_material"], r1047_values_second["reconstructed_material"])
        self.assertIsNot(
            r1047_values["material_read"], r1047_values_second["material_read"])
        r1047_intenum = module.resolve_dispute(disputed=IntEnum("R1047Enum", {"member": 1}).member, journal_records=records)
        r1047_intenum_second = module.resolve_dispute(disputed=IntEnum("R1047Enum", {"member": 1}).member, journal_records=records)
        self.assertIsNot(r1047_intenum, r1047_intenum_second)
        self.assertIsNot(
            r1047_intenum["reconstructed_material"], r1047_intenum_second["reconstructed_material"])
        self.assertIsNot(
            r1047_intenum["material_read"], r1047_intenum_second["material_read"])
        r1061_userlist = module.resolve_dispute(disputed=UserList([1]), journal_records=records)
        r1061_userlist_second = module.resolve_dispute(disputed=UserList([1]), journal_records=records)
        self.assertIsNot(r1061_userlist, r1061_userlist_second)
        self.assertIsNot(
            r1061_userlist["reconstructed_material"], r1061_userlist_second["reconstructed_material"])
        self.assertIsNot(
            r1061_userlist["material_read"], r1061_userlist_second["material_read"])
        r1061_userstring = module.resolve_dispute(disputed=UserString("x"), journal_records=records)
        r1061_userstring_second = module.resolve_dispute(disputed=UserString("x"), journal_records=records)
        self.assertIsNot(r1061_userstring, r1061_userstring_second)
        self.assertIsNot(
            r1061_userstring["reconstructed_material"], r1061_userstring_second["reconstructed_material"])
        self.assertIsNot(
            r1061_userstring["material_read"], r1061_userstring_second["material_read"])
        r1054_array_tuple = module.resolve_dispute(disputed=array("i", [1]), journal_records=("journal record one", "journal record two"))
        r1054_array_tuple_second = module.resolve_dispute(disputed=array("i", [1]), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1054_array_tuple, r1054_array_tuple_second)
        self.assertIsNot(
            r1054_array_tuple["reconstructed_material"], r1054_array_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1054_array_tuple["material_read"], r1054_array_tuple_second["material_read"])
        r1054_array_omitted = module.resolve_dispute(disputed=array("i", [1]))
        r1054_array_omitted_second = module.resolve_dispute(disputed=array("i", [1]))
        self.assertIsNot(r1054_array_omitted, r1054_array_omitted_second)
        self.assertIsNot(
            r1054_array_omitted["reconstructed_material"], r1054_array_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1054_array_omitted["material_read"], r1054_array_omitted_second["material_read"])
        r1054_array_none = module.resolve_dispute(disputed=array("i", [1]), journal_records=None)
        r1054_array_none_second = module.resolve_dispute(disputed=array("i", [1]), journal_records=None)
        self.assertIsNot(r1054_array_none, r1054_array_none_second)
        self.assertIsNot(
            r1054_array_none["reconstructed_material"], r1054_array_none_second["reconstructed_material"])
        self.assertIsNot(
            r1054_array_none["material_read"], r1054_array_none_second["material_read"])
        r1054_chainmap_tuple = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}), journal_records=("journal record one", "journal record two"))
        r1054_chainmap_tuple_second = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1054_chainmap_tuple, r1054_chainmap_tuple_second)
        self.assertIsNot(
            r1054_chainmap_tuple["reconstructed_material"], r1054_chainmap_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1054_chainmap_tuple["material_read"], r1054_chainmap_tuple_second["material_read"])
        r1054_chainmap_omitted = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}))
        r1054_chainmap_omitted_second = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}))
        self.assertIsNot(r1054_chainmap_omitted, r1054_chainmap_omitted_second)
        self.assertIsNot(
            r1054_chainmap_omitted["reconstructed_material"], r1054_chainmap_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1054_chainmap_omitted["material_read"], r1054_chainmap_omitted_second["material_read"])
        r1054_chainmap_none = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}), journal_records=None)
        r1054_chainmap_none_second = module.resolve_dispute(disputed=ChainMap({"a disputed key": "a disputed value"}), journal_records=None)
        self.assertIsNot(r1054_chainmap_none, r1054_chainmap_none_second)
        self.assertIsNot(
            r1054_chainmap_none["reconstructed_material"], r1054_chainmap_none_second["reconstructed_material"])
        self.assertIsNot(
            r1054_chainmap_none["material_read"], r1054_chainmap_none_second["material_read"])
        r1054_defaultdict_tuple = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}), journal_records=("journal record one", "journal record two"))
        r1054_defaultdict_tuple_second = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1054_defaultdict_tuple, r1054_defaultdict_tuple_second)
        self.assertIsNot(
            r1054_defaultdict_tuple["reconstructed_material"], r1054_defaultdict_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1054_defaultdict_tuple["material_read"], r1054_defaultdict_tuple_second["material_read"])
        r1054_defaultdict_omitted = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}))
        r1054_defaultdict_omitted_second = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}))
        self.assertIsNot(r1054_defaultdict_omitted, r1054_defaultdict_omitted_second)
        self.assertIsNot(
            r1054_defaultdict_omitted["reconstructed_material"], r1054_defaultdict_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1054_defaultdict_omitted["material_read"], r1054_defaultdict_omitted_second["material_read"])
        r1054_defaultdict_none = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}), journal_records=None)
        r1054_defaultdict_none_second = module.resolve_dispute(disputed=defaultdict(int, {"a disputed key": 1}), journal_records=None)
        self.assertIsNot(r1054_defaultdict_none, r1054_defaultdict_none_second)
        self.assertIsNot(
            r1054_defaultdict_none["reconstructed_material"], r1054_defaultdict_none_second["reconstructed_material"])
        self.assertIsNot(
            r1054_defaultdict_none["material_read"], r1054_defaultdict_none_second["material_read"])
        r1054_timedelta_tuple = module.resolve_dispute(disputed=timedelta(days=1), journal_records=("journal record one", "journal record two"))
        r1054_timedelta_tuple_second = module.resolve_dispute(disputed=timedelta(days=1), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1054_timedelta_tuple, r1054_timedelta_tuple_second)
        self.assertIsNot(
            r1054_timedelta_tuple["reconstructed_material"], r1054_timedelta_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1054_timedelta_tuple["material_read"], r1054_timedelta_tuple_second["material_read"])
        r1054_timedelta_omitted = module.resolve_dispute(disputed=timedelta(days=1))
        r1054_timedelta_omitted_second = module.resolve_dispute(disputed=timedelta(days=1))
        self.assertIsNot(r1054_timedelta_omitted, r1054_timedelta_omitted_second)
        self.assertIsNot(
            r1054_timedelta_omitted["reconstructed_material"], r1054_timedelta_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1054_timedelta_omitted["material_read"], r1054_timedelta_omitted_second["material_read"])
        r1054_timedelta_none = module.resolve_dispute(disputed=timedelta(days=1), journal_records=None)
        r1054_timedelta_none_second = module.resolve_dispute(disputed=timedelta(days=1), journal_records=None)
        self.assertIsNot(r1054_timedelta_none, r1054_timedelta_none_second)
        self.assertIsNot(
            r1054_timedelta_none["reconstructed_material"], r1054_timedelta_none_second["reconstructed_material"])
        self.assertIsNot(
            r1054_timedelta_none["material_read"], r1054_timedelta_none_second["material_read"])
        r1054_userdict_tuple = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}), journal_records=("journal record one", "journal record two"))
        r1054_userdict_tuple_second = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1054_userdict_tuple, r1054_userdict_tuple_second)
        self.assertIsNot(
            r1054_userdict_tuple["reconstructed_material"], r1054_userdict_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1054_userdict_tuple["material_read"], r1054_userdict_tuple_second["material_read"])
        r1054_userdict_omitted = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}))
        r1054_userdict_omitted_second = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}))
        self.assertIsNot(r1054_userdict_omitted, r1054_userdict_omitted_second)
        self.assertIsNot(
            r1054_userdict_omitted["reconstructed_material"], r1054_userdict_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1054_userdict_omitted["material_read"], r1054_userdict_omitted_second["material_read"])
        r1054_userdict_none = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}), journal_records=None)
        r1054_userdict_none_second = module.resolve_dispute(disputed=UserDict({"a disputed key": "a disputed value"}), journal_records=None)
        self.assertIsNot(r1054_userdict_none, r1054_userdict_none_second)
        self.assertIsNot(
            r1054_userdict_none["reconstructed_material"], r1054_userdict_none_second["reconstructed_material"])
        self.assertIsNot(
            r1054_userdict_none["material_read"], r1054_userdict_none_second["material_read"])

        r1119_items = module.resolve_dispute(disputed={"k": "v"}.items(), journal_records=records)
        r1119_items_second = module.resolve_dispute(disputed={"k": "v"}.items(), journal_records=records)
        self.assertIsNot(r1119_items, r1119_items_second)
        self.assertIsNot(
            r1119_items["reconstructed_material"], r1119_items_second["reconstructed_material"])
        self.assertIsNot(
            r1119_items["material_read"], r1119_items_second["material_read"])
        r1119_intflag = module.resolve_dispute(disputed=IntFlag("R1119Flag", {"member": 1}).member, journal_records=records)
        r1119_intflag_second = module.resolve_dispute(disputed=IntFlag("R1119Flag", {"member": 1}).member, journal_records=records)
        self.assertIsNot(r1119_intflag, r1119_intflag_second)
        self.assertIsNot(
            r1119_intflag["reconstructed_material"], r1119_intflag_second["reconstructed_material"])
        self.assertIsNot(
            r1119_intflag["material_read"], r1119_intflag_second["material_read"])
        r1119_strenum = module.resolve_dispute(disputed=StrEnum("R1119StrEnum", {"member": "x"}).member, journal_records=records)
        r1119_strenum_second = module.resolve_dispute(disputed=StrEnum("R1119StrEnum", {"member": "x"}).member, journal_records=records)
        self.assertIsNot(r1119_strenum, r1119_strenum_second)
        self.assertIsNot(
            r1119_strenum["reconstructed_material"], r1119_strenum_second["reconstructed_material"])
        self.assertIsNot(
            r1119_strenum["material_read"], r1119_strenum_second["material_read"])
        r1119_flag = module.resolve_dispute(disputed=Flag("R1119PlainFlag", {"member": 1}).member, journal_records=records)
        r1119_flag_second = module.resolve_dispute(disputed=Flag("R1119PlainFlag", {"member": 1}).member, journal_records=records)
        self.assertIsNot(r1119_flag, r1119_flag_second)
        self.assertIsNot(
            r1119_flag["reconstructed_material"], r1119_flag_second["reconstructed_material"])
        self.assertIsNot(
            r1119_flag["material_read"], r1119_flag_second["material_read"])
        r1128_proxy_tuple = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}), journal_records=("journal record one", "journal record two"))
        r1128_proxy_tuple_second = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1128_proxy_tuple, r1128_proxy_tuple_second)
        self.assertIsNot(
            r1128_proxy_tuple["reconstructed_material"], r1128_proxy_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1128_proxy_tuple["material_read"], r1128_proxy_tuple_second["material_read"])
        r1128_proxy_omitted = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}))
        r1128_proxy_omitted_second = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}))
        self.assertIsNot(r1128_proxy_omitted, r1128_proxy_omitted_second)
        self.assertIsNot(
            r1128_proxy_omitted["reconstructed_material"], r1128_proxy_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1128_proxy_omitted["material_read"], r1128_proxy_omitted_second["material_read"])
        r1128_proxy_none = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}), journal_records=None)
        r1128_proxy_none_second = module.resolve_dispute(disputed=MappingProxyType({"k": "v"}), journal_records=None)
        self.assertIsNot(r1128_proxy_none, r1128_proxy_none_second)
        self.assertIsNot(
            r1128_proxy_none["reconstructed_material"], r1128_proxy_none_second["reconstructed_material"])
        self.assertIsNot(
            r1128_proxy_none["material_read"], r1128_proxy_none_second["material_read"])
        r1128_namedtuple_tuple = module.resolve_dispute(disputed=namedtuple("R1128Tuple", ["field"])(1), journal_records=("journal record one", "journal record two"))
        r1128_namedtuple_tuple_second = module.resolve_dispute(disputed=namedtuple("R1128Tuple", ["field"])(1), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1128_namedtuple_tuple, r1128_namedtuple_tuple_second)
        self.assertIsNot(
            r1128_namedtuple_tuple["reconstructed_material"], r1128_namedtuple_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1128_namedtuple_tuple["material_read"], r1128_namedtuple_tuple_second["material_read"])
        r1128_namedtuple_omitted = module.resolve_dispute(disputed=namedtuple("R1128Tuple", ["field"])(1))
        r1128_namedtuple_omitted_second = module.resolve_dispute(disputed=namedtuple("R1128Tuple", ["field"])(1))
        self.assertIsNot(r1128_namedtuple_omitted, r1128_namedtuple_omitted_second)
        self.assertIsNot(
            r1128_namedtuple_omitted["reconstructed_material"], r1128_namedtuple_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1128_namedtuple_omitted["material_read"], r1128_namedtuple_omitted_second["material_read"])
        r1128_namedtuple_none = module.resolve_dispute(disputed=namedtuple("R1128Tuple", ["field"])(1), journal_records=None)
        r1128_namedtuple_none_second = module.resolve_dispute(disputed=namedtuple("R1128Tuple", ["field"])(1), journal_records=None)
        self.assertIsNot(r1128_namedtuple_none, r1128_namedtuple_none_second)
        self.assertIsNot(
            r1128_namedtuple_none["reconstructed_material"], r1128_namedtuple_none_second["reconstructed_material"])
        self.assertIsNot(
            r1128_namedtuple_none["material_read"], r1128_namedtuple_none_second["material_read"])
        r1128_keys_tuple = module.resolve_dispute(disputed={"k": "v"}.keys(), journal_records=("journal record one", "journal record two"))
        r1128_keys_tuple_second = module.resolve_dispute(disputed={"k": "v"}.keys(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1128_keys_tuple, r1128_keys_tuple_second)
        self.assertIsNot(
            r1128_keys_tuple["reconstructed_material"], r1128_keys_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1128_keys_tuple["material_read"], r1128_keys_tuple_second["material_read"])
        r1128_keys_omitted = module.resolve_dispute(disputed={"k": "v"}.keys())
        r1128_keys_omitted_second = module.resolve_dispute(disputed={"k": "v"}.keys())
        self.assertIsNot(r1128_keys_omitted, r1128_keys_omitted_second)
        self.assertIsNot(
            r1128_keys_omitted["reconstructed_material"], r1128_keys_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1128_keys_omitted["material_read"], r1128_keys_omitted_second["material_read"])
        r1128_keys_none = module.resolve_dispute(disputed={"k": "v"}.keys(), journal_records=None)
        r1128_keys_none_second = module.resolve_dispute(disputed={"k": "v"}.keys(), journal_records=None)
        self.assertIsNot(r1128_keys_none, r1128_keys_none_second)
        self.assertIsNot(
            r1128_keys_none["reconstructed_material"], r1128_keys_none_second["reconstructed_material"])
        self.assertIsNot(
            r1128_keys_none["material_read"], r1128_keys_none_second["material_read"])
        r1128_values_tuple = module.resolve_dispute(disputed={"k": "v"}.values(), journal_records=("journal record one", "journal record two"))
        r1128_values_tuple_second = module.resolve_dispute(disputed={"k": "v"}.values(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1128_values_tuple, r1128_values_tuple_second)
        self.assertIsNot(
            r1128_values_tuple["reconstructed_material"], r1128_values_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1128_values_tuple["material_read"], r1128_values_tuple_second["material_read"])
        r1128_values_omitted = module.resolve_dispute(disputed={"k": "v"}.values())
        r1128_values_omitted_second = module.resolve_dispute(disputed={"k": "v"}.values())
        self.assertIsNot(r1128_values_omitted, r1128_values_omitted_second)
        self.assertIsNot(
            r1128_values_omitted["reconstructed_material"], r1128_values_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1128_values_omitted["material_read"], r1128_values_omitted_second["material_read"])
        r1128_values_none = module.resolve_dispute(disputed={"k": "v"}.values(), journal_records=None)
        r1128_values_none_second = module.resolve_dispute(disputed={"k": "v"}.values(), journal_records=None)
        self.assertIsNot(r1128_values_none, r1128_values_none_second)
        self.assertIsNot(
            r1128_values_none["reconstructed_material"], r1128_values_none_second["reconstructed_material"])
        self.assertIsNot(
            r1128_values_none["material_read"], r1128_values_none_second["material_read"])
        r1128_intenum_tuple = module.resolve_dispute(disputed=IntEnum("R1128Enum", {"member": 1}).member, journal_records=("journal record one", "journal record two"))
        r1128_intenum_tuple_second = module.resolve_dispute(disputed=IntEnum("R1128Enum", {"member": 1}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1128_intenum_tuple, r1128_intenum_tuple_second)
        self.assertIsNot(
            r1128_intenum_tuple["reconstructed_material"], r1128_intenum_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1128_intenum_tuple["material_read"], r1128_intenum_tuple_second["material_read"])
        r1128_intenum_omitted = module.resolve_dispute(disputed=IntEnum("R1128Enum", {"member": 1}).member)
        r1128_intenum_omitted_second = module.resolve_dispute(disputed=IntEnum("R1128Enum", {"member": 1}).member)
        self.assertIsNot(r1128_intenum_omitted, r1128_intenum_omitted_second)
        self.assertIsNot(
            r1128_intenum_omitted["reconstructed_material"], r1128_intenum_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1128_intenum_omitted["material_read"], r1128_intenum_omitted_second["material_read"])
        r1128_intenum_none = module.resolve_dispute(disputed=IntEnum("R1128Enum", {"member": 1}).member, journal_records=None)
        r1128_intenum_none_second = module.resolve_dispute(disputed=IntEnum("R1128Enum", {"member": 1}).member, journal_records=None)
        self.assertIsNot(r1128_intenum_none, r1128_intenum_none_second)
        self.assertIsNot(
            r1128_intenum_none["reconstructed_material"], r1128_intenum_none_second["reconstructed_material"])
        self.assertIsNot(
            r1128_intenum_none["material_read"], r1128_intenum_none_second["material_read"])
        r1135_userlist_tuple = module.resolve_dispute(disputed=UserList([1]), journal_records=("journal record one", "journal record two"))
        r1135_userlist_tuple_second = module.resolve_dispute(disputed=UserList([1]), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1135_userlist_tuple, r1135_userlist_tuple_second)
        self.assertIsNot(
            r1135_userlist_tuple["reconstructed_material"], r1135_userlist_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userlist_tuple["material_read"], r1135_userlist_tuple_second["material_read"])
        r1135_userlist_omitted = module.resolve_dispute(disputed=UserList([1]))
        r1135_userlist_omitted_second = module.resolve_dispute(disputed=UserList([1]))
        self.assertIsNot(r1135_userlist_omitted, r1135_userlist_omitted_second)
        self.assertIsNot(
            r1135_userlist_omitted["reconstructed_material"], r1135_userlist_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userlist_omitted["material_read"], r1135_userlist_omitted_second["material_read"])
        r1135_userlist_none = module.resolve_dispute(disputed=UserList([1]), journal_records=None)
        r1135_userlist_none_second = module.resolve_dispute(disputed=UserList([1]), journal_records=None)
        self.assertIsNot(r1135_userlist_none, r1135_userlist_none_second)
        self.assertIsNot(
            r1135_userlist_none["reconstructed_material"], r1135_userlist_none_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userlist_none["material_read"], r1135_userlist_none_second["material_read"])
        r1135_userstring_tuple = module.resolve_dispute(disputed=UserString("x"), journal_records=("journal record one", "journal record two"))
        r1135_userstring_tuple_second = module.resolve_dispute(disputed=UserString("x"), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1135_userstring_tuple, r1135_userstring_tuple_second)
        self.assertIsNot(
            r1135_userstring_tuple["reconstructed_material"], r1135_userstring_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userstring_tuple["material_read"], r1135_userstring_tuple_second["material_read"])
        r1135_userstring_omitted = module.resolve_dispute(disputed=UserString("x"))
        r1135_userstring_omitted_second = module.resolve_dispute(disputed=UserString("x"))
        self.assertIsNot(r1135_userstring_omitted, r1135_userstring_omitted_second)
        self.assertIsNot(
            r1135_userstring_omitted["reconstructed_material"], r1135_userstring_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userstring_omitted["material_read"], r1135_userstring_omitted_second["material_read"])
        r1135_userstring_none = module.resolve_dispute(disputed=UserString("x"), journal_records=None)
        r1135_userstring_none_second = module.resolve_dispute(disputed=UserString("x"), journal_records=None)
        self.assertIsNot(r1135_userstring_none, r1135_userstring_none_second)
        self.assertIsNot(
            r1135_userstring_none["reconstructed_material"], r1135_userstring_none_second["reconstructed_material"])
        self.assertIsNot(
            r1135_userstring_none["material_read"], r1135_userstring_none_second["material_read"])

        r1212_slice = module.resolve_dispute(disputed=slice(1), journal_records=records)
        r1212_slice_second = module.resolve_dispute(disputed=slice(1), journal_records=records)
        self.assertIsNot(r1212_slice, r1212_slice_second)
        self.assertIsNot(
            r1212_slice["reconstructed_material"], r1212_slice_second["reconstructed_material"])
        self.assertIsNot(
            r1212_slice["material_read"], r1212_slice_second["material_read"])
        r1212_pattern = module.resolve_dispute(disputed=re.compile("a pattern"), journal_records=records)
        r1212_pattern_second = module.resolve_dispute(disputed=re.compile("a pattern"), journal_records=records)
        self.assertIsNot(r1212_pattern, r1212_pattern_second)
        self.assertIsNot(
            r1212_pattern["reconstructed_material"], r1212_pattern_second["reconstructed_material"])
        self.assertIsNot(
            r1212_pattern["material_read"], r1212_pattern_second["material_read"])
        r1212_enum = module.resolve_dispute(disputed=Enum("R1212Enum", {"member": 1}).member, journal_records=records)
        r1212_enum_second = module.resolve_dispute(disputed=Enum("R1212Enum", {"member": 1}).member, journal_records=records)
        self.assertIsNot(r1212_enum, r1212_enum_second)
        self.assertIsNot(
            r1212_enum["reconstructed_material"], r1212_enum_second["reconstructed_material"])
        self.assertIsNot(
            r1212_enum["material_read"], r1212_enum_second["material_read"])
        r1212_ipv4 = module.resolve_dispute(disputed=IPv4Address("1.2.3.4"), journal_records=records)
        r1212_ipv4_second = module.resolve_dispute(disputed=IPv4Address("1.2.3.4"), journal_records=records)
        self.assertIsNot(r1212_ipv4, r1212_ipv4_second)
        self.assertIsNot(
            r1212_ipv4["reconstructed_material"], r1212_ipv4_second["reconstructed_material"])
        self.assertIsNot(
            r1212_ipv4["material_read"], r1212_ipv4_second["material_read"])
        r1212_timezone = module.resolve_dispute(disputed=timezone.utc, journal_records=records)
        r1212_timezone_second = module.resolve_dispute(disputed=timezone.utc, journal_records=records)
        self.assertIsNot(r1212_timezone, r1212_timezone_second)
        self.assertIsNot(
            r1212_timezone["reconstructed_material"], r1212_timezone_second["reconstructed_material"])
        self.assertIsNot(
            r1212_timezone["material_read"], r1212_timezone_second["material_read"])

        r1221_items_tuple = module.resolve_dispute(disputed={"k": "v"}.items(), journal_records=("journal record one", "journal record two"))
        r1221_items_tuple_second = module.resolve_dispute(disputed={"k": "v"}.items(), journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1221_items_tuple, r1221_items_tuple_second)
        self.assertIsNot(
            r1221_items_tuple["reconstructed_material"], r1221_items_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1221_items_tuple["material_read"], r1221_items_tuple_second["material_read"])
        r1221_items_omitted = module.resolve_dispute(disputed={"k": "v"}.items())
        r1221_items_omitted_second = module.resolve_dispute(disputed={"k": "v"}.items())
        self.assertIsNot(r1221_items_omitted, r1221_items_omitted_second)
        self.assertIsNot(
            r1221_items_omitted["reconstructed_material"], r1221_items_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1221_items_omitted["material_read"], r1221_items_omitted_second["material_read"])
        r1221_items_none = module.resolve_dispute(disputed={"k": "v"}.items(), journal_records=None)
        r1221_items_none_second = module.resolve_dispute(disputed={"k": "v"}.items(), journal_records=None)
        self.assertIsNot(r1221_items_none, r1221_items_none_second)
        self.assertIsNot(
            r1221_items_none["reconstructed_material"], r1221_items_none_second["reconstructed_material"])
        self.assertIsNot(
            r1221_items_none["material_read"], r1221_items_none_second["material_read"])
        r1221_intflag_tuple = module.resolve_dispute(disputed=IntFlag("R1221Flag", {"member": 1}).member, journal_records=("journal record one", "journal record two"))
        r1221_intflag_tuple_second = module.resolve_dispute(disputed=IntFlag("R1221Flag", {"member": 1}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1221_intflag_tuple, r1221_intflag_tuple_second)
        self.assertIsNot(
            r1221_intflag_tuple["reconstructed_material"], r1221_intflag_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1221_intflag_tuple["material_read"], r1221_intflag_tuple_second["material_read"])
        r1221_intflag_omitted = module.resolve_dispute(disputed=IntFlag("R1221Flag", {"member": 1}).member)
        r1221_intflag_omitted_second = module.resolve_dispute(disputed=IntFlag("R1221Flag", {"member": 1}).member)
        self.assertIsNot(r1221_intflag_omitted, r1221_intflag_omitted_second)
        self.assertIsNot(
            r1221_intflag_omitted["reconstructed_material"], r1221_intflag_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1221_intflag_omitted["material_read"], r1221_intflag_omitted_second["material_read"])
        r1221_intflag_none = module.resolve_dispute(disputed=IntFlag("R1221Flag", {"member": 1}).member, journal_records=None)
        r1221_intflag_none_second = module.resolve_dispute(disputed=IntFlag("R1221Flag", {"member": 1}).member, journal_records=None)
        self.assertIsNot(r1221_intflag_none, r1221_intflag_none_second)
        self.assertIsNot(
            r1221_intflag_none["reconstructed_material"], r1221_intflag_none_second["reconstructed_material"])
        self.assertIsNot(
            r1221_intflag_none["material_read"], r1221_intflag_none_second["material_read"])
        r1221_strenum_tuple = module.resolve_dispute(disputed=StrEnum("R1221StrEnum", {"member": "x"}).member, journal_records=("journal record one", "journal record two"))
        r1221_strenum_tuple_second = module.resolve_dispute(disputed=StrEnum("R1221StrEnum", {"member": "x"}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1221_strenum_tuple, r1221_strenum_tuple_second)
        self.assertIsNot(
            r1221_strenum_tuple["reconstructed_material"], r1221_strenum_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1221_strenum_tuple["material_read"], r1221_strenum_tuple_second["material_read"])
        r1221_strenum_omitted = module.resolve_dispute(disputed=StrEnum("R1221StrEnum", {"member": "x"}).member)
        r1221_strenum_omitted_second = module.resolve_dispute(disputed=StrEnum("R1221StrEnum", {"member": "x"}).member)
        self.assertIsNot(r1221_strenum_omitted, r1221_strenum_omitted_second)
        self.assertIsNot(
            r1221_strenum_omitted["reconstructed_material"], r1221_strenum_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1221_strenum_omitted["material_read"], r1221_strenum_omitted_second["material_read"])
        r1221_strenum_none = module.resolve_dispute(disputed=StrEnum("R1221StrEnum", {"member": "x"}).member, journal_records=None)
        r1221_strenum_none_second = module.resolve_dispute(disputed=StrEnum("R1221StrEnum", {"member": "x"}).member, journal_records=None)
        self.assertIsNot(r1221_strenum_none, r1221_strenum_none_second)
        self.assertIsNot(
            r1221_strenum_none["reconstructed_material"], r1221_strenum_none_second["reconstructed_material"])
        self.assertIsNot(
            r1221_strenum_none["material_read"], r1221_strenum_none_second["material_read"])
        r1221_flag_tuple = module.resolve_dispute(disputed=Flag("R1221PlainFlag", {"member": 1}).member, journal_records=("journal record one", "journal record two"))
        r1221_flag_tuple_second = module.resolve_dispute(disputed=Flag("R1221PlainFlag", {"member": 1}).member, journal_records=("journal record one", "journal record two"))
        self.assertIsNot(r1221_flag_tuple, r1221_flag_tuple_second)
        self.assertIsNot(
            r1221_flag_tuple["reconstructed_material"], r1221_flag_tuple_second["reconstructed_material"])
        self.assertIsNot(
            r1221_flag_tuple["material_read"], r1221_flag_tuple_second["material_read"])
        r1221_flag_omitted = module.resolve_dispute(disputed=Flag("R1221PlainFlag", {"member": 1}).member)
        r1221_flag_omitted_second = module.resolve_dispute(disputed=Flag("R1221PlainFlag", {"member": 1}).member)
        self.assertIsNot(r1221_flag_omitted, r1221_flag_omitted_second)
        self.assertIsNot(
            r1221_flag_omitted["reconstructed_material"], r1221_flag_omitted_second["reconstructed_material"])
        self.assertIsNot(
            r1221_flag_omitted["material_read"], r1221_flag_omitted_second["material_read"])
        r1221_flag_none = module.resolve_dispute(disputed=Flag("R1221PlainFlag", {"member": 1}).member, journal_records=None)
        r1221_flag_none_second = module.resolve_dispute(disputed=Flag("R1221PlainFlag", {"member": 1}).member, journal_records=None)
        self.assertIsNot(r1221_flag_none, r1221_flag_none_second)
        self.assertIsNot(
            r1221_flag_none["reconstructed_material"], r1221_flag_none_second["reconstructed_material"])
        self.assertIsNot(
            r1221_flag_none["material_read"], r1221_flag_none_second["material_read"])

        r1223_path = module.resolve_dispute(disputed=Path("part"), journal_records=records)
        r1223_path_second = module.resolve_dispute(disputed=Path("part"), journal_records=records)
        self.assertIsNot(r1223_path, r1223_path_second)
        self.assertIsNot(
            r1223_path["reconstructed_material"], r1223_path_second["reconstructed_material"])
        self.assertIsNot(
            r1223_path["material_read"], r1223_path_second["material_read"])
        r1223_date = module.resolve_dispute(disputed=date(2026, 11, 17), journal_records=records)
        r1223_date_second = module.resolve_dispute(disputed=date(2026, 11, 17), journal_records=records)
        self.assertIsNot(r1223_date, r1223_date_second)
        self.assertIsNot(
            r1223_date["reconstructed_material"], r1223_date_second["reconstructed_material"])
        self.assertIsNot(
            r1223_date["material_read"], r1223_date_second["material_read"])
        r1223_datetime = module.resolve_dispute(disputed=datetime(2026, 11, 17, 12, 0), journal_records=records)
        r1223_datetime_second = module.resolve_dispute(disputed=datetime(2026, 11, 17, 12, 0), journal_records=records)
        self.assertIsNot(r1223_datetime, r1223_datetime_second)
        self.assertIsNot(
            r1223_datetime["reconstructed_material"], r1223_datetime_second["reconstructed_material"])
        self.assertIsNot(
            r1223_datetime["material_read"], r1223_datetime_second["material_read"])
        r1223_uuid = module.resolve_dispute(disputed=UUID(int=1), journal_records=records)
        r1223_uuid_second = module.resolve_dispute(disputed=UUID(int=1), journal_records=records)
        self.assertIsNot(r1223_uuid, r1223_uuid_second)
        self.assertIsNot(
            r1223_uuid["reconstructed_material"], r1223_uuid_second["reconstructed_material"])
        self.assertIsNot(
            r1223_uuid["material_read"], r1223_uuid_second["material_read"])
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
        r809_empty_bytes_stop = module.take_loading_stop(bundle=b"")
        r809_empty_bytes_second_stop = module.take_loading_stop(bundle=b"")
        self.assertIsNot(r809_empty_bytes_stop, r809_empty_bytes_second_stop)
        r809_empty_set_stop = module.take_loading_stop(bundle=set())
        r809_empty_set_second_stop = module.take_loading_stop(bundle=set())
        self.assertIsNot(r809_empty_set_stop, r809_empty_set_second_stop)
        r866_bytearray_stop = module.take_loading_stop(bundle=bytearray())
        r866_bytearray_second_stop = module.take_loading_stop(bundle=bytearray())
        self.assertIsNot(r866_bytearray_stop, r866_bytearray_second_stop)
        r866_complex_stop = module.take_loading_stop(bundle=0j)
        r866_complex_second_stop = module.take_loading_stop(bundle=0j)
        self.assertIsNot(r866_complex_stop, r866_complex_second_stop)
        r866_decimal_stop = module.take_loading_stop(bundle=Decimal(0))
        r866_decimal_second_stop = module.take_loading_stop(bundle=Decimal(0))
        self.assertIsNot(r866_decimal_stop, r866_decimal_second_stop)
        r866_frozenset_stop = module.take_loading_stop(bundle=frozenset())
        r866_frozenset_second_stop = module.take_loading_stop(bundle=frozenset())
        self.assertIsNot(r866_frozenset_stop, r866_frozenset_second_stop)
        r866_range_stop = module.take_loading_stop(bundle=range(0))
        r866_range_second_stop = module.take_loading_stop(bundle=range(0))
        self.assertIsNot(r866_range_stop, r866_range_second_stop)

        r924_memoryview_stop = module.take_loading_stop(bundle=memoryview(b""))
        r924_memoryview_second_stop = module.take_loading_stop(bundle=memoryview(b""))
        self.assertIsNot(r924_memoryview_stop, r924_memoryview_second_stop)
        r924_fraction_stop = module.take_loading_stop(bundle=Fraction(0))
        r924_fraction_second_stop = module.take_loading_stop(bundle=Fraction(0))
        self.assertIsNot(r924_fraction_stop, r924_fraction_second_stop)
        r924_deque_stop = module.take_loading_stop(bundle=deque())
        r924_deque_second_stop = module.take_loading_stop(bundle=deque())
        self.assertIsNot(r924_deque_stop, r924_deque_second_stop)
        r924_counter_stop = module.take_loading_stop(bundle=Counter())
        r924_counter_second_stop = module.take_loading_stop(bundle=Counter())
        self.assertIsNot(r924_counter_stop, r924_counter_second_stop)
        r924_ordered_stop = module.take_loading_stop(bundle=OrderedDict())
        r924_ordered_second_stop = module.take_loading_stop(bundle=OrderedDict())
        self.assertIsNot(r924_ordered_stop, r924_ordered_second_stop)
        r980_array_stop = module.take_loading_stop(bundle=array("i", []))
        r980_array_second_stop = module.take_loading_stop(bundle=array("i", []))
        self.assertIsNot(r980_array_stop, r980_array_second_stop)
        r980_chainmap_stop = module.take_loading_stop(bundle=ChainMap())
        r980_chainmap_second_stop = module.take_loading_stop(bundle=ChainMap())
        self.assertIsNot(r980_chainmap_stop, r980_chainmap_second_stop)
        r980_defaultdict_stop = module.take_loading_stop(bundle=defaultdict(int))
        r980_defaultdict_second_stop = module.take_loading_stop(bundle=defaultdict(int))
        self.assertIsNot(r980_defaultdict_stop, r980_defaultdict_second_stop)
        r980_timedelta_stop = module.take_loading_stop(bundle=timedelta(0))
        r980_timedelta_second_stop = module.take_loading_stop(bundle=timedelta(0))
        self.assertIsNot(r980_timedelta_stop, r980_timedelta_second_stop)
        r980_userdict_stop = module.take_loading_stop(bundle=UserDict())
        r980_userdict_second_stop = module.take_loading_stop(bundle=UserDict())
        self.assertIsNot(r980_userdict_stop, r980_userdict_second_stop)
        r986_memoryview_stop = module.take_loading_stop(bundle=memoryview(b"a bundle standing as a memoryview"))
        r986_memoryview_second_stop = module.take_loading_stop(bundle=memoryview(b"a bundle standing as a memoryview"))
        self.assertIsNot(r986_memoryview_stop, r986_memoryview_second_stop)
        r986_fraction_stop = module.take_loading_stop(bundle=Fraction(1, 2))
        r986_fraction_second_stop = module.take_loading_stop(bundle=Fraction(1, 2))
        self.assertIsNot(r986_fraction_stop, r986_fraction_second_stop)
        r986_deque_stop = module.take_loading_stop(bundle=deque(["a bundle standing as a deque"]))
        r986_deque_second_stop = module.take_loading_stop(bundle=deque(["a bundle standing as a deque"]))
        self.assertIsNot(r986_deque_stop, r986_deque_second_stop)
        r986_counter_stop = module.take_loading_stop(bundle=Counter({"a bundle key": 1}))
        r986_counter_second_stop = module.take_loading_stop(bundle=Counter({"a bundle key": 1}))
        self.assertIsNot(r986_counter_stop, r986_counter_second_stop)
        r986_ordered_stop = module.take_loading_stop(bundle=OrderedDict([("a bundle key", "a bundle value")]))
        r986_ordered_second_stop = module.take_loading_stop(bundle=OrderedDict([("a bundle key", "a bundle value")]))
        self.assertIsNot(r986_ordered_stop, r986_ordered_second_stop)
        r986_array_stop = module.take_loading_stop(bundle=array("i", [1]))
        r986_array_second_stop = module.take_loading_stop(bundle=array("i", [1]))
        self.assertIsNot(r986_array_stop, r986_array_second_stop)
        r1050_proxy_stop = module.take_loading_stop(bundle=MappingProxyType({}))
        r1050_proxy_second_stop = module.take_loading_stop(bundle=MappingProxyType({}))
        self.assertIsNot(r1050_proxy_stop, r1050_proxy_second_stop)
        r1050_namedtuple_stop = module.take_loading_stop(bundle=namedtuple("R1050Tuple", [])())
        r1050_namedtuple_second_stop = module.take_loading_stop(bundle=namedtuple("R1050Tuple", [])())
        self.assertIsNot(r1050_namedtuple_stop, r1050_namedtuple_second_stop)
        r1050_keys_stop = module.take_loading_stop(bundle={}.keys())
        r1050_keys_second_stop = module.take_loading_stop(bundle={}.keys())
        self.assertIsNot(r1050_keys_stop, r1050_keys_second_stop)
        r1050_values_stop = module.take_loading_stop(bundle={}.values())
        r1050_values_second_stop = module.take_loading_stop(bundle={}.values())
        self.assertIsNot(r1050_values_stop, r1050_values_second_stop)
        r1050_intenum_stop = module.take_loading_stop(bundle=IntEnum("R1050Enum", {"member": 0}).member)
        r1050_intenum_second_stop = module.take_loading_stop(bundle=IntEnum("R1050Enum", {"member": 0}).member)
        self.assertIsNot(r1050_intenum_stop, r1050_intenum_second_stop)
        r1056_chainmap_stop = module.take_loading_stop(bundle=ChainMap({"a bundle key": 1}))
        r1056_chainmap_second_stop = module.take_loading_stop(bundle=ChainMap({"a bundle key": 1}))
        self.assertIsNot(r1056_chainmap_stop, r1056_chainmap_second_stop)
        r1056_defaultdict_stop = module.take_loading_stop(bundle=defaultdict(int, {"a bundle key": 1}))
        r1056_defaultdict_second_stop = module.take_loading_stop(bundle=defaultdict(int, {"a bundle key": 1}))
        self.assertIsNot(r1056_defaultdict_stop, r1056_defaultdict_second_stop)
        r1056_timedelta_stop = module.take_loading_stop(bundle=timedelta(days=1))
        r1056_timedelta_second_stop = module.take_loading_stop(bundle=timedelta(days=1))
        self.assertIsNot(r1056_timedelta_stop, r1056_timedelta_second_stop)
        r1056_userdict_stop = module.take_loading_stop(bundle=UserDict({"a bundle key": "a bundle value"}))
        r1056_userdict_second_stop = module.take_loading_stop(bundle=UserDict({"a bundle key": "a bundle value"}))
        self.assertIsNot(r1056_userdict_stop, r1056_userdict_second_stop)
        r1062_userlist_empty_stop = module.take_loading_stop(bundle=UserList([]))
        r1062_userlist_empty_second_stop = module.take_loading_stop(bundle=UserList([]))
        self.assertIsNot(r1062_userlist_empty_stop, r1062_userlist_empty_second_stop)
        r1062_userlist_stop = module.take_loading_stop(bundle=UserList([1]))
        r1062_userlist_second_stop = module.take_loading_stop(bundle=UserList([1]))
        self.assertIsNot(r1062_userlist_stop, r1062_userlist_second_stop)
        r1062_userstring_empty_stop = module.take_loading_stop(bundle=UserString(""))
        r1062_userstring_empty_second_stop = module.take_loading_stop(bundle=UserString(""))
        self.assertIsNot(r1062_userstring_empty_stop, r1062_userstring_empty_second_stop)
        r1062_userstring_stop = module.take_loading_stop(bundle=UserString("x"))
        r1062_userstring_second_stop = module.take_loading_stop(bundle=UserString("x"))
        self.assertIsNot(r1062_userstring_stop, r1062_userstring_second_stop)

        r1122_proxy_stop = module.take_loading_stop(bundle=MappingProxyType({"k": "v"}))
        r1122_proxy_second_stop = module.take_loading_stop(bundle=MappingProxyType({"k": "v"}))
        self.assertIsNot(r1122_proxy_stop, r1122_proxy_second_stop)
        r1122_namedtuple_stop = module.take_loading_stop(bundle=namedtuple("R1122Tuple", ["field"])(1))
        r1122_namedtuple_second_stop = module.take_loading_stop(bundle=namedtuple("R1122Tuple", ["field"])(1))
        self.assertIsNot(r1122_namedtuple_stop, r1122_namedtuple_second_stop)
        r1122_keys_stop = module.take_loading_stop(bundle={"k": "v"}.keys())
        r1122_keys_second_stop = module.take_loading_stop(bundle={"k": "v"}.keys())
        self.assertIsNot(r1122_keys_stop, r1122_keys_second_stop)
        r1122_values_stop = module.take_loading_stop(bundle={"k": "v"}.values())
        r1122_values_second_stop = module.take_loading_stop(bundle={"k": "v"}.values())
        self.assertIsNot(r1122_values_stop, r1122_values_second_stop)
        r1122_intenum_stop = module.take_loading_stop(bundle=IntEnum("R1122Enum", {"member": 1}).member)
        r1122_intenum_second_stop = module.take_loading_stop(bundle=IntEnum("R1122Enum", {"member": 1}).member)
        self.assertIsNot(r1122_intenum_stop, r1122_intenum_second_stop)
        r1126_items_stop = module.take_loading_stop(bundle={"k": "v"}.items())
        r1126_items_second_stop = module.take_loading_stop(bundle={"k": "v"}.items())
        self.assertIsNot(r1126_items_stop, r1126_items_second_stop)
        r1126_items_empty_stop = module.take_loading_stop(bundle={}.items())
        r1126_items_empty_second_stop = module.take_loading_stop(bundle={}.items())
        self.assertIsNot(r1126_items_empty_stop, r1126_items_empty_second_stop)
        r1126_intflag_stop = module.take_loading_stop(bundle=IntFlag("R1126Flag", {"member": 1}).member)
        r1126_intflag_second_stop = module.take_loading_stop(bundle=IntFlag("R1126Flag", {"member": 1}).member)
        self.assertIsNot(r1126_intflag_stop, r1126_intflag_second_stop)
        r1126_intflag_zero_stop = module.take_loading_stop(bundle=IntFlag("R1126Flag", {"member": 0}).member)
        r1126_intflag_zero_second_stop = module.take_loading_stop(bundle=IntFlag("R1126Flag", {"member": 0}).member)
        self.assertIsNot(r1126_intflag_zero_stop, r1126_intflag_zero_second_stop)
        r1126_strenum_stop = module.take_loading_stop(bundle=StrEnum("R1126StrEnum", {"member": "x"}).member)
        r1126_strenum_second_stop = module.take_loading_stop(bundle=StrEnum("R1126StrEnum", {"member": "x"}).member)
        self.assertIsNot(r1126_strenum_stop, r1126_strenum_second_stop)
        r1126_strenum_empty_stop = module.take_loading_stop(bundle=StrEnum("R1126StrEnum", {"member": ""}).member)
        r1126_strenum_empty_second_stop = module.take_loading_stop(bundle=StrEnum("R1126StrEnum", {"member": ""}).member)
        self.assertIsNot(r1126_strenum_empty_stop, r1126_strenum_empty_second_stop)
        r1126_flag_stop = module.take_loading_stop(bundle=Flag("R1126PlainFlag", {"member": 1}).member)
        r1126_flag_second_stop = module.take_loading_stop(bundle=Flag("R1126PlainFlag", {"member": 1}).member)
        self.assertIsNot(r1126_flag_stop, r1126_flag_second_stop)
        r1126_flag_zero_stop = module.take_loading_stop(bundle=Flag("R1126PlainFlag", {"member": 0}).member)
        r1126_flag_zero_second_stop = module.take_loading_stop(bundle=Flag("R1126PlainFlag", {"member": 0}).member)
        self.assertIsNot(r1126_flag_zero_stop, r1126_flag_zero_second_stop)
        r1130_proxy_stop = module.take_loading_stop(bundle=MappingProxyType({"k": "v"}))
        r1130_proxy_second_stop = module.take_loading_stop(bundle=MappingProxyType({"k": "v"}))
        self.assertIsNot(r1130_proxy_stop, r1130_proxy_second_stop)
        r1130_namedtuple_stop = module.take_loading_stop(bundle=namedtuple("R1130Tuple", ["field"])(1))
        r1130_namedtuple_second_stop = module.take_loading_stop(bundle=namedtuple("R1130Tuple", ["field"])(1))
        self.assertIsNot(r1130_namedtuple_stop, r1130_namedtuple_second_stop)
        r1130_keys_stop = module.take_loading_stop(bundle={"k": "v"}.keys())
        r1130_keys_second_stop = module.take_loading_stop(bundle={"k": "v"}.keys())
        self.assertIsNot(r1130_keys_stop, r1130_keys_second_stop)
        r1130_values_stop = module.take_loading_stop(bundle={"k": "v"}.values())
        r1130_values_second_stop = module.take_loading_stop(bundle={"k": "v"}.values())
        self.assertIsNot(r1130_values_stop, r1130_values_second_stop)
        r1130_intenum_stop = module.take_loading_stop(bundle=IntEnum("R1130Enum", {"member": 1}).member)
        r1130_intenum_second_stop = module.take_loading_stop(bundle=IntEnum("R1130Enum", {"member": 1}).member)
        self.assertIsNot(r1130_intenum_stop, r1130_intenum_second_stop)
        r1136_date_stop = module.take_loading_stop(bundle=date(2026, 11, 17))
        r1136_date_second_stop = module.take_loading_stop(bundle=date(2026, 11, 17))
        self.assertIsNot(r1136_date_stop, r1136_date_second_stop)
        r1136_path_stop = module.take_loading_stop(bundle=Path("part"))
        r1136_path_second_stop = module.take_loading_stop(bundle=Path("part"))
        self.assertIsNot(r1136_path_stop, r1136_path_second_stop)

        r1215_slice_stop = module.take_loading_stop(bundle=slice(1))
        r1215_slice_stop_second = module.take_loading_stop(bundle=slice(1))
        self.assertIsNot(r1215_slice_stop, r1215_slice_stop_second)
        r1215_pattern_stop = module.take_loading_stop(bundle=re.compile("a pattern"))
        r1215_pattern_stop_second = module.take_loading_stop(bundle=re.compile("a pattern"))
        self.assertIsNot(r1215_pattern_stop, r1215_pattern_stop_second)
        r1215_enum_stop = module.take_loading_stop(bundle=Enum("R1215Enum", {"member": 1}).member)
        r1215_enum_stop_second = module.take_loading_stop(bundle=Enum("R1215Enum", {"member": 1}).member)
        self.assertIsNot(r1215_enum_stop, r1215_enum_stop_second)
        r1215_ipv4_stop = module.take_loading_stop(bundle=IPv4Address("1.2.3.4"))
        r1215_ipv4_stop_second = module.take_loading_stop(bundle=IPv4Address("1.2.3.4"))
        self.assertIsNot(r1215_ipv4_stop, r1215_ipv4_stop_second)
        r1215_timezone_stop = module.take_loading_stop(bundle=timezone.utc)
        r1215_timezone_stop_second = module.take_loading_stop(bundle=timezone.utc)
        self.assertIsNot(r1215_timezone_stop, r1215_timezone_stop_second)

        r1219_member = lambda: None
        r1219_element = Element("tag")
        r1219_element.append(Element("child"))
        r1219_element_empty = Element("tag")
        r1219_weakset = WeakSet([r1219_member])
        r1219_weakset_empty = WeakSet()
        r1219_weakkey = WeakKeyDictionary({r1219_member: "v"})
        r1219_weakkey_empty = WeakKeyDictionary()
        r1219_weakvalue = WeakValueDictionary({"k": r1219_member})
        r1219_weakvalue_empty = WeakValueDictionary()
        r1219_element_empty_stop = module.take_loading_stop(bundle=r1219_element_empty)
        r1219_element_empty_stop_second = module.take_loading_stop(bundle=r1219_element_empty)
        self.assertIsNot(r1219_element_empty_stop, r1219_element_empty_stop_second)
        r1219_element_stop = module.take_loading_stop(bundle=r1219_element)
        r1219_element_stop_second = module.take_loading_stop(bundle=r1219_element)
        self.assertIsNot(r1219_element_stop, r1219_element_stop_second)
        r1219_weakset_empty_stop = module.take_loading_stop(bundle=r1219_weakset_empty)
        r1219_weakset_empty_stop_second = module.take_loading_stop(bundle=r1219_weakset_empty)
        self.assertIsNot(r1219_weakset_empty_stop, r1219_weakset_empty_stop_second)
        r1219_weakset_stop = module.take_loading_stop(bundle=r1219_weakset)
        r1219_weakset_stop_second = module.take_loading_stop(bundle=r1219_weakset)
        self.assertIsNot(r1219_weakset_stop, r1219_weakset_stop_second)
        r1219_weakkey_empty_stop = module.take_loading_stop(bundle=r1219_weakkey_empty)
        r1219_weakkey_empty_stop_second = module.take_loading_stop(bundle=r1219_weakkey_empty)
        self.assertIsNot(r1219_weakkey_empty_stop, r1219_weakkey_empty_stop_second)
        r1219_weakkey_stop = module.take_loading_stop(bundle=r1219_weakkey)
        r1219_weakkey_stop_second = module.take_loading_stop(bundle=r1219_weakkey)
        self.assertIsNot(r1219_weakkey_stop, r1219_weakkey_stop_second)
        r1219_weakvalue_empty_stop = module.take_loading_stop(bundle=r1219_weakvalue_empty)
        r1219_weakvalue_empty_stop_second = module.take_loading_stop(bundle=r1219_weakvalue_empty)
        self.assertIsNot(r1219_weakvalue_empty_stop, r1219_weakvalue_empty_stop_second)
        r1219_weakvalue_stop = module.take_loading_stop(bundle=r1219_weakvalue)
        r1219_weakvalue_stop_second = module.take_loading_stop(bundle=r1219_weakvalue)
        self.assertIsNot(r1219_weakvalue_stop, r1219_weakvalue_stop_second)

        r1224_datetime_stop = module.take_loading_stop(bundle=datetime(2026, 11, 17, 12, 0))
        r1224_datetime_stop_second = module.take_loading_stop(bundle=datetime(2026, 11, 17, 12, 0))
        self.assertIsNot(r1224_datetime_stop, r1224_datetime_stop_second)
        r1224_uuid_stop = module.take_loading_stop(bundle=UUID(int=1))
        r1224_uuid_stop_second = module.take_loading_stop(bundle=UUID(int=1))
        self.assertIsNot(r1224_uuid_stop, r1224_uuid_stop_second)
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
        r808_purge_list = module.incident_append_order(acts=["purge append", "purge append", "purge append"])
        r808_purge_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append"])
        self.assertIsNot(r808_purge_list, r808_purge_list_second)
        self.assertEqual(list(r808_purge_list), ["purge append", "purge append", "purge append"])
        r808_repair_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification"))
        r808_repair_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r808_repair_tuple, r808_repair_tuple_second)
        self.assertEqual(list(r808_repair_tuple), ["repair verification", "repair verification", "repair verification"])
        r808_stop_list = module.incident_append_order(acts=["stop append", "stop append", "stop append"])
        r808_stop_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append"])
        self.assertIsNot(r808_stop_list, r808_stop_list_second)
        self.assertEqual(list(r808_stop_list), ["stop append", "stop append", "stop append"])
        r865_purge_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append"))
        r865_purge_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append"))
        self.assertIsNot(r865_purge_tuple, r865_purge_tuple_second)
        self.assertEqual(list(r865_purge_tuple), ["purge append", "purge append", "purge append"])
        r865_repair_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification"])
        r865_repair_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r865_repair_list, r865_repair_list_second)
        self.assertEqual(list(r865_repair_list), ["repair verification", "repair verification", "repair verification"])
        r865_stop_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append"))
        r865_stop_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append"))
        self.assertIsNot(r865_stop_tuple, r865_stop_tuple_second)
        self.assertEqual(list(r865_stop_tuple), ["stop append", "stop append", "stop append"])
        r865_purge_four_list = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append"])
        r865_purge_four_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append"])
        self.assertIsNot(r865_purge_four_list, r865_purge_four_list_second)
        self.assertEqual(list(r865_purge_four_list), ["purge append", "purge append", "purge append", "purge append"])
        r865_stop_four_list = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append"])
        r865_stop_four_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append"])
        self.assertIsNot(r865_stop_four_list, r865_stop_four_list_second)
        self.assertEqual(list(r865_stop_four_list), ["stop append", "stop append", "stop append", "stop append"])
        r865_repair_four_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification"))
        r865_repair_four_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r865_repair_four_tuple, r865_repair_four_tuple_second)
        self.assertEqual(list(r865_repair_four_tuple), ["repair verification", "repair verification", "repair verification", "repair verification"])
        r865_purge_four_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append"))
        r865_purge_four_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append"))
        self.assertIsNot(r865_purge_four_tuple, r865_purge_four_tuple_second)
        self.assertEqual(list(r865_purge_four_tuple), ["purge append", "purge append", "purge append", "purge append"])
        r865_stop_four_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append"))
        r865_stop_four_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append"))
        self.assertIsNot(r865_stop_four_tuple, r865_stop_four_tuple_second)
        self.assertEqual(list(r865_stop_four_tuple), ["stop append", "stop append", "stop append", "stop append"])
        r865_repair_four_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification"])
        r865_repair_four_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r865_repair_four_list, r865_repair_four_list_second)
        self.assertEqual(list(r865_repair_four_list), ["repair verification", "repair verification", "repair verification", "repair verification"])

        r923_purge_five_list = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append"])
        r923_purge_five_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append"])
        self.assertIsNot(r923_purge_five_list, r923_purge_five_list_second)
        self.assertEqual(list(r923_purge_five_list), ["purge append", "purge append", "purge append", "purge append", "purge append"])
        r923_purge_five_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append"))
        r923_purge_five_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append"))
        self.assertIsNot(r923_purge_five_tuple, r923_purge_five_tuple_second)
        self.assertEqual(list(r923_purge_five_tuple), ["purge append", "purge append", "purge append", "purge append", "purge append"])
        r923_repair_five_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r923_repair_five_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r923_repair_five_list, r923_repair_five_list_second)
        self.assertEqual(list(r923_repair_five_list), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r923_repair_five_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        r923_repair_five_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r923_repair_five_tuple, r923_repair_five_tuple_second)
        self.assertEqual(list(r923_repair_five_tuple), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r923_stop_five_list = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append"])
        r923_stop_five_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append"])
        self.assertIsNot(r923_stop_five_list, r923_stop_five_list_second)
        self.assertEqual(list(r923_stop_five_list), ["stop append", "stop append", "stop append", "stop append", "stop append"])
        r923_stop_five_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append"))
        r923_stop_five_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append"))
        self.assertIsNot(r923_stop_five_tuple, r923_stop_five_tuple_second)
        self.assertEqual(list(r923_stop_five_tuple), ["stop append", "stop append", "stop append", "stop append", "stop append"])
        r979_purge_six_list = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r979_purge_six_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        self.assertIsNot(r979_purge_six_list, r979_purge_six_list_second)
        self.assertEqual(list(r979_purge_six_list), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r979_purge_six_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        r979_purge_six_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        self.assertIsNot(r979_purge_six_tuple, r979_purge_six_tuple_second)
        self.assertEqual(list(r979_purge_six_tuple), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r979_repair_six_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r979_repair_six_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r979_repair_six_list, r979_repair_six_list_second)
        self.assertEqual(list(r979_repair_six_list), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r979_repair_six_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        r979_repair_six_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r979_repair_six_tuple, r979_repair_six_tuple_second)
        self.assertEqual(list(r979_repair_six_tuple), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r979_stop_six_list = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r979_stop_six_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        self.assertIsNot(r979_stop_six_list, r979_stop_six_list_second)
        self.assertEqual(list(r979_stop_six_list), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r979_stop_six_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        r979_stop_six_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        self.assertIsNot(r979_stop_six_tuple, r979_stop_six_tuple_second)
        self.assertEqual(list(r979_stop_six_tuple), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1049_purge_seven_list = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1049_purge_seven_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        self.assertIsNot(r1049_purge_seven_list, r1049_purge_seven_list_second)
        self.assertEqual(list(r1049_purge_seven_list), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1049_purge_seven_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        r1049_purge_seven_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        self.assertIsNot(r1049_purge_seven_tuple, r1049_purge_seven_tuple_second)
        self.assertEqual(list(r1049_purge_seven_tuple), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1049_repair_seven_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1049_repair_seven_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r1049_repair_seven_list, r1049_repair_seven_list_second)
        self.assertEqual(list(r1049_repair_seven_list), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1049_repair_seven_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        r1049_repair_seven_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r1049_repair_seven_tuple, r1049_repair_seven_tuple_second)
        self.assertEqual(list(r1049_repair_seven_tuple), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1049_stop_seven_list = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1049_stop_seven_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        self.assertIsNot(r1049_stop_seven_list, r1049_stop_seven_list_second)
        self.assertEqual(list(r1049_stop_seven_list), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1049_stop_seven_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        r1049_stop_seven_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        self.assertIsNot(r1049_stop_seven_tuple, r1049_stop_seven_tuple_second)
        self.assertEqual(list(r1049_stop_seven_tuple), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])

        r1121_purge_eight_list = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1121_purge_eight_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        self.assertIsNot(r1121_purge_eight_list, r1121_purge_eight_list_second)
        self.assertEqual(list(r1121_purge_eight_list), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1121_purge_eight_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        r1121_purge_eight_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        self.assertIsNot(r1121_purge_eight_tuple, r1121_purge_eight_tuple_second)
        self.assertEqual(list(r1121_purge_eight_tuple), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1121_repair_eight_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1121_repair_eight_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r1121_repair_eight_list, r1121_repair_eight_list_second)
        self.assertEqual(list(r1121_repair_eight_list), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1121_repair_eight_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        r1121_repair_eight_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r1121_repair_eight_tuple, r1121_repair_eight_tuple_second)
        self.assertEqual(list(r1121_repair_eight_tuple), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1121_stop_eight_list = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1121_stop_eight_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        self.assertIsNot(r1121_stop_eight_list, r1121_stop_eight_list_second)
        self.assertEqual(list(r1121_stop_eight_list), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1121_stop_eight_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        r1121_stop_eight_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        self.assertIsNot(r1121_stop_eight_tuple, r1121_stop_eight_tuple_second)
        self.assertEqual(list(r1121_stop_eight_tuple), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])

        r1214_purge_nine_list = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1214_purge_nine_list_second = module.incident_append_order(acts=["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        self.assertIsNot(r1214_purge_nine_list, r1214_purge_nine_list_second)
        self.assertEqual(list(r1214_purge_nine_list), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1214_purge_nine_tuple = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        r1214_purge_nine_tuple_second = module.incident_append_order(acts=("purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"))
        self.assertIsNot(r1214_purge_nine_tuple, r1214_purge_nine_tuple_second)
        self.assertEqual(list(r1214_purge_nine_tuple), ["purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append", "purge append"])
        r1214_repair_nine_list = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1214_repair_nine_list_second = module.incident_append_order(acts=["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        self.assertIsNot(r1214_repair_nine_list, r1214_repair_nine_list_second)
        self.assertEqual(list(r1214_repair_nine_list), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1214_repair_nine_tuple = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        r1214_repair_nine_tuple_second = module.incident_append_order(acts=("repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"))
        self.assertIsNot(r1214_repair_nine_tuple, r1214_repair_nine_tuple_second)
        self.assertEqual(list(r1214_repair_nine_tuple), ["repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification", "repair verification"])
        r1214_stop_nine_list = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1214_stop_nine_list_second = module.incident_append_order(acts=["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        self.assertIsNot(r1214_stop_nine_list, r1214_stop_nine_list_second)
        self.assertEqual(list(r1214_stop_nine_list), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
        r1214_stop_nine_tuple = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        r1214_stop_nine_tuple_second = module.incident_append_order(acts=("stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"))
        self.assertIsNot(r1214_stop_nine_tuple, r1214_stop_nine_tuple_second)
        self.assertEqual(list(r1214_stop_nine_tuple), ["stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append", "stop append"])
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
        r810_empty_mapping_stop = dict(stop)
        r810_empty_mapping_stop["effective_on_loading"] = {}
        r810_empty_mapping = module.discovery_after_stop(r810_empty_mapping_stop, bundle=bundle)
        r810_empty_mapping_second = module.discovery_after_stop(r810_empty_mapping_stop, bundle=bundle)
        self.assertIsNot(r810_empty_mapping, r810_empty_mapping_second)
        self.assertEqual(r810_empty_mapping["promotion"], bundle)
        r810_empty_tuple_stop = dict(stop)
        r810_empty_tuple_stop["effective_on_loading"] = ()
        r810_empty_tuple = module.discovery_after_stop(r810_empty_tuple_stop, bundle=bundle)
        r810_empty_tuple_second = module.discovery_after_stop(r810_empty_tuple_stop, bundle=bundle)
        self.assertIsNot(r810_empty_tuple, r810_empty_tuple_second)
        self.assertEqual(r810_empty_tuple["promotion"], bundle)
        r810_empty_bytes_stop = dict(stop)
        r810_empty_bytes_stop["effective_on_loading"] = b""
        r810_empty_bytes = module.discovery_after_stop(r810_empty_bytes_stop, bundle=bundle)
        r810_empty_bytes_second = module.discovery_after_stop(r810_empty_bytes_stop, bundle=bundle)
        self.assertIsNot(r810_empty_bytes, r810_empty_bytes_second)
        self.assertEqual(r810_empty_bytes["promotion"], bundle)
        r811_empty_string_none_stop = dict(stop)
        r811_empty_string_none_stop["effective_on_loading"] = ""
        r811_empty_string_none = module.discovery_after_stop(r811_empty_string_none_stop, bundle=None)
        r811_empty_string_none_second = module.discovery_after_stop(r811_empty_string_none_stop, bundle=None)
        self.assertIsNot(r811_empty_string_none, r811_empty_string_none_second)
        self.assertEqual(r811_empty_string_none["promotion"], None)
        self.assertEqual(r811_empty_string_none["bundle"], bundle)
        r811_empty_string_omitted_stop = dict(stop)
        r811_empty_string_omitted_stop["effective_on_loading"] = ""
        r811_empty_string_omitted = module.discovery_after_stop(r811_empty_string_omitted_stop)
        r811_empty_string_omitted_second = module.discovery_after_stop(r811_empty_string_omitted_stop)
        self.assertIsNot(r811_empty_string_omitted, r811_empty_string_omitted_second)
        self.assertEqual(r811_empty_string_omitted["promotion"], None)
        self.assertEqual(r811_empty_string_omitted["bundle"], bundle)
        r811_float_zero_none_stop = dict(stop)
        r811_float_zero_none_stop["effective_on_loading"] = 0.0
        r811_float_zero_none = module.discovery_after_stop(r811_float_zero_none_stop, bundle=None)
        r811_float_zero_none_second = module.discovery_after_stop(r811_float_zero_none_stop, bundle=None)
        self.assertIsNot(r811_float_zero_none, r811_float_zero_none_second)
        self.assertEqual(r811_float_zero_none["promotion"], None)
        self.assertEqual(r811_float_zero_none["bundle"], bundle)
        r811_float_zero_omitted_stop = dict(stop)
        r811_float_zero_omitted_stop["effective_on_loading"] = 0.0
        r811_float_zero_omitted = module.discovery_after_stop(r811_float_zero_omitted_stop)
        r811_float_zero_omitted_second = module.discovery_after_stop(r811_float_zero_omitted_stop)
        self.assertIsNot(r811_float_zero_omitted, r811_float_zero_omitted_second)
        self.assertEqual(r811_float_zero_omitted["promotion"], None)
        self.assertEqual(r811_float_zero_omitted["bundle"], bundle)
        r811_empty_list_none_stop = dict(stop)
        r811_empty_list_none_stop["effective_on_loading"] = []
        r811_empty_list_none = module.discovery_after_stop(r811_empty_list_none_stop, bundle=None)
        r811_empty_list_none_second = module.discovery_after_stop(r811_empty_list_none_stop, bundle=None)
        self.assertIsNot(r811_empty_list_none, r811_empty_list_none_second)
        self.assertEqual(r811_empty_list_none["promotion"], None)
        self.assertEqual(r811_empty_list_none["bundle"], bundle)
        r811_empty_list_omitted_stop = dict(stop)
        r811_empty_list_omitted_stop["effective_on_loading"] = []
        r811_empty_list_omitted = module.discovery_after_stop(r811_empty_list_omitted_stop)
        r811_empty_list_omitted_second = module.discovery_after_stop(r811_empty_list_omitted_stop)
        self.assertIsNot(r811_empty_list_omitted, r811_empty_list_omitted_second)
        self.assertEqual(r811_empty_list_omitted["promotion"], None)
        self.assertEqual(r811_empty_list_omitted["bundle"], bundle)
        r812_bytes = module.discovery_after_stop(b"a stop standing as bytes", bundle=bundle)
        r812_bytes_second = module.discovery_after_stop(b"a stop standing as bytes", bundle=bundle)
        self.assertIsNot(r812_bytes, r812_bytes_second)
        self.assertEqual(r812_bytes["promotion"], bundle)
        self.assertEqual(r812_bytes["bundle"], bundle)
        r812_integer = module.discovery_after_stop(7, bundle=bundle)
        r812_integer_second = module.discovery_after_stop(7, bundle=bundle)
        self.assertIsNot(r812_integer, r812_integer_second)
        self.assertEqual(r812_integer["promotion"], bundle)
        self.assertEqual(r812_integer["bundle"], bundle)
        r813_list_none = module.discovery_after_stop(["a stop standing as a list"], bundle=None)
        r813_list_none_second = module.discovery_after_stop(["a stop standing as a list"], bundle=None)
        self.assertIsNot(r813_list_none, r813_list_none_second)
        self.assertEqual(r813_list_none["promotion"], None)
        self.assertEqual(r813_list_none["bundle"], None)
        r813_list_omitted = module.discovery_after_stop(["a stop standing as a list"])
        r813_list_omitted_second = module.discovery_after_stop(["a stop standing as a list"])
        self.assertIsNot(r813_list_omitted, r813_list_omitted_second)
        self.assertEqual(r813_list_omitted["promotion"], None)
        self.assertEqual(r813_list_omitted["bundle"], None)
        r813_tuple_none = module.discovery_after_stop(("a stop standing as a tuple",), bundle=None)
        r813_tuple_none_second = module.discovery_after_stop(("a stop standing as a tuple",), bundle=None)
        self.assertIsNot(r813_tuple_none, r813_tuple_none_second)
        self.assertEqual(r813_tuple_none["promotion"], None)
        self.assertEqual(r813_tuple_none["bundle"], None)
        r813_tuple_omitted = module.discovery_after_stop(("a stop standing as a tuple",))
        r813_tuple_omitted_second = module.discovery_after_stop(("a stop standing as a tuple",))
        self.assertIsNot(r813_tuple_omitted, r813_tuple_omitted_second)
        self.assertEqual(r813_tuple_omitted["promotion"], None)
        self.assertEqual(r813_tuple_omitted["bundle"], None)
        r867_empty_set_stop = dict(stop)
        r867_empty_set_stop["effective_on_loading"] = set()
        r867_empty_set = module.discovery_after_stop(r867_empty_set_stop, bundle=bundle)
        r867_empty_set_second = module.discovery_after_stop(r867_empty_set_stop, bundle=bundle)
        self.assertIsNot(r867_empty_set, r867_empty_set_second)
        self.assertEqual(r867_empty_set["promotion"], bundle)
        r867_bytearray_stop = dict(stop)
        r867_bytearray_stop["effective_on_loading"] = bytearray()
        r867_bytearray = module.discovery_after_stop(r867_bytearray_stop, bundle=bundle)
        r867_bytearray_second = module.discovery_after_stop(r867_bytearray_stop, bundle=bundle)
        self.assertIsNot(r867_bytearray, r867_bytearray_second)
        self.assertEqual(r867_bytearray["promotion"], bundle)
        r867_complex_stop = dict(stop)
        r867_complex_stop["effective_on_loading"] = 0j
        r867_complex = module.discovery_after_stop(r867_complex_stop, bundle=bundle)
        r867_complex_second = module.discovery_after_stop(r867_complex_stop, bundle=bundle)
        self.assertIsNot(r867_complex, r867_complex_second)
        self.assertEqual(r867_complex["promotion"], bundle)
        r867_frozenset_stop = dict(stop)
        r867_frozenset_stop["effective_on_loading"] = frozenset()
        r867_frozenset = module.discovery_after_stop(r867_frozenset_stop, bundle=bundle)
        r867_frozenset_second = module.discovery_after_stop(r867_frozenset_stop, bundle=bundle)
        self.assertIsNot(r867_frozenset, r867_frozenset_second)
        self.assertEqual(r867_frozenset["promotion"], bundle)
        r867_decimal_stop = dict(stop)
        r867_decimal_stop["effective_on_loading"] = Decimal(0)
        r867_decimal = module.discovery_after_stop(r867_decimal_stop, bundle=bundle)
        r867_decimal_second = module.discovery_after_stop(r867_decimal_stop, bundle=bundle)
        self.assertIsNot(r867_decimal, r867_decimal_second)
        self.assertEqual(r867_decimal["promotion"], bundle)
        r868_float = module.discovery_after_stop(1.5, bundle=bundle)
        r868_float_second = module.discovery_after_stop(1.5, bundle=bundle)
        self.assertIsNot(r868_float, r868_float_second)
        self.assertEqual(r868_float["promotion"], bundle)
        self.assertEqual(r868_float["bundle"], bundle)
        r868_float_zero = module.discovery_after_stop(0.0, bundle=bundle)
        r868_float_zero_second = module.discovery_after_stop(0.0, bundle=bundle)
        self.assertIsNot(r868_float_zero, r868_float_zero_second)
        self.assertEqual(r868_float_zero["promotion"], bundle)
        self.assertEqual(r868_float_zero["bundle"], bundle)
        r868_set = module.discovery_after_stop({"a stop standing as a set"}, bundle=bundle)
        r868_set_second = module.discovery_after_stop({"a stop standing as a set"}, bundle=bundle)
        self.assertIsNot(r868_set, r868_set_second)
        self.assertEqual(r868_set["promotion"], bundle)
        self.assertEqual(r868_set["bundle"], bundle)
        r868_frozenset = module.discovery_after_stop(frozenset({"a stop standing as a frozenset"}), bundle=bundle)
        r868_frozenset_second = module.discovery_after_stop(frozenset({"a stop standing as a frozenset"}), bundle=bundle)
        self.assertIsNot(r868_frozenset, r868_frozenset_second)
        self.assertEqual(r868_frozenset["promotion"], bundle)
        self.assertEqual(r868_frozenset["bundle"], bundle)
        r868_true = module.discovery_after_stop(True, bundle=bundle)
        r868_true_second = module.discovery_after_stop(True, bundle=bundle)
        self.assertIsNot(r868_true, r868_true_second)
        self.assertEqual(r868_true["promotion"], bundle)
        self.assertEqual(r868_true["bundle"], bundle)
        r868_bytearray = module.discovery_after_stop(bytearray(b"a stop standing as a bytearray"), bundle=bundle)
        r868_bytearray_second = module.discovery_after_stop(bytearray(b"a stop standing as a bytearray"), bundle=bundle)
        self.assertIsNot(r868_bytearray, r868_bytearray_second)
        self.assertEqual(r868_bytearray["promotion"], bundle)
        self.assertEqual(r868_bytearray["bundle"], bundle)
        r872_empty_mapping_none_stop = dict(stop)
        r872_empty_mapping_none_stop["effective_on_loading"] = {}
        r872_empty_mapping_none = module.discovery_after_stop(r872_empty_mapping_none_stop, bundle=None)
        r872_empty_mapping_none_second = module.discovery_after_stop(r872_empty_mapping_none_stop, bundle=None)
        self.assertIsNot(r872_empty_mapping_none, r872_empty_mapping_none_second)
        self.assertEqual(r872_empty_mapping_none["promotion"], None)
        self.assertEqual(r872_empty_mapping_none["bundle"], bundle)
        r872_empty_mapping_omitted_stop = dict(stop)
        r872_empty_mapping_omitted_stop["effective_on_loading"] = {}
        r872_empty_mapping_omitted = module.discovery_after_stop(r872_empty_mapping_omitted_stop)
        r872_empty_mapping_omitted_second = module.discovery_after_stop(r872_empty_mapping_omitted_stop)
        self.assertIsNot(r872_empty_mapping_omitted, r872_empty_mapping_omitted_second)
        self.assertEqual(r872_empty_mapping_omitted["promotion"], None)
        self.assertEqual(r872_empty_mapping_omitted["bundle"], bundle)
        r872_empty_tuple_none_stop = dict(stop)
        r872_empty_tuple_none_stop["effective_on_loading"] = ()
        r872_empty_tuple_none = module.discovery_after_stop(r872_empty_tuple_none_stop, bundle=None)
        r872_empty_tuple_none_second = module.discovery_after_stop(r872_empty_tuple_none_stop, bundle=None)
        self.assertIsNot(r872_empty_tuple_none, r872_empty_tuple_none_second)
        self.assertEqual(r872_empty_tuple_none["promotion"], None)
        self.assertEqual(r872_empty_tuple_none["bundle"], bundle)
        r872_empty_tuple_omitted_stop = dict(stop)
        r872_empty_tuple_omitted_stop["effective_on_loading"] = ()
        r872_empty_tuple_omitted = module.discovery_after_stop(r872_empty_tuple_omitted_stop)
        r872_empty_tuple_omitted_second = module.discovery_after_stop(r872_empty_tuple_omitted_stop)
        self.assertIsNot(r872_empty_tuple_omitted, r872_empty_tuple_omitted_second)
        self.assertEqual(r872_empty_tuple_omitted["promotion"], None)
        self.assertEqual(r872_empty_tuple_omitted["bundle"], bundle)
        r872_empty_bytes_none_stop = dict(stop)
        r872_empty_bytes_none_stop["effective_on_loading"] = b""
        r872_empty_bytes_none = module.discovery_after_stop(r872_empty_bytes_none_stop, bundle=None)
        r872_empty_bytes_none_second = module.discovery_after_stop(r872_empty_bytes_none_stop, bundle=None)
        self.assertIsNot(r872_empty_bytes_none, r872_empty_bytes_none_second)
        self.assertEqual(r872_empty_bytes_none["promotion"], None)
        self.assertEqual(r872_empty_bytes_none["bundle"], bundle)
        r872_empty_bytes_omitted_stop = dict(stop)
        r872_empty_bytes_omitted_stop["effective_on_loading"] = b""
        r872_empty_bytes_omitted = module.discovery_after_stop(r872_empty_bytes_omitted_stop)
        r872_empty_bytes_omitted_second = module.discovery_after_stop(r872_empty_bytes_omitted_stop)
        self.assertIsNot(r872_empty_bytes_omitted, r872_empty_bytes_omitted_second)
        self.assertEqual(r872_empty_bytes_omitted["promotion"], None)
        self.assertEqual(r872_empty_bytes_omitted["bundle"], bundle)
        r873_bytes_none = module.discovery_after_stop(b"a stop standing as bytes", bundle=None)
        r873_bytes_none_second = module.discovery_after_stop(b"a stop standing as bytes", bundle=None)
        self.assertIsNot(r873_bytes_none, r873_bytes_none_second)
        self.assertEqual(r873_bytes_none["promotion"], None)
        self.assertEqual(r873_bytes_none["bundle"], None)
        r873_bytes_omitted = module.discovery_after_stop(b"a stop standing as bytes")
        r873_bytes_omitted_second = module.discovery_after_stop(b"a stop standing as bytes")
        self.assertIsNot(r873_bytes_omitted, r873_bytes_omitted_second)
        self.assertEqual(r873_bytes_omitted["promotion"], None)
        self.assertEqual(r873_bytes_omitted["bundle"], None)
        r873_integer_none = module.discovery_after_stop(7, bundle=None)
        r873_integer_none_second = module.discovery_after_stop(7, bundle=None)
        self.assertIsNot(r873_integer_none, r873_integer_none_second)
        self.assertEqual(r873_integer_none["promotion"], None)
        self.assertEqual(r873_integer_none["bundle"], None)
        r873_integer_omitted = module.discovery_after_stop(7)
        r873_integer_omitted_second = module.discovery_after_stop(7)
        self.assertIsNot(r873_integer_omitted, r873_integer_omitted_second)
        self.assertEqual(r873_integer_omitted["promotion"], None)
        self.assertEqual(r873_integer_omitted["bundle"], None)

        r925_memoryview_stop = dict(stop)
        r925_memoryview_stop["effective_on_loading"] = memoryview(b"")
        r925_memoryview = module.discovery_after_stop(r925_memoryview_stop, bundle=bundle)
        r925_memoryview_second = module.discovery_after_stop(r925_memoryview_stop, bundle=bundle)
        self.assertIsNot(r925_memoryview, r925_memoryview_second)
        self.assertEqual(r925_memoryview["promotion"], bundle)
        r925_fraction_stop = dict(stop)
        r925_fraction_stop["effective_on_loading"] = Fraction(0)
        r925_fraction = module.discovery_after_stop(r925_fraction_stop, bundle=bundle)
        r925_fraction_second = module.discovery_after_stop(r925_fraction_stop, bundle=bundle)
        self.assertIsNot(r925_fraction, r925_fraction_second)
        self.assertEqual(r925_fraction["promotion"], bundle)
        r925_deque_stop = dict(stop)
        r925_deque_stop["effective_on_loading"] = deque()
        r925_deque = module.discovery_after_stop(r925_deque_stop, bundle=bundle)
        r925_deque_second = module.discovery_after_stop(r925_deque_stop, bundle=bundle)
        self.assertIsNot(r925_deque, r925_deque_second)
        self.assertEqual(r925_deque["promotion"], bundle)
        r925_counter_stop = dict(stop)
        r925_counter_stop["effective_on_loading"] = Counter()
        r925_counter = module.discovery_after_stop(r925_counter_stop, bundle=bundle)
        r925_counter_second = module.discovery_after_stop(r925_counter_stop, bundle=bundle)
        self.assertIsNot(r925_counter, r925_counter_second)
        self.assertEqual(r925_counter["promotion"], bundle)
        r925_ordered_stop = dict(stop)
        r925_ordered_stop["effective_on_loading"] = OrderedDict()
        r925_ordered = module.discovery_after_stop(r925_ordered_stop, bundle=bundle)
        r925_ordered_second = module.discovery_after_stop(r925_ordered_stop, bundle=bundle)
        self.assertIsNot(r925_ordered, r925_ordered_second)
        self.assertEqual(r925_ordered["promotion"], bundle)
        r981_array_stop = dict(stop)
        r981_array_stop["effective_on_loading"] = array("i", [])
        r981_array = module.discovery_after_stop(r981_array_stop, bundle=bundle)
        r981_array_second = module.discovery_after_stop(r981_array_stop, bundle=bundle)
        self.assertIsNot(r981_array, r981_array_second)
        self.assertEqual(r981_array["promotion"], bundle)
        r981_chainmap_stop = dict(stop)
        r981_chainmap_stop["effective_on_loading"] = ChainMap()
        r981_chainmap = module.discovery_after_stop(r981_chainmap_stop, bundle=bundle)
        r981_chainmap_second = module.discovery_after_stop(r981_chainmap_stop, bundle=bundle)
        self.assertIsNot(r981_chainmap, r981_chainmap_second)
        self.assertEqual(r981_chainmap["promotion"], bundle)
        r981_defaultdict_stop = dict(stop)
        r981_defaultdict_stop["effective_on_loading"] = defaultdict(int)
        r981_defaultdict = module.discovery_after_stop(r981_defaultdict_stop, bundle=bundle)
        r981_defaultdict_second = module.discovery_after_stop(r981_defaultdict_stop, bundle=bundle)
        self.assertIsNot(r981_defaultdict, r981_defaultdict_second)
        self.assertEqual(r981_defaultdict["promotion"], bundle)
        r981_timedelta_stop = dict(stop)
        r981_timedelta_stop["effective_on_loading"] = timedelta(0)
        r981_timedelta = module.discovery_after_stop(r981_timedelta_stop, bundle=bundle)
        r981_timedelta_second = module.discovery_after_stop(r981_timedelta_stop, bundle=bundle)
        self.assertIsNot(r981_timedelta, r981_timedelta_second)
        self.assertEqual(r981_timedelta["promotion"], bundle)
        r981_userdict_stop = dict(stop)
        r981_userdict_stop["effective_on_loading"] = UserDict()
        r981_userdict = module.discovery_after_stop(r981_userdict_stop, bundle=bundle)
        r981_userdict_second = module.discovery_after_stop(r981_userdict_stop, bundle=bundle)
        self.assertIsNot(r981_userdict, r981_userdict_second)
        self.assertEqual(r981_userdict["promotion"], bundle)
        r926_memoryview = module.discovery_after_stop(memoryview(b"a stop standing as a memoryview"), bundle=bundle)
        r926_memoryview_second = module.discovery_after_stop(memoryview(b"a stop standing as a memoryview"), bundle=bundle)
        self.assertIsNot(r926_memoryview, r926_memoryview_second)
        self.assertEqual(r926_memoryview["promotion"], bundle)
        self.assertEqual(r926_memoryview["bundle"], bundle)
        r926_fraction = module.discovery_after_stop(Fraction(1, 2), bundle=bundle)
        r926_fraction_second = module.discovery_after_stop(Fraction(1, 2), bundle=bundle)
        self.assertIsNot(r926_fraction, r926_fraction_second)
        self.assertEqual(r926_fraction["promotion"], bundle)
        self.assertEqual(r926_fraction["bundle"], bundle)
        r926_deque = module.discovery_after_stop(deque(["a stop standing as a deque"]), bundle=bundle)
        r926_deque_second = module.discovery_after_stop(deque(["a stop standing as a deque"]), bundle=bundle)
        self.assertIsNot(r926_deque, r926_deque_second)
        self.assertEqual(r926_deque["promotion"], bundle)
        self.assertEqual(r926_deque["bundle"], bundle)
        r926_array = module.discovery_after_stop(array("i", [1]), bundle=bundle)
        r926_array_second = module.discovery_after_stop(array("i", [1]), bundle=bundle)
        self.assertIsNot(r926_array, r926_array_second)
        self.assertEqual(r926_array["promotion"], bundle)
        self.assertEqual(r926_array["bundle"], bundle)
        r926_object = module.discovery_after_stop(object(), bundle=bundle)
        r926_object_second = module.discovery_after_stop(object(), bundle=bundle)
        self.assertIsNot(r926_object, r926_object_second)
        self.assertEqual(r926_object["promotion"], bundle)
        self.assertEqual(r926_object["bundle"], bundle)
        r982_timedelta = module.discovery_after_stop(timedelta(days=1), bundle=bundle)
        r982_timedelta_second = module.discovery_after_stop(timedelta(days=1), bundle=bundle)
        self.assertIsNot(r982_timedelta, r982_timedelta_second)
        self.assertEqual(r982_timedelta["promotion"], bundle)
        self.assertEqual(r982_timedelta["bundle"], bundle)
        r982_userlist = module.discovery_after_stop(UserList([1]), bundle=bundle)
        r982_userlist_second = module.discovery_after_stop(UserList([1]), bundle=bundle)
        self.assertIsNot(r982_userlist, r982_userlist_second)
        self.assertEqual(r982_userlist["promotion"], bundle)
        self.assertEqual(r982_userlist["bundle"], bundle)
        r982_userstring = module.discovery_after_stop(UserString("x"), bundle=bundle)
        r982_userstring_second = module.discovery_after_stop(UserString("x"), bundle=bundle)
        self.assertIsNot(r982_userstring, r982_userstring_second)
        self.assertEqual(r982_userstring["promotion"], bundle)
        self.assertEqual(r982_userstring["bundle"], bundle)
        r982_complex = module.discovery_after_stop(1j, bundle=bundle)
        r982_complex_second = module.discovery_after_stop(1j, bundle=bundle)
        self.assertIsNot(r982_complex, r982_complex_second)
        self.assertEqual(r982_complex["promotion"], bundle)
        self.assertEqual(r982_complex["bundle"], bundle)
        r982_decimal = module.discovery_after_stop(Decimal(1), bundle=bundle)
        r982_decimal_second = module.discovery_after_stop(Decimal(1), bundle=bundle)
        self.assertIsNot(r982_decimal, r982_decimal_second)
        self.assertEqual(r982_decimal["promotion"], bundle)
        self.assertEqual(r982_decimal["bundle"], bundle)
        r987_memoryview_none_stop = dict(stop)
        r987_memoryview_none_stop["effective_on_loading"] = memoryview(b"")
        r987_memoryview_none = module.discovery_after_stop(r987_memoryview_none_stop, bundle=None)
        r987_memoryview_none_second = module.discovery_after_stop(r987_memoryview_none_stop, bundle=None)
        self.assertIsNot(r987_memoryview_none, r987_memoryview_none_second)
        r987_memoryview_omitted_stop = dict(stop)
        r987_memoryview_omitted_stop["effective_on_loading"] = memoryview(b"")
        r987_memoryview_omitted = module.discovery_after_stop(r987_memoryview_omitted_stop)
        r987_memoryview_omitted_second = module.discovery_after_stop(r987_memoryview_omitted_stop)
        self.assertIsNot(r987_memoryview_omitted, r987_memoryview_omitted_second)
        r987_fraction_none_stop = dict(stop)
        r987_fraction_none_stop["effective_on_loading"] = Fraction(0)
        r987_fraction_none = module.discovery_after_stop(r987_fraction_none_stop, bundle=None)
        r987_fraction_none_second = module.discovery_after_stop(r987_fraction_none_stop, bundle=None)
        self.assertIsNot(r987_fraction_none, r987_fraction_none_second)
        r987_fraction_omitted_stop = dict(stop)
        r987_fraction_omitted_stop["effective_on_loading"] = Fraction(0)
        r987_fraction_omitted = module.discovery_after_stop(r987_fraction_omitted_stop)
        r987_fraction_omitted_second = module.discovery_after_stop(r987_fraction_omitted_stop)
        self.assertIsNot(r987_fraction_omitted, r987_fraction_omitted_second)
        r987_deque_none_stop = dict(stop)
        r987_deque_none_stop["effective_on_loading"] = deque()
        r987_deque_none = module.discovery_after_stop(r987_deque_none_stop, bundle=None)
        r987_deque_none_second = module.discovery_after_stop(r987_deque_none_stop, bundle=None)
        self.assertIsNot(r987_deque_none, r987_deque_none_second)
        r987_deque_omitted_stop = dict(stop)
        r987_deque_omitted_stop["effective_on_loading"] = deque()
        r987_deque_omitted = module.discovery_after_stop(r987_deque_omitted_stop)
        r987_deque_omitted_second = module.discovery_after_stop(r987_deque_omitted_stop)
        self.assertIsNot(r987_deque_omitted, r987_deque_omitted_second)
        r987_counter_none_stop = dict(stop)
        r987_counter_none_stop["effective_on_loading"] = Counter()
        r987_counter_none = module.discovery_after_stop(r987_counter_none_stop, bundle=None)
        r987_counter_none_second = module.discovery_after_stop(r987_counter_none_stop, bundle=None)
        self.assertIsNot(r987_counter_none, r987_counter_none_second)
        r987_counter_omitted_stop = dict(stop)
        r987_counter_omitted_stop["effective_on_loading"] = Counter()
        r987_counter_omitted = module.discovery_after_stop(r987_counter_omitted_stop)
        r987_counter_omitted_second = module.discovery_after_stop(r987_counter_omitted_stop)
        self.assertIsNot(r987_counter_omitted, r987_counter_omitted_second)
        r987_ordered_none_stop = dict(stop)
        r987_ordered_none_stop["effective_on_loading"] = OrderedDict()
        r987_ordered_none = module.discovery_after_stop(r987_ordered_none_stop, bundle=None)
        r987_ordered_none_second = module.discovery_after_stop(r987_ordered_none_stop, bundle=None)
        self.assertIsNot(r987_ordered_none, r987_ordered_none_second)
        r987_ordered_omitted_stop = dict(stop)
        r987_ordered_omitted_stop["effective_on_loading"] = OrderedDict()
        r987_ordered_omitted = module.discovery_after_stop(r987_ordered_omitted_stop)
        r987_ordered_omitted_second = module.discovery_after_stop(r987_ordered_omitted_stop)
        self.assertIsNot(r987_ordered_omitted, r987_ordered_omitted_second)
        r987_array_stop = dict(stop)
        r987_array_stop["effective_on_loading"] = array("i", [1])
        r987_array = module.discovery_after_stop(r987_array_stop, bundle=bundle)
        r987_array_second = module.discovery_after_stop(r987_array_stop, bundle=bundle)
        self.assertIsNot(r987_array, r987_array_second)
        r988_memoryview_none = module.discovery_after_stop(memoryview(b"a stop standing as a memoryview"), bundle=None)
        r988_memoryview_none_second = module.discovery_after_stop(memoryview(b"a stop standing as a memoryview"), bundle=None)
        self.assertIsNot(r988_memoryview_none, r988_memoryview_none_second)
        r988_memoryview_omitted = module.discovery_after_stop(memoryview(b"a stop standing as a memoryview"))
        r988_memoryview_omitted_second = module.discovery_after_stop(memoryview(b"a stop standing as a memoryview"))
        self.assertIsNot(r988_memoryview_omitted, r988_memoryview_omitted_second)
        r988_fraction_none = module.discovery_after_stop(Fraction(1, 2), bundle=None)
        r988_fraction_none_second = module.discovery_after_stop(Fraction(1, 2), bundle=None)
        self.assertIsNot(r988_fraction_none, r988_fraction_none_second)
        r988_fraction_omitted = module.discovery_after_stop(Fraction(1, 2))
        r988_fraction_omitted_second = module.discovery_after_stop(Fraction(1, 2))
        self.assertIsNot(r988_fraction_omitted, r988_fraction_omitted_second)
        r988_deque_none = module.discovery_after_stop(deque(["a stop standing as a deque"]), bundle=None)
        r988_deque_none_second = module.discovery_after_stop(deque(["a stop standing as a deque"]), bundle=None)
        self.assertIsNot(r988_deque_none, r988_deque_none_second)
        r988_deque_omitted = module.discovery_after_stop(deque(["a stop standing as a deque"]))
        r988_deque_omitted_second = module.discovery_after_stop(deque(["a stop standing as a deque"]))
        self.assertIsNot(r988_deque_omitted, r988_deque_omitted_second)
        r988_array_none = module.discovery_after_stop(array("i", [1]), bundle=None)
        r988_array_none_second = module.discovery_after_stop(array("i", [1]), bundle=None)
        self.assertIsNot(r988_array_none, r988_array_none_second)
        r988_array_omitted = module.discovery_after_stop(array("i", [1]))
        r988_array_omitted_second = module.discovery_after_stop(array("i", [1]))
        self.assertIsNot(r988_array_omitted, r988_array_omitted_second)
        r988_object_none = module.discovery_after_stop(object(), bundle=None)
        r988_object_none_second = module.discovery_after_stop(object(), bundle=None)
        self.assertIsNot(r988_object_none, r988_object_none_second)
        r988_object_omitted = module.discovery_after_stop(object())
        r988_object_omitted_second = module.discovery_after_stop(object())
        self.assertIsNot(r988_object_omitted, r988_object_omitted_second)

        r931_empty_set_none_stop = dict(stop)
        r931_empty_set_none_stop["effective_on_loading"] = set()
        r931_empty_set_none = module.discovery_after_stop(r931_empty_set_none_stop, bundle=None)
        r931_empty_set_none_second = module.discovery_after_stop(r931_empty_set_none_stop, bundle=None)
        self.assertIsNot(r931_empty_set_none, r931_empty_set_none_second)
        self.assertEqual(r931_empty_set_none["promotion"], None)
        self.assertEqual(r931_empty_set_none["bundle"], bundle)
        r931_empty_set_omitted_stop = dict(stop)
        r931_empty_set_omitted_stop["effective_on_loading"] = set()
        r931_empty_set_omitted = module.discovery_after_stop(r931_empty_set_omitted_stop)
        r931_empty_set_omitted_second = module.discovery_after_stop(r931_empty_set_omitted_stop)
        self.assertIsNot(r931_empty_set_omitted, r931_empty_set_omitted_second)
        self.assertEqual(r931_empty_set_omitted["promotion"], None)
        self.assertEqual(r931_empty_set_omitted["bundle"], bundle)
        r931_bytearray_none_stop = dict(stop)
        r931_bytearray_none_stop["effective_on_loading"] = bytearray()
        r931_bytearray_none = module.discovery_after_stop(r931_bytearray_none_stop, bundle=None)
        r931_bytearray_none_second = module.discovery_after_stop(r931_bytearray_none_stop, bundle=None)
        self.assertIsNot(r931_bytearray_none, r931_bytearray_none_second)
        self.assertEqual(r931_bytearray_none["promotion"], None)
        self.assertEqual(r931_bytearray_none["bundle"], bundle)
        r931_bytearray_omitted_stop = dict(stop)
        r931_bytearray_omitted_stop["effective_on_loading"] = bytearray()
        r931_bytearray_omitted = module.discovery_after_stop(r931_bytearray_omitted_stop)
        r931_bytearray_omitted_second = module.discovery_after_stop(r931_bytearray_omitted_stop)
        self.assertIsNot(r931_bytearray_omitted, r931_bytearray_omitted_second)
        self.assertEqual(r931_bytearray_omitted["promotion"], None)
        self.assertEqual(r931_bytearray_omitted["bundle"], bundle)
        r931_complex_none_stop = dict(stop)
        r931_complex_none_stop["effective_on_loading"] = 0j
        r931_complex_none = module.discovery_after_stop(r931_complex_none_stop, bundle=None)
        r931_complex_none_second = module.discovery_after_stop(r931_complex_none_stop, bundle=None)
        self.assertIsNot(r931_complex_none, r931_complex_none_second)
        self.assertEqual(r931_complex_none["promotion"], None)
        self.assertEqual(r931_complex_none["bundle"], bundle)
        r931_complex_omitted_stop = dict(stop)
        r931_complex_omitted_stop["effective_on_loading"] = 0j
        r931_complex_omitted = module.discovery_after_stop(r931_complex_omitted_stop)
        r931_complex_omitted_second = module.discovery_after_stop(r931_complex_omitted_stop)
        self.assertIsNot(r931_complex_omitted, r931_complex_omitted_second)
        self.assertEqual(r931_complex_omitted["promotion"], None)
        self.assertEqual(r931_complex_omitted["bundle"], bundle)
        r931_frozenset_none_stop = dict(stop)
        r931_frozenset_none_stop["effective_on_loading"] = frozenset()
        r931_frozenset_none = module.discovery_after_stop(r931_frozenset_none_stop, bundle=None)
        r931_frozenset_none_second = module.discovery_after_stop(r931_frozenset_none_stop, bundle=None)
        self.assertIsNot(r931_frozenset_none, r931_frozenset_none_second)
        self.assertEqual(r931_frozenset_none["promotion"], None)
        self.assertEqual(r931_frozenset_none["bundle"], bundle)
        r931_frozenset_omitted_stop = dict(stop)
        r931_frozenset_omitted_stop["effective_on_loading"] = frozenset()
        r931_frozenset_omitted = module.discovery_after_stop(r931_frozenset_omitted_stop)
        r931_frozenset_omitted_second = module.discovery_after_stop(r931_frozenset_omitted_stop)
        self.assertIsNot(r931_frozenset_omitted, r931_frozenset_omitted_second)
        self.assertEqual(r931_frozenset_omitted["promotion"], None)
        self.assertEqual(r931_frozenset_omitted["bundle"], bundle)
        r931_decimal_none_stop = dict(stop)
        r931_decimal_none_stop["effective_on_loading"] = Decimal(0)
        r931_decimal_none = module.discovery_after_stop(r931_decimal_none_stop, bundle=None)
        r931_decimal_none_second = module.discovery_after_stop(r931_decimal_none_stop, bundle=None)
        self.assertIsNot(r931_decimal_none, r931_decimal_none_second)
        self.assertEqual(r931_decimal_none["promotion"], None)
        self.assertEqual(r931_decimal_none["bundle"], bundle)
        r931_decimal_omitted_stop = dict(stop)
        r931_decimal_omitted_stop["effective_on_loading"] = Decimal(0)
        r931_decimal_omitted = module.discovery_after_stop(r931_decimal_omitted_stop)
        r931_decimal_omitted_second = module.discovery_after_stop(r931_decimal_omitted_stop)
        self.assertIsNot(r931_decimal_omitted, r931_decimal_omitted_second)
        self.assertEqual(r931_decimal_omitted["promotion"], None)
        self.assertEqual(r931_decimal_omitted["bundle"], bundle)
        r932_float_none = module.discovery_after_stop(1.5, bundle=None)
        r932_float_none_second = module.discovery_after_stop(1.5, bundle=None)
        self.assertIsNot(r932_float_none, r932_float_none_second)
        self.assertEqual(r932_float_none["promotion"], None)
        self.assertEqual(r932_float_none["bundle"], None)
        r932_float_omitted = module.discovery_after_stop(1.5)
        r932_float_omitted_second = module.discovery_after_stop(1.5)
        self.assertIsNot(r932_float_omitted, r932_float_omitted_second)
        self.assertEqual(r932_float_omitted["promotion"], None)
        self.assertEqual(r932_float_omitted["bundle"], None)
        r932_float_zero_none = module.discovery_after_stop(0.0, bundle=None)
        r932_float_zero_none_second = module.discovery_after_stop(0.0, bundle=None)
        self.assertIsNot(r932_float_zero_none, r932_float_zero_none_second)
        self.assertEqual(r932_float_zero_none["promotion"], None)
        self.assertEqual(r932_float_zero_none["bundle"], None)
        r932_float_zero_omitted = module.discovery_after_stop(0.0)
        r932_float_zero_omitted_second = module.discovery_after_stop(0.0)
        self.assertIsNot(r932_float_zero_omitted, r932_float_zero_omitted_second)
        self.assertEqual(r932_float_zero_omitted["promotion"], None)
        self.assertEqual(r932_float_zero_omitted["bundle"], None)
        r932_set_none = module.discovery_after_stop({"a stop standing as a set"}, bundle=None)
        r932_set_none_second = module.discovery_after_stop({"a stop standing as a set"}, bundle=None)
        self.assertIsNot(r932_set_none, r932_set_none_second)
        self.assertEqual(r932_set_none["promotion"], None)
        self.assertEqual(r932_set_none["bundle"], None)
        r932_set_omitted = module.discovery_after_stop({"a stop standing as a set"})
        r932_set_omitted_second = module.discovery_after_stop({"a stop standing as a set"})
        self.assertIsNot(r932_set_omitted, r932_set_omitted_second)
        self.assertEqual(r932_set_omitted["promotion"], None)
        self.assertEqual(r932_set_omitted["bundle"], None)
        r932_frozenset_none = module.discovery_after_stop(frozenset({"a stop standing as a frozenset"}), bundle=None)
        r932_frozenset_none_second = module.discovery_after_stop(frozenset({"a stop standing as a frozenset"}), bundle=None)
        self.assertIsNot(r932_frozenset_none, r932_frozenset_none_second)
        self.assertEqual(r932_frozenset_none["promotion"], None)
        self.assertEqual(r932_frozenset_none["bundle"], None)
        r932_frozenset_omitted = module.discovery_after_stop(frozenset({"a stop standing as a frozenset"}))
        r932_frozenset_omitted_second = module.discovery_after_stop(frozenset({"a stop standing as a frozenset"}))
        self.assertIsNot(r932_frozenset_omitted, r932_frozenset_omitted_second)
        self.assertEqual(r932_frozenset_omitted["promotion"], None)
        self.assertEqual(r932_frozenset_omitted["bundle"], None)
        r932_true_none = module.discovery_after_stop(True, bundle=None)
        r932_true_none_second = module.discovery_after_stop(True, bundle=None)
        self.assertIsNot(r932_true_none, r932_true_none_second)
        self.assertEqual(r932_true_none["promotion"], None)
        self.assertEqual(r932_true_none["bundle"], None)
        r932_true_omitted = module.discovery_after_stop(True)
        r932_true_omitted_second = module.discovery_after_stop(True)
        self.assertIsNot(r932_true_omitted, r932_true_omitted_second)
        self.assertEqual(r932_true_omitted["promotion"], None)
        self.assertEqual(r932_true_omitted["bundle"], None)
        r932_bytearray_none = module.discovery_after_stop(bytearray(b"a stop standing as a bytearray"), bundle=None)
        r932_bytearray_none_second = module.discovery_after_stop(bytearray(b"a stop standing as a bytearray"), bundle=None)
        self.assertIsNot(r932_bytearray_none, r932_bytearray_none_second)
        self.assertEqual(r932_bytearray_none["promotion"], None)
        self.assertEqual(r932_bytearray_none["bundle"], None)
        r932_bytearray_omitted = module.discovery_after_stop(bytearray(b"a stop standing as a bytearray"))
        r932_bytearray_omitted_second = module.discovery_after_stop(bytearray(b"a stop standing as a bytearray"))
        self.assertIsNot(r932_bytearray_omitted, r932_bytearray_omitted_second)
        self.assertEqual(r932_bytearray_omitted["promotion"], None)
        self.assertEqual(r932_bytearray_omitted["bundle"], None)
        r1051_proxy_stop = dict(stop)
        r1051_proxy_stop["effective_on_loading"] = MappingProxyType({})
        r1051_proxy = module.discovery_after_stop(r1051_proxy_stop, bundle=bundle)
        r1051_proxy_second = module.discovery_after_stop(r1051_proxy_stop, bundle=bundle)
        self.assertIsNot(r1051_proxy, r1051_proxy_second)
        self.assertEqual(r1051_proxy["promotion"], bundle)
        r1051_namedtuple_stop = dict(stop)
        r1051_namedtuple_stop["effective_on_loading"] = namedtuple("R1051Tuple", [])()
        r1051_namedtuple = module.discovery_after_stop(r1051_namedtuple_stop, bundle=bundle)
        r1051_namedtuple_second = module.discovery_after_stop(r1051_namedtuple_stop, bundle=bundle)
        self.assertIsNot(r1051_namedtuple, r1051_namedtuple_second)
        self.assertEqual(r1051_namedtuple["promotion"], bundle)
        r1051_keys_stop = dict(stop)
        r1051_keys_stop["effective_on_loading"] = {}.keys()
        r1051_keys = module.discovery_after_stop(r1051_keys_stop, bundle=bundle)
        r1051_keys_second = module.discovery_after_stop(r1051_keys_stop, bundle=bundle)
        self.assertIsNot(r1051_keys, r1051_keys_second)
        self.assertEqual(r1051_keys["promotion"], bundle)
        r1051_values_stop = dict(stop)
        r1051_values_stop["effective_on_loading"] = {}.values()
        r1051_values = module.discovery_after_stop(r1051_values_stop, bundle=bundle)
        r1051_values_second = module.discovery_after_stop(r1051_values_stop, bundle=bundle)
        self.assertIsNot(r1051_values, r1051_values_second)
        self.assertEqual(r1051_values["promotion"], bundle)
        r1051_intenum_stop = dict(stop)
        r1051_intenum_stop["effective_on_loading"] = IntEnum("R1051Enum", {"member": 0}).member
        r1051_intenum = module.discovery_after_stop(r1051_intenum_stop, bundle=bundle)
        r1051_intenum_second = module.discovery_after_stop(r1051_intenum_stop, bundle=bundle)
        self.assertIsNot(r1051_intenum, r1051_intenum_second)
        self.assertEqual(r1051_intenum["promotion"], bundle)
        r1052_proxy = module.discovery_after_stop(MappingProxyType({"k": "v"}), bundle=bundle)
        r1052_proxy_second = module.discovery_after_stop(MappingProxyType({"k": "v"}), bundle=bundle)
        self.assertIsNot(r1052_proxy, r1052_proxy_second)
        self.assertEqual(r1052_proxy["promotion"], bundle)
        self.assertEqual(r1052_proxy["bundle"], bundle)
        r1052_namedtuple = module.discovery_after_stop(namedtuple("R1052Tuple", ["field"])(1), bundle=bundle)
        r1052_namedtuple_second = module.discovery_after_stop(namedtuple("R1052Tuple", ["field"])(1), bundle=bundle)
        self.assertIsNot(r1052_namedtuple, r1052_namedtuple_second)
        self.assertEqual(r1052_namedtuple["promotion"], bundle)
        self.assertEqual(r1052_namedtuple["bundle"], bundle)
        r1052_keys = module.discovery_after_stop({"k": "v"}.keys(), bundle=bundle)
        r1052_keys_second = module.discovery_after_stop({"k": "v"}.keys(), bundle=bundle)
        self.assertIsNot(r1052_keys, r1052_keys_second)
        self.assertEqual(r1052_keys["promotion"], bundle)
        self.assertEqual(r1052_keys["bundle"], bundle)
        r1052_path = module.discovery_after_stop(Path("part"), bundle=bundle)
        r1052_path_second = module.discovery_after_stop(Path("part"), bundle=bundle)
        self.assertIsNot(r1052_path, r1052_path_second)
        self.assertEqual(r1052_path["promotion"], bundle)
        self.assertEqual(r1052_path["bundle"], bundle)
        r1052_date = module.discovery_after_stop(date(2026, 11, 17), bundle=bundle)
        r1052_date_second = module.discovery_after_stop(date(2026, 11, 17), bundle=bundle)
        self.assertIsNot(r1052_date, r1052_date_second)
        self.assertEqual(r1052_date["promotion"], bundle)
        self.assertEqual(r1052_date["bundle"], bundle)
        r1063_userlist_empty_stop = dict(stop)
        r1063_userlist_empty_stop["effective_on_loading"] = UserList([])
        r1063_userlist_empty = module.discovery_after_stop(r1063_userlist_empty_stop, bundle=bundle)
        r1063_userlist_empty_second = module.discovery_after_stop(r1063_userlist_empty_stop, bundle=bundle)
        self.assertIsNot(r1063_userlist_empty, r1063_userlist_empty_second)
        r1063_userlist_stop = dict(stop)
        r1063_userlist_stop["effective_on_loading"] = UserList([1])
        r1063_userlist = module.discovery_after_stop(r1063_userlist_stop, bundle=bundle)
        r1063_userlist_second = module.discovery_after_stop(r1063_userlist_stop, bundle=bundle)
        self.assertIsNot(r1063_userlist, r1063_userlist_second)
        r1063_userstring_empty_stop = dict(stop)
        r1063_userstring_empty_stop["effective_on_loading"] = UserString("")
        r1063_userstring_empty = module.discovery_after_stop(r1063_userstring_empty_stop, bundle=bundle)
        r1063_userstring_empty_second = module.discovery_after_stop(r1063_userstring_empty_stop, bundle=bundle)
        self.assertIsNot(r1063_userstring_empty, r1063_userstring_empty_second)
        r1063_userstring_stop = dict(stop)
        r1063_userstring_stop["effective_on_loading"] = UserString("x")
        r1063_userstring = module.discovery_after_stop(r1063_userstring_stop, bundle=bundle)
        r1063_userstring_second = module.discovery_after_stop(r1063_userstring_stop, bundle=bundle)
        self.assertIsNot(r1063_userstring, r1063_userstring_second)
        r1057_array_none_stop = dict(stop)
        r1057_array_none_stop["effective_on_loading"] = array("i", [])
        r1057_array_none = module.discovery_after_stop(r1057_array_none_stop, bundle=None)
        r1057_array_none_second = module.discovery_after_stop(r1057_array_none_stop, bundle=None)
        self.assertIsNot(r1057_array_none, r1057_array_none_second)
        r1057_array_omitted_stop = dict(stop)
        r1057_array_omitted_stop["effective_on_loading"] = array("i", [])
        r1057_array_omitted = module.discovery_after_stop(r1057_array_omitted_stop)
        r1057_array_omitted_second = module.discovery_after_stop(r1057_array_omitted_stop)
        self.assertIsNot(r1057_array_omitted, r1057_array_omitted_second)
        r1057_chainmap_none_stop = dict(stop)
        r1057_chainmap_none_stop["effective_on_loading"] = ChainMap()
        r1057_chainmap_none = module.discovery_after_stop(r1057_chainmap_none_stop, bundle=None)
        r1057_chainmap_none_second = module.discovery_after_stop(r1057_chainmap_none_stop, bundle=None)
        self.assertIsNot(r1057_chainmap_none, r1057_chainmap_none_second)
        r1057_chainmap_omitted_stop = dict(stop)
        r1057_chainmap_omitted_stop["effective_on_loading"] = ChainMap()
        r1057_chainmap_omitted = module.discovery_after_stop(r1057_chainmap_omitted_stop)
        r1057_chainmap_omitted_second = module.discovery_after_stop(r1057_chainmap_omitted_stop)
        self.assertIsNot(r1057_chainmap_omitted, r1057_chainmap_omitted_second)
        r1057_defaultdict_none_stop = dict(stop)
        r1057_defaultdict_none_stop["effective_on_loading"] = defaultdict(int)
        r1057_defaultdict_none = module.discovery_after_stop(r1057_defaultdict_none_stop, bundle=None)
        r1057_defaultdict_none_second = module.discovery_after_stop(r1057_defaultdict_none_stop, bundle=None)
        self.assertIsNot(r1057_defaultdict_none, r1057_defaultdict_none_second)
        r1057_defaultdict_omitted_stop = dict(stop)
        r1057_defaultdict_omitted_stop["effective_on_loading"] = defaultdict(int)
        r1057_defaultdict_omitted = module.discovery_after_stop(r1057_defaultdict_omitted_stop)
        r1057_defaultdict_omitted_second = module.discovery_after_stop(r1057_defaultdict_omitted_stop)
        self.assertIsNot(r1057_defaultdict_omitted, r1057_defaultdict_omitted_second)
        r1057_timedelta_none_stop = dict(stop)
        r1057_timedelta_none_stop["effective_on_loading"] = timedelta(0)
        r1057_timedelta_none = module.discovery_after_stop(r1057_timedelta_none_stop, bundle=None)
        r1057_timedelta_none_second = module.discovery_after_stop(r1057_timedelta_none_stop, bundle=None)
        self.assertIsNot(r1057_timedelta_none, r1057_timedelta_none_second)
        r1057_timedelta_omitted_stop = dict(stop)
        r1057_timedelta_omitted_stop["effective_on_loading"] = timedelta(0)
        r1057_timedelta_omitted = module.discovery_after_stop(r1057_timedelta_omitted_stop)
        r1057_timedelta_omitted_second = module.discovery_after_stop(r1057_timedelta_omitted_stop)
        self.assertIsNot(r1057_timedelta_omitted, r1057_timedelta_omitted_second)
        r1057_userdict_none_stop = dict(stop)
        r1057_userdict_none_stop["effective_on_loading"] = UserDict()
        r1057_userdict_none = module.discovery_after_stop(r1057_userdict_none_stop, bundle=None)
        r1057_userdict_none_second = module.discovery_after_stop(r1057_userdict_none_stop, bundle=None)
        self.assertIsNot(r1057_userdict_none, r1057_userdict_none_second)
        r1057_userdict_omitted_stop = dict(stop)
        r1057_userdict_omitted_stop["effective_on_loading"] = UserDict()
        r1057_userdict_omitted = module.discovery_after_stop(r1057_userdict_omitted_stop)
        r1057_userdict_omitted_second = module.discovery_after_stop(r1057_userdict_omitted_stop)
        self.assertIsNot(r1057_userdict_omitted, r1057_userdict_omitted_second)
        r1058_timedelta_none = module.discovery_after_stop(timedelta(days=1), bundle=None)
        r1058_timedelta_none_second = module.discovery_after_stop(timedelta(days=1), bundle=None)
        self.assertIsNot(r1058_timedelta_none, r1058_timedelta_none_second)
        r1058_timedelta_omitted = module.discovery_after_stop(timedelta(days=1))
        r1058_timedelta_omitted_second = module.discovery_after_stop(timedelta(days=1))
        self.assertIsNot(r1058_timedelta_omitted, r1058_timedelta_omitted_second)
        r1058_userlist_none = module.discovery_after_stop(UserList([1]), bundle=None)
        r1058_userlist_none_second = module.discovery_after_stop(UserList([1]), bundle=None)
        self.assertIsNot(r1058_userlist_none, r1058_userlist_none_second)
        r1058_userlist_omitted = module.discovery_after_stop(UserList([1]))
        r1058_userlist_omitted_second = module.discovery_after_stop(UserList([1]))
        self.assertIsNot(r1058_userlist_omitted, r1058_userlist_omitted_second)
        r1058_userstring_none = module.discovery_after_stop(UserString("x"), bundle=None)
        r1058_userstring_none_second = module.discovery_after_stop(UserString("x"), bundle=None)
        self.assertIsNot(r1058_userstring_none, r1058_userstring_none_second)
        r1058_userstring_omitted = module.discovery_after_stop(UserString("x"))
        r1058_userstring_omitted_second = module.discovery_after_stop(UserString("x"))
        self.assertIsNot(r1058_userstring_omitted, r1058_userstring_omitted_second)
        r1058_complex_none = module.discovery_after_stop(1j, bundle=None)
        r1058_complex_none_second = module.discovery_after_stop(1j, bundle=None)
        self.assertIsNot(r1058_complex_none, r1058_complex_none_second)
        r1058_complex_omitted = module.discovery_after_stop(1j)
        r1058_complex_omitted_second = module.discovery_after_stop(1j)
        self.assertIsNot(r1058_complex_omitted, r1058_complex_omitted_second)
        r1058_decimal_none = module.discovery_after_stop(Decimal(1), bundle=None)
        r1058_decimal_none_second = module.discovery_after_stop(Decimal(1), bundle=None)
        self.assertIsNot(r1058_decimal_none, r1058_decimal_none_second)
        r1058_decimal_omitted = module.discovery_after_stop(Decimal(1))
        r1058_decimal_omitted_second = module.discovery_after_stop(Decimal(1))
        self.assertIsNot(r1058_decimal_omitted, r1058_decimal_omitted_second)

        r1123_proxy_stop = dict(stop)
        r1123_proxy_stop["effective_on_loading"] = MappingProxyType({"k": "v"})
        r1123_proxy = module.discovery_after_stop(r1123_proxy_stop, bundle=bundle)
        r1123_proxy_second = module.discovery_after_stop(r1123_proxy_stop, bundle=bundle)
        self.assertIsNot(r1123_proxy, r1123_proxy_second)
        self.assertEqual(r1123_proxy["promotion"], bundle)
        r1123_namedtuple_stop = dict(stop)
        r1123_namedtuple_stop["effective_on_loading"] = namedtuple("R1123Tuple", ["field"])(1)
        r1123_namedtuple = module.discovery_after_stop(r1123_namedtuple_stop, bundle=bundle)
        r1123_namedtuple_second = module.discovery_after_stop(r1123_namedtuple_stop, bundle=bundle)
        self.assertIsNot(r1123_namedtuple, r1123_namedtuple_second)
        self.assertEqual(r1123_namedtuple["promotion"], bundle)
        r1123_keys_stop = dict(stop)
        r1123_keys_stop["effective_on_loading"] = {"k": "v"}.keys()
        r1123_keys = module.discovery_after_stop(r1123_keys_stop, bundle=bundle)
        r1123_keys_second = module.discovery_after_stop(r1123_keys_stop, bundle=bundle)
        self.assertIsNot(r1123_keys, r1123_keys_second)
        self.assertEqual(r1123_keys["promotion"], bundle)
        r1123_values_stop = dict(stop)
        r1123_values_stop["effective_on_loading"] = {"k": "v"}.values()
        r1123_values = module.discovery_after_stop(r1123_values_stop, bundle=bundle)
        r1123_values_second = module.discovery_after_stop(r1123_values_stop, bundle=bundle)
        self.assertIsNot(r1123_values, r1123_values_second)
        self.assertEqual(r1123_values["promotion"], bundle)
        r1123_intenum_stop = dict(stop)
        r1123_intenum_stop["effective_on_loading"] = IntEnum("R1123Enum", {"member": 1}).member
        r1123_intenum = module.discovery_after_stop(r1123_intenum_stop, bundle=bundle)
        r1123_intenum_second = module.discovery_after_stop(r1123_intenum_stop, bundle=bundle)
        self.assertIsNot(r1123_intenum, r1123_intenum_second)
        self.assertEqual(r1123_intenum["promotion"], bundle)
        r1124_values = module.discovery_after_stop({"k": "v"}.values(), bundle=bundle)
        r1124_values_second = module.discovery_after_stop({"k": "v"}.values(), bundle=bundle)
        self.assertIsNot(r1124_values, r1124_values_second)
        self.assertEqual(r1124_values["promotion"], bundle)
        self.assertEqual(r1124_values["bundle"], bundle)
        r1124_intenum = module.discovery_after_stop(IntEnum("R1124Enum", {"member": 1}).member, bundle=bundle)
        r1124_intenum_second = module.discovery_after_stop(IntEnum("R1124Enum", {"member": 1}).member, bundle=bundle)
        self.assertIsNot(r1124_intenum, r1124_intenum_second)
        self.assertEqual(r1124_intenum["promotion"], bundle)
        self.assertEqual(r1124_intenum["bundle"], bundle)
        r1124_range = module.discovery_after_stop(range(1), bundle=bundle)
        r1124_range_second = module.discovery_after_stop(range(1), bundle=bundle)
        self.assertIsNot(r1124_range, r1124_range_second)
        self.assertEqual(r1124_range["promotion"], bundle)
        self.assertEqual(r1124_range["bundle"], bundle)
        r1124_datetime = module.discovery_after_stop(datetime(2026, 11, 17, 12, 0), bundle=bundle)
        r1124_datetime_second = module.discovery_after_stop(datetime(2026, 11, 17, 12, 0), bundle=bundle)
        self.assertIsNot(r1124_datetime, r1124_datetime_second)
        self.assertEqual(r1124_datetime["promotion"], bundle)
        self.assertEqual(r1124_datetime["bundle"], bundle)
        r1124_uuid = module.discovery_after_stop(UUID(int=1), bundle=bundle)
        r1124_uuid_second = module.discovery_after_stop(UUID(int=1), bundle=bundle)
        self.assertIsNot(r1124_uuid, r1124_uuid_second)
        self.assertEqual(r1124_uuid["promotion"], bundle)
        self.assertEqual(r1124_uuid["bundle"], bundle)
        r1127_items_stop = dict(stop)
        r1127_items_stop["effective_on_loading"] = {"k": "v"}.items()
        r1127_items = module.discovery_after_stop(r1127_items_stop, bundle=bundle)
        r1127_items_second = module.discovery_after_stop(r1127_items_stop, bundle=bundle)
        self.assertIsNot(r1127_items, r1127_items_second)
        r1127_items_empty_stop = dict(stop)
        r1127_items_empty_stop["effective_on_loading"] = {}.items()
        r1127_items_empty = module.discovery_after_stop(r1127_items_empty_stop, bundle=bundle)
        r1127_items_empty_second = module.discovery_after_stop(r1127_items_empty_stop, bundle=bundle)
        self.assertIsNot(r1127_items_empty, r1127_items_empty_second)
        r1127_intflag_stop = dict(stop)
        r1127_intflag_stop["effective_on_loading"] = IntFlag("R1127Flag", {"member": 1}).member
        r1127_intflag = module.discovery_after_stop(r1127_intflag_stop, bundle=bundle)
        r1127_intflag_second = module.discovery_after_stop(r1127_intflag_stop, bundle=bundle)
        self.assertIsNot(r1127_intflag, r1127_intflag_second)
        r1127_intflag_zero_stop = dict(stop)
        r1127_intflag_zero_stop["effective_on_loading"] = IntFlag("R1127Flag", {"member": 0}).member
        r1127_intflag_zero = module.discovery_after_stop(r1127_intflag_zero_stop, bundle=bundle)
        r1127_intflag_zero_second = module.discovery_after_stop(r1127_intflag_zero_stop, bundle=bundle)
        self.assertIsNot(r1127_intflag_zero, r1127_intflag_zero_second)
        r1127_strenum_stop = dict(stop)
        r1127_strenum_stop["effective_on_loading"] = StrEnum("R1127StrEnum", {"member": "x"}).member
        r1127_strenum = module.discovery_after_stop(r1127_strenum_stop, bundle=bundle)
        r1127_strenum_second = module.discovery_after_stop(r1127_strenum_stop, bundle=bundle)
        self.assertIsNot(r1127_strenum, r1127_strenum_second)
        r1127_strenum_empty_stop = dict(stop)
        r1127_strenum_empty_stop["effective_on_loading"] = StrEnum("R1127StrEnum", {"member": ""}).member
        r1127_strenum_empty = module.discovery_after_stop(r1127_strenum_empty_stop, bundle=bundle)
        r1127_strenum_empty_second = module.discovery_after_stop(r1127_strenum_empty_stop, bundle=bundle)
        self.assertIsNot(r1127_strenum_empty, r1127_strenum_empty_second)
        r1127_flag_stop = dict(stop)
        r1127_flag_stop["effective_on_loading"] = Flag("R1127PlainFlag", {"member": 1}).member
        r1127_flag = module.discovery_after_stop(r1127_flag_stop, bundle=bundle)
        r1127_flag_second = module.discovery_after_stop(r1127_flag_stop, bundle=bundle)
        self.assertIsNot(r1127_flag, r1127_flag_second)
        r1127_flag_zero_stop = dict(stop)
        r1127_flag_zero_stop["effective_on_loading"] = Flag("R1127PlainFlag", {"member": 0}).member
        r1127_flag_zero = module.discovery_after_stop(r1127_flag_zero_stop, bundle=bundle)
        r1127_flag_zero_second = module.discovery_after_stop(r1127_flag_zero_stop, bundle=bundle)
        self.assertIsNot(r1127_flag_zero, r1127_flag_zero_second)
        r1131_proxy_none_stop = dict(stop)
        r1131_proxy_none_stop["effective_on_loading"] = MappingProxyType({})
        r1131_proxy_none = module.discovery_after_stop(r1131_proxy_none_stop, bundle=None)
        r1131_proxy_none_second = module.discovery_after_stop(r1131_proxy_none_stop, bundle=None)
        self.assertIsNot(r1131_proxy_none, r1131_proxy_none_second)
        r1131_proxy_omitted_stop = dict(stop)
        r1131_proxy_omitted_stop["effective_on_loading"] = MappingProxyType({})
        r1131_proxy_omitted = module.discovery_after_stop(r1131_proxy_omitted_stop)
        r1131_proxy_omitted_second = module.discovery_after_stop(r1131_proxy_omitted_stop)
        self.assertIsNot(r1131_proxy_omitted, r1131_proxy_omitted_second)
        r1131_namedtuple_none_stop = dict(stop)
        r1131_namedtuple_none_stop["effective_on_loading"] = namedtuple("R1131Tuple", [])()
        r1131_namedtuple_none = module.discovery_after_stop(r1131_namedtuple_none_stop, bundle=None)
        r1131_namedtuple_none_second = module.discovery_after_stop(r1131_namedtuple_none_stop, bundle=None)
        self.assertIsNot(r1131_namedtuple_none, r1131_namedtuple_none_second)
        r1131_namedtuple_omitted_stop = dict(stop)
        r1131_namedtuple_omitted_stop["effective_on_loading"] = namedtuple("R1131Tuple", [])()
        r1131_namedtuple_omitted = module.discovery_after_stop(r1131_namedtuple_omitted_stop)
        r1131_namedtuple_omitted_second = module.discovery_after_stop(r1131_namedtuple_omitted_stop)
        self.assertIsNot(r1131_namedtuple_omitted, r1131_namedtuple_omitted_second)
        r1131_keys_none_stop = dict(stop)
        r1131_keys_none_stop["effective_on_loading"] = {}.keys()
        r1131_keys_none = module.discovery_after_stop(r1131_keys_none_stop, bundle=None)
        r1131_keys_none_second = module.discovery_after_stop(r1131_keys_none_stop, bundle=None)
        self.assertIsNot(r1131_keys_none, r1131_keys_none_second)
        r1131_keys_omitted_stop = dict(stop)
        r1131_keys_omitted_stop["effective_on_loading"] = {}.keys()
        r1131_keys_omitted = module.discovery_after_stop(r1131_keys_omitted_stop)
        r1131_keys_omitted_second = module.discovery_after_stop(r1131_keys_omitted_stop)
        self.assertIsNot(r1131_keys_omitted, r1131_keys_omitted_second)
        r1131_values_none_stop = dict(stop)
        r1131_values_none_stop["effective_on_loading"] = {}.values()
        r1131_values_none = module.discovery_after_stop(r1131_values_none_stop, bundle=None)
        r1131_values_none_second = module.discovery_after_stop(r1131_values_none_stop, bundle=None)
        self.assertIsNot(r1131_values_none, r1131_values_none_second)
        r1131_values_omitted_stop = dict(stop)
        r1131_values_omitted_stop["effective_on_loading"] = {}.values()
        r1131_values_omitted = module.discovery_after_stop(r1131_values_omitted_stop)
        r1131_values_omitted_second = module.discovery_after_stop(r1131_values_omitted_stop)
        self.assertIsNot(r1131_values_omitted, r1131_values_omitted_second)
        r1131_intenum_none_stop = dict(stop)
        r1131_intenum_none_stop["effective_on_loading"] = IntEnum("R1131Enum", {"member": 0}).member
        r1131_intenum_none = module.discovery_after_stop(r1131_intenum_none_stop, bundle=None)
        r1131_intenum_none_second = module.discovery_after_stop(r1131_intenum_none_stop, bundle=None)
        self.assertIsNot(r1131_intenum_none, r1131_intenum_none_second)
        r1131_intenum_omitted_stop = dict(stop)
        r1131_intenum_omitted_stop["effective_on_loading"] = IntEnum("R1131Enum", {"member": 0}).member
        r1131_intenum_omitted = module.discovery_after_stop(r1131_intenum_omitted_stop)
        r1131_intenum_omitted_second = module.discovery_after_stop(r1131_intenum_omitted_stop)
        self.assertIsNot(r1131_intenum_omitted, r1131_intenum_omitted_second)
        r1132_proxy_none = module.discovery_after_stop(MappingProxyType({"k": "v"}), bundle=None)
        r1132_proxy_none_second = module.discovery_after_stop(MappingProxyType({"k": "v"}), bundle=None)
        self.assertIsNot(r1132_proxy_none, r1132_proxy_none_second)
        r1132_proxy_omitted = module.discovery_after_stop(MappingProxyType({"k": "v"}))
        r1132_proxy_omitted_second = module.discovery_after_stop(MappingProxyType({"k": "v"}))
        self.assertIsNot(r1132_proxy_omitted, r1132_proxy_omitted_second)
        r1132_namedtuple_none = module.discovery_after_stop(namedtuple("R1132Tuple", ["field"])(1), bundle=None)
        r1132_namedtuple_none_second = module.discovery_after_stop(namedtuple("R1132Tuple", ["field"])(1), bundle=None)
        self.assertIsNot(r1132_namedtuple_none, r1132_namedtuple_none_second)
        r1132_namedtuple_omitted = module.discovery_after_stop(namedtuple("R1132Tuple", ["field"])(1))
        r1132_namedtuple_omitted_second = module.discovery_after_stop(namedtuple("R1132Tuple", ["field"])(1))
        self.assertIsNot(r1132_namedtuple_omitted, r1132_namedtuple_omitted_second)
        r1132_keys_none = module.discovery_after_stop({"k": "v"}.keys(), bundle=None)
        r1132_keys_none_second = module.discovery_after_stop({"k": "v"}.keys(), bundle=None)
        self.assertIsNot(r1132_keys_none, r1132_keys_none_second)
        r1132_keys_omitted = module.discovery_after_stop({"k": "v"}.keys())
        r1132_keys_omitted_second = module.discovery_after_stop({"k": "v"}.keys())
        self.assertIsNot(r1132_keys_omitted, r1132_keys_omitted_second)
        r1132_path_none = module.discovery_after_stop(Path("part"), bundle=None)
        r1132_path_none_second = module.discovery_after_stop(Path("part"), bundle=None)
        self.assertIsNot(r1132_path_none, r1132_path_none_second)
        r1132_path_omitted = module.discovery_after_stop(Path("part"))
        r1132_path_omitted_second = module.discovery_after_stop(Path("part"))
        self.assertIsNot(r1132_path_omitted, r1132_path_omitted_second)
        r1132_date_none = module.discovery_after_stop(date(2026, 11, 17), bundle=None)
        r1132_date_none_second = module.discovery_after_stop(date(2026, 11, 17), bundle=None)
        self.assertIsNot(r1132_date_none, r1132_date_none_second)
        r1132_date_omitted = module.discovery_after_stop(date(2026, 11, 17))
        r1132_date_omitted_second = module.discovery_after_stop(date(2026, 11, 17))
        self.assertIsNot(r1132_date_omitted, r1132_date_omitted_second)
        r1137_userlist_empty_none_stop = dict(stop)
        r1137_userlist_empty_none_stop["effective_on_loading"] = UserList([])
        r1137_userlist_empty_none = module.discovery_after_stop(r1137_userlist_empty_none_stop, bundle=None)
        r1137_userlist_empty_none_second = module.discovery_after_stop(r1137_userlist_empty_none_stop, bundle=None)
        self.assertIsNot(r1137_userlist_empty_none, r1137_userlist_empty_none_second)
        r1137_userlist_empty_omitted_stop = dict(stop)
        r1137_userlist_empty_omitted_stop["effective_on_loading"] = UserList([])
        r1137_userlist_empty_omitted = module.discovery_after_stop(r1137_userlist_empty_omitted_stop)
        r1137_userlist_empty_omitted_second = module.discovery_after_stop(r1137_userlist_empty_omitted_stop)
        self.assertIsNot(r1137_userlist_empty_omitted, r1137_userlist_empty_omitted_second)
        r1137_userlist_none_stop = dict(stop)
        r1137_userlist_none_stop["effective_on_loading"] = UserList([1])
        r1137_userlist_none = module.discovery_after_stop(r1137_userlist_none_stop, bundle=None)
        r1137_userlist_none_second = module.discovery_after_stop(r1137_userlist_none_stop, bundle=None)
        self.assertIsNot(r1137_userlist_none, r1137_userlist_none_second)
        r1137_userlist_omitted_stop = dict(stop)
        r1137_userlist_omitted_stop["effective_on_loading"] = UserList([1])
        r1137_userlist_omitted = module.discovery_after_stop(r1137_userlist_omitted_stop)
        r1137_userlist_omitted_second = module.discovery_after_stop(r1137_userlist_omitted_stop)
        self.assertIsNot(r1137_userlist_omitted, r1137_userlist_omitted_second)
        r1137_userstring_empty_none_stop = dict(stop)
        r1137_userstring_empty_none_stop["effective_on_loading"] = UserString("")
        r1137_userstring_empty_none = module.discovery_after_stop(r1137_userstring_empty_none_stop, bundle=None)
        r1137_userstring_empty_none_second = module.discovery_after_stop(r1137_userstring_empty_none_stop, bundle=None)
        self.assertIsNot(r1137_userstring_empty_none, r1137_userstring_empty_none_second)
        r1137_userstring_empty_omitted_stop = dict(stop)
        r1137_userstring_empty_omitted_stop["effective_on_loading"] = UserString("")
        r1137_userstring_empty_omitted = module.discovery_after_stop(r1137_userstring_empty_omitted_stop)
        r1137_userstring_empty_omitted_second = module.discovery_after_stop(r1137_userstring_empty_omitted_stop)
        self.assertIsNot(r1137_userstring_empty_omitted, r1137_userstring_empty_omitted_second)
        r1137_userstring_none_stop = dict(stop)
        r1137_userstring_none_stop["effective_on_loading"] = UserString("x")
        r1137_userstring_none = module.discovery_after_stop(r1137_userstring_none_stop, bundle=None)
        r1137_userstring_none_second = module.discovery_after_stop(r1137_userstring_none_stop, bundle=None)
        self.assertIsNot(r1137_userstring_none, r1137_userstring_none_second)
        r1137_userstring_omitted_stop = dict(stop)
        r1137_userstring_omitted_stop["effective_on_loading"] = UserString("x")
        r1137_userstring_omitted = module.discovery_after_stop(r1137_userstring_omitted_stop)
        r1137_userstring_omitted_second = module.discovery_after_stop(r1137_userstring_omitted_stop)
        self.assertIsNot(r1137_userstring_omitted, r1137_userstring_omitted_second)

        r1216_slice_stop = dict(stop)
        r1216_slice_stop["effective_on_loading"] = slice(1)
        r1216_slice = module.discovery_after_stop(r1216_slice_stop, bundle=bundle)
        r1216_slice_second = module.discovery_after_stop(r1216_slice_stop, bundle=bundle)
        self.assertIsNot(r1216_slice, r1216_slice_second)
        self.assertEqual(r1216_slice["promotion"], bundle)
        r1216_pattern_stop = dict(stop)
        r1216_pattern_stop["effective_on_loading"] = re.compile("a pattern")
        r1216_pattern = module.discovery_after_stop(r1216_pattern_stop, bundle=bundle)
        r1216_pattern_second = module.discovery_after_stop(r1216_pattern_stop, bundle=bundle)
        self.assertIsNot(r1216_pattern, r1216_pattern_second)
        self.assertEqual(r1216_pattern["promotion"], bundle)
        r1216_enum_stop = dict(stop)
        r1216_enum_stop["effective_on_loading"] = Enum("R1216Enum", {"member": 1}).member
        r1216_enum = module.discovery_after_stop(r1216_enum_stop, bundle=bundle)
        r1216_enum_second = module.discovery_after_stop(r1216_enum_stop, bundle=bundle)
        self.assertIsNot(r1216_enum, r1216_enum_second)
        self.assertEqual(r1216_enum["promotion"], bundle)
        r1216_ipv4_stop = dict(stop)
        r1216_ipv4_stop["effective_on_loading"] = IPv4Address("1.2.3.4")
        r1216_ipv4 = module.discovery_after_stop(r1216_ipv4_stop, bundle=bundle)
        r1216_ipv4_second = module.discovery_after_stop(r1216_ipv4_stop, bundle=bundle)
        self.assertIsNot(r1216_ipv4, r1216_ipv4_second)
        self.assertEqual(r1216_ipv4["promotion"], bundle)
        r1216_timezone_stop = dict(stop)
        r1216_timezone_stop["effective_on_loading"] = timezone.utc
        r1216_timezone = module.discovery_after_stop(r1216_timezone_stop, bundle=bundle)
        r1216_timezone_second = module.discovery_after_stop(r1216_timezone_stop, bundle=bundle)
        self.assertIsNot(r1216_timezone, r1216_timezone_second)
        self.assertEqual(r1216_timezone["promotion"], bundle)

        r1217_slice = module.discovery_after_stop(slice(1), bundle=bundle)
        r1217_slice_second = module.discovery_after_stop(slice(1), bundle=bundle)
        self.assertIsNot(r1217_slice, r1217_slice_second)
        self.assertEqual(r1217_slice["promotion"], bundle)
        self.assertEqual(r1217_slice["bundle"], bundle)
        r1217_pattern = module.discovery_after_stop(re.compile("a pattern"), bundle=bundle)
        r1217_pattern_second = module.discovery_after_stop(re.compile("a pattern"), bundle=bundle)
        self.assertIsNot(r1217_pattern, r1217_pattern_second)
        self.assertEqual(r1217_pattern["promotion"], bundle)
        self.assertEqual(r1217_pattern["bundle"], bundle)
        r1217_enum = module.discovery_after_stop(Enum("R1217Enum", {"member": 1}).member, bundle=bundle)
        r1217_enum_second = module.discovery_after_stop(Enum("R1217Enum", {"member": 1}).member, bundle=bundle)
        self.assertIsNot(r1217_enum, r1217_enum_second)
        self.assertEqual(r1217_enum["promotion"], bundle)
        self.assertEqual(r1217_enum["bundle"], bundle)
        r1217_ipv4 = module.discovery_after_stop(IPv4Address("1.2.3.4"), bundle=bundle)
        r1217_ipv4_second = module.discovery_after_stop(IPv4Address("1.2.3.4"), bundle=bundle)
        self.assertIsNot(r1217_ipv4, r1217_ipv4_second)
        self.assertEqual(r1217_ipv4["promotion"], bundle)
        self.assertEqual(r1217_ipv4["bundle"], bundle)
        r1217_timezone = module.discovery_after_stop(timezone.utc, bundle=bundle)
        r1217_timezone_second = module.discovery_after_stop(timezone.utc, bundle=bundle)
        self.assertIsNot(r1217_timezone, r1217_timezone_second)
        self.assertEqual(r1217_timezone["promotion"], bundle)
        self.assertEqual(r1217_timezone["bundle"], bundle)

        r1220_member = lambda: None
        r1220_element = Element("tag")
        r1220_element.append(Element("child"))
        r1220_element_empty = Element("tag")
        r1220_weakset = WeakSet([r1220_member])
        r1220_weakset_empty = WeakSet()
        r1220_weakkey = WeakKeyDictionary({r1220_member: "v"})
        r1220_weakkey_empty = WeakKeyDictionary()
        r1220_weakvalue = WeakValueDictionary({"k": r1220_member})
        r1220_weakvalue_empty = WeakValueDictionary()
        r1220_element_empty_stop = dict(stop)
        r1220_element_empty_stop["effective_on_loading"] = r1220_element_empty
        r1220_element_empty = module.discovery_after_stop(r1220_element_empty_stop, bundle=bundle)
        r1220_element_empty_second = module.discovery_after_stop(r1220_element_empty_stop, bundle=bundle)
        self.assertIsNot(r1220_element_empty, r1220_element_empty_second)
        r1220_element_stop = dict(stop)
        r1220_element_stop["effective_on_loading"] = r1220_element
        r1220_element = module.discovery_after_stop(r1220_element_stop, bundle=bundle)
        r1220_element_second = module.discovery_after_stop(r1220_element_stop, bundle=bundle)
        self.assertIsNot(r1220_element, r1220_element_second)
        r1220_weakset_empty_stop = dict(stop)
        r1220_weakset_empty_stop["effective_on_loading"] = r1220_weakset_empty
        r1220_weakset_empty = module.discovery_after_stop(r1220_weakset_empty_stop, bundle=bundle)
        r1220_weakset_empty_second = module.discovery_after_stop(r1220_weakset_empty_stop, bundle=bundle)
        self.assertIsNot(r1220_weakset_empty, r1220_weakset_empty_second)
        r1220_weakset_stop = dict(stop)
        r1220_weakset_stop["effective_on_loading"] = r1220_weakset
        r1220_weakset = module.discovery_after_stop(r1220_weakset_stop, bundle=bundle)
        r1220_weakset_second = module.discovery_after_stop(r1220_weakset_stop, bundle=bundle)
        self.assertIsNot(r1220_weakset, r1220_weakset_second)
        r1220_weakkey_empty_stop = dict(stop)
        r1220_weakkey_empty_stop["effective_on_loading"] = r1220_weakkey_empty
        r1220_weakkey_empty = module.discovery_after_stop(r1220_weakkey_empty_stop, bundle=bundle)
        r1220_weakkey_empty_second = module.discovery_after_stop(r1220_weakkey_empty_stop, bundle=bundle)
        self.assertIsNot(r1220_weakkey_empty, r1220_weakkey_empty_second)
        r1220_weakkey_stop = dict(stop)
        r1220_weakkey_stop["effective_on_loading"] = r1220_weakkey
        r1220_weakkey = module.discovery_after_stop(r1220_weakkey_stop, bundle=bundle)
        r1220_weakkey_second = module.discovery_after_stop(r1220_weakkey_stop, bundle=bundle)
        self.assertIsNot(r1220_weakkey, r1220_weakkey_second)
        r1220_weakvalue_empty_stop = dict(stop)
        r1220_weakvalue_empty_stop["effective_on_loading"] = r1220_weakvalue_empty
        r1220_weakvalue_empty = module.discovery_after_stop(r1220_weakvalue_empty_stop, bundle=bundle)
        r1220_weakvalue_empty_second = module.discovery_after_stop(r1220_weakvalue_empty_stop, bundle=bundle)
        self.assertIsNot(r1220_weakvalue_empty, r1220_weakvalue_empty_second)
        r1220_weakvalue_stop = dict(stop)
        r1220_weakvalue_stop["effective_on_loading"] = r1220_weakvalue
        r1220_weakvalue = module.discovery_after_stop(r1220_weakvalue_stop, bundle=bundle)
        r1220_weakvalue_second = module.discovery_after_stop(r1220_weakvalue_stop, bundle=bundle)
        self.assertIsNot(r1220_weakvalue, r1220_weakvalue_second)

        r1225_proxy_none_stop = dict(stop)
        r1225_proxy_none_stop["effective_on_loading"] = MappingProxyType({"k": "v"})
        r1225_proxy_none = module.discovery_after_stop(r1225_proxy_none_stop, bundle=None)
        r1225_proxy_none_second = module.discovery_after_stop(r1225_proxy_none_stop, bundle=None)
        self.assertIsNot(r1225_proxy_none, r1225_proxy_none_second)
        r1225_proxy_omitted_stop = dict(stop)
        r1225_proxy_omitted_stop["effective_on_loading"] = MappingProxyType({"k": "v"})
        r1225_proxy_omitted = module.discovery_after_stop(r1225_proxy_omitted_stop)
        r1225_proxy_omitted_second = module.discovery_after_stop(r1225_proxy_omitted_stop)
        self.assertIsNot(r1225_proxy_omitted, r1225_proxy_omitted_second)
        r1225_namedtuple_none_stop = dict(stop)
        r1225_namedtuple_none_stop["effective_on_loading"] = namedtuple("R1225Tuple", ["field"])(1)
        r1225_namedtuple_none = module.discovery_after_stop(r1225_namedtuple_none_stop, bundle=None)
        r1225_namedtuple_none_second = module.discovery_after_stop(r1225_namedtuple_none_stop, bundle=None)
        self.assertIsNot(r1225_namedtuple_none, r1225_namedtuple_none_second)
        r1225_namedtuple_omitted_stop = dict(stop)
        r1225_namedtuple_omitted_stop["effective_on_loading"] = namedtuple("R1225Tuple", ["field"])(1)
        r1225_namedtuple_omitted = module.discovery_after_stop(r1225_namedtuple_omitted_stop)
        r1225_namedtuple_omitted_second = module.discovery_after_stop(r1225_namedtuple_omitted_stop)
        self.assertIsNot(r1225_namedtuple_omitted, r1225_namedtuple_omitted_second)
        r1225_keys_none_stop = dict(stop)
        r1225_keys_none_stop["effective_on_loading"] = {"k": "v"}.keys()
        r1225_keys_none = module.discovery_after_stop(r1225_keys_none_stop, bundle=None)
        r1225_keys_none_second = module.discovery_after_stop(r1225_keys_none_stop, bundle=None)
        self.assertIsNot(r1225_keys_none, r1225_keys_none_second)
        r1225_keys_omitted_stop = dict(stop)
        r1225_keys_omitted_stop["effective_on_loading"] = {"k": "v"}.keys()
        r1225_keys_omitted = module.discovery_after_stop(r1225_keys_omitted_stop)
        r1225_keys_omitted_second = module.discovery_after_stop(r1225_keys_omitted_stop)
        self.assertIsNot(r1225_keys_omitted, r1225_keys_omitted_second)
        r1225_values_none_stop = dict(stop)
        r1225_values_none_stop["effective_on_loading"] = {"k": "v"}.values()
        r1225_values_none = module.discovery_after_stop(r1225_values_none_stop, bundle=None)
        r1225_values_none_second = module.discovery_after_stop(r1225_values_none_stop, bundle=None)
        self.assertIsNot(r1225_values_none, r1225_values_none_second)
        r1225_values_omitted_stop = dict(stop)
        r1225_values_omitted_stop["effective_on_loading"] = {"k": "v"}.values()
        r1225_values_omitted = module.discovery_after_stop(r1225_values_omitted_stop)
        r1225_values_omitted_second = module.discovery_after_stop(r1225_values_omitted_stop)
        self.assertIsNot(r1225_values_omitted, r1225_values_omitted_second)
        r1225_intenum_none_stop = dict(stop)
        r1225_intenum_none_stop["effective_on_loading"] = IntEnum("R1225Enum", {"member": 1}).member
        r1225_intenum_none = module.discovery_after_stop(r1225_intenum_none_stop, bundle=None)
        r1225_intenum_none_second = module.discovery_after_stop(r1225_intenum_none_stop, bundle=None)
        self.assertIsNot(r1225_intenum_none, r1225_intenum_none_second)
        r1225_intenum_omitted_stop = dict(stop)
        r1225_intenum_omitted_stop["effective_on_loading"] = IntEnum("R1225Enum", {"member": 1}).member
        r1225_intenum_omitted = module.discovery_after_stop(r1225_intenum_omitted_stop)
        r1225_intenum_omitted_second = module.discovery_after_stop(r1225_intenum_omitted_stop)
        self.assertIsNot(r1225_intenum_omitted, r1225_intenum_omitted_second)

        r1226_items_none_stop = dict(stop)
        r1226_items_none_stop["effective_on_loading"] = {"k": "v"}.items()
        r1226_items_none = module.discovery_after_stop(r1226_items_none_stop, bundle=None)
        r1226_items_none_second = module.discovery_after_stop(r1226_items_none_stop, bundle=None)
        self.assertIsNot(r1226_items_none, r1226_items_none_second)
        r1226_items_omitted_stop = dict(stop)
        r1226_items_omitted_stop["effective_on_loading"] = {"k": "v"}.items()
        r1226_items_omitted = module.discovery_after_stop(r1226_items_omitted_stop)
        r1226_items_omitted_second = module.discovery_after_stop(r1226_items_omitted_stop)
        self.assertIsNot(r1226_items_omitted, r1226_items_omitted_second)
        r1226_items_empty_none_stop = dict(stop)
        r1226_items_empty_none_stop["effective_on_loading"] = {}.items()
        r1226_items_empty_none = module.discovery_after_stop(r1226_items_empty_none_stop, bundle=None)
        r1226_items_empty_none_second = module.discovery_after_stop(r1226_items_empty_none_stop, bundle=None)
        self.assertIsNot(r1226_items_empty_none, r1226_items_empty_none_second)
        r1226_items_empty_omitted_stop = dict(stop)
        r1226_items_empty_omitted_stop["effective_on_loading"] = {}.items()
        r1226_items_empty_omitted = module.discovery_after_stop(r1226_items_empty_omitted_stop)
        r1226_items_empty_omitted_second = module.discovery_after_stop(r1226_items_empty_omitted_stop)
        self.assertIsNot(r1226_items_empty_omitted, r1226_items_empty_omitted_second)
        r1226_intflag_none_stop = dict(stop)
        r1226_intflag_none_stop["effective_on_loading"] = IntFlag("R1226Flag", {"member": 1}).member
        r1226_intflag_none = module.discovery_after_stop(r1226_intflag_none_stop, bundle=None)
        r1226_intflag_none_second = module.discovery_after_stop(r1226_intflag_none_stop, bundle=None)
        self.assertIsNot(r1226_intflag_none, r1226_intflag_none_second)
        r1226_intflag_omitted_stop = dict(stop)
        r1226_intflag_omitted_stop["effective_on_loading"] = IntFlag("R1226Flag", {"member": 1}).member
        r1226_intflag_omitted = module.discovery_after_stop(r1226_intflag_omitted_stop)
        r1226_intflag_omitted_second = module.discovery_after_stop(r1226_intflag_omitted_stop)
        self.assertIsNot(r1226_intflag_omitted, r1226_intflag_omitted_second)
        r1226_intflag_zero_none_stop = dict(stop)
        r1226_intflag_zero_none_stop["effective_on_loading"] = IntFlag("R1226Flag", {"member": 0}).member
        r1226_intflag_zero_none = module.discovery_after_stop(r1226_intflag_zero_none_stop, bundle=None)
        r1226_intflag_zero_none_second = module.discovery_after_stop(r1226_intflag_zero_none_stop, bundle=None)
        self.assertIsNot(r1226_intflag_zero_none, r1226_intflag_zero_none_second)
        r1226_intflag_zero_omitted_stop = dict(stop)
        r1226_intflag_zero_omitted_stop["effective_on_loading"] = IntFlag("R1226Flag", {"member": 0}).member
        r1226_intflag_zero_omitted = module.discovery_after_stop(r1226_intflag_zero_omitted_stop)
        r1226_intflag_zero_omitted_second = module.discovery_after_stop(r1226_intflag_zero_omitted_stop)
        self.assertIsNot(r1226_intflag_zero_omitted, r1226_intflag_zero_omitted_second)
        r1226_strenum_none_stop = dict(stop)
        r1226_strenum_none_stop["effective_on_loading"] = StrEnum("R1226StrEnum", {"member": "x"}).member
        r1226_strenum_none = module.discovery_after_stop(r1226_strenum_none_stop, bundle=None)
        r1226_strenum_none_second = module.discovery_after_stop(r1226_strenum_none_stop, bundle=None)
        self.assertIsNot(r1226_strenum_none, r1226_strenum_none_second)
        r1226_strenum_omitted_stop = dict(stop)
        r1226_strenum_omitted_stop["effective_on_loading"] = StrEnum("R1226StrEnum", {"member": "x"}).member
        r1226_strenum_omitted = module.discovery_after_stop(r1226_strenum_omitted_stop)
        r1226_strenum_omitted_second = module.discovery_after_stop(r1226_strenum_omitted_stop)
        self.assertIsNot(r1226_strenum_omitted, r1226_strenum_omitted_second)
        r1226_strenum_empty_none_stop = dict(stop)
        r1226_strenum_empty_none_stop["effective_on_loading"] = StrEnum("R1226StrEnum", {"member": ""}).member
        r1226_strenum_empty_none = module.discovery_after_stop(r1226_strenum_empty_none_stop, bundle=None)
        r1226_strenum_empty_none_second = module.discovery_after_stop(r1226_strenum_empty_none_stop, bundle=None)
        self.assertIsNot(r1226_strenum_empty_none, r1226_strenum_empty_none_second)
        r1226_strenum_empty_omitted_stop = dict(stop)
        r1226_strenum_empty_omitted_stop["effective_on_loading"] = StrEnum("R1226StrEnum", {"member": ""}).member
        r1226_strenum_empty_omitted = module.discovery_after_stop(r1226_strenum_empty_omitted_stop)
        r1226_strenum_empty_omitted_second = module.discovery_after_stop(r1226_strenum_empty_omitted_stop)
        self.assertIsNot(r1226_strenum_empty_omitted, r1226_strenum_empty_omitted_second)
        r1226_flag_none_stop = dict(stop)
        r1226_flag_none_stop["effective_on_loading"] = Flag("R1226PlainFlag", {"member": 1}).member
        r1226_flag_none = module.discovery_after_stop(r1226_flag_none_stop, bundle=None)
        r1226_flag_none_second = module.discovery_after_stop(r1226_flag_none_stop, bundle=None)
        self.assertIsNot(r1226_flag_none, r1226_flag_none_second)
        r1226_flag_omitted_stop = dict(stop)
        r1226_flag_omitted_stop["effective_on_loading"] = Flag("R1226PlainFlag", {"member": 1}).member
        r1226_flag_omitted = module.discovery_after_stop(r1226_flag_omitted_stop)
        r1226_flag_omitted_second = module.discovery_after_stop(r1226_flag_omitted_stop)
        self.assertIsNot(r1226_flag_omitted, r1226_flag_omitted_second)
        r1226_flag_zero_none_stop = dict(stop)
        r1226_flag_zero_none_stop["effective_on_loading"] = Flag("R1226PlainFlag", {"member": 0}).member
        r1226_flag_zero_none = module.discovery_after_stop(r1226_flag_zero_none_stop, bundle=None)
        r1226_flag_zero_none_second = module.discovery_after_stop(r1226_flag_zero_none_stop, bundle=None)
        self.assertIsNot(r1226_flag_zero_none, r1226_flag_zero_none_second)
        r1226_flag_zero_omitted_stop = dict(stop)
        r1226_flag_zero_omitted_stop["effective_on_loading"] = Flag("R1226PlainFlag", {"member": 0}).member
        r1226_flag_zero_omitted = module.discovery_after_stop(r1226_flag_zero_omitted_stop)
        r1226_flag_zero_omitted_second = module.discovery_after_stop(r1226_flag_zero_omitted_stop)
        self.assertIsNot(r1226_flag_zero_omitted, r1226_flag_zero_omitted_second)

        r1227_values_none = module.discovery_after_stop({"k": "v"}.values(), bundle=None)
        r1227_values_none_second = module.discovery_after_stop({"k": "v"}.values(), bundle=None)
        self.assertIsNot(r1227_values_none, r1227_values_none_second)
        r1227_values_omitted = module.discovery_after_stop({"k": "v"}.values())
        r1227_values_omitted_second = module.discovery_after_stop({"k": "v"}.values())
        self.assertIsNot(r1227_values_omitted, r1227_values_omitted_second)
        r1227_intenum_none = module.discovery_after_stop(IntEnum("R1227Enum", {"member": 1}).member, bundle=None)
        r1227_intenum_none_second = module.discovery_after_stop(IntEnum("R1227Enum", {"member": 1}).member, bundle=None)
        self.assertIsNot(r1227_intenum_none, r1227_intenum_none_second)
        r1227_intenum_omitted = module.discovery_after_stop(IntEnum("R1227Enum", {"member": 1}).member)
        r1227_intenum_omitted_second = module.discovery_after_stop(IntEnum("R1227Enum", {"member": 1}).member)
        self.assertIsNot(r1227_intenum_omitted, r1227_intenum_omitted_second)
        r1227_range_none = module.discovery_after_stop(range(1), bundle=None)
        r1227_range_none_second = module.discovery_after_stop(range(1), bundle=None)
        self.assertIsNot(r1227_range_none, r1227_range_none_second)
        r1227_range_omitted = module.discovery_after_stop(range(1))
        r1227_range_omitted_second = module.discovery_after_stop(range(1))
        self.assertIsNot(r1227_range_omitted, r1227_range_omitted_second)
        r1227_datetime_none = module.discovery_after_stop(datetime(2026, 11, 17, 12, 0), bundle=None)
        r1227_datetime_none_second = module.discovery_after_stop(datetime(2026, 11, 17, 12, 0), bundle=None)
        self.assertIsNot(r1227_datetime_none, r1227_datetime_none_second)
        r1227_datetime_omitted = module.discovery_after_stop(datetime(2026, 11, 17, 12, 0))
        r1227_datetime_omitted_second = module.discovery_after_stop(datetime(2026, 11, 17, 12, 0))
        self.assertIsNot(r1227_datetime_omitted, r1227_datetime_omitted_second)
        r1227_uuid_none = module.discovery_after_stop(UUID(int=1), bundle=None)
        r1227_uuid_none_second = module.discovery_after_stop(UUID(int=1), bundle=None)
        self.assertIsNot(r1227_uuid_none, r1227_uuid_none_second)
        r1227_uuid_omitted = module.discovery_after_stop(UUID(int=1))
        r1227_uuid_omitted_second = module.discovery_after_stop(UUID(int=1))
        self.assertIsNot(r1227_uuid_omitted, r1227_uuid_omitted_second)

        r1228_chainmap = module.discovery_after_stop(ChainMap({"a stop key": "a stop value"}), bundle=bundle)
        r1228_chainmap_second = module.discovery_after_stop(ChainMap({"a stop key": "a stop value"}), bundle=bundle)
        self.assertIsNot(r1228_chainmap, r1228_chainmap_second)
        r1228_userdict = module.discovery_after_stop(UserDict({"a stop key": "a stop value"}), bundle=bundle)
        r1228_userdict_second = module.discovery_after_stop(UserDict({"a stop key": "a stop value"}), bundle=bundle)
        self.assertIsNot(r1228_userdict, r1228_userdict_second)
        r1228_defaultdict = module.discovery_after_stop(defaultdict(int, {"a stop key": 1}), bundle=bundle)
        r1228_defaultdict_second = module.discovery_after_stop(defaultdict(int, {"a stop key": 1}), bundle=bundle)
        self.assertIsNot(r1228_defaultdict, r1228_defaultdict_second)
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
        r815_list_none_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store=None)
        r815_list_none_second_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store=None)
        self.assertIsNot(r815_list_none_landed, r815_list_none_second_landed)
        r814_tuple_omitted_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",))
        r814_tuple_omitted_second_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",))
        self.assertIsNot(r814_tuple_omitted_landed, r814_tuple_omitted_second_landed)
        r815_tuple_none_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store=None)
        r815_tuple_none_second_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store=None)
        self.assertIsNot(r815_tuple_none_landed, r815_tuple_none_second_landed)
        r869_bytes_omitted_landed = module.journal_record_after_append(
            b"a stop standing as bytes")
        r869_bytes_omitted_second_landed = module.journal_record_after_append(
            b"a stop standing as bytes")
        self.assertIsNot(r869_bytes_omitted_landed, r869_bytes_omitted_second_landed)
        r869_integer_omitted_landed = module.journal_record_after_append(7)
        r869_integer_omitted_second_landed = module.journal_record_after_append(7)
        self.assertIsNot(r869_integer_omitted_landed, r869_integer_omitted_second_landed)
        r869_bytes_none_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store=None)
        r869_bytes_none_second_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store=None)
        self.assertIsNot(r869_bytes_none_landed, r869_bytes_none_second_landed)
        r869_integer_none_landed = module.journal_record_after_append(
            7, store=None)
        r869_integer_none_second_landed = module.journal_record_after_append(
            7, store=None)
        self.assertIsNot(r869_integer_none_landed, r869_integer_none_second_landed)
        r874_empty_none_landed = module.journal_record_after_append(
            {}, store=None)
        r874_empty_none_second_landed = module.journal_record_after_append(
            {}, store=None)
        self.assertIsNot(r874_empty_none_landed, r874_empty_none_second_landed)
        self.assertIsNot(
            r874_empty_none_landed["stop"], r874_empty_none_second_landed["stop"])

        r927_float_omitted_landed = module.journal_record_after_append(1.5)
        r927_float_omitted_second_landed = module.journal_record_after_append(1.5)
        self.assertIsNot(r927_float_omitted_landed, r927_float_omitted_second_landed)
        r927_set_omitted_landed = module.journal_record_after_append({"a stop standing as a set"})
        r927_set_omitted_second_landed = module.journal_record_after_append({"a stop standing as a set"})
        self.assertIsNot(r927_set_omitted_landed, r927_set_omitted_second_landed)
        r927_memoryview_omitted_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"))
        r927_memoryview_omitted_second_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"))
        self.assertIsNot(r927_memoryview_omitted_landed, r927_memoryview_omitted_second_landed)
        r927_fraction_omitted_landed = module.journal_record_after_append(Fraction(1, 2))
        r927_fraction_omitted_second_landed = module.journal_record_after_append(Fraction(1, 2))
        self.assertIsNot(r927_fraction_omitted_landed, r927_fraction_omitted_second_landed)
        r927_deque_omitted_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]))
        r927_deque_omitted_second_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]))
        self.assertIsNot(r927_deque_omitted_landed, r927_deque_omitted_second_landed)
        r928_float_omitted_landed = module.journal_record_after_append(1.5)
        r928_float_omitted_second_landed = module.journal_record_after_append(1.5)
        self.assertIsNot(r928_float_omitted_landed, r928_float_omitted_second_landed)
        r928_set_omitted_landed = module.journal_record_after_append({"a stop standing as a set"})
        r928_set_omitted_second_landed = module.journal_record_after_append({"a stop standing as a set"})
        self.assertIsNot(r928_set_omitted_landed, r928_set_omitted_second_landed)
        r928_frozenset_omitted_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}))
        r928_frozenset_omitted_second_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}))
        self.assertIsNot(r928_frozenset_omitted_landed, r928_frozenset_omitted_second_landed)
        r928_bytearray_omitted_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"))
        r928_bytearray_omitted_second_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"))
        self.assertIsNot(r928_bytearray_omitted_landed, r928_bytearray_omitted_second_landed)
        r928_true_omitted_landed = module.journal_record_after_append(True)
        r928_true_omitted_second_landed = module.journal_record_after_append(True)
        self.assertIsNot(r928_true_omitted_landed, r928_true_omitted_second_landed)
        r928_memoryview_omitted_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"))
        r928_memoryview_omitted_second_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"))
        self.assertIsNot(r928_memoryview_omitted_landed, r928_memoryview_omitted_second_landed)
        r928_fraction_omitted_landed = module.journal_record_after_append(Fraction(1, 2))
        r928_fraction_omitted_second_landed = module.journal_record_after_append(Fraction(1, 2))
        self.assertIsNot(r928_fraction_omitted_landed, r928_fraction_omitted_second_landed)
        r928_float_none_landed = module.journal_record_after_append(1.5, store=None)
        r928_float_none_second_landed = module.journal_record_after_append(1.5, store=None)
        self.assertIsNot(r928_float_none_landed, r928_float_none_second_landed)
        r928_set_none_landed = module.journal_record_after_append({"a stop standing as a set"}, store=None)
        r928_set_none_second_landed = module.journal_record_after_append({"a stop standing as a set"}, store=None)
        self.assertIsNot(r928_set_none_landed, r928_set_none_second_landed)
        r928_frozenset_none_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store=None)
        r928_frozenset_none_second_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store=None)
        self.assertIsNot(r928_frozenset_none_landed, r928_frozenset_none_second_landed)
        r928_bytearray_none_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store=None)
        r928_bytearray_none_second_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store=None)
        self.assertIsNot(r928_bytearray_none_landed, r928_bytearray_none_second_landed)
        r928_true_none_landed = module.journal_record_after_append(True, store=None)
        r928_true_none_second_landed = module.journal_record_after_append(True, store=None)
        self.assertIsNot(r928_true_none_landed, r928_true_none_second_landed)
        r928_memoryview_none_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store=None)
        r928_memoryview_none_second_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store=None)
        self.assertIsNot(r928_memoryview_none_landed, r928_memoryview_none_second_landed)
        r928_fraction_none_landed = module.journal_record_after_append(Fraction(1, 2), store=None)
        r928_fraction_none_second_landed = module.journal_record_after_append(Fraction(1, 2), store=None)
        self.assertIsNot(r928_fraction_none_landed, r928_fraction_none_second_landed)
        r983_timedelta_landed = module.journal_record_after_append(timedelta(days=1))
        r983_timedelta_second_landed = module.journal_record_after_append(timedelta(days=1))
        self.assertIsNot(r983_timedelta_landed, r983_timedelta_second_landed)
        r983_userlist_landed = module.journal_record_after_append(UserList([1]))
        r983_userlist_second_landed = module.journal_record_after_append(UserList([1]))
        self.assertIsNot(r983_userlist_landed, r983_userlist_second_landed)
        r983_userstring_landed = module.journal_record_after_append(UserString("x"))
        r983_userstring_second_landed = module.journal_record_after_append(UserString("x"))
        self.assertIsNot(r983_userstring_landed, r983_userstring_second_landed)
        r983_complex_landed = module.journal_record_after_append(1j)
        r983_complex_second_landed = module.journal_record_after_append(1j)
        self.assertIsNot(r983_complex_landed, r983_complex_second_landed)
        r983_decimal_landed = module.journal_record_after_append(Decimal(1))
        r983_decimal_second_landed = module.journal_record_after_append(Decimal(1))
        self.assertIsNot(r983_decimal_landed, r983_decimal_second_landed)
        r989_deque_none_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store=None)
        r989_deque_none_second_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store=None)
        self.assertIsNot(r989_deque_none_landed, r989_deque_none_second_landed)
        r990_array_omitted_landed = module.journal_record_after_append(array("i", [1]))
        r990_array_omitted_second_landed = module.journal_record_after_append(array("i", [1]))
        self.assertIsNot(r990_array_omitted_landed, r990_array_omitted_second_landed)
        r990_array_none_landed = module.journal_record_after_append(array("i", [1]), store=None)
        r990_array_none_second_landed = module.journal_record_after_append(array("i", [1]), store=None)
        self.assertIsNot(r990_array_none_landed, r990_array_none_second_landed)
        r991_counter_landed = module.journal_record_after_append(Counter({"a stop key": 1}))
        r991_counter_second_landed = module.journal_record_after_append(Counter({"a stop key": 1}))
        self.assertIsNot(r991_counter_landed, r991_counter_second_landed)
        self.assertIsNot(r991_counter_landed["stop"], r991_counter_second_landed["stop"])
        r991_ordered_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]))
        r991_ordered_second_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]))
        self.assertIsNot(r991_ordered_landed, r991_ordered_second_landed)
        self.assertIsNot(r991_ordered_landed["stop"], r991_ordered_second_landed["stop"])
        r1053_proxy_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}))
        r1053_proxy_second_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}))
        self.assertIsNot(r1053_proxy_landed, r1053_proxy_second_landed)
        r1053_namedtuple_landed = module.journal_record_after_append(namedtuple("R1053Tuple", ["field"])(1))
        r1053_namedtuple_second_landed = module.journal_record_after_append(namedtuple("R1053Tuple", ["field"])(1))
        self.assertIsNot(r1053_namedtuple_landed, r1053_namedtuple_second_landed)
        r1053_keys_landed = module.journal_record_after_append({"k": "v"}.keys())
        r1053_keys_second_landed = module.journal_record_after_append({"k": "v"}.keys())
        self.assertIsNot(r1053_keys_landed, r1053_keys_second_landed)
        r1053_path_landed = module.journal_record_after_append(Path("part"))
        r1053_path_second_landed = module.journal_record_after_append(Path("part"))
        self.assertIsNot(r1053_path_landed, r1053_path_second_landed)
        r1053_date_landed = module.journal_record_after_append(date(2026, 11, 17))
        r1053_date_second_landed = module.journal_record_after_append(date(2026, 11, 17))
        self.assertIsNot(r1053_date_landed, r1053_date_second_landed)
        r1059_timedelta_none_landed = module.journal_record_after_append(timedelta(days=1), store=None)
        r1059_timedelta_none_second_landed = module.journal_record_after_append(timedelta(days=1), store=None)
        self.assertIsNot(r1059_timedelta_none_landed, r1059_timedelta_none_second_landed)
        r1059_userlist_none_landed = module.journal_record_after_append(UserList([1]), store=None)
        r1059_userlist_none_second_landed = module.journal_record_after_append(UserList([1]), store=None)
        self.assertIsNot(r1059_userlist_none_landed, r1059_userlist_none_second_landed)
        r1059_userstring_none_landed = module.journal_record_after_append(UserString("x"), store=None)
        r1059_userstring_none_second_landed = module.journal_record_after_append(UserString("x"), store=None)
        self.assertIsNot(r1059_userstring_none_landed, r1059_userstring_none_second_landed)
        r1059_complex_none_landed = module.journal_record_after_append(1j, store=None)
        r1059_complex_none_second_landed = module.journal_record_after_append(1j, store=None)
        self.assertIsNot(r1059_complex_none_landed, r1059_complex_none_second_landed)
        r1059_decimal_none_landed = module.journal_record_after_append(Decimal(1), store=None)
        r1059_decimal_none_second_landed = module.journal_record_after_append(Decimal(1), store=None)
        self.assertIsNot(r1059_decimal_none_landed, r1059_decimal_none_second_landed)
        r1060_counter_none_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store=None)
        r1060_counter_none_second_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store=None)
        self.assertIsNot(r1060_counter_none_landed, r1060_counter_none_second_landed)
        self.assertIsNot(r1060_counter_none_landed["stop"], r1060_counter_none_second_landed["stop"])
        r1060_ordered_none_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store=None)
        r1060_ordered_none_second_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store=None)
        self.assertIsNot(r1060_ordered_none_landed, r1060_ordered_none_second_landed)
        self.assertIsNot(r1060_ordered_none_landed["stop"], r1060_ordered_none_second_landed["stop"])
        r1064_chainmap_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}))
        r1064_chainmap_second_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}))
        self.assertIsNot(r1064_chainmap_landed, r1064_chainmap_second_landed)
        self.assertIsNot(r1064_chainmap_landed["stop"], r1064_chainmap_second_landed["stop"])
        r1064_userdict_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}))
        r1064_userdict_second_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}))
        self.assertIsNot(r1064_userdict_landed, r1064_userdict_second_landed)
        self.assertIsNot(r1064_userdict_landed["stop"], r1064_userdict_second_landed["stop"])
        r1064_defaultdict_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}))
        r1064_defaultdict_second_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}))
        self.assertIsNot(r1064_defaultdict_landed, r1064_defaultdict_second_landed)
        self.assertIsNot(r1064_defaultdict_landed["stop"], r1064_defaultdict_second_landed["stop"])

        r1125_values_landed = module.journal_record_after_append({"k": "v"}.values())
        r1125_values_second_landed = module.journal_record_after_append({"k": "v"}.values())
        self.assertIsNot(r1125_values_landed, r1125_values_second_landed)
        r1125_intenum_landed = module.journal_record_after_append(IntEnum("R1125Enum", {"member": 1}).member)
        r1125_intenum_second_landed = module.journal_record_after_append(IntEnum("R1125Enum", {"member": 1}).member)
        self.assertIsNot(r1125_intenum_landed, r1125_intenum_second_landed)
        r1125_range_landed = module.journal_record_after_append(range(1))
        r1125_range_second_landed = module.journal_record_after_append(range(1))
        self.assertIsNot(r1125_range_landed, r1125_range_second_landed)
        r1125_datetime_landed = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0))
        r1125_datetime_second_landed = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0))
        self.assertIsNot(r1125_datetime_landed, r1125_datetime_second_landed)
        r1125_uuid_landed = module.journal_record_after_append(UUID(int=1))
        r1125_uuid_second_landed = module.journal_record_after_append(UUID(int=1))
        self.assertIsNot(r1125_uuid_landed, r1125_uuid_second_landed)
        r1133_proxy_none_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store=None)
        r1133_proxy_none_second_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store=None)
        self.assertIsNot(r1133_proxy_none_landed, r1133_proxy_none_second_landed)
        r1133_namedtuple_none_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store=None)
        r1133_namedtuple_none_second_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store=None)
        self.assertIsNot(r1133_namedtuple_none_landed, r1133_namedtuple_none_second_landed)
        r1133_keys_none_landed = module.journal_record_after_append({"k": "v"}.keys(), store=None)
        r1133_keys_none_second_landed = module.journal_record_after_append({"k": "v"}.keys(), store=None)
        self.assertIsNot(r1133_keys_none_landed, r1133_keys_none_second_landed)
        r1133_path_none_landed = module.journal_record_after_append(Path("part"), store=None)
        r1133_path_none_second_landed = module.journal_record_after_append(Path("part"), store=None)
        self.assertIsNot(r1133_path_none_landed, r1133_path_none_second_landed)
        r1133_date_none_landed = module.journal_record_after_append(date(2026, 11, 17), store=None)
        r1133_date_none_second_landed = module.journal_record_after_append(date(2026, 11, 17), store=None)
        self.assertIsNot(r1133_date_none_landed, r1133_date_none_second_landed)
        r1134_chainmap_none_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store=None)
        r1134_chainmap_none_second_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store=None)
        self.assertIsNot(r1134_chainmap_none_landed, r1134_chainmap_none_second_landed)
        self.assertIsNot(r1134_chainmap_none_landed["stop"], r1134_chainmap_none_second_landed["stop"])
        r1134_userdict_none_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store=None)
        r1134_userdict_none_second_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store=None)
        self.assertIsNot(r1134_userdict_none_landed, r1134_userdict_none_second_landed)
        self.assertIsNot(r1134_userdict_none_landed["stop"], r1134_userdict_none_second_landed["stop"])
        r1134_defaultdict_none_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store=None)
        r1134_defaultdict_none_second_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store=None)
        self.assertIsNot(r1134_defaultdict_none_landed, r1134_defaultdict_none_second_landed)
        self.assertIsNot(r1134_defaultdict_none_landed["stop"], r1134_defaultdict_none_second_landed["stop"])
        r1138_memoryview_landed = module.journal_record_after_append(memoryview(bytearray(b"a stop standing as a memoryview")))
        r1138_memoryview_second_landed = module.journal_record_after_append(memoryview(bytearray(b"a stop standing as a memoryview")))
        self.assertIsNot(r1138_memoryview_landed, r1138_memoryview_second_landed)

        r1218_slice_landed = module.journal_record_after_append(slice(1))
        r1218_slice_landed_second = module.journal_record_after_append(slice(1))
        self.assertIsNot(r1218_slice_landed, r1218_slice_landed_second)
        r1218_pattern_landed = module.journal_record_after_append(re.compile("a pattern"))
        r1218_pattern_landed_second = module.journal_record_after_append(re.compile("a pattern"))
        self.assertIsNot(r1218_pattern_landed, r1218_pattern_landed_second)
        r1218_enum_landed = module.journal_record_after_append(Enum("R1218Enum", {"member": 1}).member)
        r1218_enum_landed_second = module.journal_record_after_append(Enum("R1218Enum", {"member": 1}).member)
        self.assertIsNot(r1218_enum_landed, r1218_enum_landed_second)
        r1218_ipv4_landed = module.journal_record_after_append(IPv4Address("1.2.3.4"))
        r1218_ipv4_landed_second = module.journal_record_after_append(IPv4Address("1.2.3.4"))
        self.assertIsNot(r1218_ipv4_landed, r1218_ipv4_landed_second)
        r1218_timezone_landed = module.journal_record_after_append(timezone.utc)
        r1218_timezone_landed_second = module.journal_record_after_append(timezone.utc)
        self.assertIsNot(r1218_timezone_landed, r1218_timezone_landed_second)

        r1229_values_none_landed = module.journal_record_after_append({"k": "v"}.values(), store=None)
        r1229_values_none_landed_second = module.journal_record_after_append({"k": "v"}.values(), store=None)
        self.assertIsNot(r1229_values_none_landed, r1229_values_none_landed_second)
        r1229_intenum_none_landed = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store=None)
        r1229_intenum_none_landed_second = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store=None)
        self.assertIsNot(r1229_intenum_none_landed, r1229_intenum_none_landed_second)
        r1229_range_none_landed = module.journal_record_after_append(range(1), store=None)
        r1229_range_none_landed_second = module.journal_record_after_append(range(1), store=None)
        self.assertIsNot(r1229_range_none_landed, r1229_range_none_landed_second)
        r1229_datetime_none_landed = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store=None)
        r1229_datetime_none_landed_second = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store=None)
        self.assertIsNot(r1229_datetime_none_landed, r1229_datetime_none_landed_second)
        r1229_uuid_none_landed = module.journal_record_after_append(UUID(int=1), store=None)
        r1229_uuid_none_landed_second = module.journal_record_after_append(UUID(int=1), store=None)
        self.assertIsNot(r1229_uuid_none_landed, r1229_uuid_none_landed_second)

        r1230_items_landed = module.journal_record_after_append({"k": "v"}.items())
        r1230_items_landed_second = module.journal_record_after_append({"k": "v"}.items())
        self.assertIsNot(r1230_items_landed, r1230_items_landed_second)
        r1230_items_empty_landed = module.journal_record_after_append({}.items())
        r1230_items_empty_landed_second = module.journal_record_after_append({}.items())
        self.assertIsNot(r1230_items_empty_landed, r1230_items_empty_landed_second)
        r1230_intflag_landed = module.journal_record_after_append(IntFlag("R1230Flag", {"member": 1}).member)
        r1230_intflag_landed_second = module.journal_record_after_append(IntFlag("R1230Flag", {"member": 1}).member)
        self.assertIsNot(r1230_intflag_landed, r1230_intflag_landed_second)
        r1230_intflag_zero_landed = module.journal_record_after_append(IntFlag("R1230Flag", {"member": 0}).member)
        r1230_intflag_zero_landed_second = module.journal_record_after_append(IntFlag("R1230Flag", {"member": 0}).member)
        self.assertIsNot(r1230_intflag_zero_landed, r1230_intflag_zero_landed_second)
        r1230_strenum_landed = module.journal_record_after_append(StrEnum("R1230StrEnum", {"member": "x"}).member)
        r1230_strenum_landed_second = module.journal_record_after_append(StrEnum("R1230StrEnum", {"member": "x"}).member)
        self.assertIsNot(r1230_strenum_landed, r1230_strenum_landed_second)
        r1230_strenum_empty_landed = module.journal_record_after_append(StrEnum("R1230StrEnum", {"member": ""}).member)
        r1230_strenum_empty_landed_second = module.journal_record_after_append(StrEnum("R1230StrEnum", {"member": ""}).member)
        self.assertIsNot(r1230_strenum_empty_landed, r1230_strenum_empty_landed_second)
        r1230_flag_landed = module.journal_record_after_append(Flag("R1230PlainFlag", {"member": 1}).member)
        r1230_flag_landed_second = module.journal_record_after_append(Flag("R1230PlainFlag", {"member": 1}).member)
        self.assertIsNot(r1230_flag_landed, r1230_flag_landed_second)
        r1230_flag_zero_landed = module.journal_record_after_append(Flag("R1230PlainFlag", {"member": 0}).member)
        r1230_flag_zero_landed_second = module.journal_record_after_append(Flag("R1230PlainFlag", {"member": 0}).member)
        self.assertIsNot(r1230_flag_zero_landed, r1230_flag_zero_landed_second)
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
        r814_list_empty_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store={})
        r814_list_empty_second_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store={})
        self.assertIsNot(r814_list_empty_landed, r814_list_empty_second_landed)
        r815_list_standing_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store=standing_store)
        r815_list_standing_second_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store=standing_store)
        self.assertIsNot(r815_list_standing_landed, r815_list_standing_second_landed)
        r815_tuple_empty_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store={})
        r815_tuple_empty_second_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store={})
        self.assertIsNot(r815_tuple_empty_landed, r815_tuple_empty_second_landed)
        r815_tuple_standing_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store=standing_store)
        r815_tuple_standing_second_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store=standing_store)
        self.assertIsNot(r815_tuple_standing_landed, r815_tuple_standing_second_landed)
        r814_empty_standing_landed = module.journal_record_after_append(
            {}, store=standing_store)
        r814_empty_standing_second_landed = module.journal_record_after_append(
            {}, store=standing_store)
        self.assertIsNot(r814_empty_standing_landed, r814_empty_standing_second_landed)
        self.assertIsNot(
            r814_empty_standing_landed["stop"], r814_empty_standing_second_landed["stop"])
        r869_bytes_empty_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store={})
        r869_bytes_empty_second_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store={})
        self.assertIsNot(r869_bytes_empty_landed, r869_bytes_empty_second_landed)
        r869_integer_empty_landed = module.journal_record_after_append(
            7, store={})
        r869_integer_empty_second_landed = module.journal_record_after_append(
            7, store={})
        self.assertIsNot(r869_integer_empty_landed, r869_integer_empty_second_landed)
        r869_bytes_standing_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store=standing_store)
        r869_bytes_standing_second_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store=standing_store)
        self.assertIsNot(r869_bytes_standing_landed, r869_bytes_standing_second_landed)
        r869_integer_standing_landed = module.journal_record_after_append(
            7, store=standing_store)
        r869_integer_standing_second_landed = module.journal_record_after_append(
            7, store=standing_store)
        self.assertIsNot(r869_integer_standing_landed, r869_integer_standing_second_landed)

        r928_float_empty_landed = module.journal_record_after_append(1.5, store={})
        r928_float_empty_second_landed = module.journal_record_after_append(1.5, store={})
        self.assertIsNot(r928_float_empty_landed, r928_float_empty_second_landed)
        r928_set_empty_landed = module.journal_record_after_append({"a stop standing as a set"}, store={})
        r928_set_empty_second_landed = module.journal_record_after_append({"a stop standing as a set"}, store={})
        self.assertIsNot(r928_set_empty_landed, r928_set_empty_second_landed)
        r928_frozenset_empty_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store={})
        r928_frozenset_empty_second_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store={})
        self.assertIsNot(r928_frozenset_empty_landed, r928_frozenset_empty_second_landed)
        r928_bytearray_empty_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store={})
        r928_bytearray_empty_second_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store={})
        self.assertIsNot(r928_bytearray_empty_landed, r928_bytearray_empty_second_landed)
        r928_true_empty_landed = module.journal_record_after_append(True, store={})
        r928_true_empty_second_landed = module.journal_record_after_append(True, store={})
        self.assertIsNot(r928_true_empty_landed, r928_true_empty_second_landed)
        r928_memoryview_empty_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store={})
        r928_memoryview_empty_second_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store={})
        self.assertIsNot(r928_memoryview_empty_landed, r928_memoryview_empty_second_landed)
        r928_fraction_empty_landed = module.journal_record_after_append(Fraction(1, 2), store={})
        r928_fraction_empty_second_landed = module.journal_record_after_append(Fraction(1, 2), store={})
        self.assertIsNot(r928_fraction_empty_landed, r928_fraction_empty_second_landed)
        r928_float_standing_landed = module.journal_record_after_append(1.5, store=standing_store)
        r928_float_standing_second_landed = module.journal_record_after_append(1.5, store=standing_store)
        self.assertIsNot(r928_float_standing_landed, r928_float_standing_second_landed)
        r928_set_standing_landed = module.journal_record_after_append({"a stop standing as a set"}, store=standing_store)
        r928_set_standing_second_landed = module.journal_record_after_append({"a stop standing as a set"}, store=standing_store)
        self.assertIsNot(r928_set_standing_landed, r928_set_standing_second_landed)
        r928_frozenset_standing_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store=standing_store)
        r928_frozenset_standing_second_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store=standing_store)
        self.assertIsNot(r928_frozenset_standing_landed, r928_frozenset_standing_second_landed)
        r928_bytearray_standing_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store=standing_store)
        r928_bytearray_standing_second_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store=standing_store)
        self.assertIsNot(r928_bytearray_standing_landed, r928_bytearray_standing_second_landed)
        r928_true_standing_landed = module.journal_record_after_append(True, store=standing_store)
        r928_true_standing_second_landed = module.journal_record_after_append(True, store=standing_store)
        self.assertIsNot(r928_true_standing_landed, r928_true_standing_second_landed)
        r928_memoryview_standing_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store=standing_store)
        r928_memoryview_standing_second_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store=standing_store)
        self.assertIsNot(r928_memoryview_standing_landed, r928_memoryview_standing_second_landed)
        r928_fraction_standing_landed = module.journal_record_after_append(Fraction(1, 2), store=standing_store)
        r928_fraction_standing_second_landed = module.journal_record_after_append(Fraction(1, 2), store=standing_store)
        self.assertIsNot(r928_fraction_standing_landed, r928_fraction_standing_second_landed)
        r989_deque_empty_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store={})
        r989_deque_empty_second_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store={})
        self.assertIsNot(r989_deque_empty_landed, r989_deque_empty_second_landed)
        r989_deque_standing_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store=standing_store)
        r989_deque_standing_second_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store=standing_store)
        self.assertIsNot(r989_deque_standing_landed, r989_deque_standing_second_landed)
        r990_array_empty_landed = module.journal_record_after_append(array("i", [1]), store={})
        r990_array_empty_second_landed = module.journal_record_after_append(array("i", [1]), store={})
        self.assertIsNot(r990_array_empty_landed, r990_array_empty_second_landed)
        r990_array_standing_landed = module.journal_record_after_append(array("i", [1]), store=standing_store)
        r990_array_standing_second_landed = module.journal_record_after_append(array("i", [1]), store=standing_store)
        self.assertIsNot(r990_array_standing_landed, r990_array_standing_second_landed)
        r1059_timedelta_empty_landed = module.journal_record_after_append(timedelta(days=1), store={})
        r1059_timedelta_empty_second_landed = module.journal_record_after_append(timedelta(days=1), store={})
        self.assertIsNot(r1059_timedelta_empty_landed, r1059_timedelta_empty_second_landed)
        r1059_timedelta_standing_landed = module.journal_record_after_append(timedelta(days=1), store=standing_store)
        r1059_timedelta_standing_second_landed = module.journal_record_after_append(timedelta(days=1), store=standing_store)
        self.assertIsNot(r1059_timedelta_standing_landed, r1059_timedelta_standing_second_landed)
        r1059_userlist_empty_landed = module.journal_record_after_append(UserList([1]), store={})
        r1059_userlist_empty_second_landed = module.journal_record_after_append(UserList([1]), store={})
        self.assertIsNot(r1059_userlist_empty_landed, r1059_userlist_empty_second_landed)
        r1059_userlist_standing_landed = module.journal_record_after_append(UserList([1]), store=standing_store)
        r1059_userlist_standing_second_landed = module.journal_record_after_append(UserList([1]), store=standing_store)
        self.assertIsNot(r1059_userlist_standing_landed, r1059_userlist_standing_second_landed)
        r1059_userstring_empty_landed = module.journal_record_after_append(UserString("x"), store={})
        r1059_userstring_empty_second_landed = module.journal_record_after_append(UserString("x"), store={})
        self.assertIsNot(r1059_userstring_empty_landed, r1059_userstring_empty_second_landed)
        r1059_userstring_standing_landed = module.journal_record_after_append(UserString("x"), store=standing_store)
        r1059_userstring_standing_second_landed = module.journal_record_after_append(UserString("x"), store=standing_store)
        self.assertIsNot(r1059_userstring_standing_landed, r1059_userstring_standing_second_landed)
        r1059_complex_empty_landed = module.journal_record_after_append(1j, store={})
        r1059_complex_empty_second_landed = module.journal_record_after_append(1j, store={})
        self.assertIsNot(r1059_complex_empty_landed, r1059_complex_empty_second_landed)
        r1059_complex_standing_landed = module.journal_record_after_append(1j, store=standing_store)
        r1059_complex_standing_second_landed = module.journal_record_after_append(1j, store=standing_store)
        self.assertIsNot(r1059_complex_standing_landed, r1059_complex_standing_second_landed)
        r1059_decimal_empty_landed = module.journal_record_after_append(Decimal(1), store={})
        r1059_decimal_empty_second_landed = module.journal_record_after_append(Decimal(1), store={})
        self.assertIsNot(r1059_decimal_empty_landed, r1059_decimal_empty_second_landed)
        r1059_decimal_standing_landed = module.journal_record_after_append(Decimal(1), store=standing_store)
        r1059_decimal_standing_second_landed = module.journal_record_after_append(Decimal(1), store=standing_store)
        self.assertIsNot(r1059_decimal_standing_landed, r1059_decimal_standing_second_landed)
        r1060_counter_empty_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store={})
        r1060_counter_empty_second_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store={})
        self.assertIsNot(r1060_counter_empty_landed, r1060_counter_empty_second_landed)
        self.assertIsNot(r1060_counter_empty_landed["stop"], r1060_counter_empty_second_landed["stop"])
        r1060_counter_standing_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store=standing_store)
        r1060_counter_standing_second_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store=standing_store)
        self.assertIsNot(r1060_counter_standing_landed, r1060_counter_standing_second_landed)
        self.assertIsNot(r1060_counter_standing_landed["stop"], r1060_counter_standing_second_landed["stop"])
        r1060_ordered_empty_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store={})
        r1060_ordered_empty_second_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store={})
        self.assertIsNot(r1060_ordered_empty_landed, r1060_ordered_empty_second_landed)
        self.assertIsNot(r1060_ordered_empty_landed["stop"], r1060_ordered_empty_second_landed["stop"])
        r1060_ordered_standing_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store=standing_store)
        r1060_ordered_standing_second_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store=standing_store)
        self.assertIsNot(r1060_ordered_standing_landed, r1060_ordered_standing_second_landed)
        self.assertIsNot(r1060_ordered_standing_landed["stop"], r1060_ordered_standing_second_landed["stop"])

        r1133_proxy_empty_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store={})
        r1133_proxy_empty_second_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store={})
        self.assertIsNot(r1133_proxy_empty_landed, r1133_proxy_empty_second_landed)
        r1133_proxy_standing_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store=standing_store)
        r1133_proxy_standing_second_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store=standing_store)
        self.assertIsNot(r1133_proxy_standing_landed, r1133_proxy_standing_second_landed)
        r1133_namedtuple_empty_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store={})
        r1133_namedtuple_empty_second_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store={})
        self.assertIsNot(r1133_namedtuple_empty_landed, r1133_namedtuple_empty_second_landed)
        r1133_namedtuple_standing_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store=standing_store)
        r1133_namedtuple_standing_second_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store=standing_store)
        self.assertIsNot(r1133_namedtuple_standing_landed, r1133_namedtuple_standing_second_landed)
        r1133_keys_empty_landed = module.journal_record_after_append({"k": "v"}.keys(), store={})
        r1133_keys_empty_second_landed = module.journal_record_after_append({"k": "v"}.keys(), store={})
        self.assertIsNot(r1133_keys_empty_landed, r1133_keys_empty_second_landed)
        r1133_keys_standing_landed = module.journal_record_after_append({"k": "v"}.keys(), store=standing_store)
        r1133_keys_standing_second_landed = module.journal_record_after_append({"k": "v"}.keys(), store=standing_store)
        self.assertIsNot(r1133_keys_standing_landed, r1133_keys_standing_second_landed)
        r1133_path_empty_landed = module.journal_record_after_append(Path("part"), store={})
        r1133_path_empty_second_landed = module.journal_record_after_append(Path("part"), store={})
        self.assertIsNot(r1133_path_empty_landed, r1133_path_empty_second_landed)
        r1133_path_standing_landed = module.journal_record_after_append(Path("part"), store=standing_store)
        r1133_path_standing_second_landed = module.journal_record_after_append(Path("part"), store=standing_store)
        self.assertIsNot(r1133_path_standing_landed, r1133_path_standing_second_landed)
        r1133_date_empty_landed = module.journal_record_after_append(date(2026, 11, 17), store={})
        r1133_date_empty_second_landed = module.journal_record_after_append(date(2026, 11, 17), store={})
        self.assertIsNot(r1133_date_empty_landed, r1133_date_empty_second_landed)
        r1133_date_standing_landed = module.journal_record_after_append(date(2026, 11, 17), store=standing_store)
        r1133_date_standing_second_landed = module.journal_record_after_append(date(2026, 11, 17), store=standing_store)
        self.assertIsNot(r1133_date_standing_landed, r1133_date_standing_second_landed)
        r1134_chainmap_empty_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store={})
        r1134_chainmap_empty_second_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store={})
        self.assertIsNot(r1134_chainmap_empty_landed, r1134_chainmap_empty_second_landed)
        self.assertIsNot(r1134_chainmap_empty_landed["stop"], r1134_chainmap_empty_second_landed["stop"])
        r1134_chainmap_standing_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store=standing_store)
        r1134_chainmap_standing_second_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store=standing_store)
        self.assertIsNot(r1134_chainmap_standing_landed, r1134_chainmap_standing_second_landed)
        self.assertIsNot(r1134_chainmap_standing_landed["stop"], r1134_chainmap_standing_second_landed["stop"])
        r1134_userdict_empty_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store={})
        r1134_userdict_empty_second_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store={})
        self.assertIsNot(r1134_userdict_empty_landed, r1134_userdict_empty_second_landed)
        self.assertIsNot(r1134_userdict_empty_landed["stop"], r1134_userdict_empty_second_landed["stop"])
        r1134_userdict_standing_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store=standing_store)
        r1134_userdict_standing_second_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store=standing_store)
        self.assertIsNot(r1134_userdict_standing_landed, r1134_userdict_standing_second_landed)
        self.assertIsNot(r1134_userdict_standing_landed["stop"], r1134_userdict_standing_second_landed["stop"])
        r1134_defaultdict_empty_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store={})
        r1134_defaultdict_empty_second_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store={})
        self.assertIsNot(r1134_defaultdict_empty_landed, r1134_defaultdict_empty_second_landed)
        self.assertIsNot(r1134_defaultdict_empty_landed["stop"], r1134_defaultdict_empty_second_landed["stop"])
        r1134_defaultdict_standing_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store=standing_store)
        r1134_defaultdict_standing_second_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store=standing_store)
        self.assertIsNot(r1134_defaultdict_standing_landed, r1134_defaultdict_standing_second_landed)
        self.assertIsNot(r1134_defaultdict_standing_landed["stop"], r1134_defaultdict_standing_second_landed["stop"])

        r1229_values_empty_landed = module.journal_record_after_append({"k": "v"}.values(), store={})
        r1229_values_empty_landed_second = module.journal_record_after_append({"k": "v"}.values(), store={})
        self.assertIsNot(r1229_values_empty_landed, r1229_values_empty_landed_second)
        r1229_values_standing_landed = module.journal_record_after_append({"k": "v"}.values(), store=standing_store)
        r1229_values_standing_landed_second = module.journal_record_after_append({"k": "v"}.values(), store=standing_store)
        self.assertIsNot(r1229_values_standing_landed, r1229_values_standing_landed_second)
        r1229_intenum_empty_landed = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store={})
        r1229_intenum_empty_landed_second = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store={})
        self.assertIsNot(r1229_intenum_empty_landed, r1229_intenum_empty_landed_second)
        r1229_intenum_standing_landed = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store=standing_store)
        r1229_intenum_standing_landed_second = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store=standing_store)
        self.assertIsNot(r1229_intenum_standing_landed, r1229_intenum_standing_landed_second)
        r1229_range_empty_landed = module.journal_record_after_append(range(1), store={})
        r1229_range_empty_landed_second = module.journal_record_after_append(range(1), store={})
        self.assertIsNot(r1229_range_empty_landed, r1229_range_empty_landed_second)
        r1229_range_standing_landed = module.journal_record_after_append(range(1), store=standing_store)
        r1229_range_standing_landed_second = module.journal_record_after_append(range(1), store=standing_store)
        self.assertIsNot(r1229_range_standing_landed, r1229_range_standing_landed_second)
        r1229_datetime_empty_landed = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store={})
        r1229_datetime_empty_landed_second = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store={})
        self.assertIsNot(r1229_datetime_empty_landed, r1229_datetime_empty_landed_second)
        r1229_datetime_standing_landed = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store=standing_store)
        r1229_datetime_standing_landed_second = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store=standing_store)
        self.assertIsNot(r1229_datetime_standing_landed, r1229_datetime_standing_landed_second)
        r1229_uuid_empty_landed = module.journal_record_after_append(UUID(int=1), store={})
        r1229_uuid_empty_landed_second = module.journal_record_after_append(UUID(int=1), store={})
        self.assertIsNot(r1229_uuid_empty_landed, r1229_uuid_empty_landed_second)
        r1229_uuid_standing_landed = module.journal_record_after_append(UUID(int=1), store=standing_store)
        r1229_uuid_standing_landed_second = module.journal_record_after_append(UUID(int=1), store=standing_store)
        self.assertIsNot(r1229_uuid_standing_landed, r1229_uuid_standing_landed_second)
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
        r814_list_appending_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store=appending_store)
        r814_list_appending_second_landed = module.journal_record_after_append(
            ["a stop standing as a list"], store=appending_store)
        self.assertIsNot(r814_list_appending_landed, r814_list_appending_second_landed)
        r815_tuple_appending_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store=appending_store)
        r815_tuple_appending_second_landed = module.journal_record_after_append(
            ("a stop standing as a tuple",), store=appending_store)
        self.assertIsNot(r815_tuple_appending_landed, r815_tuple_appending_second_landed)
        r869_bytes_appending_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store=appending_store)
        r869_bytes_appending_second_landed = module.journal_record_after_append(
            b"a stop standing as bytes", store=appending_store)
        self.assertIsNot(r869_bytes_appending_landed, r869_bytes_appending_second_landed)
        r869_integer_appending_landed = module.journal_record_after_append(
            7, store=appending_store)
        r869_integer_appending_second_landed = module.journal_record_after_append(
            7, store=appending_store)
        self.assertIsNot(r869_integer_appending_landed, r869_integer_appending_second_landed)

        r928_float_appending_landed = module.journal_record_after_append(1.5, store=appending_store)
        r928_float_appending_second_landed = module.journal_record_after_append(1.5, store=appending_store)
        self.assertIsNot(r928_float_appending_landed, r928_float_appending_second_landed)
        r928_set_appending_landed = module.journal_record_after_append({"a stop standing as a set"}, store=appending_store)
        r928_set_appending_second_landed = module.journal_record_after_append({"a stop standing as a set"}, store=appending_store)
        self.assertIsNot(r928_set_appending_landed, r928_set_appending_second_landed)
        r928_frozenset_appending_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store=appending_store)
        r928_frozenset_appending_second_landed = module.journal_record_after_append(frozenset({"a stop standing as a frozenset"}), store=appending_store)
        self.assertIsNot(r928_frozenset_appending_landed, r928_frozenset_appending_second_landed)
        r928_bytearray_appending_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store=appending_store)
        r928_bytearray_appending_second_landed = module.journal_record_after_append(bytearray(b"a stop standing as a bytearray"), store=appending_store)
        self.assertIsNot(r928_bytearray_appending_landed, r928_bytearray_appending_second_landed)
        r928_true_appending_landed = module.journal_record_after_append(True, store=appending_store)
        r928_true_appending_second_landed = module.journal_record_after_append(True, store=appending_store)
        self.assertIsNot(r928_true_appending_landed, r928_true_appending_second_landed)
        r928_memoryview_appending_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store=appending_store)
        r928_memoryview_appending_second_landed = module.journal_record_after_append(memoryview(b"a stop standing as a memoryview"), store=appending_store)
        self.assertIsNot(r928_memoryview_appending_landed, r928_memoryview_appending_second_landed)
        r928_fraction_appending_landed = module.journal_record_after_append(Fraction(1, 2), store=appending_store)
        r928_fraction_appending_second_landed = module.journal_record_after_append(Fraction(1, 2), store=appending_store)
        self.assertIsNot(r928_fraction_appending_landed, r928_fraction_appending_second_landed)
        r989_deque_appending_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store=appending_store)
        r989_deque_appending_second_landed = module.journal_record_after_append(deque(["a stop standing as a deque"]), store=appending_store)
        self.assertIsNot(r989_deque_appending_landed, r989_deque_appending_second_landed)
        r990_array_appending_landed = module.journal_record_after_append(array("i", [1]), store=appending_store)
        r990_array_appending_second_landed = module.journal_record_after_append(array("i", [1]), store=appending_store)
        self.assertIsNot(r990_array_appending_landed, r990_array_appending_second_landed)
        r1059_timedelta_appending_landed = module.journal_record_after_append(timedelta(days=1), store=appending_store)
        r1059_timedelta_appending_second_landed = module.journal_record_after_append(timedelta(days=1), store=appending_store)
        self.assertIsNot(r1059_timedelta_appending_landed, r1059_timedelta_appending_second_landed)
        r1059_userlist_appending_landed = module.journal_record_after_append(UserList([1]), store=appending_store)
        r1059_userlist_appending_second_landed = module.journal_record_after_append(UserList([1]), store=appending_store)
        self.assertIsNot(r1059_userlist_appending_landed, r1059_userlist_appending_second_landed)
        r1059_userstring_appending_landed = module.journal_record_after_append(UserString("x"), store=appending_store)
        r1059_userstring_appending_second_landed = module.journal_record_after_append(UserString("x"), store=appending_store)
        self.assertIsNot(r1059_userstring_appending_landed, r1059_userstring_appending_second_landed)
        r1059_complex_appending_landed = module.journal_record_after_append(1j, store=appending_store)
        r1059_complex_appending_second_landed = module.journal_record_after_append(1j, store=appending_store)
        self.assertIsNot(r1059_complex_appending_landed, r1059_complex_appending_second_landed)
        r1059_decimal_appending_landed = module.journal_record_after_append(Decimal(1), store=appending_store)
        r1059_decimal_appending_second_landed = module.journal_record_after_append(Decimal(1), store=appending_store)
        self.assertIsNot(r1059_decimal_appending_landed, r1059_decimal_appending_second_landed)
        r1060_counter_appending_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store=appending_store)
        r1060_counter_appending_second_landed = module.journal_record_after_append(Counter({"a stop key": 1}), store=appending_store)
        self.assertIsNot(r1060_counter_appending_landed, r1060_counter_appending_second_landed)
        self.assertIsNot(r1060_counter_appending_landed["stop"], r1060_counter_appending_second_landed["stop"])
        r1060_ordered_appending_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store=appending_store)
        r1060_ordered_appending_second_landed = module.journal_record_after_append(OrderedDict([("a stop key", "a stop value")]), store=appending_store)
        self.assertIsNot(r1060_ordered_appending_landed, r1060_ordered_appending_second_landed)
        self.assertIsNot(r1060_ordered_appending_landed["stop"], r1060_ordered_appending_second_landed["stop"])

        r1133_proxy_appending_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store=appending_store)
        r1133_proxy_appending_second_landed = module.journal_record_after_append(MappingProxyType({"k": "v"}), store=appending_store)
        self.assertIsNot(r1133_proxy_appending_landed, r1133_proxy_appending_second_landed)
        r1133_namedtuple_appending_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store=appending_store)
        r1133_namedtuple_appending_second_landed = module.journal_record_after_append(namedtuple("R1133Tuple", ["field"])(1), store=appending_store)
        self.assertIsNot(r1133_namedtuple_appending_landed, r1133_namedtuple_appending_second_landed)
        r1133_keys_appending_landed = module.journal_record_after_append({"k": "v"}.keys(), store=appending_store)
        r1133_keys_appending_second_landed = module.journal_record_after_append({"k": "v"}.keys(), store=appending_store)
        self.assertIsNot(r1133_keys_appending_landed, r1133_keys_appending_second_landed)
        r1133_path_appending_landed = module.journal_record_after_append(Path("part"), store=appending_store)
        r1133_path_appending_second_landed = module.journal_record_after_append(Path("part"), store=appending_store)
        self.assertIsNot(r1133_path_appending_landed, r1133_path_appending_second_landed)
        r1133_date_appending_landed = module.journal_record_after_append(date(2026, 11, 17), store=appending_store)
        r1133_date_appending_second_landed = module.journal_record_after_append(date(2026, 11, 17), store=appending_store)
        self.assertIsNot(r1133_date_appending_landed, r1133_date_appending_second_landed)
        r1134_chainmap_appending_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store=appending_store)
        r1134_chainmap_appending_second_landed = module.journal_record_after_append(ChainMap({"a stop key": "a stop value"}), store=appending_store)
        self.assertIsNot(r1134_chainmap_appending_landed, r1134_chainmap_appending_second_landed)
        self.assertIsNot(r1134_chainmap_appending_landed["stop"], r1134_chainmap_appending_second_landed["stop"])
        r1134_userdict_appending_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store=appending_store)
        r1134_userdict_appending_second_landed = module.journal_record_after_append(UserDict({"a stop key": "a stop value"}), store=appending_store)
        self.assertIsNot(r1134_userdict_appending_landed, r1134_userdict_appending_second_landed)
        self.assertIsNot(r1134_userdict_appending_landed["stop"], r1134_userdict_appending_second_landed["stop"])
        r1134_defaultdict_appending_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store=appending_store)
        r1134_defaultdict_appending_second_landed = module.journal_record_after_append(defaultdict(int, {"a stop key": 1}), store=appending_store)
        self.assertIsNot(r1134_defaultdict_appending_landed, r1134_defaultdict_appending_second_landed)
        self.assertIsNot(r1134_defaultdict_appending_landed["stop"], r1134_defaultdict_appending_second_landed["stop"])

        r1229_values_appending_landed = module.journal_record_after_append({"k": "v"}.values(), store=appending_store)
        r1229_values_appending_landed_second = module.journal_record_after_append({"k": "v"}.values(), store=appending_store)
        self.assertIsNot(r1229_values_appending_landed, r1229_values_appending_landed_second)
        r1229_intenum_appending_landed = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store=appending_store)
        r1229_intenum_appending_landed_second = module.journal_record_after_append(IntEnum("R1229Enum", {"member": 1}).member, store=appending_store)
        self.assertIsNot(r1229_intenum_appending_landed, r1229_intenum_appending_landed_second)
        r1229_range_appending_landed = module.journal_record_after_append(range(1), store=appending_store)
        r1229_range_appending_landed_second = module.journal_record_after_append(range(1), store=appending_store)
        self.assertIsNot(r1229_range_appending_landed, r1229_range_appending_landed_second)
        r1229_datetime_appending_landed = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store=appending_store)
        r1229_datetime_appending_landed_second = module.journal_record_after_append(datetime(2026, 11, 17, 12, 0), store=appending_store)
        self.assertIsNot(r1229_datetime_appending_landed, r1229_datetime_appending_landed_second)
        r1229_uuid_appending_landed = module.journal_record_after_append(UUID(int=1), store=appending_store)
        r1229_uuid_appending_landed_second = module.journal_record_after_append(UUID(int=1), store=appending_store)
        self.assertIsNot(r1229_uuid_appending_landed, r1229_uuid_appending_landed_second)
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
