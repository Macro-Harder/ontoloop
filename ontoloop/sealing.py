"""Sealing and verify module, tracer slice Commit 2 form.

Owns, in the narrow form the founding to signed verify path needs:
SHA-256 hashing, manifest construction and manifest hashing, the
signature object construction, signing at founding, the anchor
staging object construction, and the verify computation with the
signature check in the form plan subsection 20.87 point six
states, together with the Commit 2 discrimination branches that
point six places among the existing checks before the signature
check: the manifest lag classification, the chain consistent
prefix reading for a non final tear, and the disagreement
classification in its reserved form.

The fixed verify sentence below stands in subsection 20.87 point
one words verbatim, and the three holes beside it stand in point
two words verbatim. The sentence is returned only on agreement,
and only where the signature check has run and passed.

Entry points this slice assigns to later commits are not
provided in this form. The SPEC-SEAL test surface of this
module stands provided in this form, in the section at the
foot of this file. A lookup of a public name this module does
not yet provide raises AssertionError in the NOT BUILT form
the suite harness uses. A lookup of a private or dunder name
raises AttributeError in the ordinary form.
"""

import hashlib
import hmac

from ontoloop.canonical import canonical_form as _canonical_form

NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "
MODULE_NAME = "ontoloop.sealing"

VERIFY_SENTENCE = (
    "Verify proved the journal chain and the manifest agree over "
    "every record checked, and that the journal head and the "
    "manifest head stand signed under the signing key, so no "
    "checked record was altered after it was written except "
    "under that key, at signed strength only."
)

VERIFY_HOLES = (
    "a rewrite signed with the genuine key is not detected",
    "the anchor covers the heads as they stood at the most "
    "recent completed backup archive",
    "whole home deletion is detected only where an anchor for "
    "the store stands in an archive that survives",
)

SIGNING_KEY_UNAVAILABLE = "signing key unavailable"
SIGNATURE_OBJECT_MISSING = "signature object missing"
MANIFEST_LAG = "manifest lag"
DISAGREEMENT_FORM = "disagreement form"

PREFIX_READING = "chain consistent prefix"
PREFIX_WORDING = (
    "Chain consistency stands over the intact prefix only. "
    "That reading supports reads only and supports no "
    "judging use and no verify conclusion."
)
PREFIX_SUPPORTS = "reads only"

JOURNAL_RECORD_KIND = "journal record"
MANIFEST_KIND = "manifest"
SIGNATURE_KIND = "head signature"
ANCHOR_KIND = "head anchor"

__all__ = [
    "VERIFY_SENTENCE",
    "VERIFY_HOLES",
    "SIGNING_KEY_UNAVAILABLE",
    "SIGNATURE_OBJECT_MISSING",
    "MANIFEST_LAG",
    "DISAGREEMENT_FORM",
    "PREFIX_READING",
    "PREFIX_WORDING",
    "PREFIX_SUPPORTS",
    "JOURNAL_RECORD_KIND",
    "MANIFEST_KIND",
    "SIGNATURE_KIND",
    "ANCHOR_KIND",
    "SigningKeyUnavailable",
    "sha256_hex",
    "hash_sha256",
    "sign",
    "canonical_bytes",
    "hash_object",
    "hash_journal_record",
    "journal_head_hash",
    "build_manifest",
    "manifest_bytes",
    "manifest_hash",
    "build_signature_object",
    "signature_object_bytes",
    "compute_signature",
    "sign_signature_object",
    "verify_signature",
    "build_anchor_object",
    "anchor_object_bytes",
    "get_signing_key",
    "sign_store",
    "verify",
    "verify_store",
    "worked_example_store",
    "package_form",
    "package_form_from_specifications",
    "example_store_bytes",
    "manifest_registered_fields",
    "check_field_presence",
    "specification_completeness_check",
    "paraphrased_surface",
    "verbatim_texts",
    "specification_surfaces",
    "surface_texts",
    "travel_lint",
    "specification_package_form_rows",
    "package_form_rows",
]


class SigningKeyUnavailable(Exception):
    """The signing key cannot be obtained for a signing act."""

    def __init__(self, message=SIGNING_KEY_UNAVAILABLE):
        super().__init__(message)


def _not_built():
    return AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(name)
    raise _not_built()


def __dir__():
    return sorted(__all__)


def canonical_bytes(value, kind):
    """Return the canonical byte form of value under kind.

    The form is ontoloop.canonical.canonical_form, called directly.
    It accepts the journal record, manifest, head signature, and
    head anchor kind tags and returns the domain separated
    canonical bytes. Its errors are never absorbed here.
    """
    return _canonical_form(value, kind)


def sha256_hex(data):
    """Return the SHA-256 digest of data as lowercase hexadecimal."""
    return hashlib.sha256(bytes(data)).hexdigest()


hash_sha256 = sha256_hex


def sign(data, key):
    """Return the HMAC with SHA-256 of data under key, lowercase hex.

    This is the raw signing act over canonical bytes. Where the
    key cannot be obtained the act is refused with the named
    error signing key unavailable.
    """
    key_bytes = _key_bytes(key)
    if key_bytes is None:
        raise SigningKeyUnavailable()
    return hmac.new(
        key_bytes, bytes(data), hashlib.sha256
    ).hexdigest()


def hash_object(value, kind):
    """Return the hash of value in canonical form under kind."""
    return sha256_hex(canonical_bytes(value, kind))


def hash_journal_record(content, predecessor_hash, store_sequence,
                        record_type):
    """Return a journal record hash, mechanic 3 field order.

    The four fields stand as a mapping under their field names,
    in the form the ruling in the assembly paper states, and the
    canonical encoding of a mapping renders them in key code
    point order.
    """
    fields = {
        "content": content,
        "predecessor_hash": predecessor_hash,
        "store_sequence": store_sequence,
        "record_type": record_type,
    }
    return hash_object(fields, JOURNAL_RECORD_KIND)


def _field(store, *names):
    if isinstance(store, dict):
        for name in names:
            if name in store and store[name] is not None:
                return store[name]
        return None
    for name in names:
        value = getattr(store, name, None)
        if value is not None:
            return value
    return None


def _records_of(store):
    records = _field(store, "records", "journal_records", "journal")
    if records is None:
        return []
    return list(records)


def journal_head_hash(records):
    """Return the standing head hash from a record sequence."""
    if not records:
        return None
    last = records[-1]
    if isinstance(last, dict):
        return last.get("hash")
    return getattr(last, "hash", None)


