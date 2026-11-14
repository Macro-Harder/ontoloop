"""The spanning suite module: meaning checks and suite coverage checks.

This module discharges the RR-CL-22 route charge as the Step 12 gate
record states it at its section 5, charge 3, governed by plan subsection
19.101 point one: at Step 13, the Write tests unit defines the spanning
suite meaning checks for each affected class, in the suite as written at
Step 13. The affected classes are the classes the trigger at plan
subsection 18.45 names: a deduplication, clustering, normalisation,
filtering, redaction, or truncation parameter or rule; a type mapping
change; and a new enum value absorbed by a default branch, in the
capture, dataset, or evaluation path.

Each meaning check below carries a suite identifier in the naming form
plan section 6.2 settles, a fixture, and a pass condition stating the
record state that shows the meaning held and the record state that shows
the meaning changed. The identifier form used here is SPAN, then T, then
a two digit number, recorded as a transcription choice of this module:
the checks are suite checks of the spanning suite, not rows of the
refreshed list, and no list identifier is reused for any of them.

Pass condition, common form for every meaning check: the check runs the
fixture records under the rule before the change and under the rule
after the change. Meaning held: the outcome records are identical in
full, and the meaning change record entry in the suite result record
classifies the change as no meaning change shown, naming the change,
the affected class, the check identifier, the result, and the
discharging seat. Meaning changed: the outcome records differ, and the
entry classifies the change as a meaning change under a stable shape;
the change is not passed as no change in any report, and the loop
report prints the classification by pointer to that entry only.

This module also carries the suite own coverage checks, which pass or
fail for real on the suite as written: every row identifier in the
refreshed list (129) appears in exactly one manifest part; every one of
the twelve F-C2 subsections appears in exactly one manifest part; and
no manifest entry names the quantity limb of REDACT-T08. The coverage
checks read their sources at run time, the row identifiers from the row
headings of the refreshed list itself and the twelve subsections from
the F-C2 ruling record in the content re-trace, and they count a row or
a subsection as homed only where it stands as a manifest entry key,
never where it appears as a stray string value in a part. The quantity
check follows the REDACT-T08 entry in key form and in value form alike,
in object parts and in list parts alike, and it reads the limb under
the word quantity and under the amount, magnitude, unit, and source
class wordings.
"""

import json
import os
import re
import unittest

from tests import harness

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PARTS = ("manifest_part_a.json", "manifest_part_b.json", "manifest_part_c.json")

DESIGN_STEPS_DIR = os.path.normpath(
    os.path.join(TESTS_DIR, "..", "..", "design", "steps"))
REFRESHED_LIST_PATH = os.path.join(
    DESIGN_STEPS_DIR, "step-09-merged-test-list.md")
FC2_RULING_RECORD_PATH = os.path.join(
    DESIGN_STEPS_DIR, "step-13-content-retrace.md")


def refreshed_list_row_identifiers(test):
    if not os.path.exists(REFRESHED_LIST_PATH):
        test.fail("refreshed list missing: " + REFRESHED_LIST_PATH)
    with open(REFRESHED_LIST_PATH, "r", encoding="utf-8") as handle:
        text = handle.read()
    return re.findall(
        r"^####\s+([A-Z][A-Z0-9-]*-T[0-9][0-9])\b", text, re.MULTILINE)


def fc2_ruling_subsections(test):
    if not os.path.exists(FC2_RULING_RECORD_PATH):
        test.fail("F-C2 ruling record missing: " + FC2_RULING_RECORD_PATH)
    with open(FC2_RULING_RECORD_PATH, "r", encoding="utf-8") as handle:
        text = handle.read()
    return re.findall(
        r"^### 5\.[0-9]+ Subsection ([0-9]+\.[0-9]+)\b", text, re.MULTILINE)

AFFECTED_CLASSES = (
    "deduplication parameter or rule",
    "clustering parameter or rule",
    "normalisation parameter or rule",
    "filtering parameter or rule",
    "redaction parameter or rule",
    "truncation parameter or rule",
    "type mapping change",
    "new enum value absorbed by a default branch",
)


