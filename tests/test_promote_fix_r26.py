"""Fix round 26 tests for Region 3: promote wrapper.

Written first for three positions at Round 26 triage
rulings 1196 (S15-R26-SPAN-1, Low), 1197 (S15-R26-PRO-1,
Low), and 1198 (S15-R26-PRO-2, Low). Ruling 1196: key
material through a dictionary view inside a single pass
element of a delegating container subclass standing as
a mapping value at a governed position, firing at the
promote wrapper where the direct act and the dataset
surface clear it. Ruling 1197: a nested mapping inside
a delegating concrete container subclass inside a
mapping standing as an item of a delegating ChainMap
subclass, clearing through the promote wrapper where
the direct act fires on the presentation. Ruling 1198:
a keys view carrying a single pass form or carrying
byte text, standing inside a mapping standing as an
item of a delegating ChainMap subclass, clearing
through the promote wrapper where the direct act fires
on the presentation. Rulings 1105, 1106, and 1107 stand
cured in their bounded forms and stand not reopened by
any pin here: their charged forms stand as poles,
beside the standing parity forms the Round 26 papers
name.
"""

import unittest
from collections import deque

from tests.harness import require
from tests.test_cross_fix_r20 import HashableItem, inner_mapping
from tests.test_promote_fix_r21 import GetitemOnlyForm
from tests.test_promote_fix_r22 import (
    AbstractSetSubclass,
    DequeSubclass,
    DelegatingChainMapSubclass,
    ListSubclass,
    SequenceSubclass,
    SetSubclass,
    SinglePassIterable,
    TupleSubclass,
    UserListSubclass,
    _chainmap_item,
    _clean_position,
    _generator_of,
    _nested_position,
)

HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"


def _wrapped_key(text=HOLDOUT_TEXT):
    if text == HOLDOUT_TEXT:
        return (HashableItem(inner_mapping()),)
    return (HashableItem({"inner": {"text": text}}),)


def _keys_view(text=HOLDOUT_TEXT):
    return {_wrapped_key(text): 1}.keys()


def _items_view(text=HOLDOUT_TEXT):
    return {_wrapped_key(text): 1}.items()


def _keys_view_of_generator():
    return {_generator_of(_nested_position()): 1}.keys()


def _keys_view_of_bytes():
    return {HOLDOUT_TEXT.encode(): 1}.keys()


def _items_view_of_generator():
    return {1: _generator_of(_nested_position())}.items()


def _values_view_of_generator():
    return {1: _generator_of(_nested_position())}.values()


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

    def _dataset(self, holdout_material):
        module = require("ontoloop.dataset")
        bundle = {
            "instruction_items": [{"text": HOLDOUT_TEXT}],
            "holdout_items": holdout_material,
        }
        return module.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )

    def _assert_fires(self, outcome):
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["promotion_proceeds"])

    def _assert_clears(self, outcome):
        self.assertFalse(outcome["fired"])
        self.assertTrue(
            outcome["test_result_carried_on_promotion_record"]
        )

    def _assert_chainmap_pair_fires(self, make_item):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def _assert_chainmap_pair_clears(self, make_item, direct_comparisons):
        outcome = self._wrapper(_chainmap_item(make_item()))
        self._assert_clears(outcome)
        direct_outcome = self._direct(_chainmap_item(make_item()))
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(
            direct_outcome["comparisons"], direct_comparisons
        )


