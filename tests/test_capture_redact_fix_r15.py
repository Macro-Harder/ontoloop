"""Fix round 15 tests for Region 5: capture and redact.

Written first for one position at Round 15
triage ruling 529: R15-CR-1, the redact floor
gathering skipping a top level items view element
whole, counting none of the content it carries
beside the state entry, so an assembly carrying
clean content beside its state entry in that form
alone fails closed. No act here touches
ontoloop/capture.py. No test here pins the
KeyError or ValueError limbs inside ruling 491
as defects: those limbs stand NOT A DEFECT in
exactly those limbs and stand in their parity
standing. No test here reopens ruling 492: its
cure stands in its bounded nested form and the
nested forms stand pinned here as controls only.
No act here touches the material gathering act
or the state read act.
"""

import collections
import types
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
STATES = ("scan cannot run", "ready", "some unknown state")


class _SequenceContainer(collections.abc.Sequence):
    """A container element standing in the abstract sequence form."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


class _SetContainer(collections.abc.Set):
    """A container element standing in the abstract set form."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items


def _mapping_forms(state, with_content=True):
    base = {"assembly_state": state}
    if with_content:
        base["note"] = CLEAN
    return {
        "plain dict": dict(base),
        "UserDict": collections.UserDict(base),
        "OrderedDict": collections.OrderedDict(base),
        "ChainMap": collections.ChainMap(dict(base)),
        "mapping proxy": types.MappingProxyType(dict(base)),
    }


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


class TestRedactFixR15TopLevelItemsViewElement(unittest.TestCase):
    """Ruling 529, R15-CR-1: the top level items view element form."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["form"], "no exit scan result, no exit")

    def _assert_releases(self, outcome):
        self.assertFalse(outcome["refused"])

    def _scan(self, assembly):
        module = require("ontoloop.redact")
        return module.exit_scan(assembly)

    def _floor(self, assembly):
        module = require("ontoloop.redact")
        return module._assembly_content(
            assembly, _skip_top_state=True
        )

    def test_list_items_view_element_releases_ready(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan([mapping.items()]))

    def test_list_items_view_element_releases_unknown_state(self):
        mapping = {
            "assembly_state": "some unknown state",
            "note": CLEAN,
        }
        self._assert_releases(self._scan([mapping.items()]))

    def test_tuple_items_view_element_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state, "note": CLEAN}
                self._assert_releases(
                    self._scan((mapping.items(),))
                )

    def test_deque_items_view_element_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state, "note": CLEAN}
                self._assert_releases(
                    self._scan(
                        collections.deque([mapping.items()])
                    )
                )

    def test_userlist_items_view_element_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state, "note": CLEAN}
                self._assert_releases(
                    self._scan(
                        collections.UserList([mapping.items()])
                    )
                )

    def test_abstract_sequence_items_view_element_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state, "note": CLEAN}
                self._assert_releases(
                    self._scan(
                        _SequenceContainer([mapping.items()])
                    )
                )

    def test_abstract_set_items_view_element_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state, "note": CLEAN}
                self._assert_releases(
                    self._scan(_SetContainer([mapping.items()]))
                )

    def test_floor_counts_content_beside_state_on_items_element(
        self,
    ):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self.assertEqual(
            self._floor([mapping.items()]), ["note", CLEAN]
        )
        self.assertEqual(
            self._floor((mapping.items(),)), ["note", CLEAN]
        )

    def test_floor_counts_content_for_each_mapping_form(self):
        for name, mapping in _mapping_forms("ready").items():
            with self.subTest(mapping_form=name):
                self.assertEqual(
                    self._floor([mapping.items()]),
                    ["note", CLEAN],
                )

    def test_items_view_element_releases_for_each_mapping_form(
        self,
    ):
        for name, mapping in _mapping_forms("ready").items():
            with self.subTest(mapping_form=name):
                self._assert_releases(
                    self._scan([mapping.items()])
                )

    def test_items_element_releases_unknown_each_mapping_form(
        self,
    ):
        forms = _mapping_forms("some unknown state")
        for name, mapping in forms.items():
            with self.subTest(mapping_form=name):
                self._assert_releases(
                    self._scan([mapping.items()])
                )

    def test_state_only_items_view_element_still_fails_closed(
        self,
    ):
        for state in STATES:
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan([mapping.items()])
                )

    def test_state_only_items_element_in_tuple_fails_closed(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(
                    self._scan((mapping.items(),))
                )

    def test_floor_counts_no_content_on_state_only_items_element(
        self,
    ):
        mapping = {"assembly_state": "some unknown state"}
        self.assertEqual(self._floor([mapping.items()]), [])

    def test_top_level_items_view_itself_still_releases(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan(mapping.items()))
        self.assertEqual(
            self._floor(mapping.items()), ["note", CLEAN]
        )

    def test_top_level_items_view_state_only_still_fails_closed(
        self,
    ):
        mapping = {"assembly_state": "some unknown state"}
        self._assert_fails_closed(self._scan(mapping.items()))

    def test_keys_view_element_still_releases_with_content(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan([mapping.keys()]))
        self.assertEqual(self._floor([mapping.keys()]), ["note"])

    def test_values_view_element_still_releases_with_content(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan([mapping.values()]))
        self.assertEqual(
            self._floor([mapping.values()]), [CLEAN]
        )

    def test_nested_items_view_element_still_releases(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan([(mapping.items(),)]))
        self.assertEqual(
            self._floor([(mapping.items(),)]),
            ["note", CLEAN],
        )

    def test_list_and_set_of_pairs_still_release(self):
        pairs = [
            ("assembly_state", "ready"),
            ("note", CLEAN),
        ]
        self._assert_releases(self._scan([list(pairs)]))
        self._assert_releases(self._scan([set(pairs)]))

    def test_hit_beside_state_inside_viewed_mapping_refuses(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        mapping = {"assembly_state": "ready", "note": hit}
        outcome = module.exit_scan([mapping.items(), CLEAN])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_hit_as_state_value_beside_clean_content_refuses(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        assembly = [
            ("assembly_state", hit),
            ("content", CLEAN),
        ]
        outcome = module.exit_scan(assembly)
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_clean_ready_pair_assembly_still_releases(self):
        outcome = self._scan(
            [
                ("assembly_state", "ready"),
                ("content", CLEAN),
            ]
        )
        self._assert_releases(outcome)


if __name__ == "__main__":
    unittest.main()
