"""Fix round 33 tests for Region 2: cross split direct act family.

Charges pinned here, from design/steps/step-15-r33-triage.md:
rulings 1897 to 1901 (the Eval paper positions, roster 2748,
Findings 1 to 5, Low: dictionary views inside carriers inside
containers standing in delegating subclass form at the items
position in its mapping value and sequence element geometries,
at the pairs position in its sequence element geometry, and
the combined clean view form of ruling 1677 inside a
delegating container as an element at the pairs and items
positions, each silent at the direct act and carrying no
result at the dataset instruction item surface); rulings
1902 to 1908 (the Cross split paper positions, roster 2746,
findings S15-R33-CROSS-1 to S15-R33-CROSS-7, Low: carriers
inside set forms at governed mapping values, carriers and
views inside delegating set forms, set forms nested inside
reached containers at the pairs position, carriers and inner
mappings inside delegating containers at the items position,
dictionary views standing directly inside delegating
containers at the pairs position, governed views inside
delegating containers in the storage of mappings presenting
clean views at their governed entries, and governed views
inside plain containers in the storage of mappings standing
as storage values at governed entries of second mappings);
and rulings 1909 and 1910 (the Dataset paper positions,
roster 2741, findings S15-R33-DATA-1 and S15-R33-DATA-2,
Low: the equality spoof at the dataset instruction item
surface on the value side and the bool key side, and the
non bool equality spoof at the view underlying key side).
Every cure stands on ontoloop/cross_split_audit.py alone;
dataset.py and promote.py stand untouched in full under
this charge, and tests/test_unrowed_c.py stands held whole
and unchanged, with no pin of this region filed in it.
"""

import unittest
from collections import deque as _deque

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
from tests.test_promote_fix_r22 import (
    AbstractSetSubclass as DelegatingAbstractSetSubclass,
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


class SetSubclassPlain(set):
    """A set subclass whose iteration act stands inherited
    from the set base, carrying its elements in its own
    set storage."""


class SlotDelegatingListSubclass(list):
    """A list subclass carrying its elements only in one
    stored iterator held in a slot member, its iteration
    act delegating to that iterator."""

    __slots__ = ("_stored",)

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class DelegatingFrozensetSubclass(frozenset):
    """A frozenset subclass whose iteration act delegates
    to one stored iterator it carries."""

    def __new__(cls, items):
        instance = super().__new__(cls, items)
        instance._stored = iter(list(items))
        return instance

    def __iter__(self):
        return self._stored


def check_bundle_refuses(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])


def check_clean_material_clears(test_case, make_bundle,
                                comparisons=1):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertFalse(result["fired"])
            test_case.assertEqual(
                result["comparisons"], comparisons)


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


def combined_form(view):
    return CleanViewDict([
        ("o", clean_value_dict(view())),
        ("c", "plain clean value"),
    ])


class Ruling1897ItemsMappingValueDelegatingTests(unittest.TestCase):
    """Ruling 1897, Eval Finding 1: a dictionary view of any
    kind inside a carrier of any governed kind inside a
    container standing in a delegating subclass form at a
    value of a plain mapping standing at the items position
    fires at the direct act, beside the dataset surface
    firing in parity and the bundle surfaces refusing, one
    ring beyond the pairs and holdout readings rulings
    1790 and 1791 cure."""

    def test_views_in_iterator_carriers_in_delegating_list_fire(self):
        for view_name, view in VIEWS.items():
            for carrier_name in ("gen", "zip", "enum"):
                with self.subTest(view=view_name, carrier=carrier_name):
                    check_fires(self, lambda view=view, carrier_name=carrier_name: {
                        "items": {"o": DelegatingListSubclass(
                            [CARRIERS[carrier_name](view())])}})

    def test_views_in_carriers_in_other_delegating_containers_fire(self):
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name):
                check_fires(self, lambda wrap=wrap: {"items": {
                    "o": wrap(gen_of(keys_view()))}})
        for carrier_name in ("seq", "indexed", "custom", "once"):
            for view_name, view in VIEWS.items():
                with self.subTest(carrier=carrier_name, view=view_name):
                    check_fires(self, lambda carrier_name=carrier_name, view=view: {
                        "items": {"o": DelegatingDequeSubclass(
                            [CARRIERS[carrier_name](view())])}})

    def test_items_mapping_value_delegating_clean_clears(self):
        check_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_clears(self, lambda: {"items": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_clears(self, lambda: {"items": {
            "o": DelegatingTupleSubclass((zip([values_view()]),))}})

    def test_items_mapping_value_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_dataset_fires(self, lambda: {"items": {
            "o": DelegatingUserListSubclass(
                [SequenceCarrier([values_view()])])}})

    def test_items_mapping_value_bundle_and_standing_poles_stand(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": {
                "o": DelegatingListSubclass([gen_of(keys_view())])}}})
        check_fires(self, lambda: {"items": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"items": {
            "o": [gen_of(keys_view())]}})


