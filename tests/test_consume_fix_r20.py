"""Fix round 20 tests for Region 5: consume surfaces and digest.

Written test first for the seven positions charged at Round 20
triage rulings 786 to 792, each in the tagged digest form of
consumption.py: ruling 786 (Consume Finding 1 merged with Lead
Engineer line E-21, a string form carrying its process address
in a dress the ruling 728 refusal does not read, whole token
dresses and addresses separated into groups), ruling 787
(Consume Finding 2, slot content stored under a name mangled
storage name standing never read by the residual content
reading), ruling 788 (Consume Finding 3 merged with Lead
Engineer line E-20, a member of an enum mixing in bytes
carrying added state digesting by its byte content alone),
ruling 789 (Consume Finding 4, the default factory of a
defaultdict standing in no channel of the mapping kind),
ruling 790 (Consume Finding 5, a function carrying an added
attribute digesting over that attribute alone, the attribute
reading preempting the governed refusal its plain form stands
under), ruling 791 (Consume Finding 6, the filename channel
of an OSError standing outside the argument tuple the ruling
727 kind reads), and ruling 792 (Consume Finding 7, the cause
and context channels of an exception standing in no channel
of any digest form). Each class pins its ruling beside the
standing forms its cure protects.
"""

import collections
import datetime
import decimal
import enum
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


class _SpaceDecProbe:
    __slots__ = ()

    def __repr__(self):
        return "space probe %s" % (id(self),)


class _ParenDecProbe:
    __slots__ = ()

    def __repr__(self):
        return "(paren probe %s)" % (id(self),)


class _EqualsDecProbe:
    __slots__ = ()

    def __repr__(self):
        return "equals probe=%s" % (id(self),)


class _ColonAttachedProbe:
    __slots__ = ()

    def __repr__(self):
        return "colon probe:%s" % (id(self),)


class _ColonSpaceProbe:
    __slots__ = ()

    def __repr__(self):
        return "colon probe: %s" % (id(self),)


class _HashAttachedProbe:
    __slots__ = ()

    def __repr__(self):
        return "hash probe#%s" % (id(self),)


class _HexSpaceProbe:
    __slots__ = ()

    def __repr__(self):
        return "hex probe %s" % (format(id(self), "x"),)


class _AtCapitalProbe:
    __slots__ = ()

    def __repr__(self):
        return "at probe AT %s" % (id(self),)


class _BracketAttachedProbe:
    __slots__ = ()

    def __repr__(self):
        return "bracket probe[%s]" % (id(self),)


class _SemicolonProbe:
    __slots__ = ()

    def __repr__(self):
        return "semi probe; %s" % (id(self),)


class _SlashProbe:
    __slots__ = ()

    def __repr__(self):
        return "slash probe/%s" % (id(self),)


class _AtColonProbe:
    __slots__ = ()

    def __repr__(self):
        return "words probe at: %s" % (id(self),)


class _IdEqualsProbe:
    __slots__ = ()

    def __repr__(self):
        return "words probe id=%s" % (id(self),)


class _HeadDecProbe:
    __slots__ = ()

    def __repr__(self):
        return "%s head probe" % (id(self),)


class _GroupedCommaProbe:
    __slots__ = ()

    def __repr__(self):
        return "grouped probe %s" % (format(id(self), ","),)


class _GroupedUnderscoreProbe:
    __slots__ = ()

    def __repr__(self):
        return "grouped probe %s" % (format(id(self), "_"),)


class _GroupedStopProbe:
    __slots__ = ()

    def __repr__(self):
        return "grouped probe %s" % (
            format(id(self), ",").replace(",", "."),
        )


class _HexParenProbe:
    __slots__ = ()

    def __repr__(self):
        return "(hex probe %s)" % (format(id(self), "x"),)


class _HexHyphenPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), "-"),)


class _HexDotPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), "."),)


class _HexSpacePairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), " "),)


class _HexSlashPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), "/"),)


class _HexColonPairsProbe:
    __slots__ = ()

    def __repr__(self):
        return "pairs probe %s" % (_hex_pairs(id(self), ":"),)


