"""Canonical form module, tracer slice Commit 1 form.

One shared canonical byte form, in the registered forms at brief
Section 5.6 mechanics 1 to 3:

Mechanic 1: the hash algorithm is SHA-256.
Mechanic 2: UTF-8 with no byte order mark, keys in code point
order, no insignificant whitespace, integers in decimal with no
exponent, no floating point value in any hashed object, strings
as raw UTF-8 under a byte length prefix rendered in decimal,
hash links as lowercase hexadecimal, the literals true, false,
and null, and arrays in stated order.
Mechanic 3: domain separation is the prefix ontoloop-v1, a
separator byte of value zero, the kind tag, and a separator byte
of value zero, before all canonical content.

Content grammar, the tracer form of mechanic 2. A string is its
decimal byte length, a colon byte, then its raw UTF-8 bytes. A
byte string takes the same form over its raw bytes. An integer
is decimal ASCII. A mapping is an opening brace, its entries in
key code point order joined by commas, and a closing brace,
where each entry is the key in string form, a colon byte, then
the value. A sequence is an opening bracket, its items in
stated order joined by commas, and a closing bracket. This
module is the one implementation of the form: the store and
sealing modules call it directly and carry no encoder of their
own.

Built kind tags in this commit: journal record, manifest,
head signature, head anchor, and bundle. The SPEC-CANON
specification surface stands unbuilt behind the module level
guard at the foot of this file.
"""

import hashlib

MODULE_NAME = "ontoloop.canonical"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

DOMAIN_PREFIX = b"ontoloop-v1"
SEPARATOR = b"\x00"

HASH_ALGORITHM = "SHA-256"
CANONICAL_FORM_VERSION = 1

KIND_JOURNAL_RECORD = "journal record"
KIND_MANIFEST = "manifest"
KIND_HEAD_SIGNATURE = "head signature"
KIND_HEAD_ANCHOR = "head anchor"
KIND_BUNDLE = "bundle"

BUILT_KINDS = (
    KIND_JOURNAL_RECORD,
    KIND_MANIFEST,
    KIND_HEAD_SIGNATURE,
    KIND_HEAD_ANCHOR,
    KIND_BUNDLE,
)

__all__ = [
    "BUILT_KINDS",
    "CANONICAL_FORM_VERSION",
    "DOMAIN_PREFIX",
    "HASH_ALGORITHM",
    "KIND_BUNDLE",
    "KIND_HEAD_ANCHOR",
    "KIND_HEAD_SIGNATURE",
    "KIND_JOURNAL_RECORD",
    "KIND_MANIFEST",
    "MODULE_NAME",
    "NOT_BUILT_PREFIX",
    "SEPARATOR",
    "canonical_decode",
    "canonical_form",
    "canonical_form_from_specification",
    "check_vector",
    "conformance_vectors",
    "decode_canonical",
    "divergence_check",
    "domain_separated",
    "encode_canonical",
    "encode_value",
    "golden_byte_examples",
    "golden_record",
    "hash_canonical",
    "reading",
    "sealing_registrations",
    "sha256_hex",
    "worked_cases",
]


def _check_kind(kind):
    if kind not in BUILT_KINDS:
        raise ValueError("unknown kind tag: %r" % (kind,))


