"""Fix round 15 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r15-triage.md:
ruling 524 (the keys view single pair merged defect at the
R15-CROSS-1 identity, Low, with R15-SPAN-1, R15-DAT-1, and
R15-EVAL-2 counted in the same act), the direct act
audit_instruction_item reading a pairs position value
standing as a single pair in dictionary keys view form, in
each mapping form probed, for the pair it carries, or the
governed refusal, at both occasions; ruling 525 (the nested
mapping carrier merged defect at the R15-CROSS-2 identity,
Low, with R15-SPAN-2 and R15-DAT-2 counted in the same act),
the direct act reading a bundle position standing as a
mapping whose values carry a nested mapping through a
container or iterator form, for the holdout material the
nested mapping carries, or the governed refusal, at both
occasions; ruling 526 (R15-EVAL-1, Low), the enumerate
stripping reading stripping an index pair standing in each
container and iterator carrier form probed, in list position
and in items view position alike, at the evaluation call
point, at every bundle call point, at indexed_comparisons,
and at the dataset record surface; ruling 527 (Lead Engineer
line E-7, Low), the direct act reading a pairs position
value standing as a single pair in mapping form, in each
mapping form probed, for the pair it carries, or the
governed refusal form of the direct act surface, at both
occasions; and ruling 528 (Lead Engineer line E-8, Low), the
direct act reading a bundle position standing as a nested
mapping where the position itself stands wrapped in a
values view, an items view, a tuple, a deque, or a generator
form, for the holdout material the nested mapping carries,
or the governed refusal, at both occasions. dataset.py
stands expressly unchanged in this round.
"""

import collections
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


class KeysViewSinglePairTests(unittest.TestCase):
    """Ruling 524: the direct act reads a pairs position value
    standing as a single pair in dictionary keys view form."""

    def test_keys_view_plain_dictionary_fires(self):
        check_fires(self, lambda: {"pairs": {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }.keys()})

    def test_keys_view_ordered_dict_fires(self):
        check_fires(self, lambda: {"pairs": OrderedDict({
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }).keys()})

    def test_keys_view_user_dict_fires(self):
        check_fires(self, lambda: {"pairs": UserDict({
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }).keys()})

    def test_keys_view_clean_clears_with_a_comparison(self):
        forms = (
            ("plain dictionary", lambda items: {
                HashableItem(items[0]): 1,
                HashableItem(items[1]): 2,
            }.keys()),
            ("ordered dict", lambda items: OrderedDict({
                HashableItem(items[0]): 1,
                HashableItem(items[1]): 2,
            }).keys()),
            ("user dict", lambda items: UserDict({
                HashableItem(items[0]): 1,
                HashableItem(items[1]): 2,
            }).keys()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_clears_with_comparison(
                    self, lambda form=form: {
                        "pairs": form(pair_items()),
                    })

    def test_keys_view_controls_still_fire(self):
        forms = (
            ("list", lambda items: list(items)),
            ("tuple", lambda items: tuple(items)),
            ("deque", lambda items: collections.deque(items)),
            ("user list", lambda items: collections.UserList(items)),
            ("zip", lambda items: zip([items[0]], [items[1]])),
            ("values view", lambda items: {
                0: items[0], 1: items[1]}.values()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "pairs": form(pair_items()),
                })

    def test_keys_view_bundle_surfaces_standing_form(self):
        check_governed_refusal(self, lambda: {"pairs": {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT): 2,
        }.keys()})


class NestedMappingCarrierTests(unittest.TestCase):
    """Ruling 525: the direct act reads a bundle position
    standing as a mapping whose values carry a nested mapping
    through a container or iterator form."""

    def test_nested_mapping_in_deque_carrier_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": collections.deque([inner_mapping()]),
        }})

    def test_nested_mapping_in_user_list_carrier_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": collections.UserList([inner_mapping()]),
        }})

    def test_nested_mapping_in_list_holding_list_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": [[inner_mapping()]],
        }})

    def test_nested_mapping_in_generator_carrier_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": (entry for entry in [inner_mapping()]),
        }})

    def test_nested_mapping_carried_at_mid_mapping_fires(self):
        forms = (
            ("deque", lambda inner: collections.deque([inner])),
            ("user list", lambda inner: collections.UserList([inner])),
            ("list holding list", lambda inner: [[inner]]),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "holdout_items": {
                        "key": {"mid": form(inner_mapping())},
                    },
                })

    def test_clean_nested_mapping_carriers_clear(self):
        forms = (
            ("deque", lambda inner: collections.deque([inner])),
            ("user list", lambda inner: collections.UserList([inner])),
            ("list holding list", lambda inner: [[inner]]),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_clears_with_comparison(
                    self, lambda form=form: {"holdout_items": {
                        "key": form(inner_mapping()),
                    }})

    def test_nested_mapping_controls_still_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": inner_mapping(),
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": [inner_mapping()],
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": (inner_mapping(),),
        }})
        check_fires(self, lambda: {
            "holdout_items": {"key": {"text": HOLDOUT_TEXT}},
        })

    def test_carrier_bundle_surfaces_standing_form(self):
        check_governed_refusal(self, lambda: {"holdout_items": {
            "key": collections.deque([inner_mapping()]),
        }})


