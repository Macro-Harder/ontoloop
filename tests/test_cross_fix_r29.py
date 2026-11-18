"""Fix round 29 tests for Region 2: cross split readings and seam.

Charges pinned here, from design/steps/step-15-r29-triage.md:
ruling 1467 (a values view standing inside an iterator,
single pass, Sequence form, or generic iterable carrier at
a value of a plain mapping standing at the holdout_items
position of audit_instruction_item reaching no comparison
at the direct act, beside a firing at the dataset
instruction item surface and a refusal at the bundle
surfaces, at the Eval Finding 1 identity of the Round 29
Eval paper, Low); ruling 1468 (a dictionary view of any of
the three kinds standing inside an indexed access only
carrier at a value of a plain mapping standing at the
holdout_items position reaching no comparison at the
direct act, beside the same sibling decisions, at the Eval
Finding 2 identity, Low, counted severally from ruling
1467 on the carrier ground); ruling 1469 (a wrapped pair
key presented through a dictionary view standing inside
an iterator or Sequence carrier at a value of a mapping
standing at a value of a mapping standing at the pairs
position itself reaching no comparison at the direct act,
at the S15-R29-CROSS-1 identity, Low); ruling 1470 (key
material through a dictionary view standing as a value in
a dict form whose items reading, keys reading, and
iteration each present a proper subset of its entries
omitting the governed entry reaching no carried result at
the dataset instruction item surface, at the
S15-R29-CROSS-2 identity, Low); ruling 1471 (key material
through a keys view standing as a value in a dict form
whose items reading, keys reading, and iteration each
present no entry reaching no carried result at the dataset
instruction item surface, at the S15-R29-CROSS-3 identity,
Low, counted severally from ruling 1470 on the reading
ground); ruling 1472 (the dict form of ruling 1470 standing
as an element of a list at the pairs position raising an
index error at the direct act and at the promote wrapper
and reaching no carried result at the dataset instruction
item surface, at the S15-R29-CROSS-4 identity, Low); and
ruling 1473 (key material presented through a dictionary
view standing in the storage of a mapping whose items
reading presents every entry key it carries, the governed
entry included, but presents a clean plain value at the
governed entry in place of the governed view, that mapping
standing inside a container at the items position, clearing
at the dataset instruction item surface beside a firing at
the direct act and at the promote wrapper, at the
S15-R29-DATA-1 identity, Low). Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py stands
untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import Counter, OrderedDict, UserDict

from tests import harness
from tests.test_cross_fix_r19 import OnceOnlyIterable, direct_pair
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    check_clears,
    check_fires,
)
from tests.test_cross_fix_r24 import (
    check_dataset_fires,
    items_view,
    keys_view,
    values_view,
)
from tests.test_cross_fix_r26 import (
    CustomIterable,
    IndexedOnlyCarrier,
    SequenceCarrier,
    check_wrapper_fires,
    clean_keys_view,
    gen_of,
)
from tests.test_cross_fix_r28 import (
    NoItemsNoKeysUserDict,
    subset_dict,
)

OCCASIONS = ("candidate construction", "promotion")


class AllReadingsSubsetDict(dict):
    """A dict subclass whose items reading, keys reading,
    and iteration each present a proper subset of its
    entries, omitting the governed entry under the key o
    and presenting the clean entry beside it, its governed
    entry standing in the storage the subclass carries."""

    def _presented(self):
        return {
            key: value
            for key, value in dict.items(self)
            if key != "o"
        }

    def items(self):
        return self._presented().items()

    def keys(self):
        return self._presented().keys()

    def __iter__(self):
        return iter(self._presented())


class AllReadingsEmptyDict(dict):
    """A dict subclass whose items reading, keys reading,
    and iteration each present no entry, its governed
    entry standing in the storage the subclass carries."""

    def items(self):
        return {}.items()

    def keys(self):
        return {}.keys()

    def __iter__(self):
        return iter(())


class CleanValueDict(dict):
    """A dict subclass whose items reading presents every
    entry key it carries, the governed entry included, but
    presents a clean plain value at the governed entry in
    place of the governed view standing in its storage."""

    def items(self):
        return {
            key: (
                "plain clean value" if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanValueUserDict(UserDict):
    """A UserDict subclass in the same items reading form,
    its governed view standing in the mapping it wraps."""

    def items(self):
        return {
            key: (
                "plain clean value" if key == "o" else value
            )
            for key, value in self.data.items()
        }.items()


class CleanValueOrderedDict(OrderedDict):
    """An OrderedDict subclass in the same items reading
    form."""

    def items(self):
        return {
            key: (
                "plain clean value" if key == "o" else value
            )
            for key, value in OrderedDict.items(self)
        }.items()


class CleanValueCounter(Counter):
    """A Counter subclass in the same items reading form."""

    def items(self):
        return {
            key: (
                "plain clean value" if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


def subset_all_dict(view):
    return AllReadingsSubsetDict(
        [("o", view), ("c", "plain clean value")])


def empty_all_dict(view):
    return AllReadingsEmptyDict(
        [("o", view), ("c", "plain clean value")])


def clean_value_dict(view):
    return CleanValueDict(
        [("o", view), ("c", "plain clean value")])


def check_dataset_clean_poles(test_case, make_holdout):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                {
                    "instruction_items": [
                        {"text": CLEAN_TEXT}],
                    "holdout_items": make_holdout(),
                },
                occasion=occasion)
            test_case.assertFalse(result["fired"])


class Ruling1467HoldoutValuesViewCarrierTests(unittest.TestCase):
    """Ruling 1467, Eval Finding 1: a values view standing
    inside an iterator, single pass, Sequence form, or
    generic iterable carrier at a value of a plain mapping
    standing at the holdout_items position fires at the
    direct act, beside the dataset surface firing on the
    same presentations in parity, one ring past the cured
    forms of rulings 1279, 1280, and 1374."""

    def test_values_view_in_iterator_carriers_at_holdout_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": gen_of(values_view())}})
        check_fires(self, lambda: {"holdout_items": {
            "o": gen_of(gen_of(values_view()))}})
        check_fires(self, lambda: {"holdout_items": {
            "o": zip([values_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": enumerate([values_view()])}})

    def test_values_view_in_sequence_and_generic_carriers_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": SequenceCarrier([values_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": CustomIterable([values_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": OnceOnlyIterable([values_view()])}})

    def test_values_view_at_holdout_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": gen_of(values_view())}})
        check_clears(self, lambda: {"holdout_items": {
            "o": SequenceCarrier([values_view()])}})

    def test_values_view_at_holdout_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": gen_of(values_view())}})
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": SequenceCarrier([values_view()])}})

    def test_holdout_values_view_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": values_view()}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [values_view()]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": (values_view(),)}})
        check_fires(self, lambda: {"holdout_items": {
            "o": gen_of(keys_view())}})
        check_fires(self, lambda: {"holdout_items": {
            "o": gen_of(items_view())}})


class Ruling1468HoldoutIndexedOnlyCarrierTests(unittest.TestCase):
    """Ruling 1468, Eval Finding 2: a dictionary view of
    any of the three kinds standing inside an indexed
    access only carrier at a value of a plain mapping
    standing at the holdout_items position fires at the
    direct act, beside the dataset surface firing on the
    same presentations in parity, counted severally from
    ruling 1467 on the carrier ground."""

    def test_any_view_in_indexed_carrier_at_holdout_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([keys_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([items_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([values_view()])}})

    def test_indexed_carrier_at_holdout_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([keys_view()])}})

    def test_indexed_carrier_at_holdout_dataset_fires(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([values_view()])}})

    def test_indexed_keys_at_holdout_dataset_fires_listed(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([keys_view()])}},
            comparisons=2)

    def test_indexed_carrier_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": IndexedOnlyCarrier([keys_view()])}})
        check_fires(self, lambda: {"items": {
            "o": IndexedOnlyCarrier([keys_view()])}})


class Ruling1469PairsNestedMappingTests(unittest.TestCase):
    """Ruling 1469, identity S15-R29-CROSS-1: a wrapped
    pair key presented through a dictionary view standing
    inside an iterator or Sequence carrier at a value of
    a mapping standing at a value of a mapping standing
    at the pairs position itself fires at the direct act,
    beside the dataset surface firing on the same
    presentations in parity, one ring past the cured form
    of ruling 1374 in mapping depth."""

    def test_view_in_iterator_at_nested_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": {"p": gen_of(keys_view())}}})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": gen_of(gen_of(keys_view()))}}})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": zip([keys_view()])}}})

    def test_view_in_other_carriers_at_nested_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": {"p": SequenceCarrier([items_view()])}}})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": IndexedOnlyCarrier([values_view()])}}})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": CustomIterable([keys_view()])}}})

    def test_nested_pairs_mapping_subclass_forms_fire(self):
        check_fires(self, lambda: {"pairs": {
            "o": dict([("p", gen_of(keys_view()))])}})
        check_fires(self, lambda: {"pairs": OrderedDict(
            [("o", {"p": gen_of(keys_view())})])})

    def test_view_at_third_mapping_level_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": {"p": {"q": gen_of(keys_view())}}}})

    def test_nested_pairs_value_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"pairs": {
            "o": {"p": gen_of(keys_view())}}})
        check_clears(self, lambda: {"pairs": {
            "o": {"p": SequenceCarrier([keys_view()])}}})

    def test_nested_pairs_value_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": {"p": gen_of(keys_view())}}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": {"p": SequenceCarrier([keys_view()])}}})

    def test_nested_pairs_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": {"p": keys_view()}}})
        check_fires(self, lambda: {"pairs": [
            {"o": gen_of(keys_view())}]})


class Ruling1470SeamAllReadingsSubsetTests(unittest.TestCase):
    """Ruling 1470, identity S15-R29-CROSS-2: key material
    through a dictionary view standing as a value in a
    dict form whose items reading, keys reading, and
    iteration each present a proper subset of its entries
    omitting the governed entry fires at the dataset
    instruction item surface in parity with the direct
    act and the promote wrapper, one ring past the cured
    forms of rulings 1375 and 1376."""

    def test_all_readings_subset_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_all_dict(keys_view())]})

    def test_all_readings_subset_items_view_and_tuple_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_all_dict(items_view())]})
        check_dataset_fires(self, lambda: {"items": (
            subset_all_dict(keys_view()),)})

    def test_all_readings_subset_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            subset_all_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            subset_all_dict(keys_view())]})

    def test_all_readings_subset_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            subset_all_dict(keys_view())]})
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            subset_all_dict(clean_keys_view())]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_all_readings_subset_standing_pole_of_1375(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})


class Ruling1471SeamAllReadingsEmptyTests(unittest.TestCase):
    """Ruling 1471, identity S15-R29-CROSS-3: key material
    through a keys view standing as a value in a dict
    form whose items reading, keys reading, and iteration
    each present no entry fires at the dataset instruction
    item surface in parity with the direct act and the
    promote wrapper, counted severally from ruling 1470
    on the reading ground."""

    def test_all_readings_empty_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            empty_all_dict(keys_view())]})

    def test_all_readings_empty_beside_tuple_and_pairs_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            empty_all_dict(keys_view()), "x"]})
        check_dataset_fires(self, lambda: {"items": (
            empty_all_dict(keys_view()),)})
        check_dataset_fires(self, lambda: {"pairs": [
            empty_all_dict(keys_view())]})

    def test_all_readings_empty_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            empty_all_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            empty_all_dict(keys_view())]})

    def test_all_readings_empty_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            empty_all_dict(keys_view())]})
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            empty_all_dict(clean_keys_view())]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_all_readings_empty_standing_poles_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})
        check_dataset_fires(self, lambda: {"items": [
            NoItemsNoKeysUserDict([("o", keys_view())])]})


class Ruling1472PairsAllReadingsSubsetCrashTests(unittest.TestCase):
    """Ruling 1472, identity S15-R29-CROSS-4: the dict
    form of ruling 1470 standing as an element of a list
    at the pairs position stands carried in a decided
    form at every governed surface, firing on the hit
    forms and clearing on the clean forms, no exception
    standing in place of the decision."""

    def test_all_readings_subset_at_pairs_direct_fires(self):
        check_fires(self, lambda: {"pairs": [
            subset_all_dict(keys_view())]})

    def test_all_readings_subset_at_pairs_wrapper_fires(self):
        check_wrapper_fires(self, lambda: {"pairs": [
            subset_all_dict(keys_view())]})

    def test_all_readings_subset_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            subset_all_dict(keys_view())]})

    def test_all_readings_subset_at_pairs_clean_clears(self):
        check_clears(self, lambda: {"pairs": [
            subset_all_dict(keys_view())]})
        check_dataset_clean_poles(self, lambda: {"pairs": [
            subset_all_dict(keys_view())]})

    def test_all_readings_subset_at_pairs_poles_stand(self):
        check_fires(self, lambda: {"items": [
            subset_all_dict(keys_view())]})
        check_fires(self, lambda: {"pairs": [
            empty_all_dict(keys_view())]})


class Ruling1473SeamCleanValueSubstitutionTests(unittest.TestCase):
    """Ruling 1473, identity S15-R29-DATA-1: key material
    presented through a dictionary view standing in the
    storage of a mapping whose items reading presents a
    clean plain value at the governed entry, that mapping
    standing inside a container at the items position,
    fires at the dataset instruction item surface in
    parity with the direct act and the promote wrapper,
    one ring beyond the cure of ruling 1375 on the rebuild
    ground, with no act on dataset.py in any part."""

    def test_clean_value_dict_in_list_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})

    def test_clean_value_subclass_forms_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanValueUserDict(
                [("o", keys_view()), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanValueOrderedDict(
                [("o", keys_view()), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanValueCounter(
                {"o": keys_view(), "c": "plain clean value"})]})

    def test_clean_value_other_views_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(items_view())]})
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(values_view())]})

    def test_clean_value_tuple_and_mapping_value_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": (
            clean_value_dict(keys_view()),)})
        check_dataset_fires(self, lambda: {"items": {
            "x": clean_value_dict(keys_view())}})

    def test_clean_value_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            clean_value_dict(keys_view())]}, comparisons=2)

    def test_clean_value_direct_and_wrapper_poles_fire(self):
        check_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})

    def test_clean_value_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            clean_value_dict(keys_view())]})
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            clean_value_dict(clean_keys_view())]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_clean_value_standing_pole_of_1375_stands(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})


class ChargedFormsControlsTests(unittest.TestCase):
    """The charged forms of rulings 1026 and 1102 and of
    ruling 722, standing pinned beside the cures of this
    round in their standing forms, in the form the Fix
    round 28 Region 2 pin file states them."""

    def test_exact_list_beside_still_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), "x"]})

    def test_single_iterator_alone_still_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(keys_view()))]})

    def test_ruling_722_single_pass_mapping_value_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "key": OnceOnlyIterable(direct_pair())}})
        check_fires(self, lambda: {"pairs": {
            "key": OnceOnlyIterable([0, direct_pair()])}})

    def test_ruling_722_single_pass_mapping_value_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "key": OnceOnlyIterable(direct_pair())}})


if __name__ == "__main__":
    unittest.main()
