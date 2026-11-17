"""Fix round 22 tests for Region 5: consume surfaces and digest.

Written test first for the seven positions charged at Round 22
triage rulings 911 to 917, each in the tagged digest form of
consumption.py: ruling 911 (Consume Finding 1, an address stated
in groups separated by a separator sequence standing longer
than one character, with Lead Engineer line E-41 merged),
ruling 912 (Consume Finding 2, slot content standing in a base
class whose stated slot name a subclass states again under a
plain name or a single underscore name), ruling 913 (Consume
Finding 3, the name and object channels of an AttributeError),
ruling 914 (Consume Finding 4, the name channel of a NameError,
including UnboundLocalError), ruling 915 (Consume Finding 5,
the subexception content of an exception group, with Lead
Engineer line E-43 merged), ruling 916 (Consume Finding 6, two
distinct defaultdict factory types created by type constructor
calls or by successive redefinition taking one factory token,
with Lead Engineer line E-42 merged), and ruling 917 (Consume
Finding 7, a class standing as a value digesting over its
string form alone). Each class pins its ruling beside the
standing forms its cure protects.
"""

import collections
import datetime
import decimal
import re
import unittest

from tests.harness import require


def _digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


def _decimal_groups(value, separator):
    return format(value, ",").replace(",", separator)


def _hex_pairs(value, separator):
    text = format(value, "x")
    if len(text) % 2:
        text = "0" + text
    pairs = [text[index:index + 2] for index in range(0, len(text), 2)]
    return separator.join(pairs)


def _hex_fours(value, separator):
    text = format(value, "x")
    groups = []
    while text:
        groups.append(text[-4:])
        text = text[:-4]
    return separator.join(reversed(groups))


class _DecCommaSpaceProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), ", "),
        )


class _DecColonSpaceProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), ": "),
        )


class _DecSpaceHyphenSpaceProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), " - "),
        )


class _DecTwoStopsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), ".."),
        )


class _DecTwoHyphensProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), "--"),
        )


class _HexCommaSpacePairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), ", "),)


class _HexTwoColonsPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), "::"),)


class _HexHyphenSpacePairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), "- "),)


class _HexTwoColonsFoursProbe:
    __slots__ = ()

    def __repr__(self):
        return "fours probe %s" % (
            _hex_fours(id(self) + 0xABCDEF0000000000, "::"),
        )


class _DecColonGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), ":"),)


class _CoveredAddressProbe:
    __slots__ = ()

    def __repr__(self):
        return "<covered probe at %s>" % (hex(id(self)),)


class _ShortNumberProbe:
    __slots__ = ("_text",)

    def __init__(self, text):
        self._text = text

    def __repr__(self):
        return self._text


class _PlainSlotBase:
    __slots__ = ("x",)

    def __init__(self, base_value):
        _PlainSlotBase.__dict__["x"].__set__(self, base_value)


class _PlainSlotSub(_PlainSlotBase):
    __slots__ = ("x",)

    def __init__(self, base_value, sub_value):
        super().__init__(base_value)
        _PlainSlotSub.__dict__["x"].__set__(self, sub_value)


class _UnderscoreSlotBase:
    __slots__ = ("_x",)

    def __init__(self, base_value):
        _UnderscoreSlotBase.__dict__["_x"].__set__(self, base_value)


class _UnderscoreSlotSub(_UnderscoreSlotBase):
    __slots__ = ("_x",)

    def __init__(self, base_value, sub_value):
        super().__init__(base_value)
        _UnderscoreSlotSub.__dict__["_x"].__set__(self, sub_value)


class _PlainSingleSlot:
    __slots__ = ("x",)

    def __init__(self, value):
        self.x = value


class _PrivateSlots:
    __slots__ = ("__hidden", "shown")

    def __init__(self, hidden, shown):
        self.__hidden = hidden
        self.shown = shown


