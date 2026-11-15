"""Fix round 19 tests for Region 5: consume surfaces and digest.

Written test first for the three positions charged at Round 19
triage rulings 727, 728, and 729: ruling 727 (Consume Finding 1,
the attribute limb of the tagged digest encoding preempting the
argument content of an exception subclass instance carrying
added state), ruling 728 (Consume Finding 2, a string form
carrying its process address in a dress none of the three
alternatives of the ruling 672 address refusal names), and
ruling 729 (Lead Engineer line E-9, the digest shortcut limbs
reading a mixed in enum member by its intrinsic value alone).
Each class pins its ruling beside the standing forms its cure
protects.
"""

import collections
import datetime
import decimal
import enum
import fractions
import re
import unittest
from array import array

from tests.harness import require


def _digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


class _ValueErrorSub(ValueError):
    pass


class _ExceptionSub(Exception):
    pass


class _ComplexSub(complex):
    pass


class _DecimalSub(decimal.Decimal):
    pass


class _FractionSub(fractions.Fraction):
    pass


class _IntSub(int):
    pass


class _DecNoAtProbe:
    """A value stating its address as a decimal, no at wording."""

    __slots__ = ()

    def __repr__(self):
        return "<dec no at probe %s>" % (id(self),)


class _HexNoMarkerProbe:
    """A value stating its address as hex, no marker, no at wording."""

    __slots__ = ()

    def __repr__(self):
        return "<hex no marker probe %s>" % (format(id(self), "x"),)


class _HashDecProbe:
    """A value stating its decimal address behind a hash sign."""

    __slots__ = ()

    def __repr__(self):
        return "<hash probe #%s>" % (id(self),)


class _ColonDecProbe:
    """A value stating its decimal address behind a colon."""

    __slots__ = ()

    def __repr__(self):
        return "<colon probe: %s>" % (id(self),)


class _BracketDecProbe:
    """A value stating its decimal address inside brackets."""

    __slots__ = ()

    def __repr__(self):
        return "<bracket probe [%s]>" % (id(self),)


class _AtCapitalDecProbe:
    """A value stating its decimal address behind a capital At."""

    __slots__ = ()

    def __repr__(self):
        return "<at probe At %s>" % (id(self),)


class _GroupedAtProbe:
    """A value stating its address grouped with commas after at."""

    __slots__ = ()

    def __repr__(self):
        return "<grouped probe at %s>" % (format(id(self), ","),)


class _CoveredAddressProbe:
    """A value stating its address in the covered ruling 672 dress."""

    __slots__ = ()

    def __repr__(self):
        return "<covered probe at %s>" % (hex(id(self)),)


class _ShortNumberProbe:
    """A value stating a short number after the word at."""

    __slots__ = ("_text",)

    def __init__(self, text):
        self._text = text

    def __repr__(self):
        return self._text


