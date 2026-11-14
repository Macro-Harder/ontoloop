"""Fix round 8, Region 2: writable memoryview hash surfaces.

Written test first for rulings 205 to 210. A writable
memoryview, a memoryview over a bytearray, hashes with
ValueError where the charged unhashable forms hash with
TypeError. Each pin states the governed form its ruling
charges, beside the standing forms the cure preserves.
"""

import unittest

from tests.harness import require

CORE = "ontoloop.core"
CANONICAL = "ontoloop.canonical"


def writable_memoryview():
    return memoryview(bytearray(b"writable"))


class TestCoreFixR8(unittest.TestCase):
    # Ruling 205, R8-CORE-1: refusal_reason meets a name whose
    # hashing raises ValueError in the governed None form.
    def test_refusal_reason_writable_memoryview_name_returns_none(self):
        module = require(CORE)
        self.assertIsNone(module.refusal_reason(writable_memoryview()))

    def test_refusal_reason_standing_names_still_return(self):
        module = require(CORE)
        self.assertEqual(
            module.refusal_reason("unlisted record type"),
            "record type not listed",
        )
        self.assertIsNone(module.refusal_reason(["unlisted record type"]))

    # Ruling 206, R8-CORE-2: the canonical second reading meets
    # a kind whose hashing raises ValueError in the stated
    # unclassified form, at the reading and through
    # divergence_check.
    def _case(self, kind):
        return {"case": "r8-case-1", "family": "r8", "kind": kind}

    def test_second_reading_writable_memoryview_kind_returns_unclassified(self):
        module = require(CANONICAL)
        result = module.reading(
            [self._case(writable_memoryview())], reader="second")
        self.assertEqual(result, {"r8-case-1": "unclassified"})

    def test_divergence_check_writable_memoryview_kind_returns_unclassified(self):
        module = require(CANONICAL)
        kind = writable_memoryview()
        result = module.divergence_check([self._case(kind)])
        self.assertEqual(len(result["divergences"]), 1)
        self.assertEqual(result["divergences"][0]["case"], "r8-case-1")
        self.assertIs(result["divergences"][0]["first"], kind)
        self.assertEqual(result["divergences"][0]["second"], "unclassified")
        self.assertEqual(result["plan_findings"], result["divergences"])

    def test_second_reading_standing_kinds_still_return(self):
        module = require(CANONICAL)
        for kind in ("positive", "negative", "boundary"):
            result = module.reading([self._case(kind)], reader="second")
            self.assertEqual(result, {"r8-case-1": kind}, kind)
        result = module.reading(
            [self._case(["positive"])], reader="second")
        self.assertEqual(result, {"r8-case-1": "unclassified"})

    # Ruling 207, R8-CORE-3: state_transition meets a pair whose
    # hashing raises ValueError in the same KeyError form.
    def test_state_transition_writable_memoryview_state_raises_key_error(self):
        module = require(CORE)
        with self.assertRaises(KeyError):
            module.state_transition(
                writable_memoryview(), "confirmation")

    def test_state_transition_writable_memoryview_act_raises_key_error(self):
        module = require(CORE)
        with self.assertRaises(KeyError):
            module.state_transition(
                "Provisional, first period", writable_memoryview())

    def test_state_transition_standing_forms_still_decide(self):
        module = require(CORE)
        self.assertEqual(
            module.state_transition(
                "Provisional, first period", "confirmation"),
            "Confirmed",
        )
        with self.assertRaises(KeyError):
            module.state_transition(["Provisional, first period"], "confirmation")

    # Ruling 208, R8-CORE-4: check_owing_forms meets a row name
    # whose hashing raises ValueError in the governed failure form.
    def test_check_owing_forms_writable_memoryview_name_returns_failure(self):
        module = require(CORE)
        result = module.check_owing_forms({"name": writable_memoryview()})
        self.assertIs(result["passed"], False)
        self.assertEqual(result["defect_home"], "catalogue")
        self.assertEqual(result["check_point"], "section 13.3")
        self.assertEqual(result["defects"], [])
        self.assertIsNone(result["owing_statement"])

    def test_check_owing_forms_standing_forms_still_decide(self):
        module = require(CORE)
        result = module.check_owing_forms({"name": ["sync failure"]})
        self.assertIs(result["passed"], False)
        self.assertEqual(result["defects"], [])
        self.assertIsNone(result["owing_statement"])
        for name, row in module.error_catalogue().items():
            standing = module.check_owing_forms(dict(row))
            self.assertIs(standing["passed"], True, name)

    # Ruling 209, R8-CORE-5: catalogue_row_with_value meets an
    # argument whose hashing raises ValueError in the governed
    # None form, in the kind position and in the form position.
    def test_catalogue_row_with_value_writable_memoryview_kind_returns_none(self):
        module = require(CORE)
        self.assertIsNone(module.catalogue_row_with_value(
            writable_memoryview(), "advanced_form"))

    def test_catalogue_row_with_value_writable_memoryview_form_returns_none(self):
        module = require(CORE)
        self.assertIsNone(module.catalogue_row_with_value(
            "figure", writable_memoryview()))

    def test_catalogue_row_with_value_standing_forms_still_return(self):
        module = require(CORE)
        row = module.catalogue_row_with_value("figure", "advanced_form")
        self.assertIsNotNone(row)
        self.assertIn("name", row)
        self.assertIsNone(module.catalogue_row_with_value(
            ["figure"], "advanced_form"))
        self.assertIsNone(module.catalogue_row_with_value(
            "figure", ["advanced_form"]))

    # Ruling 210, R8-CORE-6: meaning_check meets an identifier
    # whose hashing raises ValueError in the same held form in
    # both directions.
    def test_meaning_check_writable_memoryview_identifier_held_direction(self):
        module = require(CORE)
        identifier = writable_memoryview()
        result = module.meaning_check(
            check_id=identifier,
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning held",
        )
        entry = result["meaning_change_record_entry"]
        self.assertEqual(entry["classification"], "no meaning change shown")
        self.assertEqual(entry["checks_run"], [identifier])
        self.assertEqual(
            result["outcome_records_before"],
            result["outcome_records_after"],
        )

    def test_meaning_check_writable_memoryview_identifier_changed_direction(self):
        module = require(CORE)
        identifier = writable_memoryview()
        result = module.meaning_check(
            check_id=identifier,
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning changed",
        )
        entry = result["meaning_change_record_entry"]
        self.assertEqual(entry["classification"], "no meaning change shown")
        self.assertEqual(entry["checks_run"], [identifier])
        self.assertEqual(
            result["outcome_records_before"],
            result["outcome_records_after"],
        )

    def test_meaning_check_standing_identifiers_still_decide(self):
        module = require(CORE)
        changed = module.meaning_check(
            check_id="SPAN-T07",
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning changed",
        )
        self.assertEqual(
            changed["meaning_change_record_entry"]["classification"],
            "meaning change under a stable shape",
        )
        held = module.meaning_check(
            check_id=["SPAN-X"],
            affected_class="type mapping change",
            fixture="fixture",
            direction="meaning changed",
        )
        self.assertEqual(
            held["meaning_change_record_entry"]["classification"],
            "no meaning change shown",
        )


if __name__ == "__main__":
    unittest.main()