class _ShadowBase:
    __slots__ = ("__hidden", "shown")

    def __init__(self, hidden, shown):
        self.__hidden = hidden
        self.shown = shown


class _ShadowSub(_ShadowBase):
    __slots__ = ("__hidden",)

    def __init__(self, base_hidden, sub_hidden, shown):
        super().__init__(base_hidden, shown)
        self.__hidden = sub_hidden


def _attribute_error(name, obj, message="missing attribute"):
    return AttributeError(message, name=name, obj=obj)


def _name_error(name, message="name is not defined"):
    return NameError(message, name=name)


def _make_local_factory():
    class _CollidingFactory:
        pass

    return _CollidingFactory


class _ModuleFactory:
    pass


class _RedefinedFactory:
    pass


_RETAINED_FACTORY = _RedefinedFactory


class _RedefinedFactory:
    pass


def _make_colliding_class(value):
    class _CollidingClass:
        held = value

    return _CollidingClass


def _make_method_class(value):
    class _MethodClass:
        held = value

        def describe(self):
            return "described"

    return _MethodClass


class _StandingClassAlpha:
    held = "alpha"


class _StandingClassBeta:
    held = "beta"


class TestConsumeFixR22AddressSequenceForms(unittest.TestCase):
    """Fix round 22, ruling 911: the separator sequence width.

    An address stated in groups separated by a separator
    sequence standing longer than one character stands refused
    at the digest surface in the governed form of ruling 850,
    as a width question on the one reading, beside the content
    bearing string forms still digesting by their content and
    the single character separator forms of ruling 850 still
    deciding as they decide.
    """

    _DECIMAL_DRESSES = (
        _DecCommaSpaceProbe,
        _DecColonSpaceProbe,
        _DecSpaceHyphenSpaceProbe,
        _DecTwoStopsProbe,
        _DecTwoHyphensProbe,
    )

    _PAIR_DRESSES = (
        _HexCommaSpacePairsProbe,
        _HexTwoColonsPairsProbe,
        _HexHyphenSpacePairsProbe,
    )

    def test_ruling_911_decimal_sequence_dresses_refused(self):
        module = require("ontoloop.consumption")
        for probe in self._DECIMAL_DRESSES:
            first, second = probe(), probe()
            for instance in (first, second):
                with self.assertRaises(
                    ValueError, msg=probe.__name__
                ) as caught:
                    module.load_with_hash_check(instance)
                self.assertEqual(
                    str(caught.exception),
                    "digest cannot read material of type "
                    + probe.__name__,
                )

    def test_ruling_911_hex_pairs_sequence_dresses_refused(self):
        module = require("ontoloop.consumption")
        for probe in self._PAIR_DRESSES:
            first, second = probe(), probe()
            for instance in (first, second):
                with self.assertRaises(
                    ValueError, msg=probe.__name__
                ) as caught:
                    module.load_with_hash_check(instance)
                self.assertEqual(
                    str(caught.exception),
                    "digest cannot read material of type "
                    + probe.__name__,
                )

    def test_ruling_911_hex_fours_sequence_dress_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_HexTwoColonsFoursProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_HexTwoColonsFoursProbe",
        )

    def test_ruling_911_sequence_dress_nested_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check([_DecCommaSpaceProbe()])
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecCommaSpaceProbe",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                {"k": _HexTwoColonsPairsProbe()}
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_HexTwoColonsPairsProbe",
        )

    def test_ruling_911_hash_check_on_fresh_instance_refused(self):
        module = require("ontoloop.consumption")
        held_first, held_second = (
            _DecTwoHyphensProbe(),
            _DecTwoHyphensProbe(),
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                held_second, expected_hash="0" * 64
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecTwoHyphensProbe",
        )
        self.assertIsNotNone(held_first)

    def test_ruling_911_content_bearing_string_forms_still_digest(self):
        self.assertNotEqual(_digest(range(3)), _digest(range(4)))
        self.assertNotEqual(
            _digest(re.compile("alpha")), _digest(re.compile("beta"))
        )
        self.assertNotEqual(
            _digest(decimal.Decimal("1.5")),
            _digest(decimal.Decimal("2.5")),
        )
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )
        self.assertNotEqual(
            _digest(datetime.datetime(2026, 1, 1, 12, 30, 15)),
            _digest(datetime.datetime(2027, 1, 1, 12, 30, 15)),
        )

    def test_ruling_911_single_character_forms_still_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_DecColonGroupsProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecColonGroupsProbe",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_CoveredAddressProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_CoveredAddressProbe",
        )

    def test_ruling_911_short_forms_and_no_content_form_stand(self):
        short_one = _ShortNumberProbe("<short probe at 123>")
        short_two = _ShortNumberProbe("<short probe at 124>")
        self.assertNotEqual(_digest(short_one), _digest(short_two))
        self.assertEqual(
            _digest(_ShortNumberProbe("<short probe at 123>")),
            _digest(short_one),
        )
        self.assertEqual(_digest(object()), _digest(object()))


