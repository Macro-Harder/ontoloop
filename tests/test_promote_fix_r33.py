"""Fix round 33 tests for Region 3: promote wrapper.

Written first for five positions at Round 33 triage
rulings 1911 (S15-R33-PROM-1, Low), 1912
(S15-R33-PROM-2, Low), 1913 (S15-R33-PROM-3, Low),
1914 (S15-R33-PROM-4, Low), and 1915
(S15-R33-PROM-5, Low). Ruling 1911: a bare text form
standing inside a single pass form standing inside a
dictionary view value standing as an element of the
delegating concrete container carrier at the composed
position, and a bare text form standing inside a
single pass form standing inside a single pass form
standing as a plain mapping value with no carrier,
each clearing through the promote wrapper where the
direct act fires, one ring beyond ruling 1684.
Ruling 1912: a delegating ChainMap form standing at
three stated geometries of the values view limb, one
ring further out from ruling 1686, each clearing
through the promote wrapper where the direct act
fires. Ruling 1913: a delegating ChainMap form
standing inside a single pass form standing as the
value paired with a wrapped key carrying the nested
position, the pair standing inside an items view
standing as an element of the carrier at the composed
position, clearing through the promote wrapper where
the direct act fires. Ruling 1914: a delegating
ChainMap form standing inside an items view standing
inside a single pass form standing as an element of
the carrier at the composed position, raising
TypeError at the promote wrapper in place of a
decision, where the direct act fires. Ruling 1915: a
self referential plain list standing inside a mapping
standing as an element of the delegating concrete
container carrier at the composed position, firing at
the promote wrapper in the refusal form where the
direct act clears, on hit material and on clean
material alike, one ring beyond ruling 1687. Rulings
1683 to 1687 stand cured in their bounded forms and
stand not reopened by any pin here: their charged
forms stand as poles beside the new forms, and the
restated pin in tests/test_promote_fix_r26.py stands
untouched.
"""

import unittest

from tests.harness import require
from tests.test_cross_fix_r20 import HashableItem, inner_mapping
from tests.test_promote_fix_r22 import (
    DelegatingChainMapSubclass,
    ListSubclass,
    SinglePassIterable,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _values_view_of(carried):
    return {1: carried}.values()


def _items_view_of_value(value):
    return {1: value}.items()


def _items_view_of_pair(key, value):
    return {key: value}.items()


def _wrapped_key(text=HOLDOUT_TEXT):
    if text == HOLDOUT_TEXT:
        return (HashableItem(inner_mapping()),)
    return (HashableItem({"inner": {"text": text}}),)


def _chainmap_nested():
    return DelegatingChainMapSubclass([_nested_position()])


def _chainmap_clean():
    return DelegatingChainMapSubclass([_clean_position()])


def _carrier(inner):
    return {"k": ListSubclass([ListSubclass([inner])])}


def _self_list():
    carried = []
    carried.append(carried)
    return carried


def _self_list_clean():
    carried = [7]
    carried.append(carried)
    return carried


def _self_list_via_tuple():
    carried = []
    carried.append((carried,))
    return carried


def _self_mapping():
    carried = {}
    carried["s"] = carried
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


class TestPromoteFixR33BareTextViewAndNestedPass(_WrapperCase):
    """Ruling 1911, S15-R33-PROM-1: a bare text form
    inside a single pass form inside a dictionary view
    value as an element of the carrier, and a bare text
    form inside two nested single pass forms as a plain
    mapping value, clearing through the wrapper where
    the direct act fires."""

    def test_text_in_gen_in_items_view_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_items_view_of_value(
                _generator_of(HOLDOUT_TEXT)))
        )

    def test_text_in_gen_in_values_view_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_values_view_of(
                _generator_of(HOLDOUT_TEXT)))
        )

    def test_text_in_spi_in_items_view_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_items_view_of_value(
                SinglePassIterable([HOLDOUT_TEXT])))
        )

    def test_text_in_gen_in_gen_at_plain_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(_generator_of(HOLDOUT_TEXT))}
        )

    def test_text_in_spi_in_spi_at_plain_value_fires(self):
        self._assert_pair_fires(
            lambda: {"k": SinglePassIterable(
                [SinglePassIterable([HOLDOUT_TEXT])])}
        )

    def test_text_in_gen_in_items_view_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: _carrier(_items_view_of_value(
                _generator_of(HOLDOUT_TEXT)))
        )

    def test_clean_text_in_gen_in_items_view_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(_items_view_of_value(
                _generator_of(CLEAN_TEXT))),
            comparisons=1,
        )

    def test_clean_text_in_gen_in_gen_at_plain_value_clears(self):
        self._assert_pair_clears(
            lambda: {"k": _generator_of(_generator_of(CLEAN_TEXT))},
            comparisons=1,
        )

    def test_text_in_gen_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_generator_of(HOLDOUT_TEXT))
        )

    def test_text_in_gen_in_gen_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_generator_of(
                _generator_of(HOLDOUT_TEXT)))
        )


