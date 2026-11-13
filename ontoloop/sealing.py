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

Entry points this slice assigns to later commits, including the
SPEC-SEAL test surface of this module, are not provided in this
form. A lookup of a public name this module does not yet provide
raises AssertionError in the NOT BUILT form the suite harness
uses. A lookup of a private or dunder name raises AttributeError
in the ordinary form.
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
    if isinstance(store, (bytes, bytearray, str)):
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
