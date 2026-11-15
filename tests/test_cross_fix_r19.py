"""Fix round 19 tests for Region 2: cross split.

Charges pinned here, from design/steps/step-15-r19-triage.md:
ruling 721 (the cross split audit single pass iterable
inside a zip inside a list or tuple defect at the bundle
surfaces, merged at the R19-CROSS-1 identity, Low, with
R19-UC-1 counted in the same act), the bundle surfaces
reaching a single pass iterable standing inside a zip
object standing inside a list or a tuple at the pairs
position; ruling 722 (the single pass iterable standing
as a plain mapping value defect at the R19-EVAL-1
identity, Low), the direct act mapping value reading
reaching a single pass iterable standing as the value
of a plain mapping; ruling 723 (the container wrapped
mapping key carrier defect at the R19-EVAL-2 identity,
Low), the direct act extra holdout reading reaching a
nested mapping standing as a key wrapped in a tuple or
a frozenset; ruling 724 (the container formed key
defect at the Lead Engineer E-7 identity, Low), the
direct act key carrier reading reaching material
standing as a container formed key; and ruling 725
(the ChainMap map order defect at the R19-DAT-1
identity, Low), the shared materialisation reading
carrying a ChainMap in the order of its maps so the
dataset instruction item surface decides the
presentation as the direct act decides it.
dataset.py stands expressly unchanged in this round,
and tests/test_unrowed_c.py stands held whole and
unchanged, with no pin of this region filed in it.
"""

import collections
import unittest
from collections import ChainMap, OrderedDict

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


def flagged_pair():
    return [dict(CANDIDATE), dict(HOLDOUT)]


def clean_pair():
    return [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]


def malformed_pair():
    return [dict(CANDIDATE)]


def direct_pair():
    return [dict(CANDIDATE), dict(HOLDOUT_ITEM)]


def inner_mapping():
    return {"inner": {"text": HOLDOUT_TEXT}}


def tuple_pair_key():
    return (HashableItem(CANDIDATE), HashableItem(HOLDOUT_ITEM))


class ZipNestedSinglePassTests(unittest.TestCase):
    """Ruling 721: a single pass iterable standing as an
    enumerate index pair or as a plain pair inside a zip
    object standing inside a list or a tuple at the pairs
    position refuses at every bundle surface."""

    def test_zip_in_list_index_pair_flagged_refuses(self):
        check_refuses(self, lambda: {"pairs": [
            zip([OnceOnlyIterable([0, flagged_pair()])]),
        ]})

    def test_zip_in_tuple_index_pair_flagged_refuses(self):
        check_refuses(self, lambda: {"pairs": (
            zip([OnceOnlyIterable([0, flagged_pair()])]),
        )})

    def test_zip_in_list_plain_pair_flagged_refuses(self):
        check_refuses(self, lambda: {"pairs": [
            zip([OnceOnlyIterable(flagged_pair())]),
        ]})

    def test_list_in_zip_in_list_index_pair_flagged_refuses(self):
        check_refuses(self, lambda: {"pairs": [
            zip([[OnceOnlyIterable([0, flagged_pair()])]]),
        ]})

    def test_zip_in_list_clean_pair_proceeds(self):
        check_proceeds(self, lambda: {"pairs": [
            zip([OnceOnlyIterable([0, clean_pair()])]),
        ]})

    def test_zip_in_list_malformed_pair_governed_refusal(self):
        check_governed_refusal(self, lambda: {"pairs": [
            zip([OnceOnlyIterable([0, malformed_pair()])]),
        ]})

    def test_zip_nested_controls_stand(self):
        check_refuses(self, lambda: {"pairs": [
            [OnceOnlyIterable([0, flagged_pair()])],
        ]})
        check_refuses(self, lambda: {"pairs":
            zip([OnceOnlyIterable([0, flagged_pair()])]),
        })
        check_fires(self, lambda: {"pairs": [
            zip([OnceOnlyIterable([0, direct_pair()])]),
        ]})


