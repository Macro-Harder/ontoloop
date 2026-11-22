"""Fix round 40 tests for rulings 2902 to 2940, Region 4.

Written test first against the governing base form of
ontoloop/consumption.py at system head
6a5cb1203992aa1c4df0e666ba4f83cfaebcb3e4. Each ruling stands
pinned at both poles in the form its triage ruling states:
the defective forms stand decided in substance after the
cure, and the standing poles and clean controls its ruling
names stand in their standing forms at both poles.
Copyright (c) J.P. Picard aka Macro-Harder.
"""

import importlib.util
import os
import sys
import types
import unittest

from tests.harness import require

UNCOPYABLE_MESSAGE = "uncopyable value in bundle copy"

_spec = importlib.util.spec_from_file_location(
    "pin38_r40", os.path.join(os.path.dirname(__file__),
    "test_consume_fix_r38.py"))
pin = importlib.util.module_from_spec(_spec)
sys.modules["pin38_r40"] = pin
_spec.loader.exec_module(pin)

Holder = pin.Holder
_assert_refused = pin._assert_refused
_assert_refused_both = pin._assert_refused_both
_assert_records = pin._assert_records
_make_module = pin._make_module
_chain_home = pin._chain_home
_target_home = pin._target_home
_pair_home = pin._pair_home
_check3 = pin._check3
_records3 = pin._records3
_mods = pin._mods
_HOME_TAIL = pin._HOME_TAIL
_HOME_SRC = pin._HOME_SRC
_GA_SRC = pin._GA_SRC
_GS_SRC = pin._GS_SRC
_CHAIR_GA = pin._CHAIR_GA
_CHAIR_VS = pin._CHAIR_VS
_CHAIR_DS = pin._CHAIR_DS
_CHAIR_EX = pin._CHAIR_EX
_CHAIR_PL = pin._CHAIR_PL
_chair = pin._chair
_hop_home = pin._hop_home


def _sev(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def seventh():\n        return _n\n"
                "    return seventh\nseventh = _fac()\n")
    elif kind == "string":
        leaf = "STR = 'HELD'\ndef seventh():\n    return STR\n"
    elif kind == "container":
        leaf = "D = {'k': 'HELD'}\ndef seventh():\n    return D['k']\n"
    else:
        leaf = "def seventh(_n='HELD'):\n    return _n\n"
    return (leaf + "def sixth():\n    return seventh()\n"
            "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def inner():\n    return third()\n"
            "def helper():\n    return inner()\n" + _HOME_TAIL)


def _eighth(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def eighth():\n        return _n\n"
                "    return eighth\neighth = _fac()\n")
    elif kind == "string":
        leaf = "STR = 'HELD'\ndef eighth():\n    return STR\n"
    elif kind == "container":
        leaf = "D = {'k': 'HELD'}\ndef eighth():\n    return D['k']\n"
    else:
        leaf = "def eighth(_n='HELD'):\n    return _n\n"
    return (leaf + "def seventh():\n    return eighth()\n"
            "def sixth():\n    return seventh()\n"
            "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def inner():\n    return third()\n"
            "def helper():\n    return inner()\n" + _HOME_TAIL)


def _eighth_case(case, source, kind, label, plain=False, pole=False):
    module, service = _mods(case)
    body = _sev(kind) if pole else _eighth(kind)
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, body)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


def _pair4(kind):
    if kind == "string":
        leaf = "STR = 'HELD'\ndef inner4():\n    return STR\n"
    elif kind == "container":
        leaf = "D = {'k': 'HELD'}\ndef inner4():\n    return D['k']\n"
    elif kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def inner4():\n        return _n\n"
                "    return inner4\ninner4 = _fac()\n")
    else:
        leaf = "def inner4(_n='HELD'):\n    return _n\n"
    return (leaf + "def inner3():\n    return inner4()\n"
            "def inner2():\n    return inner3()\n"
            "def inner():\n    return inner2()\n"
            "def pairfn():\n    return inner()\n")


def _pair5(kind):
    if kind == "string":
        leaf = "STR = 'HELD'\ndef inner5():\n    return STR\n"
    elif kind == "container":
        leaf = "D = {'k': 'HELD'}\ndef inner5():\n    return D['k']\n"
    elif kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def inner5():\n        return _n\n"
                "    return inner5\ninner5 = _fac()\n")
    else:
        leaf = "def inner5(_n='HELD'):\n    return _n\n"
    return (leaf + "def inner4():\n    return inner5()\n"
            "def inner3():\n    return inner4()\n"
            "def inner2():\n    return inner3()\n"
            "def inner():\n    return inner2()\n"
            "def pairfn():\n    return inner()\n")