class TestConsumeFixR19ExceptionChannels(unittest.TestCase):
    """Fix round 19, ruling 727: the exception argument content defect.

    An exception subclass instance carrying added instance state
    digests by its argument content and its added instance
    content together, beside the plain exception forms still
    digesting by their argument content and the standing ruling
    619 and ruling 671 forms still deciding on both channels.
    """

    def test_ruling_727_exception_subclass_argument_content_read(self):
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("beta")
        second.extra = "x"
        twin = _ValueErrorSub("alpha")
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_727_exception_subclass_added_state_still_read(self):
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("alpha")
        second.extra = "y"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(_ValueErrorSub("alpha")))

    def test_ruling_727_exception_subclass_nested_argument_read(self):
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("beta")
        second.extra = "x"
        self.assertNotEqual(_digest([first]), _digest([second]))
        self.assertNotEqual(
            _digest({"wrap": first}), _digest({"wrap": second})
        )

    def test_ruling_727_base_exception_subclass_argument_pairs_read(self):
        first = _ExceptionSub(1, 2)
        first.extra = "x"
        second = _ExceptionSub(1, 3)
        second.extra = "x"
        twin = _ExceptionSub(1, 2)
        twin.extra = "x"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_727_hash_check_rejects_differing_argument_content(self):
        module = require("ontoloop.consumption")
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("beta")
        second.extra = "x"
        expected = _digest(first)
        refused = module.load_with_hash_check(second, expected_hash=expected)
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        twin = _ValueErrorSub("alpha")
        twin.extra = "x"
        loaded = module.load_with_hash_check(twin, expected_hash=expected)
        self.assertTrue(loaded["loaded"])

    def test_ruling_727_hash_mismatch_on_differing_argument_content(self):
        module = require("ontoloop.consumption")
        first = _ValueErrorSub("alpha")
        first.extra = "x"
        second = _ValueErrorSub("beta")
        second.extra = "x"
        apart = module.load_with_hash_mismatch(
            material=first, tool_material=second
        )
        self.assertEqual(apart["position"], "unloadable")
        twin = _ValueErrorSub("alpha")
        twin.extra = "x"
        alike = module.load_with_hash_mismatch(
            material=first, tool_material=twin
        )
        self.assertEqual(alike["position"], "loadable")

    def test_ruling_727_plain_exception_forms_still_digest_by_arguments(self):
        self.assertNotEqual(
            _digest(ValueError("alpha")), _digest(ValueError("beta"))
        )
        self.assertNotEqual(
            _digest(_ValueErrorSub("alpha")), _digest(_ValueErrorSub("beta"))
        )
        self.assertEqual(
            _digest(_ValueErrorSub("alpha")), _digest(_ValueErrorSub("alpha"))
        )
        self.assertNotEqual(
            _digest(_ValueErrorSub("alpha")), _digest(_ValueErrorSub("beta"))
        )

    def test_ruling_727_ruling_619_and_671_forms_still_decide(self):
        frac_first = _FractionSub(1, 2)
        frac_first.extra = [1]
        frac_second = _FractionSub(1, 3)
        frac_second.extra = [1]
        frac_added = _FractionSub(1, 2)
        frac_added.extra = [2]
        self.assertNotEqual(_digest(frac_first), _digest(frac_second))
        self.assertNotEqual(_digest(frac_first), _digest(frac_added))
        dec_first = _DecimalSub("1.5")
        dec_first.extra = [1]
        dec_second = _DecimalSub("2.5")
        dec_second.extra = [1]
        self.assertNotEqual(_digest(dec_first), _digest(dec_second))
        comp_first = _ComplexSub(1 + 2j)
        comp_first.extra = [1]
        comp_second = _ComplexSub(1 + 3j)
        comp_second.extra = [1]
        self.assertNotEqual(_digest(comp_first), _digest(comp_second))
        self.assertNotEqual(
            _digest(array("B", b"abc")), _digest(array("B", b"abd"))
        )
        self.assertNotEqual(
            _digest(collections.deque([1, 2])),
            _digest(collections.deque([1, 3])),
        )


class TestConsumeFixR19AddressStringForms(unittest.TestCase):
    """Fix round 19, ruling 728: the address bearing string form defect.

    A string form carrying its process address in a dress none
    of the three alternatives of the ruling 672 refusal names,
    a decimal address with no at wording, a hex address with no
    hex marker and no at wording, a decimal address behind a
    hash sign, a colon, brackets, or a capital At, and a decimal
    address grouped with commas after the word at, stands
    refused at the digest surface in the governed form of ruling
    621, beside the content bearing string forms still digesting
    by their content and the covered dress still refused.
    """

    _DRESSES = (
        _DecNoAtProbe,
        _HexNoMarkerProbe,
        _HashDecProbe,
        _ColonDecProbe,
        _BracketDecProbe,
        _AtCapitalDecProbe,
        _GroupedAtProbe,
    )

    def test_ruling_728_each_uncovered_dress_refused(self):
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

    def test_ruling_728_decimal_no_at_wording_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_DecNoAtProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _DecNoAtProbe",
        )

    def test_ruling_728_hex_no_marker_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_HexNoMarkerProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _HexNoMarkerProbe",
        )

    def test_ruling_728_introducer_dresses_refused(self):
        module = require("ontoloop.consumption")
        for probe in (
            _HashDecProbe,
            _ColonDecProbe,
            _BracketDecProbe,
            _AtCapitalDecProbe,
        ):
            with self.assertRaises(ValueError, msg=probe.__name__):
                module.load_with_hash_check(probe())

    def test_ruling_728_grouped_commas_after_at_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_GroupedAtProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _GroupedAtProbe",
        )

    def test_ruling_728_uncovered_dress_nested_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check([_DecNoAtProbe()])
        with self.assertRaises(ValueError):
            module.load_with_hash_check({"k": _HexNoMarkerProbe()})
        with self.assertRaises(ValueError):
            module.load_with_hash_check([_GroupedAtProbe()])

    def test_ruling_728_covered_dress_still_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_CoveredAddressProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _CoveredAddressProbe",
        )

    def test_ruling_728_content_bearing_string_forms_still_digest(self):
        self.assertNotEqual(_digest(range(3)), _digest(range(4)))
        self.assertNotEqual(
            _digest(re.compile("alpha")), _digest(re.compile("beta"))
        )
        self.assertNotEqual(
            _digest(decimal.Decimal("1.5")), _digest(decimal.Decimal("2.5"))
        )
        self.assertNotEqual(
            _digest(decimal.Decimal("123456789012")),
            _digest(decimal.Decimal("123456789013")),
        )
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )

    def test_ruling_728_short_forms_and_no_content_form_stand(self):
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


