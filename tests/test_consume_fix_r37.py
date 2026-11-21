"""Fix round 37 tests for rulings 2444 to 2482, Regions 5 and 6.

Written test first against the governing base form of
ontoloop/consumption.py at system head
cbde686aba695294de35930a11c4d74c356af263. Each ruling stands
pinned at both poles in the form its triage ruling states:
the defective forms stand decided in substance after the
cure, and the standing poles and clean controls its ruling
names stand in their standing forms at both poles.
"""

import sys
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


def _assert_refused_both(case, module, service, bundle, workflow):
    _assert_refused(case, module, bundle, workflow)
    found = service.discover_tool(workflow)
    case.assertEqual(found["answer"], "no promotion")
    case.assertIsNone(found["bundle"])


def _assert_records(case, module, bundle, workflow):
    recorded = module.record_promotion(workflow, bundle)
    case.assertTrue(recorded["recorded"])
    return recorded


_counter = [0]


def _make_module(body, name_hint="r37_region56_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r37_region56_sub")


def _chain_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r37_region56_inner",
    )
    outer = _make_module("", "r37_region56_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r37_region56_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
    return home


def _pair_home(source, carrier_body, extra="", with_target=False):
    carrier = _make_module(carrier_body, "r37_region56_carrier")
    home = _make_module(extra + source)
    home.__dict__["CARRIER"] = carrier
    if with_target:
        home.__dict__["MOD"] = _sub_module()
    return home


def _check3(case, module, service, home, label):
    _assert_refused_both(
        case, module, service, {"part": home.K}, label + " class wf"
    )
    _assert_refused_both(
        case, module, service, {"part": home.K()},
        label + " instance wf",
    )
    _assert_refused_both(
        case, module, service, {"part": Holder(home.K)},
        label + " holder wf",
    )


def _records3(case, module, home, label):
    _assert_records(
        case, module, {"part": home.K}, label + " class wf"
    )
    _assert_records(
        case, module, {"part": home.K()}, label + " instance wf"
    )
    _assert_records(
        case, module, {"part": Holder(home.K)}, label + " holder wf"
    )


def _mods(case):
    return require("ontoloop.consumption"), require(
        "ontoloop.service_layer"
    )


_HOME_TAIL = (
    "import threading\nHELD = threading.Lock()\nPLAIN = 7\n"
)

_HOME_SRC = (
    "class K:\n    def method(self):\n"
    "        return globals()[helper()]\n"
)
_GA_SRC = (
    "class K:\n    def method(self):\n"
    "        return getattr(MOD, helper())\n"
)
_GS_SRC = (
    "class K:\n    def method(self):\n"
    "        return MOD.__dict__[helper()]\n"
)

_CHAIR_GA = (
    "class K:\n    def method(self):\n"
    "        return getattr(getmod(), 'HELD')\n"
)
_CHAIR_VS = (
    "class K:\n    def method(self):\n"
    "        return vars(getmod())['HELD']\n"
)
_CHAIR_DS = (
    "class K:\n    def method(self):\n"
    "        return getmod().__dict__['HELD']\n"
)
_CHAIR_EX = (
    "class K:\n    def method(self):\n"
    "        loc = {}\n"
    "        exec('x = HELD', getmod().__dict__, loc)\n"
    "        return loc['x']\n"
)


def _chair(case, source, extra, label, plain=False):
    module, service = _mods(case)
    home = _chain_home(source, extra)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR37Chair1ProducedName(unittest.TestCase):
    """Ruling 2444: vars subscript return under a produced name."""

    def test_2444_list_set_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k={'INNER'}):\n"
            "    return vars(OUTER)[list(_k)[0]]\n",
            "r37 2444 f1",
        )

    def test_2444_tuple_set_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k={'INNER'}):\n"
            "    return vars(OUTER)[tuple(_k)[0]]\n",
            "r37 2444 f2",
        )

    def test_2444_list_dict_default_vars_subscript(self):
        _chair(
            self, _CHAIR_VS,
            "def getmod(_k={'INNER': 1}):\n"
            "    return vars(OUTER)[list(_k)[0]]\n",
            "r37 2444 f3",
        )

    def test_2444_list_dict_default_exec(self):
        _chair(
            self, _CHAIR_EX,
            "def getmod(_k={'INNER': 1}):\n"
            "    return vars(OUTER)[list(_k)[0]]\n",
            "r37 2444 f4",
        )

    def test_2444_list_set_default_dict_subscript(self):
        _chair(
            self, _CHAIR_DS,
            "def getmod(_k={'INNER'}):\n"
            "    return vars(OUTER)[list(_k)[0]]\n",
            "r37 2444 f5",
        )

    def test_2444_list_globals_set_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "KEYS = {'INNER'}\n"
            "def getmod():\n"
            "    return vars(OUTER)[list(KEYS)[0]]\n",
            "r37 2444 f6",
        )

    def test_2444_list_closure_set_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def _fac():\n    _k = {'INNER'}\n    def getmod():\n"
            "        return vars(OUTER)[list(_k)[0]]\n"
            "    return getmod\n"
            "getmod = _fac()\n",
            "r37 2444 f7",
        )

    def test_2444_tuple_frozenset_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k=frozenset({'INNER'})):\n"
            "    return vars(OUTER)[tuple(_k)[0]]\n",
            "r37 2444 f8",
        )

    def test_2444_next_iter_dict_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k={'INNER': 1}):\n"
            "    return vars(OUTER)[next(iter(_k))]\n",
            "r37 2444 f9",
        )

    def test_2444_list_keys_dict_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k={'INNER': 1}):\n"
            "    return vars(OUTER)[list(_k.keys())[0]]\n",
            "r37 2444 f10",
        )

    def test_2444_sorted_list_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k=['INNER']):\n"
            "    return vars(OUTER)[sorted(_k)[0]]\n",
            "r37 2444 f11",
        )

    def test_2444_copy_list_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k=['INNER']):\n"
            "    return vars(OUTER)[_k.copy()[0]]\n",
            "r37 2444 f12",
        )

    def test_2444_conditional_list_default_getattr(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k=['INNER']):\n"
            "    return vars(OUTER)[('INNER' if _k else 'X')]\n",
            "r37 2444 f13",
        )

    def test_2444_plain_records(self):
        _chair(
            self,
            "class K:\n    def method(self):\n"
            "        return getattr(getmod(), 'PLAIN')\n",
            "def getmod(_k={'INNER'}):\n"
            "    return vars(OUTER)[list(_k)[0]]\n",
            "r37 2444 plain",
            plain=True,
        )

    def test_2444_direct_element_pole(self):
        _chair(
            self, _CHAIR_GA,
            "def getmod(_k=('INNER',)):\n"
            "    return vars(OUTER)[_k[0]]\n",
            "r37 2444 pole",
        )