class EnumerateIndexPairCarrierTests(unittest.TestCase):
    """Ruling 526: an enumerate index pair presented at pair
    level in a container form other than list or tuple stands
    stripped at every bundle surface."""

    def test_deque_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            collections.deque([0, flagged_pair()]),
        ]})

    def test_user_list_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            collections.UserList([0, flagged_pair()]),
        ]})

    def test_generator_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            (entry for entry in [(0, flagged_pair())]),
        ]})

    def test_map_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            map(lambda entry: entry, [(0, flagged_pair())]),
        ]})

    def test_list_iterator_index_pair_flagged_list_position(self):
        check_refuses(self, lambda: {"pairs": [
            iter([(0, flagged_pair())]),
        ]})

    def test_deque_index_pair_flagged_items_view_position(self):
        check_refuses(self, lambda: {"pairs": {
            0: collections.deque([0, flagged_pair()]),
        }.items()})

    def test_user_list_index_pair_flagged_items_view_position(self):
        check_refuses(self, lambda: {"pairs": {
            0: collections.UserList([0, flagged_pair()]),
        }.items()})

    def test_generator_index_pair_flagged_items_view_position(self):
        check_refuses(self, lambda: {"pairs": {
            0: (entry for entry in [(0, flagged_pair())]),
        }.items()})

    def test_clean_deque_index_pair_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            collections.deque([0, clean_pair()]),
        ]})
        check_proceeds(self, lambda: {"pairs": {
            0: collections.deque([0, clean_pair()]),
        }.items()})

    def test_clean_generator_index_pair_proceeds_items_view(self):
        check_proceeds(self, lambda: {"pairs": {
            0: (entry for entry in [(0, clean_pair())]),
        }.items()})

    def test_malformed_deque_index_pair_refuses_items_view(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: collections.deque([0, malformed_pair()]),
        }.items()})

    def test_malformed_user_list_index_pair_refuses_items_view(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: collections.UserList([0, malformed_pair()]),
        }.items()})

    def test_malformed_generator_index_pair_refuses_items_view(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: (entry for entry in [(0, malformed_pair())]),
        }.items()})

    def test_malformed_deque_index_pair_refuses_list_position(self):
        check_governed_refusal(self, lambda: {"pairs": [
            collections.deque([0, malformed_pair()]),
        ]})

    def test_index_pair_controls_still_decide(self):
        check_refuses(self, lambda: {"pairs": [
            [0, flagged_pair()],
        ]})
        check_refuses(self, lambda: {"pairs": [
            (0, flagged_pair()),
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


class SinglePairMappingFormTests(unittest.TestCase):
    """Ruling 527: the direct act reads a pairs position value
    standing as a single pair in mapping form."""

    def test_single_pair_plain_dictionary_index_form_fires(self):
        check_fires(self, lambda: {"pairs": {
            0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM),
        }})

    def test_single_pair_mapping_proxy_fires(self):
        check_fires(self, lambda: {"pairs": MappingProxyType({
            0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM),
        })})

    def test_single_pair_user_dict_fires(self):
        check_fires(self, lambda: {"pairs": UserDict({
            0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM),
        })})

    def test_single_pair_ordered_dict_fires(self):
        check_fires(self, lambda: {"pairs": OrderedDict({
            0: dict(CANDIDATE), 1: dict(HOLDOUT_ITEM),
        })})

    def test_single_pair_chain_map_fires(self):
        check_fires(self, lambda: {"pairs": ChainMap(
            {0: dict(CANDIDATE)}, {1: dict(HOLDOUT_ITEM)},
        )})

    def test_single_pair_plain_dictionary_name_form_fires(self):
        check_fires(self, lambda: {"pairs": {
            "left": dict(CANDIDATE), "right": dict(HOLDOUT_ITEM),
        }})

    def test_clean_single_pair_mapping_forms_clear(self):
        forms = (
            ("plain dictionary", lambda items: {
                0: items[0], 1: items[1]}),
            ("chain map", lambda items: ChainMap(
                {0: items[0]}, {1: items[1]})),
            ("user dict", lambda items: UserDict({
                0: items[0], 1: items[1]})),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_clears_with_comparison(
                    self, lambda form=form: {
                        "pairs": form(pair_items()),
                    })

    def test_single_pair_mapping_controls_still_fire(self):
        forms = (
            ("list", lambda items: list(items)),
            ("tuple", lambda items: tuple(items)),
            ("enumerate", lambda items: enumerate(items)),
            ("generator", lambda items: (
                side for side in items)),
            ("values view", lambda items: {
                0: items[0], 1: items[1]}.values()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "pairs": form(pair_items()),
                })
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(form="set", occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": {
                        HashableItem(CANDIDATE),
                        HashableItem(HOLDOUT_ITEM),
                    }},
                    occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 2)

    def test_single_pair_mapping_bundle_surfaces_standing(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: dict(CANDIDATE), 1: dict(HOLDOUT),
        }})


