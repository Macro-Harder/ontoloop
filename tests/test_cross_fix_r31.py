"""Fix round 31 tests for Region 2: cross split readings and seam.

Charges pinned here, from design/steps/step-15-r31-triage.md:
ruling 1673 (a dictionary view of any of the three kinds
standing inside a carrier of any governed kind standing
inside a container in a subclass form of a plain container
at a value of a plain mapping standing at the pairs position
of audit_instruction_item reaching no comparison at the
direct act, at the Eval Finding 1 identity of the Round 31
Eval paper, Low); ruling 1674 (a values view standing inside
a carrier of any governed kind standing inside a container
in a subclass form at a value of a plain mapping standing
at the holdout_items position reaching no comparison at the
direct act, at the Eval Finding 2 identity, Low, counted
severally from ruling 1673 on the geometry ground); ruling
1675 (a keys view or an items view standing inside an
indexed access only carrier standing inside a container in
a subclass form at a value of a plain mapping standing at
the holdout_items position reaching no comparison at the
direct act, at the Eval Finding 3 identity, Low, counted
severally from ruling 1674 on the carrier ground); ruling
1676 (a mapping standing inside a container in a subclass
form of a plain container at a value of a mapping standing
at the pairs position, carrying a view inside a carrier at
its own value, reaching no comparison at the direct act, at
the Eval Finding 4 identity, Low, counted severally from
rulings 1673 to 1675 on the position and geometry grounds);
ruling 1677 (a mapping in the clean view form of ruling
1576 whose storage carries a view in a container wrapped
form, in the combined form of a clean value inner mapping
at its governed entry, clearing at the dataset instruction
item surface beside firing at the direct act and at the
promote wrapper, at the Eval Finding 5 identity, Low,
counted severally from rulings 1681 and 1682 on the seam
ground); ruling 1678 (a wrapped pair key presented through
a dictionary view standing inside a carrier standing inside
a container subclass at a value of a mapping standing at
the pairs position itself reaching no comparison at the
direct act, at the S15-R31-CROSS-1 identity, Low, counted
severally from ruling 1673 on the presentation ground);
ruling 1679 (a values view standing inside a carrier
standing inside a container subclass at a value of a plain
mapping standing at the holdout_items position reaching no
comparison at the direct act, at the S15-R31-CROSS-2
identity, Low, counted severally from rulings 1674 and 1678
on the geometry ground); ruling 1680 (a wrapped pair key
presented through a dictionary view standing inside an
iterator carrier at a value of a mapping in a mappingproxy
form, or in a custom Mapping form, standing at a value of a
mapping standing at the pairs position itself reaching no
comparison at the direct act, at the S15-R31-CROSS-3
identity, Low); ruling 1681 (key material through a
dictionary view standing inside a plain container in the
storage of a mapping whose items reading presents a clean
dictionary view at the governed entry reaching no carried
result at the dataset instruction item surface, at the
S15-R31-CROSS-4 identity, Low, counted severally from
rulings 1677 and 1682 on the seam ground); and ruling 1682
(key material presented through a dictionary view standing
in the storage of a mapping whose items reading presents a
view of the same kind over a mapping carrying the same
entry keys with clean material in the values, in place of
the governed view whose own material stands in the values
of the mapping it stands over, clearing at the dataset
instruction item surface beside firing at the direct act
and at the promote wrapper, at the S15-R31-DATA-1 identity,
Low, counted severally from rulings 1677 and 1681 on the
geometry and side grounds). Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py stands
untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import Counter, OrderedDict, UserDict, deque
from collections.abc import Mapping
from types import MappingProxyType

from tests import harness
from tests.test_cross_fix_r19 import OnceOnlyIterable, direct_pair
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    check_clears,
    check_fires,
    tuple_pair_key,
)
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
)
from tests.test_cross_fix_r26 import (
    CustomIterable,
    IndexedOnlyCarrier,
    SequenceCarrier,
    check_wrapper_fires,
    clean_keys_view,
    gen_of,
)
from tests.test_cross_fix_r29 import clean_value_dict
from tests.test_cross_fix_r30 import (
    check_dataset_clean_poles,
    check_dataset_verbatim_clean_storage_clears,
    clean_view_dict,
)

OCCASIONS = ("candidate construction", "promotion")


class CustomMapping(Mapping):
    """A custom Mapping form carrying its entries in its
    own storage, in the form of the Cross split paper."""

    def __init__(self, data):
        self._data = dict(data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class CleanViewContainerDict(dict):
    """A dict subclass whose items reading presents a clean
    keys view at the governed entry in place of the governed
    view standing inside a plain container in its storage."""

    def items(self):
        return {
            key: (
                clean_keys_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


def container_view_dict(view, wrap):
    return CleanViewContainerDict(
        [("o", wrap(view)), ("c", "plain clean value")])


def governed_values_view():
    return {1: tuple_pair_key()}.values()


def clean_values_view():
    return {1: ("clean pair key",)}.values()


def governed_items_view():
    return {1: tuple_pair_key()}.items()


def clean_items_view():
    return {1: ("clean pair key",)}.items()


class CleanValuesViewDict(dict):
    """A dict subclass whose items reading presents a clean
    values view over a mapping carrying the same entry key
    with a clean pair value at the governed entry, in place
    of the governed values view standing in its storage."""

    def items(self):
        return {
            key: (
                clean_values_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanItemsViewDict(dict):
    """A dict subclass in the same form presenting a clean
    items view at the governed entry."""

    def items(self):
        return {
            key: (
                clean_items_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanItemsFromValuesDict(dict):
    """A dict subclass presenting a clean items view at the
    governed entry in place of a governed values view
    standing in its storage, the kind swap form."""

    def items(self):
        return {
            key: (
                clean_items_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanValuesFromItemsDict(dict):
    """A dict subclass presenting a clean values view at the
    governed entry in place of a governed items view
    standing in its storage, the kind swap form."""

    def items(self):
        return {
            key: (
                clean_values_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CleanValuesViewUserDict(UserDict):
    """A UserDict subclass in the clean values view form."""

    def items(self):
        return {
            key: (
                clean_values_view() if key == "o" else value
            )
            for key, value in self.data.items()
        }.items()


class CleanValuesViewOrderedDict(OrderedDict):
    """An OrderedDict subclass in the clean values view
    form."""

    def items(self):
        return {
            key: (
                clean_values_view() if key == "o" else value
            )
            for key, value in OrderedDict.items(self)
        }.items()


class CleanValuesViewCounter(Counter):
    """A Counter subclass in the clean values view form."""

    def items(self):
        return {
            key: (
                clean_values_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


class CombinedCleanViewDict(dict):
    """A dict subclass in the clean view form of ruling
    1576, whose storage at the governed entry carries a
    mapping in the clean value form of ruling 1473 carrying
    a governed dictionary view in its own storage."""

    def items(self):
        return {
            key: (
                clean_keys_view() if key == "o" else value
            )
            for key, value in dict.items(self)
        }.items()


def combined_dict(inner_view):
    return CombinedCleanViewDict(
        [("o", clean_value_dict(inner_view)),
         ("c", "plain clean value")])


class Ruling1673PairsCarrierInSubclassContainerTests(unittest.TestCase):
    """Ruling 1673, Eval Finding 1: a dictionary view of any
    kind inside a carrier of any governed kind inside a
    container in a subclass form at a value of a plain
    mapping standing at the pairs position fires at the
    direct act, beside the dataset surface firing on the
    same presentations in parity, one ring past the cured
    forms of rulings 1569 to 1577."""

    def test_any_view_in_iterator_carriers_in_list_subclass_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(items_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(values_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([zip([keys_view()])])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([enumerate([values_view()])])}})

    def test_view_in_carriers_in_other_subclass_containers_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": TupleSubclassPlain((zip([keys_view()]),))}})
        check_fires(self, lambda: {"pairs": {
            "o": DequeSubclassPlain(
                [SequenceCarrier([items_view()])])}})
        check_fires(self, lambda: {"pairs": {
            "o": UserListSubclassPlain(
                [IndexedOnlyCarrier([keys_view()])])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([CustomIterable([keys_view()])])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([OnceOnlyIterable([keys_view()])])}})

    def test_carrier_in_subclass_container_at_pairs_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_clears(self, lambda: {"pairs": {
            "o": TupleSubclassPlain((zip([values_view()]),))}})

    def test_carrier_in_subclass_container_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([SequenceCarrier([values_view()])])}})

    def test_pairs_subclass_container_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": [gen_of(keys_view())]}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([keys_view()])}})
        check_wrapper_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})


class Ruling1674HoldoutValuesViewInSubclassContainerTests(
        unittest.TestCase):
    """Ruling 1674, Eval Finding 2: a values view inside a
    carrier of any governed kind inside a container in a
    subclass form at a value of a plain mapping standing at
    the holdout_items position fires at the direct act,
    beside the dataset surface firing in parity, counted
    severally from ruling 1673 on the geometry ground, the
    standing poles of ruling 1673 standing pinned beside
    it."""

    def test_values_view_in_iterator_carriers_in_list_subclass_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([zip([values_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([enumerate([values_view()])])}})

    def test_values_view_in_other_carriers_in_subclass_containers(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([SequenceCarrier([values_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": TupleSubclassPlain((gen_of(values_view()),))}})
        check_fires(self, lambda: {"holdout_items": {
            "o": DequeSubclassPlain([CustomIterable([values_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": UserListSubclassPlain(
                [OnceOnlyIterable([values_view()])])}})

    def test_values_view_in_subclass_container_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})
        check_clears(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([SequenceCarrier([values_view()])])}})

    def test_values_view_in_subclass_container_dataset_fires(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})

    def test_holdout_subclass_container_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(items_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(values_view())]}})


class Ruling1675HoldoutIndexedCarrierInSubclassContainerTests(
        unittest.TestCase):
    """Ruling 1675, Eval Finding 3: a keys view or an items
    view inside an indexed access only carrier inside a
    container in a subclass form at a value of a plain
    mapping standing at the holdout_items position fires at
    the direct act, beside the dataset surface firing in
    its listed form, counted severally from ruling 1674 on
    the carrier ground."""

    def test_keys_and_items_in_indexed_in_list_subclass_fire(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([IndexedOnlyCarrier([keys_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([IndexedOnlyCarrier([items_view()])])}})

    def test_keys_and_items_in_indexed_in_other_subclass_containers(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": TupleSubclassPlain(
                (IndexedOnlyCarrier([keys_view()]),))}})
        check_fires(self, lambda: {"holdout_items": {
            "o": DequeSubclassPlain(
                [IndexedOnlyCarrier([items_view()])])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": UserListSubclassPlain(
                [IndexedOnlyCarrier([keys_view()])])}})

    def test_indexed_in_subclass_container_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([IndexedOnlyCarrier([keys_view()])])}})
        check_clears(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([IndexedOnlyCarrier([items_view()])])}})

    def test_indexed_in_subclass_container_dataset_fires_listed(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([IndexedOnlyCarrier([keys_view()])])}},
            comparisons=2)
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([IndexedOnlyCarrier([items_view()])])}},
            comparisons=2)

    def test_holdout_indexed_subclass_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": IndexedOnlyCarrier([keys_view()])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": [IndexedOnlyCarrier([keys_view()])]}})


class Ruling1676PairsMappingInSubclassContainerTests(unittest.TestCase):
    """Ruling 1676, Eval Finding 4: a mapping standing inside
    a container in a subclass form at a value of a mapping
    standing at the pairs position, carrying a view inside
    a carrier at its own value, fires at the direct act,
    beside the dataset surface firing in parity, counted
    severally from rulings 1673 to 1675 on the position and
    geometry grounds."""

    def test_mapping_in_list_subclass_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([{"p": gen_of(keys_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([{"p": zip([values_view()])}])}})

    def test_mapping_in_other_subclass_containers_at_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": TupleSubclassPlain(({"p": gen_of(keys_view())},))}})
        check_fires(self, lambda: {"pairs": {
            "o": DequeSubclassPlain([{"p": gen_of(keys_view())}])}})
        check_fires(self, lambda: {"pairs": {
            "o": UserListSubclassPlain(
                [{"p": SequenceCarrier([items_view()])}])}})

    def test_mapping_in_subclass_container_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "o": ListSubclassPlain([{"p": gen_of(keys_view())}])}})
        check_clears(self, lambda: {"pairs": {
            "o": DequeSubclassPlain([{"p": gen_of(keys_view())}])}})

    def test_mapping_in_subclass_container_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([{"p": gen_of(keys_view())}])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DequeSubclassPlain([{"p": gen_of(keys_view())}])}})

    def test_pairs_mapping_in_subclass_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": [{"p": gen_of(keys_view())}]}})
        check_fires(self, lambda: {"pairs": {
            "o": {"p": gen_of(keys_view())}}})


class Ruling1677SeamCombinedCleanViewCleanValueTests(unittest.TestCase):
    """Ruling 1677, Eval Finding 5: a mapping in the clean
    view form of ruling 1576 whose storage at the governed
    entry carries a mapping in the clean value form of
    ruling 1473 carrying a governed view in its own storage
    fires at the dataset instruction item surface in parity
    with the direct act and the promote wrapper, counted
    severally from rulings 1681 and 1682 on the seam ground,
    with no act on dataset.py in any part."""

    def test_combined_form_in_list_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            combined_dict(keys_view())]})

    def test_combined_form_in_tuple_and_deque_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": (
            combined_dict(keys_view()),)})
        check_dataset_fires(self, lambda: {"items": [
            deque([combined_dict(keys_view())])]})

    def test_combined_form_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            combined_dict(keys_view())]}, comparisons=2)

    def test_combined_form_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            combined_dict(keys_view())]})
        check_wrapper_fires(self, lambda: {"items": [
            combined_dict(keys_view())]})

    def test_combined_form_clean_poles_clear(self):
        check_clears(self, lambda: {"items": [
            combined_dict(keys_view())]})
        check_dataset_verbatim_clean_storage_clears(
            self, lambda: {"items": [
                combined_dict(clean_keys_view())]})

    def test_combined_form_standing_poles_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})


class Ruling1678CrossPairsSubclassContainerTests(unittest.TestCase):
    """Ruling 1678, identity S15-R31-CROSS-1: a wrapped pair
    key presented through a dictionary view inside a carrier
    inside a container subclass at a value of a mapping
    standing at the pairs position itself fires at the
    direct act, beside the dataset surface firing in parity,
    counted severally from ruling 1673 on the presentation
    ground."""

    def test_wrapped_key_in_carrier_in_list_subclass_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(values_view())])}})

    def test_wrapped_key_in_carrier_in_other_subclasses_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": DequeSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": UserListSubclassPlain([gen_of(keys_view())])}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([{"p": gen_of(keys_view())}])}})

    def test_wrapped_key_in_subclass_container_clean_clears(self):
        check_clears(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_clears(self, lambda: {"pairs": {
            "o": DequeSubclassPlain([gen_of(keys_view())])}})

    def test_wrapped_key_in_subclass_container_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})
        check_dataset_fires(self, lambda: {"pairs": {
            "o": DequeSubclassPlain([gen_of(keys_view())])}})

    def test_cross_pairs_subclass_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": [gen_of(keys_view())]}})
        check_fires(self, lambda: {"pairs": {
            "o": (gen_of(keys_view()),)}})


class Ruling1679CrossHoldoutSubclassContainerTests(unittest.TestCase):
    """Ruling 1679, identity S15-R31-CROSS-2: a values view
    inside a carrier inside a container subclass at a value
    of a plain mapping standing at the holdout_items
    position fires at the direct act, beside the dataset
    surface firing in parity, counted severally from
    rulings 1674 and 1678 on the geometry ground, the
    standing poles of ruling 1678 standing pinned beside
    it."""

    def test_values_view_in_carrier_in_list_subclass_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([zip([values_view()])])}})

    def test_values_view_in_carrier_in_other_subclasses_fires(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": DequeSubclassPlain([gen_of(values_view())])}})
        check_fires(self, lambda: {"holdout_items": {
            "o": UserListSubclassPlain([gen_of(values_view())])}})

    def test_values_view_in_subclass_at_holdout_clean_clears(self):
        check_clears(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})

    def test_values_view_in_subclass_at_holdout_dataset_fires(self):
        check_dataset_fires(self, lambda: {"holdout_items": {
            "o": ListSubclassPlain([gen_of(values_view())])}})

    def test_cross_holdout_subclass_standing_poles_stand(self):
        check_fires(self, lambda: {"holdout_items": {
            "o": [gen_of(values_view())]}})
        check_fires(self, lambda: {"pairs": {
            "o": ListSubclassPlain([gen_of(keys_view())])}})


class Ruling1680PairsMappingProxyCustomMappingTests(unittest.TestCase):
    """Ruling 1680, identity S15-R31-CROSS-3: a wrapped pair
    key presented through a dictionary view inside an
    iterator carrier at a value of a mapping in a
    mappingproxy form, or in a custom Mapping form, standing
    at a value of a mapping standing at the pairs position
    itself fires at the direct act, the dataset surface
    deciding the mappingproxy form in parity and standing
    in no carried form on the custom Mapping form, in the
    forms the Cross split paper states."""

    def test_view_in_iterator_at_mappingproxy_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": MappingProxyType({"p": gen_of(keys_view())})}})
        check_fires(self, lambda: {"pairs": {
            "o": MappingProxyType({"p": zip([values_view()])})}})

    def test_view_in_iterator_at_custom_mapping_pairs_value_fires(self):
        check_fires(self, lambda: {"pairs": {
            "o": CustomMapping({"p": gen_of(keys_view())})}})
        check_fires(self, lambda: {"pairs": {
            "o": CustomMapping({"p": gen_of(items_view())})}})

    def test_mappingproxy_at_pairs_dataset_and_wrapper_fire(self):
        check_dataset_fires(self, lambda: {"pairs": {
            "o": MappingProxyType({"p": gen_of(keys_view())})}})
        check_wrapper_fires(self, lambda: {"pairs": {
            "o": MappingProxyType({"p": gen_of(keys_view())})}})
        check_wrapper_fires(self, lambda: {"pairs": {
            "o": CustomMapping({"p": gen_of(keys_view())})}})

    def test_other_mapping_forms_at_pairs_clean_clear(self):
        check_clears(self, lambda: {"pairs": {
            "o": MappingProxyType({"p": gen_of(keys_view())})}})
        check_clears(self, lambda: {"pairs": {
            "o": CustomMapping({"p": gen_of(keys_view())})}})

    def test_custom_mapping_dataset_standing_pole_stands(self):
        check_dataset_clears(self, lambda: {"pairs": {
            "o": CustomMapping({"p": gen_of(keys_view())})}})

    def test_pairs_other_mapping_standing_poles_stand(self):
        check_fires(self, lambda: {"pairs": {
            "o": {"p": gen_of(keys_view())}}})
        check_fires(self, lambda: {"pairs": {
            "o": UserDict([("p", gen_of(keys_view()))])}})


class Ruling1681SeamContainerWrappedStoredViewTests(unittest.TestCase):
    """Ruling 1681, identity S15-R31-CROSS-4: key material
    through a dictionary view standing inside a plain
    container in the storage of a mapping whose items
    reading presents a clean dictionary view at the
    governed entry fires at the dataset instruction item
    surface in parity with the direct act and the promote
    wrapper, counted severally from rulings 1677 and 1682
    on the seam ground, with no act on dataset.py in any
    part."""

    def test_list_wrapped_stored_view_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(keys_view(), lambda v: [v])]})

    def test_tuple_wrapped_stored_view_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            container_view_dict(keys_view(), lambda v: (v,))]})

    def test_list_wrapped_stored_view_at_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            container_view_dict(keys_view(), lambda v: [v])]},
            comparisons=2)

    def test_container_wrapped_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            container_view_dict(keys_view(), lambda v: [v])]})
        check_wrapper_fires(self, lambda: {"items": [
            container_view_dict(keys_view(), lambda v: [v])]})

    def test_container_wrapped_clean_poles_clear(self):
        check_clears(self, lambda: {"items": [
            container_view_dict(keys_view(), lambda v: [v])]})
        check_dataset_verbatim_clean_storage_clears(
            self, lambda: {"items": [
                container_view_dict(
                    clean_keys_view(), lambda v: [v])]})

    def test_container_wrapped_standing_poles_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            clean_view_dict(keys_view())]})
        check_dataset_fires(self, lambda: {"items": [
            clean_value_dict(keys_view())]})


class Ruling1682SeamValueSideSubstitutionTests(unittest.TestCase):
    """Ruling 1682, identity S15-R31-DATA-1: key material
    presented through a dictionary view standing in the
    storage of a mapping whose items reading presents a
    view of the same kind over a mapping carrying the same
    entry keys with clean material in the values, in place
    of the governed view whose own material stands in the
    values of the mapping it stands over, fires at the
    dataset instruction item surface in parity with the
    direct act and the promote wrapper, counted severally
    from rulings 1677 and 1681 on the geometry and side
    grounds, with no act on dataset.py in any part."""

    def test_values_view_same_keys_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})

    def test_items_view_same_keys_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanItemsViewDict(
                [("o", governed_items_view()),
                 ("c", "plain clean value")])]})

    def test_kind_swap_forms_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanItemsFromValuesDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanValuesFromItemsDict(
                [("o", governed_items_view()),
                 ("c", "plain clean value")])]})

    def test_value_side_subclass_and_container_forms_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            CleanValuesViewUserDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanValuesViewOrderedDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_dataset_fires(self, lambda: {"items": [
            CleanValuesViewCounter(
                {"o": governed_values_view(),
                 "c": "plain clean value"})]})
        check_dataset_fires(self, lambda: {"items": (
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")]),)})
        check_dataset_fires(self, lambda: {"items": {
            "x": CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])}})

    def test_value_side_direct_and_wrapper_fire(self):
        check_fires(self, lambda: {"items": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_wrapper_fires(self, lambda: {"items": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})

    def test_value_side_clean_poles_clear(self):
        check_clears(self, lambda: {"items": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_dataset_clean_poles(self, lambda: {"items": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_dataset_verbatim_clean_storage_clears(
            self, lambda: {"items": [
                CleanValuesViewDict(
                    [("o", clean_values_view()),
                     ("c", "plain clean value")])]})

    def test_value_side_pairs_parity_pole_stands(self):
        check_clears(self, lambda: {"pairs": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})
        check_dataset_clears(self, lambda: {"pairs": [
            CleanValuesViewDict(
                [("o", governed_values_view()),
                 ("c", "plain clean value")])]})


class ChargedFormsControlsTests(unittest.TestCase):
    """The charged forms of rulings 1026 and 1102 and of
    ruling 722, standing pinned beside the cures of this
    round in their standing forms, in the form the Fix
    round 30 Region 2 pin file states them."""

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
