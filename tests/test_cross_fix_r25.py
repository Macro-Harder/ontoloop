"""Fix round 25 tests for Region 2: cross split readings.

Charges pinned here, from design/steps/step-15-r25-triage.md:
ruling 1100 (the cross split audit wrapped pair key presented
through a dictionary view standing inside a plain subclass
container at the items position beside a second element
defect, counted severally at the R25-CROSS-1 identity, Low);
ruling 1101 (the cross split audit wrapped pair key presented
through a dictionary view standing inside a subclass container
or an iterator container standing inside a container at the
items position beside a second element defect, counted
severally at the R25-CROSS-2 identity, Low); ruling 1102 (the
cross split audit wrapped pair key presented through a keys
view standing inside an iterator standing inside an iterator
at the deep container position defect, merged expressly at
the R25-CROSS-3 identity, Low, with R25-EVAL-1 of the Eval
paper, roster 2289, counted inside it, pins standing at the
direct act and at the evaluation call point in the form of
the Round 24 pins for ruling 1027, the evaluation call point
deciding through the same shared act at both occasions);
ruling 1103 (the cross split audit wrapped pair key presented
through a keys view standing beside a second element inside
a subclass container or an iterator container defect, counted
severally at the R25-EVAL-3 identity, Low, with R25-EVAL-2,
the keys view standing inside a generic iterable container
at the deep container position, counted severally at its own
identity in the same ruling, each cured severally); and
ruling 1104 (the dataset instruction item surface key
material presented through a dictionary view standing inside
a delegating container subclass whose iteration act stands
in an intermediate class defect, merged expressly at the
R25-DATASET-1 identity, Low, with S15-R25-SPAN-1 of the
Spanning paper, roster 2295 RESEAT, counted inside it, its
act charged at the seam test in cross_split_audit.py).
dataset.py stands untouched in full under this charge, and
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
    SequenceCarrier,
    check_clears,
    check_fires,
    inner_mapping,
    tuple_pair_key,
)
from tests.test_cross_fix_r23 import frozenset_key, single_pass_key
from tests.test_cross_fix_r24 import (
    DequeSubclassPlain,
    ListSubclassPlain,
    TupleSubclassPlain,
    UserListSubclassPlain,
    check_dataset_clears,
    check_dataset_fires,
    items_view,
    keys_view,
    values_view,
    wrapped_key,
)
from tests.test_promote_fix_r22 import (
    AbstractSetSubclass as DelegatingAbstractSetSubclass,
    DequeSubclass as DelegatingDequeSubclass,
    ListSubclass as DelegatingListSubclass,
    SequenceSubclass as DelegatingSequenceSubclass,
    SetSubclass as DelegatingSetSubclass,
    TupleSubclass as DelegatingTupleSubclass,
    UserListSubclass as DelegatingUserListSubclass,
)

OCCASIONS = ("candidate construction", "promotion")


def gen_of(item):
    return (element for element in [item])


def zip_of(item):
    return zip([item])


def map_of(item):
    return map(lambda element: element, [item])


def enum_of(item):
    return enumerate([item])


def filter_of(item):
    return filter(lambda element: True, [item])


def iter_of(item):
    return iter([item])


def reversed_of(item):
    return reversed([item, 1])


def listiter_of(item):
    return iter([item])


class CustomIterable:
    """A plain custom iterable class carrying its elements
    in a list of its own, in the form of the Eval paper."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


class DelegatingListChild(DelegatingListSubclass):
    """A plain subclass of a delegating list subclass,
    defining no iteration act of its own."""


class DelegatingListGrandChild(DelegatingListChild):
    """A plain subclass of the child form above."""


class DelegatingTupleChild(DelegatingTupleSubclass):
    """A plain subclass of a delegating tuple subclass."""


class DelegatingDequeChild(DelegatingDequeSubclass):
    """A plain subclass of a delegating deque subclass."""


class DelegatingUserListChild(DelegatingUserListSubclass):
    """A plain subclass of a delegating UserList subclass."""


class DelegatingSequenceChild(DelegatingSequenceSubclass):
    """A plain subclass of a delegating Sequence subclass."""


class DelegatingSetChild(DelegatingSetSubclass):
    """A plain subclass of a delegating set subclass."""


class DelegatingAbstractSetChild(DelegatingAbstractSetSubclass):
    """A plain subclass of a delegating abstract Set
    subclass."""


