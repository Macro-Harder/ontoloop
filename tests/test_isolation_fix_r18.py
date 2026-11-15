"""Fix round 18 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 18 triage
ruling 673: further uncopyable types escaping the copy act with
an ungoverned exception, at the identity ISO-R18-1 (roster 1946)
merged with Lead Engineer line E-9 (roster 1957). The named
types are an iterator over a memoryview, a scandir iterator of
the os module, a DirEntry object of the os module, a simple
queue object of the queue module, a token object of the
contextvars module, a memory BIO object of the ssl module, a
byref object of the ctypes module in its CArgObject form, a
ctypes pointer object escaping with a ValueError carrying the
ctypes text, a Future object of the asyncio module, a database
handle object of the dbm module and a shelve shelf standing
over such a handle, an XMLParser object, a Pickler object, a
writer object of the csv module, and a context manager object
of the decimal module as returned by its localcontext act.
Each type stands pinned at the whole bundle, direct bundle
value, holder, and nested list positions, the shelf at the
holder position its raising paper states, beside the standing
governed refusals and the standing recording controls.
"""

import asyncio
import contextvars
import csv
import ctypes
import dbm
import decimal
import io
import os
import pickle
import select
import shelve
import shutil
import ssl
import tempfile
import unittest
import xml.etree.ElementTree as _et

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


def _assert_uncopyable_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _positions(make):
    """Yield (position name, bundle, cleanup) for one fresh value."""
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
                "r18 673 " + label + " " + position + " wf",
            )
        finally:
            if cleanup is not None:
                cleanup()


def _make_memoryview_iterator():
    return iter(memoryview(b"abc")), None


def _make_scandir_iterator():
    iterator = os.scandir(tempfile.gettempdir())
    return iterator, iterator.close


def _make_dir_entry():
    iterator = os.scandir(tempfile.gettempdir())
    entry = next(iterator)
    return entry, iterator.close


def _make_simple_queue():
    import queue

    return queue.SimpleQueue(), None


_VAR = contextvars.ContextVar("r18_var")


def _make_token():
    return _VAR.set(1), None


def _make_memory_bio():
    return ssl.MemoryBIO(), None


def _make_byref():
    value = ctypes.c_int(3)
    return ctypes.byref(value), None


def _make_byref_offset():
    value = ctypes.c_int(3)
    return ctypes.byref(value, 1), None


def _make_pointer():
    value = ctypes.c_int(3)
    return ctypes.pointer(value), None


def _make_future():
    loop = asyncio.new_event_loop()
    future = loop.create_future()

    def cleanup():
        future.cancel()
        loop.close()

    return future, cleanup


def _make_dbm_handle():
    folder = tempfile.mkdtemp()
    handle = dbm.open(os.path.join(folder, "db"), "c")

    def cleanup():
        handle.close()
        shutil.rmtree(folder, ignore_errors=True)

    return handle, cleanup


def _make_xml_parser():
    return _et.XMLParser(), None


def _make_pickler():
    return pickle.Pickler(io.BytesIO()), None


def _make_csv_writer():
    return csv.writer(io.StringIO()), None


def _make_decimal_context_manager():
    return decimal.localcontext(), None


class TestRuling673FurtherUncopyableTypes(unittest.TestCase):
    """Ruling 673 (ISO-R18-1 merged with E-9): types refused."""

    def test_memoryview_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_memoryview_iterator, "mviter"
        )

    def test_scandir_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_scandir_iterator, "scandir"
        )

    def test_dir_entry_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_dir_entry, "direntry")

    def test_simple_queue_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_simple_queue, "simplequeue"
        )

    def test_token_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_token, "token")

    def test_memory_bio_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_memory_bio, "memorybio")

    def test_byref_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_byref, "byref")

    def test_byref_offset_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_byref_offset, "byref offset"
        )

    def test_pointer_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_pointer, "pointer")

    def test_future_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_future, "future")

    def test_dbm_handle_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_dbm_handle, "dbm")

    def test_shelf_over_dbm_handle_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        folder = tempfile.mkdtemp()
        handle = dbm.open(os.path.join(folder, "db"), "c")
        shelf = shelve.Shelf(handle)
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(shelf)},
                "r18 673 shelf holder wf",
            )
        finally:
            shelf.close()
            shutil.rmtree(folder, ignore_errors=True)

    def test_xml_parser_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_xml_parser, "xmlparser")

    def test_pickler_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_pickler, "pickler")

    def test_csv_writer_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_csv_writer, "csvwriter")

    def test_decimal_context_manager_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_decimal_context_manager, "decctx"
        )


class TestRuling673StandingControls(unittest.TestCase):
    """Ruling 673 controls: standing forms decide as they decide."""

    def test_poll_object_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(select.poll())},
            "r18 673 poll control wf",
        )

    def test_queue_object_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        import queue

        _assert_uncopyable_refused(
            self, module, {"part": Holder(queue.Queue())},
            "r18 673 queue control wf",
        )

    def test_context_object_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(contextvars.Context())},
            "r18 673 context control wf",
        )

    def test_ssl_context_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT))},
            "r18 673 ssl context control wf",
        )

    def test_hash_object_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        import hashlib

        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(hashlib.sha256(b"data"))},
            "r18 673 hash control wf",
        )

    def test_memoryview_at_walked_position_still_copies(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r18 673 memoryview control wf",
            {"part": memoryview(b"abc")},
        )
        part = recorded["bundle"]["part"]
        self.assertIs(type(part), bytearray)
        self.assertEqual(part, bytearray(b"abc"))

    def test_memoryview_inside_fallback_value_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(memoryview(b"abc"))},
            "r18 673 memoryview fallback control wf",
        )

    def test_ctypes_int_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        original = ctypes.c_int(3)
        recorded = module.record_promotion(
            "r18 673 ctypes int control wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied.value, 3)

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r18 673 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])


if __name__ == "__main__":
    unittest.main()
