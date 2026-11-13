"""Slice CORE, list section 2.6, plan section 6.5 and 13.3.

Data structures perspective: these tests pin the exact ten
ontology types, the closed record kind lists, the closed schema
refusal forms, the exact field set of an error catalogue row, and
the owed reading forms per catalogue row under CORE-T06.

Transcription decision: the rows state no product API names and,
for most refusals, no literal error strings beyond the words
named error. The suite names the product surface for this slice
as the module ontoloop.core, and reads each named error from the
product error catalogue rather than inventing its string, then
checks that the refusal carries exactly that catalogue error and
no other.
"""

import inspect
import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.core"

# The ten ontology types, plan section 3.1, item 2.
ONTOLOGY_TYPES = (
    "Workflow",
    "Run",
    "Step",
    "Outcome",
    "Signal",
    "Dataset",
    "Candidate",
    "Evaluation",
    "Artifact",
    "PromotionEvent",
)

# Closed store audit and journal machinery kinds named beside the
# ten types at plan section 3.1, item 2.
CLOSED_AUDIT_KINDS = (
    "access record",
    "tombstone record",
    "purge checkpoint record",
    "genesis record",
)


class TestCoreT01(unittest.TestCase):
    """CORE-T01: an unlisted record type is refused and counted."""

    def test_ontology_type_set_shape(self):
        # Suite fixture shape only; no product surface is touched.
        self.assertEqual(len(ONTOLOGY_TYPES), 10)
        self.assertNotIn("UnlistedKind", ONTOLOGY_TYPES)
        for kind in CLOSED_AUDIT_KINDS:
            self.assertNotIn(kind, ONTOLOGY_TYPES)

    def test_unlisted_record_type_refused_with_the_named_error(self):
        module = require(MODULE)
        record = module.example_a_record()
        record["record_type"] = "UnlistedKind"
        result = module.append_record(record)
        catalogue = module.error_catalogue()
        named = catalogue["unlisted record type"]["error"]
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], named)

    def test_refusal_counted_in_intake_refusal_counts_by_reason(self):
        module = require(MODULE)
        record = module.example_a_record()
        record["record_type"] = "UnlistedKind"
        before = module.intake_refusal_counts()
        module.append_record(record)
        after = module.intake_refusal_counts()
        reason = module.refusal_reason("unlisted record type")
        self.assertTrue(reason)
        self.assertEqual(after[reason], before.get(reason, 0) + 1)
        self.assertEqual(set(after.keys()) - set(before.keys()), set())


class TestCoreT02(unittest.TestCase):
    """CORE-T02: closed schema checking, three refusal limbs."""

    def test_unknown_field_refused_with_its_named_error(self):
        module = require(MODULE)
        record = module.golden_record()
        record["unknown_field"] = "value"
        result = module.check_record(record)
        named = module.error_catalogue()["unknown field"]["error"]
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], named)
        self.assertEqual(result["field"], "unknown_field")

    def test_version_newer_than_the_reader_refused(self):
        module = require(MODULE)
        record = module.golden_record()
        record["schema_version"] = module.reader_version() + 1
        result = module.check_record(record)
        named = module.error_catalogue()["version newer than reader"]["error"]
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], named)

    def test_version_below_the_reader_window_refused(self):
        module = require(MODULE)
        record = module.golden_record()
        window = module.reader_window()
        record["schema_version"] = window[0] - 1
        result = module.check_record(record)
        named = module.error_catalogue()["version below reader window"]["error"]
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], named)
        self.assertNotEqual(
            named, module.error_catalogue()["version newer than reader"]["error"]
        )


class TestCoreT03(unittest.TestCase):
    """CORE-T03: signature formation failure, ungrouped state."""

    def test_failure_produces_the_named_ungrouped_state(self):
        module = require(MODULE)
        run = module.run_missing_required_structured_field()
        result = module.form_signature(run)
        self.assertEqual(module.UNGROUPED_STATE, "ungrouped")
        self.assertEqual(result["state"], "ungrouped")
        self.assertEqual(result["state"], module.UNGROUPED_STATE)
        self.assertEqual(result["signature"], None)
        self.assertEqual(result["group_key"], None)

    def test_ungrouped_state_is_neither_error_nor_silent_pass(self):
        module = require(MODULE)
        run = module.run_missing_required_structured_field()
        result = module.form_signature(run)
        self.assertEqual(result["classification"], "ungrouped state")
        self.assertNotIn("error", result)
        self.assertIs(result["recorded"], True)
        self.assertIs(result["dataset_member"], False)


class TestCoreT04(unittest.TestCase):
    """CORE-T04: error catalogue completeness for this slice."""

    def test_every_catalogue_row_carries_the_four_stated_parts(self):
        module = require(MODULE)
        catalogue = module.error_catalogue()
        self.assertTrue(catalogue)
        for name, row in catalogue.items():
            self.assertEqual(
                set(row.keys()),
                {
                    "error",
                    "raising_module",
                    "state_change",
                    "record_home",
                    "simple_form",
                },
                name,
            )
            self.assertTrue(row["error"], name)
            self.assertTrue(row["raising_module"], name)
            self.assertTrue(row["state_change"], name)
            self.assertTrue(row["record_home"], name)
            self.assertTrue(row["simple_form"], name)

    def test_catalogue_covers_the_rows_section_4_4_names_for_core(self):
        module = require(MODULE)
        catalogue = module.error_catalogue()
        for named in module.section_4_4_core_rows():
            self.assertIn(named, catalogue)


