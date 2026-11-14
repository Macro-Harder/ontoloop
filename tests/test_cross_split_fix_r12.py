"""Fix round 12 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r12-triage.md:
ruling 388 (R12-UC-1, Low, with the pairs position enumerate
limb of R12-EVAL-1 counted in the same act), the partitioning
act reading a pairs position standing as an enumerate object
or as a zip object for the pairs it carries, or the governed
refusal, at every bundle call point and at
indexed_comparisons; ruling 389 (R12-UC-2, Low, with the pair
zip and supporting generator limbs of R12-EVAL-1 counted in
the same act), the pair reading reading a pair standing as a
zip object for the two sides it carries, and a malformed pair
in generator form standing decided as in list form, or the
governed refusal, at every bundle call point and at
indexed_comparisons; ruling 390 (Lead Engineer line E-8,
Low), the partitioning act reading a position value standing
in a set form, a frozenset form, a dictionary view form, or
an indexed access container form, and a pair standing as a
set of its two items, for the items those positions carry, or
the governed refusal stating no pair stood compared, at the
audit surfaces and at indexed_comparisons; and ruling 391
(the direct act merged defect at the R12-CS-1 identity, Low,
with R12-SPAN-1 counted in the same act), the direct act
audit_instruction_item reading a holdout side position or
items position standing in a form the partitioning act does
not read, in a plain dictionary bundle, for the holdout
material it carries, or the governed refusal, at both
occasions.
"""

import collections
import collections.abc
import unittest

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


class IndexedHoldout:
    """A container iterating only by indexed access."""

    def __init__(self, elements):
        self._elements = list(elements)

    def __getitem__(self, index):
        return self._elements[index]


class HashableItem(dict):
    """A mapping item that can stand inside a set or as a key."""

    __hash__ = object.__hash__


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


def check_governed_refusal(test_case, make_bundle):
    module = harness.require("ontoloop.cross_split_audit")
    for surface in BUNDLE_SURFACES:
        with test_case.subTest(surface=surface):
            result = getattr(module, surface)(make_bundle())
            test_case.assertTrue(result["candidate_bundle_refused"])
            test_case.assertFalse(result["promotion_proceeded"])
            test_case.assertEqual(result["comparisons"], 0)


