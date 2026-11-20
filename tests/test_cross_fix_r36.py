"""Fix round 36 tests for Region 2: cross split direct act family.

Charges pinned here, from design/steps/step-15-r36-triage.md:
ruling 2300 (the Cross split paper position, roster 2954,
finding S15-R36-CROSS-1, Low: a dictionary keys view standing
directly inside a plain list or a plain tuple inside a
delegating container inside a further delegating container,
that further container standing as an element of the pairs
sequence or of the items sequence, reaching no comparison at
the direct act and carrying no result at the dataset surface,
beside a refusal at the bundle surfaces); ruling 2301 (the
Cross split paper position, finding S15-R36-CROSS-2, Low: a
carrier inside an exact set form, or inside a plain container,
in each case inside a delegating container inside a further
delegating container standing as an element of the pairs
sequence or of the items sequence, or the delegating container
standing in a delegating set form as that sequence element,
carrying no result at the dataset surface while the direct act
and the promote wrapper judge the same presentation); and
ruling 2302 (the Dataset paper position, roster 2955, finding
S15-R36-DATA-1, Low: the sentinel all five probe discriminating
equality spoof at the dataset instruction item surface, value
side, items side, bool key side, and pairs position).
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
from tests.test_cross_fix_r20 import (
    dataset_bundle as dataset_bundle_r20,
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
from tests.test_cross_fix_r35 import (
    all_key_keys_view as r35_all_key_keys_view,
)
from tests.test_cross_fix_r35 import (
    all_values_view as r35_all_values_view,
)
from tests.test_cross_fix_r35 import (
    check_dataset_spoof_refused as check_refused_r35,
)
from tests.test_cross_fix_r35 import (
    spoof_make as spoof_make_r35,
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


class Ruling2300KeysViewPlainDelegatingDelegatingTests(
        unittest.TestCase):
    """Ruling 2300, S15-R36-CROSS-1: a dictionary keys view
    standing directly inside a plain list or a plain tuple
    inside a delegating container inside a further delegating
    container, that further container standing as an element
    of the pairs sequence or of the items sequence, with no
    carrier between, fires at the direct act, beside the
    dataset surface firing in parity and the bundle surfaces
    refusing."""

    def test_keys_view_in_plain_list_in_two_delegating_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})
        check_fires(self, lambda: {"items": [
            DelegatingTupleSubclass((DelegatingListSubclass(
                [[keys_view()]]),))]})

    def test_keys_view_in_plain_tuple_in_two_delegating_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [(keys_view(),)])])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingTupleSubclass((DelegatingDequeSubclass(
                [(keys_view(),)]),))]})

    def test_keys_view_in_plain_in_delegating_variants_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingDequeSubclass(
                [[keys_view()]])])]})
        check_fires(self, lambda: {"items": [
            DelegatingUserListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})

    def test_keys_view_two_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [(keys_view(),)])])]})

    def test_keys_view_two_delegating_clean_clears(self):
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"items": [
                        DelegatingListSubclass(
                            [DelegatingListSubclass(
                                [[clean_keys_view()]])])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)
        check_dataset_clears(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[clean_keys_view()]])])]})

    def test_keys_view_two_delegating_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [
                DelegatingListSubclass([DelegatingListSubclass(
                    [[keys_view()]])])]}})

    def test_keys_view_two_delegating_wrapper_and_poles_stand(self):
        check_wrapper_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([[keys_view()]])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[values_view()]])])]})
        check_fires(self, lambda: {"holdout_items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[keys_view()]])])]})
        check_fires(self, lambda: {"items": [
            [DelegatingListSubclass([[keys_view()]])]]})


class Ruling2301CarrierWrappedTwoDelegatingDatasetTests(
        unittest.TestCase):
    """Ruling 2301, S15-R36-CROSS-2: a carrier standing inside
    an exact set form, or inside a plain container, in each
    case inside a delegating container inside a further
    delegating container standing as an element of the pairs
    sequence or of the items sequence, or the delegating
    container standing in a delegating set form as that
    sequence element, carries its result at the dataset
    surface, in parity with the direct act and the promote
    wrapper judging the same presentation."""

    def test_carrier_in_set_in_two_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingTupleSubclass((DelegatingListSubclass(
                [{gen_of(keys_view())}]),))]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingDequeSubclass(
                [{gen_of(keys_view())}])])]})

    def test_carrier_in_plain_in_two_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [[gen_of(keys_view())]])])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [(gen_of(keys_view()),)])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingTupleSubclass(
                ([gen_of(keys_view())],))])]})

    def test_carrier_in_delegating_set_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([{gen_of(keys_view())}])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingSetSubclass(
                [{gen_of(keys_view())}])])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([(gen_of(keys_view()),)])]})
        check_dataset_fires(self, lambda: {"pairs": [
            [DelegatingSetSubclass([{gen_of(keys_view())}])]]})

    def test_carrier_two_delegating_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_wrapper_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([{gen_of(keys_view())}])]})

    def test_carrier_two_delegating_clean_clears(self):
        check_dataset_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [{gen_of(clean_keys_view())}])])]})
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [{gen_of(keys_view())}])])]})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": [
                        DelegatingListSubclass(
                            [DelegatingListSubclass(
                                [{gen_of(clean_keys_view())}])])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_carrier_two_delegating_bundle_refuses_and_poles(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingListSubclass([DelegatingListSubclass(
                    [{gen_of(keys_view())}])])]}})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([gen_of(keys_view())])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([[{gen_of(keys_view())}]])]})
        check_dataset_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([{gen_of(keys_view())}])]]})


_PROBE_NAMES = {
    "_SeamSentinelProbe", "_SeamSentinelProbeOther",
    "_SeamSentinelProbeFurther", "_SeamSentinelProbeLast",
}


def _is_sentinel_form(other):
    if type(other) is object:
        return True
    return type(other).__name__ in _PROBE_NAMES


class AllFiveProbeSpoof:
    """An object whose equality reading returns true
    against any form except the bare forms the landed
    sentinel limb probes with, a bare plain object and
    bare probe forms of the four landed probe classes,
    against each of which it returns false."""

    def __eq__(self, other):
        if _is_sentinel_form(other):
            return False
        return True

    def __ne__(self, other):
        if _is_sentinel_form(other):
            return True
        return False

    __hash__ = object.__hash__


class RaisingAllFiveProbeSpoof:
    """An object whose equality reading returns true
    against any form, and raises against each bare form
    the landed sentinel limb probes with."""

    def __eq__(self, other):
        if _is_sentinel_form(other):
            raise ValueError("no reading")
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


def all_five_values_view():
    return {1: AllFiveProbeSpoof()}.values()


def all_five_items_view():
    return {1: AllFiveProbeSpoof()}.items()


def all_five_key_keys_view():
    return {(AllFiveProbeSpoof(),): 1}.keys()


def raising_five_values_view():
    return {1: RaisingAllFiveProbeSpoof()}.values()


def raising_five_key_keys_view():
    return {(RaisingAllFiveProbeSpoof(),): 1}.keys()


class SpoofSubstDict(dict):
    """A dict subclass whose items reading presents, at
    the governed entry, a spoof counterpart view in place
    of the governed view standing in its storage."""

    MAKER = None

    def items(self):
        return {
            key: (self.MAKER() if key == "o" else value)
            for key, value in dict.items(self)
        }.items()


def spoof_make(maker, governed):
    cls = type(
        "DynSpoofDict36", (SpoofSubstDict,),
        {"MAKER": staticmethod(maker)})
    return cls([("o", governed()), ("c", "plain clean value")])


def check_dataset_spoof_refused(test_case, maker, governed,
                                wrapkey="items", comparisons=1):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle_r20(HOLDOUT_TEXT, lambda: {
                    wrapkey: [spoof_make(maker, governed)]}),
                occasion=occasion)
            test_case.assertTrue(result["fired"])
            shared = result["cross_split_audit_result"]
            test_case.assertEqual(
                shared["comparisons"], comparisons)


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


class Ruling2302SentinelAllFiveProbeSpoofTests(unittest.TestCase):
    """Ruling 2302, S15-R36-DATA-1: the sentinel all five
    probe discriminating equality spoof at the dataset
    instruction item surface: an object whose equality
    reading claims equality with the governed material
    while withholding a bool true claim against every
    bare form the landed sentinel limb probes with, the
    bare plain object and the bare probe forms of all
    four landed probe classes, by returning false against
    each of them or by raising against each of them,
    presented in place of governed material at the value
    side, the items side, the bool key side, and the pairs
    position, stands refused at the dataset surface, the
    direct act and the promote wrapper firing in parity
    with their controls."""

    def test_all_five_spoof_value_forms_refused(self):
        check_dataset_spoof_refused(
            self, all_five_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, all_five_items_view, governed_items_view)
        check_dataset_spoof_refused(
            self, raising_five_values_view, governed_values_view)

    def test_all_five_spoof_key_forms_refused(self):
        check_dataset_spoof_refused(
            self, all_five_key_keys_view, keys_view, comparisons=2)
        check_dataset_spoof_refused(
            self, raising_five_key_keys_view, keys_view,
            comparisons=2)

    def test_all_five_spoof_at_pairs_refused(self):
        check_dataset_spoof_refused(
            self, all_five_values_view, governed_values_view,
            wrapkey="pairs")

    def test_all_five_spoof_direct_and_wrapper_fire(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, all_five_values_view, governed_values_view)
        check_direct_and_wrapper_fire_on_spoof(
            self, all_five_key_keys_view, keys_view)
        check_dataset_spoof_refused(
            self, all_five_values_view, governed_values_view)

    def test_earlier_sentinel_poles_stand(self):
        check_refused_r35(
            self, r35_all_values_view, governed_values_view)
        check_refused_r35(
            self, r35_all_key_keys_view, keys_view, comparisons=2)


if __name__ == "__main__":
    unittest.main()
