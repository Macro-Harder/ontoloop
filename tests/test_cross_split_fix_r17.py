"""Fix round 17 tests for Region 2: cross split.

Charges pinned here, from design/steps/step-15-r17-triage.md:
ruling 611 (the cross split audit multi element wrapped
position merged defect at the R17-CROSS-1 identity, Low,
with R17-SPAN-1 counted in the same act), the direct act
presentation reading of ontoloop/cross_split_audit.py
reading a wrapped list or tuple position for a nested
mapping standing at any element of the position, at both
occasions; ruling 612 (the view over container wrapped
position merged defect at the R17-UC-1 identity, Low, with
Lead Engineer line E-7 counted in the same act), the view
limb of that reading reaching through a container standing
between the view and the nested mapping, at the direct act
and through the promote wrapper; ruling 613 (the view
inside a container single pair merged defect at the
R17-CROSS-2 identity, Low, with R17-SPAN-2 counted in the
same act), the pairs position reading reaching a view
standing inside a container at the pairs position;
ruling 614 (the single pass iterable form defect at the
R17-CROSS-3 identity, Low), a detection listing of a
presented position standing spent once and carried within
the act, at the direct act and at the bundle surfaces; and
ruling 615 (the mapping key carrier defect at the R17-UC-2
identity, Low, with Lead Engineer line E-8 counted in the
same act), the presentation reading reaching material
standing as a key of a mapping. dataset.py stands expressly
unchanged in this round, and no pin of this region stands
filed in tests/test_unrowed_c.py.
"""

import collections
import collections.abc
import unittest
from collections import OrderedDict, UserDict, ChainMap
from types import MappingProxyType

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"

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


def nested_position():
    return {"key": {"inner": {"text": HOLDOUT_TEXT}}}


def nested_position_b():
    return {"key_b": {"inner": {"text": HOLDOUT_TEXT}}}


def flagged_pair():
    return [dict(CANDIDATE), dict(HOLDOUT)]


def clean_pair():
    return [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]


def malformed_pair():
    return [dict(CANDIDATE)]


def direct_pair():
    return [dict(CANDIDATE), dict(HOLDOUT_ITEM)]


def chain_map_keys_view():
    return ChainMap(
        {HashableItem(CANDIDATE): 1},
        {HashableItem(HOLDOUT_ITEM): 2},
    ).keys()


def chain_map_values_view():
    return ChainMap(
        {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
    ).values()


def plain_values_view():
    return {0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM)}.values()


def plain_keys_view():
    return {
        HashableItem(CANDIDATE): 1,
        HashableItem(HOLDOUT_ITEM): 2,
    }.keys()


def plain_items_view():
    return {0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM)}.items()


class MultiElementWrappedPositionTests(unittest.TestCase):
    """Ruling 611: a wrapped position carrying a nested
    mapping at a second element or later, standing alone
    or beside a scalar, fires at the direct act."""

    def test_list_holding_two_nested_mappings_fires(self):
        check_fires(self, lambda: {"holdout_items": [
            nested_position(), nested_position_b(),
        ]}, comparisons=2)

    def test_tuple_holding_two_nested_mappings_fires(self):
        check_fires(self, lambda: {"holdout_items": (
            nested_position(), nested_position_b(),
        )}, comparisons=2)

    def test_deque_holding_two_nested_mappings_fires(self):
        check_fires(self, lambda: {"holdout_items":
            collections.deque([
                nested_position(), nested_position_b()])},
            comparisons=2)

    def test_list_nested_mapping_beside_integer_fires(self):
        check_fires(self, lambda: {"holdout_items": [
            nested_position(), 1,
        ]})

    def test_values_view_holding_two_nested_mappings_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            0: nested_position(), 1: nested_position_b(),
        }.values()}, comparisons=2)

    def test_keys_view_holding_two_nested_mappings_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(nested_position()): 1,
            HashableItem(nested_position_b()): 2,
        }.keys()}, comparisons=2)

    def test_set_holding_two_nested_mappings_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(nested_position()),
            HashableItem(nested_position_b()),
        }}, comparisons=2)

    def test_zip_forms_holding_two_nested_mappings_fire(self):
        forms = (
            ("separate tuples", lambda: zip([
                nested_position(), nested_position_b()])),
            ("one parallel tuple", lambda: zip(
                [nested_position()], [nested_position_b()])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": form(),
                }, comparisons=2)

    def test_iterator_forms_holding_two_nested_mappings_fire(self):
        forms = (
            ("generator", lambda: (
                entry for entry in [
                    nested_position(), nested_position_b()])),
            ("enumerate", lambda: enumerate([
                nested_position(), nested_position_b()])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": form(),
                }, comparisons=2)

    def test_items_and_holdout_positions_list_two_fire(self):
        check_fires(self, lambda: {"holdout": [
            nested_position(), nested_position_b(),
        ]}, comparisons=2)
        check_fires(self, lambda: {"items": [
            {"key": {"inner": {
                "text": HOLDOUT_TEXT, "split": "holdout"}}},
            {"key_b": {"inner": {
                "text": HOLDOUT_TEXT, "split": "holdout"}}},
        ]}, comparisons=2)

    def test_clean_multi_element_wrapped_positions_clear(self):
        check_clears(self, lambda: {"holdout_items": [
            nested_position(), nested_position_b(),
        ]}, comparisons=2)
        check_clears(self, lambda: {"holdout_items": [
            nested_position(), 1,
        ]}, comparisons=1)

    def test_multi_element_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": [
            nested_position(),
        ]})
        check_fires(self, lambda: {"holdout_items": {
            0: nested_position(), 1: nested_position_b(),
        }.items()}, comparisons=2)
        check_clears(self, lambda: {"holdout_items": [1, 2]},
                     comparisons=0)