class DelegatingFrozensetSubclass(frozenset):
    """A frozenset subclass whose iteration act delegates
    to one stored iterator."""

    def __new__(cls, items):
        return super().__new__(cls, ())

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class DelegatingFrozensetChild(DelegatingFrozensetSubclass):
    """A plain subclass of a delegating frozenset
    subclass."""


class IterationMixin:
    """A mixin class carrying a delegating iteration act."""

    def __iter__(self):
        return self._stored


class MixinListSubclass(IterationMixin, list):
    """A list subclass whose iteration act stands defined
    by a mixin class standing between its own class and
    its list base in its class order."""

    def __init__(self, items):
        super().__init__()
        self._stored = iter(list(items))


def clean_keys_view():
    clean_inner = {"inner": {"text": CLEAN_TEXT}}
    return {(HashableItem(clean_inner),): 1}.keys()


def check_direct_clears_zero(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertFalse(result["fired"])
            test_case.assertEqual(result["comparisons"], 0)


def check_wrapper_clears(test_case, make_holdout):
    promote = harness.require("ontoloop.promote")
    bundle = {
        "instruction_items": [
            {"instruction_text": HOLDOUT_TEXT}],
        "holdout_items": make_holdout(),
    }
    outcome = promote.test_instruction_items_against_holdout(
        bundle, occasion="promotion")
    test_case.assertFalse(outcome["fired"])


def check_dataset_text_clears(test_case, make_holdout, text):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                {
                    "instruction_items": [{"text": text}],
                    "holdout_items": make_holdout(),
                },
                occasion=occasion)
            test_case.assertFalse(result["fired"])


class Ruling1100SubclassBesideTests(unittest.TestCase):
    """Ruling 1100, identity R25-CROSS-1: the wrapped pair
    key through a dictionary view standing inside a plain
    subclass container at the items position beside a
    second element fires at the direct act, in parity with
    the same presentation standing alone inside the same
    container."""

    def test_keys_view_list_subclass_beside_string_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain(
            [keys_view(), "x"])})
        check_fires(self, lambda: {"items": ListSubclassPlain(
            ["x", keys_view()])})

    def test_keys_view_tuple_subclass_beside_string_fires(self):
        check_fires(self, lambda: {"items": TupleSubclassPlain(
            (keys_view(), "x"))})

    def test_keys_view_deque_subclass_beside_string_fires(self):
        check_fires(self, lambda: {"items": DequeSubclassPlain(
            [keys_view(), "x"])})

    def test_keys_view_userlist_subclass_beside_fires(self):
        check_fires(self, lambda: {
            "items": UserListSubclassPlain([keys_view(), "x"])})

    def test_items_view_list_subclass_beside_string_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain(
            [items_view(), "x"])})

    def test_values_view_list_subclass_beside_string_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain(
            [values_view(), "x"])})

    def test_plain_mapping_list_subclass_beside_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain(
            [{wrapped_key(): 1}, "x"])})

    def test_list_subclass_holding_list_beside_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain(
            [[keys_view(), "x"]])})

    def test_subclass_beside_clean_clears(self):
        check_clears(self, lambda: {"items": ListSubclassPlain(
            [keys_view(), "x"])})

    def test_subclass_beside_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {
            "items": ListSubclassPlain([keys_view(), "x"])})


class Ruling1101BesideElementTests(unittest.TestCase):
    """Ruling 1101, identity R25-CROSS-2: the wrapped pair
    key through a dictionary view standing inside a
    subclass container element or an iterator element
    standing inside a container at the items position
    beside a second element fires at the direct act."""

    def test_view_in_list_subclass_in_list_beside_fires(self):
        check_fires(self, lambda: {"items": [
            ListSubclassPlain([keys_view()]), "x"]})

    def test_view_in_generator_in_list_beside_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(keys_view()), "x"]})

    def test_beside_list_as_element_of_generator_fires(self):
        check_fires(self, lambda: {
            "items": gen_of([keys_view(), "x"])})

    def test_beside_element_clean_clears(self):
        check_clears(self, lambda: {"items": [
            ListSubclassPlain([keys_view()]), "x"]})
        check_clears(self, lambda: {"items": [
            gen_of(keys_view()), "x"]})

    def test_beside_element_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            ListSubclassPlain([keys_view()]), "x"]})


