"""Fix round 23 tests for Region 4: the service layer digest pair.

Written test first for the one position charged at Round 23
triage ruling 968, the merged defect at the R23-CHAIR-1
identity: the duplicated digest pair in
ontoloop/service_layer.py, at _residual_content_mapping,
_tagged_digest_form, and _ingest_material_digest behind
ingest_tool, has drifted from the consumption encoding in
ontoloop/consumption.py, so the service layer ingest and
verify pair does not round trip on material the consumption
encoding reads in its cured forms. The pins cover the six
Chair forms (the AttributeError name channel form of ruling
913, the NameError name channel form of ruling 914, the
exception group subexception form of ruling 915, the class
value namespace form of ruling 917, the shadowed slot form
of ruling 912, and the defaultdict factory form of ruling
916), the two Consume and surfaces corroborating forms
counted inside the Chair position (an exception carrying a
differing cause with an ImportError whose path channel
differs, and an exception carrying an added note), and each
merged Lead Engineer candidate form E-44 to E-49 (E-44, the
address bearing string reading in both separator widths,
the ruling 850 and ruling 911 forms; E-45, the shadowed
private slot reading, the ruling 851 form; E-46, the
exception suppression flag channel, the ruling 853 form;
E-47, the ImportError name and path channels, the ruling
854 form; E-48, the SyntaxError position and text channels,
the ruling 855 form; and E-49, the bytearray mixed in enum
member added state reading, the ruling 857 form). Each pin
asks that the service layer digest stands at parity with
the consumption digest on the same material, that two
materials differing in a named channel digest apart at
ingest, and that verify_tool returns loaded True on the
ingest digest of each readable form. No pin of this file
touches consumption.py, which stands as the parity
reference in read only form.
"""

import collections
import enum
import unittest

from tests.harness import require


def _service():
    return require("ontoloop.service_layer")


def _ingest(material):
    return _service().ingest_tool(material)["material_digest"]


def _consume_digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


def _assert_parity(test_case, material):
    digest = _ingest(material)
    test_case.assertEqual(digest, _consume_digest(material))
    loaded = _service().verify_tool(material, expected_hash=digest)
    test_case.assertTrue(loaded["loaded"])
    return digest


def _assert_apart(test_case, first, second):
    first_digest = _assert_parity(test_case, first)
    second_digest = _assert_parity(test_case, second)
    test_case.assertNotEqual(first_digest, second_digest)
    test_case.assertNotEqual(
        _consume_digest(first), _consume_digest(second)
    )


def _attribute_error(name, obj, message="missing attribute"):
    return AttributeError(message, name=name, obj=obj)


def _name_error(name, message="name is not defined"):
    return NameError(message, name=name)


class _PlainSlotBase:
    __slots__ = ("x",)

    def __init__(self, base_value):
        _PlainSlotBase.__dict__["x"].__set__(self, base_value)


class _PlainSlotSub(_PlainSlotBase):
    __slots__ = ("x",)

    def __init__(self, base_value, sub_value):
        super().__init__(base_value)
        _PlainSlotSub.__dict__["x"].__set__(self, sub_value)


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


def _make_colliding_class(value):
    class _CollidingClass:
        held = value

    return _CollidingClass


def _decimal_groups(value, separator):
    return format(value, ",").replace(",", separator)


class _DecCommaSpaceProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), ", "),
        )


class _DecTabProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (
            _decimal_groups(id(self), "\t"),
        )


class _BytearrayEnum(bytearray, enum.Enum):
    A = b"held"
    B = b"kept"


def _suppressed_error(suppress):
    try:
        try:
            raise KeyError("inner")
        except KeyError:
            raise ValueError("outer")
    except ValueError as error:
        error.__suppress_context__ = suppress
        return error


def _caused_error(cause):
    error = ValueError("main")
    error.__cause__ = cause
    return error


class TestServiceFixR23ChairForms(unittest.TestCase):
    """Ruling 968, the six Chair forms of R23-CHAIR-1."""

    def test_chair_913_attribute_error_name_channel_apart(self):
        _assert_apart(
            self,
            _attribute_error("attr_a", "thing"),
            _attribute_error("attr_b", "thing"),
        )

    def test_chair_913_attribute_error_object_channel_apart(self):
        _assert_apart(
            self,
            _attribute_error("attr", "thing_a"),
            _attribute_error("attr", "thing_b"),
        )

    def test_chair_914_name_error_name_channel_apart(self):
        _assert_apart(
            self,
            _name_error("name_a"),
            _name_error("name_b"),
        )

    def test_chair_915_exception_group_subexception_apart(self):
        _assert_apart(
            self,
            BaseExceptionGroup("grp", [ValueError("a")]),
            BaseExceptionGroup("grp", [ValueError("b")]),
        )

    def test_chair_915_exception_group_subexception_type_apart(self):
        _assert_apart(
            self,
            ExceptionGroup("grp", [ValueError("a")]),
            ExceptionGroup("grp", [KeyError("a")]),
        )

    def test_chair_917_class_value_namespace_apart(self):
        _assert_apart(
            self,
            _make_colliding_class("alpha"),
            _make_colliding_class("beta"),
        )

    def test_chair_912_shadowed_slot_base_content_apart(self):
        _assert_apart(
            self,
            _PlainSlotSub("base_a", "sub"),
            _PlainSlotSub("base_b", "sub"),
        )

    def test_chair_916_defaultdict_factory_apart(self):
        _assert_apart(
            self,
            collections.defaultdict(list, {"k": 1}),
            collections.defaultdict(dict, {"k": 1}),
        )

    def test_chair_914_name_error_nested_parity(self):
        material = {"wrap": [_name_error("name_a")]}
        self.assertEqual(_ingest(material), _ingest(material))
        _assert_parity(self, material)
        _assert_apart(
            self,
            {"wrap": [_name_error("name_a")]},
            {"wrap": [_name_error("name_b")]},
        )

    def test_chair_916_defaultdict_not_plain_mapping(self):
        digest = _assert_parity(
            self, collections.defaultdict(list, {"k": 1})
        )
        plain = _assert_parity(self, {"k": 1})
        self.assertNotEqual(digest, plain)


