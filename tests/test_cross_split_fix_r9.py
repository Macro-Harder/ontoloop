"""Fix round 9 tests for Region 3: cross split and dataset.

Charges pinned here, from design/steps/step-15-r9-triage.md:
ruling 261 (the hash guard merged defect at the R9-DAT-2
identity, Low), dataset.meaning_check meeting a check
identifier whose hashing raises ValueError in the held form
in the changed direction; ruling 262 (the hash guard merged
defect at the R9-DAT-3 identity, Low), the figure name
membership guard in dataset.check_dataset_record meeting a
name whose hashing raises ValueError in the one entry defect
form; ruling 266 (the materialisation merged defect, Low),
_materialise_iterators rebuilding a value standing in any
re-iterable container form the test presents, at both call
points; ruling 267 (R9-CS-2, Low), an iterator nested past
the standing depth cutoff standing materialised once, the
depth cutoff limb standing removed; ruling 268 (R9-CS-1,
Low), a UserString standing as a value in a mapping of items
standing collected as the one text it wraps, at both call
points and at the direct act; ruling 269 (the sliced view
merged defect, Low), a memoryview over an array in typecode
u standing read as the character content the view itself
presents, its single home in cross_split_audit.py; ruling
270 (R9-CS-5, Low), a bundle item wrapped in a container form
inside the bundle positions standing read for the item it
carries, split side included, at every bundle call point;
ruling 273 (the bundle gate merged defect, Low), each
instruction item call point reading the bundle by the
abstract mapping form at its bundle gate; and ruling 274
(Lead Engineer line E-7, Low), the bundle presentation acts
reading a bundle standing in any mapping form as a bundle,
in presentation form only.
"""

import array
import collections
import collections.abc
import types
import unittest
import weakref

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

SPANNING_REASON = (
    "spanning pair over a tested relation between the "
    "candidate bundle and the sealed holdout"
)
PRESENTATION_REASON = (
    "refused on its presentation as flagged material"
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


def check_fires(testcase, make_bundle):
    for module_name, occasion in CALL_POINTS:
        with testcase.subTest(module=module_name, occasion=occasion):
            result = call(module_name, occasion, make_bundle())
            testcase.assertTrue(result["fired"])


def gen_holdout():
    return (v for v in [{"text": HOLDOUT_TEXT}])


def writable_memoryview():
    return memoryview(bytearray(b"check-x"))


class MeaningCheckValueErrorHashTests(unittest.TestCase):
    """Ruling 261: dataset.meaning_check meets a check
    identifier whose hashing raises ValueError in the same
    held form as the TypeError forms, in both directions."""

    def check_held(self, direction):
        module = harness.require("ontoloop.dataset")
        identifier = writable_memoryview()
        result = module.meaning_check(
            check_id=identifier,
            affected_class="a class",
            fixture=None,
            direction=direction,
        )
        entry = result["meaning_change_record_entry"]
        self.assertEqual(
            entry["classification"], "no meaning change shown"
        )
        self.assertEqual(entry["checks_run"], [identifier])

    def test_writable_memoryview_identifier_changed_direction(self):
        self.check_held("meaning changed")

    def test_held_direction_and_standing_identifiers_still_decide(self):
        self.check_held("meaning held")
        module = harness.require("ontoloop.dataset")
        held = module.meaning_check(
            check_id="SPAN-X",
            affected_class="a class",
            fixture=None,
            direction="meaning held",
        )
        changed = module.meaning_check(
            check_id="SPAN-X",
            affected_class="a class",
            fixture=None,
            direction="meaning changed",
        )
        self.assertEqual(
            held["meaning_change_record_entry"]["classification"],
            "no meaning change shown",
        )
        self.assertEqual(
            changed["meaning_change_record_entry"]["classification"],
            "meaning change under a stable shape",
        )


class FigureNameValueErrorHashTests(unittest.TestCase):
    """Ruling 262: the figure name membership guard in
    dataset.check_dataset_record meets a figure name whose
    hashing raises ValueError in the one entry defect form,
    with no exception."""

    def record_with_figures(self, figures):
        module = harness.require("ontoloop.dataset")
        record = module.dataset_record_example_b()
        record["intake_account"]["figures"] = figures
        return module, record

    def test_writable_memoryview_name_in_figures_list(self):
        module, record = self.record_with_figures(
            [writable_memoryview()]
        )
        self.assertEqual(
            module.check_dataset_record(record),
            [{"artifact": "Dataset record"}],
        )

    def test_writable_memoryview_name_in_figures_tuple(self):
        module, record = self.record_with_figures(
            (writable_memoryview(),)
        )
        self.assertEqual(
            module.check_dataset_record(record),
            [{"artifact": "Dataset record"}],
        )

    def test_valid_example_b_record_still_returns_no_defect(self):
        module = harness.require("ontoloop.dataset")
        record = module.dataset_record_example_b()
        self.assertEqual(module.check_dataset_record(record), [])


class SequenceHoldout(collections.abc.Sequence):
    """A Sequence subclass holding its elements in a list."""

    def __init__(self, elements):
        self._elements = list(elements)

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]


