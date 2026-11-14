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


if __name__ == "__main__":
    unittest.main()
