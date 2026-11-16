"""Fix round 21 tests for Region 5: consume surfaces and digest.

Written test first for the eight positions charged at Round 21
triage rulings 850 to 857, each in the tagged digest form of
consumption.py: ruling 850 (Consume Finding 1, an address stated
in groups separated by a character standing outside the
separator sets of the ruling 786 cure), ruling 851 (Consume
Finding 2, private slot content standing in a base class whose
stated slot name a subclass states again), ruling 852 (Consume
Finding 3, a functools.partial carrying an added attribute),
ruling 853 (Consume Finding 4, the suppression flag channel of
an exception), ruling 854 (Consume Finding 5, the name and path
channels of an ImportError), ruling 855 (Consume Finding 6, the
position and text channels of a SyntaxError), ruling 856
(Consume Finding 7, two distinct defaultdict factory types
stating one module and one qualified name), and ruling 857
(Lead Engineer line E-32, a member of a bytearray mixed in enum
read by its intrinsic value alone). Each class pins its ruling
beside the standing forms its cure protects.
"""

import collections
import datetime
import decimal
import enum
import functools
import re
import unittest

from tests.harness import require


def _digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


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


def _decimal_groups(value, separator):
    return format(value, ",").replace(",", separator)


class _DecTabGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), "\t"),)


class _DecColonGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), ":"),)


class _DecSemicolonGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), ";"),)


class _DecSlashGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), "/"),)


class _DecNewlineGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), "\n"),)


class _HexCommaPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), ","),)


class _HexSemicolonPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), ";"),)


class _HexTabPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), "\t"),)


class _HexCommaFoursProbe:
    __slots__ = ()

    def __repr__(self):
        return "fours probe %s" % (_hex_fours(id(self), ","),)


class _DecSpaceGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), " "),)


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


class _ShadowMid(_ShadowBase):
    __slots__ = ("__hidden",)

    def __init__(self, base_hidden, mid_hidden, shown):
        super().__init__(base_hidden, shown)
        self.__hidden = mid_hidden


class _ShadowLeaf(_ShadowMid):
    __slots__ = ("__hidden",)

    def __init__(self, base_hidden, mid_hidden, leaf_hidden, shown):
        super().__init__(base_hidden, mid_hidden, shown)
        self.__hidden = leaf_hidden


class _PrivateSlots:
    __slots__ = ("__hidden", "shown")

    def __init__(self, hidden, shown):
        self.__hidden = hidden
        self.shown = shown


class _ValueErrorSub(ValueError):
    pass


def _function_one(value):
    return value + 1


def _function_two(value):
    return value - 1


def _suppressed(argument, context_argument, from_none):
    try:
        raise KeyError(context_argument)
    except KeyError:
        if from_none:
            try:
                raise ValueError(argument) from None
            except ValueError as error:
                return error
        try:
            raise ValueError(argument)
        except ValueError as error:
            return error


def _import_error(name, path, message="no module"):
    return ImportError(message, name=name, path=path)


def _syntax_assigned(text="source text a", offset=5, filename="file_a.py",
                     lineno=3, end_lineno=3, end_offset=9):
    error = SyntaxError("bad thing")
    error.filename = filename
    error.lineno = lineno
    error.offset = offset
    error.text = text
    error.end_lineno = end_lineno
    error.end_offset = end_offset
    return error


def _make_local_factory():
    class _CollidingFactory:
        pass

    return _CollidingFactory


class _ModuleFactory:
    pass


class _BytearrayEnum(bytearray, enum.Enum):
    A = b"held"
    B = b"kept"


class _BytesEnum(bytes, enum.Enum):
    A = b"held"
    B = b"kept"


