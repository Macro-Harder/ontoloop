"""Fix round 10 tests for Region 2: cross split and dataset.

Charges pinned here, from design/steps/step-15-r10-triage.md:
ruling 312 (R10-DAT-1, Low), the materialisation act in
cross_split_audit.py rebuilding a value standing in a
container form that iterates by indexed access alone, with
every iterator inside it replaced once by the list of its
items, or the governed refusal, at both call points; and
ruling 313 (the bundle unwrapping merged defect at the
R10-CS-1 identity, Low, with R10-SPAN-1 counted in the same
act), an item standing in an iterator form, in an abstract
Sequence form, or in a general iterable container form
inside the bundle positions standing read for the item it
carries, split side included, with iterators listed once
and the enumerate form taking its item from second place,
or the governed refusal, at every bundle call point and at
indexed_comparisons.
"""

import collections
import collections.abc
import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"

CALL_POINTS = (
    ("ontoloop.dataset", "candidate construction"),
    ("ontoloop.promote", "promotion"),
)

BUNDLE_SURFACES = (
    "audit_at_promotion",
    "audit_at_build",
    "audit_at_evaluation",
)


def bundle_with(holdout, items=None):
    if items is None:
        items = [{"instruction_text": HOLDOUT_TEXT}]
    return {"instruction_items": items, "holdout_items": holdout}


def call(module_name, occasion, bundle):
    module = harness.require(module_name)
    return module.test_instruction_items_against_holdout(
        bundle, occasion=occasion
    )


def gen_holdout():
    return (v for v in [{"text": HOLDOUT_TEXT}])


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


class IndexedAccessMaterialisationTests(unittest.TestCase):
    """Ruling 312: an iterator standing inside a container
    that iterates by indexed access alone stands materialised
    once, so the second instruction item fires at both call
    points."""

    ITEMS = [
        {"instruction_text": CLEAN_TEXT},
        {"instruction_text": HOLDOUT_TEXT},
    ]

    def check_second(self, make_holdout):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    module_name,
                    occasion,
                    bundle_with(make_holdout(), items=list(self.ITEMS)),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)

    def test_indexed_container_at_top_level(self):
        self.check_second(lambda: IndexedHoldout([gen_holdout()]))

    def test_indexed_container_inside_a_list(self):
        self.check_second(lambda: [IndexedHoldout([gen_holdout()])])

    def test_indexed_container_as_a_mapping_value(self):
        self.check_second(
            lambda: {"first": IndexedHoldout([gen_holdout()])}
        )

    def test_indexed_container_inside_indexed_container(self):
        self.check_second(
            lambda: IndexedHoldout([IndexedHoldout([gen_holdout()])])
        )

    def test_charged_ruling_266_forms_still_fire(self):
        self.check_second(lambda: SequenceWrap([gen_holdout()]))
        self.check_second(lambda: IterableWrap([gen_holdout()]))
        self.check_second(
            lambda: collections.deque([gen_holdout()])
        )

    def test_clean_bundle_still_clears(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    module_name,
                    occasion,
                    bundle_with(
                        IndexedHoldout(
                            [(v for v in [
                                {"text": "separate stored example "
                                         "with other terms"}
                            ])]
                        ),
                        items=[{"instruction_text": CLEAN_TEXT}],
                    ),
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)


class BundleUnwrappingIteratorAndContainerTests(unittest.TestCase):
    """Ruling 313: a bundle item wrapped in an iterator form,
    in an abstract Sequence form, or in a general iterable
    container form inside the bundle positions stands read
    for the item it carries, split side included, at every
    bundle call point and at indexed_comparisons."""

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

    def check_refuses(self, make_bundle):
        module = harness.require("ontoloop.cross_split_audit")
        for surface in BUNDLE_SURFACES:
            with self.subTest(surface=surface):
                result = getattr(module, surface)(make_bundle())
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertFalse(result["promotion_proceeded"])
                self.assertEqual(result["comparisons"], 1)
        with self.subTest(surface="indexed_comparisons"):
            result = module.indexed_comparisons(make_bundle())
            self.assertEqual(result["comparisons"], 1)

    def wrap_forms(self):
        return (
            ("generator", lambda item: (v for v in [item])),
            ("zip", lambda item: zip([item])),
            ("map", lambda item: map(lambda v: v, [item])),
            ("enumerate", lambda item: enumerate([item])),
            ("filter", lambda item: filter(None, [item])),
            ("sequence", lambda item: SequenceWrap([item])),
            ("iterable", lambda item: IterableWrap([item])),
        )

    def test_holdout_wrapped_in_items_position(self):
        for name, wrap in self.wrap_forms():
            with self.subTest(wrap=name):
                self.check_refuses(lambda wrap=wrap: {"items": [
                    dict(self.CANDIDATE), wrap(dict(self.HOLDOUT)),
                ]})

    def test_holdout_wrapped_in_holdout_items_position(self):
        for name, wrap in self.wrap_forms():
            with self.subTest(wrap=name):
                self.check_refuses(lambda wrap=wrap: {
                    "candidate_items": [dict(self.CANDIDATE)],
                    "holdout_items": [wrap(dict(self.HOLDOUT))],
                })

    def test_candidate_wrapped_in_candidate_items_position(self):
        for name, wrap in self.wrap_forms():
            with self.subTest(wrap=name):
                self.check_refuses(lambda wrap=wrap: {
                    "candidate_items": [wrap(dict(self.CANDIDATE))],
                    "holdout_items": [dict(self.HOLDOUT)],
                })

    def test_holdout_wrapped_in_bare_list_bundle(self):
        for name, wrap in self.wrap_forms():
            with self.subTest(wrap=name):
                self.check_refuses(lambda wrap=wrap: [
                    dict(self.CANDIDATE), wrap(dict(self.HOLDOUT)),
                ])

    def test_both_items_wrapped_in_items_position(self):
        self.check_refuses(lambda: {"items": [
            (v for v in [dict(self.CANDIDATE)]),
            SequenceWrap([dict(self.HOLDOUT)]),
        ]})

    def test_enumerate_item_taken_from_second_place(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE),
            enumerate([dict(self.HOLDOUT)]),
        ]})

    def test_plain_dict_control_still_refuses(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE), dict(self.HOLDOUT),
        ]})

    def test_charged_ruling_270_wrap_forms_still_refuse(self):
        for name, wrap in (
            ("list", lambda item: [item]),
            ("tuple", lambda item: (item,)),
            ("deque", lambda item: collections.deque([item])),
            ("userlist", lambda item: collections.UserList([item])),
        ):
            with self.subTest(wrap=name):
                self.check_refuses(lambda wrap=wrap: {"items": [
                    dict(self.CANDIDATE), wrap(dict(self.HOLDOUT)),
                ]})


if __name__ == "__main__":
    unittest.main()
