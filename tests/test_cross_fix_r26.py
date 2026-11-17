"""Fix round 26 tests for Region 2: cross split readings and seam.

Charges pinned here, from design/steps/step-15-r26-triage.md:
ruling 1189 (the cross split audit wrapped pair key presented
through a dictionary view standing beside a second element
inside a generic iterable container at the items position
defect, counted severally at the S15-R26-CROSS-1 identity,
Low, with S15-R26-EVAL-1 of the Eval paper counted inside
it); ruling 1190 (the wrapped pair key presented through a
dictionary view standing inside a generic iterable container
standing as an element of a container beside a second element
at the items position defect, at the S15-R26-CROSS-2 identity,
Low); ruling 1191 (the wrapped pair key presented through a
keys view standing at a mapping value inside a mapping in
its exact dict form standing as an element of a container at
the items position defect, at the S15-R26-CROSS-3 identity,
Low); ruling 1192 (the wrapped pair key presented through a
keys view standing at a value of an exact dict standing
inside a container at the items position defect, at the
S15-R26-EVAL-4 identity, Low); ruling 1193 (the wrapped pair
key presented through an items view or a values view standing
inside a Sequence form container at the deep container
position defect, at the S15-R26-EVAL-2 identity, Low);
ruling 1194 (the wrapped pair key presented through a keys
view standing inside a container carrying its elements by
indexed access alone at the deep container position defect,
at the S15-R26-EVAL-3 identity, Low); and ruling 1195 (the
dataset instruction item surface, key material presented
through a keys view standing as a value in a mapping standing
in a non plain mapping form, that mapping standing inside a
container at the items position, clearing at the dataset
surface beside a firing at the direct act and at the promote
wrapper, at the S15-R26-DATASET-1 identity, Low, its act
charged at the seam materialisation in cross_split_audit.py).
The acts of rulings 1189 and 1190 stand in one act sequence,
neither graded landed alone on the parity form, in the form
ruling 1241 records for candidate line E-61. dataset.py stands
untouched in full under this charge, and tests/test_unrowed_c.py
stands held whole and unchanged, with no pin of this region
filed in it.
"""

import unittest
from collections import ChainMap, Counter, OrderedDict, UserDict, UserList, defaultdict, deque
from collections.abc import Sequence
from types import MappingProxyType

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
)
from tests.test_cross_fix_r24 import (
    ListSubclassPlain,
    check_dataset_clears,
    check_dataset_fires,
    items_view,
    keys_view,
    values_view,
    wrapped_key,
)
from tests.test_promote_fix_r22 import (
    ListSubclass as DelegatingListSubclass,
)

OCCASIONS = ("candidate construction", "promotion")


def gen_of(item):
    return (element for element in [item])


class CustomIterable:
    """A plain custom iterable class carrying its elements
    in a list of its own, in the form of the Eval paper."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


class SequenceSubclass(SequenceCarrier):
    """A plain subclass of the abstract Sequence carrier."""


class IndexedOnlyCarrier:
    """A container carrying its elements by indexed access
    alone, with a length act and an item access act and no
    iteration act and no next act of its own."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


class SubDict(dict):
    """A plain dict subclass carrying no override of any act."""


class SubDictChild(SubDict):
    """A plain subclass of the dict subclass above."""


def clean_keys_view():
    clean_inner = {"inner": {"text": CLEAN_TEXT}}
    return {(HashableItem(clean_inner),): 1}.keys()


def check_wrapper_fires(test_case, make_holdout, comparisons=1):
    promote = harness.require("ontoloop.promote")
    bundle = {
        "instruction_items": [
            {"instruction_text": HOLDOUT_TEXT}],
        "holdout_items": make_holdout(),
    }
    outcome = promote.test_instruction_items_against_holdout(
        bundle, occasion="promotion")
    test_case.assertTrue(outcome["fired"])
    shared = outcome["cross_split_audit_result"]
    test_case.assertEqual(shared["comparisons"], comparisons)


def check_direct_fires(test_case, make_bundle, comparisons=1):
    check_fires(test_case, make_bundle, comparisons=comparisons)


