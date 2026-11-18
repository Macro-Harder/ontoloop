"""Fix round 30 tests for Region 2: cross split readings and seam.

Charges pinned here, from design/steps/step-15-r30-triage.md:
ruling 1569 (a dictionary view of any of the three kinds
standing inside a carrier of any governed kind standing
inside a plain container at a value of a plain mapping
standing at the pairs position of audit_instruction_item
reaching no comparison at the direct act, at the Eval
Finding 1 identity of the Round 30 Eval paper, Low);
ruling 1570 (a values view standing inside a carrier of
any governed kind standing inside a plain container at a
value of a plain mapping standing at the holdout_items
position reaching no comparison at the direct act, at the
Eval Finding 2 identity, Low, counted severally from
ruling 1569 on the position and view ground); ruling 1571
(a keys view or an items view standing inside an indexed
access only carrier standing inside a plain container at
a value of a plain mapping standing at the holdout_items
position reaching no comparison at the direct act, at the
Eval Finding 3 identity, Low, counted severally from
ruling 1570 on the carrier ground); ruling 1572 (a
dictionary view of any of the three kinds standing inside
an iterator or single pass carrier standing inside a list
at a value of a plain mapping standing at the items
position reaching no comparison at the direct act, at the
Eval Finding 4 identity, Low, counted severally from
rulings 1569 to 1571 on the position and carrier ground);
ruling 1573 (a wrapped pair key presented through a
dictionary view standing inside an iterator carrier at a
value of a UserDict or ChainMap standing at a value of a
mapping standing at the pairs position itself reaching no
comparison at the direct act, at the S15-R30-CROSS-1
identity, Low); ruling 1574 (a wrapped pair key presented
through a dictionary view standing inside an iterator
carrier at a value of a mapping standing inside a list or
tuple standing at a value of a mapping standing at the
pairs position itself reaching no comparison at the
direct act, at the S15-R30-CROSS-2 identity, Low, counted
severally from ruling 1573 on the container ground);
ruling 1575 (key material through a dictionary view in
the storage of a mapping whose items reading presents
every entry key with a dictionary view over clean key
material at the governed entry reaching no carried result
at the dataset instruction item surface, the seam rebuild
standing in no blind form on a view for view substitution,
at the S15-R30-CROSS-3 identity, Low); ruling 1576 (key
material presented through a dictionary view standing in
the storage of a mapping whose items reading presents a
clean dictionary view at the governed entry in place of
the governed view, that mapping standing inside a
container at the items position, clearing at the dataset
instruction item surface beside a firing at the direct act
and at the promote wrapper, at the S15-R30-DATA-1 identity,
Low, counted severally from ruling 1575 on the geometry
and side grounds); and ruling 1577 (key material presented
through a dictionary view standing in the storage of a
mapping standing as the storage value at the governed
entry of a second mapping, the inner mapping and the outer
mapping each in the clean value form of ruling 1473,
clearing at the dataset instruction item surface beside a
firing at the direct act and at the promote wrapper, at
the S15-R30-DATA-2 identity, Low, counted severally from
ruling 1576 on the reading ground). Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py stands
untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import ChainMap, Counter, OrderedDict, UserDict, UserList, deque

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
from tests.test_cross_fix_r29 import (
    CleanValueCounter,
    CleanValueDict,
    CleanValueOrderedDict,
    CleanValueUserDict,
    clean_value_dict,
)

OCCASIONS = ("candidate construction", "promotion")


class CleanViewDict(dict):
    """A dict subclass whose items reading presents every
    entry key it carries, the governed entry included, but
    presents a clean keys view over clean key material at
    the governed entry in place of the governed view
    standing in its storage."""

    def items(self):
        return {
            key: (
                clean_keys_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanViewItemsDict(dict):
    """A dict subclass in the same form presenting a clean
    items view at the governed entry."""

    def items(self):
        clean = {("clean pair key",): 1}
        return {
            key: (
                clean.items() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanViewUserDict(UserDict):
    """A UserDict subclass in the clean view form, its
    governed view standing in the mapping it wraps."""

    def items(self):
        return {
            key: (
                clean_keys_view() if key == "o" else value
            )
            for key, value in self.data.items()
        }.items()


class CleanViewOrderedDict(OrderedDict):
    """An OrderedDict subclass in the clean view form."""

    def items(self):
        return {
            key: (
                clean_keys_view() if key == "o" else value
            )
            for key, value in OrderedDict.items(self)
        }.items()


class CleanViewCounter(Counter):
    """A Counter subclass in the clean view form."""

    def items(self):
        return {
            key: (
                clean_keys_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


def clean_view_dict(view):
    return CleanViewDict(
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


def check_dataset_verbatim_clean_storage_clears(test_case, make_holdout):
    dataset = harness.require("ontoloop.dataset")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = dataset.test_instruction_items_against_holdout(
                {
                    "instruction_items": [
                        {"text": HOLDOUT_TEXT}],
                    "holdout_items": make_holdout(),
                },
                occasion=occasion)
            test_case.assertFalse(result["fired"])


class Ruling1569PairsCarrierInContainerTests(unittest.TestCase):
    """Ruling 1569, Eval Finding 1: a dictionary view of
    any kind inside a carrier of any governed kind inside
    a plain container at a value of a plain mapping
    standing at the pairs position fires at the direct
    act, beside the dataset surface firing on the same
    presentations in parity, one ring past the cured forms
    of rulings 1280, 1374, and 1469."""

    def test_any_view_in_iterator_carriers_in_list_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": [gen_of(keys_view())]}})
        check_fires(self, lambda: {"pairs": {
            "o": [gen_of(items_view())]}})
        check_fires(self, lambda: {"pairs": {
            "o": [gen_of(values_view())]}})
        check_fires(self, lambda: {"pairs": {
            "o": [zip([keys_view()])]}})
        check_fires(self, lambda: {"pairs": {
            "o": [enumerate([values_view()])]}})

    def test_view_in_other_carriers_in_containers_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": (zip([keys_view()]),)}})
        check_fires(self, lambda: {"pairs": {
            "o": deque([SequenceCarrier([keys_view()])])}})
        check_fires(self, lambda: {"pairs": {
            "o": UserList([IndexedOnlyCarrier([keys_view()])])}})
        check_fires(self, lambda: {"pairs": {
            "o": [CustomIterable([keys_view()])]}})
        check_fires(self, lambda: {"pairs": {
            "o": [OnceOnlyIterable([keys_view()])]}})

    def test_carrier_in_container_at_pairs_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "o": [gen_of(keys_view())]}})
        check_clears(self, lambda: {"pairs": {
            "o": (zip([values_view()]),)}})

    def test_carrier_in_container_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": [gen_of(keys_view())]}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": [SequenceCarrier([values_view()])]}})

    def test_pairs_carrier_in_container_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": gen_of(keys_view())}})
        check_fires(self, lambda: {"pairs": {
            "o": [keys_view()]}})
        check_fires(self, lambda: {"pairs": {
            "o": (values_view(),)}})


class Ruling1570HoldoutValuesViewInContainerTests(unittest.TestCase):
    """Ruling 1570, Eval Finding 2: a values view inside a
    carrier of any governed kind inside a plain container
    at a value of a plain mapping standing at the
    holdout_items position fires at the direct act, beside
    the dataset surface firing on the same presentations
    in parity, counted severally from ruling 1569 on the
    position and view ground."""

    def test_values_view_in_iterator_carriers_in_list_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(values_view())]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [zip([values_view()])]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [enumerate([values_view()])]}})

    def test_values_view_in_other_carriers_in_containers_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": [SequenceCarrier([values_view()])]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [CustomIterable([values_view()])]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [OnceOnlyIterable([values_view()])]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": (gen_of(values_view()),)}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [[gen_of(values_view())]]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ([gen_of(values_view())],)}})

    def test_values_view_in_container_at_holdout_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": [gen_of(values_view())]}})
        check_clears(self, lambda: {"holdout_items": {
            "o": [SequenceCarrier([values_view()])]}})

    def test_values_view_in_container_at_holdout_dataset_fires(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(values_view())]}})

    def test_holdout_container_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(keys_view())]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(items_view())]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": gen_of(values_view())}})


class Ruling1571HoldoutIndexedCarrierInContainerTests(unittest.TestCase):
    """Ruling 1571, Eval Finding 3: a keys view or an items
    view inside an indexed access only carrier inside a
    plain container at a value of a plain mapping standing
    at the holdout_items position fires at the direct act,
    beside the dataset surface firing on the same
    presentations in its listed form, counted severally
    from ruling 1570 on the carrier ground."""

    def test_keys_and_items_in_indexed_in_list_at_holdout_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([keys_view()])]}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([items_view()])]}})

    def test_keys_and_items_in_indexed_in_other_containers_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": (IndexedOnlyCarrier([keys_view()]),)}})
        check_fires(self, lambda: {"holdout_items": {
            "o": deque([IndexedOnlyCarrier([items_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": UserList([IndexedOnlyCarrier([keys_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [[IndexedOnlyCarrier([keys_view()])]]}})

    def test_indexed_in_container_at_holdout_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([keys_view()])]}})
        check_clears(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([items_view()])]}})

    def test_indexed_in_container_at_holdout_dataset_fires_listed(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([keys_view()])]}},
            comparisons=2)
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([items_view()])]}},
            comparisons=2)

    def test_holdout_indexed_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([keys_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([values_view()])}})


class Ruling1572ItemsIteratorCarrierInListTests(unittest.TestCase):
    """Ruling 1572, Eval Finding 4: a dictionary view of
    any kind inside an iterator or single pass carrier
    inside a list at a value of a plain mapping standing
    at the items position fires at the direct act, beside
    the dataset surface firing on the same presentations
    in parity, counted severally from rulings 1569 to 1571
    on the position and carrier ground."""

    def test_any_view_in_iterator_carriers_in_list_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            "o": [gen_of(keys_view())]}})
        check_fires(self, lambda: {"items": {
            "o": [gen_of(items_view())]}})
        check_fires(self, lambda: {"items": {
            "o": [gen_of(values_view())]}})

    def test_any_view_in_zip_and_enumerate_in_list_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            "o": [zip([keys_view()])]}})
        check_fires(self, lambda: {"items": {
            "o": [enumerate([keys_view()])]}})
        check_fires(self, lambda: {"items": {
            "o": [zip([values_view()])]}})
        check_fires(self, lambda: {"items": {
            "o": [enumerate([items_view()])]}})

    def test_iterator_in_list_at_items_clean_clears(self):
        check_clears(self, lambda: {"items": {
            "o": [gen_of(keys_view())]}})
        check_clears(self, lambda: {"items": {
            "o": [zip([values_view()])]}})

    def test_iterator_in_list_at_items_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": {
            "o": [gen_of(keys_view())]}})
        check_dataset_fires(self, lambda: {"items": {
            "o": [enumerate([values_view()])]}})

    def test_items_iterator_in_list_standing_poles_stand(self):
        check_fires(self, lambda: {"items": {
            "o": gen_of(keys_view())}})
        check_fires(self, lambda: {"items": {
            "o": (gen_of(keys_view()),)}})
        check_fires(self, lambda: {"items": {
            "o": [SequenceCarrier([keys_view()])]}})


class Ruling1573PairsUserDictChainMapNestedTests(unittest.TestCase):
    """Ruling 1573, identity S15-R30-CROSS-1: a wrapped
    pair key presented through a dictionary view inside an
    iterator carrier at a value of a UserDict or ChainMap
    standing at a value of a mapping standing at the pairs
    position itself fires at the direct act, beside the
    dataset surface firing on the same presentations in
    parity, one ring past the cured form of ruling 1469."""

    def test_view_in_iterator_at_userdict_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": UserDict([("p", gen_of(keys_view()))])}})
        check_fires(self, lambda: {"pairs": {
            "o": UserDict([("p", zip([items_view()]))])}})

    def test_view_in_iterator_at_chainmap_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": ChainMap({"p": gen_of(keys_view())})}})
        check_fires(self, lambda: {"pairs": {
            "o": ChainMap({"p": SequenceCarrier([values_view()])})}})

    def test_userdict_one_mapping_level_deeper_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": {"q": UserDict([("p", gen_of(keys_view()))])}}})
        check_fires(self, lambda: {"pairs": {
            "o": {"q": ChainMap({"p": gen_of(keys_view())})}}})

    def test_userdict_chainmap_at_pairs_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "o": UserDict([("p", gen_of(keys_view()))])}})
        check_clears(self, lambda: {"pairs": {
            "o": ChainMap({"p": gen_of(keys_view())})}})

    def test_userdict_chainmap_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": UserDict([("p", gen_of(keys_view()))])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": ChainMap({"p": gen_of(keys_view())})}})

    def test_pairs_nested_mapping_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": Counter({"p": gen_of(keys_view())})}})
        check_fires(self, lambda: {"pairs": {
            "o": UserDict([("p", keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": gen_of(keys_view())}}})


class Ruling1574PairsMappingInContainerTests(unittest.TestCase):
    """Ruling 1574, identity S15-R30-CROSS-2: a wrapped
    pair key presented through a dictionary view inside an
    iterator carrier at a value of a mapping standing
    inside a list or tuple standing at a value of a mapping
    standing at the pairs position itself fires at the
    direct act, beside the dataset surface firing on the
    same presentations in parity, counted severally from
    ruling 1573 on the container ground."""

    def test_mapping_in_list_at_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": [{"p": gen_of(keys_view())}]}})
        check_fires(self, lambda: {"pairs": {
            "o": [{"p": zip([values_view()])}]}})

    def test_mapping_in_tuple_at_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": ({"p": gen_of(keys_view())},)}})
        check_fires(self, lambda: {"pairs": {
            "o": ({"p": SequenceCarrier([items_view()])},)}})

    def test_mapping_in_container_at_pairs_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "o": [{"p": gen_of(keys_view())}]}})
        check_clears(self, lambda: {"pairs": {
            "o": ({"p": gen_of(keys_view())},)}})

    def test_mapping_in_container_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": [{"p": gen_of(keys_view())}]}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": ({"p": gen_of(keys_view())},)}})

    def test_pairs_mapping_in_container_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": [
            {"o": gen_of(keys_view())}]})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": keys_view()}}})


class Ruling1575SeamViewForViewTests(unittest.TestCase):
    """Ruling 1575, identity S15-R30-CROSS-3: key material
    through a dictionary view in the storage of a mapping
    whose items reading presents every entry key with a
    dictionary view over clean key material at the
    governed entry fires at the dataset instruction item
    surface in parity with the direct act and the promote
    wrapper, the seam rebuild standing in no blind form on
    a view for view substitution in the form of ruling
    1473, with no act on dataset.py in any part."""

    def test_clean_view_dict_in_list_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})

    def test_clean_view_dict_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            clean_view_dict(keys_view())]}, comparisons=2)

    def test_clean_view_dict_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})

    def test_clean_view_dict_clean_poles_clear(self):
        check_clears(self, lambda: {"items": [
            clean_view_dict(keys_view())]})
        check_dataset_verbatim_clean_storage_clears(
            self, lambda: {"items": [
                clean_view_dict(clean_keys_view())]})

    def test_clean_view_standing_pole_of_1473_stands(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})


class Ruling1576SeamCleanViewSubstitutionTests(unittest.TestCase):
    """Ruling 1576, identity S15-R30-DATA-1: key material
    presented through a dictionary view standing in the
    storage of a mapping whose items reading presents a
    clean dictionary view at the governed entry in place
    of the governed view, that mapping standing inside a
    container at the items position, fires at the dataset
    instruction item surface in parity with the direct act
    and the promote wrapper, counted severally from ruling
    1575 on the geometry and side grounds, with no act on
    dataset.py in any part."""

    def test_clean_view_subclass_forms_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanViewUserDict(
                [("o", keys_view()), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanViewOrderedDict(
                [("o", keys_view()), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanViewCounter(
                {"o": keys_view(), "c": "plain clean value"})]})

    def test_clean_view_other_stored_views_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_view_dict(items_view())]})
        check_dataset_fires(self, lambda: {"items": [
            clean_view_dict(values_view())]})

    def test_clean_items_view_presented_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanViewItemsDict(
                [("o", keys_view()), ("c", "plain clean value")])]})

    def test_clean_view_tuple_and_mapping_value_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": (
            clean_view_dict(keys_view()),)})
        check_dataset_fires(self, lambda: {"items": {
            "x": clean_view_dict(keys_view())}})

    def test_clean_view_direct_and_wrapper_poles_fire(self):
        check_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})

    def test_clean_view_clean_poles_clear(self):
        check_clears(self, lambda: {"items": [
            clean_view_dict(keys_view())]})
        check_dataset_verbatim_clean_storage_clears(
            self, lambda: {"items": [
                clean_view_dict(clean_keys_view())]})


def nested_clean_value_form(inner):
    return CleanValueDict(
        [("o", inner), ("c", "plain clean value")])


def nested_outer(inner_view):
    return nested_clean_value_form(
        clean_value_dict(inner_view))


class Ruling1577SeamNestedCleanValueTests(unittest.TestCase):
    """Ruling 1577, identity S15-R30-DATA-2: key material
    presented through a dictionary view standing in the
    storage of a mapping standing as the storage value at
    the governed entry of a second mapping, the inner
    mapping and the outer mapping each in the clean value
    form of ruling 1473, fires at the dataset instruction
    item surface in parity with the direct act and the
    promote wrapper, counted severally from ruling 1576 on
    the reading ground, with no act on dataset.py in any
    part."""

    def test_nested_clean_value_in_list_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            nested_outer(keys_view())]})

    def test_nested_clean_value_inner_subclass_forms_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            nested_clean_value_form(CleanValueUserDict(
                [("o", keys_view()), ("c", "plain clean value")]))]})
        check_dataset_fires(self, lambda: {"items": [
            nested_clean_value_form(CleanValueOrderedDict(
                [("o", keys_view()), ("c", "plain clean value")]))]})
        check_dataset_fires(self, lambda: {"items": [
            nested_clean_value_form(CleanValueCounter(
                {"o": keys_view(), "c": "plain clean value"}))]})
        check_dataset_fires(self, lambda: {"items": [
            nested_clean_value_form(nested_clean_value_form(
                clean_value_dict(keys_view())))]})
        check_dataset_fires(self, lambda: {"items": (
            nested_outer(keys_view()),)})
        check_dataset_fires(self, lambda: {"items": [
            CleanValueDict(
                [("o", [clean_value_dict(keys_view())]),
                 ("c", "plain clean value")])]})

    def test_nested_clean_value_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            nested_outer(keys_view())]}, comparisons=2)

    def test_nested_clean_value_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            nested_outer(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            nested_outer(keys_view())]})

    def test_nested_clean_value_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            nested_outer(keys_view())]})
        check_dataset_verbatim_clean_storage_clears(
            self, lambda: {"items": [
                nested_outer(clean_keys_view())]})

    def test_nested_clean_value_storage_neighbours_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanValueDict(
                [("o", [keys_view()]), ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})


class ChargedFormsControlsTests(unittest.TestCase):
    """The charged forms of rulings 1026 and 1102 and of
    ruling 722, standing pinned beside the cures of this
    round in their standing forms, in the form the Fix
    round 29 Region 2 pin file states them."""

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