class Ruling1102NestedIteratorTests(unittest.TestCase):
    """Ruling 1102, identity R25-CROSS-3 merged with
    R25-EVAL-1: the wrapped pair key through a keys view
    standing inside an iterator standing inside an
    iterator at the deep container position fires at the
    direct act, at the items and pairs positions."""

    def test_generator_in_generator_items_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(keys_view()))]})

    def test_generator_in_generator_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [
            gen_of(gen_of(keys_view()))]})

    def test_zip_in_zip_items_fires(self):
        check_fires(self, lambda: {"items": [
            zip_of(zip_of(keys_view()))]})

    def test_map_in_map_items_fires(self):
        check_fires(self, lambda: {"items": [
            map_of(map_of(keys_view()))]})

    def test_generator_in_zip_items_fires(self):
        check_fires(self, lambda: {"items": [
            zip_of(gen_of(keys_view()))]})

    def test_zip_in_generator_items_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(zip_of(keys_view()))]})

    def test_enumerate_in_generator_items_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(enum_of(keys_view()))]})

    def test_generator_in_enumerate_items_fires(self):
        check_fires(self, lambda: {"items": [
            enum_of(gen_of(keys_view()))]})

    def test_generator_in_filter_items_fires(self):
        check_fires(self, lambda: {"items": [
            filter_of(gen_of(keys_view()))]})

    def test_filter_in_generator_items_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(filter_of(keys_view()))]})

    def test_generator_in_iter_items_fires(self):
        check_fires(self, lambda: {"items": [
            iter_of(gen_of(keys_view()))]})

    def test_generator_in_reversed_items_fires(self):
        check_fires(self, lambda: {"items": [
            reversed_of(gen_of(keys_view()))]})

    def test_list_iterator_in_list_iterator_fires(self):
        check_fires(self, lambda: {"items": [
            listiter_of(listiter_of(keys_view()))]})

    def test_three_iterator_layers_items_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(gen_of(keys_view())))]})

    def test_three_iterator_layers_at_position_fires(self):
        check_fires(self, lambda: {
            "items": gen_of(gen_of(gen_of(keys_view())))})

    def test_generator_in_generator_in_tuple_fires(self):
        check_fires(self, lambda: {"items": (
            gen_of(gen_of(keys_view())),)})

    def test_generator_in_generator_in_deque_fires(self):
        check_fires(self, lambda: {"items": deque([
            gen_of(gen_of(keys_view()))])})

    def test_generator_in_generator_in_userlist_fires(self):
        check_fires(self, lambda: {"items": UserList([
            gen_of(gen_of(keys_view()))])})

    def test_generator_in_generator_in_list_subclass_fires(
            self):
        check_fires(self, lambda: {"items": ListSubclassPlain([
            gen_of(gen_of(keys_view()))])})

    def test_nested_iterator_clean_clears(self):
        check_clears(self, lambda: {"items": [
            gen_of(gen_of(keys_view()))]})

    def test_nested_iterator_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            gen_of(gen_of(keys_view()))]})


class Ruling1103Eval3BesideTests(unittest.TestCase):
    """Ruling 1103, first position, identity R25-EVAL-3:
    the wrapped pair key through a keys view standing
    beside a second element inside a subclass container
    or an iterator container fires at the direct act at
    the items position, counted severally from ruling
    1101 on the presentation geometry ground."""

    def test_beside_in_list_subclass_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            ListSubclassPlain([keys_view(), "x"])]})

    def test_beside_in_tuple_subclass_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            TupleSubclassPlain((keys_view(), "x"))]})

    def test_beside_in_deque_subclass_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            DequeSubclassPlain([keys_view(), "x"])]})

    def test_beside_in_userlist_subclass_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            UserListSubclassPlain([keys_view(), "x"])]})

    def test_beside_string_before_in_list_subclass_fires(self):
        check_fires(self, lambda: {"items": [
            ListSubclassPlain(["x", keys_view()])]})

    def test_beside_none_in_list_subclass_fires(self):
        check_fires(self, lambda: {"items": [
            ListSubclassPlain([keys_view(), None])]})

    def test_beside_number_in_list_subclass_fires(self):
        check_fires(self, lambda: {"items": [
            ListSubclassPlain([keys_view(), 2])]})

    def test_beside_in_generator_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of([keys_view(), "x"])]})

    def test_beside_in_zip_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            zip_of([keys_view(), "x"])]})

    def test_beside_in_enumerate_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            enum_of([keys_view(), "x"])]})

    def test_beside_in_reversed_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            reversed([keys_view(), "x"])]})

    def test_beside_in_map_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            map_of([keys_view(), "x"])]})

    def test_beside_in_filter_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            filter_of([keys_view(), "x"])]})

    def test_beside_in_iter_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            iter_of([keys_view(), "x"])]})

    def test_beside_in_generator_at_position_fires(self):
        check_fires(self, lambda: {
            "items": gen_of([keys_view(), "x"])})

    def test_beside_in_subclass_clean_clears(self):
        check_clears(self, lambda: {"items": [
            ListSubclassPlain([keys_view(), "x"])]})

    def test_beside_in_subclass_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            ListSubclassPlain([keys_view(), "x"])]})


