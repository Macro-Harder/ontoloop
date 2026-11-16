"""Fix round 21 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 21 triage
rulings 858 to 862: a PickleBuffer escaping the copy act
(ISO-R21-1, roster 2106), an uncopyable value in tree element
text, tail, or tag (ISO-R21-2), an uncopyable value standing
as a keyword argument of an operator methodcaller
specification (ISO-R21-3), an uncopyable callable standing
as the callable of a wider callable iterator form
(ISO-R21-4), and a globals view recursion in the
replacements limb through a view standing inside a container
in the globals mapping (ISO-R21-5). Each refused form stands
pinned at the whole bundle, direct bundle value, holder, and
nested list positions beside the standing controls its ruling
names, unless its ruling names the holder position alone.
"""

import bz2
import itertools
import operator
import pickle
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


class _Target:
    """A plain target for methodcaller call checks."""

    def fetch(self, key=None):
        return key


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
                "r21 " + label + " " + position + " wf",
            )
        finally:
            if cleanup is not None:
                cleanup()


def _lock():
    return threading.Lock()


def _make_pickle_buffer_bytes():
    return pickle.PickleBuffer(b"data"), None


def _make_pickle_buffer_bytearray():
    return pickle.PickleBuffer(bytearray(b"data")), None


class TestRuling858PickleBuffer(unittest.TestCase):
    """Ruling 858 (ISO-R21-1): PickleBuffer refused."""

    def test_pickle_buffer_over_bytes_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_pickle_buffer_bytes, "858 bytes"
        )

    def test_pickle_buffer_over_bytearray_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_pickle_buffer_bytearray, "858 barr"
        )

    def test_bz2_compressor_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(bz2.BZ2Compressor())},
            "r21 858 ruling 793 control wf",
        )

    def test_bytesio_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        import io

        recorded = module.record_promotion(
            "r21 858 bytesio control wf",
            {"part": Holder(io.BytesIO(b"data"))},
        )
        copied = recorded["bundle"]["part"].part
        self.assertEqual(copied.getvalue(), b"data")

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r21 858 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])


def _make_element_lock_text():
    element = _etree.Element("root")
    element.text = _lock()
    return element, None


def _make_element_lock_tail():
    child = _etree.Element("child")
    child.tail = _lock()
    element = _etree.Element("root")
    element.append(child)
    return element, None


def _make_element_lock_tag():
    element = _etree.Element("root")
    element.tag = _lock()
    return element, None


class TestRuling859TreeElementTextTailTag(unittest.TestCase):
    """Ruling 859 (ISO-R21-2): element text, tail, and tag reach."""

    def test_element_lock_text_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_element_lock_text, "859 text"
        )

    def test_element_lock_tail_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_element_lock_tail, "859 tail"
        )

    def test_element_lock_tag_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_element_lock_tag, "859 tag"
        )

    def test_plain_element_text_tail_tag_still_records_apart(self):
        module = require("ontoloop.consumption")
        element = _etree.Element("root")
        element.text = "hi"
        child = _etree.Element("child")
        child.tail = "bye"
        element.append(child)
        recorded = module.record_promotion(
            "r21 859 plain element control wf",
            {"part": Holder(element)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, element)
        self.assertEqual(copied.tag, "root")
        self.assertEqual(copied.text, "hi")
        self.assertEqual(list(copied)[0].tail, "bye")

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        element = _etree.Element("root", {"k": _lock()})
        _assert_uncopyable_refused(
            self, module, {"part": Holder(element)},
            "r21 859 lock attribute control wf",
        )


def _make_methodcaller_lock_keyword():
    return operator.methodcaller("fetch", key=_lock()), None


class TestRuling860MethodcallerKeywordArgument(unittest.TestCase):
    """Ruling 860 (ISO-R21-3): methodcaller keyword reach."""

    def test_methodcaller_lock_keyword_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_methodcaller_lock_keyword, "860 kw"
        )

    def test_methodcaller_plain_keyword_still_records(self):
        module = require("ontoloop.consumption")
        original = operator.methodcaller("fetch", key="plain")
        recorded = module.record_promotion(
            "r21 860 plain keyword control wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied(_Target()), "plain")

    def test_methodcaller_positional_lock_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(operator.methodcaller("get", _lock()))},
            "r21 860 positional control wf",
        )

    def test_attrgetter_plain_name_still_records(self):
        module = require("ontoloop.consumption")
        original = operator.attrgetter("real")
        recorded = module.record_promotion(
            "r21 860 attrgetter control wf", {"part": Holder(original)}
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertEqual(copied(complex(3, 4)), 3.0)

    def test_lock_at_walked_position_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(_lock())},
            "r21 860 lock control wf",
        )


def _make_map_lock():
    lock = _lock()
    return map(lock.acquire, [1]), None


def _make_starmap_lock():
    lock = _lock()
    return itertools.starmap(lock.acquire, [()]), None


def _make_takewhile_lock():
    lock = _lock()
    return itertools.takewhile(lock.acquire, [1]), None


def _make_dropwhile_lock():
    lock = _lock()
    return itertools.dropwhile(lock.acquire, [1]), None


