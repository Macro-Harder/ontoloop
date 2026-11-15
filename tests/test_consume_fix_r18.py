"""Fix round 18 tests for Region 5: consume surfaces and digest.

Written test first for the three positions charged at Round 18
triage rulings 670, 671, and 672: ruling 670 (Consume Finding 1,
the tagged digest form reading a subclass instance of a scalar
or byte like type by its intrinsic value alone, its added
instance state standing never read, with the stream limb of
ruling 620 standing in the same single channel form), ruling
671 (Consume Finding 2, the attribute limb preempting the
intrinsic content of a complex, an array, or a deque subclass
instance carrying added state), and ruling 672 (Consume
Finding 3, a string form carrying its process address in a
dress the ruling 621 pattern does not name). Each class pins
its ruling beside the standing forms its cure protects.
"""

import collections
import datetime
import decimal
import io
import re
import unittest
from array import array

from tests.harness import require


def _digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


class _IntSub(int):
    pass


class _StrSub(str):
    pass


class _FloatSub(float):
    pass


class _BytesSub(bytes):
    pass


class _BytearraySub(bytearray):
    pass


class _BytesIOSub(io.BytesIO):
    pass


class _ComplexSub(complex):
    pass


class _ArraySub(array):
    pass


class _DequeSub(collections.deque):
    pass


class _DecimalSub(decimal.Decimal):
    pass


class _NoAtProbe:
    """A value whose string form carries its address, no at wording."""

    __slots__ = ()

    def __repr__(self):
        return "<no at probe %s>" % (hex(id(self)),)


class _CapitalMarkerProbe:
    """A value whose string form carries its address, capital marker."""

    __slots__ = ()

    def __repr__(self):
        return "<capital probe at %s>" % (
            hex(id(self)).replace("0x", "0X"),
        )


class _DecimalAddressProbe:
    """A value whose string form carries its address as a decimal."""

    __slots__ = ()

    def __repr__(self):
        return "<decimal probe at %s>" % (id(self),)


class _CoveredAddressProbe:
    """A value whose string form carries its address, covered dress."""

    __slots__ = ()

    def __repr__(self):
        return "<covered probe at %s>" % (hex(id(self)),)