_FIFTH_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def fifth():\n"
    "        return _n\n    return fifth\n"
    "fifth = _fac()\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FIFTH_STRING = (
    "STR = 'HELD'\n"
    "def fifth():\n    return STR\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FIFTH_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def fifth():\n    return D['k']\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FIFTH_DEFAULT = (
    "def fifth(_n='HELD'):\n    return _n\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_CLOSURE_POLE = (
    "def _fac():\n    _n = 'HELD'\n    def fourth():\n"
    "        return _n\n    return fourth\n"
    "fourth = _fac()\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_STRING_POLE = (
    "STR = 'HELD'\n"
    "def fourth():\n    return STR\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_CONTAINER_POLE = (
    "D = {'k': 'HELD'}\n"
    "def fourth():\n    return D['k']\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL

_FOURTH_DEFAULT_POLE = (
    "def fourth(_n='HELD'):\n    return _n\n"
    "def third():\n    return fourth()\n"
    "def inner():\n    return third()\n"
    "def helper():\n    return inner()\n"
) + _HOME_TAIL


def _fifth_home(case, source, body, label):
    module, service = _mods(case)
    home = _target_home(source, body)
    _check3(case, module, service, home, label)


def _fifth_plain(case, source, body, label):
    module, service = _mods(case)
    home = _target_home(source, body.replace("'HELD'", "'PLAIN'"))
    _records3(case, module, home, label)


class TestConsumeFixR37Consume1FifthClosureHome(
    unittest.TestCase
):
    """Ruling 2445: fifth order closure name at the home map."""

    def test_2445_home_index(self):
        _fifth_home(
            self, _HOME_SRC, _FIFTH_CLOSURE, "r37 2445 home"
        )

    def test_2445_plain_records(self):
        _fifth_plain(
            self, _HOME_SRC, _FIFTH_CLOSURE, "r37 2445 plain"
        )

    def test_2445_fourth_order_pole(self):
        _fifth_home(
            self, _HOME_SRC, _FOURTH_CLOSURE_POLE, "r37 2445 pole"
        )


