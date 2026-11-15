"""Fix round 16, Region 3 pins: store append act.

Written test first for ruling 578.
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


class TestStoreFixR16AppendWrongValueHash(unittest.TestCase):
    """Ruling 578: an append over a wrong value hash is refused."""

    def _append_over_hash(self, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1]["hash"] = value
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def test_append_over_zero_hash_is_refused(self):
        _assert_refused(
            self, self._append_over_hash("0" * 64),
            "last record hash not standing")

    def test_append_over_f_hash_is_refused(self):
        _assert_refused(
            self, self._append_over_hash("f" * 64),
            "last record hash not standing")

    def test_append_over_recomputed_canonical_untouched_hash_refused(self):
        store_module = require(STORE)
        sealing = require(SEALING)
        store = _golden_store(store_module)
        last = store["records"][-1]
        last["content"] = "plain string"
        fields = {
            "content": last["content"],
            "predecessor_hash": last["predecessor_hash"],
            "store_sequence": last["store_sequence"],
            "record_type": last["record_type"],
        }
        last["canonical_bytes"] = sealing.canonical_bytes(
            fields, sealing.JOURNAL_RECORD_KIND)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        _assert_refused(
            self, (store, result, snapshot),
            "last record hash not standing")

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


class TestStoreFixR16AppendStandingNeighbours(unittest.TestCase):
    """Ruling 578 neighbours: the standing refusal forms stand."""

    def _append_over_value(self, field, value):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1][field] = copy.deepcopy(value)
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        return store, result, snapshot

    def _append_over_deleted(self, field):
        store_module = require(STORE)
        store = _golden_store(store_module)
        del store["records"][-1][field]
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

    def test_append_over_uppercase_hash_still_refused_not_standing(self):
        store_module = require(STORE)
        store = _golden_store(store_module)
        store["records"][-1]["hash"] = (
            store["records"][-1]["hash"].upper())
        snapshot = _snapshot(store)
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        _assert_refused(
            self, (store, result, snapshot),
            "predecessor hash not standing")

    def test_append_over_integer_hash_still_refused_not_standing(self):
        _assert_refused(
            self, self._append_over_value("hash", 7),
            "predecessor hash not standing")

    def test_append_over_none_hash_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_value("hash", None),
            "predecessor hash erased")

    def test_append_over_deleted_hash_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_deleted("hash"),
            "predecessor hash erased")

    def test_append_over_string_canonical_still_refused_not_standing(self):
        _assert_refused(
            self, self._append_over_value(
                "canonical_bytes", "plain string"),
            "last record canonical bytes not standing")

    def test_append_over_deleted_content_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_deleted("content"),
            "last record field erased")

    def test_append_over_none_last_record_still_refused_erased(self):
        _assert_refused(
            self, self._append_over_last(None), "predecessor hash erased")

    def test_append_over_string_content_still_refused_not_standing(self):
        _assert_refused(
            self, self._append_over_value("content", "plain string"),
            "last record field not standing")

    def test_append_over_intact_last_record_still_appends(self):
        _assert_intact_appends(self)


class TestStoreFixR16Ruling536Bound(unittest.TestCase):
    """The ruling 536 bound in its hash recomputed form stands."""

    def test_append_over_fully_recomputed_last_record_still_appends(self):
        store_module = require(STORE)
        sealing = require(SEALING)
        store = _golden_store(store_module)
        last = store["records"][-1]
        last["content"] = "plain string"
        fields = {
            "content": last["content"],
            "predecessor_hash": last["predecessor_hash"],
            "store_sequence": last["store_sequence"],
            "record_type": last["record_type"],
        }
        last["canonical_bytes"] = sealing.canonical_bytes(
            fields, sealing.JOURNAL_RECORD_KIND)
        last["hash"] = sealing.hash_journal_record(
            last["content"], last["predecessor_hash"],
            last["store_sequence"], last["record_type"])
        before_count = len(store["records"])
        result = store_module.append_record(
            store, {"payload": "next record"}, "record")
        self.assertIs(result["appended"], True)
        self.assertIs(result["reported_appended"], True)
        self.assertEqual(len(store["records"]), before_count + 1)


if __name__ == "__main__":
    unittest.main()
