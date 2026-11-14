"""Fix round 8 tests for Region 3: cross split and dataset.

Charges pinned here, from design/steps/step-15-r8-triage.md:
ruling 211 (the family 1 merged defect, Low), an iterator
inside a deque, a UserList, or a dictionary view standing
materialised once for the whole test at both call points;
ruling 212 (R8-CS-2, further byte typecode limb, Low), an
array holding byte content in a wider typecode standing
read for the text those bytes carry at both call points;
ruling 213 (the family 2 merged defect, Low), an array in
typecode u standing read as the character content it holds
at both call points and at the direct act, its single home
in cross_split_audit.py; ruling 214 (R8-CS-3, Low), the
partitioning act reading the split side of an item standing
in any mapping form at the bundle call points; ruling 215
(R8-CS-4, Low), indexed_comparisons meeting a deeply nested
or cyclic text in a governed form with no exception;
ruling 216 (R8-SPAN-1, Low), the shared text reading reading
a UserString as the text it wraps at both call points and
at the direct act; and ruling 217 (Lead Engineer line E-6,
Low), the bundle index act meeting an unhashable group or
signature value in a governed form at every bundle call
point and at indexed_comparisons, in its exception form
only.
"""

import array
import collections
import types
import unittest

from tests import harness


HOLDOUT_TEXT = "sealed holdout instruction text"
CLEAN_TEXT = "guidance for the candidate that shares no wording"
WIDE_TEXT = "sealed holdout instruction textx"

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


def gen_holdout():
    return (v for v in [{"text": HOLDOUT_TEXT}])


class IteratorInsideWrapperTests(unittest.TestCase):
    """Ruling 211: an iterator inside a deque, a UserList,
    or a dictionary view fires on the second item."""

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

    def test_deque_holding_generator(self):
        self.check_second(lambda: collections.deque([gen_holdout()]))

    def test_mapping_value_deque_holding_generator(self):
        self.check_second(
            lambda: {"first": collections.deque([gen_holdout()])}
        )

    def test_list_holding_deque_holding_generator(self):
        self.check_second(
            lambda: [collections.deque([gen_holdout()])]
        )

    def test_userlist_holding_generator(self):
        self.check_second(lambda: collections.UserList([gen_holdout()]))

    def test_list_holding_userlist_holding_generator(self):
        self.check_second(
            lambda: [collections.UserList([gen_holdout()])]
        )

    def test_mapping_value_userlist_holding_generator(self):
        self.check_second(
            lambda: {"first": collections.UserList([gen_holdout()])}
        )

    def test_dict_values_view_holding_generator(self):
        self.check_second(lambda: {"first": gen_holdout()}.values())

    def test_dict_items_view_holding_generator(self):
        self.check_second(lambda: {"first": gen_holdout()}.items())

    def test_charged_forms_still_fire_and_clean_clears(self):
        check_fires(self, lambda: bundle_with(
            {"first": gen_holdout()}, items=list(self.ITEMS)))
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, bundle_with(
                    collections.deque([{"text": HOLDOUT_TEXT}]),
                    items=[{"instruction_text": CLEAN_TEXT}],
                ))
                self.assertFalse(result["fired"])


class WiderByteTypecodeTests(unittest.TestCase):
    """Ruling 212: an array in a wider typecode holding the
    bytes of the text stands read for that text."""

    def wide(self, typecode, text=WIDE_TEXT):
        value = array.array(typecode)
        value.frombytes(text.encode("utf-8"))
        return value

    def test_instruction_text_signed_short_array_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": WIDE_TEXT}],
            items=[{"instruction_text": self.wide("h")}],
        ))

    def test_instruction_text_int_array_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": WIDE_TEXT}],
            items=[{"instruction_text": self.wide("i")}],
        ))

    def test_holdout_signed_short_array_fires(self):
        check_fires(self, lambda: bundle_with(
            self.wide("h"),
            items=[{"instruction_text": WIDE_TEXT}],
        ))

    def test_signed_byte_array_still_fires(self):
        check_fires(self, lambda: bundle_with(
            array.array("b", HOLDOUT_TEXT.encode("utf-8"))
        ))


