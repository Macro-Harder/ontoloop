"""Slice SPEC-CANON, list section 2.2, plan section 6.5.

Data structures perspective: these tests pin byte identity, the
exact set of hashed kinds, and the exact property set of the
conformance vectors.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.canonical. The unnumbered failure pair stated in the
SPEC-CANON slice paragraph (a floating point value in a hashed
object is refused) is written as a method of the SPEC-CANON-T04
case, the last row of the slice, and invents no identifier for it.
"""

import unittest

from tests.harness import require, stage_carried

MODULE = "ontoloop.canonical"

# The three hashed kinds, plan section 4.1, item 1: the domain
# separation rule carries three kind tags.
HASHED_KINDS = ("journal record", "manifest", "bundle")


class TestSpecCanonT01(unittest.TestCase):
    """SPEC-CANON-T01: byte identical canonical form per kind."""

    def test_hashed_kind_set_shape(self):
        # Suite fixture shape only; no product surface is touched.
        self.assertEqual(
            HASHED_KINDS, ("journal record", "manifest", "bundle")
        )

    def _assert_byte_identical(self, kind):
        module = require(MODULE)
        golden = module.golden_byte_examples()
        self.assertEqual(set(golden.keys()), set(HASHED_KINDS))
        record = module.golden_record(kind)
        produced = module.canonical_form(record, kind)
        self.assertIsInstance(produced, bytes)
        self.assertEqual(produced, golden[kind])

    def test_journal_record_byte_identical(self):
        self._assert_byte_identical("journal record")

    def test_manifest_byte_identical(self):
        self._assert_byte_identical("manifest")

    def test_bundle_byte_identical(self):
        self._assert_byte_identical("bundle")

    def test_reader_from_specification_alone_matches_each_kind(self):
        module = require(MODULE)
        golden = module.golden_byte_examples()
        for kind in HASHED_KINDS:
            record = module.golden_record(kind)
            from_specification = module.canonical_form_from_specification(
                record, kind
            )
            self.assertIsInstance(from_specification, bytes)
            self.assertEqual(from_specification, golden[kind])
            self.assertEqual(
                from_specification, module.canonical_form(record, kind)
            )


class TestSpecCanonT02(unittest.TestCase):
    """SPEC-CANON-T02: conformance vectors over four properties."""

    def _assert_property_vectors_pass(self, prop):
        module = require(MODULE)
        vectors = module.conformance_vectors(prop)
        self.assertTrue(vectors)
        for vector in vectors:
            self.assertEqual(
                set(vector.keys()), {"name", "input", "expected"}
            )
            self.assertIs(module.check_vector(vector), True)

    def test_field_order_vectors_pass(self):
        self._assert_property_vectors_pass("field order")

    def test_item_order_vectors_pass(self):
        self._assert_property_vectors_pass("item order")

    def test_line_framing_vectors_pass(self):
        self._assert_property_vectors_pass("line framing")

    def test_encoding_vectors_pass(self):
        self._assert_property_vectors_pass("encoding")


class TestSpecCanonT03(unittest.TestCase):
    """SPEC-CANON-T03: golden byte change, stage record evidence."""

    def test_change_recorded_as_a_specification_change(self):
        stage_carried(
            "SPEC-CANON-T03 evidence home is stage record evidence: "
            "recording a golden byte change as a specification change "
            "is a stage act, not a fixture result. Owning stage: the "
            "SPEC-CANON specification slice exit. Closing record: the "
            "stage record recording the golden byte change as a "
            "specification change at that slice exit."
        )

    def test_change_moves_the_canonical_form_version(self):
        stage_carried(
            "SPEC-CANON-T03 evidence home is stage record evidence: "
            "the canonical form version move is read from the stage "
            "record for the specification change. Owning stage: the "
            "SPEC-CANON specification slice exit. Closing record: "
            "the stage record of the specification change that moves "
            "the canonical form version at that slice exit."
        )


class TestSpecCanonT04(unittest.TestCase):
    """SPEC-CANON-T04: divergence check over the worked cases."""

    def test_two_independent_readings_agree_or_record_a_finding(self):
        module = require(MODULE)
        cases = module.worked_cases()
        self.assertTrue(cases)
        families = {case["family"] for case in cases}
        for family in families:
            kinds = {case["kind"] for case in cases
                     if case["family"] == family}
            self.assertEqual(
                kinds, {"positive", "negative", "boundary"}
            )
        first = module.reading(cases, reader="first")
        second = module.reading(cases, reader="second")
        case_ids = {case["case"] for case in cases}
        self.assertEqual(set(first.keys()), case_ids)
        self.assertEqual(set(second.keys()), case_ids)
        expected_divergent = {
            case_id for case_id in case_ids
            if first[case_id] != second[case_id]
        }
        result = module.divergence_check(cases)
        self.assertEqual(
            {item["case"] for item in result["divergences"]},
            expected_divergent,
        )
        self.assertEqual(
            {finding["case"] for finding in result["plan_findings"]},
            expected_divergent,
        )

    def test_failure_pair_floating_point_value_refused(self):
        module = require(MODULE)
        registrations = module.sealing_registrations()
        self.assertEqual(set(registrations.keys()), set(HASHED_KINDS))
        for kind in HASHED_KINDS:
            record = dict(registrations[kind])
            record["value"] = 1.5
            refused = False
            try:
                produced = module.canonical_form(record, kind)
            except Exception as exc:
                if "NOT BUILT" in str(exc):
                    raise
                refused = True
            else:
                refused = not isinstance(produced, bytes)
            self.assertTrue(refused, kind)