class ViewOverContainerWrappedPositionTests(unittest.TestCase):
    """Ruling 612: a view holding a container that holds
    a nested mapping fires at the direct act, and the
    same shape fires through the promote wrapper."""

    def test_values_view_holding_list_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            0: [nested_position()],
        }.values()})

    def test_values_view_holding_tuple_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            0: (nested_position(),),
        }.values()})

    def test_items_view_holding_list_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            0: [nested_position()],
        }.items()})

    def test_values_view_holding_deque_and_generator_fire(self):
        forms = (
            ("deque", lambda pos: collections.deque([pos])),
            ("generator", lambda pos: (
                entry for entry in [pos])),
            ("user list", lambda pos: collections.UserList([pos])),
            ("reversed list", lambda pos: reversed([pos])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {
                        0: form(nested_position()),
                    }.values(),
                })

    def test_values_view_holding_view_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            0: {0: nested_position()}.values(),
        }.values()})

    def test_values_view_holding_double_list_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            0: [[nested_position()]],
        }.values()})

    def test_chain_and_proxy_values_view_holding_list_fire(self):
        forms = (
            ("chain map", lambda value: ChainMap(
                {0: value}).values()),
            ("mapping proxy", lambda value: MappingProxyType(
                {0: value}).values()),
            ("ordered dict", lambda value: OrderedDict(
                {0: value}).values()),
            ("user dict", lambda value: UserDict(
                {0: value}).values()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": form([nested_position()]),
                })

    def test_values_view_of_list_through_wrapper_fires(self):
        module = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT},
            ],
            "holdout_items": {
                "holdout_items": {
                    0: [nested_position()],
                }.values(),
            },
        }
        result = module.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(result["fired"])
        self.assertFalse(result["promotion_proceeds"])

    def test_clean_values_view_holding_list_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            0: [nested_position()],
        }.values()})

    def test_view_over_container_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            0: nested_position(),
        }.values()})
        check_fires(self, lambda: {"holdout_items": [
            {0: [nested_position()]}.values(),
        ]})
        check_fires(self, lambda: {"holdout_items": [
            {0: nested_position()}.values(),
        ]})


class ViewInsideContainerSinglePairTests(unittest.TestCase):
    """Ruling 613: a keys view or a values view standing
    inside a list, a tuple, or a mapping value at the
    pairs position fires at the direct act."""

    def test_list_holding_chain_map_keys_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            chain_map_keys_view(),
        ]})

    def test_list_holding_plain_values_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            plain_values_view(),
        ]})

    def test_list_holding_plain_keys_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            plain_keys_view(),
        ]})

    def test_tuple_holding_plain_items_view_fires(self):
        check_fires(self, lambda: {"pairs": (
            plain_items_view(),
        )})

    def test_deque_and_generator_holding_views_fire(self):
        forms = (
            ("deque chain keys", lambda: collections.deque([
                chain_map_keys_view()])),
            ("generator plain values", lambda: (
                entry for entry in [plain_values_view()])),
            ("user list ordered keys", lambda:
                collections.UserList([OrderedDict({
                    HashableItem(CANDIDATE): 1,
                    HashableItem(HOLDOUT_ITEM): 2,
                }).keys()])),
            ("list chain values", lambda: [
                chain_map_values_view()]),
            ("list chain items", lambda: [ChainMap(
                {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
            ).items()]),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "pairs": form(),
                })

    def test_list_holding_list_holding_values_view_fires(self):
        check_fires(self, lambda: {"pairs": [
            [plain_values_view()],
        ]})

    def test_mapping_value_holding_chain_map_keys_view_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": chain_map_keys_view(),
        }})

    def test_mapping_value_holding_plain_keys_view_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": plain_keys_view(),
        }})

    def test_clean_view_inside_container_clears(self):
        check_clears(self, lambda: {"pairs": [
            chain_map_keys_view(),
        ]})
        check_clears(self, lambda: {"pairs": [
            plain_values_view(),
        ]})

    def test_view_inside_container_controls_stand(self):
        check_fires(self, lambda: {"pairs": chain_map_keys_view()})
        check_fires(self, lambda: {"pairs": [
            [dict(CANDIDATE), dict(HOLDOUT_ITEM)],
        ]})
        check_governed_refusal(self, lambda: {"pairs": [
            ChainMap(
                {HashableItem(CANDIDATE): 1},
                {HashableItem(HOLDOUT): 2},
            ).keys(),
        ]})