class Ruling1898PairsElementDelegatingTests(unittest.TestCase):
    """Ruling 1898, Eval Finding 2: a dictionary view inside
    a carrier inside a container standing in a delegating
    subclass form standing as an element of the sequence
    standing at the pairs position fires at the direct
    act, beside the dataset surface firing in parity and
    the bundle surfaces refusing, counted severally from
    ruling 1897 on the geometry ground, in the sixteen
    presentations the Eval paper names as silent."""

    def test_pairs_element_silent_presentations_fire(self):
        for view_name, view in VIEWS.items():
            with self.subTest(view=view_name, carrier="indexed"):
                check_fires(self, lambda view=view: {"pairs": [
                    DelegatingListSubclass(
                        [IndexedOnlyCarrier([view()])])]})
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name, carrier="gen"):
                check_fires(self, lambda wrap=wrap: {"pairs": [
                    wrap(gen_of(keys_view()))]})
            with self.subTest(container=container_name, carrier="indexed"):
                check_fires(self, lambda wrap=wrap: {"pairs": [
                    wrap(IndexedOnlyCarrier([keys_view()]))]})

    def test_pairs_element_delegating_clean_clears(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_clears(self, lambda: {"pairs": [
            DelegatingDequeSubclass(
                [IndexedOnlyCarrier([values_view()])])]})

    def test_pairs_element_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingTupleSubclass(
                (IndexedOnlyCarrier([items_view()]),))]})

    def test_pairs_element_bundle_and_standing_poles_stand(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingListSubclass([gen_of(keys_view())])]}})
        check_fires(self, lambda: {"pairs": [
            [gen_of(keys_view())]]})
        check_fires(self, lambda: {"pairs": [
            ListSubclassPlain([gen_of(keys_view())])]})


