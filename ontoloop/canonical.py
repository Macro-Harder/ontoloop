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
head signature, and head anchor. The bundle kind stands unbuilt
in every form, and the SPEC-CANON specification surface stands
unbuilt behind the module level guard at the foot of this file.
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
    "decode_canonical",
    "domain_separated",
    "encode_canonical",
    "encode_value",
    "hash_canonical",
    "sha256_hex",
]


def _check_kind(kind):
    if kind == KIND_BUNDLE:
        raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)
    if kind not in BUILT_KINDS:
        raise ValueError("unknown kind tag: %r" % (kind,))


def encode_value(value):
    """Return the canonical content bytes for one value.

    The content carries no domain separation. A floating point
    value anywhere in the value is refused, as mechanic 2 states
    for hashed objects.
    """
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
        parts = []
        for key in sorted(value.keys()):
            if not isinstance(key, str):
                raise TypeError("canonical form keys must be strings")
            parts.append(encode_value(key) + b":" + encode_value(value[key]))
        return b"{" + b",".join(parts) + b"}"
    if isinstance(value, (list, tuple)):
        return b"[" + b",".join(encode_value(item) for item in value) + b"]"
    raise TypeError("unsupported value in canonical form: %r" % type(value))


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
    """
    _check_kind(kind)
    header = DOMAIN_PREFIX + SEPARATOR + kind.encode("utf-8") + SEPARATOR
    if not isinstance(data, (bytes, bytearray)) or not bytes(data).startswith(header):
        raise ValueError("canonical content does not carry the named kind")
    return _Parser(bytes(data)[len(header):]).parse()


canonical_decode = decode_canonical


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)
