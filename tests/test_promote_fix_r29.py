"""Fix round 29 tests for Region 3: promote wrapper.

Written first for five positions at Round 29 triage
rulings 1474 (S15-R29-PROM-1, Low), 1475
(S15-R29-PROM-2, Low), 1476 (S15-R29-PROM-3, Low),
1477 (S15-R29-PROM-4, Low), and 1478
(S15-R29-PROM-5, Low, absorbing S15-R29-SPAN-1).
Ruling 1474: a values view carrying a plain
container holding a nested mapping, standing inside
a delegating container subclass standing as a
mapping value inside a mapping standing as an item
of a delegating ChainMap subclass, clearing through
the promote wrapper where the direct act fires.
Ruling 1475: an items view carrying a plain
container holding a nested mapping in its value at
the same position, clearing through the wrapper
where the direct act fires. Ruling 1476: a keys
view carrying a wrapped key at the same position,
clearing through the wrapper where the direct act
fires. Ruling 1477: an items view carrying a
wrapped key in its key, its value standing clean,
at the same position, clearing through the wrapper
where the direct act fires. Ruling 1478: a
delegating ChainMap subclass standing inside a
delegating container subclass standing in a
composed carrier position at the same position,
and standing inside a delegating container subclass
standing inside a plain container at that position,
raising through the wrapper on hit material and on
clean material alike, where the direct act decides
the presentation. Rulings 1377 to 1382 stand cured
in their bounded forms and stand not reopened by
any pin here: their charged forms stand as poles
beside the new forms.
"""

import unittest
from collections import ChainMap, deque

from tests.harness import require
from tests.test_cross_fix_r20 import HashableItem, inner_mapping
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


def _bytes():
    return HOLDOUT_TEXT.encode()


def _values_view_of(carried):
    return {1: carried}.values()


def _items_view_of_value(value):
    return {1: value}.items()


def _items_view_of_pair(key, value):
    return {key: value}.items()


def _keys_view_of(key):
    return {key: 1}.keys()


def _wrapped_key(text=HOLDOUT_TEXT):
    if text == HOLDOUT_TEXT:
        return (HashableItem(inner_mapping()),)
    return (HashableItem({"inner": {"text": text}}),)


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

    def _assert_chainmap_pair_fires(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def _assert_chainmap_pair_fires_decision(self, make_item,
                                             comparisons):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], comparisons)

    def _assert_chainmap_pair_clears(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def _assert_chainmap_pair_clears_compared(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def _assert_chainmap_pair_clears_compared_two(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 2)

    def _assert_candidate_fires(self, make_item):
        module = require("ontoloop.promote")
        item = make_item() if callable(make_item) else make_item
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(item),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def _assert_candidate_clears(self, make_item):
        module = require("ontoloop.promote")
        item = make_item() if callable(make_item) else make_item
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(item),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])


class TestPromoteFixR29ValuesViewPlainContainerNested(
    _WrapperCase
):
    """Ruling 1474, S15-R29-PROM-1: a values view
    carrying a plain container holding a nested
    mapping inside a delegating container subclass
    standing as a mapping value inside a ChainMap
    item mapping, clearing through the wrapper where
    the direct act fires."""

    def test_vv_list_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": TupleSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SetSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": DequeSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": UserListSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SequenceSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_in_delegating_abstract_set_fires(
        self,
    ):
        self._assert_chainmap_pair_fires(
            lambda: {"k": AbstractSetSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_tuple_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_values_view_of((_nested_position(),))])}
        )

    def test_vv_list_list_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_values_view_of([[_nested_position()]])])}
        )

    def test_vv_list_mapping_nested_in_delegating_list_fires(
        self,
    ):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_values_view_of(
                [{"x": _nested_position()}])])}
        )

    def test_vv_list_nested_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": {"j": ListSubclass(
                [_values_view_of([_nested_position()])])}}
        )

    def test_vv_list_nested_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass(
                [_values_view_of([_nested_position()])])}
        )

    def test_vv_list_nested_as_mapping_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _values_view_of([_nested_position()])}
        )

    def test_vv_list_nested_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_values_view_of([_nested_position()])]}
        )

    def test_vv_list_nested_in_generator_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _generator_of(
                _values_view_of([_nested_position()]))}
        )

    def test_vv_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_values_view_of(_nested_position())])}
        )

    def test_vv_generator_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_values_view_of(
                _generator_of(_nested_position()))])}
        )

    def test_vv_dict_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_values_view_of(
                {"x": _nested_position()})])}
        )

    def test_vv_list_generator_nested_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_values_view_of(
                [_generator_of(_nested_position())])])}
        )

    def test_vv_chainmap_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_values_view_of(
                DelegatingChainMapSubclass(
                    [_nested_position()]))])}
        )

    def test_vv_list_bytes_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass(
                [_values_view_of([_bytes()])])}
        )

    def test_vv_list_clean_nested_in_delegating_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {"k": ListSubclass(
                [_values_view_of([_clean_position()])])}
        )

    def test_vv_delegating_nested_in_delegating_clears(self):
        make_item = lambda: {"k": ListSubclass([_values_view_of(
            ListSubclass([_nested_position()]))])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


class TestPromoteFixR29ItemsViewPlainContainerNested(
    _WrapperCase
):
    """Ruling 1475, S15-R29-PROM-2: an items view
    carrying a plain container holding a nested
    mapping in its value inside a delegating
    container subclass at the same position, clearing
    through the wrapper where the direct act fires."""

    def test_iv_list_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_list_nested_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": TupleSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_list_nested_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SetSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_list_nested_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": DequeSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_list_nested_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": UserListSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_list_nested_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SequenceSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_list_nested_in_delegating_abstract_set_fires(
        self,
    ):
        self._assert_chainmap_pair_fires(
            lambda: {"k": AbstractSetSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_tuple_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_items_view_of_value((_nested_position(),))])}
        )

    def test_iv_list_nested_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass(
                [_items_view_of_value([_nested_position()])])}
        )

    def test_iv_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_items_view_of_value(_nested_position())])}
        )

    def test_iv_dict_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_items_view_of_value(
                {"x": _nested_position()})])}
        )

    def test_iv_list_generator_nested_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_items_view_of_value(
                [_generator_of(_nested_position())])])}
        )

    def test_iv_chainmap_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_items_view_of_value(
                DelegatingChainMapSubclass(
                    [_nested_position()]))])}
        )

    def test_iv_in_generator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_generator_of(
                _items_view_of_value([_nested_position()]))])}
        )

    def test_iv_list_bytes_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass(
                [_items_view_of_value([_bytes()])])}
        )

    def test_iv_list_clean_nested_in_delegating_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {"k": ListSubclass(
                [_items_view_of_value([_clean_position()])])}
        )


