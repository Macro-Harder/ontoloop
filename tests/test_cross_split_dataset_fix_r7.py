"""Fix round 7 tests for Region 4: cross split call points,
the shared module, and dataset surfaces.

Charges pinned here, from design/steps/step-15-r7-triage.md:
ruling 151 (the family 1 merged defect at R7-CS-5, Low),
a memoryview standing read as the byte content it views
on both sides of the instruction item test at both call
points, counting R7-CS-5, R7-SPAN-2, Lead Engineer lines
E-6 and E-7, and the memoryview limbs of R7-DAT-1 and
R7-DAT-2; ruling 159 (R7-CS-1, Low), an iterator in any
position the shared act re-reads per instruction item
standing materialised once for the whole test, at both
call points; ruling 160 (R7-CS-2, Low), holdout collection
forms beyond the cured set either standing unpacked and
compared or returning the governed refusal, at both call
points; ruling 161 (R7-CS-3, Low), a holdout item in a
container form inside the collection either standing read
or returning the governed refusal, at both call points;
ruling 162 (R7-CS-4, Low), an item or a mapping of items
in a non dict mapping form standing read for its text or
returning the governed refusal, at both call points;
ruling 163 (R7-SPAN-1, Low), holdout byte content nested
inside a mapping of items standing read for the text it
carries or returning the governed refusal, at both call
points; and ruling 164 (Lead Engineer line E-5, Low), a
pair element in a form the partitioning act does not read
either standing read or returning the governed refusal of
the bundle audit surfaces.
"""

import array
import collections
import types
import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"
DISTINCT_TEXT = "alpha bravo charlie delta echo"

CALL_POINTS = (
    ("ontoloop.dataset", "candidate construction"),
    ("ontoloop.promote", "promotion"),
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
            testcase.assertNotEqual(
                result.get("test_result_carried_on_promotion_record"),
                True,
            )
    return result


class MemoryviewInstructionAndHoldoutTests(unittest.TestCase):
    """Ruling 151: a memoryview stands read as the byte
    content it views on both sides of the test, at both
    call points, beside the standing byte forms."""

    def view(self, text=HOLDOUT_TEXT):
        return memoryview(text.encode("utf-8"))

    def test_instruction_text_as_memoryview_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{"instruction_text": self.view()}],
        ))

    def test_item_itself_as_memoryview_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}], items=[self.view()],
        ))

    def test_instruction_text_as_list_holding_memoryview_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{"instruction_text": [self.view()]}],
        ))

    def test_holdout_material_as_memoryview_fires(self):
        check_fires(self, lambda: bundle_with(self.view()))

    def test_holdout_list_holding_memoryview_fires(self):
        check_fires(self, lambda: bundle_with([self.view()]))

    def test_direct_act_memoryview_forms_fire(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_instruction_item(
            {"instruction_text": self.view()}, [{"text": HOLDOUT_TEXT}]
        )
        self.assertTrue(result["fired"])
        result = module.audit_instruction_item(
            HOLDOUT_TEXT, self.view()
        )
        self.assertTrue(result["fired"])

    def test_byte_forms_still_fire_and_clean_still_clears(self):
        check_fires(self, lambda: bundle_with(
            bytearray(HOLDOUT_TEXT, "utf-8"),
            items=[{"instruction_text": HOLDOUT_TEXT.encode("utf-8")}],
        ))
        check_fires(self, lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{"instruction_text": (v for v in [HOLDOUT_TEXT])}],
        ))
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, bundle_with(
                    [self.view()],
                    items=[{"instruction_text": CLEAN_TEXT}],
                ))
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)


