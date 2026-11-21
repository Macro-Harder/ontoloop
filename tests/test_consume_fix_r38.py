"""Fix round 38 tests for rulings 2594 to 2632, Regions 5 and 6.

Written test first against the governing base form of
ontoloop/consumption.py at system head
3c392e621db2d45f644b49f0354202f18c9c69bc. Each ruling stands
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


def _make_module(body, name_hint="r38_region56_mod"):
    _counter[0] += 1
    name = "%s_%d" % (name_hint, _counter[0])
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(body, module.__dict__)
    return module


def _sub_module(body=None):
    if body is None:
        body = "import threading\nPLAIN = 7\nHELD = threading.Lock()\n"
    return _make_module(body, "r38_region56_sub")


def _chain_home(source, extra=""):
    inner = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r38_region56_inner",
    )
    outer = _make_module("", "r38_region56_outer")
    outer.__dict__["INNER"] = inner
    home = _make_module(extra + source)
    home.__dict__["OUTER"] = outer
    return home


def _target_home(source, extra=""):
    target = _make_module(
        "import threading\n"
        "PLAIN = 7\n"
        "HELD = threading.Lock()\n",
        "r38_region56_target",
    )
    home = _make_module(extra + source)
    home.__dict__["MOD"] = target
    return home


def _pair_home(source, carrier_body, extra="", with_target=False):
    carrier = _make_module(carrier_body, "r38_region56_carrier")
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
_CHAIR_PL = (
    "class K:\n    def method(self):\n"
    "        return getattr(getmod(), 'PLAIN')\n"
)


def _chair(case, source, extra, label, plain=False):
    module, service = _mods(case)
    home = _chain_home(source, extra)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR38Chair1BeyondProducedName(unittest.TestCase):
    """Ruling 2594: vars subscript return, one operation beyond
    the produced name patterns of ruling 2444."""

    def test_2594_c1_conv_subscript_default(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0])[0]]\n", "r38 2594 c1_conv_subscript_default")

    def test_2594_c19_conv_subscript_globals(self):
        _chair(self, _CHAIR_GA, "KEYS = [['INNER']]\ndef getmod():\n    return vars(OUTER)[list(KEYS[0])[0]]\n", "r38 2594 c19_conv_subscript_globals")

    def test_2594_c16_keys_view_subscript(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=[{'INNER': 1}]):\n    return vars(OUTER)[list(_k[0].keys())[0]]\n", "r38 2594 c16_keys_view_subscript")

    def test_2594_c2_double_conversion(self):
        _chair(self, _CHAIR_GA, "def getmod(_k={'INNER'}):\n    return vars(OUTER)[list(tuple(_k))[0]]\n", "r38 2594 c2_double_conversion")

    def test_2594_c18_sorted_keyword_arg(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['INNER']):\n    return vars(OUTER)[sorted(_k, reverse=False)[0]]\n", "r38 2594 c18_sorted_keyword_arg")

    def test_2594_c9_conv_helper_result(self):
        _chair(self, _CHAIR_GA, "def _h():\n    return {'INNER'}\ndef getmod():\n    return vars(OUTER)[list(_h())[0]]\n", "r38 2594 c9_conv_helper_result")

    def test_2594_c10_conditional_in_conversion(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['INNER'], _d=['X']):\n    return vars(OUTER)[list(_k if _k else _d)[0]]\n", "r38 2594 c10_conditional_in_conversion")

    def test_2594_c3_pop_of_conversion(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(_k).pop(0)]\n", "r38 2594 c3_pop_of_conversion")

    def test_2594_c6_comprehension(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['INNER']):\n    return vars(OUTER)[[x for x in _k][0]]\n", "r38 2594 c6_comprehension")

    def test_2594_c11_starred_unpack(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['INNER']):\n    return vars(OUTER)[(*_k,)[0]]\n", "r38 2594 c11_starred_unpack")

    def test_2594_c7_join_assembly(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join(_k)]\n", "r38 2594 c7_join_assembly")

    def test_2594_c8_next_iter_subscript(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=[{'INNER'}]):\n    return vars(OUTER)[next(iter(_k[0]))]\n", "r38 2594 c8_next_iter_subscript")

    def test_2594_c12_set_pop_direct(self):
        _chair(self, _CHAIR_GA, "def getmod(_k={'INNER'}):\n    return vars(OUTER)[_k.pop()]\n", "r38 2594 c12_set_pop_direct")

    def test_2594_c4_conditional_element_branch(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=['INNER']):\n    return vars(OUTER)[(_k[0] if _k else 'X')]\n", "r38 2594 c4_conditional_element_branch")

    def test_2594_c1_vars_subscript_member(self):
        _chair(self, _CHAIR_VS, "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0])[0]]\n", "r38 2594 c1 vs")

    def test_2594_c1_dict_subscript_member(self):
        _chair(self, _CHAIR_DS, "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0])[0]]\n", "r38 2594 c1 ds")

    def test_2594_c1_exec_member(self):
        _chair(self, _CHAIR_EX, "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0])[0]]\n", "r38 2594 c1 ex")

    def test_2594_c7_vars_subscript_member(self):
        _chair(self, _CHAIR_VS, "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join(_k)]\n", "r38 2594 c7 vs")

    def test_2594_plain_via_c1(self):
        _chair(self, _CHAIR_PL, "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(_k[0])[0]]\n", "r38 2594 plain c1", plain=True)

    def test_2594_plain_via_c7(self):
        _chair(self, _CHAIR_PL, "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join(_k)]\n", "r38 2594 plain c7", plain=True)

    def test_2594_plain_via_c12(self):
        _chair(self, _CHAIR_PL, "def getmod(_k={'INNER'}):\n    return vars(OUTER)[_k.pop()]\n", "r38 2594 plain c12", plain=True)

    def test_2594_r2444_produced_pole(self):
        _chair(self, _CHAIR_GA, "def getmod(_k={'INNER'}):\n    return vars(OUTER)[list(_k)[0]]\n", "r38 2594 pole 2444")

    def test_2594_direct_element_pole(self):
        _chair(self, _CHAIR_GA, "def getmod(_k=('INNER',)):\n    return vars(OUTER)[_k[0]]\n", "r38 2594 pole direct")


_SIXTH_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def sixth():\n"
    "        return _n\n"
    "    return sixth\n"
    "sixth = _fac()\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_FIFTH_POLE_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def fifth():\n"
    "        return _n\n"
    "    return fifth\n"
    "fifth = _fac()\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_SIXTH_STRING = (
    "STR = 'HELD'\n"
    "def sixth():\n"
    "    return STR\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_FIFTH_POLE_STRING = (
    "STR = 'HELD'\n"
    "def fifth():\n"
    "    return STR\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_SIXTH_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def sixth():\n"
    "    return D['k']\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_FIFTH_POLE_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def fifth():\n"
    "    return D['k']\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_SIXTH_DEFAULT = (
    "def sixth(_n='HELD'):\n"
    "    return _n\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_FIFTH_POLE_DEFAULT = (
    "def fifth(_n='HELD'):\n"
    "    return _n\n"
    "def helper():\n"
    "    return inner()\n"
    "def inner():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

def _chain_home_case(case, source, body, label, plain=False):
    module, service = _mods(case)
    home = _target_home(source, body)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


def _chain_plain(case, source, body, label):
    _chain_home_case(case, source, body.replace("'HELD'", "'PLAIN'"), label, plain=True)


class TestConsumeFixR38Consume1SixthClosureHome(unittest.TestCase):
    """Ruling 2595: sixth order closure name at the home map."""

    def test_2595_home_index(self):
        _chain_home_case(self, _HOME_SRC, _SIXTH_CLOSURE, "r38 2595 home")

    def test_2595_plain_records(self):
        _chain_plain(self, _HOME_SRC, _SIXTH_CLOSURE, "r38 2595 plain")

    def test_2595_standing_pole(self):
        _chain_home_case(self, _HOME_SRC, _FIFTH_POLE_CLOSURE, "r38 2595 pole")


class TestConsumeFixR38Consume2SixthClosureForeign(unittest.TestCase):
    """Ruling 2596: sixth order closure name, foreign module."""

    def test_2596_foreign_getattr(self):
        _chain_home_case(self, _GA_SRC, _SIXTH_CLOSURE, "r38 2596 ga")

    def test_2596_foreign_dict_subscript(self):
        _chain_home_case(self, _GS_SRC, _SIXTH_CLOSURE, "r38 2596 gs")

    def test_2596_plain_records(self):
        _chain_plain(self, _GA_SRC, _SIXTH_CLOSURE, "r38 2596 plain")


class TestConsumeFixR38Consume3SixthStringHome(unittest.TestCase):
    """Ruling 2597: sixth order string name at the home map."""

    def test_2597_home_index(self):
        _chain_home_case(self, _HOME_SRC, _SIXTH_STRING, "r38 2597 home")

    def test_2597_plain_records(self):
        _chain_plain(self, _HOME_SRC, _SIXTH_STRING, "r38 2597 plain")

    def test_2597_standing_pole(self):
        _chain_home_case(self, _HOME_SRC, _FIFTH_POLE_STRING, "r38 2597 pole")


class TestConsumeFixR38Consume4SixthStringForeign(unittest.TestCase):
    """Ruling 2598: sixth order string name, foreign module."""

    def test_2598_foreign_getattr(self):
        _chain_home_case(self, _GA_SRC, _SIXTH_STRING, "r38 2598 ga")

    def test_2598_foreign_dict_subscript(self):
        _chain_home_case(self, _GS_SRC, _SIXTH_STRING, "r38 2598 gs")

    def test_2598_plain_records(self):
        _chain_plain(self, _GA_SRC, _SIXTH_STRING, "r38 2598 plain")


class TestConsumeFixR38Consume5SixthContainerHome(unittest.TestCase):
    """Ruling 2599: sixth order container name at the home map."""

    def test_2599_home_index(self):
        _chain_home_case(self, _HOME_SRC, _SIXTH_CONTAINER, "r38 2599 home")

    def test_2599_plain_records(self):
        _chain_plain(self, _HOME_SRC, _SIXTH_CONTAINER, "r38 2599 plain")

    def test_2599_standing_pole(self):
        _chain_home_case(self, _HOME_SRC, _FIFTH_POLE_CONTAINER, "r38 2599 pole")


class TestConsumeFixR38Consume6SixthContainerForeign(unittest.TestCase):
    """Ruling 2600: sixth order container name, foreign module."""

    def test_2600_foreign_getattr(self):
        _chain_home_case(self, _GA_SRC, _SIXTH_CONTAINER, "r38 2600 ga")

    def test_2600_foreign_dict_subscript(self):
        _chain_home_case(self, _GS_SRC, _SIXTH_CONTAINER, "r38 2600 gs")

    def test_2600_plain_records(self):
        _chain_plain(self, _GA_SRC, _SIXTH_CONTAINER, "r38 2600 plain")


class TestConsumeFixR38Consume7SixthDefaultHome(unittest.TestCase):
    """Ruling 2601: sixth order default name at the home map."""

    def test_2601_home_index(self):
        _chain_home_case(self, _HOME_SRC, _SIXTH_DEFAULT, "r38 2601 home")

    def test_2601_plain_records(self):
        _chain_plain(self, _HOME_SRC, _SIXTH_DEFAULT, "r38 2601 plain")

    def test_2601_standing_pole(self):
        _chain_home_case(self, _HOME_SRC, _FIFTH_POLE_DEFAULT, "r38 2601 pole")


class TestConsumeFixR38Consume8SixthDefaultForeign(unittest.TestCase):
    """Ruling 2602: sixth order default name, foreign module."""

    def test_2602_foreign_getattr(self):
        _chain_home_case(self, _GA_SRC, _SIXTH_DEFAULT, "r38 2602 ga")

    def test_2602_foreign_dict_subscript(self):
        _chain_home_case(self, _GS_SRC, _SIXTH_DEFAULT, "r38 2602 gs")

    def test_2602_plain_records(self):
        _chain_plain(self, _GA_SRC, _SIXTH_DEFAULT, "r38 2602 plain")


_PAIR_INNER3_STRING = (
    "STR = 'HELD'\n"
    "def inner3():\n"
    "    return STR\n"
    "def inner2():\n"
    "    return inner3()\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER2_STRING = (
    "STR = 'HELD'\n"
    "def inner2():\n"
    "    return STR\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER_STRING = (
    "STR = 'HELD'\n"
    "def inner():\n"
    "    return STR\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_SELF_STRING = (
    "STR = 'HELD'\n"
    "def pairfn():\n"
    "    return STR\n"
)

_PAIR_INNER3_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def inner3():\n"
    "    return D['k']\n"
    "def inner2():\n"
    "    return inner3()\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER2_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def inner2():\n"
    "    return D['k']\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def inner():\n"
    "    return D['k']\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_SELF_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def pairfn():\n"
    "    return D['k']\n"
)

_PAIR_INNER3_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def inner3():\n"
    "        return _n\n"
    "    return inner3\n"
    "inner3 = _fac()\n"
    "def inner2():\n"
    "    return inner3()\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER2_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def inner2():\n"
    "        return _n\n"
    "    return inner2\n"
    "inner2 = _fac()\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def inner():\n"
    "        return _n\n"
    "    return inner\n"
    "inner = _fac()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_SELF_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def pairfn():\n"
    "        return _n\n"
    "    return pairfn\n"
    "pairfn = _fac()\n"
)

_PAIR_INNER3_DEFAULT = (
    "def inner3(_n='HELD'):\n"
    "    return _n\n"
    "def inner2():\n"
    "    return inner3()\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER2_DEFAULT = (
    "def inner2(_n='HELD'):\n"
    "    return _n\n"
    "def inner():\n"
    "    return inner2()\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_INNER_DEFAULT = (
    "def inner(_n='HELD'):\n"
    "    return _n\n"
    "def pairfn():\n"
    "    return inner()\n"
)

_PAIR_SELF_DEFAULT = (
    "def pairfn(_n='HELD'):\n"
    "    return _n\n"
)

def _pair_case(case, source, carrier, label, plain=False, helpers=1):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    if helpers == 1:
        extra = "def helper():\n    return CARRIER.pairfn()\n" + _HOME_TAIL
    elif helpers == 2:
        extra = ("def helper2():\n    return CARRIER.pairfn()\n"
                 "def helper():\n    return helper2()\n") + _HOME_TAIL
    else:
        extra = ("def helper3():\n    return CARRIER.pairfn()\n"
                 "def helper2():\n    return helper3()\n"
                 "def helper():\n    return helper2()\n") + _HOME_TAIL
    home = _pair_home(source, body, extra, with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR38Consume9PairInner3StringHome(unittest.TestCase):
    """Ruling 2603: pair inner inner inner string at the home map."""

    def test_2603_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_STRING, "r38 2603 home", helpers=1)

    def test_2603_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_STRING, "r38 2603 plain", plain=True, helpers=1)

    def test_2603_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER2_STRING, "r38 2603 pole", helpers=1)


class TestConsumeFixR38Consume10PairInner3StringForeign(unittest.TestCase):
    """Ruling 2604: pair inner inner inner string, foreign module."""

    def test_2604_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_STRING, "r38 2604 ga", helpers=1)

    def test_2604_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER3_STRING, "r38 2604 gs", helpers=1)

    def test_2604_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_STRING, "r38 2604 plain", plain=True, helpers=1)


class TestConsumeFixR38Consume11PairInner3ContainerHome(unittest.TestCase):
    """Ruling 2605: pair inner inner inner container at the home map."""

    def test_2605_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_CONTAINER, "r38 2605 home", helpers=1)

    def test_2605_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_CONTAINER, "r38 2605 plain", plain=True, helpers=1)

    def test_2605_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER2_CONTAINER, "r38 2605 pole", helpers=1)


class TestConsumeFixR38Consume12PairInner3ContainerForeign(unittest.TestCase):
    """Ruling 2606: pair inner inner inner container, foreign module."""

    def test_2606_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_CONTAINER, "r38 2606 ga", helpers=1)

    def test_2606_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER3_CONTAINER, "r38 2606 gs", helpers=1)

    def test_2606_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_CONTAINER, "r38 2606 plain", plain=True, helpers=1)


class TestConsumeFixR38Consume13PairInner3ClosureHome(unittest.TestCase):
    """Ruling 2607: pair inner inner inner closure at the home map."""

    def test_2607_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_CLOSURE, "r38 2607 home", helpers=1)

    def test_2607_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_CLOSURE, "r38 2607 plain", plain=True, helpers=1)

    def test_2607_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER2_CLOSURE, "r38 2607 pole", helpers=1)


class TestConsumeFixR38Consume14PairInner3ClosureForeign(unittest.TestCase):
    """Ruling 2608: pair inner inner inner closure, foreign module."""

    def test_2608_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_CLOSURE, "r38 2608 ga", helpers=1)

    def test_2608_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER3_CLOSURE, "r38 2608 gs", helpers=1)

    def test_2608_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_CLOSURE, "r38 2608 plain", plain=True, helpers=1)


class TestConsumeFixR38Consume15PairInner3DefaultHome(unittest.TestCase):
    """Ruling 2609: pair inner inner inner default at the home map."""

    def test_2609_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_DEFAULT, "r38 2609 home", helpers=1)

    def test_2609_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER3_DEFAULT, "r38 2609 plain", plain=True, helpers=1)

    def test_2609_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER2_DEFAULT, "r38 2609 pole", helpers=1)


class TestConsumeFixR38Consume16PairInner3DefaultForeign(unittest.TestCase):
    """Ruling 2610: pair inner inner inner default, foreign module."""

    def test_2610_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_DEFAULT, "r38 2610 ga", helpers=1)

    def test_2610_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER3_DEFAULT, "r38 2610 gs", helpers=1)

    def test_2610_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER3_DEFAULT, "r38 2610 plain", plain=True, helpers=1)


def _mp_source(call, act):
    if act == "ga":
        return ("class K:\n    def method(self):\n"
                "        return getattr(MOD, %s)\n" % call)
    return ("class K:\n    def method(self):\n"
            "        return MOD.__dict__[%s]\n" % call)


def _member_pair(case, carrier, act, label, plain=False):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _pair_home(_mp_source("CARRIER.pairfn()", act), body, "", with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR38Consume17MemberPairInner3String(unittest.TestCase):
    """Ruling 2611: member level pair inner inner inner string."""

    def test_2611_foreign_getattr(self):
        _member_pair(self, _PAIR_INNER3_STRING, "ga", "r38 2611 ga")

    def test_2611_foreign_dict_subscript(self):
        _member_pair(self, _PAIR_INNER3_STRING, "gs", "r38 2611 gs")

    def test_2611_plain_records(self):
        _member_pair(self, _PAIR_INNER3_STRING, "ga", "r38 2611 plain", plain=True)


class TestConsumeFixR38Consume18MemberPairInner3Container(unittest.TestCase):
    """Ruling 2612: member level pair inner inner inner container."""

    def test_2612_foreign_getattr(self):
        _member_pair(self, _PAIR_INNER3_CONTAINER, "ga", "r38 2612 ga")

    def test_2612_foreign_dict_subscript(self):
        _member_pair(self, _PAIR_INNER3_CONTAINER, "gs", "r38 2612 gs")

    def test_2612_plain_records(self):
        _member_pair(self, _PAIR_INNER3_CONTAINER, "ga", "r38 2612 plain", plain=True)


class TestConsumeFixR38Consume19MemberPairInner3Closure(unittest.TestCase):
    """Ruling 2613: member level pair inner inner inner closure."""

    def test_2613_foreign_getattr(self):
        _member_pair(self, _PAIR_INNER3_CLOSURE, "ga", "r38 2613 ga")

    def test_2613_foreign_dict_subscript(self):
        _member_pair(self, _PAIR_INNER3_CLOSURE, "gs", "r38 2613 gs")

    def test_2613_plain_records(self):
        _member_pair(self, _PAIR_INNER3_CLOSURE, "ga", "r38 2613 plain", plain=True)


class TestConsumeFixR38Consume20MemberPairInner3Default(unittest.TestCase):
    """Ruling 2614: member level pair inner inner inner default."""

    def test_2614_foreign_getattr(self):
        _member_pair(self, _PAIR_INNER3_DEFAULT, "ga", "r38 2614 ga")

    def test_2614_foreign_dict_subscript(self):
        _member_pair(self, _PAIR_INNER3_DEFAULT, "gs", "r38 2614 gs")

    def test_2614_plain_records(self):
        _member_pair(self, _PAIR_INNER3_DEFAULT, "ga", "r38 2614 plain", plain=True)


class TestConsumeFixR38Consume21Deep3PairInnerStringHome(unittest.TestCase):
    """Ruling 2615: triple helper pair inner string at the home map."""

    def test_2615_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_STRING, "r38 2615 home", helpers=3)

    def test_2615_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_STRING, "r38 2615 plain", plain=True, helpers=3)

    def test_2615_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_STRING, "r38 2615 pole", helpers=2)


class TestConsumeFixR38Consume22Deep3PairInnerStringForeign(unittest.TestCase):
    """Ruling 2616: triple helper pair inner string, foreign module."""

    def test_2616_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_STRING, "r38 2616 ga", helpers=3)

    def test_2616_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER_STRING, "r38 2616 gs", helpers=3)

    def test_2616_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_STRING, "r38 2616 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume23Deep3PairInnerContainerHome(unittest.TestCase):
    """Ruling 2617: triple helper pair inner container at the home map."""

    def test_2617_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_CONTAINER, "r38 2617 home", helpers=3)

    def test_2617_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_CONTAINER, "r38 2617 plain", plain=True, helpers=3)

    def test_2617_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_CONTAINER, "r38 2617 pole", helpers=2)


class TestConsumeFixR38Consume24Deep3PairInnerContainerForeign(unittest.TestCase):
    """Ruling 2618: triple helper pair inner container, foreign module."""

    def test_2618_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_CONTAINER, "r38 2618 ga", helpers=3)

    def test_2618_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER_CONTAINER, "r38 2618 gs", helpers=3)

    def test_2618_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_CONTAINER, "r38 2618 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume25Deep3PairInnerClosureHome(unittest.TestCase):
    """Ruling 2619: triple helper pair inner closure at the home map."""

    def test_2619_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_CLOSURE, "r38 2619 home", helpers=3)

    def test_2619_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_CLOSURE, "r38 2619 plain", plain=True, helpers=3)

    def test_2619_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_CLOSURE, "r38 2619 pole", helpers=2)


class TestConsumeFixR38Consume26Deep3PairInnerClosureForeign(unittest.TestCase):
    """Ruling 2620: triple helper pair inner closure, foreign module."""

    def test_2620_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_CLOSURE, "r38 2620 ga", helpers=3)

    def test_2620_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER_CLOSURE, "r38 2620 gs", helpers=3)

    def test_2620_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_CLOSURE, "r38 2620 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume27Deep3PairInnerDefaultHome(unittest.TestCase):
    """Ruling 2621: triple helper pair inner default at the home map."""

    def test_2621_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_DEFAULT, "r38 2621 home", helpers=3)

    def test_2621_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_DEFAULT, "r38 2621 plain", plain=True, helpers=3)

    def test_2621_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_INNER_DEFAULT, "r38 2621 pole", helpers=2)


class TestConsumeFixR38Consume28Deep3PairInnerDefaultForeign(unittest.TestCase):
    """Ruling 2622: triple helper pair inner default, foreign module."""

    def test_2622_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_DEFAULT, "r38 2622 ga", helpers=3)

    def test_2622_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_INNER_DEFAULT, "r38 2622 gs", helpers=3)

    def test_2622_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_INNER_DEFAULT, "r38 2622 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume29Deep3PairSelfStringHome(unittest.TestCase):
    """Ruling 2623: triple helper pair function string at the home map."""

    def test_2623_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_STRING, "r38 2623 home", helpers=3)

    def test_2623_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_STRING, "r38 2623 plain", plain=True, helpers=3)

    def test_2623_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_STRING, "r38 2623 pole", helpers=2)


class TestConsumeFixR38Consume30Deep3PairSelfStringForeign(unittest.TestCase):
    """Ruling 2624: triple helper pair function string, foreign module."""

    def test_2624_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_STRING, "r38 2624 ga", helpers=3)

    def test_2624_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_SELF_STRING, "r38 2624 gs", helpers=3)

    def test_2624_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_STRING, "r38 2624 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume31Deep3PairSelfContainerHome(unittest.TestCase):
    """Ruling 2625: triple helper pair function container at the home map."""

    def test_2625_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_CONTAINER, "r38 2625 home", helpers=3)

    def test_2625_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_CONTAINER, "r38 2625 plain", plain=True, helpers=3)

    def test_2625_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_CONTAINER, "r38 2625 pole", helpers=2)


class TestConsumeFixR38Consume32Deep3PairSelfContainerForeign(unittest.TestCase):
    """Ruling 2626: triple helper pair function container, foreign module."""

    def test_2626_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_CONTAINER, "r38 2626 ga", helpers=3)

    def test_2626_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_SELF_CONTAINER, "r38 2626 gs", helpers=3)

    def test_2626_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_CONTAINER, "r38 2626 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume33Deep3PairSelfClosureHome(unittest.TestCase):
    """Ruling 2627: triple helper pair function closure at the home map."""

    def test_2627_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_CLOSURE, "r38 2627 home", helpers=3)

    def test_2627_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_CLOSURE, "r38 2627 plain", plain=True, helpers=3)

    def test_2627_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_CLOSURE, "r38 2627 pole", helpers=2)


class TestConsumeFixR38Consume34Deep3PairSelfClosureForeign(unittest.TestCase):
    """Ruling 2628: triple helper pair function closure, foreign module."""

    def test_2628_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_CLOSURE, "r38 2628 ga", helpers=3)

    def test_2628_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_SELF_CLOSURE, "r38 2628 gs", helpers=3)

    def test_2628_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_CLOSURE, "r38 2628 plain", plain=True, helpers=3)


class TestConsumeFixR38Consume35Deep3PairSelfDefaultHome(unittest.TestCase):
    """Ruling 2629: triple helper pair function default at the home map."""

    def test_2629_home_index(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_DEFAULT, "r38 2629 home", helpers=3)

    def test_2629_plain_records(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_DEFAULT, "r38 2629 plain", plain=True, helpers=3)

    def test_2629_standing_pole(self):
        _pair_case(self, _HOME_SRC, _PAIR_SELF_DEFAULT, "r38 2629 pole", helpers=2)


class TestConsumeFixR38Consume36Deep3PairSelfDefaultForeign(unittest.TestCase):
    """Ruling 2630: triple helper pair function default, foreign module."""

    def test_2630_foreign_getattr(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_DEFAULT, "r38 2630 ga", helpers=3)

    def test_2630_foreign_dict_subscript(self):
        _pair_case(self, _GS_SRC, _PAIR_SELF_DEFAULT, "r38 2630 gs", helpers=3)

    def test_2630_plain_records(self):
        _pair_case(self, _GA_SRC, _PAIR_SELF_DEFAULT, "r38 2630 plain", plain=True, helpers=3)


def _hop_home(source, hops, cls_name="HELD"):
    leaf = _make_module(
        "import threading\nPLAIN = 7\nHELD = threading.Lock()\n",
        "r38_region56_leaf",
    )
    node = leaf
    attr = "LEAF"
    for nm in reversed(hops):
        parent = _make_module("", "r38_region56_mid")
        parent.__dict__[attr] = node
        node = parent
        attr = nm
    outer = _make_module("", "r38_region56_outerh")
    outer.__dict__[attr] = node
    home = _make_module(source)
    home.__dict__["OUTER"] = outer
    home.__dict__["Cls"] = type("Cls", (), {"NAME": cls_name})
    return home


_SEVEN = ["L1", "L2", "L3", "L4", "L5"]
_SIXH = ["L1", "L2", "L3", "L4"]
_CHAIN7 = "OUTER.L1.L2.L3.L4.L5.LEAF"
_CHAIN6 = "OUTER.L1.L2.L3.L4.LEAF"


class TestConsumeFixR38Iso1SeventhHopChain(unittest.TestCase):
    """Ruling 2631: governed value at the seventh hop of a chain."""

    def test_2631_getattr_gathered(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n" "        return getattr(%s, Cls.NAME)\n" % _CHAIN7, _SEVEN)
        _check3(self, module, service, home, "r38 2631 getattr_gathered")

    def test_2631_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n" "        return %s.__dict__['HELD']\n" % _CHAIN7, _SEVEN)
        _check3(self, module, service, home, "r38 2631 dict_subscript_literal")

    def test_2631_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n" "        return vars(%s)[Cls.NAME]\n" % _CHAIN7, _SEVEN)
        _check3(self, module, service, home, "r38 2631 vars_subscript_gathered")

    def test_2631_exec_dict_form(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n" "        loc = {}\n" "        exec('x = HELD', %s.__dict__, loc)\n" "        return loc['x']\n" % _CHAIN7, _SEVEN)
        _check3(self, module, service, home, "r38 2631 exec_dict_form")

    def test_2631_plain_records(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n" "        return getattr(%s, Cls.NAME)\n" % _CHAIN7, _SEVEN, cls_name="PLAIN")
        _records3(self, module, home, "r38 2631 plain")

    def test_2631_sixth_hop_pole(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n" "        return getattr(%s, Cls.NAME)\n" % _CHAIN6, _SIXH)
        _check3(self, module, service, home, "r38 2631 pole")


_ISO6_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def sixth():\n"
    "        return _n\n"
    "    return sixth\n"
    "sixth = _fac()\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_ISO5_POLE_CLOSURE = (
    "def _fac():\n"
    "    _n = 'HELD'\n"
    "    def fifth():\n"
    "        return _n\n"
    "    return fifth\n"
    "fifth = _fac()\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_ISO6_STRING = (
    "STR = 'HELD'\n"
    "def sixth():\n"
    "    return STR\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_ISO5_POLE_STRING = (
    "STR = 'HELD'\n"
    "def fifth():\n"
    "    return STR\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_ISO6_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def sixth():\n"
    "    return D['k']\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_ISO5_POLE_CONTAINER = (
    "D = {'k': 'HELD'}\n"
    "def fifth():\n"
    "    return D['k']\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_ISO6_DEFAULT = (
    "def sixth(_n='HELD'):\n"
    "    return _n\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
    "def fifth():\n"
    "    return sixth()\n"
) + _HOME_TAIL

_ISO5_POLE_DEFAULT = (
    "def fifth(_n='HELD'):\n"
    "    return _n\n"
    "def mid():\n"
    "    return second()\n"
    "def second():\n"
    "    return third()\n"
    "def third():\n"
    "    return fourth()\n"
    "def fourth():\n"
    "    return fifth()\n"
) + _HOME_TAIL

_ISO_HOME = (
    "class K:\n    def method(self):\n"
    "        return globals()[mid()]\n"
)
_ISO_GA = (
    "class K:\n    def method(self):\n"
    "        return getattr(MOD, mid())\n"
)


def _iso_case(case, source, body, label, plain=False):
    module, service = _mods(case)
    text = body
    if plain:
        text = text.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, text)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumeFixR38Iso2SixthOrderClass(unittest.TestCase):
    """Ruling 2632: sixth order carried name of a class member,
    the severed act."""

    def test_2632_home_closure(self):
        _iso_case(self, _ISO_HOME, _ISO6_CLOSURE, "r38 2632 hclosure")

    def test_2632_foreign_closure(self):
        _iso_case(self, _ISO_GA, _ISO6_CLOSURE, "r38 2632 fclosure")

    def test_2632_home_string(self):
        _iso_case(self, _ISO_HOME, _ISO6_STRING, "r38 2632 hstring")

    def test_2632_foreign_string(self):
        _iso_case(self, _ISO_GA, _ISO6_STRING, "r38 2632 fstring")

    def test_2632_home_container(self):
        _iso_case(self, _ISO_HOME, _ISO6_CONTAINER, "r38 2632 hcontainer")

    def test_2632_foreign_container(self):
        _iso_case(self, _ISO_GA, _ISO6_CONTAINER, "r38 2632 fcontainer")

    def test_2632_home_default(self):
        _iso_case(self, _ISO_HOME, _ISO6_DEFAULT, "r38 2632 hdefault")

    def test_2632_foreign_default(self):
        _iso_case(self, _ISO_GA, _ISO6_DEFAULT, "r38 2632 fdefault")

    def test_2632_plain_records(self):
        _iso_case(self, _ISO_GA, _ISO6_CLOSURE, "r38 2632 plain", plain=True)

    def test_2632_fifth_order_pole(self):
        _iso_case(self, _ISO_HOME, _ISO5_POLE_CLOSURE, "r38 2632 pole")
