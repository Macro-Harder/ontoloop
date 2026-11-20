"""Fix round 30 tests for Region 3: promote wrapper.

Written first for three positions at Round 30 triage
rulings 1578 (S15-R30-PROM-1, Low), 1579
(S15-R30-PROM-2, Low), and 1580 (S15-R30-PROM-3,
Low). Ruling 1578: a text carrying element standing
inside a delegating concrete container subclass
standing in a composed carrier position at a mapping
value inside a mapping standing as an item of a
delegating ChainMap subclass, raising through the
promote wrapper by unbounded recursion where the
direct act decides the presentation, on hit material
and on clean material alike. Ruling 1579: a
delegating ChainMap subclass standing inside a
single pass form standing inside a delegating
concrete container subclass at the same position,
clearing through the promote wrapper where the
direct act fires on the presentation. Ruling 1580:
a plain payload form standing inside a single pass
form standing inside a delegating concrete container
subclass at the same position, clearing through the
promote wrapper where the direct act fires on the
presentation. Ruling 1478 stands cured in its
bounded form and stands not reopened by any pin
here: its charged forms stand as poles beside the
new forms.
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


def _chainmap_nested():
    return DelegatingChainMapSubclass([_nested_position()])


def _chainmap_clean():
    return DelegatingChainMapSubclass([_clean_position()])


def _chainmap_bytes():
    return DelegatingChainMapSubclass([HOLDOUT_TEXT.encode()])


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

    def _assert_pair_fires(self, make_item, comparisons=1):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"],
            comparisons,
        )
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], comparisons)

    def _assert_pair_clears(self, make_item, comparisons=0):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], comparisons)

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


class TestPromoteFixR30TextCarryingElement(_WrapperCase):
    """Ruling 1578, S15-R30-PROM-1: a text carrying
    element inside a delegating concrete container
    subclass standing in a composed carrier position
    at a mapping value inside a ChainMap item mapping,
    raising through the wrapper by unbounded recursion
    where the direct act decides the presentation."""

    def test_holdout_text_in_delegating_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass(
                [ListSubclass([HOLDOUT_TEXT])])}
        )

    def test_clean_text_in_delegating_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass(
                [ListSubclass([CLEAN_TEXT])])}
        )

    def test_text_in_delegating_tuple_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass(
                [TupleSubclass([HOLDOUT_TEXT])])}
        )

    def test_nested_in_delegating_tuple_clears(self):
        make_holdout = lambda: {"k": ListSubclass(
                [TupleSubclass([_nested_position()])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_nested_in_delegating_deque_clears(self):
        make_holdout = lambda: {"k": ListSubclass(
                [DequeSubclass([_nested_position()])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_nested_in_delegating_userlist_clears(self):
        make_holdout = lambda: {"k": ListSubclass(
                [UserListSubclass([_nested_position()])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_nested_in_delegating_set_clears(self):
        make_holdout = lambda: {"k": ListSubclass(
                [SetSubclass([_nested_position()])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_plain_list_nested_in_delegating_clears(self):
        make_holdout = lambda: {"k": ListSubclass(
                [ListSubclass([[_nested_position()]])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_mapping_text_value_in_delegating_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": HOLDOUT_TEXT}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_plain_tuple_text_in_delegating_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [(HOLDOUT_TEXT,)])])}
        )

    def test_chainmap_beside_text_in_carrier_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [_chainmap_nested(), HOLDOUT_TEXT])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_text_carrier_in_plain_list_value_clears(self):
        self._assert_pair_clears(
            lambda: {"k": [ListSubclass(
                [ListSubclass([HOLDOUT_TEXT])])]}
        )

    def test_text_carrier_in_generator_value_clears(self):
        self._assert_pair_clears(
            lambda: {"k": _generator_of(ListSubclass(
                [ListSubclass([HOLDOUT_TEXT])]))}
        )

    def test_text_carrier_one_mapping_deeper_clears(self):
        self._assert_pair_clears(
            lambda: {"k": {"j": ListSubclass(
                [ListSubclass([HOLDOUT_TEXT])])}}
        )

    def test_text_carrier_candidate_clears(self):
        self._assert_candidate_clears(
            lambda: {"k": ListSubclass(
                [ListSubclass([HOLDOUT_TEXT])])}
        )

    def test_int_in_delegating_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass([7])])}
        )

    def test_bytes_in_delegating_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass(
                [ListSubclass([_bytes()])])}
        )

    def test_nested_in_delegating_sequence_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass(
                [SequenceSubclass([_nested_position()])])}
        )


class TestPromoteFixR30ChainmapInSinglePass(_WrapperCase):
    """Ruling 1579, S15-R30-PROM-2: a delegating
    ChainMap subclass standing inside a single pass
    form standing inside a delegating concrete
    container subclass at the composed position,
    clearing through the wrapper where the direct
    act fires on the presentation."""

    def test_cm_in_gen_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_spi_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([_chainmap_nested()])])])}
        )

    def test_cm_in_gen_in_delegating_tuple_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [TupleSubclass(
                    [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_gen_in_delegating_set_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [SetSubclass(
                    [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_gen_in_delegating_deque_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [DequeSubclass(
                    [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_gen_in_delegating_userlist_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [UserListSubclass(
                    [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_spi_in_delegating_tuple_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [TupleSubclass([SinglePassIterable(
                    [_chainmap_nested()])])])}
        )

    def test_cm_gen_carrier_in_plain_list_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": [ListSubclass([ListSubclass(
                [_generator_of(_chainmap_nested())])])]}
        )

    def test_cm_gen_carrier_in_generator_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(ListSubclass(
                [ListSubclass(
                    [_generator_of(_chainmap_nested())])]))}
        )

    def test_cm_gen_in_delegating_sequence_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": SequenceSubclass([ListSubclass(
                [ListSubclass(
                    [_generator_of(_chainmap_nested())])])])}
        )

    def test_cm_in_gen_one_mapping_deeper_fires(self):
        self._assert_pair_fires(
            lambda: {"k": {"j": ListSubclass([ListSubclass(
                [_generator_of(_chainmap_nested())])])}}
        )

    def test_cm_in_gen_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_values_view_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(
                    _values_view_of(_chainmap_nested()))])])}
        )

    def test_cm_clean_in_gen_clears_compared(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_chainmap_clean())])])},
            comparisons=1,
        )

    def test_cm_bytes_in_gen_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_chainmap_bytes())])])}
        )

    def test_cm_in_gen_in_delegating_sequence_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [SequenceSubclass(
                    [_generator_of(_chainmap_nested())])])}
        )

    def test_cm_in_delegating_list_in_gen_clears(self):
        make_holdout = lambda: {"k": ListSubclass([_generator_of(
                ListSubclass([_chainmap_nested()]))])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_delegating_list_in_spi_clears(self):
        make_holdout = lambda: {"k": ListSubclass([SinglePassIterable(
                [ListSubclass([_chainmap_nested()])])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)


class TestPromoteFixR30PayloadInSinglePass(_WrapperCase):
    """Ruling 1580, S15-R30-PROM-3: a plain payload
    form standing inside a single pass form standing
    inside a delegating concrete container subclass
    at the composed position, clearing through the
    wrapper where the direct act fires."""

    def test_bytes_in_gen_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_bytes())])])}
        )

    def test_nested_in_gen_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_nested_position())])])}
        )

    def test_nested_in_spi_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([_nested_position()])])])}
        )

    def test_values_view_nested_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(
                    _values_view_of(_nested_position()))])])}
        )

    def test_keys_view_wrapped_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(
                    _keys_view_of(_wrapped_key()))])])}
        )

    def test_items_view_wrapped_key_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_items_view_of_pair(
                    _wrapped_key(), CLEAN_TEXT))])])},
            comparisons=2,
        )

    def test_items_view_nested_in_spi_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable(
                    [_items_view_of_value(
                        _nested_position())])])])}
        )

    def test_mapping_text_value_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of({"x": HOLDOUT_TEXT})])])}
        )

    def test_bytes_in_spi_in_delegating_tuple_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [TupleSubclass([SinglePassIterable(
                    [_bytes()])])])}
        )

    def test_nested_in_gen_in_delegating_deque_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [DequeSubclass(
                    [_generator_of(_nested_position())])])}
        )

    def test_bytes_in_gen_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_bytes())])])}
        )

    def test_bytes_in_gen_at_mapping_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(_bytes())}
        )

    def test_nested_in_gen_in_plain_list_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": [_generator_of(_nested_position())]}
        )

    def test_bytes_in_delegating_list_no_gen_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass(
                [ListSubclass([_bytes()])])}
        )
