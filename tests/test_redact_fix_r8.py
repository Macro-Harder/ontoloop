"""Fix round 8 tests for Region 5: capture, redact and consume.

Written test first for the three positions charged at Round 8
triage ruling 238 point 5: ruling 220 (S15-R8-CR-1, _material_items
reading a memoryview at any position its gathering reaches),
ruling 221 (the family 5 gathering merged defect, S15-R8-CR-2 with
Lead Engineer line E-7 counted in this act and nowhere else, the
gathering acts walking the abstract mapping and sequence forms
and the views of a walked wrapper mapping), and ruling 222
(S15-R8-CR-3, the exit scan state read on a top level assembly
standing in a mapping view form). No test in this file pins the
generator form or the array typecode u form.
"""

import collections
import collections.abc
import os
import unittest

from tests.harness import require

CLEAN = "a routine clean note"


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


def _definite(classification):
    if "firing_records" not in classification:
        return False
    for layer in classification["firing_records"].values():
        for record in layer:
            if record["outcome"] == "definite":
                return True
    return False


class _AbstractMapping(collections.abc.Mapping):
    def __init__(self, data):
        self._data = dict(data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class _AbstractSequence(collections.abc.Sequence):
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class TestRedactFixR8MaterialMemoryviewNested(unittest.TestCase):
    """Ruling 220: a memoryview inside a mapping value container."""

    def test_mv_in_list_as_mapping_value_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material({"note": [memoryview(hit)]})
        self.assertTrue(_definite(result))

    def test_mv_in_tuple_as_mapping_value_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material({"note": (memoryview(hit),)})
        self.assertTrue(_definite(result))

    def test_mv_in_mapping_as_mapping_value_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material(
            {"note": {"inner": memoryview(hit)}}
        )
        self.assertTrue(_definite(result))

    def test_mv_as_mapping_key_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material({memoryview(hit): CLEAN})
        self.assertTrue(_definite(result))

    def test_mv_value_inside_userdict_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material(
            collections.UserDict({"note": memoryview(hit)})
        )
        self.assertTrue(_definite(result))

    def test_mv_element_inside_userlist_fires_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        result = module.classify_material(
            collections.UserList([memoryview(hit)])
        )
        self.assertTrue(_definite(result))

    def test_bytes_controls_in_same_positions_fire_definite(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        for material in (
            {"note": [hit]},
            {"note": (hit,)},
            {"note": {"inner": hit}},
            {hit: CLEAN},
        ):
            self.assertTrue(_definite(module.classify_material(material)))

    def test_clean_memoryview_in_same_positions_stays_clean(self):
        module = require("ontoloop.redact")
        view = memoryview(CLEAN.encode("utf-8"))
        for material in (
            {"note": [view]},
            {"note": (view,)},
            {"note": {"inner": view}},
            {view: CLEAN},
            collections.UserDict({"note": view}),
            collections.UserList([view]),
        ):
            self.assertFalse(_definite(module.classify_material(material)))

    def test_append_mv_in_list_as_mapping_value_redacts(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, {"note": [memoryview(hit)]}, scope="run one"
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 1)
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(hit, journal)

    def test_append_mv_in_mapping_as_mapping_value_redacts(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, {"note": {"inner": memoryview(hit)}}, scope="run one"
        )
        self.assertTrue(outcome["appended"])
        self.assertFalse(outcome["refused"])
        self.assertEqual(outcome["hits_redacted"], 1)

    def test_append_mv_as_mapping_key_does_not_append_unexamined(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        before = len(store["records"])
        outcome = module.append_redacted(
            store, {memoryview(hit): CLEAN}, scope="run one"
        )
        self.assertTrue(outcome["refused"])
        self.assertEqual(len(store["records"]), before)


class TestRedactFixR8GatheringAbstractAndWrapperViews(unittest.TestCase):
    """Ruling 221: abstract forms and views of wrapper mappings."""

    def _scan(self, module, value):
        return module.exit_scan({"note": value, "content": CLEAN})

    def _assert_refuses_whole(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_value_in_abstract_mapping_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, _AbstractMapping({"detail": hit}))
        )

    def test_hit_key_in_abstract_mapping_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, _AbstractMapping({hit: CLEAN}))
        )

    def test_hit_in_abstract_sequence_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, _AbstractSequence([hit]))
        )

    def test_hit_text_in_os_environ_nested_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        key = "ONTOLOOP_R8_HIT"
        os.environ[key] = hit.decode("utf-8")
        try:
            outcome = module.exit_scan(
                {"note": os.environ, "content": CLEAN}
            )
        finally:
            del os.environ[key]
        self._assert_refuses_whole(outcome)

    def test_hit_in_userdict_views_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        wrapped = collections.UserDict({"detail": hit})
        self._assert_refuses_whole(self._scan(module, wrapped.values()))
        self._assert_refuses_whole(self._scan(module, wrapped.items()))
        keyed = collections.UserDict({hit: CLEAN})
        self._assert_refuses_whole(self._scan(module, keyed.keys()))
        self._assert_refuses_whole(self._scan(module, keyed.items()))

    def test_hit_in_chainmap_views_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        wrapped = collections.ChainMap({"detail": hit})
        self._assert_refuses_whole(self._scan(module, wrapped.values()))
        self._assert_refuses_whole(self._scan(module, wrapped.items()))
        keyed = collections.ChainMap({hit: CLEAN})
        self._assert_refuses_whole(self._scan(module, keyed.keys()))
        self._assert_refuses_whole(self._scan(module, keyed.items()))

    def test_clean_abstract_and_wrapper_view_forms_still_release(self):
        module = require("ontoloop.redact")
        clean = CLEAN.encode("utf-8")
        forms = (
            _AbstractMapping({"detail": clean}),
            _AbstractMapping({CLEAN: "x"}),
            _AbstractSequence([clean]),
            collections.UserDict({"detail": clean}).values(),
            collections.UserDict({"detail": clean}).items(),
            collections.UserDict({CLEAN: "x"}).keys(),
            collections.ChainMap({"detail": clean}).values(),
            collections.ChainMap({"detail": clean}).items(),
            collections.ChainMap({CLEAN: "x"}).keys(),
        )
        for value in forms:
            outcome = self._scan(module, value)
            self.assertFalse(outcome["refused"], "clean: %r" % (value,))

    def test_wrapper_mappings_and_plain_views_still_refuse_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        self._assert_refuses_whole(
            self._scan(module, collections.UserDict({"detail": hit}))
        )
        self._assert_refuses_whole(
            self._scan(module, collections.ChainMap({"detail": hit}))
        )
        self._assert_refuses_whole(
            self._scan(module, {"detail": hit}.values())
        )
        self._assert_refuses_whole(self._scan(module, {hit: CLEAN}.keys()))


class TestRedactFixR8StateReadViewAssembly(unittest.TestCase):
    """Ruling 222: the state read on a top level view assembly."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def _base(self):
        return {"assembly_state": "scan cannot run", "content": CLEAN}

    def test_items_view_assembly_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        self._assert_fails_closed(module.exit_scan(self._base().items()))

    def test_values_view_assembly_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        self._assert_fails_closed(module.exit_scan(self._base().values()))

    def test_keys_view_assembly_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        self._assert_fails_closed(module.exit_scan(self._base().keys()))

    def test_plain_mapping_cannot_run_control_fails_closed(self):
        module = require("ontoloop.redact")
        self._assert_fails_closed(module.exit_scan(self._base()))

    def test_items_view_assembly_carrying_hit_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = {"note": hit, "content": CLEAN}.items()
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_view_assembly_clean_content_still_releases(self):
        module = require("ontoloop.redact")
        assembly = {"assembly_state": "ready", "content": CLEAN}.items()
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])


if __name__ == "__main__":
    unittest.main()