_DEEP_INNER = {"string": pin._PAIR_INNER_STRING,
               "container": pin._PAIR_INNER_CONTAINER,
               "closure": pin._PAIR_INNER_CLOSURE,
               "default": pin._PAIR_INNER_DEFAULT}
_DEEP_SELF = {"string": pin._PAIR_SELF_STRING,
              "container": pin._PAIR_SELF_CONTAINER,
              "closure": pin._PAIR_SELF_CLOSURE,
              "default": pin._PAIR_SELF_DEFAULT}


def _helpers_src(n):
    if n == 1:
        return "def helper():\n    return CARRIER.pairfn()\n"
    if n == 2:
        return ("def helper2():\n    return CARRIER.pairfn()\n"
                "def helper():\n    return helper2()\n")
    if n == 3:
        return ("def helper3():\n    return CARRIER.pairfn()\n"
                "def helper2():\n    return helper3()\n"
                "def helper():\n    return helper2()\n")
    if n == 4:
        return ("def helper4():\n    return CARRIER.pairfn()\n"
                "def helper3():\n    return helper4()\n"
                "def helper2():\n    return helper3()\n"
                "def helper():\n    return helper2()\n")
    return ("def helper5():\n    return CARRIER.pairfn()\n"
            "def helper4():\n    return helper5()\n"
            "def helper3():\n    return helper4()\n"
            "def helper2():\n    return helper3()\n"
            "def helper():\n    return helper2()\n")


