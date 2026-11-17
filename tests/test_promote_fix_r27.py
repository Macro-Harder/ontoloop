"""Fix round 27 tests for Region 3: promote wrapper.

Written first for five positions at Round 27 triage
rulings 1284 (S15-R27-PROMOTE-1, Low), 1285
(S15-R27-PROMOTE-2, Low), 1286 (S15-R27-PROMOTE-3,
Low), 1287 (S15-R27-PROMOTE-4, Low), and 1288
(S15-R27-PROMOTE-5, Low). Ruling 1284: a byte form
carrying the sealed holdout text standing inside a
plain container or a single pass form standing as a
mapping value inside a mapping standing as an item
of a delegating ChainMap subclass, clearing through
the promote wrapper where the direct act fires.
Ruling 1285: a keys view carrying byte text or a
memoryview of the sealed text standing inside a
plain container or a single pass form at the same
position, clearing through the wrapper where the
direct act fires. Ruling 1286: an items view
carrying byte text or a memoryview of the sealed
text in its value, standing as a mapping value
inside the same item mapping, clearing through the
wrapper where the direct act fires. Ruling 1287: an
items view carrying byte text in its value, standing
inside a delegating container subclass standing as
a mapping value inside the same item mapping, firing
through the wrapper where the direct act clears.
Ruling 1288: a delegating ChainMap subclass standing
as a mapping value inside the same item mapping,
raising through the wrapper on hit material and on
clean material alike, where the direct act decides
the presentation. Rulings 1196, 1197, and 1198 stand
cured in their bounded forms and stand not reopened
by any pin here: their charged forms stand as poles,
beside the standing parity forms the Round 27 papers
name.
"""

import unittest
from collections import ChainMap, deque

from tests.harness import require
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


def _items_view_of_bytes_key():
    return {_bytes(): 1}.items()


def _items_view_of_generator():
    return {1: _generator_of(_nested_position())}.items()


def _values_view_of_bytes():
    return {1: _bytes()}.values()


def _values_view_of_memoryview():
    return {1: _memoryview()}.values()


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


class TestPromoteFixR27ByteFormInPlainCarrier(_WrapperCase):
    """Ruling 1284, S15-R27-PROMOTE-1: a byte form
    inside a plain container or a single pass form
    standing as a mapping value inside a ChainMap
    item mapping."""

    def test_bytes_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_bytes()]}
        )

    def test_bytes_in_plain_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": (_bytes(),)}
        )

    def test_bytes_in_plain_set_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": {_bytes()}}
        )

    def test_bytes_in_frozenset_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": frozenset([_bytes()])}
        )

    def test_bytes_in_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": deque([_bytes()])}
        )

    def test_bytes_in_userlist_fires(self):
        from collections import UserList

        self._assert_chainmap_pair_fires(
            lambda: {"k": UserList([_bytes()])}
        )

    def test_bytes_in_generator_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _generator_of(_bytes())}
        )

    def test_bytes_in_single_pass_iterable_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SinglePassIterable([_bytes()])}
        )

    def test_memoryview_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_memoryview()]}
        )

    def test_bytes_in_plain_set_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": {"j": {_bytes()}}}
        )

    def test_bytes_at_candidate_construction_fires(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": [_bytes()]}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_bytes_after_partial_scoring_fires(self):
        outcome = self._wrapper(
            _chainmap_item({"k": [_bytes()]}),
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_bytearray_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [bytearray(_bytes())]}
        )

    def test_clean_bytes_in_plain_set_clears(self):
        outcome = self._wrapper(
            _chainmap_item({"k": {CLEAN_TEXT.encode()}})
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item({"k": {CLEAN_TEXT.encode()}})
        )
        self.assertFalse(direct_outcome["fired"])

    def test_bytes_alone_at_mapping_value_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _bytes()}
        )

    def test_bytes_in_delegating_list_still_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": ListSubclass([_bytes()])}
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {"k": ListSubclass([_bytes()])}
            )
        )
        self.assertFalse(direct_outcome["fired"])


