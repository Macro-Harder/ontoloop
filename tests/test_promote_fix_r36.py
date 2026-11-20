"""Fix round 36 tests for Region 3: promote wrapper.

Written first for four positions at Round 36 triage
rulings 2303, 2304, 2305, and 2306 (S15-R36-PROM-1,
S15-R36-PROM-2, S15-R36-PROM-3, and S15-R36-SPAN-1,
each Low), in the forms the raising papers state
beside the standing cured forms of the same families.
Ruling 2303: a single pass form carrying ChainMap
material inside a plain container chain one position
beyond the three chains ruling 2170 cured, silent at
the promote wrapper where the direct act fires.
Ruling 2304: a ChainMap form inside a values view
inside a delegating deque form one position beyond
the mapping value position ruling 2172 cured, firing
at the promote wrapper in the refusal form where the
direct act clears. Ruling 2305: a ChainMap form
inside a values view inside a delegating list form
or a delegating tuple form at a mapping value, firing
at the promote wrapper in the refusal form where the
direct act clears. Ruling 2306: a single pass form
carrying ChainMap material inside three nested plain
mappings as an element of the carrier, and in the
further plain container chain forms of that ruling,
silent at the promote wrapper where the direct act
fires, at depth three and beyond. Rulings 2170 to
2172 stand in their outcome forms, ruling 2170
standing PARTIAL in its cured in part form, and stand
not reopened by any pin here: their charged forms and
their standing controls stand as poles beside the new
forms, in the forms the Round 36 Promote paper,
roster 2960, and the Round 36 Spanning paper, roster
2962, state. The nine referred identities of
tests.test_promote_fix_r34 stand in no pin here.
"""

import unittest

from tests.harness import require
from tests.test_promote_fix_r22 import (
    DequeSubclass,
    ListSubclass,
    TupleSubclass,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)
from tests.test_promote_fix_r35 import (
    _carrier,
    _cm_clean,
    _cm_hit,
    _list_of,
    _values_view,
)

HOLDOUT_TEXT = "sealed holdout instruction text"


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

    def _assert_pair_clears(self, make_item, comparisons=None):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        if comparisons is not None:
            self.assertEqual(
                direct_outcome["comparisons"], comparisons
            )

    def _assert_wrapper_clears_direct_fires(
        self, make_item, comparisons=1
    ):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], comparisons)

    def _assert_wrapper_fires_direct_clears(
        self, make_item, comparisons=1
    ):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"],
            comparisons,
        )
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


class TestPromoteFixR36SinglePassChainOneBeyond(
    _WrapperCase
):
    """Ruling 2303, S15-R36-PROM-1: a single pass form
    carrying ChainMap material inside a plain container
    chain one position beyond the three chains ruling
    2170 cured, silent at the wrapper where the direct
    act fires."""

    def test_gen_in_mapping_x3_value_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"y": {"z": {"x": _generator_of(_cm_hit())}}}
            )
        )

    def test_gen_in_tuple_in_tuple_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(((_generator_of(_cm_hit()),),))
        )

    def test_gen_in_list_in_mapping_x2_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"y": {"x": [_generator_of(_cm_hit())]}}
            )
        )

    def test_gen_in_list_in_list_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"x": [[_generator_of(_cm_hit())]]}
            )
        )

    def test_gen_in_mapping_in_list_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"y": [{"x": _generator_of(_cm_hit())}]}
            )
        )

    def test_gen_in_plain_list_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier([_generator_of(_cm_hit())])
        )

    def test_gen_in_gen_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "x": _generator_of(
                        _generator_of(_cm_hit())
                    )
                }
            )
        )

    def test_gen_in_mapping_x3_value_clean_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"y": {"z": {"x": _generator_of(_cm_clean())}}}
            ),
            comparisons=1,
        )

    def test_gen_in_deleg_list_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                _list_of(_generator_of(_cm_hit()))
            )
        )

    def test_gen_in_gen_at_mapping_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": {
                    "x": _generator_of(
                        _generator_of(_cm_hit())
                    )
                }
            }
        )

    def test_gen_in_mapping_in_carrier_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier({"x": _generator_of(_cm_hit())})
        )

    def test_gen_in_mapping_in_tuple_in_carrier_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier(({"x": _generator_of(_cm_hit())},))
        )

    def test_gen_in_mapping_in_plain_list_in_carrier_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier([{"x": _generator_of(_cm_hit())}])
        )