def encode_value(value, _path=None):
    """Return the canonical content bytes for one value.

    The content carries no domain separation. A floating point
    value anywhere in the value is refused, as mechanic 2 states
    for hashed objects. A container that stands on its own
    encoding path is a cycle on that path, and the act detects
    it and raises ValueError, the governed refusal form of this
    module, instead of recursing without bound. The path holds
    only the containers of the branch being encoded, so a value
    shared across branches in acyclic form encodes in the
    ordinary way, and deep finite nesting encodes to its full
    depth where the interpreter recursion allows it.
    Fix round 5, ruling 62, N-25: a finite value nested
    too deeply for the interpreter recursion to encode
    raises the governed ValueError form of this module,
    naming the value as too deeply nested in canonical
    form, beside the cyclic form above, and no encoding
    stands produced on that input.
    """
    try:
        if value is True:
            return b"true"
        if value is False:
            return b"false"
        if value is None:
            return b"null"
        if isinstance(value, float):
            raise ValueError("floating point value in a hashed object")
        if isinstance(value, int):
            return str(value).encode("ascii")
        if isinstance(value, str):
            raw = value.encode("utf-8")
            return str(len(raw)).encode("ascii") + b":" + raw
        if isinstance(value, (bytes, bytearray)):
            raw = bytes(value)
            return str(len(raw)).encode("ascii") + b":" + raw
        if isinstance(value, dict):
            if _path is None:
                _path = set()
            marker = id(value)
            if marker in _path:
                raise ValueError("cyclic value in canonical form")
            _path.add(marker)
            try:
                parts = []
                for key in sorted(value.keys()):
                    if not isinstance(key, str):
                        raise TypeError("canonical form keys must be strings")
                    parts.append(
                        encode_value(key, _path)
                        + b":"
                        + encode_value(value[key], _path)
                    )
                return b"{" + b",".join(parts) + b"}"
            finally:
                _path.discard(marker)
        if isinstance(value, (list, tuple)):
            if _path is None:
                _path = set()
            marker = id(value)
            if marker in _path:
                raise ValueError("cyclic value in canonical form")
            _path.add(marker)
            try:
                return (
                    b"["
                    + b",".join(encode_value(item, _path) for item in value)
                    + b"]"
                )
            finally:
                _path.discard(marker)
        raise TypeError("unsupported value in canonical form: %r" % type(value))
    except RecursionError:
        raise ValueError(
            "value too deeply nested in canonical form") from None


def domain_separated(kind, content):
    """Return content under the mechanic 3 domain separation rule."""
    _check_kind(kind)
    if not isinstance(content, (bytes, bytearray)):
        raise TypeError("canonical content must be bytes")
    return DOMAIN_PREFIX + SEPARATOR + kind.encode("utf-8") + SEPARATOR + bytes(content)


def encode_canonical(value, kind):
    """Return the domain separated canonical form of value under kind."""
    _check_kind(kind)
    return domain_separated(kind, encode_value(value))


canonical_form = encode_canonical


def sha256_hex(data):
    """Return the SHA-256 digest of data as lowercase hexadecimal."""
    return hashlib.sha256(bytes(data)).hexdigest()


def hash_canonical(value, kind):
    """Return the SHA-256 hash of the canonical form of value under kind."""
    return sha256_hex(encode_canonical(value, kind))


class _Parser:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def _peek(self):
        if self.pos >= len(self.data):
            raise ValueError("truncated canonical content")
        return self.data[self.pos:self.pos + 1]

    def _expect(self, token):
        if self.data[self.pos:self.pos + len(token)] != token:
            raise ValueError("malformed canonical content")
        self.pos += len(token)

    def parse(self):
        value = self._value()
        if self.pos != len(self.data):
            raise ValueError("trailing bytes in canonical content")
        return value

    def _value(self):
        token = self._peek()
        if token == b"{":
            return self._mapping()
        if token == b"[":
            return self._sequence()
        if token == b"t":
            self._expect(b"true")
            return True
        if token == b"f":
            self._expect(b"false")
            return False
        if token == b"n":
            self._expect(b"null")
            return None
        if token == b"-" or token.isdigit():
            return self._number_or_string()
        raise ValueError("malformed canonical content")

    def _digits(self):
        start = self.pos
        while self.pos < len(self.data) and self.data[self.pos:self.pos + 1].isdigit():
            self.pos += 1
        if self.pos == start:
            raise ValueError("malformed canonical content")
        return int(self.data[start:self.pos].decode("ascii"))

    def _raw(self, length):
        raw = self.data[self.pos:self.pos + length]
        if len(raw) != length:
            raise ValueError("truncated canonical content")
        self.pos += length
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw

    def _number_or_string(self):
        negative = False
        if self._peek() == b"-":
            negative = True
            self.pos += 1
        number = self._digits()
        if not negative and self._peek() == b":":
            self.pos += 1
            return self._raw(number)
        return -number if negative else number

    def _string(self):
        value = self._number_or_string()
        if not isinstance(value, (str, bytes)):
            raise ValueError("malformed canonical content")
        return value

    def _mapping(self):
        self._expect(b"{")
        result = {}
        if self._peek() == b"}":
            self.pos += 1
            return result
        while True:
            key = self._string()
            self._expect(b":")
            result[key] = self._value()
            if self._peek() == b",":
                self.pos += 1
                continue
            self._expect(b"}")
            return result

    def _sequence(self):
        self._expect(b"[")
        result = []
        if self._peek() == b"]":
            self.pos += 1
            return result
        while True:
            result.append(self._value())
            if self._peek() == b",":
                self.pos += 1
                continue
            self._expect(b"]")
            return result