def _pair_case40(case, source, carrier, label, plain=False, helpers=1):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _pair_home(source, body, _helpers_src(helpers) + _HOME_TAIL,
                      with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


def _member_case(case, carrier, act, label, plain=False):
    module, service = _mods(case)
    body = carrier
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    src = pin._mp_source("CARRIER.pairfn()", act)
    home = _pair_home(src, body, "", with_target=True)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


_CHAIR_E = [
    ("e1_list_tuple_list_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(tuple(list(_k[0])))[0]]\n"),
    ("e2_list_tuple_double_subscript", "def getmod(_k=[[['INNER']]]):\n    return vars(OUTER)[list(tuple(_k[0][0]))[0]]\n"),
    ("e3_pop_triple_conversion", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(tuple(list(_k))).pop(0)]\n"),
    ("e4_join_list_tuple", "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join(list(tuple(_k)))]\n"),
    ("e5_next_iter_list_tuple_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[next(iter(list(tuple(_k[0]))))]\n"),
    ("e6_starred_list_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[(*list(_k[0]),)[0]]\n"),
    ("e7_join_list_subscript", "def getmod(_k=[['IN', 'NER']]):\n    return vars(OUTER)[''.join(list(_k[0]))]\n"),
    ("e8_keys_copy_copy_subscript", "def getmod(_k=[{'INNER': 1}]):\n    return vars(OUTER)[list(_k[0].copy().copy().keys())[0]]\n"),
    ("e9_list_reversed_list", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(reversed(list(_k)))[0]]\n"),
    ("e10_pop_set_list_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[set(list(_k[0])).pop()]\n"),
    ("e11_comprehension_list_tuple", "def getmod(_k=['INNER']):\n    return vars(OUTER)[[x for x in list(tuple(_k))][0]]\n"),
    ("e12_join_comprehension_list", "def getmod(_k=['IN', 'NER']):\n    return vars(OUTER)[''.join([x for x in list(_k)])]\n"),
    ("e13_list_sorted_list", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(sorted(list(_k)))[0]]\n"),
    ("e14_tuple_list_tuple_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[tuple(list(tuple(_k[0])))[0]]\n"),
    ("e15_next_iter_tuple_list_subscript", "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[next(iter(tuple(list(_k[0]))))]\n"),
    ("e16_list_list_keys_subscript", "def getmod(_k=[{'INNER': 1}]):\n    return vars(OUTER)[list(list(_k[0].keys()))[0]]\n"),
    ("e17_list_reversed_tuple", "def getmod(_k=['INNER']):\n    return vars(OUTER)[list(reversed(tuple(_k)))[0]]\n"),
    ("e18_starred_tuple_conversion", "def getmod(_k=['INNER']):\n    return vars(OUTER)[(*tuple(_k),)[0]]\n"),
    ("e19_sorted_list_tuple", "def getmod(_k=['INNER']):\n    return vars(OUTER)[sorted(list(tuple(_k)))[0]]\n"),
]


def _mk_chair(name, body, member=_CHAIR_GA):
    def test(self):
        _chair(self, member, body, "r40 2902 " + name)
    test.__name__ = "test_2902_" + name
    return test


class TestConsumptionFixR40Chair1(unittest.TestCase):
    """Ruling 2902: produced name forms one further operation
    beyond the produced name patterns of ruling 2746."""

    def test_2902_e1_vars_member(self):
        _chair(self, _CHAIR_VS, _CHAIR_E[0][1], "r40 2902 e1 vs")

    def test_2902_e1_dict_member(self):
        _chair(self, _CHAIR_DS, _CHAIR_E[0][1], "r40 2902 e1 ds")

    def test_2902_e1_exec_member(self):
        _chair(self, _CHAIR_EX, _CHAIR_E[0][1], "r40 2902 e1 ex")

    def test_2902_e7_vars_member(self):
        _chair(self, _CHAIR_VS, _CHAIR_E[6][1], "r40 2902 e7 vs")

    def test_2902_plain_via_e1(self):
        _chair(self, _CHAIR_PL, _CHAIR_E[0][1], "r40 2902 plain e1",
               plain=True)

    def test_2902_plain_via_e4(self):
        _chair(self, _CHAIR_PL, _CHAIR_E[3][1], "r40 2902 plain e4",
               plain=True)

    def test_2902_plain_via_e10(self):
        _chair(self, _CHAIR_PL, _CHAIR_E[9][1], "r40 2902 plain e10",
               plain=True)

    def test_2902_r2746_d1_pole(self):
        _chair(self, _CHAIR_GA,
               "def getmod(_k=[['INNER']]):\n    return vars(OUTER)[list(tuple(_k[0]))[0]]\n",
               "r40 2902 pole 2746 d1")

    def test_2902_r2746_d11_pole(self):
        _chair(self, _CHAIR_GA,
               "def getmod(_k=[['IN', 'NER']]):\n    return vars(OUTER)[''.join(_k[0])]\n",
               "r40 2902 pole 2746 d11")

    def test_2902_direct_element_pole(self):
        _chair(self, _CHAIR_GA,
               "def getmod(_k=('INNER',)):\n    return vars(OUTER)[_k[0]]\n",
               "r40 2902 pole direct")


for _nm, _bd in _CHAIR_E:
    setattr(TestConsumptionFixR40Chair1, "test_2902_" + _nm,
            _mk_chair(_nm, _bd))


class TestConsumptionFixR40Consume1EighthClosureHome(unittest.TestCase):
    """Ruling 2903: eighth order closure at the home map."""

    def test_2903_home_index(self):
        _eighth_case(self, _HOME_SRC, "closure", "r40 2903 home")

    def test_2903_plain_records(self):
        _eighth_case(self, _HOME_SRC, "closure", "r40 2903 plain", plain=True)

    def test_2903_seventh_pole(self):
        _eighth_case(self, _HOME_SRC, "closure", "r40 2903 pole", pole=True)


class TestConsumptionFixR40Consume2EighthClosureForeign(unittest.TestCase):
    """Ruling 2904: eighth order closure at a foreign module."""

    def test_2904_foreign_getattr(self):
        _eighth_case(self, _GA_SRC, "closure", "r40 2904 ga")

    def test_2904_foreign_dict_subscript(self):
        _eighth_case(self, _GS_SRC, "closure", "r40 2904 gs")

    def test_2904_plain_records(self):
        _eighth_case(self, _GA_SRC, "closure", "r40 2904 plain", plain=True)


class TestConsumptionFixR40Consume3EighthStringHome(unittest.TestCase):
    """Ruling 2905: eighth order string at the home map."""

    def test_2905_home_index(self):
        _eighth_case(self, _HOME_SRC, "string", "r40 2905 home")

    def test_2905_plain_records(self):
        _eighth_case(self, _HOME_SRC, "string", "r40 2905 plain", plain=True)

    def test_2905_seventh_pole(self):
        _eighth_case(self, _HOME_SRC, "string", "r40 2905 pole", pole=True)


class TestConsumptionFixR40Consume4EighthStringForeign(unittest.TestCase):
    """Ruling 2906: eighth order string at a foreign module."""

    def test_2906_foreign_getattr(self):
        _eighth_case(self, _GA_SRC, "string", "r40 2906 ga")

    def test_2906_foreign_dict_subscript(self):
        _eighth_case(self, _GS_SRC, "string", "r40 2906 gs")

    def test_2906_plain_records(self):
        _eighth_case(self, _GA_SRC, "string", "r40 2906 plain", plain=True)


class TestConsumptionFixR40Consume5EighthContainerHome(unittest.TestCase):
    """Ruling 2907: eighth order container at the home map."""

    def test_2907_home_index(self):
        _eighth_case(self, _HOME_SRC, "container", "r40 2907 home")

    def test_2907_plain_records(self):
        _eighth_case(self, _HOME_SRC, "container", "r40 2907 plain", plain=True)

    def test_2907_seventh_pole(self):
        _eighth_case(self, _HOME_SRC, "container", "r40 2907 pole", pole=True)


class TestConsumptionFixR40Consume6EighthContainerForeign(unittest.TestCase):
    """Ruling 2908: eighth order container at a foreign module."""

    def test_2908_foreign_getattr(self):
        _eighth_case(self, _GA_SRC, "container", "r40 2908 ga")

    def test_2908_foreign_dict_subscript(self):
        _eighth_case(self, _GS_SRC, "container", "r40 2908 gs")

    def test_2908_plain_records(self):
        _eighth_case(self, _GA_SRC, "container", "r40 2908 plain", plain=True)


class TestConsumptionFixR40Consume7EighthDefaultHome(unittest.TestCase):
    """Ruling 2909: eighth order default at the home map."""

    def test_2909_home_index(self):
        _eighth_case(self, _HOME_SRC, "default", "r40 2909 home")

    def test_2909_plain_records(self):
        _eighth_case(self, _HOME_SRC, "default", "r40 2909 plain", plain=True)

    def test_2909_seventh_pole(self):
        _eighth_case(self, _HOME_SRC, "default", "r40 2909 pole", pole=True)


class TestConsumptionFixR40Consume8EighthDefaultForeign(unittest.TestCase):
    """Ruling 2910: eighth order default at a foreign module."""

    def test_2910_foreign_getattr(self):
        _eighth_case(self, _GA_SRC, "default", "r40 2910 ga")

    def test_2910_foreign_dict_subscript(self):
        _eighth_case(self, _GS_SRC, "default", "r40 2910 gs")

    def test_2910_plain_records(self):
        _eighth_case(self, _GA_SRC, "default", "r40 2910 plain", plain=True)


class TestConsumptionFixR40Consume9Pair5StringHome(unittest.TestCase):
    """Ruling 2911: pair inner inner inner inner inner string home."""

    def test_2911_home_index(self):
        _pair_case40(self, _HOME_SRC, _pair5("string"), "r40 2911 home", helpers=1)

    def test_2911_plain_records(self):
        _pair_case40(self, _HOME_SRC, _pair5("string"), "r40 2911 plain", plain=True, helpers=1)

    def test_2911_inner4_pole(self):
        _pair_case40(self, _HOME_SRC, _pair4("string"), "r40 2911 pole", helpers=1)


class TestConsumptionFixR40Consume10Pair5StringForeign(unittest.TestCase):
    """Ruling 2912: pair inner inner inner inner inner string foreign."""

    def test_2912_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _pair5("string"), "r40 2912 ga", helpers=1)

    def test_2912_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _pair5("string"), "r40 2912 gs", helpers=1)

    def test_2912_plain_records(self):
        _pair_case40(self, _GA_SRC, _pair5("string"), "r40 2912 plain", plain=True, helpers=1)