class Ruling1899ItemsElementDelegatingTests(unittest.TestCase):
    """Ruling 1899, Eval Finding 3: the same element
    presentations standing as elements of the sequence
    standing at the items position fire at the direct act
    and at the dataset surface, counted severally from
    rulings 1897 and 1898 on the position ground, the
    parity break standing on those two surfaces against
    the plain container poles of the same geometry."""

    def test_items_element_silent_presentations_fire(self):
        for view_name, view in VIEWS.items():
            with self.subTest(view=view_name, carrier="indexed"):
                check_fires(self, lambda view=view: {"items": [
                    DelegatingListSubclass(
                        [IndexedOnlyCarrier([view()])])]})
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name, carrier="gen"):
                check_fires(self, lambda wrap=wrap: {"items": [
                    wrap(gen_of(keys_view()))]})
            with self.subTest(container=container_name, carrier="indexed"):
                check_fires(self, lambda wrap=wrap: {"items": [
                    wrap(IndexedOnlyCarrier([keys_view()]))]})

    def test_items_element_delegating_clean_clears(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_clears(self, lambda: {"items": [
            DelegatingUserListSubclass(
                [IndexedOnlyCarrier([items_view()])])]})

    def test_items_element_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingDequeSubclass(
                [IndexedOnlyCarrier([values_view()])])]})

    def test_items_element_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [
            [gen_of(keys_view())]]})
        check_fires(self, lambda: {"items": [
            ListSubclassPlain([gen_of(keys_view())])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})


class Ruling1900PairsCombinedDelegatingTests(unittest.TestCase):
    """Ruling 1900, Eval Finding 4: the combined clean view
    form of ruling 1677 standing inside a container
    standing in a delegating subclass form standing as an
    element of the sequence standing at the pairs position
    fires at the direct act, beside the dataset surface
    firing in parity and the bundle surfaces refusing,
    counted severally from rulings 1897 to 1899 on the
    form ground."""

    def test_combined_in_delegating_containers_at_pairs_fires(self):
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name):
                check_fires(self, lambda wrap=wrap: {"pairs": [
                    wrap(combined_form(keys_view))]}, comparisons=2)

    def test_combined_in_delegating_at_pairs_clean_clears(self):
        check_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([combined_form(keys_view)])]},
            comparisons=2)
        check_clears(self, lambda: {"pairs": [
            DelegatingListSubclass([combined_form(keys_view)])]},
            comparisons=2)

    def test_combined_in_delegating_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListSubclass([combined_form(keys_view)])]},
            comparisons=2)
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingDequeSubclass([combined_form(keys_view)])]},
            comparisons=2)

    def test_combined_pairs_bundle_and_standing_poles_stand(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": [
                DelegatingListSubclass([combined_form(keys_view)])]}})
        check_fires(self, lambda: {"pairs": [
            [combined_form(keys_view)]]}, comparisons=2)


class Ruling1901ItemsCombinedDelegatingTests(unittest.TestCase):
    """Ruling 1901, Eval Finding 5: the combined clean view
    form of ruling 1677 standing inside a container
    standing in a delegating subclass form standing as an
    element of the sequence standing at the items position
    fires at the direct act and at the dataset surface,
    counted severally from ruling 1900 on the position
    ground."""

    def test_combined_in_delegating_containers_at_items_fires(self):
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name):
                check_fires(self, lambda wrap=wrap: {"items": [
                    wrap(combined_form(keys_view))]})

    def test_combined_in_delegating_at_items_clean_clears(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([combined_form(keys_view)])]})
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([combined_form(keys_view)])]})

    def test_combined_in_delegating_at_items_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([combined_form(keys_view)])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingTupleSubclass(
                (combined_form(keys_view),))]})

    def test_combined_items_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [
            [combined_form(keys_view)]]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([combined_form(keys_view)])]})