class TestConsumeFixR19MixedEnumChannels(unittest.TestCase):
    """Fix round 19, ruling 729: the mixed in enum member shortcut defect.

    A member of an int, float, or str enum carrying differing
    added state digests apart across its states, through a form
    carrying its added state beside its intrinsic value, beside
    a member carrying no added state digesting in its standing
    form, beside the plain enum member still digesting apart
    across its states, and beside the scalar and container forms
    of ruling 670 still digesting apart on differing added state.
    """

    def test_ruling_729_int_enum_differing_added_state_apart(self):
        class _IE(enum.IntEnum):
            A = 5
            B = 6

        member = _IE.A
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

    def test_ruling_729_int_enum_hash_check_rejects_differing_state(self):
        module = require("ontoloop.consumption")

        class _IE(enum.IntEnum):
            A = 5

        member = _IE.A
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

    def test_ruling_729_int_enum_no_added_state_standing_form(self):
        class _IE(enum.IntEnum):
            A = 5
            B = 6

        self.assertEqual(_digest(_IE.A), _digest(5))
        self.assertNotEqual(_digest(_IE.A), _digest(_IE.B))

    def test_ruling_729_float_enum_differing_added_state_apart(self):
        class _FE(float, enum.Enum):
            X = 1.5
            Y = 2.5

        member = _FE.X
        try:
            standing = _digest(member)
            member.extra = "one"
            first = _digest(member)
            member.extra = "two"
            second = _digest(member)
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, standing)
        self.assertNotEqual(standing, _digest(1.5))
        self.assertEqual(standing, _digest(_FE.X))
        self.assertNotEqual(_digest(_FE.X), _digest(_FE.Y))

    def test_ruling_729_str_enum_differing_added_state_apart(self):
        class _SE(str, enum.Enum):
            Y = "held"
            Z = "kept"

        member = _SE.Y
        try:
            standing = _digest(member)
            member.extra = "one"
            first = _digest(member)
            member.extra = "two"
            second = _digest(member)
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, standing)
        self.assertNotEqual(standing, _digest("held"))
        self.assertEqual(standing, _digest(_SE.Y))
        self.assertNotEqual(_digest(_SE.Y), _digest(_SE.Z))

    def test_ruling_729_mixed_enum_nested_added_state_read(self):
        class _IE(enum.IntEnum):
            A = 5

        member = _IE.A
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

    def test_ruling_729_plain_enum_member_still_apart_across_states(self):
        class _PE(enum.Enum):
            P = "plainval"
            Q = "other"

        member = _PE.P
        try:
            standing = _digest(member)
            member.extra = "one"
            first = _digest(member)
            member.extra = "two"
            second = _digest(member)
        finally:
            if "extra" in vars(member):
                del member.extra
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, standing)
        self.assertNotEqual(_digest(_PE.P), _digest(_PE.Q))

    def test_ruling_729_ruling_670_forms_still_decide(self):
        first = _IntSub(5)
        first.extra = "one"
        second = _IntSub(5)
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(_IntSub(5)), _digest(5))

        class _TupleSub(tuple):
            pass

        tup_first = _TupleSub((1, 2))
        tup_first.extra = "one"
        tup_second = _TupleSub((1, 2))
        tup_second.extra = "two"
        self.assertNotEqual(_digest(tup_first), _digest(tup_second))
        self.assertNotEqual(
            _digest(collections.deque([1, 2])),
            _digest(collections.deque([1, 3])),
        )


if __name__ == "__main__":
    unittest.main()
