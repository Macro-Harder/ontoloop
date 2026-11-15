"""Fix round 17 tests for Region 5: consume surfaces and digest.

Written test first for the four positions charged at Round 17
triage rulings 618, 619, 620, and 621: ruling 618 (Consume
Finding 1, a bundle recorded as the value None reading back at
discover as the no promotion answer), ruling 619 (Consume
Finding 2, the tagged digest form reading a subclass instance
through one channel only), ruling 620 (Consume Finding 3, a
content bearing value digesting under its type name alone),
and ruling 621 (Consume Finding 4, a generator digesting over
a string form carrying its process address). Each class pins
its ruling beside the standing forms its cure protects.
"""

import collections
import datetime
import decimal
import hashlib
import io
import os
import re
import tempfile
import unittest
from array import array

from tests.harness import require


def _digest(material):
    module = require("ontoloop.consumption")
    return module.load_with_hash_check(material)["computed_hash"]


class _DictSub(dict):
    pass


class _ListSub(list):
    pass


class _SetSub(set):
    pass


class _FrozenSub(frozenset):
    pass


class _TupleSub(tuple):
    pass


class _DecimalSub(decimal.Decimal):
    pass


class _DateSub(datetime.date):
    pass


class _ResidualProbe:
    """A residual value whose string form states no content."""

    def __init__(self, held):
        self.held = held

    def __str__(self):
        return "residual probe"


class _AddressReprProbe:
    """A value whose representation carries a process address.

    The probe carries no instance state, so its only channel
    at the digest surface stands as its string form.
    """

    __slots__ = ()

    ADDRESS = "0x1234abcd"

    def __repr__(self):
        return "<address repr probe at %s>" % (type(self).ADDRESS,)


class _AddressReprProbeSecond(_AddressReprProbe):
    ADDRESS = "0x5678ef90"


