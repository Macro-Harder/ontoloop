"""Fix round 21 tests for Region 3: promote wrapper.

Written first for two positions at Round 21 triage
rulings 847 (R21-PRO-1, Low) and 848 (R21-PRO-2, Low).
Ruling 847: a delegating container subclass, an
abstract Sequence subclass or a list subclass,
standing as an item of a delegating ChainMap subclass
at a mapping presented position, clearing through the
promote wrapper where the direct act fires on the
presentation, because the ChainMap listing hands the
subclass to the direct act in element position, where
the presentation as presented carries it in key
position. Ruling 848: a single pass iterable, a
generator or a plain iterator, standing as an item of
a delegating ChainMap subclass at a mapping presented
position, firing through the promote wrapper where
the direct act clears the presentation, because the
ChainMap listing hands its nested mapping to the
direct act in element position, where the presentation
as presented carries the iterable in key position,
a position the direct act does not list. Rulings 726,
784, and 785 stand cured in their bounded forms and
stand not reopened by any pin here: their charged
forms stand as controls.
"""

import unittest
from collections import ChainMap
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


class DelegatingChainMapSubclass(ChainMap):
    """A subclass of ChainMap carrying no maps of its
    own, whose iteration act returns one stored
    iterator on each call."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class GetitemOnlyForm:
    """A form carrying no iter act, whose getitem act
    returns the next element of one stored iterator
    in sequence, in the governed getitem only form."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __getitem__(self, index):
        return next(self._stored)


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


class TestPromoteFixR21ContainerItemOfChainMap(_WrapperCase):
    """Ruling 847, R21-PRO-1: a delegating container
    subclass standing as an item of a delegating
    ChainMap subclass."""

    def test_sequence_subclass_item_fires_through_wrapper(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_nested_position()])]
                )
            }
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_nested_position()])]
                )
            }
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_list_subclass_item_fires_through_wrapper(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [ListSubclass([_nested_position()])]
                )
            }
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [ListSubclass([_nested_position()])]
                )
            }
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_sequence_subclass_item_two_nested_mappings(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [
                        SequenceSubclass(
                            [_nested_position(), _nested_position()]
                        )
                    ]
                )
            }
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 2
        )
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [
                        SequenceSubclass(
                            [_nested_position(), _nested_position()]
                        )
                    ]
                )
            }
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 2)

    def test_sequence_item_chainmap_inside_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [SequenceSubclass([_nested_position()])]
                    )
                }
            }
        )
        self._assert_fires(outcome)

    def test_sequence_item_chainmap_two_mapping_levels_in(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": {
                        "deeper": DelegatingChainMapSubclass(
                            [SequenceSubclass([_nested_position()])]
                        )
                    }
                }
            }
        )
        self._assert_fires(outcome)

    def test_sequence_item_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_nested_position()])]
                )
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_sequence_item_after_partial_scoring(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_nested_position()])]
                )
            },
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_sequence_item_through_two_item_test(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_nested_position()])]
                )
            },
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_sequence_subclass_item_clears(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_clean_position()])]
                )
            }
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SequenceSubclass([_clean_position()])]
                )
            }
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_clean_list_subclass_item_clears(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [ListSubclass([_clean_position()])]
                )
            }
        )
        self._assert_clears(outcome)

    def test_abstract_set_subclass_item_stays_in_parity(self):
        make_holdout = lambda: {
            "holdout_items": DelegatingChainMapSubclass(
                [AbstractSetSubclass([_nested_position()])]
            )
        }
        outcome = self._wrapper(make_holdout())
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(make_holdout())
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_chainmap_subclass_item_stays_in_parity(self):
        make_holdout = lambda: {
            "holdout_items": DelegatingChainMapSubclass(
                [DelegatingChainMapSubclass([_nested_position()])]
            )
        }
        outcome = self._wrapper(make_holdout())
        self._assert_clears(outcome)
        direct_outcome = self._direct(make_holdout())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_plain_container_items_stay_in_parity(self):
        for make_item in (
            lambda: (_nested_position(),),
            lambda: [_nested_position()],
            lambda: _nested_position(),
        ):
            with self.subTest(make_item=make_item):
                outcome = self._wrapper(
                    {
                        "holdout_items": DelegatingChainMapSubclass(
                            [make_item()]
                        )
                    }
                )
                self._assert_fires(outcome)

    def test_chainmap_holding_hit_inside_tuple_stays_in_parity(self):
        make_holdout = lambda: {
            "holdout_items": (
                DelegatingChainMapSubclass([_nested_position()]),
            )
        }
        outcome = self._wrapper(make_holdout())
        self._assert_clears(outcome)
        direct_outcome = self._direct(make_holdout())
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_chainmap_holding_hit_inside_list_stays_in_parity(self):
        make_holdout = lambda: {
            "holdout_items": [
                DelegatingChainMapSubclass([_nested_position()])
            ]
        }
        outcome = self._wrapper(make_holdout())
        self._assert_clears(outcome)
        direct_outcome = self._direct(make_holdout())
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_charged_chainmap_form_still_fires(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_nested_position()]
                )
            }
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )

    def test_charged_abstract_inside_tuple_still_clears(self):
        make_holdout = lambda: {
            "holdout_items": (
                SequenceSubclass([_nested_position()]),
            )
        }
        outcome = self._wrapper(make_holdout())
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(make_holdout())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)