class TestConsumeFixR37Consume2FifthClosureForeign(
    unittest.TestCase
):
    """Ruling 2446: fifth order closure name, foreign module."""

    def test_2446_foreign_getattr(self):
        _fifth_home(
            self, _GA_SRC, _FIFTH_CLOSURE, "r37 2446 ga"
        )

    def test_2446_foreign_dict_subscript(self):
        _fifth_home(
            self, _GS_SRC, _FIFTH_CLOSURE, "r37 2446 gs"
        )

    def test_2446_plain_records(self):
        _fifth_plain(
            self, _GA_SRC, _FIFTH_CLOSURE, "r37 2446 plain"
        )


class TestConsumeFixR37Consume3FifthStringHome(
    unittest.TestCase
):
    """Ruling 2447: fifth order module string at the home map."""

    def test_2447_home_index(self):
        _fifth_home(
            self, _HOME_SRC, _FIFTH_STRING, "r37 2447 home"
        )

    def test_2447_plain_records(self):
        _fifth_plain(
            self, _HOME_SRC, _FIFTH_STRING, "r37 2447 plain"
        )

    def test_2447_fourth_order_pole(self):
        _fifth_home(
            self, _HOME_SRC, _FOURTH_STRING_POLE, "r37 2447 pole"
        )


class TestConsumeFixR37Consume4FifthStringForeign(
    unittest.TestCase
):
    """Ruling 2448: fifth order module string, foreign module."""

    def test_2448_foreign_getattr(self):
        _fifth_home(self, _GA_SRC, _FIFTH_STRING, "r37 2448 ga")

    def test_2448_foreign_dict_subscript(self):
        _fifth_home(self, _GS_SRC, _FIFTH_STRING, "r37 2448 gs")

    def test_2448_plain_records(self):
        _fifth_plain(
            self, _GA_SRC, _FIFTH_STRING, "r37 2448 plain"
        )


class TestConsumeFixR37Consume5FifthContainerHome(
    unittest.TestCase
):
    """Ruling 2449: fifth order container element, home map."""

    def test_2449_home_index(self):
        _fifth_home(
            self, _HOME_SRC, _FIFTH_CONTAINER, "r37 2449 home"
        )

    def test_2449_plain_records(self):
        _fifth_plain(
            self, _HOME_SRC, _FIFTH_CONTAINER, "r37 2449 plain"
        )

    def test_2449_fourth_order_pole(self):
        _fifth_home(
            self, _HOME_SRC, _FOURTH_CONTAINER_POLE,
            "r37 2449 pole",
        )


class TestConsumeFixR37Consume6FifthContainerForeign(
    unittest.TestCase
):
    """Ruling 2450: fifth order container element, foreign."""

    def test_2450_foreign_getattr(self):
        _fifth_home(
            self, _GA_SRC, _FIFTH_CONTAINER, "r37 2450 ga"
        )

    def test_2450_foreign_dict_subscript(self):
        _fifth_home(
            self, _GS_SRC, _FIFTH_CONTAINER, "r37 2450 gs"
        )

    def test_2450_plain_records(self):
        _fifth_plain(
            self, _GA_SRC, _FIFTH_CONTAINER, "r37 2450 plain"
        )


class TestConsumeFixR37Consume7FifthDefaultHome(
    unittest.TestCase
):
    """Ruling 2451: fifth order default name at the home map."""

    def test_2451_home_index(self):
        _fifth_home(
            self, _HOME_SRC, _FIFTH_DEFAULT, "r37 2451 home"
        )

    def test_2451_plain_records(self):
        _fifth_plain(
            self, _HOME_SRC, _FIFTH_DEFAULT, "r37 2451 plain"
        )

    def test_2451_fourth_order_pole(self):
        _fifth_home(
            self, _HOME_SRC, _FOURTH_DEFAULT_POLE, "r37 2451 pole"
        )


class TestConsumeFixR37Consume8FifthDefaultForeign(
    unittest.TestCase
):
    """Ruling 2452: fifth order default name, foreign module."""

    def test_2452_foreign_getattr(self):
        _fifth_home(self, _GA_SRC, _FIFTH_DEFAULT, "r37 2452 ga")

    def test_2452_foreign_dict_subscript(self):
        _fifth_home(self, _GS_SRC, _FIFTH_DEFAULT, "r37 2452 gs")

    def test_2452_plain_records(self):
        _fifth_plain(
            self, _GA_SRC, _FIFTH_DEFAULT, "r37 2452 plain"
        )