class Ruling1902SetCarrierAtMappingValueTests(unittest.TestCase):
    """Ruling 1902, S15-R33-CROSS-1: a carrier standing
    inside a set form at a governed mapping value reaches
    the comparison count at the direct act, in parity with
    the dataset surface and the promote wrapper judging
    the same presentation, beside the bundle surfaces
    refusing."""

    def test_carrier_in_set_forms_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": {gen_of(keys_view())}}})
        check_fires(self, lambda: {"pairs": {
            "o": frozenset([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": SetSubclassPlain([gen_of(keys_view())])}})

    def test_carrier_in_set_forms_at_holdout_and_items_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": {gen_of(values_view())}}})
        check_fires(self, lambda: {"holdout_items": {
            "o": frozenset([gen_of(values_view())])}})
        check_fires(self, lambda: {"items": {
            "o": {gen_of(keys_view())}}})

    def test_carrier_in_set_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": {gen_of(keys_view())}}})
        check_clean_material_clears(self, lambda: {"pairs": {
            "o": {gen_of(clean_keys_view())}}})
        check_clean_material_clears(self, lambda: {"pairs": {
            "o": frozenset([gen_of(clean_keys_view())])}})

    def test_carrier_in_set_dataset_and_wrapper_fire(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": {gen_of(keys_view())}}})
        check_wrapper_fires(self, lambda: {"pairs": {
            "o": {gen_of(keys_view())}}})

    def test_carrier_in_set_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": {
                "o": {gen_of(keys_view())}}}})
        check_fires(self, lambda: {"pairs": {
            "o": {gen_of(keys_view())}}})


class Ruling1903DelegatingSetTests(unittest.TestCase):
    """Ruling 1903, S15-R33-CROSS-2: a carrier or a view
    standing inside a delegating set form at a governed
    position reaches decision at the direct act and at
    the dataset surface, in parity at every governed
    surface, beside the bundle surfaces refusing, counted
    severally from ruling 1902 on the form ground."""

    def test_carrier_in_delegating_set_forms_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingSetSubclass([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingFrozensetSubclass([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingAbstractSetSubclass(
                [gen_of(keys_view())])}})

    def test_carrier_in_delegating_set_at_holdout_and_items_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": DelegatingSetSubclass([gen_of(values_view())])}})
        check_fires(self, lambda: {"items": {
            "o": DelegatingSetSubclass([gen_of(keys_view())])}})

    def test_view_alone_in_delegating_set_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingSetSubclass([keys_view()])}})

    def test_delegating_set_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingSetSubclass([gen_of(keys_view())])}})
        check_clean_material_clears(self, lambda: {"pairs": {
            "o": DelegatingSetSubclass([gen_of(clean_keys_view())])}})
        check_clean_material_clears(self, lambda: {"pairs": {
            "o": DelegatingSetSubclass([gen_of(clean_keys_view())])}})

    def test_delegating_set_dataset_and_bundle_stand(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingSetSubclass([gen_of(keys_view())])}})
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": {
                "o": DelegatingSetSubclass([gen_of(keys_view())])}}})


class Ruling1904NestedSetAtPairsTests(unittest.TestCase):
    """Ruling 1904, S15-R33-CROSS-3: a set form standing
    nested inside a reached container at the pairs
    position stands reached at the direct act and at the
    dataset surface, in parity at every governed surface,
    beside the bundle surfaces refusing, counted severally
    from rulings 1902 and 1903 on the nesting ground."""

    def test_set_nested_in_reached_containers_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{gen_of(keys_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": [DelegatingSetSubclass([gen_of(keys_view())])]}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingTupleSubclass(
                (frozenset([gen_of(keys_view())]),))}})

    def test_nested_set_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{gen_of(keys_view())}])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{gen_of(keys_view())}])}})

    def test_nested_set_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{gen_of(keys_view())}])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": [DelegatingSetSubclass([gen_of(keys_view())])]}})

    def test_nested_set_bundle_refuses(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": {
                "o": DelegatingListSubclass(
                    [{gen_of(keys_view())}])}}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{gen_of(keys_view())}])}})


class Ruling1905ItemsDelegatingContainerTests(unittest.TestCase):
    """Ruling 1905, S15-R33-CROSS-4: a carrier or an inner
    mapping standing inside a delegating container at the
    items position reaches the comparison count at the
    direct act and carries a result at the dataset
    surface, in parity at every governed surface, beside
    the bundle surfaces refusing, counted severally from
    rulings 1902 to 1904 on the position ground."""

    def test_carrier_in_delegating_container_at_items_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_fires(self, lambda: {"items": [
            DelegatingTupleSubclass((gen_of(keys_view()),))]})

    def test_mapping_in_delegating_container_at_items_fires(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([{"p": gen_of(keys_view())}])]})

    def test_items_delegating_clean_clears(self):
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_clears(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})

    def test_items_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([gen_of(keys_view())])]})
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([{"p": gen_of(keys_view())}])]})

    def test_items_delegating_bundle_and_standing_poles_stand(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [
                DelegatingListSubclass([gen_of(keys_view())])]}})
        check_fires(self, lambda: {"items": [
            [gen_of(keys_view())]]})
        check_fires(self, lambda: {"items": [
            ListSubclassPlain([gen_of(keys_view())])]})


