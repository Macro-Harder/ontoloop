"""Fix round 35 tests for Region 2: cross split direct act family.

Charges pinned here, from design/steps/step-15-r35-triage.md:
ruling 2166 (the Eval paper position, roster 2895, Finding 1,
Low: the combined clean view form of ruling 1677 standing
inside a container at a value of a plain mapping standing
at the holdout position, a cure introduced defect beside
the ruling 2035 pairs cure); ruling 2167 (the Cross split
paper position, roster 2893, finding S15-R35-CROSS-1, Low:
a dictionary keys view standing directly inside a plain
list or a plain tuple inside a delegating list standing
as an element of the pairs sequence or of the items
sequence); ruling 2168 (the Cross split paper position,
finding S15-R35-CROSS-2, Low: a carrier standing inside
an exact set form, or inside a plain container, inside a
delegating container standing as an element of the pairs
sequence or of the items sequence, carrying no result at
the dataset surface while the direct act and the promote
wrapper judge the same presentation); and ruling 2169
(the Dataset paper position, roster 2894, finding
S15-R35-DATA-1, Low: the sentinel all probe discriminating
equality spoof at the dataset instruction item surface,
value side, items side, bool key side, and pairs position).
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
from tests.test_cross_fix_r33 import combined_form
from tests.test_promote_fix_r22 import (
    DequeSubclass as DelegatingDequeSubclass,
    ListSubclass as DelegatingListSubclass,
    TupleSubclass as DelegatingTupleSubclass,
    UserListSubclass as DelegatingUserListSubclass,
)

OCCASIONS = ("candidate construction", "promotion")
BUNDLE_SURFACES = (
    "audit_at_build",
    "audit_at_evaluation",
    "audit_at_promotion",
)

HOLDOUT_CONTAINERS = {
    "dlist": lambda form: DelegatingListSubclass([form]),
    "dtuple": lambda form: DelegatingTupleSubclass((form,)),
    "ddeque": lambda form: DelegatingDequeSubclass([form]),
    "duserlist": lambda form: DelegatingUserListSubclass([form]),
    "list": lambda form: [form],
    "tuple": lambda form: (form,),
}


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


class Ruling2166CombinedContainerHoldoutMapvalTests(
        unittest.TestCase):
    """Ruling 2166, Eval Finding 1: the combined clean view
    form of ruling 1677 standing inside a container at a
    value of a plain mapping standing at the holdout
    position fires at the direct act, beside the dataset
    surface firing in parity and the bundle surfaces
    refusing, in the delegating list, delegating tuple,
    delegating deque, delegating UserList, plain list, and
    plain tuple container forms, for the keys view and the
    values view combined forms alike, the clean text pole
    clearing at the same geometry, and the standing poles
    of the ruling 2035 pairs cure standing in their cured
    form beside it."""

    def test_combined_in_delegating_containers_at_holdout_mapval_fires(self):
        for view, comparisons in ((keys_view, 4), (values_view, 3)):
            for name in ("dlist", "dtuple", "ddeque", "duserlist"):
                wrap = HOLDOUT_CONTAINERS[name]
                with self.subTest(view=view.__name__, container=name):
                    check_fires(
                        self,
                        lambda view=view, wrap=wrap: {
                            "holdout_items": {
                                "o": wrap(combined_form(view))}},
                        comparisons=comparisons)

    def test_combined_in_plain_containers_at_holdout_mapval_fires(self):
        for view, comparisons in ((keys_view, 4), (values_view, 3)):
            for name in ("list", "tuple"):
                wrap = HOLDOUT_CONTAINERS[name]
                with self.subTest(view=view.__name__, container=name):
                    check_fires(
                        self,
                        lambda view=view, wrap=wrap: {
                            "holdout_items": {
                                "o": wrap(combined_form(view))}},
                        comparisons=comparisons)

    def test_combined_holdout_mapval_dataset_fires(self):
        for name in ("dlist", "dtuple", "ddeque", "duserlist"):
            wrap = HOLDOUT_CONTAINERS[name]
            with self.subTest(container=name):
                check_dataset_fires(
                    self,
                    lambda wrap=wrap: {
                        "holdout_items": {
                            "o": wrap(combined_form(keys_view))}},
                    comparisons=4)
        check_dataset_fires(
            self,
            lambda: {"holdout_items": {
                "o": [combined_form(values_view)]}},
            comparisons=3)

    def test_combined_holdout_mapval_clean_clears(self):
        module = harness.require("ontoloop.cross_split_audit")
        for name, view in (("dlist", keys_view),
                           ("dtuple", values_view)):
            wrap = HOLDOUT_CONTAINERS[name]
            with self.subTest(container=name):
                for occasion in OCCASIONS:
                    result = module.audit_instruction_item(
                        CLEAN_TEXT,
                        {"holdout_items": {
                            "o": wrap(combined_form(view))}},
                        occasion=occasion)
                    self.assertFalse(result["fired"])

    def test_combined_holdout_mapval_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"holdout_items": {
                "o": DelegatingListSubclass(
                    [combined_form(keys_view)])}}})

    def test_ruling_2035_pairs_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})
        check_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})

    def test_holdout_neighbouring_poles_stand(self):
        check_fires(
            self,
            lambda: {"holdout_items": DelegatingListSubclass(
                [combined_form(keys_view)])},
            comparisons=4)
        check_fires(self, lambda: {"holdout_items": {
            "o": gen_of(keys_view())}})


class Ruling2167KeysViewPlainContainerDelegatingTests(
        unittest.TestCase):
    """Ruling 2167, S15-R35-CROSS-1: a dictionary keys view
    standing directly inside a plain list or a plain tuple
    inside a delegating list, that delegating list standing
    as an element of the pairs sequence or of the items
    sequence, with no carrier between, fires at the direct
    act, beside the dataset surface firing in parity and
    the bundle surfaces refusing."""

    def test_keys_view_in_plain_list_in_delegating_list_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([[keys_view()]])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([[keys_view()]])]})

    def test_keys_view_in_plain_tuple_in_delegating_list_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([(keys_view(),)])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([(keys_view(),)])]})

    def test_keys_view_plain_in_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([[keys_view()]])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([(keys_view(),)])]})

    def test_keys_view_plain_in_delegating_clean_clears(self):
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([[keys_view()]])]})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"items": [
                        DelegatingListSubclass(
                            [[clean_keys_view()]])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)
        check_dataset_clears(self, lambda: {"items": [
            DelegatingListSubclass([[clean_keys_view()]])]})

    def test_keys_view_plain_in_delegating_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [
                DelegatingListSubclass([[keys_view()]])]}})

    def test_keys_view_plain_in_delegating_wrapper_fires(self):
        check_wrapper_fires(self, lambda: {"items": [
            DelegatingListSubclass([[keys_view()]])]})

    def test_keys_view_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [[keys_view()]]})
        check_fires(self, lambda: {"items": [
            [DelegatingListSubclass([keys_view()])]]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [keys_view()])])]})


class Ruling2168CarrierWrappedDelegatingDatasetTests(
        unittest.TestCase):
    """Ruling 2168, S15-R35-CROSS-2: a carrier standing
    inside an exact set form, or inside a plain container,
    in each case inside a delegating container standing as
    an element of the pairs sequence or of the items
    sequence, carries its result at the dataset surface,
    in parity with the direct act and the promote wrapper
    judging the same presentation."""

    def test_carrier_in_set_in_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([{gen_of(keys_view())}])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([{gen_of(keys_view())}])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingTupleSubclass(({gen_of(keys_view())},))]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingDequeSubclass([{gen_of(keys_view())}])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass(
                [frozenset([gen_of(keys_view())])])]})

    def test_carrier_in_plain_container_in_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([[gen_of(keys_view())]])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([(gen_of(keys_view()),)])]})

    def test_carrier_wrapped_delegating_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([{gen_of(keys_view())}])]})
        check_wrapper_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([{gen_of(keys_view())}])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([[gen_of(keys_view())]])]})

    def test_carrier_wrapped_delegating_clean_clears(self):
        check_dataset_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([{gen_of(clean_keys_view())}])]})
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([{gen_of(keys_view())}])]})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": [
                        DelegatingListSubclass(
                            [{gen_of(clean_keys_view())}])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_carrier_wrapped_delegating_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingListSubclass([{gen_of(keys_view())}])]}})

    def test_carrier_wrapped_standing_poles_stand(self):
        check_dataset_fires(self, lambda: {"pairs": [
            [{gen_of(keys_view())}]]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([gen_of(keys_view())])]})


_PROBE_NAMES = {"_SeamSentinelProbe", "_SeamSentinelProbeOther"}


def _is_sentinel_form(other):
    if type(other) is object:
        return True
    return type(other).__name__ in _PROBE_NAMES


class AllProbeSpoof:
    """An object whose equality reading returns true
    against any form except the bare forms the landed
    sentinel limb probes with, a bare plain object and
    bare probe forms of the two landed probe classes,
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


