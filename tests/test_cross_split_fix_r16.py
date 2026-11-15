"""Fix round 16 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r16-triage.md:
ruling 566 (the nested mapping dictionary view carrier
merged defect at the R16-CROSS-1 identity, Low, with
R16-SPAN-1, R16-DAT-1, R16-EVAL-3, R16-UC-1, and Lead
Engineer line E-8 counted in the same act), the direct act
audit_instruction_item reading a bundle position standing
as a mapping whose values carry a nested mapping through
a dictionary view form, through an iterator or view form
standing inside a carrier form, or through a second level
iterator form, for the holdout material the nested mapping
carries, or the governed refusal, at both occasions;
ruling 567 (the wrapped nested mapping position merged
defect at the R16-CROSS-2 identity, Low, with R16-SPAN-3,
R16-EVAL-4, R16-UC-2, and Lead Engineer line E-9 counted
in the same act), the direct act reading a bundle position
standing as a nested mapping where the position itself
stands wrapped in a list, a UserList, a set, a frozenset,
a zip, or an enumerate form, or stands one container
deeper inside a list holding a list, a tuple holding a
tuple, a double tuple, a double deque, or a deque inside
a tuple, for the holdout material the nested mapping
carries, or the governed refusal, at both occasions;
ruling 568 (the enumerate index pair carrier merged defect
at the R16-SPAN-2 identity, Low, with R16-EVAL-1 counted
in the same act), the enumerate stripping reading stripping
an index pair standing in an abstract Sequence form, a
general iterable form, or a set or frozenset form, in list
position and in items view position alike, at the
evaluation call point, at every bundle call point, at
indexed_comparisons, and at the dataset record surface;
and ruling 569 (the ChainMap view single pair merged
defect at the R16-SPAN-4 identity, Low, with R16-EVAL-2
and Lead Engineer line E-7 counted in the same act), the
direct act reading a pairs position value standing as a
single pair in a ChainMap dictionary view form, in each
view form probed, for the pair it carries in the order
the chain carries its sides, or the governed refusal, at
both occasions. dataset.py stands expressly unchanged in
this round.
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


class SequenceCarrier(collections.abc.Sequence):
    """An index pair carrier standing in abstract Sequence form."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)


