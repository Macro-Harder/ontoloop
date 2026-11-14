"""Fix round 13 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r13-triage.md:
ruling 434 (the pairs position enumerate index pair merged
defect at the R13-EVAL-1 identity, Low, with R13-UC-1 counted
in the same act), the pair reading and the pairs position
reading unwrapping an enumerate object standing between the
act and a pair, in each probed nesting, for the pair it
carries, or the governed refusal, at every bundle call point,
at indexed_comparisons, and at the dataset record surface;
ruling 435 (Lead Engineer line E-7, Low), the partitioning
act reading a pairs position standing as a dictionary items
view for the pairs it carries, or the governed refusal
stating no pair stood compared, at the audit surfaces and at
indexed_comparisons; ruling 436 (R13-SPAN-1, Low), the direct
act audit_instruction_item reading a bundle position standing
as a mapping carrying holdout items in its values for the
holdout material it carries, or the governed refusal, at both
occasions; and ruling 437 (R13-SPAN-2, Low), the direct act
reading a pairs position value standing as a single pair, in
each probed container form, for the pair it carries, or the
governed refusal, at both occasions.
"""

import collections
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
HOLDOUT_ITEM = {"text": HOLDOUT_TEXT, "split": "holdout"}


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


class PairsEnumerateIndexPairTests(unittest.TestCase):
    """Ruling 434: a pair or a pairs position standing behind
    an enumerate object stands read for the pair it carries,
    and a malformed pair in that form stands decided as the
    same pair in list form decides."""

    def test_malformed_one_item_enumerate_pair_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": [
            enumerate([dict(CANDIDATE)]),
        ]})

    def test_enumerate_pair_holding_one_tuple_pair_refuses(self):
        check_refuses(self, lambda: {"pairs": [
            enumerate([[dict(CANDIDATE), dict(HOLDOUT)]]),
        ]})

    def test_well_formed_enumerate_pair_still_decides(self):
        check_refuses(self, lambda: {"pairs": [
            enumerate([dict(CANDIDATE), dict(HOLDOUT)]),
        ]})
        check_governed_refusal(self, lambda: {"pairs": [
            enumerate([]),
        ]})
        check_governed_refusal(self, lambda: {"pairs": [
            enumerate([dict(CANDIDATE), dict(HOLDOUT),
                       dict(CLEAN_HOLDOUT)]),
        ]})

    def test_malformed_pair_controls_still_refuse(self):
        forms = (
            ("list", lambda item: [item]),
            ("generator", lambda item: (side for side in [item])),
            ("map", lambda item: map(lambda side: side, [item])),
            ("filter", lambda item: filter(lambda side: True, [item])),
            ("reversed", lambda item: reversed([item])),
            ("iter", lambda item: iter([item])),
            ("zip", lambda item: zip([item])),
        )
        for name, form in forms:
            with self.subTest(form=name):
                check_governed_refusal(self, lambda form=form: {
                    "pairs": [form(dict(CANDIDATE))],
                })

    def test_double_enumerate_position_flagged(self):
        check_refuses(self, lambda: {"pairs": enumerate(enumerate([
            [dict(CANDIDATE), dict(HOLDOUT)],
        ]))})

    def test_zip_position_holding_enumerate_flagged(self):
        check_refuses(self, lambda: {"pairs": zip(enumerate([
            [dict(CANDIDATE), dict(HOLDOUT)],
        ]))})

    def test_generator_position_yielding_enumerate_flagged(self):
        check_refuses(self, lambda: {"pairs": (
            position for position in [enumerate([
                [dict(CANDIDATE), dict(HOLDOUT)],
            ])]
        )})

    def test_triple_enumerate_position_flagged(self):
        check_refuses(self, lambda: {"pairs": enumerate(enumerate(
            enumerate([
                [dict(CANDIDATE), dict(HOLDOUT)],
            ])))})

    def test_malformed_pair_under_double_enumerate_refuses(self):
        check_governed_refusal(self, lambda: {"pairs": enumerate(
            enumerate([
                [dict(CANDIDATE)],
            ]))})

    def test_clean_pair_under_double_enumerate_proceeds(self):
        check_proceeds(self, lambda: {"pairs": enumerate(enumerate([
            [dict(CANDIDATE), dict(CLEAN_HOLDOUT)],
        ]))})

    def test_neighbouring_position_compositions_still_refuse(self):
        check_refuses(self, lambda: {"pairs": enumerate([
            [dict(CANDIDATE), dict(HOLDOUT)],
        ])})
        check_refuses(self, lambda: {"pairs": enumerate([
            zip([dict(CANDIDATE)], [dict(HOLDOUT)]),
        ])})
        check_refuses(self, lambda: {"pairs": zip([
            zip([dict(CANDIDATE)], [dict(HOLDOUT)]),
        ])})


class PairsPositionItemsViewTests(unittest.TestCase):
    """Ruling 435: a pairs position standing as a dictionary
    items view stands read for the pairs it carries."""

    def test_items_view_position_flagged(self):
        check_refuses(self, lambda: {"pairs": {
            0: [dict(CANDIDATE), dict(HOLDOUT)],
        }.items()})

    def test_items_view_position_clean(self):
        check_proceeds(self, lambda: {"pairs": {
            0: [dict(CANDIDATE), dict(CLEAN_HOLDOUT)],
        }.items()})

    def test_list_and_values_view_controls_still_decide(self):
        check_refuses(self, lambda: {"pairs": [
            [dict(CANDIDATE), dict(HOLDOUT)],
        ]})
        check_refuses(self, lambda: {"pairs": {
            0: [dict(CANDIDATE), dict(HOLDOUT)],
        }.values()})
        check_refuses(self, lambda: {
            "candidate_items": {HashableItem(CANDIDATE)},
            "holdout_items": {HashableItem(HOLDOUT)},
        })