class TestPromoteFixR29KeysViewWrappedKey(_WrapperCase):
    """Ruling 1476, S15-R29-PROM-3: a keys view
    carrying a wrapped key inside a delegating
    container subclass at the same position, clearing
    through the wrapper where the direct act fires."""

    def test_kv_wrapped_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": TupleSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SetSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": DequeSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": UserListSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SequenceSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_in_delegating_abstract_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": AbstractSetSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_hashable_item_alone_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_keys_view_of(
                HashableItem(inner_mapping()))])}
        )

    def test_kv_wrapped_in_plain_list_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [[_keys_view_of(_wrapped_key())]])}
        )

    def test_kv_wrapped_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": {"j": ListSubclass(
                [_keys_view_of(_wrapped_key())])}}
        )

    def test_kv_wrapped_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass(
                [_keys_view_of(_wrapped_key())])}
        )

    def test_kv_wrapped_as_mapping_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _keys_view_of(_wrapped_key())}
        )

    def test_kv_wrapped_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_keys_view_of(_wrapped_key())]}
        )

    def test_kv_wrapped_in_generator_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _generator_of(
                _keys_view_of(_wrapped_key()))}
        )

    def test_kv_generator_key_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_keys_view_of(
                _generator_of(_nested_position()))])}
        )

    def test_kv_bytes_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass(
                [_keys_view_of(_bytes())])}
        )

    def test_kv_clean_wrapped_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {"k": ListSubclass(
                [_keys_view_of(_wrapped_key(CLEAN_TEXT))])}
        )


class TestPromoteFixR29ItemsViewWrappedKey(_WrapperCase):
    """Ruling 1477, S15-R29-PROM-4: an items view
    carrying a wrapped key in its key, its value
    standing clean, inside a delegating container
    subclass at the same position, clearing through
    the wrapper where the direct act fires."""

    def test_iv_wrapped_key_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": ListSubclass([_items_view_of_pair(
                _wrapped_key(), CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": TupleSubclass([_items_view_of_pair(
                _wrapped_key(), CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": SetSubclass([_items_view_of_pair(
                _wrapped_key(), CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": DequeSubclass([_items_view_of_pair(
                _wrapped_key(), CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": UserListSubclass(
                [_items_view_of_pair(_wrapped_key(),
                                     CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": SequenceSubclass(
                [_items_view_of_pair(_wrapped_key(),
                                     CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_in_delegating_abstract_set_fires(
        self,
    ):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": AbstractSetSubclass(
                [_items_view_of_pair(_wrapped_key(),
                                     CLEAN_TEXT)])}, 2
        )

    def test_iv_wrapped_key_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass([_items_view_of_pair(
                _wrapped_key(), CLEAN_TEXT)])}
        )

    def test_iv_wrapped_key_as_mapping_value_fires(self):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": _items_view_of_pair(
                _wrapped_key(), CLEAN_TEXT)}, 2
        )

    def test_iv_wrapped_key_in_generator_in_delegating_fires(
        self,
    ):
        self._assert_chainmap_pair_fires_decision(
            lambda: {"k": ListSubclass([_generator_of(
                _items_view_of_pair(_wrapped_key(),
                                    CLEAN_TEXT))])}, 2
        )

    def test_iv_bytes_key_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([_items_view_of_pair(
                _bytes(), CLEAN_TEXT)])}
        )

    def test_iv_clean_wrapped_key_in_delegating_clears(self):
        self._assert_chainmap_pair_clears_compared_two(
            lambda: {"k": ListSubclass([_items_view_of_pair(
                _wrapped_key(CLEAN_TEXT), CLEAN_TEXT)])}
        )