class SetHoldout(collections.abc.Set):
    """A Set subclass holding its elements in a set."""

    def __init__(self, elements):
        self._elements = set(elements)

    def __contains__(self, element):
        return element in self._elements

    def __iter__(self):
        return iter(self._elements)

    def __len__(self):
        return len(self._elements)


class IterableHoldout:
    """A general iterable container holding its elements."""

    def __init__(self, elements):
        self._elements = list(elements)

    def __iter__(self):
        return iter(self._elements)


class MaterialisationContainerTests(unittest.TestCase):
    """Ruling 266: an iterator inside an abstract Sequence,
    an abstract Set, a general iterable container, or a
    WeakSet fires on the second item at both call points."""

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

    def test_sequence_subclass_holding_generator(self):
        self.check_second(lambda: SequenceHoldout([gen_holdout()]))

    def test_list_holding_sequence_subclass_holding_generator(self):
        self.check_second(
            lambda: [SequenceHoldout([gen_holdout()])]
        )

    def test_deque_holding_sequence_subclass_holding_generator(self):
        self.check_second(
            lambda: collections.deque(
                [SequenceHoldout([gen_holdout()])]
            )
        )

    def test_mapping_value_sequence_subclass_holding_generator(self):
        self.check_second(
            lambda: {"first": SequenceHoldout([gen_holdout()])}
        )

    def test_set_subclass_holding_generator(self):
        self.check_second(lambda: SetHoldout([gen_holdout()]))

    def test_mapping_value_set_subclass_holding_generator(self):
        self.check_second(
            lambda: {"first": SetHoldout([gen_holdout()])}
        )

    def test_general_iterable_container_holding_generator(self):
        self.check_second(lambda: IterableHoldout([gen_holdout()]))

    def test_weakset_holding_generator(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                generator = gen_holdout()
                holdout = weakref.WeakSet([generator])
                result = call(
                    module_name,
                    occasion,
                    bundle_with(holdout, items=list(self.ITEMS)),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)

    def test_charged_ruling_211_forms_still_fire(self):
        self.check_second(
            lambda: collections.deque([gen_holdout()])
        )
        self.check_second(
            lambda: collections.UserList([gen_holdout()])
        )
        self.check_second(lambda: {"first": gen_holdout()}.values())

    def test_clean_bundle_still_clears(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    module_name,
                    occasion,
                    bundle_with(
                        SequenceHoldout(
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


class MaterialisationDepthTests(unittest.TestCase):
    """Ruling 267: an iterator nested past the standing depth
    cutoff of 100 fires on the second item at both call
    points, the depth cutoff limb standing removed."""

    ITEMS = [
        {"instruction_text": CLEAN_TEXT},
        {"instruction_text": HOLDOUT_TEXT},
    ]

    def wrapped(self, depth):
        value = gen_holdout()
        for _ in range(depth):
            value = [value]
        return value

    def check_second_at_depth(self, depth):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    module_name,
                    occasion,
                    bundle_with(
                        self.wrapped(depth), items=list(self.ITEMS)
                    ),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)

    def test_generator_wrapped_in_101_lists(self):
        self.check_second_at_depth(101)

    def test_generator_wrapped_in_130_lists(self):
        self.check_second_at_depth(130)

    def test_generator_wrapped_in_100_lists_still_fires(self):
        self.check_second_at_depth(100)


class UserStringMappingValueTests(unittest.TestCase):
    """Ruling 268: a UserString standing as a value in a
    mapping of items stands collected as the one text it
    wraps, at both call points and at the direct act."""

    def test_mapping_with_one_userstring_value_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": collections.UserString(HOLDOUT_TEXT)}
        ))

    def test_mapping_userstring_beside_clean_string_fires(self):
        check_fires(self, lambda: bundle_with({
            "first": CLEAN_TEXT,
            "second": collections.UserString(HOLDOUT_TEXT),
        }))

    def test_mapping_userstring_beside_clean_bytes_fires(self):
        check_fires(self, lambda: bundle_with({
            "first": b"clean bytes carrying no holdout wording",
            "second": collections.UserString(HOLDOUT_TEXT),
        }))

    def test_direct_act_mapping_userstring_value_fires(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_instruction_item(
            HOLDOUT_TEXT,
            {"first": collections.UserString(HOLDOUT_TEXT)},
        )
        self.assertTrue(result["fired"])

    def test_plain_string_mapping_value_still_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": HOLDOUT_TEXT}
        ))