class TestConsumeFixR22RestatedSlotNames(unittest.TestCase):
    """Fix round 22, ruling 912: the restated plain slot name.

    Slot content standing in a base class whose stated slot
    name a subclass states again under a plain name or a
    single underscore name stands read by the residual content
    reading at every stating class, so material differing in
    that content alone digests apart, beside the standing slot
    forms and the ruling 851 forms still deciding as they
    decide.
    """

    def test_ruling_912_plain_base_slot_content_apart(self):
        self.assertNotEqual(
            _digest(_PlainSlotSub("base_a", "sub")),
            _digest(_PlainSlotSub("base_b", "sub")),
        )
        self.assertEqual(
            _digest(_PlainSlotSub("base_a", "sub")),
            _digest(_PlainSlotSub("base_a", "sub")),
        )

    def test_ruling_912_single_underscore_base_content_apart(self):
        self.assertNotEqual(
            _digest(_UnderscoreSlotSub("base_a", "sub")),
            _digest(_UnderscoreSlotSub("base_b", "sub")),
        )
        self.assertEqual(
            _digest(_UnderscoreSlotSub("base_a", "sub")),
            _digest(_UnderscoreSlotSub("base_a", "sub")),
        )

    def test_ruling_912_residual_mapping_carries_both_slots(self):
        module = require("ontoloop.consumption")
        mapping = module._residual_content_mapping(
            _PlainSlotSub("base_a", "sub")
        )
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping["x"], "sub")
        self.assertIn("base_a", mapping.values())
        self.assertGreaterEqual(len(mapping), 2)
        under = module._residual_content_mapping(
            _UnderscoreSlotSub("base_a", "sub")
        )
        self.assertIsNotNone(under)
        self.assertEqual(under["_x"], "sub")
        self.assertIn("base_a", under.values())

    def test_ruling_912_restated_slot_nested_and_mapping_value(self):
        self.assertNotEqual(
            _digest([_PlainSlotSub("base_a", "sub")]),
            _digest([_PlainSlotSub("base_b", "sub")]),
        )
        self.assertNotEqual(
            _digest({"wrap": _UnderscoreSlotSub("base_a", "sub")}),
            _digest({"wrap": _UnderscoreSlotSub("base_b", "sub")}),
        )

    def test_ruling_912_hash_check_rejects_differing_base(self):
        module = require("ontoloop.consumption")
        expected = _digest(_PlainSlotSub("base_a", "sub"))
        refused = module.load_with_hash_check(
            _PlainSlotSub("base_b", "sub"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _PlainSlotSub("base_a", "sub"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_912_standing_slot_forms_still_decide(self):
        self.assertNotEqual(
            _digest(_PlainSlotSub("base_a", "sub_a")),
            _digest(_PlainSlotSub("base_a", "sub_b")),
        )
        self.assertNotEqual(
            _digest(_PlainSingleSlot("alpha")),
            _digest(_PlainSingleSlot("beta")),
        )
        self.assertEqual(
            _digest(_PlainSingleSlot("alpha")),
            _digest(_PlainSingleSlot("alpha")),
        )
        self.assertNotEqual(
            _digest(_PrivateSlots("alpha", "x")),
            _digest(_PrivateSlots("beta", "x")),
        )
        self.assertNotEqual(
            _digest(_ShadowSub("base_a", "sub", "s")),
            _digest(_ShadowSub("base_b", "sub", "s")),
        )


class TestConsumeFixR22AttributeErrorChannels(unittest.TestCase):
    """Fix round 22, ruling 913: the AttributeError channels.

    The exception kind reading states the name and object
    channels of an AttributeError beside its argument content
    and its added state, so two materials differing in any of
    those channels digest apart, in the plain form and in the
    added state form alike.
    """

    def test_ruling_913_differing_name_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_attribute_error("attr_a", "thing")),
            _digest(_attribute_error("attr_b", "thing")),
        )
        self.assertEqual(
            _digest(_attribute_error("attr_a", "thing")),
            _digest(_attribute_error("attr_a", "thing")),
        )

    def test_ruling_913_differing_object_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_attribute_error("attr", "thing_a")),
            _digest(_attribute_error("attr", "thing_b")),
        )
        self.assertNotEqual(
            _digest(_attribute_error("attr", [1, 2])),
            _digest(_attribute_error("attr", [1, 3])),
        )
        self.assertEqual(
            _digest(_attribute_error("attr", [1, 2])),
            _digest(_attribute_error("attr", [1, 2])),
        )

    def test_ruling_913_differing_name_with_added_state_apart(self):
        first = _attribute_error("attr_a", "thing")
        first.extra = "x"
        second = _attribute_error("attr_b", "thing")
        second.extra = "x"
        twin = _attribute_error("attr_a", "thing")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_913_differing_object_with_added_state_apart(self):
        first = _attribute_error("attr", "thing_a")
        first.extra = "x"
        second = _attribute_error("attr", "thing_b")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_913_attribute_error_nested_and_hash_check(self):
        module = require("ontoloop.consumption")
        self.assertNotEqual(
            _digest([_attribute_error("attr_a", "thing")]),
            _digest([_attribute_error("attr_b", "thing")]),
        )
        expected = _digest(_attribute_error("attr_a", "thing"))
        refused = module.load_with_hash_check(
            _attribute_error("attr_b", "thing"),
            expected_hash=expected,
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _attribute_error("attr_a", "thing"),
            expected_hash=expected,
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_913_standing_exception_forms_still_decide(self):
        self.assertNotEqual(
            _digest(_attribute_error("attr", "thing", "message_a")),
            _digest(_attribute_error("attr", "thing", "message_b")),
        )
        self.assertNotEqual(
            _digest(ImportError("m", name="mod_a", path="/p/a")),
            _digest(ImportError("m", name="mod_b", path="/p/a")),
        )
        first = OSError(2, "msg", "file_a")
        first.extra = "x"
        second = OSError(2, "msg", "file_b")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(
            _digest(ValueError("alpha")), _digest(ValueError("beta"))
        )


class TestConsumeFixR22NameErrorChannel(unittest.TestCase):
    """Fix round 22, ruling 914: the NameError name channel.

    The exception kind reading states the name channel of a
    NameError beside its argument content and its added state,
    so two materials differing in that channel digest apart,
    in the plain form and in the added state form alike, the
    UnboundLocalError subclass deciding in the same form.
    """

    def test_ruling_914_differing_name_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_name_error("name_a")),
            _digest(_name_error("name_b")),
        )
        self.assertEqual(
            _digest(_name_error("name_a")),
            _digest(_name_error("name_a")),
        )

    def test_ruling_914_unbound_local_error_name_apart(self):
        self.assertNotEqual(
            _digest(UnboundLocalError("m", name="name_a")),
            _digest(UnboundLocalError("m", name="name_b")),
        )
        self.assertEqual(
            _digest(UnboundLocalError("m", name="name_a")),
            _digest(UnboundLocalError("m", name="name_a")),
        )

    def test_ruling_914_differing_name_with_added_state_apart(self):
        first = _name_error("name_a")
        first.extra = "x"
        second = _name_error("name_b")
        second.extra = "x"
        twin = _name_error("name_a")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_914_name_error_nested_read(self):
        self.assertNotEqual(
            _digest([_name_error("name_a")]),
            _digest([_name_error("name_b")]),
        )
        self.assertNotEqual(
            _digest({"wrap": _name_error("name_a")}),
            _digest({"wrap": _name_error("name_b")}),
        )

    def test_ruling_914_hash_check_rejects_differing_name(self):
        module = require("ontoloop.consumption")
        expected = _digest(_name_error("name_a"))
        refused = module.load_with_hash_check(
            _name_error("name_b"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _name_error("name_a"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_914_standing_exception_forms_still_decide(self):
        self.assertNotEqual(
            _digest(_name_error("name_a", "message_a")),
            _digest(_name_error("name_a", "message_b")),
        )
        caused = ValueError("main")
        caused.__cause__ = ValueError("cause_a")
        other_caused = ValueError("main")
        other_caused.__cause__ = ValueError("cause_b")
        self.assertNotEqual(_digest(caused), _digest(other_caused))
        self.assertEqual(
            _digest(ValueError("alpha")), _digest(ValueError("alpha"))
        )


class TestConsumeFixR22ExceptionGroupChannel(unittest.TestCase):
    """Fix round 22, ruling 915: the group subexception channel.

    The exception channel reading states the subexception
    content an exception group carries beside its argument
    content and its added state, so two groups differing in a
    subexception alone digest apart in the plain form as in
    the added state form.
    """

    def test_ruling_915_differing_subexception_argument_apart(self):
        self.assertNotEqual(
            _digest(BaseExceptionGroup("grp", [ValueError("a")])),
            _digest(BaseExceptionGroup("grp", [ValueError("b")])),
        )
        self.assertEqual(
            _digest(BaseExceptionGroup("grp", [ValueError("a")])),
            _digest(BaseExceptionGroup("grp", [ValueError("a")])),
        )

    def test_ruling_915_differing_subexception_type_apart(self):
        self.assertNotEqual(
            _digest(ExceptionGroup("grp", [ValueError("a")])),
            _digest(ExceptionGroup("grp", [KeyError("a")])),
        )
        self.assertEqual(
            _digest(ExceptionGroup("grp", [ValueError("a")])),
            _digest(ExceptionGroup("grp", [ValueError("a")])),
        )

    def test_ruling_915_differing_subexception_message_apart(self):
        first = BaseExceptionGroup(
            "grp", [ValueError("first message")]
        )
        second = BaseExceptionGroup(
            "grp", [ValueError("second message")]
        )
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_915_group_nested_in_list_apart(self):
        self.assertNotEqual(
            _digest([BaseExceptionGroup("grp", [ValueError("a")])]),
            _digest([BaseExceptionGroup("grp", [ValueError("b")])]),
        )
        self.assertNotEqual(
            _digest({"wrap": ExceptionGroup("grp", [ValueError("a")])}),
            _digest({"wrap": ExceptionGroup("grp", [KeyError("a")])}),
        )

    def test_ruling_915_hash_check_rejects_differing_group(self):
        module = require("ontoloop.consumption")
        expected = _digest(
            BaseExceptionGroup("grp", [ValueError("a")])
        )
        refused = module.load_with_hash_check(
            BaseExceptionGroup("grp", [ValueError("b")]),
            expected_hash=expected,
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            BaseExceptionGroup("grp", [ValueError("a")]),
            expected_hash=expected,
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_915_group_with_added_state_still_apart(self):
        first = BaseExceptionGroup("grp", [ValueError("a")])
        first.extra = "x"
        second = BaseExceptionGroup("grp", [ValueError("b")])
        second.extra = "x"
        twin = BaseExceptionGroup("grp", [ValueError("a")])
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_915_standing_group_forms_still_decide(self):
        self.assertNotEqual(
            _digest(BaseExceptionGroup("grp_a", [ValueError("a")])),
            _digest(BaseExceptionGroup("grp_b", [ValueError("a")])),
        )
        self.assertNotEqual(
            _digest(
                BaseExceptionGroup(
                    "grp", [ValueError("a"), ValueError("a")]
                )
            ),
            _digest(BaseExceptionGroup("grp", [ValueError("a")])),
        )
        self.assertNotEqual(
            _digest(ValueError("alpha")), _digest(ValueError("beta"))
        )


class TestConsumeFixR22FactoryTokenForms(unittest.TestCase):
    """Fix round 22, ruling 916: the defaultdict factory token.

    The factory token states the factory itself in a governed
    form no two distinct factory types share: a factory type
    created by a type constructor call, or retained from a
    definition a later definition of the same name replaced,
    stands under the governed refusal for the digest act where
    no standing module state names that type, beside the
    module level type factories and the builtin callable
    factories still deciding as they decide.
    """

    def test_ruling_916_dynamic_factory_types_refused(self):
        module = require("ontoloop.consumption")
        first_factory = type(
            "DynFactory", (), {"__module__": __name__}
        )
        second_factory = type(
            "DynFactory", (), {"__module__": __name__}
        )
        self.assertIsNot(first_factory, second_factory)
        self.assertEqual(
            first_factory.__module__
            + "."
            + first_factory.__qualname__,
            second_factory.__module__
            + "."
            + second_factory.__qualname__,
        )
        for factory in (first_factory, second_factory):
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check(
                    collections.defaultdict(factory, {"k": 1})
                )
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type defaultdict",
            )

    def test_ruling_916_dynamic_factory_nested_refused(self):
        module = require("ontoloop.consumption")
        factory = type("DynFactory", (), {"__module__": __name__})
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                [collections.defaultdict(factory, {"k": 1})]
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type defaultdict",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                {"wrap": collections.defaultdict(factory, {"k": 1})}
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type defaultdict",
        )

    def test_ruling_916_dynamic_factory_hash_check_refused(self):
        module = require("ontoloop.consumption")
        factory = type("DynFactory", (), {"__module__": __name__})
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                collections.defaultdict(factory, {"k": 1}),
                expected_hash="0" * 64,
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type defaultdict",
        )

    def test_ruling_916_redefined_factory_forms_decide(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                collections.defaultdict(_RETAINED_FACTORY, {"k": 1})
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type defaultdict",
        )
        self.assertNotEqual(
            _digest(
                collections.defaultdict(_RedefinedFactory, {"k": 1})
            ),
            _digest(collections.defaultdict(list, {"k": 1})),
        )
        self.assertEqual(
            _digest(
                collections.defaultdict(_RedefinedFactory, {"k": 1})
            ),
            _digest(
                collections.defaultdict(_RedefinedFactory, {"k": 1})
            ),
        )

    def test_ruling_916_module_level_type_factories_still_apart(self):
        self.assertNotEqual(
            _digest(collections.defaultdict(list, {"a": 1})),
            _digest(collections.defaultdict(int, {"a": 1})),
        )
        self.assertEqual(
            _digest(collections.defaultdict(list, {"a": 1})),
            _digest(collections.defaultdict(list, {"a": 1})),
        )
        self.assertNotEqual(
            _digest(collections.defaultdict(_ModuleFactory, {"a": 1})),
            _digest(collections.defaultdict(list, {"a": 1})),
        )
        self.assertEqual(
            _digest(collections.defaultdict(_ModuleFactory, {"a": 1})),
            _digest(collections.defaultdict(_ModuleFactory, {"a": 1})),
        )

    def test_ruling_916_local_scope_factories_still_refused(self):
        module = require("ontoloop.consumption")
        first_factory = _make_local_factory()
        second_factory = _make_local_factory()
        self.assertIsNot(first_factory, second_factory)
        for factory in (first_factory, second_factory):
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check(
                    collections.defaultdict(factory, {"k": 1})
                )
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type defaultdict",
            )

    def test_ruling_916_standing_factory_forms_still_decide(self):
        module = require("ontoloop.consumption")
        self.assertNotEqual(
            _digest(collections.defaultdict(len, {"a": 1})),
            _digest(collections.defaultdict(list, {"a": 1})),
        )
        self.assertEqual(
            _digest(collections.defaultdict(None, {"a": 1})),
            _digest({"a": 1}),
        )

        def _factory():
            return 0

        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                collections.defaultdict(_factory, {"a": 1})
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type defaultdict",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                collections.defaultdict(lambda: 0, {"a": 1})
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type defaultdict",
        )