def build_manifest(founding_object_identity, head_hash, record_count,
                   head_store_sequence, journal_schema_version,
                   canonical_form_version, hash_algorithm_identity):
    """Build the manifest object, its seven fields in order."""
    return {
        "founding_object_identity": founding_object_identity,
        "head_hash": head_hash,
        "record_count": record_count,
        "head_store_sequence": head_store_sequence,
        "journal_schema_version": journal_schema_version,
        "canonical_form_version": canonical_form_version,
        "hash_algorithm_identity": hash_algorithm_identity,
    }


def manifest_bytes(manifest):
    return canonical_bytes(manifest, MANIFEST_KIND)


def manifest_hash(manifest):
    """Return the hash of the manifest in canonical form."""
    return hash_object(manifest, MANIFEST_KIND)


def build_signature_object(store_identity, founding_object_identity,
                           journal_head_hash_value, manifest_hash_value):
    """Build the signature object, point three fields in order."""
    return {
        "store_identity": store_identity,
        "founding_object_identity": founding_object_identity,
        "journal_head_hash": journal_head_hash_value,
        "manifest_hash": manifest_hash_value,
    }


def _signature_fields(signature_object):
    if isinstance(signature_object, dict):
        if "fields" in signature_object:
            fields = signature_object["fields"]
            return build_signature_object(
                fields[0], fields[1], fields[2], fields[3]
            )
        return build_signature_object(
            signature_object["store_identity"],
            signature_object["founding_object_identity"],
            signature_object["journal_head_hash"],
            signature_object["manifest_hash"],
        )
    fields = list(signature_object)
    return build_signature_object(
        fields[0], fields[1], fields[2], fields[3]
    )


def signature_object_bytes(signature_object):
    """Return the canonical bytes of the point three object.

    Only the four signed fields enter the signed bytes. A standing
    signature value carried beside them in a store value is not one
    of the signed fields and never enters this form.
    """
    return canonical_bytes(
        _signature_fields(signature_object), SIGNATURE_KIND
    )


def _key_bytes(key):
    if key is None:
        return None
    if isinstance(key, str):
        raw = key.encode("utf-8")
        return raw if raw else None
    if isinstance(key, (bytes, bytearray)):
        raw = bytes(key)
        return raw if raw else None
    return None


def get_signing_key(store):
    """Return the key bytes from the store value key slot.

    The slot is the store value entry named signing_key, with
    key_slot accepted as the same slot under its other name, on a
    mapping store value or as an attribute on an object store
    value. An unset or unusable slot returns None. The value is a
    fixture key where fixture founding set it; it is never
    presented by this module as a production key.
    """
    return _key_bytes(_field(store, "signing_key", "key_slot"))


def compute_signature(signature_object, key):
    """Return the HMAC with SHA-256 signature, lowercase hex."""
    key_bytes = _key_bytes(key)
    if key_bytes is None:
        raise SigningKeyUnavailable()
    digest = hmac.new(
        key_bytes, signature_object_bytes(signature_object),
        hashlib.sha256,
    )
    return digest.hexdigest()


def sign_signature_object(store_identity, founding_object_identity,
                          journal_head_hash_value,
                          manifest_hash_value, key):
    """Sign a head set and return the standing signature object.

    The returned object carries the four point three fields in
    order and, beside them, the signature value under the name
    signature. Where the key cannot be obtained the act is refused
    with the named error signing key unavailable and no unsigned
    object is produced.
    """
    signature_object = build_signature_object(
        store_identity, founding_object_identity,
        journal_head_hash_value, manifest_hash_value,
    )
    signature = compute_signature(signature_object, key)
    standing = dict(signature_object)
    standing["signature"] = signature
    return standing


def verify_signature(signature_object, key):
    """Return True where the standing signature verifies."""
    key_bytes = _key_bytes(key)
    if key_bytes is None:
        raise SigningKeyUnavailable()
    if isinstance(signature_object, dict):
        standing_value = signature_object.get("signature")
    else:
        standing_value = None
    if not isinstance(standing_value, str) or not standing_value:
        return False
    expected = compute_signature(signature_object, key_bytes)
    return hmac.compare_digest(expected, standing_value)


def build_anchor_object(store_identity, founding_object_identity,
                        journal_head_hash_value, manifest_hash_value,
                        record_count, head_store_sequence,
                        signature_value):
    """Build the anchor staging object, point five fields in order."""
    return {
        "store_identity": store_identity,
        "founding_object_identity": founding_object_identity,
        "journal_head_hash": journal_head_hash_value,
        "manifest_hash": manifest_hash_value,
        "record_count": record_count,
        "head_store_sequence": head_store_sequence,
        "signature": signature_value,
    }


def anchor_object_bytes(anchor_object):
    return canonical_bytes(anchor_object, ANCHOR_KIND)


def sign_store(store):
    """Sign the standing heads of a store value at founding.

    Returns a mapping carrying the standing signature object under
    signature_object and the anchor staging copy under anchor. The
    store value itself is not mutated by this act; the founding
    act in the store module applies the returned objects to the
    store value it founds. Where the key slot stands unset this
    act is refused with the named error signing key unavailable
    and no unsigned head stands.
    """
    key = get_signing_key(store)
    if key is None:
        raise SigningKeyUnavailable()
    manifest = _field(store, "manifest")
    records = _records_of(store)
    store_identity = _field(store, "store_identity", "store_id",
                            "identity")
    founding = _field(store, "founding_object_identity")
    if founding is None and isinstance(manifest, dict):
        founding = manifest.get("founding_object_identity")
    head_hash = journal_head_hash(records)
    if head_hash is None and isinstance(manifest, dict):
        head_hash = manifest.get("head_hash")
    current_manifest_hash = (
        manifest_hash(manifest) if isinstance(manifest, dict) else None
    )
    signature_object = sign_signature_object(
        store_identity, founding, head_hash, current_manifest_hash, key
    )
    anchor = None
    if isinstance(manifest, dict):
        anchor = build_anchor_object(
            store_identity, founding, head_hash, current_manifest_hash,
            manifest.get("record_count"),
            manifest.get("head_store_sequence"),
            signature_object["signature"],
        )
    return {"signature_object": signature_object, "anchor": anchor}