class TestPromoteFixR27KeysViewInPlainCarrier(_WrapperCase):
    """Ruling 1285, S15-R27-PROMOTE-2: a keys view
    carrying byte text or a memoryview standing
    inside a plain container or a single pass form
    at a mapping value inside a ChainMap item
    mapping."""

    def test_kv_bytes_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_keys_view_of_bytes()]}
        )

    def test_kv_bytes_in_plain_tuple_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": (_keys_view_of_bytes(),)}
        )

    def test_kv_bytes_in_deque_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": deque([_keys_view_of_bytes()])}
        )

    def test_kv_bytes_in_userlist_fires(self):
        from collections import UserList

        self._assert_chainmap_pair_fires(
            lambda: {"k": UserList([_keys_view_of_bytes()])}
        )

    def test_kv_bytes_in_generator_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": _generator_of(_keys_view_of_bytes())
            }
        )

    def test_kv_bytes_in_single_pass_iterable_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SinglePassIterable(
                    [_keys_view_of_bytes()]
                )
            }
        )

    def test_kv_bytes_in_iterator_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": iter([_keys_view_of_bytes()])}
        )

    def test_kv_bytes_in_zip_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": zip([_keys_view_of_bytes()])}
        )

    def test_kv_bytes_in_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": map(
                    lambda x: x, [_keys_view_of_bytes()]
                )
            }
        )

    def test_kv_bytes_in_list_in_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [[_keys_view_of_bytes()]]}
        )

    def test_kv_bytes_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": {"j": [_keys_view_of_bytes()]}}
        )

    def test_kv_memoryview_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_keys_view_of_memoryview()]}
        )

    def test_kv_memoryview_in_generator_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": _generator_of(
                    _keys_view_of_memoryview()
                )
            }
        )

    def test_kv_bytes_at_candidate_construction_fires(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": [_keys_view_of_bytes()]}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_kv_bytes_alone_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _keys_view_of_bytes()}
        )

    def test_kv_bytes_in_delegating_list_still_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": ListSubclass([_keys_view_of_bytes()])}
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {"k": ListSubclass([_keys_view_of_bytes()])}
            )
        )
        self.assertFalse(direct_outcome["fired"])

    def test_kv_bytes_in_delegating_set_still_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": SetSubclass([_keys_view_of_bytes()])}
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {"k": SetSubclass([_keys_view_of_bytes()])}
            )
        )
        self.assertFalse(direct_outcome["fired"])

    def test_kv_generator_in_plain_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_keys_view_of_generator()]}
        )

    def test_clean_kv_bytes_in_plain_list_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": [{CLEAN_TEXT.encode(): 1}.keys()]}
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {"k": [{CLEAN_TEXT.encode(): 1}.keys()]}
            )
        )
        self.assertFalse(direct_outcome["fired"])

    def test_kv_bytes_in_getitem_only_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": GetitemOnlyForm([_keys_view_of_bytes()])
            }
        )


class TestPromoteFixR27ItemsViewAtMappingValue(_WrapperCase):
    """Ruling 1286, S15-R27-PROMOTE-3: an items view
    carrying byte text or a memoryview in its value,
    standing as a mapping value inside a ChainMap
    item mapping."""

    def test_iv_bytes_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _items_view_of_bytes_value()}
        )

    def test_iv_memoryview_value_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": _items_view_of_memoryview_value()
            }
        )

    def test_iv_bytes_value_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": {"j": _items_view_of_bytes_value()}
            }
        )

    def test_iv_bytes_value_in_map_in_list_as_item_fires(self):
        outcome = self._wrapper(
            _chainmap_item(
                [{"k": _items_view_of_bytes_value()}]
            )
        )
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                [{"k": _items_view_of_bytes_value()}]
            )
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_iv_bytes_value_at_candidate_construction_fires(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": _items_view_of_bytes_value()}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_iv_bytes_value_after_partial_scoring_fires(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": _items_view_of_bytes_value()}
            ),
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_iv_bytes_value_in_plain_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_items_view_of_bytes_value()]}
        )

    def test_iv_bytes_value_in_generator_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": _generator_of(
                    _items_view_of_bytes_value()
                )
            }
        )

    def test_iv_bytes_key_still_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": _items_view_of_bytes_key()}
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {"k": _items_view_of_bytes_key()}
            )
        )
        self.assertFalse(direct_outcome["fired"])

    def test_vv_bytes_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _values_view_of_bytes()}
        )

    def test_vv_memoryview_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _values_view_of_memoryview()}
        )

    def test_iv_generator_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _items_view_of_generator()}
        )

    def test_clean_iv_bytes_value_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": {1: CLEAN_TEXT.encode()}.items()}
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {"k": {1: CLEAN_TEXT.encode()}.items()}
            )
        )
        self.assertFalse(direct_outcome["fired"])


