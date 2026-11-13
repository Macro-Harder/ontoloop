"""Sealing and verify module, tracer slice Commit 1 form.

Owns, in the narrow form the founding to signed verify path needs:
SHA-256 hashing, manifest construction and manifest hashing, the
signature object construction, signing at founding, the anchor
staging object construction, and the verify computation on its
agreement path with the signature check in the form plan
subsection 20.87 point six states.

The fixed verify sentence below stands in subsection 20.87 point
one words verbatim, and the three holes beside it stand in point
two words verbatim. The sentence is returned only on agreement,
and only where the signature check has run and passed.

Entry points this slice assigns to later commits, including the
SPEC-SEAL test surface of this module and the verify
discrimination branches for the manifest lag case, the non final
tear prefix reading, and chain and manifest disagreement, are not
provided in this form. A lookup of a public name this module does
not yet provide raises AssertionError in the NOT BUILT form the
suite harness uses. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
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

JOURNAL_RECORD_KIND = "journal record"
MANIFEST_KIND = "manifest"
SIGNATURE_KIND = "head signature"
ANCHOR_KIND = "head anchor"

__all__ = [
    "VERIFY_SENTENCE",
    "VERIFY_HOLES",
    "SIGNING_KEY_UNAVAILABLE",
    "SIGNATURE_OBJECT_MISSING",
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


def _recomputed_head(records):
    """Recompute the chain, returning its head hash or None.

    A None return means the recomputation did not stand: a record
    hash or a predecessor link disagreed with the standing bytes.
    The classification of that finding is a later commit branch
    and is not produced in this form.
    """
    previous_hash = None
    head = None
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            return None
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
            return None
        if stored_hash is not None and recomputed != stored_hash:
            return None
        if index > 0 and record.get("predecessor_hash") != previous_hash:
            return None
        previous_hash = recomputed
        head = recomputed
    return head


def verify(store):
    """Run verify over a store value, Commit 1 agreement form.

    Existing checks run first: the founding object stands, the
    chain recomputes from the canonical bytes, and the manifest
    agrees with the chain. The signature check then runs only
    where the store stands fully checked and its chain and
    manifest agree, in the form subsection 20.87 point six states:

    a missing signature object returns unverifiable naming the
    case signature object missing; a key that cannot be obtained
    returns unverifiable naming the case signing key unavailable,
    with no chain only agreement in its place; a signature that
    does not verify returns disagreement. On agreement the result
    carries the output, the signed verify sentence in its verbatim
    form, and the three holes beside it, and on no other output
    does any sentence stand in the result.

    The classification branches for a chain or manifest finding
    that is not agreement, including the manifest lag case and the
    chain consistent prefix reading, are Commit 2 branches in this
    module. Where such a finding stands in this form, verify
    raises AssertionError in the NOT BUILT form rather than
    producing a Commit 2 result. A bytes input is the SPEC-SEAL
    example store form, which is not built in this slice, and
    raises the same NOT BUILT form.
    """
    if isinstance(store, (bytes, bytearray, str)):
        raise _not_built()
    records = _records_of(store)
    manifest = _field(store, "manifest")
    if not records or not isinstance(manifest, dict):
        raise _not_built()
    founding = _field(store, "founding_object_identity")
    if founding is None:
        founding = manifest.get("founding_object_identity")
    if founding is None:
        raise _not_built()
    head = _recomputed_head(records)
    if head is None:
        raise _not_built()
    if manifest.get("head_hash") != head:
        raise _not_built()
    if manifest.get("record_count") != len(records):
        raise _not_built()
    last = records[-1]
    if isinstance(last, dict) and "store_sequence" in last:
        if manifest.get("head_store_sequence") != last["store_sequence"]:
            raise _not_built()
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
        return {"output": "disagreement"}
    if not verify_signature(signature_object, key):
        return {"output": "disagreement"}
    return {
        "output": "agreement",
        "sentence": VERIFY_SENTENCE,
        "holes": list(VERIFY_HOLES),
    }


verify_store = verify