class _HexUnderscoreFoursProbe:
    __slots__ = ()

    def __repr__(self):
        return "fours probe %s" % (_hex_fours(id(self), "_"),)


class _HexUnderscoreHeadProbe:
    __slots__ = ()

    def __repr__(self):
        return "head probe _%s" % (format(id(self), "x"),)


class _DecHyphenGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), "-"),)


class _DecSpaceGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), " "),)


class _DecApostropheGroupsProbe:
    __slots__ = ()

    def __repr__(self):
        return "groups probe %s" % (_decimal_groups(id(self), "'"),)


class _DecSpaceAtProbe:
    __slots__ = ()

    def __repr__(self):
        return "at probe at %s" % (_decimal_groups(id(self), " "),)


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


class _PrivateSlots:
    __slots__ = ("__hidden", "shown")

    def __init__(self, hidden, shown):
        self.__hidden = hidden
        self.shown = shown


class _PrivateSlotAlone:
    __slots__ = ("__hidden",)

    def __init__(self, hidden):
        self.__hidden = hidden


class _PrivateBase:
    __slots__ = ("__secret",)

    def __init__(self, secret):
        self.__secret = secret


class _PrivateChild(_PrivateBase):
    __slots__ = ("shown",)

    def __init__(self, secret, shown):
        super().__init__(secret)
        self.shown = shown


class _SingleUnderscoreSlots:
    __slots__ = ("_hidden",)

    def __init__(self, hidden):
        self._hidden = hidden


class _ValueErrorSub(ValueError):
    pass


class _PrivateSlotError(ValueError):
    __slots__ = ("__hidden",)

    def __init__(self, argument, hidden):
        super().__init__(argument)
        self.__hidden = hidden


class _BytesEnum(bytes, enum.Enum):
    A = b"held"
    B = b"kept"


class _IntEnum(enum.IntEnum):
    A = 5
    B = 6


class _PlainEnum(enum.Enum):
    P = "plainval"
    Q = "other"


def _function_one():
    return 1


def _function_two():
    return 2


def _caused(argument, cause_argument):
    error = ValueError(argument)
    error.__cause__ = ValueError(cause_argument)
    return error


def _contexted(argument, context_argument):
    try:
        raise RuntimeError(context_argument)
    except RuntimeError:
        try:
            raise ValueError(argument)
        except ValueError as error:
            return error