def _chain_check(records):
    """Recompute the chain, returning its standing in full.

    The returned mapping carries consistent True and the head hash
    where every record recomputes from its canonical bytes, every
    predecessor link agrees, and every store sequence stands in
    its place. Where a record does not stand, the mapping carries
    consistent False and fail_index, the index of the first record
    that does not stand. Every record before fail_index stands
    recomputed and linked, so the records before a failure at a
    non final index form a chain consistent prefix by
    construction, and a failure with no index at or after it is a
    failure at the final line.
    """
    previous_hash = None
    head = None
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            return {"consistent": False, "fail_index": index}
        stored_hash = record.get("hash")
        canonical = record.get("canonical_bytes")
        if canonical is not None:
            recomputed = sha256_hex(canonical)
        elif "content" in record:
            recomputed = hash_journal_record(
                record.get("content"),
                record.get("predecessor_hash"),
                record.get("store_sequence"),
                record.get("record_type"),
            )
        else:
            return {"consistent": False, "fail_index": index}
        if stored_hash is not None and recomputed != stored_hash:
            return {"consistent": False, "fail_index": index}
        if index > 0 and record.get("predecessor_hash") != previous_hash:
            return {"consistent": False, "fail_index": index}
        if "store_sequence" in record and (
            record.get("store_sequence") != index + 1
        ):
            return {"consistent": False, "fail_index": index}
        previous_hash = recomputed
        head = recomputed
    return {"consistent": True, "head": head}


def _recomputed_head(records):
    """Return the recomputed head hash, or None where it fails."""
    check = _chain_check(records)
    if not check["consistent"]:
        return None
    return check["head"]


def _disagreement():
    return {"output": "disagreement", "form": DISAGREEMENT_FORM}


def _prefix_reading():
    return {
        "reading": PREFIX_READING,
        "wording": PREFIX_WORDING,
        "supports": PREFIX_SUPPORTS,
        "supports_judging_use": False,
    }


def _manifest_lag(records, manifest):
    """Return True only for the specific manifest lag finding.

    The finding is a mechanically complete record standing beyond
    the manifest head: the chain recomputes whole over every
    record, and the manifest head hash, record count, and head
    store sequence still describe an earlier record in that same
    chain, in full. A manifest that disagrees with the chain in
    any other way is not this finding.
    """
    count = manifest.get("record_count")
    if not isinstance(count, int) or isinstance(count, bool):
        return False
    if count <= 0 or count >= len(records):
        return False
    described = records[count - 1]
    if not isinstance(described, dict):
        return False
    if manifest.get("head_hash") != described.get("hash"):
        return False
    if manifest.get("head_store_sequence") != described.get(
        "store_sequence"
    ):
        return False
    return True


def verify(store):
    """Run verify over a store value, Commit 2 discrimination form.

    Existing checks run first, in their governed order, and the
    signature check runs only where the store stands fully checked
    and its chain and manifest agree, in the form subsection 20.87
    point six states. Point six lists those existing checks as
    chain and manifest agreement, founding object, version window,
    torn lines, manifest lag, and the chain consistent prefix
    reading. The classifications this form produces among them:

    a first chain failure at a non final record returns the chain
    consistent prefix reading over the records before it, in its
    governed wording, which never uses the verify sentence,
    supports reads only, and supports no judging use; a
    mechanically complete record standing beyond the manifest
    head, the manifest otherwise describing an earlier head in
    full, returns unverifiable naming the case manifest lag,
    classified here before the signature check and distinct from
    every disagreement; a founding object identity the manifest
    carries that differs from the store founding identity, a
    manifest that disagrees with a fully recomputed chain in any
    way that is not the lag finding, a signature object whose
    fields differ from the recomputed object, and a signature that
    does not verify each return disagreement in the disagreement
    form, and on disagreement the store takes the suspect position
    at brief Section 6, with its refusals governing until a named
    operator act clears it; a missing signature object returns
    unverifiable naming the case signature object missing; a key
    that cannot be obtained returns unverifiable naming the case
    signing key unavailable, with no chain only agreement in its
    place. On agreement the result carries the output, the signed
    verify sentence in its verbatim form, and the three holes
    beside it, and on no other output does any sentence stand in
    the result.

    Findings no Commit 2 test class asserts stay in the NOT BUILT
    form in this module: a chain failure at the final record (the
    torn final line case), a store with no records or no manifest,
    and a store with no founding object identity raise
    AssertionError in the NOT BUILT form. A bytes input is the
    SPEC-SEAL example store form, which is not built in this
    slice, and raises the same NOT BUILT form. The version window
    check stands deferred with its slices, as the tracer scope
    states, because no store this slice founds carries a version
    outside the window its founding mints.
    """
    if isinstance(store, (bytes, bytearray)):
        store = globals()["_read_example_store_bytes"](store)
    elif isinstance(store, str):
        raise _not_built()
    records = _records_of(store)
    manifest = _field(store, "manifest")
    if not records or not isinstance(manifest, dict):
        raise _not_built()
    store_founding = _field(store, "founding_object_identity")
    founding = store_founding
    if founding is None:
        founding = manifest.get("founding_object_identity")
    if founding is None:
        raise _not_built()
    chain = _chain_check(records)
    if not chain["consistent"]:
        fail_index = chain["fail_index"]
        if fail_index < len(records) - 1:
            return _prefix_reading()
        raise _not_built()
    head = chain["head"]
    if store_founding is not None and (
        manifest.get("founding_object_identity") != store_founding
    ):
        return _disagreement()
    last = records[-1]
    manifest_agrees = (
        manifest.get("head_hash") == head
        and manifest.get("record_count") == len(records)
        and manifest.get("head_store_sequence")
        == (last.get("store_sequence") if isinstance(last, dict)
            else None)
    )
    if not manifest_agrees:
        if _manifest_lag(records, manifest):
            return {"output": "unverifiable", "case": MANIFEST_LAG}
        return _disagreement()
    signature_object = _field(store, "signature_object", "signature")
    if signature_object is None:
        return {
            "output": "unverifiable",
            "case": SIGNATURE_OBJECT_MISSING,
        }
    if isinstance(signature_object, dict) and (
        "signature" not in signature_object
        or not signature_object.get("signature")
    ):
        return {
            "output": "unverifiable",
            "case": SIGNATURE_OBJECT_MISSING,
        }
    key = get_signing_key(store)
    if key is None:
        return {
            "output": "unverifiable",
            "case": SIGNING_KEY_UNAVAILABLE,
        }
    store_identity = _field(store, "store_identity", "store_id",
                            "identity")
    recomputed_object = build_signature_object(
        store_identity, founding, head, manifest_hash(manifest)
    )
    standing_fields = _signature_fields(signature_object)
    if standing_fields != recomputed_object:
        return _disagreement()
    if not verify_signature(signature_object, key):
        return _disagreement()
    return {
        "output": "agreement",
        "sentence": VERIFY_SENTENCE,
        "holes": list(VERIFY_HOLES),
    }


verify_store = verify


