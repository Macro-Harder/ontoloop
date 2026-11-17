"""Fix round 24 tests for Region 2: cross split and spanning seam.

Charges pinned here, from design/steps/step-15-r24-triage.md:
ruling 1026 (the cross split audit wrapped pair key presented
through a dictionary view standing inside a container beside a
second element defect, merged expressly, at the R24-CROSS-1
identity, Low), with R24-UC-2 of the Unrowed C paper, roster
2249, counted inside it in the bounded form that ruling states;
ruling 1027 (the cross split audit wrapped pair key presented
through a keys view standing inside a subclass container and
inside an iterator container at the deep container position
defect, merged expressly, at the R24-EVAL-1 identity, Low),
with R24-EVAL-2 of the Eval paper, roster 2237, counted inside
it; and ruling 1028 (the spanning seam, key material presented
through a dictionary view standing inside a container subclass
standing inside a container defect, counted severally at the
R24-SPAN-1 identity, Low), whose cure lands in
cross_split_audit.py and at the one named call point of the
dataset instruction item surface materialisation in dataset.py.
dataset.py stands otherwise untouched in full under this
charge, and tests/test_unrowed_c.py stands held whole and
unchanged, with no pin of this region filed in it.
"""

import unittest
from collections import UserList, deque

from tests import harness
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    HashableItem,
    check_clears,
    check_fires,
    inner_mapping,
    tuple_pair_key,
)
from tests.test_cross_fix_r23 import frozenset_key, single_pass_key
from tests.test_promote_fix_r22 import (
    DequeSubclass as DelegatingDequeSubclass,
    ListSubclass as DelegatingListSubclass,
    SequenceSubclass as DelegatingSequenceSubclass,
    TupleSubclass as DelegatingTupleSubclass,
    UserListSubclass as DelegatingUserListSubclass,
)

OCCASIONS = ("candidate construction", "promotion")


def wrapped_key():
    return (HashableItem(inner_mapping()),)


def keys_view():
    return {wrapped_key(): 1}.keys()


def items_view():
    return {wrapped_key(): 1}.items()


def values_view():
    return {wrapped_key(): 1}.values()


def tuple_keys_view():
    return {tuple_pair_key(): 1}.keys()


def tuple_values_view():
    return {1: tuple_pair_key()}.values()


class ListSubclassPlain(list):
    """A list subclass carrying its elements in its own
    storage, in the plain form of the Eval paper."""


class TupleSubclassPlain(tuple):
    """A tuple subclass in the same plain form."""


class DequeSubclassPlain(deque):
    """A deque subclass in the same plain form."""


class UserListSubclassPlain(UserList):
    """A UserList subclass in the same plain form."""


def dataset_bundle(text, holdout):
    return {
        "instruction_items": [{"text": text}],
        "holdout_items": holdout,
    }


def check_dataset_fires(test_case, make_holdout, comparisons=1):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(HOLDOUT_TEXT, make_holdout()),
                occasion=occasion)
            test_case.assertTrue(result["fired"])
            shared = result["cross_split_audit_result"]
            test_case.assertEqual(shared["comparisons"], comparisons)


def check_dataset_clears(test_case, make_holdout):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                dataset_bundle(HOLDOUT_TEXT, make_holdout()),
                occasion=occasion)
            test_case.assertFalse(result["fired"])


class Ruling1026ListBesideTests(unittest.TestCase):
    """Ruling 1026, Cross split limb, identity R24-CROSS-1:
    the wrapped pair key through a dictionary view standing
    inside a list beside a second element fires at the
    direct act, in parity with the same presentation
    standing alone inside the list."""

    def test_keys_view_list_beside_string_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), "x"]})
        check_fires(self, lambda: {"items": ["x", keys_view()]})

    def test_keys_view_list_beside_none_and_bytes_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), None]})
        check_fires(self, lambda: {"items": [None, keys_view()]})
        check_fires(self, lambda: {"items": [keys_view(), b"x"]})
        check_fires(self, lambda: {"items": [b"x", keys_view()]})

    def test_keys_view_list_beside_containers_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), [1]]})
        check_fires(self, lambda: {"items": [keys_view(), {"a": 1}]})
        check_fires(self, lambda: {"items": [keys_view(), (1,)]})

    def test_keys_view_list_beside_number_after_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), 2]})
        check_fires(self, lambda: {"items": [keys_view(), True]})
        check_fires(self, lambda: {"items": [keys_view(), 2.5]})

    def test_items_view_list_beside_string_fires(self):
        check_fires(self, lambda: {"items": [items_view(), "x"]})
        check_fires(self, lambda: {"items": ["x", items_view()]})

    def test_values_view_list_beside_string_fires(self):
        check_fires(self, lambda: {"items": [values_view(), "x"]})
        check_fires(self, lambda: {"items": ["x", values_view()]})

    def test_plain_mapping_list_beside_string_fires(self):
        check_fires(self, lambda: {"items": [{wrapped_key(): 1}, "x"]})

    def test_keys_view_list_in_list_string_after_inner_fires(self):
        check_fires(self, lambda: {"items": [[keys_view(), "x"]]})

    def test_keys_view_list_in_list_string_after_outer_fires(self):
        check_fires(self, lambda: {"items": [[keys_view()], "x"]})

    def test_keys_view_list_beside_string_clean_clears(self):
        check_clears(self, lambda: {"items": [keys_view(), "x"]})


