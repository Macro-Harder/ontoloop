"""Fix round 16 tests for Region 5: promote wrapper and redact.

Written first for two positions at Round 16 triage
rulings 570 and 571: ruling 570 (R16-PRO-1, Low), the
promote wrapper materialisation in promote.py standing
the holdout material in a form the direct act reads, in
the set and frozenset forms, in the ChainMap form with
its maps order standing as the chain carries it, and in
the wrapped nested mapping forms, so verbatim holdout
content presented in each such form fires at the
promotion occasion through the wrapper in parity with
the direct act; and ruling 571 (R16-CR-1, Low), the
redact floor gathering under the _skip_top_state flag
counting the content a top level element in a mapping
form, a set form carrying a member beyond the pair, and
an indexable sequence form carrying an element beyond
the pair carries beside the state entry. No act here
touches ontoloop/capture.py as a product act: capture.py
stands named as a standing test home surface of this
region and carries no act in this round. No act here
touches any direct act reading in
ontoloop/cross_split_audit.py, and no line of
cross_split_audit.py stands changed by the ruling 570
cure in this region. No test here pins the KeyError,
ValueError, or TypeError terminator forms of ruling 491
as defects, and no test here touches the material
gathering act or the state read act.
"""

import collections
import types
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"
STATES = ("scan cannot run", "ready", "some unknown state")

CANDIDATE = {
    "group": "g1",
    "signature": "s1",
    "text": "shared bundle text alpha",
    "split": "candidate",
}
HOLDOUT_ITEM = {"text": HOLDOUT_TEXT, "split": "holdout"}
CLEAN_HOLDOUT_ITEM = {"text": "unrelated wording entirely",
                      "split": "holdout"}


class HashableItem(dict):
    """A mapping item that can stand inside a set."""

    __hash__ = object.__hash__


class _SequenceContainer(collections.abc.Sequence):
    """A container standing in the abstract sequence form."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


class _SetContainer(collections.abc.Set):
    """A container standing in the abstract set form."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items


class _MappingContainer(collections.abc.Mapping):
    """A mapping standing in the abstract mapping form."""

    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, key):
        return self._items[key]


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
        "abstract mapping": _MappingContainer(base),
    }


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


def _nested_position(text=HOLDOUT_TEXT):
    return {"key": {"inner": {"text": text}}}