class TestPromoteFixR21SinglePassItemOfChainMap(_WrapperCase):
    """Ruling 848, R21-PRO-2: a single pass iterable
    standing as an item of a delegating ChainMap
    subclass."""

    def test_generator_item_clears_through_wrapper(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_generator_of(_nested_position())]
                )
            }
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_generator_of(_nested_position())]
                )
            }
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_plain_iterator_item_clears_through_wrapper(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [iter([_nested_position()])]
                )
            }
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [iter([_nested_position()])]
                )
            }
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_single_pass_iterable_item_clears(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SinglePassIterable([_nested_position()])]
                )
            }
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [SinglePassIterable([_nested_position()])]
                )
            }
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_generator_item_chainmap_inside_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [_generator_of(_nested_position())]
                    )
                }
            }
        )
        self._assert_clears(outcome)

    def test_generator_item_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": DelegatingChainMapSubclass(
                    [_generator_of(_nested_position())]
                )
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_clean_generator_item_clears(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_generator_of(_clean_position())]
                )
            }
        )
        self._assert_clears(outcome)

    def test_clean_plain_iterator_item_clears(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [iter([_clean_position()])]
                )
            }
        )
        self._assert_clears(outcome)

    def test_generator_inside_list_subclass_still_fires(self):
        outcome = self._wrapper(
            {
                "holdout_items": ListSubclass(
                    [_generator_of(_nested_position())]
                )
            }
        )
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": ListSubclass(
                    [_generator_of(_nested_position())]
                )
            }
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_generator_inside_tuple_as_mapping_value_fires(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": (_generator_of(_nested_position()),)
                }
            }
        )
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": {
                    "inner": (_generator_of(_nested_position()),)
                }
            }
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_generator_as_key_of_plain_mapping_clears(self):
        def make_material():
            return {
                "holdout_items": {
                    _generator_of(_nested_position()): "clean value"
                }
            }

        outcome = self._wrapper(make_material())
        self._assert_clears(outcome)
        direct_outcome = self._direct(make_material())
        self.assertFalse(direct_outcome["fired"])

    def test_getitem_only_item_stays_in_parity(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [GetitemOnlyForm([_nested_position()])]
                )
            }
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [GetitemOnlyForm([_nested_position()])]
                )
            }
        )
        self.assertFalse(direct_outcome["fired"])


if __name__ == "__main__":
    unittest.main()