class TestConsumeFixR21AddressSeparatorForms(unittest.TestCase):
    """Fix round 21, ruling 850: the group separator character.

    An address stated in groups separated by a character
    standing outside the separator sets of the ruling 786 cure
    stands refused at the digest surface in the governed form
    of that cure, beside the content bearing string forms
    still digesting by their content and the ruling 786 forms
    still deciding as they decide.
    """

    _DRESSES = (
        _DecTabGroupsProbe,
        _DecColonGroupsProbe,
        _DecSemicolonGroupsProbe,
        _DecSlashGroupsProbe,
        _DecNewlineGroupsProbe,
        _HexCommaPairsProbe,
        _HexSemicolonPairsProbe,
        _HexTabPairsProbe,
    )

    def test_ruling_850_each_new_separator_dress_refused(self):
        module = require("ontoloop.consumption")
        for probe in self._DRESSES:
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

    def test_ruling_850_new_dress_nested_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check([_DecTabGroupsProbe()])
        with self.assertRaises(ValueError):
            module.load_with_hash_check({"k": _HexCommaPairsProbe()})

    def test_ruling_850_hash_check_on_fresh_instance_refused(self):
        module = require("ontoloop.consumption")
        held_first, held_second = (
            _DecColonGroupsProbe(),
            _DecColonGroupsProbe(),
        )
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                held_second, expected_hash="0" * 64
            )
        self.assertIsNotNone(held_first)

    def test_ruling_850_hex_fours_new_separator_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_HexCommaFoursProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _HexCommaFoursProbe",
        )

    def test_ruling_850_content_bearing_string_forms_still_digest(self):
        self.assertNotEqual(_digest(range(3)), _digest(range(4)))
        self.assertNotEqual(
            _digest(re.compile("alpha")), _digest(re.compile("beta"))
        )
        self.assertNotEqual(
            _digest(decimal.Decimal("1.5")),
            _digest(decimal.Decimal("2.5")),
        )
        self.assertNotEqual(
            _digest(decimal.Decimal("123456789012")),
            _digest(decimal.Decimal("123456789013")),
        )
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )
        self.assertNotEqual(
            _digest(datetime.datetime(2026, 1, 1, 12, 30, 15)),
            _digest(datetime.datetime(2027, 1, 1, 12, 30, 15)),
        )

    def test_ruling_850_ruling_786_forms_still_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check(_DecSpaceGroupsProbe())
        with self.assertRaises(ValueError):
            module.load_with_hash_check(_CoveredAddressProbe())

    def test_ruling_850_short_forms_and_no_content_form_stand(self):
        short_one = _ShortNumberProbe("<short probe at 123>")
        short_two = _ShortNumberProbe("<short probe at 124>")
        self.assertNotEqual(_digest(short_one), _digest(short_two))
        self.assertEqual(
            _digest(_ShortNumberProbe("<short probe at 123>")),
            _digest(short_one),
        )
        self.assertEqual(_digest(object()), _digest(object()))


