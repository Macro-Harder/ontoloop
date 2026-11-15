"""Fix round 19 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 19 triage
rulings 730 to 733: further uncopyable types escaping the copy
act (ISO-R19-1, roster 2002, merged with Lead Engineer line
E-10, roster 2011), an uncopyable element inside an iterator
(ISO-R19-2), an uncopyable value in exception arguments
(ISO-R19-3), and two type forms recorded in shared form
(ISO-R19-4). Each refused type stands pinned at the whole
bundle, direct bundle value, holder, and nested list positions,
beside the standing governed refusals and the standing
recording controls.
"""

import contextvars
import csv
import ctypes
import io
import itertools
import json
import logging
import multiprocessing
import pickle
import socket
import sqlite3
import ssl
import threading
import unittest
import xml.parsers.expat

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class _SuperBase:
    def greet(self):
        return "hello"


class _PointerFieldStructure(ctypes.Structure):
    _fields_ = [("p", ctypes.POINTER(ctypes.c_int))]


class _CharPointerFieldStructure(ctypes.Structure):
    _fields_ = [("p", ctypes.c_char_p)]


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
                "r19 " + label + " " + position + " wf",
            )
        finally:
            if cleanup is not None:
                cleanup()


def _make_csv_reader():
    return csv.reader(io.StringIO("a,b\n1,2\n")), None


def _make_csv_dict_reader():
    return csv.DictReader(io.StringIO("a,b\n1,2\n")), None


def _make_pyexpat_parser():
    return xml.parsers.expat.ParserCreate(), None


def _make_unpickler():
    return pickle.Unpickler(io.BytesIO(b"")), None


def _make_sqlite_blob():
    connection = sqlite3.connect(":memory:")
    connection.execute("create table t (b blob)")
    connection.execute("insert into t values (zeroblob(3))")
    blob = connection.blobopen("t", "b", 1)

    def cleanup():
        blob.close()
        connection.close()

    return blob, cleanup


def _make_ssl_socket_object():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    incoming = ssl.MemoryBIO()
    outgoing = ssl.MemoryBIO()
    return context.wrap_bio(incoming, outgoing), None


def _make_getset_descriptor():
    return int.__dict__["real"], None


def _make_super_object():
    return super(_SuperBase, _SuperBase()), None


def _make_mp_lock():
    return multiprocessing.Lock(), None


def _make_mp_semaphore():
    return multiprocessing.Semaphore(), None


def _make_mp_event():
    return multiprocessing.Event(), None


def _make_mp_condition():
    return multiprocessing.Condition(), None


def _make_mp_process():
    return multiprocessing.Process(target=lambda: None), None


def _make_c_char_p():
    return ctypes.c_char_p(b"hello"), None


def _make_c_wchar_p():
    return ctypes.c_wchar_p("hello"), None


def _make_c_void_p():
    return ctypes.c_void_p(12345), None


_CALLBACK_TYPE = ctypes.CFUNCTYPE(None)


def _make_callback():
    return _CALLBACK_TYPE(lambda: None), None


def _make_pointer_array():
    first = ctypes.pointer(ctypes.c_int(1))
    second = ctypes.pointer(ctypes.c_int(2))
    array_type = ctypes.POINTER(ctypes.c_int) * 2
    return array_type(first, second), None


def _make_void_pointer_array():
    array_type = ctypes.c_void_p * 2
    return array_type(111, 222), None


def _make_pointer_field_structure():
    instance = _PointerFieldStructure()
    target = ctypes.c_int(5)
    instance.p = ctypes.pointer(target)
    return instance, None


def _make_char_pointer_field_structure():
    instance = _CharPointerFieldStructure()
    instance.p = b"hello"
    return instance, None


def _make_context_var():
    return contextvars.ContextVar("r19_var"), None


def _make_json_decoder():
    return json.JSONDecoder(), None


