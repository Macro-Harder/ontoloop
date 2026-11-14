"""Fix round 9 tests for Region 6: the isolation copy act.

Written test first for the positions charged at Round 9 triage
rulings 279 and 280: the copy act _bundle_copy in consumption.py
returning an enum member itself where the member carries mutable
instance state, so the state stands shared in both directions,
and the structural limbs of the same act dropping the instance
attribute state of a container or wrapper part, downgrading
several subclass forms to their plain base type, and losing a
defaultdict factory. Each class pins the cure beside the
standing forms its charge protects.
"""

import unittest
from array import array
from collections import ChainMap, UserDict, UserList, UserString
from collections import defaultdict, deque, namedtuple
from enum import Enum, IntEnum, IntFlag, StrEnum
from types import MappingProxyType

from tests.harness import require


class IntMember(IntEnum):
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4
    M5 = 5
    M6 = 6


class StrMember(StrEnum):
    M1 = "one"
    M2 = "two"
    M3 = "three"
    M4 = "four"
    M5 = "five"
    M6 = "six"


class FlagMember(IntFlag):
    M1 = 1
    M2 = 2
    M3 = 4
    M4 = 8
    M5 = 16
    M6 = 32


class PlainMember(Enum):
    M1 = "one"
    M2 = "two"
    M3 = "three"
    M4 = "four"
    M5 = "five"
    M6 = "six"


MEMBER_CLASSES = [IntMember, StrMember, FlagMember, PlainMember]

REFUSAL_MESSAGE = "enum member with mutable instance state in bundle copy"


class DictSub(dict):
    pass


class ListSub(list):
    pass


class SetSub(set):
    pass


class FrozenSub(frozenset):
    pass


class TupleSub(tuple):
    pass


class BytearraySub(bytearray):
    pass


class DequeSub(deque):
    pass


class ArraySub(array):
    pass


class UserDictSub(UserDict):
    pass


class UserListSub(UserList):
    pass


class ChainMapSub(ChainMap):
    pass


class DefaultDictSub(defaultdict):
    pass


class PairBase(namedtuple("PairBase", ["x", "y"])):
    pass


class NeedsArgumentDict(dict):
    def __init__(self, required):
        super().__init__()


class IntSub(int):
    pass


def _held(instance):
    instance.held = ["original"]
    return instance


FORMS = [
    ("dict subclass", lambda: _held(DictSub({"k": "v"}))),
    ("list subclass", lambda: _held(ListSub([1, 2]))),
    ("set subclass", lambda: _held(SetSub({1, 2}))),
    ("frozenset subclass", lambda: _held(FrozenSub({1, 2}))),
    ("tuple subclass", lambda: _held(TupleSub((1, 2)))),
    ("bytearray subclass", lambda: _held(BytearraySub(b"ab"))),
    ("deque subclass", lambda: _held(DequeSub([1, 2]))),
    ("array subclass", lambda: _held(ArraySub("i", [1, 2]))),
    ("plain UserDict", lambda: _held(UserDict({"k": "v"}))),
    ("plain UserList", lambda: _held(UserList([1, 2]))),
    ("plain UserString", lambda: _held(UserString("bundle text"))),
    ("plain ChainMap", lambda: _held(ChainMap({"k": "v"}))),
    ("UserDict subclass", lambda: _held(UserDictSub({"k": "v"}))),
    ("UserList subclass", lambda: _held(UserListSub([1, 2]))),
    ("ChainMap subclass", lambda: _held(ChainMapSub({"k": "v"}))),
    ("namedtuple subclass", lambda: _held(PairBase(1, 2))),
]