class SinglePassMappingValueTests(unittest.TestCase):
    """Ruling 722: a single pass iterable holding a plain
    pair or an enumerate index pair, standing as the value
    of a plain mapping, fires at the direct act."""

    def test_mapping_value_plain_pair_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": OnceOnlyIterable(direct_pair()),
        }})

    def test_mapping_value_index_pair_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": OnceOnlyIterable([0, direct_pair()]),
        }})

    def test_mapping_value_at_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "key": OnceOnlyIterable([
                dict(HOLDOUT_ITEM), dict(HOLDOUT_ITEM)]),
        }}, comparisons=2)

    def test_mapping_value_at_holdout_fires(self):
        check_fires(self, lambda: {"holdout": {
            "key": OnceOnlyIterable([
                dict(HOLDOUT_ITEM), dict(HOLDOUT_ITEM)]),
        }}, comparisons=2)

    def test_mapping_value_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            "key": OnceOnlyIterable(direct_pair()),
        }})

    def test_mapping_value_two_deep_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {"key": OnceOnlyIterable(direct_pair())},
        }})

    def test_mapping_value_inside_list_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": [OnceOnlyIterable(direct_pair())],
        }})

    def test_mapping_value_clean_clears_with_comparison(self):
        check_clears(self, lambda: {"pairs": {
            "key": OnceOnlyIterable(direct_pair()),
        }})

    def test_mapping_value_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            "key": direct_pair(),
        }})
        check_fires(self, lambda: {"pairs": {
            "key": (entry for entry in direct_pair()),
        }})
        check_fires(self, lambda: {"pairs": {
            "key": OnceOnlyIterable(direct_pair()),
        }.items()})
        check_fires(self, lambda: {"pairs": {
            "key": OnceOnlyIterable(direct_pair()),
        }.values()})


class WrappedMappingKeyTests(unittest.TestCase):
    """Ruling 723: a nested mapping standing as a key
    wrapped in a one element tuple, standing at the
    holdout_items position, fires at the direct act."""

    def test_tuple_wrapped_key_at_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()),): 1,
        }})

    def test_two_element_tuple_wrapped_key_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()), "second"): 1,
        }})

    def test_frozenset_wrapped_key_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            frozenset([HashableItem(inner_mapping())]): 1,
        }})

    def test_tuple_wrapped_key_at_outer_mapping_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "outer": {(HashableItem(inner_mapping()),): 1},
        }})

    def test_tuple_wrapped_key_inside_list_carrier_fires(self):
        check_fires(self, lambda: {"holdout_items": [
            {(HashableItem(inner_mapping()),): 1},
        ]})

    def test_tuple_wrapped_key_items_view_form_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()),): 1,
        }.items()})

    def test_wrapped_key_clean_clears_with_comparison(self):
        check_clears(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()),): 1,
        }})

    def test_wrapped_key_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()),): 1,
        }.keys()})


class ContainerFormedKeyTests(unittest.TestCase):
    """Ruling 724: holdout material standing as a container
    formed key of a mapping presented directly, and
    standing as an entry key of an items view at the pairs
    position, fires at the direct act."""

    def test_single_pass_key_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            OnceOnlyIterable(direct_pair()): 1,
        }})

    def test_single_pass_key_at_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            OnceOnlyIterable(direct_pair()): 1,
        }})

    def test_single_pass_key_at_holdout_fires(self):
        check_fires(self, lambda: {"holdout": {
            OnceOnlyIterable(direct_pair()): 1,
        }})

    def test_single_pass_key_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            OnceOnlyIterable(direct_pair()): 1,
        }})

    def test_tuple_pair_key_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }})

    def test_tuple_pair_key_at_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }})

    def test_frozenset_pair_key_at_pairs_fires(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": {
                        frozenset(tuple_pair_key()): 1,
                    }},
                    occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 2)

    def test_tuple_pair_key_inside_list_at_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": [
            {tuple_pair_key(): 1},
        ]})

    def test_tuple_pair_key_at_mapping_value_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "outer": {tuple_pair_key(): 1},
        }})

    def test_tuple_pair_key_items_view_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }.items()})

    def test_single_pass_key_items_view_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            OnceOnlyIterable(direct_pair()): 1,
        }.items()})

    def test_nested_mapping_key_items_view_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            HashableItem(inner_mapping()): 1,
        }.items()})

    def test_container_key_clean_clears_with_comparison(self):
        check_clears(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }})

    def test_container_key_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            HashableItem(inner_mapping()): 1,
        }.items()})
        check_governed_refusal(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }})