class TestConsumeFixR22ClassValueForms(unittest.TestCase):
    """Fix round 22, ruling 917: the class standing as a value.

    The class value reading states the namespace content of a
    class beside its stated names, in a governed form no two
    distinct classes share on names alone, so two distinct
    classes stating one module and one qualified name digest
    apart whatever their namespaces carry, beside classes
    carrying no namespace difference digesting in their
    standing forms.
    """

    def test_ruling_917_differing_namespace_content_apart(self):
        first = _make_colliding_class("alpha")
        second = _make_colliding_class("beta")
        self.assertIsNot(first, second)
        self.assertEqual(str(first), str(second))
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(
            _digest(first), _digest(_make_colliding_class("alpha"))
        )

    def test_ruling_917_class_with_method_namespace_apart(self):
        first = _make_method_class("alpha")
        second = _make_method_class("beta")
        self.assertEqual(str(first), str(second))
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(
            _digest(first), _digest(_make_method_class("alpha"))
        )

    def test_ruling_917_class_value_nested_apart(self):
        self.assertNotEqual(
            _digest([_make_colliding_class("alpha")]),
            _digest([_make_colliding_class("beta")]),
        )

    def test_ruling_917_class_value_as_mapping_value_apart(self):
        self.assertNotEqual(
            _digest({"wrap": _make_colliding_class("alpha")}),
            _digest({"wrap": _make_colliding_class("beta")}),
        )

    def test_ruling_917_hash_check_rejects_differing_class(self):
        module = require("ontoloop.consumption")
        expected = _digest(_make_colliding_class("alpha"))
        refused = module.load_with_hash_check(
            _make_colliding_class("beta"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _make_colliding_class("alpha"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_917_same_class_repeated_reading_equal(self):
        held = _make_colliding_class("alpha")
        self.assertEqual(_digest(held), _digest(held))
        self.assertEqual(
            _digest(_StandingClassAlpha), _digest(_StandingClassAlpha)
        )

    def test_ruling_917_differing_qualified_names_still_apart(self):
        self.assertNotEqual(
            _digest(_StandingClassAlpha), _digest(_StandingClassBeta)
        )

    def test_ruling_917_standing_value_forms_still_decide(self):
        self.assertEqual(_digest(object()), _digest(object()))

        class _Residual:
            def __init__(self, held):
                self.held = held

        self.assertNotEqual(
            _digest(_Residual("alpha")), _digest(_Residual("beta"))
        )
        self.assertEqual(
            _digest(_Residual("alpha")), _digest(_Residual("alpha"))
        )


if __name__ == "__main__":
    unittest.main()
