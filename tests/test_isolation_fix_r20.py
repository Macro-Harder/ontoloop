"""Fix round 20 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 20 triage
rulings 793 to 800: further uncopyable types escaping the copy
act (ISO-R20-1, roster 2054, merged with Lead Engineer line
E-22, roster 2065), an uncopyable value in tree element
attributes and children (ISO-R20-2), an uncopyable value in an
operator call specification (ISO-R20-3), an uncopyable callable
exercised through a callable iterator or filter (ISO-R20-4), a
cache wrapper recorded in shared form (ISO-R20-5), a globals
view recursion in the replacements limb (ISO-R20-6), exception
cause and context chains recorded in no part (Lead Engineer
line E-23), and a CDLL object recorded carrying the caller
handle (Lead Engineer line E-24). Each refused form stands
pinned at the whole bundle, direct bundle value, holder, and
nested list positions beside the standing controls its ruling
names, unless its ruling names the holder position alone.
"""

import bz2
import ctypes
import ctypes.util
import functools
import io
import logging
import lzma
import operator
import sqlite3
import struct
import threading
import types
import unittest
import xml.etree.ElementTree as _etree

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class _IntFieldStructure(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int)]


def _assert_uncopyable_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _positions(make):
    obj, cleanup = make()
    yield "whole", obj, cleanup
    obj, cleanup = make()
    yield "direct", {"part": obj}, cleanup
    obj, cleanup = make()
    yield "holder", {"part": Holder(obj)}, cleanup
    obj, cleanup = make()
    yield "nested", {"part": Holder([obj])}, cleanup


def _check_positions(case, module, make, label):
    for position, bundle, cleanup in _positions(make):
        try:
            _assert_uncopyable_refused(
                case, module, bundle,
                "r20 " + label + " " + position + " wf",
            )
        finally:
            if cleanup is not None:
                cleanup()


def _lock():
    return threading.Lock()


def _make_bz2_compressor():
    return bz2.BZ2Compressor(), None


def _make_bz2_decompressor():
    return bz2.BZ2Decompressor(), None


def _make_lzma_compressor():
    return lzma.LZMACompressor(), None


def _make_lzma_decompressor():
    return lzma.LZMADecompressor(), None


def _make_struct_object():
    return struct.Struct("i"), None


def _make_sqlite_row():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select 1 as a")
    row = cursor.fetchone()

    def cleanup():
        cursor.close()
        connection.close()

    return row, cleanup


