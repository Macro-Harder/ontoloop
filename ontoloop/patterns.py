"""Pattern set module, slice SPEC-PATTERN form.

The pattern set surface: the registered pattern set, version 1,
that redaction classification consumes as an input. The set
stands as stated data in this module: each family carries its
exact expression and its positive and negative worked cases,
with a boundary case per family, a completeness check over a
stated set, and a matching act decided by the stated expression
of each family.

Pattern set version 1 stands as authored specification in the
design record of this slice: no source stated an exact
expression or a worked case for any family, and the expressions
and cases in this module are the authored specification act of
slice SPEC-PATTERN, carrying the guessed source class, not text
transcribed from the brief or the plan.

What this slice does not build stands unbuilt behind the module
level guard at the foot of this file: the redaction scanner
itself and every consuming surface, any pattern set version
other than version 1, and any specification artifact outside
this module. A lookup of a public name this module does not
provide raises AssertionError in the NOT BUILT form the suite
harness uses. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.patterns"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "pattern_set",
    "matches",
    "boundary_readings",
    "completeness_check",
]


# Section: pattern set data and matching, roster 902.
# Names: _PATTERN_SET_V1, _BOUNDARY_CASES_V1,
# _BOUNDARY_DECISIONS_V1, pattern_set, and matches.
# Insertion point for the whole section: in
# system/ontoloop/patterns.py, after the module docstring and
# roster 904's constants at the head of the assembled file,
# before roster 903's boundary and completeness section and
# before roster 904's __all__ and guard foot at the foot, in
# the composition order the scope act states.
# Cross section contract, stated for the assembly check and
# for roster 903: the boundary case for a family stands at
# _BOUNDARY_CASES_V1[family], a plain string, and its authored
# decision stands at _BOUNDARY_DECISIONS_V1[family], the bool
# True for every family at version 1, where True states the
# authored MATCH decision, that the family expression
# fullmatches its boundary case. Both companion mappings are
# derived at module load from the one stated structure
# _PATTERN_SET_V1, so they cannot drift from it. Roster 903's
# boundary_readings can read either companion mapping, or the
# boundary_case and boundary_decision keys of an entry of
# _PATTERN_SET_V1, through the module globals at call time,
# without editing this section. No name in this section is
# defined by any other section, and this section calls no
# name another section owns.
# Refusal form, stated here and in this seat's paper: a
# version other than 1 and an unknown family name both raise
# ValueError, the stated refusal form the landed fragments
# use for an unknown argument to a present function. This
# section carries no in function NOT BUILT seam.

import re

# The authored version 1 pattern set, in whole form, taken
# from the appended specification part of
# design/steps/step-14-spec-pattern-shape.md. The families
# stand in the brief order, five families, each with its
# authored key string, its authored exact expression, its
# authored positive and negative worked cases exactly as
# authored, and its authored boundary case with its authored
# decision. True as a boundary_decision states MATCH.
# Everything in this structure is authored and guessed, in
# the honesty form the specification part states: no
# expression, key string, or case below is source text,
# transcription, or a registered value, and every case value
# is a synthetic shape example only.
_PATTERN_SET_V1 = (
    {
        "family": "private_key_block_headers",
        "expression": (
            "-----BEGIN (?:(?:RSA|EC|DSA|OPENSSH|ENCRYPTED|PGP) )?"
            "PRIVATE KEY-----"
        ),
        "positive_cases": (
            "-----BEGIN PRIV" "ATE KEY-----",
            "-----BEGIN RSA PRIV" "ATE KEY-----",
        ),
        "negative_cases": (
            "-----BEGIN PUBLIC KEY-----",
            "-----BEGIN PRIVATE KEY----",
        ),
        "boundary_case": "-----BEGIN OPENSSH PRIV" "ATE KEY-----",
        "boundary_decision": True,
    },
    {
        "family": "cloud_access_key_shapes",
        "expression": "(?:AKIA|ASIA)[0-9A-Z]{16}",
        "positive_cases": (
            "AKIA1234" "567890ABCDEF",
        ),
        "negative_cases": (
            "AKIA1234567890ABCDE",
            "akia1234567890ABCDEF",
        ),
        "boundary_case": "ASIA1234" "567890ABCDEF",
        "boundary_decision": True,
    },
    {
        "family": (
            "source_host_and_token_issuing_service_token_prefixes"
        ),
        "expression": (
            "(?:ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}"
            "|ghu_[A-Za-z0-9]{36}|ghs_[A-Za-z0-9]{36}"
            "|ghr_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}"
            "|glpat-[A-Za-z0-9_-]{20,}|xox[bpasr]-[A-Za-z0-9-]{10,}"
            "|npm_[A-Za-z0-9]{36}|pypi-[A-Za-z0-9_-]{20,}"
            "|sk_live_[A-Za-z0-9]{16,}|rk_live_[A-Za-z0-9]{16,})"
        ),
        "positive_cases": (
            "ghp_Ab1A" "b1Ab1Ab1Ab1Ab1Ab1Ab1Ab1Ab1Ab1Ab1",
            "xoxb-123" "4567890ab",
        ),
        "negative_cases": (
            "ghp_Ab1",
            "acme_1234567890ABCDEFGHIJ1234567890",
        ),
        "boundary_case": "glpat-aB3x" "Y9kLmN2pQ7rStUvW",
        "boundary_decision": True,
    },
    {
        "family": (
            "assignment_forms_pairing_a_credential_bearing_name"
            "_with_a_value"
        ),
        "expression": (
            "(?i)(?:client[ _-]secret|access[ _-]token"
            "|refresh[ _-]token|api[ _-]key|access[ _-]key"
            "|secret[ _-]key|private[ _-]key|signing[ _-]key"
            "|session[ _-]key|password|passwd|secret|token"
            "|apikey|authorisation|credentials|credential"
            "|passphrase|bearer)\\s*[:=]\\s*"
            "(?:\"[^\"\\s][^\"]*\"|'[^'\\s][^']*'"
            "|[^\\s;]{4,})"
        ),
        "positive_cases": (
            "password = Sy" "ntheticValue123",
            "api_key: sy" "nthetic-value-1234",
        ),
        "negative_cases": (
            "username = SyntheticValue123",
            "password:",
        ),
        "boundary_case": "client secret = Sy" "ntheticValue123",
        "boundary_decision": True,
    },
    {
        "family": "authorisation_header_forms",
        "expression": (
            "(?i)(?:Authorization|Proxy-Authorization):[ \\t]*"
            "(?:Bearer[ \\t]+[A-Za-z0-9._~+/=-]{8,}"
            "|Basic[ \\t]+[A-Za-z0-9+/]{8,}={0,2})"
        ),
        "positive_cases": (
            "Authorization: Bearer syn" "thetic-token-123456",
        ),
        "negative_cases": (
            "Authorization: Bearer short",
            "X-Api-Key: Bearer synthetic-token-123456",
        ),
        "boundary_case": "Authorization: Basic U3l" "udGhlVGljMTIz",
        "boundary_decision": True,
    },
)

_BOUNDARY_CASES_V1 = {
    entry["family"]: entry["boundary_case"]
    for entry in _PATTERN_SET_V1
}

_BOUNDARY_DECISIONS_V1 = {
    entry["family"]: entry["boundary_decision"]
    for entry in _PATTERN_SET_V1
}


def _entry_for_family(family):
    for entry in _PATTERN_SET_V1:
        if entry["family"] == family:
            return entry
    raise ValueError("unknown pattern family: %r" % (family,))


def pattern_set(version=1):
    """Return the pattern set for one version.

    At version 1, the only version this section builds, the
    return is a mapping keyed by the five family key strings
    in the brief order. Each value is an entry mapping whose
    keys are exactly expression, positive_cases, and
    negative_cases, in that order: the authored exact
    expression for the family, and its authored positive and
    negative worked cases as lists of case strings. The
    boundary case and its decision stand in the stated
    structure and in the companion mappings named in the
    header of this section, and they do not travel in this
    return, whose key set the tests pin exactly. A fresh
    mapping of fresh entry mappings holding fresh case lists
    is built on each call, so a caller cannot mutate the
    stated set through a returned value. Any version other
    than 1 raises ValueError, the stated refusal form named
    in the header of this section.
    """
    if version != 1:
        raise ValueError("unknown pattern set version: %r" % (version,))
    return {
        entry["family"]: {
            "expression": entry["expression"],
            "positive_cases": list(entry["positive_cases"]),
            "negative_cases": list(entry["negative_cases"]),
        }
        for entry in _PATTERN_SET_V1
    }


def matches(family, case, version=1):
    """Return whether a case matches a family expression.

    At version 1, the return is the bool True where the
    family expression fullmatches the case under
    re.fullmatch semantics, and the bool False where it does
    not. The expression applied is the same stated expression
    pattern_set returns for the family, read from the one
    stated structure, so this act and that return cannot
    disagree. Any version other than 1 raises ValueError,
    and an unknown family name raises ValueError, the stated
    refusal form named in the header of this section.
    """
    if version != 1:
        raise ValueError("unknown pattern set version: %r" % (version,))
    entry = _entry_for_family(family)
    return re.fullmatch(entry["expression"], case) is not None


# Section: failure and boundary, roster 903.
# Functions: boundary_readings, completeness_check.
# Insertion point for the whole section: in
# system/ontoloop/patterns.py, in the roster 903 failure
# and boundary section, after roster 902's data and
# matching section and before roster 904's __all__ list
# and guard foot, in the composition order the scope
# section 7 states.
# Cross section calls, stated for the assembly check:
# boundary_readings reads the version 1 pattern set by
# calling pattern_set through the module globals at call
# time, with the keyword version=1. pattern_set stands in
# roster 902's section. No part of roster 902's set data
# (no expression, no positive case, no negative case) is
# copied into this section: the family keys, and the
# expression each first reading applies, are read from
# that call at call time, and nothing else is read from
# roster 902's section.
# What this section itself carries, as its own authored
# data: the boundary case per family, drawn from the
# boundary worked cases the authored specification part
# appended to design/steps/step-14-spec-pattern-shape.md
# states, and the structural judgement table per family
# in the _structural_reading functions below. A structural
# reading is a hand stated shape judgement: it parses the
# case with plain string operations and judges the parsed
# parts against the family's named form. It never runs
# the family's expression, and it never runs any regular
# expression at all. The ground facts a structural
# reading judges against (the type word list of family 1,
# the prefixes and lengths of family 2, the prefix
# entries of family 3, the 19 grounded names of family 4,
# the header names and schemes of family 5) are the
# specification part's stated facts for that family,
# restated here as parsing tables. The production method
# differs from the first reading; the ground is shared,
# as two readings of one specification must share it.


# The boundary case per family, in the specification
# part's family order. Each string is copied character
# for character from the boundary case its family's item
# in the authored specification part states.
_BOUNDARY_CASES = {
    "private_key_block_headers": (
        "-----BEGIN OPENSSH PRIV" "ATE KEY-----"
    ),
    "cloud_access_key_shapes": "ASIA1234" "567890ABCDEF",
    "source_host_and_token_issuing_service_token_prefixes": (
        "glpat-aB3x" "Y9kLmN2pQ7rStUvW"
    ),
    "assignment_forms_pairing_a_credential_bearing_name_with_a_value": (
        "client secret = Sy" "ntheticValue123"
    ),
    "authorisation_header_forms": (
        "Authorization: Basic U3l" "udGhlVGljMTIz"
    ),
}


_ASCII_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_ASCII_LOWER = "abcdefghijklmnopqrstuvwxyz"
_ASCII_DIGITS = "0123456789"
_ASCII_ALNUM = _ASCII_UPPER + _ASCII_LOWER + _ASCII_DIGITS


def _all_in(text, allowed):
    return all(character in allowed for character in text)


# Structural reading, family 1: private key block
# headers. Judgement: the case is a single header line
# framed by five dashes at each end, opening with the
# word BEGIN, closing with the words PRIVATE KEY, and
# carrying at most one type word before PRIVATE KEY,
# from the authored closed list.
def _structural_reading_private_key_block_headers(case):
    frame = "-----"
    opening = frame + "BEGIN "
    if not case.startswith(opening):
        return False
    if not case.endswith(frame):
        return False
    core = case[len(opening):len(case) - len(frame)]
    if core == "PRIVATE KEY":
        return True
    parts = core.split(" ")
    type_words = {"RSA", "EC", "DSA", "OPENSSH", "ENCRYPTED", "PGP"}
    return (
        len(parts) == 3
        and parts[0] in type_words
        and parts[1] == "PRIVATE"
        and parts[2] == "KEY"
    )


# Structural reading, family 2: cloud access key shapes.
# Judgement: the case is exactly 20 characters long, its
# first four characters are one of the two authored
# prefixes, and its remaining 16 characters are each an
# upper case letter or a digit.
def _structural_reading_cloud_access_key_shapes(case):
    if len(case) != 20:
        return False
    if case[:4] not in ("AKIA", "ASIA"):
        return False
    return _all_in(case[4:], _ASCII_UPPER + _ASCII_DIGITS)


# Structural reading, family 3: source host and token
# issuing service token prefixes. Judgement: the case
# opens with one of the authored prefix entries, stated
# here as parsing rows of prefix, body length rule, and
# body character class, and the body after that prefix
# satisfies the entry's length rule and character class.
# A case opening with a listed prefix whose body fails
# that entry's rule is refused on that entry, and a case
# opening with no listed prefix is refused outright, so
# no generic token shape is admitted. Rows stand in the
# specification part's entry order P-1 to P-12, with the
# Slack row (P-8) judged by its own parse below the
# table, because its prefix carries a variable letter.
_PREFIX_ROWS = (
    # prefix, exact body length or None, minimum body
    # length, allowed body characters
    ("ghp_", 36, 36, _ASCII_ALNUM),
    ("gho_", 36, 36, _ASCII_ALNUM),
    ("ghu_", 36, 36, _ASCII_ALNUM),
    ("ghs_", 36, 36, _ASCII_ALNUM),
    ("ghr_", 36, 36, _ASCII_ALNUM),
    ("github_pat_", None, 22, _ASCII_ALNUM + "_"),
    ("glpat-", None, 20, _ASCII_ALNUM + "_-"),
    ("npm_", 36, 36, _ASCII_ALNUM),
    ("pypi-", None, 20, _ASCII_ALNUM + "_-"),
    ("sk_live_", None, 16, _ASCII_ALNUM),
    ("rk_live_", None, 16, _ASCII_ALNUM),
)


def _structural_reading_token_prefixes(case):
    for prefix, exact_length, minimum_length, allowed in _PREFIX_ROWS:
        if case.startswith(prefix):
            body = case[len(prefix):]
            if exact_length is not None and len(body) != exact_length:
                return False
            if len(body) < minimum_length:
                return False
            return _all_in(body, allowed)
    # Entry P-8, Slack: the letters xox, one letter from
    # the authored set, a hyphen, then a body of 10 or
    # more alphanumeric or hyphen characters.
    if (
        len(case) >= 5
        and case[:3] == "xox"
        and case[3] in "bpasr"
        and case[4] == "-"
    ):
        body = case[5:]
        return len(body) >= 10 and _all_in(body, _ASCII_ALNUM + "-")
    return False


# Structural reading, family 4: assignment forms pairing
# a credential bearing name with a value. Judgement: the
# case splits at its first colon or equals sign into a
# name part and a value part. The name part, lower cased
# and with underscore and hyphen separators read as the
# space of the normalised form, is one of the 19
# grounded Layer 1 names the specification part lists.
# The value part, after the whitespace the separator
# carries, is present in one of the authored value
# shapes: a double quoted value whose first character is
# neither a quote nor whitespace, a single quoted value
# on the same rule, or a bare value of 4 or more
# characters carrying no whitespace and no semicolon.
_ASSIGNMENT_NAMES = {
    "password",
    "passwd",
    "secret",
    "client secret",
    "token",
    "access token",
    "refresh token",
    "api key",
    "apikey",
    "access key",
    "secret key",
    "private key",
    "signing key",
    "session key",
    "authorisation",
    "credential",
    "credentials",
    "passphrase",
    "bearer",
}


def _structural_reading_assignment_forms(case):
    separator_positions = [
        position
        for position in (case.find("="), case.find(":"))
        if position != -1
    ]
    if not separator_positions:
        return False
    separator = min(separator_positions)
    name = case[:separator].rstrip().lower()
    name = name.replace("_", " ").replace("-", " ")
    if name not in _ASSIGNMENT_NAMES:
        return False
    value = case[separator + 1:].lstrip()
    if not value:
        return False
    if value[0] in ("\"", "'"):
        quote = value[0]
        return (
            len(value) >= 3
            and value.endswith(quote)
            and value[1] not in (quote, " ", "\t", "\n", "\r")
            and quote not in value[1:-1]
        )
    return (
        len(value) >= 4
        and ";" not in value
        and not any(character.isspace() for character in value)
    )


# Structural reading, family 5: authorisation header
# forms. Judgement: the case splits at its first colon
# into a header name and a rest. The header name, read
# without regard to letter case, is one of the two
# authored header names. The rest, after optional
# horizontal whitespace, splits into a scheme word and a
# body. The scheme, read without regard to letter case,
# is Bearer, whose body is 8 or more characters from the
# authored token character set, or Basic, whose body is
# 8 or more base characters followed by at most two
# equals padding characters.
def _structural_reading_authorisation_header_forms(case):
    colon = case.find(":")
    if colon == -1:
        return False
    header_name = case[:colon].lower()
    if header_name not in ("authorization", "proxy-authorization"):
        return False
    rest = case[colon + 1:].lstrip(" \t")
    parts = rest.split(None, 1)
    if len(parts) != 2:
        return False
    scheme = parts[0].lower()
    body = parts[1]
    if scheme == "bearer":
        allowed = _ASCII_ALNUM + "._~+/=-"
        return len(body) >= 8 and _all_in(body, allowed)
    if scheme == "basic":
        core = body.rstrip("=")
        padding = len(body) - len(core)
        if padding > 2:
            return False
        return len(core) >= 8 and _all_in(core, _ASCII_ALNUM + "+/")
    return False


# The structural reading per family, keyed by the same
# family key strings the boundary case table carries.
_STRUCTURAL_READINGS = {
    "private_key_block_headers": (
        _structural_reading_private_key_block_headers
    ),
    "cloud_access_key_shapes": (
        _structural_reading_cloud_access_key_shapes
    ),
    "source_host_and_token_issuing_service_token_prefixes": (
        _structural_reading_token_prefixes
    ),
    "assignment_forms_pairing_a_credential_bearing_name_with_a_value": (
        _structural_reading_assignment_forms
    ),
    "authorisation_header_forms": (
        _structural_reading_authorisation_header_forms
    ),
}


# Insertion point: roster 903 failure section, first new
# definition in this section in the assembled file.
def boundary_readings():
    """Return the boundary case and two readings per family.

    The version 1 pattern set is read by calling
    pattern_set through the module globals at call time,
    with the keyword version=1; that name stands in
    roster 902's section of the assembled module, so this
    is a cross section call, and the families of the
    return are keyed exactly as that call's return keys
    them. Returns a fresh mapping with exactly the keys
    families and findings. Each families entry carries
    exactly the keys boundary_case, first_reading, and
    second_reading. boundary_case is the family's
    authored boundary case, from this section's boundary
    case table. first_reading is the family's expression
    decision on that case: the bool True where the
    expression read from the pattern set entry full
    matches the case under re.fullmatch, and the bool
    False where it does not. The re module is imported
    inside this function, so this section carries no
    import statement of its own and no reading depends on
    another section's imports. second_reading is this
    section's structural reading of the same case: the
    bool its family's structural judgement function
    returns, produced by parsing the case as that
    function states, never by running the expression.
    Both readings are therefore bools, a reading form
    this section adopts as its authored form, the test
    pinning no reading type beyond comparability.
    findings is a list, in the pattern set's family
    order, naming exactly the families whose first and
    second readings differ, no more and no less, so a
    divergence between the expression and the structural
    judgement surfaces here in the test's own form. A
    family the pattern set returns that stands in
    neither of this section's tables raises KeyError
    rather than receiving an invented case or reading:
    the authored set carries exactly the five families
    its tables carry, and a further family is a scope
    change, not a form this function invents a reading
    for.
    """
    import re

    pattern_set = globals()["pattern_set"](version=1)
    families = {}
    findings = []
    for family, entry in pattern_set.items():
        boundary_case = _BOUNDARY_CASES[family]
        first_reading = (
            re.fullmatch(entry["expression"], boundary_case) is not None
        )
        second_reading = _STRUCTURAL_READINGS[family](boundary_case)
        families[family] = {
            "boundary_case": boundary_case,
            "first_reading": first_reading,
            "second_reading": second_reading,
        }
        if first_reading != second_reading:
            findings.append(family)
    return {"families": families, "findings": findings}


# Insertion point: roster 903 failure section, second
# new definition in this section in the assembled file.
def completeness_check(mapping):
    """Check a stated family mapping for missing expressions.

    Returns a fresh mapping with exactly the keys
    complete and incomplete. A family stands incomplete
    where its entry carries no expression, in any of
    these forms: the entry is None, which is the form
    the failure pair pins for a family stated only as a
    name; the entry is a mapping with no expression key;
    the entry is a mapping whose expression value is not
    truthy, an empty string among them; or the entry is
    any other value, which carries no expression field
    in the entry form the pattern set uses. incomplete
    is a list naming exactly the incomplete families, in
    the order the given mapping carries them. complete
    is the bool False where any family stands incomplete,
    and the bool True where none does, an empty mapping
    among the complete inputs. That complete form, the
    ordering, and the treatment of entry forms beyond
    the pinned None form are this section's authored
    readings, stated in its paper as such, because the
    test pins the check on the single None call alone.
    On the pinned call, completeness_check on a mapping
    holding family_without_expression with the value
    None, this returns complete False with incomplete
    equal to the list holding exactly that family.
    """
    incomplete = []
    for family, entry in mapping.items():
        if entry is None:
            incomplete.append(family)
            continue
        get_expression = getattr(entry, "get", None)
        if get_expression is None:
            incomplete.append(family)
        elif not get_expression("expression"):
            incomplete.append(family)
    return {"complete": not incomplete, "incomplete": incomplete}


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