class Ruling1026OtherContainersBesideTests(unittest.TestCase):
    """Ruling 1026, Unrowed C limb, R24-UC-2 counted inside
    it in its bounded form: the wrapped pair key through a
    keys view standing inside a tuple, a deque, or a
    UserList beside a second element fires at the direct
    act."""

    def test_keys_view_tuple_beside_string_fires(self):
        check_fires(self, lambda: {"items": (keys_view(), "x")})
        check_fires(self, lambda: {"items": ("x", keys_view())})

    def test_keys_view_tuple_beside_other_siblings_fires(self):
        check_fires(self, lambda: {"items": (keys_view(), None)})
        check_fires(self, lambda: {"items": (keys_view(), b"x")})
        check_fires(self, lambda: {"items": (keys_view(), 2)})

    def test_keys_view_deque_beside_string_fires(self):
        check_fires(
            self, lambda: {"items": deque([keys_view(), "x"])})

    def test_keys_view_userlist_beside_string_fires(self):
        check_fires(
            self, lambda: {"items": UserList([keys_view(), "x"])})

    def test_plain_mapping_tuple_beside_string_fires(self):
        check_fires(
            self, lambda: {"items": ({wrapped_key(): 1}, "x")})

    def test_keys_view_tuple_in_list_string_after_outer_fires(self):
        check_fires(self, lambda: {"items": [(keys_view(),), "x"]})

    def test_keys_view_list_in_tuple_string_after_inner_fires(self):
        check_fires(self, lambda: {"items": ([keys_view(), "x"],)})


class Ruling1027SubclassContainerTests(unittest.TestCase):
    """Ruling 1027, Eval limb R24-EVAL-1: the wrapped pair
    key through a keys view standing inside a plain subclass
    container at the deep container position fires at the
    direct act, at the items and pairs positions."""

    def test_list_subclass_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [ListSubclassPlain([keys_view()])]})

    def test_tuple_subclass_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [TupleSubclassPlain((keys_view(),))]})

    def test_deque_subclass_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [DequeSubclassPlain([keys_view()])]})

    def test_userlist_subclass_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [UserListSubclassPlain([keys_view()])]})

    def test_list_subclass_in_tuple_items_fires(self):
        check_fires(
            self,
            lambda: {"items": (ListSubclassPlain([keys_view()]),)})

    def test_list_subclass_in_deque_items_fires(self):
        check_fires(
            self,
            lambda: {"items": deque(
                [ListSubclassPlain([keys_view()])])})

    def test_list_subclass_in_userlist_items_fires(self):
        check_fires(
            self,
            lambda: {"items": UserList(
                [ListSubclassPlain([keys_view()])])})

    def test_list_subclass_in_list_subclass_items_fires(self):
        check_fires(
            self,
            lambda: {"items": ListSubclassPlain(
                [ListSubclassPlain([keys_view()])])})

    def test_list_subclass_in_list_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [[ListSubclassPlain([keys_view()])]]})

    def test_list_subclass_in_list_pairs_fires(self):
        check_fires(
            self,
            lambda: {"pairs": [ListSubclassPlain([keys_view()])]})

    def test_list_subclass_in_list_clean_clears(self):
        check_clears(
            self,
            lambda: {"items": [ListSubclassPlain([keys_view()])]})


