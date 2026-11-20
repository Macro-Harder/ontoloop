"""Fix round 35 tests for Region 3: promote wrapper.

Written first for three positions at Round 35 triage
rulings 2170, 2171, and 2172 (S15-R35-PROM-10,
S15-R35-PROM-11, and S15-R35-PROM-12, each Low), in
the narrowed forms the raising paper states beside
the standing cured forms of the same families.
Ruling 2170: a single pass form carrying ChainMap
material inside a plain container form at an
intermediate position, silent at the promote wrapper
where the direct act fires, in the forms standing
inside a mapping inside a mapping, inside a plain
list inside a mapping, and inside a plain tuple, in
each case as an element of the carrier. Ruling 2171:
a ChainMap form inside a values view whose carried
form stands inside two single pass wrappings at a
mapping value, and a ChainMap form inside a values
view standing inside two single pass forms at a
mapping value, silent at the promote wrapper where
the direct act fires. Ruling 2172: a ChainMap form
inside a values view inside a delegating deque form
at a mapping value, firing at the promote wrapper in
the refusal form where the direct act clears, in its
two carried forms. Rulings 1911 to 1915, 2046, 1478,
1579, 1685, 1686, and 2030 to 2045 stand cured in
their bounded forms and stand not reopened by any
pin here: their charged forms stand as poles beside
the new forms, in the forms the Round 35 Promote
paper, roster 2899, states at its section 4 and the
standing pin files of those rounds state. The nine
referred identities of tests.test_promote_fix_r34
stand in no pin here.
"""

import unittest

from tests.harness import require
from tests.test_promote_fix_r22 import (
    DelegatingChainMapSubclass,
    DequeSubclass,
    ListSubclass,
    TupleSubclass,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)

HOLDOUT_TEXT = "sealed holdout instruction text"


def _cm_hit():
    return DelegatingChainMapSubclass([_nested_position()])


def _cm_clean():
    return DelegatingChainMapSubclass([_clean_position()])


def _carrier(inner):
    return {"k": ListSubclass([ListSubclass([inner])])}


def _values_view(carried):
    return {1: carried}.values()


def _items_view(value):
    return {1: value}.items()


def _list_of(*elements):
    return ListSubclass(list(elements))


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

    def _assert_pair_clears(self, make_item, comparisons):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
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


class TestPromoteFixR35SinglePassInsidePlainContainer(
    _WrapperCase
):
    """Ruling 2170, S15-R35-PROM-10: a single pass form
    carrying ChainMap material inside a plain container
    form at an intermediate position, silent at the
    wrapper where the direct act fires, in the narrowed
    forms of the ruling."""

    def test_gen_in_mapping_in_mapping_value_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"y": {"x": _generator_of(_cm_hit())}}
            )
        )

    def test_gen_in_plain_tuple_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier((_generator_of(_cm_hit()),))
        )

    def test_gen_in_plain_list_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"x": [_generator_of(_cm_hit())]}
            )
        )

    def test_gen_in_mapping_in_mapping_value_clean_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {"y": {"x": _generator_of(_cm_clean())}}
            ),
            comparisons=1,
        )

    def test_gen_at_plain_mapping_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {"k": _generator_of(_cm_hit())}
        )

    def test_gen_in_gen_at_plain_mapping_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": _generator_of(_generator_of(_cm_hit()))
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


class TestPromoteFixR35ChainMapInValuesViewTwoWrappings(
    _WrapperCase
):
    """Ruling 2171, S15-R35-PROM-11: a ChainMap form
    inside a values view standing inside two single
    pass wrappings or two single pass forms at a
    mapping value, silent at the wrapper where the
    direct act fires."""

    def test_chainmap_in_view_in_two_wrappings_at_value_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": _values_view(
                    _generator_of(
                        _generator_of(_list_of(_cm_hit()))
                    )
                )
            }
        )

    def test_chainmap_view_in_two_single_pass_at_value_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": _generator_of(
                    _generator_of(
                        _values_view(
                            _list_of(_list_of(_cm_hit()))
                        )
                    )
                )
            }
        )

    def test_view_in_single_pass_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": _generator_of(
                    _values_view(
                        _list_of(
                            _list_of(
                                _generator_of(_cm_hit())
                            )
                        )
                    )
                )
            }
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

    def test_chainmap_in_view_in_two_wrappings_clean_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": _values_view(
                    _generator_of(
                        _generator_of(_list_of(_cm_clean()))
                    )
                )
            },
            comparisons=1,
        )

    def test_chainmap_in_gen_in_view_at_value_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: {
                "k": _values_view(
                    _generator_of(_list_of(_list_of(_cm_hit())))
                )
            }
        )

    def test_chainmap_in_deleg_lists_at_value_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: {
                "k": ListSubclass(
                    [ListSubclass([_cm_hit()])]
                )
            }
        )


class TestPromoteFixR35ChainMapInViewInDelegatingDeque(
    _WrapperCase
):
    """Ruling 2172, S15-R35-PROM-12: a ChainMap form
    inside a values view inside a delegating deque
    form at a mapping value, firing at the wrapper in
    the refusal form where the direct act clears."""

    def test_view_through_gen_in_deque_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [
                        _values_view(
                            _list_of(
                                _list_of(
                                    _generator_of(_cm_hit())
                                )
                            )
                        )
                    ]
                )
            },
            comparisons=0,
        )

    def test_view_without_gen_in_deque_at_value_clears(self):
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

    def test_view_single_deleg_in_deque_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [
                        _values_view(
                            _list_of(
                                _generator_of(_cm_hit())
                            )
                        )
                    ]
                )
            },
            comparisons=0,
        )

    def test_items_view_value_deleg_in_deque_at_value_clears(self):
        self._assert_pair_clears(
            lambda: {
                "k": DequeSubclass(
                    [
                        _items_view(
                            _list_of(
                                _list_of(
                                    _generator_of(_cm_hit())
                                )
                            )
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

    def test_gen_in_deque_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": DequeSubclass([_generator_of(_cm_hit())])
            }
        )

    def test_view_carrying_gen_in_deque_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "k": DequeSubclass(
                    [_values_view(_generator_of(_cm_hit()))]
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

    def test_view_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                _values_view(
                    _generator_of(
                        _list_of(
                            _list_of(
                                _generator_of(_cm_hit())
                            )
                        )
                    )
                )
            )
        )

    def test_view_delegating_nested_in_list_still_fires(self):
        outcome = self._wrapper(
            _chainmap_item(
                {
                    "k": _list_of(
                        _values_view(
                            _list_of(_nested_position())
                        )
                    )
                }
            )
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"],
            1,
        )
        direct_outcome = self._direct(
            _chainmap_item(
                {
                    "k": _list_of(
                        _values_view(
                            _list_of(_nested_position())
                        )
                    )
                }
            )
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