class SlicedTypecodeUViewTests(unittest.TestCase):
    """Ruling 269: a memoryview over an array in typecode u
    stands read as the character content the view itself
    presents, so a sliced view resolves to its slice."""

    def u_array(self, text=HOLDOUT_TEXT):
        return array.array("u", text)

    def head_view(self):
        return memoryview(self.u_array())[:4]

    def tail_view(self):
        return memoryview(self.u_array())[4:]

    def check_clears(self, make_bundle):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, make_bundle())
                self.assertFalse(result["fired"])

    def test_sliced_view_as_holdout_material_clears(self):
        self.check_clears(lambda: bundle_with(self.head_view()))

    def test_sliced_view_as_instruction_text_clears(self):
        self.check_clears(lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{"instruction_text": self.head_view()}],
        ))

    def test_sliced_memoryview_over_bytes_still_clears(self):
        self.check_clears(lambda: bundle_with(
            memoryview(HOLDOUT_TEXT.encode("utf-8"))[:4]
        ))

    def test_sliced_u_array_itself_still_resolves_to_slice(self):
        self.check_clears(lambda: bundle_with(self.u_array()[:4]))

    def test_whole_view_still_fires(self):
        check_fires(self, lambda: bundle_with(
            memoryview(self.u_array())
        ))

    def test_head_word_alone_against_tail_slice_clears(self):
        self.check_clears(lambda: bundle_with(
            self.tail_view(),
            items=[{"instruction_text": "sealed"}],
        ))

    def test_tail_slice_content_fires_on_its_own_text(self):
        check_fires(self, lambda: bundle_with(
            self.tail_view(),
            items=[{"instruction_text": HOLDOUT_TEXT[4:]}],
        ))


class WrappedBundleItemTests(unittest.TestCase):
    """Ruling 270: a bundle item wrapped in a container form
    inside the bundle positions stands read for the item it
    carries, split side included, at every bundle call point."""

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

    def test_holdout_wrapped_in_list_in_items(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE), [dict(self.HOLDOUT)],
        ]})
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons({"items": [
            dict(self.CANDIDATE), [dict(self.HOLDOUT)],
        ]})
        self.assertEqual(result["comparisons"], 1)

    def test_holdout_wrapped_in_tuple_in_items(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE), (dict(self.HOLDOUT),),
        ]})

    def test_holdout_wrapped_in_deque_in_items(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE),
            collections.deque([dict(self.HOLDOUT)]),
        ]})

    def test_holdout_wrapped_in_list_in_bare_list_bundle(self):
        self.check_refuses(lambda: [
            dict(self.CANDIDATE), [dict(self.HOLDOUT)],
        ])

    def test_holdout_wrapped_in_list_in_holdout_items(self):
        self.check_refuses(lambda: {
            "candidate_items": [dict(self.CANDIDATE)],
            "holdout_items": [[dict(self.HOLDOUT)]],
        })

    def test_plain_dict_control_still_refuses(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE), dict(self.HOLDOUT),
        ]})

    def test_pairs_position_control_still_refuses(self):
        self.check_refuses(lambda: {"pairs": [
            (dict(self.CANDIDATE), dict(self.HOLDOUT)),
        ]})


