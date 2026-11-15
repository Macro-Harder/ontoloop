"""Fix round 20 tests for Region 2: cross split.

Charges pinned here, from design/steps/step-15-r20-triage.md:
ruling 779 (the dataset instruction item surface ChainMap
dictionary view pair presentation defect at the R20-DAT-1
identity, Low), the shared materialisation reading carrying
a dictionary view standing over a ChainMap in the order of
its maps; ruling 780 (the cross split audit key carrier
standing as a key of a mapping at a mapping value of the
pairs position defect at the R20-EVAL-1 identity, Low), the
direct act mapping value reading reaching a key carrier at
that value; ruling 781 (the cross split audit single pass
iterable inside a list or tuple inside a plain iterator at
the bundle surfaces defect at the R20-UC-1 identity, Low),
the bundle surface reading reaching a single pass iterable
in that arrangement; ruling 782 (the cross split audit
wrapped nested mapping key at the items position defect at
the Lead Engineer E-17 identity, Low), the wrapped key
reading of ruling 723 extending to the items position; and
ruling 783 (the cross split audit tuple pair key presented
through a values view defect at the Lead Engineer E-18
identity, Low), the key carrier reading of ruling 724
extending to a key presented through the values view of its
mapping at the direct act and at the bundle surfaces alike.
dataset.py stands expressly unchanged in this round, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import collections
import unittest
from collections import ChainMap, OrderedDict
from collections.abc import Sequence

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


class SequenceCarrier(Sequence):
    """An abstract Sequence form carrying its elements."""

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


def check_refuses(test_case, make_bundle, comparisons=1):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], comparisons)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], comparisons)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertTrue(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], comparisons)


def check_proceeds(test_case, make_bundle, comparisons=0):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertFalse(result["candidate_bundle_refused"])
            test_case.assertTrue(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], comparisons)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], comparisons)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertFalse(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], comparisons)


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


def clean_bundle_pair():
    return [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]


def malformed_pair():
    return [dict(CANDIDATE)]


def direct_pair():
    return [dict(CANDIDATE), dict(HOLDOUT_ITEM)]


def inner_mapping():
    return {"inner": {"text": HOLDOUT_TEXT}}


def tuple_pair_key():
    return (HashableItem(CANDIDATE), HashableItem(HOLDOUT_ITEM))


def bundle_tuple_pair_key():
    return (HashableItem(CANDIDATE), HashableItem(HOLDOUT))


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


def check_dataset_pair(test_case, make_pairs):
    check_dataset_fires(test_case, make_pairs)
    check_dataset_not_candidate(test_case, make_pairs)


def chain_map_keys_view():
    return ChainMap(
        {HashableItem(CANDIDATE): 1},
        {HashableItem(HOLDOUT_ITEM): 2},
    ).keys()


def chain_map_values_view():
    return ChainMap(
        {"first": HashableItem(CANDIDATE)},
        {"second": HashableItem(HOLDOUT_ITEM)},
    ).values()


class ChainMapViewDatasetOrderTests(unittest.TestCase):
    """Ruling 779: a dictionary view standing over a ChainMap
    at the pairs position keeps the order of its maps at the
    dataset instruction item surface, as the direct act
    decides the view itself."""

    def test_materialised_keys_view_keeps_map_order(self):
        module = harness.require("ontoloop.cross_split_audit")
        candidate_key = HashableItem(CANDIDATE)
        holdout_key = HashableItem(HOLDOUT_ITEM)
        materialised = module._materialise_iterators(
            {"pairs": ChainMap(
                {candidate_key: 1}, {holdout_key: 2}).keys()})
        self.assertEqual(
            materialised["pairs"], [candidate_key, holdout_key])

    def test_materialised_values_view_keeps_map_order(self):
        module = harness.require("ontoloop.cross_split_audit")
        candidate_item = HashableItem(CANDIDATE)
        holdout_item = HashableItem(HOLDOUT_ITEM)
        materialised = module._materialise_iterators(
            {"pairs": ChainMap(
                {"first": candidate_item},
                {"second": holdout_item}).values()})
        self.assertEqual(
            materialised["pairs"], [candidate_item, holdout_item])

    def test_keys_view_at_pairs_dataset_decides_in_map_order(self):
        check_dataset_pair(self, chain_map_keys_view)

    def test_values_view_at_pairs_dataset_decides_in_map_order(self):
        check_dataset_pair(self, chain_map_values_view)

    def test_keys_view_inside_list_dataset_fires(self):
        check_dataset_pair(self, lambda: [chain_map_keys_view()])

    def test_values_view_inside_list_dataset_fires(self):
        check_dataset_pair(self, lambda: [chain_map_values_view()])

    def test_keys_view_inside_deque_dataset_fires(self):
        check_dataset_pair(
            self, lambda: collections.deque([chain_map_keys_view()]))

    def test_keys_view_at_mapping_value_dataset_fires(self):
        check_dataset_pair(
            self, lambda: {"key": chain_map_keys_view()})

    def test_keys_view_three_containers_deep_dataset_fires(self):
        check_dataset_pair(self, lambda: [[[chain_map_keys_view()]]])

    def test_keys_view_inside_zip_dataset_fires(self):
        check_dataset_pair(
            self, lambda: zip([chain_map_keys_view()]))

    def test_keys_view_through_generator_dataset_fires(self):
        check_dataset_pair(
            self, lambda: (view for view in [chain_map_keys_view()]))

    def test_three_map_keys_view_dataset_fires(self):
        def make():
            return ChainMap(
                {HashableItem(CANDIDATE): 1},
                {},
                {HashableItem(HOLDOUT_ITEM): 2},
            ).keys()
        check_dataset_pair(self, make)

    def test_keys_view_ordered_dict_maps_dataset_fires(self):
        def make():
            return ChainMap(
                OrderedDict([(HashableItem(CANDIDATE), 1)]),
                OrderedDict([(HashableItem(HOLDOUT_ITEM), 2)]),
            ).keys()
        check_dataset_pair(self, make)

    def test_chain_map_view_dataset_clean_clears(self):
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    dataset_bundle(CLEAN_TEXT, chain_map_keys_view),
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_chain_map_view_controls_stand(self):
        check_fires(self, lambda: {"pairs": chain_map_keys_view()})
        check_fires(self, lambda: {"pairs": chain_map_values_view()})
        check_dataset_pair(self, lambda: ChainMap(
            {HashableItem(CANDIDATE): 1},
            {HashableItem(HOLDOUT_ITEM): 2},
        ))
        check_dataset_pair(self, lambda: {
            HashableItem(CANDIDATE): 1,
            HashableItem(HOLDOUT_ITEM): 2,
        }.keys())
        check_dataset_pair(self, lambda: ChainMap(
            {
                HashableItem(CANDIDATE): 1,
                HashableItem(HOLDOUT_ITEM): 2,
            },
        ).keys())


class KeyCarrierMappingValuePairsTests(unittest.TestCase):
    """Ruling 780: a key carrier standing as a key of a mapping
    standing at a mapping value of the pairs position fires
    at the direct act."""

    def test_tuple_pair_key_at_mapping_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {tuple_pair_key(): 1},
        }})

    def test_single_pass_key_at_mapping_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {OnceOnlyIterable(direct_pair()): 1},
        }})

    def test_frozenset_pair_key_at_mapping_value_fires(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"pairs": {
                        "outer": {frozenset(tuple_pair_key()): 1},
                    }},
                    occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertGreaterEqual(result["comparisons"], 1)

    def test_wrapped_nested_key_at_mapping_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {(HashableItem(inner_mapping()),): 1},
        }})

    def test_key_carrier_at_mapping_value_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "outer": {tuple_pair_key(): 1},
        }})

    def test_key_carrier_mapping_value_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            "outer": {tuple_pair_key(): 1},
        }})
        check_fires(self, lambda: {"pairs": {
            "outer": {
                HashableItem(CANDIDATE): 1,
                HashableItem(HOLDOUT_ITEM): 2,
            },
        }})
        check_fires(self, lambda: {"pairs": {
            "outer": {tuple_pair_key(): 1},
        }.values()})
        check_governed_refusal(self, lambda: {"pairs": {
            "outer": {bundle_tuple_pair_key(): 1},
        }})


def plain_iterator(form, elements):
    if form == "map":
        return map(lambda element: element, elements)
    if form == "filter":
        return filter(lambda element: True, elements)
    if form == "generator":
        return (element for element in elements)
    if form == "list iterator":
        return iter(elements)
    if form == "reversed":
        return reversed(elements)
    raise ValueError(form)


def iterator_arrangement(pair, inner_form="list",
                         iterator_form="map", outer_form="list"):
    if inner_form == "list":
        inner = [OnceOnlyIterable(pair)]
    else:
        inner = (OnceOnlyIterable(pair),)
    iterator = plain_iterator(iterator_form, [inner])
    if outer_form == "list":
        return {"pairs": [iterator]}
    if outer_form == "tuple":
        return {"pairs": (iterator,)}
    if outer_form == "deque":
        return {"pairs": collections.deque([iterator])}
    if outer_form == "user list":
        return {"pairs": collections.UserList([iterator])}
    if outer_form == "sequence":
        return {"pairs": SequenceCarrier([iterator])}
    raise ValueError(outer_form)


class SinglePassInsideIteratorBundleTests(unittest.TestCase):
    """Ruling 781: a single pass iterable carrying a pair,
    standing inside a list or a tuple, standing inside a
    plain iterator, standing as an element of a list at the
    pairs position, refuses at every bundle surface."""

    def test_map_iterator_inner_list_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair()))

    def test_filter_iterator_inner_list_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), iterator_form="filter"))

    def test_generator_inner_list_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), iterator_form="generator"))

    def test_list_iterator_inner_list_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), iterator_form="list iterator"))

    def test_reversed_inner_list_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), iterator_form="reversed"))

    def test_map_iterator_inner_list_index_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            [0, flagged_pair()]))

    def test_generator_inner_list_index_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            [0, flagged_pair()], iterator_form="generator"))

    def test_map_iterator_inner_tuple_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), inner_form="tuple"))

    def test_filter_iterator_inner_tuple_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), inner_form="tuple",
            iterator_form="filter"))

    def test_generator_inner_tuple_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), inner_form="tuple",
            iterator_form="generator"))

    def test_list_iterator_inner_tuple_plain_pair_refuses(self):
        check_refuses(self, lambda: iterator_arrangement(
            flagged_pair(), inner_form="tuple",
            iterator_form="list iterator"))

    def test_iterator_as_tuple_element_refuses_at_build(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_build(iterator_arrangement(
            flagged_pair(), outer_form="tuple"))
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertFalse(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 1)

    def test_iterator_as_deque_element_refuses_at_build(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_build(iterator_arrangement(
            flagged_pair(), iterator_form="generator",
            outer_form="deque"))
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertFalse(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 1)

    def test_iterator_as_user_list_element_refuses_at_build(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_build(iterator_arrangement(
            flagged_pair(), outer_form="user list"))
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertFalse(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 1)

    def test_iterator_as_sequence_element_refuses_at_build(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_build(iterator_arrangement(
            flagged_pair(), iterator_form="generator",
            outer_form="sequence"))
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertFalse(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 1)

    def test_clean_pair_in_same_arrangement_proceeds(self):
        check_proceeds(self, lambda: iterator_arrangement(
            clean_bundle_pair()), comparisons=0)
        check_clears(self, lambda: iterator_arrangement(
            direct_pair()))

    def test_malformed_pair_in_same_arrangement_refused(self):
        check_governed_refusal(self, lambda: iterator_arrangement(
            malformed_pair()))

    def test_single_pass_inside_iterator_controls_stand(self):
        check_refuses(self, lambda: {"pairs": [
            [OnceOnlyIterable(flagged_pair())],
        ]})
        check_refuses(self, lambda: {"pairs": [
            plain_iterator("map", [OnceOnlyIterable(flagged_pair())]),
        ]})
        check_refuses(self, lambda: {"pairs": [
            plain_iterator("map", [[flagged_pair()]]),
        ]})
        check_fires(self, lambda: iterator_arrangement(
            direct_pair()))


class WrappedKeyItemsPositionTests(unittest.TestCase):
    """Ruling 782: a nested mapping standing as a key wrapped
    in a one element tuple, standing at the items position,
    fires at the direct act, in parity with its holdout_items,
    pairs, and holdout forms."""

    def test_tuple_wrapped_key_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }})

    def test_tuple_wrapped_key_at_items_view_fires(self):
        check_fires(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }.items()})

    def test_wrapped_key_at_items_clean_clears(self):
        check_clears(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }})

    def test_wrapped_key_items_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()),): 1,
        }})
        check_fires(self, lambda: {"pairs": {
            (HashableItem(inner_mapping()),): 1,
        }})
        check_fires(self, lambda: {"holdout": {
            (HashableItem(inner_mapping()),): 1,
        }})
        check_fires(self, lambda: {"items": {
            HashableItem({"key": {"inner": {
                "text": HOLDOUT_TEXT, "split": "holdout"}}}): 1,
        }.items()})
        check_governed_refusal(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }})


class TuplePairKeyValuesViewTests(unittest.TestCase):
    """Ruling 783: a tuple pair key presented through the
    values view of its mapping, at the holdout_items position,
    fires at the direct act and refuses at the bundle
    surfaces, in parity with its direct, items view, and
    keys view forms."""

    def test_tuple_pair_key_values_view_direct_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }.values()})

    def test_tuple_pair_key_values_view_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }.values()})

    def test_tuple_pair_key_values_view_bundle_refuses(self):
        check_refuses(self, lambda: {
            "candidate_items": [dict(CANDIDATE)],
            "holdout_items": {bundle_tuple_pair_key(): 1}.values(),
        })

    def test_tuple_pair_key_values_view_bundle_clean_proceeds(self):
        def clean_key():
            return (
                HashableItem(CANDIDATE),
                HashableItem(CLEAN_HOLDOUT),
            )
        check_proceeds(self, lambda: {
            "candidate_items": [dict(CANDIDATE)],
            "holdout_items": {clean_key(): 1}.values(),
        }, comparisons=0)

    def test_tuple_pair_key_values_view_controls_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }.items()}, comparisons=3)
        check_fires(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }.keys()}, comparisons=2)


if __name__ == "__main__":
    unittest.main()
