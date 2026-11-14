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
        catalogue = module.error_catalogue()
        self.assertTrue(catalogue)
        agent_rows = []
        owing_by_name = {}
        for name, catalogue_row in catalogue.items():
            result = module.check_owing_forms(dict(catalogue_row))
            self.assertIn("owing_statement", result, name)
            owing = result["owing_statement"]
            self.assertIsNotNone(owing, name)
            self.assertEqual(owing.get("name"), name, name)
            self.assertIn(
                owing.get("named_reader"), ("agent", "operator"), name
            )
            owing_by_name[name] = owing
            if owing.get("named_reader") == "agent":
                agent_rows.append(name)
        self.assertEqual(set(owing_by_name), set(catalogue))
        self.assertTrue(agent_rows)
        for name in agent_rows:
            owing = owing_by_name[name]
            self.assertTrue(owing.get("agentic_form"), name)
            self.assertIs(
                module.check_owing_forms(dict(owing))["passed"],
                True,
                name,
            )
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


class TestCoreMeaningCheckFixR1(unittest.TestCase):
    """Fix round 1: meaning_check for the type mapping class.

    Written test first for the COR cure of S15-R1-005 and
    S15-R1-072: the SpanT07 pair's surface, built on
    ontoloop.core in the form MeaningCheckBase pins, ahead
    of the spanning joining extension recorded at this act.
    """

    def _run(self, module, direction):
        return module.meaning_check(
            check_id="SPAN-T07",
            affected_class="type mapping change",
            fixture=(
                "Example A records whose field values sit at "
                "the type mapping boundary"
            ),
            direction=direction,
        )

    def test_meaning_held_record_state(self):
        module = require(MODULE)
        result = self._run(module, "meaning held")
        self.assertEqual(
            result["outcome_records_before"],
            result["outcome_records_after"],
        )
        entry = result["meaning_change_record_entry"]
        self.assertEqual(
            entry["classification"], "no meaning change shown"
        )
        self.assertEqual(entry["affected_classes"], ["type mapping change"])
        self.assertEqual(entry["checks_run"], ["SPAN-T07"])
        self.assertTrue(entry["change_named"])
        self.assertTrue(entry["discharging_seat_named"])
        self.assertEqual(entry["home"], "suite result record")

    def test_meaning_changed_record_state(self):
        module = require(MODULE)
        result = self._run(module, "meaning changed")
        self.assertNotEqual(
            result["outcome_records_before"],
            result["outcome_records_after"],
        )
        entry = result["meaning_change_record_entry"]
        self.assertEqual(
            entry["classification"],
            "meaning change under a stable shape",
        )
        self.assertTrue(entry["result_of_each_check"])
        self.assertFalse(result["passed_as_no_change_in_any_report"])
        self.assertEqual(
            result["loop_report_form"], "classification by pointer only"
        )