class RaisingAllProbeSpoof:
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


def all_values_view():
    return {1: AllProbeSpoof()}.values()


def all_items_view():
    return {1: AllProbeSpoof()}.items()


def all_key_keys_view():
    return {(AllProbeSpoof(),): 1}.keys()


def raising_values_view():
    return {1: RaisingAllProbeSpoof()}.values()


def raising_key_keys_view():
    return {(RaisingAllProbeSpoof(),): 1}.keys()


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
        "DynSpoofDict35", (SpoofSubstDict,),
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


class Ruling2169SentinelAllProbeSpoofTests(unittest.TestCase):
    """Ruling 2169, S15-R35-DATA-1: the sentinel all probe
    discriminating equality spoof at the dataset
    instruction item surface: an object whose equality
    reading claims equality with the governed material
    while withholding a bool true claim against every
    bare form the landed sentinel limb probes with, by
    returning false against each of them or by raising
    against each of them, presented in place of governed
    material at the value side, the items side, the bool
    key side, and the pairs position, stands refused at
    the dataset surface, the direct act and the promote
    wrapper firing in parity with their controls."""

    def test_all_probe_spoof_value_forms_refused(self):
        check_dataset_spoof_refused(
            self, all_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, all_items_view, governed_items_view)
        check_dataset_spoof_refused(
            self, raising_values_view, governed_values_view)

    def test_all_probe_spoof_key_forms_refused(self):
        check_dataset_spoof_refused(
            self, all_key_keys_view, keys_view, comparisons=2)
        check_dataset_spoof_refused(
            self, raising_key_keys_view, keys_view, comparisons=2)

    def test_all_probe_spoof_at_pairs_refused(self):
        check_dataset_spoof_refused(
            self, all_values_view, governed_values_view,
            wrapkey="pairs")

    def test_all_probe_spoof_direct_and_wrapper_fire(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, all_values_view, governed_values_view)
        check_direct_and_wrapper_fire_on_spoof(
            self, all_key_keys_view, keys_view)
        check_dataset_spoof_refused(
            self, all_values_view, governed_values_view)


if __name__ == "__main__":
    unittest.main()