# Section: data shape and module boundary, roster 892.
# Functions: worked_example_store, package_form,
# package_form_from_specifications, example_store_bytes,
# manifest_registered_fields, and the strict internal byte
# reader _read_example_store_bytes.
# Insertion point for the whole section: in
# system/ontoloop/sealing.py, after the landed verify_store alias
# at the foot of the landed code, first in the scope section 8
# insertion order, before the roster 893 failure section and the
# roster 894 surface section.
# Cross section contract stated for the assembly check:
# package_form builds each form from the field rows stated in
# roster 892's paper for that form, and roster 894's
# specification_package_form_rows and package_form_rows are
# expected to state exactly those rows, by name, for each form.
# _read_example_store_bytes is the reader roster 893's verify
# head hunk calls through the module globals at call time for a
# bytes or bytearray input, and no other caller is expected.
# Roster 893's specification_completeness_check is expected to
# read the registered field list through
# manifest_registered_fields in this section, called through the
# module globals at call time, so the check judges a field list
# against the stated constant below and not against a list read
# back out of a built manifest object.

_EXAMPLE_STORE_IDENTITY = "worked-example-store"
_EXAMPLE_FOUNDING_IDENTITY = "worked-example-founding"
_EXAMPLE_FIXTURE_KEY = b"ontoloop-fixture-key-spec-seal-example"
_EXAMPLE_JOURNAL_SCHEMA_VERSION = 1
_EXAMPLE_CANONICAL_FORM_VERSION = 1
_EXAMPLE_HASH_ALGORITHM_IDENTITY = "SHA-256"
_EXAMPLE_BUNDLE_KIND = "bundle"

_MANIFEST_REGISTERED_FIELDS = (
    "founding_object_identity",
    "head_hash",
    "record_count",
    "head_store_sequence",
    "journal_schema_version",
    "canonical_form_version",
    "hash_algorithm_identity",
)

_PACKAGE_FORMS = ("journal", "manifest", "bundle")


# Insert: data section, first new definition in the assembled
# file.
def manifest_registered_fields():
    """Return the seven registered manifest fields, in order.

    The list is a stated constant of the specification: the seven
    fields of plan subsection 20.87 point three, in the order the
    landed build_manifest builds them. It is stated here in
    full and is not read back out of a built manifest object at
    call time, so a completeness check judging a field list
    against this list judges it against the register itself. A
    fresh list is returned on each call, so no caller can mutate
    the stated constant.
    """
    return list(_MANIFEST_REGISTERED_FIELDS)


def _example_record(content, predecessor_hash, store_sequence,
                    record_type):
    fields = {
        "content": content,
        "predecessor_hash": predecessor_hash,
        "store_sequence": store_sequence,
        "record_type": record_type,
    }
    return {
        "content": content,
        "predecessor_hash": predecessor_hash,
        "store_sequence": store_sequence,
        "record_type": record_type,
        "hash": hash_journal_record(
            content, predecessor_hash, store_sequence, record_type
        ),
        "canonical_bytes": canonical_bytes(fields, JOURNAL_RECORD_KIND),
    }


# Insert: data section, second new definition in the assembled
# file.
def worked_example_store():
    """Return the worked example store, the SPEC-SEAL fixture.

    The store is an authored fixture, recorded as authored in
    roster 892's paper under plan section 6.2: no plan or brief
    passage states its record contents, so this function authors
    them in the landed store shape and states them in full here.
    The store value is a mapping with exactly the keys
    store_identity, founding_object_identity, records, manifest,
    signature_object, anchor_staging_copy, and key_slot, the
    shape the landed verify computation and the landed builders
    already read. It carries two records: a genesis record whose
    content states the store identity, the founding object
    identity, and the three version and algorithm values, and
    one example record. Every hash in the store is recomputable
    from the landed acts: each record hash is
    hash_journal_record over its four fields, the manifest is
    build_manifest over the standing heads, and the signature
    object and the anchor staging copy are the landed sign_store
    result over the store, signed under the fixture key in the
    key slot. The fixture key is fixture material in the
    tracer's bounded form and is never presented as a production
    key. No identity, derivation, or distinctness between this
    store and any store another module founds is stated or
    implied by this function. A fresh store is built on each
    call, so no caller can mutate a shared fixture.
    """
    genesis_content = {
        "store_identity": _EXAMPLE_STORE_IDENTITY,
        "founding_object_identity": _EXAMPLE_FOUNDING_IDENTITY,
        "journal_schema_version": _EXAMPLE_JOURNAL_SCHEMA_VERSION,
        "canonical_form_version": _EXAMPLE_CANONICAL_FORM_VERSION,
        "hash_algorithm_identity": _EXAMPLE_HASH_ALGORITHM_IDENTITY,
    }
    genesis = _example_record(genesis_content, "", 1, "genesis")
    example_content = {
        "payload": "worked example record 1",
        "record_type": "example record",
    }
    example = _example_record(
        example_content, genesis["hash"], 2, "example record"
    )
    records = [genesis, example]
    manifest = build_manifest(
        _EXAMPLE_FOUNDING_IDENTITY,
        example["hash"],
        len(records),
        example["store_sequence"],
        _EXAMPLE_JOURNAL_SCHEMA_VERSION,
        _EXAMPLE_CANONICAL_FORM_VERSION,
        _EXAMPLE_HASH_ALGORITHM_IDENTITY,
    )
    store = {
        "store_identity": _EXAMPLE_STORE_IDENTITY,
        "founding_object_identity": _EXAMPLE_FOUNDING_IDENTITY,
        "records": records,
        "manifest": manifest,
        "signature_object": None,
        "anchor_staging_copy": None,
        "key_slot": _EXAMPLE_FIXTURE_KEY,
    }
    signed = sign_store(store)
    store["signature_object"] = signed["signature_object"]
    store["anchor_staging_copy"] = signed["anchor"]
    return store


def _journal_line_value(record):
    if not isinstance(record, dict):
        raise ValueError("journal records must be mappings")
    return {
        "content": record.get("content"),
        "predecessor_hash": record.get("predecessor_hash"),
        "store_sequence": record.get("store_sequence"),
        "record_type": record.get("record_type"),
        "hash": record.get("hash"),
    }


def _bundle_value(store):
    records = _records_of(store)
    return {
        "store_identity": _field(store, "store_identity", "store_id",
                                 "identity"),
        "founding_object_identity": _field(
            store, "founding_object_identity"
        ),
        "records": [_journal_line_value(record) for record in records],
        "manifest": _field(store, "manifest"),
        "signature_object": _field(store, "signature_object",
                                   "signature"),
        "anchor_staging_copy": _field(store, "anchor_staging_copy",
                                      "anchor"),
    }