class TestConsumeFixR18ScalarChannels(unittest.TestCase):
    """Fix round 18, ruling 670: the scalar single channel defect.

    A subclass instance of a scalar or byte like type digests
    by its intrinsic value and its added instance content
    together, and a stream subclass instance digests by the
    content it holds and its added instance content together,
    beside plain instances of the same kinds digesting in
    their standing forms.
    """

    def test_ruling_670_int_subclass_differing_added_state_apart(self):
        first = _IntSub(5)
        first.extra = "one"
        second = _IntSub(5)
        second.extra = "two"
        twin = _IntSub(5)
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))
        self.assertNotEqual(_digest(first), _digest(5))

    def test_ruling_670_int_subclass_intrinsic_value_still_read(self):
        first = _IntSub(5)
        first.extra = "one"
        second = _IntSub(6)
        second.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_670_str_subclass_differing_added_state_apart(self):
        first = _StrSub("held text")
        first.extra = "one"
        second = _StrSub("held text")
        second.extra = "two"
        twin = _StrSub("held text")
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))
        self.assertNotEqual(_digest(first), _digest("held text"))

    def test_ruling_670_float_subclass_differing_added_state_apart(self):
        first = _FloatSub(1.5)
        first.extra = "one"
        second = _FloatSub(1.5)
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(1.5))

    def test_ruling_670_bytes_subclass_differing_added_state_apart(self):
        first = _BytesSub(b"held bytes")
        first.extra = "one"
        second = _BytesSub(b"held bytes")
        second.extra = "two"
        twin = _BytesSub(b"held bytes")
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))
        self.assertNotEqual(_digest(first), _digest(b"held bytes"))

    def test_ruling_670_bytearray_subclass_added_state_apart(self):
        first = _BytearraySub(b"held bytes")
        first.extra = "one"
        second = _BytearraySub(b"held bytes")
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(bytearray(b"held bytes")))

    def test_ruling_670_scalar_subclass_nested_added_state_read(self):
        first = _IntSub(5)
        first.extra = "one"
        second = _IntSub(5)
        second.extra = "two"
        self.assertNotEqual(_digest([first]), _digest([second]))
        self.assertNotEqual(
            _digest({"wrap": first}), _digest({"wrap": second})
        )
        text_first = _StrSub("held text")
        text_first.extra = "one"
        text_second = _StrSub("held text")
        text_second.extra = "two"
        self.assertNotEqual(_digest([text_first]), _digest([text_second]))

    def test_ruling_670_hash_check_rejects_differing_added_state(self):
        module = require("ontoloop.consumption")
        first = _IntSub(5)
        first.extra = "one"
        second = _IntSub(5)
        second.extra = "two"
        expected = _digest(first)
        refused = module.load_with_hash_check(second, expected_hash=expected)
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")
        twin = _IntSub(5)
        twin.extra = "one"
        loaded = module.load_with_hash_check(twin, expected_hash=expected)
        self.assertTrue(loaded["loaded"])

    def test_ruling_670_hash_mismatch_on_differing_added_state(self):
        module = require("ontoloop.consumption")
        first = _IntSub(5)
        first.extra = "one"
        second = _IntSub(5)
        second.extra = "two"
        apart = module.load_with_hash_mismatch(
            material=first, tool_material=second
        )
        self.assertEqual(apart["position"], "unloadable")
        twin = _IntSub(5)
        twin.extra = "one"
        alike = module.load_with_hash_mismatch(
            material=first, tool_material=twin
        )
        self.assertEqual(alike["position"], "loadable")

    def test_ruling_670_stream_subclass_added_state_read(self):
        first = _BytesIOSub(b"held content")
        first.extra = "one"
        second = _BytesIOSub(b"held content")
        second.extra = "two"
        twin = _BytesIOSub(b"held content")
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))
        self.assertNotEqual(_digest(first), _digest(io.BytesIO(b"held content")))

    def test_ruling_670_stream_content_still_decides(self):
        first = _BytesIOSub(b"content one")
        first.extra = "one"
        second = _BytesIOSub(b"content two")
        second.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(
            _digest(io.BytesIO(b"abc")), _digest(io.BytesIO(b"abd"))
        )
        self.assertEqual(
            _digest(io.BytesIO(b"abc")), _digest(io.BytesIO(b"abc"))
        )

    def test_ruling_670_plain_forms_still_digest_as_they_digest_now(self):
        self.assertEqual(_digest(_IntSub(5)), _digest(5))
        self.assertEqual(_digest(_StrSub("held text")), _digest("held text"))
        self.assertEqual(_digest(_FloatSub(1.5)), _digest(1.5))
        self.assertEqual(_digest(_BytesSub(b"held")), _digest(b"held"))
        self.assertEqual(
            _digest(_BytearraySub(b"held")), _digest(bytearray(b"held"))
        )
        self.assertEqual(_digest(b"alpha"), _digest(bytearray(b"alpha")))
        self.assertEqual(_digest(b"alpha"), _digest(memoryview(b"alpha")))