class TestConsumeFixR20AddressStringForms(unittest.TestCase):
    """Fix round 20, ruling 786: the address bearing string form.

    A string form carrying its process address in a whole token
    dress outside the ruling 728 alternatives, or separated
    into groups, stands refused at the digest surface in the
    governed form of ruling 621, beside the content bearing
    string forms still digesting by their content and the
    bounded short forms still standing.
    """

    _WHOLE = (
        _SpaceDecProbe,
        _ParenDecProbe,
        _EqualsDecProbe,
        _ColonAttachedProbe,
        _ColonSpaceProbe,
        _HashAttachedProbe,
        _HexSpaceProbe,
        _AtCapitalProbe,
        _BracketAttachedProbe,
        _SemicolonProbe,
        _SlashProbe,
        _AtColonProbe,
        _IdEqualsProbe,
        _HeadDecProbe,
        _GroupedCommaProbe,
        _GroupedUnderscoreProbe,
        _GroupedStopProbe,
        _HexParenProbe,
    )

    _SEPARATED = (
        _HexHyphenPairsProbe,
        _HexDotPairsProbe,
        _HexSpacePairsProbe,
        _HexSlashPairsProbe,
        _HexColonPairsProbe,
        _HexUnderscoreFoursProbe,
        _HexUnderscoreHeadProbe,
        _DecHyphenGroupsProbe,
        _DecSpaceGroupsProbe,
        _DecApostropheGroupsProbe,
        _DecSpaceAtProbe,
    )

    def test_ruling_786_each_whole_token_dress_refused(self):
        module = require("ontoloop.consumption")
        for probe in self._WHOLE:
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

    def test_ruling_786_each_separated_group_dress_refused(self):
        module = require("ontoloop.consumption")
        for probe in self._SEPARATED:
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

    def test_ruling_786_address_dress_nested_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check([_SpaceDecProbe()])
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _SpaceDecProbe",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check({"k": _HexHyphenPairsProbe()})
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _HexHyphenPairsProbe",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check([_DecSpaceGroupsProbe()])
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _DecSpaceGroupsProbe",
        )

    def test_ruling_786_hash_check_on_fresh_instance_refused(self):
        module = require("ontoloop.consumption")
        first, second = _SpaceDecProbe(), _SpaceDecProbe()
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(first)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _SpaceDecProbe",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                second, expected_hash="0" * 64
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _SpaceDecProbe",
        )
        held_first, held_second = (
            _HexHyphenPairsProbe(),
            _HexHyphenPairsProbe(),
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(
                held_second, expected_hash="0" * 64
            )
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _HexHyphenPairsProbe",
        )
        self.assertIsNotNone(held_first)

    def test_ruling_786_covered_and_r19_dresses_still_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_CoveredAddressProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _CoveredAddressProbe",
        )

    def test_ruling_786_content_bearing_string_forms_still_digest(self):
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

    def test_ruling_786_short_forms_and_no_content_form_stand(self):
        short_one = _ShortNumberProbe("<short probe at 123>")
        short_two = _ShortNumberProbe("<short probe at 124>")
        self.assertNotEqual(_digest(short_one), _digest(short_two))
        self.assertEqual(
            _digest(_ShortNumberProbe("<short probe at 123>")),
            _digest(short_one),
        )
        self.assertEqual(_digest(object()), _digest(object()))
        self.assertEqual(
            _digest({"beta", "alpha", "gamma"}),
            "e89afefd95e143b21da7c8d5ed17c7b36fa4d8640ba53ff"
            "98c1e30acc9b6d41f",
        )


