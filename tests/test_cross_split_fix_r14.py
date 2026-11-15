"""Fix round 14 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r14-triage.md:
ruling 479 (the items view pairs merged defect at the
R14-CROSS-1 identity, Low, with R14-DAT-1, R14-EVAL-1, and
R14-UC-1 counted in the same act), the pair reading and the
pairs position reading reading a pairs position standing as
a dictionary items view in each probed nesting and entry
form for the pairs it carries, with enumerate index pairs
stripped, or the governed refusal, at every bundle call
point, at indexed_comparisons, and at the dataset record
surface; ruling 480 (R14-UC-2, Low), the governed refusal
reading testing the pairs an items view position carries
beside the entry forms it tests now; ruling 481 (the single
pair direct act merged defect at the R14-SPAN-2 identity,
Low, with R14-CROSS-2, R14-DAT-2, and R14-EVAL-2 counted in
the same act), the direct act audit_instruction_item reading
a pairs position value standing as a single pair in each
probed container and iterator form for the pair it carries,
or the governed refusal, at both occasions; and ruling 482
(R14-SPAN-1, Low), the direct act reading a bundle position
standing as a mapping whose values themselves stand as
mappings carrying holdout material, for the holdout material
it carries, or the governed refusal, at both occasions.
"""

import collections
import unittest
from collections.abc import Sequence

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"

OCCASIONS = ("candidate construction", "promotion")

BUNDLE_SURFACES = (
    "audit_at_promotion",
    "audit_at_build",
    "audit_at_evaluation",
)

CANDIDATE = {
    "group": "g1",
    "signature": "s1",
    "text": "shared bundle text alpha",
    "split": "candidate",
}
HOLDOUT = {
    "group": "g1",
    "signature": "s9",
    "text": "shared bundle text alpha",
    "split": "holdout",
}
CLEAN_HOLDOUT = {
    "group": "g2",
    "signature": "s9",
    "text": "unrelated wording entirely",
    "split": "holdout",
}
HOLDOUT_ITEM = {"text": HOLDOUT_TEXT, "split": "holdout"}


class HashableItem(dict):
    """A mapping item that can stand inside a set."""

    __hash__ = object.__hash__


class IndexedOnly:
    """A container that iterates by indexed access alone."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._items[index]
        if index < 0 or index >= len(self._items):
            raise IndexError(index)
        return self._items[index]

    def __len__(self):
        return len(self._items)


class PairSequence(Sequence):
    """An abstract Sequence instance holding its elements."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


