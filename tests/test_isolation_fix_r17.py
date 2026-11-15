"""Fix round 17 tests for Region 4: the isolation copy act.

Written test first for the positions charged at Round 17 triage
rulings 622 and 623: ruling 622, the ruling 574 sharing form at
two separate top level bundle values, cured with the globals
cache and the method landing memo carried at the level of the
one copy act, and ruling 623, the further uncopyable types
escaping with an ungoverned TypeError, a select poll object, a
sqlite3 cursor, a hashlib hash object, and an HMAC object.
Each class pins its cure beside the standing forms its charge
protects.
"""

import hashlib
import hmac
import select
import sqlite3
import types
import unittest

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


class PairHolder:
    """A plain custom class instance holding two parts."""

    def __init__(self, first, second):
        self.first = first
        self.second = second


class Service:
    def __init__(self):
        self.tags = ["original"]


def _template():
    return 1


def _template_method(self, value=None):
    return value


def _synthetic_function(globals_map):
    return types.FunctionType(_template.__code__, globals_map, "synthetic")


def _shared_pair():
    source = {"k": [1]}
    shared = {"__builtins__": {}, "held": source.values()}
    first = _synthetic_function(shared)
    second = _synthetic_function(shared)
    return source, shared, first, second


def _assert_shared_globals(case, module, workflow, first, second,
                           shared, source):
    case.assertIsNot(first, second)
    case.assertIs(first.__globals__, second.__globals__)
    case.assertIsNot(first.__globals__, shared)
    case.assertEqual(first.__globals__["held"], [[1]])
    first.__globals__["marker"] = "through first"
    case.assertEqual(second.__globals__.get("marker"), "through first")
    source["k"].append(99)
    found = module.discover(workflow)
    return found


def _assert_uncopyable_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