class TestPromoteFixR27ItemsViewInDelegatingCarrier(_WrapperCase):
    """Ruling 1287, S15-R27-PROMOTE-4: an items view
    carrying byte text in its value, standing inside
    a delegating container subclass standing as a
    mapping value inside a ChainMap item mapping,
    in the firing direction."""

    def test_iv_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_tuple_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": TupleSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_set_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": SetSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_deque_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_userlist_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": UserListSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_sequence_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": SequenceSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_abstract_set_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": AbstractSetSubclass(
                    [_items_view_of_bytes_value()]
                )
            }
        )

    def test_iv_in_delegating_list_one_mapping_deeper_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": {
                    "j": ListSubclass(
                        [_items_view_of_bytes_value()]
                    )
                }
            }
        )

    def test_iv_in_delegating_list_in_map_in_list_as_item_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                [
                    {
                        "k": ListSubclass(
                            [_items_view_of_bytes_value()]
                        )
                    }
                ]
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                [
                    {
                        "k": ListSubclass(
                            [_items_view_of_bytes_value()]
                        )
                    }
                ]
            )
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_clean_iv_in_delegating_list_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass(
                    [{1: CLEAN_TEXT.encode()}.items()]
                )
            }
        )

    def test_iv_generator_in_delegating_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_items_view_of_generator()]
                )
            }
        )

    def test_iv_bytes_value_in_plain_list_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_items_view_of_bytes_value()]}
        )


class TestPromoteFixR27DelegatingChainMapValue(_WrapperCase):
    """Ruling 1288, S15-R27-PROMOTE-5: a delegating
    ChainMap subclass standing as a mapping value
    inside a ChainMap item mapping, raising through
    the wrapper in place of a decision."""

    def test_delegating_chainmap_nested_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": DelegatingChainMapSubclass(
                    [_nested_position()]
                )
            }
        )

    def test_delegating_chainmap_nested_in_plain_list_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": [
                    DelegatingChainMapSubclass(
                        [_nested_position()]
                    )
                ]
            }
        )

    def test_delegating_chainmap_nested_at_candidate_fires(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {
                    "k": DelegatingChainMapSubclass(
                        [_nested_position()]
                    )
                }
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_delegating_chainmap_keys_view_generator_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": DelegatingChainMapSubclass(
                    [_keys_view_of_generator()]
                )
            }
        )

    def test_delegating_chainmap_plain_text_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": DelegatingChainMapSubclass(
                    [HOLDOUT_TEXT]
                )
            }
        )

    def test_delegating_chainmap_clean_nested_clears(self):
        outcome = self._wrapper(
            _chainmap_item(
                {
                    "k": DelegatingChainMapSubclass(
                        [_clean_position()]
                    )
                }
            )
        )
        self._assert_clears(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                {
                    "k": DelegatingChainMapSubclass(
                        [_clean_position()]
                    )
                }
            )
        )
        self.assertFalse(direct_outcome["fired"])

    def test_delegating_chainmap_clean_at_candidate_clears(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {
                    "k": DelegatingChainMapSubclass(
                        [_clean_position()]
                    )
                }
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_plain_chainmap_nested_still_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ChainMap(_nested_position())}
        )


if __name__ == "__main__":
    unittest.main()
