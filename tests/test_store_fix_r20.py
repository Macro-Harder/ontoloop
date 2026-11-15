"""Fix round 20, ruling 801: the governed append act rollback.

A canonical refusal raised at the signing step of
append_record, over a store level field the canonical layer
refuses, stands returned in the refusal mapping form with
the act rolled back whole, in the same limb family as the
signing key unavailable refusal.
"""

import copy
import unittest

from tests.harness import require

MODULE = "ontoloop.store"

REFUSAL = {
    "error": "signing key unavailable",
    "appended": False,
    "reported_appended": False,
}

CONTENT = {"record_type": "golden record", "payload": "r20 append"}


def _snapshot(store):
    return (
        copy.deepcopy(store.get("records")),
        copy.deepcopy(store.get("manifest")),
        copy.deepcopy(store.get("signature_object")),
        copy.deepcopy(store.get("anchor_staging_copy")),
        store.get("key_slot"),
    )


def _assert_rolled_back(case, store, before):
    records, manifest, signature, anchor, slot = before
    case.assertEqual(store.get("records"), records)
    case.assertEqual(store.get("manifest"), manifest)
    case.assertEqual(store.get("signature_object"), signature)
    case.assertEqual(store.get("anchor_staging_copy"), anchor)
    case.assertEqual(store.get("key_slot"), slot)


class TestAppendCanonicalRefusalAtSigning(unittest.TestCase):

    def _variant(self, mutate):
        module = require(MODULE)
        store = module.golden_record_store()
        mutate(store)
        before = _snapshot(store)
        result = module.append_record(store, dict(CONTENT))
        self.assertEqual(result, REFUSAL)
        _assert_rolled_back(self, store, before)

    def test_store_identity_float_rolls_back_whole(self):
        def mutate(store):
            store["store_identity"] = 1.5
        self._variant(mutate)

    def test_founding_identity_mapping_with_float_rolls_back(self):
        def mutate(store):
            store["founding_object_identity"] = {"nested": 1.5}
        self._variant(mutate)

    def test_manifest_schema_version_float_rolls_back(self):
        def mutate(store):
            store["manifest"]["journal_schema_version"] = 1.5
        self._variant(mutate)

    def test_manifest_hash_algorithm_set_rolls_back(self):
        def mutate(store):
            store["manifest"]["hash_algorithm_identity"] = {"SHA-256"}
        self._variant(mutate)

    def test_capture_append_delegation_rolls_back_whole(self):
        module = require(MODULE)
        store = module.golden_record_store()
        store["store_identity"] = 1.5
        before = _snapshot(store)
        result = module.capture_append(store)
        self.assertEqual(result.get("refused"), True)
        self.assertEqual(result.get("error"), "signing key unavailable")
        _assert_rolled_back(self, store, before)


class TestAppendStandingFormsStillStand(unittest.TestCase):

    def test_signing_key_unavailable_still_rolls_back_whole(self):
        module = require(MODULE)
        store = module.golden_record_store()
        store["key_slot"] = "not bytes"
        before = _snapshot(store)
        result = module.append_record(store, dict(CONTENT))
        self.assertEqual(result, REFUSAL)
        _assert_rolled_back(self, store, before)

    def test_governed_append_still_appends_and_agrees(self):
        module = require(MODULE)
        store = module.golden_record_store()
        result = module.append_record(store, dict(CONTENT))
        self.assertTrue(result["appended"])
        self.assertEqual(len(store["records"]), 3)
        outcome = module.verify(store)
        self.assertEqual(outcome["output"], "agreement")


if __name__ == "__main__":
    unittest.main()
