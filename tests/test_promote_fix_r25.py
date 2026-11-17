"""Fix round 25 tests for Region 3: promote wrapper.

Written first for three positions at Round 25 triage
rulings 1105 (S15-R25-SPAN-2, Low), 1106 (R25-PRO-1,
Low), and 1107 (R25-PRO-2, Low). Ruling 1105: key
material presented through a dictionary view standing
inside a delegating container subclass standing as a
direct mapping value at the items or pairs position,
firing at the promote wrapper where the direct act
and the dataset surface clear it. Ruling 1106: a keys
view or an items view carrying a single pass form,
standing as an item of a delegating ChainMap subclass
or inside a container standing as that item, firing
through the promote wrapper where the direct act
clears the presentation. Ruling 1107: a byte form
carrying the sealed holdout text, standing as an item
of a delegating ChainMap subclass or inside a
container standing as that item, firing through the
promote wrapper where the direct act clears the
presentation. Rulings 1029, 1030, and 1031 stand
cured in their bounded forms and stand not reopened
by any pin here: their charged forms stand as
controls, beside the standing parity forms the Round
25 papers name.
"""

import unittest
from collections import OrderedDict, UserDict, UserList, deque
from types import MappingProxyType

from tests.harness import require
from tests.test_cross_fix_r20 import HashableItem, inner_mapping
from tests.test_promote_fix_r21 import GetitemOnlyForm
from tests.test_promote_fix_r22 import (
    AbstractSetSubclass,
    DequeSubclass,
    DelegatingChainMapSubclass,
    ListSubclass,
    SequenceSubclass,
    SetSubclass,
    SinglePassIterable,
    TupleSubclass,
    UserListSubclass,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _wrapped_key(text=HOLDOUT_TEXT):
    if text == HOLDOUT_TEXT:
        return (HashableItem(inner_mapping()),)
    return (HashableItem({"inner": {"text": text}}),)


def _keys_view(text=HOLDOUT_TEXT):
    return {_wrapped_key(text): 1}.keys()


def _items_view(text=HOLDOUT_TEXT):
    return {_wrapped_key(text): 1}.items()


def _keys_view_of_generator():
    return {_generator_of(_nested_position()): 1}.keys()


def _items_view_of_generator():
    return {1: _generator_of(_nested_position())}.items()


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

    def _dataset(self, holdout_material):
        module = require("ontoloop.dataset")
        bundle = {
            "instruction_items": [{"text": HOLDOUT_TEXT}],
            "holdout_items": holdout_material,
        }
        return module.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )

    def _assert_fires(self, outcome):
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["promotion_proceeds"])

    def _assert_clears(self, outcome):
        self.assertFalse(outcome["fired"])
        self.assertTrue(
            outcome["test_result_carried_on_promotion_record"]
        )

    def _assert_chainmap_pair_clears(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


class TestPromoteFixR25SpanMappingValue(_WrapperCase):
    """Ruling 1105, S15-R25-SPAN-2: a dictionary view
    inside a delegating container subclass standing
    as a direct mapping value at the items or pairs
    position."""

    def _assert_three_surface_clears(self, make_holdout):
        outcome = self._wrapper(make_holdout())
        self._assert_clears(outcome)
        direct_outcome = self._direct(make_holdout())
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)
        dataset_outcome = self._dataset(make_holdout())
        self.assertFalse(dataset_outcome["fired"])

    def test_keys_view_deleg_list_mapping_value_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {"items": {"k": ListSubclass([_keys_view()])}}
        )

    def test_keys_view_deleg_list_mapping_value_pairs_clears(self):
        self._assert_three_surface_clears(
            lambda: {"pairs": {"k": ListSubclass([_keys_view()])}}
        )

    def test_keys_view_deleg_tuple_mapping_value_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {"items": {"k": TupleSubclass([_keys_view()])}}
        )

    def test_keys_view_deleg_sequence_mapping_value_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {"k": SequenceSubclass([_keys_view()])}
            }
        )

    def test_keys_view_deleg_set_mapping_value_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {"items": {"k": SetSubclass([_keys_view()])}}
        )

    def test_items_view_deleg_list_mapping_value_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {"items": {"k": ListSubclass([_items_view()])}}
        )

    def test_keys_view_deleg_list_nested_mapping_value_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": {"j": ListSubclass([_keys_view()])}
                }
            }
        )

    def test_mapping_value_at_candidate_construction_clears(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "items": {"k": ListSubclass([_keys_view()])}
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_clean_key_material_mapping_value_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [_keys_view("unrelated wording entirely")]
                    )
                }
            }
        )

    def test_clean_text_against_mapping_value_clears(self):
        outcome = self._wrapper(
            {"items": {"k": ListSubclass([_keys_view()])}},
            items=[{"instruction_text": CLEAN_TEXT}],
        )
        self._assert_clears(outcome)

    def test_exact_list_mapping_value_still_fires(self):
        make = lambda: {"items": {"k": [_keys_view()]}}
        outcome = self._wrapper(make())
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(make())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_deleg_list_in_list_as_mapping_value_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {"k": [ListSubclass([_keys_view()])]}
            }
        )

    def test_mapping_as_whole_holdout_clears(self):
        self._assert_three_surface_clears(
            lambda: {"k": ListSubclass([_keys_view()])}
        )

    def test_mapping_value_at_holdout_items_position_fires(self):
        make = lambda: {
            "holdout_items": {"k": ListSubclass([_keys_view()])}
        }
        outcome = self._wrapper(make())
        self._assert_fires(outcome)
        direct_outcome = self._direct(make())
        self.assertTrue(direct_outcome["fired"])