class Ruling1027IteratorContainerTests(unittest.TestCase):
    """Ruling 1027, Eval limb R24-EVAL-2: the wrapped pair
    key through a keys view standing inside an iterator
    container at the deep container position fires at the
    direct act, at the items and pairs positions."""

    def test_generator_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [(x for x in [keys_view()])]})

    def test_zip_in_list_items_fires(self):
        check_fires(
            self, lambda: {"items": [zip([keys_view()])]})

    def test_enumerate_in_list_items_fires(self):
        check_fires(
            self, lambda: {"items": [enumerate([keys_view()])]})

    def test_reversed_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [reversed([keys_view(), 1])]})

    def test_map_in_list_items_fires(self):
        check_fires(
            self,
            lambda: {"items": [map(lambda z: z, [keys_view()])]})

    def test_generator_in_tuple_items_fires(self):
        check_fires(
            self,
            lambda: {"items": ((x for x in [keys_view()]),)})

    def test_generator_in_list_pairs_fires(self):
        check_fires(
            self,
            lambda: {"pairs": [(x for x in [keys_view()])]})

    def test_generator_in_list_clean_clears(self):
        check_clears(
            self,
            lambda: {"items": [(x for x in [keys_view()])]})


class Ruling1028DatasetSeamTests(unittest.TestCase):
    """Ruling 1028, identity R24-SPAN-1: key material through
    a dictionary view standing inside a delegating container
    subclass standing inside a container clears at the
    dataset instruction item surface, as the direct act and
    the promote wrapper clear the same presentation, beside
    the charged forms of ruling 908 still firing there and
    the plain presentations still deciding in parity."""

    def test_dataset_delegating_list_subclass_keys_clears(self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingListSubclass([keys_view()])]})

    def test_dataset_delegating_list_subclass_tuple_keys_clears(
            self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingListSubclass([tuple_keys_view()])]})

    def test_dataset_delegating_sequence_subclass_keys_clears(
            self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingSequenceSubclass([keys_view()])]})

    def test_dataset_delegating_userlist_subclass_keys_clears(
            self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingUserListSubclass([keys_view()])]})

    def test_dataset_delegating_deque_subclass_keys_clears(self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingDequeSubclass([keys_view()])]})

    def test_dataset_delegating_tuple_subclass_keys_clears(self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingTupleSubclass([keys_view()])]})

    def test_dataset_delegating_list_subclass_values_clears(self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingListSubclass([tuple_values_view()])]})

    def test_dataset_delegating_list_subclass_items_clears(self):
        check_dataset_clears(
            self,
            lambda: {"items": [
                DelegatingListSubclass([items_view()])]})

    def test_dataset_delegating_list_subclass_pairs_clears(self):
        check_dataset_clears(
            self,
            lambda: {"pairs": [
                DelegatingListSubclass([keys_view()])]})

    def test_dataset_delegating_list_subclass_holdout_clears(
            self):
        check_dataset_clears(
            self,
            lambda: {"holdout_items": [
                DelegatingListSubclass([keys_view()])]})

    def test_direct_and_wrapper_clear_delegating_form(self):
        module = harness.require("ontoloop.cross_split_audit")
        promote = harness.require("ontoloop.promote")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"items": [
                        DelegatingListSubclass([keys_view()])]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 0)
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": {"items": [
                DelegatingListSubclass([keys_view()])]},
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertFalse(outcome["fired"])

    def test_dataset_exact_two_containers_still_fires(self):
        check_dataset_fires(
            self, lambda: {"items": [[keys_view()]]})

    def test_dataset_plain_list_subclass_fires_in_parity(self):
        check_dataset_fires(
            self,
            lambda: {"items": [ListSubclassPlain([keys_view()])]})


class Ruling1026To1028ControlsTests(unittest.TestCase):
    """Controls: the charged forms of rulings 906, 907, and
    965 still fire, the parity carriers of the papers still
    fire, and clean material in the probed forms clears on
    a comparison."""

    def test_one_container_keys_view_items_still_fires(self):
        check_fires(self, lambda: {"items": [keys_view()]})

    def test_two_containers_keys_view_items_still_fires(self):
        check_fires(self, lambda: {"items": [[keys_view()]]})

    def test_tuple_carrier_two_containers_still_fires(self):
        check_fires(
            self, lambda: {"items": [[tuple_keys_view()]]})

    def test_frozenset_carrier_two_containers_still_fires(self):
        check_fires(
            self,
            lambda: {"items": [[{frozenset_key(): 1}.keys()]]})

    def test_single_pass_carrier_two_containers_still_fires(
            self):
        check_fires(
            self,
            lambda: {"items": [[{single_pass_key(): 1}.keys()]]})

    def test_items_and_values_views_two_containers_still_fire(
            self):
        check_fires(self, lambda: {"items": [[items_view()]]})
        check_fires(self, lambda: {"items": [[values_view()]]})

    def test_beside_int_before_still_fires(self):
        check_fires(self, lambda: {"items": [0, keys_view()]})
        check_fires(self, lambda: {"items": [1, keys_view()]})
        check_fires(self, lambda: {"items": [False, keys_view()]})


if __name__ == "__main__":
    unittest.main()