def decode_canonical(data, kind):
    """Decode domain separated canonical bytes back to their value.

    The domain header must name kind exactly. Sequences decode
    as lists. A length prefixed item decodes as a string where
    its bytes are valid UTF-8, and as bytes otherwise.
    Fix round 5, ruling 62, N-25: canonical content nested
    too deeply for the interpreter recursion to parse raises
    the governed ValueError form of this module, naming the
    value as too deeply nested in canonical form, and no
    value stands decoded on that input.
    """
    _check_kind(kind)
    header = DOMAIN_PREFIX + SEPARATOR + kind.encode("utf-8") + SEPARATOR
    if not isinstance(data, (bytes, bytearray)) or not bytes(data).startswith(header):
        raise ValueError("canonical content does not carry the named kind")
    try:
        return _Parser(bytes(data)[len(header):]).parse()
    except RecursionError:
        raise ValueError(
            "value too deeply nested in canonical form") from None


canonical_decode = decode_canonical


# Insertion point: after the canonical_decode alias and before the module guard, roster 884 data section, first new definition in the assembled file.
def golden_byte_examples():
    """Return the golden canonical byte example for each hashed kind.

    The mapping carries exactly the three hashed kinds: journal
    record, manifest, and bundle. Each value is a stored literal
    byte string, stated in full in this function, and is not
    computed at call time from the encoder it pins. A fresh
    mapping is returned on each call.
    """
    return {
        KIND_JOURNAL_RECORD: (
            b"ontoloop-v1\x00journal record\x00"
            b"{4:name:21:journal record golden,5:value:1}"
        ),
        KIND_MANIFEST: (
            b"ontoloop-v1\x00manifest\x00"
            b"{4:name:15:manifest golden,5:value:2}"
        ),
        KIND_BUNDLE: (
            b"ontoloop-v1\x00bundle\x00"
            b"{4:name:13:bundle golden,5:value:3}"
        ),
    }


# Insertion point: after the canonical_decode alias and before the module guard, roster 884 data section, second new definition in the assembled file.
def golden_record(kind):
    """Return the golden record for one hashed kind.

    The record is the value whose canonical form under kind is
    the golden byte example for that kind. Only the three hashed
    kinds carry a golden record; any other kind raises
    ValueError. A fresh mapping is returned on each call.
    """
    if kind == KIND_JOURNAL_RECORD:
        return {"name": "journal record golden", "value": 1}
    if kind == KIND_MANIFEST:
        return {"name": "manifest golden", "value": 2}
    if kind == KIND_BUNDLE:
        return {"name": "bundle golden", "value": 3}
    raise ValueError("unknown kind tag: %r" % (kind,))


