"""Fix round 11 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r11-triage.md:
ruling 351 (R11-DAT-1, Low), the pairs limb of the partitioning
act in cross_split_audit.py reading each side of a pair, in
both pair forms, through the same unwrapping act the other
bundle positions use, or the governed refusal, at every bundle
call point and at indexed_comparisons; ruling 352 (the direct
act merged defect at the R11-CS-1 identity, Low, with
R11-SPAN-1 counted in the same act), the direct act
audit_instruction_item reading a value standing in a container
form that iterates by indexed access alone for the material it
carries, in parity with the materialisation reading under
ruling 312, or the governed refusal, at both occasions; and
ruling 357 (Lead Engineer line E-8, Low), the partitioning act
reading a position value standing in a deque form, a UserList
form, an abstract Sequence form, or a general iterable
container form, with iterators listed once, and a pairs
position standing in those forms and a bare bundle standing
as a deque or a general iterable container, for the items
those positions carry, or the governed refusal in a form that
states no pair stood compared as its ground, at the three
audit surfaces and at indexed_comparisons.
"""

import collections
import collections.abc
import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"

OCCASIONS = ("candidate construction", "promotion")

CALL_POINTS = (
    ("ontoloop.dataset", "candidate construction"),
    ("ontoloop.promote", "promotion"),
)

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
    """A container iterating only by indexed access.

    The class carries no iteration act of its own, stands
    registered as no abstract Sequence, and iterates only
    through its indexed access act, which raises IndexError
    past its last element through the list it holds.
    """

    def __init__(self, elements):
        self._elements = list(elements)

    def __getitem__(self, index):
        return self._elements[index]


class SequenceWrap(collections.abc.Sequence):
    """An abstract Sequence subclass holding its elements."""

    def __init__(self, elements):
        self._elements = list(elements)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]


class IterableWrap:
    """A general iterable container holding its elements."""

    def __init__(self, elements):
        self._elements = list(elements)

    def __iter__(self):
        return iter(self._elements)


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


def check_proceeds_with_one_comparison(test_case, make_bundle):
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


class PairsUnwrappingTests(unittest.TestCase):
    """Ruling 351: each side of a pair, in both pair forms,
    stands read through the unwrapping act, so a wrapped side
    reaches a comparison as the item it carries."""

    def wrap_forms(self):
        return (
            ("list", lambda item: [item]),
            ("tuple", lambda item: (item,)),
            ("deque", lambda item: collections.deque([item])),
            ("userlist", lambda item: collections.UserList([item])),
            ("generator", lambda item: (v for v in [item])),
        )

    def test_holdout_side_wrapped_in_pairs_list_form(self):
        for name, wrap in self.wrap_forms():
            with self.subTest(wrap=name):
                check_refuses(self, lambda wrap=wrap: {"pairs": [
                    [dict(CANDIDATE), wrap(dict(HOLDOUT))],
                ]})

    def test_candidate_side_wrapped_in_generator_in_pairs(self):
        check_refuses(self, lambda: {"pairs": [
            [(v for v in [dict(CANDIDATE)]), dict(HOLDOUT)],
        ]})

    def test_holdout_entry_wrapped_in_mapping_form_pair(self):
        for name, wrap in (
            ("list", lambda item: [item]),
            ("generator", lambda item: (v for v in [item])),
        ):
            with self.subTest(wrap=name):
                check_refuses(self, lambda wrap=wrap: {"pairs": [
                    {
                        "candidate": dict(CANDIDATE),
                        "holdout": wrap(dict(HOLDOUT)),
                    },
                ]})

    def test_dataset_record_surface_refuses_wrapped_pairs(self):
        module = harness.require("ontoloop.dataset")
        result = module.cross_split_audit_at_build({"pairs": [
            [dict(CANDIDATE), (v for v in [dict(HOLDOUT)])],
        ]})
        shared = result["cross_split_audit_result"]
        self.assertTrue(shared["candidate_bundle_refused"])
        self.assertEqual(shared["comparisons"], 1)

    def test_plain_pairs_controls_still_refuse(self):
        check_refuses(self, lambda: {"pairs": [
            [dict(CANDIDATE), dict(HOLDOUT)],
        ]})
        check_refuses(self, lambda: {"pairs": [
            {
                "candidate": dict(CANDIDATE),
                "holdout": dict(HOLDOUT),
            },
        ]})

    def test_clean_wrapped_pair_proceeds_with_one_comparison(self):
        check_proceeds_with_one_comparison(self, lambda: {"pairs": [
            [dict(CANDIDATE), [dict(CLEAN_HOLDOUT)]],
        ]})


