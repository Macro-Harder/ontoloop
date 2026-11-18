"""Fix round 28 tests for Region 3: promote wrapper.

Written first for six positions at Round 28 triage
rulings 1377 (S15-R28-PROM-1, Low), 1378
(S15-R28-PROM-2, Low), 1379 (S15-R28-PROM-3, Low),
1380 (S15-R28-PROM-4, Low), 1381 (S15-R28-PROM-5,
Low), and 1382 (S15-R28-PROM-6, Low, absorbing
S15-R28-SPAN-1). Ruling 1377: a values view carrying
byte text or a memoryview of the sealed holdout
text, standing inside a delegating container
subclass standing as a mapping value inside a
mapping standing as an item of a delegating
ChainMap subclass, firing through the promote
wrapper where the direct act clears. Ruling 1378: a
byte form carrying the sealed text standing inside
a single pass form standing inside a delegating
container subclass at the same position, clearing
through the wrapper where the direct act fires.
Ruling 1379: a keys view carrying byte text or a
memoryview at the same composed position, clearing
through the wrapper where the direct act fires.
Ruling 1380: an items view carrying byte text or a
memoryview in its value at the same composed
position, clearing through the wrapper where the
direct act fires. Ruling 1381: an items view
carrying a nested mapping in its value, standing
inside a delegating container subclass at the same
position, clearing through the wrapper where the
direct act fires. Ruling 1382: a delegating ChainMap
subclass standing inside a delegating container
subclass at the same position, and at the plain
holdout positions the Spanning paper names, raising
through the wrapper on hit material and on clean
material alike, where the direct act decides the
presentation. Rulings 1284 to 1288 stand cured in
their bounded forms and stand not reopened by any
pin here: their charged forms stand as poles beside
the new forms.
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


def _memoryview():
    return memoryview(HOLDOUT_TEXT.encode())


def _keys_view_of_bytes():
    return {_bytes(): 1}.keys()


def _keys_view_of_memoryview():
    return {_memoryview(): 1}.keys()


def _keys_view_of_generator():
    return {_generator_of(_nested_position()): 1}.keys()


def _items_view_of_bytes_value():
    return {1: _bytes()}.items()


def _items_view_of_memoryview_value():
    return {1: _memoryview()}.items()


def _items_view_of_generator():
    return {1: _generator_of(_nested_position())}.items()


def _items_view_of_nested_value():
    return {1: _nested_position()}.items()


def _items_view_of_clean_nested_value():
    return {1: _clean_position()}.items()


def _values_view_of_bytes():
    return {1: _bytes()}.values()


def _values_view_of_memoryview():
    return {1: _memoryview()}.values()


def _values_view_of_generator():
    return {1: _generator_of(_nested_position())}.values()


def _values_view_of_nested():
    return {1: _nested_position()}.values()


def _values_view_of_clean_bytes():
    return {1: CLEAN_TEXT.encode()}.values()


def _wrapped_key(text=HOLDOUT_TEXT):
    if text == HOLDOUT_TEXT:
        return (HashableItem(inner_mapping()),)
    return (HashableItem({"inner": {"text": text}}),)


def _span_keys_view(text=HOLDOUT_TEXT):
    return {_wrapped_key(text): 1}.keys()


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

    def _assert_plain_holdout_pair(self, make_holdout, fired,
                                   comparisons):
        outcome = self._wrapper(make_holdout())
        direct_outcome = self._direct(make_holdout())
        self.assertEqual(direct_outcome["fired"], fired)
        self.assertEqual(direct_outcome["comparisons"], comparisons)
        if fired:
            self._assert_fires(outcome)
            self.assertEqual(
                outcome["cross_split_audit_result"]["comparisons"],
                comparisons,
            )
        else:
            self._assert_clears(outcome)


class TestPromoteFixR28ValuesViewInDelegatingCarrier(_WrapperCase):
    """Ruling 1377, S15-R28-PROM-1: a values view
    carrying byte text or a memoryview inside a
    delegating container subclass standing as a
    mapping value inside a ChainMap item mapping,
    firing through the wrapper where the direct act
    clears."""

    def test_vv_bytes_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([_values_view_of_bytes()])}
        )

    def test_vv_bytes_in_delegating_tuple_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": TupleSubclass([_values_view_of_bytes()])}
        )

    def test_vv_bytes_in_delegating_set_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": SetSubclass([_values_view_of_bytes()])}
        )

    def test_vv_bytes_in_delegating_deque_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": DequeSubclass([_values_view_of_bytes()])}
        )

    def test_vv_bytes_in_delegating_userlist_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": UserListSubclass([_values_view_of_bytes()])
            }
        )

    def test_vv_bytes_in_delegating_sequence_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": SequenceSubclass([_values_view_of_bytes()])
            }
        )

    def test_vv_bytes_in_delegating_abstract_set_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": AbstractSetSubclass([_values_view_of_bytes()])
            }
        )

    def test_vv_memoryview_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass([_values_view_of_memoryview()])
            }
        )

    def test_vv_memoryview_in_delegating_sequence_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": SequenceSubclass(
                    [_values_view_of_memoryview()]
                )
            }
        )

    def test_vv_bytes_in_plain_list_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass([[_values_view_of_bytes()]])
            }
        )

    def test_vv_bytes_in_delegating_list_one_mapping_deeper(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": {"j": ListSubclass([_values_view_of_bytes()])}
            }
        )

    def test_vv_bytes_in_delegating_list_in_list_as_item(self):
        self._assert_chainmap_pair_clears(
            lambda: [{"k": ListSubclass([_values_view_of_bytes()])}]
        )

    def test_vv_bytes_in_delegating_list_at_candidate(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": ListSubclass([_values_view_of_bytes()])}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_vv_bytes_in_plain_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_values_view_of_bytes()]}
        )

    def test_vv_bytes_in_generator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_values_view_of_bytes())]
                )
            }
        )

    def test_vv_nested_in_delegating_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_values_view_of_nested()])}
        )

    def test_vv_generator_in_delegating_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass([_values_view_of_generator()])
            }
        )

    def test_clean_vv_bytes_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass([_values_view_of_clean_bytes()])
            }
        )


class TestPromoteFixR28ByteInSinglePassInDelegating(_WrapperCase):
    """Ruling 1378, S15-R28-PROM-2: a byte form inside
    a single pass form inside a delegating container
    subclass standing as a mapping value inside a
    ChainMap item mapping, clearing through the
    wrapper where the direct act fires."""

    def test_bytes_in_generator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_generator_of(_bytes())])}
        )

    def test_bytes_in_generator_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": TupleSubclass([_generator_of(_bytes())])}
        )

    def test_bytes_in_generator_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SetSubclass([_generator_of(_bytes())])}
        )

    def test_bytes_in_generator_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": DequeSubclass([_generator_of(_bytes())])}
        )

    def test_bytes_in_generator_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": UserListSubclass([_generator_of(_bytes())])
            }
        )

    def test_bytes_in_generator_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SequenceSubclass([_generator_of(_bytes())])
            }
        )

    def test_bytes_in_generator_in_delegating_abstract_set(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": AbstractSetSubclass(
                    [_generator_of(_bytes())]
                )
            }
        )

    def test_bytes_in_single_pass_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [SinglePassIterable([_bytes()])]
                )
            }
        )

    def test_bytes_in_iterator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([iter([_bytes()])])}
        )

    def test_bytes_in_zip_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([zip([_bytes()])])}
        )

    def test_bytes_in_map_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [map(lambda x: x, [_bytes()])]
                )
            }
        )

    def test_memoryview_in_generator_in_delegating_list(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_memoryview())]
                )
            }
        )

    def test_memoryview_in_single_pass_in_delegating_seq(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SequenceSubclass(
                    [SinglePassIterable([_memoryview()])]
                )
            }
        )

    def test_bytes_in_plain_list_in_generator_in_delegating(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass([_generator_of([_bytes()])])
            }
        )

    def test_bytes_in_generator_in_delegating_one_deeper(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": {
                    "j": ListSubclass([_generator_of(_bytes())])
                }
            }
        )

    def test_bytes_in_generator_in_delegating_at_candidate(self):
        self._assert_candidate_fires(
            {"k": ListSubclass([_generator_of(_bytes())])}
        )

    def test_bytes_in_generator_at_mapping_value_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _generator_of(_bytes())}
        )

    def test_bytes_in_plain_list_in_delegating_still_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([[_bytes()]])}
        )

    def test_bytes_in_plain_tuple_in_delegating_still_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([(_bytes(),)])}
        )

    def test_clean_bytes_in_generator_in_delegating_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(CLEAN_TEXT.encode())]
                )
            }
        )


class TestPromoteFixR28KeysViewInSinglePassInDelegating(
        _WrapperCase):
    """Ruling 1379, S15-R28-PROM-3: a keys view
    carrying byte text or a memoryview inside a
    single pass form inside a delegating container
    subclass standing as a mapping value inside a
    ChainMap item mapping, clearing through the
    wrapper where the direct act fires."""

    def test_kv_bytes_in_generator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_keys_view_of_bytes())]
                )
            }
        )

    def test_kv_bytes_in_generator_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": TupleSubclass(
                    [_generator_of(_keys_view_of_bytes())]
                )
            }
        )

    def test_kv_bytes_in_generator_in_delegating_seq_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SequenceSubclass(
                    [_generator_of(_keys_view_of_bytes())]
                )
            }
        )

    def test_kv_bytes_in_single_pass_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [SinglePassIterable([_keys_view_of_bytes()])]
                )
            }
        )

    def test_kv_bytes_in_iterator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass([iter([_keys_view_of_bytes()])])
            }
        )

    def test_kv_memoryview_in_generator_in_delegating_list(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_keys_view_of_memoryview())]
                )
            }
        )

    def test_kv_bytes_in_generator_in_delegating_at_candidate(self):
        self._assert_candidate_fires(
            {
                "k": ListSubclass(
                    [_generator_of(_keys_view_of_bytes())]
                )
            }
        )

    def test_kv_bytes_in_generator_at_mapping_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _generator_of(_keys_view_of_bytes())}
        )

    def test_kv_generator_in_generator_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_keys_view_of_generator())]
                )
            }
        )

    def test_clean_kv_in_generator_in_delegating_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {
                "k": ListSubclass(
                    [
                        _generator_of(
                            {CLEAN_TEXT.encode(): 1}.keys()
                        )
                    ]
                )
            }
        )


class TestPromoteFixR28ItemsViewInSinglePassInDelegating(
        _WrapperCase):
    """Ruling 1380, S15-R28-PROM-4: an items view
    carrying byte text or a memoryview in its value
    inside a single pass form inside a delegating
    container subclass standing as a mapping value
    inside a ChainMap item mapping, clearing through
    the wrapper where the direct act fires."""

    def test_iv_bytes_in_generator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_items_view_of_bytes_value())]
                )
            }
        )

    def test_iv_bytes_in_generator_in_delegating_seq_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SequenceSubclass(
                    [_generator_of(_items_view_of_bytes_value())]
                )
            }
        )

    def test_iv_bytes_in_single_pass_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [
                        SinglePassIterable(
                            [_items_view_of_bytes_value()]
                        )
                    ]
                )
            }
        )

    def test_iv_bytes_in_iterator_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [iter([_items_view_of_bytes_value()])]
                )
            }
        )

    def test_iv_memoryview_in_generator_in_delegating_list(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [
                        _generator_of(
                            _items_view_of_memoryview_value()
                        )
                    ]
                )
            }
        )

    def test_iv_bytes_in_generator_in_delegating_at_candidate(self):
        self._assert_candidate_fires(
            {
                "k": ListSubclass(
                    [_generator_of(_items_view_of_bytes_value())]
                )
            }
        )

    def test_iv_bytes_at_mapping_value_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _items_view_of_bytes_value()}
        )

    def test_iv_bytes_in_delegating_list_still_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass([_items_view_of_bytes_value()])
            }
        )

    def test_iv_generator_in_generator_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_items_view_of_generator())]
                )
            }
        )

    def test_clean_iv_in_generator_in_delegating_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {
                "k": ListSubclass(
                    [
                        _generator_of(
                            {1: CLEAN_TEXT.encode()}.items()
                        )
                    ]
                )
            }
        )


class TestPromoteFixR28ItemsViewNestedInDelegating(_WrapperCase):
    """Ruling 1381, S15-R28-PROM-5: an items view
    carrying a nested mapping in its value, standing
    inside a delegating container subclass standing
    as a mapping value inside a ChainMap item
    mapping, clearing through the wrapper where the
    direct act fires."""

    def test_iv_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass([_items_view_of_nested_value()])
            }
        )

    def test_iv_nested_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": TupleSubclass([_items_view_of_nested_value()])
            }
        )

    def test_iv_nested_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SetSubclass([_items_view_of_nested_value()])
            }
        )

    def test_iv_nested_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": DequeSubclass([_items_view_of_nested_value()])
            }
        )

    def test_iv_nested_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": UserListSubclass(
                    [_items_view_of_nested_value()]
                )
            }
        )

    def test_iv_nested_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SequenceSubclass(
                    [_items_view_of_nested_value()]
                )
            }
        )

    def test_iv_nested_in_delegating_abstract_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": AbstractSetSubclass(
                    [_items_view_of_nested_value()]
                )
            }
        )

    def test_iv_nested_in_delegating_one_mapping_deeper(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": {
                    "j": ListSubclass(
                        [_items_view_of_nested_value()]
                    )
                }
            }
        )

    def test_iv_nested_in_delegating_at_candidate(self):
        self._assert_candidate_fires(
            {"k": ListSubclass([_items_view_of_nested_value()])}
        )

    def test_iv_nested_at_mapping_value_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _items_view_of_nested_value()}
        )

    def test_iv_nested_in_plain_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_items_view_of_nested_value()]}
        )

    def test_iv_bytes_in_delegating_list_still_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass([_items_view_of_bytes_value()])
            }
        )

    def test_clean_iv_nested_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {
                "k": ListSubclass(
                    [_items_view_of_clean_nested_value()]
                )
            }
        )


class TestPromoteFixR28ChainMapInDelegatingCarrier(_WrapperCase):
    """Ruling 1382, S15-R28-PROM-6 absorbing
    S15-R28-SPAN-1: a delegating ChainMap subclass
    standing inside a delegating container subclass
    standing as a mapping value inside a ChainMap
    item mapping, and at the plain holdout positions
    the Spanning paper names, raising through the
    wrapper where the direct act decides."""

    def test_cm_nested_in_delegating_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_delegating_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": TupleSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_delegating_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SetSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_delegating_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": DequeSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_delegating_userlist_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": UserListSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_delegating_sequence_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SequenceSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_delegating_abstract_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": AbstractSetSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_nested_in_generator_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [
                        _generator_of(
                            DelegatingChainMapSubclass(
                                [_nested_position()]
                            )
                        )
                    ]
                )
            }
        )

    def test_cm_nested_in_plain_list_in_delegating_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [
                        [
                            DelegatingChainMapSubclass(
                                [_nested_position()]
                            )
                        ]
                    ]
                )
            }
        )

    def test_cm_nested_in_delegating_one_mapping_deeper(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": {
                    "j": ListSubclass(
                        [
                            DelegatingChainMapSubclass(
                                [_nested_position()]
                            )
                        ]
                    )
                }
            }
        )

    def test_cm_nested_in_delegating_at_candidate_fires(self):
        self._assert_candidate_fires(
            {
                "k": ListSubclass(
                    [DelegatingChainMapSubclass(
                        [_nested_position()]
                    )]
                )
            }
        )

    def test_cm_clean_in_delegating_sequence_clears(self):
        self._assert_chainmap_pair_clears_compared(
            lambda: {
                "k": SequenceSubclass(
                    [DelegatingChainMapSubclass(
                        [_clean_position()]
                    )]
                )
            }
        )

    def test_cm_in_delegating_list_at_items_position(self):
        self._assert_plain_holdout_pair(
            lambda: {
                "items": ListSubclass(
                    [
                        DelegatingChainMapSubclass(
                            [{"k": _span_keys_view()}]
                        )
                    ]
                )
            },
            False,
            0,
        )

    def test_cm_in_delegating_list_as_items_mapping_value(self):
        self._assert_plain_holdout_pair(
            lambda: {
                "items": {
                    "o": ListSubclass(
                        [
                            DelegatingChainMapSubclass(
                                [{"k": _span_keys_view()}]
                            )
                        ]
                    )
                }
            },
            False,
            0,
        )

    def test_cm_in_delegating_list_at_holdout_items_position(self):
        self._assert_plain_holdout_pair(
            lambda: {
                "holdout_items": ListSubclass(
                    [
                        DelegatingChainMapSubclass(
                            [{"k": _span_keys_view()}]
                        )
                    ]
                )
            },
            True,
            1,
        )

    def test_cm_in_delegating_list_as_holdout_mapping_value(self):
        self._assert_plain_holdout_pair(
            lambda: {
                "holdout_items": {
                    "o": ListSubclass(
                        [
                            DelegatingChainMapSubclass(
                                [{"k": _span_keys_view()}]
                            )
                        ]
                    )
                }
            },
            False,
            0,
        )

    def test_cm_clean_in_delegating_list_at_holdout_items(self):
        self._assert_plain_holdout_pair(
            lambda: {
                "holdout_items": ListSubclass(
                    [
                        DelegatingChainMapSubclass(
                            [{"k": _span_keys_view(CLEAN_TEXT)}]
                        )
                    ]
                )
            },
            False,
            1,
        )

    def test_cm_nested_at_mapping_value_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": DelegatingChainMapSubclass(
                    [_nested_position()]
                )
            }
        )

    def test_cm_nested_in_plain_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": [
                    DelegatingChainMapSubclass(
                        [_nested_position()]
                    )
                ]
            }
        )

    def test_cm_nested_in_generator_at_map_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": _generator_of(
                    DelegatingChainMapSubclass(
                        [_nested_position()]
                    )
                )
            }
        )
