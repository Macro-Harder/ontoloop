"""Fix round 37 tests for Region 2: cross split audit family.

Charges pinned here, from design/steps/step-15-r37-triage.md:
ruling 2439 (the Cross split paper position, roster 3021,
finding S15-R37-CROSS-1, Low: a carrier standing inside an
exact set form, or standing inside a plain container, in
each case standing inside a delegating container, and that
delegating container standing inside a delegating set form
standing as an element of the pairs sequence or of the
items sequence, carrying no result at the dataset surface,
while the direct act and the promote wrapper judge the same
presentation); ruling 2440 (the Dataset paper position,
roster 3022, finding S15-R37-DATA-1, Low, absorbing the
Cross split paper position, roster 3021, finding
S15-R37-CROSS-2, Low, on the one sentinel identity ground:
the sentinel all seven probe discriminating equality spoof
at the dataset instruction item surface, value side, items
side, bool key side, and pairs position, a form claiming
equality as a bool true against any form except the seven
bare forms the landed sentinel limb probes with, the bare
plain object beside bare probe forms of the six landed
probe classes, withholding against each of them by
returning false, by raising, by returning a non bool
truthy claim, or by returning the not implemented form);
and ruling 2441 (the Eval paper position, roster 3023,
finding S15-R37-EVAL-1, Low: a governed values view inside
a generator carrier inside a double delegating container
form whose inner step stands as a delegating list form, in
the six forms its paper lists, and a governed items view
or values view inside a generator carrier inside the chain
delegating list inside delegating list inside plain list,
in each case standing as an element of the pairs sequence
or of the items sequence, and in the double delegating
list form as an element of the holdout sequence, standing
silent at the direct act and carrying no result at the
promote wrapper, while the dataset surface fires on the
same presentation, the defect standing introduced by the
Fix round 36 Region 2 act, rulings 2300 to 2302 themselves
standing LANDED in full and charged to no act here).
Every cure stands on ontoloop/cross_split_audit.py alone;
dataset.py stands untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest

from tests import harness
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    check_clears,
    check_fires,
)
from tests.test_cross_fix_r24 import (
    check_dataset_fires,
    dataset_bundle,
    keys_view,
    values_view,
)
from tests.test_cross_fix_r26 import clean_keys_view, gen_of
from tests.test_cross_fix_r31 import (
    governed_items_view,
    governed_values_view,
)
from tests.test_cross_fix_r36 import (
    all_five_key_keys_view,
    all_five_values_view,
    spoof_make,
)
from tests.test_cross_fix_r36 import (
    check_dataset_spoof_refused as check_refused_r36,
)
from tests.test_promote_fix_r22 import (
    DequeSubclass as DelegatingDequeSubclass,
    ListSubclass as DelegatingListSubclass,
    SetSubclass as DelegatingSetSubclass,
    TupleSubclass as DelegatingTupleSubclass,
    UserListSubclass as DelegatingUserListSubclass,
)

OCCASIONS = ("candidate construction", "promotion")
BUNDLE_SURFACES = (
    "audit_at_build",
    "audit_at_evaluation",
    "audit_at_promotion",
)


def check_bundle_refuses(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])


def check_wrapper_fires(test_case, make_holdout, comparisons=1):
    promote = harness.require("ontoloop.promote")
    bundle = {
        "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
        "holdout_items": make_holdout(),
    }
    result = promote.test_instruction_items_against_holdout(
        bundle, occasion="promotion")
    test_case.assertTrue(result["fired"])
    shared = result["cross_split_audit_result"]
    test_case.assertEqual(shared["comparisons"], comparisons)


def check_dataset_clears(test_case, make_holdout):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(HOLDOUT_TEXT, make_holdout()),
                occasion=occasion)
            test_case.assertFalse(result["fired"])


def check_dataset_spoof_refused(test_case, maker, governed,
                                wrapkey="items", comparisons=1):
    check_refused_r36(
        test_case, maker, governed,
        wrapkey=wrapkey, comparisons=comparisons)


def check_direct_and_wrapper_fire_on_spoof(
        test_case, maker, governed, wrapkey="items"):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT,
                {wrapkey: [spoof_make(maker, governed)]},
                occasion=occasion)
            test_case.assertTrue(result["fired"])
            test_case.assertEqual(result["comparisons"], 1)
    check_wrapper_fires(test_case, lambda: {
        wrapkey: [spoof_make(maker, governed)]})


class Ruling2439CarrierWrappedDelegatingSetDatasetTests(
        unittest.TestCase):
    """Ruling 2439, S15-R37-CROSS-1: a carrier standing
    inside an exact set form, or standing inside a plain
    container, in each case standing inside a delegating
    container, and that delegating container standing
    inside a delegating set form standing as an element of
    the pairs sequence or of the items sequence, carries
    its result at the dataset surface, in parity with the
    direct act and the promote wrapper judging the same
    presentation."""

    def test_carrier_in_set_in_delegating_in_deleg_set_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})

    def test_carrier_in_plain_in_delegating_in_deleg_set_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [[gen_of(keys_view())]])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [(gen_of(keys_view()),)])])]})

    def test_carrier_delegating_variants_in_deleg_set_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingTupleSubclass(
                ({gen_of(keys_view())},))])]})
        check_dataset_fires(self, lambda: {"pairs": [
            [DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingDequeSubclass(
                [{gen_of(keys_view())}])])]})

    def test_carrier_deleg_set_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_wrapper_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})

    def test_carrier_deleg_set_clean_clears(self):
        check_dataset_clears(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(clean_keys_view())}])])]})
        check_clears(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": [
                        DelegatingSetSubclass(
                            [DelegatingListSubclass(
                                [{gen_of(clean_keys_view())}])])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_carrier_deleg_set_bundle_refuses_and_poles(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingSetSubclass([DelegatingListSubclass(
                    [{gen_of(keys_view())}])])]}})
        check_dataset_fires(self, lambda: {"holdout_items": [
            DelegatingSetSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([DelegatingSetSubclass(
                [{gen_of(keys_view())}])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([{gen_of(keys_view())}])]})


_PROBE_NAMES_SEVEN = {
    "_SeamSentinelProbe", "_SeamSentinelProbeOther",
    "_SeamSentinelProbeFurther", "_SeamSentinelProbeLast",
    "_SeamSentinelProbeBeyond", "_SeamSentinelProbeFinal",
}


def _is_seven_form(other):
    if type(other) is object:
        return True
    return type(other).__name__ in _PROBE_NAMES_SEVEN


class AllSevenProbeSpoof:
    """An object whose equality reading returns true
    against any form except the seven bare forms the
    landed sentinel limb probes with, a bare plain object
    and bare probe forms of the six landed probe classes,
    against each of which it returns false."""

    def __eq__(self, other):
        if _is_seven_form(other):
            return False
        return True

    def __ne__(self, other):
        if _is_seven_form(other):
            return True
        return False

    __hash__ = object.__hash__


class RaisingAllSevenProbeSpoof:
    """An object whose equality reading returns true
    against any form, and raises against each of the seven
    bare forms the landed sentinel limb probes with."""

    def __eq__(self, other):
        if _is_seven_form(other):
            raise ValueError("no reading")
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


class NonBoolAllSevenProbeSpoof:
    """An object whose equality reading returns true as a
    bool against any form except the seven bare forms the
    landed sentinel limb probes with, against each of
    which it returns a non bool truthy claim."""

    def __eq__(self, other):
        if _is_seven_form(other):
            return 1
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


class NotImplementedAllSevenProbeSpoof:
    """An object whose equality reading returns true as a
    bool against any form except the seven bare forms the
    landed sentinel limb probes with, against each of
    which it returns the not implemented form."""

    def __eq__(self, other):
        if _is_seven_form(other):
            return NotImplemented
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


def seven_values_view():
    return {1: AllSevenProbeSpoof()}.values()


def seven_items_view():
    return {1: AllSevenProbeSpoof()}.items()


def seven_key_keys_view():
    return {(AllSevenProbeSpoof(),): 1}.keys()


def raising_seven_values_view():
    return {1: RaisingAllSevenProbeSpoof()}.values()


def raising_seven_key_keys_view():
    return {(RaisingAllSevenProbeSpoof(),): 1}.keys()


def nonbool_seven_values_view():
    return {1: NonBoolAllSevenProbeSpoof()}.values()


def notimpl_seven_values_view():
    return {1: NotImplementedAllSevenProbeSpoof()}.values()


class Ruling2440SentinelAllSevenProbeSpoofTests(
        unittest.TestCase):
    """Ruling 2440, S15-R37-DATA-1 absorbing
    S15-R37-CROSS-2: the sentinel all seven probe
    discriminating equality spoof at the dataset
    instruction item surface: an object whose equality
    reading claims equality with the governed material
    while withholding a bool true claim against every
    bare form the landed sentinel limb probes with, the
    bare plain object and the bare probe forms of all six
    landed probe classes, by returning false against each
    of them, by raising against each of them, by returning
    a non bool truthy claim against each of them, or by
    returning the not implemented form against each of
    them, presented in place of governed material at the
    value side, the items side, the bool key side, and
    the pairs position, stands refused at the dataset
    surface, the direct act and the promote wrapper firing
    in parity with their controls."""

    def test_all_seven_spoof_value_forms_refused(self):
        check_dataset_spoof_refused(
            self, seven_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, seven_items_view, governed_items_view)
        check_dataset_spoof_refused(
            self, raising_seven_values_view, governed_values_view)

    def test_all_seven_spoof_key_forms_refused(self):
        check_dataset_spoof_refused(
            self, seven_key_keys_view, keys_view, comparisons=2)
        check_dataset_spoof_refused(
            self, raising_seven_key_keys_view, keys_view,
            comparisons=2)

    def test_all_seven_spoof_at_pairs_refused(self):
        check_dataset_spoof_refused(
            self, seven_values_view, governed_values_view,
            wrapkey="pairs")

    def test_all_seven_spoof_further_withholding_refused(self):
        check_dataset_spoof_refused(
            self, nonbool_seven_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, notimpl_seven_values_view, governed_values_view)

    def test_all_seven_spoof_direct_and_wrapper_fire(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, seven_values_view, governed_values_view)
        check_direct_and_wrapper_fire_on_spoof(
            self, seven_key_keys_view, keys_view)
        check_dataset_spoof_refused(
            self, seven_values_view, governed_values_view)

    def test_earlier_sentinel_poles_stand(self):
        check_refused_r36(
            self, all_five_values_view, governed_values_view)
        check_refused_r36(
            self, all_five_values_view, governed_values_view,
            wrapkey="pairs")
        check_refused_r36(
            self, all_five_key_keys_view, keys_view, comparisons=2)


def _clean_view(kind):
    return getattr(
        {"o": "plain clean value", "c": "more clean text"}, kind)()


def clean_values_view():
    return _clean_view("values")


def clean_items_view():
    return _clean_view("items")


class Ruling2441GeneratorCarrierDelegatingListChainTests(
        unittest.TestCase):
    """Ruling 2441, S15-R37-EVAL-1: a governed values view
    inside a generator carrier inside a double delegating
    container form whose inner step stands as a delegating
    list form, and a governed items view or values view
    inside a generator carrier inside the chain delegating
    list inside delegating list inside plain list, in each
    case standing as an element of the pairs sequence or of
    the items sequence, and in the double delegating list
    form as an element of the holdout sequence, stands
    judged at the direct act and carries a result at the
    promote wrapper, in parity with the dataset surface
    firing on the same presentation."""

    def test_values_gen_double_deleg_list_inner_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingTupleSubclass(
                (gen_of(values_view()),))])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingTupleSubclass((DelegatingListSubclass(
                [gen_of(values_view())]),))]})

    def test_values_gen_double_deleg_list_inner_items_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingTupleSubclass(
                (gen_of(values_view()),))])]})
        check_fires(self, lambda: {"items": [
            DelegatingTupleSubclass((DelegatingListSubclass(
                [gen_of(values_view())]),))]})

    def test_values_gen_double_deleg_variants_fires(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [DelegatingListSubclass(
                    [gen_of(values_view())])])])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [DelegatingListSubclass(
                    [gen_of(values_view())])])])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingDequeSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})
        check_fires(self, lambda: {"items": [
            DelegatingUserListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})

    def test_views_gen_in_delegating_chain_fires(self):
        from tests.test_cross_fix_r24 import items_view
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[gen_of(items_view())]])])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[gen_of(items_view())]])])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[gen_of(values_view())]])])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[gen_of(values_view())]])])]})

    def test_values_gen_double_deleg_holdout_and_dataset(self):
        check_fires(self, lambda: {"holdout_items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})

    def test_values_gen_double_deleg_wrapper_fires(self):
        check_wrapper_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})
        check_wrapper_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[gen_of(values_view())]])])]})

    def test_gen_chain_clean_clears_and_bundle_refuses(self):
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [gen_of(values_view())])])]})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": [
                        DelegatingListSubclass(
                            [DelegatingListSubclass(
                                [gen_of(clean_values_view())])])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 0)
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": [
                        DelegatingListSubclass(
                            [DelegatingListSubclass(
                                [[gen_of(clean_items_view())]])])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 0)
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingListSubclass([DelegatingListSubclass(
                    [gen_of(values_view())])])]}})


if __name__ == "__main__":
    unittest.main()