class NestedIteratorMaterialisationTests(unittest.TestCase):
    """Ruling 159: an iterator inside a mapping of items
    value stands materialised once for the whole test, so
    the second instruction item still fires, at both call
    points."""

    ITEMS = [
        {"instruction_text": CLEAN_TEXT},
        {"instruction_text": HOLDOUT_TEXT},
    ]

    def test_mapping_value_generator_fires_on_second_item(self):
        check = lambda: bundle_with(
            {"first": (v for v in [{"text": HOLDOUT_TEXT}])},
            items=list(self.ITEMS),
        )
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, check())
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)

    def test_mapping_value_list_iterator_fires_on_second_item(self):
        check = lambda: bundle_with(
            {"first": iter([{"text": HOLDOUT_TEXT}])},
            items=list(self.ITEMS),
        )
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, check())
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 2)

    def test_list_value_iterator_fires_on_second_item(self):
        check = lambda: bundle_with(
            {"first": iter([{"text": HOLDOUT_TEXT}])},
            items=list(self.ITEMS),
        )
        result = check()
        self.assertTrue(result["instruction_items"])


class HoldoutCollectionBeyondCuredTests(unittest.TestCase):
    """Ruling 160: collection forms beyond the cured set
    carrying the holdout text fire at both call points."""

    def test_dict_items_view_pair_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": {"text": HOLDOUT_TEXT}}.items()
        ))

    def test_zip_object_pair_fires(self):
        check_fires(self, lambda: bundle_with(
            zip(["first"], [{"text": HOLDOUT_TEXT}])
        ))

    def test_mapping_value_as_bytes_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": HOLDOUT_TEXT.encode("utf-8")}
        ))

    def test_array_holdout_fires(self):
        check_fires(self, lambda: bundle_with(
            array.array("b", HOLDOUT_TEXT.encode("utf-8"))
        ))

    def test_cured_collection_forms_still_fire(self):
        check_fires(self, lambda: bundle_with(
            collections.deque([HOLDOUT_TEXT])
        ))
        check_fires(self, lambda: bundle_with(
            {"first": HOLDOUT_TEXT}.values()
        ))


class HoldoutItemContainerTests(unittest.TestCase):
    """Ruling 161: a holdout item in a container form inside
    the collection stands read for the text it carries, at
    both call points."""

    def test_list_element_holding_text_fires(self):
        check_fires(self, lambda: bundle_with([[HOLDOUT_TEXT]]))

    def test_tuple_element_holding_text_fires(self):
        check_fires(self, lambda: bundle_with([(HOLDOUT_TEXT,)]))

    def test_generator_element_holding_text_fires(self):
        check_fires(self, lambda: bundle_with(
            [(v for v in [HOLDOUT_TEXT])]
        ))

    def test_top_generator_yielding_generator_fires(self):
        check_fires(self, lambda: bundle_with(
            (v for v in [(w for w in [HOLDOUT_TEXT])])
        ))

    def test_standing_item_forms_still_fire(self):
        check_fires(self, lambda: bundle_with([{"text": HOLDOUT_TEXT}]))
        check_fires(self, lambda: bundle_with([HOLDOUT_TEXT]))


class NonDictMappingFormTests(unittest.TestCase):
    """Ruling 162: an item or a mapping of items in a non
    dict mapping form stands read for its text, at both
    call points, on a text sharing no word with any key
    name."""

    ITEMS = [{"instruction_text": DISTINCT_TEXT}]

    def proxy(self):
        return types.MappingProxyType({"text": DISTINCT_TEXT})

    def test_instruction_item_as_mappingproxy_fires(self):
        check_fires(self, lambda: {
            "instruction_items": [self.proxy()],
            "holdout_items": [{"text": DISTINCT_TEXT}],
        })

    def test_instruction_item_as_userdict_fires(self):
        check_fires(self, lambda: {
            "instruction_items": [
                collections.UserDict({"text": DISTINCT_TEXT})
            ],
            "holdout_items": [{"text": DISTINCT_TEXT}],
        })

    def test_instruction_text_value_as_mappingproxy_fires(self):
        check_fires(self, lambda: {
            "instruction_items": [{"instruction_text": self.proxy()}],
            "holdout_items": [{"text": DISTINCT_TEXT}],
        })

    def test_holdout_item_as_mappingproxy_fires(self):
        check_fires(self, lambda: {
            "instruction_items": list(self.ITEMS),
            "holdout_items": [self.proxy()],
        })

    def test_holdout_item_as_userdict_fires(self):
        check_fires(self, lambda: {
            "instruction_items": list(self.ITEMS),
            "holdout_items": [
                collections.UserDict({"text": DISTINCT_TEXT})
            ],
        })

    def test_holdout_material_as_mappingproxy_of_items_fires(self):
        check_fires(self, lambda: {
            "instruction_items": list(self.ITEMS),
            "holdout_items": types.MappingProxyType(
                {"first": {"text": DISTINCT_TEXT}}
            ),
        })

    def test_instruction_text_as_array_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{
                "instruction_text": array.array(
                    "b", HOLDOUT_TEXT.encode("utf-8"))
            }],
        ))

    def test_dict_forms_and_ordered_dict_control_still_fire(self):
        check_fires(self, lambda: {
            "instruction_items": [
                collections.OrderedDict({"text": DISTINCT_TEXT})
            ],
            "holdout_items": [{"text": DISTINCT_TEXT}],
        })
        check_fires(self, lambda: bundle_with([{"text": HOLDOUT_TEXT}]))


