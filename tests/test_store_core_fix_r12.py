"""Fix round 12, Region 3 pins: store, sealing, and core.

Written test first for rulings 392, 393, 394, and 395.
Each pin states the governed form its ruling charges,
beside the standing forms the cure preserves.
"""

import copy
import unittest
from decimal import Decimal
from fractions import Fraction

from tests.harness import require

CORE = "ontoloop.core"
STORE = "ontoloop.store"
SEALING = "ontoloop.sealing"


def _record_with_version(module, version):
    record = module.golden_record()
    record["schema_version"] = version
    return record


def _golden_store(store_module):
    return copy.deepcopy(store_module.golden_record_store())


def _erase_hash(record, form):
    if form == "none":
        record["hash"] = None
    elif form == "deleted":
        del record["hash"]
    else:
        raise ValueError(form)


class TestCoreFixR12VersionForms(unittest.TestCase):
    """Ruling 392: Decimal and Fraction versions above the reader."""

    def _check(self, version):
        module = require(CORE)
        return module.check_record(
            _record_with_version(module, version))

    def _newer(self, module):
        return module.error_catalogue()[
            "version newer than reader"]["error"]

    def _below(self, module):
        return module.error_catalogue()[
            "version below reader window"]["error"]

    def test_decimal_4_returns_newer_refusal(self):
        module = require(CORE)
        result = self._check(Decimal(4))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], self._newer(module))

    def test_decimal_3_5_returns_newer_refusal(self):
        module = require(CORE)
        result = self._check(Decimal("3.5"))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], self._newer(module))

    def test_decimal_infinity_returns_newer_refusal(self):
        module = require(CORE)
        result = self._check(Decimal("Infinity"))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], self._newer(module))

    def test_fraction_7_2_returns_newer_refusal(self):
        module = require(CORE)
        result = self._check(Fraction(7, 2))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], self._newer(module))

    def test_fraction_4_1_returns_newer_refusal(self):
        module = require(CORE)
        result = self._check(Fraction(4, 1))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], self._newer(module))

    def test_decimal_and_fraction_at_or_below_reader_return_below(self):
        module = require(CORE)
        below = self._below(module)
        forms = (
            Decimal(2), Decimal(3), Decimal("NaN"),
            Fraction(2, 1), Fraction(3, 1),
        )
        for version in forms:
            result = self._check(version)
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], below, repr(version))

    def test_decimal_signalling_nan_returns_below(self):
        module = require(CORE)
        result = self._check(Decimal("sNaN"))
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["error"], self._below(module))

    def test_int_and_float_forms_still_decide_as_they_decide(self):
        module = require(CORE)
        newer = self._newer(module)
        below = self._below(module)
        for version in (4, 3.5, 4.0, float("inf")):
            result = self._check(version)
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], newer, repr(version))
        for version in (2.5, 1.5, 2.999):
            result = self._check(version)
            self.assertIs(result["accepted"], False, repr(version))
            self.assertEqual(result["error"], below, repr(version))
        for version in (1, 2, 3):
            result = self._check(version)
            self.assertIs(result["accepted"], True, repr(version))


class TestSealingFixR12ErasedHash(unittest.TestCase):
    """Ruling 393: an erased stored hash returns disagreement."""

    def _verify_both(self, store):
        store_module = require(STORE)
        sealing = require(SEALING)
        return store_module.verify(store), sealing.verify(store)

    def test_first_record_hash_none_returns_disagreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        _erase_hash(store["records"][0], "none")
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")

    def test_first_record_hash_deleted_returns_disagreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        _erase_hash(store["records"][0], "deleted")
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")

    def test_last_record_hash_none_returns_disagreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        _erase_hash(store["records"][-1], "none")
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")

    def test_last_record_hash_deleted_returns_disagreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        _erase_hash(store["records"][-1], "deleted")
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")

    def test_every_record_hash_none_returns_disagreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        for record in store["records"]:
            _erase_hash(record, "none")
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")

    def test_every_record_hash_deleted_returns_disagreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        for record in store["records"]:
            _erase_hash(record, "deleted")
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")

    def test_anchored_form_over_erased_hash_returns_disagreement(self):
        store_module = require(STORE)
        for form in ("none", "deleted"):
            store = _golden_store(store_module)
            anchor = dict(store["anchor_staging_copy"])
            _erase_hash(store["records"][-1], form)
            result = store_module.verify(store, anchor=anchor)
            self.assertEqual(result["output"], "disagreement", form)

    def test_other_erased_fields_still_return_disagreement(self):
        store_module = require(STORE)
        fields = (
            "content", "predecessor_hash",
            "store_sequence", "record_type",
        )
        for field in fields:
            store = _golden_store(store_module)
            del store["records"][0][field]
            result = store_module.verify(store)
            self.assertEqual(
                result["output"], "disagreement", field)
            self.assertIn(
                "content_mismatch",
                result.get("failed_checks", []), field)

    def test_hash_in_wrong_value_form_still_returns_unverifiable(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][0]["hash"] = ""
        result = store_module.verify(store)
        self.assertEqual(result["output"], "unverifiable")
        store = _golden_store(store_module)
        store["records"][-1]["hash"] = ""
        result = store_module.verify(store)
        self.assertEqual(result["output"], "unverifiable")

    def test_intact_store_still_returns_agreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "agreement")
            self.assertEqual(
                result["sentence"], store_module.VERIFY_SENTENCE)
            self.assertEqual(
                result["holes"], list(store_module.VERIFY_HOLES))