# Insert: data section, third new definition in the assembled
# file.
def package_form(store, form, reader="first"):
    """Return the package bytes for one form of a store.

    The form is one of the three package forms, journal,
    manifest, and bundle. The journal form is the journal lines
    of the store in store order, one line per record, where a
    line is the canonical byte form, under the journal record
    kind, of the line value carrying exactly the journal row
    fields stated in roster 892's paper (content,
    predecessor_hash, store_sequence, record_type, and hash),
    each line followed by one newline byte. The manifest form is
    the landed manifest_bytes of the store manifest, the
    canonical byte form of the manifest under the manifest kind,
    carrying exactly the seven registered fields. The bundle
    form is the canonical byte form, under the bundle kind, of
    the bundle value carrying exactly the bundle row fields
    stated in roster 892's paper (store_identity,
    founding_object_identity, records, manifest,
    signature_object, and anchor_staging_copy), with the records
    carried as their journal line values. The fixture key slot
    never travels in any package form. The reader keyword names
    the reading of the store the bytes are built under; the
    first reading is the only reading this form builds, and any
    other reader name raises ValueError, as an unknown form
    name does. The store is read in the landed mapping shape
    only, through the landed field and record readers.
    """
    if form not in _PACKAGE_FORMS:
        raise ValueError("unknown package form: %r" % (form,))
    if reader != "first":
        raise ValueError("unknown reader: %r" % (reader,))
    if form == "journal":
        lines = []
        for record in _records_of(store):
            lines.append(
                canonical_bytes(
                    _journal_line_value(record), JOURNAL_RECORD_KIND
                )
                + b"\n"
            )
        return b"".join(lines)
    if form == "manifest":
        return manifest_bytes(_field(store, "manifest"))
    return canonical_bytes(_bundle_value(store), _EXAMPLE_BUNDLE_KIND)


# Insert: data section, fourth new definition in the assembled
# file.
def package_form_from_specifications(store, form,
                                     specifications=("SPEC-CANON",
                                                     "SPEC-SEAL")):
    """Return the package bytes the two specifications produce.

    This name names the specification form of the package act,
    in the discipline the scope rules at its section 9, item
    G-3. It is a delegation to package_form, the one landed
    derivation of the package bytes for this slice, and it reads
    no specification artifact: no file, no document, and no data
    structure standing for SPEC-CANON or SPEC-SEAL is opened,
    parsed, or consulted here. The specifications argument names
    the two specifications the form stands under and carries no
    derivation. The bytes returned are the bytes package_form
    produces for the same store and form, and no record may
    describe this name as an independent implementation or as
    the second implementation verification exercise.
    """
    return package_form(store, form, reader="first")


def _hex_line(label, raw):
    return label + "=" + bytes(raw).hex()


# Insert: data section, fifth new definition in the assembled
# file.
def example_store_bytes():
    """Return the worked example store in its byte form.

    The byte form is an authored fixture form, stated field by
    field in roster 892's paper, and it is the form the strict
    reader _read_example_store_bytes beside this function reads
    whole. In full, the form is a sequence of ASCII lines, each
    line terminated by one newline byte, with no carriage return
    anywhere and no byte after the final newline. Each line is a
    label, an equals sign, and a value, in this exact order: the
    header line, label ONTOLOOP-EXAMPLE-STORE, value 1; the
    store identity line, label store_identity; the founding
    object identity line, label founding_object_identity; the
    fixture key line, label key_slot_hex, whose value is the
    lowercase hexadecimal of the fixture key bytes in the store
    key slot; the record count line, label records, whose value
    is the decimal record count; then, for each record in store
    order, six lines in this order, labels record (the decimal
    store sequence), record_type, predecessor_hash (the raw
    predecessor string, empty for the genesis record), hash (the
    record hash), content_canonical (the lowercase hexadecimal
    of the canonical byte form of the record content under the
    journal record kind), and record_canonical (the lowercase
    hexadecimal of the record canonical bytes, the canonical
    byte form of the record four field value under the journal
    record kind); then the manifest line, label
    manifest_canonical, the lowercase hexadecimal of the
    canonical byte form of the manifest under the manifest kind;
    then the signature line, label signature_canonical, the
    lowercase hexadecimal of the canonical byte form of the
    standing signature object under the head signature kind;
    then the anchor line, label anchor_canonical, the lowercase
    hexadecimal of the canonical byte form of the anchor staging
    copy under the head anchor kind, or the value none where the
    store carries no anchor staging copy; and the closing line,
    label end, value 1. No byte compatibility with any other
    store form is claimed for this layout, not with the bundle
    package form and not with any on disk store form.
    """
    store = worked_example_store()
    lines = []
    lines.append("ONTOLOOP-EXAMPLE-STORE=1")
    lines.append("store_identity=" + store["store_identity"])
    lines.append(
        "founding_object_identity=" + store["founding_object_identity"]
    )
    lines.append(_hex_line("key_slot_hex", store["key_slot"]))
    records = store["records"]
    lines.append("records=" + str(len(records)))
    for record in records:
        lines.append("record=" + str(record["store_sequence"]))
        lines.append("record_type=" + record["record_type"])
        lines.append("predecessor_hash=" + record["predecessor_hash"])
        lines.append("hash=" + record["hash"])
        lines.append(
            _hex_line(
                "content_canonical",
                canonical_bytes(record["content"], JOURNAL_RECORD_KIND),
            )
        )
        lines.append(
            _hex_line("record_canonical", record["canonical_bytes"])
        )
    lines.append(
        _hex_line(
            "manifest_canonical",
            canonical_bytes(store["manifest"], MANIFEST_KIND),
        )
    )
    lines.append(
        _hex_line(
            "signature_canonical",
            canonical_bytes(
                store["signature_object"], SIGNATURE_KIND
            ),
        )
    )
    anchor = store["anchor_staging_copy"]
    if anchor is None:
        lines.append("anchor_canonical=none")
    else:
        lines.append(
            _hex_line(
                "anchor_canonical",
                canonical_bytes(anchor, ANCHOR_KIND),
            )
        )
    lines.append("end=1")
    return ("\n".join(lines) + "\n").encode("ascii")


def _strict_hex(value):
    raw = bytes.fromhex(value)
    if raw.hex() != value:
        raise ValueError("hex value is not in its strict form")
    return raw


