"""Fix round 23 tests for Region 2: cross split.

Charge pinned here, from design/steps/step-15-r23-triage.md:
ruling 965 (the cross split audit wrapped pair key presented
through a keys view standing inside two containers at the
items and pairs positions defect, merged expressly, at the
R23-CROSS-1 identity, Low), with R23-EVAL-1 of the Eval
paper, roster 2187, counted inside it, and the dataset
instruction item surface limb counted inside it in the
form of Round 22 ruling 905. The cure extends the view
reading of the direct act audit_instruction_item in
ontoloop/cross_split_audit.py to the wrapped pair key
presented through a keys view standing inside two or more
containers at the items position and at the pairs
position, in parity with the same view standing inside
one container at those positions. dataset.py stands
untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import UserList, deque

from tests import harness
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    HashableItem,
    OnceOnlyIterable,
    check_clears,
    check_fires,
    check_governed_refusal,
    direct_pair,
    inner_mapping,
    tuple_pair_key,
)

OCCASIONS = ("candidate construction", "promotion")


def wrapped_key():
    return (HashableItem(inner_mapping()),)


def single_pass_key():
    return OnceOnlyIterable(direct_pair())


def frozenset_key():
    return frozenset(tuple_pair_key())


def check_fires_exactly(test_case, make_bundle, expected):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertTrue(result["fired"])
            test_case.assertEqual(result["comparisons"], expected)


def dataset_bundle(text, holdout):
    return {
        "instruction_items": [{"text": text}],
        "holdout_items": holdout,
    }


def check_dataset_holdout_fires(test_case, make_holdout):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(HOLDOUT_TEXT, make_holdout()),
                occasion=occasion)
            test_case.assertTrue(result["fired"])
            shared = result["cross_split_audit_result"]
            test_case.assertEqual(shared["comparisons"], 1)


def check_dataset_holdout_clears(test_case, make_holdout):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(CLEAN_TEXT, make_holdout()),
                occasion=occasion)
            test_case.assertFalse(result["fired"])


class WrappedKeysViewTwoContainersCrossTests(unittest.TestCase):
    """Ruling 965, Cross split limb, identity R23-CROSS-1:
    the wrapped pair key through a keys view standing
    inside two containers at the items position, and
    inside a list inside a list at the pairs position,
    fires at the direct act."""

    def test_wrapped_keys_view_list_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.keys()]]})

    def test_wrapped_keys_view_tuple_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [({
            wrapped_key(): 1,
        }.keys(),)]})

    def test_wrapped_keys_view_list_in_tuple_items_fires(self):
        check_fires(self, lambda: {"items": ([{
            wrapped_key(): 1,
        }.keys()],)})

    def test_wrapped_keys_view_tuple_in_tuple_items_fires(self):
        check_fires(self, lambda: {"items": (({
            wrapped_key(): 1,
        }.keys(),),)})

    def test_wrapped_keys_view_deque_in_deque_items_fires(self):
        check_fires(self, lambda: {"items": deque([deque([{
            wrapped_key(): 1,
        }.keys()])])})

    def test_wrapped_keys_view_userlist_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [UserList([{
            wrapped_key(): 1,
        }.keys()])]})

    def test_wrapped_keys_view_list_in_userlist_items_fires(self):
        check_fires(self, lambda: {"items": UserList([[{
            wrapped_key(): 1,
        }.keys()]])})

    def test_wrapped_keys_view_three_containers_items_fires(self):
        check_fires(self, lambda: {"items": [[[{
            wrapped_key(): 1,
        }.keys()]]]})

    def test_wrapped_keys_view_list_in_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [[{
            wrapped_key(): 1,
        }.keys()]]})


class WrappedKeysViewTwoContainersEvalTests(unittest.TestCase):
    """Ruling 965, Eval limb, R23-EVAL-1 counted inside it:
    the same wrapped key through the same keys view
    inside two container levels at the items and pairs
    positions fires at the direct act."""

    def test_eval_wrapped_keys_view_list_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.keys()]]})

    def test_eval_wrapped_keys_view_tuple_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [({
            wrapped_key(): 1,
        }.keys(),)]})

    def test_eval_wrapped_keys_view_list_in_tuple_items_fires(self):
        check_fires(self, lambda: {"items": ([{
            wrapped_key(): 1,
        }.keys()],)})

    def test_eval_wrapped_keys_view_deque_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [deque([{
            wrapped_key(): 1,
        }.keys()])]})

    def test_eval_wrapped_keys_view_three_levels_items_fires(self):
        check_fires(self, lambda: {"items": [[[{
            wrapped_key(): 1,
        }.keys()]]]})

    def test_eval_wrapped_keys_view_list_in_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [[{
            wrapped_key(): 1,
        }.keys()]]})


class WrappedKeysViewTwoContainersDatasetTests(unittest.TestCase):
    """Ruling 965, dataset instruction item surface limb,
    counted inside the merged defect: the surface decides
    the presentation as the direct act decides it, with
    no act under this ruling touching dataset.py."""

    def test_dataset_items_wrapped_keys_view_two_containers_fires(self):
        check_dataset_holdout_fires(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.keys()]]})

    def test_dataset_items_wrapped_keys_view_two_containers_clears(self):
        check_dataset_holdout_clears(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.keys()]]})


class WrappedKeysViewTwoContainersControlsTests(unittest.TestCase):
    """Ruling 965 controls: the charged forms of rulings
    906 and 907 still fire, the parity carriers of the
    papers still fire at the same depth, the holdout side
    forms still fire, clean material in the probed form
    clears on a comparison, and the bundle surfaces on
    the pairs form still return the governed refusal."""

    def test_one_container_keys_view_items_still_fires(self):
        check_fires(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.keys()]})

    def test_wrapped_items_view_two_containers_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.items()]]})

    def test_wrapped_values_view_two_containers_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.values()]]})

    def test_tuple_keys_view_two_containers_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            tuple_pair_key(): 1,
        }.keys()]]})

    def test_frozenset_keys_view_two_containers_items_fires(self):
        check_fires_exactly(self, lambda: {"items": [[{
            frozenset_key(): 1,
        }.keys()]]}, 1)

    def test_single_pass_keys_view_two_containers_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            single_pass_key(): 1,
        }.keys()]]})

    def test_wrapped_keys_view_two_containers_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": [[{
            wrapped_key(): 1,
        }.keys()]]})

    def test_wrapped_keys_view_two_containers_holdout_fires(self):
        check_fires(self, lambda: {"holdout": [[{
            wrapped_key(): 1,
        }.keys()]]})

    def test_wrapped_keys_view_two_containers_clean_clears(self):
        check_clears(self, lambda: {"items": [[{
            wrapped_key(): 1,
        }.keys()]]})
        check_clears(self, lambda: {"pairs": [[{
            wrapped_key(): 1,
        }.keys()]]})

    def test_pairs_two_containers_bundle_governed_refusal_stands(self):
        check_governed_refusal(self, lambda: {"pairs": [[{
            wrapped_key(): 1,
        }.keys()]]})


if __name__ == "__main__":
    unittest.main()