class TestConsumptionFixR40Consume11Pair5ContainerHome(unittest.TestCase):
    """Ruling 2913: pair inner inner inner inner inner container home."""

    def test_2913_home_index(self):
        _pair_case40(self, _HOME_SRC, _pair5("container"), "r40 2913 home", helpers=1)

    def test_2913_plain_records(self):
        _pair_case40(self, _HOME_SRC, _pair5("container"), "r40 2913 plain", plain=True, helpers=1)

    def test_2913_inner4_pole(self):
        _pair_case40(self, _HOME_SRC, _pair4("container"), "r40 2913 pole", helpers=1)


class TestConsumptionFixR40Consume12Pair5ContainerForeign(unittest.TestCase):
    """Ruling 2914: pair inner inner inner inner inner container foreign."""

    def test_2914_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _pair5("container"), "r40 2914 ga", helpers=1)

    def test_2914_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _pair5("container"), "r40 2914 gs", helpers=1)

    def test_2914_plain_records(self):
        _pair_case40(self, _GA_SRC, _pair5("container"), "r40 2914 plain", plain=True, helpers=1)


class TestConsumptionFixR40Consume13Pair5ClosureHome(unittest.TestCase):
    """Ruling 2915: pair inner inner inner inner inner closure home."""

    def test_2915_home_index(self):
        _pair_case40(self, _HOME_SRC, _pair5("closure"), "r40 2915 home", helpers=1)

    def test_2915_plain_records(self):
        _pair_case40(self, _HOME_SRC, _pair5("closure"), "r40 2915 plain", plain=True, helpers=1)

    def test_2915_inner4_pole(self):
        _pair_case40(self, _HOME_SRC, _pair4("closure"), "r40 2915 pole", helpers=1)