_PAIR_INNER2_STRING = (
    "STR = 'HELD'\n"
    "def inner2():\n    return STR\n"
    "def inner():\n    return inner2()\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_INNER2_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def inner2():\n    return D['k']\n"
    "def inner():\n    return inner2()\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_INNER2_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def inner2():\n"
    "        return _n\n    return inner2\n"
    "inner2 = _fac()\n"
    "def inner():\n    return inner2()\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_INNER2_DEFAULT = (
    "def inner2(_n='HELD'):\n    return _n\n"
    "def inner():\n    return inner2()\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_POLE_STRING = (
    "STR = 'HELD'\n"
    "def inner():\n    return STR\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_POLE_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def inner():\n    return D['k']\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_POLE_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def inner():\n"
    "        return _n\n    return inner\n"
    "inner = _fac()\n"
    "def pairfn():\n    return inner()\n"
)
_PAIR_POLE_DEFAULT = (
    "def inner(_n='HELD'):\n    return _n\n"
    "def pairfn():\n    return inner()\n"
)


def _pair_inner2_home(case, source, carrier, label, plain=False,
                      helpers=1):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    if helpers == 1:
        extra = (
            "def helper():\n    return CARRIER.pairfn()\n"
        ) + _HOME_TAIL
    else:
        extra = (
            "def helper2():\n    return CARRIER.pairfn()\n"
            "def helper():\n    return helper2()\n"
        ) + _HOME_TAIL
    home = _pair_home(source, body, extra, with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR37Consume9PairInner2StringHome(
    unittest.TestCase
):
    """Ruling 2453: pair inner inner module string, home map."""

    def test_2453_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_STRING, "r37 2453 home"
        )

    def test_2453_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_STRING,
            "r37 2453 plain", plain=True,
        )

    def test_2453_pair_inner_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_STRING, "r37 2453 pole"
        )


class TestConsumeFixR37Consume10PairInner2StringForeign(
    unittest.TestCase
):
    """Ruling 2454: pair inner inner module string, foreign."""

    def test_2454_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_STRING, "r37 2454 ga"
        )

    def test_2454_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_STRING, "r37 2454 gs"
        )

    def test_2454_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_STRING,
            "r37 2454 plain", plain=True,
        )


class TestConsumeFixR37Consume11PairInner2ContainerHome(
    unittest.TestCase
):
    """Ruling 2455: pair inner inner container element, home."""

    def test_2455_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2455 home",
        )

    def test_2455_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2455 plain", plain=True,
        )

    def test_2455_pair_inner_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_CONTAINER,
            "r37 2455 pole",
        )


class TestConsumeFixR37Consume12PairInner2ContainerForeign(
    unittest.TestCase
):
    """Ruling 2456: pair inner inner container element, foreign."""

    def test_2456_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CONTAINER, "r37 2456 ga"
        )

    def test_2456_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_CONTAINER, "r37 2456 gs"
        )

    def test_2456_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2456 plain", plain=True,
        )


class TestConsumeFixR37Consume13PairInner2ClosureHome(
    unittest.TestCase
):
    """Ruling 2457: pair inner inner closure name, home map."""

    def test_2457_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CLOSURE, "r37 2457 home"
        )

    def test_2457_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CLOSURE,
            "r37 2457 plain", plain=True,
        )

    def test_2457_pair_inner_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_CLOSURE, "r37 2457 pole"
        )


class TestConsumeFixR37Consume14PairInner2ClosureForeign(
    unittest.TestCase
):
    """Ruling 2458: pair inner inner closure name, foreign."""

    def test_2458_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CLOSURE, "r37 2458 ga"
        )

    def test_2458_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_CLOSURE, "r37 2458 gs"
        )

    def test_2458_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CLOSURE,
            "r37 2458 plain", plain=True,
        )


class TestConsumeFixR37Consume15PairInner2DefaultHome(
    unittest.TestCase
):
    """Ruling 2459: pair inner inner default name, home map."""

    def test_2459_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_DEFAULT, "r37 2459 home"
        )

    def test_2459_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_DEFAULT,
            "r37 2459 plain", plain=True,
        )

    def test_2459_pair_inner_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_DEFAULT, "r37 2459 pole"
        )


class TestConsumeFixR37Consume16PairInner2DefaultForeign(
    unittest.TestCase
):
    """Ruling 2460: pair inner inner default name, foreign."""

    def test_2460_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_DEFAULT, "r37 2460 ga"
        )

    def test_2460_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_DEFAULT, "r37 2460 gs"
        )

    def test_2460_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_DEFAULT,
            "r37 2460 plain", plain=True,
        )


