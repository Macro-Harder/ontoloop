"""Fix round 40 tests for Region 3: promote wrapper.

Written first for one position at Round 40 triage
ruling 2899 (S15-R40-PROM-1, entry N-1581, Low,
absorbing S15-R40-SPAN-1, entry N-1592, Low), in the
forms the raising papers state beside the standing
cured forms of the same families. Ruling 2899: a
single pass form carrying ChainMap material, standing
inside a plain container chain one ring beyond the
twenty five chains ruling 2744 cured, stands silent at
the promote wrapper, carrying no cross split result,
where the direct act fires, in the nineteen forms
of the Round 40 Promote paper, roster 3237, at its
section 4, forms D-a, D-b, D-c, D-d, D-e, D-f, D-g,
D-h, D-i, D-j, D-k, D-l, D-n, D-p, D-q, D-s, D-t, D-u,
and D-v, and in the sixteen chain forms of the
Round 40 Spanning paper, roster 3238, at its
section 4. Ruling 2744 stands CURED in its charged
form and stands not reopened by any pin here: its
charged forms and its standing controls stand as
poles beside the new forms. The nine referred
identities of tests.test_promote_fix_r34 stand in no
pin here. The stopped line S1856-a stands pinned here
in one pin only, as a standing control in its
standing posture, wrapper clearing beside the direct
act firing, in the form the Fix round 39 Region 3
paper states, and stands cured by no act of this
round. The stopped line S1856-c stands in no pin
here.
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


def _maps(count, inner):
    result = inner
    for _ in range(count):
        result = {"a": result}
    return result


def _lists(count, inner):
    result = inner
    for _ in range(count):
        result = [result]
    return result


def _tuples(count, inner):
    result = inner
    for _ in range(count):
        result = (result,)
    return result


def _gen():
    return _generator_of(_cm_hit())


def _gen_clean():
    return _generator_of(_cm_clean())


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


class TestPromoteFixR40PromoteFormsOneRingBeyond(
    _WrapperCase
):
    """Ruling 2899, Promote limb, S15-R40-PROM-1: the
    nineteen forms D-a to D-v of the Round 40 Promote
    paper, each a generator carrying ChainMap material
    inside a plain container chain one ring beyond the
    twenty five chains ruling 2744 cured, silent at the
    wrapper where the direct act fires. Form D-a stands
    silent at the candidate construction occasion beside
    it, with the bundle proceeding, in the form the
    paper states."""

    def test_d_a_gen_in_mapping_x8_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_maps(8, _gen())))

    def test_d_b_gen_in_list_x6_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_lists(6, _gen())))

    def test_d_c_gen_in_tuple_x6_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_tuples(6, _gen())))

    def test_d_d_gen_in_list_x4_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(3, _lists(4, _gen())))
        )

    def test_d_e_gen_in_mapping_x3_in_list_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_lists(4, _maps(3, _gen())))
        )

    def test_d_f_gen_in_mapping_x2_in_list_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(4, _lists(1, _maps(2, _gen()))))
        )

    def test_d_g_gen_in_mapping_in_list_in_tuple_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_tuples(4, _lists(1, _maps(1, _gen()))))
        )

    def test_d_h_gen_in_mapping_x4_in_list_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_lists(4, _maps(4, _gen())))
        )

    def test_d_i_gen_in_list_in_mapping_x6_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_maps(6, _lists(1, _gen())))
        )

    def test_d_j_gen_in_tuple_in_mapping_x6_in_carrier_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_maps(6, _tuples(1, _gen())))
        )

    def test_d_k_gen_in_mapping_x3_in_tuple_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(3, _tuples(1, _maps(3, _gen()))))
        )

    def test_d_l_gen_in_list_x3_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(4, _lists(3, _gen())))
        )

    def test_d_n_gen_in_mapping_x3_in_tuple_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_tuples(4, _maps(3, _gen())))
        )

    def test_d_p_gen_in_mapping_x4_in_tuple_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(2, _tuples(1, _maps(4, _gen()))))
        )

    def test_d_q_gen_in_tuple_x4_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(3, _tuples(4, _gen())))
        )

    def test_d_s_gen_in_mapping_x2_in_list_in_mapping_in_list_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                _lists(2, _maps(1, _lists(1, _maps(2, _gen()))))
            )
        )

    def test_d_t_gen_in_mapping_in_list_in_mapping_x2_in_list_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(
                _maps(
                    2,
                    _lists(
                        1, _maps(2, _lists(1, _maps(1, _gen())))
                    ),
                )
            )
        )

    def test_d_u_gen_in_mapping_x4_in_list_in_mapping_x3_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(3, _lists(1, _maps(4, _gen()))))
        )

    def test_d_v_gen_in_mapping_in_tuple_in_mapping_x5_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(5, _tuples(1, _maps(1, _gen()))))
        )


class TestPromoteFixR40SpanningFormsOneRingBeyond(
    _WrapperCase
):
    """Ruling 2899, Spanning limb, S15-R40-SPAN-1
    absorbed: the sixteen chain forms of the Round 40
    Spanning paper, each a generator carrying a
    ChainMap hit form inside a plain container chain
    one position beyond the twenty five chains the Fix
    round 39 chain limb of ruling 2744 carries, standing
    as an element of the carrier, silent at the wrapper
    where the direct act fires."""

    def test_span_gen_in_mapping_x8_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_maps(8, _gen())))

    def test_span_gen_in_list_x6_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_lists(6, _gen())))

    def test_span_gen_in_tuple_x6_in_carrier_fires(self):
        self._assert_pair_fires(lambda: _carrier(_tuples(6, _gen())))

    def test_span_gen_in_mapping_x7_in_plain_list_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_lists(1, _maps(7, _gen())))
        )

    def test_span_gen_in_mapping_x7_in_plain_tuple_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_tuples(1, _maps(7, _gen())))
        )

    def test_span_gen_in_plain_list_in_mapping_x6_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(6, _lists(1, _gen())))
        )

    def test_span_gen_in_plain_tuple_in_mapping_x6_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(6, _tuples(1, _gen())))
        )

    def test_span_gen_in_list_x5_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(1, _lists(5, _gen())))
        )

    def test_span_gen_in_list_x3_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(4, _lists(3, _gen())))
        )

    def test_span_gen_in_mapping_x5_in_list_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_lists(2, _maps(5, _gen())))
        )

    def test_span_gen_in_mapping_x6_in_plain_list_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(1, _lists(1, _maps(6, _gen()))))
        )

    def test_span_gen_in_tuple_x3_in_mapping_x4_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(4, _tuples(3, _gen())))
        )

    def test_span_gen_in_list_x2_in_mapping_x5_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(5, _lists(2, _gen())))
        )

    def test_span_gen_in_mapping_in_tuple_in_mapping_x5_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(5, _tuples(1, _maps(1, _gen()))))
        )

    def test_span_gen_in_mapping_x5_in_plain_tuple_in_mapping_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(1, _tuples(1, _maps(5, _gen()))))
        )

    def test_span_gen_in_mapping_x5_in_plain_list_in_mapping_x2_in_carrier_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_maps(2, _lists(1, _maps(5, _gen()))))
        )


class TestPromoteFixR40Controls(_WrapperCase):
    """Controls of ruling 2899: the clean poles at the
    charged depths, the neighbouring forms the raising
    papers decide in parity, the cured geometries of
    ruling 2744, and the standing silent controls of
    the cure classes, the last of them standing as the
    stopped line S1856-a in its standing posture,
    passing on both trees."""

    def test_clean_depth8_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(_maps(8, _gen_clean())),
            comparisons=1,
        )

    def test_clean_list_x6_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(_lists(6, _gen_clean())),
            comparisons=1,
        )

    def test_clean_depth7_in_carrier_clears(self):
        self._assert_pair_clears(
            lambda: _carrier(_maps(7, _gen_clean())),
            comparisons=1,
        )

    def test_gen_in_mapping_x4_in_list_x2_in_carrier_still_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_lists(2, _maps(4, _gen())))
        )

    def test_gen_in_mapping_x6_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_maps(6, _gen()))
        )

    def test_d_w_gen_in_mapping_x5_in_plain_list_in_carrier_still_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_lists(1, _maps(5, _gen())))
        )

    def test_gen_in_mapping_x7_in_deleg_list_in_carrier_still_fires(
        self,
    ):
        self._assert_pair_fires(
            lambda: _carrier(_list_of(_maps(7, _gen())))
        )

    def test_gen_in_gen_in_mapping_x7_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(
                _maps(7, _generator_of(_generator_of(_cm_hit())))
            )
        )

    def test_gen_in_mapping_x2_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_maps(2, _gen()))
        )

    def test_gen_in_mapping_x3_in_carrier_still_fires(self):
        self._assert_pair_fires(
            lambda: _carrier(_maps(3, _gen()))
        )

    def test_gen_in_mapping_in_carrier_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier({"x": _gen()})
        )

    def test_gen_in_mapping_in_tuple_in_carrier_still_clears(self):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier(({"x": _gen()},))
        )

    def test_gen_in_mapping_in_plain_list_in_carrier_still_clears(
        self,
    ):
        self._assert_wrapper_clears_direct_fires(
            lambda: _carrier([{"x": _gen()}])
        )


if __name__ == "__main__":
    unittest.main()