class TestConsumptionFixR40Consume14Pair5ClosureForeign(unittest.TestCase):
    """Ruling 2916: pair inner inner inner inner inner closure foreign."""

    def test_2916_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _pair5("closure"), "r40 2916 ga", helpers=1)

    def test_2916_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _pair5("closure"), "r40 2916 gs", helpers=1)

    def test_2916_plain_records(self):
        _pair_case40(self, _GA_SRC, _pair5("closure"), "r40 2916 plain", plain=True, helpers=1)


class TestConsumptionFixR40Consume15Pair5DefaultHome(unittest.TestCase):
    """Ruling 2917: pair inner inner inner inner inner default home."""

    def test_2917_home_index(self):
        _pair_case40(self, _HOME_SRC, _pair5("default"), "r40 2917 home", helpers=1)

    def test_2917_plain_records(self):
        _pair_case40(self, _HOME_SRC, _pair5("default"), "r40 2917 plain", plain=True, helpers=1)

    def test_2917_inner4_pole(self):
        _pair_case40(self, _HOME_SRC, _pair4("default"), "r40 2917 pole", helpers=1)


class TestConsumptionFixR40Consume16Pair5DefaultForeign(unittest.TestCase):
    """Ruling 2918: pair inner inner inner inner inner default foreign."""

    def test_2918_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _pair5("default"), "r40 2918 ga", helpers=1)

    def test_2918_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _pair5("default"), "r40 2918 gs", helpers=1)

    def test_2918_plain_records(self):
        _pair_case40(self, _GA_SRC, _pair5("default"), "r40 2918 plain", plain=True, helpers=1)


class TestConsumptionFixR40Consume17MemberPair5String(unittest.TestCase):
    """Ruling 2919: member level pair inner inner inner inner inner string."""

    def test_2919_getattr(self):
        _member_case(self, _pair5("string"), "ga", "r40 2919 ga")

    def test_2919_dict_subscript(self):
        _member_case(self, _pair5("string"), "gs", "r40 2919 gs")

    def test_2919_plain_records(self):
        _member_case(self, _pair5("string"), "ga", "r40 2919 plain", plain=True)

    def test_2919_inner4_pole(self):
        _member_case(self, _pair4("string"), "ga", "r40 2919 pole")


class TestConsumptionFixR40Consume18MemberPair5Container(unittest.TestCase):
    """Ruling 2920: member level pair inner inner inner inner inner container."""

    def test_2920_getattr(self):
        _member_case(self, _pair5("container"), "ga", "r40 2920 ga")

    def test_2920_dict_subscript(self):
        _member_case(self, _pair5("container"), "gs", "r40 2920 gs")

    def test_2920_plain_records(self):
        _member_case(self, _pair5("container"), "ga", "r40 2920 plain", plain=True)

    def test_2920_inner4_pole(self):
        _member_case(self, _pair4("container"), "ga", "r40 2920 pole")