def _mp_source(call, act):
    if act == "ga":
        return (
            "class K:\n    def method(self):\n"
            "        return getattr(MOD, %s)\n" % call
        )
    return (
        "class K:\n    def method(self):\n"
        "        return MOD.__dict__[%s]\n" % call
    )


def _member_pair2(case, carrier, act, label, plain=False):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _pair_home(
        _mp_source("CARRIER.pairfn()", act), body, "",
        with_target=True,
    )
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR37Consume17MemberPairInner2String(
    unittest.TestCase
):
    """Ruling 2461: member direct pair inner inner string."""

    def test_2461_foreign_getattr(self):
        _member_pair2(
            self, _PAIR_INNER2_STRING, "ga", "r37 2461 ga"
        )

    def test_2461_foreign_dict_subscript(self):
        _member_pair2(
            self, _PAIR_INNER2_STRING, "gs", "r37 2461 gs"
        )

    def test_2461_plain_records(self):
        _member_pair2(
            self, _PAIR_INNER2_STRING, "ga", "r37 2461 plain",
            plain=True,
        )


class TestConsumeFixR37Consume18MemberPairInner2Container(
    unittest.TestCase
):
    """Ruling 2462: member direct pair inner inner container."""

    def test_2462_foreign_getattr(self):
        _member_pair2(
            self, _PAIR_INNER2_CONTAINER, "ga", "r37 2462 ga"
        )

    def test_2462_foreign_dict_subscript(self):
        _member_pair2(
            self, _PAIR_INNER2_CONTAINER, "gs", "r37 2462 gs"
        )

    def test_2462_plain_records(self):
        _member_pair2(
            self, _PAIR_INNER2_CONTAINER, "ga", "r37 2462 plain",
            plain=True,
        )


class TestConsumeFixR37Consume19MemberPairInner2Closure(
    unittest.TestCase
):
    """Ruling 2463: member direct pair inner inner closure."""

    def test_2463_foreign_getattr(self):
        _member_pair2(
            self, _PAIR_INNER2_CLOSURE, "ga", "r37 2463 ga"
        )

    def test_2463_foreign_dict_subscript(self):
        _member_pair2(
            self, _PAIR_INNER2_CLOSURE, "gs", "r37 2463 gs"
        )

    def test_2463_plain_records(self):
        _member_pair2(
            self, _PAIR_INNER2_CLOSURE, "ga", "r37 2463 plain",
            plain=True,
        )


class TestConsumeFixR37Consume20MemberPairInner2Default(
    unittest.TestCase
):
    """Ruling 2464: member direct pair inner inner default."""

    def test_2464_foreign_getattr(self):
        _member_pair2(
            self, _PAIR_INNER2_DEFAULT, "ga", "r37 2464 ga"
        )

    def test_2464_foreign_dict_subscript(self):
        _member_pair2(
            self, _PAIR_INNER2_DEFAULT, "gs", "r37 2464 gs"
        )

    def test_2464_plain_records(self):
        _member_pair2(
            self, _PAIR_INNER2_DEFAULT, "ga", "r37 2464 plain",
            plain=True,
        )


class TestConsumeFixR37Consume21DeepPairInnerStringHome(
    unittest.TestCase
):
    """Ruling 2465: deep pair inner module string, home map."""

    def test_2465_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_STRING,
            "r37 2465 home", helpers=2,
        )

    def test_2465_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_STRING,
            "r37 2465 plain", plain=True, helpers=2,
        )

    def test_2465_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_STRING,
            "r37 2465 pole", helpers=1,
        )


class TestConsumeFixR37Consume22DeepPairInnerStringForeign(
    unittest.TestCase
):
    """Ruling 2466: deep pair inner module string, foreign."""

    def test_2466_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_STRING, "r37 2466 ga",
            helpers=2,
        )

    def test_2466_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_STRING, "r37 2466 gs",
            helpers=2,
        )

    def test_2466_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_STRING,
            "r37 2466 plain", plain=True, helpers=2,
        )


class TestConsumeFixR37Consume23DeepPairInnerContainerHome(
    unittest.TestCase
):
    """Ruling 2467: deep pair inner container element, home."""

    def test_2467_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2467 home", helpers=2,
        )

    def test_2467_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2467 plain", plain=True, helpers=2,
        )

    def test_2467_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_CONTAINER,
            "r37 2467 pole", helpers=1,
        )