class TestServiceFixR23ConsumeCorroboratingForms(unittest.TestCase):
    """Ruling 968, the two Consume corroborating forms."""

    def test_consume_differing_cause_apart(self):
        _assert_apart(
            self,
            _caused_error(ValueError("cause_a")),
            _caused_error(ValueError("cause_b")),
        )

    def test_consume_cause_import_error_path_channel_apart(self):
        _assert_apart(
            self,
            _caused_error(
                ImportError("m", name="mod", path="/p/a.py")
            ),
            _caused_error(
                ImportError("m", name="mod", path="/p/b.py")
            ),
        )

    def test_consume_added_note_apart_and_round_trip(self):
        noted = ValueError("main")
        noted.add_note("a note standing here")
        plain = ValueError("main")
        _assert_apart(self, noted, plain)
        other = ValueError("main")
        other.add_note("a differing note standing here")
        _assert_apart(self, noted, other)


class TestServiceFixR23LeadEngineerForms(unittest.TestCase):
    """Ruling 968, the merged candidate forms E-44 to E-49."""

    def test_e44_address_sequence_width_refused_at_ingest(self):
        service = _service()
        consumption = require("ontoloop.consumption")
        probe = _DecCommaSpaceProbe()
        with self.assertRaises(ValueError) as caught:
            consumption.load_with_hash_check(probe)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecCommaSpaceProbe",
        )
        with self.assertRaises(ValueError) as caught:
            service.ingest_tool(probe)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecCommaSpaceProbe",
        )

    def test_e44_address_single_separator_width_refused(self):
        service = _service()
        consumption = require("ontoloop.consumption")
        probe = _DecTabProbe()
        with self.assertRaises(ValueError) as caught:
            consumption.load_with_hash_check(probe)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecTabProbe",
        )
        with self.assertRaises(ValueError) as caught:
            service.ingest_tool(probe)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecTabProbe",
        )
        with self.assertRaises(ValueError) as caught:
            service.verify_tool(probe, expected_hash="0" * 64)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type "
            "_DecTabProbe",
        )

    def test_e45_shadowed_private_slot_apart(self):
        _assert_apart(
            self,
            _ShadowSub("base_a", "sub", "s"),
            _ShadowSub("base_b", "sub", "s"),
        )

    def test_e46_suppression_flag_channel_apart(self):
        _assert_apart(
            self,
            _suppressed_error(True),
            _suppressed_error(False),
        )

    def test_e47_import_error_name_channel_apart(self):
        _assert_apart(
            self,
            ImportError("m", name="mod_a", path="/p/a.py"),
            ImportError("m", name="mod_b", path="/p/a.py"),
        )

    def test_e47_import_error_path_channel_apart(self):
        _assert_apart(
            self,
            ImportError("m", name="mod", path="/p/a.py"),
            ImportError("m", name="mod", path="/p/b.py"),
        )

    def test_e48_syntax_error_text_channel_apart(self):
        _assert_apart(
            self,
            SyntaxError("bad", ("f.py", 1, 2, "line one")),
            SyntaxError("bad", ("f.py", 1, 2, "line two")),
        )

    def test_e48_syntax_error_position_channel_apart(self):
        _assert_apart(
            self,
            SyntaxError("bad", ("f.py", 1, 2, "line one")),
            SyntaxError("bad", ("f.py", 1, 9, "line one")),
        )

    def test_e49_bytearray_enum_added_state_apart(self):
        member = _BytearrayEnum.A
        try:
            member.extra = "one"
            first = _ingest(member)
            self.assertEqual(first, _consume_digest(member))
            member.extra = "two"
            second = _ingest(member)
            self.assertEqual(second, _consume_digest(member))
            self.assertNotEqual(first, second)
            loaded = _service().verify_tool(
                member, expected_hash=second
            )
            self.assertTrue(loaded["loaded"])
        finally:
            if "extra" in vars(member):
                del member.extra


class TestServiceFixR23Controls(unittest.TestCase):
    """Ruling 968 controls: plain material still round trips."""

    def test_plain_material_round_trips_in_full(self):
        class _PlainObject:
            def __init__(self):
                self.held = "value"

        class _SlottedObject:
            __slots__ = ("held",)

            def __init__(self):
                self.held = "value"

        for material in (
            {"k": [1, 2, 3]},
            "a plain string",
            [1, "two", 3.0],
            (1, 2),
            {1, 2, 3},
            _PlainObject(),
            _SlottedObject(),
            ValueError("plain"),
            None,
            42,
        ):
            _assert_parity(self, material)


if __name__ == "__main__":
    unittest.main()
