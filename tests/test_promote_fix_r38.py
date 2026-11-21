"""Fix round 38 tests for Region 3: promote wrapper.

Written first for one position at Round 38 triage
ruling 2592 (S15-R38-PROM-1, entry N-1404, Low,
absorbing S15-R38-SPAN-1, entry N-1413, Low), in the
forms the raising papers state beside the standing
cured forms of the same families. Ruling 2592: a
single pass form carrying ChainMap material, standing
inside a plain container chain one ring beyond the
extended chains ruling 2442 cured, stands silent at
the promote wrapper, carrying no cross split result,
where the direct act fires, in the fourteen forms of
the Round 38 Promote paper, roster 3108, at its
section 4, forms B-a, B-b, B-c, B-d, B-e, B-g, B-h,
B-i, B-j, B-k, B-l, B-m, B-n, and B-o, and in the
fifteen chain forms of the Round 38 Spanning paper,
roster 3110, at its section 4. Ruling 2442 stands
CURED in its charged form and stands not reopened by
any pin here: its charged forms and its standing
controls stand as poles beside the new forms. The
nine referred identities of
tests.test_promote_fix_r34 stand in no pin here. The
stopped line S1856-a stands pinned here in one pin
only, as a standing control in its standing posture,
wrapper clearing beside the direct act firing, in the
form the Fix round 37 Region 3 paper states, and
stands cured by no act of this round. The stopped
line S1856-c stands in no pin here.
"""

import unittest

from tests.harness import require
from tests.test_promote_fix_r22 import (
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


def _m6_gen():
    return {
        "a": {
            "b": {
                "c": {
                    "d": {
                        "e": {
                            "f": _generator_of(_cm_hit())
                        }
                    }
                }
            }
        }
    }


class TestPromoteFixR38PromoteFormsOneRingBeyond(
    _WrapperCase
):
    """Ruling 2592, Promote limb, S15-R38-PROM-1: the
    fourteen forms B-a, B-b, B-c, B-d, B-e, B-g, B-h,
    B-i, B-j, B-k, B-l, B-m, B-n, and B-o of the Round
    38 Promote paper, each a generator carrying
    ChainMap material inside a plain container chain
    one ring beyond the chains ruling 2442 cured,
    silent at the wrapper where the direct act fires.
    Form B-a stands silent at the candidate
    construction occasion beside it, with the bundle
    proceeding, in the form the paper states."""

    def test_b_a_gen_in_mapping_x6_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_m6_gen()))

    def test_b_b_gen_in_list_x4_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier([[[[_generator_of(_cm_hit())]]]])
        )

    def test_b_c_gen_in_tuple_x4_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(((((_generator_of(_cm_hit()),),),),))
        )

    def test_b_d_gen_in_list_x3_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": [[[_generator_of(_cm_hit())]]]}}
            )
        )

    def test_b_e_gen_in_mapping_x3_in_list_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                [[{"a": {"b": {"c": _generator_of(_cm_hit())}}}]]
            )
        )

    def test_b_g_gen_in_mapping_in_list_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": [{"c": _generator_of(_cm_hit())}]}}
            )
        )

    def test_b_h_gen_in_mapping_in_list_in_tuple_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier((([{"c": _generator_of(_cm_hit())}],),))
        )

    def test_b_i_gen_in_mapping_x4_in_list_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                [
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
                ]
            )
        )

    def test_b_j_gen_in_list_in_mapping_x4_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": [_generator_of(_cm_hit())]
                            }
                        }
                    }
                }
            )
        )

    def test_b_k_gen_in_tuple_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": (_generator_of(_cm_hit()),)
                            }
                        }
                    }
                }
            )
        )

    def test_b_l_gen_in_mapping_x3_in_tuple_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"x": ({"a": {"b": {"c": _generator_of(_cm_hit())}}},)}
            )
        )

    def test_b_m_gen_in_list_x2_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": {"c": [[_generator_of(_cm_hit())]]}}}
            )
        )

    def test_b_n_gen_in_tuple_x2_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": ((_generator_of(_cm_hit()),),)}}
            )
        )

    def test_b_o_gen_in_mapping_x3_in_tuple_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                (({"a": {"b": {"c": _generator_of(_cm_hit())}}},),)
            )
        )


