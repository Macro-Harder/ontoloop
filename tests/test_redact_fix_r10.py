"""Fix round 10 tests for Region 5: redact gathering and state read.

Written first for two positions at Round 10
triage ruling 334 point 5: ruling 319 (Lead Engineer
line E-10, the material gathering on a value standing
in a general iterable form) and ruling 320 (Lead
Engineer line E-11, the exit scan state read on a pair
standing in a deque form or in an abstract sequence
form). No test here pins the generator form ruled not
a defect at Round 6 ruling 133 as a defect. One test
here pins that the generator form stands untouched by
the ruling 319 cure, in its standing form.
"""

import collections
import collections.abc
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


class _GeneralIterable:
    """A container carrying an iteration act alone.

    The class stands in no sequence, set, mapping,
    view, or array form. It carries no length act, no
    indexed access act, and no containment act, and it
    carries no next act, so it stands as a container
    that can be read again, and not as an iterator.
    """

    def __init__(self, data):
        self._data = list(data)

    def __iter__(self):
        return iter(self._data)


class _AbstractSequence(collections.abc.Sequence):
    def __init__(self, data):
        self._data = list(data)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class _AbstractSet(collections.abc.Set):
    def __init__(self, data):
        self._data = set(data)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class TestRedactFixR10MaterialGeneralIterable(unittest.TestCase):
    """Ruling 319: hit material inside a general iterable container."""

    def _hit(self):
        return _hit_bytes(require("ontoloop.redact"))

    def _fires(self, material):
        module = require("ontoloop.redact")
        return _definite(module.classify_material(material))

    def test_hit_bytes_in_general_iterable_top_level_fires(self):
        self.assertTrue(self._fires(_GeneralIterable([self._hit()])))

    def test_hit_text_in_general_iterable_top_level_fires(self):
        hit_text = self._hit().decode("utf-8")
        self.assertTrue(self._fires(_GeneralIterable([hit_text])))

    def test_hit_in_general_iterable_as_mapping_value_fires(self):
        material = {"note": _GeneralIterable([self._hit()])}
        self.assertTrue(self._fires(material))

    def test_hit_in_general_iterable_inside_list_fires(self):
        self.assertTrue(self._fires([_GeneralIterable([self._hit()])]))

    def test_hit_in_general_iterable_inside_general_iterable_fires(self):
        material = _GeneralIterable([_GeneralIterable([self._hit()])])
        self.assertTrue(self._fires(material))

    def test_memoryview_in_general_iterable_fires(self):
        material = _GeneralIterable([memoryview(self._hit())])
        self.assertTrue(self._fires(material))

    def test_hit_in_general_iterable_as_mapping_key_fires(self):
        material = {_GeneralIterable([self._hit()]): CLEAN}
        self.assertTrue(self._fires(material))

    def test_clean_general_iterable_stays_clean(self):
        module = require("ontoloop.redact")
        clean = CLEAN.encode("utf-8")
        forms = (
            _GeneralIterable([clean]),
            {"note": _GeneralIterable([clean])},
            [_GeneralIterable([clean])],
            _GeneralIterable([_GeneralIterable([clean])]),
            {_GeneralIterable([clean]): CLEAN},
        )
        for material in forms:
            self.assertFalse(
                _definite(module.classify_material(material)),
                "clean form fired: %r" % (material,),
            )

    def test_append_general_iterable_hit_not_appended_unexamined(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        hit = _hit_bytes(module)
        store = store_module.golden_record_store()
        outcome = module.append_redacted(
            store, _GeneralIterable([hit]), scope="run one"
        )
        self.assertTrue(outcome["refused"] or outcome["hits_redacted"] == 1)
        journal = b"\n".join(
            record["canonical_bytes"] for record in store["records"]
        )
        self.assertNotIn(hit, journal)

    def test_cyclic_general_iterable_fails_closed(self):
        module = require("ontoloop.redact")
        container = _GeneralIterable([])
        container._data.append(container)
        result = module.classify_material(container)
        self.assertTrue(result.get("refused"))
        self.assertEqual(result.get("form"), "no exit scan result, no exit")

    def test_cyclic_general_iterable_append_refused(self):
        module = require("ontoloop.redact")
        store_module = require("ontoloop.store")
        container = _GeneralIterable([])
        container._data.append(container)
        store = store_module.golden_record_store()
        before = len(store["records"])
        outcome = module.append_redacted(store, container, scope="run one")
        self.assertTrue(outcome["refused"])
        self.assertFalse(outcome["appended"])
        self.assertEqual(len(store["records"]), before)

    def test_list_and_cured_abstract_forms_still_fire(self):
        hit = self._hit()
        self.assertTrue(self._fires([hit]))
        self.assertTrue(self._fires(_AbstractSequence([hit])))
        self.assertTrue(self._fires(_AbstractSet([hit])))

    def test_generator_form_stands_untouched(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)

        def _gen():
            yield hit

        generator = _gen()
        result = module.classify_material(generator)
        self.assertFalse(_definite(result))
        self.assertEqual(list(generator), [hit])


class TestRedactFixR10StateReadPairForms(unittest.TestCase):
    """Ruling 320: the state read on deque and abstract sequence pairs."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def test_state_value_read_on_deque_pair(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.deque(["assembly_state", "scan cannot run"]),
            collections.deque(["content", CLEAN]),
        ]
        self.assertEqual(
            module._assembly_state_value(assembly), "scan cannot run"
        )

    def test_state_value_read_on_abstract_sequence_pair(self):
        module = require("ontoloop.redact")
        assembly = [
            _AbstractSequence(["assembly_state", "scan cannot run"]),
            _AbstractSequence(["content", CLEAN]),
        ]
        self.assertEqual(
            module._assembly_state_value(assembly), "scan cannot run"
        )

    def test_list_of_deque_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.deque(["assembly_state", "scan cannot run"]),
            collections.deque(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_list_of_abstract_sequence_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            _AbstractSequence(["assembly_state", "scan cannot run"]),
            _AbstractSequence(["content", CLEAN]),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_deque_of_deque_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = collections.deque(
            [
                collections.deque(["assembly_state", "scan cannot run"]),
                collections.deque(["content", CLEAN]),
            ]
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_tuple_of_deque_pairs_cannot_run_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = (
            collections.deque(["assembly_state", "scan cannot run"]),
            collections.deque(["content", CLEAN]),
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_list_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = [
            ("assembly_state", "scan cannot run"),
            ("content", CLEAN),
        ]
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_userlist_pair_control_still_fails_closed(self):
        module = require("ontoloop.redact")
        assembly = collections.UserList(
            [
                ("assembly_state", "scan cannot run"),
                ("content", CLEAN),
            ]
        )
        self._assert_fails_closed(module.exit_scan(assembly))

    def test_hit_in_deque_pair_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = [
            collections.deque(["note", hit]),
            collections.deque(["content", CLEAN]),
        ]
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_in_abstract_sequence_pair_refuses_whole(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = [
            _AbstractSequence(["note", hit]),
            _AbstractSequence(["content", CLEAN]),
        ]
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_ready_deque_pair_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.deque(["assembly_state", "ready"]),
            collections.deque(["content", CLEAN]),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_ready_abstract_sequence_pair_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            _AbstractSequence(["assembly_state", "ready"]),
            _AbstractSequence(["content", CLEAN]),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_clean_deque_pair_without_state_entry_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            collections.deque(["note", CLEAN]),
            collections.deque(["content", CLEAN]),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])

    def test_clean_abstract_sequence_pair_without_state_releases(self):
        module = require("ontoloop.redact")
        assembly = [
            _AbstractSequence(["note", CLEAN]),
            _AbstractSequence(["content", CLEAN]),
        ]
        outcome = module.exit_scan(assembly)
        self.assertFalse(outcome["refused"])


if __name__ == "__main__":
    unittest.main()