class TestConsumptionFixR40Consume19MemberPair5Closure(unittest.TestCase):
    """Ruling 2921: member level pair inner inner inner inner inner closure."""

    def test_2921_getattr(self):
        _member_case(self, _pair5("closure"), "ga", "r40 2921 ga")

    def test_2921_dict_subscript(self):
        _member_case(self, _pair5("closure"), "gs", "r40 2921 gs")

    def test_2921_plain_records(self):
        _member_case(self, _pair5("closure"), "ga", "r40 2921 plain", plain=True)

    def test_2921_inner4_pole(self):
        _member_case(self, _pair4("closure"), "ga", "r40 2921 pole")


class TestConsumptionFixR40Consume20MemberPair5Default(unittest.TestCase):
    """Ruling 2922: member level pair inner inner inner inner inner default."""

    def test_2922_getattr(self):
        _member_case(self, _pair5("default"), "ga", "r40 2922 ga")

    def test_2922_dict_subscript(self):
        _member_case(self, _pair5("default"), "gs", "r40 2922 gs")

    def test_2922_plain_records(self):
        _member_case(self, _pair5("default"), "ga", "r40 2922 plain", plain=True)

    def test_2922_inner4_pole(self):
        _member_case(self, _pair4("default"), "ga", "r40 2922 pole")


class TestConsumptionFixR40Consume21Deep5InnerStringHome(unittest.TestCase):
    """Ruling 2923: deep pair one helper past, inner string home."""

    def test_2923_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["string"], "r40 2923 home", helpers=5)

    def test_2923_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["string"], "r40 2923 plain", plain=True, helpers=5)

    def test_2923_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["string"], "r40 2923 pole", helpers=4)


class TestConsumptionFixR40Consume22Deep5InnerStringForeign(unittest.TestCase):
    """Ruling 2924: deep pair one helper past, inner string foreign."""

    def test_2924_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["string"], "r40 2924 ga", helpers=5)

    def test_2924_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_INNER["string"], "r40 2924 gs", helpers=5)

    def test_2924_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["string"], "r40 2924 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume23Deep5InnerContainerHome(unittest.TestCase):
    """Ruling 2925: deep pair one helper past, inner container home."""

    def test_2925_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["container"], "r40 2925 home", helpers=5)

    def test_2925_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["container"], "r40 2925 plain", plain=True, helpers=5)

    def test_2925_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["container"], "r40 2925 pole", helpers=4)


class TestConsumptionFixR40Consume24Deep5InnerContainerForeign(unittest.TestCase):
    """Ruling 2926: deep pair one helper past, inner container foreign."""

    def test_2926_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["container"], "r40 2926 ga", helpers=5)

    def test_2926_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_INNER["container"], "r40 2926 gs", helpers=5)

    def test_2926_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["container"], "r40 2926 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume25Deep5InnerClosureHome(unittest.TestCase):
    """Ruling 2927: deep pair one helper past, inner closure home."""

    def test_2927_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["closure"], "r40 2927 home", helpers=5)

    def test_2927_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["closure"], "r40 2927 plain", plain=True, helpers=5)

    def test_2927_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["closure"], "r40 2927 pole", helpers=4)


class TestConsumptionFixR40Consume26Deep5InnerClosureForeign(unittest.TestCase):
    """Ruling 2928: deep pair one helper past, inner closure foreign."""

    def test_2928_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["closure"], "r40 2928 ga", helpers=5)

    def test_2928_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_INNER["closure"], "r40 2928 gs", helpers=5)

    def test_2928_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["closure"], "r40 2928 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume27Deep5InnerDefaultHome(unittest.TestCase):
    """Ruling 2929: deep pair one helper past, inner default home."""

    def test_2929_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["default"], "r40 2929 home", helpers=5)

    def test_2929_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["default"], "r40 2929 plain", plain=True, helpers=5)

    def test_2929_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_INNER["default"], "r40 2929 pole", helpers=4)


class TestConsumptionFixR40Consume28Deep5InnerDefaultForeign(unittest.TestCase):
    """Ruling 2930: deep pair one helper past, inner default foreign."""

    def test_2930_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["default"], "r40 2930 ga", helpers=5)

    def test_2930_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_INNER["default"], "r40 2930 gs", helpers=5)

    def test_2930_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_INNER["default"], "r40 2930 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume29Deep5SelfStringHome(unittest.TestCase):
    """Ruling 2931: deep pair one helper past, self string home."""

    def test_2931_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["string"], "r40 2931 home", helpers=5)

    def test_2931_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["string"], "r40 2931 plain", plain=True, helpers=5)

    def test_2931_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["string"], "r40 2931 pole", helpers=4)


