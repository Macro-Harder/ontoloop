"""Fix round 22 tests for Region 3: promote wrapper.

Written first for two positions at Round 22 triage
rulings 909 (R22-PRO-1, Low) and 910 (R22-PRO-2, Low).
Ruling 909: a delegating container subclass standing
inside a container standing as an item of a delegating
ChainMap subclass at a mapping presented position,
clearing through the promote wrapper where the direct
act fires on the presentation, because the ChainMap
item materialisation hands the inner subclass to the
direct act in element position inside the container,
where the presentation as presented carries it in key
position inside a container standing in key position.
Ruling 910: a single pass iterable standing inside a
container standing as an item of a delegating ChainMap
subclass at a mapping presented position, firing
through the promote wrapper where the direct act
clears the presentation, because the ChainMap item
materialisation lists the iterable into element
position inside the container, where the presentation
as presented carries it in key position inside a
container standing in key position, a position the
direct act does not list. Rulings 847, 848, 726, 784,
and 785 stand cured in their bounded forms and stand
not reopened by any pin here: their charged forms and
the bounded parity positions the Round 22 Promote
paper names stand as controls.
"""

import unittest
from collections import ChainMap, deque, UserList
from collections.abc import Sequence, Set as AbstractSet

from tests.harness import require

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _nested_position(text=HOLDOUT_TEXT):
    return {"key": {"inner": {"text": text}}}


def _clean_position():
    return _nested_position("unrelated wording entirely")


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


class ListSubclass(list):
    """A list subclass whose iteration act delegates
    to one stored iterator."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class TupleSubclass(tuple):
    """A tuple subclass whose iteration act delegates
    to one stored iterator."""

    def __new__(cls, items):
        return super().__new__(cls, ())

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class SetSubclass(set):
    """A set subclass whose iteration act delegates
    to one stored iterator."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class DequeSubclass(deque):
    """A deque subclass whose iteration act delegates
    to one stored iterator."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class UserListSubclass(UserList):
    """A UserList subclass whose iteration act
    delegates to one stored iterator."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class DelegatingChainMapSubclass(ChainMap):
    """A subclass of ChainMap carrying no maps of its
    own, whose iteration act returns one stored
    iterator on each call."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


def _generator_of(item):
    return (element for element in [item])


class SinglePassIterable:
    """A general iterable carrying no next method of
    its own, whose iter act returns one stored
    iterator, standing listed once only."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


def _chainmap_item(item):
    return {
        "holdout_items": DelegatingChainMapSubclass([item])
    }


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

    def _assert_pair_fires(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def _assert_pair_clears(self, make_item, comparisons=None):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        if comparisons is not None:
            self.assertEqual(
                direct_outcome["comparisons"], comparisons
            )


class TestPromoteFixR22DelegatingInsideContainerItem(
    _WrapperCase
):
    """Ruling 909, R22-PRO-1: a delegating container
    subclass standing inside a container standing as
    an item of a delegating ChainMap subclass."""

    def test_tuple_carrying_sequence_subclass_fires(self):
        self._assert_pair_fires(
            lambda: (SequenceSubclass([_nested_position()]),)
        )

    def test_list_carrying_sequence_subclass_fires(self):
        self._assert_pair_fires(
            lambda: [SequenceSubclass([_nested_position()])]
        )

    def test_list_carrying_list_subclass_fires(self):
        self._assert_pair_fires(
            lambda: [ListSubclass([_nested_position()])]
        )

    def test_tuple_carrying_list_subclass_fires(self):
        self._assert_pair_fires(
            lambda: (ListSubclass([_nested_position()]),)
        )

    def test_deque_carrying_sequence_subclass_fires(self):
        self._assert_pair_fires(
            lambda: deque([SequenceSubclass([_nested_position()])])
        )

    def test_userlist_carrying_sequence_subclass_fires(self):
        self._assert_pair_fires(
            lambda: UserList(
                [SequenceSubclass([_nested_position()])]
            )
        )

    def test_tuple_in_tuple_carrying_sequence_fires(self):
        self._assert_pair_fires(
            lambda: ((SequenceSubclass([_nested_position()]),),)
        )

    def test_sequence_carrying_sequence_subclass_fires(self):
        self._assert_pair_fires(
            lambda: SequenceSubclass(
                [SequenceSubclass([_nested_position()])]
            )
        )

    def test_set_subclass_carrying_sequence_fires(self):
        self._assert_pair_fires(
            lambda: SetSubclass(
                [SequenceSubclass([_nested_position()])]
            )
        )

    def test_tuple_carrying_tuple_subclass_fires(self):
        self._assert_pair_fires(
            lambda: (TupleSubclass([_nested_position()]),)
        )

    def test_tuple_carrying_set_subclass_fires(self):
        self._assert_pair_fires(
            lambda: (SetSubclass([_nested_position()]),)
        )

    def test_deque_subclass_carrying_sequence_fires(self):
        self._assert_pair_fires(
            lambda: DequeSubclass(
                [SequenceSubclass([_nested_position()])]
            )
        )

    def test_userlist_subclass_carrying_sequence_fires(self):
        self._assert_pair_fires(
            lambda: UserListSubclass(
                [SequenceSubclass([_nested_position()])]
            )
        )

    def test_tuple_sequence_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                (SequenceSubclass([_nested_position()]),)
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_tuple_sequence_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item(
                (SequenceSubclass([_nested_position()]),)
            ),
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_tuple_sequence_chainmap_in_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [
                            (
                                SequenceSubclass(
                                    [_nested_position()]
                                ),
                            )
                        ]
                    )
                }
            }
        )
        self._assert_fires(outcome)

    def test_tuple_sequence_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item(
                (SequenceSubclass([_nested_position()]),)
            ),
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_tuple_carrying_sequence_clears(self):
        self._assert_pair_clears(
            lambda: (SequenceSubclass([_clean_position()]),),
            comparisons=1,
        )

    def test_clean_list_carrying_list_subclass_clears(self):
        self._assert_pair_clears(
            lambda: [ListSubclass([_clean_position()])],
            comparisons=1,
        )

    def test_clean_deque_carrying_sequence_clears(self):
        self._assert_pair_clears(
            lambda: deque([SequenceSubclass([_clean_position()])]),
            comparisons=1,
        )

    def test_abstract_set_carrying_sequence_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass(
                [SequenceSubclass([_nested_position()])]
            ),
            comparisons=0,
        )

    def test_tuple_carrying_abstract_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: (AbstractSetSubclass([_nested_position()]),),
            comparisons=0,
        )

    def test_chainmap_carrying_sequence_stays_parity(self):
        self._assert_pair_fires(
            lambda: DelegatingChainMapSubclass(
                [SequenceSubclass([_nested_position()])]
            )
        )

    def test_mapping_value_sequence_stays_parity(self):
        self._assert_pair_fires(
            lambda: {"k": SequenceSubclass([_nested_position()])}
        )

    def test_single_pass_carrying_sequence_stays_parity(self):
        self._assert_pair_clears(
            lambda: SinglePassIterable(
                [SequenceSubclass([_nested_position()])]
            ),
            comparisons=0,
        )