class TestConsumeFixR37Consume24DeepPairInnerContainerForeign(
    unittest.TestCase
):
    """Ruling 2468: deep pair inner container element, foreign."""

    def test_2468_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2468 ga", helpers=2,
        )

    def test_2468_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2468 gs", helpers=2,
        )

    def test_2468_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CONTAINER,
            "r37 2468 plain", plain=True, helpers=2,
        )


class TestConsumeFixR37Consume25DeepPairInnerClosureHome(
    unittest.TestCase
):
    """Ruling 2469: deep pair inner closure name, home map."""

    def test_2469_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CLOSURE,
            "r37 2469 home", helpers=2,
        )

    def test_2469_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_CLOSURE,
            "r37 2469 plain", plain=True, helpers=2,
        )

    def test_2469_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_CLOSURE,
            "r37 2469 pole", helpers=1,
        )


class TestConsumeFixR37Consume26DeepPairInnerClosureForeign(
    unittest.TestCase
):
    """Ruling 2470: deep pair inner closure name, foreign."""

    def test_2470_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CLOSURE, "r37 2470 ga",
            helpers=2,
        )

    def test_2470_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_CLOSURE, "r37 2470 gs",
            helpers=2,
        )

    def test_2470_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_CLOSURE,
            "r37 2470 plain", plain=True, helpers=2,
        )


class TestConsumeFixR37Consume27DeepPairInnerDefaultHome(
    unittest.TestCase
):
    """Ruling 2471: deep pair inner default name, home map."""

    def test_2471_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_DEFAULT,
            "r37 2471 home", helpers=2,
        )

    def test_2471_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_INNER2_DEFAULT,
            "r37 2471 plain", plain=True, helpers=2,
        )

    def test_2471_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_POLE_DEFAULT,
            "r37 2471 pole", helpers=1,
        )


class TestConsumeFixR37Consume28DeepPairInnerDefaultForeign(
    unittest.TestCase
):
    """Ruling 2472: deep pair inner default name, foreign."""

    def test_2472_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_DEFAULT, "r37 2472 ga",
            helpers=2,
        )

    def test_2472_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_INNER2_DEFAULT, "r37 2472 gs",
            helpers=2,
        )

    def test_2472_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_INNER2_DEFAULT,
            "r37 2472 plain", plain=True, helpers=2,
        )


_PAIR_SELF_STRING = (
    "STR = 'HELD'\n"
    "def pairfn():\n    return STR\n"
)
_PAIR_SELF_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def pairfn():\n    return D['k']\n"
)
_PAIR_SELF_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def pairfn():\n"
    "        return _n\n    return pairfn\n"
    "pairfn = _fac()\n"
)
_PAIR_SELF_DEFAULT = (
    "def pairfn(_n='HELD'):\n    return _n\n"
)


class TestConsumeFixR37Consume29DeepPairSelfStringHome(
    unittest.TestCase
):
    """Ruling 2473: deep pair self module string, home map."""

    def test_2473_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_STRING, "r37 2473 home",
            helpers=2,
        )

    def test_2473_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_STRING,
            "r37 2473 plain", plain=True, helpers=2,
        )

    def test_2473_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_STRING, "r37 2473 pole",
            helpers=1,
        )


class TestConsumeFixR37Consume30DeepPairSelfStringForeign(
    unittest.TestCase
):
    """Ruling 2474: deep pair self module string, foreign."""

    def test_2474_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_STRING, "r37 2474 ga",
            helpers=2,
        )

    def test_2474_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_SELF_STRING, "r37 2474 gs",
            helpers=2,
        )

    def test_2474_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_STRING,
            "r37 2474 plain", plain=True, helpers=2,
        )


class TestConsumeFixR37Consume31DeepPairSelfContainerHome(
    unittest.TestCase
):
    """Ruling 2475: deep pair self container element, home."""

    def test_2475_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_CONTAINER,
            "r37 2475 home", helpers=2,
        )

    def test_2475_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_CONTAINER,
            "r37 2475 plain", plain=True, helpers=2,
        )

    def test_2475_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_CONTAINER,
            "r37 2475 pole", helpers=1,
        )


class TestConsumeFixR37Consume32DeepPairSelfContainerForeign(
    unittest.TestCase
):
    """Ruling 2476: deep pair self container element, foreign."""

    def test_2476_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_CONTAINER, "r37 2476 ga",
            helpers=2,
        )

    def test_2476_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_SELF_CONTAINER, "r37 2476 gs",
            helpers=2,
        )

    def test_2476_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_CONTAINER,
            "r37 2476 plain", plain=True, helpers=2,
        )