class TypecodeUArrayTests(unittest.TestCase):
    """Ruling 213: an array in typecode u stands read as
    the character content it holds, in the governing
    reading the redact exit scan gives that form."""

    def u_array(self, text=HOLDOUT_TEXT):
        return array.array("u", text)

    def test_holdout_u_array_fires(self):
        check_fires(self, lambda: bundle_with(self.u_array()))

    def test_instruction_text_u_array_fires(self):
        check_fires(self, lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{"instruction_text": self.u_array()}],
        ))

    def test_mapping_value_u_array_fires(self):
        check_fires(self, lambda: bundle_with(
            {"first": self.u_array()}
        ))

    def test_memoryview_of_u_array_fires(self):
        check_fires(self, lambda: bundle_with(
            memoryview(self.u_array())
        ))

    def test_direct_act_u_array_forms_fire(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_instruction_item(
            HOLDOUT_TEXT, self.u_array()
        )
        self.assertTrue(result["fired"])
        result = module.audit_instruction_item(
            {"instruction_text": self.u_array()},
            [{"text": HOLDOUT_TEXT}],
        )
        self.assertTrue(result["fired"])

    def test_byte_array_still_fires_and_clean_clears(self):
        check_fires(self, lambda: bundle_with(
            array.array("B", HOLDOUT_TEXT.encode("utf-8"))
        ))
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, bundle_with(
                    self.u_array(),
                    items=[{"instruction_text": CLEAN_TEXT}],
                ))
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)


class NonDictMappingSplitTests(unittest.TestCase):
    """Ruling 214: an item in a non dict mapping form stands
    read for its split side by the partitioning act."""

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
        for surface in ("audit_at_promotion", "audit_at_build",
                        "audit_at_evaluation"):
            with self.subTest(surface=surface):
                result = getattr(module, surface)(make_bundle())
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertFalse(result["promotion_proceeded"])
                self.assertEqual(result["comparisons"], 1)

    def test_holdout_item_as_mappingproxy_in_items(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE),
            types.MappingProxyType(dict(self.HOLDOUT)),
        ]})

    def test_holdout_item_as_userdict_in_items(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE),
            collections.UserDict(dict(self.HOLDOUT)),
        ]})

    def test_holdout_item_as_mappingproxy_in_bare_list(self):
        self.check_refuses(lambda: [
            dict(self.CANDIDATE),
            types.MappingProxyType(dict(self.HOLDOUT)),
        ])

    def test_dict_control_still_refuses(self):
        self.check_refuses(lambda: {"items": [
            dict(self.CANDIDATE), dict(self.HOLDOUT),
        ]})


