"""Fix round 32 tests for Region 2: cross split delegating containers.

Charges pinned here, from design/steps/step-15-r32-triage.md:
ruling 1790 (a dictionary view of any kind inside a carrier of
any governed kind inside a container standing in a delegating
subclass form of a plain container at a value of a mapping
standing at the pairs position of audit_instruction_item
reaching no comparison at the direct act, silent at the
direct act and carrying no result at the dataset instruction
item surface beside a refusal at the bundle surfaces, at the
Eval Finding 1 identity of the Round 32 Eval paper, roster
2704, Low); ruling 1791 (the same view and carrier forms
inside a delegating subclass container at a value of a
mapping standing at the holdout_items position reaching no
comparison at the direct act, silent at the same two surfaces
beside the same refusal, at the Eval Finding 2 identity, Low,
counted severally from ruling 1790 on the position ground);
ruling 1792 (a mapping standing inside a delegating subclass
container at a value of a mapping standing at the pairs
position, carrying a view inside a carrier at its own value,
reaching no comparison at the direct act, silent at the same
two surfaces beside the same refusal, at the Eval Finding 3
identity, Low, counted severally from rulings 1790 and 1791
on the geometry ground); and ruling 1793 (the carrier and
inner mapping forms standing inside a double container with
one delegating level at either depth at the pairs position
reaching no comparison at the direct act, silent at the same
two surfaces beside the same refusal, at the Eval Finding 4
identity, Low, counted severally from rulings 1790 to 1792 on
the container depth ground). Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py and
promote.py stand untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest

from tests import harness
from tests.test_cross_fix_r19 import OnceOnlyIterable
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    check_clears,
    check_fires,
)
from tests.test_cross_fix_r24 import (
    ListSubclassPlain,
    check_dataset_fires,
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


def check_direct_clean_view_clears(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertFalse(result["fired"])
            test_case.assertEqual(result["comparisons"], 1)


class Ruling1790PairsDelegatingContainerTests(unittest.TestCase):
    """Ruling 1790, Eval Finding 1: a dictionary view of any
    kind inside a carrier of any governed kind inside a
    container standing in a delegating subclass form at a
    value of a plain mapping standing at the pairs position
    fires at the direct act, beside the dataset surface
    firing on the same presentations in parity and the
    bundle surfaces refusing, one ring past the cured forms
    of rulings 1673 to 1677."""

    def test_views_in_iterator_carriers_in_delegating_list_fire(self):
        for view_name, view in VIEWS.items():
            for carrier_name in ("gen", "zip", "enum"):
                with self.subTest(view=view_name, carrier=carrier_name):
                    check_fires(self, lambda view=view, carrier_name=carrier_name: {
                        "pairs": {"o": DelegatingListSubclass(
                            [CARRIERS[carrier_name](view())])}})

    def test_views_in_carriers_in_other_delegating_containers_fire(self):
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name):
                check_fires(self, lambda wrap=wrap: {"pairs": {
                    "o": wrap(gen_of(keys_view()))}})
        for carrier_name in ("seq", "indexed", "custom", "once"):
            for view_name, view in VIEWS.items():
                with self.subTest(carrier=carrier_name, view=view_name):
                    check_fires(self, lambda carrier_name=carrier_name, view=view: {
                        "pairs": {"o": DelegatingDequeSubclass(
                            [CARRIERS[carrier_name](view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingTupleSubclass(
                (SequenceCarrier([items_view()]),))}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingUserListSubclass(
                [IndexedOnlyCarrier([values_view()])])}})

    def test_carrier_in_delegating_container_at_pairs_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingTupleSubclass((zip([values_view()]),))}})

    def test_carrier_in_delegating_container_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingDequeSubclass(
                [SequenceCarrier([values_view()])])}})

    def test_delegating_pairs_bundle_and_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_bundle_refuses(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": [gen_of(keys_view())]}})
        check_direct_clean_view_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([gen_of(clean_keys_view())])}})


class Ruling1791HoldoutDelegatingContainerTests(unittest.TestCase):
    """Ruling 1791, Eval Finding 2: the same view and carrier
    forms inside a delegating subclass container at a value
    of a plain mapping standing at the holdout_items position
    fire at the direct act, beside the dataset surface firing
    in parity and the bundle surfaces refusing, counted
    severally from ruling 1790 on the position ground, the
    standing poles of ruling 1790 standing pinned beside it."""

    def test_views_in_iterator_carriers_in_delegating_list_fire(self):
        for view_name, view in VIEWS.items():
            for carrier_name in ("gen", "zip", "enum"):
                with self.subTest(view=view_name, carrier=carrier_name):
                    check_fires(self, lambda view=view, carrier_name=carrier_name: {
                        "holdout_items": {"o": DelegatingListSubclass(
                            [CARRIERS[carrier_name](view())])}})

    def test_views_in_carriers_in_other_delegating_containers_fire(self):
        for container_name, wrap in DELEGATING.items():
            with self.subTest(container=container_name):
                check_fires(self, lambda wrap=wrap: {"holdout_items": {
                    "o": wrap(gen_of(values_view()))}})
        for carrier_name in ("seq", "indexed", "custom", "once"):
            for view_name, view in VIEWS.items():
                with self.subTest(carrier=carrier_name, view=view_name):
                    check_fires(self, lambda carrier_name=carrier_name, view=view: {
                        "holdout_items": {"o": DelegatingUserListSubclass(
                            [CARRIERS[carrier_name](view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": DelegatingTupleSubclass(
                (IndexedOnlyCarrier([keys_view()]),))}})

    def test_carrier_in_delegating_container_at_holdout_clean_clears(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": DelegatingListSubclass([gen_of(values_view())])}})
        check_clears(self, lambda: {"holdout_items": {
            "o": DelegatingListSubclass([gen_of(values_view())])}})
        check_clears(self, lambda: {"holdout_items": {
            "o": DelegatingDequeSubclass(
                [SequenceCarrier([keys_view()])])}})

    def test_carrier_in_delegating_container_at_holdout_dataset_fires(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": DelegatingListSubclass([gen_of(values_view())])}})
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": DelegatingTupleSubclass(
                (gen_of(keys_view()),))}})

    def test_delegating_holdout_bundle_and_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": DelegatingListSubclass([gen_of(values_view())])}})
        check_bundle_refuses(self, lambda: {"holdout_items": {
            "o": DelegatingListSubclass([gen_of(values_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(values_view())]}})


class Ruling1792PairsMappingInDelegatingContainerTests(
        unittest.TestCase):
    """Ruling 1792, Eval Finding 3: a mapping standing inside
    a delegating subclass container at a value of a mapping
    standing at the pairs position, carrying a view inside a
    carrier at its own value, fires at the direct act, beside
    the dataset surface firing in parity and the bundle
    surfaces refusing, counted severally from rulings 1790
    and 1791 on the geometry ground."""

    def test_mapping_in_delegating_list_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": gen_of(keys_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": zip([values_view()])}])}})

    def test_mapping_in_other_delegating_containers_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingTupleSubclass(({"p": gen_of(keys_view())},))}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingDequeSubclass([{"p": gen_of(items_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingUserListSubclass(
                [{"p": SequenceCarrier([values_view()])}])}})

    def test_mapping_in_delegating_container_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": gen_of(keys_view())}])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": gen_of(keys_view())}])}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingDequeSubclass([{"p": gen_of(keys_view())}])}})

    def test_mapping_in_delegating_container_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": gen_of(keys_view())}])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingUserListSubclass(
                [{"p": gen_of(values_view())}])}})

    def test_delegating_mapping_bundle_and_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": gen_of(keys_view())}])}})
        check_bundle_refuses(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([{"p": gen_of(keys_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([{"p": gen_of(keys_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": [{"p": gen_of(keys_view())}]}})


class ListSub(list):
    pass


DOUBLE_MIXES = {
    "dlist-in-list": lambda carrier: [
        DelegatingListSubclass([carrier])],
    "list-in-dlist": lambda carrier: DelegatingListSubclass(
        [[carrier]]),
    "dlist-in-dlist": lambda carrier: DelegatingListSubclass(
        [DelegatingListSubclass([carrier])]),
    "listsub-in-dlist": lambda carrier: DelegatingListSubclass(
        [ListSub([carrier])]),
    "dlist-in-listsub": lambda carrier: ListSub(
        [DelegatingListSubclass([carrier])]),
}


class Ruling1793PairsDoubleContainerDelegatingTests(
        unittest.TestCase):
    """Ruling 1793, Eval Finding 4: the carrier and inner
    mapping forms standing inside a double container with
    one delegating level at either depth at the pairs
    position fire at the direct act, beside the dataset
    surface firing in parity and the bundle surfaces
    refusing, counted severally from rulings 1790 to 1792
    on the container depth ground, the standing poles of
    rulings 1790 to 1792 standing pinned beside it."""

    def test_carrier_in_double_container_with_delegating_level_fires(self):
        for mix_name, mix in DOUBLE_MIXES.items():
            with self.subTest(mix=mix_name):
                check_fires(self, lambda mix=mix: {"pairs": {
                    "o": mix(gen_of(values_view()))}})

    def test_mapping_in_double_container_with_delegating_level_fires(self):
        for mix_name, mix in DOUBLE_MIXES.items():
            with self.subTest(mix=mix_name):
                check_fires(self, lambda mix=mix: {"pairs": {
                    "o": mix({"p": gen_of(keys_view())})}})

    def test_double_container_with_delegating_level_clean_clears(self):
        check_fires(self, lambda: {"pairs": {
            "o": [DelegatingListSubclass([gen_of(values_view())])]}})
        check_clears(self, lambda: {"pairs": {
            "o": [DelegatingListSubclass([gen_of(values_view())])]}})
        check_clears(self, lambda: {"pairs": {
            "o": DelegatingListSubclass([[gen_of(keys_view())]])}})

    def test_double_container_with_delegating_level_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": [DelegatingListSubclass([gen_of(values_view())])]}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DelegatingListSubclass(
                [[{"p": gen_of(keys_view())}]])}})

    def test_double_container_bundle_and_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": [DelegatingListSubclass([gen_of(values_view())])]}})
        check_bundle_refuses(self, lambda: {"pairs": {
            "o": [DelegatingListSubclass([gen_of(values_view())])]}})
        check_fires(self, lambda: {"pairs": {
            "o": [ListSubclassPlain([gen_of(values_view())])]}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([[gen_of(values_view())]])}})
        check_fires(self, lambda: {"pairs": {
            "o": [[gen_of(values_view())]]}})


if __name__ == "__main__":
    unittest.main()