class TestConsumeFixR20MangledSlotContent(unittest.TestCase):
    """Fix round 20, ruling 787: the name mangled slot content.

    Slot content stored under a name mangled storage name
    stands read by the residual content reading, so material
    differing in that content alone digests apart, beside the
    standing slot and attribute forms still deciding.
    """

    def test_ruling_787_private_slot_content_read(self):
        self.assertNotEqual(
            _digest(_PrivateSlots("alpha", "x")),
            _digest(_PrivateSlots("beta", "x")),
        )
        self.assertEqual(
            _digest(_PrivateSlots("alpha", "x")),
            _digest(_PrivateSlots("alpha", "x")),
        )
        self.assertNotEqual(
            _digest(_PrivateSlots("alpha", "x")),
            _digest(_PrivateSlots("alpha", "y")),
        )

    def test_ruling_787_private_slot_alone_read(self):
        module = require("ontoloop.consumption")
        mapping = module._residual_content_mapping(
            _PrivateSlotAlone("alpha")
        )
        self.assertIsNotNone(mapping)
        self.assertNotEqual(
            _digest(_PrivateSlotAlone("alpha")),
            _digest(_PrivateSlotAlone("beta")),
        )

    def test_ruling_787_private_slot_nested_and_mapping_value_read(self):
        self.assertNotEqual(
            _digest([_PrivateSlots("alpha", "x")]),
            _digest([_PrivateSlots("beta", "x")]),
        )
        self.assertNotEqual(
            _digest({"wrap": _PrivateSlots("alpha", "x")}),
            _digest({"wrap": _PrivateSlots("beta", "x")}),
        )

    def test_ruling_787_private_slot_inherited_read(self):
        self.assertNotEqual(
            _digest(_PrivateChild("alpha", "x")),
            _digest(_PrivateChild("beta", "x")),
        )
        self.assertEqual(
            _digest(_PrivateChild("alpha", "x")),
            _digest(_PrivateChild("alpha", "x")),
        )

    def test_ruling_787_private_slot_on_exception_subclass_read(self):
        first = _PrivateSlotError("arg", "alpha")
        first.extra = "x"
        second = _PrivateSlotError("arg", "beta")
        second.extra = "x"
        twin = _PrivateSlotError("arg", "alpha")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_787_hash_check_rejects_differing_hidden_content(self):
        module = require("ontoloop.consumption")
        expected = _digest(_PrivateSlots("alpha", "x"))
        refused = module.load_with_hash_check(
            _PrivateSlots("beta", "x"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _PrivateSlots("alpha", "x"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_787_standing_slot_forms_still_decide(self):
        self.assertNotEqual(
            _digest(_SingleUnderscoreSlots("alpha")),
            _digest(_SingleUnderscoreSlots("beta")),
        )

        class _PlainSlots:
            __slots__ = ("held",)

            def __init__(self, held):
                self.held = held

        self.assertNotEqual(
            _digest(_PlainSlots("alpha")), _digest(_PlainSlots("beta"))
        )


class TestConsumeFixR20BytesEnumChannels(unittest.TestCase):
    """Fix round 20, ruling 788: the bytes mixed in enum member.

    A member of an enum mixing in bytes carrying added state
    digests by its byte content and its added state together,
    beside a member carrying no added state digesting in its
    standing form and the ruling 729 forms still deciding.
    """

    def test_ruling_788_bytes_enum_differing_added_state_apart(self):
        member = _BytesEnum.A
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

    def test_ruling_788_bytes_enum_hash_check_rejects_differing_state(self):
        module = require("ontoloop.consumption")
        member = _BytesEnum.A
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

    def test_ruling_788_bytes_enum_no_added_state_standing_form(self):
        self.assertEqual(_digest(_BytesEnum.A), _digest(_BytesEnum.A))
        self.assertNotEqual(_digest(_BytesEnum.A), _digest(_BytesEnum.B))
        member = _BytesEnum.A
        try:
            standing = _digest(member)
            member.extra = "one"
            self.assertNotEqual(_digest(member), standing)
        finally:
            if "extra" in vars(member):
                del member.extra

    def test_ruling_788_bytes_enum_nested_added_state_read(self):
        member = _BytesEnum.A
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

    def test_ruling_788_ruling_729_and_plain_enum_forms_still_decide(self):
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
        plain = _PlainEnum.P
        try:
            plain.extra = "one"
            plain_first = _digest(plain)
            plain.extra = "two"
            plain_second = _digest(plain)
        finally:
            if "extra" in vars(plain):
                del plain.extra
        self.assertNotEqual(plain_first, plain_second)

    def test_ruling_788_tuple_and_complex_mixed_enum_controls_apart(self):
        class _TupleEnum(tuple, enum.Enum):
            A = (1, 2)

        class _ComplexEnum(complex, enum.Enum):
            A = 1 + 2j

        for member in (_TupleEnum.A, _ComplexEnum.A):
            try:
                member.extra = "one"
                first = _digest(member)
                member.extra = "two"
                second = _digest(member)
            finally:
                if "extra" in vars(member):
                    del member.extra
            self.assertNotEqual(first, second)


class TestConsumeFixR20DefaultFactory(unittest.TestCase):
    """Fix round 20, ruling 789: the defaultdict factory channel.

    The mapping kind states the default factory of a
    defaultdict beside its entries, so two mappings differing
    in their factory alone digest apart, beside mappings
    carrying no factory digesting in their standing forms,
    and a factory no governed form states standing under the
    governed refusal.
    """

    def test_ruling_789_differing_factory_alone_apart(self):
        first = collections.defaultdict(list, {"a": 1})
        second = collections.defaultdict(int, {"a": 1})
        twin = collections.defaultdict(list, {"a": 1})
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_789_factory_read_nested(self):
        self.assertNotEqual(
            _digest([collections.defaultdict(list, {"a": 1})]),
            _digest([collections.defaultdict(int, {"a": 1})]),
        )
        self.assertNotEqual(
            _digest({"wrap": collections.defaultdict(list, {"a": 1})}),
            _digest({"wrap": collections.defaultdict(int, {"a": 1})}),
        )

    def test_ruling_789_subclass_pair_differing_factory_apart(self):
        class _DDSub(collections.defaultdict):
            pass

        first = _DDSub(list, {"a": 1})
        first.extra = "x"
        second = _DDSub(int, {"a": 1})
        second.extra = "x"
        twin = _DDSub(list, {"a": 1})
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_789_hash_check_rejects_differing_factory(self):
        module = require("ontoloop.consumption")
        expected = _digest(collections.defaultdict(list, {"a": 1}))
        refused = module.load_with_hash_check(
            collections.defaultdict(int, {"a": 1}),
            expected_hash=expected,
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            collections.defaultdict(list, {"a": 1}),
            expected_hash=expected,
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_789_no_factory_forms_stand(self):
        self.assertEqual(
            _digest(collections.defaultdict(None, {"a": 1})),
            _digest({"a": 1}),
        )
        self.assertNotEqual(
            _digest(collections.defaultdict(list, {"a": 1})),
            _digest(collections.defaultdict(list, {"a": 2})),
        )
        self.assertNotEqual(_digest({"a": 1}), _digest({"a": 2}))

    def test_ruling_789_factory_with_no_governed_form_refused(self):
        module = require("ontoloop.consumption")

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


class TestConsumeFixR20FunctionAttributePreemption(unittest.TestCase):
    """Fix round 20, ruling 790: the function attribute defect.

    A function carrying an added attribute stands under the
    governed refusal its plain form stands under, beside the
    standing attribute bearing forms of the other families
    still digesting as they digest.
    """

    def test_ruling_790_function_with_attribute_refused(self):
        module = require("ontoloop.consumption")
        _function_one.extra = "x"
        try:
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check(_function_one)
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type function",
            )
        finally:
            del _function_one.extra

    def test_ruling_790_two_functions_same_attribute_never_equal(self):
        module = require("ontoloop.consumption")
        _function_one.extra = "x"
        _function_two.extra = "x"
        try:
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check(_function_one)
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type function",
            )
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check(_function_two)
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type function",
            )
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check(
                    _function_two,
                    expected_hash="0" * 64,
                )
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type function",
            )
        finally:
            del _function_one.extra
            del _function_two.extra

    def test_ruling_790_function_differing_defaults_refused(self):
        module = require("ontoloop.consumption")

        def _with_default(value=1):
            return value

        _with_default.extra = "x"
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_with_default)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type function",
        )

        def _with_default(value=2):
            return value

        _with_default.extra = "x"
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_with_default)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type function",
        )

    def test_ruling_790_function_nested_with_attribute_refused(self):
        module = require("ontoloop.consumption")
        _function_one.extra = "x"
        try:
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check([_function_one])
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type function",
            )
            with self.assertRaises(ValueError) as caught:
                module.load_with_hash_check({"k": _function_one})
            self.assertEqual(
                str(caught.exception),
                "digest cannot read material of type function",
            )
        finally:
            del _function_one.extra

    def test_ruling_790_plain_function_and_iterator_guard_stand(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_function_one)
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type function",
        )

        class _IteratorWithAttribute:
            def __init__(self):
                self.extra = "x"

            def __iter__(self):
                return self

            def __next__(self):
                raise StopIteration

        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_IteratorWithAttribute())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _IteratorWithAttribute",
        )

    def test_ruling_790_standing_attribute_forms_still_digest(self):
        class _Residual:
            def __init__(self, held):
                self.held = held

        self.assertNotEqual(
            _digest(_Residual("alpha")), _digest(_Residual("beta"))
        )
        self.assertEqual(
            _digest(_Residual("alpha")), _digest(_Residual("alpha"))
        )