class TestPromoteFixR26ViewInSinglePassElement(_WrapperCase):
    """Ruling 1196, S15-R26-SPAN-1: a dictionary view
    inside a single pass element of a delegating
    container subclass standing as a mapping value."""

    def _assert_three_surface_clears(self, make_holdout):
        outcome = self._wrapper(make_holdout())
        self._assert_clears(outcome)
        direct_outcome = self._direct(make_holdout())
        self.assertFalse(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 0)
        dataset_outcome = self._dataset(make_holdout())
        self.assertFalse(dataset_outcome["fired"])

    def test_kv_gen_deleg_list_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_list_pairs_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "pairs": {
                    "k": ListSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_list_holdout_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "holdout_items": {
                    "k": ListSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_tuple_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": TupleSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_set_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": SetSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_deque_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": DequeSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_userlist_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": UserListSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_gen_deleg_sequence_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": SequenceSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            }
        )

    def test_kv_iterator_deleg_list_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass([iter([_keys_view()])])
                }
            }
        )

    def test_kv_single_pass_deleg_list_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [SinglePassIterable([_keys_view()])]
                    )
                }
            }
        )

    def test_kv_zip_deleg_list_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass([zip([_keys_view()])])
                }
            }
        )

    def test_kv_map_deleg_list_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [map(lambda x: x, [_keys_view()])]
                    )
                }
            }
        )

    def test_items_view_gen_deleg_list_items_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [_generator_of(_items_view())]
                    )
                }
            }
        )

    def test_kv_in_list_in_gen_deleg_list_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [_generator_of([_keys_view()])]
                    )
                }
            }
        )

    def test_kv_gen_deleg_list_nested_mapping_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": {
                        "j": ListSubclass(
                            [_generator_of(_keys_view())]
                        )
                    }
                }
            }
        )

    def test_kv_gen_deleg_list_candidate_clears(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": {
                "items": {
                    "k": ListSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            },
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertFalse(outcome["fired"])
        self.assertTrue(outcome["bundle_proceeds"])

    def test_clean_kv_gen_deleg_list_clears(self):
        self._assert_three_surface_clears(
            lambda: {
                "items": {
                    "k": ListSubclass(
                        [
                            _generator_of(
                                _keys_view(
                                    "unrelated wording entirely"
                                )
                            )
                        ]
                    )
                }
            }
        )

    def test_clean_text_against_carrier_clears(self):
        outcome = self._wrapper(
            {
                "items": {
                    "k": ListSubclass(
                        [_generator_of(_keys_view())]
                    )
                }
            },
            items=[{"instruction_text": CLEAN_TEXT}],
        )
        self._assert_clears(outcome)

    def test_exact_list_mapping_value_still_fires(self):
        make = lambda: {"items": {"k": [_keys_view()]}}
        outcome = self._wrapper(make())
        self._assert_fires(outcome)
        self.assertEqual(
            outcome["cross_split_audit_result"]["comparisons"], 1
        )
        direct_outcome = self._direct(make())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_exact_list_gen_kv_carried_form_stands(self):
        make = lambda: {
            "items": {"k": [_generator_of(_keys_view())]}
        }
        outcome = self._wrapper(make())
        self._assert_fires(outcome)
        direct_outcome = self._direct(make())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)
        dataset_outcome = self._dataset(make())
        self.assertTrue(dataset_outcome["fired"])

    def test_deleg_list_gen_alone_at_items_fires(self):
        make = lambda: {
            "items": ListSubclass([_generator_of(_keys_view())])
        }
        outcome = self._wrapper(make())
        self._assert_fires(outcome)
        direct_outcome = self._direct(make())
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_ruling_1105_charged_form_still_clears(self):
        self._assert_three_surface_clears(
            lambda: {"items": {"k": ListSubclass([_keys_view()])}}
        )


class TestPromoteFixR26NestedMappingInItemMapping(_WrapperCase):
    """Ruling 1197, S15-R26-PRO-1: a nested mapping
    inside a delegating concrete container subclass
    inside a mapping standing as a ChainMap item."""

    def test_nested_deleg_list_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_nested_position()])}
        )

    def test_nested_deleg_tuple_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": TupleSubclass([_nested_position()])}
        )

    def test_nested_deleg_set_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SetSubclass([_nested_position()])}
        )

    def test_nested_deleg_deque_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": DequeSubclass([_nested_position()])}
        )

    def test_nested_deleg_userlist_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": UserListSubclass([_nested_position()])}
        )

    def test_item_map_in_list_as_item_fires(self):
        outcome = self._wrapper(
            _chainmap_item(
                [{"k": ListSubclass([_nested_position()])}]
            )
        )
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            _chainmap_item(
                [{"k": ListSubclass([_nested_position()])}]
            )
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_deleg_list_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": {"j": ListSubclass([_nested_position()])}
            }
        )

    def test_items_view_gen_deleg_list_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass([_items_view_of_generator()])
            }
        )

    def test_values_view_gen_deleg_set_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SetSubclass([_values_view_of_generator()])
            }
        )

    def test_gen_nested_deleg_list_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": ListSubclass(
                    [_generator_of(_nested_position())]
                )
            }
        )

    def test_nested_at_candidate_construction_fires(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": ListSubclass([_nested_position()])}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_nested_after_partial_scoring_fires(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": ListSubclass([_nested_position()])}
            ),
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_nested_through_two_item_test_fires(self):
        outcome = self._wrapper(
            _chainmap_item(
                {"k": ListSubclass([_nested_position()])}
            ),
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_nested_deleg_sequence_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SequenceSubclass([_nested_position()])}
        )

    def test_nested_deleg_abstract_set_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": AbstractSetSubclass([_nested_position()])
            }
        )

    def test_nested_plain_list_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_nested_position()]}
        )

    def test_clean_nested_deleg_list_in_item_map_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([_clean_position()])},
            1
        )

    def test_string_deleg_list_in_item_map_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([HOLDOUT_TEXT])},
            0
        )

    def test_bytes_deleg_list_in_item_map_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {"k": ListSubclass([HOLDOUT_TEXT.encode()])},
            0
        )

    def test_getitem_nested_deleg_list_in_item_map_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": ListSubclass(
                    [GetitemOnlyForm([_nested_position()])]
                )
            },
            0
        )