class TestCoreT05(unittest.TestCase):
    """CORE-T05: pure core functions over Examples A and D."""

    def test_pure_functions_compute_from_given_inputs(self):
        module = require(MODULE)
        record = module.example_a_record()
        encoded = module.canonical_encoding(record)
        self.assertIsInstance(encoded, bytes)
        digest = module.hash_record(record)
        self.assertIsInstance(digest, bytes)
        self.assertEqual(len(digest), 32)
        self.assertIs(module.verify_record(record, digest), True)
        case = module.example_d_inputs()
        moved = module.state_transition(case["state"], case["act"])
        self.assertEqual(moved, case["expected_state"])
        self.assertEqual(module.canonical_encoding(record), encoded)

    def test_pure_functions_take_given_inputs_only(self):
        module = require(MODULE)
        expected = {
            "canonical_encoding": ["record"],
            "hash_record": ["record"],
            "verify_record": ["record", "digest"],
            "state_transition": ["state", "act"],
        }
        for name, params in expected.items():
            function = getattr(module, name)
            self.assertEqual(
                list(inspect.signature(function).parameters), params, name
            )

    def test_pure_functions_have_no_clock_disk_network_or_surface_access(self):
        module = require(MODULE)
        banned = (
            "datetime",
            "time.time",
            "time.monotonic",
            "open(",
            "socket",
            "urllib",
            "requests.",
            "os.environ",
            "random",
        )
        for name in (
            "canonical_encoding",
            "hash_record",
            "verify_record",
            "state_transition",
        ):
            source = inspect.getsource(getattr(module, name))
            for token in banned:
                self.assertNotIn(token, source, name + ": " + token)


class TestCoreT06(unittest.TestCase):
    """CORE-T06, Amendment 1 row: owing forms per catalogue row."""

    def test_simple_form_owed_on_every_catalogue_row(self):
        module = require(MODULE)
        for name, row in module.error_catalogue().items():
            self.assertTrue(row["simple_form"], name)

    def test_agentic_form_owed_where_the_named_reader_is_an_agent(self):
        module = require(MODULE)
        defects = module.owing_form_defects()
        agent_rows = [
            name
            for name, row in module.error_catalogue().items()
            if row.get("named_reader") == "agent"
        ]
        self.assertTrue(agent_rows)
        for name in agent_rows:
            row = module.error_catalogue()[name]
            self.assertTrue(row.get("agentic_form"), name)
            self.assertNotIn(name, defects)

    def test_advanced_form_owed_where_wording_states_a_figure_bound_or_reason(self):
        module = require(MODULE)
        for name, row in module.error_catalogue().items():
            wording = str(row.get("error", "")) + " " + str(
                row.get("simple_form", "")
            )
            states_value = (
                any(char.isdigit() for char in wording)
                or "bound" in wording
                or "refusal" in wording
            )
            if states_value:
                self.assertTrue(row.get("advanced_form"), name)

    def test_row_missing_an_owed_form_is_a_defect_in_the_catalogue(self):
        module = require(MODULE)
        catalogue = module.error_catalogue()
        name = next(iter(catalogue))
        broken = dict(catalogue[name])
        broken["simple_form"] = None
        result = module.check_owing_forms(broken)
        self.assertIs(result["passed"], False)
        self.assertEqual(result["defect_home"], "catalogue")
        self.assertIn(name, result["defects"])

    def test_owed_form_with_a_different_value_fails_the_owing_row(self):
        module = require(MODULE)
        for form in ("simple_form", "advanced_form", "agentic_form"):
            for kind in ("figure", "bound", "refusal_reason"):
                row = module.catalogue_row_with_value(kind, form)
                varied = dict(row)
                varied[form] = dict(row[form])
                original = row[form][kind]
                if isinstance(original, int):
                    varied[form][kind] = original + 1
                else:
                    varied[form][kind] = str(original) + " altered"
                result = module.check_owing_forms(varied)
                self.assertIs(result["passed"], False, form + ": " + kind)
                self.assertEqual(result["defect_home"], "catalogue")
                self.assertEqual(result["check_point"], "section 13.3")
                self.assertTrue(result["defects"])
                self.assertIn(row["name"], result["defects"])

    def test_printed_claim_inside_an_artifact_is_governed_by_its_owing_row(self):
        module = require(MODULE)
        claims = module.printed_claims()
        self.assertTrue(claims)
        homes = {claim["printed_home"] for claim in claims}
        self.assertIn("artifact", homes)
        self.assertIn("loop report", homes)
        for claim in claims:
            self.assertEqual(claim["governing_row"], claim["owing_row"])
            self.assertIs(claim["substitute_for_owing_row"], False)


if __name__ == "__main__":
    unittest.main()