class Ruling1103Eval2GenericIterableTests(unittest.TestCase):
    """Ruling 1103, second position, identity R25-EVAL-2:
    the wrapped pair key through a keys view standing
    inside a generic iterable container at the deep
    container position fires at the direct act, at the
    items and pairs positions, counted severally from
    ruling 1102."""

    def test_sequence_carrier_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([keys_view()])]})

    def test_sequence_carrier_in_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [
            SequenceCarrier([keys_view()])]})

    def test_once_only_iterable_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [
            OnceOnlyIterable([keys_view()])]})

    def test_once_only_iterable_in_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [
            OnceOnlyIterable([keys_view()])]})

    def test_custom_iterable_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [
            CustomIterable([keys_view()])]})

    def test_sequence_in_sequence_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([SequenceCarrier([keys_view()])])]})

    def test_sequence_in_custom_iterable_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            CustomIterable([SequenceCarrier([keys_view()])])]})

    def test_custom_iterable_in_sequence_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([CustomIterable([keys_view()])])]})

    def test_once_only_in_sequence_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([OnceOnlyIterable([keys_view()])])]})

    def test_sequence_in_list_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            [SequenceCarrier([keys_view()])]]})

    def test_sequence_in_tuple_fires(self):
        check_fires(self, lambda: {"items": (
            SequenceCarrier([keys_view()]),)})

    def test_sequence_in_deque_fires(self):
        check_fires(self, lambda: {"items": deque([
            SequenceCarrier([keys_view()])])})

    def test_sequence_in_userlist_fires(self):
        check_fires(self, lambda: {"items": UserList([
            SequenceCarrier([keys_view()])])})

    def test_sequence_in_list_subclass_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain([
            SequenceCarrier([keys_view()])])})

    def test_sequence_in_generator_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(SequenceCarrier([keys_view()]))]})

    def test_sequence_at_mapping_value_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            {"k": SequenceCarrier([keys_view()])}]})

    def test_generic_iterable_clean_clears(self):
        check_clears(self, lambda: {"items": [
            SequenceCarrier([keys_view()])]})

    def test_generic_iterable_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            SequenceCarrier([keys_view()])]})