class TestStoreFixR12AppendErasedHash(unittest.TestCase):
    """Ruling 394: an append over an erased last hash is refused."""

    def _append_over_erased(self, form):
        store_module = require(STORE)
        store = _golden_store(store_module)
        _erase_hash(store["records"][-1], form)
        before_count = len(store["records"])
        before_manifest = copy.deepcopy(store["manifest"])
        before_signature = copy.deepcopy(store["signature_object"])
        before_anchor = copy.deepcopy(store["anchor_staging_copy"])
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return (
            store, result, before_count,
            before_manifest, before_signature, before_anchor,
        )

    def _assert_refused_with_no_record_and_no_heads(self, outcome):
        (store, result, before_count,
         before_manifest, before_signature, before_anchor) = outcome
        self.assertIs(result["appended"], False)
        self.assertIs(result["reported_appended"], False)
        self.assertEqual(result["error"], "predecessor hash erased")
        self.assertEqual(len(store["records"]), before_count)
        self.assertEqual(store["manifest"], before_manifest)
        self.assertEqual(store["signature_object"], before_signature)
        self.assertEqual(
            store["anchor_staging_copy"], before_anchor)

    def test_append_over_last_hash_deleted_is_refused(self):
        self._assert_refused_with_no_record_and_no_heads(
            self._append_over_erased("deleted"))

    def test_append_over_last_hash_none_is_refused(self):
        self._assert_refused_with_no_record_and_no_heads(
            self._append_over_erased("none"))

    def test_append_over_intact_last_record_still_appends(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        before_count = len(store["records"])
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        self.assertIs(result["appended"], True)
        self.assertIs(result["reported_appended"], True)
        self.assertEqual(len(store["records"]), before_count + 1)
        verified = store_module.verify(store)
        self.assertEqual(verified["output"], "agreement")


class TestSealingFixR12TravelLintHoles(unittest.TestCase):
    """Ruling 395: a non iterable verify holes value is governed."""

    def _surface_with_holes(self, holes):
        sealing = require(SEALING)
        surfaces = sealing.specification_surfaces()
        carried = sealing.surface_texts(surfaces[0])
        carried["verify holes"] = holes
        return carried

    def test_non_iterable_holes_values_return_governed_outcome(self):
        sealing = require(SEALING)
        forms = (5, 1.5, True, None, object())
        for holes in forms:
            surface = self._surface_with_holes(holes)
            result = sealing.travel_lint(surface)
            self.assertIs(result["passed"], False, repr(holes))
            self.assertIn(
                "verify holes", result["paraphrases"], repr(holes))

    def test_string_holes_value_still_returns_governed_outcome(self):
        sealing = require(SEALING)
        surface = self._surface_with_holes("a string value")
        result = sealing.travel_lint(surface)
        self.assertIs(result["passed"], False)
        self.assertIn("verify holes", result["paraphrases"])

    def test_mapping_generator_and_list_holes_still_pass(self):
        sealing = require(SEALING)
        holes = list(sealing.VERIFY_HOLES)
        mapping_form = {hole: True for hole in holes}
        generator_form = (hole for hole in holes)
        for form in (mapping_form, generator_form, list(holes)):
            surface = self._surface_with_holes(form)
            result = sealing.travel_lint(surface)
            self.assertIs(result["passed"], True, repr(form))
            self.assertEqual(result["paraphrases"], [], repr(form))


if __name__ == "__main__":
    unittest.main()