class TestConsumeFixR21ShadowedPrivateSlot(unittest.TestCase):
    """Fix round 21, ruling 851: the shadowed private slot.

    Private slot content standing in a base class whose stated
    slot name a subclass states again stands read by the
    residual content reading under the storage name of its
    stating class, so material differing in that content alone
    digests apart, beside the ruling 787 forms still deciding.
    """

    def test_ruling_851_shadowed_base_slot_content_read(self):
        self.assertNotEqual(
            _digest(_ShadowSub("base_a", "sub", "s")),
            _digest(_ShadowSub("base_b", "sub", "s")),
        )
        self.assertEqual(
            _digest(_ShadowSub("base_a", "sub", "s")),
            _digest(_ShadowSub("base_a", "sub", "s")),
        )

    def test_ruling_851_residual_mapping_carries_both_slots(self):
        module = require("ontoloop.consumption")
        mapping = module._residual_content_mapping(
            _ShadowSub("base_a", "sub", "s")
        )
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping["__hidden"], "sub")
        self.assertEqual(mapping["_ShadowBase__hidden"], "base_a")
        self.assertEqual(mapping["shown"], "s")

    def test_ruling_851_shadowed_slot_nested_and_mapping_value_read(self):
        self.assertNotEqual(
            _digest([_ShadowSub("base_a", "sub", "s")]),
            _digest([_ShadowSub("base_b", "sub", "s")]),
        )
        self.assertNotEqual(
            _digest({"wrap": _ShadowSub("base_a", "sub", "s")}),
            _digest({"wrap": _ShadowSub("base_b", "sub", "s")}),
        )

    def test_ruling_851_hash_check_rejects_differing_base_content(self):
        module = require("ontoloop.consumption")
        expected = _digest(_ShadowSub("base_a", "sub", "s"))
        refused = module.load_with_hash_check(
            _ShadowSub("base_b", "sub", "s"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _ShadowSub("base_a", "sub", "s"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_851_three_level_shadowing_read(self):
        self.assertNotEqual(
            _digest(_ShadowLeaf("base_a", "mid", "leaf", "s")),
            _digest(_ShadowLeaf("base_b", "mid", "leaf", "s")),
        )
        self.assertNotEqual(
            _digest(_ShadowLeaf("base_a", "mid", "leaf", "s")),
            _digest(_ShadowLeaf("base_a", "mid2", "leaf", "s")),
        )

    def test_ruling_851_standing_slot_forms_still_decide(self):
        self.assertNotEqual(
            _digest(_ShadowSub("base_a", "sub_a", "s")),
            _digest(_ShadowSub("base_a", "sub_b", "s")),
        )
        self.assertNotEqual(
            _digest(_PrivateSlots("alpha", "x")),
            _digest(_PrivateSlots("beta", "x")),
        )
        self.assertEqual(
            _digest(_PrivateSlots("alpha", "x")),
            _digest(_PrivateSlots("alpha", "x")),
        )


class TestConsumeFixR21PartialAttribute(unittest.TestCase):
    """Fix round 21, ruling 852: the partial attribute defect.

    A functools.partial carrying an added attribute stands
    under the governed refusal its plain form stands under,
    beside the standing attribute bearing forms of the other
    families still digesting as they digest and the ruling
    790 forms still deciding as they decide.
    """

    def test_ruling_852_partial_with_attribute_refused(self):
        module = require("ontoloop.consumption")
        partial = functools.partial(_function_one, 1)
        partial.tag = "same"
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(partial)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type partial",
        )

    def test_ruling_852_two_partials_same_attribute_never_equal(self):
        module = require("ontoloop.consumption")
        first = functools.partial(_function_one, 1)
        first.tag = "same"
        second = functools.partial(_function_two, 9)
        second.tag = "same"
        with self.assertRaises(ValueError):
            module.load_with_hash_check(first)
        with self.assertRaises(ValueError):
            module.load_with_hash_check(second)
        with self.assertRaises(ValueError):
            module.load_with_hash_check(second, expected_hash="0" * 64)

    def test_ruling_852_partial_differing_keywords_refused(self):
        module = require("ontoloop.consumption")

        def _with_keyword(value, scale=1):
            return value * scale

        first = functools.partial(_with_keyword, 1, scale=2)
        first.tag = "same"
        second = functools.partial(_with_keyword, 1, scale=3)
        second.tag = "same"
        with self.assertRaises(ValueError):
            module.load_with_hash_check(first)
        with self.assertRaises(ValueError):
            module.load_with_hash_check(second)

    def test_ruling_852_partial_nested_with_attribute_refused(self):
        module = require("ontoloop.consumption")
        partial = functools.partial(_function_one, 1)
        partial.tag = "same"
        with self.assertRaises(ValueError):
            module.load_with_hash_check([partial])
        with self.assertRaises(ValueError):
            module.load_with_hash_check({"k": partial})

    def test_ruling_852_plain_partial_and_function_forms_stand(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                functools.partial(_function_one, 1)
            )
        with self.assertRaises(ValueError):
            module.load_with_hash_check(_function_one)
        _function_one.extra = "x"
        try:
            with self.assertRaises(ValueError):
                module.load_with_hash_check(_function_one)
        finally:
            del _function_one.extra

    def test_ruling_852_standing_attribute_forms_still_digest(self):
        class _Residual:
            def __init__(self, held):
                self.held = held

        self.assertNotEqual(
            _digest(_Residual("alpha")), _digest(_Residual("beta"))
        )
        self.assertEqual(
            _digest(_Residual("alpha")), _digest(_Residual("alpha"))
        )


class TestConsumeFixR21SuppressionChannel(unittest.TestCase):
    """Fix round 21, ruling 853: the suppression flag channel.

    The digest forms state the suppression flag channel of an
    exception beside its argument content and its added state,
    so two exceptions differing in their suppression alone
    digest apart, in the plain form and in the added state
    form alike, beside the ruling 792 forms still deciding.
    """

    def test_ruling_853_differing_suppression_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_suppressed("main", "ctx", False)),
            _digest(_suppressed("main", "ctx", True)),
        )
        self.assertEqual(
            _digest(_suppressed("main", "ctx", True)),
            _digest(_suppressed("main", "ctx", True)),
        )
        self.assertNotEqual(
            _digest(_suppressed("main", "ctx", True)),
            _digest(ValueError("main")),
        )

    def test_ruling_853_differing_suppression_with_added_state_apart(self):
        first = _suppressed("main", "ctx", False)
        first.extra = "x"
        second = _suppressed("main", "ctx", True)
        second.extra = "x"
        twin = _suppressed("main", "ctx", False)
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_853_suppression_nested_read(self):
        self.assertNotEqual(
            _digest([_suppressed("main", "ctx", False)]),
            _digest([_suppressed("main", "ctx", True)]),
        )
        self.assertNotEqual(
            _digest({"wrap": _suppressed("main", "ctx", False)}),
            _digest({"wrap": _suppressed("main", "ctx", True)}),
        )

    def test_ruling_853_hash_check_rejects_differing_suppression(self):
        module = require("ontoloop.consumption")
        expected = _digest(_suppressed("main", "ctx", False))
        refused = module.load_with_hash_check(
            _suppressed("main", "ctx", True), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _suppressed("main", "ctx", False), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_853_suppress_flag_without_context_apart(self):
        flagged = ValueError("main")
        flagged.__suppress_context__ = True
        twin = ValueError("main")
        twin.__suppress_context__ = True
        self.assertNotEqual(_digest(flagged), _digest(ValueError("main")))
        self.assertEqual(_digest(flagged), _digest(twin))

    def test_ruling_853_ruling_792_and_727_forms_stand(self):
        caused = ValueError("main")
        caused.__cause__ = ValueError("cause_a")
        other_caused = ValueError("main")
        other_caused.__cause__ = ValueError("cause_b")
        self.assertNotEqual(_digest(caused), _digest(other_caused))
        self.assertNotEqual(
            _digest(ValueError("alpha")), _digest(ValueError("beta"))
        )
        self.assertEqual(
            _digest(ValueError("alpha")), _digest(ValueError("alpha"))
        )


class TestConsumeFixR21ImportErrorChannels(unittest.TestCase):
    """Fix round 21, ruling 854: the ImportError channels.

    The exception kind reading states the name and path
    channels of an ImportError beside its argument content
    and its added state, so two materials differing in any of
    those channels digest apart, in the plain form and in the
    added state form alike.
    """

    def test_ruling_854_differing_name_and_path_apart_plain(self):
        self.assertNotEqual(
            _digest(_import_error("mod_a", "/p/a")),
            _digest(_import_error("mod_b", "/p/a")),
        )
        self.assertNotEqual(
            _digest(_import_error("mod_a", "/p/a")),
            _digest(_import_error("mod_a", "/p/b")),
        )
        self.assertEqual(
            _digest(_import_error("mod_a", "/p/a")),
            _digest(_import_error("mod_a", "/p/a")),
        )

    def test_ruling_854_differing_name_with_added_state_apart(self):
        first = _import_error("mod_a", "/p/a")
        first.extra = "x"
        second = _import_error("mod_b", "/p/a")
        second.extra = "x"
        third = _import_error("mod_a", "/p/b")
        third.extra = "x"
        twin = _import_error("mod_a", "/p/a")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(third))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_854_import_error_nested_read(self):
        self.assertNotEqual(
            _digest([_import_error("mod_a", "/p/a")]),
            _digest([_import_error("mod_b", "/p/a")]),
        )
        self.assertNotEqual(
            _digest({"wrap": _import_error("mod_a", "/p/a")}),
            _digest({"wrap": _import_error("mod_a", "/p/b")}),
        )

    def test_ruling_854_hash_check_rejects_differing_name(self):
        module = require("ontoloop.consumption")
        expected = _digest(_import_error("mod_a", "/p/a"))
        refused = module.load_with_hash_check(
            _import_error("mod_b", "/p/a"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _import_error("mod_a", "/p/a"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_854_module_not_found_subclass_channels_read(self):
        self.assertNotEqual(
            _digest(ModuleNotFoundError("m", name="mod_a", path="/p/a")),
            _digest(ModuleNotFoundError("m", name="mod_b", path="/p/a")),
        )
        self.assertNotEqual(
            _digest(ModuleNotFoundError("m", name="mod_a", path="/p/a")),
            _digest(ModuleNotFoundError("m", name="mod_a", path="/p/b")),
        )

    def test_ruling_854_ruling_791_and_727_forms_stand(self):
        first = OSError(2, "msg", "file_a")
        first.extra = "x"
        second = OSError(2, "msg", "file_b")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        sub_first = _ValueErrorSub("alpha")
        sub_first.extra = "x"
        sub_second = _ValueErrorSub("beta")
        sub_second.extra = "x"
        self.assertNotEqual(_digest(sub_first), _digest(sub_second))
        self.assertNotEqual(
            _digest(_import_error("mod_a", "/p/a", "message_a")),
            _digest(_import_error("mod_a", "/p/a", "message_b")),
        )


class TestConsumeFixR21SyntaxErrorChannels(unittest.TestCase):
    """Fix round 21, ruling 855: the SyntaxError channels.

    The exception kind reading states the position and text
    channels of a SyntaxError beside its argument content and
    its added state, in the plain form and in the added state
    form alike, so two materials differing in any of those
    channels digest apart.
    """

    def test_ruling_855_differing_text_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_syntax_assigned(text="source text a")),
            _digest(_syntax_assigned(text="source text b")),
        )
        self.assertEqual(
            _digest(_syntax_assigned(text="source text a")),
            _digest(_syntax_assigned(text="source text a")),
        )

    def test_ruling_855_differing_positions_apart_plain(self):
        self.assertNotEqual(
            _digest(_syntax_assigned(offset=5)),
            _digest(_syntax_assigned(offset=8)),
        )
        self.assertNotEqual(
            _digest(_syntax_assigned(end_offset=9)),
            _digest(_syntax_assigned(end_offset=12)),
        )
        self.assertNotEqual(
            _digest(_syntax_assigned(end_lineno=3)),
            _digest(_syntax_assigned(end_lineno=4)),
        )
        self.assertNotEqual(
            _digest(_syntax_assigned(lineno=3)),
            _digest(_syntax_assigned(lineno=7)),
        )

    def test_ruling_855_differing_filename_with_added_state_apart(self):
        first = _syntax_assigned(filename="file_a.py", lineno=3)
        first.extra = "x"
        second = _syntax_assigned(filename="file_b.py", lineno=3)
        second.extra = "x"
        third = _syntax_assigned(filename="file_a.py", lineno=7)
        third.extra = "x"
        twin = _syntax_assigned(filename="file_a.py", lineno=3)
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(third))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_855_differing_text_with_added_state_apart(self):
        first = _syntax_assigned(text="source text a")
        first.extra = "x"
        second = _syntax_assigned(text="source text b")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_855_syntax_error_nested_read(self):
        self.assertNotEqual(
            _digest([_syntax_assigned(text="source text a")]),
            _digest([_syntax_assigned(text="source text b")]),
        )
        self.assertNotEqual(
            _digest({"wrap": _syntax_assigned(offset=5)}),
            _digest({"wrap": _syntax_assigned(offset=8)}),
        )

    def test_ruling_855_hash_check_rejects_differing_text(self):
        module = require("ontoloop.consumption")
        expected = _digest(_syntax_assigned(text="source text a"))
        refused = module.load_with_hash_check(
            _syntax_assigned(text="source text b"),
            expected_hash=expected,
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _syntax_assigned(text="source text a"),
            expected_hash=expected,
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_855_constructor_form_channels_read(self):
        first = SyntaxError(
            "bad thing", ("file_a.py", 3, 5, "source text a", 3, 9)
        )
        second = SyntaxError(
            "bad thing", ("file_a.py", 3, 5, "source text b", 3, 9)
        )
        third = SyntaxError(
            "bad thing", ("file_a.py", 3, 8, "source text a", 3, 9)
        )
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(third))

    def test_ruling_855_ruling_791_and_727_forms_stand(self):
        self.assertNotEqual(
            _digest(OSError(2, "msg", "file_a")),
            _digest(OSError(2, "msg", "file_b")),
        )
        sub_first = _ValueErrorSub("alpha")
        sub_first.extra = "x"
        sub_second = _ValueErrorSub("beta")
        sub_second.extra = "x"
        self.assertNotEqual(_digest(sub_first), _digest(sub_second))
        self.assertNotEqual(
            _digest(_syntax_assigned()),
            _digest(SyntaxError("other thing")),
        )