class TestConsumptionFixR40Consume30Deep5SelfStringForeign(unittest.TestCase):
    """Ruling 2932: deep pair one helper past, self string foreign."""

    def test_2932_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["string"], "r40 2932 ga", helpers=5)

    def test_2932_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_SELF["string"], "r40 2932 gs", helpers=5)

    def test_2932_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["string"], "r40 2932 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume31Deep5SelfContainerHome(unittest.TestCase):
    """Ruling 2933: deep pair one helper past, self container home."""

    def test_2933_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["container"], "r40 2933 home", helpers=5)

    def test_2933_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["container"], "r40 2933 plain", plain=True, helpers=5)

    def test_2933_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["container"], "r40 2933 pole", helpers=4)


class TestConsumptionFixR40Consume32Deep5SelfContainerForeign(unittest.TestCase):
    """Ruling 2934: deep pair one helper past, self container foreign."""

    def test_2934_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["container"], "r40 2934 ga", helpers=5)

    def test_2934_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_SELF["container"], "r40 2934 gs", helpers=5)

    def test_2934_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["container"], "r40 2934 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume33Deep5SelfClosureHome(unittest.TestCase):
    """Ruling 2935: deep pair one helper past, self closure home."""

    def test_2935_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["closure"], "r40 2935 home", helpers=5)

    def test_2935_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["closure"], "r40 2935 plain", plain=True, helpers=5)

    def test_2935_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["closure"], "r40 2935 pole", helpers=4)


class TestConsumptionFixR40Consume34Deep5SelfClosureForeign(unittest.TestCase):
    """Ruling 2936: deep pair one helper past, self closure foreign."""

    def test_2936_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["closure"], "r40 2936 ga", helpers=5)

    def test_2936_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_SELF["closure"], "r40 2936 gs", helpers=5)

    def test_2936_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["closure"], "r40 2936 plain", plain=True, helpers=5)


class TestConsumptionFixR40Consume35Deep5SelfDefaultHome(unittest.TestCase):
    """Ruling 2937: deep pair one helper past, self default home."""

    def test_2937_home_index(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["default"], "r40 2937 home", helpers=5)

    def test_2937_plain_records(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["default"], "r40 2937 plain", plain=True, helpers=5)

    def test_2937_four_helper_pole(self):
        _pair_case40(self, _HOME_SRC, _DEEP_SELF["default"], "r40 2937 pole", helpers=4)


class TestConsumptionFixR40Consume36Deep5SelfDefaultForeign(unittest.TestCase):
    """Ruling 2938: deep pair one helper past, self default foreign."""

    def test_2938_foreign_getattr(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["default"], "r40 2938 ga", helpers=5)

    def test_2938_foreign_dict_subscript(self):
        _pair_case40(self, _GS_SRC, _DEEP_SELF["default"], "r40 2938 gs", helpers=5)

    def test_2938_plain_records(self):
        _pair_case40(self, _GA_SRC, _DEEP_SELF["default"], "r40 2938 plain", plain=True, helpers=5)


_NINE = ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]
_EIGHTH = ["L1", "L2", "L3", "L4", "L5", "L6"]
_CHAIN9 = "OUTER.L1.L2.L3.L4.L5.L6.L7.LEAF"
_CHAIN8H = "OUTER.L1.L2.L3.L4.L5.L6.LEAF"


class TestConsumptionFixR40Iso1NinthHop(unittest.TestCase):
    """Ruling 2939: governed value at the ninth hop of a chain."""

    def test_2939_getattr_gathered(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return getattr(%s, Cls.NAME)\n"
                         % _CHAIN9, _NINE)
        _check3(self, module, service, home, "r40 2939 ga")

    def test_2939_dict_subscript_literal(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return %s.__dict__['HELD']\n"
                         % _CHAIN9, _NINE)
        _check3(self, module, service, home, "r40 2939 ds")

    def test_2939_vars_subscript_gathered(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return vars(%s)[Cls.NAME]\n"
                         % _CHAIN9, _NINE)
        _check3(self, module, service, home, "r40 2939 vs")

    def test_2939_exec_dict_form(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        loc = {}\n"
                         "        exec('x = HELD', %s.__dict__, loc)\n"
                         "        return loc['x']\n" % _CHAIN9, _NINE)
        _check3(self, module, service, home, "r40 2939 ex")

    def test_2939_plain_records(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return getattr(%s, Cls.NAME)\n"
                         % _CHAIN9, _NINE, cls_name="PLAIN")
        _records3(self, module, home, "r40 2939 plain")

    def test_2939_eighth_hop_pole(self):
        module, service = _mods(self)
        home = _hop_home("class K:\n    def method(self):\n"
                         "        return getattr(%s, Cls.NAME)\n"
                         % _CHAIN8H, _EIGHTH)
        _check3(self, module, service, home, "r40 2939 pole")


