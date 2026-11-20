"""Fix round 27 tests for Region 2: cross split readings and seam.

Charges pinned here, from design/steps/step-15-r27-triage.md:
ruling 1277 (the cross split audit wrapped pair key presented
through a dictionary view standing inside an iterator container,
a generic iterable container, or an indexed access container
standing at a value of a mapping standing at the items position
itself, reaching no comparison at the direct act, at the
S15-R27-CROSS-1 identity, Low); ruling 1278 (the same key
through a view inside a carrier of those forms standing at a
value of a mapping standing in a non plain mapping form
standing as an element of a container, at the S15-R27-CROSS-2
identity, Low, counted severally from ruling 1277 on the
presentation geometry ground); ruling 1279 (the wrapped pair
key through an items view or a values view standing beside a
second element inside a tuple, a deque, or a UserList standing
as the position value itself, in defect at the items position
at the evaluation call point, at the S15-R27-EVAL-1 identity,
Low); ruling 1280 (the same key through a view beside a second
element inside a re-iterable container standing inside a
Sequence form carrier or an indexed access only carrier, at
the S15-R27-EVAL-2 identity, Low, counted severally from
ruling 1279); ruling 1281 (key material through a keys view
standing as a value in a mapping standing in a non plain
mapping form inside a container at the items position,
clearing at the dataset instruction item surface beside a
firing at the direct act and at the promote wrapper, the loss
standing on the seam rebuilt mapping reading standing empty
of the governed entry, at the S15-R27-DATASET-1 identity,
Low); ruling 1282 (key material through a keys view standing
inside a single pass form standing as a value in a non plain
mapping inside a container, firing at the dataset surface
beside a clearing at the direct act, at the
S15-R27-DATASET-2 identity, Low, counted severally from
ruling 1281 on the direction ground); ruling 1283 (key
material through a dictionary view standing as a value in a
ChainMap subclass standing inside a container, firing at the
dataset surface beside a clearing at the direct act and at
the promote wrapper, the delegating subclass form, at the
S15-R27-DATASET-3 identity, Low); and ruling 1289 (the same
material through a view standing as a value in a plain
ChainMap subclass standing inside a container, firing at the
dataset surface where the direct act and the promote wrapper
clear it, at the S15-R27-SPAN-1 identity, Low, counted
severally from ruling 1283 on the carrier ground). The acts
of rulings 1277 and 1278 stand in the one act sequence of
this region, as do the acts of rulings 1279 and 1280 and the
acts of rulings 1283 and 1289, no act graded landed alone on
the parity form. Every cure stands on
ontoloop/cross_split_audit.py alone; dataset.py stands
untouched in full under this charge, and
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import ChainMap, Counter, OrderedDict, UserDict, UserList, defaultdict, deque
from types import MappingProxyType

from tests import harness
from tests.test_cross_fix_r20 import (
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    check_clears,
    check_fires,
)
from tests.test_cross_fix_r24 import (
    DequeSubclassPlain,
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
    SubDict,
    check_wrapper_fires,
    clean_keys_view,
    gen_of,
)
from tests.test_promote_fix_r22 import (
    ListSubclass as DelegatingListSubclass,
)

OCCASIONS = ("candidate construction", "promotion")


class PlainChainMapSubclass(ChainMap):
    """A plain ChainMap subclass carrying no override of
    any act among them."""


class PlainChainMapSubclassChild(PlainChainMapSubclass):
    """A plain subclass of the ChainMap subclass above."""


class DelegatingChainMapSubclass(ChainMap):
    """A ChainMap subclass whose readings delegate to a
    stored ChainMap it carries."""

    def __init__(self, *maps):
        self._stored = ChainMap(*maps)

    @property
    def maps(self):
        return self._stored.maps

    @maps.setter
    def maps(self, value):
        self._stored.maps = value


class ParamDict(dict):
    """A dict subclass whose constructor carries a further
    required parameter ahead of its data."""

    def __init__(self, tag, data=None):
        super().__init__(data if data is not None else {})


class ParamUserDict(UserDict):
    """A UserDict subclass in the same constructor form."""

    def __init__(self, tag, data=None):
        super().__init__(data if data is not None else {})


class NoItemsDict(dict):
    """A dict subclass whose items reading presents no
    entry."""

    def items(self):
        return {}.items()


class NoItemsUserDict(UserDict):
    """A UserDict subclass in the same reading form."""

    def items(self):
        return {}.items()


class RaisingDict(dict):
    """A dict subclass whose constructor raises on the one
    argument rebuild, its further parameter standing
    keyword only and required."""

    def __init__(self, data=None, *, tag):
        super().__init__(data if data is not None else {})


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


class Ruling1277PositionMappingTests(unittest.TestCase):
    """Ruling 1277, identity S15-R27-CROSS-1: a wrapped pair
    key through a dictionary view inside an iterator, generic
    iterable, or indexed access carrier at a value of a
    mapping standing at the items position itself fires at
    the direct act, beside the dataset surface firing on the
    same presentations in parity."""

    def test_view_in_iterator_carriers_at_value_fires(self):
        check_fires(self, lambda: {"items": {
            "o": gen_of(keys_view())}})
        check_fires(self, lambda: {"items": {
            "o": gen_of(gen_of(keys_view()))}})
        check_fires(self, lambda: {"items": {
            "o": zip([keys_view()])}})
        check_fires(self, lambda: {"items": {
            "o": map(lambda element: element, [keys_view()])}})
        check_fires(self, lambda: {"items": {
            "o": enumerate([keys_view()])}})
        check_fires(self, lambda: {"items": {
            "o": reversed([keys_view()])}})

    def test_view_in_generic_carriers_at_value_fires(self):
        check_fires(self, lambda: {"items": {
            "o": SequenceCarrier([keys_view()])}})
        check_fires(self, lambda: {"items": {
            "o": CustomIterable([keys_view()])}})
        check_fires(self, lambda: {"items": {
            "o": IndexedOnlyCarrier([keys_view()])}})

    def test_view_in_beside_carriers_at_value_fires(self):
        check_fires(self, lambda: {"items": {
            "o": SequenceCarrier([keys_view(), "x"])}})
        check_fires(self, lambda: {"items": {
            "o": [gen_of(keys_view()), "x"]}})

    def test_view_at_value_of_non_plain_position_mapping_fires(self):
        check_fires(self, lambda: {"items": SubDict(
            [("o", gen_of(keys_view()))])})
        check_fires(self, lambda: {"items": OrderedDict(
            [("o", gen_of(keys_view()))])})

    def test_items_and_values_views_in_carriers_at_value_fire(self):
        check_fires(self, lambda: {"items": {
            "o": gen_of(items_view())}})
        check_fires(self, lambda: {"items": {
            "o": IndexedOnlyCarrier([items_view()])}})
        check_fires(self, lambda: {"items": {
            "o": SequenceCarrier([values_view()])}})

    def test_position_mapping_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"items": {
            "o": gen_of(keys_view())}})
        check_clears(self, lambda: {"items": {
            "o": SequenceCarrier([keys_view(), "x"])}})

    def test_position_mapping_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": {
            "o": gen_of(keys_view())}})
        check_dataset_fires(self, lambda: {"items": {
            "o": SequenceCarrier([keys_view()])}})
        check_dataset_fires(self, lambda: {"items": {
            "o": IndexedOnlyCarrier([keys_view()])}})

    def test_position_mapping_standing_poles_stand(self):
        check_fires(self, lambda: {"items": {"o": keys_view()}})
        check_fires(self, lambda: {"items": {
            "o": [keys_view()]}})
        check_fires(self, lambda: {"items": {
            "o": [keys_view(), "x"]}})
        check_fires(self, lambda: {"items": {
            "o": (keys_view(),)}})
        check_fires(self, lambda: {"items": [
            {"o": gen_of(keys_view())}]})


class Ruling1278NonPlainElementTests(unittest.TestCase):
    """Ruling 1278, identity S15-R27-CROSS-2: a wrapped pair
    key through a dictionary view inside an iterator, generic
    iterable, or indexed access carrier at a value of a
    mapping standing in a non plain mapping form standing as
    an element of a container fires at the direct act,
    counted severally from ruling 1277 on the presentation
    geometry ground, its act standing in the one act sequence
    of this region beside the act of ruling 1277."""

    def test_view_in_generator_at_value_of_non_plain_elements_fires(self):
        check_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            OrderedDict([("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            ChainMap({"o": gen_of(keys_view())})]})
        check_fires(self, lambda: {"items": [
            UserDict([("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            defaultdict(list, [("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            MappingProxyType({"o": gen_of(keys_view())})]})

    def test_view_in_further_carriers_at_subdict_value_fires(self):
        check_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(gen_of(keys_view())))])]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", SequenceCarrier([keys_view()]))])]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", CustomIterable([keys_view()]))])]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", IndexedOnlyCarrier([keys_view()]))])]})

    def test_subdict_element_in_further_containers_fires(self):
        check_fires(self, lambda: {"items": (
            SubDict([("o", gen_of(keys_view()))]),)})
        check_fires(self, lambda: {"items": deque(
            [SubDict([("o", gen_of(keys_view()))])])})
        check_fires(self, lambda: {"items": UserList(
            [SubDict([("o", gen_of(keys_view()))])])})

    def test_items_and_values_views_at_subdict_value_fire(self):
        check_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(items_view()))])]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", SequenceCarrier([values_view()]))])]})

    def test_subdict_element_pairs_position_fires(self):
        check_fires(self, lambda: {"pairs": [
            SubDict([("o", gen_of(keys_view()))])]})

    def test_non_plain_element_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_clears(self, lambda: {"items": [
            SubDict([("o", SequenceCarrier([keys_view()]))])]})

    def test_non_plain_element_dataset_fires_in_parity(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_dataset_fires(self, lambda: {"items": [
            OrderedDict([("o", gen_of(keys_view()))])]})

    def test_non_plain_element_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [
            {"o": gen_of(keys_view())}]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())])]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", [keys_view()])])]})
        check_fires(self, lambda: {"holdout_items": [
            SubDict([("o", gen_of(keys_view()))])]}, comparisons=2)


class Ruling1279BesidePositionValueTests(unittest.TestCase):
    """Ruling 1279, identity S15-R27-EVAL-1: a wrapped pair
    key through an items view or a values view standing
    beside a second element inside a tuple, a deque, or a
    UserList standing as the position value itself fires at
    the items position at the evaluation call point, the
    direct act deciding through the same shared act."""

    def test_items_view_beside_in_tuple_deque_userlist_fires(self):
        check_fires(self, lambda: {"items": (items_view(), "x")})
        check_fires(self, lambda: {"items": deque(
            [items_view(), "x"])})
        check_fires(self, lambda: {"items": UserList(
            [items_view(), "x"])})

    def test_values_view_beside_in_tuple_deque_userlist_fires(self):
        check_fires(self, lambda: {"items": (values_view(), "x")})
        check_fires(self, lambda: {"items": deque(
            [values_view(), "x"])})
        check_fires(self, lambda: {"items": UserList(
            [values_view(), "x"])})

    def test_items_view_beside_in_plain_subclass_containers_fires(self):
        check_fires(self, lambda: {"items": TupleSubclassPlain(
            (items_view(), "x"))})
        check_fires(self, lambda: {"items": DequeSubclassPlain(
            [items_view(), "x"])})
        check_fires(self, lambda: {"items": UserListSubclassPlain(
            [items_view(), "x"])})

    def test_items_view_beside_further_elements_fires(self):
        check_fires(self, lambda: {"items": (items_view(), None)})
        check_fires(self, lambda: {"items": (items_view(), 2)})
        check_fires(self, lambda: {"items": ("x", items_view())})
        check_fires(self, lambda: {"items": (
            items_view(), "x", "y")})

    def test_beside_position_value_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"items": (items_view(), "x")})
        check_clears(self, lambda: {"items": deque(
            [values_view(), "x"])})

    def test_beside_position_value_standing_poles_stand(self):
        check_fires(self, lambda: {"items": (items_view(),)})
        check_fires(self, lambda: {"items": [items_view(), "x"]})
        check_fires(self, lambda: {"items": (keys_view(), "x")})


class Ruling1280BesideNestedCarrierTests(unittest.TestCase):
    """Ruling 1280, identity S15-R27-EVAL-2: a wrapped pair
    key through an items view or a values view standing
    beside a second element inside a re-iterable container
    standing inside a Sequence form carrier or an indexed
    access only carrier fires at the items position at the
    evaluation call point, counted severally from ruling
    1279 on the presentation geometry ground, its act
    standing in the one act sequence of this region beside
    the act of ruling 1279."""

    def test_items_view_beside_in_inner_containers_in_sequence_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            [(items_view(), "x")])})
        check_fires(self, lambda: {"items": SequenceCarrier(
            [deque([items_view(), "x"])])})
        check_fires(self, lambda: {"items": SequenceCarrier(
            [UserList([items_view(), "x"])])})
        check_fires(self, lambda: {"items": SequenceCarrier(
            [[items_view(), "x"]])})

    def test_items_view_beside_in_inner_containers_in_indexed_fires(self):
        check_fires(self, lambda: {"items": IndexedOnlyCarrier(
            [(items_view(), "x")])})
        check_fires(self, lambda: {"items": IndexedOnlyCarrier(
            [deque([items_view(), "x"])])})
        check_fires(self, lambda: {"items": IndexedOnlyCarrier(
            [UserList([items_view(), "x"])])})
        check_fires(self, lambda: {"items": IndexedOnlyCarrier(
            [[items_view(), "x"]])})

    def test_values_view_beside_in_tuple_in_sequence_fires(self):
        check_fires(self, lambda: {"items": SequenceCarrier(
            [(values_view(), "x")])})

    def test_beside_carrier_inside_containers_fires(self):
        check_fires(self, lambda: {"items": [SequenceCarrier(
            [(items_view(), "x")])]})
        check_fires(self, lambda: {"items": [IndexedOnlyCarrier(
            [(items_view(), "x")])]})

    def test_beside_nested_carrier_clean_clears_on_comparison(self):
        check_clears(self, lambda: {"items": SequenceCarrier(
            [(items_view(), "x")])})

    def test_beside_nested_carrier_standing_poles_stand(self):
        check_fires(self, lambda: {"items": [
            SequenceCarrier([items_view()])]})
        check_fires(self, lambda: {"items": SequenceCarrier(
            [(keys_view(), "x")])})
        check_fires(self, lambda: {"items": CustomIterable(
            [(items_view(), "x")])})
        check_fires(self, lambda: {"items": gen_of(
            (items_view(), "x"))})


class Ruling1281SeamRebuiltEmptyTests(unittest.TestCase):
    """Ruling 1281, identity S15-R27-DATASET-1: key material
    through a keys view standing as a value in a mapping
    standing in a non plain mapping form inside a container
    at the items position fires at the dataset instruction
    item surface in parity with the direct act and the
    promote wrapper, where the seam rebuild stands empty of
    the governed entry, its act standing at the rebuilt
    mapping reading in cross_split_audit.py, with no act on
    dataset.py in any part."""

    def test_param_dict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            ParamDict("t", [("o", keys_view())])]})

    def test_param_userdict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            ParamUserDict("t", [("o", keys_view())])]})

    def test_param_dict_beside_and_pairs_dataset_fire(self):
        check_dataset_fires(self, lambda: {"items": [
            ParamDict("t", [("o", keys_view())]), "x"]})
        check_dataset_fires(self, lambda: {"pairs": [
            ParamDict("t", [("o", keys_view())])]})

    def test_no_items_dict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            NoItemsDict([("o", keys_view())])]})

    def test_no_items_userdict_dataset_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            NoItemsUserDict([("o", keys_view())])]})

    def test_no_items_dict_pairs_dataset_fires(self):
        check_dataset_fires(self, lambda: {"pairs": [
            NoItemsDict([("o", keys_view())])]})

    def test_rebuilt_empty_direct_and_wrapper_poles_fire(self):
        check_fires(self, lambda: {"items": [
            ParamDict("t", [("o", keys_view())])]})
        check_fires(self, lambda: {"items": [
            NoItemsDict([("o", keys_view())])]})
        check_wrapper_fires(self, lambda: {"items": [
            ParamDict("t", [("o", keys_view())])]})
        check_wrapper_fires(self, lambda: {"items": [
            NoItemsUserDict([("o", keys_view())])]})

    def test_rebuilt_empty_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            ParamDict("t", [("o", keys_view())])]})
        dataset = harness.require("ontoloop.dataset")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = dataset.test_instruction_items_against_holdout(
                    {
                        "instruction_items": [
                            {"text": HOLDOUT_TEXT}],
                        "holdout_items": {"items": [
                            NoItemsDict([("o", clean_keys_view())])]},
                    },
                    occasion=occasion)
                self.assertFalse(result["fired"])

    def test_raising_constructor_standing_pole_fires(self):
        check_dataset_fires(self, lambda: {"items": [
            RaisingDict([("o", keys_view())], tag="t")]})
        check_fires(self, lambda: {"items": [
            RaisingDict([("o", keys_view())], tag="t")]})


class Ruling1282SeamSinglePassValueTests(unittest.TestCase):
    """Ruling 1282, identity S15-R27-DATASET-2: key material
    through a keys view standing inside a single pass form
    standing as a value in a non plain mapping inside a
    container at the items position stands decided at the
    dataset instruction item surface in the form the direct
    act states, in parity at every governed surface under
    the parity form of Section D of the triage and the
    counsel of ruling 1333, the single pass forms of this
    ruling standing on the same presentations as the
    iterator carrier forms of ruling 1278, whose cure in
    the one act sequence of this region extends the direct
    act readings to them, counted severally from ruling
    1281 on the direction ground, the bound contradiction
    between the counting no comparison clause of this
    ruling and the cure of ruling 1278 standing disclosed
    in the builder paper of this region in the open."""

    def test_generator_value_in_non_plain_mappings_fires_in_parity(self):
        check_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            OrderedDict([("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            UserDict([("o", gen_of(keys_view()))])]})
        check_fires(self, lambda: {"items": [
            ChainMap({"o": gen_of(keys_view())})]})
        check_fires(self, lambda: {"items": [
            Counter({"o": gen_of(keys_view())})]})
        check_fires(self, lambda: {"items": [
            MappingProxyType({"o": gen_of(keys_view())})]})
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_dataset_fires(self, lambda: {"items": [
            ChainMap({"o": gen_of(keys_view())})]})

    def test_generator_value_pairs_fires_in_parity(self):
        check_fires(self, lambda: {"pairs": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_dataset_fires(self, lambda: {"pairs": [
            SubDict([("o", gen_of(keys_view()))])]})

    def test_further_single_pass_values_fire_in_parity(self):
        check_fires(self, lambda: {"items": [
            SubDict([("o", iter([keys_view()]))])]})
        check_fires(self, lambda: {"items": [
            SubDict([("o", gen_of([keys_view()]))])]})
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", iter([keys_view()]))])]})

    def test_single_pass_value_wrapper_pole_stands(self):
        check_wrapper_fires(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})

    def test_single_pass_value_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})
        check_clears(self, lambda: {"items": [
            SubDict([("o", gen_of(keys_view()))])]})

    def test_single_pass_value_standing_poles_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", [keys_view()])])]})
        check_dataset_fires(self, lambda: {"items": [
            {"o": gen_of(keys_view())}]})
        check_dataset_fires(self, lambda: {"items": [
            SubDict([("o", keys_view())])]})


class Ruling1283SeamDelegatingChainMapTests(unittest.TestCase):
    """Ruling 1283, identity S15-R27-DATASET-3: key material
    through a dictionary view standing as a value in a
    ChainMap subclass in its delegating form, that subclass
    standing inside a container at the items position,
    counts no comparison at the dataset instruction item
    surface, in the form the direct act and the promote
    wrapper state, counted severally from ruling 1289 on
    the carrier ground, its act standing in the one act
    sequence of this region beside the act of ruling 1289."""

    def test_delegating_chainmap_dataset_clears(self):
        check_dataset_clears(self, lambda: {"items": [
            DelegatingChainMapSubclass({"o": keys_view()})]})
        check_dataset_clears(self, lambda: {"items": [
            DelegatingChainMapSubclass({"o": items_view()})]})

    def test_delegating_chainmap_in_tuple_dataset_clears(self):
        check_dataset_clears(self, lambda: {"items": (
            DelegatingChainMapSubclass({"o": keys_view()}),)})

    def test_delegating_chainmap_direct_and_wrapper_poles_clear(self):
        check_direct_clears_zero(self, lambda: {"items": [
            DelegatingChainMapSubclass({"o": keys_view()})]})
        check_wrapper_clears(self, lambda: {"items": [
            DelegatingChainMapSubclass({"o": keys_view()})]})

    def test_delegating_chainmap_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            DelegatingChainMapSubclass({"o": keys_view()})]})


class Ruling1289SeamPlainChainMapSubclassTests(unittest.TestCase):
    """Ruling 1289, identity S15-R27-SPAN-1: key material
    through a dictionary view standing as a value in a
    plain ChainMap subclass standing inside a container at
    the items position counts no comparison at the dataset
    instruction item surface, where the direct act and the
    promote wrapper clear it, counted severally from ruling
    1283 on the carrier ground, its act standing in the one
    act sequence of this region beside the act of ruling
    1283, neither act graded landed alone on the parity
    form."""

    def test_plain_chainmap_subclass_dataset_clears(self):
        check_dataset_clears(self, lambda: {"items": [
            PlainChainMapSubclass({"o": keys_view()})]})
        check_dataset_clears(self, lambda: {"items": [
            PlainChainMapSubclassChild({"o": keys_view()})]})
        check_dataset_clears(self, lambda: {"items": [
            PlainChainMapSubclass({"o": items_view()})]})
        check_dataset_clears(self, lambda: {"items": [
            PlainChainMapSubclass({"o": values_view()})]})

    def test_plain_chainmap_subclass_in_further_positions_clears(self):
        check_dataset_clears(self, lambda: {"items": (
            PlainChainMapSubclass({"o": keys_view()}),)})
        check_dataset_clears(self, lambda: {"items": [
            {"p": PlainChainMapSubclass({"o": keys_view()})}]})
        check_dataset_clears(self, lambda: {"items": [[
            PlainChainMapSubclass({"o": keys_view()})]]})
        check_dataset_clears(self, lambda: {
            "items": PlainChainMapSubclass({"o": keys_view()})})

    def test_plain_chainmap_subclass_direct_and_wrapper_poles_clear(self):
        check_direct_clears_zero(self, lambda: {"items": [
            PlainChainMapSubclass({"o": keys_view()})]})
        check_wrapper_clears(self, lambda: {"items": [
            PlainChainMapSubclass({"o": keys_view()})]})

    def test_plain_chainmap_subclass_clean_poles_clear(self):
        check_dataset_clean_poles(self, lambda: {"items": [
            PlainChainMapSubclass({"o": keys_view()})]})

    def test_chainmap_standing_poles_stand(self):
        check_dataset_fires(self, lambda: {"items": [
            ChainMap({"o": keys_view()})]})
        check_fires(self, lambda: {"items": [
            ChainMap({"o": keys_view()})]})
        check_dataset_fires(self, lambda: {"pairs": [
            PlainChainMapSubclass({"o": keys_view()})]})
        check_fires(self, lambda: {"pairs": [
            PlainChainMapSubclass({"o": keys_view()})]})


class ChargedFormsControlsTests(unittest.TestCase):
    """The charged forms of rulings 1026 to 1028 and of
    rulings 1100 to 1104, standing pinned beside the cures
    of this round in their standing forms."""

    def test_exact_list_beside_still_fires(self):
        check_fires(self, lambda: {"items": [keys_view(), "x"]})

    def test_sequence_alone_still_fires(self):
        from tests.test_cross_fix_r20 import SequenceCarrier as SC
        check_fires(self, lambda: {"items": [SC([keys_view()])]})

    def test_single_iterator_alone_still_fires(self):
        check_fires(self, lambda: {"items": [
            gen_of(gen_of(keys_view()))]})

    def test_delegating_parent_dataset_still_clears(self):
        check_dataset_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        check_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})
        check_wrapper_fires(self, lambda: {"items": [
            DelegatingListSubclass([keys_view()])]})

    def test_exact_two_container_dataset_still_fires(self):
        check_dataset_fires(self, lambda: {"items": [[keys_view()]]})


if __name__ == "__main__":
    unittest.main()
