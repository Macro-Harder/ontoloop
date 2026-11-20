"""Fix round 34 tests for Region 2: cross split direct act family.

Charges pinned here, from design/steps/step-15-r34-triage.md:
rulings 2030 to 2036 (the Eval paper positions, roster 2820,
Findings 1 to 7, Low: dictionary views inside generator
carriers inside delegating containers inside plain lists at
items mapping values and as sequence elements at the pairs
and items positions, the combined clean view form of ruling
1677 inside two containers and inside delegating containers
at governed mapping values as elements and at mapping
values, and plain mappings inside delegating containers at
items mapping values carrying views inside generator
carriers at their own values); rulings 2037 to 2039 (the
Cross split paper positions, roster 2821, findings
S15-R34-CROSS-1 to S15-R34-CROSS-3, Low: carriers inside
exact set forms standing as sequence elements, dictionary
views standing directly inside delegating containers at the
items position, and governed views inside delegating
containers inside further containers in the storage of
mappings presenting clean views at their governed entries);
ruling 2040 (the Dataset paper position, roster 2819,
finding S15-R34-DATA-1, Low: the sentinel discriminating
equality spoof at the dataset instruction item surface on
the value side, the items side, the bool key side, and the
pairs position); and rulings 2041 to 2045 (the Spanning
paper positions, roster 2827, findings S15-R34-SPAN-1 to
S15-R34-SPAN-5, Low: the combined form inside stacked
delegating containers and inside delegating containers
inside plain containers as sequence elements, dictionary
views directly inside stacked containers at the pairs
position, governed views inside carriers inside container
storage wraps, and delegating storage wraps inside further
containers in storage). Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py and
promote.py stand untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest

from tests import harness
from tests.test_cross_fix_r19 import OnceOnlyIterable
from tests.test_cross_fix_r20 import (
    CANDIDATE,
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    HashableItem,
    check_clears,
    check_fires,
)
from tests.test_cross_fix_r20 import (
    dataset_bundle as dataset_bundle_r20,
)
from tests.test_cross_fix_r24 import (
    ListSubclassPlain,
    check_dataset_fires,
    dataset_bundle,
    items_view,
    keys_view,
    values_view,
)
from tests.test_cross_fix_r26 import (
    CustomIterable,
    IndexedOnlyCarrier,
    SequenceCarrier,
    clean_keys_view,
    gen_of,
)
from tests.test_cross_fix_r29 import clean_value_dict
from tests.test_cross_fix_r30 import CleanViewDict
from tests.test_cross_fix_r31 import container_view_dict
from tests.test_cross_fix_r33 import (
    SetSubclassPlain,
    SlotDelegatingListSubclass,
    combined_form,
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

VIEWS = {
    "keys": keys_view,
    "items": items_view,
    "values": values_view,
}

CARRIERS = {
    "gen": lambda view: gen_of(view),
    "zip": lambda view: zip([view]),
    "enum": lambda view: enumerate([view]),
    "seq": lambda view: SequenceCarrier([view]),
    "indexed": lambda view: IndexedOnlyCarrier([view]),
    "custom": lambda view: CustomIterable([view]),
    "once": lambda view: OnceOnlyIterable([view]),
}

DELEGATING = {
    "dlist": lambda carrier: DelegatingListSubclass([carrier]),
    "dtuple": lambda carrier: DelegatingTupleSubclass((carrier,)),
    "ddeque": lambda carrier: DelegatingDequeSubclass([carrier]),
    "duserlist": lambda carrier: DelegatingUserListSubclass([carrier]),
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


class Ruling2030ItemsMapvalCarrierDelegatingInListTests(
        unittest.TestCase):
    """Ruling 2030, Eval Finding 1: a dictionary view inside
    a generator carrier inside a delegating container
    inside a plain list standing at a value of a plain
    mapping standing at the items position fires at the
    direct act, beside the dataset surface firing in
    parity and the bundle surfaces refusing."""

    def test_views_in_gen_in_delegating_in_list_at_items_mapval_fire(self):
        for view_name, view in VIEWS.items():
            with self.subTest(view=view_name):
                check_fires(self, lambda view=view: {"items": {
                    "o": [DelegatingListSubclass(
                        [gen_of(view())])]}})

    def test_items_mapval_nested_clean_clears(self):
        check_fires(self, lambda: {"items": {
            "o": [DelegatingListSubclass([gen_of(keys_view())])]}})
        check_clears(self, lambda: {"items": {
            "o": [DelegatingListSubclass([gen_of(keys_view())])]}})

    def test_items_mapval_nested_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": {
            "o": [DelegatingListSubclass([gen_of(keys_view())])]}})
        check_dataset_fires(self, lambda: {"items": {
            "o": [DelegatingListSubclass([gen_of(values_view())])]}})

    def test_items_mapval_nested_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": {
                "o": [DelegatingListSubclass(
                    [gen_of(keys_view())])]}}})


class Ruling2031PairsElementCarrierDelegatingInListTests(
        unittest.TestCase):
    """Ruling 2031, Eval Finding 2: a dictionary view inside
    a carrier inside a delegating container inside a plain
    list standing as an element of the sequence standing
    at the pairs position fires at the direct act, beside
    the dataset surface firing in parity and the bundle
    surfaces refusing."""

    def test_pairs_element_nested_presentations_fire(self):
        check_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})
        for view_name, view in VIEWS.items():
            with self.subTest(view=view_name, carrier="indexed"):
                check_fires(self, lambda view=view: {"pairs": [
                    [DelegatingListSubclass(
                        [IndexedOnlyCarrier([view()])])]]})

    def test_pairs_element_nested_clean_clears(self):
        check_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})
        check_clears(self, lambda: {"pairs": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})

    def test_pairs_element_nested_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})
        check_dataset_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass(
                [IndexedOnlyCarrier([values_view()])])]]})

    def test_pairs_element_nested_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                [DelegatingListSubclass([gen_of(keys_view())])]]}})


class Ruling2032ItemsElementCarrierDelegatingInListTests(
        unittest.TestCase):
    """Ruling 2032, Eval Finding 3: the same nested element
    presentations standing as elements of the sequence
    standing at the items position fire at the direct act
    and at the dataset surface, counted severally from
    ruling 2031 on the position ground."""

    def test_items_element_nested_presentations_fire(self):
        check_fires(self, lambda: {"items": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})
        for view_name, view in VIEWS.items():
            with self.subTest(view=view_name, carrier="indexed"):
                check_fires(self, lambda view=view: {"items": [
                    [DelegatingListSubclass(
                        [IndexedOnlyCarrier([view()])])]]})

    def test_items_element_nested_clean_clears(self):
        check_fires(self, lambda: {"items": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})
        check_clears(self, lambda: {"items": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})

    def test_items_element_nested_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            [DelegatingListSubclass([gen_of(keys_view())])]]})
        check_dataset_fires(self, lambda: {"items": [
            [DelegatingListSubclass(
                [IndexedOnlyCarrier([values_view()])])]]})


class Ruling2033CombinedDoubleContainerPairsTests(
        unittest.TestCase):
    """Ruling 2033, Eval Finding 4: the combined clean view
    form of ruling 1677 standing inside two containers, at
    least the inner standing in a delegating form, as an
    element of the sequence standing at the pairs position
    fires at the direct act, beside the dataset surface
    firing in parity and the bundle surfaces refusing."""

    def test_combined_double_container_pairs_presentations_fire(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([[combined_form(keys_view)]])]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingTupleSubclass((
                DelegatingListSubclass([combined_form(keys_view)]),))]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingTupleSubclass(
                (combined_form(keys_view),))])]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [DelegatingListSubclass([combined_form(keys_view)])])])]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingDequeSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingUserListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)

    def test_combined_double_container_pairs_clean_clears(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)

    def test_combined_double_container_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([[combined_form(keys_view)]])]}, comparisons=2)

    def test_combined_double_container_pairs_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingListSubclass([DelegatingListSubclass(
                    [combined_form(keys_view)])])]}})


class Ruling2034CombinedDoubleContainerItemsTests(
        unittest.TestCase):
    """Ruling 2034, Eval Finding 5: the same double
    container combined presentations standing as elements
    of the sequence standing at the items position fire
    at the direct act and at the dataset surface, counted
    severally from ruling 2033 on the position ground."""

    def test_combined_double_container_items_presentations_fire(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([[combined_form(keys_view)]])]})
        check_fires(self, lambda: {"items": [
            DelegatingTupleSubclass((
                DelegatingListSubclass([combined_form(keys_view)]),))]})
        check_fires(self, lambda: {"items": [
            DelegatingDequeSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]})

    def test_combined_double_container_items_clean_clears(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]})
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]})

    def test_combined_double_container_items_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([[combined_form(keys_view)]])]})


class Ruling2035CombinedDelegatingPairsMapvalTests(
        unittest.TestCase):
    """Ruling 2035, Eval Finding 6: the combined clean view
    form standing inside a delegating container standing
    at a value of a plain mapping standing at the pairs
    position fires at the direct act, beside the dataset
    surface firing in parity and the standing items and
    holdout mapping value poles standing in their cured
    forms."""

    def test_combined_in_delegating_at_pairs_mapval_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingDequeSubclass([combined_form(keys_view)])}})

    def test_combined_in_delegating_pairs_mapval_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})

    def test_combined_in_delegating_pairs_mapval_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})

    def test_combined_in_delegating_standing_poles_stand(self):
        check_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})
        check_dataset_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass([combined_form(keys_view)])}})


class Ruling2036InnerMappingDelegatingItemsMapvalTests(
        unittest.TestCase):
    """Ruling 2036, Eval Finding 7: a plain mapping standing
    at a value of a plain mapping standing at the items
    position, the inner mapping standing inside a
    delegating container and carrying a dictionary view
    inside a generator carrier at its own value, fires at
    the direct act, beside the dataset surface firing in
    parity."""

    def test_inner_mapping_in_delegating_at_items_mapval_fires(self):
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name):
                check_fires(self, lambda wrap=wrap: {"items": {
                    "o": wrap({"p": gen_of(keys_view())})}})

    def test_inner_mapping_items_mapval_clean_clears(self):
        check_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass(
                [{"p": gen_of(keys_view())}])}})
        check_clears(self, lambda: {"items": {
            "o": DelegatingListSubclass(
                [{"p": gen_of(keys_view())}])}})

    def test_inner_mapping_items_mapval_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass(
                [{"p": gen_of(keys_view())}])}})
        check_dataset_fires(self, lambda: {"items": {
            "o": DelegatingDequeSubclass(
                [{"p": gen_of(values_view())}])}})


class Ruling2037CarrierInExactSetElementTests(unittest.TestCase):
    """Ruling 2037, S15-R34-CROSS-1: a carrier standing
    inside an exact set form, an exact set, a frozenset,
    or a plain set subclass, standing as an element of
    the sequence standing at the pairs position or at the
    items position fires at the direct act, beside the
    dataset surface and the promote wrapper judging the
    same presentation in their standing forms, and the
    same set form standing inside a plain list standing
    as an element of the pairs sequence."""

    def test_carrier_in_exact_set_element_presentations_fire(self):
        check_fires(self, lambda: {"pairs": [{gen_of(keys_view())}]})
        check_fires(self, lambda: {"pairs": [
            frozenset([gen_of(keys_view())])]})
        check_fires(self, lambda: {"pairs": [
            SetSubclassPlain([gen_of(keys_view())])]})
        check_fires(self, lambda: {"items": [{gen_of(keys_view())}]})
        check_fires(self, lambda: {"items": [
            frozenset([gen_of(keys_view())])]})
        check_fires(self, lambda: {"pairs": [[{gen_of(keys_view())}]]})

    def test_carrier_in_exact_set_element_clean_clears(self):
        check_fires(self, lambda: {"pairs": [{gen_of(keys_view())}]})
        check_clears(self, lambda: {"pairs": [{gen_of(keys_view())}]})

    def test_carrier_in_exact_set_element_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            {gen_of(keys_view())}]})
        check_dataset_fires(self, lambda: {"items": [
            {gen_of(keys_view())}]})

    def test_carrier_in_exact_set_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingSetSubclass([gen_of(keys_view())])]})
        check_wrapper_fires(self, lambda: {"pairs": [
            {gen_of(keys_view())}]})


class Ruling2038ViewDirectlyInDelegatingItemsTests(
        unittest.TestCase):
    """Ruling 2038, S15-R34-CROSS-2: a dictionary view
    standing directly inside a delegating container, with
    no carrier standing between, standing as an element
    of the sequence standing at the items position fires
    at the direct act, beside the dataset surface firing
    in parity and the bundle surfaces refusing, counted
    severally from ruling 1906, whose charged forms stand
    at the pairs position alone."""

    def test_view_directly_in_delegating_items_presentations_fire(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingTupleSubclass((keys_view(),))]})
        check_fires(self, lambda: {"items": [
            DelegatingDequeSubclass([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([values_view()])]})

    def test_view_directly_in_delegating_items_clean_clears(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})

    def test_view_directly_in_delegating_items_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingDequeSubclass([values_view()])]})

    def test_view_directly_in_delegating_items_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [
                DelegatingListSubclass([keys_view()])]}})


class Ruling2039DelegatingInContainerStorageTests(
        unittest.TestCase):
    """Ruling 2039, S15-R34-CROSS-3: a governed view
    standing inside a delegating container standing
    inside a further container in the storage of a
    mapping presenting a clean view at its governed
    entry fires at the direct act, beside the dataset
    surface firing in parity and the bundle surfaces
    refusing, one ring beyond the single wrap form
    ruling 1907 cures."""

    def test_stored_view_double_wrap_presentations_fire(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass(
                [DelegatingListSubclass([view])]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: [DelegatingListSubclass([view])])]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass(
                [DelegatingDequeSubclass([view])]))]})

    def test_stored_view_double_wrap_clean_clears(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass(
                [DelegatingListSubclass([view])]))]})
        check_clears(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass(
                [DelegatingListSubclass([view])]))]})

    def test_stored_view_double_wrap_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: DelegatingListSubclass(
                    [DelegatingListSubclass([view])]))]})
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: [DelegatingListSubclass([view])])]})

    def test_stored_view_double_wrap_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [container_view_dict(
                keys_view(),
                lambda view: DelegatingListSubclass(
                    [DelegatingListSubclass([view])]))]}})


class DiscriminatingSpoof:
    """An object whose equality reading returns true
    against any form except a bare plain object, against
    which it returns false."""

    def __eq__(self, other):
        if type(other) is object:
            return False
        return True

    def __ne__(self, other):
        if type(other) is object:
            return True
        return False

    __hash__ = object.__hash__


class RaisingSpoof:
    """An object whose equality reading returns true
    against any form, and raises against a bare plain
    object."""

    def __eq__(self, other):
        if type(other) is object:
            raise ValueError("no reading")
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


def disc_values_view():
    return {1: DiscriminatingSpoof()}.values()


def disc_items_view():
    return {1: DiscriminatingSpoof()}.items()


def disc_key_keys_view():
    return {(DiscriminatingSpoof(),): 1}.keys()


def raise_values_view():
    return {1: RaisingSpoof()}.values()


def raise_key_keys_view():
    return {(RaisingSpoof(),): 1}.keys()


def governed_values_view():
    from tests.test_cross_fix_r31 import (
        governed_values_view as maker,
    )
    return maker()


def governed_items_view():
    from tests.test_cross_fix_r31 import (
        governed_items_view as maker,
    )
    return maker()


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
        "DynSpoofDict34", (SpoofSubstDict,),
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


class Ruling2040SentinelDiscriminatingSpoofTests(
        unittest.TestCase):
    """Ruling 2040, S15-R34-DATA-1: the sentinel
    discriminating equality spoof at the dataset
    instruction item surface: an object whose equality
    reading returns true against any form except a bare
    plain object, or raises against it, presented in
    place of governed material at the positions the
    Dataset paper states, stands refused at the dataset
    surface, the direct act and the promote wrapper
    firing in parity with their controls at every
    position but the pairs position, whose direct and
    wrapper posture stands as the paper states."""

    def test_discriminating_spoof_value_forms_refused(self):
        check_dataset_spoof_refused(
            self, disc_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, disc_items_view, governed_items_view)
        check_dataset_spoof_refused(
            self, raise_values_view, governed_values_view)

    def test_discriminating_spoof_key_forms_refused(self):
        check_dataset_spoof_refused(
            self, disc_key_keys_view, keys_view, comparisons=2)
        check_dataset_spoof_refused(
            self, raise_key_keys_view, keys_view, comparisons=2)

    def test_discriminating_spoof_at_pairs_refused(self):
        check_dataset_spoof_refused(
            self, disc_values_view, governed_values_view,
            wrapkey="pairs")

    def test_discriminating_spoof_direct_and_wrapper_fire(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, disc_values_view, governed_values_view)
        check_direct_and_wrapper_fire_on_spoof(
            self, disc_key_keys_view, keys_view)
        check_dataset_spoof_refused(
            self, disc_values_view, governed_values_view)


class Ruling2041CombinedDelegatingInDelegatingTests(
        unittest.TestCase):
    """Ruling 2041, S15-R34-SPAN-1: the combined clean view
    form standing inside a delegating container standing
    inside a further delegating container, as an element
    of the sequences standing at the pairs, items, and
    holdout_items positions, fires at the direct act,
    beside the dataset surface firing in parity."""

    def test_combined_delegating_in_delegating_presentations_fire(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_fires(self, lambda: {"holdout_items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=4)
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingTupleSubclass(
                (combined_form(keys_view),))])]}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(items_view)])])]}, comparisons=2)

    def test_combined_delegating_in_delegating_clean_clears(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)

    def test_combined_delegating_in_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=2)
        check_dataset_fires(self, lambda: {"holdout_items": [
            DelegatingListSubclass([DelegatingListSubclass(
                [combined_form(keys_view)])])]}, comparisons=4)


class Ruling2042CombinedDelegatingInPlainPairsTests(
        unittest.TestCase):
    """Ruling 2042, S15-R34-SPAN-2: the combined clean view
    form standing inside a delegating container standing
    inside a plain container, as an element of the
    sequence standing at the pairs position, fires at the
    direct act, beside the dataset surface firing in
    parity, the reverse container order standing as its
    firing bound."""

    def test_combined_delegating_in_plain_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([combined_form(keys_view)])]]}, comparisons=2)

    def test_combined_delegating_in_plain_pairs_clean_clears(self):
        check_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([combined_form(keys_view)])]]}, comparisons=2)
        check_clears(self, lambda: {"pairs": [
            [DelegatingListSubclass([combined_form(keys_view)])]]}, comparisons=2)

    def test_combined_delegating_in_plain_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            [DelegatingListSubclass([combined_form(keys_view)])]]}, comparisons=2)


class Ruling2043ViewDirectlyInStackedContainersTests(
        unittest.TestCase):
    """Ruling 2043, S15-R34-SPAN-3: a dictionary view
    standing directly inside stacked containers at the
    pairs position, with no carrier standing between,
    where either stacked container stands in a delegating
    form, fires at the direct act, beside the dataset
    surface firing in parity."""

    def test_view_in_stacked_containers_pairs_presentations_fire(self):
        check_fires(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([DelegatingTupleSubclass(
                (keys_view(),))])}})
        check_fires(self, lambda: {"pairs": {"o":
            DelegatingTupleSubclass((
                DelegatingListSubclass([keys_view()]),))}})
        check_fires(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([DelegatingDequeSubclass(
                [values_view()])])}})
        check_fires(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([[keys_view()]])}})
        check_fires(self, lambda: {"pairs": {"o":
            [DelegatingListSubclass([keys_view()])]}})
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([DelegatingListSubclass(
                [keys_view()])])]})

    def test_view_in_stacked_containers_pairs_clean_clears(self):
        check_fires(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([[keys_view()]])}})
        check_clears(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([[keys_view()]])}})

    def test_view_in_stacked_containers_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([DelegatingTupleSubclass(
                (keys_view(),))])}})
        check_dataset_fires(self, lambda: {"pairs": {"o":
            DelegatingListSubclass([[keys_view()]])}})


class Ruling2044ViewInCarrierInStorageWrapTests(
        unittest.TestCase):
    """Ruling 2044, S15-R34-SPAN-4: a governed view
    standing inside a carrier of a governed kind standing
    inside a container standing as the storage wrap of a
    mapping presenting a clean view at its governed
    entry fires at the direct act, beside the dataset
    surface firing in parity and the bundle surfaces
    refusing."""

    def test_stored_view_in_carrier_in_wrap_presentations_fire(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([gen_of(view)]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingSetSubclass([gen_of(view)]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([zip([view])]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: [gen_of(view)])]})

    def test_stored_view_in_carrier_in_wrap_clean_clears(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([gen_of(view)]))]})
        check_clears(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([gen_of(view)]))]})

    def test_stored_view_in_carrier_in_wrap_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: DelegatingListSubclass(
                    [gen_of(view)]))]})
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: [gen_of(view)])]})

    def test_stored_view_in_carrier_in_wrap_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [container_view_dict(
                keys_view(),
                lambda view: DelegatingListSubclass(
                    [gen_of(view)]))]}})


class Ruling2045DelegatingWrapInFurtherContainerTests(
        unittest.TestCase):
    """Ruling 2045, S15-R34-SPAN-5: a governed view
    standing inside a delegating container standing as
    the storage wrap of a mapping presenting a clean view
    at its governed entry, that wrap itself standing
    inside a further container in the storage, fires at
    the direct act, beside the dataset surface firing in
    parity."""

    def test_stored_delegating_wrap_in_further_container_fires(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: [SlotDelegatingListSubclass([view])])]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: [DelegatingListSubclass([view])])]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: (DelegatingListSubclass([view]),))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass(
                [DelegatingListSubclass([view])]))]})

    def test_stored_delegating_wrap_clean_clears(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: [DelegatingListSubclass([view])])]})
        check_clears(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: [DelegatingListSubclass([view])])]})

    def test_stored_delegating_wrap_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: [DelegatingListSubclass([view])])]})
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: DelegatingListSubclass(
                    [DelegatingListSubclass([view])]))]})


if __name__ == "__main__":
    unittest.main()