class TestPromoteFixR33ChainMapValuesViewFurtherOut(_WrapperCase):
    """Ruling 1912, S15-R33-PROM-2: a delegating
    ChainMap form at three geometries of the values
    view limb one ring further out, clearing through
    the wrapper where the direct act fires."""

    def test_cm_in_gen_in_gen_in_values_view_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _values_view_of(_generator_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_nested())])])))}
        )

    def test_cm_chain_in_values_view_in_plain_list_fires(self):
        self._assert_pair_fires(
            lambda: {"k": [_values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_nested())])]))]}
        )

    def test_cm_chain_in_values_view_in_gen_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(_values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_nested())])])))}
        )

    def test_cm_chain_in_values_view_in_spi_fires(self):
        self._assert_pair_fires(
            lambda: {"k": SinglePassIterable([_values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_nested())])]))])}
        )

    def test_cm_chain_in_values_view_in_list_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: {"k": [_values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_nested())])]))]}
        )

    def test_cm_in_gen_in_values_view_still_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_nested())])]))}
        )

    def test_cm_in_gen_in_gen_in_carrier_chain_values_view_still_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_generator_of(
                        _chainmap_nested()))])]))}
        )

    def test_cm_clean_chain_in_values_view_in_list_clears(self):
        self._assert_pair_clears(
            lambda: {"k": [_values_view_of(
                ListSubclass([ListSubclass(
                    [_generator_of(_chainmap_clean())])]))]},
            comparisons=1,
        )

    def test_cm_gen_first_values_view_silent_still_clears(self):
        make_holdout = lambda: {"k": _values_view_of(_generator_of(
                ListSubclass([ListSubclass(
                    [_chainmap_nested()])])))}
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)


class TestPromoteFixR33ChainMapItemsViewKeySide(_WrapperCase):
    """Ruling 1913, S15-R33-PROM-3: a delegating
    ChainMap form inside a single pass form as the
    value paired with a wrapped key carrying the nested
    position, inside an items view as an element of the
    carrier, clearing through the wrapper where the
    direct act fires."""

    def test_cm_in_gen_paired_with_wrapped_key_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_items_view_of_pair(
                _wrapped_key(), _generator_of(_chainmap_nested()))),
            comparisons=2,
        )

    def test_wrapped_key_side_alone_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_items_view_of_pair(
                _wrapped_key(), _generator_of(_chainmap_clean()))),
            comparisons=2,
        )

    def test_cm_value_side_alone_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_items_view_of_pair(
                _wrapped_key(CLEAN_TEXT),
                _generator_of(_chainmap_nested()))),
            comparisons=2,
        )

    def test_cm_in_gen_paired_with_wrapped_key_candidate_fires(self):
        self._assert_candidate_fires(
            lambda: _carrier(_items_view_of_pair(
                _wrapped_key(), _generator_of(_chainmap_nested())))
        )

    def test_clean_key_and_clean_cm_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(_items_view_of_pair(
                _wrapped_key(CLEAN_TEXT),
                _generator_of(_chainmap_clean()))),
            comparisons=2,
        )


class TestPromoteFixR33ChainMapItemsViewInSinglePass(_WrapperCase):
    """Ruling 1914, S15-R33-PROM-4: a delegating
    ChainMap form inside an items view inside a single
    pass form as an element of the carrier, raising
    TypeError at the wrapper in place of a decision,
    where the direct act fires."""

    def test_cm_in_items_view_in_gen_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_generator_of(
                _items_view_of_value(_chainmap_nested())))
        )

    def test_cm_in_items_view_in_spi_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(SinglePassIterable(
                [_items_view_of_value(_chainmap_nested())]))
        )

    def test_cm_clean_in_items_view_in_gen_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(_generator_of(
                _items_view_of_value(_chainmap_clean()))),
            comparisons=1,
        )

    def test_cm_in_gen_in_gen_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_generator_of(
                _generator_of(_chainmap_nested())))
        )


class TestPromoteFixR33SelfReferentialInMappingInCarrier(_WrapperCase):
    """Ruling 1915, S15-R33-PROM-5: a self referential
    plain list inside a mapping as an element of the
    carrier, firing at the wrapper in the refusal form
    where the direct act clears, on hit material and on
    clean material alike."""

    def test_self_list_in_mapping_in_carrier_clears(self):
        make_holdout = lambda: _carrier({"x": _self_list()})
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_clean_in_mapping_in_carrier_clears(self):
        make_holdout = lambda: _carrier({"x": _self_list_clean()})
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_via_tuple_in_mapping_in_carrier_clears(self):
        make_holdout = lambda: _carrier({"x": _self_list_via_tuple()})
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_in_mapping_candidate_clears(self):
        make_holdout = lambda: _carrier({"x": _self_list()})
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)
        self._assert_candidate_fires(make_holdout)

    def test_self_list_in_carrier_still_fires(self):
        outcome = self._wrapper(_chainmap_item(
            _carrier(_self_list())
        ))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(
            _carrier(_self_list())
        ))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_list_in_gen_in_carrier_still_fires(self):
        outcome = self._wrapper(_chainmap_item(
            _carrier(_generator_of(_self_list()))
        ))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(
            _carrier(_generator_of(_self_list()))
        ))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_self_mapping_in_mapping_in_carrier_still_clears(self):
        make_holdout = lambda: _carrier({"x": _self_mapping()})
        outcome = self._wrapper(_chainmap_item(make_holdout()))
        self._assert_fires(outcome)
        direct_outcome = self._direct(_chainmap_item(make_holdout()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