class TestConsumeFixR17DiscoverNoneBundle(unittest.TestCase):
    """Fix round 17, ruling 618: the recorded None bundle reading.

    A bundle recorded as the value None reads back at discover
    as the promotion answer carrying the None bundle, standing
    apart from the no promotion answer for a workflow that was
    never recorded, beside the falsy bundle forms still reading
    back as promotions.
    """

    def test_ruling_618_recorded_none_bundle_discovers_as_promotion(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion("r17 618 none workflow", None)
        self.assertTrue(recorded["recorded"])
        self.assertIsNone(recorded["bundle"])
        found = module.discover("r17 618 none workflow")
        self.assertEqual(found["answer"], "promotion")
        self.assertFalse(found["is_error"])
        self.assertIsNone(found["bundle"])

    def test_ruling_618_never_recorded_workflow_still_no_promotion(self):
        module = require("ontoloop.consumption")
        found = module.discover("r17 618 never recorded workflow")
        self.assertEqual(found["answer"], "no promotion")
        self.assertFalse(found["is_error"])
        self.assertIsNone(found["bundle"])

    def test_ruling_618_falsy_bundles_still_read_back_as_promotions(self):
        module = require("ontoloop.consumption")
        for bundle in (0, "", [], False):
            name = "r17 618 falsy workflow %r" % (bundle,)
            module.record_promotion(name, bundle)
            found = module.discover(name)
            self.assertEqual(found["answer"], "promotion", repr(bundle))
            self.assertEqual(found["bundle"], bundle, repr(bundle))

    def test_ruling_618_recorded_none_does_not_leak_to_other_workflow(self):
        module = require("ontoloop.consumption")
        module.record_promotion("r17 618 holder workflow", None)
        found = module.discover("r17 618 holder workflow")
        self.assertEqual(found["answer"], "promotion")
        other = module.discover("r17 618 unrelated workflow")
        self.assertEqual(other["answer"], "no promotion")
        self.assertIsNone(other["bundle"])

    def test_ruling_618_recorded_none_beside_recorded_mapping(self):
        module = require("ontoloop.consumption")
        module.record_promotion("r17 618 mapping workflow", {"a": 1})
        module.record_promotion("r17 618 none beside workflow", None)
        mapped = module.discover("r17 618 mapping workflow")
        self.assertEqual(mapped["answer"], "promotion")
        self.assertEqual(mapped["bundle"], {"a": 1})
        noned = module.discover("r17 618 none beside workflow")
        self.assertEqual(noned["answer"], "promotion")
        self.assertIsNone(noned["bundle"])


class TestConsumeFixR17SubclassDigestChannels(unittest.TestCase):
    """Fix round 17, ruling 619: the subclass single channel defect.

    The tagged digest form reads a subclass instance of an
    accepted shape through every channel its substance
    carries: a container subclass instance digests by its
    container content and its added instance content
    together, and a Decimal or date subclass instance
    digests by its intrinsic value and its added instance
    content together, beside the plain forms of the same
    shapes digesting as they digest now.
    """

    def test_ruling_619_dict_subclass_differing_added_state_apart(self):
        first = _DictSub({"k": 1})
        first.extra = "one"
        second = _DictSub({"k": 1})
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_619_dict_subclass_identical_added_state_equal(self):
        first = _DictSub({"k": 1})
        first.extra = "one"
        second = _DictSub({"k": 1})
        second.extra = "one"
        self.assertEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest({"k": 1}))

    def test_ruling_619_list_subclass_added_state_read(self):
        first = _ListSub([1, 2])
        first.extra = "one"
        second = _ListSub([1, 2])
        second.extra = "two"
        twin = _ListSub([1, 2])
        twin.extra = "one"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))
        self.assertNotEqual(_digest(first), _digest([1, 2]))

    def test_ruling_619_set_subclass_added_state_read(self):
        first = _SetSub({1, 2})
        first.extra = "one"
        second = _SetSub({1, 2})
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest({1, 2}))

    def test_ruling_619_frozenset_subclass_added_state_read(self):
        first = _FrozenSub({1, 2})
        first.extra = "one"
        second = _FrozenSub({1, 2})
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest(frozenset({1, 2})))

    def test_ruling_619_tuple_subclass_added_state_read(self):
        first = _TupleSub((1, 2))
        first.extra = "one"
        second = _TupleSub((1, 2))
        second.extra = "two"
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertNotEqual(_digest(first), _digest((1, 2)))

    def test_ruling_619_decimal_subclass_intrinsic_value_read(self):
        first = _DecimalSub("1.5")
        first.extra = [1]
        second = _DecimalSub("2.5")
        second.extra = [1]
        self.assertNotEqual(_digest(first), _digest(second))

    def test_ruling_619_decimal_subclass_added_state_read(self):
        first = _DecimalSub("1.5")
        first.extra = [1]
        second = _DecimalSub("1.5")
        second.extra = [2]
        twin = _DecimalSub("1.5")
        twin.extra = [1]
        self.assertNotEqual(_digest(first), _digest(second))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_619_date_subclass_both_channels_read(self):
        first = _DateSub(2026, 3, 4)
        first.extra = [1]
        later = _DateSub(2027, 3, 4)
        later.extra = [1]
        added = _DateSub(2026, 3, 4)
        added.extra = [2]
        twin = _DateSub(2026, 3, 4)
        twin.extra = [1]
        self.assertNotEqual(_digest(first), _digest(later))
        self.assertNotEqual(_digest(first), _digest(added))
        self.assertEqual(_digest(first), _digest(twin))

    def test_ruling_619_subclass_nested_added_state_read(self):
        first = _DictSub({"k": 1})
        first.extra = "one"
        second = _DictSub({"k": 1})
        second.extra = "two"
        self.assertNotEqual(_digest([first]), _digest([second]))
        self.assertNotEqual(
            _digest({"wrap": first}), _digest({"wrap": second})
        )

    def test_ruling_619_plain_forms_still_digest_as_they_digest_now(self):
        plain_sub = _DictSub({"k": 1})
        self.assertEqual(_digest(plain_sub), _digest({"k": 1}))
        self.assertNotEqual(
            _digest(decimal.Decimal("1.5")), _digest(decimal.Decimal("2.5"))
        )
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )
        self.assertNotEqual(
            _digest(_ResidualProbe(1)), _digest(_ResidualProbe(2))
        )
        self.assertEqual(
            _digest(_ResidualProbe(1)), _digest(_ResidualProbe(1))
        )