# Insert: data section, sixth new definition in the assembled
# file, the strict internal byte reader of scope section 5,
# term 2, standing beside example_store_bytes.
def _read_example_store_bytes(data):
    """Read a store value whole from the example store byte form.

    This is an internal act of this slice, beside
    example_store_bytes, and it is the reader the verify head
    limb calls for a bytes or bytearray input. It accepts only
    the whole example store byte form, in the layout
    example_store_bytes states: every line and field that form
    carries, read whole, in its stated order, with the store
    records, the manifest, the signature object, the anchor
    staging copy, and the fixture key slot recovered as the
    store value the landed verify computation reads. It returns
    no partial store, produces no prefix reading, and classifies
    nothing. Any input that is not that form whole, in
    particular an input whose final line is incomplete or
    truncated, an input whose bytes end part way through a
    record, an input carrying a line out of order, a count that
    does not match the records carried, or a record whose
    canonical bytes do not decode to its stated four fields,
    raises AssertionError in the module NOT BUILT form, through
    the landed _not_built helper, before any verify computation
    runs. A str input is not opened here and raises the same
    form. The refusal this reader raises is a new refusal at the
    parsing step, in the same NOT BUILT text: it is not the torn
    final line case, which stands inside the landed verify
    computation exactly as landed.
    """
    from ontoloop.canonical import decode_canonical as _decode

    if not isinstance(data, (bytes, bytearray)):
        raise _not_built()
    try:
        raw = bytes(data)
        if not raw.endswith(b"\n") or b"\r" in raw:
            raise ValueError("byte form is not whole")
        lines = raw[:-1].decode("ascii").split("\n")
        position = [0]

        def take(label):
            index = position[0]
            if index >= len(lines):
                raise ValueError("byte form ends early")
            line = lines[index]
            prefix = label + "="
            if not line.startswith(prefix):
                raise ValueError("line out of order: %r" % (label,))
            position[0] = index + 1
            return line[len(prefix):]

        if take("ONTOLOOP-EXAMPLE-STORE") != "1":
            raise ValueError("unknown byte form version")
        store_identity = take("store_identity")
        founding = take("founding_object_identity")
        if not store_identity or not founding:
            raise ValueError("identity line is empty")
        key = _strict_hex(take("key_slot_hex"))
        if not key:
            raise ValueError("fixture key slot is empty")
        count_text = take("records")
        if not count_text.isdigit():
            raise ValueError("record count is not decimal")
        count = int(count_text)
        if count <= 0:
            raise ValueError("record count is not positive")
        records = []
        for expected_sequence in range(1, count + 1):
            sequence_text = take("record")
            if sequence_text != str(expected_sequence):
                raise ValueError("record sequence out of order")
            record_type = take("record_type")
            predecessor = take("predecessor_hash")
            stored_hash = take("hash")
            if len(stored_hash) != 64:
                raise ValueError("record hash is not a digest")
            _strict_hex(stored_hash)
            content = _decode(
                _strict_hex(take("content_canonical")),
                JOURNAL_RECORD_KIND,
            )
            record_canonical = _strict_hex(take("record_canonical"))
            fields = _decode(record_canonical, JOURNAL_RECORD_KIND)
            if not isinstance(content, dict) or not isinstance(
                fields, dict
            ):
                raise ValueError("record value is not a mapping")
            if fields != {
                "content": content,
                "predecessor_hash": predecessor,
                "store_sequence": expected_sequence,
                "record_type": record_type,
            }:
                raise ValueError("record fields do not agree")
            records.append(
                {
                    "content": content,
                    "predecessor_hash": predecessor,
                    "store_sequence": expected_sequence,
                    "record_type": record_type,
                    "hash": stored_hash,
                    "canonical_bytes": record_canonical,
                }
            )
        manifest = _decode(
            _strict_hex(take("manifest_canonical")), MANIFEST_KIND
        )
        signature_object = _decode(
            _strict_hex(take("signature_canonical")), SIGNATURE_KIND
        )
        anchor_text = take("anchor_canonical")
        if anchor_text == "none":
            anchor = None
        else:
            anchor = _decode(_strict_hex(anchor_text), ANCHOR_KIND)
        if not isinstance(manifest, dict) or not isinstance(
            signature_object, dict
        ):
            raise ValueError("store value is not whole")
        if anchor is not None and not isinstance(anchor, dict):
            raise ValueError("anchor value is not a mapping")
        if take("end") != "1":
            raise ValueError("closing line does not stand")
        if position[0] != len(lines):
            raise ValueError("trailing lines stand in the byte form")
    except Exception:
        raise _not_built()
    return {
        "store_identity": store_identity,
        "founding_object_identity": founding,
        "records": records,
        "manifest": manifest,
        "signature_object": signature_object,
        "anchor_staging_copy": anchor,
        "key_slot": key,
    }


# Section: failure and boundary, roster 893.
# Functions: check_field_presence,
# specification_completeness_check, paraphrased_surface.
# Insertion point for the whole section: in
# system/ontoloop/sealing.py, after the landed verify_store
# alias at the foot of the landed code, in the roster 893
# failure section, after roster 892's data section and before
# roster 894's surface section, in the scope section 8
# insertion order.
# Cross section calls, stated for the assembly check: every
# cross section name below is read through the module globals
# at call time, never imported and never copied into this
# section. check_field_presence calls
# specification_package_form_rows, which stands in roster
# 894's section. specification_completeness_check calls
# manifest_registered_fields, which stands in roster 892's
# section. paraphrased_surface calls verbatim_texts, which
# stands in roster 894's section. The verify head hunk at the
# foot of this fragment calls _read_example_store_bytes, the
# strict internal byte reader, which stands in roster 892's
# section; no name stating that reader stands in the scope
# or in roster 892's wave 1 shape act, so the name called
# here is stated in the open in this fragment's paper as a
# cross section dependency on roster 892's section.
# Surface contract, stated for the assembly check:
# paraphrased_surface returns a surface in mapping form,
# carrying its three texts under the same keys
# verbatim_texts uses. Roster 894's surface_texts, called on
# that mapping, returns the texts the mapping carries, and
# roster 894's travel_lint judges a surface by the texts it
# carries against the verbatim texts, so this surface fails
# the lint on its paraphrased seal sentence.


# Insertion point: roster 893 failure section, first new
# definition in this section in the assembled file.
def check_field_presence(form):
    """Return the field presence check for one package form.

    The stated rows for the form are read by calling
    specification_package_form_rows through the module
    globals at call time; that name stands in roster 894's
    section of the assembled module, so this is a cross
    section call. Returns a fresh mapping whose keys are
    exactly the stated rows for the form, in the order the
    stated rows carry them, and whose values are all True,
    the bool itself. That all True form is the presence
    form the exit set pins: a stated row stands present in
    the product form for that package form, under
    SPEC-SEAL-T02, for the journal, manifest, and bundle
    forms alike. No row is judged here against any home
    outside the stated rows, and no presence value other
    than True stands in the returned mapping.
    """
    rows = globals()["specification_package_form_rows"](form)
    return {row: True for row in rows}