class TestPromoteFixR25ViewCarryingSinglePassItem(_WrapperCase):
    """Ruling 1106, R25-PRO-1: a keys view or an items
    view carrying a single pass form, standing as an
    item of a delegating ChainMap subclass or inside
    a container standing as that item."""

    def test_keys_view_generator_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: _keys_view_of_generator()
        )

    def test_keys_view_generator_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [_keys_view_of_generator()]
        )

    def test_keys_view_generator_in_tuple_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: (_keys_view_of_generator(),)
        )

    def test_keys_view_generator_in_deque_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: deque([_keys_view_of_generator()])
        )

    def test_keys_view_generator_in_userlist_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: UserList([_keys_view_of_generator()])
        )

    def test_keys_view_generator_in_list_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [[_keys_view_of_generator()]]
        )

    def test_keys_view_generator_in_sequence_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: SequenceSubclass([_keys_view_of_generator()])
        )

    def test_keys_view_generator_in_list_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: ListSubclass([_keys_view_of_generator()])
        )

    def test_keys_view_generator_in_set_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: SetSubclass([_keys_view_of_generator()])
        )

    def test_keys_view_generator_in_deque_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: DequeSubclass([_keys_view_of_generator()])
        )

    def test_items_view_generator_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: _items_view_of_generator()
        )

    def test_items_view_generator_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [_items_view_of_generator()]
        )

    def test_items_view_generator_in_tuple_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: (_items_view_of_generator(),)
        )

    def test_items_view_generator_in_deque_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: deque([_items_view_of_generator()])
        )

    def test_items_view_generator_in_tuple_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [(_items_view_of_generator(),)]
        )

    def test_items_view_generator_in_tuple_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: TupleSubclass([_items_view_of_generator()])
        )

    def test_items_view_generator_in_userlist_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: UserListSubclass([_items_view_of_generator()])
        )

    def test_keys_view_single_pass_iterable_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                SinglePassIterable([_nested_position()]): 1
            }.keys()
        )

    def test_keys_view_plain_iterator_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [
                {iter([_nested_position()]): 1}.keys()
            ]
        )

    def test_items_view_single_pass_iterable_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                1: SinglePassIterable([_nested_position()])
            }.items()
        )

    def test_keys_view_getitem_carrying_generator_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                GetitemOnlyForm(
                    [_generator_of(_nested_position())]
                ): 1
            }.keys()
        )

    def test_userdict_keys_view_generator_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: UserDict(
                {_generator_of(_nested_position()): 1}
            ).keys()
        )

    def test_mappingproxy_keys_view_generator_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: MappingProxyType(
                {_generator_of(_nested_position()): 1}
            ).keys()
        )

    def test_ordereddict_items_view_generator_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [
                OrderedDict(
                    [(1, _generator_of(_nested_position()))]
                ).items()
            ]
        )

    def test_keys_view_at_candidate_construction_clears(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                _keys_view_of_generator()
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_keys_view_after_partial_scoring_clears(self):
        outcome = self._wrapper(
            _chainmap_item(_keys_view_of_generator()),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_keys_view_through_two_item_test_clears(self):
        outcome = self._wrapper(
            _chainmap_item(_keys_view_of_generator()),
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_clears(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_keys_view_chainmap_in_mapping_value_clears(self):
        outcome = self._wrapper(
            {
                "holdout_items": {
                    "inner": DelegatingChainMapSubclass(
                        [_keys_view_of_generator()]
                    )
                }
            }
        )
        self._assert_clears(outcome)

    def test_clean_keys_view_generator_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {_generator_of(_clean_position()): 1}.keys()
        )

    def test_clean_items_view_generator_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [{1: _generator_of(_clean_position())}.items()]
        )

    def test_values_view_generator_alone_stays_parity(self):
        self._assert_chainmap_pair_clears(
            lambda: {1: _generator_of(_nested_position())}.values()
        )

    def test_keys_view_getitem_direct_stays_parity(self):
        outcome = self._wrapper(
            _chainmap_item(
                {
                    GetitemOnlyForm([_nested_position()]): 1
                }.keys()
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {
                    GetitemOnlyForm([_nested_position()]): 1
                }.keys()
            )
        )
        self.assertFalse(direct_outcome["fired"])

    def test_items_view_single_pass_in_key_position_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                _generator_of(_nested_position()): 1
            }.items()
        )


