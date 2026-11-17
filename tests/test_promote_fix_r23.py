"""Fix round 23 tests for Region 3: promote wrapper.

Written first for two positions at Round 23 triage
rulings 966 (R23-PRO-1, Low) and 967 (R23-SPAN-1, Low).
Ruling 966: a single pass form standing inside a
delegating abstract Set subclass, in the forms the
nested materialisation carries raw, firing through
the promote wrapper where the direct act clears the
presentation, because the delegating abstract Set
branch of the wrapper materialisation carries a Set
form element in its key form only where the listing
yields exactly one element standing itself as an
iterator or as a single pass iterable in no delegating
container form, and in every other case returns the
listed elements raw. Ruling 967: key material
presented through a dictionary view standing as an
item of a delegating ChainMap subclass, firing
through the promote wrapper where the direct act
clears the same presentation, because the wrapper
materialisation hands the view content to the shared
act in a listed form the act fires on, where the act
as presented reaches no comparison through that item
layer on a view form. Rulings 909 and 910 stand cured
in their bounded forms and stand not reopened by any
pin here: their charged forms and the bounded parity
positions the Round 23 papers name stand as controls.
"""

import unittest
from collections import deque, UserList

from tests.harness import require
from tests.test_promote_fix_r22 import (
    AbstractSetSubclass,
    DelegatingChainMapSubclass,
    SequenceSubclass,
    SinglePassIterable,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)
from tests.test_cross_fix_r20 import (
    HashableItem,
    inner_mapping,
    tuple_pair_key,
)

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _wrapped_key():
    return (HashableItem(inner_mapping()),)


def _values_of_pair_key():
    return {1: tuple_pair_key()}.values()


def _values_of_nested_pair_key():
    return {"o": {tuple_pair_key(): 1}}.values()


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


class TestPromoteFixR23SetSinglePassBesideSecond(
    _WrapperCase
):
    """Ruling 966, R23-PRO-1: a single pass form
    standing inside a delegating abstract Set subclass
    in the forms the nested materialisation carries
    raw."""

    def test_generator_beside_generator_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_nested_position()),
                _generator_of(_clean_position()),
            ]),
            comparisons=0,
        )

    def test_generator_beside_generator_reversed_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_clean_position()),
                _generator_of(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_generator_beside_tuple_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_nested_position()),
                (_clean_position(),),
            ]),
            comparisons=0,
        )

    def test_generator_beside_string_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_nested_position()),
                "plain",
            ]),
            comparisons=0,
        )

    def test_single_pass_iterable_beside_string_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                SinglePassIterable([_nested_position()]),
                "plain",
            ]),
            comparisons=0,
        )

    def test_plain_iterator_beside_string_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                iter([_nested_position()]),
                "plain",
            ]),
            comparisons=0,
        )

    def test_tuple_carrying_generator_one_element_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                (_generator_of(_nested_position()),),
            ]),
            comparisons=0,
        )

    def test_sequence_carrying_generator_one_element_clears(
        self,
    ):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                SequenceSubclass(
                    [_generator_of(_nested_position())]
                ),
            ]),
            comparisons=0,
        )

    def test_list_carrying_generator_one_element_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                [_generator_of(_nested_position())],
            ]),
            comparisons=0,
        )

    def test_set_form_inside_tuple_clears(self):
        self._assert_pair_clears(
            lambda: (
                AbstractSetSubclass([
                    _generator_of(_nested_position()),
                    _generator_of(_clean_position()),
                ]),
            ),
            comparisons=0,
        )

    def test_set_form_inside_list_clears(self):
        self._assert_pair_clears(
            lambda: [
                AbstractSetSubclass([
                    _generator_of(_nested_position()),
                    _generator_of(_clean_position()),
                ]),
            ],
            comparisons=0,
        )

    def test_set_single_pass_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                AbstractSetSubclass([
                    _generator_of(_nested_position()),
                    "plain",
                ])
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_set_single_pass_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item(
                AbstractSetSubclass([
                    _generator_of(_nested_position()),
                    "plain",
                ])
            ),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_set_single_pass_chainmap_in_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass([
                        AbstractSetSubclass([
                            _generator_of(_nested_position()),
                            "plain",
                        ]),
                    ])
                }
            }
        )
        self._assert_clears(outcome)

    def test_set_single_pass_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item(
                AbstractSetSubclass([
                    _generator_of(_nested_position()),
                    "plain",
                ])
            ),
            items=[
                {"instruction_text": HOLDOUT_TEXT},
                {"instruction_text": CLEAN_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_two_generators_in_set_clear(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_clean_position()),
                _generator_of(_clean_position()),
            ]),
            comparisons=0,
        )

    def test_one_generator_alone_in_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_sequence_alone_in_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                SequenceSubclass([_nested_position()]),
            ]),
            comparisons=0,
        )

    def test_two_sequences_in_set_stay_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                SequenceSubclass([_nested_position()]),
                SequenceSubclass([_clean_position()]),
            ]),
            comparisons=0,
        )

    def test_tuple_nested_alone_in_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                (_nested_position(),),
            ]),
            comparisons=0,
        )

    def test_tuple_nested_beside_string_in_set_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                (_nested_position(),),
                "plain",
            ]),
            comparisons=0,
        )