class DirectActMappingPositionTests(unittest.TestCase):
    """Ruling 436: the direct act reads a bundle position
    standing as a mapping carrying holdout items in its
    values, at each position the finding names."""

    def check_fires(self, make_bundle):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT, make_bundle(), occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_holdout_items_mapping_holding_an_item_mapping(self):
        self.check_fires(lambda: {
            "holdout_items": {"key": {"text": HOLDOUT_TEXT}},
        })

    def test_holdout_items_mapping_holding_plain_text(self):
        self.check_fires(lambda: {
            "holdout_items": {"key": HOLDOUT_TEXT},
        })

    def test_holdout_items_mapping_holding_a_list_of_items(self):
        self.check_fires(lambda: {
            "holdout_items": {"key": [{"text": HOLDOUT_TEXT}]},
        })

    def test_holdout_alias_mapping_position(self):
        self.check_fires(lambda: {
            "holdout": {"key": {"text": HOLDOUT_TEXT}},
        })

    def test_items_mapping_position_holding_holdout_item(self):
        self.check_fires(lambda: {
            "items": {"key": dict(HOLDOUT_ITEM)},
        })

    def test_pairs_mapping_position_holding_a_list_pair(self):
        self.check_fires(lambda: {
            "pairs": {"key": [dict(CANDIDATE), dict(HOLDOUT_ITEM)]},
        })

    def test_ordered_dict_position(self):
        self.check_fires(lambda: {
            "holdout_items": collections.OrderedDict(
                {"key": {"text": HOLDOUT_TEXT}}),
        })

    def test_user_dict_position(self):
        self.check_fires(lambda: {
            "holdout_items": collections.UserDict(
                {"key": {"text": HOLDOUT_TEXT}}),
        })

    def test_direct_act_controls_still_fire(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                top = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"key": {"text": HOLDOUT_TEXT}},
                    occasion=occasion)
                self.assertTrue(top["fired"])
                self.assertEqual(top["comparisons"], 1)
                view = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"holdout_items": {
                        "key": {"text": HOLDOUT_TEXT},
                    }.values()},
                    occasion=occasion)
                self.assertTrue(view["fired"])
                self.assertEqual(view["comparisons"], 1)
                single = module.audit_instruction_item(
                    HOLDOUT_TEXT,
                    {"holdout_items": {"text": HOLDOUT_TEXT}},
                    occasion=occasion)
                self.assertTrue(single["fired"])
                self.assertEqual(single["comparisons"], 1)

    def test_clean_mapping_position_clears_with_a_comparison(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    CLEAN_TEXT,
                    {"holdout_items": {"key": {"text": HOLDOUT_TEXT}}},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)
        bundle_result = module.audit_at_promotion({
            "holdout_items": {"key": {"text": HOLDOUT_TEXT}},
        })
        self.assertTrue(bundle_result["candidate_bundle_refused"])
        self.assertEqual(bundle_result["comparisons"], 0)


class DirectActSinglePairTests(unittest.TestCase):
    """Ruling 437: the direct act reads a pairs position value
    standing as a single pair, in each container form probed."""

    def check_fires(self, make_bundle):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    HOLDOUT_TEXT, make_bundle(), occasion=occasion)
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_single_pair_in_list_form(self):
        self.check_fires(lambda: {
            "pairs": [dict(CANDIDATE), dict(HOLDOUT_ITEM)],
        })

    def test_single_pair_in_tuple_form(self):
        self.check_fires(lambda: {
            "pairs": (dict(CANDIDATE), dict(HOLDOUT_ITEM)),
        })

    def test_single_pair_in_deque_form(self):
        self.check_fires(lambda: {
            "pairs": collections.deque(
                [dict(CANDIDATE), dict(HOLDOUT_ITEM)]),
        })

    def test_single_pair_in_user_list_form(self):
        self.check_fires(lambda: {
            "pairs": collections.UserList(
                [dict(CANDIDATE), dict(HOLDOUT_ITEM)]),
        })

    def test_direct_act_pair_controls_still_fire(self):
        self.check_fires(lambda: {
            "pairs": [[dict(CANDIDATE), dict(HOLDOUT_ITEM)]],
        })
        self.check_fires(lambda: {
            "pairs": {
                "candidate": dict(CANDIDATE),
                "holdout": dict(HOLDOUT_ITEM),
            },
        })

    def test_clean_single_pair_clears_with_a_comparison(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    CLEAN_TEXT,
                    {"pairs": [dict(CANDIDATE), dict(HOLDOUT_ITEM)]},
                    occasion=occasion)
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)
        for pair in (
            [dict(CANDIDATE), dict(HOLDOUT)],
            [dict(CANDIDATE), dict(CLEAN_HOLDOUT)],
        ):
            bundle_result = module.audit_at_promotion({"pairs": pair})
            self.assertTrue(bundle_result["candidate_bundle_refused"])
            self.assertEqual(bundle_result["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
