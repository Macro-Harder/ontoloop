"""Fix round 37 tests for Region 3: promote wrapper.

Written first for one position at Round 37 triage
ruling 2442 (S15-R37-PROM-1, entry N-1316, Low,
absorbing S15-R37-SPAN-1, entry N-1325, Low), in the
forms the raising papers state beside the standing
cured forms of the same families. Ruling 2442: a
single pass form carrying ChainMap material, standing
inside a plain container chain one ring beyond the
chains rulings 2303 and 2306 cured, stands silent at
the promote wrapper, carrying no cross split result,
where the direct act fires, in the eight forms of the
Round 37 Promote paper, roster 3043, at its section 4,
forms B-a, B-c, B-d, B-e, B-f, B-h, B-j, and B-k, and
in the nine chain forms of the Round 37 Spanning
paper, roster 3029, at its section 4. Rulings 2303
and 2306 stand CURED in their charged forms and stand
not reopened by any pin here: their charged forms and
their standing controls stand as poles beside the new
forms. The nine referred identities of
tests.test_promote_fix_r34 stand in no pin here. The
stopped line S1856-a stands pinned here in one pin
only, as a standing control in its standing posture,
wrapper clearing beside the direct act firing, in the
form the Fix round 36 Region 3 paper states, and
stands cured by no act of this round. The stopped
line S1856-c stands in no pin here.
"""

import unittest

from tests.harness import require
from tests.test_promote_fix_r22 import (
    ListSubclass,
    _chainmap_item,
    _generator_of,
)
from tests.test_promote_fix_r35 import (
    _carrier,
    _cm_clean,
    _cm_hit,
    _list_of,
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


class TestPromoteFixR37PromoteFormsOneRingBeyond(
    _WrapperCase
):
    """Ruling 2442, Promote limb, S15-R37-PROM-1: the
    eight forms B-a, B-c, B-d, B-e, B-f, B-h, B-j, and
    B-k of the Round 37 Promote paper, each a generator
    carrying ChainMap material inside a plain container
    chain one ring beyond the chains rulings 2303 and
    2306 cured, silent at the wrapper where the direct
    act fires."""

    def test_b_a_gen_in_mapping_x5_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": {
                                    "e": _generator_of(
                                        _cm_hit()
                                    )
                                }
                            }
                        }
                    }
                }
            )
        )

    def test_b_c_gen_in_list_x3_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                [[[_generator_of(_cm_hit())]]]
            )
        )

    def test_b_d_gen_in_tuple_x3_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                (((_generator_of(_cm_hit()),),),)
            )
        )

    def test_b_e_gen_in_list_x3_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"x": [[[_generator_of(_cm_hit())]]]}
            )
        )

    def test_b_f_gen_in_mapping_x3_in_list_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                [
                    {
                        "a": {
                            "b": {
                                "c": _generator_of(_cm_hit())
                            }
                        }
                    }
                ]
            )
        )

    def test_b_h_gen_in_tuple_in_mapping_x2_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": (_generator_of(_cm_hit()),)}}
            )
        )

    def test_b_j_gen_in_mapping_x2_in_list_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": [
                        {
                            "b": {
                                "c": _generator_of(_cm_hit())
                            }
                        }
                    ]
                }
            )
        )

    def test_b_k_gen_in_mapping_in_list_in_tuple_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                ([{"x": _generator_of(_cm_hit())}],)
            )
        )


class TestPromoteFixR37SpanningFormsOneRingBeyond(
    _WrapperCase
):
    """Ruling 2442, Spanning limb, S15-R37-SPAN-1
    absorbed: the nine chain forms of the Round 37
    Spanning paper, each a generator carrying a
    ChainMap hit form inside a plain container chain
    one position beyond the nine chains the Fix round
    36 chain limb carries, as an element of the
    carrier, silent at the wrapper where the direct
    act fires."""

    def test_span_gen_in_mapping_x5_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": {
                                    "e": _generator_of(
                                        _cm_hit()
                                    )
                                }
                            }
                        }
                    }
                }
            )
        )

    def test_span_gen_in_mapping_x3_in_plain_list_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                [
                    {
                        "a": {
                            "b": {
                                "c": _generator_of(_cm_hit())
                            }
                        }
                    }
                ]
            )
        )

    def test_span_gen_in_mapping_x4_in_plain_list_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                [
                    {
                        "a": {
                            "b": {
                                "c": {
                                    "d": _generator_of(
                                        _cm_hit()
                                    )
                                }
                            }
                        }
                    }
                ]
            )
        )

    def test_span_gen_in_plain_list_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": [_generator_of(_cm_hit())]
                        }
                    }
                }
            )
        )

    def test_span_gen_in_plain_tuple_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": (_generator_of(_cm_hit()),)
                        }
                    }
                }
            )
        )

    def test_span_gen_in_mapping_x2_in_tuple_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": ({"b": {"c": _generator_of(_cm_hit())}},)}
            )
        )

    def test_span_gen_in_list_x2_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": [[_generator_of(_cm_hit())]]}}
            )
        )

    def test_span_gen_in_tuple_x2_in_mapping_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": ((_generator_of(_cm_hit()),),)}
            )
        )

    def test_span_gen_in_mapping_x3_in_tuple_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                (
                    {
                        "a": {
                            "b": {
                                "c": _generator_of(_cm_hit())
                            }
                        }
                    },
                )
            )
        )


class TestPromoteFixR37Controls(_WrapperCase):
    """Controls of ruling 2442: the clean pole at the
    charged depth, the neighbouring forms the raising
    papers decide in parity, the cured geometries of
    rulings 2303 and 2306, and the standing silent
    controls of the cure classes, the last of them
    standing as the stopped line S1856-a in its
    standing posture, passing on both trees."""

    def test_clean_depth5_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": {
                                    "e": _generator_of(
                                        _cm_clean()
                                    )
                                }
                            }
                        }
                    }
                }
            ),
            comparisons=1,
        )

    def test_gen_in_mapping_x4_value_chain_in_carrier_still_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "y": {
                        "z": {
                            "w": {
                                "x": _generator_of(_cm_hit())
                            }
                        }
                    }
                }
            )
        )

    def test_gen_in_gen_in_gen_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "x": _generator_of(
                        _generator_of(
                            _generator_of(_cm_hit())
                        )
                    )
                }
            )
        )

    def test_gen_in_mapping_x3_in_deleg_list_in_carrier_still_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                _list_of(
                    {
                        "a": {
                            "b": {
                                "c": _generator_of(_cm_hit())
                            }
                        }
                    }
                )
            )
        )

    def test_nested_gen_in_mapping_x3_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": _generator_of(
                                _generator_of(_cm_hit())
                            )
                        }
                    }
                }
            )
        )

    def test_gen_in_mapping_x2_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"y": {"x": _generator_of(_cm_hit())}}
            )
        )

    def test_gen_in_mapping_x3_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": {"c": _generator_of(_cm_hit())}}}
            )
        )

    def test_gen_in_mapping_x3_at_value_still_fires(self):
        self._assert_pair_fires(
            lambda: {
                "a": {"b": {"c": _generator_of(_cm_hit())}}
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

    def test_gen_in_mapping_in_plain_list_in_carrier_still_clears(
        self,
    ):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier([{"x": _generator_of(_cm_hit())}])
        )


if __name__ == "__main__":
    unittest.main()