class TestPromoteFixR23ViewAsChainMapItem(_WrapperCase):
    """Ruling 967, R23-SPAN-1: key material presented
    through a dictionary view standing as an item of a
    delegating ChainMap subclass."""

    def test_values_view_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [_values_of_pair_key()],
            comparisons=0,
        )

    def test_values_view_in_tuple_clears(self):
        self._assert_pair_clears(
            lambda: (_values_of_pair_key(),),
            comparisons=0,
        )

    def test_values_view_in_deque_clears(self):
        self._assert_pair_clears(
            lambda: deque([_values_of_pair_key()]),
            comparisons=0,
        )

    def test_values_view_in_list_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [[_values_of_pair_key()]],
            comparisons=0,
        )

    def test_values_view_alone_clears(self):
        self._assert_pair_clears(
            lambda: _values_of_pair_key(),
            comparisons=0,
        )

    def test_keys_view_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [{tuple_pair_key(): 1}.keys()],
            comparisons=0,
        )

    def test_items_view_wrapped_key_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [{_wrapped_key(): 1}.items()],
            comparisons=0,
        )

    def test_frozenset_key_values_view_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [
                {1: frozenset(tuple_pair_key())}.values()
            ],
            comparisons=0,
        )

    def test_nested_mapping_values_view_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [_values_of_nested_pair_key()],
            comparisons=0,
        )

    def test_values_view_over_wrapped_key_alone_clears(self):
        self._assert_pair_clears(
            lambda: {_wrapped_key(): 1}.values(),
            comparisons=0,
        )

    def test_values_view_inside_items_view_clears(self):
        self._assert_pair_clears(
            lambda: {"k": _values_of_pair_key()}.items(),
            comparisons=0,
        )

    def test_keys_view_alone_clears(self):
        self._assert_pair_clears(
            lambda: {tuple_pair_key(): 1}.keys(),
            comparisons=0,
        )

    def test_items_view_alone_clears(self):
        self._assert_pair_clears(
            lambda: {_wrapped_key(): 1}.items(),
            comparisons=0,
        )

    def test_values_view_in_userlist_clears(self):
        self._assert_pair_clears(
            lambda: UserList([_values_of_pair_key()]),
            comparisons=0,
        )

    def test_values_view_in_plain_set_clears(self):
        self._assert_pair_clears(
            lambda: {_values_of_pair_key()},
            comparisons=0,
        )

    def test_values_view_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                [_values_of_pair_key()]
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_values_view_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item([_values_of_pair_key()]),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_values_view_chainmap_in_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass([
                        [_values_of_pair_key()],
                    ])
                }
            }
        )
        self._assert_clears(outcome)

    def test_values_view_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item([_values_of_pair_key()]),
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_plain_mapping_in_list_stays_firing(self):
        self._assert_pair_fires(
            lambda: [{tuple_pair_key(): 1}]
        )

    def test_clean_values_view_in_list_clears(self):
        clean_key = (
            HashableItem({"group": "g1"}),
            HashableItem({"text": "unrelated"}),
        )
        self._assert_pair_clears(
            lambda: [{1: clean_key}.values()],
            comparisons=0,
        )

    def test_view_without_chainmap_layer_stays_firing(self):
        holdout = {"holdout_items": [_values_of_pair_key()]}
        outcome = self._wrapper(holdout)
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            {"holdout_items": [_values_of_pair_key()]}
        )
        self.assertTrue(direct_outcome["fired"])

    def test_ruling_909_charged_form_stays_firing(self):
        self._assert_pair_fires(
            lambda: (SequenceSubclass([_nested_position()]),)
        )

    def test_ruling_910_charged_form_stays_clearing(self):
        self._assert_pair_clears(
            lambda: (_generator_of(_nested_position()),),
            comparisons=0,
        )


if __name__ == "__main__":
    unittest.main()
