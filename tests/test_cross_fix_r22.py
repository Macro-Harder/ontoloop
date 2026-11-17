"""Fix round 22 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r22-triage.md:
ruling 905 (the cross split audit key material presented
through a view standing at a mapping value or inside a list
at the pairs position defect at the R22-CROSS-1 identity,
Low), the direct act view walk reaching key material
presented through a values view or an items view standing
at a mapping value of the pairs position, and through an
items view standing inside a list at that position;
ruling 906 (the cross split audit key material presented
through a view standing inside a container at the items
position defect at the R22-CROSS-2 identity, Low), the
direct act view reading reaching a view standing one level
inside the items position, as a mapping value and as a
container element, and at the holdout_items and holdout
positions in the Eval form; ruling 907 (the cross split
audit wrapped and single pass pair keys presented through
a keys view or an items view standing inside a list at the
items position defect at the R22-EVAL-3 identity, Low),
counted severally from ruling 906 on the view kinds and
carrier classes; and ruling 908 (the dataset instruction
item surface view key material clearing through its
holdout materialisation defect at the R22-DAT-1 identity,
Low), the dataset.py act at the one named call point only,
the _materialise_iterators call inside
dataset.test_instruction_items_against_holdout.
tests/test_unrowed_c.py stands held whole and unchanged,
with no pin of this region filed in it.
"""

import unittest
from collections import deque

from tests import harness
from tests.test_cross_fix_r20 import (
    CANDIDATE,
    CLEAN_TEXT,
    HOLDOUT_TEXT,
    HashableItem,
    OnceOnlyIterable,
    check_clears,
    check_dataset_pair,
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


def check_fires_at_least(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertTrue(result["fired"])
            test_case.assertGreaterEqual(result["comparisons"], 1)


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


class ViewAtMappingValuePairsTests(unittest.TestCase):
    """Ruling 905: key material presented through a view
    standing at a mapping value or inside a list at the
    pairs position fires at the direct act."""

    def test_items_view_at_mapping_value_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {"outer": {
            tuple_pair_key(): 1,
        }.items()}})

    def test_values_view_of_intermediate_at_mapping_value_fires(self):
        check_fires(self, lambda: {"pairs": {"outer": {
            "inner": {tuple_pair_key(): 1},
        }.values()}})

    def test_items_view_two_mapping_values_deep_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {"outer": {"inner": {
            tuple_pair_key(): 1,
        }.items()}}})

    def test_values_view_two_mapping_values_deep_pairs_fires(self):
        check_fires(self, lambda: {"pairs": {"outer": {"inner": {
            tuple_pair_key(): 1,
        }.values()}}})

    def test_single_pass_items_view_at_mapping_value_fires(self):
        check_fires(self, lambda: {"pairs": {"outer": {
            single_pass_key(): 1,
        }.items()}})

    def test_items_view_inside_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [{
            tuple_pair_key(): 1,
        }.items()]})

    def test_wrapped_items_view_inside_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [{
            wrapped_key(): 1,
        }.items()]})

    def test_single_pass_items_view_inside_list_pairs_fires(self):
        check_fires(self, lambda: {"pairs": [{
            single_pass_key(): 1,
        }.items()]})

    def test_frozenset_items_view_inside_list_pairs_fires(self):
        check_fires_at_least(self, lambda: {"pairs": [{
            frozenset_key(): 1,
        }.items()]})

    def test_view_at_mapping_value_pairs_clean_clears(self):
        check_clears(self, lambda: {"pairs": {"outer": {
            tuple_pair_key(): 1,
        }.items()}})
        check_clears(self, lambda: {"pairs": [{
            tuple_pair_key(): 1,
        }.items()]})

    def test_view_pairs_dataset_spanning_form_fires(self):
        check_dataset_pair(self, lambda: {"outer": {
            tuple_pair_key(): 1,
        }.items()})

    def test_view_pairs_controls_stand(self):
        check_fires(self, lambda: {"pairs": {"outer": {
            tuple_pair_key(): 1,
        }.values()}})
        check_fires(self, lambda: {"pairs": {"outer": {
            tuple_pair_key(): 1,
        }}})
        check_fires(self, lambda: {"pairs": [{
            tuple_pair_key(): 1,
        }]})
        check_governed_refusal(self, lambda: {"pairs": {"outer": {
            tuple_pair_key(): 1,
        }.items()}})


