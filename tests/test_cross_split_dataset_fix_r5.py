"""Fix round 5 tests for Region 4: cross split call points,
the shared module side collections, and dataset surfaces.

Charges pinned here, from design/steps/step-15-r5-triage.md:
ruling 39 (N-02, Medium), holdout material in a collection
form the act does not unpack, a set, a frozenset, a
generator of strings or of mappings, and a mapping of
items, either stands unpacked and compared or returns the
governed refusal, at both instruction item call points;
ruling 56 (N-19, Low), the instruction text value in a non
text form either stands read for its text or returns the
governed refusal, at both call points; ruling 81 (N-44,
Medium), a candidate or holdout side of a shared module
bundle standing as a single mapping or a bare string
either stands read for its items or returns the governed
refusal of that surface; ruling 54 (N-17, Low), a non
mapping bundle returns the governed refusal at the dataset
call point only; ruling 51 (N-14, Low), an unhashable kind
returns the stated ValueError form; ruling 52 (N-15, Low),
a non iterable figures value returns the defect list;
ruling 53 (N-16, Low), a present but malformed intake
account returns a defect entry; and ruling 55 (N-18, Low),
next_build checks its pool as a list of run identities.

Genuine forms stand preserved exactly beside each cure:
list, tuple, plain string, and single mapping holdout
material; the S15-R3-016 item extraction forms; both sides
of a bundle in list form; the whole bundle single item
presentation forms; the governed kind forms; the list and
set figures name collections and the mapping figures form;
the standing and absent intake account forms; and the list
and tuple pool forms.
"""

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


def check_fires(testcase, module_name, occasion, bundle):
    module = harness.require(module_name)
    result = module.test_instruction_items_against_holdout(
        bundle, occasion=occasion
    )
    testcase.assertTrue(result["fired"])
    testcase.assertEqual(result["items_tested"], 1)
    testcase.assertEqual(result["fired_item"], HOLDOUT_TEXT)
    testcase.assertNotEqual(
        result.get("test_result_carried_on_promotion_record"), True
    )
    return result


class HoldoutCollectionFormTests(unittest.TestCase):
    """Ruling 39: holdout material in a set, a frozenset, a
    generator, or a mapping of items stands unpacked and
    compared at both call points, beside the control forms."""

    def check_holdout_form(self, make_holdout):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                check_fires(
                    self, module_name, occasion,
                    bundle_with(make_holdout()),
                )

    def test_set_holdout_fires_at_both_call_points(self):
        self.check_holdout_form(lambda: {HOLDOUT_TEXT})

    def test_frozenset_holdout_fires_at_both_call_points(self):
        self.check_holdout_form(lambda: frozenset({HOLDOUT_TEXT}))

    def test_generator_of_strings_fires_at_both_call_points(self):
        self.check_holdout_form(
            lambda: (value for value in [HOLDOUT_TEXT])
        )

    def test_generator_of_mappings_fires_at_both_call_points(self):
        self.check_holdout_form(
            lambda: (value for value in [{"text": HOLDOUT_TEXT}])
        )

    def test_mapping_of_items_fires_at_both_call_points(self):
        self.check_holdout_form(
            lambda: {"first": {"text": HOLDOUT_TEXT}}
        )

    def test_direct_act_counts_one_comparison_on_each_form(self):
        module = harness.require("ontoloop.cross_split_audit")
        forms = (
            lambda: {HOLDOUT_TEXT},
            lambda: frozenset({HOLDOUT_TEXT}),
            lambda: (value for value in [HOLDOUT_TEXT]),
            lambda: (value for value in [{"text": HOLDOUT_TEXT}]),
            lambda: {"first": {"text": HOLDOUT_TEXT}},
        )
        for make_holdout in forms:
            with self.subTest(form=make_holdout):
                result = module.audit_instruction_item(
                    {"instruction_text": HOLDOUT_TEXT}, make_holdout()
                )
                self.assertTrue(result["fired"])
                self.assertEqual(result["comparisons"], 1)

    def test_control_holdout_forms_still_fire_at_both_call_points(self):
        controls = (
            lambda: [{"text": HOLDOUT_TEXT}],
            lambda: ({"text": HOLDOUT_TEXT},),
            lambda: HOLDOUT_TEXT,
            lambda: {"text": HOLDOUT_TEXT},
        )
        for make_holdout in controls:
            self.check_holdout_form(make_holdout)