def chain_map_pair():
    return ChainMap(
        {HashableItem(CANDIDATE): 1},
        {HashableItem(HOLDOUT_ITEM): 2},
    )


def dataset_bundle(text, make_pairs):
    return {
        "instruction_items": [{"text": text}],
        "holdout_items": {"pairs": make_pairs()},
    }


def check_dataset_fires(test_case, make_pairs):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(HOLDOUT_TEXT, make_pairs),
                occasion=occasion)
            test_case.assertTrue(result["fired"])
            shared = result["cross_split_audit_result"]
            test_case.assertEqual(shared["comparisons"], 1)


def check_dataset_not_candidate(test_case, make_pairs):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(CANDIDATE_TEXT, make_pairs),
                occasion=occasion)
            test_case.assertFalse(result["fired"])


class ChainMapDatasetOrderTests(unittest.TestCase):
    """Ruling 725: a ChainMap whose two maps carry the
    candidate item and the holdout item as their keys,
    standing at the pairs position, keeps its map order
    at the dataset instruction item surface."""

    def test_materialised_chain_map_keeps_map_order(self):
        module = harness.require("ontoloop.cross_split_audit")
        candidate_key = HashableItem(CANDIDATE)
        holdout_key = HashableItem(HOLDOUT_ITEM)
        materialised = module._materialise_iterators(
            {"pairs": ChainMap(
                {candidate_key: 1}, {holdout_key: 2})})
        keys = list(materialised["pairs"].keys())
        self.assertEqual(keys, [candidate_key, holdout_key])

    def test_chain_map_at_pairs_dataset_fires_on_verbatim(self):
        check_dataset_fires(self, chain_map_pair)

    def test_chain_map_at_pairs_dataset_not_on_candidate(self):
        check_dataset_not_candidate(self, chain_map_pair)

    def test_chain_map_inside_list_dataset_fires(self):
        check_dataset_fires(self, lambda: [chain_map_pair()])
        check_dataset_not_candidate(self, lambda: [chain_map_pair()])

    def test_chain_map_inside_deque_dataset_fires(self):
        check_dataset_fires(
            self, lambda: collections.deque([chain_map_pair()]))
        check_dataset_not_candidate(
            self, lambda: collections.deque([chain_map_pair()]))

    def test_three_map_chain_map_dataset_fires(self):
        def make():
            return ChainMap(
                {HashableItem(CANDIDATE): 1},
                {HashableItem(HOLDOUT_ITEM): 2},
                {},
            )
        check_dataset_fires(self, make)
        check_dataset_not_candidate(self, make)

    def test_chain_map_three_containers_deep_dataset_fires(self):
        check_dataset_fires(self, lambda: [[[chain_map_pair()]]])
        check_dataset_not_candidate(
            self, lambda: [[[chain_map_pair()]]])

    def test_chain_map_at_mapping_value_dataset_fires(self):
        check_dataset_fires(self, lambda: {"key": chain_map_pair()})
        check_dataset_not_candidate(
            self, lambda: {"key": chain_map_pair()})

    def test_chain_map_dataset_clean_clears(self):
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    dataset_bundle(CLEAN_TEXT, chain_map_pair),
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_chain_map_dataset_controls_stand(self):
        check_fires(self, lambda: {"pairs": chain_map_pair()})
        check_dataset_fires(self, lambda: {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        })
        check_dataset_fires(self, lambda: OrderedDict([
            (HashableItem(CANDIDATE), 1),
            (HashableItem(HOLDOUT_ITEM), 2),
        ]))


if __name__ == "__main__":
    unittest.main()
