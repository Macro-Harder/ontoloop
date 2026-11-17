"""Fix round 24 tests for Region 3: promote wrapper.

Written first for three positions at Round 24 triage
rulings 1029 (R24-PRO-1, Low), 1030 (R24-PRO-2, Low),
and 1031 (R24-UC-1, Low). Ruling 1029: a getitem only
form carrying a single pass form, standing as an item
of a delegating ChainMap subclass or inside a
container standing as that item, firing through the
promote wrapper where the direct act clears the
presentation, because the nested materialisation
hands the form to the standing element form, which
lists it once into element position. Ruling 1030: a
values view carrying a single pass form, standing as
an element of a delegating abstract Set subclass,
firing through the promote wrapper where the direct
act clears the presentation, because the Set element
helper returns the view raw. Ruling 1031: a string
standing inside a container standing as an item of
a delegating ChainMap subclass driving the promote
wrapper into unbounded recursion, because the plain
container limb of the nested materialisation lists a
string into its characters and every one character
string into itself. Rulings 966, 967, 909, and 910
stand cured in their bounded forms and stand not
reopened by any pin here: their charged forms and
the bounded parity positions the Round 24 papers
name stand as controls.
"""

import unittest
from collections import deque, UserList

from tests.harness import require
from tests.test_promote_fix_r21 import GetitemOnlyForm
from tests.test_promote_fix_r22 import (
    AbstractSetSubclass,
    DelegatingChainMapSubclass,
    ListSubclass,
    SequenceSubclass,
    SetSubclass,
    SinglePassIterable,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _getitem_of(item):
    return GetitemOnlyForm([_generator_of(item)])


def _getitem_of_single_pass(item):
    return GetitemOnlyForm([SinglePassIterable([item])])


def _getitem_of_iterator(item):
    return GetitemOnlyForm([iter([item])])


def _getitem_of_values_view(item):
    return GetitemOnlyForm(
        [{1: _generator_of(item)}.values()]
    )


def _values_view_of(item):
    return {1: _generator_of(item)}.values()


def _values_view_of_single_pass(item):
    return {1: SinglePassIterable([item])}.values()


def _values_view_of_iterator(item):
    return {1: iter([item])}.values()


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


class TestPromoteFixR24GetitemAsChainMapItem(_WrapperCase):
    """Ruling 1029, R24-PRO-1: a getitem only form
    carrying a single pass form, standing as an item
    of a delegating ChainMap subclass or inside a
    container standing as that item."""

    def test_getitem_generator_alone_clears(self):
        self._assert_pair_clears(
            lambda: _getitem_of(_nested_position()),
            comparisons=0,
        )

    def test_getitem_generator_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [_getitem_of(_nested_position())],
            comparisons=0,
        )

    def test_getitem_generator_in_list_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [[_getitem_of(_nested_position())]],
            comparisons=0,
        )

    def test_getitem_generator_in_tuple_clears(self):
        self._assert_pair_clears(
            lambda: (_getitem_of(_nested_position()),),
            comparisons=0,
        )

    def test_getitem_generator_in_tuple_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [(_getitem_of(_nested_position()),)],
            comparisons=0,
        )

    def test_getitem_generator_in_plain_set_clears(self):
        self._assert_pair_clears(
            lambda: {_getitem_of(_nested_position())},
            comparisons=0,
        )

    def test_getitem_generator_in_frozenset_clears(self):
        self._assert_pair_clears(
            lambda: frozenset([_getitem_of(_nested_position())]),
            comparisons=0,
        )

    def test_getitem_generator_in_deque_clears(self):
        self._assert_pair_clears(
            lambda: deque([_getitem_of(_nested_position())]),
            comparisons=0,
        )

    def test_getitem_generator_in_deque_in_deque_clears(self):
        self._assert_pair_clears(
            lambda: deque(
                [deque([_getitem_of(_nested_position())])]
            ),
            comparisons=0,
        )

    def test_getitem_generator_in_sequence_subclass_clears(self):
        self._assert_pair_clears(
            lambda: SequenceSubclass(
                [_getitem_of(_nested_position())]
            ),
            comparisons=0,
        )

    def test_getitem_generator_in_set_subclass_clears(self):
        self._assert_pair_clears(
            lambda: SetSubclass([_getitem_of(_nested_position())]),
            comparisons=0,
        )

    def test_getitem_single_pass_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [
                _getitem_of_single_pass(_nested_position())
            ],
            comparisons=0,
        )

    def test_getitem_iterator_in_tuple_clears(self):
        self._assert_pair_clears(
            lambda: (
                _getitem_of_iterator(_nested_position()),
            ),
            comparisons=0,
        )

    def test_getitem_values_view_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [
                _getitem_of_values_view(_nested_position())
            ],
            comparisons=0,
        )

    def test_getitem_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                [_getitem_of(_nested_position())]
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_getitem_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item([_getitem_of(_nested_position())]),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_getitem_chainmap_in_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [[_getitem_of(_nested_position())]]
                    )
                }
            }
        )
        self._assert_clears(outcome)

    def test_getitem_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item([_getitem_of(_nested_position())]),
            items=[
                {"instruction_text": HOLDOUT_TEXT},
                {"instruction_text": CLEAN_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_getitem_generator_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [_getitem_of(_clean_position())]
        )

    def test_getitem_nested_direct_in_list_stays_parity(self):
        self._assert_pair_clears(
            lambda: [GetitemOnlyForm([_nested_position()])]
        )

    def test_ruling_966_charged_form_stays_clearing(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _generator_of(_nested_position()),
                "plain",
            ]),
            comparisons=0,
        )

    def test_ruling_967_charged_form_stays_clearing(self):
        self._assert_pair_clears(
            lambda: [_values_view_of(_nested_position())],
            comparisons=0,
        )


