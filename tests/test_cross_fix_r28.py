"""Fix round 28 tests for Region 2: cross split readings and seam.

Charges pinned here, from design/steps/step-15-r28-triage.md:
ruling 1374 (the cross split audit wrapped pair key presented
through a dictionary view standing inside an iterator
container, a generic iterable container, or an indexed access
container standing at a value of a mapping standing at the
pairs position itself, reaching no comparison at the direct
act while the dataset instruction item surface reaches the
same material, at the S15-R28-CROSS-1 identity, Low); ruling
1375 (key material through a dictionary view standing as a
value in a mapping whose items reading presents a proper
subset of its entries, the seam rebuild carrying entries but
not the governed entry and the presented carries reading
standing blind to the governed entry it carries, clearing at
the dataset instruction item surface beside a firing at the
direct act and at the promote wrapper, at the
S15-R28-DATA-1 identity, Low); and ruling 1376 (key material
through a keys view standing as a value in a dict form whose
items and keys readings both present no entry, its presented
carries reading standing blind to its stored entries,
clearing at the dataset instruction item surface beside a
firing at the direct act and at the promote wrapper, at the
S15-R28-DATA-2 identity, Low, counted severally from ruling
1375 on the reading ground). Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py stands
untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import OrderedDict, UserDict

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
    SubDict,
    check_wrapper_fires,
    clean_keys_view,
    gen_of,
)

OCCASIONS = ("candidate construction", "promotion")


class SubsetItemsDict(dict):
    """A dict subclass whose items reading presents a proper
    subset of its entries, omitting the governed entry under
    the key o and presenting the clean entry beside it."""

    def items(self):
        return {
            key: value
            for key, value in dict.items(self)
            if key != "o"
        }.items()


class SubsetItemsUserDict(UserDict):
    """A UserDict subclass in the same items reading form."""

    def items(self):
        return {
            key: value
            for key, value in self.data.items()
            if key != "o"
        }.items()


class SubsetItemsOrderedDict(OrderedDict):
    """An OrderedDict subclass in the same items reading
    form."""

    def items(self):
        return {
            key: value
            for key, value in OrderedDict.items(self)
            if key != "o"
        }.items()


class NoItemsNoKeysDict(dict):
    """A dict subclass whose items reading and whose keys
    reading each present no entry, its governed entry
    standing in the storage the subclass carries."""

    def items(self):
        return {}.items()

    def keys(self):
        return {}.keys()


class NoItemsNoKeysUserDict(UserDict):
    """A UserDict subclass in the same reading form, standing
    in parity at the dataset surface in its standing form
    because the presented carries reading reads the mapping
    a UserDict wraps."""

    def items(self):
        return {}.items()

    def keys(self):
        return {}.keys()


class NoItemsDict(dict):
    """A dict subclass whose items reading presents no
    entry, the charged form of ruling 1281."""

    def items(self):
        return {}.items()


class ParamDict(dict):
    """A dict subclass whose constructor carries a further
    required parameter ahead of its data, a charged form of
    ruling 1281 beside it."""

    def __init__(self, tag, data=None):
        super().__init__(data if data is not None else {})


def subset_dict(view):
    return SubsetItemsDict([("o", view), ("c", "plain clean value")])


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


class Ruling1374PairsPositionMappingTests(unittest.TestCase):
    """Ruling 1374, identity S15-R28-CROSS-1: a wrapped pair
    key through a dictionary view inside an iterator, generic
    iterable, or indexed access carrier at a value of a
    mapping standing at the pairs position itself fires at
    the direct act, beside the dataset surface firing on the
    same presentations in parity, one ring past the cured
    form of ruling 1277 at the position that cure stands
    scoped away from."""

    def test_view_in_iterator_carriers_at_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": gen_of(keys_view())}})
        check_fires(self, lambda: {"pairs": {
            "o": gen_of(gen_of(keys_view()))}})
        check_fires(self, lambda: {"pairs": {
            "o": zip([keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": map(lambda element: element, [keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": enumerate([keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": reversed([keys_view()])}})

    def test_view_in_generic_carriers_at_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": SequenceCarrier([keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": CustomIterable([keys_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": IndexedOnlyCarrier([keys_view()])}})

    def test_view_at_value_of_non_plain_pairs_mapping_fires(self):
        check_fires(self, lambda: {"pairs": SubDict(
            [("o", gen_of(keys_view()))])})
        check_fires(self, lambda: {"pairs": OrderedDict(
            [("o", gen_of(keys_view()))])})

    def test_items_and_values_views_in_carriers_at_pairs_fire(self):
        check_fires(self, lambda: {"pairs": {
            "o": gen_of(items_view())}})
        check_fires(self, lambda: {"pairs": {
            "o": IndexedOnlyCarrier([items_view()])}})
        check_fires(self, lambda: {"pairs": {
            "o": SequenceCarrier([values_view()])}})

    def test_pairs_position_mapping_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"pairs": {
            "o": gen_of(keys_view())}})
        check_clears(self, lambda: {"pairs": {
            "o": SequenceCarrier([keys_view()])}})

    def test_pairs_position_mapping_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": gen_of(keys_view())}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": SequenceCarrier([keys_view()])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": IndexedOnlyCarrier([keys_view()])}})

    def test_pairs_position_mapping_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {"o": keys_view()}})
        check_fires(self, lambda: {"pairs": {
            "o": [keys_view()]}})
        check_fires(self, lambda: {"pairs": {
            "o": (keys_view(),)}})
        check_fires(self, lambda: {"pairs": {
            "o": [keys_view(), "x"]}}, comparisons=2)
        check_fires(self, lambda: {"pairs": [
            {"o": gen_of(keys_view())}]})


class Ruling1375SeamSubsetItemsTests(unittest.TestCase):
    """Ruling 1375, identity S15-R28-DATA-1: key material
    through a dictionary view standing as a value in a
    mapping whose items reading presents a proper subset of
    its entries fires at the dataset instruction item
    surface in parity with the direct act and the promote
    wrapper, the loss standing on the seam materialisation
    together with the ruling 1281 guard in its landed form,
    its act standing at the seam readings in
    cross_split_audit.py, with no act on dataset.py in any
    part."""

    def test_subset_dict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})

    def test_subset_dict_in_tuple_and_beside_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": (
            subset_dict(keys_view()),)})
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(keys_view()), "x"]})

    def test_subset_dict_items_view_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(items_view())]})

    def test_subset_userdict_and_ordered_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            SubsetItemsUserDict(
                [("o", keys_view()), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            SubsetItemsOrderedDict(
                [("o", keys_view()), ("c", "plain clean value")])]})

    def test_subset_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            subset_dict(keys_view())]}, comparisons=2)
        check_dataset_fires(self, lambda: {"pairs": [
            SubsetItemsUserDict(
                [("o", keys_view()), ("c", "plain clean value")])]},
            comparisons=2)

    def test_subset_direct_and_wrapper_poles_fire(self):
        check_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})

    def test_subset_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            subset_dict(keys_view())]})
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            subset_dict(clean_keys_view())]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_subset_standing_poles_of_ruling_1281_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            NoItemsDict([("o", keys_view())])]})
        check_dataset_fires(self, lambda: {"items": [
            ParamDict("t", [("o", keys_view())])]})


class Ruling1376SeamNoItemsNoKeysTests(unittest.TestCase):
    """Ruling 1376, identity S15-R28-DATA-2: key material
    through a keys view standing as a value in a dict form
    whose items and keys readings both present no entry
    fires at the dataset instruction item surface in parity
    with the direct act and the promote wrapper, the loss
    standing on the presented limb of the ruling 1281 guard,
    counted severally from ruling 1375 on the reading
    ground, the standing poles of ruling 1375 standing
    pinned beside it."""

    def test_no_items_no_keys_dict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            NoItemsNoKeysDict([("o", keys_view())])]})

    def test_no_items_no_keys_dict_beside_and_tuple_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            NoItemsNoKeysDict(
                [("o", keys_view()), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": (
            NoItemsNoKeysDict([("o", keys_view())]),)})

    def test_no_items_no_keys_dict_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            NoItemsNoKeysDict([("o", keys_view())])]})

    def test_no_items_no_keys_userdict_parity_pole_stands(self):
        check_dataset_fires(self, lambda: {"items": [
            NoItemsNoKeysUserDict([("o", keys_view())])]})
        check_fires(self, lambda: {"items": [
            NoItemsNoKeysUserDict([("o", keys_view())])]})

    def test_no_items_no_keys_direct_and_wrapper_poles_fire(self):
        check_fires(self, lambda: {"items": [
            NoItemsNoKeysDict([("o", keys_view())])]})
        check_wrapper_fires(self, lambda: {"items": [
            NoItemsNoKeysDict([("o", keys_view())])]})

    def test_no_items_no_keys_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            NoItemsNoKeysDict([("o", keys_view())])]})
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            NoItemsNoKeysDict(
                                [("o", clean_keys_view())])]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_no_items_no_keys_standing_pole_of_ruling_1375(self):
        check_dataset_fires(self, lambda: {"items": [
            subset_dict(keys_view())]})


class ChargedFormsControlsTests(unittest.TestCase):
    """The charged forms of rulings 1026 and 1102 and of
    ruling 722, standing pinned beside the cures of this
    round in their standing forms, ruling 722 standing as
    the bound the pairs position act of ruling 1374 stands
    charged against in the open."""

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