_ISO_HOME_G = ("class K:\n    def method(self):\n"
               "        return globals()[mid()]\n")
_ISO_GA_G = ("class K:\n    def method(self):\n"
             "        return getattr(MOD, mid())\n")


def _iso7(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def seventh():\n        return _n\n"
                "    return seventh\nseventh = _fac()\n")
    elif kind == "string":
        leaf = "S = 'HELD'\ndef seventh():\n    return S\n"
    elif kind == "container":
        leaf = "L = ['HELD']\ndef seventh():\n    return L[0]\n"
    else:
        leaf = "def seventh(_n='HELD'):\n    return _n\n"
    return (leaf + "def sixth():\n    return seventh()\n"
            "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def second():\n    return third()\n"
            "def mid():\n    return second()\n" + _HOME_TAIL)


def _iso8(kind):
    if kind == "closure":
        leaf = ("def _fac():\n    _n = 'HELD'\n"
                "    def eighth():\n        return _n\n"
                "    return eighth\neighth = _fac()\n")
    elif kind == "string":
        leaf = "S = 'HELD'\ndef eighth():\n    return S\n"
    elif kind == "container":
        leaf = "L = ['HELD']\ndef eighth():\n    return L[0]\n"
    else:
        leaf = "def eighth(_n='HELD'):\n    return _n\n"
    return (leaf + "def seventh():\n    return eighth()\n"
            "def sixth():\n    return seventh()\n"
            "def fifth():\n    return sixth()\n"
            "def fourth():\n    return fifth()\n"
            "def third():\n    return fourth()\n"
            "def second():\n    return third()\n"
            "def mid():\n    return second()\n" + _HOME_TAIL)


def _iso_case(case, source, kind, label, plain=False, pole=False):
    module, service = _mods(case)
    body = _iso7(kind) if pole else _iso8(kind)
    if plain:
        body = body.replace("'HELD'", "'PLAIN'")
    home = _target_home(source, body)
    if plain:
        _records3(case, module, home, label)
    else:
        _check3(case, module, service, home, label)


class TestConsumptionFixR40Iso2EighthOrder(unittest.TestCase):
    """Ruling 2940: name carried at an eighth order step, severed
    from the Consume eighth order family, on the bundle copy act
    at the class, instance, and holder positions."""

    def test_2940_closure_home(self):
        _iso_case(self, _ISO_HOME_G, "closure", "r40 2940 closure home")

    def test_2940_closure_foreign(self):
        _iso_case(self, _ISO_GA_G, "closure", "r40 2940 closure ga")

    def test_2940_container_home(self):
        _iso_case(self, _ISO_HOME_G, "container", "r40 2940 container home")

    def test_2940_container_foreign(self):
        _iso_case(self, _ISO_GA_G, "container", "r40 2940 container ga")

    def test_2940_string_home(self):
        _iso_case(self, _ISO_HOME_G, "string", "r40 2940 string home")

    def test_2940_string_foreign(self):
        _iso_case(self, _ISO_GA_G, "string", "r40 2940 string ga")

    def test_2940_default_home(self):
        _iso_case(self, _ISO_HOME_G, "default", "r40 2940 default home")

    def test_2940_default_foreign(self):
        _iso_case(self, _ISO_GA_G, "default", "r40 2940 default ga")

    def test_2940_plain_records(self):
        _iso_case(self, _ISO_GA_G, "closure", "r40 2940 plain",
                  plain=True)

    def test_2940_seventh_pole(self):
        _iso_case(self, _ISO_HOME_G, "closure", "r40 2940 pole",
                  pole=True)


if __name__ == "__main__":
    unittest.main()
