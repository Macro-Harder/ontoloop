"""Fix round 15, Region 3 pins: store append act.

Written test first for ruling 536.
Each pin states the governed form its ruling charges,
beside the standing forms the cure preserves.
"""

import copy
import unittest
from fractions import Fraction

from tests.harness import require

STORE = "ontoloop.store"


def _golden_store(store_module):
    return copy.deepcopy(store_module.golden_record_store())


def _snapshot(store):
    return (
        copy.deepcopy(store["records"]),
        copy.deepcopy(store["manifest"]),
        copy.deepcopy(store["signature_object"]),
        copy.deepcopy(store["anchor_staging_copy"]),
    )


def _assert_unchanged(test_case, store, snapshot):
    records, manifest, signature, anchor = snapshot
    test_case.assertEqual(store["records"], records)
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


class TestStoreFixR15AppendWrongValueJournalField(unittest.TestCase):
    """Ruling 536: an append over a wrong value journal field is refused."""

    def _append_over(self, field, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1][field] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def test_append_over_string_content_is_refused(self):
        _assert_refused(
            self, self._append_over("content", "plain string"),
            "last record field not standing")

    def test_append_over_integer_content_is_refused(self):
        _assert_refused(
            self, self._append_over("content", 7),
            "last record field not standing")

    def test_append_over_none_content_is_refused(self):
        _assert_refused(
            self, self._append_over("content", None),
            "last record field not standing")

    def test_append_over_none_record_type_is_refused(self):
        _assert_refused(
            self, self._append_over("record_type", None),
            "last record field not standing")

    def test_append_over_integer_record_type_is_refused(self):
        _assert_refused(
            self, self._append_over("record_type", 7),
            "last record field not standing")

    def test_append_over_empty_string_record_type_is_refused(self):
        _assert_refused(
            self, self._append_over("record_type", ""),
            "last record field not standing")

    def test_append_over_integer_predecessor_hash_is_refused(self):
        _assert_refused(
            self, self._append_over("predecessor_hash", 7),
            "last record field not standing")

    def test_append_over_none_predecessor_hash_is_refused(self):
        _assert_refused(
            self, self._append_over("predecessor_hash", None),
            "last record field not standing")

    def test_append_over_empty_string_predecessor_hash_is_refused(self):
        _assert_refused(
            self, self._append_over("predecessor_hash", ""),
            "last record field not standing")

    def test_append_over_string_store_sequence_is_refused(self):
        _assert_refused(
            self, self._append_over("store_sequence", "2"),
            "last record field not standing")

    def test_append_over_none_store_sequence_is_refused(self):
        _assert_refused(
            self, self._append_over("store_sequence", None),
            "last record field not standing")

    def test_append_over_negative_store_sequence_is_refused(self):
        _assert_refused(
            self, self._append_over("store_sequence", -1),
            "last record field not standing")

    def test_append_over_fraction_store_sequence_is_refused(self):
        _assert_refused(
            self, self._append_over("store_sequence", Fraction(3, 2)),
            "last record field not standing")

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


class TestStoreFixR15AppendStandingNeighbours(unittest.TestCase):
    """Ruling 536 neighbours: the rulings 488, 489, and 490 forms stand."""

    def _append_over_deleted(self, field):
        store_module = require(STORE)
        store = _golden_store(store_module)
        del store["records"][-1][field]
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def _append_over_value(self, field, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1][field] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def _append_over_last(self, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def test_append_over_deleted_content_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_deleted("content"),
            "last record field erased")

    def test_append_over_deleted_record_type_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_deleted("record_type"),
            "last record field erased")

    def test_append_over_deleted_predecessor_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_deleted("predecessor_hash"),
            "last record field erased")

    def test_append_over_deleted_sequence_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_deleted("store_sequence"),
            "last record field erased")

    def test_append_over_string_canonical_still_refused_not_standing(self):
        _assert_refused(
            self, self._append_over_value(
                "canonical_bytes", "plain string"),
            "last record canonical bytes not standing")

    def test_append_over_empty_bytes_canonical_still_refused(self):
        _assert_refused(
            self, self._append_over_value("canonical_bytes", b""),
            "last record canonical bytes not standing")

    def test_append_over_none_last_record_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_last(None), "predecessor hash erased")

    def test_append_over_list_last_record_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_last(["record"]),
            "predecessor hash erased")

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


if __name__ == "__main__":
    unittest.main()
