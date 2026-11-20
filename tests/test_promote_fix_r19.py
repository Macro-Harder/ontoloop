"""Fix round 19 tests for Region 3: promote wrapper.

Written first for one position at Round 19 triage
ruling 726 (R19-PRO-1, Low): single use material
standing in a subclass of a named container form,
whose iteration act delegates to one stored iterator,
clearing through the promote wrapper, where the direct
act decides the same presentations in their firing
forms. The named container forms stand beside ruling
668, which recognises single use by standing container
forms alone. Rulings 616, 668, and 669 stand cured in
their charged forms and stand not reopened by any pin
here: their forms stand as controls.
"""

import unittest
from collections import ChainMap, deque, UserList
from collections.abc import Mapping, Sequence, Set as AbstractSet

from tests.harness import require

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _nested_position(text=HOLDOUT_TEXT):
    return {"key": {"inner": {"text": text}}}


class ListSubclass(list):
    """A list subclass carrying no stored elements of
    its own, whose iteration act returns one stored
    list iterator on each call."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class TupleSubclass(tuple):
    """A tuple subclass in the same delegating form."""

    def __new__(cls, items):
        instance = super().__new__(cls, ())
        instance._stored = iter(list(items))
        return instance

    def __init__(self, items):
        pass

    def __iter__(self):
        return self._stored


class DequeSubclass(deque):
    """A deque subclass in the same delegating form."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class SetSubclass(set):
    """A set subclass in the same delegating form."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class FrozensetSubclass(frozenset):
    """A frozenset subclass in the same delegating form."""

    def __new__(cls, items):
        instance = super().__new__(cls, ())
        instance._stored = iter(list(items))
        return instance

    def __init__(self, items):
        pass

    def __iter__(self):
        return self._stored


class UserListSubclass(UserList):
    """A UserList subclass in the same delegating form."""

    def __init__(self, items):
        super().__init__()
        self.data = []
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class SequenceSubclass(Sequence):
    """A subclass of the abstract Sequence form whose
    iteration act delegates to one stored iterator."""

    def __init__(self, items):
        self._items = list(items)
        self._stored = iter(list(items))

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        return self._stored


class AbstractSetSubclass(AbstractSet):
    """A subclass of the abstract Set form whose
    iteration act delegates to one stored iterator."""

    def __init__(self, items):
        self._items = list(items)
        self._stored = iter(list(items))

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return self._stored


class DictSubclass(dict):
    """A dict subclass in the same delegating form,
    standing in parity between the acts, the direct
    act reaching no comparison on this presentation."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class MappingSubclass(Mapping):
    """A subclass of the abstract Mapping form whose
    iteration act delegates to one stored iterator
    over its one key, standing in parity between the
    acts in the same way. It stands presented as the
    holdout mapping itself, its one key standing as
    the holdout_items key."""

    def __init__(self, item):
        self._data = {"holdout_items": item}
        self._stored = iter(["holdout_items"])

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return self._stored


class StrSubclass(str):
    """A str subclass in the same delegating form,
    standing in parity between the acts."""

    def __new__(cls, items):
        instance = super().__new__(cls, "")
        instance._stored = iter(list(items))
        return instance

    def __init__(self, items):
        pass

    def __iter__(self):
        return self._stored


_SUBCLASS_FORMS = (
    ListSubclass,
    TupleSubclass,
    DequeSubclass,
    SetSubclass,
    FrozensetSubclass,
    UserListSubclass,
    SequenceSubclass,
    AbstractSetSubclass,
)