class BundleGateMappingFormTests(unittest.TestCase):
    """Ruling 273: each instruction item call point reads the
    bundle by the abstract mapping form at its bundle gate,
    so a bundle in any mapping form decides in substance."""

    def mapping_forms(self, bundle):
        return (
            collections.UserDict(bundle),
            types.MappingProxyType(bundle),
            collections.ChainMap(bundle),
        )

    def plain_bundle(self, items):
        return {
            "instruction_items": items,
            "holdout_items": [{"text": HOLDOUT_TEXT}],
        }

    def test_clean_bundle_in_mapping_forms_clears(self):
        for form in self.mapping_forms(
            self.plain_bundle([{"instruction_text": CLEAN_TEXT}])
        ):
            for module_name, occasion in CALL_POINTS:
                with self.subTest(
                    form=type(form).__name__,
                    module=module_name,
                    occasion=occasion,
                ):
                    result = call(module_name, occasion, form)
                    self.assertFalse(result["fired"])
                    self.assertEqual(result["items_tested"], 1)

    def test_firing_bundle_in_mapping_forms_fires_in_substance(self):
        for form in self.mapping_forms(
            self.plain_bundle([{"instruction_text": HOLDOUT_TEXT}])
        ):
            for module_name, occasion in CALL_POINTS:
                with self.subTest(
                    form=type(form).__name__,
                    module=module_name,
                    occasion=occasion,
                ):
                    result = call(module_name, occasion, form)
                    self.assertTrue(result["fired"])
                    self.assertEqual(result["items_tested"], 1)

    def test_plain_dict_decides_and_non_mapping_bundle_refused(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    module_name,
                    occasion,
                    self.plain_bundle(
                        [{"instruction_text": CLEAN_TEXT}]
                    ),
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)
                refused = call(
                    module_name,
                    occasion,
                    [{"instruction_text": HOLDOUT_TEXT}],
                )
                self.assertTrue(refused["fired"])
                self.assertEqual(
                    refused["refusal_form"],
                    "cross split audit refusal",
                )
                self.assertNotIn("items_tested", refused)


class BundlePresentationMappingFormTests(unittest.TestCase):
    """Ruling 274: the bundle presentation acts read a bundle
    standing in any mapping form as a bundle, in the same
    mapping form as the partitioning act reads its items.
    Presentation form only: no pair selection stands pinned
    here beyond the pairs the standing acts present."""

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

    def spanning_bundle(self):
        return {"items": [dict(self.CANDIDATE), dict(self.HOLDOUT)]}

    def check_spanning_refusal(self, make_bundle):
        module = harness.require("ontoloop.cross_split_audit")
        for surface in BUNDLE_SURFACES:
            with self.subTest(surface=surface):
                result = getattr(module, surface)(make_bundle())
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertFalse(result["promotion_proceeded"])
                self.assertEqual(result["comparisons"], 1)
                self.assertEqual(result["typed_reason"], SPANNING_REASON)

    def test_userdict_bundle_refused_on_spanning_reason(self):
        self.check_spanning_refusal(
            lambda: collections.UserDict(self.spanning_bundle())
        )

    def test_mappingproxy_bundle_refused_on_spanning_reason(self):
        self.check_spanning_refusal(
            lambda: types.MappingProxyType(self.spanning_bundle())
        )

    def test_indexed_comparisons_counts_mapping_form_bundles(self):
        module = harness.require("ontoloop.cross_split_audit")
        for bundle in (
            collections.UserDict(self.spanning_bundle()),
            types.MappingProxyType(self.spanning_bundle()),
            self.spanning_bundle(),
        ):
            with self.subTest(form=type(bundle).__name__):
                result = module.indexed_comparisons(bundle)
                self.assertEqual(result["comparisons"], 1)

    def test_clean_and_ungoverned_mapping_forms_still_decide(self):
        module = harness.require("ontoloop.cross_split_audit")
        clean = collections.UserDict({"items": [
            {"group": "g1", "signature": "s1",
             "text": "shared bundle text alpha", "split": "candidate"},
            {"group": "g2", "signature": "s9",
             "text": "unrelated wording entirely", "split": "holdout"},
        ]})
        result = module.audit_at_promotion(clean)
        self.assertFalse(result["candidate_bundle_refused"])
        self.assertTrue(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 0)
        ungoverned = collections.UserDict({
            "candidate_items": dict(self.CANDIDATE),
            "holdout_items": [dict(self.HOLDOUT)],
        })
        result = module.audit_at_promotion(ungoverned)
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertEqual(result["comparisons"], 0)
        self.assertEqual(result["typed_reason"], PRESENTATION_REASON)


if __name__ == "__main__":
    unittest.main()
