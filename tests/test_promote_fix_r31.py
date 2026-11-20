"""Fix round 31 tests for Region 3: promote wrapper.

Written first for five positions at Round 31 triage
rulings 1683 (S15-R31-PROM-1, Low), 1684
(S15-R31-PROM-2, Low), 1685 (S15-R31-PROM-3, Low),
1686 (S15-R31-PROM-4, Low), and 1687
(S15-R31-PROM-5, Low). Ruling 1683: a delegating
ChainMap subclass and plain payload forms standing
inside a nested single pass form standing inside a
delegating concrete container subclass standing in
a composed carrier position at a mapping value
inside a mapping standing as an item of a delegating
ChainMap subclass, clearing through the promote
wrapper where the direct act fires on the
presentation. Ruling 1684: a bare text form standing
inside a single pass form at the same position,
clearing through the promote wrapper where the
direct act fires. Ruling 1685: a single pass form
standing inside a mapping standing as an element of
a delegating concrete container subclass at the same
position, firing through the promote wrapper where
the direct act clears. Ruling 1686: a delegating
concrete container subclass carrying a single pass
form standing inside a dictionary view standing as
a mapping value inside a mapping standing as an item
of a delegating ChainMap subclass, clearing through
the promote wrapper where the direct act fires.
Ruling 1687: a self referential plain container
standing as an element of a delegating concrete
container subclass at the same position, raising
through the promote wrapper by unbounded recursion
where the direct act decides the presentation, on
hit material and on clean material alike. Rulings
1578 to 1580 and ruling 1478 stand cured in their
bounded forms and stand not reopened by any pin
here: their charged forms stand as poles beside the
new forms, and the restated pin in
tests/test_promote_fix_r26.py stands untouched.
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


def _self_list():
    carried = []
    carried.append(carried)
    return carried


def _self_mapping():
    carried = {}
    carried["s"] = carried
    return carried


def _self_list_via_tuple():
    carried = []
    carried.append((carried,))
    return carried


def _self_list_clean():
    carried = [7]
    carried.append(carried)
    return carried


def _self_delegating():
    carried = ListSubclass([1])
    carried._stored = iter([carried])
    return carried


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


class TestPromoteFixR31NestedSinglePass(_WrapperCase):
    """Ruling 1683, S15-R31-PROM-1: a delegating
    ChainMap subclass and plain payload forms inside
    a nested single pass form inside a delegating
    concrete container subclass at the composed
    carrier position, clearing through the wrapper
    where the direct act fires."""

    def test_cm_in_gen_in_gen_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_chainmap_nested()))])])}
        )

    def test_cm_in_spi_in_spi_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([SinglePassIterable(
                    [_chainmap_nested()])])])])}
        )

    def test_cm_in_spi_in_gen_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(SinglePassIterable(
                    [_chainmap_nested()]))])])}
        )

    def test_cm_in_gen_in_spi_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([_generator_of(
                    _chainmap_nested())])])])}
        )

    def test_cm_in_gen_in_gen_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_generator_of(
                    _chainmap_nested())))])])}
        )

    def test_cm_in_gen_in_gen_in_delegating_tuple_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [TupleSubclass([_generator_of(_generator_of(
                    _chainmap_nested()))])])}
        )

    def test_cm_in_gen_in_gen_in_delegating_deque_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [DequeSubclass([_generator_of(_generator_of(
                    _chainmap_nested()))])])}
        )

    def test_cm_in_gen_in_gen_in_delegating_set_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [SetSubclass([_generator_of(_generator_of(
                    _chainmap_nested()))])])}
        )

    def test_cm_in_gen_in_gen_in_delegating_userlist_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [UserListSubclass([_generator_of(_generator_of(
                    _chainmap_nested()))])])}
        )

    def test_cm_nested_carrier_in_sequence_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": SequenceSubclass([ListSubclass(
                [ListSubclass([_generator_of(_generator_of(
                    _chainmap_nested()))])])])}
        )

    def test_cm_nested_one_mapping_deeper_fires(self):
        self._assert_pair_fires(
            lambda: {"k": {"j": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_chainmap_nested()))])])}}
        )

    def test_cm_nested_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_chainmap_nested()))])])}
        )

    def test_bytes_in_gen_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_bytes()))])])}
        )

    def test_bytes_in_spi_in_spi_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([SinglePassIterable(
                    [_bytes()])])])])}
        )

    def test_nested_in_gen_in_spi_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([_generator_of(
                    _nested_position())])])])}
        )

    def test_nested_in_spi_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(SinglePassIterable(
                    [_nested_position()]))])])}
        )

    def test_items_view_wrapped_key_in_spi_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([_generator_of(
                    _items_view_of_pair(
                        _wrapped_key(), CLEAN_TEXT))])])])},
            comparisons=2,
        )

    def test_cm_in_gen_in_mapping_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of({"x": _generator_of(
                    _chainmap_nested())})])])}
        )

    def test_cm_in_gen_in_gen_as_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(_generator_of(
                _chainmap_nested()))}
        )

    def test_cm_in_gen_in_gen_in_plain_list_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": [_generator_of(_generator_of(
                _chainmap_nested()))]}
        )

    def test_cm_clean_in_gen_in_gen_clears_compared(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_chainmap_clean()))])])},
            comparisons=1,
        )

    def test_cm_bytes_in_gen_in_gen_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(_generator_of(_chainmap_bytes()))])])}
        )


class TestPromoteFixR31BareTextInSinglePass(_WrapperCase):
    """Ruling 1684, S15-R31-PROM-2: a bare text form
    inside a single pass form inside a delegating
    concrete container subclass at the composed
    carrier position, clearing through the wrapper
    where the direct act fires."""

    def test_text_in_gen_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(HOLDOUT_TEXT)])])}
        )

    def test_text_in_spi_in_delegating_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [SinglePassIterable([HOLDOUT_TEXT])])])}
        )

    def test_text_in_gen_in_delegating_tuple_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [TupleSubclass([_generator_of(HOLDOUT_TEXT)])])}
        )

    def test_text_in_gen_in_delegating_deque_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [DequeSubclass([_generator_of(HOLDOUT_TEXT)])])}
        )

    def test_text_in_gen_in_delegating_set_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [SetSubclass([_generator_of(HOLDOUT_TEXT)])])}
        )

    def test_text_in_gen_in_delegating_userlist_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass(
                [UserListSubclass([_generator_of(HOLDOUT_TEXT)])])}
        )

    def test_text_carrier_in_sequence_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": SequenceSubclass([ListSubclass(
                [ListSubclass([_generator_of(HOLDOUT_TEXT)])])])}
        )

    def test_text_one_mapping_deeper_fires(self):
        self._assert_pair_fires(
            lambda: {"k": {"j": ListSubclass([ListSubclass(
                [_generator_of(HOLDOUT_TEXT)])])}}
        )

    def test_text_in_gen_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(HOLDOUT_TEXT)])])}
        )

    def test_tuple_text_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of((HOLDOUT_TEXT,))])])}
        )

    def test_list_text_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of([HOLDOUT_TEXT])])])}
        )

    def test_clean_text_in_gen_clears_compared(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(CLEAN_TEXT)])])},
            comparisons=1,
        )

    def test_mapping_text_value_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of({"x": HOLDOUT_TEXT})])])}
        )

    def test_int_in_gen_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [_generator_of(7)])])}
        )


class TestPromoteFixR31SinglePassInMappingInCarrier(_WrapperCase):
    """Ruling 1685, S15-R31-PROM-3: a single pass form
    inside a mapping standing as an element of a
    delegating concrete container subclass at the
    composed carrier position, firing through the
    wrapper where the direct act clears."""

    def test_cm_in_gen_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(_chainmap_nested())}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_in_spi_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": SinglePassIterable(
                    [_chainmap_nested()])}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_nested_in_gen_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(_nested_position())}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_bytes_in_gen_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(_bytes())}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_bytes_in_spi_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": SinglePassIterable([_bytes()])}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_values_view_in_gen_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(
                    _values_view_of(_nested_position()))}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_keys_view_wrapped_in_gen_at_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(
                    _keys_view_of(_wrapped_key()))}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_items_view_wrapped_in_gen_at_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(_items_view_of_pair(
                    _wrapped_key(), CLEAN_TEXT))}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 2)

    def test_mapping_in_tuple_in_carrier_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [({"x": _generator_of(_chainmap_nested())},)])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_mapping_in_plain_list_in_carrier_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [[{"x": _generator_of(_chainmap_nested())}]])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_mapping_carrier_in_sequence_value_clears(self):
        make_holdout = lambda: {"k": SequenceSubclass([ListSubclass(
                [ListSubclass(
                    [{"x": _generator_of(_chainmap_nested())}])])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_mapping_one_mapping_deeper_clears(self):
        make_holdout = lambda: {"k": {"j": ListSubclass([ListSubclass(
                [{"x": _generator_of(_chainmap_nested())}])])}}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_gen_at_value_candidate_clears(self):
        self._assert_candidate_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(_chainmap_nested())}])])}
        )

    def test_cm_at_mapping_value_no_pass_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _chainmap_nested()}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_clean_in_gen_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(_chainmap_clean())}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_int_in_gen_at_mapping_value_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(7)}])])}
        )

    def test_text_in_gen_at_mapping_value_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [{"x": _generator_of(HOLDOUT_TEXT)}])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)


class TestPromoteFixR31CarrierChainInView(_WrapperCase):
    """Ruling 1686, S15-R31-PROM-4: a delegating
    concrete container subclass carrying a single
    pass form standing inside a dictionary view
    standing as a mapping value inside a mapping
    standing as an item of a delegating ChainMap
    subclass, clearing through the wrapper where the
    direct act fires."""

    def test_cm_gen_chain_in_values_view_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _values_view_of(ListSubclass(
                [ListSubclass([_generator_of(_chainmap_nested())])]))}
        )

    def test_cm_gen_chain_in_items_view_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _items_view_of_value(ListSubclass(
                [ListSubclass([_generator_of(_chainmap_nested())])]))}
        )

    def test_bytes_gen_chain_in_values_view_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _values_view_of(ListSubclass(
                [ListSubclass([_generator_of(_bytes())])]))}
        )

    def test_bytes_gen_chain_in_items_view_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _items_view_of_value(ListSubclass(
                [ListSubclass([_generator_of(_bytes())])]))}
        )

    def test_cm_gen_chain_in_values_view_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": _values_view_of(ListSubclass(
                [ListSubclass([_generator_of(_chainmap_nested())])]))}
        )

    def test_cm_chain_no_pass_in_values_view_clears(self):
        make_holdout = lambda: {"k": _values_view_of(ListSubclass(
                [ListSubclass([_chainmap_nested()])]))}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_cm_clean_gen_chain_in_values_view_clears(self):
        self._assert_pair_clears(
            lambda: {"k": _values_view_of(ListSubclass(
                [ListSubclass([_generator_of(_chainmap_clean())])]))},
            comparisons=1,
        )

    def test_chain_in_gen_at_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(ListSubclass(
                [ListSubclass([_generator_of(_chainmap_nested())])]))}
        )


class TestPromoteFixR31SelfReferentialCarrierElement(_WrapperCase):
    """Ruling 1687, S15-R31-PROM-5: a self referential
    plain container standing as an element of a
    delegating concrete container subclass at the
    composed carrier position, raising through the
    wrapper by unbounded recursion where the direct
    act decides the presentation."""

    def test_self_list_in_delegating_list_decides(self):
        outcome = self._wrapper(_chainmap_item(
            {"k": ListSubclass([ListSubclass([_self_list()])])}
        ))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(
            {"k": ListSubclass([ListSubclass([_self_list()])])}
        ))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_mapping_in_delegating_list_clears(self):
        make_holdout = lambda: {"k": ListSubclass([ListSubclass(
                [_self_mapping()])])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_via_tuple_in_delegating_decides(self):
        outcome = self._wrapper(_chainmap_item(
            {"k": ListSubclass([ListSubclass(
                [_self_list_via_tuple()])])}
        ))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(
            {"k": ListSubclass([ListSubclass(
                [_self_list_via_tuple()])])}
        ))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_clean_in_delegating_decides(self):
        outcome = self._wrapper(_chainmap_item(
            {"k": ListSubclass([ListSubclass(
                [_self_list_clean()])])}
        ))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(
            {"k": ListSubclass([ListSubclass(
                [_self_list_clean()])])}
        ))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_candidate_decides(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": ListSubclass([ListSubclass([_self_list()])])}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_delegating_self_in_delegating_clears(self):
        make_holdout = lambda: {"k": ListSubclass([_self_delegating()])}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_int_in_delegating_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass([7])])}
        )

    def test_bytes_in_delegating_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": ListSubclass([ListSubclass([_bytes()])])}
        )


if __name__ == "__main__":
    unittest.main()