class TestRuling730FurtherUncopyableTypes(unittest.TestCase):
    """Ruling 730 (ISO-R19-1 merged with E-10): types refused."""

    def test_csv_reader_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_csv_reader, "730 reader")

    def test_csv_dict_reader_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_csv_dict_reader, "730 dictreader"
        )

    def test_pyexpat_parser_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_pyexpat_parser, "730 expat")

    def test_unpickler_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_unpickler, "730 unpickler")

    def test_sqlite_blob_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_sqlite_blob, "730 blob")

    def test_ssl_socket_object_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_ssl_socket_object, "730 sslsock"
        )

    def test_getset_descriptor_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_getset_descriptor, "730 getset"
        )

    def test_super_object_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_super_object, "730 super")

    def test_multiprocessing_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_mp_lock, "730 mplock")

    def test_multiprocessing_semaphore_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_mp_semaphore, "730 mpsemaphore"
        )

    def test_multiprocessing_event_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_mp_event, "730 mpevent")

    def test_multiprocessing_condition_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_mp_condition, "730 mpcondition"
        )

    def test_multiprocessing_process_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_mp_process, "730 mpprocess")

    def test_c_char_p_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_c_char_p, "730 charp")

    def test_c_wchar_p_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_c_wchar_p, "730 wcharp")

    def test_c_void_p_with_address_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_c_void_p, "730 voidp")

    def test_callback_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_callback, "730 callback")

    def test_pointer_array_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_pointer_array, "730 ptrarray"
        )

    def test_void_pointer_array_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_void_pointer_array, "730 voidparray"
        )

    def test_pointer_field_structure_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_pointer_field_structure, "730 ptrstruct"
        )

    def test_char_pointer_field_structure_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_char_pointer_field_structure,
            "730 charpstruct",
        )

    def test_context_var_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_context_var, "730 ctxvar")

    def test_json_decoder_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_json_decoder, "730 jsondecoder"
        )