class TestPromoteFixR24GetitemAsSetElement(_WrapperCase):
    """Ruling 1029, R24-PRO-1: a getitem only form
    carrying a single pass form, standing as an
    element of a delegating abstract Set subclass."""

    def test_getitem_generator_alone_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _getitem_of(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_getitem_generator_beside_string_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _getitem_of(_nested_position()),
                "plain",
            ]),
            comparisons=0,
        )

    def test_getitem_in_tuple_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                (_getitem_of(_nested_position()),),
            ]),
            comparisons=0,
        )

    def test_getitem_in_list_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                [_getitem_of(_nested_position())],
            ]),
            comparisons=0,
        )

    def test_set_form_inside_list_clears(self):
        self._assert_pair_clears(
            lambda: [
                AbstractSetSubclass([
                    _getitem_of(_nested_position()),
                ]),
            ],
            comparisons=0,
        )

    def test_set_form_inside_tuple_clears(self):
        self._assert_pair_clears(
            lambda: (
                AbstractSetSubclass([
                    _getitem_of(_nested_position()),
                ]),
            ),
            comparisons=0,
        )

    def test_getitem_single_pass_alone_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _getitem_of_single_pass(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_getitem_iterator_alone_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _getitem_of_iterator(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_getitem_values_view_alone_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _getitem_of_values_view(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_clean_getitem_generator_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _getitem_of(_clean_position()),
            ]),
            comparisons=0,
        )

    def test_getitem_nested_direct_in_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                GetitemOnlyForm([_nested_position()]),
            ]),
            comparisons=0,
        )

    def test_ruling_910_charged_form_stays_clearing(self):
        self._assert_pair_clears(
            lambda: (_generator_of(_nested_position()),),
            comparisons=0,
        )


class TestPromoteFixR24ValuesViewAsSetElement(_WrapperCase):
    """Ruling 1030, R24-PRO-2: a values view carrying
    a single pass form, standing as an element of a
    delegating abstract Set subclass."""

    def test_values_view_generator_alone_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _values_view_of(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_values_view_beside_string_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _values_view_of(_nested_position()),
                "plain",
            ]),
            comparisons=0,
        )

    def test_values_view_beside_clean_generator_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _values_view_of(_nested_position()),
                _generator_of(_clean_position()),
            ]),
            comparisons=0,
        )

    def test_values_view_single_pass_alone_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _values_view_of_single_pass(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_values_view_iterator_alone_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _values_view_of_iterator(_nested_position()),
            ]),
            comparisons=0,
        )

    def test_values_view_in_tuple_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                (_values_view_of(_nested_position()),),
            ]),
            comparisons=0,
        )

    def test_values_view_in_tuple_beside_string_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                (_values_view_of(_nested_position()), "plain"),
            ]),
            comparisons=0,
        )

    def test_values_view_in_list_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                [_values_view_of(_nested_position())],
            ]),
            comparisons=0,
        )

    def test_values_view_in_deque_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                deque([_values_view_of(_nested_position())]),
            ]),
            comparisons=0,
        )

    def test_values_view_in_frozenset_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                frozenset(
                    [_values_view_of(_nested_position())]
                ),
            ]),
            comparisons=0,
        )

    def test_set_form_inside_list_clears(self):
        self._assert_pair_clears(
            lambda: [
                AbstractSetSubclass([
                    _values_view_of(_nested_position()),
                ]),
            ],
            comparisons=0,
        )

    def test_values_view_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                AbstractSetSubclass([
                    _values_view_of(_nested_position()),
                ])
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_values_view_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item(
                AbstractSetSubclass([
                    _values_view_of(_nested_position()),
                ])
            ),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_values_view_chainmap_in_mapping_value(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [
                            AbstractSetSubclass([
                                _values_view_of(
                                    _nested_position()
                                ),
                            ]),
                        ]
                    )
                }
            }
        )
        self._assert_clears(outcome)

    def test_values_view_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item(
                AbstractSetSubclass([
                    _values_view_of(_nested_position()),
                ])
            ),
            items=[
                {"instruction_text": HOLDOUT_TEXT},
                {"instruction_text": CLEAN_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_values_view_in_set_clears(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                _values_view_of(_clean_position()),
            ]),
            comparisons=0,
        )

    def test_values_view_nested_direct_in_set_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                {1: _nested_position()}.values(),
            ]),
            comparisons=0,
        )

    def test_keys_view_generator_in_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                {
                    _generator_of(_nested_position()): 1
                }.keys(),
            ]),
            comparisons=0,
        )

    def test_items_view_generator_in_set_stays_parity(self):
        self._assert_pair_clears(
            lambda: AbstractSetSubclass([
                {1: _generator_of(_nested_position())}.items(),
            ]),
            comparisons=0,
        )