class TestConsumeFixR20OSErrorFilename(unittest.TestCase):
    """Fix round 20, ruling 791: the OSError filename channel.

    The exception kind reading states the filename channel of
    an OSError beside its argument content and its added
    state, so two materials differing in any of those channels
    digest apart, beside the ruling 727 forms still deciding.
    """

    def test_ruling_791_oserror_differing_filename_with_state_apart(self):
        first = OSError(2, "msg", "file_a")
        first.extra = "x"
        second = OSError(2, "msg", "file_b")
        second.extra = "x"
        twin = OSError(2, "msg", "file_a")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_791_oserror_filename_and_argument_channels_apart(self):
        first = OSError(2, "msg", "file_a")
        first.extra = "x"
        other_argument = OSError(3, "msg", "file_a")
        other_argument.extra = "x"
        other_state = OSError(2, "msg", "file_a")
        other_state.extra = "y"
        self.assertNotEqual(_digest(first), _digest(other_argument))
        self.assertNotEqual(_digest(first), _digest(other_state))

    def test_ruling_791_oserror_filename_nested_read(self):
        first = OSError(2, "msg", "file_a")
        first.extra = "x"
        second = OSError(2, "msg", "file_b")
        second.extra = "x"
        self.assertNotEqual(_digest([first]), _digest([second]))

    def test_ruling_791_hash_check_rejects_differing_filename(self):
        module = require("ontoloop.consumption")
        first = OSError(2, "msg", "file_a")
        first.extra = "x"
        second = OSError(2, "msg", "file_b")
        second.extra = "x"
        expected = _digest(first)
        refused = module.load_with_hash_check(
            second, expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")

    def test_ruling_791_plain_oserror_and_ruling_727_forms_stand(self):
        self.assertNotEqual(
            _digest(OSError(2, "msg", "file_a")),
            _digest(OSError(2, "msg", "file_b")),
        )
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("beta")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))