class TestConsumeFixR18AttributePreempting(unittest.TestCase):
    """Fix round 18, ruling 671: the attribute limb preempting defect.

    A complex, an array, or a deque subclass instance carrying
    added instance state digests by its intrinsic content and
    its added instance content together, beside the plain forms
    of those types digesting as they digest now and the standing
    ruling 619 forms still deciding on both channels.
    """

    def test_ruling_671_complex_subclass_intrinsic_content_read(self):
        first = _ComplexSub(1 + 2j)
        first.extra = [1]
        second = _ComplexSub(1 + 3j)
        second.extra = [1]
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_671_complex_subclass_added_state_read(self):
        first = _ComplexSub(1 + 2j)
        first.extra = [1]
        second = _ComplexSub(1 + 2j)
        second.extra = [2]
        twin = _ComplexSub(1 + 2j)
        twin.extra = [1]
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_671_complex_hash_check_rejects_differing_intrinsic(self):
        module = require("ontoloop.consumption")
        first = _ComplexSub(1 + 2j)
        first.extra = [1]
        second = _ComplexSub(1 + 3j)
        second.extra = [1]
        expected = _digest(first)
        refused = module.load_with_hash_check(second, expected_hash=expected)
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")

    def test_ruling_671_array_subclass_intrinsic_content_read(self):
        first = _ArraySub("B", b"abc")
        first.extra = "one"
        second = _ArraySub("B", b"abd")
        second.extra = "one"
        added = _ArraySub("B", b"abc")
        added.extra = "two"
        twin = _ArraySub("B", b"abc")
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(added))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_671_deque_subclass_intrinsic_content_read(self):
        first = _DequeSub([1, 2])
        first.extra = "one"
        second = _DequeSub([1, 3])
        second.extra = "one"
        added = _DequeSub([1, 2])
        added.extra = "two"
        twin = _DequeSub([1, 2])
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(added))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_671_plain_forms_still_digest_as_they_digest_now(self):
        self.assertNotEqual(_digest(1 + 2j), _digest(1 + 3j))
        self.assertNotEqual(
            _digest(array("B", b"abc")), _digest(array("B", b"abd"))
        )
        self.assertNotEqual(
            _digest(collections.deque([1, 2])),
            _digest(collections.deque([1, 3])),
        )
        bare = _DequeSub([1, 2])
        self.assertEqual(_digest(bare), _digest(_DequeSub([1, 2])))
        self.assertNotEqual(_digest(bare), _digest(_DequeSub([1, 3])))

    def test_ruling_671_ruling_619_forms_still_decide_on_both_channels(self):
        first = _DecimalSub("1.5")
        first.extra = [1]
        second = _DecimalSub("2.5")
        second.extra = [1]
        added = _DecimalSub("1.5")
        added.extra = [2]
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(added))
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )


class TestConsumeFixR18AddressStringForms(unittest.TestCase):
    """Fix round 18, ruling 672: the address bearing string form defect.

    A string form carrying its process address in any dress,
    with no at wording before it, behind a capital hex marker,
    or as a decimal number after the word at, stands refused
    at the digest surface in the governed form of ruling 621,
    beside the content bearing string forms still digesting
    by their content and the covered dress still refused.
    """

    def test_ruling_672_no_at_wording_address_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_NoAtProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _NoAtProbe",
        )

    def test_ruling_672_capital_marker_address_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_CapitalMarkerProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _CapitalMarkerProbe",
        )

    def test_ruling_672_decimal_address_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_DecimalAddressProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _DecimalAddressProbe",
        )

    def test_ruling_672_address_forms_refused_at_each_fresh_instance(self):
        module = require("ontoloop.consumption")
        for probe in (
            _NoAtProbe,
            _CapitalMarkerProbe,
            _DecimalAddressProbe,
            _CoveredAddressProbe,
        ):
            for _ in range(2):
                with self.assertRaises(ValueError) as caught:
                    module.load_with_hash_check(probe())
                self.assertEqual(
                    str(caught.exception),
                    "digest cannot read material of type "
                    + probe.__name__,
                )

    def test_ruling_672_address_form_nested_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check([_NoAtProbe()])
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _NoAtProbe",
        )
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check({"k": _DecimalAddressProbe()})
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _DecimalAddressProbe",
        )

    def test_ruling_672_covered_dress_still_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError) as caught:
            module.load_with_hash_check(_CoveredAddressProbe())
        self.assertEqual(
            str(caught.exception),
            "digest cannot read material of type _CoveredAddressProbe",
        )

    def test_ruling_672_content_bearing_string_forms_still_digest(self):
        self.assertNotEqual(_digest(range(3)), _digest(range(4)))
        self.assertNotEqual(
            _digest(re.compile("alpha")), _digest(re.compile("beta"))
        )
        self.assertNotEqual(
            _digest(decimal.Decimal("1.5")), _digest(decimal.Decimal("2.5"))
        )
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )

    def test_ruling_672_plain_object_no_content_form_stands(self):
        self.assertEqual(_digest(object()), _digest(object()))
        self.assertEqual(
            _digest({"beta", "alpha", "gamma"}),
            "e89afefd95e143b21da7c8d5ed17c7b36fa4d8640ba53ff"
            "98c1e30acc9b6d41f",
        )


if __name__ == "__main__":
    unittest.main()