class IterableCarrier:
    """An index pair carrier standing in general iterable form."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


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


def check_fires(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertTrue(result["fired"])
            test_case.assertEqual(result["comparisons"], 1)


def check_clears_with_comparison(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                CLEAN_TEXT, make_bundle(), occasion=occasion)
            test_case.assertFalse(result["fired"])
            test_case.assertEqual(result["comparisons"], 1)


def pair_items():
    return [dict(CANDIDATE), dict(HOLDOUT_ITEM)]


def flagged_pair():
    return [dict(CANDIDATE), dict(HOLDOUT)]


def clean_pair():
    return [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]


def malformed_pair():
    return [dict(CANDIDATE)]


def inner_mapping():
    return {"inner": {"text": HOLDOUT_TEXT}}


def nested_position():
    return {"key": {"inner": {"text": HOLDOUT_TEXT}}}


def hashable_pair():
    return (HashableItem(CANDIDATE), HashableItem(HOLDOUT))


def hashable_clean_pair():
    return (HashableItem(CANDIDATE), HashableItem(CLEAN_HOLDOUT))


def hashable_malformed_pair():
    return (HashableItem(CANDIDATE),)


class NestedMappingViewCarrierTests(unittest.TestCase):
    """Ruling 566: the direct act reads a bundle position
    standing as a mapping whose values carry a nested mapping
    through a dictionary view form, through an iterator or
    view form standing inside a carrier form, or through a
    second level iterator form."""

    def test_values_view_at_outer_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {0: inner_mapping()}.values(),
        }})

    def test_items_view_at_outer_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {0: inner_mapping()}.items(),
        }})

    def test_keys_view_at_outer_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {HashableItem(inner_mapping()): 1}.keys(),
        }})

    def test_values_view_at_mid_mapping_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {"mid": {0: inner_mapping()}.values()},
        }})

    def test_items_view_at_mid_mapping_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": {"mid": {0: inner_mapping()}.items()},
        }})

    def test_ordered_and_user_dict_view_forms_fire(self):
        forms = (
            ("ordered values view", lambda inner: OrderedDict({
                0: inner}).values()),
            ("ordered items view", lambda inner: OrderedDict({
                0: inner}).items()),
            ("user dict values view", lambda inner: UserDict({
                0: inner}).values()),
            ("user dict items view", lambda inner: UserDict({
                0: inner}).items()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {"key": form(inner_mapping())},
                })

    def test_generator_holding_generator_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": (entry for entry in [
                (inner for inner in [inner_mapping()])]),
        }})

    def test_carrier_holding_generator_fires(self):
        forms = (
            ("deque holding generator", lambda inner:
                collections.deque([
                    (entry for entry in [inner])])),
            ("list holding generator", lambda inner: [
                (entry for entry in [inner])]),
            ("user list holding generator", lambda inner:
                collections.UserList([
                    (entry for entry in [inner])])),
            ("tuple holding generator", lambda inner: (
                (entry for entry in [inner]),)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {"key": form(inner_mapping())},
                })

    def test_second_level_iterator_forms_fire(self):
        forms = (
            ("zip holding zip", lambda inner: zip([
                zip([inner])])),
            ("reversed holding reversed", lambda inner:
                reversed([reversed([inner])])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {"key": form(inner_mapping())},
                })

    def test_carrier_holding_view_fires(self):
        forms = (
            ("deque holding values view", lambda inner:
                collections.deque([{0: inner}.values()])),
            ("list holding values view", lambda inner: [
                {0: inner}.values()]),
            ("list holding items view", lambda inner: [
                {0: inner}.items()]),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {"key": form(inner_mapping())},
                })

    def test_clean_view_and_second_level_carriers_clear(self):
        forms = (
            ("values view", lambda inner: {0: inner}.values()),
            ("items view", lambda inner: {0: inner}.items()),
            ("generator holding generator", lambda inner: (
                entry for entry in [
                    (item for item in [inner])])),
            ("deque holding values view", lambda inner:
                collections.deque([{0: inner}.values()])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_clears_with_comparison(
                    self, lambda form=form: {"holdout_items": {
                        "key": form(inner_mapping()),
                    }})

    def test_carrier_controls_still_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": inner_mapping(),
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": collections.deque([inner_mapping()]),
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": (entry for entry in [inner_mapping()]),
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": collections.UserList([inner_mapping()]),
        }})

    def test_view_carrier_bundle_surfaces_standing_form(self):
        check_governed_refusal(self, lambda: {"holdout_items": {
            "key": {0: inner_mapping()}.values(),
        }})
        check_governed_refusal(self, lambda: {"holdout_items": {
            "key": (entry for entry in [
                (inner for inner in [inner_mapping()])]),
        }})


class WrappedNestedMappingPositionR16Tests(unittest.TestCase):
    """Ruling 567: the direct act reads a bundle position
    standing as a nested mapping where the position itself
    stands wrapped in a list, a UserList, a set, a frozenset,
    a zip, or an enumerate form, or stands one container
    deeper inside such a form."""

    def test_wrapped_position_list_fires(self):
        check_fires(self, lambda: {"holdout_items": [
            nested_position(),
        ]})

    def test_wrapped_position_user_list_fires(self):
        check_fires(self, lambda: {"holdout_items":
            collections.UserList([nested_position()])})

    def test_wrapped_position_set_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(nested_position()),
        }})

    def test_wrapped_position_frozenset_fires(self):
        check_fires(self, lambda: {"holdout_items": frozenset({
            HashableItem(nested_position()),
        })})

    def test_wrapped_position_zip_fires(self):
        check_fires(self, lambda: {"holdout_items": zip([
            nested_position(),
        ])})

    def test_wrapped_position_enumerate_fires(self):
        check_fires(self, lambda: {"holdout_items": enumerate([
            nested_position(),
        ])})

    def test_wrapped_position_double_tuple_fires(self):
        check_fires(self, lambda: {"holdout_items": ((
            nested_position(),
        ),)})

    def test_wrapped_position_double_deque_fires(self):
        check_fires(self, lambda: {"holdout_items":
            collections.deque([
                collections.deque([nested_position()])])})

    def test_wrapped_position_one_container_deeper_fires(self):
        forms = (
            ("list holding list", lambda pos: [[pos]]),
            ("tuple holding tuple", lambda pos: ((pos,),)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": form(nested_position()),
                })

    def test_wrapped_position_deque_inside_tuple_fires(self):
        check_fires(self, lambda: {"holdout_items": (
            collections.deque([nested_position()]),
        )})

    def test_wrapped_position_general_iterable_fires(self):
        check_fires(self, lambda: {"holdout_items":
            IterableCarrier([nested_position()])})

    def test_clean_wrapped_positions_clear(self):
        forms = (
            ("list", lambda pos: [pos]),
            ("user list", lambda pos: collections.UserList([pos])),
            ("zip", lambda pos: zip([pos])),
            ("enumerate", lambda pos: enumerate([pos])),
            ("double tuple", lambda pos: ((pos,),)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_clears_with_comparison(
                    self, lambda form=form: {
                        "holdout_items": form(nested_position()),
                    })

    def test_wrapped_position_controls_still_fire(self):
        check_fires(self, lambda: {"holdout_items":
            nested_position()})
        check_fires(self, lambda: {"holdout_items":
            nested_position().values()})
        check_fires(self, lambda: {"holdout_items":
            nested_position().items()})
        check_fires(self, lambda: {"holdout_items": (
            nested_position(),
        )})
        check_fires(self, lambda: {"holdout_items":
            collections.deque([nested_position()])})
        check_fires(self, lambda: {"holdout_items": (
            entry for entry in [nested_position()])})

    def test_wrapped_position_bundle_surfaces_standing(self):
        forms = (
            ("list", lambda pos: [pos]),
            ("user list", lambda pos: collections.UserList([pos])),
            ("zip", lambda pos: zip([pos])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_proceeds(self, lambda form=form: {
                    "holdout_items": form(nested_position()),
                })


class EnumerateIndexPairCarrierR16Tests(unittest.TestCase):
    """Ruling 568: an enumerate index pair presented at pair
    level in an abstract Sequence form, a general iterable
    form, or a set or frozenset form stands stripped at
    every bundle surface."""

    def test_sequence_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            SequenceCarrier([0, flagged_pair()]),
        ]})

    def test_sequence_index_pair_flagged_items_view(self):
        check_refuses(self, lambda: {"pairs": {
            0: SequenceCarrier([0, flagged_pair()]),
        }.items()})

    def test_iterable_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            IterableCarrier([0, flagged_pair()]),
        ]})

    def test_iterable_index_pair_flagged_items_view(self):
        check_refuses(self, lambda: {"pairs": {
            0: IterableCarrier([0, flagged_pair()]),
        }.items()})

    def test_set_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            {0, hashable_pair()},
        ]})

    def test_frozenset_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            frozenset({0, hashable_pair()}),
        ]})

    def test_set_index_pair_flagged_items_view(self):
        forms = (
            ("set", lambda pair: {0, pair}),
            ("frozenset", lambda pair: frozenset({0, pair})),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_refuses(self, lambda form=form: {"pairs": {
                    0: form(hashable_pair()),
                }.items()})

    def test_clean_sequence_index_pair_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            SequenceCarrier([0, clean_pair()]),
        ]})
        check_proceeds(self, lambda: {"pairs": {
            0: SequenceCarrier([0, clean_pair()]),
        }.items()})

    def test_clean_iterable_index_pair_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            IterableCarrier([0, clean_pair()]),
        ]})
        check_proceeds(self, lambda: {"pairs": {
            0: IterableCarrier([0, clean_pair()]),
        }.items()})

    def test_clean_set_index_pair_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            {0, hashable_clean_pair()},
        ]})

    def test_malformed_sequence_index_pair_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            SequenceCarrier([0, malformed_pair()]),
        ]})
        check_governed_refusal(self, lambda: {"pairs": {
            0: SequenceCarrier([0, malformed_pair()]),
        }.items()})

    def test_malformed_iterable_index_pair_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            IterableCarrier([0, malformed_pair()]),
        ]})
        check_governed_refusal(self, lambda: {"pairs": {
            0: IterableCarrier([0, malformed_pair()]),
        }.items()})

    def test_malformed_set_index_pair_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            {0, hashable_malformed_pair()},
        ]})
        check_governed_refusal(self, lambda: {"pairs": [
            frozenset({0, hashable_malformed_pair()}),
        ]})

    def test_index_pair_controls_still_decide(self):
        check_refuses(self, lambda: {"pairs": [
            [0, flagged_pair()],
        ]})
        check_refuses(self, lambda: {"pairs": [
            (0, flagged_pair()),
        ]})
        check_refuses(self, lambda: {"pairs": [
            collections.deque([0, flagged_pair()]),
        ]})
        check_refuses(self, lambda: {"pairs": enumerate([
            flagged_pair(),
        ])})
        check_proceeds(self, lambda: {"pairs": [
            [0, clean_pair()],
        ]})
        check_governed_refusal(self, lambda: {"pairs": {
            0: (0, malformed_pair()),
        }.items()})


class ChainMapViewSinglePairTests(unittest.TestCase):
    """Ruling 569: the direct act reads a pairs position value
    standing as a single pair in a ChainMap dictionary view
    form, for the pair it carries in the order the chain
    carries its sides."""

    def test_chain_map_keys_view_split_maps_fires(self):
        check_fires(self, lambda: {"pairs": ChainMap(
            {HashableItem(CANDIDATE): 1},
            {HashableItem(HOLDOUT_ITEM): 2},
        ).keys()})

    def test_chain_map_values_view_split_maps_fires(self):
        check_fires(self, lambda: {"pairs": ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
        ).values()})

    def test_chain_map_items_view_split_maps_fires(self):
        check_fires(self, lambda: {"pairs": ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
        ).items()})

    def test_clean_chain_map_views_clear_with_comparison(self):
        forms = (
            ("keys view", lambda items: ChainMap(
                {HashableItem(items[0]): 1},
                {HashableItem(items[1]): 2},
            ).keys()),
            ("values view", lambda items: ChainMap(
                {0: items[0]}, {1: items[1]},
            ).values()),
            ("items view", lambda items: ChainMap(
                {0: items[0]}, {1: items[1]},
            ).items()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_clears_with_comparison(
                    self, lambda form=form: {
                        "pairs": form(pair_items()),
                    })

    def test_chain_map_view_controls_still_fire(self):
        check_fires(self, lambda: {"pairs": {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }.keys()})
        check_fires(self, lambda: {"pairs": OrderedDict({
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }).keys()})
        check_fires(self, lambda: {"pairs": UserDict({
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }).keys()})
        check_fires(self, lambda: {"pairs": ChainMap({
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }).keys()})
        check_fires(self, lambda: {"pairs": ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
        )})

    def test_chain_map_view_bundle_surfaces_standing(self):
        check_governed_refusal(self, lambda: {"pairs": ChainMap(
            {HashableItem(CANDIDATE): 1},
            {HashableItem(HOLDOUT): 2},
        ).keys()})


if __name__ == "__main__":
    unittest.main()
