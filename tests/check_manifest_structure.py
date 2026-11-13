"""Structural coverage check for the unified manifest schema.

Standalone checker, not collected by the test discovery pattern.
Run from the system repo root with:
    python3 tests/check_manifest_structure.py

It asserts the LE-C2 unified schema over the three manifest parts:
parse and envelope form, preserved fields where they stood, entry
completeness, module existence on disk without import, and case class
existence by syntax tree reading. It also asserts the LE-C4 includes
trace entry by entry, on the values quoted in the tracing paper at
design/steps/step-14-lec4-tracing.md section 7 (LEC4-P3 and LEC4-P5),
which quote manifest part A directly. The merged list placements are
not schema input for the includes limb (LEC4-P9).

RA-5 dialect note: this checker cites the note at
design/steps/step-13-reaudit-ra5.md section 3. Two shapes that are not
entry forms in any manifest part still return no subtree in the
REDACT-T08 quantity traversal: a dictionary whose mention sits inside
a list held as a field value with the limb as a sibling field, and a
bare list of strings holding the mention and a wording as separate
items. The unified schema adopts neither shape. Every entry here is a
JSON object whose fields name it. If a later manifest dialect adopts
either shape, the traversal in test_spanning.py must grow with it, as
a separate new test act.
"""

import ast
import json
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PART_FILES = {
    "a": "manifest_part_a.json",
    "b": "manifest_part_b.json",
    "c": "manifest_part_c.json",
}
EXPECTED_ENVELOPE = {
    "a": ("A", "data structures"),
    "b": ("B", "failure and boundary"),
    "c": ("C", "end to end and evidence"),
}
EXPECTED_DISPOSITION = [
    "SPEC-CANON-T03",
    "SPEC-CORPUS-T03",
    "SPEC-DICT-T03",
    "SPEC-PATTERN-T03",
    "GOLDEN-T04",
    "POP-T01",
    "POP-T02",
    "POP-T03",
    "POP-T04",
    "POP-T05",
    "CONSUME-T10",
]
EXPECTED_INCLUDES = {
    "SPEC-CANON-T04": (
        "unnumbered SPEC-CANON failure pair, floating point value refused",
        "TestSpecCanonT04",
        "tests.test_spec_canon",
    ),
    "SPEC-SEAL-T04": (
        "unnumbered SPEC-SEAL failure pair, manifest field list missing one of seven registered fields",
        "TestSpecSealT04",
        "tests.test_spec_seal",
    ),
    "SPEC-PATTERN-T02": (
        "unnumbered SPEC-PATTERN failure pair, family stated only as a name fails completeness",
        "TestSpecPatternT02",
        "tests.test_spec_pattern",
    ),
}
EXPECTED_SPAN_IDS = ["SPAN-T%02d" % n for n in range(1, 9)]
EXPECTED_1986_METHODS = [
    "test_verbatim_case_at_candidate_construction",
    "test_near_verbatim_case_at_candidate_construction",
    "test_clean_case_at_candidate_construction",
    "test_verbatim_case_at_promotion",
    "test_near_verbatim_case_at_promotion",
    "test_clean_case_at_promotion",
    "test_no_clearance_claim_until_a_promotion_record_carries_the_result",
]

failures = []
class_count = [0]
_class_cache = {}


def fail(part, key, assertion, detail):
    failures.append(
        "FAIL part=%s entry=%s assertion=%s: %s" % (part, key, assertion, detail)
    )


def module_path(module):
    if not isinstance(module, str) or not module.startswith("tests."):
        return None
    leaf = module[len("tests."):]
    if not leaf or "." in leaf or "/" in leaf:
        return None
    return os.path.join(TESTS_DIR, leaf + ".py")


def check_module(part, key, module, assertion):
    path = module_path(module)
    if path is None:
        fail(part, key, assertion, "module not in dotted tests form: %r" % (module,))
        return False
    if not os.path.isfile(path):
        fail(part, key, assertion, "module file missing on disk: %s" % module)
        return False
    return True


def class_names(module):
    if module in _class_cache:
        return _class_cache[module]
    names = set()
    path = module_path(module)
    if path is not None and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), filename=path)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                names.add(node.name)
    _class_cache[module] = names
    return names


def check_class(part, key, case, module, assertion):
    class_count[0] += 1
    if case not in class_names(module):
        fail(
            part,
            key,
            assertion,
            "case class %r not defined in module %s" % (case, module),
        )
        return False
    return True