def _make_filterfalse_lock():
    lock = _lock()
    return itertools.filterfalse(lock.acquire, [1]), None


def _make_groupby_lock():
    lock = _lock()
    return itertools.groupby([1], key=lock.acquire), None


def _make_accumulate_lock():
    lock = _lock()
    return itertools.accumulate([1, 2], lock.acquire), None


def _plain_predicate(value):
    return value > 1


def _plain_callable():
    return 42


class TestRuling861WiderCallableIterators(unittest.TestCase):
    """Ruling 861 (ISO-R21-4): wider callable iterator forms."""

    def test_map_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(self, module, _make_map_lock, "861 map")

    def test_starmap_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_starmap_lock, "861 starmap"
        )

    def test_takewhile_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_takewhile_lock, "861 takewhile"
        )

    def test_dropwhile_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_dropwhile_lock, "861 dropwhile"
        )

    def test_filterfalse_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_filterfalse_lock, "861 filterfalse"
        )

    def test_groupby_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_groupby_lock, "861 groupby"
        )

    def test_accumulate_bound_lock_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module, _make_accumulate_lock, "861 accumulate"
        )

    def test_refusal_exercises_no_callable(self):
        module = require("ontoloop.consumption")
        lock = _lock()
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(map(lock.acquire, [1]))},
            "r21 861 no exercise map wf",
        )
        self.assertFalse(lock.locked())
        lock = _lock()
        _assert_uncopyable_refused(
            self, module,
            {"part": Holder(itertools.takewhile(lock.acquire, [1]))},
            "r21 861 no exercise takewhile wf",
        )
        self.assertFalse(lock.locked())

    def test_map_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        caller = map(_plain_predicate, [1, 2])
        recorded = module.record_promotion(
            "r21 861 plain map control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(list(copied), [False, True])

    def test_takewhile_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        caller = itertools.takewhile(_plain_predicate, [2, 3, 1])
        recorded = module.record_promotion(
            "r21 861 plain takewhile control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(list(copied), [2, 3])

    def test_callable_iterator_plain_function_still_records(self):
        module = require("ontoloop.consumption")
        caller = iter(_plain_callable, 999)
        recorded = module.record_promotion(
            "r21 861 plain calliter control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(next(copied), 42)

    def test_plain_iterator_mutable_elements_still_record(self):
        module = require("ontoloop.consumption")
        caller = iter([[1, 2], [3]])
        recorded = module.record_promotion(
            "r21 861 plain iterator control wf", {"part": caller}
        )
        copied = recorded["bundle"]["part"]
        self.assertEqual(list(copied), [[1, 2], [3]])
        self.assertEqual(list(caller), [[1, 2], [3]])


def _template(value):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(_template.__code__, globals_map, "synthetic")


def _make_nested_view_function(container_kind):
    def make():
        globals_map = {"__builtins__": {}}
        view = globals_map.values()
        if container_kind == "list":
            globals_map["held"] = [view]
        elif container_kind == "dict":
            globals_map["held"] = {"inner": view}
        else:
            globals_map["held"] = (view,)
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        return func, None

    return make


class TestRuling862GlobalsViewInsideContainer(unittest.TestCase):
    """Ruling 862 (ISO-R21-5): self view inside a container."""

    def test_view_inside_list_in_globals_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_nested_view_function("list"), "862 list",
        )

    def test_view_inside_mapping_in_globals_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_nested_view_function("dict"), "862 dict",
        )

    def test_view_inside_tuple_in_globals_is_refused(self):
        module = require("ontoloop.consumption")
        _check_positions(
            self, module,
            _make_nested_view_function("tuple"), "862 tuple",
        )

    def test_function_over_plain_globals_still_records(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}, "held": [1, 2]}
        func = _synthetic_function(globals_map)
        recorded = module.record_promotion(
            "r21 862 plain globals control wf", {"part": Holder(func)}
        )
        self.assertIn("part", recorded["bundle"])

    def test_direct_self_view_still_refused(self):
        module = require("ontoloop.consumption")
        globals_map = {"__builtins__": {}}
        globals_map["view"] = globals_map.values()
        func = _synthetic_function(globals_map)
        globals_map["func"] = func
        _assert_uncopyable_refused(
            self, module, {"part": Holder(func)},
            "r21 862 ruling 798 control wf",
        )

    def test_ruling_622_view_of_another_mapping_still_records(self):
        module = require("ontoloop.consumption")
        source = {"k": [1]}
        shared = {"__builtins__": {}, "held": source.values()}
        first = _synthetic_function(shared)
        second = _synthetic_function(shared)
        recorded = module.record_promotion(
            "r21 862 ruling 622 control wf",
            {"first": first, "second": second},
        )
        bundle = recorded["bundle"]
        self.assertIs(
            bundle["first"].__globals__, bundle["second"].__globals__
        )
        self.assertIsNot(bundle["first"].__globals__, shared)
        self.assertEqual(bundle["first"].__globals__["held"], [[1]])


if __name__ == "__main__":
    unittest.main()