class TestConsumeFixR37Consume33DeepPairSelfClosureHome(
    unittest.TestCase
):
    """Ruling 2477: deep pair self closure name, home map."""

    def test_2477_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_CLOSURE, "r37 2477 home",
            helpers=2,
        )

    def test_2477_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_CLOSURE,
            "r37 2477 plain", plain=True, helpers=2,
        )

    def test_2477_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_CLOSURE,
            "r37 2477 pole", helpers=1,
        )


class TestConsumeFixR37Consume34DeepPairSelfClosureForeign(
    unittest.TestCase
):
    """Ruling 2478: deep pair self closure name, foreign."""

    def test_2478_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_CLOSURE, "r37 2478 ga",
            helpers=2,
        )

    def test_2478_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_SELF_CLOSURE, "r37 2478 gs",
            helpers=2,
        )

    def test_2478_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_CLOSURE,
            "r37 2478 plain", plain=True, helpers=2,
        )


class TestConsumeFixR37Consume35DeepPairSelfDefaultHome(
    unittest.TestCase
):
    """Ruling 2479: deep pair self default name, home map."""

    def test_2479_home_index(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_DEFAULT, "r37 2479 home",
            helpers=2,
        )

    def test_2479_plain_records(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_DEFAULT,
            "r37 2479 plain", plain=True, helpers=2,
        )

    def test_2479_single_helper_pole(self):
        _pair_inner2_home(
            self, _HOME_SRC, _PAIR_SELF_DEFAULT,
            "r37 2479 pole", helpers=1,
        )


class TestConsumeFixR37Consume36DeepPairSelfDefaultForeign(
    unittest.TestCase
):
    """Ruling 2480: deep pair self default name, foreign."""

    def test_2480_foreign_getattr(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_DEFAULT, "r37 2480 ga",
            helpers=2,
        )

    def test_2480_foreign_dict_subscript(self):
        _pair_inner2_home(
            self, _GS_SRC, _PAIR_SELF_DEFAULT, "r37 2480 gs",
            helpers=2,
        )

    def test_2480_plain_records(self):
        _pair_inner2_home(
            self, _GA_SRC, _PAIR_SELF_DEFAULT,
            "r37 2480 plain", plain=True, helpers=2,
        )


def _six_hop_home(source, cls_name="HELD"):
    leaf = _make_module(
        "import threading\n"
        "PLAIN = 7\nHELD = threading.Lock()\n",
        "r37_region56_leaf6",
    )
    l4 = _make_module("", "r37_region56_l4")
    l4.__dict__["LEAF"] = leaf
    l3 = _make_module("", "r37_region56_l3")
    l3.__dict__["L4"] = l4
    l2 = _make_module("", "r37_region56_l2")
    l2.__dict__["L3"] = l3
    l1 = _make_module("", "r37_region56_l1")
    l1.__dict__["L2"] = l2
    outer = _make_module("", "r37_region56_outer6")
    outer.__dict__["L1"] = l1
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    home.__dict__["Cls"] = type("Cls", (), {"NAME": cls_name})
    return home


def _five_hop_home(source, cls_name="HELD"):
    leaf = _make_module(
        "import threading\n"
        "PLAIN = 7\nHELD = threading.Lock()\n",
        "r37_region56_leaf5",
    )
    l3 = _make_module("", "r37_region56_l3b")
    l3.__dict__["LEAF"] = leaf
    l2 = _make_module("", "r37_region56_l2b")
    l2.__dict__["L3"] = l3
    l1 = _make_module("", "r37_region56_l1b")
    l1.__dict__["L2"] = l2
    outer = _make_module("", "r37_region56_outer5")
    outer.__dict__["L1"] = l1
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    home.__dict__["Cls"] = type("Cls", (), {"NAME": cls_name})
    return home