class TestPromoteFixR22SinglePassInsideContainerItem(
    _WrapperCase
):
    """Ruling 910, R22-PRO-2: a single pass iterable
    standing inside a container standing as an item of
    a delegating ChainMap subclass."""

    def test_tuple_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: (_generator_of(_nested_position()),),
            comparisons=0,
        )

    def test_list_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: [_generator_of(_nested_position())],
            comparisons=0,
        )

    def test_tuple_in_tuple_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: ((_generator_of(_nested_position()),),),
            comparisons=0,
        )

    def test_sequence_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: SequenceSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_list_subclass_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: ListSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_tuple_subclass_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: TupleSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_set_subclass_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: SetSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_deque_subclass_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: DequeSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_userlist_subclass_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: UserListSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_abstract_set_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_tuple_carrying_single_pass_iterable_clears(self):
        self._assert_pair_clears(
            lambda: (
                SinglePassIterable([_nested_position()]),
            ),
            comparisons=0,
        )

    def test_tuple_carrying_plain_iterator_clears(self):
        self._assert_pair_clears(
            lambda: (iter([_nested_position()]),),
            comparisons=0,
        )

    def test_tuple_generator_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                (_generator_of(_nested_position()),)
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_tuple_generator_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item((_generator_of(_nested_position()),)),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_tuple_generator_chainmap_in_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [(_generator_of(_nested_position()),)]
                    )
                }
            }
        )
        self._assert_clears(outcome)

    def test_sequence_generator_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item(
                SequenceSubclass(
                    [_generator_of(_nested_position())]
                )
            ),
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_list_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: [_generator_of(_clean_position())],
            comparisons=0,
        )

    def test_clean_sequence_carrying_generator_clears(self):
        self._assert_pair_clears(
            lambda: SequenceSubclass(
                [_generator_of(_clean_position())]
            ),
            comparisons=0,
        )

    def test_chainmap_carrying_generator_stays_parity(self):
        self._assert_pair_clears(
            lambda: DelegatingChainMapSubclass(
                [_generator_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_mapping_value_generator_stays_parity(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(_nested_position())}
        )

    def test_generator_carrying_generator_stays_parity(self):
        self._assert_pair_clears(
            lambda: _generator_of(
                _generator_of(_nested_position())
            ),
            comparisons=0,
        )

    def test_generator_carrying_sequence_stays_parity(self):
        self._assert_pair_clears(
            lambda: _generator_of(
                SequenceSubclass([_nested_position()])
            ),
            comparisons=0,
        )


if __name__ == "__main__":
    unittest.main()