class InstructionTextFormTests(unittest.TestCase):
    """Ruling 56: an instruction text value standing as a
    list or a mapping, and an item itself standing as a
    list, stand read for the text they carry, at both
    call points, beside the S15-R3-016 extraction forms."""

    def check_item_form(self, item):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                check_fires(
                    self, module_name, occasion,
                    bundle_with(
                        [{"text": HOLDOUT_TEXT}], items=[item]
                    ),
                )

    def test_instruction_text_as_list_fires(self):
        self.check_item_form({"instruction_text": [HOLDOUT_TEXT]})

    def test_instruction_text_as_mapping_fires(self):
        self.check_item_form(
            {"instruction_text": {"text": HOLDOUT_TEXT}}
        )

    def test_item_itself_as_list_fires(self):
        self.check_item_form([HOLDOUT_TEXT])

    def test_extraction_forms_of_r3_016_still_fire(self):
        forms = (
            HOLDOUT_TEXT,
            {"text": HOLDOUT_TEXT},
            {"content": HOLDOUT_TEXT},
            {"instruction_text": HOLDOUT_TEXT},
        )
        for item in forms:
            self.check_item_form(item)

    def test_clean_item_forms_still_clear(self):
        for module_name, occasion in CALL_POINTS:
            with self.subTest(module=module_name, occasion=occasion):
                module = harness.require(module_name)
                bundle = bundle_with(
                    [{"text": HOLDOUT_TEXT}],
                    items=[{"instruction_text": CLEAN_TEXT}],
                )
                result = module.test_instruction_items_against_holdout(
                    bundle, occasion=occasion
                )
                self.assertFalse(result["fired"])
                self.assertEqual(result["items_tested"], 1)


class SharedModuleSideCollectionTests(unittest.TestCase):
    """Ruling 81: a candidate or holdout side standing as a
    single mapping or a bare string returns the governed
    refusal of the shared module bundle surfaces, beside
    the list form control and the whole bundle single item
    presentation controls."""

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

    def check_refused_at_promotion(self, material):
        module = harness.require("ontoloop.cross_split_audit")
        result = module.audit_at_promotion(material)
        self.assertTrue(result["candidate_bundle_refused"])
        self.assertFalse(result["promotion_proceeded"])
        return result

    def test_list_form_control_refuses_on_the_shared_pair(self):
        result = self.check_refused_at_promotion(
            {
                "candidate_items": [self.CANDIDATE],
                "holdout_items": [self.HOLDOUT],
            }
        )
        self.assertEqual(result["comparisons"], 1)

    def test_holdout_side_as_single_mapping_refuses(self):
        self.check_refused_at_promotion(
            {
                "candidate_items": [self.CANDIDATE],
                "holdout_items": self.HOLDOUT,
            }
        )

    def test_candidate_side_as_single_mapping_refuses(self):
        self.check_refused_at_promotion(
            {
                "candidate_items": self.CANDIDATE,
                "holdout_items": [self.HOLDOUT],
            }
        )

    def test_candidate_side_as_bare_string_refuses(self):
        self.check_refused_at_promotion(
            {
                "candidate_items": "shared bundle text alpha",
                "holdout_items": [self.HOLDOUT],
            }
        )

    def test_holdout_side_as_bare_string_refuses(self):
        self.check_refused_at_promotion(
            {
                "candidate_items": [self.CANDIDATE],
                "holdout_items": "shared bundle text alpha",
            }
        )

    def test_single_mapping_side_refuses_at_build_and_evaluation(self):
        module = harness.require("ontoloop.cross_split_audit")
        material = {
            "candidate_items": [self.CANDIDATE],
            "holdout_items": self.HOLDOUT,
        }
        for act in (module.audit_at_build, module.audit_at_evaluation):
            with self.subTest(act=act.__name__):
                result = act(material)
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertFalse(result["promotion_proceeded"])

    def test_clean_list_bundle_still_clears(self):
        module = harness.require("ontoloop.cross_split_audit")
        material = {
            "candidate_items": [
                {"group": "g2", "signature": "s2", "text": CLEAN_TEXT}
            ],
            "holdout_items": [self.HOLDOUT],
        }
        result = module.audit_at_promotion(material)
        self.assertFalse(result["candidate_bundle_refused"])
        self.assertTrue(result["promotion_proceeded"])
        self.assertEqual(result["comparisons"], 0)

    def test_whole_bundle_single_item_controls_stand(self):
        module = harness.require("ontoloop.cross_split_audit")
        for material in ("a clean single string", dict(self.CANDIDATE)):
            with self.subTest(material=type(material).__name__):
                result = module.audit_at_promotion(material)
                self.assertTrue(result["candidate_bundle_refused"])
                self.assertEqual(result["comparisons"], 0)


