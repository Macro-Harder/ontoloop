"""Fix round 18 tests for Region 2: cross split.

Charges pinned here, from design/steps/step-15-r18-triage.md:
ruling 662 (the cross split audit view inside a container
single pair merged defect at the R18-CROSS-1 identity, Low,
with R18-SPAN-1, R18-UC-1, and R18-UC-2 counted in the same
act), the pairs position reading of the direct act reaching
a dictionary view standing inside a container at any depth
and inside a nested mapping value; ruling 663 (the single
pass iterable nested form merged defect at the R18-CROSS-2
identity, Low, with R18-SPAN-4 counted in the same act on
its direct act limb), a detection listing of a presented
position standing spent once and carried within the act at
any nesting, at the direct act and at the bundle surfaces;
ruling 664 (the items view key carrier merged defect at
the R18-CROSS-3 identity, Low, with R18-SPAN-2 counted in
the same act), the presentation reading reaching material
standing as a key of a mapping presented through its items
view; ruling 665 (the ChainMap keys wrong side merged
defect at the R18-CROSS-4 identity, Low, with R18-SPAN-3
and R18-UC-4 counted in the same act), the pairs position
reading taking the sides of a ChainMap keys presentation
in the order of its maps; ruling 666 (the view through a
values view defect at the R18-UC-3 identity, Low), the
pairs position reading reaching a view standing presented
through a second view; and ruling 667 (the keyed mapping
at a mapping value defect at the R18-UC-5 identity, Low),
the presentation reading reaching material standing as
the keys of a mapping standing at a mapping value.
dataset.py stands expressly unchanged in this round, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import collections
import collections.abc
import unittest
from collections import OrderedDict, UserDict, ChainMap
from types import MappingProxyType

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"
CANDIDATE_TEXT = "shared bundle text alpha"

OCCASIONS = ("candidate construction", "promotion")

BUNDLE_SURFACES = (
    "audit_at_promotion",
    "audit_at_build",
    "audit_at_evaluation",
)

CANDIDATE = {
    "group": "g1",
    "signature": "s1",
    "text": "shared bundle text alpha",
    "split": "candidate",
}
HOLDOUT = {
    "group": "g1",
    "signature": "s9",
    "text": "shared bundle text alpha",
    "split": "holdout",
}
CLEAN_HOLDOUT = {
    "group": "g2",
    "signature": "s9",
    "text": "unrelated wording entirely",
    "split": "holdout",
}
HOLDOUT_ITEM = {"text": HOLDOUT_TEXT, "split": "holdout"}


class HashableItem(dict):
    """A mapping item that can stand inside a set or as a key."""

    __hash__ = object.__hash__


class OnceOnlyIterable:
    """A general iterable standing listed once only.

    The first listing yields its elements and later
    listings yield none. It carries no next method of
    its own, so it stands apart from an iterator.
    """

    def __init__(self, items):
        self._items = list(items)
        self._spent = False

    def __iter__(self):
        if self._spent:
            return iter([])
        self._spent = True
        return iter(self._items)


class ReIterableCarrier:
    """A general iterable container standing re-iterable."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