class TestRuling793FurtherUncopyableTypes(unittest.TestCase):
    """Ruling 793 (ISO-R20-1 merged with E-22): types refused."""

    def test_bz2_compressor_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_bz2_compressor, "793 bz2comp"
        )

    def test_bz2_decompressor_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_bz2_decompressor, "793 bz2decomp"
        )

    def test_lzma_compressor_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_lzma_compressor, "793 lzmacomp"
        )

    def test_lzma_decompressor_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_lzma_decompressor, "793 lzmadecomp"
        )

    def test_struct_object_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_struct_object, "793 struct")

    def test_sqlite_row_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_sqlite_row, "793 row")

    def test_csv_reader_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        import csv

        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(csv.reader(io.StringIO("a,b\n")))},
            "r20 793 csv reader control wf",
        )

    def test_bytesio_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r20 793 bytesio control wf",
            {"part": Holder(io.BytesIO(b"data"))},
        )
        copied = recorded["bundle"]["part"].part
        self.assertEqual(copied.getvalue(), b"data")

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r20 793 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_zlib_objects_inside_holder_still_record_apart(self):
        module = require("ontoloop.consumption")
        import zlib

        compressor = zlib.compressobj()
        recorded = module.record_promotion(
            "r20 793 zlib control wf", {"part": Holder(compressor)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, compressor)
        self.assertEqual(copied.flush(), compressor.flush())
        decompressor = zlib.decompressobj()
        recorded = module.record_promotion(
            "r20 793 zlib decomp control wf",
            {"part": Holder(decompressor)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, decompressor)


def _make_element_lock_attribute():
    element = _etree.Element("root", {"k": _lock()})
    return element, None


def _make_element_socket_attribute():
    import socket

    left, right = socket.socketpair()

    def cleanup():
        left.close()
        right.close()

    element = _etree.Element("root", {"k": left})
    return element, cleanup


def _make_element_child_lock_attribute():
    child = _etree.Element("child", {"k": _lock()})
    element = _etree.Element("root")
    element.append(child)
    return element, None


def _make_tree_lock_attribute():
    root = _etree.Element("root", {"k": _lock()})
    return _etree.ElementTree(root), None


class TestRuling794TreeElementReach(unittest.TestCase):
    """Ruling 794 (ISO-R20-2): element attributes and children."""

    def test_element_lock_attribute_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_element_lock_attribute, "794 attr"
        )

    def test_element_socket_attribute_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_element_socket_attribute, "794 sockattr"
        )

    def test_element_child_lock_attribute_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_element_child_lock_attribute, "794 child"
        )

    def test_tree_lock_attribute_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_tree_lock_attribute, "794 tree"
        )

    def test_plain_element_inside_holder_still_records_apart(self):
        module = require("ontoloop.consumption")
        element = _etree.Element("root", {"k": "v"})
        child = _etree.Element("child")
        child.text = "hi"
        element.append(child)
        recorded = module.record_promotion(
            "r20 794 plain element control wf",
            {"part": Holder(element)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, element)
        self.assertEqual(copied.attrib, {"k": "v"})
        self.assertEqual(list(copied)[0].text, "hi")
        copied.attrib["k"] = "changed"
        self.assertEqual(element.attrib, {"k": "v"})

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(_lock())},
            "r20 794 lock control wf",
        )


def _make_methodcaller_lock():
    return operator.methodcaller("get", _lock()), None


def _make_itemgetter_lock():
    return operator.itemgetter(_lock()), None