class NonMappingBundleDatasetTests(unittest.TestCase):
    """Ruling 54: a non mapping bundle returns the governed
    refusal at the dataset call point, with no exception."""

    def check_bundle_form(self, bundle):
        module = harness.require("ontoloop.dataset")
        result = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertEqual(
            result, expected_refusal("candidate construction")
        )
        self.assertNotIn("items_tested", result)

    def test_none_bundle_returns_the_refusal(self):
        self.check_bundle_form(None)

    def test_string_bundle_returns_the_refusal(self):
        self.check_bundle_form("a bundle in string form")

    def test_list_bundle_returns_the_refusal(self):
        self.check_bundle_form([{"instruction_text": HOLDOUT_TEXT}])

    def test_tuple_bundle_returns_the_refusal(self):
        self.check_bundle_form(({"instruction_text": HOLDOUT_TEXT},))

    def test_mapping_bundle_forms_still_decide_as_pinned(self):
        module = harness.require("ontoloop.dataset")
        bundle = bundle_with([{"text": HOLDOUT_TEXT}])
        result = module.test_instruction_items_against_holdout(
            bundle, occasion="candidate construction"
        )
        self.assertTrue(result["fired"])
        self.assertEqual(result["items_tested"], 1)


class CandidateKindFormTests(unittest.TestCase):
    """Ruling 51: an unhashable kind raises the stated
    ValueError form, beside the standing kind forms."""

    def test_list_kind_raises_value_error(self):
        module = harness.require("ontoloop.dataset")
        with self.assertRaises(ValueError):
            module.candidate_with_instruction_item(
                kind=["clean instruction"]
            )

    def test_mapping_kind_raises_value_error(self):
        module = harness.require("ontoloop.dataset")
        with self.assertRaises(ValueError):
            module.candidate_with_instruction_item(kind={"k": 1})

    def test_hashable_outside_kinds_still_raise_value_error(self):
        module = harness.require("ontoloop.dataset")
        for kind in (None, ("clean instruction",), "no such kind"):
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    module.candidate_with_instruction_item(kind=kind)

    def test_governed_kinds_still_return_their_bundles(self):
        module = harness.require("ontoloop.dataset")
        for kind in (
            "verbatim holdout content",
            "near verbatim holdout content",
            "clean instruction",
        ):
            with self.subTest(kind=kind):
                bundle = module.candidate_with_instruction_item(kind=kind)
                self.assertEqual(bundle["kind"], kind)
                self.assertEqual(bundle["instruction_item_count"], 1)


def example_record():
    module = harness.require("ontoloop.dataset")
    return module, module.dataset_record_example_b()


class CheckDatasetRecordFormTests(unittest.TestCase):
    """Rulings 52 and 53: a non iterable figures value
    returns the defect list, and a present but malformed
    intake account returns a defect entry, beside the
    standing forms of both limbs."""

    def test_non_iterable_figures_return_the_defect_list(self):
        module, _record = example_record()
        for value in (123, 1.5, True):
            with self.subTest(value=value):
                _module, record = example_record()
                record["intake_account"]["figures"] = value
                self.assertEqual(
                    module.check_dataset_record(record),
                    [{"artifact": "Dataset record"}],
                )

    def test_governed_figures_forms_still_return_no_defect(self):
        module, record = example_record()
        names = sorted(record["intake_account"]["figures"])
        for value in (list(names), set(names)):
            with self.subTest(form=type(value).__name__):
                _module, fresh = example_record()
                fresh["intake_account"]["figures"] = value
                self.assertEqual(module.check_dataset_record(fresh), [])
        _module, fresh = example_record()
        self.assertEqual(module.check_dataset_record(fresh), [])

    def test_malformed_intake_account_returns_a_defect(self):
        module, _record = example_record()
        for value in ("an account in string form", ["a"], 42):
            with self.subTest(value=value):
                _module, record = example_record()
                record["intake_account"] = value
                self.assertEqual(
                    module.check_dataset_record(record),
                    [{"artifact": "Dataset record"}],
                )

    def test_absent_intake_account_still_returns_no_defect(self):
        module, record = example_record()
        del record["intake_account"]
        self.assertEqual(module.check_dataset_record(record), [])


class NextBuildPoolFormTests(unittest.TestCase):
    """Ruling 55: a string pool value returns the governed
    refusal of the surface instead of exploding into single
    character run identities, beside the standing pools."""

    def test_string_pool_raises_value_error(self):
        module = harness.require("ontoloop.dataset")
        with self.assertRaises(ValueError):
            module.next_build(
                {"pool_run_ids": "abc", "appended_run": "x"}
            )

    def test_list_pool_still_returns_the_following_pool(self):
        module = harness.require("ontoloop.dataset")
        result = module.next_build(
            {"pool_run_ids": ["a", "b"], "appended_run": "x"}
        )
        self.assertEqual(result, {"pool_run_ids": ["a", "b", "x"]})

    def test_tuple_pool_still_returns_its_items_in_order(self):
        module = harness.require("ontoloop.dataset")
        result = module.next_build(
            {"pool_run_ids": ("a", "b"), "appended_run": "x"}
        )
        self.assertEqual(result, {"pool_run_ids": ["a", "b", "x"]})


if __name__ == "__main__":
    unittest.main()