class Ruling1906ViewDirectlyInDelegatingContainerTests(
        unittest.TestCase):
    """Ruling 1906, S15-R33-CROSS-5: a dictionary view
    standing directly inside a delegating list, deque, or
    tuple container at the pairs position, with no carrier
    standing between, reaches the comparison count at the
    direct act and carries a result at the dataset
    surface, in parity at every governed surface, beside
    the bundle surfaces refusing, counted severally from
    rulings 1902 to 1905 on the carrier ground."""

    def test_view_directly_in_delegating_containers_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingDequeSubclass([keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingTupleSubclass((keys_view(),))}})

    def test_view_directly_in_delegating_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([keys_view()])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([keys_view()])}})
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": {"o": DelegatingListSubclass(
                        [clean_keys_view()])}},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_view_directly_in_delegating_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([keys_view()])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingDequeSubclass([values_view()])}})

    def test_view_directly_bundle_and_standing_poles_stand(self):
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"pairs": {
                "o": DelegatingListSubclass([keys_view()])}}})
        check_fires(self, lambda: {"pairs": {
            "o": [keys_view()]}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([keys_view()])}})


class Ruling1907DelegatingStorageWrapTests(unittest.TestCase):
    """Ruling 1907, S15-R33-CROSS-6: a governed view
    standing inside a delegating container in the storage
    of a mapping presenting a clean view at its governed
    entry reaches decision at the direct act and at the
    dataset surface, beside the bundle surfaces refusing,
    counted severally from rulings 1902 to 1906 on the
    storage ground. The promote wrapper pole of this
    ruling stands bounded in the builder paper in the
    open: the wrapper materialisation in its own file
    rebuilds a mapping from its presented items, so the
    storage form stands outside the surfaces this pin
    judges here."""

    def test_stored_view_in_delegating_wraps_fires(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([view]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingSetSubclass([view]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([[view]]))]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(), lambda view: _deque([view]))]})

    def test_stored_view_delegating_wrap_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: DelegatingListSubclass([view]))]})
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: DelegatingSetSubclass([view]))]})
        check_bundle_refuses(self, lambda: {
            "instruction_items": [{"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [
                container_view_dict(
                    keys_view(),
                    lambda view: DelegatingListSubclass([view]))]}})

    def test_stored_view_slot_delegating_wrap_fires(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: SlotDelegatingListSubclass([view]))]})
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(
                keys_view(),
                lambda view: SlotDelegatingListSubclass([view]))]})

    def test_stored_view_plain_wrap_standing_pole_stands(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(), lambda view: [view])]})
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(),
            lambda view: DelegatingListSubclass([view]))]})


class CleanViewOuterDict(dict):
    """A dict subclass whose items reading presents an
    inner mapping carrying a clean keys view at the
    governed entry, in place of the inner mapping whose
    storage carries the governed view inside a plain
    container."""

    def items(self):
        return {
            key: (
                {"n": clean_keys_view()} if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


def nested_storage_dict():
    return CleanViewOuterDict([
        ("o", {"n": [keys_view()]}),
        ("c", "plain clean value"),
    ])


class Ruling1908NestedStorageDepthTests(unittest.TestCase):
    """Ruling 1908, S15-R33-CROSS-7: a governed view
    standing inside a plain container in the storage of
    a mapping standing as the storage value at the
    governed entry of a second mapping reaches decision
    at the direct act and at the dataset surface, in
    parity at every governed surface, beside the bundle
    surfaces refusing, counted severally from ruling
    1907 on the storage ground."""

    def test_nested_storage_wrapped_view_fires(self):
        check_fires(self, lambda: {"items": [nested_storage_dict()]})

    def test_nested_storage_wrapped_view_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            nested_storage_dict()]})

    def test_nested_storage_wrapped_view_wrapper_fires(self):
        check_wrapper_fires(self, lambda: {"items": [
            nested_storage_dict()]})

    def test_nested_storage_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [container_view_dict(
            keys_view(), lambda view: {"n": view})]})
        check_fires(self, lambda: {"items": [nested_storage_dict()]})