# Insertion point: after the canonical_decode alias and before the module guard, roster 884 data section, third new definition in the assembled file.
def worked_cases():
    """Return the worked cases for the divergence check.

    Each case is a mapping with the keys case, family, kind,
    input, and expected. The case key holds the case identity.
    The kind key holds the case kind, one of positive, negative,
    and boundary, and does not hold a hashed kind tag. Every
    family present carries exactly one case of each case kind.
    The input value is a value in the canonical value grammar,
    and expected states the reading outcome for that input, the
    string accept or the string refuse. A fresh list of fresh
    cases is returned on each call.
    """
    return [
        {
            "case": "field-order-positive",
            "family": "field order",
            "kind": "positive",
            "input": {"b": 1, "a": 2},
            "expected": "accept",
        },
        {
            "case": "field-order-negative",
            "family": "field order",
            "kind": "negative",
            "input": {"value": 1.5},
            "expected": "refuse",
        },
        {
            "case": "field-order-boundary",
            "family": "field order",
            "kind": "boundary",
            "input": {},
            "expected": "accept",
        },
        {
            "case": "item-order-positive",
            "family": "item order",
            "kind": "positive",
            "input": [2, 1],
            "expected": "accept",
        },
        {
            "case": "item-order-negative",
            "family": "item order",
            "kind": "negative",
            "input": [1.5],
            "expected": "refuse",
        },
        {
            "case": "item-order-boundary",
            "family": "item order",
            "kind": "boundary",
            "input": [],
            "expected": "accept",
        },
        {
            "case": "encoding-positive",
            "family": "encoding",
            "kind": "positive",
            "input": "abc",
            "expected": "accept",
        },
        {
            "case": "encoding-negative",
            "family": "encoding",
            "kind": "negative",
            "input": 1.5,
            "expected": "refuse",
        },
        {
            "case": "encoding-boundary",
            "family": "encoding",
            "kind": "boundary",
            "input": "",
            "expected": "accept",
        },
    ]


# Insertion point: after the canonical_decode alias and before the module guard, roster 884 data section, fourth new definition in the assembled file.
def sealing_registrations():
    """Return the sealing registration record for each hashed kind.

    The mapping carries exactly the three hashed kinds: journal
    record, manifest, and bundle. Each value is a mapping
    standing as a record for that kind, carrying a name key and
    a value key holding an integer. A fresh mapping of fresh
    records is returned on each call.
    """
    return {
        KIND_JOURNAL_RECORD: {
            "name": "journal record registration",
            "value": 1,
        },
        KIND_MANIFEST: {
            "name": "manifest registration",
            "value": 2,
        },
        KIND_BUNDLE: {
            "name": "bundle registration",
            "value": 3,
        },
    }


# Insertion point: in system/ontoloop/canonical.py, after the line canonical_decode = decode_canonical and before the module level __getattr__ guard, in the roster 885 checking section, after the roster 884 data section and before the roster 886 surface section.
def check_vector(vector):
    """Judge one conformance vector against the landed form.

    A vector is a mapping with exactly the keys name, input, and
    expected, in the form the tests pin. Only input and expected
    carry the judgement; name carries none. The judgement is a
    recomputation against the landed encoder, never a restatement
    of the vector's own expected value. Returns True, the bool
    itself, exactly when the expected value stands as one of the
    landed forms of the input: the canonical content bytes the
    landed encode_value produces for the input; the domain
    separated canonical form bytes of the input under a built
    kind, where the kind is either carried by the input itself as
    a value and kind pair or is the kind named in the domain
    header of the expected bytes; or the lowercase hexadecimal
    SHA-256, as sha256_hex renders it, of one of those byte forms.
    A value and kind pair stands as a mapping with exactly the
    keys value and kind, or record and kind, or as a two item
    sequence whose second item is the kind. Any other expected
    value returns False, and an input the landed encoder refuses,
    a floating point value among them, returns False for that
    byte form rather than raising.
    """
    try:
        value = vector["input"]
        expected = vector["expected"]
    except (TypeError, KeyError):
        return False
    byte_forms = []
    try:
        byte_forms.append(encode_value(value))
    except Exception:
        pass
    for kind in globals().get("BUILT_KINDS", ()):
        try:
            byte_forms.append(encode_canonical(value, kind))
        except Exception:
            pass
    pair = None
    if isinstance(value, dict):
        keys = set(value.keys())
        if keys == {"value", "kind"}:
            pair = (value["value"], value["kind"])
        elif keys == {"record", "kind"}:
            pair = (value["record"], value["kind"])
    elif isinstance(value, (list, tuple)) and len(value) == 2:
        pair = (value[0], value[1])
    if pair is not None:
        try:
            byte_forms.append(encode_canonical(pair[0], pair[1]))
        except Exception:
            pass
    if isinstance(expected, (bytes, bytearray)):
        return any(bytes(expected) == form for form in byte_forms)
    if isinstance(expected, str):
        return any(expected == sha256_hex(form) for form in byte_forms)
    return False