class TestRedactFixR16TopLevelElementForms(unittest.TestCase):
    """Ruling 571, R16-CR-1: the three remaining forms of
    _is_top_state_entry at the redact floor gathering."""

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

    def test_list_mapping_element_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                mapping = {"assembly_state": state, "note": CLEAN}
                self._assert_releases(self._scan([mapping]))

    def test_mapping_element_in_container_assemblies_releases(self):
        forms = (
            ("tuple", lambda el: (el,)),
            ("deque", lambda el: collections.deque([el])),
            ("UserList", lambda el: collections.UserList([el])),
            ("abstract sequence",
             lambda el: _SequenceContainer([el])),
            ("abstract set", lambda el: _SetContainer([el])),
        )
        for name, form in forms:
            for state in ("ready", "some unknown state"):
                with self.subTest(form=name, state=state):
                    mapping = {"assembly_state": state, "note": CLEAN}
                    self._assert_releases(self._scan(form(mapping)))

    def test_floor_counts_content_beside_state_on_mapping_element(
        self,
    ):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self.assertEqual(self._floor([mapping]), [CLEAN])
        self.assertEqual(self._floor((mapping,)), [CLEAN])

    def test_mapping_element_releases_for_each_mapping_form(self):
        for name, mapping in _mapping_forms("ready").items():
            with self.subTest(mapping_form=name):
                self._assert_releases(self._scan([mapping]))

    def test_mapping_element_unknown_state_each_mapping_form(self):
        forms = _mapping_forms("some unknown state")
        for name, mapping in forms.items():
            with self.subTest(mapping_form=name):
                self._assert_releases(self._scan([mapping]))

    def test_set_element_with_member_beyond_pair_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                element = {"assembly_state", state, CLEAN}
                self._assert_releases(self._scan([element]))

    def test_frozenset_element_with_member_beyond_pair_releases(
        self,
    ):
        element = frozenset({"assembly_state", "ready", CLEAN})
        self._assert_releases(self._scan([element]))

    def test_floor_counts_content_on_set_element_beyond_pair(self):
        element = {"assembly_state", "ready", CLEAN}
        floor = self._floor([element])
        self.assertIn(CLEAN, floor)
        self.assertNotIn("assembly_state", floor)

    def test_abstract_set_element_beyond_pair_releases(self):
        element = _SetContainer(["assembly_state", "ready", CLEAN])
        self._assert_releases(self._scan([element]))

    def test_sequence_element_with_element_beyond_pair_releases(
        self,
    ):
        forms = (
            ("list element", ["assembly_state", "ready", CLEAN]),
            ("tuple element", ("assembly_state", "ready", CLEAN)),
        )
        for name, element in forms:
            with self.subTest(form=name):
                self._assert_releases(self._scan([element]))

    def test_sequence_element_forms_beyond_pair_release(self):
        forms = (
            ("deque element",
             collections.deque(["assembly_state", "ready", CLEAN])),
            ("UserList element",
             collections.UserList(
                 ["assembly_state", "ready", CLEAN])),
            ("abstract sequence element",
             _SequenceContainer(["assembly_state", "ready", CLEAN])),
        )
        for name, element in forms:
            with self.subTest(form=name):
                self._assert_releases(self._scan([element]))

    def test_floor_counts_content_beyond_pair_on_sequence_element(
        self,
    ):
        self.assertEqual(
            self._floor([["assembly_state", "ready", CLEAN]]),
            [CLEAN],
        )
        self.assertEqual(
            self._floor([("assembly_state", "ready", CLEAN)]),
            [CLEAN],
        )

    def test_state_only_mapping_element_still_fails_closed(self):
        for state in STATES:
            with self.subTest(state=state):
                mapping = {"assembly_state": state}
                self._assert_fails_closed(self._scan([mapping]))
        mapping = {"assembly_state": "some unknown state"}
        self.assertEqual(self._floor([mapping]), [])

    def test_state_only_pair_elements_still_fail_closed(self):
        self._assert_fails_closed(
            self._scan([{"assembly_state", "ready"}])
        )
        self._assert_fails_closed(
            self._scan([["assembly_state", "ready"]])
        )
        self.assertEqual(
            self._floor([["assembly_state", "ready"]]), []
        )

    def test_top_level_and_nested_mapping_forms_still_decide(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan(dict(mapping)))
        self.assertEqual(self._floor(dict(mapping)), [CLEAN])
        self._assert_releases(self._scan([[dict(mapping)]]))
        pairs = [("assembly_state", "ready"), ("note", CLEAN)]
        self._assert_releases(self._scan([list(pairs)]))
        self._assert_releases(self._scan([set(pairs)]))

    def test_view_element_forms_still_decide(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(self._scan([mapping.items()]))
        self.assertEqual(
            self._floor([mapping.items()]), ["note", CLEAN]
        )
        self._assert_releases(self._scan([mapping.keys()]))
        self.assertEqual(self._floor([mapping.keys()]), ["note"])
        self._assert_releases(self._scan([mapping.values()]))
        self.assertEqual(self._floor([mapping.values()]), [CLEAN])

    def test_hit_beside_state_inside_mapping_element_refuses(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        mapping = {"assembly_state": "ready", "note": hit}
        outcome = module.exit_scan([mapping, CLEAN])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])

    def test_cannot_run_state_in_mapping_element_fails_closed(self):
        mapping = {"assembly_state": "scan cannot run", "note": CLEAN}
        self._assert_fails_closed(self._scan([mapping]))

    def test_mapping_element_beside_clean_pair_still_releases(self):
        mapping = {"assembly_state": "ready", "note": CLEAN}
        self._assert_releases(
            self._scan([mapping, ("content", CLEAN)])
        )