class TestConsumeFixR21FactoryTokenCollision(unittest.TestCase):
    """Fix round 21, ruling 856: the factory token collision.

    Two distinct defaultdict factory types stating one module
    and one qualified name stand under the governed refusal
    for the digest act, their name form stating no distinction
    between them, beside the module level type factories and
    the builtin callable factories still deciding as they
    decide and the ruling 789 forms still standing.
    """

    def test_ruling_856_colliding_local_factories_refused(self):
        module = require("ontoloop.consumption")
        first_factory = _make_local_factory()
        second_factory = _make_local_factory()
        self.assertIsNot(first_factory, second_factory)
        self.assertEqual(
            first_factory.__module__ + "." + first_factory.__qualname__,
            second_factory.__module__ + "." + second_factory.__qualname__,
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

    def test_ruling_856_colliding_factory_nested_refused(self):
        module = require("ontoloop.consumption")
        factory = _make_local_factory()
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                [collections.defaultdict(factory, {"k": 1})]
            )
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                {"wrap": collections.defaultdict(factory, {"k": 1})}
            )

    def test_ruling_856_colliding_factory_hash_check_refused(self):
        module = require("ontoloop.consumption")
        factory = _make_local_factory()
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                collections.defaultdict(factory, {"k": 1}),
                expected_hash="0" * 64,
            )

    def test_ruling_856_module_level_type_factories_still_apart(self):
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

    def test_ruling_856_builtin_callable_factory_stands(self):
        self.assertNotEqual(
            _digest(collections.defaultdict(len, {"a": 1})),
            _digest(collections.defaultdict(list, {"a": 1})),
        )
        self.assertEqual(
            _digest(collections.defaultdict(len, {"a": 1})),
            _digest(collections.defaultdict(len, {"a": 1})),
        )

    def test_ruling_856_no_governed_form_factories_still_refused(self):
        module = require("ontoloop.consumption")

        def _factory():
            return 0

        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                collections.defaultdict(_factory, {"a": 1})
            )
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                collections.defaultdict(lambda: 0, {"a": 1})
            )
        self.assertEqual(
            _digest(collections.defaultdict(None, {"a": 1})),
            _digest({"a": 1}),
        )


