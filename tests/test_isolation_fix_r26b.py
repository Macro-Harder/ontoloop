"""Fix round 26 tests for Region 8, the null handler cure.

Written test first against the final merged form of
ontoloop/consumption.py after Region 5, push 221. The defect
pole pins stand refused with the governed ValueError before
the cure in the erroring form the probe settled, a null
handler inside a holder raising ValueError, uncopyable value
in bundle copy, and record apart after the cure. The control
pins record or stand refused at both poles: a logger inside
a holder stands refused in its standing form, and a governed
value reached through the members of a class standing in a
non standard library globals mapping stands refused in its
standing transitive form.
"""

import logging
import sys
import threading
import types
import unittest

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"


class Holder:
    """A plain custom class instance, standing in no named form."""

    def __init__(self, part):
        self.part = part


def _assert_refused(case, module, bundle, workflow):
    with case.assertRaises(ValueError) as caught:
        module.record_promotion(workflow, bundle)
    case.assertEqual(str(caught.exception), UNCOPYABLE_MESSAGE)
    found = module.discover(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


_counter = [0]


def _make_module(body):
    _counter[0] += 1
    name = "r26_region8_mod_%d" % _counter[0]
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


class TestRegion8NullHandlerCure(unittest.TestCase):
    """Region 8: a null handler inside a holder records apart."""

    def test_null_handler_inside_holder_records_apart(self):
        module = require("ontoloop.consumption")
        original = logging.NullHandler()
        recorded = module.record_promotion(
            "r26 region8 null handler holder wf",
            {"part": Holder(original)},
        )
        copied = recorded["bundle"]["part"].part
        self.assertIsNot(copied, original)
        self.assertIsInstance(copied, logging.NullHandler)

    def test_null_handler_in_list_inside_holder_records_apart(self):
        module = require("ontoloop.consumption")
        original = logging.NullHandler()
        recorded = module.record_promotion(
            "r26 region8 null handler list wf",
            {"part": Holder([original])},
        )
        copied = recorded["bundle"]["part"].part[0]
        self.assertIsNot(copied, original)
        self.assertIsInstance(copied, logging.NullHandler)

    def test_plain_handler_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(logging.Handler())},
            "r26 region8 plain handler holder wf",
        )

    def test_logger_inside_holder_still_refused(self):
        module = require("ontoloop.consumption")
        _assert_refused(
            self, module,
            {"part": Holder(logging.getLogger("r26region8"))},
            "r26 region8 logger holder wf",
        )

    def test_plain_list_inside_holder_still_records(self):
        module = require("ontoloop.consumption")
        recorded = module.record_promotion(
            "r26 region8 plain list holder wf",
            {"part": Holder([1, 2])},
        )
        self.assertEqual(recorded["bundle"]["part"].part, [1, 2])

    def test_lock_through_member_of_non_stdlib_globals_still_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "class K:\n"
            "    def method(self):\n"
            "        return HELD\n"
        )
        _assert_refused(
            self, module,
            {"part": Holder(mod.K)},
            "r26 region8 non stdlib member lock wf",
        )

    def test_lock_through_helper_of_non_stdlib_globals_still_refused(self):
        module = require("ontoloop.consumption")
        mod = _make_module(
            "import threading\n"
            "HELD = threading.Lock()\n"
            "def helper():\n"
            "    return HELD\n"
            "class K:\n"
            "    def method(self):\n"
            "        return helper()\n"
        )
        _assert_refused(
            self, module,
            {"part": Holder(mod.K)},
            "r26 region8 non stdlib helper lock wf",
        )


if __name__ == "__main__":
    unittest.main()