class Ruling1189GenericBesideTests(unittest.TestCase):
    """Ruling 1189, identity S15-R26-CROSS-1 merged with
    S15-R26-EVAL-1: the wrapped pair key through a dictionary
    view standing beside a second element inside a generic
    iterable container at the items position fires at the
    direct act and at the evaluation call point, in parity
    with the same presentation standing alone inside the same
    container and with the dataset instruction item surface."""

    def test_keys_view_sequence_beside_string_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            [keys_view(), "x"])})

    def test_keys_view_sequence_beside_none_and_number_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            [keys_view(), None])})
        check_fires(self, lambda: {"items": SequenceCarrier(
            [keys_view(), 2])})

    def test_keys_view_custom_iterable_beside_string_fires(self):
        check_fires(self, lambda: {"items": CustomIterable(
            [keys_view(), "x"])})

    def test_keys_view_once_only_beside_string_fires(self):
        check_fires(self, lambda: {"items": OnceOnlyIterable(
            [keys_view(), "x"])})

    def test_items_view_sequence_beside_string_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            [items_view(), "x"])})

    def test_values_view_sequence_beside_string_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            [values_view(), "x"])})

    def test_string_before_view_in_sequence_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            ["x", keys_view()])})

    def test_beside_sequence_at_position_itself_fires(self):
        check_fires(self, lambda: {
            "items": SequenceCarrier([keys_view(), "x"])})

    def test_beside_sequence_inside_containers_fires(self):
        check_fires(self, lambda: {"items": [[
            SequenceCarrier([keys_view(), "x"])]]})
        check_fires(self, lambda: {"items": (
            SequenceCarrier([keys_view(), "x"]),)})

    def test_beside_generic_clean_clears(self):
        check_clears(self, lambda: {"items": SequenceCarrier(
            [keys_view(), "x"])})
        check_clears(self, lambda: {"items": CustomIterable(
            [keys_view(), "x"])})

    def test_beside_generic_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": SequenceCarrier(
            [keys_view(), "x"])})

    def test_beside_generic_pairs_and_holdout_poles_stand(self):
        check_direct_fires(self, lambda: {"pairs": [
            SequenceCarrier([keys_view(), "x"])]}, comparisons=2)
        check_direct_fires(self, lambda: {"holdout_items": [
            SequenceCarrier([keys_view(), "x"])]}, comparisons=3)
        check_direct_fires(self, lambda: {"holdout_items": [
            [keys_view(), "x"]]}, comparisons=3)


class Ruling1190GenericElementBesideTests(unittest.TestCase):
    """Ruling 1190, identity S15-R26-CROSS-2: the wrapped pair
    key through a dictionary view standing inside a generic
    iterable container standing as an element of a container
    beside a second element at the items position fires at
    the direct act, counted severally from ruling 1189 on the
    presentation geometry ground, its act standing in the one
    act sequence of this region beside the act of ruling 1189."""

    def test_view_in_custom_iterable_in_list_beside_fires(self):
        check_fires(self, lambda: {"items": [
            CustomIterable([keys_view()]), "x"]})

    def test_view_in_sequence_in_list_beside_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([keys_view()]), "x"]})

    def test_view_in_once_only_in_list_beside_fires(self):
        check_fires(self, lambda: {"items": [
            OnceOnlyIterable([keys_view()]), "x"]})

    def test_string_before_sequence_element_fires(self):
        check_fires(self, lambda: {"items": [
            "x", SequenceCarrier([keys_view()])]})

    def test_generic_element_beside_clean_clears(self):
        check_clears(self, lambda: {"items": [
            SequenceCarrier([keys_view()]), "x"]})
        check_clears(self, lambda: {"items": [
            CustomIterable([keys_view()]), "x"]})

    def test_generic_element_beside_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            CustomIterable([keys_view()]), "x"]})

    def test_generic_element_beside_pairs_pole_stands(self):
        check_direct_fires(self, lambda: {"pairs": [
            SequenceCarrier([keys_view()]), "x"]}, comparisons=1)