class TestPromoteFixR24StringInsideContainerItem(_WrapperCase):
    """Ruling 1031, R24-UC-1: a string standing inside
    a container standing as an item of a delegating
    ChainMap subclass, driving the wrapper into
    unbounded recursion on the standing form."""

    def test_string_alone_as_item_clears(self):
        self._assert_pair_clears(
            lambda: "plainstring",
            comparisons=0,
        )

    def test_one_character_string_in_list_clears(self):
        self._assert_pair_clears(
            lambda: ["x"],
            comparisons=0,
        )

    def test_two_character_string_in_list_clears(self):
        self._assert_pair_clears(
            lambda: ["xy"],
            comparisons=0,
        )

    def test_string_in_tuple_clears(self):
        self._assert_pair_clears(
            lambda: ("plainstring",),
            comparisons=0,
        )

    def test_string_in_deque_clears(self):
        self._assert_pair_clears(
            lambda: deque(["plainstring"]),
            comparisons=0,
        )

    def test_string_in_userlist_clears(self):
        self._assert_pair_clears(
            lambda: UserList(["plainstring"]),
            comparisons=0,
        )

    def test_string_beside_mapping_in_list_clears(self):
        self._assert_pair_clears(
            lambda: ["plainstring", {"k": "v"}]
        )

    def test_string_in_list_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [["plainstring"]],
            comparisons=0,
        )

    def test_string_in_plain_set_clears(self):
        self._assert_pair_clears(
            lambda: {"plainstring"},
            comparisons=0,
        )

    def test_string_in_frozenset_clears(self):
        self._assert_pair_clears(
            lambda: frozenset(["plainstring"]),
            comparisons=0,
        )

    def test_string_in_sequence_subclass_clears(self):
        self._assert_pair_clears(
            lambda: SequenceSubclass(["plainstring"]),
            comparisons=0,
        )

    def test_string_in_list_subclass_clears(self):
        self._assert_pair_clears(
            lambda: ListSubclass(["plainstring"]),
            comparisons=0,
        )

    def test_string_in_deque_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [deque(["plainstring"])],
            comparisons=0,
        )

    def test_string_carrying_holdout_text_in_list_clears(self):
        self._assert_pair_clears(
            lambda: [HOLDOUT_TEXT],
            comparisons=0,
        )

    def test_string_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(["plainstring"]),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_string_after_partial_scoring(self):
        outcome = self._wrapper(
            _chainmap_item(["plainstring"]),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_string_through_two_item_test(self):
        outcome = self._wrapper(
            _chainmap_item(["plainstring"]),
            items=[
                {"instruction_text": HOLDOUT_TEXT},
                {"instruction_text": CLEAN_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_empty_string_in_list_stays_parity(self):
        self._assert_pair_clears(
            lambda: [""],
            comparisons=0,
        )

    def test_integer_in_list_stays_parity(self):
        self._assert_pair_clears(
            lambda: [7],
            comparisons=0,
        )

    def test_bytes_in_list_stays_parity(self):
        self._assert_pair_clears(
            lambda: [b"plainbytes"],
            comparisons=0,
        )

    def test_bytearray_in_list_stays_parity(self):
        self._assert_pair_clears(
            lambda: [bytearray(b"plainbytes")],
            comparisons=0,
        )

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