class PairsPositionIteratorFormTests(unittest.TestCase):
    """Ruling 388: a pairs position standing as an enumerate
    object or as a zip object stands read for the pairs it
    carries, in list pair form and in mapping pair form."""

    def test_enumerate_position_list_pair_flagged(self):
        check_refuses(self, lambda: {"pairs": enumerate([
            [dict(CANDIDATE), dict(HOLDOUT)],
        ])})

    def test_enumerate_position_list_pair_clean(self):
        check_proceeds(self, lambda: {"pairs": enumerate([
            [dict(CANDIDATE), dict(CLEAN_HOLDOUT)],
        ])})

    def test_enumerate_position_mapping_pair_flagged(self):
        check_refuses(self, lambda: {"pairs": enumerate([
            {"candidate": dict(CANDIDATE), "holdout": dict(HOLDOUT)},
        ])})

    def test_zip_position_list_pair_flagged(self):
        check_refuses(self, lambda: {"pairs": zip([
            [dict(CANDIDATE), dict(HOLDOUT)],
        ])})

    def test_zip_position_list_pair_clean(self):
        check_proceeds(self, lambda: {"pairs": zip([
            [dict(CANDIDATE), dict(CLEAN_HOLDOUT)],
        ])})

    def test_zip_position_mapping_pair_flagged(self):
        check_refuses(self, lambda: {"pairs": zip([
            {"candidate": dict(CANDIDATE), "holdout": dict(HOLDOUT)},
        ])})

    def test_dataset_record_surface_enumerate_and_zip(self):
        module = harness.require("ontoloop.dataset")
        for name, make in (
            ("enumerate", lambda: {"pairs": enumerate([
                [dict(CANDIDATE), dict(HOLDOUT)],
            ])}),
            ("zip", lambda: {"pairs": zip([
                [dict(CANDIDATE), dict(HOLDOUT)],
            ])}),
        ):
            with self.subTest(form=name):
                result = module.cross_split_audit_at_build(make())
                shared = result["cross_split_audit_result"]
                self.assertTrue(shared["candidate_bundle_refused"])
                self.assertEqual(shared["comparisons"], 1)

    def test_neighbouring_position_controls_still_refuse(self):
        forms = (
            ("list", lambda pairs: list(pairs)),
            ("deque", lambda pairs: collections.deque(pairs)),
            ("map", lambda pairs: map(lambda pair: pair, pairs)),
            ("filter", lambda pairs: filter(lambda pair: True, pairs)),
            ("reversed", lambda pairs: reversed(pairs)),
            ("iter", lambda pairs: iter(pairs)),
            ("generator", lambda pairs: (pair for pair in pairs)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_refuses(self, lambda form=form: {"pairs": form([
                    [dict(CANDIDATE), dict(HOLDOUT)],
                ])})


class PairZipFormTests(unittest.TestCase):
    """Ruling 389: a pair standing as a zip object stands read
    for the two sides it carries, and a malformed pair in
    generator form stands decided as in list form."""

    def test_zip_pair_flagged(self):
        check_refuses(self, lambda: {"pairs": [
            zip([dict(CANDIDATE)], [dict(HOLDOUT)]),
        ]})

    def test_zip_pair_clean(self):
        check_proceeds(self, lambda: {"pairs": [
            zip([dict(CANDIDATE)], [dict(CLEAN_HOLDOUT)]),
        ]})

    def test_dataset_record_surface_zip_pair(self):
        module = harness.require("ontoloop.dataset")
        result = module.cross_split_audit_at_build({"pairs": [
            zip([dict(CANDIDATE)], [dict(HOLDOUT)]),
        ]})
        shared = result["cross_split_audit_result"]
        self.assertTrue(shared["candidate_bundle_refused"])
        self.assertEqual(shared["comparisons"], 1)

    def test_malformed_one_item_pair_in_generator_form_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": (
            pair for pair in [[dict(CANDIDATE)]]
        )})

    def test_malformed_one_item_pair_in_list_form_still_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            [dict(CANDIDATE)],
        ]})

    def test_malformed_generator_pair_itself_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            (side for side in [dict(CANDIDATE)]),
        ]})

    def test_neighbouring_iterator_pair_forms_still_decide(self):
        forms = (
            ("enumerate", lambda: enumerate(
                [dict(CANDIDATE), dict(HOLDOUT)])),
            ("generator", lambda: (
                side for side in [dict(CANDIDATE), dict(HOLDOUT)])),
            ("map", lambda: map(
                lambda side: side, [dict(CANDIDATE), dict(HOLDOUT)])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_refuses(self, lambda form=form: {"pairs": [form()]})


class PartitioningSetViewIndexedTests(unittest.TestCase):
    """Ruling 390: the partitioning act reads position values
    in set, frozenset, dictionary view, and indexed access
    forms, and a pair standing as a set of its two items."""

    def flagged_and_clean(self, make_position):
        check_refuses(self, lambda: {
            "candidate_items": make_position([dict(CANDIDATE)]),
            "holdout_items": make_position([dict(HOLDOUT)]),
        })
        check_proceeds(self, lambda: {
            "candidate_items": make_position([dict(CANDIDATE)]),
            "holdout_items": make_position([dict(CLEAN_HOLDOUT)]),
        })

    def test_side_positions_as_sets(self):
        check_refuses(self, lambda: {
            "candidate_items": {HashableItem(CANDIDATE)},
            "holdout_items": {HashableItem(HOLDOUT)},
        })
        check_proceeds(self, lambda: {
            "candidate_items": {HashableItem(CANDIDATE)},
            "holdout_items": {HashableItem(CLEAN_HOLDOUT)},
        })

    def test_side_positions_as_frozensets(self):
        check_refuses(self, lambda: {
            "candidate_items": frozenset({HashableItem(CANDIDATE)}),
            "holdout_items": frozenset({HashableItem(HOLDOUT)}),
        })
        check_proceeds(self, lambda: {
            "candidate_items": frozenset({HashableItem(CANDIDATE)}),
            "holdout_items": frozenset({HashableItem(CLEAN_HOLDOUT)}),
        })

    def test_side_positions_as_values_views(self):
        self.flagged_and_clean(
            lambda items: {0: items[0]}.values())

    def test_side_positions_as_keys_views(self):
        check_refuses(self, lambda: {
            "candidate_items": {HashableItem(CANDIDATE): 1}.keys(),
            "holdout_items": {HashableItem(HOLDOUT): 1}.keys(),
        })
        check_proceeds(self, lambda: {
            "candidate_items": {HashableItem(CANDIDATE): 1}.keys(),
            "holdout_items": {HashableItem(CLEAN_HOLDOUT): 1}.keys(),
        })

    def test_side_positions_as_indexed_containers(self):
        self.flagged_and_clean(
            lambda items: IndexedHoldout(items))

    def test_items_position_as_values_view_and_indexed(self):
        for name, form in (
            ("values view", lambda items: {0: items[0], 1: items[1]}.values()),
            ("indexed", lambda items: IndexedHoldout(items)),
        ):
            with self.subTest(form=name):
                check_refuses(self, lambda form=form: {
                    "items": form([dict(CANDIDATE), dict(HOLDOUT)]),
                })
                check_proceeds(self, lambda form=form: {
                    "items": form(
                        [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]),
                })

    def test_pair_standing_as_a_set_of_its_two_items(self):
        check_refuses(self, lambda: {"pairs": [
            {HashableItem(CANDIDATE), HashableItem(HOLDOUT)},
        ]})

    def test_split_items_reads_each_probed_form(self):
        module = harness.require("ontoloop.cross_split_audit")
        forms = (
            ("set", lambda items: {HashableItem(items[0])}),
            ("frozenset", lambda items: frozenset(
                {HashableItem(items[0])})),
            ("values view", lambda items: {0: items[0]}.values()),
            ("keys view", lambda items: {HashableItem(items[0]): 1}.keys()),
            ("indexed", lambda items: IndexedHoldout(items)),
        )
        for name, form in forms:
            with self.subTest(form=name):
                candidate, holdout = module._split_items({
                    "candidate_items": form([dict(CANDIDATE)]),
                    "holdout_items": form([dict(HOLDOUT)]),
                })
                self.assertEqual(len(candidate), 1)
                self.assertEqual(len(holdout), 1)
                self.assertEqual(
                    candidate[0]["text"], CANDIDATE["text"])
                self.assertEqual(holdout[0]["text"], HOLDOUT["text"])

    def test_ruling_357_forms_still_decide(self):
        check_refuses(self, lambda: {
            "candidate_items": collections.deque([dict(CANDIDATE)]),
            "holdout_items": collections.deque([dict(HOLDOUT)]),
        })
        check_proceeds(self, lambda: {
            "candidate_items": [dict(CANDIDATE)],
            "holdout_items": [dict(CLEAN_HOLDOUT)],
        })


class DirectActBundleRouteTests(unittest.TestCase):
    """Ruling 391: the direct act reads a holdout side position
    or items position standing in an unread form in a plain
    dictionary bundle, at both occasions."""

    def check_fires(self, make_bundle):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT, make_bundle(), occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_indexed_holdout_items_holding_a_mapping(self):
        self.check_fires(lambda: {
            "holdout_items": IndexedHoldout([{"text": HOLDOUT_TEXT}]),
        })

    def test_indexed_holdout_items_holding_plain_text(self):
        self.check_fires(lambda: {
            "holdout_items": IndexedHoldout([HOLDOUT_TEXT]),
        })

    def test_indexed_holdout_items_holding_a_generator(self):
        self.check_fires(lambda: {
            "holdout_items": IndexedHoldout(
                [(v for v in [{"text": HOLDOUT_TEXT}])]),
        })

    def test_indexed_under_the_holdout_alias_key(self):
        self.check_fires(lambda: {
            "holdout": IndexedHoldout([{"text": HOLDOUT_TEXT}]),
        })

    def test_indexed_items_position_holding_holdout_item(self):
        self.check_fires(lambda: {
            "items": IndexedHoldout([
                {"text": HOLDOUT_TEXT, "split": "holdout"},
            ]),
        })

    def test_values_view_holdout_items(self):
        self.check_fires(lambda: {
            "holdout_items": {0: {"text": HOLDOUT_TEXT}}.values(),
        })

    def test_single_mapping_holdout_items(self):
        self.check_fires(lambda: {
            "holdout_items": {"text": HOLDOUT_TEXT},
        })

    def test_bare_string_holdout_items(self):
        self.check_fires(lambda: {"holdout_items": HOLDOUT_TEXT})

    def test_set_of_plain_text_holdout_items(self):
        self.check_fires(lambda: {"holdout_items": {HOLDOUT_TEXT}})

    def test_frozenset_of_plain_text_holdout_items(self):
        self.check_fires(lambda: {
            "holdout_items": frozenset({HOLDOUT_TEXT}),
        })

    def test_keys_view_holdout_items(self):
        self.check_fires(lambda: {
            "holdout_items": {HOLDOUT_TEXT: 1}.keys(),
        })

    def test_items_view_holdout_items(self):
        self.check_fires(lambda: {
            "holdout_items": {0: {"text": HOLDOUT_TEXT}}.items(),
        })

    def test_values_view_items_position(self):
        self.check_fires(lambda: {
            "items": {0: {"text": HOLDOUT_TEXT,
                          "split": "holdout"}}.values(),
        })

    def test_indexed_pairs_position(self):
        self.check_fires(lambda: {
            "pairs": IndexedHoldout([
                [dict(CANDIDATE), {"text": HOLDOUT_TEXT,
                                   "split": "holdout"}],
            ]),
        })

    def test_clean_indexed_bundle_clears_with_a_comparison(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    CLEAN_TEXT,
                    {"holdout_items": IndexedHoldout(
                        [{"text": HOLDOUT_TEXT}])},
                    occasion=occasion,
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_list_and_userdict_controls_still_fire(self):
        self.check_fires(lambda: {
            "holdout_items": [{"text": HOLDOUT_TEXT}],
        })
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    collections.UserDict({
                        "holdout_items": IndexedHoldout(
                            [{"text": HOLDOUT_TEXT}]),
                    }),
                    occasion=occasion,
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 1)


if __name__ == "__main__":
    unittest.main()