class TestPromoteFixR26KeysViewInItemMapping(_WrapperCase):
    """Ruling 1198, S15-R26-PRO-2: a keys view carrying
    a single pass form or byte text, inside a mapping
    standing as an item of a delegating ChainMap
    subclass."""

    def test_kv_gen_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _keys_view_of_generator()}
        )

    def test_kv_gen_one_mapping_deeper_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": {"j": _keys_view_of_generator()}}
        )

    def test_kv_bytes_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _keys_view_of_bytes()}
        )

    def test_kv_gen_in_list_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": [_keys_view_of_generator()]}
        )

    def test_kv_gen_in_tuple_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": (_keys_view_of_generator(),)}
        )

    def test_kv_gen_in_deleg_list_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": ListSubclass([_keys_view_of_generator()])}
        )

    def test_kv_gen_in_deleg_set_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": SetSubclass([_keys_view_of_generator()])}
        )

    def test_kv_gen_in_generator_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": _generator_of(_keys_view_of_generator())
            }
        )

    def test_kv_gen_in_single_pass_in_item_map_fires(self):
        self._assert_chainmap_pair_fires(
            lambda: {
                "k": SinglePassIterable(
                    [_keys_view_of_generator()]
                )
            }
        )

    def test_kv_gen_in_map_in_list_as_item_fires(self):
        outcome = self._wrapper(
            _chainmap_item([{"k": _keys_view_of_generator()}])
        )
        self._assert_fires(outcome)
        direct_outcome = self._direct(
            _chainmap_item([{"k": _keys_view_of_generator()}])
        )
        self.assertTrue(direct_outcome["fired"])
        self.assertEqual(direct_outcome["comparisons"], 1)

    def test_kv_gen_at_candidate_construction_fires(self):
        module = require("ontoloop.promote")
        bundle = {
            "instruction_items": [
                {"instruction_text": HOLDOUT_TEXT}
            ],
            "holdout_items": _chainmap_item(
                {"k": _keys_view_of_generator()}
            ),
        }
        outcome = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(outcome["fired"])
        self.assertFalse(outcome["bundle_proceeds"])

    def test_kv_gen_after_partial_scoring_fires(self):
        outcome = self._wrapper(
            _chainmap_item({"k": _keys_view_of_generator()}),
            after_partial_scoring=True,
        )
        self._assert_fires(outcome)

    def test_kv_gen_through_two_item_test_fires(self):
        outcome = self._wrapper(
            _chainmap_item({"k": _keys_view_of_generator()}),
            items=[
                {"instruction_text": CLEAN_TEXT},
                {"instruction_text": HOLDOUT_TEXT},
            ],
        )
        self._assert_fires(outcome)
        self.assertEqual(outcome["items_tested"], 2)

    def test_items_view_gen_in_item_map_stays_firing(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _items_view_of_generator()}
        )

    def test_values_view_gen_in_item_map_stays_firing(self):
        self._assert_chainmap_pair_fires(
            lambda: {"k": _values_view_of_generator()}
        )

    def test_kv_gen_as_item_directly_stays_clearing(self):
        self._assert_chainmap_pair_clears(
            lambda: _keys_view_of_generator(),
            0
        )

    def test_clean_kv_gen_in_item_map_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: {
                "k": {
                    _generator_of(_clean_position()): 1
                }.keys()
            },
            1
        )


class TestPromoteFixR26StandingControls(_WrapperCase):
    """Standing poles: the charged forms of rulings
    1106 and 1107 still decide as charged."""

    def test_ruling_1106_kv_gen_in_list_as_item_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [_keys_view_of_generator()],
            0
        )

    def test_ruling_1107_bytes_in_list_as_item_clears(self):
        self._assert_chainmap_pair_clears(
            lambda: [HOLDOUT_TEXT.encode()],
            0
        )


if __name__ == "__main__":
    unittest.main()