class DirectActIndexedAccessTests(unittest.TestCase):
    """Ruling 352: holdout material, and an instruction text,
    standing in a container form that iterates by indexed
    access alone stand read by the direct act for the
    material they carry, at both occasions."""

    def check_fires(self, make_holdout, instruction=HOLDOUT_TEXT):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    instruction,
                    make_holdout(),
                    occasion=occasion,
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_indexed_at_top_level_holding_a_mapping(self):
        self.check_fires(
            lambda: IndexedHoldout([{"text": HOLDOUT_TEXT}])
        )

    def test_indexed_holding_a_generator_of_a_mapping(self):
        self.check_fires(
            lambda: IndexedHoldout(
                [(v for v in [{"text": HOLDOUT_TEXT}])]
            )
        )

    def test_indexed_holding_the_plain_holdout_text(self):
        self.check_fires(lambda: IndexedHoldout([HOLDOUT_TEXT]))

    def test_indexed_inside_a_list(self):
        self.check_fires(
            lambda: [IndexedHoldout([{"text": HOLDOUT_TEXT}])]
        )

    def test_indexed_as_a_mapping_value(self):
        self.check_fires(
            lambda: {"first": IndexedHoldout([{"text": HOLDOUT_TEXT}])}
        )

    def test_indexed_inside_an_abstract_sequence(self):
        self.check_fires(
            lambda: SequenceWrap(
                [IndexedHoldout([{"text": HOLDOUT_TEXT}])]
            )
        )

    def test_indexed_inside_an_indexed_container(self):
        self.check_fires(
            lambda: IndexedHoldout(
                [IndexedHoldout([{"text": HOLDOUT_TEXT}])]
            )
        )

    def test_instruction_text_standing_as_an_indexed_container(self):
        self.check_fires(
            lambda: [{"text": HOLDOUT_TEXT}],
            instruction=IndexedHoldout([HOLDOUT_TEXT]),
        )

    def test_clean_indexed_holdout_clears_with_a_comparison(self):
        module = harness.require("ontoloop.cross_split_audit")
        for occasion in OCCASIONS:
            with self.subTest(occasion=occasion):
                result = module.audit_instruction_item(
                    CLEAN_TEXT,
                    IndexedHoldout([{"text": HOLDOUT_TEXT}]),
                    occasion=occasion,
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_call_points_still_fire_on_the_same_forms(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        ]
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                module = harness.require(module_name)
                result = module.test_instruction_items_against_holdout(
                    {
                        "instruction_items": list(items),
                        "holdout_items": IndexedHoldout(
                            [(v for v in [{"text": HOLDOUT_TEXT}])]
                        ),
                    },
                    occasion=occasion,
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)


class PartitioningPositionFormTests(unittest.TestCase):
    """Ruling 357: the partitioning act reads a position value
    standing in a deque form, a UserList form, an abstract
    Sequence form, or a general iterable container form, with
    iterators listed once, and a pairs position standing in
    those forms and a bare bundle standing as a deque or a
    general iterable container, for the items those positions
    carry."""

    def position_forms(self):
        return (
            ("deque", lambda items: collections.deque(items)),
            ("userlist", lambda items: collections.UserList(items)),
            ("sequence", lambda items: SequenceWrap(items)),
            ("iterable", lambda items: IterableWrap(items)),
            ("generator", lambda items: (v for v in items)),
        )

    def test_side_positions_in_each_form(self):
        for name, form in self.position_forms():
            with self.subTest(form=name):
                check_refuses(self, lambda form=form: {
                    "candidate_items": form([dict(CANDIDATE)]),
                    "holdout_items": form([dict(HOLDOUT)]),
                })
                check_proceeds_with_one_comparison(
                    self, lambda form=form: {
                        "candidate_items": form([dict(CANDIDATE)]),
                        "holdout_items": form([dict(CLEAN_HOLDOUT)]),
                    }
                )

    def test_items_position_as_a_deque(self):
        check_refuses(self, lambda: {
            "items": collections.deque(
                [dict(CANDIDATE), dict(HOLDOUT)]
            ),
        })
        check_proceeds_with_one_comparison(self, lambda: {
            "items": collections.deque(
                [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]
            ),
        })

    def test_items_position_in_sequence_and_iterable_forms(self):
        for name, form in (
            ("sequence", lambda items: SequenceWrap(items)),
            ("iterable", lambda items: IterableWrap(items)),
        ):
            with self.subTest(form=name):
                check_refuses(self, lambda form=form: {
                    "items": form([dict(CANDIDATE), dict(HOLDOUT)]),
                })

    def test_pairs_position_as_a_deque(self):
        check_refuses(self, lambda: {
            "pairs": collections.deque(
                [[dict(CANDIDATE), dict(HOLDOUT)]]
            ),
        })
        check_proceeds_with_one_comparison(self, lambda: {
            "pairs": collections.deque(
                [[dict(CANDIDATE), dict(CLEAN_HOLDOUT)]]
            ),
        })

    def test_pairs_standing_as_deque_and_sequence_pairs(self):
        check_refuses(self, lambda: {"pairs": [
            collections.deque([dict(CANDIDATE), dict(HOLDOUT)]),
        ]})
        check_refuses(self, lambda: {"pairs": [
            SequenceWrap([dict(CANDIDATE), dict(HOLDOUT)]),
        ]})

    def test_bare_bundle_as_a_deque(self):
        check_refuses(self, lambda: collections.deque(
            [dict(CANDIDATE), dict(HOLDOUT)]
        ))
        check_proceeds_with_one_comparison(
            self, lambda: collections.deque(
                [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]
            )
        )

    def test_bare_bundle_as_a_general_iterable_container(self):
        check_refuses(self, lambda: IterableWrap(
            [dict(CANDIDATE), dict(HOLDOUT)]
        ))
        check_proceeds_with_one_comparison(
            self, lambda: IterableWrap(
                [dict(CANDIDATE), dict(CLEAN_HOLDOUT)]
            )
        )

    def test_list_and_tuple_controls_still_decide(self):
        check_refuses(self, lambda: {
            "candidate_items": [dict(CANDIDATE)],
            "holdout_items": (dict(HOLDOUT),),
        })
        check_proceeds_with_one_comparison(self, lambda: {
            "candidate_items": (dict(CANDIDATE),),
            "holdout_items": [dict(CLEAN_HOLDOUT)],
        })


if __name__ == "__main__":
    unittest.main()
