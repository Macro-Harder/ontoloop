"""Fix round 18 tests for Region 3: promote wrapper.

Written first for two positions at Round 18 triage
rulings 668 and 669: ruling 668 (R18-PRO-1, Low), the
promote wrapper detection and materialisation acts
deciding single use material by the identity test
alone, so material that is single use in substance
but does not stand in that identity form stands
listed by the detection act before any materialisation
runs, in three limbs, a container whose iteration act
returns a fresh wrapper object on each call delegating
to one stored iterator, a getitem only container
backed by a stored iterator at the wrapped position,
and a container whose iteration act permits one call;
and ruling 669 (R18-PRO-2, Low), an iterator form
standing as an element of a set or frozenset at the
wrapped position standing spent by the failed set
rebuild and the fallback that follows it. Ruling 616
stands cured in its charged form and stands not
reopened by any pin here: its forms stand as controls.
"""

import itertools
import unittest

from tests.harness import require

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _nested_position(text=HOLDOUT_TEXT):
    return {"key": {"inner": {"text": text}}}


class _GeneratorBackedIterable:
    """The cured ruling 616 class: one stored generator."""

    def __init__(self, items):
        self._stored = (item for item in items)

    def __iter__(self):
        return self._stored


class _ListIteratorBackedIterable:
    """The cured ruling 616 class: one stored list iterator."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return self._stored


class _GeneratorFunctionForm:
    """Limb one: the iteration act is a generator function
    yielding from one stored generator."""

    def __init__(self, items):
        self._stored = (item for item in items)

    def __iter__(self):
        yield from self._stored


class _GeneratorExpressionForm:
    """Limb one: the iteration act returns a generator
    expression over one stored list iterator."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return (item for item in self._stored)


class _MapObjectForm:
    """Limb one: the iteration act returns a map object
    over one stored list iterator."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return map(lambda item: item, self._stored)


class _ChainObjectForm:
    """Limb one: the iteration act returns an itertools
    chain object over one stored list iterator."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return itertools.chain(self._stored)


class _DelegatingIterator:
    """An iterator object delegating to one stored iterator."""

    def __init__(self, stored):
        self._stored = stored

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._stored)