class SequenceCarrier(collections.abc.Sequence):
    """An abstract Sequence carrier holding its elements."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


def check_fires(test_case, make_bundle, comparisons=1):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertTrue(result["fired"])
            test_case.assertEqual(result["comparisons"], comparisons)


def check_clears(test_case, make_bundle, comparisons=1):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                CLEAN_TEXT, make_bundle(), occasion=occasion)
            test_case.assertFalse(result["fired"])
            test_case.assertEqual(result["comparisons"], comparisons)


def check_refuses(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 1)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], 1)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertTrue(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], 1)


def check_proceeds(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertFalse(result["candidate_bundle_refused"])
            test_case.assertTrue(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertFalse(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], 0)


def check_governed_refusal(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertTrue(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], 0)


def inner_mapping():
    return {"inner": {"text": HOLDOUT_TEXT}}


def flagged_pair():
    return [dict(CANDIDATE), dict(HOLDOUT)]


def clean_pair():
    return [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]


def malformed_pair():
    return [dict(CANDIDATE)]


def direct_pair():
    return [dict(CANDIDATE), dict(HOLDOUT_ITEM)]


def plain_values_view():
    return {0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM)}.values()


def plain_keys_view():
    return {
        HashableItem(CANDIDATE): 1,
        HashableItem(HOLDOUT_ITEM): 2,
    }.keys()


def plain_items_view():
    return {0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM)}.items()


def chain_map_keys_view():
    return ChainMap(
        {HashableItem(CANDIDATE): 1},
        {HashableItem(HOLDOUT_ITEM): 2},
    ).keys()


class ViewInsideContainerAnyDepthTests(unittest.TestCase):
    """Ruling 662: a dictionary view standing inside a
    container at any depth, or inside a nested mapping
    value at the pairs position, fires at the direct act."""

    def test_list_holding_deque_holding_values_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            collections.deque([plain_values_view()]),
        ]})

    def test_deque_holding_deque_holding_values_view_fires(self):
        check_fires(self, lambda: {"pairs":
            collections.deque([
                collections.deque([plain_values_view()])]),
        })

    def test_list_holding_user_list_holding_values_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            collections.UserList([plain_values_view()]),
        ]})

    def test_list_holding_zip_holding_values_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            zip([plain_values_view()]),
        ]})

    def test_three_containers_deep_forms_fire(self):
        forms = (
            ("list list list", lambda view: [[ [view] ]]),
            ("tuple tuple tuple", lambda view: (((view,),),)),
            ("list list list keys", lambda view: [[ [view] ]]),
        )
        views = (
            plain_values_view, plain_values_view, plain_keys_view,
        )
        for (name, form), view_form in zip(forms, views):
            with self.subTest(form=name):
                check_fires(self, lambda form=form, view_form=view_form: {
                    "pairs": form(view_form()),
                })

    def test_second_container_spanning_forms_fire(self):
        forms = (
            ("enumerate", lambda view: enumerate([view])),
            ("sequence carrier", lambda view: SequenceCarrier([view])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {"pairs": [
                    form(chain_map_keys_view()),
                ]})

    def test_nested_mapping_value_holding_view_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": {"inner_key": plain_values_view()},
        }})

    def test_nested_mapping_value_mapping_forms_fire(self):
        forms = (
            ("plain in plain", lambda inner: {
                "key": dict(inner)}),
            ("ordered in ordered", lambda inner: OrderedDict(
                [("key", OrderedDict(inner))])),
            ("user dict in plain", lambda inner: {
                "key": UserDict(inner)}),
            ("proxy in plain", lambda inner: {
                "key": MappingProxyType(dict(inner))}),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {"pairs": form(
                    {"inner_key": plain_keys_view()},
                )})

    def test_clean_deep_container_forms_clear(self):
        check_clears(self, lambda: {"pairs": [
            collections.deque([plain_values_view()]),
        ]})
        check_clears(self, lambda: {"pairs": [
            [[plain_values_view()]],
        ]})
        check_clears(self, lambda: {"pairs": {
            "key": {"inner_key": plain_values_view()},
        }})

    def test_view_inside_container_controls_stand(self):
        check_fires(self, lambda: {"pairs": [plain_values_view()]})
        check_fires(self, lambda: {"pairs": [[plain_values_view()]]})
        check_fires(self, lambda: {"pairs": {
            "key": plain_values_view(),
        }})
        check_governed_refusal(self, lambda: {"pairs": [
            collections.deque([plain_values_view()]),
        ]})


class SinglePassNestedFormTests(unittest.TestCase):
    """Ruling 663: a single pass iterable standing nested
    inside a list or a tuple element of the pairs position,
    or standing as a value inside an items view at that
    position, is read in full and no second listing raises."""

    def test_nested_list_once_only_index_pair_flagged_refuses(self):
        check_refuses(self, lambda: {"pairs": [
            [OnceOnlyIterable([0, flagged_pair()])],
        ]})

    def test_nested_tuple_once_only_index_pair_flagged_refuses(self):
        check_refuses(self, lambda: {"pairs": [
            (OnceOnlyIterable([0, flagged_pair()]),),
        ]})

    def test_nested_once_only_index_pair_clean_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            [OnceOnlyIterable([0, clean_pair()])],
        ]})

    def test_nested_once_only_index_pair_malformed_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            [OnceOnlyIterable([0, malformed_pair()])],
        ]})

    def test_once_only_holding_list_holding_once_only_refuses(self):
        check_refuses(self, lambda: {"pairs":
            OnceOnlyIterable([
                [OnceOnlyIterable([0, flagged_pair()])],
            ]),
        })

    def test_items_view_once_only_index_pair_direct_fires(self):
        check_fires(self, lambda: {"pairs": {
            0: OnceOnlyIterable([0, direct_pair()]),
        }.items()})

    def test_items_view_once_only_plain_pair_direct_fires(self):
        check_fires(self, lambda: {"pairs": {
            0: OnceOnlyIterable(direct_pair()),
        }.items()})

    def test_items_view_list_holding_once_only_direct_fires(self):
        check_fires(self, lambda: {"pairs": {
            0: [OnceOnlyIterable([0, direct_pair()])],
        }.items()})

    def test_items_view_once_only_direct_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            0: OnceOnlyIterable([0, direct_pair()]),
        }.items()})

    def test_single_pass_nested_controls_stand(self):
        check_refuses(self, lambda: {"pairs": [
            OnceOnlyIterable([0, flagged_pair()]),
        ]})
        check_refuses(self, lambda: {"pairs": [
            ReIterableCarrier([0, flagged_pair()]),
        ]})
        check_refuses(self, lambda: {
            "pairs": (entry for entry in [flagged_pair()]),
        })
        check_fires(self, lambda: {"pairs": {
            0: [[0, direct_pair()]],
        }.items()})


class ItemsViewKeyCarrierTests(unittest.TestCase):
    """Ruling 664: material standing as a key of a mapping
    presented through its items view fires at the direct
    act, at the holdout_items, holdout, and items positions."""

    def test_items_view_key_at_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }.items()})

    def test_items_view_key_at_holdout_fires(self):
        check_fires(self, lambda: {"holdout": {
            HashableItem(inner_mapping()): 1,
        }.items()})

    def test_items_view_key_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            HashableItem({"key": {"inner": {
                "text": HOLDOUT_TEXT, "split": "holdout"}}}): 1,
        }.items()})

    def test_clean_items_view_key_clears_with_comparison(self):
        check_clears(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }.items()})

    def test_items_view_key_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }.keys()})
        check_fires(self, lambda: {"holdout_items": {
            0: inner_mapping(),
        }.items()})


class ChainMapKeysOrderTests(unittest.TestCase):
    """Ruling 665: a pair whose sides stand as the keys of
    a ChainMap at the pairs position stands read in the
    order of its maps, so the holdout side stands compared."""

    def test_chain_map_keys_at_position_fire_on_verbatim(self):
        check_fires(self, lambda: {"pairs": ChainMap(
            {HashableItem(CANDIDATE): 1},
            {HashableItem(HOLDOUT_ITEM): 2},
        )})

    def test_chain_map_keys_do_not_fire_on_candidate_text(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    CANDIDATE_TEXT,
                    {"pairs": ChainMap(
                        {HashableItem(CANDIDATE): 1},
                        {HashableItem(HOLDOUT_ITEM): 2},
                    )},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_chain_map_keys_inside_list_fire(self):
        check_fires(self, lambda: {"pairs": [ChainMap(
            {HashableItem(CANDIDATE): 1},
            {HashableItem(HOLDOUT_ITEM): 2},
        )]})

    def test_clean_chain_map_keys_clear_with_comparison(self):
        check_clears(self, lambda: {"pairs": ChainMap(
            {HashableItem(CANDIDATE): 1},
            {HashableItem(HOLDOUT_ITEM): 2},
        )})

    def test_chain_map_keys_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }})
        check_fires(self, lambda: {"pairs": ChainMap({
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        })})
        check_fires(self, lambda: {"pairs": chain_map_keys_view()})


class ViewThroughValuesViewTests(unittest.TestCase):
    """Ruling 666: a dictionary view standing presented
    through a values view at the pairs position fires at
    the direct act."""

    def test_view_through_plain_values_view_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": plain_values_view(),
        }.values()})

    def test_view_through_ordered_values_view_fires(self):
        check_fires(self, lambda: {"pairs": OrderedDict(
            {"key": plain_values_view()},
        ).values()})

    def test_chain_map_values_view_inside_list_holding_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            ChainMap({"key": plain_values_view()}).values(),
        ]})

    def test_list_holding_view_through_values_view_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": [plain_values_view()],
        }.values()})

    def test_clean_view_through_values_view_clears(self):
        check_clears(self, lambda: {"pairs": {
            "key": plain_values_view(),
        }.values()})

    def test_view_through_view_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            "key": plain_values_view(),
        }.items()})
        check_fires(self, lambda: {"pairs": [plain_values_view()]})
        check_fires(self, lambda: {"pairs": {
            "key": plain_values_view(),
        }})


class KeyedMappingAtMappingValueTests(unittest.TestCase):
    """Ruling 667: a pair whose sides stand as the keys of
    a mapping standing at a mapping value of the pairs
    position fires at the direct act."""

    def test_keyed_mapping_at_mapping_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {
                HashableItem(CANDIDATE): 1,
                HashableItem(HOLDOUT_ITEM): 2,
            },
        }})

    def test_keyed_mapping_at_mapping_value_inside_list_fires(self):
        check_fires(self, lambda: {"pairs": [{
            "outer": {
                HashableItem(CANDIDATE): 1,
                HashableItem(HOLDOUT_ITEM): 2,
            },
        }]})

    def test_clean_keyed_mapping_at_mapping_value_clears(self):
        check_clears(self, lambda: {"pairs": {
            "outer": {
                HashableItem(CANDIDATE): 1,
                HashableItem(HOLDOUT_ITEM): 2,
            },
        }})

    def test_keyed_mapping_at_value_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }})
        check_fires(self, lambda: {"pairs": [{
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }]})


if __name__ == "__main__":
    unittest.main()
