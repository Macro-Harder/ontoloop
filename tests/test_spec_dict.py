"""Slice SPEC-DICT, list section 2.1, plan section 6.5.

Data structures perspective: these tests pin the exact field sets,
field order, and value forms the rows state.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.dictionary, with function names taken from the behaviour
wording of each row. Fields a row does not state are not invented;
where a row names a registered set without listing its members in
the row (the four disposition words at DQ-SPEC-7, the seven and the
relation cross types), the test reads the registered set from the
product surface and checks exact use of that set, never a guessed
member list.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.dictionary"

# Example A field order, as plan section 3.4 states the parts of a
# captured review run, in the order the brief names them.
EXAMPLE_A_FIELD_ORDER = (
    "run identity",
    "workflow identity",
    "workflow definition version",
    "schema version",
    "task verbatim",
    "steps",
    "outcome record",
    "signal records",
)


class TestSpecDictT01(unittest.TestCase):
    """SPEC-DICT-T01: validator over the machine readable source."""

    def test_validator_passes_source_at_its_named_version(self):
        module = require(MODULE)
        source = module.dictionary_source()
        result = module.validate_dictionary_source(source)
        self.assertEqual(
            set(result.keys()), {"accepted", "version", "refused_fields"}
        )
        self.assertIs(result["accepted"], True)
        self.assertEqual(result["version"], source["version"])
        self.assertEqual(result["refused_fields"], [])

    def test_validator_refuses_source_with_an_unlisted_field(self):
        module = require(MODULE)
        source = module.dictionary_source()
        varied = dict(source)
        varied["fields"] = tuple(source["fields"]) + ("unlisted_field",)
        result = module.validate_dictionary_source(varied)
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["refused_fields"], ["unlisted_field"])


class TestSpecDictT02(unittest.TestCase):
    """SPEC-DICT-T02: field level audit against the EVAL minimum."""

    def test_every_field_traced_in_both_directions(self):
        module = require(MODULE)
        inventory = module.step7_inventory()
        rows = module.field_level_audit(inventory)
        fields = [entry["field"] for entry in inventory]
        expected = {
            (field, direction)
            for field in fields
            for direction in ("dictionary_to_minimum", "minimum_to_dictionary")
        }
        traced = {(row["field"], row["direction"]) for row in rows}
        self.assertEqual(traced, expected)
        for row in rows:
            self.assertEqual(
                set(row.keys()), {"field", "direction", "disposition"}
            )

    def test_only_the_four_disposition_words_at_dq_spec_7(self):
        module = require(MODULE)
        registered = module.dq_spec_7_dispositions()
        self.assertEqual(len(registered), 4)
        rows = module.field_level_audit(module.step7_inventory())
        used = {row["disposition"] for row in rows}
        self.assertEqual(used - set(registered), set())
        self.assertTrue(used)

    def test_eval_minimum_is_materialised_as_the_trace_target(self):
        module = require(MODULE)
        minimum = module.eval_minimum()
        self.assertTrue(minimum)
        minimum_fields = {entry["field"] for entry in minimum}
        inventory_fields = {
            entry["field"] for entry in module.step7_inventory()
        }
        self.assertEqual(minimum_fields, inventory_fields)
        rows = module.field_level_audit(module.step7_inventory())
        for row in rows:
            self.assertIn(row["field"], minimum_fields)

    def test_missing_or_contradicted_row_blocks_closure(self):
        module = require(MODULE)
        rows = module.field_level_audit(module.step7_inventory())
        contradicted = [dict(row) for row in rows]
        target = next(
            row for row in contradicted
            if row["disposition"] != "contradicted"
        )
        target["disposition"] = "contradicted"
        result = module.audit_closure(contradicted)
        self.assertIs(result["closed"], False)
        self.assertTrue(
            any(
                entry == target["field"]
                or (
                    isinstance(entry, dict)
                    and entry.get("field") == target["field"]
                )
                for entry in result["blocking_rows"]
            )
        )
        missing = [dict(row) for row in rows]
        removed = missing.pop(1)
        result_missing = module.audit_closure(missing)
        self.assertIs(result_missing["closed"], False)
        self.assertTrue(
            any(
                entry == removed["field"]
                or (
                    isinstance(entry, dict)
                    and entry.get("field") == removed["field"]
                )
                for entry in result_missing["blocking_rows"]
            )
        )


class TestSpecDictT03(unittest.TestCase):
    """SPEC-DICT-T03: re performance list, stage record evidence."""

    def test_reperformance_list_exists_and_is_signed(self):
        stage_carried(
            "SPEC-DICT-T03 evidence home is stage record evidence: the "
            "re performance list and its signing by the audit performer "
            "seat are stage acts, not fixture results. Owning stage: "
            "the SPEC-DICT specification slice exit. Closing record: "
            "the stage record of the re performance list signing by "
            "the audit performer seat at that slice exit."
        )

    def test_no_trace_row_cites_the_list_before_that_signing(self):
        stage_carried(
            "SPEC-DICT-T03 evidence home is stage record evidence: "
            "citation order against the signing is read from the stage "
            "record, not from a fixture. Owning stage: the SPEC-DICT "
            "specification slice exit. Closing record: the stage "
            "record of the re performance list signing by the audit "
            "performer seat, against which citation order is read."
        )


class TestSpecDictT04(unittest.TestCase):
    """SPEC-DICT-T04: example code shapes against the dictionary."""

    def test_example_a_field_set_shape(self):
        # Suite fixture shape only; no product surface is touched.
        self.assertEqual(len(EXAMPLE_A_FIELD_ORDER), 8)
        self.assertEqual(len(set(EXAMPLE_A_FIELD_ORDER)), 8)
        self.assertEqual(EXAMPLE_A_FIELD_ORDER[0], "run identity")
        self.assertEqual(EXAMPLE_A_FIELD_ORDER[-1], "signal records")

    def test_field_in_example_shapes_not_in_dictionary_fails(self):
        module = require(MODULE)
        shapes = module.example_code_shapes()
        self.assertTrue(shapes)
        source = module.dictionary_source()
        dictionary_fields = set(source["fields"])
        shape_fields = set()
        for shape in shapes:
            shape_fields.update(shape["fields"])
        self.assertTrue(shape_fields)
        outside = shape_fields - dictionary_fields
        self.assertTrue(outside)
        result = module.dictionary_check(tuple(shape_fields))
        self.assertIs(result["accepted"], False)
        self.assertEqual(set(result["refused_fields"]), outside)


class TestSpecDictT05(unittest.TestCase):
    """SPEC-DICT-T05: relation catalogue and never reuse register."""

    def test_relation_rows_state_tombstone_and_supersession(self):
        module = require(MODULE)
        rows = module.relation_catalogue()
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(
                set(row.keys()),
                {
                    "cross_type_reference",
                    "tombstone_behaviour",
                    "supersession_behaviour",
                },
            )
            self.assertTrue(row["tombstone_behaviour"])
            self.assertTrue(row["supersession_behaviour"])
            self.assertIn("tombstone", row["tombstone_behaviour"])
            self.assertIn("supersession", row["supersession_behaviour"])
        stated = {row["cross_type_reference"] for row in rows}
        self.assertEqual(stated, set(module.registered_cross_types()))

    def test_never_reuse_register_refuses_a_retired_name(self):
        module = require(MODULE)
        retired = module.retired_names()[0]
        result = module.register_name(retired)
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["name"], retired)


if __name__ == "__main__":
    unittest.main()
