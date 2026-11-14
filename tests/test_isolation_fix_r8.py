"""Fix round 8 tests for Region 6: the isolation copy act.

Written test first for the position charged at Round 8 triage
ruling 223 (ISO-R8-1): the atom limb of _bundle_copy in
consumption.py returning a subclass instance of a plain atom
type by reference, so a mutable attribute on the subclass
instance is shared in both directions between the original
and the copy. Each class pins the cure beside the standing
registry forms its charge protects: a bundle carrying
subclass instances of the atom types holding a mutable
attribute records and discovers with that attribute copied
apart under both mutation forms, at the store limb, at the
record return limb, and at the discover limb.
"""

import unittest

from tests.harness import require


class IntSub(int):
    pass


class StrSub(str):
    pass


class BytesSub(bytes):
    pass


class FloatSub(float):
    pass


class ComplexSub(complex):
    pass


def _make(cls, value):
    instance = cls(value)
    instance.held = ["original"]
    return instance


CASES = [
    (IntSub, 7),
    (StrSub, "bundle text"),
    (BytesSub, b"bundle bytes"),
    (FloatSub, 2.5),
    (ComplexSub, complex(1, 2)),
]


class TestIsolationFixR8AtomSubclass(unittest.TestCase):
    """Ruling 223: subclass instances of atom types copy apart."""

    def test_caller_mutation_after_record_reaches_no_discover(self):
        module = require("ontoloop.consumption")
        for index, (cls, value) in enumerate(CASES):
            with self.subTest(cls=cls.__name__):
                instance = _make(cls, value)
                bundle = {"part": instance}
                workflow = "r8 caller mutation workflow %d" % index
                module.record_promotion(workflow, bundle)
                instance.held.append("caller mutation")
                found = module.discover(workflow)
                copied = found["bundle"]["part"]
                self.assertIsNot(copied, instance)
                self.assertIsInstance(copied, cls)
                self.assertEqual(copied, value)
                self.assertEqual(copied.held, ["original"])

    def test_discover_mutation_reaches_no_caller_and_no_later(self):
        module = require("ontoloop.consumption")
        for index, (cls, value) in enumerate(CASES):
            with self.subTest(cls=cls.__name__):
                instance = _make(cls, value)
                bundle = {"part": instance}
                workflow = "r8 discover mutation workflow %d" % index
                module.record_promotion(workflow, bundle)
                found = module.discover(workflow)
                found["bundle"]["part"].held.append("return mutation")
                self.assertEqual(instance.held, ["original"])
                again = module.discover(workflow)
                self.assertEqual(again["bundle"]["part"].held, ["original"])
                self.assertIsNot(again["bundle"]["part"], instance)

    def test_record_return_carries_a_copy_not_the_caller_object(self):
        module = require("ontoloop.consumption")
        for index, (cls, value) in enumerate(CASES):
            with self.subTest(cls=cls.__name__):
                instance = _make(cls, value)
                bundle = {"part": instance}
                workflow = "r8 record return workflow %d" % index
                recorded = module.record_promotion(workflow, bundle)
                returned = recorded["bundle"]["part"]
                self.assertIsNot(returned, instance)
                self.assertIsInstance(returned, cls)
                self.assertEqual(returned.held, ["original"])
                returned.held.append("record return mutation")
                self.assertEqual(instance.held, ["original"])
                found = module.discover(workflow)
                self.assertEqual(found["bundle"]["part"].held, ["original"])

    def test_top_level_subclass_bundle_copies_apart(self):
        module = require("ontoloop.consumption")
        instance = _make(IntSub, 11)
        module.record_promotion("r8 top level workflow", instance)
        instance.held.append("caller mutation")
        found = module.discover("r8 top level workflow")
        self.assertIsNot(found["bundle"], instance)
        self.assertIsInstance(found["bundle"], IntSub)
        self.assertEqual(found["bundle"], 11)
        self.assertEqual(found["bundle"].held, ["original"])

    def test_subclass_inside_list_copies_apart(self):
        module = require("ontoloop.consumption")
        instance = _make(StrSub, "nested text")
        bundle = {"items": ["x", instance]}
        module.record_promotion("r8 nested list workflow", bundle)
        instance.held.append("caller mutation")
        found = module.discover("r8 nested list workflow")
        copied = found["bundle"]["items"][1]
        self.assertIsNot(copied, instance)
        self.assertEqual(copied.held, ["original"])
        copied.held.append("return mutation")
        self.assertEqual(instance.held, ["original", "caller mutation"])
        again = module.discover("r8 nested list workflow")
        self.assertEqual(again["bundle"]["items"][1].held, ["original"])

    def test_plain_atom_forms_still_pass(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r8 standing workflow", "bundle version 1"
        )
        self.assertEqual(recorded["bundle"], "bundle version 1")
        found = module.discover("r8 standing workflow")
        self.assertEqual(found["bundle"], "bundle version 1")
        plain = module.record_promotion(
            "r8 plain atoms workflow",
            {"n": 3, "f": 1.5, "b": True, "raw": b"xy", "none": None},
        )
        self.assertEqual(
            plain["bundle"],
            {"n": 3, "f": 1.5, "b": True, "raw": b"xy", "none": None},
        )
        missing = module.discover("r8 never recorded workflow")
        self.assertEqual(missing["answer"], "no promotion")
        self.assertIsNone(missing["bundle"])


if __name__ == "__main__":
    unittest.main()