class Ruling1191DictElementTests(unittest.TestCase):
    """Ruling 1191, identity S15-R26-CROSS-3: the wrapped pair
    key through a keys view standing at a mapping value inside
    a mapping in its exact dict form standing as an element of
    a container at the items position fires at the direct act,
    on the plain mapping limb element reading."""

    def test_keys_view_value_in_dict_in_list_fires(self):
        check_fires(self, lambda: {"items": [{"o": keys_view()}]})

    def test_keys_view_value_in_dict_in_tuple_and_deque_fires(self):
        check_fires(self, lambda: {"items": ({"o": keys_view()},)})
        check_fires(self, lambda: {"items": deque(
            [{"o": keys_view()}])})

    def test_list_subclass_carrier_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": ListSubclassPlain([keys_view()])}]})

    def test_list_subclass_beside_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": ListSubclassPlain([keys_view(), "x"])}]})

    def test_exact_list_beside_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": [keys_view(), "x"]}]})

    def test_generator_in_generator_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": gen_of(gen_of(keys_view()))}]})

    def test_dict_element_clean_clears(self):
        check_clears(self, lambda: {"items": [{"o": keys_view()}]})

    def test_dict_element_standing_poles_stand(self):
        check_fires(self, lambda: {"items": {"o": keys_view()}})
        check_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())])]})
        check_fires(self, lambda: {"items": [{"o": items_view()}]})
        check_fires(self, lambda: {"items": [{"o": values_view()}]})
        check_fires(self, lambda: {"items": [
            {"o": SequenceCarrier([keys_view()])}]})
        check_direct_fires(self, lambda: {"pairs": [
            {"o": keys_view()}]}, comparisons=1)


class Ruling1192DictValueDeepTests(unittest.TestCase):
    """Ruling 1192, identity S15-R26-EVAL-4: the wrapped pair
    key through a keys view standing at a value of an exact
    dict standing inside a container at the items position
    fires at the evaluation call point, on the deep view
    reading, counted severally from ruling 1191."""

    def test_keys_view_in_list_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": [keys_view()]}]})

    def test_keys_view_in_tuple_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": (keys_view(),)}]})

    def test_keys_view_in_generator_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": gen_of(keys_view())}]})

    def test_keys_view_in_gen_in_gen_at_dict_value_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": gen_of(gen_of(keys_view()))}]})

    def test_dict_in_list_in_list_fires(self):
        check_fires(self, lambda: {"items": [[{"o": keys_view()}]]})

    def test_dict_in_generator_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of({"o": keys_view()})]})

    def test_dict_in_sequence_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([{"o": keys_view()}])]})

    def test_dict_in_custom_iterable_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            CustomIterable([{"o": keys_view()}])]})

    def test_dict_with_second_key_fires(self):
        check_fires(self, lambda: {"items": [
            {"o": keys_view(), "p": "z"}]})

    def test_dict_value_clean_clears(self):
        check_clears(self, lambda: {"items": [
            {"o": [keys_view()]}]})

    def test_dict_value_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            {"o": [keys_view()]}]})

    def test_dict_value_standing_pole_stands(self):
        check_fires(self, lambda: {"items": [
            OrderedDict([("o", [keys_view()])])]})


class Ruling1193SequenceViewsTests(unittest.TestCase):
    """Ruling 1193, identity S15-R26-EVAL-2: the wrapped pair
    key through an items view or a values view standing inside
    a Sequence form container at the deep container position
    fires at the items and holdout_items positions at the
    evaluation call point."""

    def test_items_view_in_sequence_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([items_view()])]})

    def test_values_view_in_sequence_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([values_view()])]})

    def test_items_view_in_sequence_subclass_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceSubclass([items_view()])]})

    def test_items_view_in_sequence_in_containers_fires(self):
        check_fires(self, lambda: {"items": (
            SequenceCarrier([items_view()]),)})
        check_fires(self, lambda: {"items": [[
            SequenceCarrier([items_view()])]]})

    def test_items_view_in_sequence_through_iterators_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(SequenceCarrier([items_view()]))]})
        check_fires(self, lambda: {"items": [
            SequenceCarrier([gen_of(items_view())])]})

    def test_views_in_sequence_holdout_items_fire(self):
        check_fires(self, lambda: {"holdout_items": [
            SequenceCarrier([items_view()])]})
        check_fires(self, lambda: {"holdout_items": [
            SequenceCarrier([values_view()])]})

    def test_sequence_views_clean_clears(self):
        check_clears(self, lambda: {"items": [
            SequenceCarrier([items_view()])]})

    def test_sequence_views_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            SequenceCarrier([items_view()])]})


