"""Slice SPEC-PATTERN, list section 2.4, plan section 6.5.

Data structures perspective: these tests pin, per family of
pattern set version 1, the exact expression form: a family is an
expression, never a name alone, and its worked cases split into
positive and negative sets with no overlap.

Transcription decision: the rows state no product API names. The
suite names the product surface for this slice as the module
ontoloop.patterns. The unnumbered failure pair stated in the
SPEC-PATTERN slice paragraph (a family stated only as a name
fails the completeness check) is written as a method of the
SPEC-PATTERN-T02 case and invents no identifier for it.
"""

import re
import unittest

try:
    from tests.harness import require, stage_carried
except ImportError:
    from harness import require, stage_carried

MODULE = "ontoloop.patterns"


class TestSpecPatternT01(unittest.TestCase):
    """SPEC-PATTERN-T01: exact expression per family, version 1."""

    def test_each_family_matches_its_positive_worked_cases(self):
        module = require(MODULE)
        pattern_set = module.pattern_set(version=1)
        self.assertTrue(pattern_set)
        for family, entry in pattern_set.items():
            self.assertEqual(
                set(entry.keys()),
                {"expression", "positive_cases", "negative_cases"},
            )
            self.assertTrue(entry["expression"])
            self.assertTrue(entry["positive_cases"])
            expression = re.compile(entry["expression"])
            for case in entry["positive_cases"]:
                self.assertIsNotNone(expression.fullmatch(case), case)
                self.assertIs(module.matches(family, case, version=1), True)

    def test_each_family_refuses_its_negative_worked_cases(self):
        module = require(MODULE)
        pattern_set = module.pattern_set(version=1)
        for family, entry in pattern_set.items():
            self.assertTrue(entry["negative_cases"])
            self.assertEqual(
                set(entry["positive_cases"]) & set(entry["negative_cases"]),
                set(),
            )
            expression = re.compile(entry["expression"])
            for case in entry["negative_cases"]:
                self.assertIsNone(expression.fullmatch(case), case)
                self.assertIs(module.matches(family, case, version=1), False)


class TestSpecPatternT02(unittest.TestCase):
    """SPEC-PATTERN-T02: boundary case per family, two readings."""

    def test_boundary_case_decided_the_same_way_by_two_readings(self):
        module = require(MODULE)
        result = module.boundary_readings()
        self.assertTrue(result["families"])
        self.assertEqual(
            set(result["families"]),
            set(module.pattern_set(version=1).keys()),
        )
        for family in result["families"]:
            self.assertTrue(
                result["families"][family]["boundary_case"], family
            )
            first = result["families"][family]["first_reading"]
            second = result["families"][family]["second_reading"]
            if first != second:
                self.assertIn(family, result["findings"])
        self.assertEqual(
            set(result["findings"]),
            {
                family
                for family in result["families"]
                if result["families"][family]["first_reading"]
                != result["families"][family]["second_reading"]
            },
        )

    def test_failure_pair_family_stated_only_as_a_name_fails(self):
        module = require(MODULE)
        result = module.completeness_check({"family_without_expression": None})
        self.assertIs(result["complete"], False)
        self.assertEqual(result["incomplete"], ["family_without_expression"])


class TestSpecPatternT03(unittest.TestCase):
    """SPEC-PATTERN-T03: no citation before the slice exit lands."""

    def test_no_persistent_record_cites_version_1_before_exit(self):
        stage_carried(
            "SPEC-PATTERN-T03 evidence home is stage record evidence: "
            "whether any persistent record fixture cites version 1 as "
            "specified before the slice exit lands is read from the "
            "stage record at the slice exit, not from a fixture."
        )


if __name__ == "__main__":
    unittest.main()