class TestPromoteFixR36ViewInDequeOneBeyond(
    _WrapperCase
):
    """Ruling 2304, S15-R36-PROM-2: a ChainMap form
    inside a values view inside a delegating deque
    form one position beyond the mapping value position
    ruling 2172 cured, firing at the wrapper in the
    refusal form where the direct act clears."""

    def test_view_in_deque_in_deque_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [
                        DequeSubclass(
                            [
                                _values_view(
                                    _list_of(
                                        _list_of(_cm_hit())
                                    )
                                )
                            ]
                        )
                    ]
                )
            },
            comparisons=0,
        )

    def test_view_in_deque_in_plain_list_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": [
                    DequeSubclass(
                        [
                            _values_view(
                                _list_of(_list_of(_cm_hit()))
                            )
                        ]
                    )
                ]
            },
            comparisons=0,
        )

    def test_view_in_deque_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                DequeSubclass(
                    [
                        _values_view(
                            _list_of(_list_of(_cm_hit()))
                        )
                    ]
                )
            ),
            comparisons=0,
        )

    def test_view_in_deque_in_deleg_tuple_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": TupleSubclass(
                    (
                        DequeSubclass(
                            [
                                _values_view(
                                    _list_of(
                                        _list_of(_cm_hit())
                                    )
                                )
                            ]
                        ),
                    )
                )
            },
            comparisons=0,
        )

    def test_view_in_deque_at_value_still_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [
                        _values_view(
                            _list_of(_list_of(_cm_hit()))
                        )
                    ]
                )
            },
            comparisons=0,
        )

    def test_view_in_deque_clean_still_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [
                        _values_view(
                            _list_of(
                                _list_of(
                                    _generator_of(_cm_clean())
                                )
                            )
                        )
                    ]
                )
            },
            comparisons=0,
        )


class TestPromoteFixR36ViewInDelegatingListOrTuple(
    _WrapperCase
):
    """Ruling 2305, S15-R36-PROM-3: a ChainMap form
    inside a values view inside a delegating list form
    or a delegating tuple form at a mapping value,
    firing at the wrapper in the refusal form where
    the direct act clears."""

    def test_view_in_deleg_list_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": _list_of(
                    _values_view(
                        _list_of(
                            _list_of(
                                _generator_of(_cm_hit())
                            )
                        )
                    )
                )
            },
            comparisons=0,
        )

    def test_view_in_deleg_tuple_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": TupleSubclass(
                    (
                        _values_view(
                            _list_of(
                                _list_of(
                                    _generator_of(_cm_hit())
                                )
                            )
                        ),
                    )
                )
            },
            comparisons=0,
        )

    def test_view_single_deleg_in_deleg_list_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": _list_of(
                    _values_view(_list_of(_cm_hit()))
                )
            },
            comparisons=0,
        )

    def test_view_in_two_deleg_lists_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": _list_of(
                    _list_of(
                        _values_view(
                            _list_of(_list_of(_cm_hit()))
                        )
                    )
                )
            },
            comparisons=0,
        )

    def test_view_in_plain_list_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": [
                    _values_view(
                        _list_of(
                            _list_of(
                                _generator_of(_cm_hit())
                            )
                        )
                    )
                ]
            }
        )

    def test_view_in_plain_tuple_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": (
                    _values_view(
                        _list_of(
                            _list_of(
                                _generator_of(_cm_hit())
                            )
                        )
                    ),
                )
            }
        )

    def test_view_delegating_nested_in_list_still_fires(self):
        self._assert_wrapper_fires_direct_clears(
            lambda: {
                "k": _list_of(
                    _values_view(
                        _list_of(_nested_position())
                    )
                )
            }
        )

    def test_view_carrying_gen_in_list_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": _list_of(
                    _values_view(_generator_of(_cm_hit()))
                )
            }
        )


class TestPromoteFixR36NestedMappingDepthThree(
    _WrapperCase
):
    """Ruling 2306, S15-R36-SPAN-1: a single pass form
    carrying ChainMap material inside three nested
    plain mappings as an element of the carrier, and
    in the further plain container chain forms of the
    ruling, silent at the wrapper where the direct act
    fires, at depth three and beyond."""

    def test_gen_in_mapping_x3_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": {"c": _generator_of(_cm_hit())}}}
            )
        )

    def test_gen_in_list_in_mapping_x2_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": [_generator_of(_cm_hit())]}}
            )
        )

    def test_gen_in_mapping_in_tuple_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": ({"b": _generator_of(_cm_hit())},)}
            )
        )

    def test_gen_in_mapping_x4_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": _generator_of(_cm_hit())
                            }
                        }
                    }
                }
            )
        )

    def test_gen_in_mapping_x2_in_plain_list_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                [{"y": {"x": _generator_of(_cm_hit())}}]
            )
        )

    def test_gen_in_mapping_x3_clean_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"a": {"b": {"c": _generator_of(_cm_clean())}}}
            ),
            comparisons=1,
        )

    def test_gen_in_mapping_x2_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"y": {"x": _generator_of(_cm_hit())}}
            )
        )

    def test_gen_in_mapping_x3_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "a": {"b": {"c": _generator_of(_cm_hit())}}
            }
        )


if __name__ == "__main__":
    unittest.main()