class IterableContainer:
    """A general iterable container holding its elements."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


def check_refuses(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 1)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], 1)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertTrue(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], 1)


def check_proceeds(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertFalse(result["candidate_bundle_refused"])
            test_case.assertTrue(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertFalse(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], 0)


def check_governed_refusal(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="indexed_comparisons"):
        result = module.indexed_comparisons(make_bundle())
        test_case.assertEqual(result["comparisons"], 0)
    with test_case.subTest(surface="dataset record surface"):
        dataset = harness.require("ontoloop.dataset")
        result = dataset.cross_split_audit_at_build(make_bundle())
        shared = result["cross_split_audit_result"]
        test_case.assertTrue(shared["candidate_bundle_refused"])
        test_case.assertEqual(shared["comparisons"], 0)


def check_fires(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for occasion in OCCASIONS:
        with test_case.subTest(occasion=occasion):
            result = module.audit_instruction_item(
                HOLDOUT_TEXT, make_bundle(), occasion=occasion)
            test_case.assertTrue(result["fired"])
            test_case.assertEqual(result["comparisons"], 1)


class ItemsViewPairsExtendedTests(unittest.TestCase):
    """Ruling 479: a pairs position standing as a dictionary
    items view stands read in each probed nesting and entry
    form for the pairs it carries, or refused in the
    governed form."""

    def test_items_view_malformed_pair_forms_refuse(self):
        forms = (
            ("one item list", lambda: [dict(CANDIDATE)]),
            ("three item list", lambda: [
                dict(CANDIDATE), dict(HOLDOUT), dict(CLEAN_HOLDOUT)]),
            ("string pair", lambda: "ab"),
            ("tuple one item", lambda: (dict(CANDIDATE),)),
            ("enumerate one item", lambda: enumerate(
                [dict(CANDIDATE)])),
            ("generator one item", lambda: (
                side for side in [dict(CANDIDATE)])),
            ("zip one item", lambda: zip([dict(CANDIDATE)])),
            ("indexed access pair", lambda: IndexedOnly(
                [dict(CANDIDATE), dict(HOLDOUT)])),
            ("values view pair", lambda: {
                0: dict(CANDIDATE), 1: dict(HOLDOUT)}.values()),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_governed_refusal(self, lambda form=form: {
                    "pairs": {0: form()}.items(),
                })

    def test_items_view_index_pair_flagged(self):
        check_refuses(self, lambda: {"pairs": {
            0: (0, [dict(CANDIDATE), dict(HOLDOUT)]),
        }.items()})
        check_refuses(self, lambda: {"pairs": {
            0: [0, [dict(CANDIDATE), dict(HOLDOUT)]],
        }.items()})

    def test_items_view_index_pair_clean_proceeds(self):
        check_proceeds(self, lambda: {"pairs": {
            0: (0, [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]),
        }.items()})

    def test_items_view_nested_flagged(self):
        check_refuses(self, lambda: {"pairs": {
            0: {0: [dict(CANDIDATE), dict(HOLDOUT)]}.items(),
        }.items()})
        check_refuses(self, lambda: {"pairs": {
            0: [{0: [dict(CANDIDATE), dict(HOLDOUT)]}.items()],
        }.items()})

    def test_items_view_nested_clean_proceeds(self):
        check_proceeds(self, lambda: {"pairs": {
            0: {0: [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]}.items(),
        }.items()})

    def test_items_view_two_entry_items_refuse(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: dict(CANDIDATE), 1: dict(HOLDOUT),
        }.items()})

    def test_items_view_controls_still_decide(self):
        check_refuses(self, lambda: {"pairs": {
            0: [dict(CANDIDATE), dict(HOLDOUT)],
        }.items()})
        check_proceeds(self, lambda: {"pairs": {
            0: [dict(CANDIDATE), dict(CLEAN_HOLDOUT)],
        }.items()})
        check_refuses(self, lambda: {"pairs": [
            [dict(CANDIDATE), dict(HOLDOUT)],
        ]})


class ItemsViewGovernedRefusalTests(unittest.TestCase):
    """Ruling 480: the governed refusal reading tests the
    pairs an items view position carries."""

    def test_items_view_malformed_pair_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: [dict(CANDIDATE)],
        }.items()})

    def test_items_view_malformed_under_index_pair_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": {
            0: (0, [dict(CANDIDATE)]),
        }.items()})

    def test_items_view_refusal_controls_still_decide(self):
        check_governed_refusal(self, lambda: {"pairs": [
            [dict(CANDIDATE)],
        ]})
        check_governed_refusal(self, lambda: {"pairs": {
            0: [dict(CANDIDATE)],
        }.values()})
        check_refuses(self, lambda: {"pairs": {
            0: [dict(CANDIDATE), dict(HOLDOUT)],
        }.items()})


class DirectActSinglePairExtendedTests(unittest.TestCase):
    """Ruling 481: the direct act reads a pairs position
    value standing as a single pair in each probed container
    and iterator form."""

    def pair_items(self):
        return [dict(CANDIDATE), dict(HOLDOUT_ITEM)]

    def test_single_pair_in_iterator_and_view_forms(self):
        forms = (
            ("enumerate", lambda items: enumerate(items)),
            ("generator", lambda items: (
                side for side in items)),
            ("map", lambda items: map(lambda side: side, items)),
            ("iter", lambda items: iter(items)),
            ("filter", lambda items: filter(
                lambda side: True, items)),
            ("values view", lambda items: {
                0: items[0], 1: items[1]}.values()),
            ("items view", lambda items: {
                0: items[0], 1: items[1]}.items()),
            ("abstract sequence", lambda items: PairSequence(items)),
            ("general iterable", lambda items: IterableContainer(
                items)),
            ("indexed access", lambda items: IndexedOnly(items)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, lambda form=form: {
                    "pairs": form(self.pair_items()),
                })

    def test_single_pair_in_reversed_form(self):
        check_fires(self, lambda: {
            "pairs": reversed(
                [dict(HOLDOUT_ITEM), dict(CANDIDATE)]),
        })

    def test_single_pair_in_set_forms(self):
        module = harness.require("ontoloop.cross_split_audit")
        forms = (
            ("set", lambda: {
                HashableItem(CANDIDATE), HashableItem(HOLDOUT_ITEM)}),
            ("frozenset", lambda: frozenset([
                HashableItem(CANDIDATE), HashableItem(HOLDOUT_ITEM)])),
        )
        for name, form in forms:
            for occasion in OCCASIONS:
                with self.subTest(form=name, occasion=occasion):
                    result = module.audit_instruction_item(
                        HOLDOUT_TEXT, {"pairs": form()},
                        occasion=occasion)
                    self.assertTrue(result["fired"])
                    self.assertEqual(result["comparisons"], 2)

    def test_clean_single_pair_in_extended_forms_clears(self):
        module = harness.require("ontoloop.cross_split_audit")
        forms = (
            ("enumerate", lambda items: enumerate(items)),
            ("values view", lambda items: {
                0: items[0], 1: items[1]}.values()),
        )
        for name, form in forms:
            for occasion in OCCASIONS:
                with self.subTest(form=name, occasion=occasion):
                    result = module.audit_instruction_item(
                        CLEAN_TEXT,
                        {"pairs": form(self.pair_items())},
                        occasion=occasion)
                    self.assertFalse(result["fired"])
                    self.assertEqual(result["comparisons"], 1)

    def test_direct_act_single_pair_controls_still_fire(self):
        check_fires(self, lambda: {
            "pairs": [dict(CANDIDATE), dict(HOLDOUT_ITEM)],
        })
        check_fires(self, lambda: {
            "pairs": (dict(CANDIDATE), dict(HOLDOUT_ITEM)),
        })
        check_fires(self, lambda: {
            "pairs": collections.deque(
                [dict(CANDIDATE), dict(HOLDOUT_ITEM)]),
        })
        check_fires(self, lambda: {
            "pairs": collections.UserList(
                [dict(CANDIDATE), dict(HOLDOUT_ITEM)]),
        })
        check_fires(self, lambda: {
            "pairs": zip([dict(CANDIDATE)], [dict(HOLDOUT_ITEM)]),
        })


class DirectActNestedMappingTests(unittest.TestCase):
    """Ruling 482: the direct act reads a bundle position
    standing as a mapping whose values themselves stand as
    mappings carrying holdout material."""

    def test_nested_mapping_positions_fire(self):
        forms = (
            ("holdout items nested item", lambda: {
                "holdout_items": {
                    "key": {"inner": {"text": HOLDOUT_TEXT}}}}),
            ("holdout items nested text", lambda: {
                "holdout_items": {"key": {"inner": HOLDOUT_TEXT}}}),
            ("holdout alias nested", lambda: {
                "holdout": {
                    "key": {"inner": {"text": HOLDOUT_TEXT}}}}),
            ("items nested", lambda: {
                "items": {"key": {"inner": dict(HOLDOUT_ITEM)}}}),
            ("pairs nested", lambda: {
                "pairs": {"key": {"inner": [
                    dict(CANDIDATE), dict(HOLDOUT_ITEM)]}}}),
            ("ordered dict nested", lambda: {
                "holdout_items": collections.OrderedDict({
                    "key": collections.OrderedDict({
                        "inner": {"text": HOLDOUT_TEXT}})})}),
            ("list holding mapping", lambda: {
                "holdout_items": {
                    "key": [{"inner": {"text": HOLDOUT_TEXT}}]}}),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_fires(self, form)

    def test_clean_nested_mapping_clears_with_a_comparison(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    CLEAN_TEXT,
                    {"holdout_items": {
                        "key": {"inner": {"text": HOLDOUT_TEXT}}}},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_nested_mapping_controls_still_decide(self):
        check_fires(self, lambda: {
            "holdout_items": {"key": {"text": HOLDOUT_TEXT}},
        })
        module = harness.require("ontoloop.cross_split_audit")
        bundle_result = module.audit_at_promotion({
            "holdout_items": {
                "key": {"inner": {"text": HOLDOUT_TEXT}}},
        })
        self.assertTrue(bundle_result["candidate_bundle_refused"])
        self.assertEqual(bundle_result["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