# Insertion point: in system/ontoloop/canonical.py, after the line canonical_decode = decode_canonical and before the module level __getattr__ guard, in the roster 885 checking section, after check_vector in this same section and before the roster 886 surface section.
def divergence_check(cases):
    """Return the divergences between the two readings of cases.

    Cases is the worked case sequence. Each worked case carries
    its identifier under the key case, its family under the key
    family, and its case class under the key kind, where the word
    kind in a worked case names the case class, positive,
    negative, or boundary, and never a hashed kind tag. The two
    readings are read by calling reading through the module
    globals at call time, once with reader first and once with
    reader second; reading stands in roster 886's section of the
    assembled module, so this is a cross section call. A case
    diverges where the two readings return different values for
    its identifier. Returns a mapping with exactly the keys
    divergences and plan_findings. Divergences lists one item per
    divergent case, in case order, each item carrying the keys
    case, first, and second, holding the case identifier and the
    two readings' values for it. Plan_findings lists one item per
    divergent case, in the same order and with the same keys and
    values, because every divergence is recorded as a plan
    finding naming the same case set, neither dropping a
    divergence nor inventing one. This function evidences the
    divergence machinery only: the two readings are two readings
    inside this one module, and nothing here presents them as
    independent implementations.
    """
    cases = list(cases)
    read = globals()["reading"]
    first = read(cases, reader="first")
    second = read(cases, reader="second")
    divergences = []
    plan_findings = []
    seen = set()
    for case in cases:
        case_id = case["case"]
        if case_id in seen:
            continue
        seen.add(case_id)
        if first[case_id] != second[case_id]:
            item = {
                "case": case_id,
                "first": first[case_id],
                "second": second[case_id],
            }
            divergences.append(item)
            plan_findings.append(dict(item))
    return {"divergences": divergences, "plan_findings": plan_findings}


# Section: surface and fixed text, roster 886.
# Functions: canonical_form_from_specification,
# conformance_vectors, reading.
# Insertion point for the whole section: between the landed alias
# canonical_decode = decode_canonical and the module guard foot,
# after the roster 884 data section and the roster 885 checking
# section, in the scope section 8 insertion order. The fixed foot
# edits (__all__ extension and __dir__ addition) are not in this
# fragment; they stand in foot-886.md as exact old and new text.
# Cross section contract stated for the assembly check:
# conformance_vectors returns vectors whose input is one value in
# the landed content grammar and whose expected is the stored
# literal content bytes that encode_value produces for that input,
# with no domain separation. Roster 885 check_vector judges a
# vector by that contract. reading returns a mapping from each
# case identifier to the case class word for that case, and
# roster 885 divergence_check reads both readings through the
# module globals at call time under the names first and second.

# Insert: surface section, before the module guard foot.
def canonical_form_from_specification(record, kind):
    """Return the canonical form of record under kind.

    This name names the hardcoded form landed in this module. It
    is a delegation to canonical_form, the one landed
    implementation of the form, and it reads no specification
    artifact: no file, no document, and no data structure standing
    for the specification is opened, parsed, or consulted here.
    The bytes returned are the bytes canonical_form produces for
    the same record and kind.
    """
    return canonical_form(record, kind)