class NestedByteContentInMappingTests(unittest.TestCase):
    """Ruling 163: holdout byte content nested inside a
    mapping of items stands read for the text it carries,
    at both call points."""

    def test_mapping_value_as_bytearray_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": bytearray(HOLDOUT_TEXT, "utf-8")}
        ))

    def test_mapping_value_as_list_holding_bytes_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": [HOLDOUT_TEXT.encode("utf-8")]}
        ))

    def test_mapping_value_as_tuple_holding_bytes_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": (HOLDOUT_TEXT.encode("utf-8"),)}
        ))

    def test_mapping_value_as_set_holding_bytes_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": {HOLDOUT_TEXT.encode("utf-8")}}
        ))

    def test_mapping_value_as_deque_holding_bytes_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": collections.deque(
                [HOLDOUT_TEXT.encode("utf-8")])}
        ))

    def test_mapping_value_as_generator_holding_bytes_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": (v for v in [HOLDOUT_TEXT.encode("utf-8")])}
        ))

    def test_mapping_holding_bytes_beside_integer_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": HOLDOUT_TEXT.encode("utf-8"), "other": 42}
        ))

    def test_mapping_holding_bytes_beside_clean_string_fires(self):
        check_fires(self, lambda: bundle_with(
            {
                "first": "clean wording only",
                "second": HOLDOUT_TEXT.encode("utf-8"),
            }
        ))

    def test_unread_element_does_not_drop_collection_fires(self):
        check_fires(self, lambda: bundle_with(
            {
                "first": [
                    {"text": HOLDOUT_TEXT},
                    HOLDOUT_TEXT.encode("utf-8"),
                ]
            }
        ))


class PairElementMappingTests(unittest.TestCase):
    """Ruling 164: a pair element standing as a mapping
    inside the pairs list either stands read for the
    candidate and holdout items it carries or returns the
    governed refusal, beside the list form control and
    the cured position forms of ruling 88."""

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

    def test_pair_as_mapping_refuses_on_shared_material(self):
        module = harness.require("ontoloop.cross_split_audit")
        for surface in ("audit_at_promotion", "audit_at_build",
                        "audit_at_evaluation"):
            with self.subTest(surface=surface):
                result = getattr(module, surface)(
                    {"pairs": [{
                        "candidate": self.CANDIDATE,
                        "holdout": self.HOLDOUT,
                    }]}
                )
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertFalse(result["promotion_proceeded"])
                self.assertEqual(result["comparisons"], 1)

    def test_pair_as_list_control_refuses_on_shared_material(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion(
            {"pairs": [[self.CANDIDATE, self.HOLDOUT]]}
        )
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertEqual(result["comparisons"], 1)

    def test_cured_position_forms_still_refuse(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion(
            {"pairs": {"pair": [self.CANDIDATE, self.HOLDOUT]}}
        )
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertEqual(result["comparisons"], 0)


if __name__ == "__main__":
    unittest.main()