class TestConsumeFixR37Iso1SixthHopChain(unittest.TestCase):
    """Ruling 2481: governed value at the sixth hop of a chain."""

    def test_2481_getattr_gathered(self):
        module, service = _mods(self)
        home = _six_hop_home(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            OUTER.L1.L2.L3.L4.LEAF, Cls.NAME\n"
            "        )\n"
        )
        _check3(self, module, service, home, "r37 2481 ga")

    def test_2481_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _six_hop_home(
            "class K:\n    def method(self):\n"
            "        return OUTER.L1.L2.L3.L4.LEAF.__dict__[\n"
            "            'HELD'\n"
            "        ]\n"
        )
        _check3(self, module, service, home, "r37 2481 ds")

    def test_2481_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _six_hop_home(
            "class K:\n    def method(self):\n"
            "        return vars(OUTER.L1.L2.L3.L4.LEAF)[\n"
            "            Cls.NAME\n"
            "        ]\n"
        )
        _check3(self, module, service, home, "r37 2481 vs")

    def test_2481_exec_dict_form(self):
        module, service = _mods(self)
        home = _six_hop_home(
            "class K:\n    def method(self):\n"
            "        loc = {}\n"
            "        exec(\n"
            "            'x = HELD',\n"
            "            OUTER.L1.L2.L3.L4.LEAF.__dict__, loc,\n"
            "        )\n"
            "        return loc['x']\n"
        )
        _check3(self, module, service, home, "r37 2481 ex")

    def test_2481_plain_records(self):
        module, service = _mods(self)
        home = _six_hop_home(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            OUTER.L1.L2.L3.L4.LEAF, Cls.NAME\n"
            "        )\n",
            cls_name="PLAIN",
        )
        _records3(self, module, home, "r37 2481 plain")

    def test_2481_fifth_hop_pole(self):
        module, service = _mods(self)
        home = _five_hop_home(
            "class K:\n    def method(self):\n"
            "        return getattr(\n"
            "            OUTER.L1.L2.L3.LEAF, Cls.NAME\n"
            "        )\n"
        )
        _check3(self, module, service, home, "r37 2481 pole")


_ISO2_CLOSURE = (
    "def _fac():\n    _n = 'HELD'\n    def fifth():\n"
    "        return _n\n    return fifth\n"
    "fifth = _fac()\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO2_STRING = (
    "STR = 'HELD'\n"
    "def fifth():\n    return STR\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO2_CONTAINER = (
    "D = ['HELD']\n"
    "def fifth():\n    return D[0]\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO2_DEFAULT = (
    "def fifth(_n='HELD'):\n    return _n\n"
    "def fourth():\n    return fifth()\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)
_ISO2_FOURTH_POLE = (
    "def _fac():\n    _n = 'HELD'\n    def fourth():\n"
    "        return _n\n    return fourth\n"
    "fourth = _fac()\n"
    "def third():\n    return fourth()\n"
    "def second():\n    return third()\n"
    "def mid():\n    return second()\n"
)

_ISO2_HOME = (
    "class K:\n    def method(self):\n"
    "        return globals()[mid()]\n"
)
_ISO2_GA = (
    "class K:\n    def method(self):\n"
    "        return getattr(MOD, mid())\n"
)


def _iso2_home(case, source, body, label, plain=False):
    module, service = _mods(case)
    text = body
    if plain:
        text = text.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, text + _HOME_TAIL)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR37Iso2FifthOrderClass(unittest.TestCase):
    """Ruling 2482: fifth order carried name of a class member."""

    def test_2482_home_closure(self):
        _iso2_home(self, _ISO2_HOME, _ISO2_CLOSURE, "r37 2482 hc")

    def test_2482_foreign_closure(self):
        _iso2_home(self, _ISO2_GA, _ISO2_CLOSURE, "r37 2482 fc")

    def test_2482_home_string(self):
        _iso2_home(self, _ISO2_HOME, _ISO2_STRING, "r37 2482 hs")

    def test_2482_foreign_string(self):
        _iso2_home(self, _ISO2_GA, _ISO2_STRING, "r37 2482 fs")

    def test_2482_home_container(self):
        _iso2_home(
            self, _ISO2_HOME, _ISO2_CONTAINER, "r37 2482 hb"
        )

    def test_2482_foreign_container(self):
        _iso2_home(self, _ISO2_GA, _ISO2_CONTAINER, "r37 2482 fb")

    def test_2482_home_default(self):
        _iso2_home(self, _ISO2_HOME, _ISO2_DEFAULT, "r37 2482 hd")

    def test_2482_foreign_default(self):
        _iso2_home(self, _ISO2_GA, _ISO2_DEFAULT, "r37 2482 fd")

    def test_2482_plain_records(self):
        _iso2_home(
            self, _ISO2_GA, _ISO2_CLOSURE, "r37 2482 plain",
            plain=True,
        )

    def test_2482_fourth_order_pole(self):
        _iso2_home(
            self, _ISO2_HOME, _ISO2_FOURTH_POLE, "r37 2482 pole"
        )