class TestCoreFixR5(unittest.TestCase):
    """Fix round 5, Region 3: core surfaces, rulings 38, 44 to 47.

    Written test first for N-01, N-07, N-08, N-09, and N-10.
    Each pin states the governed form its ruling charges,
    beside the standing forms the cure preserves.
    """

    def _record_with_version(self, module, version):
        record = module.golden_record()
        record["schema_version"] = version
        return record

    # Act 1, ruling 38, N-01: the version stands checked as a
    # version of the window in substance.
    def test_fractional_versions_return_the_governed_refusal(self):
        module = require(MODULE)
        below = module.error_catalogue()[
            "version below reader window"]["error"]
        for version in (2.5, 1.5, 2.999):
            result = module.check_record(
                self._record_with_version(module, version))
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], below, repr(version))

    def test_fractional_version_above_reader_returns_newer_refusal(self):
        module = require(MODULE)
        newer = module.error_catalogue()[
            "version newer than reader"]["error"]
        result = module.check_record(
            self._record_with_version(module, 3.5))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], newer)

    def test_nan_and_true_return_the_governed_refusal(self):
        module = require(MODULE)
        below = module.error_catalogue()[
            "version below reader window"]["error"]
        for version in (float("nan"), True):
            result = module.check_record(
                self._record_with_version(module, version))
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], below, repr(version))

    def test_non_numeric_versions_return_the_governed_refusal(self):
        module = require(MODULE)
        below = module.error_catalogue()[
            "version below reader window"]["error"]
        forms = (
            "3", "abc", None, [1], {"a": 1}, (1,), 1j,
        )
        for version in forms:
            result = module.check_record(
                self._record_with_version(module, version))
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], below, repr(version))

    def test_standing_integer_versions_still_decide_as_pinned(self):
        module = require(MODULE)
        below = module.error_catalogue()[
            "version below reader window"]["error"]
        newer = module.error_catalogue()[
            "version newer than reader"]["error"]
        for version in (1, 2, 3):
            result = module.check_record(
                self._record_with_version(module, version))
            self.assertIs(result["accepted"], True, repr(version))
        for version in (0, -1):
            result = module.check_record(
                self._record_with_version(module, version))
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], below, repr(version))
        result = module.check_record(
            self._record_with_version(module, 4))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], newer)

    # Act 2, ruling 44, N-07: the scan matches the module
    # qualified hash call.
    def test_builtins_hash_call_recorded_at_its_true_line(self):
        module = require(MODULE)
        source = "import builtins\nvalue = builtins.hash(item)\n"
        scan = module.determinism_source_scan(source)
        self.assertEqual(
            scan["builtin_hash_uses_for_grouping_ordering_assignment"],
            ["builtin hash function used at line 2"],
        )

    def test_standing_hash_call_forms_still_recorded(self):
        module = require(MODULE)
        direct = module.determinism_source_scan("value = hash(item)\n")
        self.assertEqual(
            direct["builtin_hash_uses_for_grouping_ordering_assignment"],
            ["builtin hash function used at line 1"],
        )
        imported = module.determinism_source_scan(
            "from builtins import hash\nvalue = hash(item)\n")
        self.assertEqual(
            imported["builtin_hash_uses_for_grouping_ordering_assignment"],
            ["builtin hash function used at line 2"],
        )

    def test_module_own_source_still_returns_its_standing_result(self):
        module = require(MODULE)
        scan = module.determinism_source_scan()
        self.assertEqual(
            scan["builtin_hash_uses_for_grouping_ordering_assignment"], [])
        self.assertEqual(scan["set_iteration_order_constructions"], [])
        self.assertTrue(scan["whole_core_source_scanned"])

    # Act 3, ruling 45, N-08: the core canonical surfaces meet
    # deep finite nesting in a governed form.
    def _deep_mapping(self, depth):
        value = {"leaf": "x"}
        for _ in range(depth):
            value = {"a": value}
        return value

    def test_canonical_encoding_deep_nesting_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.canonical_encoding(self._deep_mapping(1500))
        self.assertIn("too deeply nested", str(caught.exception))

    def test_hash_record_deep_nesting_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.hash_record(self._deep_mapping(1500))
        self.assertIn("too deeply nested", str(caught.exception))

    def test_deep_nesting_at_standing_depth_still_encodes(self):
        module = require(MODULE)
        record = self._deep_mapping(800)
        encoded = module.canonical_encoding(record)
        self.assertIsInstance(encoded, bytes)
        self.assertTrue(encoded)
        digest = module.hash_record(record)
        self.assertIsInstance(digest, bytes)
        self.assertEqual(len(digest), 32)

    # Act 4, ruling 46, N-09: meaning_check meets an unhashable
    # check identifier in one governed form in both directions.
    def test_unhashable_check_id_returns_held_form_in_both_directions(self):
        module = require(MODULE)
        held = module.meaning_check(
            check_id=["SPAN-X"],
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning held",
        )
        changed = module.meaning_check(
            check_id=["SPAN-X"],
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning changed",
        )
        self.assertEqual(changed, held)
        entry = held["meaning_change_record_entry"]
        self.assertEqual(
            entry["classification"], "no meaning change shown")
        self.assertEqual(entry["checks_run"], [["SPAN-X"]])
        self.assertEqual(
            held["outcome_records_before"],
            held["outcome_records_after"],
        )

    def test_standing_identifier_forms_still_decide_as_pinned(self):
        module = require(MODULE)
        held = module.meaning_check(
            check_id="SPAN-T07",
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning held",
        )
        self.assertEqual(
            held["meaning_change_record_entry"]["classification"],
            "no meaning change shown",
        )
        changed = module.meaning_check(
            check_id="SPAN-T07",
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning changed",
        )
        entry = changed["meaning_change_record_entry"]
        self.assertEqual(
            entry["classification"],
            "meaning change under a stable shape",
        )
        self.assertEqual(
            entry["result_of_each_check"],
            {"SPAN-T07": "meaning check result recorded"},
        )

    # Act 5, ruling 47, N-10: dispose_determinism_failure fails
    # closed on a non mapping failure value.
    def test_non_mapping_failure_values_return_the_undisposed_form(self):
        module = require(MODULE)
        for value in (None, 5, (1, 2), "failure"):
            result = module.dispose_determinism_failure(value)
            self.assertEqual(result, {"disposed": False}, repr(value))

    def test_standing_failure_mapping_still_disposes_as_pinned(self):
        module = require(MODULE)
        failure = {
            "row_failed": True,
            "recorded_limb": "source",
            "recorded_computation": "seeded computation",
            "disposed": False,
        }
        disposed = module.dispose_determinism_failure(failure)
        self.assertIs(disposed["disposed"], True)
        self.assertIs(failure["disposed"], False)
        self.assertTrue(
            module.core_exit_passes(
                undisposed_failure=None, disposed=[disposed]))