class TestRuling622SeparateTopLevelValues(unittest.TestCase):
    """Ruling 622 (ISO-R17-1): sharing across root bundle values."""

    def test_two_functions_as_bundle_mapping_values_share_globals(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        recorded = module.record_promotion(
            "r17 622 mapping values wf",
            {"first": first, "second": second},
        )
        returned = recorded["bundle"]
        found = _assert_shared_globals(
            self, module, "r17 622 mapping values wf",
            returned["first"], returned["second"], shared, source,
        )
        discovered = found["bundle"]
        self.assertIs(discovered["first"].__globals__,
                      discovered["second"].__globals__)
        self.assertEqual(discovered["first"].__globals__["held"], [[1]])

    def test_two_functions_as_bundle_list_elements_share_globals(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        recorded = module.record_promotion(
            "r17 622 list elements wf", {"part": [first, second]}
        )
        returned = recorded["bundle"]["part"]
        found = _assert_shared_globals(
            self, module, "r17 622 list elements wf",
            returned[0], returned[1], shared, source,
        )
        discovered = found["bundle"]["part"]
        self.assertIs(discovered[0].__globals__,
                      discovered[1].__globals__)

    def test_two_functions_as_bundle_tuple_elements_share_globals(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        recorded = module.record_promotion(
            "r17 622 tuple elements wf", {"part": (first, second)}
        )
        returned = recorded["bundle"]["part"]
        found = _assert_shared_globals(
            self, module, "r17 622 tuple elements wf",
            returned[0], returned[1], shared, source,
        )
        discovered = found["bundle"]["part"]
        self.assertIs(discovered[0].__globals__,
                      discovered[1].__globals__)

    def test_two_functions_in_separate_holders_share_globals(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        recorded = module.record_promotion(
            "r17 622 separate holders wf",
            {"first": Holder(first), "second": Holder(second)},
        )
        returned = recorded["bundle"]
        found = _assert_shared_globals(
            self, module, "r17 622 separate holders wf",
            returned["first"].part, returned["second"].part,
            shared, source,
        )
        discovered = found["bundle"]
        self.assertIs(discovered["first"].part.__globals__,
                      discovered["second"].part.__globals__)

    def test_two_functions_in_nested_mapping_values_share_globals(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        recorded = module.record_promotion(
            "r17 622 nested mapping wf",
            {"part": {"inner_first": first, "inner_second": second}},
        )
        returned = recorded["bundle"]["part"]
        found = _assert_shared_globals(
            self, module, "r17 622 nested mapping wf",
            returned["inner_first"], returned["inner_second"],
            shared, source,
        )
        discovered = found["bundle"]["part"]
        self.assertIs(discovered["inner_first"].__globals__,
                      discovered["inner_second"].__globals__)

    def test_rebuilt_bound_method_as_separate_value_shares_bound_object(self):
        module = require("ontoloop.consumption")
        source = {"k": ["v"]}
        service = Service()
        func = types.FunctionType(
            _template_method.__code__, {"__builtins__": {}},
            _template_method.__name__,
        )
        func.__defaults__ = (source.values(),)
        method = types.MethodType(func, service)
        recorded = module.record_promotion(
            "r17 622 separate method wf",
            {"svc": service, "meth": method},
        )
        returned = recorded["bundle"]
        self.assertIsNot(returned["svc"], service)
        self.assertIs(returned["meth"].__self__, returned["svc"])
        self.assertEqual(returned["meth"].__defaults__[0], [["v"]])
        source["k"].append(99)
        found = module.discover("r17 622 separate method wf")
        discovered = found["bundle"]
        self.assertIs(discovered["meth"].__self__, discovered["svc"])
        self.assertEqual(discovered["meth"].__defaults__[0], [["v"]])
        discovered["svc"].tags.append("copy side")
        self.assertEqual(discovered["meth"].__self__.tags,
                         ["original", "copy side"])
        self.assertEqual(service.tags, ["original"])

    def test_holder_form_of_ruling_574_still_shares_globals(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        holder = PairHolder(first, second)
        recorded = module.record_promotion(
            "r17 622 holder control wf", {"part": holder}
        )
        returned = recorded["bundle"]["part"]
        self.assertIs(returned.first.__globals__,
                      returned.second.__globals__)
        self.assertIsNot(returned.first.__globals__, shared)
        self.assertEqual(returned.first.__globals__["held"], [[1]])

    def test_separate_copy_acts_stand_apart(self):
        module = require("ontoloop.consumption")
        source, shared, first, second = _shared_pair()
        module.record_promotion(
            "r17 622 act one wf", {"first": first, "second": second}
        )
        module.record_promotion(
            "r17 622 act two wf", {"first": first, "second": second}
        )
        one = module.discover("r17 622 act one wf")["bundle"]
        two = module.discover("r17 622 act two wf")["bundle"]
        self.assertIs(one["first"].__globals__,
                      one["second"].__globals__)
        self.assertIs(two["first"].__globals__,
                      two["second"].__globals__)
        self.assertIsNot(one["first"].__globals__,
                         two["first"].__globals__)


class TestRuling623FurtherUncopyableTypes(unittest.TestCase):
    """Ruling 623 (ISO-R17-2): further uncopyable types refused."""

    def test_poll_object_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        poller = select.poll()
        _assert_uncopyable_refused(
            self, module, {"part": Holder(poller)},
            "r17 623 poll holder wf",
        )

    def test_poll_object_nested_in_list_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        poller = select.poll()
        _assert_uncopyable_refused(
            self, module, {"part": Holder([poller])},
            "r17 623 poll nested wf",
        )

    def test_sqlite_cursor_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        connection = sqlite3.connect(":memory:")
        try:
            cursor = connection.cursor()
            _assert_uncopyable_refused(
                self, module, {"part": Holder(cursor)},
                "r17 623 cursor holder wf",
            )
        finally:
            connection.close()

    def test_hashlib_hash_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        digest = hashlib.sha256(b"data")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(digest)},
            "r17 623 hash holder wf",
        )

    def test_hashlib_hash_as_direct_value_is_refused(self):
        module = require("ontoloop.consumption")
        digest = hashlib.sha256(b"data")
        _assert_uncopyable_refused(
            self, module, {"part": digest},
            "r17 623 hash direct wf",
        )

    def test_hmac_object_inside_holder_is_refused(self):
        module = require("ontoloop.consumption")
        mac = hmac.new(b"key", b"message", "sha256")
        _assert_uncopyable_refused(
            self, module, {"part": Holder(mac)},
            "r17 623 hmac holder wf",
        )

    def test_sqlite_connection_control_still_refused(self):
        module = require("ontoloop.consumption")
        connection = sqlite3.connect(":memory:")
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(connection)},
                "r17 623 connection control wf",
            )
        finally:
            connection.close()

    def test_epoll_control_still_refused(self):
        module = require("ontoloop.consumption")
        poller = select.epoll()
        try:
            _assert_uncopyable_refused(
                self, module, {"part": Holder(poller)},
                "r17 623 epoll control wf",
            )
        finally:
            poller.close()

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r17 623 plain list control wf", {"part": Holder([1, 2])}
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])


if __name__ == "__main__":
    unittest.main()