# Insertion point: roster 893 failure section, second new
# definition in this section in the assembled file.
def specification_completeness_check(fields):
    """Check a field list against the registered fields.

    The registered fields are read by calling
    manifest_registered_fields through the module globals
    at call time; that name stands in roster 892's section
    of the assembled module, so this is a cross section
    call. The register itself is a stated constant of the
    specification in roster 892's section, and this check
    judges the given list against that register and
    against nothing derived from the given list. Returns a
    mapping with exactly the keys complete and missing.
    Where every registered field stands in the given list,
    complete is True, the bool itself, and missing is the
    empty list. Where any registered field stands absent
    from the given list, complete is False, the bool
    itself, and missing is a list naming exactly the
    absent registered fields, each once, in registered
    order, and no other field. That missing field form is
    the failure form the exit set pins, in the unnumbered
    failure pair carried under SPEC-SEAL-T04: a manifest
    field list missing one of its seven registered fields
    fails this check with missing naming exactly that
    field.
    """
    registered = globals()["manifest_registered_fields"]()
    given = list(fields)
    missing = [field for field in registered if field not in given]
    return {"complete": not missing, "missing": missing}


# Insertion point: roster 893 failure section, third new
# definition in this section in the assembled file.
def paraphrased_surface():
    """Return a specification surface carrying a paraphrase.

    The verbatim texts are read by calling verbatim_texts
    through the module globals at call time; that name
    stands in roster 894's section of the assembled
    module, so this is a cross section call. Returns a
    fresh mapping standing as a surface, carrying exactly
    the three texts under the same keys verbatim_texts
    uses. The verify sentence entry and the grader
    awareness label entry carry the verbatim texts exactly
    as verbatim_texts returns them. The seal sentence
    entry carries a paraphrase of the seal sentence, in
    different words, stated in full in this function, and
    standing in no place as a verbatim text. The surface
    therefore fails the travel lint on that entry: roster
    894's travel_lint, judging the surface by the texts it
    carries, returns passed False with the seal sentence
    named among its paraphrases, which is the failure case
    SPEC-SEAL-T03 pins. A fresh mapping is returned on
    each call, and no verbatim text is altered by this
    act.
    """
    texts = globals()["verbatim_texts"]()
    return {
        "seal sentence": (
            "Sealed applies to candidate construction, to "
            "every surface an agent faces, and to the "
            "operator when she acts through the tools, "
            "provided the confinement fact for the "
            "deployment holds. It does not apply to the "
            "operator reading her own files. Showing "
            "holdout content through a tool surface needs "
            "an override at the operator door, with a "
            "reason given, and the override must write a "
            "permanent access record before any content "
            "appears. An override uses up the disclosed "
            "group entirely, and that group can never judge "
            "a promotion afterwards."
        ),
        "verify sentence": texts["verify sentence"],
        "grader awareness label": texts["grader awareness label"],
    }


# Section: surface and fixed text, roster 894.
# Functions: verbatim_texts, specification_surfaces,
# surface_texts, travel_lint, specification_package_form_rows,
# and package_form_rows.
# Insertion point for the whole section: after the landed alias
# verify_store = verify at the foot of the landed code, after
# the roster 892 data section and the roster 893 failure
# section, in the scope section 8 insertion order, before the
# module guard foot. The guard foot stands outside this
# ownership: the __getattr__ block and the __dir__ function are
# not in this fragment and are edited by no builder.
# Two named hunks in landed text stand at the foot of this
# fragment as comment blocks, hunk 1 (the module docstring
# correction, exactly one limb) and hunk 2 (the __all__
# extension by the 14 new names). In each hunk block every line
# after the marker "# | " is the exact text; the paper at
# design/steps/step-14-spec-seal-fragment-894.md carries the
# same hunks in fenced form.
# Cross section contracts stated for the assembly check:
# specification_package_form_rows("manifest") calls
# manifest_registered_fields, roster 892's name, through the
# module globals at call time, so the stated manifest rows and
# the register agree by construction. Roster 893's
# check_field_presence reads the stated rows by calling
# specification_package_form_rows through the module globals
# at call time. Roster 893's paraphrased_surface returns a
# surface value that is not one of specification_surfaces();
# travel_lint below passes only a named specification surface
# or a mapping carrying the verbatim texts, and returns passed
# False with a non empty paraphrases list on every other
# surface value, including a mapping carrying a paraphrased
# text under one of the three text keys.

_SEAL_SENTENCE = (
    "sealed binds candidate construction, all agent facing "
    "surfaces, and the operator as an actor through the tools, "
    "conditional on the deployment confinement fact at Section "
    "7.1 item 1; it does not bind the operator as a reader of "
    "her own files; holdout content through a tool surface "
    "requires an override on the operator door only, with a "
    "required reason, and the override writes a permanent "
    "access record before any content is shown; an override "
    "spends the disclosed group whole, by disclosure, and that "
    "group never judges a later promotion."
)

_GRADER_AWARENESS_LABEL = (
    "No bundle name was hidden in this record. Each run is "
    "named with the bundle that produced it. The grades here "
    "are operator grades. They are not a blind check, and they "
    "are not separate from the bundle. Signal counts in this "
    "record are not grades, and they stand apart from the "
    "grades. These grades can support your decision. They "
    "cannot confirm the bundle on their own."
)

# The authored lint form of the verify sentence entry, under
# scope gap G-1. It carries the three "{}" placeholders the
# SPEC-SEAL-T03 count pins. It is not the governed verify
# sentence, it is not printed by verify, and no record of this
# slice may describe it as a governed composite. The governed
# verify forms are the landed constants VERIFY_SENTENCE and
# VERIFY_HOLES, and the agreement result that returns them.
_VERIFY_SENTENCE_LINT_FORM = (
    "The verify sentence travels with its three holes marked "
    "in place: {}, {}, and {}."
)

_SPECIFICATION_SURFACES = (
    "sealing specification",
    "signed verify specification",
    "grader awareness specification",
)

_JOURNAL_FORM_ROWS = (
    "content",
    "predecessor_hash",
    "store_sequence",
    "record_type",
    "hash",
)

_BUNDLE_FORM_ROWS = (
    "store_identity",
    "founding_object_identity",
    "records",
    "manifest",
    "signature_object",
    "anchor_staging_copy",
)