class TestRuling730StandingControls(unittest.TestCase):
    """Ruling 730 controls: standing forms decide as they decide."""

    def test_csv_writer_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(csv.writer(io.StringIO()))},
            "r19 730 csv writer control wf",
        )

    def test_csv_dict_writer_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        writer = csv.DictWriter(io.StringIO(), fieldnames=["a"])
        _assert_uncopyable_refused(
            self, module, {"part": Holder(writer)},
            "r19 730 csv dict writer control wf",
        )

    def test_pickler_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(pickle.Pickler(io.BytesIO()))},
            "r19 730 pickler control wf",
        )

    def test_sqlite_cursor_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        connection = sqlite3.connect(":memory:")
        try:
            _assert_uncopyable_refused(
                self, module,
                {"part": Holder(connection.cursor())},
                "r19 730 cursor control wf",
            )
        finally:
            connection.close()

    def test_memory_bio_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(ssl.MemoryBIO())},
            "r19 730 memory bio control wf",
        )

    def test_bytesio_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r19 730 bytesio control wf",
            {"part": Holder(io.BytesIO(b"data"))},
        )
        copied = recorded["bundle"]["part"].part
        self.assertEqual(copied.getvalue(), b"data")

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r19 730 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_ctypes_int_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        original = ctypes.c_int(3)
        recorded = module.record_promotion(
            "r19 730 ctypes int control wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied.value, 3)

    def test_plain_structure_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        original = _IntFieldStructure()
        original.x = 7
        recorded = module.record_promotion(
            "r19 730 plain structure control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied.x, 7)

    def test_pure_python_unpickler_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        original = pickle._Unpickler(io.BytesIO(b""))
        recorded = module.record_promotion(
            "r19 730 pure unpickler control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)


def _lock():
    return threading.Lock()


def _socket_pair():
    left, right = socket.socketpair()
    return left, right


def _generator():
    yield 1


def _make_list_iterator_lock():
    return iter([_lock()]), None


def _make_dict_key_iterator_lock():
    return iter({_lock(): "value"}), None


def _make_set_iterator_lock():
    return iter({_lock()}), None


def _make_enumerate_lock():
    return enumerate([_lock()]), None


def _make_zip_lock():
    return zip([_lock()]), None


def _make_map_lock():
    return map(lambda item: item, [_lock()]), None


def _make_chain_lock():
    return itertools.chain([_lock()]), None


def _make_islice_lock():
    return itertools.islice([_lock()], 1), None


def _make_reversed_lock():
    return reversed([_lock()]), None


def _make_list_iterator_socket():
    left, right = _socket_pair()

    def cleanup():
        left.close()
        right.close()

    return iter([left]), cleanup


def _make_list_iterator_generator():
    return iter([_generator()]), None


def _make_list_iterator_reader():
    return iter([csv.reader(io.StringIO("a,b\n"))]), None


class TestRuling731IteratorElements(unittest.TestCase):
    """Ruling 731 (ISO-R19-2): iterator elements refused."""

    def test_lock_in_list_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_list_iterator_lock, "731 listiter"
        )

    def test_lock_in_dict_key_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_dict_key_iterator_lock, "731 dictiter"
        )

    def test_lock_in_set_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_set_iterator_lock, "731 setiter"
        )

    def test_lock_in_enumerate_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_enumerate_lock, "731 enumerate"
        )

    def test_lock_in_zip_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_zip_lock, "731 zip")

    def test_lock_in_map_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_map_lock, "731 map")

    def test_lock_in_chain_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_chain_lock, "731 chain")

    def test_lock_in_islice_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_islice_lock, "731 islice")

    def test_lock_in_reversed_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_reversed_lock, "731 reversed"
        )

    def test_socket_in_list_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_list_iterator_socket, "731 sockiter"
        )

    def test_generator_in_list_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_list_iterator_generator, "731 geniter"
        )

    def test_reader_in_list_iterator_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_list_iterator_reader, "731 readeriter"
        )

    def test_plain_iterator_with_mutable_elements_still_records(self):
        module = require("ontoloop.consumption")
        caller = iter([[1, 2], [3]])
        recorded = module.record_promotion(
            "r19 731 plain iterator control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(list(copied), [[1, 2], [3]])
        self.assertEqual(list(caller), [[1, 2], [3]])

    def test_plain_iterator_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        caller = iter([[1, 2], [3]])
        recorded = module.record_promotion(
            "r19 731 holder iterator control wf",
            {"part": Holder(caller)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertEqual(list(copied), [[1, 2], [3]])
        self.assertEqual(list(caller), [[1, 2], [3]])

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(_lock())},
            "r19 731 lock control wf",
        )


def _make_exception_lock():
    return ValueError(_lock()), None


def _make_exception_socket():
    left, right = _socket_pair()

    def cleanup():
        left.close()
        right.close()

    return ValueError(left), cleanup


def _make_exception_generator():
    return ValueError(_generator()), None


class TestRuling732ExceptionArguments(unittest.TestCase):
    """Ruling 732 (ISO-R19-3): exception arguments refused."""

    def test_exception_with_lock_argument_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_exception_lock, "732 exclock"
        )

    def test_exception_with_socket_argument_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_exception_socket, "732 excsocket"
        )

    def test_exception_with_generator_argument_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_exception_generator, "732 excgen"
        )

    def test_exception_with_plain_argument_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r19 732 plain argument control wf",
            {"part": Holder(ValueError([1, 2]))},
        )
        copied = recorded["bundle"]["part"].part
        self.assertEqual(copied.args, ([1, 2],))

    def test_exception_with_lock_attribute_still_refused(self):
        module = require("ontoloop.consumption")
        error = ValueError("plain")
        error.bad = _lock()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(error)},
            "r19 732 lock attribute control wf",
        )


def _make_logger():
    return logging.getLogger("r19.region4.probe"), None


def _make_logger_adapter():
    adapter = logging.LoggerAdapter(
        logging.getLogger("r19.region4.adapter"), {}
    )
    return adapter, None


def _make_pipe_connection():
    left, right = multiprocessing.Pipe()

    def cleanup():
        left.close()
        right.close()

    return left, cleanup


class TestRuling733SharedFormTypes(unittest.TestCase):
    """Ruling 733 (ISO-R19-4): shared form types refused."""

    def test_logger_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_logger, "733 logger")

    def test_logger_adapter_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_logger_adapter, "733 adapter"
        )

    def test_pipe_connection_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_pipe_connection, "733 pipeconn"
        )

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r19 733 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_null_handler_inside_holder_still_records_apart(self):
        module = require("ontoloop.consumption")
        original = logging.NullHandler()
        recorded = module.record_promotion(
            "r19 733 null handler control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertIsInstance(copied, logging.NullHandler)

    def test_socket_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        left, right = _socket_pair()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(left)},
                "r19 733 socket control wf",
            )
        finally:
            left.close()
            right.close()


if __name__ == "__main__":
    unittest.main()