class TestConsumeFixR17NoContentDigest(unittest.TestCase):
    """Fix round 17, ruling 620: the no content type name defect.

    A value whose substance stands in content the digest
    reading reaches in substance, an in memory stream among
    them, digests by that content, and a value whose content
    stands in a channel the reading cannot reach without
    consumption, an iterator among them, stands refused at
    the digest surface, so differing content never digests
    equal and a hash checked load never accepts material
    its hash does not name.
    """

    def test_ruling_620_bytesio_differing_content_apart(self):
        self.assertNotEqual(
            _digest(io.BytesIO(b"abc")), _digest(io.BytesIO(b"abd"))
        )

    def test_ruling_620_bytesio_identical_content_equal(self):
        self.assertEqual(
            _digest(io.BytesIO(b"abc")), _digest(io.BytesIO(b"abc"))
        )
        self.assertNotEqual(
            _digest(io.BytesIO(b"abc")), _digest(io.BytesIO(b"abd"))
        )

    def test_ruling_620_stringio_content_read(self):
        self.assertNotEqual(
            _digest(io.StringIO("alpha")), _digest(io.StringIO("beta"))
        )
        self.assertEqual(
            _digest(io.StringIO("alpha")), _digest(io.StringIO("alpha"))
        )

    def test_ruling_620_bytesio_nested_content_read(self):
        self.assertNotEqual(
            _digest([io.BytesIO(b"abc")]), _digest([io.BytesIO(b"abd")])
        )
        self.assertNotEqual(
            _digest({"k": io.BytesIO(b"abc")}),
            _digest({"k": io.BytesIO(b"abd")}),
        )

    def test_ruling_620_hash_check_rejects_differing_stream(self):
        module = require("ontoloop.consumption")
        expected = _digest(io.BytesIO(b"expected content"))
        refused = module.load_with_hash_check(
            io.BytesIO(b"differing content"), expected_hash=expected
        )
        self.assertFalse(refused["loaded"])
        self.assertEqual(refused["position"], "unloadable")

    def test_ruling_620_hash_check_accepts_matching_stream(self):
        module = require("ontoloop.consumption")
        expected = _digest(io.BytesIO(b"expected content"))
        loaded = module.load_with_hash_check(
            io.BytesIO(b"expected content"), expected_hash=expected
        )
        self.assertTrue(loaded["loaded"])
        self.assertEqual(loaded["position"], "loadable")

    def test_ruling_620_hash_mismatch_on_differing_streams(self):
        module = require("ontoloop.consumption")
        apart = module.load_with_hash_mismatch(
            material=io.BytesIO(b"one"), tool_material=io.BytesIO(b"two")
        )
        self.assertEqual(apart["position"], "unloadable")
        alike = module.load_with_hash_mismatch(
            material=io.BytesIO(b"one"), tool_material=io.BytesIO(b"one")
        )
        self.assertEqual(alike["position"], "loadable")
        self.assertTrue(alike["loaded"])

    def test_ruling_620_zip_and_map_iterators_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check(zip([1, 2]))
        with self.assertRaises(ValueError):
            module.load_with_hash_check(map(str, [1, 2]))

    def test_ruling_620_further_iterator_forms_refused(self):
        module = require("ontoloop.consumption")
        forms = (
            enumerate([1, 2]),
            filter(None, [1, 2]),
            reversed([1, 2]),
            iter([1, 2]),
        )
        for form in forms:
            with self.assertRaises(ValueError, msg=repr(type(form))):
                module.load_with_hash_check(form)

    def test_ruling_620_standing_content_forms_still_decide(self):
        self.assertEqual(_digest(b"alpha"), _digest(bytearray(b"alpha")))
        self.assertEqual(
            _digest(b"alpha"), _digest(memoryview(b"alpha"))
        )
        self.assertNotEqual(
            _digest(array("B", b"abc")), _digest(array("B", b"abd"))
        )
        self.assertNotEqual(
            _digest(collections.deque([1, 2])),
            _digest(collections.deque([1, 3])),
        )
        self.assertEqual(
            _digest("alpha"),
            hashlib.sha256("alpha".encode("utf-8")).hexdigest(),
        )


class TestConsumeFixR17GeneratorAddressDigest(unittest.TestCase):
    """Fix round 17, ruling 621: the generator address digest defect.

    No digest form carries the process address of a value,
    and a generator value stands refused at the digest
    surface in the governed form, beside the content bearing
    string forms still digesting by their content and the
    every process forms still standing in every process.
    """

    def test_ruling_621_generator_refused_at_digest_surface(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check(item for item in [1, 2])

    def test_ruling_621_two_generators_over_same_items_refused(self):
        module = require("ontoloop.consumption")
        for _ in range(2):
            with self.assertRaises(ValueError):
                module.load_with_hash_check(item for item in [1, 2])

    def test_ruling_621_generator_nested_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check([(item for item in [1, 2])])
        with self.assertRaises(ValueError):
            module.load_with_hash_check(
                {"k": (item for item in [1, 2])}
            )

    def test_ruling_621_address_carrying_repr_refused(self):
        module = require("ontoloop.consumption")
        with self.assertRaises(ValueError):
            module.load_with_hash_check(_AddressReprProbe())
        with self.assertRaises(ValueError):
            module.load_with_hash_check(_AddressReprProbeSecond())

    def test_ruling_621_open_file_value_refused(self):
        module = require("ontoloop.consumption")
        handle, path = tempfile.mkstemp()
        try:
            os.write(handle, b"file content one")
            os.close(handle)
            with open(path, "r", encoding="utf-8") as stream:
                with self.assertRaises(ValueError):
                    module.load_with_hash_check(stream)
        finally:
            os.unlink(path)

    def test_ruling_621_set_digest_stands_in_every_process_form(self):
        self.assertEqual(
            _digest({"beta", "alpha", "gamma"}),
            "e89afefd95e143b21da7c8d5ed17c7b36fa4d8640ba53ff"
            "98c1e30acc9b6d41f",
        )

    def test_ruling_621_content_bearing_string_forms_still_digest(self):
        self.assertNotEqual(
            _digest(decimal.Decimal("1.5")), _digest(decimal.Decimal("2.5"))
        )
        self.assertNotEqual(_digest(range(3)), _digest(range(4)))
        self.assertNotEqual(
            _digest(re.compile("alpha")), _digest(re.compile("beta"))
        )
        self.assertNotEqual(
            _digest(datetime.date(2026, 1, 1)),
            _digest(datetime.date(2027, 1, 1)),
        )
        self.assertNotEqual(_digest(1 + 2j), _digest(1 + 3j))

    def test_ruling_621_plain_object_no_content_form_stands(self):
        self.assertEqual(_digest(object()), _digest(object()))


if __name__ == "__main__":
    unittest.main()