class TestIsolationFixR9EnumMember(unittest.TestCase):
    """Ruling 279: an enum member carrying mutable state is refused."""

    def test_refusal_at_mapping_value_position(self):
        module = require("ontoloop.consumption")
        for index, cls in enumerate(MEMBER_CLASSES):
            with self.subTest(cls=cls.__name__):
                member = cls.M1
                member.held = ["original"]
                workflow = "r9 enum mapping workflow %d" % index
                with self.assertRaises(ValueError) as caught:
                    module.record_promotion(workflow, {"part": member})
                self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_refusal_at_top_level_position(self):
        module = require("ontoloop.consumption")
        for index, cls in enumerate(MEMBER_CLASSES):
            with self.subTest(cls=cls.__name__):
                member = cls.M2
                member.held = ["original"]
                workflow = "r9 enum top level workflow %d" % index
                with self.assertRaises(ValueError) as caught:
                    module.record_promotion(workflow, member)
                self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_refusal_inside_a_list(self):
        module = require("ontoloop.consumption")
        for index, cls in enumerate(MEMBER_CLASSES):
            with self.subTest(cls=cls.__name__):
                member = cls.M3
                member.held = ["original"]
                bundle = {"items": ["x", member]}
                workflow = "r9 enum list workflow %d" % index
                with self.assertRaises(ValueError) as caught:
                    module.record_promotion(workflow, bundle)
                self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_refusal_inside_a_tuple(self):
        module = require("ontoloop.consumption")
        for index, cls in enumerate(MEMBER_CLASSES):
            with self.subTest(cls=cls.__name__):
                member = cls.M4
                member.held = ["original"]
                bundle = {"pair": (member, 1)}
                workflow = "r9 enum tuple workflow %d" % index
                with self.assertRaises(ValueError) as caught:
                    module.record_promotion(workflow, bundle)
                self.assertEqual(str(caught.exception), REFUSAL_MESSAGE)

    def test_member_with_no_added_attribute_stands_shared(self):
        module = require("ontoloop.consumption")
        for index, cls in enumerate(MEMBER_CLASSES):
            with self.subTest(cls=cls.__name__):
                member = cls.M5
                workflow = "r9 enum plain workflow %d" % index
                recorded = module.record_promotion(workflow, {"part": member})
                self.assertIs(recorded["bundle"]["part"], member)
                found = module.discover(workflow)
                self.assertIs(found["bundle"]["part"], member)

    def test_member_with_immutable_attribute_alone_stands_shared(self):
        module = require("ontoloop.consumption")
        for index, cls in enumerate(MEMBER_CLASSES):
            with self.subTest(cls=cls.__name__):
                member = cls.M6
                member.note = "plain"
                workflow = "r9 enum immutable workflow %d" % index
                recorded = module.record_promotion(workflow, {"part": member})
                self.assertIs(recorded["bundle"]["part"], member)
                found = module.discover(workflow)
                self.assertIs(found["bundle"]["part"], member)
                self.assertEqual(found["bundle"]["part"].note, "plain")