class IndexedComparisonsRecursionTests(unittest.TestCase):
    """Ruling 215: indexed_comparisons meets a deeply
    nested or cyclic text in a governed form."""

    def bundle_with_text(self, text_value):
        return {"items": [
            {"group": "g1", "signature": "s1", "text": text_value,
             "split": "candidate"},
            {"group": "g1", "signature": "s9",
             "text": "shared bundle text alpha", "split": "holdout"},
        ]}

    def test_deeply_nested_text_no_exception(self):
        nested = HOLDOUT_TEXT
        for _ in range(1500):
            nested = [nested]
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(
            self.bundle_with_text(nested)
        )
        self.assertEqual(result["comparisons"], 0)
        self.assertEqual(result["cost_units"], 0)

    def test_cyclic_text_no_exception(self):
        cyclic = [HOLDOUT_TEXT]
        cyclic.append(cyclic)
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(
            self.bundle_with_text(cyclic)
        )
        self.assertEqual(result["comparisons"], 0)

    def test_standing_counting_form_still_counts(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons({"items": [
            {"group": "g1", "signature": "s1",
             "text": "shared bundle text alpha", "split": "candidate"},
            {"group": "g1", "signature": "s9",
             "text": "shared bundle text alpha", "split": "holdout"},
        ]})
        self.assertEqual(result["comparisons"], 1)
        self.assertEqual(result["cost_weight_per_pair"], 5)


class UserStringReadingTests(unittest.TestCase):
    """Ruling 216: a UserString stands read as the text it
    wraps, clean and firing, at both call points and at
    the direct act."""

    def test_instruction_text_userstring_clean_clears(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, bundle_with(
                    [{"text": HOLDOUT_TEXT}],
                    items=[{
                        "instruction_text":
                            collections.UserString(CLEAN_TEXT)
                    }],
                ))
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)

    def check_fires_in_substance(self, make_bundle):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                result = call(module_name, occasion, make_bundle())
                self.assertTrue(result["fired"])
                self.assertEqual(result["items_tested"], 1)

    def test_instruction_text_userstring_of_holdout_fires(self):
        self.check_fires_in_substance(lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[{
                "instruction_text": collections.UserString(HOLDOUT_TEXT)
            }],
        ))

    def test_item_itself_userstring_fires(self):
        self.check_fires_in_substance(lambda: bundle_with(
            [{"text": HOLDOUT_TEXT}],
            items=[collections.UserString(HOLDOUT_TEXT)],
        ))

    def test_holdout_userstring_fires(self):
        self.check_fires_in_substance(lambda: bundle_with(
            collections.UserString(HOLDOUT_TEXT)
        ))

    def test_holdout_list_holding_userstring_fires(self):
        self.check_fires_in_substance(lambda: bundle_with(
            [collections.UserString(HOLDOUT_TEXT)]
        ))

    def test_direct_act_userstring_forms_decide(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_instruction_item(
            {"instruction_text": collections.UserString(CLEAN_TEXT)},
            [{"text": HOLDOUT_TEXT}],
        )
        self.assertFalse(result["fired"])
        self.assertFalse(result.get("text_form_refused", False))
        result = module.audit_instruction_item(
            HOLDOUT_TEXT, collections.UserString(HOLDOUT_TEXT)
        )
        self.assertTrue(result["fired"])


class BundleIndexUnhashableTests(unittest.TestCase):
    """Ruling 217: an unhashable group or signature value
    meets a governed form, with no exception escaping, at
    every bundle call point and at indexed_comparisons.
    This class pins the exception form only."""

    def bundle(self, field, value):
        candidate = {
            "group": "g1", "signature": "s1",
            "text": "shared bundle text alpha", "split": "candidate",
        }
        holdout = {
            "group": "g1", "signature": "s9",
            "text": "shared bundle text alpha", "split": "holdout",
        }
        candidate[field] = value
        holdout[field] = value
        return {"items": [candidate, holdout]}

    def test_list_group_value_governed_at_bundle_call_points(self):
        module = harness.require("ontoloop.cross_split_audit")
        for surface in ("audit_at_promotion", "audit_at_build",
                        "audit_at_evaluation"):
            with self.subTest(surface=surface):
                result = getattr(module, surface)(
                    self.bundle("group", ["g1"])
                )
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertFalse(result["promotion_proceeded"])
                self.assertEqual(result["comparisons"], 0)

    def test_mapping_signature_value_governed_at_bundle_call_points(self):
        module = harness.require("ontoloop.cross_split_audit")
        for surface in ("audit_at_promotion", "audit_at_build",
                        "audit_at_evaluation"):
            with self.subTest(surface=surface):
                result = getattr(module, surface)(
                    self.bundle("signature", {"s": "s1"})
                )
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertEqual(result["comparisons"], 0)

    def test_unhashable_values_governed_at_indexed_comparisons(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.indexed_comparisons(
            self.bundle("group", ["g1"])
        )
        self.assertEqual(result["comparisons"], 0)
        result = module.indexed_comparisons(
            self.bundle("signature", {"s": "s1"})
        )
        self.assertEqual(result["comparisons"], 0)

    def test_standing_bundle_still_decides(self):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion({"items": [
            {"group": "g1", "signature": "s1",
             "text": "shared bundle text alpha", "split": "candidate"},
            {"group": "g1", "signature": "s9",
             "text": "shared bundle text alpha", "split": "holdout"},
        ]})
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertEqual(result["comparisons"], 1)


if __name__ == "__main__":
    unittest.main()