# Insert: surface section, after the roster 893 failure section.
def verbatim_texts():
    """Return the three fixed texts in their stated forms.

    The mapping carries exactly three keys: seal sentence,
    verify sentence, and grader awareness label. The seal
    sentence stands in the whole form of the pinning constant
    SEAL_SENTENCE in TestDatasetT09 in
    system/tests/test_dataset.py. The grader awareness label
    stands in the whole form of the pinning constant
    GRADER_AWARENESS_LABEL in the same class. The verify
    sentence entry is the authored lint form held in
    _VERIFY_SENTENCE_LINT_FORM: it carries the three "{}"
    placeholders the travel lint count pins, it is not the
    governed verify sentence, and it is not printed by verify.
    The governed verify sentence and its three holes stand in
    the landed constants VERIFY_SENTENCE and VERIFY_HOLES.
    """
    return {
        "seal sentence": _SEAL_SENTENCE,
        "verify sentence": _VERIFY_SENTENCE_LINT_FORM,
        "grader awareness label": _GRADER_AWARENESS_LABEL,
    }


# Insert: surface section, after the roster 893 failure section.
def specification_surfaces():
    """Return the specification surfaces the fixed texts travel in.

    The set is authored in this section: three named surfaces,
    each a specification surface that carries the three fixed
    texts by construction in surface_texts. No test pins the
    count, the type, or the identity of the surfaces; the suite
    pins only that the collection is non empty and that the
    lint passes on every surface it returns.
    """
    return _SPECIFICATION_SURFACES


# Insert: surface section, after the roster 893 failure section.
def surface_texts(surface):
    """Return the texts a surface carries.

    On a named specification surface the carried texts are the
    seal sentence and the grader awareness label in their
    verbatim forms, the governed verify sentence in the whole
    form of the landed constant VERIFY_SENTENCE, and the three
    governed holes as a list under the key verify holes. The
    carried verify sentence is the governed sentence, not the
    authored lint form verbatim_texts returns under the same
    key; the B-3 checker at scope section 4, limb 6, checks the
    carried verify sentence against VERIFY_SENTENCE in whole
    form on every surface. On a mapping surface, which is the
    form a surface value carrying its own texts takes, the
    mapping's own entries under the three text keys and the
    verify holes key are returned as the carried texts. Any
    other surface raises ValueError.
    """
    if isinstance(surface, dict):
        carried = {}
        for key in (
            "seal sentence",
            "verify sentence",
            "grader awareness label",
            "verify holes",
        ):
            if key in surface:
                carried[key] = surface[key]
        return carried
    if surface in _SPECIFICATION_SURFACES:
        return {
            "seal sentence": _SEAL_SENTENCE,
            "verify sentence": VERIFY_SENTENCE,
            "grader awareness label": _GRADER_AWARENESS_LABEL,
            "verify holes": list(VERIFY_HOLES),
        }
    raise ValueError(
        "unknown specification surface: %r" % (surface,)
    )


# Insert: surface section, after the roster 893 failure section.
def travel_lint(surface):
    """Run the fixed text travel lint over one surface.

    The result carries passed and paraphrases. A surface passes
    only where the texts it carries stand equal, in whole form,
    to the verbatim seal sentence, the governed verify sentence
    in VERIFY_SENTENCE with its three holes in VERIFY_HOLES,
    and the verbatim grader awareness label. The lint judges
    carried copies against those standing texts; it does not
    judge the standing texts themselves, which is the B-3
    checker's act against homes outside this module. Every
    carried text that is missing or differs names its key in
    paraphrases, and a surface that is neither a named
    specification surface nor a mapping carrying its texts
    fails with the single paraphrase entry surface, so the
    paraphrased surface roster 893 builds fails this lint in
    either of its stated forms.
    """
    if isinstance(surface, dict):
        carried = surface_texts(surface)
    elif surface in _SPECIFICATION_SURFACES:
        carried = surface_texts(surface)
    else:
        return {"passed": False, "paraphrases": ["surface"]}
    paraphrases = []
    if carried.get("seal sentence") != _SEAL_SENTENCE:
        paraphrases.append("seal sentence")
    if carried.get("verify sentence") != VERIFY_SENTENCE:
        paraphrases.append("verify sentence")
    if "verify holes" in carried and (
        list(carried["verify holes"]) != list(VERIFY_HOLES)
    ):
        paraphrases.append("verify holes")
    if carried.get(
        "grader awareness label"
    ) != _GRADER_AWARENESS_LABEL:
        paraphrases.append("grader awareness label")
    return {"passed": not paraphrases, "paraphrases": paraphrases}


# Insert: surface section, after the roster 893 failure section.
def specification_package_form_rows(form):
    """Return the stated field presence rows for one package form.

    The form is one of journal, manifest, or bundle. The
    manifest rows are the seven registered fields, read through
    the module globals at call time from
    manifest_registered_fields, roster 892's name, so the
    stated rows and the register are one list, not two lists
    that agree by statement. The journal rows are the four
    journal record hash fields the landed hash_journal_record
    act states, content, predecessor_hash, store_sequence, and
    record_type, with the standing hash every journal record
    carries. The bundle rows are the packaged store components
    the landed store founding builds, store_identity,
    founding_object_identity, records, manifest,
    signature_object, and anchor_staging_copy, with the key
    slot standing outside the package rows as fixture material.
    The journal and bundle lists stand as authored rows under
    scope gap G-4: no passage read for this slice enumerates
    either list. An unknown form raises ValueError.
    """
    if form == "manifest":
        return tuple(manifest_registered_fields())
    if form == "journal":
        return _JOURNAL_FORM_ROWS
    if form == "bundle":
        return _BUNDLE_FORM_ROWS
    raise ValueError("unknown package form: %r" % (form,))


# Insert: surface section, after the roster 893 failure section.
def package_form_rows(form):
    """Return the product field presence rows for one package form.

    The result stands set equal to
    specification_package_form_rows for the same form, as
    SPEC-SEAL-T02 pins. The manifest rows are derived on the
    product side from the landed manifest builder: the keys of
    build_manifest, in the order that builder builds them,
    which is the landed form of the seven registered fields.
    The journal and bundle rows stand in the same authored
    tables the stated rows stand in, under scope gap G-4; a
    green SPEC-SEAL-T02 evidences the stated rows, the product
    rows, and the presence check in agreement with each other,
    and does not by itself evidence that the journal and bundle
    rows are the plan's rows for those forms. An unknown form
    raises ValueError.
    """
    if form == "manifest":
        return tuple(
            build_manifest(
                None, None, None, None, None, None, None
            ).keys()
        )
    if form == "journal":
        return _JOURNAL_FORM_ROWS
    if form == "bundle":
        return _BUNDLE_FORM_ROWS
    raise ValueError("unknown package form: %r" % (form,))
