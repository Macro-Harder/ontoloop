"""Fix round 17 tests for Region 3: promote wrapper and redact.

Written first for two positions at Round 17 triage
rulings 616 and 617: ruling 616 (R17-PRO-1, Low), the
promote wrapper detection act in promote.py listing a
single pass iterable at the wrapped position a second
time after its first listing spent it, so the nested
mapping it carries states no finding and the wrapper
clears, where the direct act on a fresh presentation
of the same shape fires; and ruling 617 (R17-CR-1,
Low), the redact floor reading in redact.py counting
the state value itself as floor content in the set
form limb of the beside content act, so a set form
element whose only member beyond its pair stands at
zero bytes releases instead of failing closed, where
the mapping form and sequence form elements on
identical substance fail closed. No act here touches
ontoloop/capture.py as a product act: capture.py
stands named as a standing test home surface of this
region and carries no act in this round. No act here
touches any direct act reading in
ontoloop/cross_split_audit.py.
"""

import collections
import unittest

from tests.harness import require

CLEAN = "a routine clean note"
HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


class _SetContainer(collections.abc.Set):
    """A container standing in the abstract set form."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items


class _GeneratorBackedIterable:
    """A single pass iterable backed by a stored generator.

    The class carries no next method of its own, and
    its iter act returns one stored generator, so the
    iterable stands listed once only.
    """

    def __init__(self, items):
        self._stored = (item for item in items)

    def __iter__(self):
        return self._stored


class _ListIteratorBackedIterable:
    """A single pass iterable backed by a stored list iterator."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class _ReIterableContainer:
    """A container whose iter act returns a fresh iterator."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)


def _nested_position(text=HOLDOUT_TEXT):
    return {"key": {"inner": {"text": text}}}


def _hit_bytes(module):
    return module.secret_bearing_shapes()[0]["raw_bytes"]


class TestPromoteFixR17SinglePassIterable(unittest.TestCase):
    """Ruling 616, R17-PRO-1: a single pass iterable at
    the wrapped position of the promote wrapper."""

    def _wrapper(self, holdout_material, items=None, **kwargs):
        module = require("ontoloop.promote")
        if items is None:
            items = [{"instruction_text": HOLDOUT_TEXT}]
        bundle = {
            "instruction_items": items,
            "holdout_items": holdout_material,
        }
        return module.test_instruction_items_against_holdout(
            bundle, occasion="promotion", **kwargs
        )

    def _direct(self, holdout_material):
        module = require("ontoloop.cross_split_audit")
        return module.audit_instruction_item(
            HOLDOUT_TEXT, holdout_material, occasion="promotion"
        )

    def _assert_fires(self, outcome):
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["promotion_proceeds"])

    def _assert_clears(self, outcome):
        self.assertFalse(outcome["fired"])
        self.assertTrue(
            outcome["test_result_carried_on_promotion_record"]
        )

    def test_generator_backed_iterable_fires_through_wrapper(self):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": _GeneratorBackedIterable(
                    [_nested_position()])}
            )
            self._assert_fires(outcome)

    def test_list_iterator_backed_iterable_fires_through_wrapper(
        self,
    ):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": _ListIteratorBackedIterable(
                    [_nested_position()])}
            )
            self._assert_fires(outcome)

    def test_direct_act_fires_on_fresh_single_pass_presentations(
        self,
    ):
        for factory in (
            _GeneratorBackedIterable,
            _ListIteratorBackedIterable,
        ):
            outcome = self._direct(
                {"holdout_items": factory([_nested_position()])}
            )
            self.assertTrue(outcome["fired"])
            self.assertEqual(outcome["comparisons"], 1)

    def test_reiterable_container_still_fires_through_wrapper(
        self,
    ):
        outcome = self._wrapper(
            {"holdout_items": _ReIterableContainer(
                [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_clean_single_pass_iterable_clears_through_wrapper(
        self,
    ):
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        for factory in (
            _GeneratorBackedIterable,
            _ListIteratorBackedIterable,
        ):
            with self.subTest(factory=factory.__name__):
                outcome = self._wrapper(
                    {"holdout_items": factory([clean_position])}
                )
                self._assert_clears(outcome)

    def test_single_pass_inside_mapping_value_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {"inner": _GeneratorBackedIterable(
                [_nested_position()])}}
        )
        self._assert_fires(outcome)

    def test_single_pass_fires_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": _GeneratorBackedIterable(
                    [_nested_position()])
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_single_pass_fires_after_partial_scoring(self):
        outcome = self._wrapper(
            {"holdout_items": _GeneratorBackedIterable(
                [_nested_position()])},
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_single_pass_fires_on_second_instruction_item(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        ]
        outcome = self._wrapper(
            {"holdout_items": _GeneratorBackedIterable(
                [_nested_position()])},
            items=items,
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_detection_act_does_not_spend_single_pass_iterable(
        self,
    ):
        module = require("ontoloop.promote")
        for factory in (
            _GeneratorBackedIterable,
            _ListIteratorBackedIterable,
        ):
            with self.subTest(factory=factory.__name__):
                iterable = factory([_nested_position()])
                detected = module._wrapper_subtree_has_iterator(
                    iterable, frozenset()
                )
                self.assertTrue(detected)
                self.assertEqual(
                    list(iterable), [_nested_position()]
                )

    def test_materialised_single_pass_reads_in_full_twice(self):
        module = require("ontoloop.promote")
        shared = require("ontoloop.cross_split_audit")
        material = module._materialise_holdout_for_wrapper(
            {"holdout_items": _GeneratorBackedIterable(
                [_nested_position()])},
            shared,
        )
        for _trial in range(2):
            outcome = shared.audit_instruction_item(
                HOLDOUT_TEXT, material, occasion="promotion"
            )
            self.assertTrue(outcome["fired"])
            self.assertEqual(outcome["comparisons"], 1)

    def test_wrapper_controls_still_decide(self):
        self._assert_fires(self._wrapper(
            {"holdout_items": _nested_position()}
        ))
        self._assert_fires(self._wrapper(
            {"holdout_items": (_nested_position(),)}
        ))
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        self._assert_clears(self._wrapper(
            {"holdout_items": clean_position}
        ))


class TestRedactFixR17SetFormFloor(unittest.TestCase):
    """Ruling 617, R17-CR-1: the set form limb of the
    redact floor reading counting the state value."""

    def _assert_fails_closed(self, outcome):
        self.assertTrue(outcome["refused"])
        self.assertEqual(
            outcome["form"], "no exit scan result, no exit"
        )

    def _assert_releases(self, outcome):
        self.assertFalse(outcome["refused"])

    def _scan(self, assembly):
        module = require("ontoloop.redact")
        return module.exit_scan(assembly)

    def _floor(self, assembly):
        module = require("ontoloop.redact")
        return module._assembly_content(
            assembly, _skip_top_state=True
        )

    def test_set_element_empty_string_beyond_pair_fails_closed(
        self,
    ):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                element = {"assembly_state", state, ""}
                self._assert_fails_closed(self._scan([element]))

    def test_floor_on_set_element_zero_member_counts_no_state(
        self,
    ):
        element = {"assembly_state", "ready", ""}
        self.assertEqual(self._floor([element]), [""])

    def test_set_element_empty_bytes_beyond_pair_fails_closed(
        self,
    ):
        element = {"assembly_state", "ready", b""}
        self._assert_fails_closed(self._scan([element]))
        self.assertEqual(self._floor([element]), [b""])

    def test_set_element_empty_tuple_beyond_pair_fails_closed(
        self,
    ):
        element = {"assembly_state", "ready", ()}
        self._assert_fails_closed(self._scan([element]))
        self.assertEqual(self._floor([element]), [])

    def test_set_element_empty_frozenset_beyond_pair_fails(
        self,
    ):
        element = {"assembly_state", "ready", frozenset()}
        self._assert_fails_closed(self._scan([element]))
        self.assertEqual(self._floor([element]), [])

    def test_set_element_tuple_of_empty_beyond_pair_fails(
        self,
    ):
        element = {"assembly_state", "ready", ("",)}
        self._assert_fails_closed(self._scan([element]))
        self.assertEqual(self._floor([element]), [""])

    def test_frozenset_element_zero_member_fails_closed(self):
        element = frozenset({"assembly_state", "ready", ""})
        self._assert_fails_closed(self._scan([element]))

    def test_abstract_set_element_zero_member_fails_closed(self):
        element = _SetContainer(["assembly_state", "ready", ""])
        self._assert_fails_closed(self._scan([element]))

    def test_set_element_zero_member_in_tuple_assembly_fails(
        self,
    ):
        element = {"assembly_state", "ready", ""}
        self._assert_fails_closed(self._scan((element,)))

    def test_mapping_and_sequence_zero_forms_still_fail_closed(
        self,
    ):
        mapping = {"assembly_state": "ready", "note": ""}
        self._assert_fails_closed(self._scan([mapping]))
        self.assertEqual(self._floor([mapping]), [""])
        sequence = ["assembly_state", "ready", ""]
        self._assert_fails_closed(self._scan([sequence]))
        self.assertEqual(self._floor([sequence]), [""])

    def test_clean_set_element_still_releases(self):
        for state in ("ready", "some unknown state"):
            with self.subTest(state=state):
                element = {"assembly_state", state, CLEAN}
                self._assert_releases(self._scan([element]))

    def test_floor_counts_clean_member_on_set_element(self):
        element = {"assembly_state", "ready", CLEAN}
        floor = self._floor([element])
        self.assertIn(CLEAN, floor)
        self.assertNotIn("assembly_state", floor)

    def test_set_element_tuple_carrying_clean_note_releases(
        self,
    ):
        element = {"assembly_state", "ready", (CLEAN,)}
        self._assert_releases(self._scan([element]))

    def test_two_member_set_element_still_fails_closed(self):
        element = {"assembly_state", "ready"}
        self._assert_fails_closed(self._scan([element]))
        self.assertEqual(self._floor([element]), [])

    def test_empty_member_set_beside_clean_pair_releases(self):
        element = {"assembly_state", "ready", ""}
        assembly = [element, ("content", CLEAN)]
        self._assert_releases(self._scan(assembly))

    def test_hit_member_beyond_pair_in_set_form_refuses(self):
        module = require("ontoloop.redact")
        hit = _hit_bytes(module)
        element = {"assembly_state", "ready", hit}
        outcome = module.exit_scan([element])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["refused_scope"], "whole")
        self.assertFalse(outcome["released_in_part"])


if __name__ == "__main__":
    unittest.main()