def main():
    parts = {}
    # Assertion A: parse and envelope form.
    for letter, filename in sorted(PART_FILES.items()):
        path = os.path.join(TESTS_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:
            fail(letter, filename, "A", "does not parse as JSON: %s" % exc)
            continue
        parts[letter] = data
        if not isinstance(data, dict):
            fail(letter, filename, "A", "top level is not an object")
            continue
        for field in ("part", "seat", "perspective", "rows", "unrowed"):
            if field not in data:
                fail(letter, filename, "A", "envelope field missing: %s" % field)
        if data.get("part") != letter:
            fail(letter, filename, "A", "part value is not %r" % letter)
        seat, perspective = EXPECTED_ENVELOPE[letter]
        if data.get("seat") != seat:
            fail(letter, filename, "A", "seat value is not %r" % seat)
        if data.get("perspective") != perspective:
            fail(letter, filename, "A", "perspective value is not %r" % perspective)
        if not isinstance(data.get("rows"), dict):
            fail(letter, filename, "A", "rows is not an object")
        if not isinstance(data.get("unrowed"), dict):
            fail(letter, filename, "A", "unrowed is not an object")
    if "a" in parts and "harness" not in parts["a"]:
        fail("a", "harness", "A", "harness missing in part A")
    for letter in ("b", "c"):
        if letter in parts and "harness" in parts[letter]:
            fail(letter, "harness", "A", "harness stands outside part A")
    if "c" in parts and "spanning" not in parts["c"]:
        fail("c", "spanning", "A", "spanning missing in part C")

    # Row and unrowed entry maps across parts.
    row_home = {}
    unrowed_home = {}
    for letter, data in sorted(parts.items()):
        if not isinstance(data, dict):
            continue
        rows = data.get("rows") if isinstance(data.get("rows"), dict) else {}
        unrowed = data.get("unrowed") if isinstance(data.get("unrowed"), dict) else {}
        for key in rows:
            row_home.setdefault(key, []).append(letter)
        for key in unrowed:
            unrowed_home.setdefault(key, []).append(letter)

    # Assertion C: entry completeness, exactly one part each.
    total_rows = sum(
        len(d.get("rows", {})) for d in parts.values() if isinstance(d, dict)
    )
    total_unrowed = sum(
        len(d.get("unrowed", {})) for d in parts.values() if isinstance(d, dict)
    )
    if total_rows != 129:
        fail("all", "rows", "C", "row entries number %d, expected 129" % total_rows)
    if total_unrowed != 12:
        fail(
            "all",
            "unrowed",
            "C",
            "unrowed entries number %d, expected 12" % total_unrowed,
        )
    for key, homes in sorted(row_home.items()):
        if len(homes) != 1:
            fail("all", key, "C", "row stands in %d parts" % len(homes))
    for key, homes in sorted(unrowed_home.items()):
        if len(homes) != 1:
            fail("all", key, "C", "subsection stands in %d parts" % len(homes))

    # Assertions B1 and B2, with D and E on every row entry.
    disposition_found = []
    includes_found = {}
    for letter, data in sorted(parts.items()):
        if not isinstance(data, dict) or not isinstance(data.get("rows"), dict):
            continue
        for key, entry in sorted(data["rows"].items()):
            if not isinstance(entry, dict):
                fail(letter, key, "A", "row entry is not an object")
                continue
            if "case" not in entry or "module" not in entry:
                fail(letter, key, "A", "row entry lacks case or module")
                continue
            if "disposition" in entry:
                disposition_found.append(key)
                if entry["disposition"] != "stage-carried":
                    fail(letter, key, "B1", "disposition value is not stage-carried")
            if "includes" in entry:
                includes_found[key] = entry["includes"]
            check_module(letter, key, entry.get("module"), "D")
            check_class(letter, key, entry.get("case"), entry.get("module"), "E")
    if sorted(disposition_found) != sorted(EXPECTED_DISPOSITION):
        fail(
            "all",
            "disposition",
            "B1",
            "disposition stands on %s, expected exactly the 11 named rows"
            % sorted(disposition_found),
        )
    if set(includes_found) != set(EXPECTED_INCLUDES):
        fail(
            "all",
            "includes",
            "B2",
            "includes stands on %s, expected exactly the 3 named rows"
            % sorted(includes_found),
        )
    for key, (value, _case, _module) in sorted(EXPECTED_INCLUDES.items()):
        if includes_found.get(key) != value:
            fail("all", key, "B2", "includes value does not equal the filed value")

    # LEC4-P8 entry by entry assertions, on LEC4-P3 and LEC4-P5 values.
    all_rows = {}
    for letter, data in sorted(parts.items()):
        if isinstance(data, dict) and isinstance(data.get("rows"), dict):
            for key, entry in data["rows"].items():
                all_rows[key] = (letter, entry)
    for key, (value, case, module) in sorted(EXPECTED_INCLUDES.items()):
        if key not in all_rows:
            fail("all", key, "LEC4-P8", "governing entry does not exist")
            continue
        letter, entry = all_rows[key]
        if "includes" not in entry:
            fail(letter, key, "LEC4-P8", "includes field absent on governing entry")
        elif entry["includes"] != value:
            fail(letter, key, "LEC4-P8", "includes value differs from LEC4-P3 value")
        if entry.get("case") != case:
            fail(letter, key, "LEC4-P8", "case value differs from LEC4-P5 value")
        if entry.get("module") != module:
            fail(letter, key, "LEC4-P8", "module value differs from LEC4-P5 value")
        check_module(letter, key, module, "LEC4-P8")
        check_class(letter, key, case, module, "LEC4-P8")
    if "SPEC-PATTERN-T03" in all_rows:
        letter, entry = all_rows["SPEC-PATTERN-T03"]
        if "includes" in entry:
            fail(letter, "SPEC-PATTERN-T03", "LEC4-P8", "includes field stands on T03")
    else:
        fail("all", "SPEC-PATTERN-T03", "LEC4-P8", "entry does not exist")
    if len(includes_found) != 3:
        fail(
            "all",
            "includes",
            "LEC4-P8",
            "includes field count is %d, expected exactly 3" % len(includes_found),
        )

    # Assertion B4: harness in part A.
    if "a" in parts:
        harness = parts["a"].get("harness")
        if not isinstance(harness, dict) or harness.get("module") != "tests.harness":
            fail("a", "harness", "B4", "harness module is not tests.harness")
        else:
            check_module("a", "harness", harness["module"], "D")

    # Assertion B3: spanning in part C only, in its filed form.
    for letter, data in sorted(parts.items()):
        if letter != "c" and isinstance(data, dict) and "spanning" in data:
            fail(letter, "spanning", "B3", "spanning stands outside part C")
    if "c" in parts and isinstance(parts["c"].get("spanning"), dict):
        spanning = parts["c"]["spanning"]
        for field in ("module", "coverage_cases", "record_cases", "meaning_checks"):
            if field not in spanning:
                fail("c", "spanning", "B3", "spanning field missing: %s" % field)
        if spanning.get("module") != "tests.test_spanning":
            fail("c", "spanning", "B3", "spanning module is not tests.test_spanning")
        checks = spanning.get("meaning_checks")
        if not isinstance(checks, dict) or sorted(checks) != EXPECTED_SPAN_IDS:
            fail("c", "spanning", "B3", "meaning_checks do not hold SPAN-T01 to SPAN-T08")
        check_module("c", "spanning", spanning.get("module"), "D")
        span_module = spanning.get("module")
        for case in spanning.get("coverage_cases", []):
            check_class("c", "spanning", case, span_module, "E")
        for case in spanning.get("record_cases", []):
            check_class("c", "spanning", case, span_module, "E")
        if isinstance(checks, dict):
            for span_id, entry in sorted(checks.items()):
                if not isinstance(entry, dict) or "case" not in entry:
                    fail("c", span_id, "B3", "meaning check entry lacks case")
                else:
                    check_class("c", span_id, entry["case"], span_module, "E")

    # Assertion B5, with D and E on every unrowed entry.
    for letter, data in sorted(parts.items()):
        if not isinstance(data, dict) or not isinstance(data.get("unrowed"), dict):
            continue
        for key, entry in sorted(data["unrowed"].items()):
            if not isinstance(entry, dict):
                fail(letter, key, "A", "unrowed entry is not an object")
                continue
            if not isinstance(entry.get("cases"), list):
                fail(letter, key, "B5", "cases is not a list")
            if "module" not in entry:
                fail(letter, key, "B5", "module missing")
            if entry.get("counted_under") != key:
                fail(letter, key, "B5", "counted_under does not equal its key")
            if entry.get("row_identifier") is not None:
                fail(letter, key, "B5", "row_identifier is not null")
            check_module(letter, key, entry.get("module"), "D")
            if isinstance(entry.get("cases"), list):
                for case in entry["cases"]:
                    check_class(letter, key, case, entry.get("module"), "E")
    entry_1986 = None
    if "c" in parts and isinstance(parts["c"].get("unrowed"), dict):
        entry_1986 = parts["c"]["unrowed"].get("19.86")
    if not isinstance(entry_1986, dict):
        fail("c", "19.86", "B5", "subsection 19.86 entry missing")
    else:
        if entry_1986.get("methods") != EXPECTED_1986_METHODS:
            fail("c", "19.86", "B5", "methods not preserved as filed")
        if entry_1986.get("test_count") != 7:
            fail("c", "19.86", "B5", "test_count not preserved as filed")

    # Assertion F: failure form and clean run counts.
    if failures:
        for line in failures:
            print(line)
        print("FAILED: %d assertion failure(s)" % len(failures))
        return 1
    print(
        "OK parts parsed: 3, row entries: %d, unrowed entries: %d, "
        "disposition markings: %d, includes fields: %d, class names verified: %d"
        % (
            total_rows,
            total_unrowed,
            len(disposition_found),
            len(includes_found),
            class_count[0],
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