class SinglePassIterableFormTests(unittest.TestCase):
    """Ruling 614: a general iterable standing listed
    once only is read in full at the direct act and at
    the bundle surfaces, and no second listing raises."""

    def test_once_only_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            OnceOnlyIterable([0, flagged_pair()]),
        ]})

    def test_once_only_index_pair_flagged_items_view(self):
        check_refuses(self, lambda: {"pairs": {
            0: OnceOnlyIterable([0, flagged_pair()]),
        }.items()})

    def test_once_only_index_pair_clean_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            OnceOnlyIterable([0, clean_pair()]),
        ]})

    def test_once_only_index_pair_malformed_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            OnceOnlyIterable([0, malformed_pair()]),
        ]})

    def test_once_only_pairs_value_flagged_refuses(self):
        check_refuses(self, lambda: {
            "pairs": OnceOnlyIterable([flagged_pair()]),
        })

    def test_once_only_pairs_value_direct_fires(self):
        check_fires(self, lambda: {
            "pairs": OnceOnlyIterable([direct_pair()]),
        })

    def test_once_only_pairs_value_direct_clean_clears(self):
        check_clears(self, lambda: {
            "pairs": OnceOnlyIterable([direct_pair()]),
        })

    def test_once_only_index_pair_direct_fires(self):
        check_fires(self, lambda: {"pairs": [
            OnceOnlyIterable([0, direct_pair()]),
        ]})

    def test_single_pass_controls_stand(self):
        check_refuses(self, lambda: {"pairs": [
            ReIterableCarrier([0, flagged_pair()]),
        ]})
        check_refuses(self, lambda: {
            "pairs": ReIterableCarrier([flagged_pair()]),
        })
        check_refuses(self, lambda: {
            "pairs": (entry for entry in [flagged_pair()]),
        })


class MappingKeyCarrierTests(unittest.TestCase):
    """Ruling 615: material standing as a key of a plain
    mapping, at the pairs position or at an outer or
    middle mapping value, fires at the direct act."""

    def test_nested_mapping_key_at_outer_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {HashableItem(inner_mapping()): 1},
        }})

    def test_nested_mapping_key_at_mid_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {"mid": {HashableItem(inner_mapping()): 1}},
        }})

    def test_nested_mapping_key_at_position_itself_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }})

    def test_item_standing_as_key_at_outer_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {HashableItem(HOLDOUT_ITEM): 1},
        }})

    def test_nested_mapping_key_in_carriers_at_outer_fires(self):
        forms = (
            ("list carrier", lambda value: [value]),
            ("deque carrier", lambda value:
                collections.deque([value])),
            ("tuple carrier", lambda value: (value,)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {"key": form(
                        {HashableItem(inner_mapping()): 1})},
                })

    def test_nested_mapping_key_in_mapping_forms_fire(self):
        forms = (
            ("ordered dict", lambda keyed: OrderedDict(keyed)),
            ("user dict", lambda keyed: UserDict(keyed)),
            ("mapping proxy", lambda keyed: MappingProxyType(
                dict(keyed))),
            ("chain map", lambda keyed: ChainMap(dict(keyed))),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {"key": form(
                        {HashableItem(inner_mapping()): 1})},
                })

    def test_pair_sides_standing_as_keys_fire(self):
        forms = (
            ("plain mapping", lambda keyed: dict(keyed)),
            ("ordered dict", lambda keyed: OrderedDict(keyed)),
            ("user dict", lambda keyed: UserDict(keyed)),
            ("mapping proxy", lambda keyed: MappingProxyType(
                dict(keyed))),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "pairs": form({
                        HashableItem(CANDIDATE): 1,
                        HashableItem(HOLDOUT_ITEM): 2,
                    }),
                })

    def test_clean_key_carrier_clears_with_comparison(self):
        check_clears(self, lambda: {"holdout_items": {
            "key": {HashableItem(inner_mapping()): 1},
        }})

    def test_key_carrier_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {HashableItem(inner_mapping()): 1}.keys(),
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": {HashableItem(inner_mapping()): 1}.items(),
        }})
        check_fires(self, lambda: {"pairs": {
            "first": dict(CANDIDATE),
            "second": dict(HOLDOUT_ITEM),
        }})


if __name__ == "__main__":
    unittest.main()