class SpoofEq:
    """A clean standing object whose own equality reading
    returns true against any form it is compared with."""

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    __hash__ = object.__hash__


class NonBoolEq:
    """An object whose equality reading returns the truthy
    non bool value 1 against any form."""

    def __eq__(self, other):
        return 1

    def __ne__(self, other):
        return 0

    __hash__ = object.__hash__


def spoof_values_view():
    return {1: SpoofEq()}.values()


def spoof_items_view():
    return {1: SpoofEq()}.items()


def spoof_tuple_values_view():
    return {1: (SpoofEq(), SpoofEq())}.values()


def spoof_second_values_view():
    return {1: (HashableItem(CANDIDATE), SpoofEq())}.values()


def spoof_key_keys_view():
    return {(SpoofEq(),): 1}.keys()


def nonbool_key_keys_view():
    return {(NonBoolEq(),): 1}.keys()


def governed_values_view():
    from tests.test_cross_fix_r31 import governed_values_view as maker
    return maker()


def governed_items_view():
    from tests.test_cross_fix_r31 import governed_items_view as maker
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
        "DynSpoofDict", (SpoofSubstDict,),
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


class Ruling1909DatasetEqualitySpoofTests(unittest.TestCase):
    """Ruling 1909, S15-R33-DATA-1: the equality spoof at
    the dataset instruction item surface, value side and
    bool key side: a clean standing object whose own
    equality reading returns true against any form,
    presented in place of governed material at the
    positions the Dataset paper states, stands refused
    at the dataset surface, the direct act and the
    promote wrapper firing in parity with their
    controls."""

    def test_spoof_value_at_values_and_items_views_refused(self):
        check_dataset_spoof_refused(
            self, spoof_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, spoof_items_view, governed_items_view)

    def test_spoof_tuple_and_second_element_refused(self):
        check_dataset_spoof_refused(
            self, spoof_tuple_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, spoof_second_values_view, governed_values_view)

    def test_spoof_bool_key_side_refused(self):
        check_dataset_spoof_refused(
            self, spoof_key_keys_view, keys_view, comparisons=2)

    def test_spoof_at_pairs_position_refused(self):
        check_dataset_spoof_refused(
            self, spoof_values_view, governed_values_view,
            wrapkey="pairs")

    def test_spoof_direct_and_wrapper_fire_in_parity(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, spoof_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, spoof_values_view, governed_values_view)


class Ruling1910ViewKeyNonBoolSpoofTests(unittest.TestCase):
    """Ruling 1910, S15-R33-DATA-2: the non bool equality
    spoof at the view underlying key side, dataset
    surface only: an object whose equality reading
    returns the truthy non bool value 1 against any
    form, presented inside the tuple key a keys view
    stands over, stands as no match at the dataset
    surface, counted severally from ruling 1909 on the
    guard ground."""

    def test_nonbool_key_spoof_refused_at_dataset(self):
        check_dataset_spoof_refused(
            self, nonbool_key_keys_view, keys_view, comparisons=2)

    def test_nonbool_key_direct_and_wrapper_fire(self):
        check_direct_and_wrapper_fire_on_spoof(
            self, nonbool_key_keys_view, keys_view)
        check_dataset_spoof_refused(
            self, nonbool_key_keys_view, keys_view, comparisons=2)

    def test_nonbool_value_side_standing_pole_stands(self):
        def nonbool_values_view():
            return {1: NonBoolEq()}.values()
        check_dataset_spoof_refused(
            self, nonbool_values_view, governed_values_view)
        check_dataset_spoof_refused(
            self, nonbool_key_keys_view, keys_view, comparisons=2)


if __name__ == "__main__":
    unittest.main()