class Ruling1194IndexedOnlyTests(unittest.TestCase):
    """Ruling 1194, identity S15-R26-EVAL-3: the wrapped pair
    key through a keys view standing inside a container
    carrying its elements by indexed access alone at the deep
    container position fires at the items and pairs positions
    at the evaluation call point."""

    def test_keys_view_in_indexed_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            IndexedOnlyCarrier([keys_view()])]})

    def test_keys_view_in_indexed_in_tuple_and_gen_fires(self):
        check_fires(self, lambda: {"items": (
            IndexedOnlyCarrier([keys_view()]),)})
        check_fires(self, lambda: {"items": [
            gen_of(IndexedOnlyCarrier([keys_view()]))]})

    def test_keys_view_in_indexed_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [
            IndexedOnlyCarrier([keys_view()])]})

    def test_keys_view_beside_string_in_indexed_fires(self):
        check_fires(self, lambda: {"items": [
            IndexedOnlyCarrier([keys_view(), "x"])]})

    def test_items_view_in_indexed_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            IndexedOnlyCarrier([items_view()])]})

    def test_sequence_in_indexed_in_list_fires(self):
        check_fires(self, lambda: {"items": [
            IndexedOnlyCarrier([SequenceCarrier([keys_view()])])]})

    def test_indexed_clean_clears(self):
        check_clears(self, lambda: {"items": [
            IndexedOnlyCarrier([keys_view()])]})

    def test_indexed_standing_poles_stand(self):
        check_fires(self, lambda: {
            "items": IndexedOnlyCarrier([keys_view()])})
        check_fires(self, lambda: {"holdout_items": [
            IndexedOnlyCarrier([keys_view()])]})
        check_fires(self, lambda: {"items": [
            IndexedOnlyCarrier([{wrapped_key(): 1}])]})


class Ruling1195DatasetSeamTests(unittest.TestCase):
    """Ruling 1195, identity S15-R26-DATASET-1: key material
    through a keys view standing as a value in a mapping
    standing in a non plain mapping form, that mapping standing
    inside a container at the items position, fires at the
    dataset instruction item surface in parity with the direct
    act and the promote wrapper, its act standing at the seam
    materialisation in cross_split_audit.py, with no act on
    dataset.py in any part."""

    def test_subdict_in_list_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())])]})

    def test_subdict_in_containers_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": (
            SubDict([("o", keys_view())]),)})
        check_dataset_fires(self, lambda: {"items": deque(
            [SubDict([("o", keys_view())])])})
        check_dataset_fires(self, lambda: {"items": UserList(
            [SubDict([("o", keys_view())])])})
        check_dataset_fires(self, lambda: {"items": [[
            SubDict([("o", keys_view())])]]})

    def test_subdict_beside_and_as_value_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())]), "x"]})
        check_dataset_fires(self, lambda: {"items": [
            {"p": SubDict([("o", keys_view())])}]})

    def test_subdict_child_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDictChild([("o", keys_view())])]})

    def test_ordered_and_default_dict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            OrderedDict([("o", keys_view())])]})
        check_dataset_fires(self, lambda: {"items": [
            defaultdict(list, [("o", keys_view())])]})

    def test_counter_and_userdict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            Counter({"o": keys_view()})]})
        check_dataset_fires(self, lambda: {"items": [
            UserDict([("o", keys_view())])]})

    def test_chainmap_and_proxy_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            ChainMap({"o": keys_view()})]})
        check_dataset_fires(self, lambda: {"items": [
            MappingProxyType({"o": keys_view()})]})

    def test_carrier_at_value_in_subdict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", [keys_view()])])]})

    def test_nested_subdict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("p", SubDict([("o", keys_view())]))])]})
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("p", {"o": keys_view()})])]})

    def test_subdict_dataset_clean_poles_clear(self):
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": CLEAN_TEXT}],
                        "holdout_items": {"items": [
                            SubDict([("o", keys_view())])]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            SubDict([("o", clean_keys_view())])]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_subdict_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())])]})
        check_wrapper_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())])]})
        check_dataset_fires(self, lambda: {"pairs": [
            SubDict([("o", keys_view())])]})
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", items_view())])]})
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", values_view())])]})


class ChargedFormsControlsTests(unittest.TestCase):
    """The charged forms of rulings 1026 to 1028 and of
    rulings 1100 to 1104, standing pinned beside the cures
    of this round in their standing forms."""

    def test_exact_list_beside_still_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), "x"]})

    def test_sequence_alone_still_fires(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([keys_view()])]})

    def test_single_iterator_alone_still_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(keys_view()))]})

    def test_delegating_parent_dataset_still_clears(self):
        check_dataset_clears(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})

    def test_exact_two_container_dataset_still_fires(self):
        check_dataset_fires(self, lambda: {"items": [[keys_view()]]})


if __name__ == "__main__":
    unittest.main()