class Ruling1104DatasetSeamTests(unittest.TestCase):
    """Ruling 1104, identity R25-DATASET-1 merged with
    S15-R25-SPAN-1: key material through a dictionary view
    standing inside a delegating container subclass whose
    iteration act stands in an intermediate class clears
    at the dataset instruction item surface, as the direct
    act and the promote wrapper clear the same
    presentation."""

    def test_dataset_list_child_in_list_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingListChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingListChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_list_child_in_tuple_clears(self):
        check_dataset_fires(self, lambda: {"items": (
            DelegatingListChild([keys_view()]),)})
        check_fires(self, lambda: {"items": (
            DelegatingListChild([keys_view()]),)})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": (
            DelegatingListChild([keys_view()]),)})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_list_child_in_list_in_list_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            [DelegatingListChild([keys_view()])]]})
        check_fires(self, lambda: {"items": [
            [DelegatingListChild([keys_view()])]]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            [DelegatingListChild([keys_view()])]]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_list_child_pairs_clears(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingListChild([keys_view()])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingListChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"pairs": [
            DelegatingListChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_list_child_values_view_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListChild([values_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingListChild([values_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingListChild([values_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_tuple_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingTupleChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingTupleChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingTupleChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_deque_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingDequeChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingDequeChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingDequeChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_userlist_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingUserListChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingUserListChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingUserListChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_sequence_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingSequenceChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingSequenceChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingSequenceChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_list_grandchild_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListGrandChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingListGrandChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingListGrandChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_set_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingSetChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingSetChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingSetChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_abstract_set_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingAbstractSetChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingAbstractSetChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingAbstractSetChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_frozenset_child_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingFrozensetChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingFrozensetChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingFrozensetChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_mixin_form_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            MixinListSubclass([keys_view()])]})
        check_fires(self, lambda: {"items": [
            MixinListSubclass([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            MixinListSubclass([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_set_child_pairs_clears(self):
        check_dataset_fires(self, lambda: {"pairs": [
            DelegatingSetChild([keys_view()])]})
        check_fires(self, lambda: {"pairs": [
            DelegatingSetChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"pairs": [
            DelegatingSetChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_set_child_holdout_items_clears(self):
        check_dataset_fires(self, lambda: {"holdout_items": [
            DelegatingSetChild([keys_view()])]})
        check_fires(self, lambda: {"holdout_items": [
            DelegatingSetChild([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"holdout_items": [
            DelegatingSetChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_set_child_items_view_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingSetChild([items_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingSetChild([items_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingSetChild([items_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_set_child_in_tuple_in_list_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            (DelegatingSetChild([keys_view()]),)]})
        check_fires(self, lambda: {"items": [
            (DelegatingSetChild([keys_view()]),)]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            (DelegatingSetChild([keys_view()]),)]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_set_child_in_list_in_list_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            [DelegatingSetChild([keys_view()])]]})
        check_fires(self, lambda: {"items": [
            [DelegatingSetChild([keys_view()])]]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            [DelegatingSetChild([keys_view()])]]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_abstract_set_child_in_list_in_list(
            self):
        check_dataset_fires(self, lambda: {"items": [
            [DelegatingAbstractSetChild([keys_view()])]]})
        check_fires(self, lambda: {"items": [
            [DelegatingAbstractSetChild([keys_view()])]]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            [DelegatingAbstractSetChild([keys_view()])]]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_direct_and_wrapper_clear_child_forms(self):
        check_fires(self, lambda: {"items": [
            DelegatingListChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingSetChild([keys_view()])]})
        check_fires(self, lambda: {"items": [
            MixinListSubclass([keys_view()])]})
        
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingListChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingSetChild([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_child_alone_still_fires(self):
        check_dataset_fires(self, lambda: {
            "items": DelegatingListChild([keys_view()])})

    def test_dataset_clean_text_against_child_clears(self):
        check_dataset_text_clears(
            self,
            lambda: {"items": [
                DelegatingListGrandChild([keys_view()])]},
            CLEAN_TEXT)

    def test_dataset_clean_key_material_in_child_clears(self):
        check_dataset_text_clears(
            self,
            lambda: {"items": [
                DelegatingListGrandChild([clean_keys_view()])]},
            HOLDOUT_TEXT)


class ChargedFormsControlsTests(unittest.TestCase):
    """Controls: the charged forms of rulings 1026, 1027,
    and 1028 still decide as charged, the parity carriers
    of the papers still fire, and the standing forms of
    the neighbouring readings still fire."""

    def test_exact_list_beside_still_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), "x"]})

    def test_subclass_alone_still_fires(self):
        check_fires(self, lambda: {"items": ListSubclassPlain(
            [keys_view()])})

    def test_single_iterator_alone_still_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(keys_view())]})

    def test_sequence_carrier_at_position_still_fires(self):
        check_fires(self, lambda: {
            "items": SequenceCarrier([keys_view()])})

    def test_tuple_carrier_nested_iterator_still_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of({tuple_pair_key(): 1}.keys()))]})

    def test_items_and_values_views_nested_iterator_fire(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(items_view()))]})
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(values_view()))]})

    def test_frozenset_and_single_pass_carriers_in_sequence(
            self):
        check_fires(self, lambda: {"items": [SequenceCarrier(
            [{frozenset_key(): 1}.keys()])]})
        check_fires(self, lambda: {"items": [SequenceCarrier(
            [{single_pass_key(): 1}.keys()])]})

    def test_nested_iterator_holdout_positions_still_fire(
            self):
        check_fires(self, lambda: {"holdout_items": [
            gen_of(gen_of(keys_view()))]})
        check_fires(self, lambda: {"holdout": [
            gen_of(gen_of(keys_view()))]})

    def test_dataset_parent_form_still_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        promote = harness.require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}],
            "holdout_items": (lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})(),
        }
        outcome = promote.test_instruction_items_against_holdout(
            bundle, occasion="promotion")
        self.assertTrue(outcome["fired"])
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1)

    def test_dataset_exact_two_containers_still_fires(self):
        check_dataset_fires(
            self, lambda: {"items": [[keys_view()]]})


if __name__ == "__main__":
    unittest.main()