class TestIsolationFixR9ContainerAttributes(unittest.TestCase):
    """Ruling 280: container and wrapper parts copy their attributes."""

    def test_caller_mutation_after_record_reaches_no_discover(self):
        module = require("ontoloop.consumption")
        for index, (name, make) in enumerate(FORMS):
            with self.subTest(form=name):
                instance = make()
                workflow = "r9 forms caller workflow %d" % index
                module.record_promotion(workflow, {"part": instance})
                instance.held.append("caller mutation")
                found = module.discover(workflow)
                copied = found["bundle"]["part"]
                self.assertIsNot(copied, instance)
                self.assertIs(type(copied), type(instance))
                self.assertEqual(copied, instance)
                self.assertEqual(copied.held, ["original"])

    def test_discover_mutation_reaches_no_caller_and_no_later(self):
        module = require("ontoloop.consumption")
        for index, (name, make) in enumerate(FORMS):
            with self.subTest(form=name):
                instance = make()
                workflow = "r9 forms discover workflow %d" % index
                module.record_promotion(workflow, {"part": instance})
                found = module.discover(workflow)
                copied = found["bundle"]["part"]
                self.assertIs(type(copied), type(instance))
                copied.held.append("return mutation")
                self.assertEqual(instance.held, ["original"])
                again = module.discover(workflow)
                self.assertEqual(again["bundle"]["part"].held, ["original"])
                self.assertIsNot(again["bundle"]["part"], instance)

    def test_record_return_carries_attribute_apart(self):
        module = require("ontoloop.consumption")
        for index, (name, make) in enumerate(FORMS):
            with self.subTest(form=name):
                instance = make()
                workflow = "r9 forms record workflow %d" % index
                recorded = module.record_promotion(workflow, {"part": instance})
                returned = recorded["bundle"]["part"]
                self.assertIsNot(returned, instance)
                self.assertIs(type(returned), type(instance))
                self.assertEqual(returned.held, ["original"])
                returned.held.append("record return mutation")
                self.assertEqual(instance.held, ["original"])
                found = module.discover(workflow)
                self.assertEqual(found["bundle"]["part"].held, ["original"])

    def test_top_level_attribute_form_copies_apart(self):
        module = require("ontoloop.consumption")
        instance = _held(DictSub({"k": "v"}))
        module.record_promotion("r9 forms top level workflow", instance)
        instance.held.append("caller mutation")
        found = module.discover("r9 forms top level workflow")
        copied = found["bundle"]
        self.assertIsNot(copied, instance)
        self.assertIs(type(copied), DictSub)
        self.assertEqual(copied, {"k": "v"})
        self.assertEqual(copied.held, ["original"])

    def test_defaultdict_factory_stands_on_the_copy(self):
        module = require("ontoloop.consumption")
        plain = defaultdict(list, {"k": [1]})
        module.record_promotion("r9 plain defaultdict workflow", {"part": plain})
        found = module.discover("r9 plain defaultdict workflow")
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), defaultdict)
        self.assertIs(copied.default_factory, list)
        self.assertEqual(copied["missing"], [])
        subclassed = _held(DefaultDictSub(list, {"k": [1]}))
        module.record_promotion(
            "r9 subclass defaultdict workflow", {"part": subclassed}
        )
        subclassed.held.append("caller mutation")
        found = module.discover("r9 subclass defaultdict workflow")
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), DefaultDictSub)
        self.assertIs(copied.default_factory, list)
        self.assertEqual(copied.held, ["original"])
        self.assertEqual(copied["missing"], [])

    def test_dict_subclass_requiring_an_argument_falls_back(self):
        module = require("ontoloop.consumption")
        instance = NeedsArgumentDict("seed")
        instance["k"] = ["v"]
        module.record_promotion("r9 fallback workflow", {"part": instance})
        instance["k"].append("caller mutation")
        found = module.discover("r9 fallback workflow")
        copied = found["bundle"]["part"]
        self.assertIs(type(copied), dict)
        self.assertEqual(copied, {"k": ["v"]})

    def test_standing_forms_still_pass(self):
        module = require("ontoloop.consumption")
        atom = IntSub(7)
        atom.held = ["original"]
        module.record_promotion("r9 standing atom workflow", {"part": atom})
        atom.held.append("caller mutation")
        found = module.discover("r9 standing atom workflow")
        copied_atom = found["bundle"]["part"]
        self.assertIsNot(copied_atom, atom)
        self.assertIsInstance(copied_atom, IntSub)
        self.assertEqual(copied_atom.held, ["original"])
        proxy = MappingProxyType({"k": ["v"]})
        module.record_promotion("r9 standing proxy workflow", {"part": proxy})
        found = module.discover("r9 standing proxy workflow")
        copied_proxy = found["bundle"]["part"]
        self.assertIs(type(copied_proxy), dict)
        self.assertEqual(copied_proxy, {"k": ["v"]})
        view = memoryview(b"abc")
        module.record_promotion("r9 standing view workflow", {"part": view})
        found = module.discover("r9 standing view workflow")
        copied_view = found["bundle"]["part"]
        self.assertIs(type(copied_view), bytearray)
        self.assertEqual(bytes(copied_view), b"abc")
        recorded = module.record_promotion(
            "r9 standing text workflow", "bundle version 1"
        )
        self.assertEqual(recorded["bundle"], "bundle version 1")
        found = module.discover("r9 standing text workflow")
        self.assertEqual(found["bundle"], "bundle version 1")
        missing = module.discover("r9 never recorded workflow")
        self.assertEqual(missing["answer"], "no promotion")
        self.assertIsNone(missing["bundle"])


if __name__ == "__main__":
    unittest.main()
