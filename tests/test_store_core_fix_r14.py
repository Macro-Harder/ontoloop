"""Fix round 14, Region 3 pins: store append act.

Written test first for rulings 488, 489, and 490.
Each pin states the governed form its ruling charges,
beside the standing forms the cure preserves.
"""

import copy
import unittest

from tests.harness import require

STORE = "ontoloop.store"


def _golden_store(store_module):
    return copy.deepcopy(store_module.golden_record_store())


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


def _assert_refused(test_case, outcome, error):
    store, result, snapshot = outcome
    test_case.assertIs(result["appended"], False)
    test_case.assertIs(result["reported_appended"], False)
    test_case.assertEqual(result["error"], error)
    _assert_unchanged(test_case, store, snapshot)


def _assert_intact_appends(test_case):
    store_module = require(STORE)
    store = _golden_store(store_module)
    before_count = len(store["records"])
    result = store_module.append_record(
        store, {"payload": "next record"}, "record")
    test_case.assertIs(result["appended"], True)
    test_case.assertIs(result["reported_appended"], True)
    test_case.assertEqual(len(store["records"]), before_count + 1)
    verified = store_module.verify(store)
    test_case.assertEqual(verified["output"], "agreement")


class TestStoreFixR14AppendWrongCanonicalForm(unittest.TestCase):
    """Ruling 488: an append over a wrong form canonical field is refused."""

    def _append_over(self, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1]["canonical_bytes"] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def test_append_over_string_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over("plain string"),
            "last record canonical bytes not standing")

    def test_append_over_integer_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over(7),
            "last record canonical bytes not standing")

    def test_append_over_empty_bytes_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over(b""),
            "last record canonical bytes not standing")

    def test_append_over_empty_string_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over(""),
            "last record canonical bytes not standing")

    def test_append_over_list_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over(["canonical"]),
            "last record canonical bytes not standing")

    def test_append_over_dict_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over({"canonical": "bytes"}),
            "last record canonical bytes not standing")

    def test_append_over_true_canonical_is_refused(self):
        _assert_refused(
            self, self._append_over(True),
            "last record canonical bytes not standing")

    def test_append_over_erased_canonical_still_refused_erased(self):
        store_module = require(STORE)
        for form in ("none", "deleted"):
            store = _golden_store(store_module)
            if form == "none":
                store["records"][-1]["canonical_bytes"] = None
            else:
                del store["records"][-1]["canonical_bytes"]
            snapshot = _snapshot(store)
            result = store_module.append_record(
                store, {"payload": "next record"}, "record")
            _assert_refused(
                self, (store, result, snapshot),
                "last record canonical bytes erased")

    def test_append_over_bytearray_and_memoryview_canonical_appends(self):
        store_module = require(STORE)
        for form in ("bytearray", "memoryview"):
            store = _golden_store(store_module)
            real = store["records"][-1]["canonical_bytes"]
            if form == "bytearray":
                store["records"][-1]["canonical_bytes"] = bytearray(real)
            else:
                store["records"][-1]["canonical_bytes"] = memoryview(real)
            before_count = len(store["records"])
            result = store_module.append_record(
                store, {"payload": "next record"}, "record")
            self.assertIs(result["appended"], True, form)
            self.assertIs(result["reported_appended"], True, form)
            self.assertEqual(
                len(store["records"]), before_count + 1, form)
            verified = store_module.verify(store)
            self.assertEqual(verified["output"], "agreement", form)

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


class TestStoreFixR14AppendErasedJournalField(unittest.TestCase):
    """Ruling 489: an append over an erased journal field is refused."""

    def _append_over_deleted(self, field):
        store_module = require(STORE)
        store = _golden_store(store_module)
        del store["records"][-1][field]
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def test_append_over_deleted_content_is_refused(self):
        _assert_refused(
            self, self._append_over_deleted("content"),
            "last record field erased")

    def test_append_over_deleted_record_type_is_refused(self):
        _assert_refused(
            self, self._append_over_deleted("record_type"),
            "last record field erased")

    def test_append_over_deleted_predecessor_hash_is_refused(self):
        _assert_refused(
            self, self._append_over_deleted("predecessor_hash"),
            "last record field erased")

    def test_append_over_deleted_store_sequence_is_refused(self):
        _assert_refused(
            self, self._append_over_deleted("store_sequence"),
            "last record field erased")

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


class TestStoreFixR14AppendNonMappingLastRecord(unittest.TestCase):
    """Ruling 490: an append over a non mapping last record is refused."""

    def _append_over(self, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def test_append_over_none_last_record_is_refused(self):
        _assert_refused(
            self, self._append_over(None), "predecessor hash erased")

    def test_append_over_string_last_record_is_refused(self):
        _assert_refused(
            self, self._append_over("plain string"),
            "predecessor hash erased")

    def test_append_over_list_last_record_is_refused(self):
        _assert_refused(
            self, self._append_over(["record"]), "predecessor hash erased")

    def test_append_over_empty_mapping_still_refused_erased(self):
        _assert_refused(
            self, self._append_over({}), "predecessor hash erased")

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


if __name__ == "__main__":
    unittest.main()
