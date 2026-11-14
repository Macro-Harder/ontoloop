"""Fix round 6 tests for Region 4: cross split call points,
the shared module, and dataset surfaces.

Charges pinned here, from design/steps/step-15-r6-triage.md:
ruling 85 (R6-CS-1, Medium), an iterator holdout stands
materialised once for the whole test at both call points;
ruling 88 (line D-6, Medium), material in the items or pairs
position of a shared module bundle in a form the partitioning
act does not read returns the governed refusal; ruling 98
(the C-F merged defect, Low), the shared recursive text reading
meets a deeply nested or cyclic text form in the governed
refusal at every call point it serves; ruling 101 (R6-CS-2,
Low), holdout collection forms beyond the cured set either
stand unpacked and compared or return the governed refusal,
at both call points; ruling 102 (R6-CS-3, Low), the instruction
text value standing as bytes or as a generator either stands
read for its text or returns the governed refusal, at both
call points; ruling 115 (R6-SPAN-1, Low), a non mapping bundle
returns the governed refusal at the promotion call point;
ruling 96 (R6-DAT-1, Low), an unhashable figure name inside a
name collection returns the defect list; and ruling 97
(R6-DAT-2, Low), dataset.meaning_check meets an unhashable
check identifier in one governed form in both directions.
"""

import collections
import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"

CALL_POINTS = (
    ("ontoloop.dataset", "candidate construction"),
    ("ontoloop.promote", "promotion"),
)


def bundle_with(holdout, items=None):
    if items is None:
        items = [{"instruction_text": HOLDOUT_TEXT}]
    return {"instruction_items": items, "holdout_items": holdout}


def expected_refusal(occasion):
    result = {
        "fired": True,
        "refusal_form": "cross split audit refusal",
        "field_scope": "instruction text field",
        "wider_material_compared": False,
    }
    if occasion == "promotion":
        result["promotion_proceeds"] = False
    else:
        result["bundle_proceeds"] = False
    return result


def call(testcase, module_name, occasion, bundle):
    module = harness.require(module_name)
    return module.test_instruction_items_against_holdout(
        bundle, occasion=occasion
    )


class IteratorHoldoutMultiItemTests(unittest.TestCase):
    """Ruling 85: a two item bundle whose second item carries
    the holdout text fires at both call points where the
    holdout stands as an iterator form, beside the single
    item charged forms and the clean two item bundle."""

    ITEMS = [
        {"instruction_text": CLEAN_TEXT},
        {"instruction_text": HOLDOUT_TEXT},
    ]

    def check_form(self, make_holdout):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(make_holdout(), items=list(self.ITEMS)),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)
                self.assertEqual(result["fired_item"], HOLDOUT_TEXT)
                self.assertNotEqual(
                    result.get("test_result_carried_on_promotion_record"),
                    True,
                )

    def test_generator_of_text_fires_on_the_second_item(self):
        self.check_form(lambda: (value for value in [HOLDOUT_TEXT]))

    def test_generator_of_one_mapping_fires_on_the_second_item(self):
        self.check_form(
            lambda: (value for value in [{"text": HOLDOUT_TEXT}])
        )

    def test_list_iterator_fires_on_the_second_item(self):
        self.check_form(lambda: iter([{"text": HOLDOUT_TEXT}]))

    def test_map_object_fires_on_the_second_item(self):
        self.check_form(
            lambda: map(lambda value: value, [{"text": HOLDOUT_TEXT}])
        )

    def test_single_item_iterator_forms_still_fire(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(
                        (value for value in [HOLDOUT_TEXT])
                    ),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 1)

    def test_clean_two_item_bundle_still_clears(self):
        items = [
            {"instruction_text": CLEAN_TEXT},
            {"instruction_text": "further clean guidance text"},
        ]
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(
                        (value for value in [HOLDOUT_TEXT]),
                        items=items,
                    ),
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 2)


