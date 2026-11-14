"""Fix round 9, Region 2: eval and store hash surfaces.

Written test first for rulings 257, 258, and 265. A writable
memoryview, a memoryview over a bytearray, hashes with
ValueError where the charged unhashable forms hash with
TypeError, and a Simple figure entry standing in a form the
Advanced lookup cannot key on escapes the store checker.
Each pin states a form.
"""

import unittest

from tests.harness import require

EVAL = "ontoloop.eval"
STORE = "ontoloop.store"

EXPECTED_DEFECTS = [
    {"artifact": "store security record",
     "defect": "limits figure set not the one figure"},
    {"artifact": "store security record",
     "defect": "advanced counterpart missing"},
    {"artifact": "store security record",
     "defect": "advanced figure with no simple counterpart"},
]


def writable_memoryview():
    return memoryview(bytearray(b"writable"))


class TestEvalStoreFixR9(unittest.TestCase):
    # Ruling 257, Chair Finding F-3: aggregate_example meets an
    # example whose hashing raises ValueError in the governed
    # unknown example form.
    def test_aggregate_example_writable_memoryview_raises_governed(self):
        module = require(EVAL)
        example = writable_memoryview()
        with self.assertRaises(ValueError) as caught:
            module.aggregate_example(example)
        self.assertEqual(
            str(caught.exception), "unknown example: %r" % (example,))

    def test_aggregate_example_standing_letters_still_return(self):
        module = require(EVAL)
        for letter in (["B"], {"letter": "B"}):
            with self.assertRaises(ValueError, msg=repr(letter)) as caught:
                module.aggregate_example(letter)
            self.assertEqual(
                str(caught.exception),
                "unknown example: %r" % (letter,))
        for letter in ("B", "D"):
            result = module.aggregate_example(letter)
            scores = result["per_group_scores"]
            self.assertAlmostEqual(
                result["aggregate"], sum(scores) / len(scores))

    # Ruling 258, Chair Finding F-4: margin_components meets a
    # group count whose hashing raises ValueError in the
    # governed unknown group count form.
    def test_margin_components_writable_memoryview_raises_governed(self):
        module = require(EVAL)
        count = writable_memoryview()
        with self.assertRaises(ValueError) as caught:
            module.margin_components(groups=count)
        self.assertEqual(
            str(caught.exception),
            "unknown group count: %r" % (count,))

    def test_margin_components_standing_counts_still_return(self):
        module = require(EVAL)
        for count in ([8], {"count": 8}, {8}):
            with self.assertRaises(ValueError, msg=repr(count)) as caught:
                module.margin_components(groups=count)
            self.assertEqual(
                str(caught.exception),
                "unknown group count: %r" % (count,))
        for count in (8, 10, 30):
            result = module.margin_components(groups=count)
            self.assertEqual(
                set(result["components"]),
                {"practical", "noise", "absolute floor"},
            )

    # Ruling 265, Store Finding F-1: check_store_security_record
    # meets a Simple figure entry standing in a form the
    # Advanced lookup cannot key on, in the governed defect
    # list form, with no exception escaping.
    def _record_with_entry(self, module, entry):
        record = module.store_security_record(
            module.golden_record_store())
        varied = dict(record)
        simple = dict(record["simple"])
        simple["limits_figures"] = [entry]
        varied["simple"] = simple
        return varied

    def test_store_checker_unkeyable_figure_entries_return_defects(self):
        module = require(STORE)
        entries = (["writer wait bound"], {"figure": "writer wait bound"},
                   writable_memoryview())
        for entry in entries:
            defects = module.check_store_security_record(
                self._record_with_entry(module, entry))
            self.assertEqual(defects, EXPECTED_DEFECTS, repr(entry))
            self.assertTrue(all(
                defect["artifact"] == "store security record"
                for defect in defects))

    def test_store_checker_standing_entries_still_return(self):
        module = require(STORE)
        record = module.store_security_record(
            module.golden_record_store())
        self.assertEqual(module.check_store_security_record(record), [])
        for entry in (8, ("writer wait bound",)):
            defects = module.check_store_security_record(
                self._record_with_entry(module, entry))
            self.assertEqual(defects, EXPECTED_DEFECTS, repr(entry))


if __name__ == "__main__":
    unittest.main()
