"""Fix round 21 tests for Region 2: cross split.

Charges pinned here, from design/steps/step-15-r21-triage.md:
ruling 844 (the cross split audit key carrier standing as a
key of a mapping standing two mapping values deep at the
pairs position defect at the R21-EVAL-1 identity, Low), the
direct act mapping value reading reaching a key carrier at
the second mapping value depth, at the dataset instruction
item surface in the same form; ruling 845 (the cross split
audit key material presented through a view at the items
position defect at the R21-EVAL-2 identity, Low), the direct
act view reading reaching key material presented through a
keys view or a values view standing at the items position;
ruling 846 (the cross split audit indexed_comparisons
standing alone returning no comparison defect at the
R21-CROSS-3 identity, Low), the indexed reading reaching a
pair standing inside two plain iterators at the pairs
position, in parity with the bundle surfaces; and ruling
849 (the cross split audit key carrier standing three
mapping values deep at the pairs position defect at the
Lead Engineer E-31 identity, Low), the direct act mapping
value reading reaching a key carrier at the third mapping
value depth. dataset.py stands expressly unchanged in this
round, and tests/test_unrowed_c.py stands held whole and
unchanged, with no pin of this region filed in it.
"""

import unittest

from tests import harness
from tests.test_cross_fix_r20 import (
    CANDIDATE,
    CLEAN_HOLDOUT,
    CLEAN_TEXT,
    HOLDOUT,
    HOLDOUT_TEXT,
    HashableItem,
    OnceOnlyIterable,
    bundle_tuple_pair_key,
    check_clears,
    check_dataset_pair,
    check_fires,
    check_governed_refusal,
    check_proceeds,
    check_refuses,
    clean_bundle_pair,
    direct_pair,
    flagged_pair,
    inner_mapping,
    plain_iterator,
    tuple_pair_key,
)


def two_deep(carrier):
    return {"pairs": {"outer": {"inner": carrier}}}


def three_deep(carrier):
    return {"pairs": {"first": {"second": {"third": carrier}}}}


class KeyCarrierTwoMappingValuesDeepTests(unittest.TestCase):
    """Ruling 844: a key carrier standing as a key of a mapping
    standing two mapping values deep at the pairs position
    fires at the direct act, in parity with its charged one
    mapping value form of ruling 780."""

    def test_tuple_pair_key_two_deep_fires(self):
        check_fires(self, lambda: two_deep({tuple_pair_key(): 1}))

    def test_single_pass_key_two_deep_fires(self):
        check_fires(
            self,
            lambda: two_deep({OnceOnlyIterable(direct_pair()): 1}))

    def test_frozenset_pair_key_two_deep_fires(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in ("candidate construction", "promotion"):
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    two_deep({frozenset(tuple_pair_key()): 1}),
                    occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertGreaterEqual(result["comparisons"], 1)

    def test_wrapped_nested_key_two_deep_fires(self):
        check_fires(
            self,
            lambda: two_deep({(HashableItem(inner_mapping()),): 1}))

    def test_tuple_pair_key_in_list_at_second_level_fires(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {"inner": [{tuple_pair_key(): 1}]},
        }})

    def test_key_carrier_two_deep_clean_clears(self):
        check_clears(self, lambda: two_deep({tuple_pair_key(): 1}))

    def test_key_carrier_two_deep_dataset_fires(self):
        check_dataset_pair(
            self, lambda: {"outer": {"inner": {tuple_pair_key(): 1}}})

    def test_key_carrier_two_deep_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            "outer": {tuple_pair_key(): 1},
        }})
        check_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            "outer": {"inner": {tuple_pair_key(): 1}},
        }})
        check_fires(self, lambda: {"pairs": {
            "outer": {
                HashableItem(CANDIDATE): 1,
                HashableItem({"text": HOLDOUT_TEXT,
                              "split": "holdout"}): 2,
            },
        }})
        check_governed_refusal(self, lambda: two_deep(
            {bundle_tuple_pair_key(): 1}))


class KeyCarrierThreeMappingValuesDeepTests(unittest.TestCase):
    """Ruling 849: a key carrier standing as a key of a mapping
    standing three mapping values deep at the pairs position
    fires at the direct act, in parity with its charged one
    mapping value form of ruling 780 and with the second
    depth form of ruling 844."""

    def test_tuple_pair_key_three_deep_fires(self):
        check_fires(self, lambda: three_deep({tuple_pair_key(): 1}))

    def test_single_pass_key_three_deep_fires(self):
        check_fires(
            self,
            lambda: three_deep(
                {OnceOnlyIterable(direct_pair()): 1}))

    def test_key_carrier_three_deep_clean_clears(self):
        check_clears(
            self, lambda: three_deep({tuple_pair_key(): 1}))

    def test_key_carrier_three_deep_controls_stand(self):
        check_fires(self, lambda: {"pairs": {
            tuple_pair_key(): 1,
        }})
        check_fires(self, lambda: {"pairs": {
            "outer": {tuple_pair_key(): 1},
        }})
        check_fires(self, lambda: two_deep({tuple_pair_key(): 1}))
        check_governed_refusal(self, lambda: three_deep(
            {bundle_tuple_pair_key(): 1}))