class TestPromoteFixR16WrapperMaterialisedForms(unittest.TestCase):
    """Ruling 570, R16-PRO-1: verbatim holdout content
    presented in materialised forms fires through the
    promote wrapper at the promotion occasion."""

    def _wrapper(self, holdout_material, items=None):
        module = require("ontoloop.promote")
        if items is None:
            items = [{"instruction_text": HOLDOUT_TEXT}]
        bundle = {
            "instruction_items": items,
            "holdout_items": holdout_material,
        }
        return module.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )

    def _direct(self, holdout_material):
        module = require("ontoloop.cross_split_audit")
        return module.audit_instruction_item(
            HOLDOUT_TEXT, holdout_material, occasion="promotion"
        )

    def _assert_fires(self, outcome):
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["promotion_proceeds"])

    def _assert_clears(self, outcome):
        self.assertFalse(outcome["fired"])
        self.assertTrue(
            outcome["test_result_carried_on_promotion_record"]
        )

    def test_set_pair_fires_through_wrapper_repeated_trials(self):
        for _trial in range(5):
            outcome = self._wrapper({"pairs": {
                HashableItem(CANDIDATE),
                HashableItem(HOLDOUT_ITEM),
            }})
            self._assert_fires(outcome)

    def test_frozenset_pair_fires_through_wrapper(self):
        outcome = self._wrapper({"pairs": frozenset({
            HashableItem(CANDIDATE),
            HashableItem(HOLDOUT_ITEM),
        })})
        self._assert_fires(outcome)

    def test_set_pair_clean_clears_through_wrapper(self):
        outcome = self._wrapper({"pairs": {
            HashableItem(CANDIDATE),
            HashableItem(CLEAN_HOLDOUT_ITEM),
        }})
        self._assert_clears(outcome)

    def test_chain_map_pair_fires_through_wrapper(self):
        outcome = self._wrapper({"pairs": collections.ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
        )})
        self._assert_fires(outcome)

    def test_chain_map_pair_clean_clears_through_wrapper(self):
        outcome = self._wrapper({"pairs": collections.ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(CLEAN_HOLDOUT_ITEM)},
        )})
        self._assert_clears(outcome)

    def test_wrapped_position_values_view_fires(self):
        outcome = self._wrapper(
            {"holdout_items": _nested_position().values()}
        )
        self._assert_fires(outcome)

    def test_wrapped_position_items_view_fires(self):
        outcome = self._wrapper(
            {"holdout_items": _nested_position().items()}
        )
        self._assert_fires(outcome)

    def test_wrapped_position_tuple_fires(self):
        outcome = self._wrapper(
            {"holdout_items": (_nested_position(),)}
        )
        self._assert_fires(outcome)

    def test_wrapped_position_deque_fires(self):
        outcome = self._wrapper(
            {"holdout_items": collections.deque([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_wrapped_position_generator_fires(self):
        outcome = self._wrapper(
            {"holdout_items": (
                entry for entry in [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_clean_wrapped_positions_clear_through_wrapper(self):
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        forms = (
            ("values view", lambda pos: pos.values()),
            ("items view", lambda pos: pos.items()),
            ("tuple", lambda pos: (pos,)),
            ("deque", lambda pos: collections.deque([pos])),
            ("generator", lambda pos: (
                entry for entry in [pos])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                outcome = self._wrapper(
                    {"holdout_items": form(clean_position)}
                )
                self._assert_clears(outcome)

    def test_wrapper_controls_still_fire(self):
        self._assert_fires(self._wrapper({"pairs": [
            dict(CANDIDATE), dict(HOLDOUT_ITEM),
        ]}))
        self._assert_fires(self._wrapper(
            {"holdout_items": _nested_position()}
        ))

    def test_direct_act_forms_still_decide(self):
        outcome = self._direct({"pairs": {
            HashableItem(CANDIDATE),
            HashableItem(HOLDOUT_ITEM),
        }})
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 2)
        outcome = self._direct({"pairs": collections.ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
        )})
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 1)
        outcome = self._direct(
            {"holdout_items": _nested_position().values()}
        )
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 1)

    def test_generator_holdout_fires_on_second_item(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        ]
        outcome = self._wrapper(
            (value for value in [{"text": HOLDOUT_TEXT}]),
            items=items,
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)


if __name__ == "__main__":
    unittest.main()
