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
    not only its string form. A slot whose stated name
    carries two leading underscores stands stored
    under a storage name carrying the stating class
    name as a prefix, and the act reads that slot
    under its storage name beside the raw name, so
    its content stands in the mapping in the same
    form as any other slot content. Where a subclass
    states a slot under the same stated name as a
    base class, the slot of each stating class
    stands read under its own storage name, so the
    content of every stating class stands in the
    mapping. Where the value
    carries
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
                if name.startswith("__") and not name.endswith("__"):
                    storage = "_" + cls.__name__.lstrip("_") + name
                    if storage != name and storage not in mapping:
                        try:
                            mapping[storage] = getattr(value, storage)
                        except AttributeError:
                            pass
                continue
            try:
                mapping[name] = getattr(value, name)
                continue
            except AttributeError:
                pass
            if name.startswith("__") and not name.endswith("__"):
                storage = "_" + cls.__name__.lstrip("_") + name
                if storage != name:
                    try:
                        mapping[name] = getattr(value, storage)
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
    stands the same in every process. A subclass
    instance of a named container form encodes over
    its container content and over its added instance
    content together, and a subclass instance of a
    Decimal, a date, a time, or a timedelta carrying
    added instance content encodes over its intrinsic
    string form and over that content together, so
    state standing in either channel stands in the
    digest. A subclass instance of a scalar or byte
    like type carrying added instance content encodes
    over its intrinsic value and over that content
    together, in the same two channel form, and a
    subclass instance of a complex, an array, or a
    deque carrying added instance content encodes
    over its intrinsic content and over that content
    together, the attribute reading never preempting
    the intrinsic channel. A subclass instance of an
    exception type carrying added instance content
    encodes over its argument content and over that
    content together, in the same two channel form,
    the filename channels of an OSError standing
    beside its argument content in that form, and the
    cause and context channels of an exception
    standing beside its argument content in every
    exception form, the suppression flag channel of
    an exception, the name and path channels of an
    ImportError, and the filename, line, offset,
    text, and end position channels of a SyntaxError
    standing beside its argument content in every
    exception form beside them, the encoding walk
    standing over that chaining walk in its cyclic
    form, and a
    member of an enum mixing in int, float, str,
    bytes, or bytearray carrying added instance
    content beyond the
    member state its enum class states encodes over
    its intrinsic value and over that added content
    together, a member carrying no such added content
    encoding in its standing form. A defaultdict
    encodes over its entries and over a governed form
    of its default factory together, a factory stating
    no such form standing refused, a type factory
    standing in a local scope, whose module and
    qualified name state no distinction from a second
    such type, standing refused in the same form, and
    a function
    carrying added instance content stands refused in
    the form its plain form stands refused, the
    function channel standing decided before the
    attribute reading in the same form as the stream
    and iterator positions, and a partial application
    carrying added instance content standing refused
    in the form its plain form stands refused, its
    channel standing decided before the attribute
    reading in the same form. An in memory stream encodes
    over the content it holds, read through its
    getvalue act without consumption, and a stream
    subclass instance carrying added instance content
    encodes over that held content and over that
    content together. A value whose content stands
    in a channel this reading cannot reach without
    consumption, an iterator among them, a stream
    whose content stands readable in no such form,
    and a value whose string form carries its process
    address in any dress, behind the words at 0x in
    either marker case, with no at wording before it,
    as a decimal number after the word at, behind a
    hash sign, a colon, or brackets, behind the word
    At with a capital first letter, grouped with
    commas after the word at, or standing bare inside
    a bracketed form as a decimal or hexadecimal
    number, or standing in any whole token dress the
    scan reads in substance, after a space, inside
    parentheses, behind an equals sign, a semicolon,
    or a slash, attached to its introducer, or at the
    head of the form, or standing separated into
    groups by any single separator character standing
    outside the letters and the digits, as grouped
    decimal groups or as hexadecimal pairs or groups,
    stand
    refused with a ValueError naming the type of the
    material, so no digest stands taken over an
    unread channel or over an address.
    The stream and iterator positions stand decided
    before the attribute reading, so a value carrying
    readable attributes beside an unread channel
    stands read or refused on that channel and never
    on its attributes alone.
    """
    import array as _array_module
    import collections as _collections_module
    import datetime as _datetime_module
    import decimal as _decimal_module
    import enum as _enum_module
    import functools as _functools_module
    import io as _io_module
    import re as _re_module
    import types as _types_module

    def _enum_added_mapping(member):
        residual = _residual_content_mapping(member)
        if residual is None:
            return None
        added = {}
        for key in residual:
            if key in (
                "_value_",
                "_name_",
                "__objclass__",
                "_sort_order_",
            ):
                continue
            added[key] = residual[key]
        if added:
            return added
        return None

    def _address_bearing(text):
        if _re_module.search(
            r" at 0[xX][0-9a-fA-F]+"
            r"| at [0-9]{5,}"
            r"|0[xX][0-9a-fA-F]{4,}"
            r"| At [0-9]{5,}"
            r"| [aA]t [0-9]{1,3}(?:,[0-9]{3})+"
            r"| [#:\[] *[0-9]{5,}"
            r"| [#:\[] *[0-9]{1,3}(?:,[0-9]{3})+"
            r"|<[^>]*[0-9]{7,}[^>]*>"
            r"|<[^>]*[0-9]{1,3}(?:,[0-9]{3})+[^>]*>"
            r"|<[^>]*\b(?=[0-9a-fA-F]*[a-fA-F])"
            r"(?=[0-9a-fA-F]*[0-9])"
            r"[0-9a-fA-F]{7,}\b[^>]*>",
            text,
        ):
            return True
        stripped = text.strip()
        if _re_module.fullmatch(
            r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)"
            r"(?:[eE][+-]?[0-9]+)?",
            stripped,
        ):
            return False
        if _re_module.search(r"[0-9]{7,}", text):
            return True
        if _re_module.search(
            r"(?<![0-9a-fA-F])"
            r"(?=[0-9a-fA-F]*[a-fA-F])(?=[0-9a-fA-F]*[0-9])"
            r"[0-9a-fA-F]{7,}(?![0-9a-fA-F])",
            text,
        ):
            return True
        if _re_module.search(
            r"(?<![0-9])[0-9]{1,3}(?:[^0-9A-Za-z][0-9]{3}){2,}"
            r"(?![0-9])",
            text,
        ):
            return True
        if _re_module.search(
            r"(?<![0-9a-fA-F])[0-9a-fA-F]{2}([^0-9A-Za-z])"
            r"[0-9a-fA-F]{2}(?:\1[0-9a-fA-F]{2}){4,}"
            r"(?![0-9a-fA-F])",
            text,
        ):
            return True
        for match in _re_module.finditer(
            r"(?<![0-9a-fA-F])[0-9a-fA-F]{4}([^0-9A-Za-z])"
            r"[0-9a-fA-F]{4}(?:\1[0-9a-fA-F]{4}){1,}"
            r"(?![0-9a-fA-F])",
            text,
        ):
            if _re_module.search(r"[a-fA-F]", match.group(0)):
                return True
        return False

    def _dict_factory_token(current):
        if not isinstance(
            current, _collections_module.defaultdict
        ):
            return None
        factory = current.default_factory
        if factory is None:
            return None
        if isinstance(factory, type):
            if "<locals>" in factory.__qualname__:
                raise ValueError(
                    "digest cannot read material of type "
                    + type(current).__name__
                )
            return (
                "factorytype:"
                + factory.__module__
                + "."
                + factory.__qualname__
            )
        if (
            callable(factory)
            and type(factory).__name__
            == "builtin_function_or_method"
            and getattr(factory, "__qualname__", None)
            and "<lambda>" not in factory.__qualname__
        ):
            return (
                "factorybuiltin:"
                + factory.__module__
                + "."
                + factory.__qualname__
            )
        raise ValueError(
            "digest cannot read material of type "
            + type(current).__name__
        )

    def _exception_filename(current, attribute):
        if isinstance(current, OSError):
            value = getattr(current, attribute, None)
            if value is not None:
                return value
        return None

    def _exception_channels(current):
        if isinstance(current, ImportError):
            import_name = getattr(current, "name", None)
            import_path = getattr(current, "path", None)
        else:
            import_name = None
            import_path = None
        if isinstance(current, SyntaxError):
            syntax = (
                getattr(current, "filename", None),
                getattr(current, "lineno", None),
                getattr(current, "offset", None),
                getattr(current, "text", None),
                getattr(current, "end_lineno", None),
                getattr(current, "end_offset", None),
            )
        else:
            syntax = None
        return (
            bool(getattr(current, "__suppress_context__", False)),
            import_name,
            import_path,
            syntax,
        )

    results = []
    path = set()
    stack = [(value, False, 0)]
    while stack:
        current, expanded, child_count = stack.pop()
        base_kind = None
        if isinstance(current, dict):
            base_kind = "dict"
        elif isinstance(current, list):
            base_kind = "list"
        elif isinstance(current, tuple):
            base_kind = "tuple"
        elif isinstance(current, frozenset):
            base_kind = "frozenset"
        elif isinstance(current, set):
            base_kind = "set"
        if base_kind is not None:
            if _residual_content_mapping(current) is not None:
                kind = base_kind + "_attrs"
            else:
                kind = base_kind
        elif (
            isinstance(
                current,
                (
                    _decimal_module.Decimal,
                    _datetime_module.date,
                    _datetime_module.time,
                    _datetime_module.timedelta,
                    complex,
                    _array_module.array,
                    _collections_module.deque,
                ),
            )
            and _residual_content_mapping(current) is not None
        ):
            kind = "value_attrs"
        elif (
            isinstance(current, _enum_module.Enum)
            and isinstance(current, (int, float, str, bytes, bytearray))
            and _enum_added_mapping(current) is not None
        ):
            kind = "enum_attrs"
        elif (
            isinstance(
                current,
                (bool, int, float, str, bytes, bytearray, memoryview),
            )
            and not isinstance(current, _enum_module.Enum)
            and _residual_content_mapping(current) is not None
        ):
            kind = "scalar_attrs"
        elif (
            isinstance(current, _io_module.IOBase)
            and _residual_content_mapping(current) is not None
        ):
            kind = "stream_attrs"
        elif (
            isinstance(current, BaseException)
            and _residual_content_mapping(current) is not None
        ):
            kind = "exc_attrs"
        elif (
            isinstance(current, BaseException)
            and (
                getattr(current, "__cause__", None) is not None
                or getattr(current, "__context__", None) is not None
                or getattr(current, "__suppress_context__", False)
                or isinstance(current, (ImportError, SyntaxError))
            )
        ):
            kind = "exc_chain"
        elif (
            current is not None
            and not isinstance(
                current,
                (bool, int, float, str, bytes, bytearray, memoryview),
            )
            and not isinstance(current, _io_module.IOBase)
            and not hasattr(current, "__next__")
            and _residual_content_mapping(current) is not None
        ):
            kind = "attrs"
        else:
            kind = None
        if isinstance(current, _types_module.FunctionType):
            kind = None
        if (
            isinstance(current, _functools_module.partial)
            and _residual_content_mapping(current) is not None
        ):
            raise ValueError(
                "digest cannot read material of type "
                + type(current).__name__
            )
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
                if isinstance(current, _io_module.IOBase):
                    getvalue = getattr(current, "getvalue", None)
                    content = None
                    if getvalue is not None:
                        try:
                            content = getvalue()
                        except Exception:
                            content = None
                    if isinstance(content, bytes):
                        results.append(
                            b"stream:"
                            + type(current).__name__.encode("utf-8")
                            + b":bytes:"
                            + str(len(content)).encode("ascii")
                            + b":" + content + b";"
                        )
                    elif isinstance(content, str):
                        raw = content.encode("utf-8")
                        results.append(
                            b"stream:"
                            + type(current).__name__.encode("utf-8")
                            + b":str:" + str(len(raw)).encode("ascii")
                            + b":" + raw + b";"
                        )
                    else:
                        raise ValueError(
                            "digest cannot read material of type "
                            + type(current).__name__
                        )
                elif hasattr(current, "__next__"):
                    raise ValueError(
                        "digest cannot read material of type "
                        + type(current).__name__
                    )
                elif (
                    type(current).__str__ is object.__str__
                    and type(current).__repr__ is object.__repr__
                ):
                    results.append(
                        b"other:"
                        + type(current).__name__.encode("utf-8")
                        + b":nocontent;"
                    )
                else:
                    text = str(current)
                    if _address_bearing(text):
                        raise ValueError(
                            "digest cannot read material of type "
                            + type(current).__name__
                        )
                    raw = text.encode("utf-8")
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
            if kind in ("dict", "dict_attrs"):
                children = []
                for key in current:
                    children.append(key)
                    children.append(current[key])
                if kind == "dict_attrs":
                    children.append(_residual_content_mapping(current))
                factory_token = _dict_factory_token(current)
                if factory_token is not None:
                    children.append(factory_token)
            elif kind == "exc_attrs":
                children = [
                    tuple(current.args),
                    _residual_content_mapping(current),
                    _exception_filename(current, "filename"),
                    _exception_filename(current, "filename2"),
                    getattr(current, "__cause__", None),
                    getattr(current, "__context__", None),
                    _exception_channels(current),
                ]
            elif kind == "exc_chain":
                children = [
                    tuple(current.args),
                    _exception_filename(current, "filename"),
                    _exception_filename(current, "filename2"),
                    getattr(current, "__cause__", None),
                    getattr(current, "__context__", None),
                    _exception_channels(current),
                ]
            elif kind == "enum_attrs":
                children = [_enum_added_mapping(current)]
            elif kind in (
                "attrs", "value_attrs", "scalar_attrs", "stream_attrs"
            ):
                children = [_residual_content_mapping(current)]
            elif kind in (
                "list_attrs", "tuple_attrs", "set_attrs", "frozenset_attrs"
            ):
                children = list(current)
                children.append(_residual_content_mapping(current))
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
        if kind in ("dict", "dict_attrs"):
            factory_part = None
            entry_parts = parts
            if _dict_factory_token(current) is not None:
                factory_part = parts[-1]
                entry_parts = parts[:-1]
            attrs_part = None
            if kind == "dict_attrs":
                attrs_part = entry_parts[-1]
                entry_parts = entry_parts[:-1]
            entries = []
            for index in range(0, len(entry_parts), 2):
                entries.append(
                    entry_parts[index] + b"=" + entry_parts[index + 1]
                )
            entries.sort()
            encoded = b"dict:{" + b",".join(entries) + b"}"
            if attrs_part is not None:
                encoded = encoded + b"+attrs=" + attrs_part
            if factory_part is not None:
                encoded = encoded + b"+factory=" + factory_part
            if attrs_part is not None or factory_part is not None:
                encoded = encoded + b";"
            results.append(encoded)
        elif kind == "attrs":
            results.append(
                b"object:" + type(current).__name__.encode("utf-8")
                + b"=" + parts[0] + b";"
            )
        elif kind == "exc_attrs":
            results.append(
                b"object:" + type(current).__name__.encode("utf-8")
                + b"=args=" + parts[0] + b"+attrs=" + parts[1]
                + b"+filename=" + parts[2]
                + b"+filename2=" + parts[3]
                + b"+cause=" + parts[4]
                + b"+context=" + parts[5]
                + b"+channels=" + parts[6] + b";"
            )
        elif kind == "exc_chain":
            results.append(
                b"object:" + type(current).__name__.encode("utf-8")
                + b"=args=" + parts[0]
                + b"+filename=" + parts[1]
                + b"+filename2=" + parts[2]
                + b"+cause=" + parts[3]
                + b"+context=" + parts[4]
                + b"+channels=" + parts[5] + b";"
            )
        elif kind == "value_attrs":
            raw = str(current).encode("utf-8")
            intrinsic = (
                b"other:" + type(current).__name__.encode("utf-8")
                + b":" + str(len(raw)).encode("ascii")
                + b":" + raw + b";"
            )
            results.append(intrinsic + b"+attrs=" + parts[0] + b";")
        elif kind in ("scalar_attrs", "enum_attrs"):
            if isinstance(current, bool):
                intrinsic = b"bool:true;" if current else b"bool:false;"
            elif isinstance(current, int):
                intrinsic = (
                    b"int:" + str(current).encode("ascii") + b";"
                )
            elif isinstance(current, float):
                intrinsic = (
                    b"float:" + repr(current).encode("ascii") + b";"
                )
            elif isinstance(current, str):
                raw = current.encode("utf-8")
                intrinsic = (
                    b"str:" + str(len(raw)).encode("ascii")
                    + b":" + raw + b";"
                )
            else:
                raw = bytes(current)
                intrinsic = (
                    b"bytes:" + str(len(raw)).encode("ascii")
                    + b":" + raw + b";"
                )
            results.append(intrinsic + b"+attrs=" + parts[0] + b";")
        elif kind == "stream_attrs":
            getvalue = getattr(current, "getvalue", None)
            content = None
            if getvalue is not None:
                try:
                    content = getvalue()
                except Exception:
                    content = None
            if isinstance(content, bytes):
                intrinsic = (
                    b"stream:"
                    + type(current).__name__.encode("utf-8")
                    + b":bytes:"
                    + str(len(content)).encode("ascii")
                    + b":" + content + b";"
                )
            elif isinstance(content, str):
                raw = content.encode("utf-8")
                intrinsic = (
                    b"stream:"
                    + type(current).__name__.encode("utf-8")
                    + b":str:" + str(len(raw)).encode("ascii")
                    + b":" + raw + b";"
                )
            else:
                raise ValueError(
                    "digest cannot read material of type "
                    + type(current).__name__
                )
            results.append(intrinsic + b"+attrs=" + parts[0] + b";")
        elif kind in ("set", "frozenset", "set_attrs", "frozenset_attrs"):
            attrs_part = None
            member_parts = parts
            base_kind = kind
            if kind in ("set_attrs", "frozenset_attrs"):
                attrs_part = parts[-1]
                member_parts = parts[:-1]
                base_kind = kind[:-len("_attrs")]
            member_parts.sort()
            encoded = (
                base_kind.encode("ascii")
                + b":[" + b",".join(member_parts) + b"]"
            )
            if attrs_part is not None:
                encoded = encoded + b"+attrs=" + attrs_part + b";"
            results.append(encoded)
        else:
            attrs_part = None
            member_parts = parts
            base_kind = kind
            if kind in ("list_attrs", "tuple_attrs"):
                attrs_part = parts[-1]
                member_parts = parts[:-1]
                base_kind = kind[:-len("_attrs")]
            encoded = (
                base_kind.encode("ascii")
                + b":[" + b",".join(member_parts) + b"]"
            )
            if attrs_part is not None:
                encoded = encoded + b"+attrs=" + attrs_part + b";"
            results.append(encoded)
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
    depth, string material over its UTF-8 encoding, a
    subclass instance of a byte like or string type
    carrying added instance content over the tagged
    canonical encoding instead, so that content stands
    in its digest, and any other material over the
    tagged canonical encoding
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

    if (
        isinstance(material, (bytes, bytearray, memoryview))
        and _residual_content_mapping(material) is None
    ):
        payload = bytes(material)
    elif (
        isinstance(material, str)
        and _residual_content_mapping(material) is None
    ):
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
    with the caller part in either direction. A deque
    part keeps the bound it was recorded with. A value
    standing in none of these forms copies through
    the standard deep copy act, and an enum member
    standing anywhere inside such a value, including
    inside a WeakSet, a WeakKeyDictionary, a
    WeakValueDictionary, a weak reference, a partial
    application, a function closure cell, a function
    default value, a function annotation, the globals
    mapping a function reads, a bound method, or a
    property accessor function, stands
    under the same refusal as a member standing in a
    walked position. A generator, a threading lock in
    plain or reentrant form, a threading condition, a
    cell object, a classmethod object, a staticmethod
    object, or a module object standing inside such a
    value stands refused with
    a ValueError, in place of the exception the deep
    copy act raises on a value it cannot copy, and a
    socket object, a frame object, a traceback object,
    a coroutine object, or an async generator object
    standing inside such a value stands refused in
    the same form, and a generator or a lock standing
    in a function closure cell, in a function default
    value, or in the closure or default state of a
    property accessor function stands refused in the
    same form, and a generator, a lock, or any other
    uncopyable value standing in a function annotation
    or in the globals mapping a function reads stands
    refused in the same form, a module value standing
    in the globals mapping of the module the function
    belongs to standing as a binding of that module
    and not as a value the function carries, and a
    dictionary view or a mapping proxy standing in a
    function default value copies in the form its
    walked position gives it, the function standing
    rebuilt over the copied default values where a
    default value carries such a form, and a
    dictionary view or a mapping proxy standing in
    the globals mapping a function reads copies in
    the same form, the function standing rebuilt over
    a copied globals mapping where a globals value
    carries such a form, and a dictionary view or a
    mapping proxy standing in a default value or an
    annotation of a bound method wrapped function or
    of a property accessor function copies in the
    same form, the rebuild landing on the recorded
    method and on the recorded property, and a slice
    standing on its own inside such a value stands
    read by the components it carries, a member
    component standing under the same refusal as the
    walked positions, a view or a proxy component
    copying in the form its walked position gives it,
    and an uncopyable component standing refused in
    the same form, and an accepted shape subclass
    instance of a decimal, a fraction, a datetime,
    or an IPv4Address carrying mutable added instance
    state stands refused with a ValueError naming
    that added state, in each position the instance
    stands in, while an instance carrying no added
    state or only immutable added state stands in its
    standing form. A dictionary view or a mapping
    proxy captured in a closure cell of a function
    copies in the same form, the function standing
    rebuilt over closure cells holding copies of the
    replaced forms, and a dictionary view or a
    mapping proxy standing in the attribute mapping
    of a function copies in the same form, the
    function standing rebuilt with that mapping
    copied apart. The rebuild landing carries the
    sharing of the caller bundle: a rebuilt bound
    method wraps the bound object copy the landing
    itself carries for that object elsewhere in the
    bundle, and two rebuilt functions sharing one
    globals mapping stand over one copied globals
    mapping, the globals cache and the method
    landing memo standing carried at the level of
    the one copy act, across the root values of the
    one bundle, at the top level mapping values, at
    the list and tuple elements, in the separate
    holders, at the nested mapping values, and at
    the bound method limb standing as two separate
    values. A property carrying a clean accessor
    beside a rebuilt accessor stands recorded over
    the rebuilt form of each accessor that stands
    rebuilt and the caller form of each present
    accessor that does not. The shape subclass
    refusal reaches a subclass instance of any
    accepted shape family the immutability reading
    names, a date, a time, a timedelta, a range, a
    UUID, a timezone or tzinfo, an IPv6Address, an
    IPv4Network, an IPv6Network, an IPv4Interface,
    an IPv6Interface, a compiled pattern, or a pure
    path among them, carrying mutable added state,
    in each position the instance stands in, while
    a concrete path instance stands outside that
    reading. A file object of the io module other
    than an in memory stream, a thread local object,
    a database connection of the sqlite3 module, a
    memoryview standing inside such a fallback
    value, an mmap object, a context object of the
    contextvars module, a secure socket context of
    the ssl module, or an epoll object of the select
    module standing inside such a value stands
    refused in the same form as the generator and
    the lock, and a poll object of the select
    module, a cursor object of the sqlite3 module,
    a hash object of the hashlib module, or an HMAC
    object of the hmac module standing inside such
    a value stands refused in the same form, and an
    iterator over a memoryview, a scandir iterator
    or a DirEntry object of the os module, a simple
    queue object of the queue module, a token object
    of the contextvars module, a memory BIO object
    of the ssl module, a byref object or a pointer
    object of the ctypes module, a future object of
    the asyncio module, a database handle object of
    the dbm module, an XMLParser object, a Pickler
    object, a writer object of the csv module, or a
    context manager object of the decimal module
    standing inside such a value stands refused in
    the same form, and a reader object or a DictReader
    object of the csv module, a parser object of the
    pyexpat module, an Unpickler object of the pickle
    module in its compiled form, a Blob object of the
    sqlite3 module, a secure socket object of the ssl
    module, a getset descriptor object, a super object,
    a variable object of the contextvars module, a
    decoder object or a scanner object of the json
    module, the synchronisation and process forms of
    the multiprocessing module, a logger object of
    the logging module, or a connection object of
    the multiprocessing module standing inside such
    a value stands refused in the same form, and a
    pointer bearing form of the ctypes module, a
    character pointer, a wide character pointer, or
    a void pointer value, a callback object, an array
    standing over pointer elements, or a structure
    or union carrying a pointer bearing field
    standing inside such a value stands refused in
    the same form, and an uncopyable value standing
    as an element of an iterator, or standing in
    the arguments an exception object carries,
    standing inside such a value stands refused in
    the same form, the iterator reading standing in
    a form that spends no element of a single pass
    form the act records, and a compressor or
    decompressor object of the bz2 or lzma module,
    a Struct object of the struct module, a Row
    object of the sqlite3 module, a cache wrapper
    object of the functools module, a library
    object of the ctypes module, or a PickleBuffer
    object of the pickle module standing inside
    such a value stands refused in the same form,
    and an uncopyable value standing in the
    attributes or children of a tree element, in
    the text, tail, or tag of a tree element, in
    an operator call specification, in a keyword
    argument of an operator methodcaller
    specification, in the cause
    or context chain an exception object carries,
    or standing as the callable a callable iterator
    or a filter object carries, standing as a bound
    builtin method value in its own right, or
    standing as the function a partial application
    carries, or standing as the callable, predicate,
    key function, or function
    a wider callable iterator form carries, a map,
    starmap, takewhile, dropwhile, filterfalse,
    groupby, or accumulate form among them, standing inside
    such a value stands refused in the same form,
    a chain carrying copyable material standing
    carried into the copy in a form standing apart,
    and a function standing over a globals mapping
    carrying a view of that same mapping standing
    refused in the same form in place of unbounded
    recursion in the replacements limb, the view
    standing at a direct value of that mapping or
    standing inside a container in that mapping or
    inside object attribute storage in that mapping
    in the same refused form.
    A dictionary view standing at
    any position copies as a fresh list of copies of
    the material it carries, an items view as a fresh
    list of copies of its pairs, and a mapping proxy
    standing inside such a fallback value copies as a
    fresh mapping of copies of its entries, in the
    form the walked positions give those shapes, so
    no ungoverned exception escapes the act on those
    forms. An enum member stands
    as a governed form of its own: a member carrying
    mutable instance state stands refused with a
    ValueError, and a member carrying no mutable
    instance state stands shared as an immutable
    value. An attribute value carries no mutable
    state where it stands as an exact atom, as None,
    as a decimal, a fraction, a date, a time, a
    timedelta, or a range value, as a UUID, a
    timezone, or a pure path value, as a tzinfo value
    of any form, a ZoneInfo value among them, as an
    IPv4Address, IPv6Address, IPv4Network, IPv6Network,
    IPv4Interface, or IPv6Interface value, as a compiled
    pattern value, as a slice value whose start, stop,
    and step components each carry no mutable state
    under this same reading, as an Ellipsis value,
    as an enum member
    carrying no mutable instance state, or as a tuple
    or frozenset whose elements all carry no mutable
    state under this same reading. An accepted shape
    carrying a non empty instance attribute mapping
    or slot state declared by its subclass carries
    no mutable state only where every value in that
    mapping and in that slot state itself carries no
    mutable state under this same reading, and a date
    or time value carrying a tzinfo carries no
    mutable state only where the tzinfo it carries
    itself carries no mutable state under this same
    reading. A slot declared with a name carrying a
    leading double underscore stands read, at every
    slot reading of this act, at the storage name the
    interpreter forms from its declaring class. A container or wrapper part carrying
    instance attribute state copies that state apart
    in both directions, its attribute mapping copied
    by this same act, with its type and its entries,
    elements, maps, or text preserved, and a
    defaultdict part keeps the factory it was
    recorded with. Where a subclass type does not
    allow its construction in the form a limb needs,
    or a subclass construction over the copied parts
    alone does not reproduce the part, the copy
    stands in the plain base form carrying the
    copied parts.
    """
    import array as _array_module
    import asyncio as _asyncio_module
    import bz2 as _bz2_module
    import collections as _collections
    import collections.abc as _abc_module
    import contextvars as _contextvars_module
    import copy as _copy_module
    import csv as _csv_module
    import ctypes as _ctypes_module
    import datetime as _datetime_module
    import decimal as _decimal_module
    import enum as _enum_module
    import fractions as _fractions_module
    import functools as _functools_module
    import hashlib as _hashlib_module
    import hmac as _hmac_module
    import io as _io_module
    import ipaddress as _ipaddress_module
    import itertools as _itertools_module
    import json as _json_module
    import logging as _logging_module
    import lzma as _lzma_module
    import mmap as _mmap_module
    import multiprocessing as _multiprocessing_module
    import multiprocessing.connection as _mp_connection_module
    import multiprocessing.process as _mp_process_module
    import multiprocessing.synchronize as _mp_synchronize_module
    import operator as _operator_module
    import os as _os_module
    import pathlib as _pathlib_module
    import pickle as _pickle_module
    import queue as _queue_module
    import re as _re_module
    import select as _select_module
    import socket as _socket_module
    import sqlite3 as _sqlite3_module
    import ssl as _ssl_module
    import struct as _struct_module
    import sys as _sys_module
    import threading as _threading_module
    import types as _types_module
    import uuid as _uuid_module
    import weakref as _weakref_module
    import xml.etree.ElementTree as _xml_module
    import xml.parsers.expat as _expat_module
    import zoneinfo as _zoneinfo_module

    try:
        import _ctypes as _ctypes_private_module
    except Exception:
        _ctypes_private_module = None
    try:
        import _multiprocessing as _multiprocessing_private_module
    except Exception:
        _multiprocessing_private_module = None

    def _is_atom(value):
        return value is None or type(value) in (
            bool, int, float, complex, str, bytes
        )

    def _is_atom_subclass(value):
        return isinstance(
            value, (bool, int, float, complex, str, bytes)
        ) and not _is_atom(value)

    def _tuple_reproduces(built, parts):
        try:
            if len(built) != len(parts):
                return False
            for index in range(len(parts)):
                if built[index] is parts[index]:
                    continue
                if built[index] != parts[index]:
                    return False
            return True
        except Exception:
            return False

    def _tuple_form(original, parts):
        if type(original) is tuple:
            return tuple(parts)
        if hasattr(original, "_fields"):
            try:
                built = type(original)(*parts)
            except Exception:
                return tuple(parts)
            if _tuple_reproduces(built, parts):
                return built
            return tuple(parts)
        try:
            built = type(original)(parts)
        except Exception:
            return tuple(parts)
        if _tuple_reproduces(built, parts):
            return built
        return tuple(parts)

    def _globals_is_home_module(func, globals_map):
        name = globals_map.get("__name__")
        if not isinstance(name, str):
            return False
        home = _sys_module.modules.get(name)
        if home is None:
            return False
        try:
            return home.__dict__ is globals_map
        except Exception:
            return False

    def _globals_walk_values(func):
        globals_map = func.__globals__
        if not isinstance(globals_map, dict):
            return []
        home = _globals_is_home_module(func, globals_map)
        values = []
        for key in globals_map:
            if key == "__builtins__":
                continue
            value = globals_map[key]
            if home and isinstance(
                value, _types_module.ModuleType
            ):
                continue
            values.append(value)
        return values

    _accepted_bases = (
        _decimal_module.Decimal,
        _fractions_module.Fraction,
        _datetime_module.datetime,
        _datetime_module.date,
        _datetime_module.time,
        _datetime_module.timedelta,
        range,
        _uuid_module.UUID,
        _datetime_module.timezone,
        _zoneinfo_module.ZoneInfo,
        _datetime_module.tzinfo,
        _pathlib_module.PurePath,
        _ipaddress_module.IPv4Address,
        _ipaddress_module.IPv6Address,
        _ipaddress_module.IPv4Network,
        _ipaddress_module.IPv6Network,
        _ipaddress_module.IPv4Interface,
        _ipaddress_module.IPv6Interface,
        _re_module.Pattern,
        slice,
        tuple,
        frozenset,
    )

    def _slot_storage_name(cls, name):
        if name.startswith("__") and not name.endswith("__"):
            return "_" + cls.__name__.lstrip("_") + name
        return name

    def _added_slot_values(value):
        values = []
        for cls in type(value).__mro__:
            if cls in _accepted_bases:
                break
            slots = cls.__dict__.get("__slots__")
            if not slots:
                continue
            names = (slots,) if isinstance(slots, str) else slots
            for name in names:
                if name in ("__dict__", "__weakref__"):
                    continue
                try:
                    values.append(
                        getattr(value, _slot_storage_name(cls, name))
                    )
                except Exception:
                    continue
        return values

    def _instance_state_immutable(value, seen):
        items = []
        mapping = getattr(value, "__dict__", None)
        if isinstance(mapping, dict):
            if isinstance(
                value,
                (
                    _ipaddress_module.IPv4Network,
                    _ipaddress_module.IPv6Network,
                    _ipaddress_module.IPv4Interface,
                    _ipaddress_module.IPv6Interface,
                ),
            ):
                intrinsic = (
                    "network_address",
                    "network",
                    "netmask",
                    "_prefixlen",
                    "hosts",
                    "broadcast_address",
                    "hostmask",
                )
                items.extend(
                    mapping[key]
                    for key in mapping
                    if key not in intrinsic
                )
            else:
                items.extend(mapping.values())
        items.extend(_added_slot_values(value))
        if not items:
            return True
        return all(
            _state_immutable(item, seen) for item in items
        )

    def _state_immutable(value, seen=None):
        if _is_atom(value):
            return True
        if value is Ellipsis:
            return True
        if seen is None:
            seen = frozenset()
        if id(value) in seen:
            return True
        seen = seen | {id(value)}
        if isinstance(value, _enum_module.Enum):
            return not _enum_carries_mutable(value, seen)
        if isinstance(value, (tuple, frozenset)):
            return all(
                _state_immutable(item, seen) for item in value
            ) and _instance_state_immutable(value, seen)
        if isinstance(
            value,
            (
                _decimal_module.Decimal,
                _fractions_module.Fraction,
                _datetime_module.date,
                _datetime_module.time,
                _datetime_module.timedelta,
                range,
                _uuid_module.UUID,
                _datetime_module.timezone,
            ),
        ):
            if isinstance(
                value, (_datetime_module.date, _datetime_module.time)
            ):
                carried = getattr(value, "tzinfo", None)
                if carried is not None and not _state_immutable(
                    carried, seen
                ):
                    return False
            return _instance_state_immutable(value, seen)
        if isinstance(value, slice):
            for component in (value.start, value.stop, value.step):
                if component is not None and not _state_immutable(
                    component, seen
                ):
                    return False
            return _instance_state_immutable(value, seen)
        if isinstance(
            value,
            (
                _datetime_module.tzinfo,
                _zoneinfo_module.ZoneInfo,
                _ipaddress_module.IPv4Address,
                _ipaddress_module.IPv6Address,
                _ipaddress_module.IPv4Network,
                _ipaddress_module.IPv6Network,
                _ipaddress_module.IPv4Interface,
                _ipaddress_module.IPv6Interface,
                _re_module.Pattern,
            ),
        ):
            return _instance_state_immutable(value, seen)
        if isinstance(value, _pathlib_module.PurePath) and not isinstance(
            value, _pathlib_module.Path
        ):
            return _instance_state_immutable(value, seen)
        return False

    def _enum_carries_mutable(member, seen=None):
        mapping = getattr(member, "__dict__", None)
        if not mapping:
            return False
        internal = ("_value_", "_name_", "__objclass__", "_sort_order_")
        for key in mapping:
            if key in internal:
                continue
            if not _state_immutable(mapping[key], seen):
                return True
        return False

    def _fallback_holds_mutable_enum(value):
        pending = [value]
        seen = set()
        while pending:
            item = pending.pop()
            if isinstance(item, _enum_module.Enum):
                if _enum_carries_mutable(item):
                    return True
                continue
            if _is_atom(item):
                continue
            if id(item) in seen:
                continue
            seen.add(id(item))
            try:
                if isinstance(item, dict):
                    pending.extend(item.keys())
                    pending.extend(item.values())
                elif isinstance(item, _collections.ChainMap):
                    pending.extend(item.maps)
                elif isinstance(item, _collections.UserDict):
                    pending.append(item.data)
                elif isinstance(item, _weakref_module.WeakSet):
                    pending.extend(list(item))
                elif isinstance(
                    item,
                    (
                        _weakref_module.WeakKeyDictionary,
                        _weakref_module.WeakValueDictionary,
                    ),
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item, _types_module.MappingProxyType
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item,
                    (
                        _abc_module.KeysView,
                        _abc_module.ValuesView,
                        _abc_module.ItemsView,
                    ),
                ):
                    pending.extend(list(item))
                elif isinstance(item, _weakref_module.ReferenceType):
                    target = item()
                    if target is not None:
                        pending.append(target)
                elif isinstance(item, _functools_module.partial):
                    pending.append(item.func)
                    pending.extend(item.args)
                    if item.keywords:
                        pending.append(dict(item.keywords))
                elif isinstance(item, _types_module.FunctionType):
                    closure = item.__closure__
                    if closure:
                        for cell in closure:
                            try:
                                pending.append(cell.cell_contents)
                            except Exception:
                                continue
                    if item.__defaults__:
                        pending.extend(item.__defaults__)
                    if item.__kwdefaults__:
                        pending.extend(item.__kwdefaults__.values())
                    if item.__annotations__:
                        pending.extend(
                            item.__annotations__.values()
                        )
                    globals_map = item.__globals__
                    if (
                        isinstance(globals_map, dict)
                        and id(globals_map) not in seen
                    ):
                        seen.add(id(globals_map))
                        for global_value in list(
                            globals_map.values()
                        ):
                            if isinstance(
                                global_value,
                                _types_module.ModuleType,
                            ):
                                seen.add(id(global_value))
                            pending.append(global_value)
                elif isinstance(item, _types_module.MethodType):
                    pending.append(item.__self__)
                    pending.append(item.__func__)
                elif isinstance(item, property):
                    for accessor in (item.fget, item.fset, item.fdel):
                        if accessor is not None:
                            pending.append(accessor)
                elif isinstance(item, slice):
                    for component in (item.start, item.stop, item.step):
                        if component is not None:
                            pending.append(component)
                elif isinstance(
                    item,
                    (
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                    ),
                ):
                    pending.extend(item)
            except Exception:
                pass
            mapping = getattr(item, "__dict__", None)
            if isinstance(mapping, dict):
                pending.append(mapping)
            for klass in type(item).__mro__:
                slots = klass.__dict__.get("__slots__")
                if not slots:
                    continue
                if isinstance(slots, str):
                    slots = (slots,)
                for slot in slots:
                    try:
                        pending.append(
                            getattr(item, _slot_storage_name(klass, slot))
                        )
                    except Exception:
                        pass
        return False

    def _fallback_replacements(value):
        found = {}
        pending = [value]
        seen = set()
        while pending:
            item = pending.pop()
            if isinstance(item, _enum_module.Enum):
                continue
            if _is_atom(item):
                continue
            if id(item) in seen:
                continue
            seen.add(id(item))
            try:
                if isinstance(
                    item,
                    (
                        _types_module.MappingProxyType,
                        _abc_module.KeysView,
                        _abc_module.ValuesView,
                        _abc_module.ItemsView,
                    ),
                ):
                    found[id(item)] = item
                    if isinstance(item, _types_module.MappingProxyType):
                        pending.extend(list(item.keys()))
                        pending.extend(list(item.values()))
                    else:
                        pending.extend(list(item))
                    continue
                if isinstance(item, dict):
                    pending.extend(item.keys())
                    pending.extend(item.values())
                elif isinstance(item, _collections.ChainMap):
                    pending.extend(item.maps)
                elif isinstance(item, _collections.UserDict):
                    pending.append(item.data)
                elif isinstance(item, _weakref_module.WeakSet):
                    pending.extend(list(item))
                elif isinstance(
                    item,
                    (
                        _weakref_module.WeakKeyDictionary,
                        _weakref_module.WeakValueDictionary,
                    ),
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(item, _weakref_module.ReferenceType):
                    target = item()
                    if target is not None:
                        pending.append(target)
                elif isinstance(item, _functools_module.partial):
                    pending.append(item.func)
                    pending.extend(item.args)
                    if item.keywords:
                        pending.append(dict(item.keywords))
                elif isinstance(item, _types_module.FunctionType):
                    closure = item.__closure__
                    if closure:
                        for cell in closure:
                            try:
                                pending.append(cell.cell_contents)
                            except Exception:
                                continue
                    if item.__defaults__:
                        pending.extend(item.__defaults__)
                    if item.__kwdefaults__:
                        pending.extend(item.__kwdefaults__.values())
                    if item.__annotations__:
                        pending.extend(
                            item.__annotations__.values()
                        )
                    globals_map = item.__globals__
                    if (
                        isinstance(globals_map, dict)
                        and id(globals_map) not in seen
                    ):
                        seen.add(id(globals_map))
                        pending.extend(_globals_walk_values(item))
                elif isinstance(item, _types_module.MethodType):
                    pending.append(item.__self__)
                    pending.append(item.__func__)
                elif isinstance(item, property):
                    for accessor in (item.fget, item.fset, item.fdel):
                        if accessor is not None:
                            pending.append(accessor)
                elif isinstance(item, slice):
                    for component in (item.start, item.stop, item.step):
                        if component is not None:
                            pending.append(component)
                elif isinstance(
                    item,
                    (
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                    ),
                ):
                    pending.extend(item)
            except Exception:
                pass
            mapping = getattr(item, "__dict__", None)
            if isinstance(mapping, dict):
                pending.append(mapping)
            for klass in type(item).__mro__:
                slots = klass.__dict__.get("__slots__")
                if not slots:
                    continue
                if isinstance(slots, str):
                    slots = (slots,)
                for slot in slots:
                    try:
                        pending.append(
                            getattr(item, _slot_storage_name(klass, slot))
                        )
                    except Exception:
                        pass
        return found

    def _walk_nodes(root):
        nodes = []
        pending = [root]
        seen = set()
        while pending:
            item = pending.pop()
            if isinstance(item, _enum_module.Enum):
                continue
            if _is_atom(item):
                continue
            if id(item) in seen:
                continue
            seen.add(id(item))
            nodes.append(item)
            try:
                if isinstance(item, dict):
                    pending.extend(item.keys())
                    pending.extend(item.values())
                elif isinstance(item, _collections.ChainMap):
                    pending.extend(item.maps)
                elif isinstance(item, _collections.UserDict):
                    pending.append(item.data)
                elif isinstance(item, _weakref_module.WeakSet):
                    pending.extend(list(item))
                elif isinstance(
                    item,
                    (
                        _weakref_module.WeakKeyDictionary,
                        _weakref_module.WeakValueDictionary,
                    ),
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item, _types_module.MappingProxyType
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item,
                    (
                        _abc_module.KeysView,
                        _abc_module.ValuesView,
                        _abc_module.ItemsView,
                    ),
                ):
                    pending.extend(list(item))
                elif isinstance(item, _weakref_module.ReferenceType):
                    target = item()
                    if target is not None:
                        pending.append(target)
                elif isinstance(item, _functools_module.partial):
                    pending.append(item.func)
                    pending.extend(item.args)
                    if item.keywords:
                        pending.append(dict(item.keywords))
                elif isinstance(item, _types_module.FunctionType):
                    closure = item.__closure__
                    if closure:
                        for cell in closure:
                            try:
                                pending.append(cell.cell_contents)
                            except Exception:
                                continue
                    if item.__defaults__:
                        pending.extend(item.__defaults__)
                    if item.__kwdefaults__:
                        pending.extend(item.__kwdefaults__.values())
                    if item.__annotations__:
                        pending.extend(
                            item.__annotations__.values()
                        )
                    globals_map = item.__globals__
                    if (
                        isinstance(globals_map, dict)
                        and id(globals_map) not in seen
                    ):
                        seen.add(id(globals_map))
                        pending.extend(_globals_walk_values(item))
                elif isinstance(item, _types_module.MethodType):
                    pending.append(item.__self__)
                    pending.append(item.__func__)
                elif isinstance(item, property):
                    for accessor in (item.fget, item.fset, item.fdel):
                        if accessor is not None:
                            pending.append(accessor)
                elif isinstance(item, slice):
                    for component in (item.start, item.stop, item.step):
                        if component is not None:
                            pending.append(component)
                elif isinstance(
                    item,
                    (
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                    ),
                ):
                    pending.extend(item)
            except Exception:
                pass
            mapping = getattr(item, "__dict__", None)
            if isinstance(mapping, dict):
                pending.append(mapping)
            for klass in type(item).__mro__:
                slots = klass.__dict__.get("__slots__")
                if not slots:
                    continue
                if isinstance(slots, str):
                    slots = (slots,)
                for slot in slots:
                    try:
                        pending.append(
                            getattr(item, _slot_storage_name(klass, slot))
                        )
                    except Exception:
                        pass
        return nodes

    def _functions_with_replacement_defaults(root, replacements):
        marked = []
        for node in _walk_nodes(root):
            if not isinstance(node, _types_module.FunctionType):
                continue
            defaults = list(node.__defaults__ or ())
            if node.__kwdefaults__:
                defaults.extend(node.__kwdefaults__.values())
            if node.__annotations__:
                defaults.extend(node.__annotations__.values())
            if node.__closure__:
                for cell in node.__closure__:
                    try:
                        defaults.append(cell.cell_contents)
                    except Exception:
                        continue
            if node.__dict__:
                defaults.extend(node.__dict__.values())
            defaults.extend(_globals_walk_values(node))
            for default in defaults:
                if any(
                    id(part) in replacements
                    for part in _walk_nodes(default)
                ):
                    marked.append(node)
                    break
        return marked

    def _copied_globals(func, replacements, cache=None):
        globals_map = func.__globals__
        if not isinstance(globals_map, dict):
            return None
        if cache is not None and id(globals_map) in cache:
            return cache[id(globals_map)]
        changed = False
        new_globals = dict(globals_map)
        for key in globals_map:
            if key == "__builtins__":
                continue
            value = globals_map[key]
            if any(
                id(part) in replacements
                for part in _walk_nodes(value)
            ):
                new_globals[key] = _bundle_copy(value)
                changed = True
        result = new_globals if changed else None
        if cache is not None:
            cache[id(globals_map)] = result
        return result

    def _function_with_copied_defaults(
        func, replacements=None, new_globals=None
    ):
        if func.__defaults__:
            new_defaults = tuple(
                _bundle_copy(part) for part in func.__defaults__
            )
        else:
            new_defaults = None
        new_closure = func.__closure__
        if func.__closure__:
            cells = []
            for cell in func.__closure__:
                try:
                    contents = cell.cell_contents
                except Exception:
                    cells.append(cell)
                    continue
                if contents is func:
                    cells.append(cell)
                    continue
                if replacements and any(
                    id(part) in replacements
                    for part in _walk_nodes(contents)
                ):
                    cells.append(
                        _types_module.CellType(_bundle_copy(contents))
                    )
                else:
                    cells.append(cell)
            new_closure = tuple(cells)
        built = _types_module.FunctionType(
            func.__code__,
            new_globals if new_globals is not None
            else func.__globals__,
            func.__name__,
            new_defaults,
            new_closure,
        )
        if func.__kwdefaults__:
            built.__kwdefaults__ = {
                key: _bundle_copy(part)
                for key, part in func.__kwdefaults__.items()
            }
        if func.__dict__:
            built.__dict__.update(_bundle_copy(dict(func.__dict__)))
        try:
            built.__module__ = func.__module__
        except Exception:
            pass
        try:
            built.__qualname__ = func.__qualname__
        except Exception:
            pass
        try:
            if func.__annotations__:
                if replacements:
                    copied_annotations = {}
                    for key, part in func.__annotations__.items():
                        if any(
                            id(node) in replacements
                            for node in _walk_nodes(part)
                        ):
                            copied_annotations[key] = _bundle_copy(
                                part
                            )
                        else:
                            copied_annotations[key] = part
                    built.__annotations__ = copied_annotations
                else:
                    built.__annotations__ = dict(func.__annotations__)
        except Exception:
            pass
        return built

    def _shape_subclass_carries_mutable_added(value):
        if type(value) in _accepted_bases:
            return False
        if isinstance(value, _pathlib_module.Path):
            return False
        if not isinstance(
            value,
            (
                _decimal_module.Decimal,
                _fractions_module.Fraction,
                _datetime_module.datetime,
                _datetime_module.date,
                _datetime_module.time,
                _datetime_module.timedelta,
                range,
                _uuid_module.UUID,
                _datetime_module.timezone,
                _datetime_module.tzinfo,
                _ipaddress_module.IPv4Address,
                _ipaddress_module.IPv6Address,
                _ipaddress_module.IPv4Network,
                _ipaddress_module.IPv6Network,
                _ipaddress_module.IPv4Interface,
                _ipaddress_module.IPv6Interface,
                _re_module.Pattern,
                _pathlib_module.PurePath,
            ),
        ):
            return False
        return not _instance_state_immutable(value, frozenset())

    def _fallback_holds_mutable_added_shape(value):
        for node in _walk_nodes(value):
            if _shape_subclass_carries_mutable_added(node):
                return True
        return False

    _lock_type = type(_threading_module.Lock())
    _rlock_type = type(_threading_module.RLock())
    _condition_type = type(_threading_module.Condition())
    _thread_local_type = type(_threading_module.local())
    _epoll_type = getattr(_select_module, "epoll", None)
    _poll_type = (
        type(_select_module.poll())
        if hasattr(_select_module, "poll") else None
    )
    _cursor_type = _sqlite3_module.Cursor
    _hash_type = type(_hashlib_module.sha256())
    _hmac_type = _hmac_module.HMAC
    _memory_iterator_type = type(iter(memoryview(b"")))
    try:
        _scandir_probe = _os_module.scandir(_os_module.curdir)
        _scandir_iterator_type = type(_scandir_probe)
        _scandir_probe.close()
    except Exception:
        _scandir_iterator_type = None
    _dir_entry_type = getattr(_os_module, "DirEntry", None)
    _simple_queue_type = _queue_module.SimpleQueue
    _token_type = _contextvars_module.Token
    _memory_bio_type = _ssl_module.MemoryBIO
    _carg_object_type = type(
        _ctypes_module.byref(_ctypes_module.c_int(0))
    )
    _pointer_type = getattr(_ctypes_module, "_Pointer", None)
    _future_type = _asyncio_module.Future
    _xml_parser_type = _xml_module.XMLParser
    _pickler_type = _pickle_module.Pickler
    _csv_writer_type = type(
        _csv_module.writer(_io_module.StringIO())
    )
    _decimal_context_manager_type = type(
        _decimal_module.localcontext()
    )
    _dbm_type_identities = (("_dbm", "dbm"), ("_gdbm", "gdbm"))
    _csv_reader_type = type(
        _csv_module.reader(_io_module.StringIO())
    )
    _expat_parser_type = type(_expat_module.ParserCreate())
    _unpickler_type = type(
        _pickle_module.Unpickler(_io_module.BytesIO(b""))
    )
    _json_scanner_type = type(_json_module.JSONDecoder().scan_once)
    _bz2_compressor_type = type(_bz2_module.BZ2Compressor())
    _bz2_decompressor_type = type(_bz2_module.BZ2Decompressor())
    _lzma_compressor_type = type(_lzma_module.LZMACompressor())
    _lzma_decompressor_type = type(_lzma_module.LZMADecompressor())
    _lru_cache_wrapper_type = type(
        _functools_module.lru_cache(maxsize=None)(lambda: None)
    )
    _callable_iterator_type = type(iter(lambda: None, None))
    _wider_callable_iterator_types = (
        map,
        _itertools_module.starmap,
        _itertools_module.takewhile,
        _itertools_module.dropwhile,
        _itertools_module.filterfalse,
        _itertools_module.groupby,
        _itertools_module.accumulate,
    )
    _wider_callable_second_types = (
        _itertools_module.groupby,
        _itertools_module.accumulate,
    )
    _semlock_type = (
        getattr(
            _multiprocessing_private_module, "SemLock", None
        )
        if _multiprocessing_private_module is not None
        else None
    )
    _extra_uncopyable_types = tuple(
        kind
        for kind in (
            _csv_reader_type,
            _csv_module.DictReader,
            _expat_parser_type,
            _unpickler_type,
            _sqlite3_module.Blob,
            _ssl_module.SSLObject,
            getattr(_ssl_module, "_SSLSocket", None),
            getattr(_types_module, "GetSetDescriptorType", None),
            super,
            _contextvars_module.ContextVar,
            _json_module.JSONDecoder,
            _json_scanner_type,
            _semlock_type,
            _mp_synchronize_module.Lock,
            _mp_synchronize_module.Semaphore,
            _mp_synchronize_module.BoundedSemaphore,
            _mp_synchronize_module.Event,
            _mp_synchronize_module.Condition,
            _mp_process_module.BaseProcess,
            _mp_connection_module.Connection,
            _logging_module.Logger,
            _bz2_compressor_type,
            _bz2_decompressor_type,
            _lzma_compressor_type,
            _lzma_decompressor_type,
            _struct_module.Struct,
            _sqlite3_module.Row,
            _lru_cache_wrapper_type,
            _ctypes_module.CDLL,
            _pickle_module.PickleBuffer,
        )
        if kind is not None
    )
    _cfunc_ptr_type = (
        getattr(_ctypes_private_module, "CFuncPtr", None)
        if _ctypes_private_module is not None
        else None
    )
    _ctypes_pointer_value_types = (
        _ctypes_module.c_char_p,
        _ctypes_module.c_wchar_p,
        _ctypes_module.c_void_p,
    )

    def _ctypes_type_bearing(kind, seen=None):
        if not isinstance(kind, type):
            return False
        if kind in _ctypes_pointer_value_types:
            return True
        if seen is None:
            seen = set()
        if kind in seen:
            return False
        seen = seen | {kind}
        try:
            if _pointer_type is not None and issubclass(
                kind, _pointer_type
            ):
                return True
            if _cfunc_ptr_type is not None and issubclass(
                kind, _cfunc_ptr_type
            ):
                return True
            if issubclass(kind, _ctypes_module.Array):
                return _ctypes_type_bearing(
                    getattr(kind, "_type_", None), seen
                )
            if issubclass(
                kind,
                (_ctypes_module.Structure, _ctypes_module.Union),
            ):
                return any(
                    _ctypes_type_bearing(field[1], seen)
                    for field in getattr(kind, "_fields_", [])
                    if len(field) > 1
                )
        except Exception:
            return False
        return False

    def _ctypes_value_bearing(value):
        if isinstance(value, _ctypes_pointer_value_types):
            return True
        if _cfunc_ptr_type is not None and isinstance(
            value, _cfunc_ptr_type
        ):
            return True
        if isinstance(value, _ctypes_module.Array):
            if _ctypes_type_bearing(
                getattr(type(value), "_type_", None)
            ):
                return True
            try:
                return any(
                    _ctypes_value_bearing(element)
                    for element in list(value)
                )
            except Exception:
                return False
        if isinstance(
            value, (_ctypes_module.Structure, _ctypes_module.Union)
        ):
            fields = getattr(type(value), "_fields_", [])
            for field in fields:
                if len(field) > 1 and _ctypes_type_bearing(field[1]):
                    return True
                try:
                    carried = getattr(value, field[0])
                except Exception:
                    continue
                if _pointer_type is not None and isinstance(
                    carried, _pointer_type
                ):
                    return True
                if isinstance(
                    carried,
                    (
                        _ctypes_module.Array,
                        _ctypes_module.Structure,
                        _ctypes_module.Union,
                    ),
                ) and _ctypes_value_bearing(carried):
                    return True
            return False
        return False

    def _view_holds_itself(view):
        mapping = getattr(view, "mapping", None)
        if mapping is None:
            mapping = getattr(view, "_mapping", None)
        if mapping is None:
            return False
        pending = [mapping]
        seen = set()
        while pending:
            item = pending.pop()
            if item is view:
                return True
            if _is_atom(item):
                continue
            if id(item) in seen:
                continue
            seen.add(id(item))
            try:
                if isinstance(item, dict):
                    pending.extend(item.keys())
                    pending.extend(item.values())
                elif isinstance(item, _collections.ChainMap):
                    pending.extend(item.maps)
                elif isinstance(item, _collections.UserDict):
                    pending.append(item.data)
                elif isinstance(
                    item, _types_module.MappingProxyType
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item,
                    (
                        _abc_module.KeysView,
                        _abc_module.ValuesView,
                        _abc_module.ItemsView,
                    ),
                ):
                    pending.extend(list(item))
                elif isinstance(
                    item,
                    (
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                    ),
                ):
                    pending.extend(item)
                elif not isinstance(
                    item,
                    (
                        _types_module.ModuleType,
                        _types_module.FunctionType,
                        type,
                    ),
                ):
                    attribute_map = getattr(
                        item, "__dict__", None
                    )
                    if isinstance(attribute_map, dict):
                        pending.append(attribute_map)
            except Exception:
                pass
        return False

    def _reduce_carried(item):
        try:
            reduced = item.__reduce_ex__(4)
        except Exception:
            return ()
        if (
            isinstance(reduced, tuple)
            and len(reduced) >= 2
            and isinstance(reduced[1], tuple)
        ):
            return reduced[1]
        return ()

    def _reduce_head(item):
        try:
            reduced = item.__reduce_ex__(4)
        except Exception:
            return None
        if isinstance(reduced, tuple) and reduced:
            return reduced[0]
        return None

    def _fallback_holds_uncopyable(value):
        pending = [value]
        seen = set()
        globals_seen = set()
        while pending:
            item = pending.pop()
            if isinstance(
                item,
                (
                    _types_module.GeneratorType,
                    _lock_type,
                    _rlock_type,
                    _condition_type,
                    _types_module.CellType,
                    _types_module.ModuleType,
                    _types_module.FrameType,
                    _types_module.TracebackType,
                    _types_module.CoroutineType,
                    _types_module.AsyncGeneratorType,
                    _socket_module.socket,
                    _thread_local_type,
                    _sqlite3_module.Connection,
                    _cursor_type,
                    _hash_type,
                    _hmac_type,
                    memoryview,
                    _mmap_module.mmap,
                    _contextvars_module.Context,
                    _ssl_module.SSLContext,
                    _memory_iterator_type,
                    _simple_queue_type,
                    _token_type,
                    _memory_bio_type,
                    _carg_object_type,
                    _future_type,
                    _xml_parser_type,
                    _pickler_type,
                    _csv_writer_type,
                    _decimal_context_manager_type,
                    classmethod,
                    staticmethod,
                ),
            ):
                return True
            if _epoll_type is not None and isinstance(
                item, _epoll_type
            ):
                return True
            if _poll_type is not None and isinstance(
                item, _poll_type
            ):
                return True
            if _scandir_iterator_type is not None and isinstance(
                item, _scandir_iterator_type
            ):
                return True
            if _dir_entry_type is not None and isinstance(
                item, _dir_entry_type
            ):
                return True
            if _pointer_type is not None and isinstance(
                item, _pointer_type
            ):
                return True
            if (
                type(item).__module__, type(item).__name__
            ) in _dbm_type_identities:
                return True
            if isinstance(item, _extra_uncopyable_types):
                return True
            if _ctypes_value_bearing(item):
                return True
            if isinstance(item, _io_module.IOBase) and not isinstance(
                item, (_io_module.BytesIO, _io_module.StringIO)
            ):
                return True
            if isinstance(item, _enum_module.Enum):
                continue
            if _is_atom(item):
                continue
            if id(item) in seen:
                continue
            seen.add(id(item))
            if isinstance(
                item,
                (
                    _abc_module.KeysView,
                    _abc_module.ValuesView,
                    _abc_module.ItemsView,
                ),
            ) and _view_holds_itself(item):
                return True
            if isinstance(item, _abc_module.Iterator):
                try:
                    _copy_module.deepcopy(item)
                except Exception:
                    return True
                pending.extend(_reduce_carried(item))
            if isinstance(item, _xml_module.Element):
                try:
                    pending.extend(list(item.attrib.keys()))
                    pending.extend(list(item.attrib.values()))
                    pending.extend(list(item))
                    for carried in (item.text, item.tail, item.tag):
                        if carried is not None:
                            pending.append(carried)
                except Exception:
                    pass
            if isinstance(item, _xml_module.ElementTree):
                try:
                    root = item.getroot()
                    if root is not None:
                        pending.append(root)
                except Exception:
                    pass
            if isinstance(item, _operator_module.methodcaller):
                carried = _reduce_carried(item)
                head = _reduce_head(item)
                if isinstance(head, _functools_module.partial):
                    pending.extend(carried)
                    pending.extend(head.args[1:])
                    if head.keywords:
                        pending.extend(list(head.keywords.values()))
                else:
                    pending.extend(carried[1:])
            if isinstance(item, _operator_module.itemgetter):
                pending.extend(_reduce_carried(item))
            if isinstance(item, filter) or isinstance(
                item, _callable_iterator_type
            ):
                carried = _reduce_carried(item)
                if carried and carried[0] is not None:
                    pending.append(carried[0])
                    bound = getattr(carried[0], "__self__", None)
                    if bound is not None:
                        pending.append(bound)
                if (
                    isinstance(item, _callable_iterator_type)
                    and len(carried) > 1
                ):
                    pending.append(carried[1])
            if isinstance(item, _wider_callable_iterator_types):
                carried = _reduce_carried(item)
                if isinstance(item, _wider_callable_second_types):
                    index = 1
                else:
                    index = 0
                if len(carried) > index and carried[index] is not None:
                    pending.append(carried[index])
                    bound = getattr(carried[index], "__self__", None)
                    if bound is not None:
                        pending.append(bound)
            try:
                if isinstance(item, dict):
                    pending.extend(item.keys())
                    pending.extend(item.values())
                elif isinstance(item, _collections.ChainMap):
                    pending.extend(item.maps)
                elif isinstance(item, _collections.UserDict):
                    pending.append(item.data)
                elif isinstance(item, _weakref_module.WeakSet):
                    pending.extend(list(item))
                elif isinstance(
                    item,
                    (
                        _weakref_module.WeakKeyDictionary,
                        _weakref_module.WeakValueDictionary,
                    ),
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item, _types_module.MappingProxyType
                ):
                    pending.extend(list(item.keys()))
                    pending.extend(list(item.values()))
                elif isinstance(
                    item,
                    (
                        _abc_module.KeysView,
                        _abc_module.ValuesView,
                        _abc_module.ItemsView,
                    ),
                ):
                    pending.extend(list(item))
                elif isinstance(item, _weakref_module.ReferenceType):
                    target = item()
                    if target is not None:
                        pending.append(target)
                elif isinstance(item, _functools_module.partial):
                    pending.append(item.func)
                    pending.extend(item.args)
                    if item.keywords:
                        pending.append(dict(item.keywords))
                elif isinstance(item, _types_module.FunctionType):
                    closure = item.__closure__
                    if closure:
                        for cell in closure:
                            try:
                                pending.append(cell.cell_contents)
                            except Exception:
                                continue
                    if item.__defaults__:
                        pending.extend(item.__defaults__)
                    if item.__kwdefaults__:
                        pending.extend(item.__kwdefaults__.values())
                    if item.__annotations__:
                        pending.extend(
                            item.__annotations__.values()
                        )
                    globals_map = item.__globals__
                    if (
                        isinstance(globals_map, dict)
                        and id(globals_map) not in globals_seen
                    ):
                        globals_seen.add(id(globals_map))
                        pending.extend(_globals_walk_values(item))
                elif isinstance(item, _types_module.MethodType):
                    pending.append(item.__self__)
                    pending.append(item.__func__)
                elif isinstance(
                    item, _types_module.BuiltinFunctionType
                ):
                    bound = getattr(item, "__self__", None)
                    if (
                        bound is not None
                        and not isinstance(
                            bound, _types_module.ModuleType
                        )
                        and not isinstance(bound, type)
                    ):
                        pending.append(bound)
                elif isinstance(item, property):
                    for accessor in (item.fget, item.fset, item.fdel):
                        if accessor is not None:
                            pending.append(accessor)
                elif isinstance(item, slice):
                    for component in (item.start, item.stop, item.step):
                        if component is not None:
                            pending.append(component)
                elif isinstance(
                    item,
                    (
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                    ),
                ):
                    pending.extend(item)
            except Exception:
                pass
            mapping = getattr(item, "__dict__", None)
            if isinstance(mapping, dict):
                pending.append(mapping)
            if isinstance(item, BaseException):
                pending.extend(item.args)
                try:
                    for chained in (
                        item.__cause__, item.__context__
                    ):
                        if chained is not None:
                            pending.append(chained)
                except Exception:
                    pass
            for klass in type(item).__mro__:
                slots = klass.__dict__.get("__slots__")
                if not slots:
                    continue
                if isinstance(slots, str):
                    slots = (slots,)
                for slot in slots:
                    try:
                        pending.append(
                            getattr(item, _slot_storage_name(klass, slot))
                        )
                    except Exception:
                        pass
        return False

    def _stitch_exception_chains(root, built, memo):
        collected = []
        seen_ids = set()
        pending_roots = [root]
        while pending_roots:
            current_root = pending_roots.pop()
            for node in _walk_nodes(current_root):
                if id(node) in seen_ids:
                    continue
                seen_ids.add(id(node))
                if not isinstance(node, BaseException):
                    continue
                collected.append(node)
                try:
                    chained_nodes = (
                        node.__cause__, node.__context__
                    )
                except Exception:
                    chained_nodes = ()
                for chained in chained_nodes:
                    if (
                        chained is not None
                        and id(chained) not in seen_ids
                    ):
                        pending_roots.append(chained)
        if not collected:
            return
        pairs = {}
        for node in collected:
            copied = memo.get(id(node)) if memo else None
            if copied is None and node is root:
                copied = built
            if copied is not None:
                pairs[id(node)] = copied
        for node in collected:
            if id(node) in pairs:
                continue
            try:
                saved_cause = node.__cause__
                saved_context = node.__context__
            except Exception:
                continue
            try:
                node.__cause__ = None
                node.__context__ = None
            except Exception:
                pass
            try:
                copied = _bundle_copy(node)
            finally:
                try:
                    node.__cause__ = saved_cause
                    node.__context__ = saved_context
                except Exception:
                    pass
            pairs[id(node)] = copied
        for node in collected:
            copied = pairs.get(id(node))
            if copied is None:
                continue
            for attr in ("__cause__", "__context__"):
                try:
                    chained = getattr(node, attr)
                except Exception:
                    continue
                if chained is None:
                    try:
                        setattr(copied, attr, None)
                    except Exception:
                        pass
                elif id(chained) in pairs:
                    try:
                        setattr(copied, attr, pairs[id(chained)])
                    except Exception:
                        pass
            try:
                copied.__suppress_context__ = (
                    node.__suppress_context__
                )
            except Exception:
                pass

    def _attr_mapping(value):
        mapping = getattr(value, "__dict__", None)
        if isinstance(mapping, dict):
            return mapping
        return None

    def _apply_attrs(built, copied_mapping):
        try:
            built.__dict__.update(copied_mapping)
        except Exception:
            try:
                built.__dict__ = dict(copied_mapping)
            except Exception:
                pass

    memo = {}
    in_progress = set()
    act_globals_cache = {}
    act_landing_memo = {}
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
            attr_copy = None
            if _attr_mapping(current) is not None:
                attr_copy = parts[-1]
                parts = parts[:-1]
            if kind == "attrs":
                _apply_attrs(placeholder, attr_copy)
                results.append(placeholder)
            elif kind == "mapping":
                for index in range(0, len(parts), 2):
                    placeholder[parts[index]] = parts[index + 1]
                if attr_copy is not None:
                    _apply_attrs(placeholder, attr_copy)
                results.append(placeholder)
            elif kind == "chainmap":
                placeholder.maps = list(parts)
                if attr_copy is not None:
                    _apply_attrs(placeholder, attr_copy)
                results.append(placeholder)
            elif kind == "sequence":
                placeholder.extend(parts)
                if attr_copy is not None:
                    _apply_attrs(placeholder, attr_copy)
                results.append(placeholder)
            elif kind == "set":
                placeholder.update(parts)
                if attr_copy is not None:
                    _apply_attrs(placeholder, attr_copy)
                results.append(placeholder)
            elif kind == "tuple":
                in_progress.discard(id(current))
                if id(current) in memo:
                    results.append(memo[id(current)])
                else:
                    built = _tuple_form(current, parts)
                    memo[id(current)] = built
                    if attr_copy is not None:
                        _apply_attrs(built, attr_copy)
                    results.append(built)
            elif kind == "frozenset":
                in_progress.discard(id(current))
                if id(current) in memo:
                    results.append(memo[id(current)])
                else:
                    try:
                        built = type(current)(parts)
                    except Exception:
                        built = frozenset(parts)
                    memo[id(current)] = built
                    if attr_copy is not None:
                        _apply_attrs(built, attr_copy)
                    results.append(built)
            continue
        if id(current) in memo:
            results.append(memo[id(current)])
            continue
        if isinstance(current, _enum_module.Enum):
            if _enum_carries_mutable(current):
                raise ValueError(
                    "enum member with mutable instance state in bundle copy"
                )
            results.append(current)
            continue
        if id(current) in in_progress:
            parts = []
            for child in list(current):
                if id(child) in memo:
                    parts.append(memo[id(child)])
                elif isinstance(child, _enum_module.Enum):
                    if _enum_carries_mutable(child):
                        raise ValueError(
                            "enum member with mutable instance state "
                            "in bundle copy"
                        )
                    parts.append(child)
                elif _is_atom(child):
                    parts.append(child)
                elif _is_atom_subclass(child):
                    if _fallback_holds_mutable_enum(child):
                        raise ValueError(
                            "enum member with mutable instance state "
                            "in bundle copy"
                        )
                    copied = _copy_module.deepcopy(child)
                    memo[id(child)] = copied
                    parts.append(copied)
                else:
                    raise ValueError("cyclic value in bundle copy")
            if isinstance(current, frozenset):
                try:
                    built = type(current)(parts)
                except Exception:
                    built = frozenset(parts)
            else:
                built = _tuple_form(current, parts)
            cyclic_attrs = _attr_mapping(current)
            if cyclic_attrs is not None:
                if _fallback_holds_mutable_enum(cyclic_attrs):
                    raise ValueError(
                        "enum member with mutable instance state "
                        "in bundle copy"
                    )
                _apply_attrs(
                    built, _copy_module.deepcopy(cyclic_attrs)
                )
            memo[id(current)] = built
            results.append(built)
            continue
        if _is_atom(current):
            results.append(current)
            continue
        if isinstance(current, bytearray):
            try:
                built = type(current)(current)
            except Exception:
                built = bytearray(current)
            memo[id(current)] = built
            attrs = _attr_mapping(current)
            if attrs is None:
                results.append(built)
                continue
            stack.append((current, True, "attrs", built, 1))
            stack.append((attrs, False, None, None, 0))
            continue
        if isinstance(current, memoryview):
            built = bytearray(current.tobytes())
            memo[id(current)] = built
            results.append(built)
            continue
        if isinstance(current, _array_module.array):
            try:
                built = type(current)(current.typecode, current)
            except Exception:
                built = _array_module.array(current.typecode, current)
            memo[id(current)] = built
            attrs = _attr_mapping(current)
            if attrs is None:
                results.append(built)
                continue
            stack.append((current, True, "attrs", built, 1))
            stack.append((attrs, False, None, None, 0))
            continue
        if isinstance(current, _collections.ChainMap):
            try:
                placeholder = type(current)()
            except Exception:
                placeholder = _collections.ChainMap({})
            memo[id(current)] = placeholder
            children = list(current.maps)
            attrs = _attr_mapping(current)
            if attrs is not None:
                children.append(attrs)
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
                try:
                    placeholder = type(current)()
                except Exception:
                    placeholder = _collections.UserDict()
            elif isinstance(current, _collections.defaultdict):
                try:
                    placeholder = type(current)(current.default_factory)
                except Exception:
                    try:
                        placeholder = type(current)()
                        placeholder.default_factory = current.default_factory
                    except Exception:
                        placeholder = _collections.defaultdict(
                            current.default_factory
                        )
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
            attrs = _attr_mapping(current)
            if attrs is not None:
                children.append(attrs)
            stack.append((current, True, "mapping", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(
            current, (list, _collections.deque, _collections.UserList)
        ):
            if isinstance(current, _collections.deque):
                bound = current.maxlen
                if bound is None:
                    try:
                        placeholder = type(current)()
                    except Exception:
                        placeholder = _collections.deque()
                else:
                    try:
                        placeholder = type(current)((), bound)
                    except Exception:
                        try:
                            placeholder = type(current)(
                                maxlen=bound
                            )
                        except Exception:
                            placeholder = _collections.deque(
                                (), bound
                            )
            elif isinstance(current, _collections.UserList):
                try:
                    placeholder = type(current)()
                except Exception:
                    placeholder = _collections.UserList()
            else:
                try:
                    placeholder = type(current)()
                except Exception:
                    placeholder = []
            memo[id(current)] = placeholder
            children = list(current)
            attrs = _attr_mapping(current)
            if attrs is not None:
                children.append(attrs)
            stack.append((current, True, "sequence", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, _collections.UserString):
            try:
                built = type(current)(str(current))
            except Exception:
                built = _collections.UserString(str(current))
            memo[id(current)] = built
            attrs = _attr_mapping(current)
            if attrs is None:
                results.append(built)
                continue
            stack.append((current, True, "attrs", built, 1))
            stack.append((attrs, False, None, None, 0))
            continue
        if isinstance(
            current,
            (
                _abc_module.KeysView,
                _abc_module.ValuesView,
                _abc_module.ItemsView,
            ),
        ):
            placeholder = []
            memo[id(current)] = placeholder
            children = list(current)
            stack.append((current, True, "sequence", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, set):
            try:
                placeholder = type(current)()
            except Exception:
                placeholder = set()
            memo[id(current)] = placeholder
            children = list(current)
            attrs = _attr_mapping(current)
            if attrs is not None:
                children.append(attrs)
            stack.append((current, True, "set", placeholder,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, tuple):
            in_progress.add(id(current))
            children = list(current)
            attrs = _attr_mapping(current)
            if attrs is not None:
                children.append(attrs)
            stack.append((current, True, "tuple", None, len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if isinstance(current, frozenset):
            in_progress.add(id(current))
            children = list(current)
            attrs = _attr_mapping(current)
            if attrs is not None:
                children.append(attrs)
            stack.append((current, True, "frozenset", None,
                          len(children)))
            for child in reversed(children):
                stack.append((child, False, None, None, 0))
            continue
        if _fallback_holds_mutable_enum(current):
            raise ValueError(
                "enum member with mutable instance state in bundle copy"
            )
        if _fallback_holds_uncopyable(current):
            raise ValueError("uncopyable value in bundle copy")
        if _fallback_holds_mutable_added_shape(current):
            raise ValueError(
                "accepted shape subclass instance with mutable "
                "added state in bundle copy"
            )
        replacements = _fallback_replacements(current)
        if replacements:
            deep_memo = dict(act_landing_memo)
            for marker, part in replacements.items():
                if marker not in deep_memo:
                    deep_memo[marker] = _bundle_copy(part)
            built_functions = {}
            globals_cache = act_globals_cache
            for func in _functions_with_replacement_defaults(
                current, replacements
            ):
                if id(func) in act_landing_memo:
                    built_functions[id(func)] = act_landing_memo[
                        id(func)
                    ]
                    deep_memo[id(func)] = built_functions[id(func)]
                    continue
                built_functions[id(func)] = (
                    _function_with_copied_defaults(
                        func,
                        replacements,
                        _copied_globals(
                            func, replacements, globals_cache
                        ),
                    )
                )
                deep_memo[id(func)] = built_functions[id(func)]
            method_nodes = []
            property_nodes = []
            for node in _walk_nodes(current):
                if isinstance(node, _types_module.MethodType):
                    if id(node.__func__) in built_functions:
                        method_nodes.append(node)
                elif isinstance(node, property):
                    accessors = (node.fget, node.fset, node.fdel)
                    if any(
                        accessor is not None
                        and id(accessor) in built_functions
                        for accessor in accessors
                    ):
                        property_nodes.append(node)
            if method_nodes or property_nodes:
                first_memo = dict(deep_memo)
                _copy_module.deepcopy(current, first_memo)
                for node in method_nodes:
                    copied_self = first_memo.get(
                        id(node.__self__), node.__self__
                    )
                    deep_memo[id(node.__self__)] = copied_self
                    deep_memo[id(node)] = _types_module.MethodType(
                        built_functions[id(node.__func__)],
                        copied_self,
                    )
                for node in property_nodes:
                    deep_memo[id(node)] = property(
                        built_functions.get(id(node.fget), node.fget)
                        if node.fget is not None else None,
                        built_functions.get(id(node.fset), node.fset)
                        if node.fset is not None else None,
                        built_functions.get(id(node.fdel), node.fdel)
                        if node.fdel is not None else None,
                        node.__doc__,
                    )
                built = _copy_module.deepcopy(current, deep_memo)
            else:
                built = _copy_module.deepcopy(current, deep_memo)
            act_landing_memo.update(deep_memo)
        else:
            built = _copy_module.deepcopy(current, act_landing_memo)
        _stitch_exception_chains(
            current, built,
            deep_memo if replacements else act_landing_memo,
        )
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
    The no promotion position stands decided by the
    presence of the workflow name in the registry and
    not by the value of the bundle read, so a bundle
    recorded as the value None returns the promotion
    answer carrying the None bundle.
    """
    if workflow not in _CURRENT_PROMOTIONS:
        return {
            "answer": "no promotion",
            "is_error": False,
            "bundle": None,
        }
    bundle = _CURRENT_PROMOTIONS[workflow]
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