class ViewInsideContainerItemsTests(unittest.TestCase):
    """Ruling 906: key material presented through a view
    standing inside a container at the items position fires
    at the direct act, and at the holdout positions in the
    Eval form."""

    def test_wrapped_keys_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.keys()]})

    def test_wrapped_keys_view_inside_tuple_items_fires(self):
        check_fires(self, lambda: {"items": ({
            wrapped_key(): 1,
        }.keys(),)})

    def test_wrapped_keys_view_at_mapping_value_items_fires(self):
        check_fires(self, lambda: {"items": {"outer": {
            wrapped_key(): 1,
        }.keys()}})

    def test_tuple_values_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            tuple_pair_key(): 1,
        }.values()]})

    def test_tuple_values_view_inside_tuple_items_fires(self):
        check_fires(self, lambda: {"items": ({
            tuple_pair_key(): 1,
        }.values(),)})

    def test_tuple_values_view_inside_deque_items_fires(self):
        check_fires(self, lambda: {"items": deque([{
            tuple_pair_key(): 1,
        }.values()])})

    def test_tuple_values_view_inside_list_in_list_items_fires(self):
        check_fires(self, lambda: {"items": [[{
            tuple_pair_key(): 1,
        }.values()]]})

    def test_tuple_values_view_at_mapping_value_items_fires(self):
        check_fires(self, lambda: {"items": {"outer": {
            tuple_pair_key(): 1,
        }.values()}})

    def test_frozenset_values_view_inside_list_items_fires(self):
        check_fires_at_least(self, lambda: {"items": [{
            frozenset_key(): 1,
        }.values()]})

    def test_single_pass_values_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            single_pass_key(): 1,
        }.values()]})

    def test_wrapped_values_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.values()]})

    def test_tuple_values_view_inside_list_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": [{
            tuple_pair_key(): 1,
        }.values()]})

    def test_tuple_values_view_inside_list_holdout_fires(self):
        check_fires(self, lambda: {"holdout": [{
            tuple_pair_key(): 1,
        }.values()]})

    def test_wrapped_values_view_inside_list_holdout_items_fires(self):
        check_fires(self, lambda: {"holdout_items": [{
            wrapped_key(): 1,
        }.values()]})

    def test_single_pass_values_view_inside_list_holdout_fires(self):
        check_fires(self, lambda: {"holdout": [{
            single_pass_key(): 1,
        }.values()]})

    def test_view_inside_container_items_clean_clears(self):
        check_clears(self, lambda: {"items": [{
            tuple_pair_key(): 1,
        }.values()]})
        check_clears(self, lambda: {"holdout_items": [{
            tuple_pair_key(): 1,
        }.values()]})

    def test_view_inside_container_controls_stand(self):
        check_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.values()})
        check_fires(self, lambda: {"items": [{
            tuple_pair_key(): 1,
        }]})
        check_fires(self, lambda: {"items": [{
            tuple_pair_key(): 1,
        }.keys()]})


class KeysItemsViewInsideListItemsTests(unittest.TestCase):
    """Ruling 907: the wrapped and single pass pair keys
    presented through a keys view or an items view standing
    inside a list at the items position fire at the direct
    act, beside the parity carriers still firing."""

    def test_wrapped_keys_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.keys()]})

    def test_wrapped_items_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.items()]})

    def test_single_pass_items_view_inside_list_items_fires(self):
        check_fires(self, lambda: {"items": [{
            single_pass_key(): 1,
        }.items()]})

    def test_single_pass_items_view_inside_list_holdout_items(self):
        check_fires_at_least(self, lambda: {"holdout_items": [{
            single_pass_key(): 1,
        }.items()]})

    def test_keys_items_view_inside_list_clean_clears(self):
        check_clears(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.keys()]})
        check_clears(self, lambda: {"items": [{
            wrapped_key(): 1,
        }.items()]})

    def test_keys_items_view_parity_carriers_stand(self):
        check_fires(self, lambda: {"items": [{
            tuple_pair_key(): 1,
        }.keys()]})
        check_fires(self, lambda: {"items": [{
            frozenset_key(): 1,
        }.keys()]})
        check_fires(self, lambda: {"items": [{
            single_pass_key(): 1,
        }.keys()]})
        check_fires(self, lambda: {"items": {
            wrapped_key(): 1,
        }.keys()})


class DatasetViewKeyMaterialTests(unittest.TestCase):
    """Ruling 908: view key material at the items and pairs
    positions fires at the dataset instruction item surface,
    beside the same presentations firing at the direct act."""

    def test_dataset_items_values_view_tuple_key_fires(self):
        check_dataset_holdout_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.values()})

    def test_dataset_items_values_view_wrapped_key_fires(self):
        check_dataset_holdout_fires(self, lambda: {"items": {
            wrapped_key(): 1,
        }.values()})

    def test_dataset_items_keys_view_wrapped_key_fires(self):
        check_dataset_holdout_fires(self, lambda: {"items": {
            wrapped_key(): 1,
        }.keys()})

    def test_dataset_pairs_values_view_tuple_key_fires(self):
        check_dataset_holdout_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }.values()})

    def test_dataset_view_forms_clean_clears(self):
        check_dataset_holdout_clears(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.values()})
        check_dataset_holdout_clears(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }.values()})

    def test_dataset_view_parity_forms_stand(self):
        check_dataset_holdout_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.keys()})
        check_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.values()})
        check_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }.values()})


if __name__ == "__main__":
    unittest.main()