class TestPromoteFixR38SpanningFormsOneRingBeyond(
    _WrapperCase
):
    """Ruling 2592, Spanning limb, S15-R38-SPAN-1
    absorbed: the fifteen chain forms of the Round 38
    Spanning paper, each a generator carrying a
    ChainMap hit form inside a plain container chain
    one position beyond the fifteen chains the Fix
    round 37 chain limb carries, as an element of the
    carrier, silent at the wrapper where the direct
    act fires."""

    def test_span_gen_in_mapping_x6_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_m6_gen()))

    def test_span_gen_in_mapping_x5_in_plain_list_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                [
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
                ]
            )
        )

    def test_span_gen_in_mapping_x4_in_plain_tuple_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                (
                    {
                        "a": {
                            "b": {
                                "c": {
                                    "d": _generator_of(_cm_hit())
                                }
                            }
                        }
                    },
                )
            )
        )

    def test_span_gen_in_plain_list_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": [_generator_of(_cm_hit())]
                            }
                        }
                    }
                }
            )
        )

    def test_span_gen_in_plain_tuple_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": (_generator_of(_cm_hit()),)
                            }
                        }
                    }
                }
            )
        )

    def test_span_gen_in_list_x4_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier([[[[_generator_of(_cm_hit())]]]])
        )

    def test_span_gen_in_tuple_x3_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": (((_generator_of(_cm_hit()),),),)}}
            )
        )

    def test_span_gen_in_mapping_x3_in_plain_list_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"x": [{"a": {"b": {"c": _generator_of(_cm_hit())}}}]}
            )
        )

    def test_span_gen_in_mapping_x3_in_plain_tuple_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"x": ({"a": {"b": {"c": _generator_of(_cm_hit())}}},)}
            )
        )

    def test_span_gen_in_plain_list_in_mapping_x3_in_plain_list_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                [{"a": {"b": {"c": [_generator_of(_cm_hit())]}}}]
            )
        )

    def test_span_gen_in_mapping_x2_in_plain_list_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": [{"c": {"d": _generator_of(_cm_hit())}}]}}
            )
        )

    def test_span_gen_in_mapping_x4_in_plain_list_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "x": [
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
                }
            )
        )

    def test_span_gen_in_list_x2_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": {"c": [[_generator_of(_cm_hit())]]}}}
            )
        )

    def test_span_gen_in_tuple_x2_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {"a": {"b": ((_generator_of(_cm_hit()),),)}}
            )
        )

    def test_span_gen_in_mapping_in_tuple_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": ({"d": _generator_of(_cm_hit())},)
                        }
                    }
                }
            )
        )


class TestPromoteFixR38Controls(_WrapperCase):
    """Controls of ruling 2592: the clean poles at the
    charged depths, the neighbouring forms the raising
    papers decide in parity, the cured geometries of
    ruling 2442, and the standing silent controls of
    the cure classes, the last of them standing as the
    stopped line S1856-a in its standing posture,
    passing on both trees."""

    def test_clean_depth6_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": {
                                    "e": {
                                        "f": _generator_of(
                                            _cm_clean()
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            ),
            comparisons=1,
        )

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

    def test_b_f_gen_in_tuple_in_mapping_x3_in_carrier_still_fires(
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

    def test_gen_in_mapping_x5_in_deleg_list_in_carrier_still_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                _list_of(
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
        )

    def test_gen_in_gen_in_mapping_x5_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                {
                    "a": {
                        "b": {
                            "c": {
                                "d": {
                                    "e": _generator_of(
                                        _generator_of(_cm_hit())
                                    )
                                }
                            }
                        }
                    }
                }
            )
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