def load_manifest_parts(test):
    parts = []
    for name in MANIFEST_PARTS:
        path = os.path.join(TESTS_DIR, name)
        if not os.path.exists(path):
            test.fail("manifest part missing from the suite as written: " + name)
        with open(path, "r", encoding="utf-8") as handle:
            parts.append((name, json.load(handle)))
    return parts


def string_tokens(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str):
                out.add(key)
            string_tokens(value, out)
    elif isinstance(node, (list, tuple)):
        for item in node:
            string_tokens(item, out)
    elif isinstance(node, str):
        out.add(node)
    return out


def entry_keys(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str):
                out.add(key)
            entry_keys(value, out)
    elif isinstance(node, (list, tuple)):
        for item in node:
            entry_keys(item, out)
    return out


REDACT_T08_LIMB_PATTERN = re.compile(
    r"\b(quantity|quantities|amount|amounts|magnitude|units?|source class)\b")


def redact_t08_entry_subtrees(node, out):
    if isinstance(node, dict):
        mentioned = False
        for key, value in node.items():
            if isinstance(key, str) and "REDACT-T08" in key:
                mentioned = True
            if isinstance(value, str) and "REDACT-T08" in value:
                mentioned = True
        if mentioned:
            out.append(node)
        for value in node.values():
            redact_t08_entry_subtrees(value, out)
    elif isinstance(node, (list, tuple)):
        for item in node:
            redact_t08_entry_subtrees(item, out)
    return out


class MeaningCheckBase:
    """Shared assertions for the eight meaning checks, as a mixin.

    This class is not a test case on its own: each meaning check below
    inherits it together with unittest.TestCase.
    """

    MODULE = None
    SUITE_ID = None
    AFFECTED_CLASS = None
    FIXTURE = None

    def run_check(self, direction):
        mod = harness.require(self.MODULE)
        return mod.meaning_check(
            check_id=self.SUITE_ID,
            affected_class=self.AFFECTED_CLASS,
            fixture=self.FIXTURE,
            direction=direction,
        )

    def test_meaning_held_record_state(self):
        result = self.run_check("meaning held")
        self.assertEqual(result["outcome_records_before"], result["outcome_records_after"])
        entry = result["meaning_change_record_entry"]
        self.assertEqual(entry["classification"], "no meaning change shown")
        self.assertEqual(entry["affected_classes"], [self.AFFECTED_CLASS])
        self.assertEqual(entry["checks_run"], [self.SUITE_ID])
        self.assertTrue(entry["change_named"])
        self.assertTrue(entry["discharging_seat_named"])
        self.assertEqual(entry["home"], "suite result record")

    def test_meaning_changed_record_state(self):
        result = self.run_check("meaning changed")
        self.assertNotEqual(result["outcome_records_before"], result["outcome_records_after"])
        entry = result["meaning_change_record_entry"]
        self.assertEqual(entry["classification"], "meaning change under a stable shape")
        self.assertEqual(entry["affected_classes"], [self.AFFECTED_CLASS])
        self.assertEqual(entry["checks_run"], [self.SUITE_ID])
        self.assertTrue(entry["change_named"])
        self.assertTrue(entry["discharging_seat_named"])
        self.assertEqual(entry["home"], "suite result record")
        self.assertTrue(entry["result_of_each_check"])
        self.assertFalse(result["passed_as_no_change_in_any_report"])
        self.assertEqual(result["loop_report_form"], "classification by pointer only")


class SpanT01DeduplicationMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T01: deduplication parameter or rule, dataset path."""

    MODULE = "ontoloop.dataset"
    SUITE_ID = "SPAN-T01"
    AFFECTED_CLASS = "deduplication parameter or rule"
    FIXTURE = "grouped fixture store with exact duplicate runs at the dedup threshold"


class SpanT02ClusteringMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T02: clustering parameter or rule, dataset path."""

    MODULE = "ontoloop.dataset"
    SUITE_ID = "SPAN-T02"
    AFFECTED_CLASS = "clustering parameter or rule"
    FIXTURE = "grouped fixture store with near verbatim pairs at the cluster boundary"