class WrappedNestedMappingPositionTests(unittest.TestCase):
    """Ruling 528: the direct act reads a bundle position
    standing as a nested mapping where the position itself
    stands wrapped in a view, sequence, or iterator form."""

    def test_wrapped_position_values_view_fires(self):
        check_fires(self, lambda: {"holdout_items":
            nested_position().values()})

    def test_wrapped_position_items_view_fires(self):
        check_fires(self, lambda: {"holdout_items":
            nested_position().items()})

    def test_wrapped_position_tuple_fires(self):
        check_fires(self, lambda: {"holdout_items": (
            nested_position(),
        )})

    def test_wrapped_position_deque_fires(self):
        check_fires(self, lambda: {"holdout_items":
            collections.deque([nested_position()])})

    def test_wrapped_position_generator_fires(self):
        check_fires(self, lambda: {"holdout_items": (
            entry for entry in [nested_position()])})

    def test_clean_wrapped_positions_clear(self):
        forms = (
            ("values view", lambda pos: pos.values()),
            ("items view", lambda pos: pos.items()),
            ("tuple", lambda pos: (pos,)),
            ("deque", lambda pos: collections.deque([pos])),
            ("generator", lambda pos: (
                entry for entry in [pos])),
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
            MappingProxyType(nested_position())})
        check_fires(self, lambda: {"holdout_items": {
            "key": MappingProxyType(
                {"inner": {"text": HOLDOUT_TEXT}}),
        }})
        check_fires(self, lambda: {"holdout_items":
            UserDict(nested_position())})
        check_fires(self, lambda: {"holdout_items":
            ChainMap(nested_position())})
        check_fires(self, lambda: {"holdout_items": {
            "a": {"b": {"c": {"text": HOLDOUT_TEXT}}},
        }})

    def test_ruling_525_carrier_forms_decide_as_charged(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": collections.deque([inner_mapping()]),
        }})
        check_fires(self, lambda: {"holdout_items": {
            "key": collections.UserList([inner_mapping()]),
        }})

    def test_wrapped_position_bundle_surfaces_standing(self):
        forms = (
            ("values view", lambda pos: pos.values()),
            ("items view", lambda pos: pos.items()),
            ("tuple", lambda pos: (pos,)),
            ("deque", lambda pos: collections.deque([pos])),
            ("generator", lambda pos: (
                entry for entry in [pos])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_proceeds(self, lambda form=form: {
                    "holdout_items": form(nested_position()),
                })


if __name__ == "__main__":
    unittest.main()