class _WrapperCase(unittest.TestCase):
    def _wrapper(self, holdout_material, items=None, **kwargs):
        module = require("ontoloop.promote")
        if items is None:
            items = [{"instruction_text": HOLDOUT_TEXT}]
        bundle = {
            "instruction_items": items,
            "holdout_items": holdout_material,
        }
        return module.test_instruction_items_against_holdout(
            bundle, occasion="promotion", **kwargs
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


class TestPromoteFixR19SubclassForms(_WrapperCase):
    """Ruling 726, R19-PRO-1: single use material in a
    subclass of a named container form."""

    def test_list_subclass_fires_through_wrapper(self):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": ListSubclass([_nested_position()])}
            )
            self._assert_fires(outcome)

    def test_tuple_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": TupleSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_deque_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": DequeSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_set_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": SetSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_frozenset_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": FrozensetSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_userlist_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": UserListSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_sequence_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": SequenceSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_abstract_set_subclass_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": AbstractSetSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_direct_act_fires_on_fresh_subclass_presentations(self):
        for factory in _SUBCLASS_FORMS:
            with self.subTest(factory=factory.__name__):
                outcome = self._direct(
                    {"holdout_items": factory([_nested_position()])}
                )
                self.assertTrue(outcome["fired"])
                self.assertEqual(outcome["comparisons"], 1)

    def test_list_subclass_two_nested_mappings_fires(self):
        outcome = self._wrapper(
            {"holdout_items": ListSubclass(
                [_nested_position(), _nested_position()])}
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 2
        )

    def test_list_subclass_holding_generator_fires(self):
        outcome = self._wrapper(
            {"holdout_items": ListSubclass(
                [(item for item in [_nested_position()])])}
        )
        self._assert_fires(outcome)

    def test_list_subclass_inside_mapping_value_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {"inner": ListSubclass(
                [_nested_position()])}}
        )
        self._assert_fires(outcome)

    def test_subclass_fires_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": ListSubclass([_nested_position()])
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_subclass_fires_after_partial_scoring(self):
        outcome = self._wrapper(
            {"holdout_items": ListSubclass([_nested_position()])},
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_subclass_fires_on_second_instruction_item(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        ]
        outcome = self._wrapper(
            {"holdout_items": ListSubclass([_nested_position()])},
            items=items,
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_subclass_forms_clear_through_wrapper(self):
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        for factory in (ListSubclass, TupleSubclass):
            with self.subTest(factory=factory.__name__):
                outcome = self._wrapper(
                    {"holdout_items": factory([clean_position])}
                )
                self._assert_clears(outcome)

    def test_detection_act_does_not_spend_subclass_forms(self):
        module = require("ontoloop.promote")
        for factory in (ListSubclass, DequeSubclass):
            with self.subTest(factory=factory.__name__):
                container = factory([_nested_position()])
                detected = module._wrapper_subtree_has_iterator(
                    container, frozenset()
                )
                self.assertTrue(detected)
                self.assertEqual(
                    list(container), [_nested_position()]
                )

    def test_materialised_subclass_reads_in_full_twice(self):
        module = require("ontoloop.promote")
        shared = require("ontoloop.cross_split_audit")
        material = module._materialise_holdout_for_wrapper(
            {"holdout_items": ListSubclass([_nested_position()])},
            shared,
        )
        for _trial in range(2):
            outcome = shared.audit_instruction_item(
                HOLDOUT_TEXT, material, occasion="promotion"
            )
            self.assertTrue(outcome["fired"])
            self.assertEqual(outcome["comparisons"], 1)

    def test_subclass_inside_tuple_stays_in_parity(self):
        make_holdout = lambda: {"holdout_items": (ListSubclass([_nested_position()]),)}
        outcome = self._wrapper(make_holdout())
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(make_holdout())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_tuple_subclass_inside_list_stays_in_parity(self):
        make_holdout = lambda: {"holdout_items": [TupleSubclass([_nested_position()])]}
        outcome = self._wrapper(make_holdout())
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(make_holdout())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_subclass_as_whole_holdout_stays_in_parity(self):
        wrapper_outcome = self._wrapper(ListSubclass([_nested_position()]))
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(ListSubclass([_nested_position()]))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_subclass_in_chainmap_value_stays_in_parity(self):
        wrapper_outcome = self._wrapper(
            ChainMap({"holdout_items": ListSubclass([_nested_position()])})
        )
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(
            ChainMap({"holdout_items": ListSubclass([_nested_position()])})
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_subclass_at_pairs_key_stays_in_parity(self):
        wrapper_outcome = self._wrapper(
            {"pairs": ListSubclass([_nested_position()])}
        )
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(
            {"pairs": ListSubclass([_nested_position()])}
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_dict_subclass_stays_in_parity(self):
        wrapper_outcome = self._wrapper(
            {"holdout_items": DictSubclass([_nested_position()])}
        )
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(
            {"holdout_items": DictSubclass([_nested_position()])}
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_mapping_subclass_stays_in_parity(self):
        wrapper_outcome = self._wrapper(
            MappingSubclass(_nested_position())
        )
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(
            MappingSubclass(_nested_position())
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_str_subclass_stays_in_parity(self):
        wrapper_outcome = self._wrapper(
            {"holdout_items": StrSubclass([_nested_position()])}
        )
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(
            {"holdout_items": StrSubclass([_nested_position()])}
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