# Insert: surface section, before the module guard foot.
def conformance_vectors(prop):
    """Return the shipped conformance vectors for one property.

    The property is one of the four exact strings the suite uses:
    field order, item order, line framing, and encoding. Each
    vector is a mapping with exactly the keys name, input, and
    expected. The input is one value in the landed content
    grammar, authored over text forms only: strings, integers,
    booleans, null, sequences, and mappings. No vector carries a
    bytes typed input, so no vector states an expected decode.
    The expected value of each vector is a stored literal: the
    canonical content bytes for the input, with no domain
    separation. An unknown property raises ValueError.
    """
    if prop == "field order":
        return [
            {
                "name": "field order: two keys stated out of order",
                "input": {"b": 1, "a": 2},
                "expected": b"{1:a:2,1:b:1}",
            },
            {
                "name": "field order: three keys stated reversed",
                "input": {"c": "x", "b": "y", "a": "z"},
                "expected": b"{1:a:1:z,1:b:1:y,1:c:1:x}",
            },
            {
                "name": "field order: nested mapping keys ordered",
                "input": {"outer": {"b": 1, "a": 2}},
                "expected": b"{5:outer:{1:a:2,1:b:1}}",
            },
        ]
    if prop == "item order":
        return [
            {
                "name": "item order: integers keep stated order",
                "input": [3, 1, 2],
                "expected": b"[3,1,2]",
            },
            {
                "name": "item order: strings keep stated order",
                "input": ["b", "a"],
                "expected": b"[1:b,1:a]",
            },
            {
                "name": "item order: sequence inside a mapping",
                "input": {"items": [2, 1]},
                "expected": b"{5:items:[2,1]}",
            },
        ]
    if prop == "line framing":
        return [
            {
                "name": "line framing: sequence carries no terminator",
                "input": [1, 2],
                "expected": b"[1,2]",
            },
            {
                "name": "line framing: mapping carries no terminator",
                "input": {"a": 1},
                "expected": b"{1:a:1}",
            },
            {
                "name": "line framing: string carries no frame bytes",
                "input": "abc",
                "expected": b"3:abc",
            },
        ]
    if prop == "encoding":
        return [
            {
                "name": "encoding: true literal",
                "input": True,
                "expected": b"true",
            },
            {
                "name": "encoding: false literal",
                "input": False,
                "expected": b"false",
            },
            {
                "name": "encoding: null literal",
                "input": None,
                "expected": b"null",
            },
            {
                "name": "encoding: positive integer in decimal",
                "input": 42,
                "expected": b"42",
            },
            {
                "name": "encoding: negative integer in decimal",
                "input": -7,
                "expected": b"-7",
            },
            {
                "name": "encoding: string under a byte length prefix",
                "input": "abc",
                "expected": b"3:abc",
            },
            {
                "name": "encoding: empty string",
                "input": "",
                "expected": b"0:",
            },
            {
                "name": "encoding: non ascii string as raw utf 8",
                "input": "é",
                "expected": b"2:\xc3\xa9",
            },
        ]
    raise ValueError("unknown conformance property: %r" % (prop,))


# Insert: surface section, before the module guard foot.
def reading(cases, reader="first"):
    """Return one named reading of the worked cases.

    The result maps each case identifier, the value at the case
    key of each worked case, to that reading's result for the
    case. The result for a case is its case class. In a worked
    case the kind key carries the case class, one of positive,
    negative, or boundary; it is never a hashed kind tag, and no
    part of this reading joins it to one. The first reading takes
    the case class as the case states it. The second reading
    classifies the case through its own table of the three case
    class words, and returns unclassified for a kind word outside
    that table, where the first reading returns the word as
    stated; on the shipped worked cases, whose kind words are
    exactly the three case classes, the two readings agree. An
    unknown reader name raises ValueError.
    """
    if reader == "first":
        return {case["case"]: case["kind"] for case in cases}
    if reader == "second":
        classes = {
            "positive": "positive",
            "negative": "negative",
            "boundary": "boundary",
        }
        # Fix round 7, ruling 158: an unhashable case kind
        # stands outside the table of the three case class
        # words, so it meets this reading in its stated
        # unclassified form, with no exception.
        classified = {}
        for case in cases:
            try:
                classified[case["case"]] = classes.get(
                    case["kind"], "unclassified")
            except (TypeError, ValueError):
                classified[case["case"]] = "unclassified"
        return classified
    raise ValueError("unknown reader: %r" % (reader,))


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