class SpanT03NormalisationMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T03: normalisation parameter or rule, capture path."""

    MODULE = "ontoloop.capture"
    SUITE_ID = "SPAN-T03"
    AFFECTED_CLASS = "normalisation parameter or rule"
    FIXTURE = "Example A varied by normalisation sensitive field forms"


class SpanT04FilteringMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T04: filtering parameter or rule, dataset path."""

    MODULE = "ontoloop.dataset"
    SUITE_ID = "SPAN-T04"
    AFFECTED_CLASS = "filtering parameter or rule"
    FIXTURE = "grouped fixture store with runs at the eligibility filter boundary"


class SpanT05RedactionMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T05: redaction parameter or rule, capture path."""

    MODULE = "ontoloop.redact"
    SUITE_ID = "SPAN-T05"
    AFFECTED_CLASS = "redaction parameter or rule"
    FIXTURE = "labelled secret bearing shapes per family at the classification boundary"


class SpanT06TruncationMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T06: truncation parameter or rule, capture path."""

    MODULE = "ontoloop.capture"
    SUITE_ID = "SPAN-T06"
    AFFECTED_CLASS = "truncation parameter or rule"
    FIXTURE = "payloads at and over the capture caps of row CAPTURE-T05"


class SpanT07TypeMappingMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T07: type mapping change, capture and dataset paths."""

    MODULE = "core"
    SUITE_ID = "SPAN-T07"
    AFFECTED_CLASS = "type mapping change"
    FIXTURE = "Example A records whose field values sit at the type mapping boundary"


class SpanT08NewEnumMeaningTests(MeaningCheckBase, unittest.TestCase):
    """SPAN-T08: new enum value absorbed by a default branch, evaluation path."""

    MODULE = "ontoloop.eval"
    SUITE_ID = "SPAN-T08"
    AFFECTED_CLASS = "new enum value absorbed by a default branch"
    FIXTURE = "Example D cases carrying a value the default branch would absorb"


class MeaningCheckDefinitionTests(unittest.TestCase):
    """Every affected class stands defined in the suite as written."""

    def test_each_affected_class_has_exactly_one_defined_check(self):
        defined = {}
        for obj in list(globals().values()):
            if isinstance(obj, type) and issubclass(obj, MeaningCheckBase) and obj is not MeaningCheckBase:
                self.assertNotIn(obj.AFFECTED_CLASS, defined, obj.__name__)
                defined[obj.AFFECTED_CLASS] = obj
        self.assertEqual(sorted(defined), sorted(AFFECTED_CLASSES))

    def test_each_check_carries_identifier_fixture_and_pass_condition(self):
        for obj in list(globals().values()):
            if isinstance(obj, type) and issubclass(obj, MeaningCheckBase) and obj is not MeaningCheckBase:
                self.assertRegex(obj.SUITE_ID, r"^SPAN-T[0-9][0-9]$", obj.__name__)
                self.assertTrue(obj.FIXTURE, obj.__name__)
                self.assertTrue(obj.MODULE, obj.__name__)
                methods = [name for name in dir(obj) if name.startswith("test_")]
                self.assertIn("test_meaning_held_record_state", methods, obj.__name__)
                self.assertIn("test_meaning_changed_record_state", methods, obj.__name__)


class MeaningChangeRecordTests(unittest.TestCase):
    """The discharge route at plan subsection 19.101 points two to four."""

    def test_entry_names_change_classes_checks_results_classification_and_seat(self):
        mod = harness.require("ontoloop.golden_span")
        entry = mod.latest_meaning_change_entry()
        for field in ("change", "affected_classes", "checks_run",
                      "result_of_each_check", "classification", "discharging_seat"):
            self.assertIn(field, entry)
        self.assertIn(entry["classification"],
                      ("meaning change under a stable shape", "no meaning change shown"))
        self.assertTrue(entry["change"])
        self.assertTrue(entry["affected_classes"])
        self.assertTrue(entry["checks_run"])
        self.assertTrue(entry["discharging_seat"])
        results = entry["result_of_each_check"]
        self.assertEqual(len(results), len(entry["checks_run"]))
        if isinstance(results, dict):
            self.assertEqual(sorted(results), sorted(entry["checks_run"]))
            values = list(results.values())
        else:
            values = list(results)
        for value in values:
            self.assertTrue(value)

    def test_bar_stands_until_such_an_entry_stands(self):
        mod = harness.require("ontoloop.golden_span")
        state = mod.discharge_state(entry=None)
        self.assertFalse(state["discharged"])
        self.assertTrue(state["bar_stands"])
        self.assertFalse(state["change_passed_as_no_change"])

    def test_entry_covering_every_affected_class_discharges_the_bar(self):
        mod = harness.require("ontoloop.golden_span")
        checks = ["SPAN-T%02d" % number for number in range(1, 9)]
        entry = dict(mod.latest_meaning_change_entry())
        entry["affected_classes"] = list(AFFECTED_CLASSES)
        entry["checks_run"] = checks
        entry["result_of_each_check"] = {
            check: "meaning check result recorded" for check in checks}
        state = mod.discharge_state(
            entry=entry, affected_classes=list(AFFECTED_CLASSES))
        self.assertTrue(state["discharged"])
        self.assertFalse(state["bar_stands"])

    def test_entry_missing_an_affected_class_leaves_the_bar_standing(self):
        mod = harness.require("ontoloop.golden_span")
        checks = ["SPAN-T%02d" % number for number in range(1, 9)]
        entry = dict(mod.latest_meaning_change_entry())
        entry["affected_classes"] = list(AFFECTED_CLASSES[:-1])
        entry["checks_run"] = checks
        entry["result_of_each_check"] = {
            check: "meaning check result recorded" for check in checks}
        state = mod.discharge_state(
            entry=entry, affected_classes=list(AFFECTED_CLASSES))
        self.assertFalse(state["discharged"])
        self.assertTrue(state["bar_stands"])
        self.assertFalse(state["change_passed_as_no_change"])

    def test_loop_report_prints_the_classification_by_pointer_only(self):
        mod = harness.require("ontoloop.golden_span")
        entry = mod.latest_meaning_change_entry()
        printed = mod.loop_report_classification(entry)
        self.assertEqual(printed["form"], "pointer")
        self.assertEqual(printed["points_to"], entry["entry_identity"])
        self.assertNotEqual(printed.get("classification_text"), entry["classification"])


class CoverageRowsTests(unittest.TestCase):
    """Coverage: every row identifier appears in exactly one manifest part."""

    def test_there_are_129_row_identifiers_in_the_refreshed_list(self):
        identifiers = refreshed_list_row_identifiers(self)
        self.assertEqual(len(identifiers), 129)
        self.assertEqual(len(set(identifiers)), 129)

    def test_every_row_identifier_appears_in_exactly_one_manifest_part(self):
        identifiers = refreshed_list_row_identifiers(self)
        parts = load_manifest_parts(self)
        key_sets = [(name, entry_keys(data, set())) for name, data in parts]
        for identifier in identifiers:
            homes = [name for name, keys in key_sets if identifier in keys]
            self.assertEqual(len(homes), 1, identifier + " in parts: " + ", ".join(homes))

class CoverageUnrowedTests(unittest.TestCase):
    """Coverage: every F-C2 subsection appears in exactly one manifest part."""

    def test_every_fc2_subsection_appears_in_exactly_one_manifest_part(self):
        subsections = fc2_ruling_subsections(self)
        self.assertEqual(len(subsections), 12)
        self.assertEqual(len(set(subsections)), 12)
        parts = load_manifest_parts(self)
        key_sets = [(name, entry_keys(data, set())) for name, data in parts]
        for subsection in subsections:
            homes = [name for name, keys in key_sets if subsection in keys]
            self.assertEqual(len(homes), 1, subsection + " in parts: " + ", ".join(homes))


class CoverageRedactT08QuantityTests(unittest.TestCase):
    """Coverage: no manifest entry names the quantity limb of REDACT-T08."""

    def test_no_redact_t08_entry_names_a_quantity_limb(self):
        parts = load_manifest_parts(self)
        entries_found = 0
        for name, data in parts:
            for subtree in redact_t08_entry_subtrees(data, []):
                entries_found += 1
                for token in string_tokens(subtree, set()):
                    self.assertIsNone(
                        REDACT_T08_LIMB_PATTERN.search(token.lower()),
                        name + ": REDACT-T08 entry names a quantity limb: " + token)
        self.assertGreater(entries_found, 0)


if __name__ == "__main__":
    unittest.main()
