"""Fix round 20 tests for Region 3: promote wrapper.

Written first for two positions at Round 20 triage
rulings 784 (R20-PRO-1, Low) and 785 (Lead Engineer
line E-19, Low). Ruling 784: single use material
standing in a delegating abstract form subclass, an
abstract Sequence or an abstract Set subclass whose
iteration act delegates to one stored iterator,
standing inside a container at a position outside
the mapping presentation, firing through the promote
wrapper where the direct act clears the presentation
as presented. Ruling 785: holdout material presented
through the promote wrapper in a subclass of
ChainMap whose iteration act delegates to one stored
iterator, raising an ungoverned TypeError through
the wrapper on hit material and on clean material
alike, where the direct act fires on the hit form
and clears on a comparison on the clean form.
Ruling 726 stands cured in its bounded form and
stands not reopened by any pin here: its charged
forms stand as controls.
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
    """A list subclass in the delegating form of
    ruling 726, standing as a control."""

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

    def _assert_parity_clears(self, make_material):
        wrapper_outcome = self._wrapper(make_material())
        self._assert_clears(wrapper_outcome)
        direct_outcome = self._direct(make_material())
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


class TestPromoteFixR20AbstractInsideContainer(_WrapperCase):
    """Ruling 784, R20-PRO-1: a delegating abstract
    form subclass standing inside a container."""

    def test_sequence_subclass_inside_tuple_clears(self):
        for _trial in range(3):
            self._assert_parity_clears(
                lambda: {
                    "holdout_items": (
                        SequenceSubclass([_nested_position()]),
                    )
                }
            )

    def test_abstract_set_subclass_inside_tuple_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": (
                    AbstractSetSubclass([_nested_position()]),
                )
            }
        )

    def test_sequence_subclass_inside_list_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": [
                    SequenceSubclass([_nested_position()])
                ]
            }
        )

    def test_abstract_set_subclass_inside_list_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": [
                    AbstractSetSubclass([_nested_position()])
                ]
            }
        )

    def test_sequence_subclass_inside_deque_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": deque(
                    [SequenceSubclass([_nested_position()])]
                )
            }
        )

    def test_sequence_subclass_inside_userlist_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": UserList(
                    [SequenceSubclass([_nested_position()])]
                )
            }
        )

    def test_sequence_subclass_inside_frozenset_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": frozenset(
                    [SequenceSubclass([_nested_position()])]
                )
            }
        )

    def test_sequence_subclass_as_second_list_element_clears(self):
        def make_material():
            return {
                "holdout_items": [
                    _clean_position(),
                    SequenceSubclass([_nested_position()]),
                ]
            }

        wrapper_outcome = self._wrapper(make_material())
        self._assert_clears(wrapper_outcome)
        direct_outcome = self._direct(make_material())
        self.assertFalse(direct_outcome["fired"])

    def test_sequence_subclass_inside_tuple_as_mapping_value_clears(
        self,
    ):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": {
                    "inner": (
                        SequenceSubclass([_nested_position()]),
                    )
                }
            }
        )

    def test_sequence_subclass_inside_sequence_subclass_clears(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": SequenceSubclass(
                    [SequenceSubclass([_nested_position()])]
                )
            }
        )

    def test_abstract_inside_container_at_candidate_construction(
        self,
    ):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": (
                    SequenceSubclass([_nested_position()]),
                )
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_abstract_inside_container_after_partial_scoring(self):
        outcome = self._wrapper(
            {
                "holdout_items": (
                    SequenceSubclass([_nested_position()]),
                )
            },
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_clean_abstract_inside_container_clears(self):
        for container in (
            lambda item: (item,),
            lambda item: [item],
        ):
            with self.subTest(container=container):
                outcome = self._wrapper(
                    {
                        "holdout_items": container(
                            SequenceSubclass([_clean_position()])
                        )
                    }
                )
                self._assert_clears(outcome)

    def test_abstract_at_mapping_position_still_fires(self):
        outcome = self._wrapper(
            {"holdout_items": SequenceSubclass([_nested_position()])}
        )
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            {"holdout_items": SequenceSubclass([_nested_position()])}
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_abstract_set_at_mapping_position_still_fires(self):
        outcome = self._wrapper(
            {
                "holdout_items": AbstractSetSubclass(
                    [_nested_position()]
                )
            }
        )
        self._assert_fires(outcome)

    def test_concrete_subclass_inside_tuple_stays_in_parity(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": (
                    ListSubclass([_nested_position()]),
                )
            }
        )

    def test_sequence_as_whole_holdout_stays_in_parity(self):
        self._assert_parity_clears(
            lambda: SequenceSubclass([_nested_position()])
        )

    def test_sequence_in_chainmap_value_stays_in_parity(self):
        self._assert_parity_clears(
            lambda: ChainMap(
                {
                    "holdout_items": SequenceSubclass(
                        [_nested_position()]
                    )
                }
            )
        )

    def test_sequence_at_pairs_key_stays_in_parity(self):
        self._assert_parity_clears(
            lambda: {"pairs": SequenceSubclass([_nested_position()])}
        )

    def test_sequence_inside_mapping_inside_list_fires(self):
        def make_material():
            return {
                "holdout_items": [
                    {"inner": SequenceSubclass([_nested_position()])}
                ]
            }

        wrapper_outcome = self._wrapper(make_material())
        self._assert_fires(wrapper_outcome)
        direct_outcome = self._direct(make_material())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_list_subclass_inside_list_subclass_stays_in_parity(self):
        self._assert_parity_clears(
            lambda: {
                "holdout_items": ListSubclass(
                    [ListSubclass([_nested_position()])]
                )
            }
        )


class TestPromoteFixR20DelegatingChainMap(_WrapperCase):
    """Ruling 785, line E-19: a delegating ChainMap
    subclass through the promote wrapper."""

    def test_chainmap_subclass_hit_fires_through_wrapper(self):
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

    def test_chainmap_subclass_clean_clears_through_wrapper(self):
        outcome = self._wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_clean_position()]
                )
            },
            items=[{"instruction_text": HOLDOUT_TEXT}],
        )
        self._assert_clears(outcome)

    def test_chainmap_subclass_direct_act_decides_fresh_forms(self):
        hit = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_nested_position()]
                )
            }
        )
        self.assertTrue(hit["fired"])
        self.assertEqual(hit["comparisons"], 1)
        clean = self._direct(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_clean_position()]
                )
            }
        )
        self.assertFalse(clean["fired"])
        self.assertEqual(clean["comparisons"], 1)

    def test_chainmap_subclass_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": DelegatingChainMapSubclass(
                    [_nested_position()]
                )
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_chainmap_subclass_detection_does_not_spend(self):
        module = require("ontoloop.promote")
        container = DelegatingChainMapSubclass([_nested_position()])
        detected = module._wrapper_subtree_has_iterator(
            container, frozenset()
        )
        self.assertTrue(detected)
        self.assertEqual(list(container), [_nested_position()])

    def test_chainmap_subclass_materialised_reads_twice(self):
        module = require("ontoloop.promote")
        shared = require("ontoloop.cross_split_audit")
        material = module._materialise_holdout_for_wrapper(
            {
                "holdout_items": DelegatingChainMapSubclass(
                    [_nested_position()]
                )
            },
            shared,
        )
        for _trial in range(2):
            outcome = shared.audit_instruction_item(
                HOLDOUT_TEXT, material, occasion="promotion"
            )
            self.assertTrue(outcome["fired"])
            self.assertEqual(outcome["comparisons"], 1)

    def test_chainmap_subclass_as_whole_holdout_in_parity(self):
        self._assert_parity_clears(
            lambda: DelegatingChainMapSubclass([_nested_position()])
        )


if __name__ == "__main__":
    unittest.main()