class ItemsPairsPositionTests(unittest.TestCase):
    """Ruling 88: a bundle presenting its items as a mapping
    or as a bare string, or its pairs as a mapping, returns
    the governed refusal of the shared module bundle
    surfaces, beside the list form controls."""

    CANDIDATE = {
        "group": "g1",
        "signature": "s1",
        "text": "shared bundle text alpha",
    }
    HOLDOUT = {
        "group": "g1",
        "signature": "s9",
        "text": "shared bundle text alpha",
    }

    def check_refused(self, material):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion(material)
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertFalse(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 0)
        return result

    def items_list_form(self):
        candidate = dict(self.CANDIDATE)
        holdout = dict(self.HOLDOUT)
        holdout["split"] = "holdout"
        return [candidate, holdout]

    def test_items_as_mapping_refuses(self):
        items = self.items_list_form()
        self.check_refused({"items": {"a": items[0], "b": items[1]}})

    def test_items_as_bare_string_refuses(self):
        self.check_refused({"items": "shared bundle text alpha"})

    def test_pairs_as_mapping_refuses(self):
        self.check_refused(
            {"pairs": {"pair": [self.CANDIDATE, self.HOLDOUT]}}
        )

    def test_items_list_form_control_refuses_on_the_shared_pair(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion(
            {"items": self.items_list_form()}
        )
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertEqual(result["comparisons"], 1)

    def test_pairs_list_form_control_refuses_on_the_shared_pair(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion(
            {"pairs": [[self.CANDIDATE, self.HOLDOUT]]}
        )
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertEqual(result["comparisons"], 1)

    def test_cured_side_position_forms_still_refuse(self):
        self.check_refused(
            {
                "candidate_items": [self.CANDIDATE],
                "holdout_items": self.HOLDOUT,
            }
        )


class RecursiveTextRefusalTests(unittest.TestCase):
    """Ruling 98: a text form nested past the interpreter
    limit and a cyclic text form return the governed refusal
    of the surface at both call points, with no exception,
    beside the standing nested forms still firing."""

    def deep_item(self):
        value = HOLDOUT_TEXT
        for _ in range(1500):
            value = [value]
        return {"instruction_text": value}

    def cyclic_item(self):
        value = [HOLDOUT_TEXT]
        value.append(value)
        return {"instruction_text": value}

    def check_refusal(self, make_item):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(
                        [{"text": HOLDOUT_TEXT}], items=[make_item()]
                    ),
                )
                self.assertEqual(result, expected_refusal(occasion))
                self.assertNotIn("items_tested", result)

    def test_deeply_nested_text_returns_the_refusal(self):
        self.check_refusal(self.deep_item)

    def test_cyclic_text_returns_the_refusal(self):
        self.check_refusal(self.cyclic_item)

    def test_direct_act_returns_the_refusal_form(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_instruction_item(
            self.deep_item(), [{"text": HOLDOUT_TEXT}]
        )
        self.assertTrue(result["fired"])
        self.assertEqual(
            result["refusal_form"], "cross split audit refusal"
        )

    def test_standing_nested_text_forms_still_fire(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(
                        [{"text": HOLDOUT_TEXT}],
                        items=[{"instruction_text": [[HOLDOUT_TEXT]]}],
                    ),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 1)


class PlainIterable:
    """An iterable that stands as no iterator and as none of
    the cured container forms."""

    def __iter__(self):
        yield HOLDOUT_TEXT


class HoldoutCollectionBeyondCuredTests(unittest.TestCase):
    """Ruling 101: holdout collection forms beyond the cured
    set carrying the holdout text fire at both call points,
    beside the cured forms still firing and the clean bundle
    still clearing."""

    def check_form(self, make_holdout):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(make_holdout()),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 1)
                self.assertEqual(result["fired_item"], HOLDOUT_TEXT)

    def test_bytes_holdout_fires(self):
        self.check_form(lambda: HOLDOUT_TEXT.encode("utf-8"))

    def test_bytearray_holdout_fires(self):
        self.check_form(lambda: bytearray(HOLDOUT_TEXT, "utf-8"))

    def test_deque_holdout_fires(self):
        self.check_form(lambda: collections.deque([HOLDOUT_TEXT]))

    def test_dict_keys_view_holdout_fires(self):
        self.check_form(lambda: {HOLDOUT_TEXT: 1}.keys())

    def test_dict_values_view_holdout_fires(self):
        self.check_form(lambda: {"first": HOLDOUT_TEXT}.values())

    def test_plain_iterable_instance_holdout_fires(self):
        self.check_form(lambda: PlainIterable())

    def test_mapping_value_as_list_of_items_fires(self):
        self.check_form(lambda: {"first": [{"text": HOLDOUT_TEXT}]})

    def test_mapping_value_as_tuple_of_items_fires(self):
        self.check_form(lambda: {"first": ({"text": HOLDOUT_TEXT},)})

    def test_mapping_with_an_integer_value_beside_an_item_fires(self):
        self.check_form(
            lambda: {"first": {"text": HOLDOUT_TEXT}, "other": 42}
        )

    def test_cured_collection_forms_still_fire(self):
        forms = (
            lambda: {HOLDOUT_TEXT},
            lambda: [{"text": HOLDOUT_TEXT}],
            lambda: {"first": {"text": HOLDOUT_TEXT}},
        )
        for make_holdout in forms:
            self.check_form(make_holdout)

    def test_clean_bundle_still_clears(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(
                        HOLDOUT_TEXT.encode("utf-8"),
                        items=[{"instruction_text": CLEAN_TEXT}],
                    ),
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)


class InstructionTextBytesGeneratorTests(unittest.TestCase):
    """Ruling 102: the instruction text position carrying the
    holdout text as bytes or as a generator fires at both
    call points, beside the standing item forms."""

    def check_item(self, make_item):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(
                    self, module_name, occasion,
                    bundle_with(
                        [{"text": HOLDOUT_TEXT}], items=[make_item()]
                    ),
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 1)
                self.assertEqual(result["fired_item"], HOLDOUT_TEXT)

    def test_instruction_text_as_bytes_fires(self):
        self.check_item(
            lambda: {"instruction_text": HOLDOUT_TEXT.encode("utf-8")}
        )

    def test_item_itself_as_bytes_fires(self):
        self.check_item(lambda: HOLDOUT_TEXT.encode("utf-8"))

    def test_instruction_text_as_generator_fires(self):
        self.check_item(
            lambda: {
                "instruction_text": (
                    value for value in [HOLDOUT_TEXT]
                )
            }
        )

    def test_standing_item_forms_still_fire(self):
        self.check_item(lambda: {"instruction_text": HOLDOUT_TEXT})
        self.check_item(lambda: HOLDOUT_TEXT)


class PromotionNonMappingBundleTests(unittest.TestCase):
    """Ruling 115: a non mapping bundle returns the governed
    refusal at the promotion call point, with no exception,
    beside the standing mapping bundle forms."""

    def check_bundle_form(self, bundle):
        module = harness.require("ontoloop.promote")
        result = module.test_instruction_items_against_holdout(
            bundle, occasion="promotion"
        )
        self.assertEqual(result, expected_refusal("promotion"))
        self.assertNotIn("items_tested", result)

    def test_none_bundle_returns_the_refusal(self):
        self.check_bundle_form(None)

    def test_string_bundle_returns_the_refusal(self):
        self.check_bundle_form("a bundle in string form")

    def test_list_bundle_returns_the_refusal(self):
        self.check_bundle_form([{"instruction_text": HOLDOUT_TEXT}])

    def test_tuple_bundle_returns_the_refusal(self):
        self.check_bundle_form(({"instruction_text": HOLDOUT_TEXT},))

    def test_integer_bundle_returns_the_refusal(self):
        self.check_bundle_form(42)

    def test_set_bundle_returns_the_refusal(self):
        self.check_bundle_form({"a bundle in set form"})

    def test_byte_string_bundle_returns_the_refusal(self):
        self.check_bundle_form(b"a bundle in byte form")

    def test_mapping_bundle_forms_still_decide_as_pinned(self):
        module = harness.require("ontoloop.promote")
        result = module.test_instruction_items_against_holdout(
            bundle_with([{"text": HOLDOUT_TEXT}]), occasion="promotion"
        )
        self.assertTrue(result["fired"])
        self.assertEqual(result["items_tested"], 1)


class UnhashableFigureNameTests(unittest.TestCase):
    """Ruling 96: an unhashable figure name inside a name
    collection returns the defect list of the surface, beside
    the standing figures forms."""

    def record_with_figures(self, figures):
        module = harness.require("ontoloop.dataset")
        record = module.dataset_record_example_b()
        record["intake_account"]["figures"] = figures
        return module, record

    def test_unhashable_names_return_the_defect_list(self):
        forms = (
            [["runs seen"]],
            [{"name": "runs seen"}],
            [{"runs seen"}],
            ["runs seen", ["runs with outcomes"]],
        )
        for figures in forms:
            with self.subTest(form=type(figures[0]).__name__):
                module, record = self.record_with_figures(figures)
                self.assertEqual(
                    module.check_dataset_record(record),
                    [{"artifact": "Dataset record"}],
                )

    def test_standing_figures_forms_still_return_no_defect(self):
        module = harness.require("ontoloop.dataset")
        record = module.dataset_record_example_b()
        names = sorted(record["intake_account"]["figures"])
        _module, fresh = self.record_with_figures(list(names))
        self.assertEqual(module.check_dataset_record(fresh), [])
        _module, fresh = self.record_with_figures(set(names))
        self.assertEqual(module.check_dataset_record(fresh), [])


class MeaningCheckUnhashableTests(unittest.TestCase):
    """Ruling 97: dataset.meaning_check meets an unhashable
    check identifier in one governed form in both directions,
    beside the standing identifier forms."""

    def test_unhashable_identifier_returns_one_form_both_ways(self):
        module = harness.require("ontoloop.dataset")
        for check_id in (["SPAN-X"], {"id": 1}, {"SPAN-X"}):
            with self.subTest(form=type(check_id).__name__):
                held = module.meaning_check(
                    check_id=check_id,
                    affected_class="a class",
                    fixture=None,
                    direction="meaning held",
                )
                changed = module.meaning_check(
                    check_id=check_id,
                    affected_class="a class",
                    fixture=None,
                    direction="meaning changed",
                )
                self.assertEqual(changed, held)
                self.assertEqual(
                    held["meaning_change_record_entry"]["classification"],
                    "no meaning change shown",
                )

    def test_standing_identifier_forms_still_decide_as_pinned(self):
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


if __name__ == "__main__":
    unittest.main()