class TestSpecCanonFixR4(unittest.TestCase):
    """Fix round 4, ruling 26: canonical cycle detection.

    Written test first for N-08. The canonical encoding
    act detects a cycle on its encoding path and raises
    its governed ValueError form, instead of
    RecursionError, beside the standing acyclic cases,
    including deep finite nesting and shared acyclic
    content still encoding byte identically.
    """

    def test_self_referential_list_raises_value_error(self):
        module = require(MODULE)
        material = []
        material.append(material)
        with self.assertRaises(ValueError):
            module.encode_canonical(material, "journal record")

    def test_self_referential_mapping_raises_value_error(self):
        module = require(MODULE)
        material = {}
        material["self"] = material
        with self.assertRaises(ValueError):
            module.encode_canonical(material, "journal record")

    def test_cycle_through_a_tuple_raises_value_error(self):
        module = require(MODULE)
        material = []
        material.append((material,))
        with self.assertRaises(ValueError):
            module.encode_canonical(material, "journal record")

    def test_encode_value_cycle_raises_value_error(self):
        module = require(MODULE)
        material = []
        material.append(material)
        with self.assertRaises(ValueError):
            module.encode_value(material)

    def test_hash_canonical_cycle_raises_value_error(self):
        module = require(MODULE)
        material = {}
        material["self"] = material
        with self.assertRaises(ValueError):
            module.hash_canonical(material, "journal record")

    def test_acyclic_encodings_byte_identical(self):
        module = require(MODULE)
        record = module.golden_record("journal record")
        self.assertEqual(
            module.encode_canonical(record, "journal record"),
            module.golden_byte_examples()["journal record"],
        )
        value = {"b": [1, "x", True, None], "a": {"nested": [2, 3]}}
        self.assertEqual(
            module.encode_value(value),
            b"{1:a:{6:nested:[2,3]},1:b:[1,1:x,true,null]}",
        )

    def test_deep_finite_nesting_still_encodes(self):
        module = require(MODULE)
        material = "x"
        for _ in range(120):
            material = [material]
        produced = module.encode_canonical(material, "journal record")
        self.assertIsInstance(produced, bytes)
        self.assertEqual(
            produced, module.encode_canonical(material, "journal record")
        )

    def test_shared_acyclic_content_still_encodes(self):
        module = require(MODULE)
        shared = [1, 2]
        produced = module.encode_value([shared, shared, {"again": shared}])
        self.assertEqual(produced, b"[[1,2],[1,2],{5:again:[1,2]}]")


class TestSpecCanonFixR5(unittest.TestCase):
    """Fix round 5, Region 3, ruling 62: canonical depth form.

    Written test first for N-25. The canonical encode and
    decode acts meet deep finite nesting with the governed
    ValueError form of the module, beside the standing
    acyclic and cyclic cases still deciding as pinned.
    """

    def _deep_list(self, depth):
        value = "x"
        for _ in range(depth):
            value = [value]
        return value

    def test_encode_canonical_deep_nesting_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.encode_canonical(
                self._deep_list(1500), "journal record")
        self.assertIn("too deeply nested", str(caught.exception))

    def test_encode_value_deep_nesting_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.encode_value(self._deep_list(1500))
        self.assertIn("too deeply nested", str(caught.exception))

    def test_hash_canonical_deep_nesting_raises_value_error(self):
        module = require(MODULE)
        with self.assertRaises(ValueError) as caught:
            module.hash_canonical(
                self._deep_list(1500), "journal record")
        self.assertIn("too deeply nested", str(caught.exception))

    def test_decode_canonical_deep_list_nesting_raises_value_error(self):
        module = require(MODULE)
        raw = (
            b"ontoloop-v1\x00journal record\x00"
            + b"[" * 1500 + b"1:x" + b"]" * 1500
        )
        with self.assertRaises(ValueError) as caught:
            module.decode_canonical(raw, "journal record")
        self.assertIn("too deeply nested", str(caught.exception))

    def test_decode_canonical_deep_mapping_nesting_raises_value_error(self):
        module = require(MODULE)
        content = b"1:x"
        for _ in range(1500):
            content = b"{1:a:" + content + b"}"
        raw = b"ontoloop-v1\x00journal record\x00" + content
        with self.assertRaises(ValueError) as caught:
            module.decode_canonical(raw, "journal record")
        self.assertIn("too deeply nested", str(caught.exception))

    def test_standing_depth_still_encodes_and_decodes(self):
        module = require(MODULE)
        value = self._deep_list(120)
        produced = module.encode_canonical(value, "journal record")
        self.assertIsInstance(produced, bytes)
        self.assertEqual(
            module.decode_canonical(produced, "journal record"), value)

    def test_standing_cyclic_cases_still_raise_the_cycle_form(self):
        module = require(MODULE)
        material = []
        material.append(material)
        with self.assertRaises(ValueError) as caught:
            module.encode_canonical(material, "journal record")
        self.assertEqual(
            str(caught.exception), "cyclic value in canonical form")

    def test_standing_acyclic_cases_still_encode_byte_identical(self):
        module = require(MODULE)
        record = module.golden_record("journal record")
        self.assertEqual(
            module.encode_canonical(record, "journal record"),
            module.golden_byte_examples()["journal record"],
        )


if __name__ == "__main__":
    unittest.main()