class TestRuling795OperatorCallSpecification(unittest.TestCase):
    """Ruling 795 (ISO-R20-3): operator call specification reach."""

    def test_methodcaller_lock_argument_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_methodcaller_lock, "795 methodcaller"
        )

    def test_itemgetter_lock_item_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_itemgetter_lock, "795 itemgetter"
        )

    def test_attrgetter_plain_name_still_records(self):
        module = require("ontoloop.consumption")
        original = operator.attrgetter("real")
        recorded = module.record_promotion(
            "r20 795 attrgetter control wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied(complex(3, 4)), 3.0)

    def test_plain_call_specifications_still_record(self):
        module = require("ontoloop.consumption")
        caller = operator.methodcaller("get", "key")
        recorded = module.record_promotion(
            "r20 795 plain methodcaller control wf",
            {"part": Holder(caller)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, caller)
        self.assertEqual(copied({"key": 9}), 9)
        getter = operator.itemgetter("a")
        recorded = module.record_promotion(
            "r20 795 plain itemgetter control wf",
            {"part": Holder(getter)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, getter)
        self.assertEqual(copied({"a": 5}), 5)


def _make_callable_iterator_lock():
    lock = _lock()
    return iter(lock.acquire, True), None


def _make_filter_lock():
    lock = _lock()
    return filter(lock.acquire, [1]), None


def _plain_predicate(value):
    return value > 1


def _plain_callable():
    return 42


class TestRuling796CallableIteratorAndFilter(unittest.TestCase):
    """Ruling 796 (ISO-R20-4): callable carried by iterator forms."""

    def test_callable_iterator_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_callable_iterator_lock, "796 calliter"
        )

    def test_filter_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_filter_lock, "796 filter")

    def test_refusal_exercises_no_callable(self):
        module = require("ontoloop.consumption")
        lock = _lock()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(iter(lock.acquire, True))},
            "r20 796 no exercise iter wf",
        )
        self.assertFalse(lock.locked())
        lock = _lock()
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(filter(lock.acquire, [1]))},
            "r20 796 no exercise filter wf",
        )
        self.assertFalse(lock.locked())

    def test_plain_filter_still_records_in_snapshot_form(self):
        module = require("ontoloop.consumption")
        caller = filter(_plain_predicate, [1, 2, 3])
        recorded = module.record_promotion(
            "r20 796 plain filter control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(list(copied), [2, 3])

    def test_callable_iterator_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        caller = iter(_plain_callable, 999)
        recorded = module.record_promotion(
            "r20 796 plain calliter control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(next(copied), 42)

    def test_plain_iterator_mutable_elements_still_record(self):
        module = require("ontoloop.consumption")
        caller = iter([[1, 2], [3]])
        recorded = module.record_promotion(
            "r20 796 plain iterator control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(list(copied), [[1, 2], [3]])
        self.assertEqual(list(caller), [[1, 2], [3]])


def _template(value):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(_template.__code__, globals_map, "synthetic")


def _make_cache_wrapper():
    globals_map = {"__builtins__": {}}
    func = _synthetic_function(globals_map)
    wrapper = functools.lru_cache(maxsize=None)(func)
    wrapper(1)
    return wrapper, None


class TestRuling797CacheWrapper(unittest.TestCase):
    """Ruling 797 (ISO-R20-5): cache wrapper shared form refused."""

    def test_cache_wrapper_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_cache_wrapper, "797 lru")

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r20 797 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_null_handler_inside_holder_still_records_apart(self):
        module = require("ontoloop.consumption")
        original = logging.NullHandler()
        recorded = module.record_promotion(
            "r20 797 null handler control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertIsInstance(copied, logging.NullHandler)

    def test_plain_synthetic_function_still_stands_in_its_form(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}
        func = _synthetic_function(globals_map)
        recorded = module.record_promotion(
            "r20 797 plain function control wf", {"part": Holder(func)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIs(copied, func)


def _make_self_view_function():
    globals_map = {"__builtins__": {}}
    globals_map["view"] = globals_map.values()
    func = _synthetic_function(globals_map)
    globals_map["func"] = func
    return func, None


class TestRuling798GlobalsSelfView(unittest.TestCase):
    """Ruling 798 (ISO-R20-6): globals self view recursion."""

    def test_one_function_over_self_view_globals_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_self_view_function, "798 onefunc"
        )

    def test_two_functions_over_self_view_globals_are_refused(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}
        globals_map["view"] = globals_map.values()
        first = _synthetic_function(globals_map)
        second = _synthetic_function(globals_map)
        globals_map["first"] = first
        globals_map["second"] = second
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder((first, second))},
            "r20 798 twofunc wf",
        )

    def test_view_with_class_and_instance_is_refused(self):
        module = require("ontoloop.consumption")

        class Local:
            pass

        globals_map = {"__builtins__": {}}
        globals_map["view"] = globals_map.values()
        globals_map["cls"] = Local
        globals_map["inst"] = Local()
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)}, "r20 798 classinst wf"
        )

    def test_function_over_plain_globals_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "held": [1, 2]}
        func = _synthetic_function(globals_map)
        recorded = module.record_promotion(
            "r20 798 plain globals control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])

    def test_ruling_622_view_of_another_mapping_still_records(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        shared = {"__builtins__": {}, "held": source.values()}
        first = _synthetic_function(shared)
        second = _synthetic_function(shared)
        recorded = module.record_promotion(
            "r20 798 ruling 622 control wf",
            {"first": first, "second": second},
        )
        bundle = recorded["bundle"]
        self.assertIs(
            bundle["first"].__globals__, bundle["second"].__globals__
        )
        self.assertIsNot(bundle["first"].__globals__, shared)
        self.assertEqual(bundle["first"].__globals__["held"], [[1]])


def _make_cause_lock_exception():
    try:
        try:
            raise RuntimeError(_lock())
        except RuntimeError as cause:
            raise ValueError("outer") from cause
    except ValueError as error:
        return error, None


def _make_context_lock_exception():
    try:
        try:
            raise RuntimeError(_lock())
        except RuntimeError:
            raise ValueError("outer")
    except ValueError as error:
        return error, None


def _make_cause_plain_exception():
    try:
        try:
            raise RuntimeError(["plain cause"])
        except RuntimeError as cause:
            raise ValueError("outer") from cause
    except ValueError as error:
        return error, None


def _make_context_plain_exception():
    try:
        try:
            raise RuntimeError("plain context")
        except RuntimeError:
            raise ValueError("outer")
    except ValueError as error:
        return error, None


class TestRuling799ExceptionChains(unittest.TestCase):
    """Ruling 799 (E-23): exception cause and context chains."""

    def test_cause_chain_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_cause_lock_exception, "799 cause"
        )

    def test_context_chain_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_context_lock_exception, "799 context"
        )

    def test_plain_cause_is_carried_into_the_copy_apart(self):
        module = require("ontoloop.consumption")
        original, _cleanup = _make_cause_plain_exception()
        recorded = module.record_promotion(
            "r20 799 plain cause wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertIsNotNone(copied.__cause__)
        self.assertIsNot(copied.__cause__, original.__cause__)
        self.assertEqual(copied.__cause__.args, (["plain cause"],))
        self.assertIs(copied.__context__, copied.__cause__)
        self.assertTrue(copied.__suppress_context__)
        copied.__cause__.args[0].append("changed")
        self.assertEqual(original.__cause__.args, (["plain cause"],))
        found = module.discover("r20 799 plain cause wf")
        discovered = found["bundle"]["part"].part
        self.assertIsNotNone(discovered.__cause__)
        self.assertEqual(discovered.__cause__.args, (["plain cause"],))

    def test_plain_context_is_carried_into_the_copy_apart(self):
        module = require("ontoloop.consumption")
        original, _cleanup = _make_context_plain_exception()
        recorded = module.record_promotion(
            "r20 799 plain context wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNone(copied.__cause__)
        self.assertIsNotNone(copied.__context__)
        self.assertIsNot(copied.__context__, original.__context__)
        self.assertEqual(copied.__context__.args, ("plain context",))
        self.assertFalse(copied.__suppress_context__)

    def test_chain_cycle_terminates_and_is_carried(self):
        module = require("ontoloop.consumption")
        first = ValueError("first")
        second = RuntimeError("second")
        first.__cause__ = second
        second.__cause__ = first
        recorded = module.record_promotion(
            "r20 799 cycle wf", {"part": Holder(first)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, first)
        self.assertIsNot(copied.__cause__, second)
        self.assertEqual(copied.__cause__.args, ("second",))
        self.assertIs(copied.__cause__.__cause__, copied)

    def test_exception_plain_argument_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r20 799 plain argument control wf",
            {"part": Holder(ValueError([1, 2]))},
        )
        copied = recorded["bundle"]["part"].part
        self.assertEqual(copied.args, ([1, 2],))

    def test_exception_lock_argument_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(ValueError(_lock()))},
            "r20 799 lock argument control wf",
        )

    def test_exception_lock_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        error = ValueError("plain")
        error.bad = _lock()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(error)},
            "r20 799 lock attribute control wf",
        )


def _make_cdll():
    name = ctypes.util.find_library("c") or "libc.so.6"
    return ctypes.CDLL(name), None


class TestRuling800CdllHandle(unittest.TestCase):
    """Ruling 800 (E-24): CDLL handle sharing refused."""

    def test_cdll_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_cdll, "800 cdll")

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r20 800 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_ctypes_scalar_and_structure_still_record_apart(self):
        module = require("ontoloop.consumption")
        original = ctypes.c_int(3)
        recorded = module.record_promotion(
            "r20 800 ctypes int control wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied.value, 3)
        structure = _IntFieldStructure()
        structure.x = 7
        recorded = module.record_promotion(
            "r20 800 structure control wf", {"part": Holder(structure)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, structure)
        self.assertEqual(copied.x, 7)

    def test_null_handler_inside_holder_still_records_apart(self):
        module = require("ontoloop.consumption")
        original = logging.NullHandler()
        recorded = module.record_promotion(
            "r20 800 null handler control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertIsInstance(copied, logging.NullHandler)


if __name__ == "__main__":
    unittest.main()