class TestConsumeFixR20ExceptionChaining(unittest.TestCase):
    """Fix round 20, ruling 792: the exception chaining channels.

    The digest forms state the cause and context channels of
    an exception beside its argument content and its added
    state, in a governed form that terminates on a chain
    standing in a cycle, so two exceptions differing in their
    chaining alone digest apart, in the plain form and in the
    added state form alike.
    """

    def test_ruling_792_differing_cause_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_caused("main", "cause_a")),
            _digest(_caused("main", "cause_b")),
        )
        self.assertEqual(
            _digest(_caused("main", "cause_a")),
            _digest(_caused("main", "cause_a")),
        )
        self.assertNotEqual(
            _digest(_caused("main", "cause_a")),
            _digest(ValueError("main")),
        )

    def test_ruling_792_differing_context_alone_apart_plain(self):
        self.assertNotEqual(
            _digest(_contexted("main", "ctx_a")),
            _digest(_contexted("main", "ctx_b")),
        )
        self.assertEqual(
            _digest(_contexted("main", "ctx_a")),
            _digest(_contexted("main", "ctx_a")),
        )
        self.assertNotEqual(
            _digest(_contexted("main", "ctx_a")),
            _digest(ValueError("main")),
        )

    def test_ruling_792_differing_cause_with_added_state_apart(self):
        first = _caused("main", "cause_a")
        first.extra = "x"
        second = _caused("main", "cause_b")
        second.extra = "x"
        twin = _caused("main", "cause_a")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_792_differing_context_with_added_state_apart(self):
        first = _contexted("main", "ctx_a")
        first.extra = "x"
        second = _contexted("main", "ctx_b")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_792_hash_check_rejects_differing_cause(self):
        module = require("ontoloop.consumption")
        expected = _digest(_caused("main", "cause_a"))
        refused = module.load_with_hash_check(
            _caused("main", "cause_b"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        loaded = module.load_with_hash_check(
            _caused("main", "cause_a"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])

    def test_ruling_792_chained_form_nested_read(self):
        self.assertNotEqual(
            _digest([_caused("main", "cause_a")]),
            _digest([_caused("main", "cause_b")]),
        )

    def test_ruling_792_chain_cycle_terminates_in_governed_form(self):
        module = require("ontoloop.consumption")
        first = ValueError("first")
        second = ValueError("second")
        first.__cause__ = second
        second.__cause__ = first
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(first)
        self.assertEqual(
            str(caught.exception),
            "cyclic value in canonical form",
        )

    def test_ruling_792_unchained_and_ruling_727_forms_stand(self):
        self.assertNotEqual(
            _digest(ValueError("alpha")), _digest(ValueError("beta"))
        )
        self.assertEqual(
            _digest(ValueError("alpha")), _digest(ValueError("alpha"))
        )
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("beta")
        second.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))


if __name__ == "__main__":
    unittest.main()
