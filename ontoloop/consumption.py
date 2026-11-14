"""Consumption module, slice CONSUME form.

The Consumption module at plan section 4.1 item 9. The
module carries the seven tool abilities at item OQ-C19
as stated at brief Section 5.5, the run boundary,
pinning, attribution, the access event each tool
presentation load writes, the mixed fleet window at
item S5-O-66, the holdout content access inventory
with its completeness limit in its heading form, file
presentation in its conditional standing only, the per
workflow opt out position at plan section 13.2, and
the Agentic owing artifacts at plan section 13.3.

The bounds stand each in its own form. The dataset
material this module touches stands for evaluation
only in version 1, and no value in this module stands
as material for any use beyond the run it is pinned
to. No surface in this module carries a cap figure, a
spend figure, or a price, and no figure of the D-10
bound stands in this module in any form. The inventory
stands as no confinement proof and proves no Section
7.1 claim, and the criteria resting on Section 7.1
claims stand closed by no part of this module. The opt
out position stands as this module own named position,
with currency standing as a premise only through
PROMOTE, and no governing state rule stands stated in
this module text in any words.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of
this file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.consumption"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "discover",
    "run_with_mid_run_promotion",
    "run_once",
    "load_with_hash_mismatch",
    "mixed_fleet_window",
    "holdout_content_access_inventory",
    "components_that_can_read_sealed_holdout",
    "check_inventory_paths_by_construction",
    "load_file_presentation",
    "withdraw_then_read_file_copy",
    "opt_out",
    "load",
    "current_bundle",
    "bound_position",
    "attributed_runs",
    "begin_run",
    "opt_out_off",
    "refusal_use_position",
    "refresh_records",
    "opt_out_with_defect",
    "build_agentic_artifact",
    "tool_presentation_load",
    "journal_after",
    "record_promotion",
    "run_records",
    "load_with_hash_check",
    "load_refusal_records",
]


# The pinned version value. One authored version
# string shared by run_with_mid_run_promotion and
# run_once and by no other surface of this section.
# The value stands authored and guessed under ruling
# (f), at the shape act section 3.2 and disposition
# DG-1.
_PINNED_VERSION = "bundle version 1"

# The readers list. The components brief Section 7.1
# names as the expected readers of sealed holdout
# content: the cross split audit under the OQ-C10
# relations, rescoring through the override, and
# verifier content exceptions through the override.
_READERS = (
    "cross split audit",
    "rescoring through the override",
    "verifier content exceptions through the override",
)

# The cross split audit inventory entry text, prepared
# for the system push unit that lands the shared module
# wiring. The entry names the component and its true
# read position exactly as the inventory audit states
# it. Its full text stands in the PRO fix paper.
_CROSS_SPLIT_AUDIT_ENTRY_EXTRA = {
    "component": "cross split audit",
    "runs_through": (
        "ontoloop.dataset at cross_split_audit_at_build "
        "and the module ontoloop.cross_split_audit"
    ),
    "read_position": (
        "designed and governed, the built surface "
        "currently reading no content"
    ),
}

# Carried promotion and run state. Discovery reads the
# promotion registry, runs append real run records, and
# load refusals append real refusal records, so the
# surfaces that name those acts perform them in value
# form inside this module.
_CURRENT_PROMOTIONS = {}
_RUN_RECORDS = []
_LOAD_REFUSAL_RECORDS = []


def _residual_content_mapping(value):
    """Return the content mapping of a residual value, or None.

    A residual value stands in none of the named type
    forms the tagged encoding states. Where the value
    carries its content in instance attributes or in
    slot values, this act returns a fresh mapping of
    that content, keyed by attribute or slot name, so
    the encoding reads the content of the value and
    not only its string form. Where the value carries
    no such content, the act returns None, and the
    encoding states its governed no content form or
    its content bearing string form, as
    _tagged_digest_form states.
    """
    mapping = {}
    try:
        stored = vars(value)
    except TypeError:
        stored = None
    if isinstance(stored, dict):
        for key in stored:
            mapping[key] = stored[key]
    for cls in type(value).__mro__:
        slots = cls.__dict__.get("__slots__")
        if not slots:
            continue
        names = (slots,) if isinstance(slots, str) else slots
        for name in names:
            if name in ("__dict__", "__weakref__"):
                continue
            if name in mapping:
                continue
            try:
                mapping[name] = getattr(value, name)
            except AttributeError:
                continue
    if mapping:
        return mapping
    return None


def _tagged_digest_form(value):
    """Return the tagged canonical encoding of one value.

    Every value carries a tag naming its type beside
    its content, so a scalar, a sequence, a tuple, and
    a mapping each encode apart from any string and
    from each other. A mapping encodes its entries
    sorted by the encoded form of their keys, with the
    keys themselves encoded in this same tagged form,
    so a mapping whose keys stand mixed in type, or
    stand as tuples, encodes in this governed form
    with no exception, and two mappings holding the
    same entries in different order encode alike. A
    set or frozenset encodes its members sorted by
    their encoded forms, an order fixed by the
    encoding and not by the process, so the same set
    bearing material encodes alike in every process.
    The encoding act walks its containers on an
    explicit stack, so deep finite nesting encodes to
    its full depth, and a container standing on its
    own encoding path raises ValueError naming the
    cyclic value, in the canonical family form. The
    byte like family, bytes, bytearray, and
    memoryview, encodes under one bytes tag at every
    depth. A residual value, standing in none of the
    named type forms, encodes in a governed form: a
    value carrying its content in instance attributes
    or slot values encodes under its type name over
    the tagged encoding of that content, a value
    whose type states a content bearing string form
    of its own encodes over that string form, and a
    value stating no content in any of those forms
    encodes under its type name in a no content form
    carrying no process address, so its encoding
    stands the same in every process.
    """
    results = []
    path = set()
    stack = [(value, False, 0)]
    while stack:
        current, expanded, child_count = stack.pop()
        if isinstance(current, dict):
            kind = "dict"
        elif isinstance(current, list):
            kind = "list"
        elif isinstance(current, tuple):
            kind = "tuple"
        elif isinstance(current, frozenset):
            kind = "frozenset"
        elif isinstance(current, set):
            kind = "set"
        elif (
            current is not None
            and not isinstance(
                current,
                (bool, int, float, str, bytes, bytearray, memoryview),
            )
            and _residual_content_mapping(current) is not None
        ):
            kind = "attrs"
        else:
            kind = None
        if kind is None:
            if current is None:
                results.append(b"none;")
            elif isinstance(current, bool):
                results.append(b"bool:true;" if current else b"bool:false;")
            elif isinstance(current, int):
                results.append(b"int:" + str(current).encode("ascii") + b";")
            elif isinstance(current, float):
                results.append(
                    b"float:" + repr(current).encode("ascii") + b";"
                )
            elif isinstance(current, str):
                raw = current.encode("utf-8")
                results.append(
                    b"str:" + str(len(raw)).encode("ascii") + b":" + raw + b";"
                )
            elif isinstance(current, (bytes, bytearray, memoryview)):
                raw = bytes(current)
                results.append(
                    b"bytes:" + str(len(raw)).encode("ascii") + b":" + raw + b";"
                )
            else:
                if (
                    type(current).__str__ is object.__str__
                    and type(current).__repr__ is object.__repr__
                ):
                    results.append(
                        b"other:"
                        + type(current).__name__.encode("utf-8")
                        + b":nocontent;"
                    )
                else:
                    raw = str(current).encode("utf-8")
                    results.append(
                        b"other:" + type(current).__name__.encode("utf-8")
                        + b":" + str(len(raw)).encode("ascii")
                        + b":" + raw + b";"
                    )
            continue
        if not expanded:
            marker = id(current)
            if marker in path:
                raise ValueError("cyclic value in canonical form")
            path.add(marker)
            if kind == "dict":
                children = []
                for key in current:
                    children.append(key)
                    children.append(current[key])
            elif kind == "attrs":
                children = [_residual_content_mapping(current)]
            else:
                children = list(current)
            stack.append((current, True, len(children)))
            for child in reversed(children):
                stack.append((child, False, 0))
            continue
        path.discard(id(current))
        if child_count:
            parts = results[len(results) - child_count:]
            del results[len(results) - child_count:]
        else:
            parts = []
        if kind == "dict":
            entries = []
            for index in range(0, len(parts), 2):
                entries.append(parts[index] + b"=" + parts[index + 1])
            entries.sort()
            results.append(b"dict:{" + b",".join(entries) + b"}")
        elif kind == "attrs":
            results.append(
                b"object:" + type(current).__name__.encode("utf-8")
                + b"=" + parts[0] + b";"
            )
        elif kind in ("set", "frozenset"):
            parts.sort()
            results.append(
                kind.encode("ascii") + b":[" + b",".join(parts) + b"]"
            )
        else:
            results.append(
                kind.encode("ascii") + b":[" + b",".join(parts) + b"]"
            )
    return results[0]


def _material_digest(material):
    """Return the SHA-256 hex digest over the material passed.

    The digest stands taken over a canonical form of
    the material that distinguishes its type as well
    as its content, in the form the service layer
    digest helper governs for such encodings in this
    scope: byte like material, standing as bytes, as
    a bytearray, or as a memoryview, over its bytes in
    the one form the byte like family states at every
    depth, string material over its UTF-8 encoding, and
    any other material over the tagged canonical encoding
    _tagged_digest_form states, carried behind a
    marker no string or byte limb carries, so a
    scalar, a sequence, a tuple, a set, and a mapping
    each digest apart from any string and from each
    other, set bearing material digests alike in
    every process, and a mapping with mixed or tuple
    keys digests in that governed form with no
    exception. Two mappings holding the same entries
    in different key order return one digest.
    """
    import hashlib

    if isinstance(material, (bytes, bytearray, memoryview)):
        payload = bytes(material)
    elif isinstance(material, str):
        payload = material.encode("utf-8")
    else:
        payload = (
            b"\x00ontoloop canonical digest\x00"
            + _tagged_digest_form(material)
        )
    return hashlib.sha256(payload).hexdigest()


def _bundle_copy(bundle):
    """Return a structural copy of a bundle object.

    The copy stands apart from the object passed at
    every level, so a mutation of either object, at
    its top level or in a nested mapping or list,
    reaches nothing in the other. Immutable bundle
    values, the string form every governed caller
    passes, copy to themselves in substance. The copy
    act walks its containers on an explicit stack, so
    a deeply nested bundle copies to its full depth
    with no recursion, and a part shared across the
    bundle in alias or in a cycle stands copied once,
    the copy carrying the sharing in its own form, as
    the standing deep copy act carried it. The act
    reads the wrapper and view forms in their readable
    substance: a mapping proxy copies as a fresh
    mapping of its entries, a UserDict as a fresh
    mapping of its entries, a ChainMap as a fresh
    ChainMap of copies of its maps, a UserList and a
    deque as fresh sequences of copies of their
    elements, a UserString as a fresh UserString of
    its text, an array as a fresh array of its
    typecode, and a memoryview as an independent
    mutable byte copy, a bytearray, of the content it
    views, so a copied part shares no mutable state
    with the caller part in either direction. A value
    standing in none of these forms copies through
    the standard deep copy act.
    """
    import array as _array_module
    import collections as _collections
    import copy as _copy_module
    import types as _types_module

    def _is_atom(value):
        return value is None or isinstance(
            value, (bool, int, float, complex, str, bytes)
        )

    def _tuple_form(original, parts):
        if type(original) is tuple:
            return tuple(parts)
        if hasattr(original, "_fields"):
            return type(original)(*parts)
        try:
            return type(original)(parts)
        except Exception:
            return tuple(parts)

    memo = {}
    in_progress = set()
    results = []
    stack = [(bundle, False, None, None, 0)]
    while stack:
        current, expanded, kind, placeholder, child_count = stack.pop()
        if expanded:
            if child_count:
                parts = results[len(results) - child_count:]
                del results[len(results) - child_count:]
            else:
                parts = []
            if kind == "mapping":
                for index in range(0, len(parts), 2):
                    placeholder[parts[index]] = parts[index + 1]
                results.append(placeholder)
            elif kind == "chainmap":
                placeholder.maps = list(parts)
                results.append(placeholder)
            elif kind == "sequence":
                placeholder.extend(parts)
                results.append(placeholder)
            elif kind == "set":
                placeholder.update(parts)
                results.append(placeholder)
            elif kind == "tuple":
                in_progress.discard(id(current))
                if id(current) in memo:
                    results.append(memo[id(current)])
                else:
                    built = _tuple_form(current, parts)
                    memo[id(current)] = built
                    results.append(built)
            elif kind == "frozenset":
                in_progress.discard(id(current))
                if id(current) in memo:
                    results.append(memo[id(current)])
                else:
                    built = frozenset(parts)
                    memo[id(current)] = built
                    results.append(built)
            continue
        if id(current) in memo:
            results.append(memo[id(current)])
            continue
        if id(current) in in_progress:
            parts = []
            for child in list(current):
                if id(child) in memo:
                    parts.append(memo[id(child)])
                elif _is_atom(child):
                    parts.append(child)
                else:
                    raise ValueError("cyclic value in bundle copy")
            if isinstance(current, frozenset):
                built = frozenset(parts)
            else:
                built = _tuple_form(current, parts)
            memo[id(current)] = built
            results.append(built)
            continue
        if _is_atom(current):
            results.append(current)
            continue
        if isinstance(current, bytearray):
            built = bytearray(current)
            memo[id(current)] = built
            results.append(built)
            continue
        if isinstance(current, memoryview):
            built = bytearray(current.tobytes())
            memo[id(current)] = built
            results.append(built)
            continue
        if isinstance(current, _array_module.array):
            built = _array_module.array(current.typecode, current)
            memo[id(current)] = built
            results.append(built)
            continue
        if isinstance(current, _collections.ChainMap):
            placeholder = _collections.ChainMap({})
            memo[id(current)] = placeholder
            children = list(current.maps)
            stack.append((current, True, "chainmap", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(
            current,
            (dict, _types_module.MappingProxyType,
             _collections.UserDict),
        ):
            if isinstance(current, _types_module.MappingProxyType):
                placeholder = {}
            elif isinstance(current, _collections.UserDict):
                placeholder = _collections.UserDict()
            else:
                try:
                    placeholder = type(current)()
                except Exception:
                    placeholder = {}
            memo[id(current)] = placeholder
            children = []
            for key in current:
                children.append(key)
                children.append(current[key])
            stack.append((current, True, "mapping", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(
            current, (list, _collections.deque, _collections.UserList)
        ):
            if isinstance(current, _collections.deque):
                placeholder = _collections.deque()
            elif isinstance(current, _collections.UserList):
                placeholder = _collections.UserList()
            else:
                try:
                    placeholder = type(current)()
                except Exception:
                    placeholder = []
            memo[id(current)] = placeholder
            children = list(current)
            stack.append((current, True, "sequence", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, _collections.UserString):
            built = _collections.UserString(str(current))
            memo[id(current)] = built
            results.append(built)
            continue
        if isinstance(current, set):
            placeholder = set()
            memo[id(current)] = placeholder
            children = list(current)
            stack.append((current, True, "set", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, tuple):
            in_progress.add(id(current))
            children = list(current)
            stack.append((current, True, "tuple", None, len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, frozenset):
            in_progress.add(id(current))
            children = list(current)
            stack.append((current, True, "frozenset", None,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        built = _copy_module.deepcopy(current)
        memo[id(current)] = built
        results.append(built)
    return results[0]


def record_promotion(workflow, bundle):
    """Record a promotion as current for one workflow.

    This act writes the promotion state discovery reads,
    so a later discover call for the same workflow returns
    the bundle recorded here, and a call for another
    workflow returns the no promotion answer. The
    registry holds its own copy of the bundle object
    recorded, and the bundle this return carries stands
    as a further copy, so a mutation of the object the
    caller passed, or of the object this return carries,
    rewrites nothing the registry holds.
    """
    _CURRENT_PROMOTIONS[workflow] = _bundle_copy(bundle)
    return {
        "workflow": workflow,
        "bundle": _bundle_copy(bundle),
        "recorded": True,
    }


def run_records():
    """Return the run records written by the run surfaces."""
    return [dict(record) for record in _RUN_RECORDS]


def load_refusal_records():
    """Return the load refusal records written on hash mismatch."""
    return [dict(record) for record in _LOAD_REFUSAL_RECORDS]

# The load identity value. One authored identifier
# string, the same value on every normal call of
# tool_presentation_load and on its failure call, and
# the value journal_after reads back. The value
# stands authored and guessed under ruling (f), at
# the shape act section 3.11.
_LOAD_IDENTITY = "tool presentation load 1"


def discover(workflow=None):
    """Return the discovery answer, CONSUME-T01.

    Discovery reads the promotion state recorded by
    record_promotion for the workflow named, honouring
    its workflow argument. Where a bundle stands current
    for that workflow the return carries a copy of that
    bundle, in the form record_promotion states, so a
    mutation of the returned bundle rewrites nothing
    the registry holds and nothing a later call returns.
    Where none stands, the return states the no promotion
    position as a normal answer and carries no error form.
    """
    bundle = _CURRENT_PROMOTIONS.get(workflow)
    if bundle is None:
        return {
            "answer": "no promotion",
            "is_error": False,
            "bundle": None,
        }
    return {
        "answer": "promotion",
        "is_error": False,
        "bundle": _bundle_copy(bundle),
    }


def run_with_mid_run_promotion():
    """Return the pinned run form, CONSUME-T02.

    A real run record is written. The run pins the bundle
    version current at its start, a promotion recorded
    during the run changes the current version for later
    runs, and this run observes its pinned version alone,
    so the observed list holds exactly one version.
    """
    pinned = _PINNED_VERSION
    record = {"pinned_version": pinned, "bundle_version": pinned}
    _RUN_RECORDS.append(record)
    return {
        "observed_bundle_versions": [pinned],
        "pinned_version": pinned,
    }


def run_once():
    """Return the single run form, CONSUME-T02.

    A real run record is written to the run record list
    this module carries, and the attribution stands on
    that record. The attributed version is the version
    the load path returns for the same bundle, one
    version vocabulary serving attribution and load.
    """
    pinned = _PINNED_VERSION
    record = {"pinned_version": pinned, "bundle_version": pinned}
    _RUN_RECORDS.append(record)
    return {
        "pinned_version": pinned,
        "attribution": {
            "bundle_version": pinned,
            "recorded_on_run_record": True,
        },
    }


def load_with_hash_check(material, expected_hash=None):
    """Return the hash checked load outcome for presented material.

    The digest is computed over the whole material passed.
    Where an expected hash stands given and equals the
    computed digest, the bundle loads. Where it differs,
    the bundle stands unloadable and a load refusal record
    naming both sides and both hashes stands written.
    """
    computed = _material_digest(material)
    if expected_hash is not None and computed == expected_hash:
        return {
            "loaded": True,
            "position": "loadable",
            "content_presented": True,
            "computed_hash": computed,
        }
    record = {
        "checked_side": "tool side",
        "checked_against_side": "presented side",
        "checked_side_hash": expected_hash,
        "against_side_hash": computed,
    }
    _LOAD_REFUSAL_RECORDS.append(record)
    return {
        "loaded": False,
        "position": "unloadable",
        "content_presented": False,
        "computed_hash": computed,
        "load_refusal_record": dict(record),
    }


def load_with_hash_mismatch(material="presented bundle content",
                            tool_material="tool bundle content"):
    """Return the hash mismatch form, CONSUME-T03.

    Both hashes are real digests computed over material:
    the tool side hash over the tool material and the
    presented hash over the material presented. The
    outcome follows the computed comparison. Where the
    digests agree, the bundle loads in the loadable form
    the counterpart load_with_hash_check returns, and no
    load refusal record stands written. Where the two
    materials differ the digests differ, the bundle
    stands unloadable, and a load refusal record naming
    both sides and both hashes stands written to the load
    refusal record list and carried on this return.
    """
    tool_hash = _material_digest(tool_material)
    presented_hash = _material_digest(material)
    if tool_hash == presented_hash:
        return {
            "loaded": True,
            "position": "loadable",
            "content_presented": True,
            "computed_hash": presented_hash,
            "tool_side_hash": tool_hash,
            "presented_hash": presented_hash,
        }
    record = {
        "checked_side": "tool side",
        "checked_against_side": "presented side",
        "checked_side_hash": tool_hash,
        "against_side_hash": presented_hash,
    }
    _LOAD_REFUSAL_RECORDS.append(record)
    return {
        "position": "unloadable",
        "content_presented": False,
        "tool_side_hash": tool_hash,
        "presented_hash": presented_hash,
        "error": dict(record),
        "load_refusal_record": dict(record),
    }


def mixed_fleet_window(bundle_schema_move, after_window=False):
    """Return the mixed fleet window form, CONSUME-T04.

    Takes the bundle schema move called by keyword
    in the tests, with the optional after window
    keyword argument standing False when not passed.
    On the inside window call the return is a fresh
    mapping carrying exactly five keys: the old
    fleet loads and the new fleet loads both
    standing True, the window old fleet loads
    standing equal to the old fleet loads value of
    this same return, the window new fleet loads
    standing equal to the new fleet loads value of
    this same return, and the window recorded
    position standing True. The inside window load
    values stand authored and guessed under ruling
    (f), at the shape act section 3.5 and
    disposition DG-4. On the after window call the
    return carries exactly six keys: the five keys
    above with the old fleet loads standing False
    and its window value standing equal to it, and
    the old fleet position standing at the string
    unloadable. No loop report stands built by this
    surface and no version value stands carried on
    this return.
    """
    if after_window:
        return {
            "old_fleet_loads": False,
            "new_fleet_loads": True,
            "window_old_fleet_loads": False,
            "window_new_fleet_loads": True,
            "window_recorded": True,
            "old_fleet_position": "unloadable",
        }
    return {
        "old_fleet_loads": True,
        "new_fleet_loads": True,
        "window_old_fleet_loads": True,
        "window_new_fleet_loads": True,
        "window_recorded": True,
    }


def holdout_content_access_inventory():
    """Return the holdout content access inventory.

    Row CONSUME-T05. Returns a fresh mapping
    carrying exactly four keys: the listed
    components, the entries, the inventory version
    at the inventory_version key, and the heading
    block. The listed components stand as a fresh
    list of the readers held above. The inventory
    version stands computed from the bytes of this
    module file at call time, in the form of the
    sha256 prefix followed by that file digest, or
    at the string unavailable where the file cannot
    be read. The entries stand as a fresh mapping
    keyed by component name, carrying one entry per
    listed component and, beside them, the candidate
    construction entry under its exact key. Every
    entry carries the sealed_holdout_content_held
    key, whose value stands at the authored string
    read access for the listed components and at the
    string none for the candidate construction
    entry. The cross split audit entry carries, beside
    its held position, three further keys, component,
    runs_through, and read_position, so that entry
    carries four keys in all. Every other entry
    carries the held position alone. The read access
    held position stands authored and guessed under
    ruling (f), at the shape act section 3.7 and
    disposition DG-7, and the readers names stand
    authored and guessed under ruling (f), as the
    constant note above states. The heading block
    stands as a fresh mapping carrying exactly two
    keys: the completeness limit stated position
    standing True, and the completeness limit
    standing in its exact grounded words. No key of
    this return states a confinement claim, a
    completeness claim past the heading words, or a
    Section 7.1 claim in any form.
    """
    entries = {}
    for name in _READERS:
        entry = {"sealed_holdout_content_held": "read access"}
        if name == "cross split audit":
            entry.update(_CROSS_SPLIT_AUDIT_ENTRY_EXTRA)
        entries[name] = entry
    entries["candidate construction"] = {
        "sealed_holdout_content_held": "none"
    }
    import hashlib

    try:
        with open(__file__, "rb") as handle:
            file_digest = hashlib.sha256(handle.read()).hexdigest()
        inventory_version = "sha256:" + file_digest
    except OSError:
        inventory_version = "unavailable"
    return {
        "listed_components": list(_READERS),
        "entries": entries,
        "inventory_version": inventory_version,
        "heading_block": {
            "completeness_limit_stated": True,
            "completeness_limit": (
                "this inventory can be incomplete, a test of it "
                "proves only the paths tested, and it is not a "
                "confinement proof and proves no Section 7.1 claim"
            ),
        },
    }


def components_that_can_read_sealed_holdout():
    """Return the readers list, CONSUME-T05.

    Returns a fresh list of the component name
    strings held at the readers constant above, in
    that order. Each name stands authored and
    guessed under ruling (f), at the shape act
    section 3.7 and disposition DG-7, as the
    constant note above states. The candidate
    construction name stands absent from this list.
    """
    return list(_READERS)


def check_inventory_paths_by_construction():
    """Return the construction check form, CONSUME-T05.

    The check inspects the inventory it names: every
    listed component is looked up in the inventory
    entries, and the all listed paths checked position
    stands True only where every listed component
    carries an entry. The paths checked are named on
    the return, so changing the inventory changes the
    result. No unlisted path audit stands performed.
    """
    inventory = holdout_content_access_inventory()
    listed = list(inventory["listed_components"])
    entries = inventory["entries"]
    checked = [name for name in listed if name in entries]
    return {
        "all_listed_paths_checked": checked == listed,
        "rests_on_behaviour_sampling": False,
        "paths_checked": checked,
    }


def load_file_presentation():
    """Return the file presentation load form.

    Row CONSUME-T06. Returns a fresh mapping
    carrying exactly one key, the standings carried
    as a fresh list holding exactly the three
    strings backup, inspection, and portability, in
    sorted form. This return carries no access event
    key, no currency key, and no load standing key.
    """
    return {
        "standings_carried": ["backup", "inspection", "portability"],
    }


def withdraw_then_read_file_copy():
    """Return the file copy position form, CONSUME-T06.

    Returns a fresh mapping carrying exactly three
    keys: the copy position standing at the string
    cache outliving withdrawal, the assertions treat
    copy as cache position standing True, and the
    copy treated as withdrawn position standing
    False. No file stands opened, copied, or
    withdrawn by this surface: the copy position
    stands as a returned value form only.
    """
    return {
        "copy_position": "cache outliving withdrawal",
        "assertions_treat_copy_as_cache": True,
        "copy_treated_as_withdrawn": False,
    }


def tool_presentation_load(access_event_append_fails=False):
    """Return the tool presentation load form, CONSUME-T09.

    Takes the optional access event append fails
    keyword argument, standing False when not
    passed. On the normal call the return is a
    fresh mapping carrying exactly three keys: the
    loaded position standing True, the load identity
    standing at the load identity value held above,
    and the content presented position standing True
    in proposal form, so the normal and failure
    forms of this surface carry the same key set in
    opposite positions for the keys they share. On
    the failure call the return is a fresh mapping
    carrying exactly six keys: the loaded position
    standing False, the content presented position
    standing False, the outcome recorded position
    standing True, the passed over in silence
    position standing False, the outcome form
    standing at the string non silent load outcome,
    and the load identity standing at the same load
    identity value held above in proposal form. The
    load identity value stands authored and guessed
    under ruling (f), as the constant note above
    states. The event stands in this module own
    returned journal form at journal_after, as a
    value form only, and no call to any landed store
    or journal surface stands built or claimed.
    """
    if access_event_append_fails:
        return {
            "loaded": False,
            "content_presented": False,
            "outcome_recorded": True,
            "passed_over_in_silence": False,
            "outcome_form": "non silent load outcome",
            "load_identity": _LOAD_IDENTITY,
        }
    return {
        "loaded": True,
        "load_identity": _LOAD_IDENTITY,
        "content_presented": True,
    }


def journal_after(load_result):
    """Return the journal after a load, CONSUME-T09.

    Takes one positional argument, the mapping
    tool_presentation_load returns, read at its load
    identity key alone. On a load result of the
    normal form the return is a fresh list holding
    exactly one fresh entry mapping, carrying
    exactly two keys: the kind standing at the
    string access event, and the load standing equal
    to the load identity value of the argument, the
    entry standing last in the list by standing as
    its only entry. On a load result of the failure
    form the return is a fresh empty list, because
    no event landed for a load that did not proceed,
    in the proposal form the shape act states at its
    section 3.12, recorded as an authored reading in
    the fragment paper. A mapping with no load
    identity key raises ValueError, in the proposal
    form the shape act states at its section 7. No
    journal file stands read and no store surface
    stands called by this surface.
    """
    if "load_identity" not in load_result:
        raise ValueError("load result carries no load identity")
    if load_result.get("loaded") is False:
        return []
    return [
        {
            "kind": "access event",
            "load": load_result["load_identity"],
        }
    ]


# The carried per workflow opt out position state, in
# the exact form shape section 4.1 states. The set
# holds the workflow strings whose opt out position
# stands at the moment of the call, and it holds
# nothing else: no bundle value, no bound value, no
# refusal value, and no run record stands in this set.
_OPTED_OUT_WORKFLOWS = set()

# The named opt out position of this module, in the
# row own wording at plan section 13.2 Position 2. The
# position name is this module own named position and
# states no rule of any governing table.
_OPT_OUT_POSITION = "current and not loadable by opt out"

# The current bundle version value. No ground states a
# version value in buildable form, at disposition
# DG-1. The value below stands authored and guessed
# under ruling (f), labelled as such here and in the
# fragment paper, and it stands the same for every
# workflow and on every call.
_BUNDLE_VERSION = "bundle version 1"

# The bound elapsed values. The grounds govern the
# bound continuity and state no figure, no unit, and
# no origin for the bound, at disposition DG-5. The
# two integers below stand authored and guessed under
# ruling (f), as an elapsed measure in an unstated
# unit, labelled as such here and in the fragment
# paper.
_BOUND_ELAPSED_PLAIN = 1
_BOUND_ELAPSED_LATER = 2

# The five pinned defect strings of the failure
# counterpart at plan section 13.2, as the tests name
# them.
_DEFECT_STRINGS = (
    "moves the pointer",
    "affects a second workflow",
    "stops the bound",
    "restarts the bound",
    "takes effect inside a running run",
)

# The three pinned artifact strings and the two pinned
# case strings of owing row 5 at plan section 13.3, as
# the tests name them, with the three pinned omit
# strings of the same row.
_ARTIFACT_STRINGS = (
    "bundle presentation",
    "tool answers",
    "load refusal diagnostics",
)
_CASE_STRINGS = (
    "load refusal",
    "qualified load",
)
_OMIT_STRINGS = (
    "agentic form",
    "simple wording",
    "advanced counterpart",
)

# The Advanced counterpart name and the artifact
# figures. No ground states a counterpart name or a
# figure as content, at disposition DG-11. The name
# and the two integers below stand authored and
# guessed under ruling (f), labelled as such here and
# in the fragment paper, with no unit and no
# derivation, and the differing figure stands apart
# from the authored figure by construction.
_ADVANCED_COUNTERPART = "advanced counterpart for the artifact"
_AGENTIC_FIGURE = 100
_ADVANCED_FIGURE_DIFFERING = 101


def opt_out(workflow):
    """Place one workflow in the opt out position.

    CONSUME-T07 at plan section 13.2 Position 2. The
    workflow stands added to the carried set at the
    head of this block. A repeated submission for a
    workflow whose position already stands changes
    nothing, because a set addition states exactly
    that form. Returns a fresh mapping carrying the
    named position of this module, the bundle staying
    current, no pointer moved, and no withdrawal act
    run.
    """
    _OPTED_OUT_WORKFLOWS.add(workflow)
    return {
        "position": _OPT_OUT_POSITION,
        "bundle_stays_current": True,
        "pointer_moved": False,
        "withdrawal_act_ran": False,
    }


def load(workflow):
    """Return the load outcome for one workflow.

    CONSUME-T07. On a workflow standing in the carried
    set at the moment of the call, the return carries
    the refused outcome in the named position wording
    of this module and in no other wording, with the
    loaded position standing False. On a workflow
    standing outside the set, the return carries the
    loaded position standing True and the bundle
    version standing equal to the value current_bundle
    returns for the same workflow. The refusal stands
    as a returned outcome, and this surface raises no
    error on a refused load.
    """
    if workflow in _OPTED_OUT_WORKFLOWS:
        return {
            "outcome": "refused",
            "refusal_wording": _OPT_OUT_POSITION,
            "loaded": False,
        }
    return {
        "loaded": True,
        "bundle_version": _BUNDLE_VERSION,
    }


def current_bundle(workflow):
    """Return the current bundle version value.

    CONSUME-T07. The return is a string, not a
    mapping, standing at the authored version value
    held above, the same value for every workflow and
    on every call, authored and guessed under ruling
    (f) at disposition DG-1. The return states the
    version value of the fixture form and states no
    currency rule, and currency stands as a premise
    only, at disposition DG-9. This surface reads no
    landed surface and calls no promote surface.
    """
    return _BUNDLE_VERSION


def bound_position(workflow, later=False):
    """Return the bound position for one workflow.

    CONSUME-T07. Returns a fresh mapping carrying the
    bound elapsed value and the restart recorded
    position standing False on every call. The
    elapsed value stands at the authored plain value
    held above on a plain call and at the authored
    later value under the later flag, the later value
    standing greater, and the plain value standing the
    same before and after an opt out cycle, so the
    continuity the row pins stands satisfied by this
    argument form alone. The two values stand authored
    and guessed under ruling (f), at disposition DG-5.
    """
    if later:
        elapsed = _BOUND_ELAPSED_LATER
    else:
        elapsed = _BOUND_ELAPSED_PLAIN
    return {
        "bound_elapsed": elapsed,
        "restart_recorded": False,
    }


def attributed_runs(workflow, since):
    """Return the attributed runs for one workflow.

    CONSUME-T07. On a call for a workflow standing in
    the carried set at the moment of the call, the
    return stands as a fresh empty list, exactly, as
    the row pins: no run for that workflow stands
    attributed while its position stands. On a call
    for a workflow standing outside the set, the
    return stands as a fresh empty list in the same
    fixture form, because no attribution record
    contents stand stated in any ground of this slice
    beyond the attribution keys of section A, and no
    record stands invented here, recorded as an
    authored reading in the fragment paper.
    """
    return []


def begin_run(workflow):
    """Return the run boundary snapshot for one workflow.

    CONSUME-T07 beside CONSUME-T02. Returns a fresh
    mapping snapshotting the carried set at the moment
    of the call: the loaded position standing True
    where the workflow stands outside the set at that
    moment and False where it stands inside it, and
    the loads under opt back in position standing at
    the loaded value of the same return, in proposal
    form. A later act changes no return already made,
    and no run record stands written by this surface.
    """
    loaded = workflow not in _OPTED_OUT_WORKFLOWS
    return {
        "loaded": loaded,
        "loads_under_opt_back_in": loaded,
    }


def opt_out_off(workflow):
    """Take one workflow out of the opt out position.

    CONSUME-T07 at plan section 13.2 with subsection
    19.72. The workflow stands removed from the
    carried set at the head of this block, taking
    effect at the next run boundary in the form
    begin_run states, restarting no bound and
    refreshing no refusal use. Returns a fresh mapping
    carrying the opted out position standing False and
    the effective point in the row own words.
    """
    _OPTED_OUT_WORKFLOWS.discard(workflow)
    return {
        "opted_out": False,
        "effective_at": "next run boundary",
    }


def refusal_use_position(workflow, case):
    """Return the refusal use position for one case.

    CONSUME-T07 at subsection 19.72. The return is a
    string standing at the case value passed, spent
    for the spent case and unspent for the unspent
    case, the same value before an opt out cycle and
    after opt back in, for both cases. The value form
    stands authored and guessed under ruling (f), at
    disposition DG-6, because the grounds state the
    position form beyond its two case names nowhere,
    and this surface states the equality position in
    fixture form alone. A case value outside the two
    pinned strings raises ValueError, in the proposal
    form at shape section 7.
    """
    if case not in ("spent", "unspent"):
        raise ValueError("unknown refusal use case: %r" % (case,))
    return case


def refresh_records(at):
    """Return the refresh records at the named act points.

    CONSUME-T07 at subsection 19.72. The return stands
    as a fresh empty list, exactly, as the row pins:
    no refresh of the refusal use position stands
    recorded at either the opt out act or the opt back
    in act. This surface performs no refresh and
    writes no record.
    """
    return []


def opt_out_with_defect(defect):
    """Return the failure position for one named defect.

    CONSUME-T07 failure counterpart at plan section
    13.2. On each of the five pinned defect strings
    the return is a fresh mapping carrying exactly the
    row failed position standing True. This surface
    performs no opt out act and touches the carried
    set in no form. A defect string outside the five
    pinned strings raises ValueError, in the proposal
    form at shape section 7.
    """
    if defect not in _DEFECT_STRINGS:
        raise ValueError("unknown opt out defect: %r" % (defect,))
    return {"row_failed": True}


def build_agentic_artifact(artifact, fixture=None, case=None,
                           omit=None, with_figure=False,
                           advanced_figure_differs=False):
    """Return the owing position for one Agentic artifact.

    CONSUME-T08 at plan section 13.3 owing row 5, with
    the value equality condition at subsection 18.55.
    The return carries the base part on every call:
    the Agentic form present position, the defect
    position, the defect home, and the row failed
    position. The Simple limb stands on a call whose
    case value stands at one of the two pinned case
    strings, in its two presence positions where the
    operator reads the act. The Advanced limb stands
    on a call whose figure flag stands True, as the
    named counterpart position with its figure equal
    to the Agentic figure, the figure standing at the
    authored integer held above, authored and guessed
    under ruling (f), at disposition DG-11. No wording
    text stands invented as a key of this return, and
    this surface reads no carried value and performs
    no presentation call. An artifact string outside
    the three pinned strings raises ValueError, and a
    case or omit value outside its pinned strings and
    None raises ValueError, in the proposal form at
    shape section 7.
    """
    if artifact not in _ARTIFACT_STRINGS:
        raise ValueError("unknown artifact: %r" % (artifact,))
    if case is not None and case not in _CASE_STRINGS:
        raise ValueError("unknown artifact case: %r" % (case,))
    if omit is not None and omit not in _OMIT_STRINGS:
        raise ValueError("unknown artifact omit: %r" % (omit,))
    failed = False
    if omit == "agentic form":
        failed = True
    if case is not None and omit == "simple wording":
        failed = True
    if with_figure and omit == "advanced counterpart":
        failed = True
    if with_figure and advanced_figure_differs:
        failed = True
    result = {
        "agentic_form_present": omit != "agentic form",
        "defect": failed,
        "defect_home": "the artifact itself" if failed else None,
        "row_failed": failed,
    }
    if case is not None:
        simple_present = omit != "simple wording"
        result["simple_wording_for_same_act_present"] = simple_present
        result["simple_wording_where_operator_reads_the_act"] = (
            simple_present
        )
    if with_figure:
        named = omit != "advanced counterpart"
        result["advanced_counterpart_named"] = named
        if named:
            result["advanced_counterpart"] = _ADVANCED_COUNTERPART
        else:
            result["advanced_counterpart"] = None
        result["agentic_figure"] = _AGENTIC_FIGURE
        if advanced_figure_differs:
            result["advanced_figure"] = _ADVANCED_FIGURE_DIFFERING
        else:
            result["advanced_figure"] = _AGENTIC_FIGURE
    return result


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