class TestPromoteFixR25ByteFormItem(_WrapperCase):
    """Ruling 1107, R25-PRO-2: a byte form carrying
    the sealed holdout text, standing as an item of
    a delegating ChainMap subclass or inside a
    container standing as that item."""

    def test_bytes_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: HOLDOUT_TEXT.encode()
        )

    def test_bytes_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [HOLDOUT_TEXT.encode()]
        )

    def test_bytes_in_list_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [[HOLDOUT_TEXT.encode()]]
        )

    def test_bytes_in_tuple_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: (HOLDOUT_TEXT.encode(),)
        )

    def test_bytes_in_deque_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: deque([HOLDOUT_TEXT.encode()])
        )

    def test_bytes_in_userlist_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: UserList([HOLDOUT_TEXT.encode()])
        )

    def test_bytes_in_sequence_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: SequenceSubclass([HOLDOUT_TEXT.encode()])
        )

    def test_bytes_in_list_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: ListSubclass([HOLDOUT_TEXT.encode()])
        )

    def test_bytearray_alone_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: bytearray(HOLDOUT_TEXT.encode())
        )

    def test_bytearray_in_tuple_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: (bytearray(HOLDOUT_TEXT.encode()),)
        )

    def test_bytes_at_candidate_construction_clears(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                HOLDOUT_TEXT.encode()
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_bytes_after_partial_scoring_clears(self):
        outcome = self._wrapper(
            _chainmap_item(HOLDOUT_TEXT.encode()),
            after_partial_scoring=True,
        )
        self._assert_clears(outcome)

    def test_clean_bytes_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [CLEAN_TEXT.encode()]
        )

    def test_bytes_in_mapping_value_as_item_stays_firing(self):
        make = lambda: {"k": HOLDOUT_TEXT.encode()}
        outcome = self._wrapper(_chainmap_item(make()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make()))
        self.assertTrue(direct_outcome["fired"])

    def test_bytes_in_abstract_set_subclass_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: AbstractSetSubclass([HOLDOUT_TEXT.encode()])
        )

    def test_plain_bytes_in_list_stays_parity(self):
        self._assert_chainmap_pair_clears(
            lambda: [b"plain byte content"]
        )


class TestPromoteFixR25StandingControls(_WrapperCase):
    """Standing poles: the charged forms of rulings
    1029, 1030, and 1031 still decide as charged."""

    def test_ruling_1029_getitem_generator_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [
                GetitemOnlyForm(
                    [_generator_of(_nested_position())]
                )
            ]
        )

    def test_ruling_1030_values_view_in_set_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: AbstractSetSubclass(
                [{1: _generator_of(_nested_position())}.values()]
            )
        )

    def test_ruling_1031_string_in_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [HOLDOUT_TEXT]
        )


if __name__ == "__main__":
    unittest.main()