class TestPromoteFixR29ChainMapInComposedCarrier(
    _WrapperCase
):
    """Ruling 1478, S15-R29-PROM-5 absorbing
    S15-R29-SPAN-1: a delegating ChainMap subclass
    standing inside a delegating container subclass
    standing in a composed carrier position, and
    standing inside a delegating container subclass
    standing inside a plain container, at a mapping
    value inside a ChainMap item mapping, raising
    through the wrapper where the direct act decides
    the presentation, on hit material and on clean
    material alike."""

    def test_cm_in_delegating_list_in_delegating_list_clears(self):
        make_item = lambda: {"k": ListSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_tuple_in_delegating_list_clears(self):
        make_item = lambda: {"k": ListSubclass([TupleSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_set_in_delegating_list_clears(self):
        make_item = lambda: {"k": ListSubclass([SetSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_deque_in_delegating_list_clears(self):
        make_item = lambda: {"k": ListSubclass([DequeSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_userlist_in_delegating_clears(self):
        make_item = lambda: {"k": ListSubclass([UserListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_delegating_tuple_clears(self):
        make_item = lambda: {"k": TupleSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_delegating_set_clears(self):
        make_item = lambda: {"k": SetSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_delegating_deque_clears(self):
        make_item = lambda: {"k": DequeSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_delegating_user_clears(self):
        make_item = lambda: {"k": UserListSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_plain_list_clears(self):
        make_item = lambda: {"k": [ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])]}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_plain_tuple_clears(self):
        make_item = lambda: {"k": (ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])]),)}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_generator_clears(self):
        make_item = lambda: {"k": _generator_of(ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])]))}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_in_generator_in_delegating(self):
        make_item = lambda: {"k": ListSubclass([_generator_of(
            ListSubclass([DelegatingChainMapSubclass(
                [_nested_position()])]))])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_in_delegating_one_deeper(self):
        make_item = lambda: {"k": {"j": ListSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_nested_position()])])])}}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_in_delegating_candidate(self):
        self._assert_candidate_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [DelegatingChainMapSubclass(
                    [_nested_position()])])])}
        )

    def test_cm_bytes_in_delegating_in_delegating_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [DelegatingChainMapSubclass([_bytes()])])])}
        )

    def test_cm_clean_in_delegating_in_delegating_clears(self):
        make_item = lambda: {"k": ListSubclass([ListSubclass(
            [DelegatingChainMapSubclass(
                [_clean_position()])])])}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_clean_in_delegating_in_plain_list_clears(self):
        make_item = lambda: {"k": [ListSubclass(
            [DelegatingChainMapSubclass(
                [_clean_position()])])]}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_span_clean_in_plain_tuple_clears(self):
        make_item = lambda: {"k": (ListSubclass(
            [DelegatingChainMapSubclass(
                [_clean_position()])]),)}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_span_clean_in_generator_clears(self):
        make_item = lambda: {"k": _generator_of(ListSubclass(
            [DelegatingChainMapSubclass(
                [_clean_position()])]))}
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_span_in_plain_list_candidate_clears(self):
        self._assert_candidate_clears(
            lambda: {"k": [ListSubclass(
                [DelegatingChainMapSubclass(
                    [_nested_position()])])]}
        )

    def test_cm_in_delegating_as_mapping_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [DelegatingChainMapSubclass(
                    [_nested_position()])])}
        )

    def test_cm_in_plain_list_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass(
                [[DelegatingChainMapSubclass(
                    [_nested_position()])]])}
        )

    def test_cm_in_generator_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_generator_of(
                DelegatingChainMapSubclass(
                    [_nested_position()]))])}
        )

    def test_cm_in_delegating_sequence_in_delegating_clears(
        self,
    ):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([SequenceSubclass(
                [DelegatingChainMapSubclass(
                    [_nested_position()])])])}
        )

    def test_cm_in_delegating_abstract_set_in_delegating(
        self,
    ):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([AbstractSetSubclass(
                [DelegatingChainMapSubclass(
                    [_nested_position()])])])}
        )

    def test_cm_in_delegating_sequence_in_plain_list_clears(
        self,
    ):
        self._assert_chainmap_pair_clears(
            lambda: {"k": [SequenceSubclass(
                [DelegatingChainMapSubclass(
                    [_nested_position()])])]}
        )


if __name__ == "__main__":
    unittest.main()