class ViewAtItemsPositionTests(unittest.TestCase):
    """Ruling 845: key material presented through a keys view
    or a values view standing at the items position fires at
    the direct act, in parity with its charged view forms of
    rulings 782 and 783 at their charged positions."""

    def test_wrapped_key_through_keys_view_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }.keys()})

    def test_wrapped_key_through_values_view_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }.values()})

    def test_tuple_pair_key_through_values_view_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.values()})

    def test_frozenset_key_through_values_view_at_items_fires(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in ("candidate construction", "promotion"):
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"items": {
                        frozenset(tuple_pair_key()): 1,
                    }.values()},
                    occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertGreaterEqual(result["comparisons"], 1)

    def test_single_pass_key_through_values_view_at_items_fires(self):
        check_fires(self, lambda: {"items": {
            OnceOnlyIterable(direct_pair()): 1,
        }.values()})

    def test_view_at_items_clean_clears(self):
        check_clears(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.values()})
        check_clears(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }.keys()})

    def test_view_at_items_controls_stand(self):
        check_fires(self, lambda: {"items": {
            (HashableItem(inner_mapping()),): 1,
        }})
        check_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }.keys()})
        check_fires(self, lambda: {"items": {
            tuple_pair_key(): 1,
        }})
        check_fires(self, lambda: {"holdout_items": {
            tuple_pair_key(): 1,
        }.values()})
        check_fires(self, lambda: {"holdout_items": {
            (HashableItem(inner_mapping()),): 1,
        }.values()})


def double_iterator(pair_form, first, second):
    if pair_form == "list once":
        core = [OnceOnlyIterable(flagged_pair())]
    elif pair_form == "direct once":
        core = OnceOnlyIterable(flagged_pair())
    elif pair_form == "plain in list":
        core = [flagged_pair()]
    elif pair_form == "clean in list":
        core = [OnceOnlyIterable(clean_bundle_pair())]
    elif pair_form == "malformed in list":
        core = [OnceOnlyIterable([dict(CANDIDATE)])]
    else:
        raise ValueError(pair_form)
    inner = plain_iterator(second, [core])
    outer = plain_iterator(first, [inner])
    return {"pairs": [outer]}


class IndexedComparisonsDoubleIteratorTests(unittest.TestCase):
    """Ruling 846: indexed_comparisons standing alone returns
    the comparison for holdout material standing in an
    iterable presentation inside two plain iterators at the
    pairs position, in parity with the bundle surfaces."""

    def test_indexed_map_inside_generator_returns_comparison(self):
        check_refuses(self, lambda: double_iterator(
            "list once", "map", "generator"))

    def test_indexed_generator_inside_map_returns_comparison(self):
        check_refuses(self, lambda: double_iterator(
            "list once", "generator", "map"))

    def test_indexed_list_iterator_inside_filter_returns(self):
        check_refuses(self, lambda: double_iterator(
            "list once", "filter", "list iterator"))

    def test_indexed_generator_inside_generator_returns(self):
        check_refuses(self, lambda: double_iterator(
            "list once", "generator", "generator"))

    def test_indexed_once_only_directly_inside_two_iterators(self):
        check_refuses(self, lambda: double_iterator(
            "direct once", "map", "generator"))

    def test_indexed_plain_pair_inside_list_inside_two(self):
        check_refuses(self, lambda: double_iterator(
            "plain in list", "map", "generator"))

    def test_indexed_double_iterator_clean_proceeds(self):
        check_proceeds(self, lambda: double_iterator(
            "clean in list", "map", "generator"), comparisons=0)
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(double_iterator(
            "clean in list", "map", "generator"))
        self.assertEqual(result["comparisons"], 0)

    def test_indexed_double_iterator_malformed_refused(self):
        check_governed_refusal(self, lambda: double_iterator(
            "malformed in list", "map", "generator"))

    def test_indexed_double_iterator_controls_stand(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons({"pairs": [
            plain_iterator(
                "map", [[OnceOnlyIterable(flagged_pair())]]),
        ]})
        self.assertEqual(result["comparisons"], 1)
        check_refuses(self, lambda: {"pairs": [
            [OnceOnlyIterable(flagged_pair())],
        ]})
        check_refuses(self, lambda: {"pairs": [
            plain_iterator(
                "map", [OnceOnlyIterable(flagged_pair())]),
        ]})
        check_fires(self, lambda: {"pairs": {
            "outer": {tuple_pair_key(): 1},
        }})


if __name__ == "__main__":
    unittest.main()
