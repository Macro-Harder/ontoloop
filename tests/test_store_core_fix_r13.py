"""Fix round 13, Region 3 pins: store and sealing.

Written test first for rulings 438, 439, and 440.
Each pin states the governed form its ruling charges,
beside the standing forms the cure preserves.
"""

import copy
import unittest

from tests.harness import require

STORE = "ontoloop.store"
SEALING = "ontoloop.sealing"


def _golden_store(store_module):
    return copy.deepcopy(store_module.golden_record_store())


def _wrong_hash_forms(store):
    correct = store["records"][-1]["hash"]
    return (
        ("empty string", ""),
        ("integer zero", 0),
        ("false", False),
        ("short string", "abc"),
        ("correct digest as bytes", correct.encode()),
        ("correct digest as bytearray", bytearray(correct.encode())),
        ("correct digest in uppercase", correct.upper()),
        ("correct digest inside a list", [correct]),
    )


def _erase_canonical(record, form):
    if form == "none":
        record["canonical_bytes"] = None
    elif form == "deleted":
        del record["canonical_bytes"]
    else:
        raise ValueError(form)


def _snapshot(store):
    return (
        len(store["records"]),
        copy.deepcopy(store["manifest"]),
        copy.deepcopy(store["signature_object"]),
        copy.deepcopy(store["anchor_staging_copy"]),
    )


def _assert_unchanged(test_case, store, snapshot):
    count, manifest, signature, anchor = snapshot
    test_case.assertEqual(len(store["records"]), count)
    test_case.assertEqual(store["manifest"], manifest)
    test_case.assertEqual(store["signature_object"], signature)
    test_case.assertEqual(store["anchor_staging_copy"], anchor)


class TestStoreFixR13AppendWrongHashForm(unittest.TestCase):
    """Ruling 438: an append over a wrong form last hash is refused."""

    def _append_over(self, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1]["hash"] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def _assert_refused(self, outcome):
        store, result, snapshot = outcome
        self.assertIs(result["appended"], False)
        self.assertIs(result["reported_appended"], False)
        self.assertEqual(
            result["error"], "predecessor hash not standing")
        _assert_unchanged(self, store, snapshot)

    def test_append_over_empty_string_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(self._append_over(forms["empty string"]))

    def test_append_over_integer_zero_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(self._append_over(forms["integer zero"]))

    def test_append_over_false_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(self._append_over(forms["false"]))

    def test_append_over_short_string_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(self._append_over(forms["short string"]))

    def test_append_over_bytes_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(
            self._append_over(forms["correct digest as bytes"]))

    def test_append_over_bytearray_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(
            self._append_over(forms["correct digest as bytearray"]))

    def test_append_over_uppercase_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(
            self._append_over(forms["correct digest in uppercase"]))

    def test_append_over_list_hash_is_refused(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        forms = dict(_wrong_hash_forms(store))
        self._assert_refused(
            self._append_over(forms["correct digest inside a list"]))

    def test_append_over_erased_hash_still_refused_erased(self):
        store_module = require(STORE)
        for form in ("none", "deleted"):
            store = _golden_store(store_module)
            if form == "none":
                store["records"][-1]["hash"] = None
            else:
                del store["records"][-1]["hash"]
            snapshot = _snapshot(store)
            result = store_module.append_record(
                store, {"payload": "next record"}, "record")
            self.assertIs(result["appended"], False, form)
            self.assertIs(result["reported_appended"], False, form)
            self.assertEqual(
                result["error"], "predecessor hash erased", form)
            _assert_unchanged(self, store, snapshot)

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


class TestSealingFixR13ErasedCanonicalBytes(unittest.TestCase):
    """Ruling 439: an erased canonical bytes field is a disagreement."""

    def _verify_both(self, store):
        store_module = require(STORE)
        sealing = require(SEALING)
        return store_module.verify(store), sealing.verify(store)

    def _store_with_erasure(self, position, form):
        store_module = require(STORE)
        store = _golden_store(store_module)
        if position == "first":
            _erase_canonical(store["records"][0], form)
        elif position == "last":
            _erase_canonical(store["records"][-1], form)
        elif position == "every":
            for record in store["records"]:
                _erase_canonical(record, form)
        else:
            raise ValueError(position)
        return store

    def _assert_disagreement(self, position, form):
        store = self._store_with_erasure(position, form)
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "disagreement")
            self.assertIn(
                "content_mismatch", result.get("failed_checks", []))

    def test_first_record_canonical_deleted_returns_disagreement(self):
        self._assert_disagreement("first", "deleted")

    def test_first_record_canonical_none_returns_disagreement(self):
        self._assert_disagreement("first", "none")

    def test_last_record_canonical_deleted_returns_disagreement(self):
        self._assert_disagreement("last", "deleted")

    def test_last_record_canonical_none_returns_disagreement(self):
        self._assert_disagreement("last", "none")

    def test_every_record_canonical_deleted_returns_disagreement(self):
        self._assert_disagreement("every", "deleted")

    def test_every_record_canonical_none_returns_disagreement(self):
        self._assert_disagreement("every", "none")

    def test_anchored_form_over_erased_canonical_returns_disagreement(self):
        store_module = require(STORE)
        cases = (("first", "deleted"), ("last", "none"))
        for position, form in cases:
            store = self._store_with_erasure(position, form)
            anchor = dict(store["anchor_staging_copy"])
            result = store_module.verify(store, anchor=anchor)
            self.assertEqual(
                result["output"], "disagreement", (position, form))

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

    def test_canonical_empty_bytes_still_returns_unverifiable(self):
        store_module = require(STORE)
        for index in (0, -1):
            store = _golden_store(store_module)
            store["records"][index]["canonical_bytes"] = b""
            result = store_module.verify(store)
            self.assertEqual(result["output"], "unverifiable", index)

    def test_intact_store_still_returns_agreement(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        for result in self._verify_both(store):
            self.assertEqual(result["output"], "agreement")
            self.assertEqual(
                result["sentence"], store_module.VERIFY_SENTENCE)
            self.assertEqual(
                result["holes"], list(store_module.VERIFY_HOLES))


class TestStoreFixR13AppendErasedCanonicalBytes(unittest.TestCase):
    """Ruling 440: an append over an erased canonical field is refused."""

    def _append_over_erased(self, form):
        store_module = require(STORE)
        store = _golden_store(store_module)
        _erase_canonical(store["records"][-1], form)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def _assert_refused(self, outcome):
        store, result, snapshot = outcome
        self.assertIs(result["appended"], False)
        self.assertIs(result["reported_appended"], False)
        self.assertEqual(
            result["error"], "last record canonical bytes erased")
        _assert_unchanged(self, store, snapshot)

    def test_append_over_last_canonical_deleted_is_refused(self):
        self._assert_refused(self._append_over_erased("deleted"))

    def test_append_over_last_canonical_none_is_refused(self):
        self._assert_refused(self._append_over_erased("none"))

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


if __name__ == "__main__":
    unittest.main()