class TestConsumeFixR21BytearrayEnumMember(unittest.TestCase):
    """Fix round 21, ruling 857: the bytearray mixed in member.

    A member of a bytearray mixed in enum carrying differing
    added state digests apart across its states, through the
    enum kind beside the bytes form of ruling 788, beside a
    member carrying no added state digesting in its standing
    form and the ruling 729 forms still deciding.
    """

    def test_ruling_857_bytearray_enum_differing_added_state_apart(self):
        member = _BytearrayEnum.A
        try:
            member.extra = "one"
            first = _digest(member)
            member.extra = "two"
            second = _digest(member)
            member.extra = "one"
            twin = _digest(member)
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertEqual(first, twin)

    def test_ruling_857_bytearray_enum_hash_check_rejects_state(self):
        module = require("ontoloop.consumption")
        member = _BytearrayEnum.A
        try:
            member.extra = "one"
            expected = _digest(member)
            member.extra = "two"
            refused = module.load_with_hash_check(
                member, expected_hash=expected
            )
            self.assertFalse(refused["loaded"])
            self.assertEqual(refused["position"], "unloadable")
            member.extra = "one"
            loaded = module.load_with_hash_check(
                member, expected_hash=expected
            )
            self.assertTrue(loaded["loaded"])
        finally:
            if "extra" in vars(member):
                del member.extra

    def test_ruling_857_bytearray_enum_no_added_state_standing_form(self):
        self.assertEqual(
            _digest(_BytearrayEnum.A), _digest(_BytearrayEnum.A)
        )
        self.assertNotEqual(
            _digest(_BytearrayEnum.A), _digest(_BytearrayEnum.B)
        )
        member = _BytearrayEnum.A
        try:
            standing = _digest(member)
            member.extra = "one"
            self.assertNotEqual(_digest(member), standing)
        finally:
            if "extra" in vars(member):
                del member.extra

    def test_ruling_857_bytearray_enum_nested_added_state_read(self):
        member = _BytearrayEnum.A
        try:
            member.extra = "one"
            first = _digest([member])
            first_map = _digest({"wrap": member})
            member.extra = "two"
            second = _digest([member])
            second_map = _digest({"wrap": member})
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertNotEqual(first_map, second_map)

    def test_ruling_857_bytes_enum_form_of_ruling_788_stands(self):
        member = _BytesEnum.A
        try:
            member.extra = "one"
            first = _digest(member)
            member.extra = "two"
            second = _digest(member)
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertNotEqual(_digest(_BytesEnum.A), _digest(_BytesEnum.B))

    def test_ruling_857_ruling_729_mixed_enum_forms_stand(self):
        class _IntEnum(enum.IntEnum):
            A = 5
            B = 6

        member = _IntEnum.A
        try:
            member.extra = "one"
            first = _digest(member)
            member.extra = "two"
            second = _digest(member)
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertEqual(_digest(_IntEnum.A), _digest(5))

        class _StrEnum(str, enum.Enum):
            Y = "held"
            Z = "kept"

        str_member = _StrEnum.Y
        try:
            str_member.extra = "one"
            str_first = _digest(str_member)
            str_member.extra = "two"
            str_second = _digest(str_member)
        finally:
            if "extra" in vars(str_member):
                del str_member.extra
        self.assertNotEqual(str_first, str_second)


if __name__ == "__main__":
    unittest.main()