class _FreshIteratorObjectForm:
    """Line E-7, first class: the iteration act returns a
    fresh iterator object on each call, delegating in its
    turn to one stored iterator."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __iter__(self):
        return _DelegatingIterator(self._stored)


class _FreshGeneratorForm:
    """Line E-7, second class: the iteration act returns a
    fresh generator on each call over one stored generator."""

    def __init__(self, items):
        self._stored = (item for item in items)

    def __iter__(self):
        return (item for item in self._stored)


class _GetitemOnlyForm:
    """Limb two: no iteration act of its own, and the
    getitem act returns the next element of one stored
    iterator in sequence."""

    def __init__(self, items):
        self._stored = iter(list(items))

    def __getitem__(self, index):
        try:
            return next(self._stored)
        except StopIteration:
            raise IndexError(index)


class _ReIterableGetitemForm:
    """A getitem only container backed by an indexable list."""

    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, index):
        return self._items[index]


class _OneIterationOnlyForm:
    """Limb three: the iteration act permits one iteration
    and raises RuntimeError on a second call."""

    def __init__(self, items):
        self._items = list(items)
        self._used = False

    def __iter__(self):
        if self._used:
            raise RuntimeError("second iteration not permitted")
        self._used = True
        return iter(self._items)


class _HashableReIterableContainer:
    """A re-iterable container standing hashable by identity,
    holding a nested mapping, for the set control."""

    def __init__(self, items):
        self._items = list(items)

    def __iter__(self):
        return iter(self._items)

    def __hash__(self):
        return object.__hash__(self)


_FRESH_WRAPPER_FORMS = (
    _GeneratorFunctionForm,
    _GeneratorExpressionForm,
    _MapObjectForm,
    _ChainObjectForm,
    _FreshIteratorObjectForm,
    _FreshGeneratorForm,
)


class _WrapperCase(unittest.TestCase):
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


class TestPromoteFixR18SingleUseForms(_WrapperCase):
    """Ruling 668, R18-PRO-1: single use material the
    identity test does not recognise, in three limbs."""

    def test_generator_function_form_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": _GeneratorFunctionForm(
                [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_generator_expression_form_fires_through_wrapper(self):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": _GeneratorExpressionForm(
                    [_nested_position()])}
            )
            self._assert_fires(outcome)

    def test_map_object_form_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": _MapObjectForm([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_chain_object_form_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": _ChainObjectForm([_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_fresh_iterator_object_form_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": _FreshIteratorObjectForm(
                [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_fresh_generator_form_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": _FreshGeneratorForm(
                [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_direct_act_fires_on_fresh_wrapper_presentations(self):
        for factory in _FRESH_WRAPPER_FORMS:
            with self.subTest(factory=factory.__name__):
                outcome = self._direct(
                    {"holdout_items": factory([_nested_position()])}
                )
                self.assertTrue(outcome["fired"])
                self.assertEqual(outcome["comparisons"], 1)

    def test_fresh_wrapper_inside_mapping_value_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {"inner": _GeneratorExpressionForm(
                [_nested_position()])}}
        )
        self._assert_fires(outcome)

    def test_fresh_wrapper_inside_tuple_and_list_fires(self):
        outcome = self._wrapper(
            {"holdout_items": (_GeneratorFunctionForm(
                [_nested_position()]),)}
        )
        self._assert_fires(outcome)
        outcome = self._wrapper(
            {"holdout_items": [[_MapObjectForm(
                [_nested_position()])]]}
        )
        self._assert_fires(outcome)

    def test_fresh_wrapper_fires_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": _ChainObjectForm(
                    [_nested_position()])
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_fresh_wrapper_fires_after_partial_scoring(self):
        outcome = self._wrapper(
            {"holdout_items": _GeneratorExpressionForm(
                [_nested_position()])},
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_fresh_wrapper_fires_on_second_instruction_item(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        ]
        outcome = self._wrapper(
            {"holdout_items": _FreshGeneratorForm(
                [_nested_position()])},
            items=items,
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_fresh_wrapper_clears_through_wrapper(self):
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        for factory in _FRESH_WRAPPER_FORMS:
            with self.subTest(factory=factory.__name__):
                outcome = self._wrapper(
                    {"holdout_items": factory([clean_position])}
                )
                self._assert_clears(outcome)

    def test_getitem_only_form_fires_through_wrapper(self):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": _GetitemOnlyForm(
                    [_nested_position()])}
            )
            self._assert_fires(outcome)

    def test_direct_act_fires_on_getitem_only_presentation(self):
        outcome = self._direct(
            {"holdout_items": _GetitemOnlyForm([_nested_position()])}
        )
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 1)

    def test_getitem_only_inside_mapping_value_stays_in_parity(self):
        wrapper_outcome = self._wrapper(
            {"holdout_items": {"inner": _GetitemOnlyForm(
                [_nested_position()])}}
        )
        self.assertFalse(wrapper_outcome["fired"])
        direct_outcome = self._direct(
            {"holdout_items": {"inner": _GetitemOnlyForm(
                [_nested_position()])}}
        )
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)

    def test_reiterable_getitem_container_still_fires(self):
        outcome = self._wrapper(
            {"holdout_items": _ReIterableGetitemForm(
                [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_one_iteration_only_hit_fires_through_wrapper(self):
        outcome = self._wrapper(
            {"holdout_items": _OneIterationOnlyForm(
                [_nested_position()])}
        )
        self._assert_fires(outcome)

    def test_one_iteration_only_clean_clears_through_wrapper(self):
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        outcome = self._wrapper(
            {"holdout_items": _OneIterationOnlyForm(
                [clean_position])}
        )
        self._assert_clears(outcome)

    def test_direct_act_decides_one_iteration_only_forms(self):
        outcome = self._direct(
            {"holdout_items": _OneIterationOnlyForm(
                [_nested_position()])}
        )
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 1)
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        outcome = self._direct(
            {"holdout_items": _OneIterationOnlyForm(
                [clean_position])}
        )
        self.assertFalse(outcome["fired"])

    def test_detection_act_does_not_spend_recognised_forms(self):
        module = require("ontoloop.promote")
        for factory in (
            _GeneratorExpressionForm,
            _FreshGeneratorForm,
        ):
            with self.subTest(factory=factory.__name__):
                container = factory([_nested_position()])
                detected = module._wrapper_subtree_has_iterator(
                    container, frozenset()
                )
                self.assertTrue(detected)
                self.assertEqual(
                    list(container), [_nested_position()]
                )
        container = _OneIterationOnlyForm([_nested_position()])
        detected = module._wrapper_subtree_has_iterator(
            container, frozenset()
        )
        self.assertTrue(detected)
        self.assertEqual(list(container), [_nested_position()])
        container = _GetitemOnlyForm([_nested_position()])
        detected = module._wrapper_subtree_has_iterator(
            container, frozenset()
        )
        self.assertTrue(detected)
        self.assertEqual(list(container), [_nested_position()])

    def test_materialised_fresh_wrapper_reads_in_full_twice(self):
        module = require("ontoloop.promote")
        shared = require("ontoloop.cross_split_audit")
        material = module._materialise_holdout_for_wrapper(
            {"holdout_items": _GeneratorExpressionForm(
                [_nested_position()])},
            shared,
        )
        for _trial in range(2):
            outcome = shared.audit_instruction_item(
                HOLDOUT_TEXT, material, occasion="promotion"
            )
            self.assertTrue(outcome["fired"])
            self.assertEqual(outcome["comparisons"], 1)

    def test_cured_single_pass_forms_still_fire_through_wrapper(self):
        for factory in (
            _GeneratorBackedIterable,
            _ListIteratorBackedIterable,
        ):
            with self.subTest(factory=factory.__name__):
                outcome = self._wrapper(
                    {"holdout_items": factory([_nested_position()])}
                )
                self._assert_fires(outcome)


class TestPromoteFixR18SetForms(_WrapperCase):
    """Ruling 669, R18-PRO-2: an iterator form standing as
    an element of a set or frozenset at the wrapped position."""

    def test_set_holding_cured_class_fires_through_wrapper(self):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": {_GeneratorBackedIterable(
                    [_nested_position()])}}
            )
            self._assert_fires(outcome)

    def test_set_holding_generator_fires_through_wrapper(self):
        for _trial in range(3):
            outcome = self._wrapper(
                {"holdout_items": {
                    (item for item in [_nested_position()])}}
            )
            self._assert_fires(outcome)

    def test_frozenset_holding_cured_class_fires(self):
        outcome = self._wrapper(
            {"holdout_items": frozenset([
                _GeneratorBackedIterable([_nested_position()])])}
        )
        self._assert_fires(outcome)

    def test_frozenset_holding_generator_fires(self):
        outcome = self._wrapper(
            {"holdout_items": frozenset([
                (item for item in [_nested_position()])])}
        )
        self._assert_fires(outcome)

    def test_set_holding_list_iterator_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {iter([_nested_position()])}}
        )
        self._assert_fires(outcome)

    def test_set_form_inside_mapping_value_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {"inner": {
                (item for item in [_nested_position()])}}}
        )
        self._assert_fires(outcome)

    def test_set_holding_generator_item_field_mapping_fires(self):
        item_field = {"instruction_text": HOLDOUT_TEXT}
        outcome = self._wrapper(
            {"holdout_items": {(item for item in [item_field])}}
        )
        self._assert_fires(outcome)

    def test_set_holding_cured_class_two_nested_mappings_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {_GeneratorBackedIterable(
                [_nested_position(), _nested_position()])}}
        )
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 2
        )

    def test_set_forms_fire_at_candidate_construction(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "holdout_items": {
                    (item for item in [_nested_position()])}
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_set_forms_fire_after_partial_scoring(self):
        outcome = self._wrapper(
            {"holdout_items": {_GeneratorBackedIterable(
                [_nested_position()])}},
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_set_forms_fire_on_second_instruction_item(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        ]
        outcome = self._wrapper(
            {"holdout_items": {
                (item for item in [_nested_position()])}},
            items=items,
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_clean_set_forms_clear_through_wrapper(self):
        clean_position = _nested_position(
            "unrelated wording entirely"
        )
        outcome = self._wrapper(
            {"holdout_items": {
                (item for item in [clean_position])}}
        )
        self._assert_clears(outcome)
        outcome = self._wrapper(
            {"holdout_items": {_GeneratorBackedIterable(
                [clean_position])}}
        )
        self._assert_clears(outcome)

    def test_set_holding_reiterable_hashable_container_fires(self):
        outcome = self._wrapper(
            {"holdout_items": {_HashableReIterableContainer(
                [_nested_position()])}}
        )
        self._assert_fires(outcome)

    def test_direct_act_fires_on_fresh_set_presentations(self):
        outcome = self._direct(
            {"holdout_items": {
                (item for item in [_nested_position()])}}
        )
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 1)
        outcome = self._direct(
            {"holdout_items": {_GeneratorBackedIterable(
                [_nested_position(), _nested_position()])}}
        )
        self.assertTrue(outcome["fired"])
        self.assertEqual(outcome["comparisons"], 2)

    def test_materialised_set_form_reads_in_full_twice(self):
        module = require("ontoloop.promote")
        shared = require("ontoloop.cross_split_audit")
        material = module._materialise_holdout_for_wrapper(
            {"holdout_items": {
                (item for item in [_nested_position()])}},
            shared,
        )
        for _trial in range(2):
            outcome = shared.audit_instruction_item(
                HOLDOUT_TEXT, material, occasion="promotion"
            )
            self.assertTrue(outcome["fired"])
            self.assertEqual(outcome["comparisons"], 1)


if __name__ == "__main__":
    unittest.main()