class TestCoreFixR6(unittest.TestCase):
    """Fix round 6, Region 3: core scalar lookups, rulings 91 to 93.

    Written test first for R6-CORE-1, R6-CAT-1, and R6-CAT-2.
    Each pin states the governed form its ruling charges,
    beside the standing forms the cure preserves.
    """

    # Ruling 91: state_transition meets an unhashable state or
    # act value in its stated KeyError form.
    def test_state_transition_unhashable_state_raises_key_error(self):
        module = require(MODULE)
        with self.assertRaises(KeyError):
            module.state_transition(
                ["Provisional, first period"], "confirmation")

    def test_state_transition_unhashable_act_raises_key_error(self):
        module = require(MODULE)
        with self.assertRaises(KeyError):
            module.state_transition(
                "Provisional, first period", ["confirmation"])

    def test_state_transition_unhashable_mapping_raises_key_error(self):
        module = require(MODULE)
        with self.assertRaises(KeyError):
            module.state_transition(
                {"state": 1}, "confirmation")

    def test_state_transition_standing_forms_still_decide(self):
        module = require(MODULE)
        self.assertEqual(
            module.state_transition(
                "Provisional, first period", "confirmation"),
            "Confirmed",
        )
        with self.assertRaises(KeyError):
            module.state_transition("X", "confirmation")

    # Ruling 92: check_owing_forms returns its governed failure
    # form on a row in no mapping form, on an unhashable name,
    # and on a named row carrying a malformed form value.
    def _assert_governed_failure(self, result):
        self.assertIs(result["passed"], False)
        self.assertEqual(result["defect_home"], "catalogue")
        self.assertIsNone(result["owing_statement"])

    def test_check_owing_forms_non_mapping_rows_return_failure(self):
        module = require(MODULE)
        for row in (None, "sync failure", ["sync failure"], 5):
            result = module.check_owing_forms(row)
            self._assert_governed_failure(result)
            self.assertEqual(result["defects"], [], repr(row))

    def test_check_owing_forms_unhashable_name_returns_failure(self):
        module = require(MODULE)
        result = module.check_owing_forms({"name": ["sync failure"]})
        self._assert_governed_failure(result)
        self.assertEqual(result["defects"], [])

    def test_check_owing_forms_malformed_form_value_returns_failure(self):
        module = require(MODULE)
        catalogue_row = module.error_catalogue()["sync failure"]
        statement = module.check_owing_forms(
            catalogue_row)["owing_statement"]
        named = dict(statement)
        named["simple_form"] = "a plain string, not a form mapping"
        result = module.check_owing_forms(named)
        self.assertIs(result["passed"], False)
        self.assertEqual(result["defects"], ["sync failure"])
        self.assertIsNotNone(result["owing_statement"])

    def test_check_owing_forms_standing_rows_still_pass(self):
        module = require(MODULE)
        for name, row in module.error_catalogue().items():
            result = module.check_owing_forms(dict(row))
            self.assertIs(result["passed"], True, name)
        empty = module.check_owing_forms({})
        self.assertIs(empty["passed"], False)
        unknown = module.check_owing_forms({"name": "no such row"})
        self.assertIs(unknown["passed"], False)

    # Ruling 93: catalogue_row_with_value returns its governed
    # form, None, on an unhashable kind argument.
    def test_catalogue_row_with_value_unhashable_kind_returns_none(self):
        module = require(MODULE)
        for kind in (["figure"], {"figure": 1}):
            result = module.catalogue_row_with_value(
                kind, "advanced_form")
            self.assertIsNone(result, repr(kind))

    def test_catalogue_row_with_value_standing_kinds_still_return(self):
        module = require(MODULE)
        row = module.catalogue_row_with_value("figure", "advanced_form")
        self.assertIsNotNone(row)
        self.assertIn("name", row)
        self.assertIsNone(
            module.catalogue_row_with_value("no such kind", "advanced_form"))
        self.assertIsNone(
            module.catalogue_row_with_value("figure", "no such form"))


if __name__ == "__main__":
    unittest.main()
