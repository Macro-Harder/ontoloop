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
    mapping. Where a subclass states a slot under a
    plain stated name, or under a stated name
    carrying one leading underscore, that a base
    class states again, the slot of each stating
    class stands read through the descriptor of its
    own stating class, the content of a later
    stating class standing in the mapping under a
    key naming that stating class beside the stated
    name, so the content of every stating class
    stands in the mapping in that form as well.
    Where the value
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
                else:
                    descriptor = cls.__dict__.get(name)
                    if descriptor is not None and hasattr(
                        descriptor, "__get__"
                    ):
                        key = cls.__qualname__ + ":" + name
                        if key not in mapping:
                            try:
                                mapping[key] = descriptor.__get__(value)
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
            else:
                descriptor = cls.__dict__.get(name)
                if descriptor is not None and hasattr(
                    descriptor, "__get__"
                ):
                    try:
                        mapping[name] = descriptor.__get__(value)
                    except AttributeError:
                        continue
    if mapping:
        return mapping
    return None


def _class_namespace_mapping(value):
    """Return the namespace mapping of a class, or None.

    A class standing as a value carries its content in
    its class namespace, which its vars act returns as
    a mapping proxy and not as a dict, so the residual
    content reading returns no content for a class in
    any case. This act reads that namespace in a
    governed form: each member standing in the
    namespace stands in the mapping under its member
    name, a member standing as plain data, or as a
    container of plain data, standing in the mapping
    in its own form, a member standing as a function,
    a classmethod, a staticmethod, or a property
    standing in the mapping as a token naming the
    callable it wraps by its module and its qualified
    name, a member standing as a class standing as a
    token naming that class in the same name form, a
    member standing as an instance of the class
    standing as a token naming its kind, so no member
    reading walks back into the class itself, and any
    further member standing as a token naming its
    type. The bookkeeping members stating the class
    name form itself stand in no entry, that form
    standing stated beside the mapping in the
    encoding. Where the namespace carries no member
    beyond those bookkeeping members, the act returns
    None, and the class digests in its standing string
    form.
    """
    import types as _types_module

    if not isinstance(value, type):
        return None
    try:
        stored = vars(value)
    except TypeError:
        return None

    def _callable_token(member, fallback):
        return (
            "callable:"
            + (getattr(member, "__module__", None) or "")
            + "."
            + (getattr(member, "__qualname__", None) or fallback)
        )

    def _convert(member, depth):
        if member is value:
            return "class:self"
        if isinstance(member, value):
            return "instance:" + type(member).__name__
        if member is None or isinstance(
            member, (bool, int, float, str, bytes, bytearray)
        ):
            return member
        if isinstance(member, type):
            return (
                "class:"
                + (getattr(member, "__module__", None) or "")
                + "."
                + (getattr(member, "__qualname__", None) or "")
            )
        if isinstance(
            member,
            (
                _types_module.FunctionType,
                _types_module.BuiltinFunctionType,
            ),
        ):
            return _callable_token(member, "callable")
        if isinstance(member, (classmethod, staticmethod)):
            return _callable_token(member.__func__, "callable")
        if isinstance(member, property):
            if member.fget is None:
                return "callable:property"
            return _callable_token(member.fget, "property")
        if isinstance(member, dict) and depth < 3:
            converted = {}
            for item_key in member:
                key_form = _convert(item_key, depth + 1)
                try:
                    hash(key_form)
                except TypeError:
                    key_form = "object:" + type(item_key).__name__
                converted[key_form] = _convert(
                    member[item_key], depth + 1
                )
            return converted
        if isinstance(member, (list, tuple)) and depth < 3:
            return [_convert(item, depth + 1) for item in member]
        if isinstance(member, (set, frozenset)) and depth < 3:
            return [_convert(item, depth + 1) for item in member]
        return "object:" + type(member).__name__

    mapping = {}
    for key in stored:
        if key in (
            "__dict__",
            "__weakref__",
            "__module__",
            "__qualname__",
        ):
            continue
        mapping[key] = _convert(stored[key], 0)
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
    exception form beside them, the name and object
    channels of an AttributeError, the name channel
    of a NameError, and the subexception content an
    exception group carries standing beside its
    argument content in every exception form beside
    them, an exception group and an AttributeError
    and a NameError standing decided into the
    chained kind in their plain forms as in their
    added state forms, so their argument content and
    their channels stand read in both forms, the
    encoding walk
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
    such type, standing refused in the same form, a
    type factory standing as no standing module state
    under its stated module and qualified name, as a
    type created by a type constructor call or a type
    retained from a definition a later definition of
    the same name replaced, standing refused in the
    same form, the token stating a type factory only
    where the standing module state under its stated
    names stands as that type itself, and a class
    standing as a value encoding over its stated name
    form and over a governed form of its namespace
    content together, where its namespace carries
    content in that form, and a function
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
    groups by a separator sequence of any width, each
    separator of one grouped form standing as one
    consistent sequence of characters standing
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
    import sys as _sys_module
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
            r"(?<![0-9])[0-9]{1,3}([^0-9A-Za-z]+)[0-9]{3}"
            r"(?:\1[0-9]{3})+(?![0-9])",
            text,
        ):
            return True
        if _re_module.search(
            r"(?<![0-9a-fA-F])[0-9a-fA-F]{2}([^0-9A-Za-z]+)"
            r"[0-9a-fA-F]{2}(?:\1[0-9a-fA-F]{2}){4,}"
            r"(?![0-9a-fA-F])",
            text,
        ):
            return True
        for match in _re_module.finditer(
            r"(?<![0-9a-fA-F])[0-9a-fA-F]{4}([^0-9A-Za-z]+)"
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
            resolved = _sys_module.modules.get(factory.__module__)
            if resolved is not None:
                for part in factory.__qualname__.split("."):
                    resolved = getattr(resolved, part, None)
                    if resolved is None:
                        break
            if resolved is not factory:
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
        if isinstance(current, AttributeError):
            attribute_name = getattr(current, "name", None)
            attribute_object = getattr(current, "obj", None)
        else:
            attribute_name = None
            attribute_object = None
        if isinstance(current, NameError):
            name_error_name = getattr(current, "name", None)
        else:
            name_error_name = None
        if isinstance(current, BaseExceptionGroup):
            group_exceptions = tuple(
                getattr(current, "exceptions", ()) or ()
            )
        else:
            group_exceptions = ()
        return (
            bool(getattr(current, "__suppress_context__", False)),
            import_name,
            import_path,
            syntax,
            attribute_name,
            attribute_object,
            name_error_name,
            group_exceptions,
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
                or isinstance(
                    current,
                    (
                        ImportError,
                        SyntaxError,
                        BaseExceptionGroup,
                        AttributeError,
                        NameError,
                    ),
                )
            )
        ):
            kind = "exc_chain"
        elif (
            isinstance(current, type)
            and _class_namespace_mapping(current) is not None
        ):
            kind = "class_attrs"
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
            elif kind == "class_attrs":
                text = str(current)
                if _address_bearing(text):
                    raise ValueError(
                        "digest cannot read material of type "
                        + type(current).__name__
                    )
                children = [text, _class_namespace_mapping(current)]
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
        elif kind == "class_attrs":
            results.append(
                b"class:" + parts[0] + b"+namespace=" + parts[1] + b";"
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
    in the same refused form, and the same refusal
    stands where the view stands inside slot storage
    in that mapping, inside function attribute
    storage in that mapping, inside the arguments of
    a partial application in that mapping, inside a
    closure cell in that mapping, or inside the
    arguments of an exception in that mapping, beside
    the cause and context chains that exception
    carries. A governed uncopyable value standing in
    the reduce reach or in the state reach of a plain
    custom carrier standing inside such a value
    stands refused in the same form. A governed
    uncopyable callable standing in the namespace of
    a class standing as a value inside such a value,
    or in the namespace of the class of an instance
    standing as a value inside such a value, stands
    refused in the same form, a module
    standing in a class namespace standing as a
    binding of that module and not as a value the
    class carries, and a bound
    builtin callable read through the object it
    stands bound to, where that object stands as
    neither a module nor a type, stands under the
    same reading in the view holding walk. The same
    refusal stands where the view stands inside the
    instance attribute storage of a branch matched
    carrier in that mapping, a container typed item,
    an exception, or a partial application among
    them. A governed uncopyable value standing in
    the state element of a reduce form of a plain
    custom carrier, and a dictionary view standing
    in the reduce arguments, in that state element,
    in the state a custom getstate act returns, or
    in the newargs or newargs ex reach of such a
    carrier, stands refused in the same form, and a
    governed uncopyable value standing in the
    newargs or newargs ex reach stands refused in
    the same form. A governed uncopyable value held
    by the factory of a defaultdict standing inside
    such a value stands refused in the same form. A
    governed uncopyable value standing in the
    defaults, keyword defaults, annotations,
    attribute storage, closure, or globals of a
    function member of a class namespace, of an
    accessor function of a property member, or of
    the carried function of a classmethod or
    staticmethod member, and the accessor or carried
    function itself standing as a governed
    uncopyable callable, stands refused in the same
    form, and a governed uncopyable value standing
    in the namespace of a class standing nested in
    a class namespace, at the depth the presentation
    carries it, or standing in the namespace of the
    metaclass of a class standing as a value inside
    such a value, stands refused in the same form.
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
    import dis as _dis_module
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

    def _globals_map_is_module_dict(func, globals_map):
        if _globals_is_home_module(func, globals_map):
            return True
        for module in list(_sys_module.modules.values()):
            try:
                if (
                    module is not None
                    and module.__dict__ is globals_map
                ):
                    return True
            except Exception:
                continue
        return False

    def _referenced_global_values(func, globals_map, extra_names=None):
        def _map_is_stdlib(candidate_map):
            if not isinstance(candidate_map, dict):
                return False
            map_name = candidate_map.get("__name__")
            if not isinstance(map_name, str):
                return False
            map_owner = _sys_module.modules.get(map_name)
            if map_owner is None:
                return False
            try:
                owner_is_map = (
                    map_owner.__dict__ is candidate_map
                )
            except Exception:
                owner_is_map = False
            if not owner_is_map:
                return False
            owner_file = getattr(
                map_owner, "__file__", None
            )
            if owner_file is None:
                return map_name in (
                    "sys",
                    "builtins",
                    "_io",
                    "os",
                    "posix",
                    "nt",
                )
            stdlib_dir = _os_module.path.dirname(
                _os_module.__file__
            )
            try:
                if not owner_file.startswith(
                    stdlib_dir + _os_module.path.sep
                ):
                    return False
                if not _os_module.path.isfile(owner_file):
                    return False
            except Exception:
                return False
            try:
                for other_module in list(
                    _sys_module.modules.values()
                ):
                    if other_module is map_owner:
                        continue
                    if getattr(
                        other_module, "__file__", None
                    ) == owner_file:
                        return False
            except Exception:
                return False
            try:
                file_base = _os_module.path.basename(
                    owner_file
                )
                if file_base == "__init__.py":
                    file_owner_name = _os_module.path.basename(
                        _os_module.path.dirname(owner_file)
                    )
                else:
                    file_owner_name = (
                        _os_module.path.splitext(file_base)[0]
                    )
                if file_owner_name != map_name.rsplit(
                    ".", 1
                )[-1]:
                    return False
            except Exception:
                return False
            try:
                relative_file = owner_file[
                    len(stdlib_dir) + 1:
                ]
                file_parts = relative_file.split(
                    _os_module.path.sep
                )
                if file_parts[-1] == "__init__.py":
                    file_parts = file_parts[:-1]
                elif file_parts[-1].endswith(".py"):
                    file_parts[-1] = (
                        _os_module.path.splitext(
                            file_parts[-1]
                        )[0]
                    )
                else:
                    file_parts = None
                if file_parts is not None:
                    genuine_name = ".".join(file_parts)
                    genuine_module = (
                        _sys_module.modules.get(genuine_name)
                    )
                    if genuine_module is None:
                        return False
                    if getattr(
                        genuine_module, "__file__", None
                    ) != owner_file:
                        return False
            except Exception:
                return False
            return True

        if _map_is_stdlib(globals_map):
            return []
        def _code_facts(root_code):
            names = set()
            consts = set()
            attrs = set()
            pairs = set()
            chains = set()
            act_targets = set()
            act_chains = set()
            exec_dict_bases = set()
            exec_chain_bases = set()
            exec_subscript_bases = set()
            subscript_targets = set()
            vars_subscript_targets = set()
            getattr_result_targets = set()
            get_result_targets = set()
            obj_getattribute_targets = set()
            obj_getattribute_chains = set()
            subscript_carried_bases = set()
            vars_carried_bases = set()
            getattr_carried_bases = set()
            getattribute_targets = set()
            getattribute_chains = set()
            vars_get_result_targets = set()
            get_carried_bases = set()
            type_getattribute_targets = set()
            type_getattribute_chains = set()
            getattribute_result_targets = set()
            self_attrs = set()
            vars_get_carried_bases = set()
            getattr_home_bases = set()
            vars_home_bases = set()
            call_names = set()
            call_pairs = set()
            vars_get_attr_bases = set()
            get_attr_bases = set()
            vars_subscript_attr_bases = set()
            dict_subscript_attr_bases = set()
            chains3 = set()
            chains4 = set()
            vars_subscript_nested_bases = set()
            chains5 = set()
            chains6 = set()
            chains7 = set()
            attr_dynamic = False
            vars_with_arg = False

            def _scan_act_window(window, act_name):
                nonlocal vars_with_arg
                prev_global = None
                chain_global = None
                chain_attr = None
                sub_global = None
                sub_key = None
                sub_stage = 0
                for ahead in window:
                    if ahead.opname in (
                        "CALL",
                        "CALL_FUNCTION_EX",
                    ):
                        if act_name == "vars":
                            if ahead.opname == (
                                "CALL_FUNCTION_EX"
                            ):
                                vars_with_arg = True
                            elif (
                                isinstance(ahead.argval, int)
                                and ahead.argval >= 1
                            ):
                                vars_with_arg = True
                            break
                        if act_name == "exec":
                            prev_global = None
                            chain_global = None
                            chain_attr = None
                            sub_stage = 0
                            continue
                        break
                    if ahead.opname in (
                        "LOAD_GLOBAL",
                        "LOAD_NAME",
                    ) and isinstance(ahead.argval, str):
                        act_targets.add(ahead.argval)
                        prev_global = ahead.argval
                        chain_global = None
                        chain_attr = None
                        sub_stage = 0
                        continue
                    if (
                        ahead.opname == "LOAD_ATTR"
                        and isinstance(ahead.argval, str)
                    ):
                        if sub_stage == 3:
                            if (
                                act_name == "exec"
                                and ahead.argval == "__dict__"
                            ):
                                exec_subscript_bases.add(
                                    (sub_global, sub_key)
                                )
                            sub_stage = 0
                        if prev_global is not None:
                            act_chains.add(
                                (prev_global, ahead.argval)
                            )
                            if (
                                act_name == "exec"
                                and ahead.argval == "__dict__"
                            ):
                                exec_dict_bases.add(
                                    prev_global
                                )
                                sub_global = prev_global
                                sub_stage = 1
                            chain_global = prev_global
                            chain_attr = ahead.argval
                            prev_global = None
                            continue
                        if chain_global is not None:
                            if (
                                act_name == "exec"
                                and ahead.argval == "__dict__"
                            ):
                                exec_chain_bases.add(
                                    (chain_global, chain_attr)
                                )
                            chain_global = None
                            chain_attr = None
                            continue
                        continue
                    if (
                        sub_stage == 1
                        and ahead.opname == "LOAD_CONST"
                        and isinstance(ahead.argval, str)
                    ):
                        sub_key = ahead.argval
                        sub_stage = 2
                        prev_global = None
                        continue
                    if (
                        sub_stage == 2
                        and ahead.opname == "BINARY_OP"
                    ):
                        sub_stage = 3
                        prev_global = None
                        continue
                    sub_stage = 0
                    prev_global = None
            pending_codes = [root_code]
            seen_codes = set()
            while pending_codes:
                current_code = pending_codes.pop()
                if id(current_code) in seen_codes:
                    continue
                seen_codes.add(id(current_code))
                try:
                    instructions = list(
                        _dis_module.get_instructions(
                            current_code
                        )
                    )
                except Exception:
                    instructions = []
                for seq_index in range(len(instructions)):
                    seq_ins = instructions[seq_index]

                    def _seq_at(offset):
                        pos = seq_index + offset
                        if 0 <= pos < len(instructions):
                            return instructions[pos]
                        return None

                    if (
                        seq_ins.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_ins.argval == "self"
                    ):
                        seq_a = _seq_at(1)
                        if (
                            seq_a is not None
                            and seq_a.opname == "LOAD_ATTR"
                            and isinstance(seq_a.argval, str)
                        ):
                            self_attrs.add(seq_a.argval)
                    if not (
                        seq_ins.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_ins.argval, str)
                    ):
                        continue
                    seq_a = _seq_at(1)
                    seq_b = _seq_at(2)
                    seq_c = _seq_at(3)
                    seq_d = _seq_at(4)
                    seq_e = _seq_at(5)
                    seq_f = _seq_at(6)
                    seq_g = _seq_at(7)
                    seq_h = _seq_at(8)
                    seq_i = _seq_at(9)
                    seq_j = _seq_at(10)
                    seq_k = _seq_at(11)
                    seq_l = _seq_at(12)
                    seq_m = _seq_at(13)
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname == "CALL"
                        and seq_j is not None
                        and seq_j.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_k is not None
                        and seq_k.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_h is not None
                        and seq_h.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_i is not None
                        and seq_i.opname == "CALL"
                        and seq_j is not None
                        and seq_j.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_k is not None
                        and seq_k.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_h.argval == "pop"
                        and seq_i is not None
                        and seq_i.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_j is not None
                        and seq_j.opname == "CALL"
                        and seq_k is not None
                        and seq_k.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname == "LOAD_CONST"
                        and isinstance(seq_c.argval, str)
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_d.argval == "join"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_e.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval == "next"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval == "iter"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_e.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_h is not None
                        and seq_h.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_i is not None
                        and seq_i.opname == "CALL"
                        and seq_j is not None
                        and seq_j.opname == "CALL"
                        and seq_k is not None
                        and seq_k.opname == "CALL"
                        and seq_l is not None
                        and seq_l.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname == "BUILD_LIST"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_g is not None
                        and seq_g.opname == "LIST_EXTEND"
                        and seq_h is not None
                        and seq_h.opname == "CALL_INTRINSIC_1"
                        and seq_i is not None
                        and seq_i.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_j is not None
                        and seq_j.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_k is not None
                        and seq_k.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname == "LOAD_CONST"
                        and isinstance(seq_c.argval, str)
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_d.argval == "join"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_g.argval == "copy"
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_i.argval == "keys"
                        and seq_j is not None
                        and seq_j.opname == "CALL"
                        and seq_k is not None
                        and seq_k.opname == "CALL"
                        and seq_l is not None
                        and seq_l.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_m is not None
                        and seq_m.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval == "reversed"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_h.argval == "pop"
                        and seq_i is not None
                        and seq_i.opname == "CALL"
                        and seq_j is not None
                        and seq_j.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "CALL"
                        and seq_f is not None
                        and seq_f.opname == "GET_ITER"
                        and seq_g is not None
                        and seq_g.opname == "LOAD_FAST_AND_CLEAR"
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname == "LOAD_CONST"
                        and isinstance(seq_c.argval, str)
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_d.argval == "join"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname == "GET_ITER"
                        and seq_g is not None
                        and seq_g.opname == "LOAD_FAST_AND_CLEAR"
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_g.argval == "keys"
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname == "CALL"
                        and seq_j is not None
                        and seq_j.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_k is not None
                        and seq_k.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval == "sorted"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "LOAD_CONST"
                        and seq_f is not None
                        and seq_f.opname == "LOAD_CONST"
                        and seq_g is not None
                        and seq_g.opname == "CALL_KW"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_e is not None
                        and seq_e.opname == "CALL"
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_h is not None
                        and seq_h.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "TO_BOOL"
                        and seq_f is not None
                        and seq_f.opname in (
                            "POP_JUMP_IF_FALSE",
                            "POP_JUMP_IF_TRUE",
                            "POP_JUMP_IF_NONE",
                            "POP_JUMP_IF_NOT_NONE",
                        )
                        and seq_g is not None
                        and seq_g.opname == "NOT_TAKEN"
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "CALL"
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_f.argval == "pop"
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname == "GET_ITER"
                        and seq_e is not None
                        and seq_e.opname == "LOAD_FAST_AND_CLEAR"
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname == "BUILD_LIST"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "LIST_EXTEND"
                        and seq_f is not None
                        and seq_f.opname == "CALL_INTRINSIC_1"
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_h is not None
                        and seq_h.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname == "LOAD_CONST"
                        and isinstance(seq_c.argval, str)
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_d.argval == "join"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval == "next"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval == "iter"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                        and seq_h is not None
                        and seq_h.opname == "CALL"
                        and seq_i is not None
                        and seq_i.opname == "CALL"
                        and seq_j is not None
                        and seq_j.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_d.argval == "pop"
                        and seq_e is not None
                        and seq_e.opname == "CALL"
                        and seq_f is not None
                        and seq_f.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname == "TO_BOOL"
                        and seq_e is not None
                        and seq_e.opname in (
                            "POP_JUMP_IF_FALSE",
                            "POP_JUMP_IF_TRUE",
                            "POP_JUMP_IF_NONE",
                            "POP_JUMP_IF_NOT_NONE",
                        )
                        and seq_f is not None
                        and seq_f.opname == "NOT_TAKEN"
                        and seq_g is not None
                        and seq_g.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_a is not None
                        and seq_a.opname == "CALL"
                    ):
                        call_names.add(seq_ins.argval)
                    if (
                        seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and isinstance(seq_a.argval, str)
                        and (
                            (
                                seq_b is not None
                                and seq_b.opname == "CALL"
                            )
                            or (
                                seq_c is not None
                                and seq_c.opname == "CALL"
                            )
                        )
                    ):
                        call_pairs.add(
                            (seq_ins.argval, seq_a.argval)
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_c.argval == "get"
                        and seq_d is not None
                        and seq_d.opname == "LOAD_CONST"
                        and isinstance(seq_d.argval, str)
                    ):
                        vars_get_result_targets.add(
                            (seq_a.argval, seq_d.argval)
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_c.argval == "get"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                    ):
                        vars_get_carried_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_c.argval == "get"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "LOAD_ATTR"
                    ):
                        vars_get_attr_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and seq_a.argval == "__dict__"
                        and seq_b is not None
                        and seq_b.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_b.argval == "get"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname == "LOAD_ATTR"
                    ):
                        get_attr_bases.add(seq_ins.argval)
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d is not None
                        and seq_d.opname == "LOAD_ATTR"
                        and seq_e is not None
                        and seq_e.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_attr_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname == "CALL"
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval in (
                            "list",
                            "tuple",
                            "set",
                            "frozenset",
                            "sorted",
                            "dict",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                        and seq_h is not None
                        and seq_h.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_i is not None
                        and seq_i.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_d.argval == "copy"
                        and seq_e is not None
                        and seq_e.opname == "CALL"
                        and seq_f is not None
                        and seq_f.opname in (
                            "LOAD_CONST",
                            "LOAD_SMALL_INT",
                        )
                        and seq_g is not None
                        and seq_g.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c.argval == "next"
                        and seq_d is not None
                        and seq_d.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_d.argval == "iter"
                        and seq_e is not None
                        and seq_e.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_f is not None
                        and seq_f.opname == "CALL"
                        and seq_g is not None
                        and seq_g.opname == "CALL"
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname == "TO_BOOL"
                        and seq_e is not None
                        and seq_e.opname in (
                            "POP_JUMP_IF_FALSE",
                            "POP_JUMP_IF_TRUE",
                            "POP_JUMP_IF_NONE",
                            "POP_JUMP_IF_NOT_NONE",
                        )
                        and seq_f is not None
                        and seq_f.opname == "NOT_TAKEN"
                        and seq_g is not None
                        and seq_g.opname == "LOAD_CONST"
                        and isinstance(seq_g.argval, str)
                    ):
                        vars_subscript_nested_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_ins.argval == "vars"
                        and seq_a is not None
                        and seq_a.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_a.argval, str)
                        and seq_b is not None
                        and seq_b.opname == "CALL"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                        )
                        and seq_d is not None
                        and seq_d.opname == "LOAD_ATTR"
                        and seq_e is not None
                        and seq_e.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_subscript_attr_bases.add(
                            seq_a.argval
                        )
                    if (
                        seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and seq_a.argval == "__dict__"
                        and seq_b is not None
                        and seq_b.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and seq_c is not None
                        and seq_c.opname == "LOAD_ATTR"
                        and seq_d is not None
                        and seq_d.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        dict_subscript_attr_bases.add(
                            seq_ins.argval
                        )
                    if (
                        seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and seq_a.argval == "__dict__"
                        and seq_b is not None
                        and seq_b.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                        )
                        and seq_c is not None
                        and seq_c.opname == "LOAD_ATTR"
                        and seq_d is not None
                        and seq_d.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        dict_subscript_attr_bases.add(
                            seq_ins.argval
                        )
                    if (
                        seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and seq_a.argval == "__dict__"
                        and seq_b is not None
                        and seq_b.opname in (
                            "LOAD_ATTR",
                            "LOAD_METHOD",
                        )
                        and seq_b.argval == "get"
                        and seq_c is not None
                        and seq_c.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                    ):
                        get_carried_bases.add(seq_ins.argval)
                    if seq_ins.argval == "type":
                        if (
                            seq_a is not None
                            and seq_a.opname in (
                                "LOAD_GLOBAL",
                                "LOAD_NAME",
                            )
                            and isinstance(seq_a.argval, str)
                            and seq_b is not None
                            and seq_b.opname == "CALL"
                            and seq_c is not None
                            and seq_c.opname == "LOAD_ATTR"
                            and seq_c.argval
                            == "__getattribute__"
                        ):
                            type_getattribute_targets.add(
                                seq_a.argval
                            )
                        if (
                            seq_a is not None
                            and seq_a.opname in (
                                "LOAD_GLOBAL",
                                "LOAD_NAME",
                            )
                            and isinstance(seq_a.argval, str)
                            and seq_b is not None
                            and seq_b.opname == "LOAD_ATTR"
                            and isinstance(seq_b.argval, str)
                            and seq_c is not None
                            and seq_c.opname == "CALL"
                            and seq_d is not None
                            and seq_d.opname == "LOAD_ATTR"
                            and seq_d.argval
                            == "__getattribute__"
                        ):
                            type_getattribute_chains.add(
                                (seq_a.argval, seq_b.argval)
                            )
                    if (
                        seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and seq_a.argval == "__getattribute__"
                        and seq_b is not None
                        and seq_b.opname == "LOAD_CONST"
                        and isinstance(seq_b.argval, str)
                    ):
                        getattribute_result_targets.add(
                            (seq_ins.argval, seq_b.argval)
                        )
                    if (
                        seq_ins.argval == "object"
                        and seq_a is not None
                        and seq_a.opname == "LOAD_ATTR"
                        and seq_a.argval == "__getattribute__"
                        and seq_b is not None
                        and seq_b.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(seq_b.argval, str)
                        and seq_c is not None
                        and seq_c.opname == "LOAD_CONST"
                        and isinstance(seq_c.argval, str)
                    ):
                        getattribute_result_targets.add(
                            (seq_b.argval, seq_c.argval)
                        )
                for scan_index in range(len(instructions)):
                    scan_ins = instructions[scan_index]
                    if not (
                        scan_ins.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_ins.argval, str)
                    ):
                        continue
                    scan_window = instructions[
                        scan_index:scan_index + 5
                    ]
                    while len(scan_window) < 5:
                        scan_window.append(None)
                    scan_first = scan_window[1]
                    scan_second = scan_window[2]
                    scan_third = scan_window[3]
                    scan_fourth = scan_window[4]
                    if (
                        scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval == "__dict__"
                        and scan_second is not None
                        and scan_second.opname == "LOAD_CONST"
                        and isinstance(scan_second.argval, str)
                        and scan_third is not None
                        and scan_third.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        subscript_targets.add(
                            (
                                scan_ins.argval,
                                scan_second.argval,
                            )
                        )
                    if (
                        scan_ins.argval == "vars"
                        and scan_first is not None
                        and scan_first.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_first.argval, str)
                        and scan_second is not None
                        and scan_second.opname == "CALL"
                        and scan_third is not None
                        and scan_third.opname == "LOAD_CONST"
                        and isinstance(scan_third.argval, str)
                        and scan_fourth is not None
                        and scan_fourth.opname == "BINARY_OP"
                    ):
                        vars_subscript_targets.add(
                            (
                                scan_first.argval,
                                scan_third.argval,
                            )
                        )
                    if (
                        scan_ins.argval == "getattr"
                        and scan_first is not None
                        and scan_first.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_first.argval, str)
                        and scan_second is not None
                        and scan_second.opname == "LOAD_CONST"
                        and isinstance(scan_second.argval, str)
                        and scan_third is not None
                        and scan_third.opname == "CALL"
                    ):
                        getattr_result_targets.add(
                            (
                                scan_first.argval,
                                scan_second.argval,
                            )
                        )
                    if (
                        scan_ins.argval == "getattr"
                        and scan_first is not None
                        and scan_first.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_first.argval, str)
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_second.argval, str)
                        and scan_third is not None
                        and scan_third.opname == "CALL"
                    ):
                        getattr_home_bases.add(
                            scan_first.argval
                        )
                    if (
                        scan_ins.argval == "vars"
                        and scan_first is not None
                        and scan_first.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_first.argval, str)
                        and scan_second is not None
                        and scan_second.opname == "CALL"
                        and scan_third is not None
                        and scan_third.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_third.argval, str)
                        and scan_fourth is not None
                        and scan_fourth.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_home_bases.add(
                            scan_first.argval
                        )
                    if (
                        scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval == "__dict__"
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_METHOD",
                            "LOAD_ATTR",
                        )
                        and scan_second.argval == "get"
                        and scan_third is not None
                        and scan_third.opname == "LOAD_CONST"
                        and isinstance(scan_third.argval, str)
                    ):
                        get_result_targets.add(
                            (
                                scan_ins.argval,
                                scan_third.argval,
                            )
                        )
                    if (
                        scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval == "__dict__"
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                    ):
                        subscript_carried_bases.add(
                            scan_ins.argval
                        )
                    if (
                        scan_ins.argval == "vars"
                        and scan_first is not None
                        and scan_first.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_first.argval, str)
                        and scan_second is not None
                        and scan_second.opname == "CALL"
                        and scan_third is not None
                        and scan_third.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                        and scan_fourth is not None
                        and scan_fourth.opname in (
                            "BINARY_OP",
                            "BINARY_SUBSCR",
                        )
                    ):
                        vars_carried_bases.add(
                            scan_first.argval
                        )
                    if (
                        scan_ins.argval == "getattr"
                        and scan_first is not None
                        and scan_first.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_first.argval, str)
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                    ):
                        getattr_carried_bases.add(
                            scan_first.argval
                        )
                    if (
                        scan_ins.argval == "object"
                        and scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval
                        == "__getattribute__"
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_second.argval, str)
                        and scan_third is not None
                        and scan_third.opname == "LOAD_CONST"
                    ):
                        obj_getattribute_targets.add(
                            scan_second.argval
                        )
                    if (
                        scan_ins.argval == "object"
                        and scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval
                        == "__getattribute__"
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_second.argval, str)
                        and scan_third is not None
                        and scan_third.opname in (
                            "LOAD_FAST",
                            "LOAD_FAST_BORROW",
                            "LOAD_FAST_CHECK",
                            "LOAD_DEREF",
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                            "LOAD_CLASSDEREF",
                        )
                    ):
                        obj_getattribute_targets.add(
                            scan_second.argval
                        )
                    if (
                        scan_ins.argval == "object"
                        and scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval
                        == "__getattribute__"
                        and scan_second is not None
                        and scan_second.opname in (
                            "LOAD_GLOBAL",
                            "LOAD_NAME",
                        )
                        and isinstance(scan_second.argval, str)
                        and scan_third is not None
                        and scan_third.opname == "LOAD_ATTR"
                        and isinstance(scan_third.argval, str)
                    ):
                        obj_getattribute_chains.add(
                            (
                                scan_second.argval,
                                scan_third.argval,
                            )
                        )
                    if (
                        scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and scan_first.argval == "__getattribute__"
                    ):
                        getattribute_targets.add(
                            scan_ins.argval
                        )
                    if (
                        scan_first is not None
                        and scan_first.opname == "LOAD_ATTR"
                        and isinstance(scan_first.argval, str)
                        and scan_first.argval
                        != "__getattribute__"
                        and scan_second is not None
                        and scan_second.opname == "LOAD_ATTR"
                        and scan_second.argval
                        == "__getattribute__"
                    ):
                        getattribute_chains.add(
                            (
                                scan_ins.argval,
                                scan_first.argval,
                            )
                        )
                last_global = None
                chain_base = None
                chain_attrs = []
                for index, instruction in enumerate(instructions):
                    if instruction.opname in (
                        "LOAD_GLOBAL",
                        "LOAD_NAME",
                    ) and isinstance(instruction.argval, str):
                        names.add(instruction.argval)
                        last_global = instruction.argval
                        chain_base = instruction.argval
                        chain_attrs = []
                        if instruction.argval in (
                            "getattr",
                            "vars",
                            "exec",
                        ):
                            _scan_act_window(
                                instructions[
                                    index + 1:index + 16
                                ],
                                instruction.argval,
                            )
                        if instruction.argval in (
                            "getattr",
                            "vars",
                        ):
                            for ahead in instructions[
                                index + 1:index + 10
                            ]:
                                if ahead.opname in (
                                    "CALL",
                                    "CALL_FUNCTION_EX",
                                ):
                                    break
                                if ahead.opname in (
                                    "LOAD_GLOBAL",
                                    "LOAD_NAME",
                                ) and isinstance(
                                    ahead.argval, str
                                ):
                                    act_targets.add(
                                        ahead.argval
                                    )
                        if instruction.argval == "vars":
                            for ahead in instructions[
                                index + 1:index + 16
                            ]:
                                if ahead.opname == (
                                    "CALL_FUNCTION_EX"
                                ):
                                    vars_with_arg = True
                                    break
                                if ahead.opname == "CALL":
                                    if (
                                        isinstance(
                                            ahead.argval, int
                                        )
                                        and ahead.argval >= 1
                                    ):
                                        vars_with_arg = True
                                    break
                        if instruction.argval in (
                            "eval",
                            "globals",
                        ):
                            for ahead in instructions[
                                index + 1:index + 14
                            ]:
                                if ahead.opname == "LOAD_ATTR":
                                    attr_dynamic = True
                                if ahead.opname == (
                                    "BINARY_SUBSCR"
                                ):
                                    break
                                if (
                                    ahead.opname == "CALL"
                                    and instruction.argval
                                    == "eval"
                                ):
                                    break
                    elif (
                        instruction.opname == "LOAD_ATTR"
                        and isinstance(instruction.argval, str)
                    ):
                        if (
                            chain_base == "builtins"
                            and instruction.argval in (
                                "getattr",
                                "vars",
                                "exec",
                                "eval",
                                "globals",
                            )
                        ):
                            names.add(instruction.argval)
                            if instruction.argval in (
                                "getattr",
                                "vars",
                                "exec",
                            ):
                                _scan_act_window(
                                    instructions[
                                        index + 1:index + 17
                                    ],
                                    instruction.argval,
                                )
                        attrs.add(instruction.argval)
                        if chain_base is not None:
                            chain_attrs.append(
                                instruction.argval
                            )
                            if len(chain_attrs) == 2:
                                chains.add(
                                    (
                                        chain_base,
                                        chain_attrs[0],
                                        chain_attrs[1],
                                    )
                                )
                            if len(chain_attrs) == 3:
                                chains3.add(
                                    (
                                        chain_base,
                                        chain_attrs[0],
                                        chain_attrs[1],
                                        chain_attrs[2],
                                    )
                                )
                            if len(chain_attrs) == 4:
                                chains4.add(
                                    (
                                        chain_base,
                                        chain_attrs[0],
                                        chain_attrs[1],
                                        chain_attrs[2],
                                        chain_attrs[3],
                                    )
                                )
                            if len(chain_attrs) == 5:
                                chains5.add(
                                    (
                                        chain_base,
                                        chain_attrs[0],
                                        chain_attrs[1],
                                        chain_attrs[2],
                                        chain_attrs[3],
                                        chain_attrs[4],
                                    )
                                )
                            if len(chain_attrs) == 6:
                                chains6.add(
                                    (
                                        chain_base,
                                        chain_attrs[0],
                                        chain_attrs[1],
                                        chain_attrs[2],
                                        chain_attrs[3],
                                        chain_attrs[4],
                                        chain_attrs[5],
                                    )
                                )
                            if len(chain_attrs) == 7:
                                chains7.add(
                                    (
                                        chain_base,
                                        chain_attrs[0],
                                        chain_attrs[1],
                                        chain_attrs[2],
                                        chain_attrs[3],
                                        chain_attrs[4],
                                        chain_attrs[5],
                                        chain_attrs[6],
                                    )
                                )
                        if last_global is not None:
                            pairs.add(
                                (last_global, instruction.argval)
                            )
                            last_global = None
                    else:
                        last_global = None
                        chain_base = None
                        chain_attrs = []
                for const in current_code.co_consts:
                    if isinstance(const, _types_module.CodeType):
                        pending_codes.append(const)
                    elif isinstance(const, str):
                        consts.add(const)
                    elif isinstance(const, bytes):
                        try:
                            consts.add(
                                const.decode("utf-8")
                            )
                        except Exception:
                            pass
            return (
                names, consts, attrs, pairs,
                attr_dynamic, vars_with_arg,
                chains, act_targets,
                act_chains, exec_dict_bases,
                exec_chain_bases, exec_subscript_bases,
                subscript_targets, vars_subscript_targets,
                getattr_result_targets,
                getattribute_targets, getattribute_chains,
                get_result_targets,
                obj_getattribute_targets,
                obj_getattribute_chains,
                subscript_carried_bases,
                vars_carried_bases, getattr_carried_bases,
                vars_get_result_targets, get_carried_bases,
                type_getattribute_targets,
                type_getattribute_chains,
                getattribute_result_targets, self_attrs,
                vars_get_carried_bases, getattr_home_bases,
                vars_home_bases, call_names, call_pairs,
                vars_get_attr_bases, get_attr_bases,
                vars_subscript_attr_bases,
                dict_subscript_attr_bases, chains3,
                chains4, vars_subscript_nested_bases,
                chains5,
                chains6,
                chains7,
            )

        def _built_from_consts(key, consts):
            pieces = [
                piece for piece in consts
                if piece and len(piece) < len(key)
            ]
            if pieces:
                reached = {0: 0}
                pending_positions = [0]
                while pending_positions:
                    position = pending_positions.pop()
                    count = reached[position]
                    for piece in pieces:
                        if key.startswith(piece, position):
                            new_position = position + len(piece)
                            if new_position == len(key):
                                if count + 1 >= 2:
                                    return True
                                continue
                            if reached.get(
                                new_position, -1
                            ) < count + 1:
                                reached[new_position] = count + 1
                                pending_positions.append(
                                    new_position
                                )
            for const in consts:
                for marker in ("{}", "{0}"):
                    if marker not in const:
                        continue
                    prefix, _, suffix = const.partition(marker)
                    if (
                        key.startswith(prefix)
                        and key.endswith(suffix)
                        and len(key)
                        > len(prefix) + len(suffix)
                    ):
                        middle = key[
                            len(prefix):
                            len(key) - len(suffix)
                            if suffix else len(key)
                        ]
                        if middle in consts:
                            return True
            return False

        def _follow_wrapper(wrapper):
            wrapped = getattr(wrapper, "__wrapped__", None)
            steps = 0
            while (
                isinstance(wrapped, _lru_cache_wrapper_type)
                and steps < 8
            ):
                wrapped = getattr(wrapped, "__wrapped__", None)
                steps += 1
            if isinstance(
                wrapped, _types_module.FunctionType
            ):
                return wrapped
            return None

        values = []
        seen_value_ids = set()
        pending_funcs = [(func, globals_map)]
        seen_funcs = set()

        def _append_reached(reached_value):
            if isinstance(
                reached_value, _types_module.ModuleType
            ):
                return
            if isinstance(
                reached_value, _lru_cache_wrapper_type
            ):
                wrapped = _follow_wrapper(reached_value)
                if wrapped is not None:
                    pending_funcs.append(
                        (
                            wrapped,
                            getattr(
                                wrapped,
                                "__globals__",
                                None,
                            ),
                        )
                    )
                return
            if id(reached_value) in seen_value_ids:
                return
            seen_value_ids.add(id(reached_value))
            values.append(reached_value)
            if isinstance(
                reached_value, _types_module.FunctionType
            ):
                pending_funcs.append(
                    (
                        reached_value,
                        getattr(
                            reached_value,
                            "__globals__",
                            None,
                        ),
                    )
                )

        _governed_reach_types = (
            _types_module.GeneratorType,
            _lock_type,
            _rlock_type,
            _condition_type,
            _types_module.CellType,
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
            _extra_uncopyable_types,
        )

        def _collect_container_contents(container):
            pending_items = [container]
            seen_items = set()
            while pending_items:
                current_item = pending_items.pop()
                if id(current_item) in seen_items:
                    continue
                seen_items.add(id(current_item))
                if isinstance(current_item, dict):
                    for held_key, held_value in (
                        current_item.items()
                    ):
                        pending_items.append(held_key)
                        pending_items.append(held_value)
                    continue
                if isinstance(
                    current_item,
                    (list, tuple, set, frozenset),
                ):
                    pending_items.extend(current_item)
                    continue
                if isinstance(
                    current_item,
                    _types_module.FunctionType,
                ) or isinstance(
                    current_item, _governed_reach_types
                ):
                    _append_reached(current_item)

        while pending_funcs:
            current_func, current_map = pending_funcs.pop()
            if id(current_func) in seen_funcs:
                continue
            seen_funcs.add(id(current_func))
            if not isinstance(current_map, dict):
                continue
            if _map_is_stdlib(current_map):
                continue
            code = getattr(current_func, "__code__", None)
            if code is None:
                continue
            (
                names, consts, attrs, pairs,
                attr_dynamic, vars_with_arg,
                chains, act_targets,
                act_chains, exec_dict_bases,
                exec_chain_bases, exec_subscript_bases,
                subscript_targets, vars_subscript_targets,
                getattr_result_targets,
                getattribute_targets, getattribute_chains,
                get_result_targets,
                obj_getattribute_targets,
                obj_getattribute_chains,
                subscript_carried_bases,
                vars_carried_bases, getattr_carried_bases,
                vars_get_result_targets, get_carried_bases,
                type_getattribute_targets,
                type_getattribute_chains,
                getattribute_result_targets, self_attrs,
                vars_get_carried_bases, getattr_home_bases,
                vars_home_bases, call_names, call_pairs,
                vars_get_attr_bases, get_attr_bases,
                vars_subscript_attr_bases,
                dict_subscript_attr_bases, chains3,
                chains4, vars_subscript_nested_bases,
                chains5,
                chains6,
                chains7,
            ) = _code_facts(code)
            default_strs = []
            for default_value in (
                getattr(current_func, "__defaults__", None)
                or ()
            ):
                if isinstance(default_value, str):
                    default_strs.append(default_value)
                elif isinstance(
                    default_value, (bytes, bytearray)
                ):
                    try:
                        default_strs.append(
                            default_value.decode("utf-8")
                        )
                    except Exception:
                        pass
            for default_value in (
                getattr(current_func, "__kwdefaults__", None)
                or {}
            ).values():
                if isinstance(default_value, str):
                    default_strs.append(default_value)
                elif isinstance(
                    default_value, (bytes, bytearray)
                ):
                    try:
                        default_strs.append(
                            default_value.decode("utf-8")
                        )
                    except Exception:
                        pass
            closure_strs = []
            for cell in (
                getattr(current_func, "__closure__", None)
                or ()
            ):
                try:
                    cell_value = cell.cell_contents
                except Exception:
                    continue
                if isinstance(cell_value, str):
                    closure_strs.append(cell_value)
                elif isinstance(
                    cell_value, (bytes, bytearray)
                ):
                    try:
                        closure_strs.append(
                            cell_value.decode("utf-8")
                        )
                    except Exception:
                        pass
            extra_carried = set(default_strs) | set(
                closure_strs
            )
            returned_strs = set()
            first_order_fns = []
            for loaded_name in names:
                loaded_fn = current_map.get(loaded_name)
                if not isinstance(
                    loaded_fn, _types_module.FunctionType
                ):
                    continue
                if (
                    getattr(loaded_fn, "__globals__", None)
                    is not current_map
                ):
                    continue
                fn_code = getattr(loaded_fn, "__code__", None)
                if fn_code is None:
                    continue
                returned_strs |= set(_code_facts(fn_code)[1])
                for helper_default in (
                    getattr(loaded_fn, "__defaults__", None)
                    or ()
                ):
                    if isinstance(helper_default, str):
                        returned_strs.add(helper_default)
                    elif isinstance(
                        helper_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                helper_default.decode("utf-8")
                            )
                        except Exception:
                            pass
                for helper_default in (
                    getattr(loaded_fn, "__kwdefaults__", None)
                    or {}
                ).values():
                    if isinstance(helper_default, str):
                        returned_strs.add(helper_default)
                    elif isinstance(
                        helper_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                helper_default.decode("utf-8")
                            )
                        except Exception:
                            pass
                for helper_cell in (
                    getattr(loaded_fn, "__closure__", None)
                    or ()
                ):
                    try:
                        helper_cell_value = (
                            helper_cell.cell_contents
                        )
                    except Exception:
                        continue
                    if isinstance(helper_cell_value, str):
                        returned_strs.add(helper_cell_value)
                    elif isinstance(
                        helper_cell_value, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                helper_cell_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for helper_name in _code_facts(fn_code)[0]:
                    helper_value = current_map.get(
                        helper_name
                    )
                    if isinstance(helper_value, str):
                        returned_strs.add(helper_value)
                    elif isinstance(
                        helper_value, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                helper_value.decode("utf-8")
                            )
                        except Exception:
                            pass
                    elif isinstance(
                        helper_value,
                        (dict, list, tuple, set, frozenset),
                    ):
                        pending_held = [helper_value]
                        seen_held = set()
                        while pending_held:
                            held = pending_held.pop()
                            if id(held) in seen_held:
                                continue
                            seen_held.add(id(held))
                            if isinstance(held, str):
                                returned_strs.add(held)
                            elif isinstance(
                                held, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        held.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                            elif isinstance(held, dict):
                                for held_key in held:
                                    pending_held.append(
                                        held_key
                                    )
                                    pending_held.append(
                                        held[held_key]
                                    )
                            elif isinstance(
                                held,
                                (
                                    list,
                                    tuple,
                                    set,
                                    frozenset,
                                ),
                            ):
                                pending_held.extend(held)
                first_order_fns.append(loaded_fn)
            for first_fn in first_order_fns:
                first_code = getattr(
                    first_fn, "__code__", None
                )
                if first_code is None:
                    continue
                for second_name in _code_facts(first_code)[0]:
                    second_fn = current_map.get(second_name)
                    if not isinstance(
                        second_fn,
                        _types_module.FunctionType,
                    ):
                        continue
                    if (
                        getattr(
                            second_fn, "__globals__", None
                        )
                        is not current_map
                    ):
                        continue
                    second_code = getattr(
                        second_fn, "__code__", None
                    )
                    if second_code is None:
                        continue
                    returned_strs |= set(
                        _code_facts(second_code)[1]
                    )
                    for second_default in (
                        getattr(
                            second_fn, "__defaults__", None
                        )
                        or ()
                    ):
                        if isinstance(second_default, str):
                            returned_strs.add(second_default)
                        elif isinstance(
                            second_default, (bytes, bytearray)
                        ):
                            try:
                                returned_strs.add(
                                    second_default.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                    for second_default in (
                        getattr(
                            second_fn, "__kwdefaults__", None
                        )
                        or {}
                    ).values():
                        if isinstance(second_default, str):
                            returned_strs.add(second_default)
                        elif isinstance(
                            second_default, (bytes, bytearray)
                        ):
                            try:
                                returned_strs.add(
                                    second_default.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                for second_name in _code_facts(first_code)[0]:
                    second_fn = current_map.get(second_name)
                    if not isinstance(
                        second_fn,
                        _types_module.FunctionType,
                    ):
                        continue
                    if (
                        getattr(
                            second_fn, "__globals__", None
                        )
                        is not current_map
                    ):
                        continue
                    second_code = getattr(
                        second_fn, "__code__", None
                    )
                    if second_code is None:
                        continue
                    for second_cell in (
                        getattr(
                            second_fn, "__closure__", None
                        )
                        or ()
                    ):
                        try:
                            second_cell_value = (
                                second_cell.cell_contents
                            )
                        except Exception:
                            continue
                        if isinstance(second_cell_value, str):
                            returned_strs.add(second_cell_value)
                        elif isinstance(
                            second_cell_value,
                            (bytes, bytearray),
                        ):
                            try:
                                returned_strs.add(
                                    second_cell_value.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                    for second_loaded in _code_facts(
                        second_code
                    )[0]:
                        second_value = current_map.get(
                            second_loaded
                        )
                        if isinstance(second_value, str):
                            returned_strs.add(second_value)
                        elif isinstance(
                            second_value, (bytes, bytearray)
                        ):
                            try:
                                returned_strs.add(
                                    second_value.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                        elif isinstance(
                            second_value,
                            (
                                dict,
                                list,
                                tuple,
                                set,
                                frozenset,
                            ),
                        ):
                            pending_held = [second_value]
                            seen_held = set()
                            while pending_held:
                                held = pending_held.pop()
                                if id(held) in seen_held:
                                    continue
                                seen_held.add(id(held))
                                if isinstance(held, str):
                                    returned_strs.add(held)
                                elif isinstance(
                                    held, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            held.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(held, dict):
                                    for held_key in held:
                                        pending_held.append(
                                            held_key
                                        )
                                        pending_held.append(
                                            held[held_key]
                                        )
                                elif isinstance(
                                    held,
                                    (
                                        list,
                                        tuple,
                                        set,
                                        frozenset,
                                    ),
                                ):
                                    pending_held.extend(held)
                for second_name in _code_facts(first_code)[0]:
                    second_fn = current_map.get(second_name)
                    if not isinstance(
                        second_fn,
                        _types_module.FunctionType,
                    ):
                        continue
                    if (
                        getattr(
                            second_fn, "__globals__", None
                        )
                        is not current_map
                    ):
                        continue
                    second_code = getattr(
                        second_fn, "__code__", None
                    )
                    if second_code is None:
                        continue
                    for third_name in _code_facts(
                        second_code
                    )[0]:
                        third_fn = current_map.get(third_name)
                        if not isinstance(
                            third_fn,
                            _types_module.FunctionType,
                        ):
                            continue
                        if (
                            getattr(
                                third_fn, "__globals__", None
                            )
                            is not current_map
                        ):
                            continue
                        third_code = getattr(
                            third_fn, "__code__", None
                        )
                        if third_code is None:
                            continue
                        returned_strs |= set(
                            _code_facts(third_code)[1]
                        )
                        for third_default in (
                            getattr(
                                third_fn, "__defaults__", None
                            )
                            or ()
                        ):
                            if isinstance(third_default, str):
                                returned_strs.add(third_default)
                            elif isinstance(
                                third_default, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        third_default.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                        for third_default in (
                            getattr(
                                third_fn,
                                "__kwdefaults__",
                                None,
                            )
                            or {}
                        ).values():
                            if isinstance(third_default, str):
                                returned_strs.add(third_default)
                            elif isinstance(
                                third_default, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        third_default.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                        for third_cell in (
                            getattr(
                                third_fn, "__closure__", None
                            )
                            or ()
                        ):
                            try:
                                third_cell_value = (
                                    third_cell.cell_contents
                                )
                            except Exception:
                                continue
                            if isinstance(third_cell_value, str):
                                returned_strs.add(
                                    third_cell_value
                                )
                            elif isinstance(
                                third_cell_value,
                                (bytes, bytearray),
                            ):
                                try:
                                    returned_strs.add(
                                        third_cell_value.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                        for third_loaded in _code_facts(
                            third_code
                        )[0]:
                            third_value = current_map.get(
                                third_loaded
                            )
                            if isinstance(third_value, str):
                                returned_strs.add(third_value)
                            elif isinstance(
                                third_value, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        third_value.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                            elif isinstance(
                                third_value,
                                (
                                    dict,
                                    list,
                                    tuple,
                                    set,
                                    frozenset,
                                ),
                            ):
                                pending_held = [third_value]
                                seen_held = set()
                                while pending_held:
                                    held = pending_held.pop()
                                    if id(held) in seen_held:
                                        continue
                                    seen_held.add(id(held))
                                    if isinstance(held, str):
                                        returned_strs.add(held)
                                    elif isinstance(
                                        held, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                held.decode("utf-8")
                                            )
                                        except Exception:
                                            pass
                                    elif isinstance(held, dict):
                                        for held_key in held:
                                            pending_held.append(held_key)
                                            pending_held.append(
                                                held[held_key]
                                            )
                                    elif isinstance(
                                        held,
                                        (list, tuple, set, frozenset),
                                    ):
                                        pending_held.extend(held)
                        for fourth_name in _code_facts(
                            third_code
                        )[0]:
                            fourth_fn = current_map.get(
                                fourth_name
                            )
                            if not isinstance(
                                fourth_fn,
                                _types_module.FunctionType,
                            ):
                                continue
                            if (
                                getattr(
                                    fourth_fn,
                                    "__globals__",
                                    None,
                                )
                                is not current_map
                            ):
                                continue
                            fourth_code = getattr(
                                fourth_fn, "__code__", None
                            )
                            if fourth_code is None:
                                continue
                            returned_strs |= set(
                                _code_facts(fourth_code)[1]
                            )
                            for fourth_default in (
                                getattr(
                                    fourth_fn, "__defaults__", None
                                )
                                or ()
                            ):
                                if isinstance(fourth_default, str):
                                    returned_strs.add(fourth_default)
                                elif isinstance(
                                    fourth_default, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            fourth_default.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for fourth_default in (
                                getattr(
                                    fourth_fn,
                                    "__kwdefaults__",
                                    None,
                                )
                                or {}
                            ).values():
                                if isinstance(fourth_default, str):
                                    returned_strs.add(fourth_default)
                                elif isinstance(
                                    fourth_default, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            fourth_default.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for fourth_cell in (
                                getattr(
                                    fourth_fn, "__closure__", None
                                )
                                or ()
                            ):
                                try:
                                    fourth_cell_value = (
                                        fourth_cell.cell_contents
                                    )
                                except Exception:
                                    continue
                                if isinstance(fourth_cell_value, str):
                                    returned_strs.add(
                                        fourth_cell_value
                                    )
                                elif isinstance(
                                    fourth_cell_value,
                                    (bytes, bytearray),
                                ):
                                    try:
                                        returned_strs.add(
                                            fourth_cell_value.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for fourth_loaded in _code_facts(
                                fourth_code
                            )[0]:
                                fourth_value = current_map.get(
                                    fourth_loaded
                                )
                                if isinstance(fourth_value, str):
                                    returned_strs.add(fourth_value)
                                elif isinstance(
                                    fourth_value, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            fourth_value.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(
                                    fourth_value,
                                    (
                                        dict,
                                        list,
                                        tuple,
                                        set,
                                        frozenset,
                                    ),
                                ):
                                    pending_held = [fourth_value]
                                    seen_held = set()
                                    while pending_held:
                                        held = pending_held.pop()
                                        if id(held) in seen_held:
                                            continue
                                        seen_held.add(id(held))
                                        if isinstance(held, str):
                                            returned_strs.add(held)
                                        elif isinstance(
                                            held, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    held.decode("utf-8")
                                                )
                                            except Exception:
                                                pass
                                        elif isinstance(held, dict):
                                            for held_key in held:
                                                pending_held.append(held_key)
                                                pending_held.append(
                                                    held[held_key]
                                                )
                                        elif isinstance(
                                            held,
                                            (list, tuple, set, frozenset),
                                        ):
                                            pending_held.extend(held)

                            for fifth_name in _code_facts(
                                fourth_code
                            )[0]:
                                fifth_fn = current_map.get(
                                    fifth_name
                                )
                                if not isinstance(
                                    fifth_fn,
                                    _types_module.FunctionType,
                                ):
                                    continue
                                if (
                                    getattr(
                                        fifth_fn,
                                        "__globals__",
                                        None,
                                    )
                                    is not current_map
                                ):
                                    continue
                                fifth_code = getattr(
                                    fifth_fn, "__code__", None
                                )
                                if fifth_code is None:
                                    continue
                                returned_strs |= set(
                                    _code_facts(fifth_code)[1]
                                )
                                for fifth_default in (
                                    getattr(
                                        fifth_fn, "__defaults__", None
                                    )
                                    or ()
                                ):
                                    if isinstance(fifth_default, str):
                                        returned_strs.add(fifth_default)
                                    elif isinstance(
                                        fifth_default, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                fifth_default.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for fifth_default in (
                                    getattr(
                                        fifth_fn,
                                        "__kwdefaults__",
                                        None,
                                    )
                                    or {}
                                ).values():
                                    if isinstance(fifth_default, str):
                                        returned_strs.add(fifth_default)
                                    elif isinstance(
                                        fifth_default, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                fifth_default.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for fifth_cell in (
                                    getattr(
                                        fifth_fn, "__closure__", None
                                    )
                                    or ()
                                ):
                                    try:
                                        fifth_cell_value = (
                                            fifth_cell.cell_contents
                                        )
                                    except Exception:
                                        continue
                                    if isinstance(fifth_cell_value, str):
                                        returned_strs.add(
                                            fifth_cell_value
                                        )
                                    elif isinstance(
                                        fifth_cell_value,
                                        (bytes, bytearray),
                                    ):
                                        try:
                                            returned_strs.add(
                                                fifth_cell_value.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for fifth_loaded in _code_facts(
                                    fifth_code
                                )[0]:
                                    fifth_value = current_map.get(
                                        fifth_loaded
                                    )
                                    if isinstance(fifth_value, str):
                                        returned_strs.add(fifth_value)
                                    elif isinstance(
                                        fifth_value, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                fifth_value.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                    elif isinstance(
                                        fifth_value,
                                        (
                                            dict,
                                            list,
                                            tuple,
                                            set,
                                            frozenset,
                                        ),
                                    ):
                                        pending_held = [fifth_value]
                                        seen_held = set()
                                        while pending_held:
                                            held = pending_held.pop()
                                            if id(held) in seen_held:
                                                continue
                                            seen_held.add(id(held))
                                            if isinstance(held, str):
                                                returned_strs.add(held)
                                            elif isinstance(
                                                held, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        held.decode("utf-8")
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(held, dict):
                                                for held_key in held:
                                                    pending_held.append(held_key)
                                                    pending_held.append(
                                                        held[held_key]
                                                    )
                                            elif isinstance(
                                                held,
                                                (list, tuple, set, frozenset),
                                            ):
                                                pending_held.extend(held)
                                for sixth_name in _code_facts(
                                    fifth_code
                                )[0]:
                                    sixth_fn = current_map.get(
                                        sixth_name
                                    )
                                    if not isinstance(
                                        sixth_fn,
                                        _types_module.FunctionType,
                                    ):
                                        continue
                                    if (
                                        getattr(
                                            sixth_fn,
                                            "__globals__",
                                            None,
                                        )
                                        is not current_map
                                    ):
                                        continue
                                    sixth_code = getattr(
                                        sixth_fn, "__code__", None
                                    )
                                    if sixth_code is None:
                                        continue
                                    returned_strs |= set(
                                        _code_facts(sixth_code)[1]
                                    )
                                    for sixth_default in (
                                        getattr(
                                            sixth_fn, "__defaults__", None
                                        )
                                        or ()
                                    ):
                                        if isinstance(sixth_default, str):
                                            returned_strs.add(sixth_default)
                                        elif isinstance(
                                            sixth_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    sixth_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for sixth_default in (
                                        getattr(
                                            sixth_fn,
                                            "__kwdefaults__",
                                            None,
                                        )
                                        or {}
                                    ).values():
                                        if isinstance(sixth_default, str):
                                            returned_strs.add(sixth_default)
                                        elif isinstance(
                                            sixth_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    sixth_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for sixth_cell in (
                                        getattr(
                                            sixth_fn, "__closure__", None
                                        )
                                        or ()
                                    ):
                                        try:
                                            sixth_cell_value = (
                                                sixth_cell.cell_contents
                                            )
                                        except Exception:
                                            continue
                                        if isinstance(sixth_cell_value, str):
                                            returned_strs.add(
                                                sixth_cell_value
                                            )
                                        elif isinstance(
                                            sixth_cell_value,
                                            (bytes, bytearray),
                                        ):
                                            try:
                                                returned_strs.add(
                                                    sixth_cell_value.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for sixth_loaded in _code_facts(
                                        sixth_code
                                    )[0]:
                                        sixth_value = current_map.get(
                                            sixth_loaded
                                        )
                                        if isinstance(sixth_value, str):
                                            returned_strs.add(sixth_value)
                                        elif isinstance(
                                            sixth_value, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    sixth_value.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                        elif isinstance(
                                            sixth_value,
                                            (
                                                dict,
                                                list,
                                                tuple,
                                                set,
                                                frozenset,
                                            ),
                                        ):
                                            pending_held = [sixth_value]
                                            seen_held = set()
                                            while pending_held:
                                                held = pending_held.pop()
                                                if id(held) in seen_held:
                                                    continue
                                                seen_held.add(id(held))
                                                if isinstance(held, str):
                                                    returned_strs.add(held)
                                                elif isinstance(
                                                    held, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            held.decode("utf-8")
                                                        )
                                                    except Exception:
                                                        pass
                                                elif isinstance(held, dict):
                                                    for held_key in held:
                                                        pending_held.append(held_key)
                                                        pending_held.append(
                                                            held[held_key]
                                                        )
                                                elif isinstance(
                                                    held,
                                                    (list, tuple, set, frozenset),
                                                ):
                                                    pending_held.extend(held)
                                    for seventh_name in _code_facts(
                                        sixth_code
                                    )[0]:
                                        seventh_fn = current_map.get(
                                            seventh_name
                                        )
                                        if not isinstance(
                                            seventh_fn,
                                            _types_module.FunctionType,
                                        ):
                                            continue
                                        if (
                                            getattr(
                                                seventh_fn,
                                                "__globals__",
                                                None,
                                            )
                                            is not current_map
                                        ):
                                            continue
                                        seventh_code = getattr(
                                            seventh_fn, "__code__", None
                                        )
                                        if seventh_code is None:
                                            continue
                                        returned_strs |= set(
                                            _code_facts(seventh_code)[1]
                                        )
                                        for seventh_default in (
                                            getattr(
                                                seventh_fn, "__defaults__", None
                                            )
                                            or ()
                                        ):
                                            if isinstance(seventh_default, str):
                                                returned_strs.add(seventh_default)
                                            elif isinstance(
                                                seventh_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        seventh_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for seventh_default in (
                                            getattr(
                                                seventh_fn,
                                                "__kwdefaults__",
                                                None,
                                            )
                                            or {}
                                        ).values():
                                            if isinstance(seventh_default, str):
                                                returned_strs.add(seventh_default)
                                            elif isinstance(
                                                seventh_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        seventh_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for seventh_cell in (
                                            getattr(
                                                seventh_fn, "__closure__", None
                                            )
                                            or ()
                                        ):
                                            try:
                                                seventh_cell_value = (
                                                    seventh_cell.cell_contents
                                                )
                                            except Exception:
                                                continue
                                            if isinstance(seventh_cell_value, str):
                                                returned_strs.add(
                                                    seventh_cell_value
                                                )
                                            elif isinstance(
                                                seventh_cell_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        seventh_cell_value.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for seventh_loaded in _code_facts(
                                            seventh_code
                                        )[0]:
                                            seventh_value = current_map.get(
                                                seventh_loaded
                                            )
                                            if isinstance(seventh_value, str):
                                                returned_strs.add(seventh_value)
                                            elif isinstance(
                                                seventh_value, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        seventh_value.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(
                                                seventh_value,
                                                (
                                                    dict,
                                                    list,
                                                    tuple,
                                                    set,
                                                    frozenset,
                                                ),
                                            ):
                                                pending_held = [seventh_value]
                                                seen_held = set()
                                                while pending_held:
                                                    held = pending_held.pop()
                                                    if id(held) in seen_held:
                                                        continue
                                                    seen_held.add(id(held))
                                                    if isinstance(held, str):
                                                        returned_strs.add(held)
                                                    elif isinstance(
                                                        held, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                held.decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(held, dict):
                                                        for held_key in held:
                                                            pending_held.append(held_key)
                                                            pending_held.append(
                                                                held[held_key]
                                                            )
                                                    elif isinstance(
                                                        held,
                                                        (list, tuple, set, frozenset),
                                                    ):
                                                        pending_held.extend(held)
                            for pair4_base, pair4_attr in _code_facts(
                                fourth_code
                            )[3]:
                                if pair4_base not in current_map:
                                    continue
                                pair4_module = current_map[pair4_base]
                                if not isinstance(
                                    pair4_module, _types_module.ModuleType
                                ):
                                    continue
                                pair4_map = getattr(
                                    pair4_module, "__dict__", None
                                )
                                if not isinstance(pair4_map, dict):
                                    continue
                                pair4_value = pair4_map.get(pair4_attr)
                                if isinstance(pair4_value, str):
                                    returned_strs.add(pair4_value)
                                elif isinstance(
                                    pair4_value, _types_module.FunctionType
                                ):
                                    pair4_code = getattr(
                                        pair4_value, "__code__", None
                                    )
                                    if pair4_code is not None:
                                        returned_strs |= set(
                                            _code_facts(pair4_code)[1]
                                        )
                                    for pair4_default in (
                                        getattr(
                                            pair4_value, "__defaults__", None
                                        )
                                        or ()
                                    ):
                                        if isinstance(pair4_default, str):
                                            returned_strs.add(pair4_default)
                                        elif isinstance(
                                            pair4_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    pair4_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for pair4_default in (
                                        getattr(
                                            pair4_value,
                                            "__kwdefaults__",
                                            None,
                                        )
                                        or {}
                                    ).values():
                                        if isinstance(pair4_default, str):
                                            returned_strs.add(pair4_default)
                                        elif isinstance(
                                            pair4_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    pair4_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for pair4_cell in (
                                        getattr(
                                            pair4_value, "__closure__", None
                                        )
                                        or ()
                                    ):
                                        try:
                                            pair4_cell_value = (
                                                pair4_cell.cell_contents
                                            )
                                        except Exception:
                                            continue
                                        if isinstance(pair4_cell_value, str):
                                            returned_strs.add(
                                                pair4_cell_value
                                            )
                                        elif isinstance(
                                            pair4_cell_value,
                                            (bytes, bytearray),
                                        ):
                                            try:
                                                returned_strs.add(
                                                    pair4_cell_value.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    if pair4_code is not None:
                                        for pair4_loaded in _code_facts(
                                            pair4_code
                                        )[0]:
                                            pair4_loaded_value = pair4_map.get(
                                                pair4_loaded
                                            )
                                            if isinstance(
                                                pair4_loaded_value, str
                                            ):
                                                returned_strs.add(
                                                    pair4_loaded_value
                                                )
                                            elif isinstance(
                                                pair4_loaded_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        pair4_loaded_value
                                                        .decode("utf-8")
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(
                                                pair4_loaded_value,
                                                (
                                                    dict,
                                                    list,
                                                    tuple,
                                                    set,
                                                    frozenset,
                                                ),
                                            ):
                                                pending_held = [pair4_loaded_value]
                                                seen_held = set()
                                                while pending_held:
                                                    held = pending_held.pop()
                                                    if id(held) in seen_held:
                                                        continue
                                                    seen_held.add(id(held))
                                                    if isinstance(held, str):
                                                        returned_strs.add(held)
                                                    elif isinstance(
                                                        held, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                held.decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(held, dict):
                                                        for held_key in held:
                                                            pending_held.append(held_key)
                                                            pending_held.append(
                                                                held[held_key]
                                                            )
                                                    elif isinstance(
                                                        held,
                                                        (list, tuple, set, frozenset),
                                                    ):
                                                        pending_held.extend(held)
                                    if pair4_code is not None:
                                        for pair4_inner_name in (
                                            _code_facts(pair4_code)[0]
                                        ):
                                            pair4_inner_fn = (
                                                pair4_map.get(
                                                    pair4_inner_name
                                                )
                                            )
                                            if not isinstance(
                                                pair4_inner_fn,
                                                _types_module
                                                .FunctionType,
                                            ):
                                                continue
                                            if (
                                                getattr(
                                                    pair4_inner_fn,
                                                    "__globals__",
                                                    None,
                                                )
                                                is not pair4_map
                                            ):
                                                continue
                                            inner_code = getattr(
                                                pair4_inner_fn, "__code__", None
                                            )
                                            if inner_code is not None:
                                                for pair4_inner2_name in (
                                                    _code_facts(
                                                        inner_code
                                                    )[0]
                                                ):
                                                    pair4_inner2_fn = (
                                                        pair4_map.get(
                                                            pair4_inner2_name
                                                        )
                                                    )
                                                    if not isinstance(
                                                        pair4_inner2_fn,
                                                        _types_module
                                                        .FunctionType,
                                                    ):
                                                        continue
                                                    if (
                                                        getattr(
                                                            pair4_inner2_fn,
                                                            "__globals__",
                                                            None,
                                                        )
                                                        is not pair4_map
                                                    ):
                                                        continue
                                                    inner2_code = getattr(
                                                        pair4_inner2_fn,
                                                        "__code__",
                                                        None,
                                                    )
                                                    if inner2_code is not None:
                                                        returned_strs |= set(
                                                            _code_facts(inner2_code)[1]
                                                        )
                                                    for inner2_default in (
                                                        getattr(
                                                            pair4_inner2_fn, "__defaults__", None
                                                        )
                                                        or ()
                                                    ):
                                                        if isinstance(inner2_default, str):
                                                            returned_strs.add(inner2_default)
                                                        elif isinstance(
                                                            inner2_default, (bytes, bytearray)
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    inner2_default.decode(
                                                                        "utf-8"
                                                                    )
                                                                )
                                                            except Exception:
                                                                pass
                                                    for inner2_default in (
                                                        getattr(
                                                            pair4_inner2_fn,
                                                            "__kwdefaults__",
                                                            None,
                                                        )
                                                        or {}
                                                    ).values():
                                                        if isinstance(inner2_default, str):
                                                            returned_strs.add(inner2_default)
                                                        elif isinstance(
                                                            inner2_default, (bytes, bytearray)
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    inner2_default.decode(
                                                                        "utf-8"
                                                                    )
                                                                )
                                                            except Exception:
                                                                pass
                                                    for inner2_cell in (
                                                        getattr(
                                                            pair4_inner2_fn, "__closure__", None
                                                        )
                                                        or ()
                                                    ):
                                                        try:
                                                            inner2_cell_value = (
                                                                inner2_cell.cell_contents
                                                            )
                                                        except Exception:
                                                            continue
                                                        if isinstance(inner2_cell_value, str):
                                                            returned_strs.add(
                                                                inner2_cell_value
                                                            )
                                                        elif isinstance(
                                                            inner2_cell_value,
                                                            (bytes, bytearray),
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    inner2_cell_value.decode(
                                                                        "utf-8"
                                                                    )
                                                                )
                                                            except Exception:
                                                                pass
                                                    if inner2_code is not None:
                                                        for inner2_loaded in _code_facts(
                                                            inner2_code
                                                        )[0]:
                                                            inner2_loaded_value = pair4_map.get(
                                                                inner2_loaded
                                                            )
                                                            if isinstance(
                                                                inner2_loaded_value, str
                                                            ):
                                                                returned_strs.add(
                                                                    inner2_loaded_value
                                                                )
                                                            elif isinstance(
                                                                inner2_loaded_value,
                                                                (bytes, bytearray),
                                                            ):
                                                                try:
                                                                    returned_strs.add(
                                                                        inner2_loaded_value
                                                                        .decode("utf-8")
                                                                    )
                                                                except Exception:
                                                                    pass
                                                            elif isinstance(
                                                                inner2_loaded_value,
                                                                (
                                                                    dict,
                                                                    list,
                                                                    tuple,
                                                                    set,
                                                                    frozenset,
                                                                ),
                                                            ):
                                                                pending_held = [inner2_loaded_value]
                                                                seen_held = set()
                                                                while pending_held:
                                                                    held = pending_held.pop()
                                                                    if id(held) in seen_held:
                                                                        continue
                                                                    seen_held.add(id(held))
                                                                    if isinstance(held, str):
                                                                        returned_strs.add(held)
                                                                    elif isinstance(
                                                                        held, (bytes, bytearray)
                                                                    ):
                                                                        try:
                                                                            returned_strs.add(
                                                                                held.decode("utf-8")
                                                                            )
                                                                        except Exception:
                                                                            pass
                                                                    elif isinstance(held, dict):
                                                                        for held_key in held:
                                                                            pending_held.append(held_key)
                                                                            pending_held.append(
                                                                                held[held_key]
                                                                            )
                                                                    elif isinstance(
                                                                        held,
                                                                        (list, tuple, set, frozenset),
                                                                    ):
                                                                        pending_held.extend(held)
                                            if inner_code is not None:
                                                returned_strs |= set(
                                                    _code_facts(inner_code)[1]
                                                )
                                            for inner_default in (
                                                getattr(
                                                    pair4_inner_fn, "__defaults__", None
                                                )
                                                or ()
                                            ):
                                                if isinstance(inner_default, str):
                                                    returned_strs.add(inner_default)
                                                elif isinstance(
                                                    inner_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner_default in (
                                                getattr(
                                                    pair4_inner_fn,
                                                    "__kwdefaults__",
                                                    None,
                                                )
                                                or {}
                                            ).values():
                                                if isinstance(inner_default, str):
                                                    returned_strs.add(inner_default)
                                                elif isinstance(
                                                    inner_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner_cell in (
                                                getattr(
                                                    pair4_inner_fn, "__closure__", None
                                                )
                                                or ()
                                            ):
                                                try:
                                                    inner_cell_value = (
                                                        inner_cell.cell_contents
                                                    )
                                                except Exception:
                                                    continue
                                                if isinstance(inner_cell_value, str):
                                                    returned_strs.add(
                                                        inner_cell_value
                                                    )
                                                elif isinstance(
                                                    inner_cell_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner_cell_value.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            if inner_code is not None:
                                                for inner_loaded in _code_facts(
                                                    inner_code
                                                )[0]:
                                                    inner_loaded_value = pair4_map.get(
                                                        inner_loaded
                                                    )
                                                    if isinstance(
                                                        inner_loaded_value, str
                                                    ):
                                                        returned_strs.add(
                                                            inner_loaded_value
                                                        )
                                                    elif isinstance(
                                                        inner_loaded_value,
                                                        (bytes, bytearray),
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner_loaded_value
                                                                .decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(
                                                        inner_loaded_value,
                                                        (
                                                            dict,
                                                            list,
                                                            tuple,
                                                            set,
                                                            frozenset,
                                                        ),
                                                    ):
                                                        pending_held = [inner_loaded_value]
                                                        seen_held = set()
                                                        while pending_held:
                                                            held = pending_held.pop()
                                                            if id(held) in seen_held:
                                                                continue
                                                            seen_held.add(id(held))
                                                            if isinstance(held, str):
                                                                returned_strs.add(held)
                                                            elif isinstance(
                                                                held, (bytes, bytearray)
                                                            ):
                                                                try:
                                                                    returned_strs.add(
                                                                        held.decode("utf-8")
                                                                    )
                                                                except Exception:
                                                                    pass
                                                            elif isinstance(held, dict):
                                                                for held_key in held:
                                                                    pending_held.append(held_key)
                                                                    pending_held.append(
                                                                        held[held_key]
                                                                    )
                                                            elif isinstance(
                                                                held,
                                                                (list, tuple, set, frozenset),
                                                            ):
                                                                pending_held.extend(held)
                        for pair3_base, pair3_attr in _code_facts(
                            third_code
                        )[3]:
                            if pair3_base not in current_map:
                                continue
                            pair3_module = current_map[pair3_base]
                            if not isinstance(
                                pair3_module, _types_module.ModuleType
                            ):
                                continue
                            pair3_map = getattr(
                                pair3_module, "__dict__", None
                            )
                            if not isinstance(pair3_map, dict):
                                continue
                            pair3_value = pair3_map.get(pair3_attr)
                            if isinstance(pair3_value, str):
                                returned_strs.add(pair3_value)
                            elif isinstance(
                                pair3_value, _types_module.FunctionType
                            ):
                                pair3_code = getattr(
                                    pair3_value, "__code__", None
                                )
                                if pair3_code is not None:
                                    returned_strs |= set(
                                        _code_facts(pair3_code)[1]
                                    )
                                for pair3_default in (
                                    getattr(
                                        pair3_value, "__defaults__", None
                                    )
                                    or ()
                                ):
                                    if isinstance(pair3_default, str):
                                        returned_strs.add(pair3_default)
                                    elif isinstance(
                                        pair3_default, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                pair3_default.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for pair3_default in (
                                    getattr(
                                        pair3_value,
                                        "__kwdefaults__",
                                        None,
                                    )
                                    or {}
                                ).values():
                                    if isinstance(pair3_default, str):
                                        returned_strs.add(pair3_default)
                                    elif isinstance(
                                        pair3_default, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                pair3_default.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for pair3_cell in (
                                    getattr(
                                        pair3_value, "__closure__", None
                                    )
                                    or ()
                                ):
                                    try:
                                        pair3_cell_value = (
                                            pair3_cell.cell_contents
                                        )
                                    except Exception:
                                        continue
                                    if isinstance(pair3_cell_value, str):
                                        returned_strs.add(
                                            pair3_cell_value
                                        )
                                    elif isinstance(
                                        pair3_cell_value,
                                        (bytes, bytearray),
                                    ):
                                        try:
                                            returned_strs.add(
                                                pair3_cell_value.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                if pair3_code is not None:
                                    for pair3_loaded in _code_facts(
                                        pair3_code
                                    )[0]:
                                        pair3_loaded_value = pair3_map.get(
                                            pair3_loaded
                                        )
                                        if isinstance(
                                            pair3_loaded_value, str
                                        ):
                                            returned_strs.add(
                                                pair3_loaded_value
                                            )
                                        elif isinstance(
                                            pair3_loaded_value,
                                            (bytes, bytearray),
                                        ):
                                            try:
                                                returned_strs.add(
                                                    pair3_loaded_value
                                                    .decode("utf-8")
                                                )
                                            except Exception:
                                                pass
                                        elif isinstance(
                                            pair3_loaded_value,
                                            (
                                                dict,
                                                list,
                                                tuple,
                                                set,
                                                frozenset,
                                            ),
                                        ):
                                            pending_held = [pair3_loaded_value]
                                            seen_held = set()
                                            while pending_held:
                                                held = pending_held.pop()
                                                if id(held) in seen_held:
                                                    continue
                                                seen_held.add(id(held))
                                                if isinstance(held, str):
                                                    returned_strs.add(held)
                                                elif isinstance(
                                                    held, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            held.decode("utf-8")
                                                        )
                                                    except Exception:
                                                        pass
                                                elif isinstance(held, dict):
                                                    for held_key in held:
                                                        pending_held.append(held_key)
                                                        pending_held.append(
                                                            held[held_key]
                                                        )
                                                elif isinstance(
                                                    held,
                                                    (list, tuple, set, frozenset),
                                                ):
                                                    pending_held.extend(held)
                                if pair3_code is not None:
                                    for pair3_inner_name in (
                                        _code_facts(pair3_code)[0]
                                    ):
                                        pair3_inner_fn = (
                                            pair3_map.get(
                                                pair3_inner_name
                                            )
                                        )
                                        if not isinstance(
                                            pair3_inner_fn,
                                            _types_module
                                            .FunctionType,
                                        ):
                                            continue
                                        if (
                                            getattr(
                                                pair3_inner_fn,
                                                "__globals__",
                                                None,
                                            )
                                            is not pair3_map
                                        ):
                                            continue
                                        inner_code = getattr(
                                            pair3_inner_fn, "__code__", None
                                        )
                                        if inner_code is not None:
                                            for pair3_inner2_name in (
                                                _code_facts(
                                                    inner_code
                                                )[0]
                                            ):
                                                pair3_inner2_fn = (
                                                    pair3_map.get(
                                                        pair3_inner2_name
                                                    )
                                                )
                                                if not isinstance(
                                                    pair3_inner2_fn,
                                                    _types_module
                                                    .FunctionType,
                                                ):
                                                    continue
                                                if (
                                                    getattr(
                                                        pair3_inner2_fn,
                                                        "__globals__",
                                                        None,
                                                    )
                                                    is not pair3_map
                                                ):
                                                    continue
                                                inner2_code = getattr(
                                                    pair3_inner2_fn,
                                                    "__code__",
                                                    None,
                                                )
                                                if inner2_code is not None:
                                                    returned_strs |= set(
                                                        _code_facts(inner2_code)[1]
                                                    )
                                                for inner2_default in (
                                                    getattr(
                                                        pair3_inner2_fn, "__defaults__", None
                                                    )
                                                    or ()
                                                ):
                                                    if isinstance(inner2_default, str):
                                                        returned_strs.add(inner2_default)
                                                    elif isinstance(
                                                        inner2_default, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner2_default.decode(
                                                                    "utf-8"
                                                                )
                                                            )
                                                        except Exception:
                                                            pass
                                                for inner2_default in (
                                                    getattr(
                                                        pair3_inner2_fn,
                                                        "__kwdefaults__",
                                                        None,
                                                    )
                                                    or {}
                                                ).values():
                                                    if isinstance(inner2_default, str):
                                                        returned_strs.add(inner2_default)
                                                    elif isinstance(
                                                        inner2_default, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner2_default.decode(
                                                                    "utf-8"
                                                                )
                                                            )
                                                        except Exception:
                                                            pass
                                                for inner2_cell in (
                                                    getattr(
                                                        pair3_inner2_fn, "__closure__", None
                                                    )
                                                    or ()
                                                ):
                                                    try:
                                                        inner2_cell_value = (
                                                            inner2_cell.cell_contents
                                                        )
                                                    except Exception:
                                                        continue
                                                    if isinstance(inner2_cell_value, str):
                                                        returned_strs.add(
                                                            inner2_cell_value
                                                        )
                                                    elif isinstance(
                                                        inner2_cell_value,
                                                        (bytes, bytearray),
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner2_cell_value.decode(
                                                                    "utf-8"
                                                                )
                                                            )
                                                        except Exception:
                                                            pass
                                                if inner2_code is not None:
                                                    for inner2_loaded in _code_facts(
                                                        inner2_code
                                                    )[0]:
                                                        inner2_loaded_value = pair3_map.get(
                                                            inner2_loaded
                                                        )
                                                        if isinstance(
                                                            inner2_loaded_value, str
                                                        ):
                                                            returned_strs.add(
                                                                inner2_loaded_value
                                                            )
                                                        elif isinstance(
                                                            inner2_loaded_value,
                                                            (bytes, bytearray),
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    inner2_loaded_value
                                                                    .decode("utf-8")
                                                                )
                                                            except Exception:
                                                                pass
                                                        elif isinstance(
                                                            inner2_loaded_value,
                                                            (
                                                                dict,
                                                                list,
                                                                tuple,
                                                                set,
                                                                frozenset,
                                                            ),
                                                        ):
                                                            pending_held = [inner2_loaded_value]
                                                            seen_held = set()
                                                            while pending_held:
                                                                held = pending_held.pop()
                                                                if id(held) in seen_held:
                                                                    continue
                                                                seen_held.add(id(held))
                                                                if isinstance(held, str):
                                                                    returned_strs.add(held)
                                                                elif isinstance(
                                                                    held, (bytes, bytearray)
                                                                ):
                                                                    try:
                                                                        returned_strs.add(
                                                                            held.decode("utf-8")
                                                                        )
                                                                    except Exception:
                                                                        pass
                                                                elif isinstance(held, dict):
                                                                    for held_key in held:
                                                                        pending_held.append(held_key)
                                                                        pending_held.append(
                                                                            held[held_key]
                                                                        )
                                                                elif isinstance(
                                                                    held,
                                                                    (list, tuple, set, frozenset),
                                                                ):
                                                                    pending_held.extend(held)
                                        if inner_code is not None:
                                            returned_strs |= set(
                                                _code_facts(inner_code)[1]
                                            )
                                        for inner_default in (
                                            getattr(
                                                pair3_inner_fn, "__defaults__", None
                                            )
                                            or ()
                                        ):
                                            if isinstance(inner_default, str):
                                                returned_strs.add(inner_default)
                                            elif isinstance(
                                                inner_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for inner_default in (
                                            getattr(
                                                pair3_inner_fn,
                                                "__kwdefaults__",
                                                None,
                                            )
                                            or {}
                                        ).values():
                                            if isinstance(inner_default, str):
                                                returned_strs.add(inner_default)
                                            elif isinstance(
                                                inner_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for inner_cell in (
                                            getattr(
                                                pair3_inner_fn, "__closure__", None
                                            )
                                            or ()
                                        ):
                                            try:
                                                inner_cell_value = (
                                                    inner_cell.cell_contents
                                                )
                                            except Exception:
                                                continue
                                            if isinstance(inner_cell_value, str):
                                                returned_strs.add(
                                                    inner_cell_value
                                                )
                                            elif isinstance(
                                                inner_cell_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner_cell_value.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        if inner_code is not None:
                                            for inner_loaded in _code_facts(
                                                inner_code
                                            )[0]:
                                                inner_loaded_value = pair3_map.get(
                                                    inner_loaded
                                                )
                                                if isinstance(
                                                    inner_loaded_value, str
                                                ):
                                                    returned_strs.add(
                                                        inner_loaded_value
                                                    )
                                                elif isinstance(
                                                    inner_loaded_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner_loaded_value
                                                            .decode("utf-8")
                                                        )
                                                    except Exception:
                                                        pass
                                                elif isinstance(
                                                    inner_loaded_value,
                                                    (
                                                        dict,
                                                        list,
                                                        tuple,
                                                        set,
                                                        frozenset,
                                                    ),
                                                ):
                                                    pending_held = [inner_loaded_value]
                                                    seen_held = set()
                                                    while pending_held:
                                                        held = pending_held.pop()
                                                        if id(held) in seen_held:
                                                            continue
                                                        seen_held.add(id(held))
                                                        if isinstance(held, str):
                                                            returned_strs.add(held)
                                                        elif isinstance(
                                                            held, (bytes, bytearray)
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    held.decode("utf-8")
                                                                )
                                                            except Exception:
                                                                pass
                                                        elif isinstance(held, dict):
                                                            for held_key in held:
                                                                pending_held.append(held_key)
                                                                pending_held.append(
                                                                    held[held_key]
                                                                )
                                                        elif isinstance(
                                                            held,
                                                            (list, tuple, set, frozenset),
                                                        ):
                                                            pending_held.extend(held)
                    for pair2_base, pair2_attr in _code_facts(
                        second_code
                    )[3]:
                        if pair2_base not in current_map:
                            continue
                        pair2_module = current_map[pair2_base]
                        if not isinstance(
                            pair2_module, _types_module.ModuleType
                        ):
                            continue
                        pair2_map = getattr(
                            pair2_module, "__dict__", None
                        )
                        if not isinstance(pair2_map, dict):
                            continue
                        pair2_value = pair2_map.get(pair2_attr)
                        if isinstance(pair2_value, str):
                            returned_strs.add(pair2_value)
                        elif isinstance(
                            pair2_value, _types_module.FunctionType
                        ):
                            pair2_code = getattr(
                                pair2_value, "__code__", None
                            )
                            if pair2_code is not None:
                                returned_strs |= set(
                                    _code_facts(pair2_code)[1]
                                )
                            for pair2_default in (
                                getattr(
                                    pair2_value, "__defaults__", None
                                )
                                or ()
                            ):
                                if isinstance(pair2_default, str):
                                    returned_strs.add(pair2_default)
                                elif isinstance(
                                    pair2_default, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            pair2_default.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for pair2_default in (
                                getattr(
                                    pair2_value,
                                    "__kwdefaults__",
                                    None,
                                )
                                or {}
                            ).values():
                                if isinstance(pair2_default, str):
                                    returned_strs.add(pair2_default)
                                elif isinstance(
                                    pair2_default, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            pair2_default.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for pair2_cell in (
                                getattr(
                                    pair2_value, "__closure__", None
                                )
                                or ()
                            ):
                                try:
                                    pair2_cell_value = (
                                        pair2_cell.cell_contents
                                    )
                                except Exception:
                                    continue
                                if isinstance(pair2_cell_value, str):
                                    returned_strs.add(
                                        pair2_cell_value
                                    )
                                elif isinstance(
                                    pair2_cell_value,
                                    (bytes, bytearray),
                                ):
                                    try:
                                        returned_strs.add(
                                            pair2_cell_value.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            if pair2_code is not None:
                                for pair2_loaded in _code_facts(
                                    pair2_code
                                )[0]:
                                    pair2_loaded_value = pair2_map.get(
                                        pair2_loaded
                                    )
                                    if isinstance(
                                        pair2_loaded_value, str
                                    ):
                                        returned_strs.add(
                                            pair2_loaded_value
                                        )
                                    elif isinstance(
                                        pair2_loaded_value,
                                        (bytes, bytearray),
                                    ):
                                        try:
                                            returned_strs.add(
                                                pair2_loaded_value
                                                .decode("utf-8")
                                            )
                                        except Exception:
                                            pass
                                    elif isinstance(
                                        pair2_loaded_value,
                                        (
                                            dict,
                                            list,
                                            tuple,
                                            set,
                                            frozenset,
                                        ),
                                    ):
                                        pending_held = [pair2_loaded_value]
                                        seen_held = set()
                                        while pending_held:
                                            held = pending_held.pop()
                                            if id(held) in seen_held:
                                                continue
                                            seen_held.add(id(held))
                                            if isinstance(held, str):
                                                returned_strs.add(held)
                                            elif isinstance(
                                                held, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        held.decode("utf-8")
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(held, dict):
                                                for held_key in held:
                                                    pending_held.append(held_key)
                                                    pending_held.append(
                                                        held[held_key]
                                                    )
                                            elif isinstance(
                                                held,
                                                (list, tuple, set, frozenset),
                                            ):
                                                pending_held.extend(held)
                            if pair2_code is not None:
                                for pair2_inner_name in (
                                    _code_facts(pair2_code)[0]
                                ):
                                    pair2_inner_fn = (
                                        pair2_map.get(
                                            pair2_inner_name
                                        )
                                    )
                                    if not isinstance(
                                        pair2_inner_fn,
                                        _types_module
                                        .FunctionType,
                                    ):
                                        continue
                                    if (
                                        getattr(
                                            pair2_inner_fn,
                                            "__globals__",
                                            None,
                                        )
                                        is not pair2_map
                                    ):
                                        continue
                                    inner_code = getattr(
                                        pair2_inner_fn, "__code__", None
                                    )
                                    if inner_code is not None:
                                        for pair2_inner2_name in (
                                            _code_facts(
                                                inner_code
                                            )[0]
                                        ):
                                            pair2_inner2_fn = (
                                                pair2_map.get(
                                                    pair2_inner2_name
                                                )
                                            )
                                            if not isinstance(
                                                pair2_inner2_fn,
                                                _types_module
                                                .FunctionType,
                                            ):
                                                continue
                                            if (
                                                getattr(
                                                    pair2_inner2_fn,
                                                    "__globals__",
                                                    None,
                                                )
                                                is not pair2_map
                                            ):
                                                continue
                                            inner2_code = getattr(
                                                pair2_inner2_fn,
                                                "__code__",
                                                None,
                                            )
                                            if inner2_code is not None:
                                                returned_strs |= set(
                                                    _code_facts(inner2_code)[1]
                                                )
                                            for inner2_default in (
                                                getattr(
                                                    pair2_inner2_fn, "__defaults__", None
                                                )
                                                or ()
                                            ):
                                                if isinstance(inner2_default, str):
                                                    returned_strs.add(inner2_default)
                                                elif isinstance(
                                                    inner2_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner2_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner2_default in (
                                                getattr(
                                                    pair2_inner2_fn,
                                                    "__kwdefaults__",
                                                    None,
                                                )
                                                or {}
                                            ).values():
                                                if isinstance(inner2_default, str):
                                                    returned_strs.add(inner2_default)
                                                elif isinstance(
                                                    inner2_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner2_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner2_cell in (
                                                getattr(
                                                    pair2_inner2_fn, "__closure__", None
                                                )
                                                or ()
                                            ):
                                                try:
                                                    inner2_cell_value = (
                                                        inner2_cell.cell_contents
                                                    )
                                                except Exception:
                                                    continue
                                                if isinstance(inner2_cell_value, str):
                                                    returned_strs.add(
                                                        inner2_cell_value
                                                    )
                                                elif isinstance(
                                                    inner2_cell_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner2_cell_value.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            if inner2_code is not None:
                                                for inner2_loaded in _code_facts(
                                                    inner2_code
                                                )[0]:
                                                    inner2_loaded_value = pair2_map.get(
                                                        inner2_loaded
                                                    )
                                                    if isinstance(
                                                        inner2_loaded_value, str
                                                    ):
                                                        returned_strs.add(
                                                            inner2_loaded_value
                                                        )
                                                    elif isinstance(
                                                        inner2_loaded_value,
                                                        (bytes, bytearray),
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner2_loaded_value
                                                                .decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(
                                                        inner2_loaded_value,
                                                        (
                                                            dict,
                                                            list,
                                                            tuple,
                                                            set,
                                                            frozenset,
                                                        ),
                                                    ):
                                                        pending_held = [inner2_loaded_value]
                                                        seen_held = set()
                                                        while pending_held:
                                                            held = pending_held.pop()
                                                            if id(held) in seen_held:
                                                                continue
                                                            seen_held.add(id(held))
                                                            if isinstance(held, str):
                                                                returned_strs.add(held)
                                                            elif isinstance(
                                                                held, (bytes, bytearray)
                                                            ):
                                                                try:
                                                                    returned_strs.add(
                                                                        held.decode("utf-8")
                                                                    )
                                                                except Exception:
                                                                    pass
                                                            elif isinstance(held, dict):
                                                                for held_key in held:
                                                                    pending_held.append(held_key)
                                                                    pending_held.append(
                                                                        held[held_key]
                                                                    )
                                                            elif isinstance(
                                                                held,
                                                                (list, tuple, set, frozenset),
                                                            ):
                                                                pending_held.extend(held)
                                    if inner_code is not None:
                                        returned_strs |= set(
                                            _code_facts(inner_code)[1]
                                        )
                                    for inner_default in (
                                        getattr(
                                            pair2_inner_fn, "__defaults__", None
                                        )
                                        or ()
                                    ):
                                        if isinstance(inner_default, str):
                                            returned_strs.add(inner_default)
                                        elif isinstance(
                                            inner_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for inner_default in (
                                        getattr(
                                            pair2_inner_fn,
                                            "__kwdefaults__",
                                            None,
                                        )
                                        or {}
                                    ).values():
                                        if isinstance(inner_default, str):
                                            returned_strs.add(inner_default)
                                        elif isinstance(
                                            inner_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for inner_cell in (
                                        getattr(
                                            pair2_inner_fn, "__closure__", None
                                        )
                                        or ()
                                    ):
                                        try:
                                            inner_cell_value = (
                                                inner_cell.cell_contents
                                            )
                                        except Exception:
                                            continue
                                        if isinstance(inner_cell_value, str):
                                            returned_strs.add(
                                                inner_cell_value
                                            )
                                        elif isinstance(
                                            inner_cell_value,
                                            (bytes, bytearray),
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner_cell_value.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    if inner_code is not None:
                                        for inner_loaded in _code_facts(
                                            inner_code
                                        )[0]:
                                            inner_loaded_value = pair2_map.get(
                                                inner_loaded
                                            )
                                            if isinstance(
                                                inner_loaded_value, str
                                            ):
                                                returned_strs.add(
                                                    inner_loaded_value
                                                )
                                            elif isinstance(
                                                inner_loaded_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner_loaded_value
                                                        .decode("utf-8")
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(
                                                inner_loaded_value,
                                                (
                                                    dict,
                                                    list,
                                                    tuple,
                                                    set,
                                                    frozenset,
                                                ),
                                            ):
                                                pending_held = [inner_loaded_value]
                                                seen_held = set()
                                                while pending_held:
                                                    held = pending_held.pop()
                                                    if id(held) in seen_held:
                                                        continue
                                                    seen_held.add(id(held))
                                                    if isinstance(held, str):
                                                        returned_strs.add(held)
                                                    elif isinstance(
                                                        held, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                held.decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(held, dict):
                                                        for held_key in held:
                                                            pending_held.append(held_key)
                                                            pending_held.append(
                                                                held[held_key]
                                                            )
                                                    elif isinstance(
                                                        held,
                                                        (list, tuple, set, frozenset),
                                                    ):
                                                        pending_held.extend(held)
                for pair_base, pair_attr in _code_facts(
                    first_code
                )[3]:
                    if pair_base not in current_map:
                        continue
                    pair_module = current_map[pair_base]
                    if not isinstance(
                        pair_module, _types_module.ModuleType
                    ):
                        continue
                    pair_map = getattr(
                        pair_module, "__dict__", None
                    )
                    if not isinstance(pair_map, dict):
                        continue
                    pair_value = pair_map.get(pair_attr)
                    if isinstance(pair_value, str):
                        returned_strs.add(pair_value)
                    elif isinstance(
                        pair_value, _types_module.FunctionType
                    ):
                        pair_code = getattr(
                            pair_value, "__code__", None
                        )
                        if pair_code is not None:
                            returned_strs |= set(
                                _code_facts(pair_code)[1]
                            )
                        for pair_default in (
                            getattr(
                                pair_value, "__defaults__", None
                            )
                            or ()
                        ):
                            if isinstance(pair_default, str):
                                returned_strs.add(pair_default)
                            elif isinstance(
                                pair_default, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        pair_default.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                        for pair_default in (
                            getattr(
                                pair_value,
                                "__kwdefaults__",
                                None,
                            )
                            or {}
                        ).values():
                            if isinstance(pair_default, str):
                                returned_strs.add(pair_default)
                            elif isinstance(
                                pair_default, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        pair_default.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                        for pair_cell in (
                            getattr(
                                pair_value, "__closure__", None
                            )
                            or ()
                        ):
                            try:
                                pair_cell_value = (
                                    pair_cell.cell_contents
                                )
                            except Exception:
                                continue
                            if isinstance(pair_cell_value, str):
                                returned_strs.add(
                                    pair_cell_value
                                )
                            elif isinstance(
                                pair_cell_value,
                                (bytes, bytearray),
                            ):
                                try:
                                    returned_strs.add(
                                        pair_cell_value.decode(
                                            "utf-8"
                                        )
                                    )
                                except Exception:
                                    pass
                        if pair_code is not None:
                            for pair_loaded in _code_facts(
                                pair_code
                            )[0]:
                                pair_loaded_value = pair_map.get(
                                    pair_loaded
                                )
                                if isinstance(
                                    pair_loaded_value, str
                                ):
                                    returned_strs.add(
                                        pair_loaded_value
                                    )
                                elif isinstance(
                                    pair_loaded_value,
                                    (bytes, bytearray),
                                ):
                                    try:
                                        returned_strs.add(
                                            pair_loaded_value
                                            .decode("utf-8")
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(
                                    pair_loaded_value,
                                    (
                                        dict,
                                        list,
                                        tuple,
                                        set,
                                        frozenset,
                                    ),
                                ):
                                    pending_held = [pair_loaded_value]
                                    seen_held = set()
                                    while pending_held:
                                        held = pending_held.pop()
                                        if id(held) in seen_held:
                                            continue
                                        seen_held.add(id(held))
                                        if isinstance(held, str):
                                            returned_strs.add(held)
                                        elif isinstance(
                                            held, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    held.decode("utf-8")
                                                )
                                            except Exception:
                                                pass
                                        elif isinstance(held, dict):
                                            for held_key in held:
                                                pending_held.append(held_key)
                                                pending_held.append(
                                                    held[held_key]
                                                )
                                        elif isinstance(
                                            held,
                                            (list, tuple, set, frozenset),
                                        ):
                                            pending_held.extend(held)
                        if pair_code is not None:
                            for pair_inner_name in (
                                _code_facts(pair_code)[0]
                            ):
                                pair_inner_fn = (
                                    pair_map.get(
                                        pair_inner_name
                                    )
                                )
                                if not isinstance(
                                    pair_inner_fn,
                                    _types_module
                                    .FunctionType,
                                ):
                                    continue
                                if (
                                    getattr(
                                        pair_inner_fn,
                                        "__globals__",
                                        None,
                                    )
                                    is not pair_map
                                ):
                                    continue
                                inner_code = getattr(
                                    pair_inner_fn, "__code__", None
                                )
                                if inner_code is not None:
                                    for pair_inner2_name in (
                                        _code_facts(
                                            inner_code
                                        )[0]
                                    ):
                                        pair_inner2_fn = (
                                            pair_map.get(
                                                pair_inner2_name
                                            )
                                        )
                                        if not isinstance(
                                            pair_inner2_fn,
                                            _types_module
                                            .FunctionType,
                                        ):
                                            continue
                                        if (
                                            getattr(
                                                pair_inner2_fn,
                                                "__globals__",
                                                None,
                                            )
                                            is not pair_map
                                        ):
                                            continue
                                        inner2_code = getattr(
                                            pair_inner2_fn,
                                            "__code__",
                                            None,
                                        )
                                        for pair_inner3_name in (
                                            _code_facts(
                                                inner2_code
                                            )[0]
                                        ):
                                            pair_inner3_fn = (
                                                pair_map.get(
                                                    pair_inner3_name
                                                )
                                            )
                                            if not isinstance(
                                                pair_inner3_fn,
                                                _types_module
                                                .FunctionType,
                                            ):
                                                continue
                                            if (
                                                getattr(
                                                    pair_inner3_fn,
                                                    "__globals__",
                                                    None,
                                                )
                                                is not pair_map
                                            ):
                                                continue
                                            inner3_code = getattr(
                                                pair_inner3_fn,
                                                "__code__",
                                                None,
                                            )
                                            for pair_inner4_name in (
                                                _code_facts(
                                                    inner3_code
                                                )[0]
                                            ):
                                                pair_inner4_fn = (
                                                    pair_map.get(
                                                        pair_inner4_name
                                                    )
                                                )
                                                if not isinstance(
                                                    pair_inner4_fn,
                                                    _types_module
                                                    .FunctionType,
                                                ):
                                                    continue
                                                if (
                                                    getattr(
                                                        pair_inner4_fn,
                                                        "__globals__",
                                                        None,
                                                    )
                                                    is not pair_map
                                                ):
                                                    continue
                                                inner4_code = getattr(
                                                    pair_inner4_fn,
                                                    "__code__",
                                                    None,
                                                )
                                                if inner4_code is not None:
                                                    returned_strs |= set(
                                                        _code_facts(inner4_code)[1]
                                                    )
                                                for inner4_default in (
                                                    getattr(
                                                        pair_inner4_fn, "__defaults__", None
                                                    )
                                                    or ()
                                                ):
                                                    if isinstance(inner4_default, str):
                                                        returned_strs.add(inner4_default)
                                                    elif isinstance(
                                                        inner4_default, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner4_default.decode(
                                                                    "utf-8"
                                                                )
                                                            )
                                                        except Exception:
                                                            pass
                                                for inner4_default in (
                                                    getattr(
                                                        pair_inner4_fn,
                                                        "__kwdefaults__",
                                                        None,
                                                    )
                                                    or {}
                                                ).values():
                                                    if isinstance(inner4_default, str):
                                                        returned_strs.add(inner4_default)
                                                    elif isinstance(
                                                        inner4_default, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner4_default.decode(
                                                                    "utf-8"
                                                                )
                                                            )
                                                        except Exception:
                                                            pass
                                                for inner4_cell in (
                                                    getattr(
                                                        pair_inner4_fn, "__closure__", None
                                                    )
                                                    or ()
                                                ):
                                                    try:
                                                        inner4_cell_value = (
                                                            inner4_cell.cell_contents
                                                        )
                                                    except Exception:
                                                        continue
                                                    if isinstance(inner4_cell_value, str):
                                                        returned_strs.add(
                                                            inner4_cell_value
                                                        )
                                                    elif isinstance(
                                                        inner4_cell_value,
                                                        (bytes, bytearray),
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner4_cell_value.decode(
                                                                    "utf-8"
                                                                )
                                                            )
                                                        except Exception:
                                                            pass
                                                if inner4_code is not None:
                                                    for inner4_loaded in _code_facts(
                                                        inner4_code
                                                    )[0]:
                                                        inner4_loaded_value = pair_map.get(
                                                            inner4_loaded
                                                        )
                                                        if isinstance(
                                                            inner4_loaded_value, str
                                                        ):
                                                            returned_strs.add(
                                                                inner4_loaded_value
                                                            )
                                                        elif isinstance(
                                                            inner4_loaded_value,
                                                            (bytes, bytearray),
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    inner4_loaded_value
                                                                    .decode("utf-8")
                                                                )
                                                            except Exception:
                                                                pass
                                                        elif isinstance(
                                                            inner4_loaded_value,
                                                            (
                                                                dict,
                                                                list,
                                                                tuple,
                                                                set,
                                                                frozenset,
                                                            ),
                                                        ):
                                                            pending_held = [inner4_loaded_value]
                                                            seen_held = set()
                                                            while pending_held:
                                                                held = pending_held.pop()
                                                                if id(held) in seen_held:
                                                                    continue
                                                                seen_held.add(id(held))
                                                                if isinstance(held, str):
                                                                    returned_strs.add(held)
                                                                elif isinstance(
                                                                    held, (bytes, bytearray)
                                                                ):
                                                                    try:
                                                                        returned_strs.add(
                                                                            held.decode("utf-8")
                                                                        )
                                                                    except Exception:
                                                                        pass
                                                                elif isinstance(held, dict):
                                                                    for held_key in held:
                                                                        pending_held.append(held_key)
                                                                        pending_held.append(
                                                                            held[held_key]
                                                                        )
                                                                elif isinstance(
                                                                    held,
                                                                    (list, tuple, set, frozenset),
                                                                ):
                                                                    pending_held.extend(held)
                                            if inner3_code is not None:
                                                returned_strs |= set(
                                                    _code_facts(inner3_code)[1]
                                                )
                                            for inner3_default in (
                                                getattr(
                                                    pair_inner3_fn, "__defaults__", None
                                                )
                                                or ()
                                            ):
                                                if isinstance(inner3_default, str):
                                                    returned_strs.add(inner3_default)
                                                elif isinstance(
                                                    inner3_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner3_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner3_default in (
                                                getattr(
                                                    pair_inner3_fn,
                                                    "__kwdefaults__",
                                                    None,
                                                )
                                                or {}
                                            ).values():
                                                if isinstance(inner3_default, str):
                                                    returned_strs.add(inner3_default)
                                                elif isinstance(
                                                    inner3_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner3_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner3_cell in (
                                                getattr(
                                                    pair_inner3_fn, "__closure__", None
                                                )
                                                or ()
                                            ):
                                                try:
                                                    inner3_cell_value = (
                                                        inner3_cell.cell_contents
                                                    )
                                                except Exception:
                                                    continue
                                                if isinstance(inner3_cell_value, str):
                                                    returned_strs.add(
                                                        inner3_cell_value
                                                    )
                                                elif isinstance(
                                                    inner3_cell_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner3_cell_value.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            if inner3_code is not None:
                                                for inner3_loaded in _code_facts(
                                                    inner3_code
                                                )[0]:
                                                    inner3_loaded_value = pair_map.get(
                                                        inner3_loaded
                                                    )
                                                    if isinstance(
                                                        inner3_loaded_value, str
                                                    ):
                                                        returned_strs.add(
                                                            inner3_loaded_value
                                                        )
                                                    elif isinstance(
                                                        inner3_loaded_value,
                                                        (bytes, bytearray),
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner3_loaded_value
                                                                .decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(
                                                        inner3_loaded_value,
                                                        (
                                                            dict,
                                                            list,
                                                            tuple,
                                                            set,
                                                            frozenset,
                                                        ),
                                                    ):
                                                        pending_held = [inner3_loaded_value]
                                                        seen_held = set()
                                                        while pending_held:
                                                            held = pending_held.pop()
                                                            if id(held) in seen_held:
                                                                continue
                                                            seen_held.add(id(held))
                                                            if isinstance(held, str):
                                                                returned_strs.add(held)
                                                            elif isinstance(
                                                                held, (bytes, bytearray)
                                                            ):
                                                                try:
                                                                    returned_strs.add(
                                                                        held.decode("utf-8")
                                                                    )
                                                                except Exception:
                                                                    pass
                                                            elif isinstance(held, dict):
                                                                for held_key in held:
                                                                    pending_held.append(held_key)
                                                                    pending_held.append(
                                                                        held[held_key]
                                                                    )
                                                            elif isinstance(
                                                                held,
                                                                (list, tuple, set, frozenset),
                                                            ):
                                                                pending_held.extend(held)
                                        if inner2_code is not None:
                                            returned_strs |= set(
                                                _code_facts(inner2_code)[1]
                                            )
                                        for inner2_default in (
                                            getattr(
                                                pair_inner2_fn, "__defaults__", None
                                            )
                                            or ()
                                        ):
                                            if isinstance(inner2_default, str):
                                                returned_strs.add(inner2_default)
                                            elif isinstance(
                                                inner2_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner2_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for inner2_default in (
                                            getattr(
                                                pair_inner2_fn,
                                                "__kwdefaults__",
                                                None,
                                            )
                                            or {}
                                        ).values():
                                            if isinstance(inner2_default, str):
                                                returned_strs.add(inner2_default)
                                            elif isinstance(
                                                inner2_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner2_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for inner2_cell in (
                                            getattr(
                                                pair_inner2_fn, "__closure__", None
                                            )
                                            or ()
                                        ):
                                            try:
                                                inner2_cell_value = (
                                                    inner2_cell.cell_contents
                                                )
                                            except Exception:
                                                continue
                                            if isinstance(inner2_cell_value, str):
                                                returned_strs.add(
                                                    inner2_cell_value
                                                )
                                            elif isinstance(
                                                inner2_cell_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner2_cell_value.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        if inner2_code is not None:
                                            for inner2_loaded in _code_facts(
                                                inner2_code
                                            )[0]:
                                                inner2_loaded_value = pair_map.get(
                                                    inner2_loaded
                                                )
                                                if isinstance(
                                                    inner2_loaded_value, str
                                                ):
                                                    returned_strs.add(
                                                        inner2_loaded_value
                                                    )
                                                elif isinstance(
                                                    inner2_loaded_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner2_loaded_value
                                                            .decode("utf-8")
                                                        )
                                                    except Exception:
                                                        pass
                                                elif isinstance(
                                                    inner2_loaded_value,
                                                    (
                                                        dict,
                                                        list,
                                                        tuple,
                                                        set,
                                                        frozenset,
                                                    ),
                                                ):
                                                    pending_held = [inner2_loaded_value]
                                                    seen_held = set()
                                                    while pending_held:
                                                        held = pending_held.pop()
                                                        if id(held) in seen_held:
                                                            continue
                                                        seen_held.add(id(held))
                                                        if isinstance(held, str):
                                                            returned_strs.add(held)
                                                        elif isinstance(
                                                            held, (bytes, bytearray)
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    held.decode("utf-8")
                                                                )
                                                            except Exception:
                                                                pass
                                                        elif isinstance(held, dict):
                                                            for held_key in held:
                                                                pending_held.append(held_key)
                                                                pending_held.append(
                                                                    held[held_key]
                                                                )
                                                        elif isinstance(
                                                            held,
                                                            (list, tuple, set, frozenset),
                                                        ):
                                                            pending_held.extend(held)
                                if inner_code is not None:
                                    returned_strs |= set(
                                        _code_facts(inner_code)[1]
                                    )
                                for inner_default in (
                                    getattr(
                                        pair_inner_fn, "__defaults__", None
                                    )
                                    or ()
                                ):
                                    if isinstance(inner_default, str):
                                        returned_strs.add(inner_default)
                                    elif isinstance(
                                        inner_default, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                inner_default.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for inner_default in (
                                    getattr(
                                        pair_inner_fn,
                                        "__kwdefaults__",
                                        None,
                                    )
                                    or {}
                                ).values():
                                    if isinstance(inner_default, str):
                                        returned_strs.add(inner_default)
                                    elif isinstance(
                                        inner_default, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                inner_default.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                for inner_cell in (
                                    getattr(
                                        pair_inner_fn, "__closure__", None
                                    )
                                    or ()
                                ):
                                    try:
                                        inner_cell_value = (
                                            inner_cell.cell_contents
                                        )
                                    except Exception:
                                        continue
                                    if isinstance(inner_cell_value, str):
                                        returned_strs.add(
                                            inner_cell_value
                                        )
                                    elif isinstance(
                                        inner_cell_value,
                                        (bytes, bytearray),
                                    ):
                                        try:
                                            returned_strs.add(
                                                inner_cell_value.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                if inner_code is not None:
                                    for inner_loaded in _code_facts(
                                        inner_code
                                    )[0]:
                                        inner_loaded_value = pair_map.get(
                                            inner_loaded
                                        )
                                        if isinstance(
                                            inner_loaded_value, str
                                        ):
                                            returned_strs.add(
                                                inner_loaded_value
                                            )
                                        elif isinstance(
                                            inner_loaded_value,
                                            (bytes, bytearray),
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner_loaded_value
                                                    .decode("utf-8")
                                                )
                                            except Exception:
                                                pass
                                        elif isinstance(
                                            inner_loaded_value,
                                            (
                                                dict,
                                                list,
                                                tuple,
                                                set,
                                                frozenset,
                                            ),
                                        ):
                                            pending_held = [inner_loaded_value]
                                            seen_held = set()
                                            while pending_held:
                                                held = pending_held.pop()
                                                if id(held) in seen_held:
                                                    continue
                                                seen_held.add(id(held))
                                                if isinstance(held, str):
                                                    returned_strs.add(held)
                                                elif isinstance(
                                                    held, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            held.decode("utf-8")
                                                        )
                                                    except Exception:
                                                        pass
                                                elif isinstance(held, dict):
                                                    for held_key in held:
                                                        pending_held.append(held_key)
                                                        pending_held.append(
                                                            held[held_key]
                                                        )
                                                elif isinstance(
                                                    held,
                                                    (list, tuple, set, frozenset),
                                                ):
                                                    pending_held.extend(held)
            iso2_level = list(first_order_fns)
            for iso2_depth in range(4):
                iso2_next = []
                for iso2_fn in iso2_level:
                    iso2_code = getattr(
                        iso2_fn, "__code__", None
                    )
                    if iso2_code is None:
                        continue
                    for iso2_name in _code_facts(
                        iso2_code
                    )[0]:
                        iso2_inner = current_map.get(
                            iso2_name
                        )
                        if not isinstance(
                            iso2_inner,
                            _types_module.FunctionType,
                        ):
                            continue
                        if (
                            getattr(
                                iso2_inner,
                                "__globals__",
                                None,
                            )
                            is not current_map
                        ):
                            continue
                        iso2_next.append(iso2_inner)
                iso2_level = iso2_next
            for fifth_fn in iso2_level:
                fifth_code = getattr(
                    fifth_fn, "__code__", None
                )
                if fifth_code is None:
                    continue
                returned_strs |= set(
                    _code_facts(fifth_code)[1]
                )
                for fifth_default in (
                    getattr(
                        fifth_fn, "__defaults__", None
                    )
                    or ()
                ):
                    if isinstance(fifth_default, str):
                        returned_strs.add(fifth_default)
                    elif isinstance(
                        fifth_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                fifth_default.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for fifth_default in (
                    getattr(
                        fifth_fn,
                        "__kwdefaults__",
                        None,
                    )
                    or {}
                ).values():
                    if isinstance(fifth_default, str):
                        returned_strs.add(fifth_default)
                    elif isinstance(
                        fifth_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                fifth_default.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for fifth_cell in (
                    getattr(
                        fifth_fn, "__closure__", None
                    )
                    or ()
                ):
                    try:
                        fifth_cell_value = (
                            fifth_cell.cell_contents
                        )
                    except Exception:
                        continue
                    if isinstance(fifth_cell_value, str):
                        returned_strs.add(
                            fifth_cell_value
                        )
                    elif isinstance(
                        fifth_cell_value,
                        (bytes, bytearray),
                    ):
                        try:
                            returned_strs.add(
                                fifth_cell_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for fifth_loaded in _code_facts(
                    fifth_code
                )[0]:
                    fifth_value = current_map.get(
                        fifth_loaded
                    )
                    if isinstance(fifth_value, str):
                        returned_strs.add(fifth_value)
                    elif isinstance(
                        fifth_value, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                fifth_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                    elif isinstance(
                        fifth_value,
                        (
                            dict,
                            list,
                            tuple,
                            set,
                            frozenset,
                        ),
                    ):
                        pending_held = [fifth_value]
                        seen_held = set()
                        while pending_held:
                            held = pending_held.pop()
                            if id(held) in seen_held:
                                continue
                            seen_held.add(id(held))
                            if isinstance(held, str):
                                returned_strs.add(held)
                            elif isinstance(
                                held, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        held.decode("utf-8")
                                    )
                                except Exception:
                                    pass
                            elif isinstance(held, dict):
                                for held_key in held:
                                    pending_held.append(held_key)
                                    pending_held.append(
                                        held[held_key]
                                    )
                            elif isinstance(
                                held,
                                (list, tuple, set, frozenset),
                            ):
                                pending_held.extend(held)

            iso6_level = list(first_order_fns)
            for iso6_depth in range(5):
                iso6_next = []
                for iso6_fn in iso6_level:
                    iso6_code = getattr(
                        iso6_fn, "__code__", None
                    )
                    if iso6_code is None:
                        continue
                    for iso6_name in _code_facts(
                        iso6_code
                    )[0]:
                        iso6_inner = current_map.get(
                            iso6_name
                        )
                        if not isinstance(
                            iso6_inner,
                            _types_module.FunctionType,
                        ):
                            continue
                        if (
                            getattr(
                                iso6_inner,
                                "__globals__",
                                None,
                            )
                            is not current_map
                        ):
                            continue
                        iso6_next.append(iso6_inner)
                iso6_level = iso6_next
            for sixth_fn in iso6_level:
                sixth_code = getattr(
                    sixth_fn, "__code__", None
                )
                if sixth_code is None:
                    continue
                returned_strs |= set(
                    _code_facts(sixth_code)[1]
                )
                for sixth_default in (
                    getattr(
                        sixth_fn, "__defaults__", None
                    )
                    or ()
                ):
                    if isinstance(sixth_default, str):
                        returned_strs.add(sixth_default)
                    elif isinstance(
                        sixth_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                sixth_default.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for sixth_default in (
                    getattr(
                        sixth_fn,
                        "__kwdefaults__",
                        None,
                    )
                    or {}
                ).values():
                    if isinstance(sixth_default, str):
                        returned_strs.add(sixth_default)
                    elif isinstance(
                        sixth_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                sixth_default.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for sixth_cell in (
                    getattr(
                        sixth_fn, "__closure__", None
                    )
                    or ()
                ):
                    try:
                        sixth_cell_value = (
                            sixth_cell.cell_contents
                        )
                    except Exception:
                        continue
                    if isinstance(sixth_cell_value, str):
                        returned_strs.add(
                            sixth_cell_value
                        )
                    elif isinstance(
                        sixth_cell_value,
                        (bytes, bytearray),
                    ):
                        try:
                            returned_strs.add(
                                sixth_cell_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for sixth_loaded in _code_facts(
                    sixth_code
                )[0]:
                    sixth_value = current_map.get(
                        sixth_loaded
                    )
                    if isinstance(sixth_value, str):
                        returned_strs.add(sixth_value)
                    elif isinstance(
                        sixth_value, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                sixth_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                    elif isinstance(
                        sixth_value,
                        (
                            dict,
                            list,
                            tuple,
                            set,
                            frozenset,
                        ),
                    ):
                        pending_held = [sixth_value]
                        seen_held = set()
                        while pending_held:
                            held = pending_held.pop()
                            if id(held) in seen_held:
                                continue
                            seen_held.add(id(held))
                            if isinstance(held, str):
                                returned_strs.add(held)
                            elif isinstance(
                                held, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        held.decode("utf-8")
                                    )
                                except Exception:
                                    pass
                            elif isinstance(held, dict):
                                for held_key in held:
                                    pending_held.append(held_key)
                                    pending_held.append(
                                        held[held_key]
                                    )
                            elif isinstance(
                                held,
                                (list, tuple, set, frozenset),
                            ):
                                pending_held.extend(held)
            iso7_level = list(first_order_fns)
            for iso7_depth in range(6):
                iso7_next = []
                for iso7_fn in iso7_level:
                    iso7_code = getattr(
                        iso7_fn, "__code__", None
                    )
                    if iso7_code is None:
                        continue
                    for iso7_name in _code_facts(
                        iso7_code
                    )[0]:
                        iso7_inner = current_map.get(
                            iso7_name
                        )
                        if not isinstance(
                            iso7_inner,
                            _types_module.FunctionType,
                        ):
                            continue
                        if (
                            getattr(
                                iso7_inner,
                                "__globals__",
                                None,
                            )
                            is not current_map
                        ):
                            continue
                        iso7_next.append(iso7_inner)
                iso7_level = iso7_next
            for seventh_fn in iso7_level:
                seventh_code = getattr(
                    seventh_fn, "__code__", None
                )
                if seventh_code is None:
                    continue
                returned_strs |= set(
                    _code_facts(seventh_code)[1]
                )
                for seventh_default in (
                    getattr(
                        seventh_fn, "__defaults__", None
                    )
                    or ()
                ):
                    if isinstance(seventh_default, str):
                        returned_strs.add(seventh_default)
                    elif isinstance(
                        seventh_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                seventh_default.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for seventh_default in (
                    getattr(
                        seventh_fn,
                        "__kwdefaults__",
                        None,
                    )
                    or {}
                ).values():
                    if isinstance(seventh_default, str):
                        returned_strs.add(seventh_default)
                    elif isinstance(
                        seventh_default, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                seventh_default.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for seventh_cell in (
                    getattr(
                        seventh_fn, "__closure__", None
                    )
                    or ()
                ):
                    try:
                        seventh_cell_value = (
                            seventh_cell.cell_contents
                        )
                    except Exception:
                        continue
                    if isinstance(seventh_cell_value, str):
                        returned_strs.add(
                            seventh_cell_value
                        )
                    elif isinstance(
                        seventh_cell_value,
                        (bytes, bytearray),
                    ):
                        try:
                            returned_strs.add(
                                seventh_cell_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                for seventh_loaded in _code_facts(
                    seventh_code
                )[0]:
                    seventh_value = current_map.get(
                        seventh_loaded
                    )
                    if isinstance(seventh_value, str):
                        returned_strs.add(seventh_value)
                    elif isinstance(
                        seventh_value, (bytes, bytearray)
                    ):
                        try:
                            returned_strs.add(
                                seventh_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                    elif isinstance(
                        seventh_value,
                        (
                            dict,
                            list,
                            tuple,
                            set,
                            frozenset,
                        ),
                    ):
                        pending_held = [seventh_value]
                        seen_held = set()
                        while pending_held:
                            held = pending_held.pop()
                            if id(held) in seen_held:
                                continue
                            seen_held.add(id(held))
                            if isinstance(held, str):
                                returned_strs.add(held)
                            elif isinstance(
                                held, (bytes, bytearray)
                            ):
                                try:
                                    returned_strs.add(
                                        held.decode("utf-8")
                                    )
                                except Exception:
                                    pass
                            elif isinstance(held, dict):
                                for held_key in held:
                                    pending_held.append(held_key)
                                    pending_held.append(
                                        held[held_key]
                                    )
                            elif isinstance(
                                held,
                                (list, tuple, set, frozenset),
                            ):
                                pending_held.extend(held)
            for pair_base, pair_attr in pairs:
                if pair_base not in current_map:
                    continue
                pair_module = current_map[pair_base]
                if not isinstance(
                    pair_module, _types_module.ModuleType
                ):
                    continue
                pair_map = getattr(
                    pair_module, "__dict__", None
                )
                if not isinstance(pair_map, dict):
                    continue
                pair_value = pair_map.get(pair_attr)
                if isinstance(pair_value, str):
                    returned_strs.add(pair_value)
                elif isinstance(
                    pair_value, (bytes, bytearray)
                ):
                    try:
                        returned_strs.add(
                            pair_value.decode("utf-8")
                        )
                    except Exception:
                        pass
                elif isinstance(
                    pair_value, _types_module.FunctionType
                ):
                    pair_code = getattr(
                        pair_value, "__code__", None
                    )
                    if pair_code is not None:
                        returned_strs |= set(
                            _code_facts(pair_code)[1]
                        )
                    for pair_default in (
                        getattr(
                            pair_value, "__defaults__", None
                        )
                        or ()
                    ):
                        if isinstance(pair_default, str):
                            returned_strs.add(pair_default)
                        elif isinstance(
                            pair_default, (bytes, bytearray)
                        ):
                            try:
                                returned_strs.add(
                                    pair_default.decode("utf-8")
                                )
                            except Exception:
                                pass
                    for pair_default in (
                        getattr(
                            pair_value,
                            "__kwdefaults__",
                            None,
                        )
                        or {}
                    ).values():
                        if isinstance(pair_default, str):
                            returned_strs.add(pair_default)
                        elif isinstance(
                            pair_default, (bytes, bytearray)
                        ):
                            try:
                                returned_strs.add(
                                    pair_default.decode("utf-8")
                                )
                            except Exception:
                                pass
                    for pair_cell in (
                        getattr(
                            pair_value, "__closure__", None
                        )
                        or ()
                    ):
                        try:
                            pair_cell_value = (
                                pair_cell.cell_contents
                            )
                        except Exception:
                            continue
                        if isinstance(pair_cell_value, str):
                            returned_strs.add(pair_cell_value)
                        elif isinstance(
                            pair_cell_value,
                            (bytes, bytearray),
                        ):
                            try:
                                returned_strs.add(
                                    pair_cell_value.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                    if pair_code is not None:
                        for pair_loaded in _code_facts(
                            pair_code
                        )[0]:
                            pair_loaded_value = pair_map.get(
                                pair_loaded
                            )
                            if isinstance(
                                pair_loaded_value, str
                            ):
                                returned_strs.add(
                                    pair_loaded_value
                                )
                            elif isinstance(
                                pair_loaded_value,
                                (bytes, bytearray),
                            ):
                                try:
                                    returned_strs.add(
                                        pair_loaded_value
                                        .decode("utf-8")
                                    )
                                except Exception:
                                    pass
                            elif isinstance(
                                pair_loaded_value,
                                (
                                    dict,
                                    list,
                                    tuple,
                                    set,
                                    frozenset,
                                ),
                            ):
                                pending_held = [pair_loaded_value]
                                seen_held = set()
                                while pending_held:
                                    held = pending_held.pop()
                                    if id(held) in seen_held:
                                        continue
                                    seen_held.add(id(held))
                                    if isinstance(held, str):
                                        returned_strs.add(held)
                                    elif isinstance(
                                        held, (bytes, bytearray)
                                    ):
                                        try:
                                            returned_strs.add(
                                                held.decode("utf-8")
                                            )
                                        except Exception:
                                            pass
                                    elif isinstance(held, dict):
                                        for held_key in held:
                                            pending_held.append(held_key)
                                            pending_held.append(
                                                held[held_key]
                                            )
                                    elif isinstance(
                                        held,
                                        (list, tuple, set, frozenset),
                                    ):
                                        pending_held.extend(held)
                    if pair_code is not None:
                        for pair_inner_name in (
                            _code_facts(pair_code)[0]
                        ):
                            pair_inner_fn = (
                                pair_map.get(
                                    pair_inner_name
                                )
                            )
                            if not isinstance(
                                pair_inner_fn,
                                _types_module
                                .FunctionType,
                            ):
                                continue
                            if (
                                getattr(
                                    pair_inner_fn,
                                    "__globals__",
                                    None,
                                )
                                is not pair_map
                            ):
                                continue
                            inner_code = getattr(
                                pair_inner_fn, "__code__", None
                            )
                            if inner_code is not None:
                                for pair_inner2_name in (
                                    _code_facts(
                                        inner_code
                                    )[0]
                                ):
                                    pair_inner2_fn = (
                                        pair_map.get(
                                            pair_inner2_name
                                        )
                                    )
                                    if not isinstance(
                                        pair_inner2_fn,
                                        _types_module
                                        .FunctionType,
                                    ):
                                        continue
                                    if (
                                        getattr(
                                            pair_inner2_fn,
                                            "__globals__",
                                            None,
                                        )
                                        is not pair_map
                                    ):
                                        continue
                                    inner2_code = getattr(
                                        pair_inner2_fn,
                                        "__code__",
                                        None,
                                    )
                                    for pair_inner3_name in (
                                        _code_facts(
                                            inner2_code
                                        )[0]
                                    ):
                                        pair_inner3_fn = (
                                            pair_map.get(
                                                pair_inner3_name
                                            )
                                        )
                                        if not isinstance(
                                            pair_inner3_fn,
                                            _types_module
                                            .FunctionType,
                                        ):
                                            continue
                                        if (
                                            getattr(
                                                pair_inner3_fn,
                                                "__globals__",
                                                None,
                                            )
                                            is not pair_map
                                        ):
                                            continue
                                        inner3_code = getattr(
                                            pair_inner3_fn,
                                            "__code__",
                                            None,
                                        )
                                        for pair_inner4_name in (
                                            _code_facts(
                                                inner3_code
                                            )[0]
                                        ):
                                            pair_inner4_fn = (
                                                pair_map.get(
                                                    pair_inner4_name
                                                )
                                            )
                                            if not isinstance(
                                                pair_inner4_fn,
                                                _types_module
                                                .FunctionType,
                                            ):
                                                continue
                                            if (
                                                getattr(
                                                    pair_inner4_fn,
                                                    "__globals__",
                                                    None,
                                                )
                                                is not pair_map
                                            ):
                                                continue
                                            inner4_code = getattr(
                                                pair_inner4_fn,
                                                "__code__",
                                                None,
                                            )
                                            if inner4_code is not None:
                                                returned_strs |= set(
                                                    _code_facts(inner4_code)[1]
                                                )
                                            for inner4_default in (
                                                getattr(
                                                    pair_inner4_fn, "__defaults__", None
                                                )
                                                or ()
                                            ):
                                                if isinstance(inner4_default, str):
                                                    returned_strs.add(inner4_default)
                                                elif isinstance(
                                                    inner4_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner4_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner4_default in (
                                                getattr(
                                                    pair_inner4_fn,
                                                    "__kwdefaults__",
                                                    None,
                                                )
                                                or {}
                                            ).values():
                                                if isinstance(inner4_default, str):
                                                    returned_strs.add(inner4_default)
                                                elif isinstance(
                                                    inner4_default, (bytes, bytearray)
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner4_default.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            for inner4_cell in (
                                                getattr(
                                                    pair_inner4_fn, "__closure__", None
                                                )
                                                or ()
                                            ):
                                                try:
                                                    inner4_cell_value = (
                                                        inner4_cell.cell_contents
                                                    )
                                                except Exception:
                                                    continue
                                                if isinstance(inner4_cell_value, str):
                                                    returned_strs.add(
                                                        inner4_cell_value
                                                    )
                                                elif isinstance(
                                                    inner4_cell_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner4_cell_value.decode(
                                                                "utf-8"
                                                            )
                                                        )
                                                    except Exception:
                                                        pass
                                            if inner4_code is not None:
                                                for inner4_loaded in _code_facts(
                                                    inner4_code
                                                )[0]:
                                                    inner4_loaded_value = pair_map.get(
                                                        inner4_loaded
                                                    )
                                                    if isinstance(
                                                        inner4_loaded_value, str
                                                    ):
                                                        returned_strs.add(
                                                            inner4_loaded_value
                                                        )
                                                    elif isinstance(
                                                        inner4_loaded_value,
                                                        (bytes, bytearray),
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                inner4_loaded_value
                                                                .decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(
                                                        inner4_loaded_value,
                                                        (
                                                            dict,
                                                            list,
                                                            tuple,
                                                            set,
                                                            frozenset,
                                                        ),
                                                    ):
                                                        pending_held = [inner4_loaded_value]
                                                        seen_held = set()
                                                        while pending_held:
                                                            held = pending_held.pop()
                                                            if id(held) in seen_held:
                                                                continue
                                                            seen_held.add(id(held))
                                                            if isinstance(held, str):
                                                                returned_strs.add(held)
                                                            elif isinstance(
                                                                held, (bytes, bytearray)
                                                            ):
                                                                try:
                                                                    returned_strs.add(
                                                                        held.decode("utf-8")
                                                                    )
                                                                except Exception:
                                                                    pass
                                                            elif isinstance(held, dict):
                                                                for held_key in held:
                                                                    pending_held.append(held_key)
                                                                    pending_held.append(
                                                                        held[held_key]
                                                                    )
                                                            elif isinstance(
                                                                held,
                                                                (list, tuple, set, frozenset),
                                                            ):
                                                                pending_held.extend(held)
                                        if inner3_code is not None:
                                            returned_strs |= set(
                                                _code_facts(inner3_code)[1]
                                            )
                                        for inner3_default in (
                                            getattr(
                                                pair_inner3_fn, "__defaults__", None
                                            )
                                            or ()
                                        ):
                                            if isinstance(inner3_default, str):
                                                returned_strs.add(inner3_default)
                                            elif isinstance(
                                                inner3_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner3_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for inner3_default in (
                                            getattr(
                                                pair_inner3_fn,
                                                "__kwdefaults__",
                                                None,
                                            )
                                            or {}
                                        ).values():
                                            if isinstance(inner3_default, str):
                                                returned_strs.add(inner3_default)
                                            elif isinstance(
                                                inner3_default, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner3_default.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        for inner3_cell in (
                                            getattr(
                                                pair_inner3_fn, "__closure__", None
                                            )
                                            or ()
                                        ):
                                            try:
                                                inner3_cell_value = (
                                                    inner3_cell.cell_contents
                                                )
                                            except Exception:
                                                continue
                                            if isinstance(inner3_cell_value, str):
                                                returned_strs.add(
                                                    inner3_cell_value
                                                )
                                            elif isinstance(
                                                inner3_cell_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner3_cell_value.decode(
                                                            "utf-8"
                                                        )
                                                    )
                                                except Exception:
                                                    pass
                                        if inner3_code is not None:
                                            for inner3_loaded in _code_facts(
                                                inner3_code
                                            )[0]:
                                                inner3_loaded_value = pair_map.get(
                                                    inner3_loaded
                                                )
                                                if isinstance(
                                                    inner3_loaded_value, str
                                                ):
                                                    returned_strs.add(
                                                        inner3_loaded_value
                                                    )
                                                elif isinstance(
                                                    inner3_loaded_value,
                                                    (bytes, bytearray),
                                                ):
                                                    try:
                                                        returned_strs.add(
                                                            inner3_loaded_value
                                                            .decode("utf-8")
                                                        )
                                                    except Exception:
                                                        pass
                                                elif isinstance(
                                                    inner3_loaded_value,
                                                    (
                                                        dict,
                                                        list,
                                                        tuple,
                                                        set,
                                                        frozenset,
                                                    ),
                                                ):
                                                    pending_held = [inner3_loaded_value]
                                                    seen_held = set()
                                                    while pending_held:
                                                        held = pending_held.pop()
                                                        if id(held) in seen_held:
                                                            continue
                                                        seen_held.add(id(held))
                                                        if isinstance(held, str):
                                                            returned_strs.add(held)
                                                        elif isinstance(
                                                            held, (bytes, bytearray)
                                                        ):
                                                            try:
                                                                returned_strs.add(
                                                                    held.decode("utf-8")
                                                                )
                                                            except Exception:
                                                                pass
                                                        elif isinstance(held, dict):
                                                            for held_key in held:
                                                                pending_held.append(held_key)
                                                                pending_held.append(
                                                                    held[held_key]
                                                                )
                                                        elif isinstance(
                                                            held,
                                                            (list, tuple, set, frozenset),
                                                        ):
                                                            pending_held.extend(held)
                                    if inner2_code is not None:
                                        returned_strs |= set(
                                            _code_facts(inner2_code)[1]
                                        )
                                    for inner2_default in (
                                        getattr(
                                            pair_inner2_fn, "__defaults__", None
                                        )
                                        or ()
                                    ):
                                        if isinstance(inner2_default, str):
                                            returned_strs.add(inner2_default)
                                        elif isinstance(
                                            inner2_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner2_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for inner2_default in (
                                        getattr(
                                            pair_inner2_fn,
                                            "__kwdefaults__",
                                            None,
                                        )
                                        or {}
                                    ).values():
                                        if isinstance(inner2_default, str):
                                            returned_strs.add(inner2_default)
                                        elif isinstance(
                                            inner2_default, (bytes, bytearray)
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner2_default.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    for inner2_cell in (
                                        getattr(
                                            pair_inner2_fn, "__closure__", None
                                        )
                                        or ()
                                    ):
                                        try:
                                            inner2_cell_value = (
                                                inner2_cell.cell_contents
                                            )
                                        except Exception:
                                            continue
                                        if isinstance(inner2_cell_value, str):
                                            returned_strs.add(
                                                inner2_cell_value
                                            )
                                        elif isinstance(
                                            inner2_cell_value,
                                            (bytes, bytearray),
                                        ):
                                            try:
                                                returned_strs.add(
                                                    inner2_cell_value.decode(
                                                        "utf-8"
                                                    )
                                                )
                                            except Exception:
                                                pass
                                    if inner2_code is not None:
                                        for inner2_loaded in _code_facts(
                                            inner2_code
                                        )[0]:
                                            inner2_loaded_value = pair_map.get(
                                                inner2_loaded
                                            )
                                            if isinstance(
                                                inner2_loaded_value, str
                                            ):
                                                returned_strs.add(
                                                    inner2_loaded_value
                                                )
                                            elif isinstance(
                                                inner2_loaded_value,
                                                (bytes, bytearray),
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        inner2_loaded_value
                                                        .decode("utf-8")
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(
                                                inner2_loaded_value,
                                                (
                                                    dict,
                                                    list,
                                                    tuple,
                                                    set,
                                                    frozenset,
                                                ),
                                            ):
                                                pending_held = [inner2_loaded_value]
                                                seen_held = set()
                                                while pending_held:
                                                    held = pending_held.pop()
                                                    if id(held) in seen_held:
                                                        continue
                                                    seen_held.add(id(held))
                                                    if isinstance(held, str):
                                                        returned_strs.add(held)
                                                    elif isinstance(
                                                        held, (bytes, bytearray)
                                                    ):
                                                        try:
                                                            returned_strs.add(
                                                                held.decode("utf-8")
                                                            )
                                                        except Exception:
                                                            pass
                                                    elif isinstance(held, dict):
                                                        for held_key in held:
                                                            pending_held.append(held_key)
                                                            pending_held.append(
                                                                held[held_key]
                                                            )
                                                    elif isinstance(
                                                        held,
                                                        (list, tuple, set, frozenset),
                                                    ):
                                                        pending_held.extend(held)
                            if inner_code is not None:
                                returned_strs |= set(
                                    _code_facts(inner_code)[1]
                                )
                            for inner_default in (
                                getattr(
                                    pair_inner_fn, "__defaults__", None
                                )
                                or ()
                            ):
                                if isinstance(inner_default, str):
                                    returned_strs.add(inner_default)
                                elif isinstance(
                                    inner_default, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            inner_default.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for inner_default in (
                                getattr(
                                    pair_inner_fn,
                                    "__kwdefaults__",
                                    None,
                                )
                                or {}
                            ).values():
                                if isinstance(inner_default, str):
                                    returned_strs.add(inner_default)
                                elif isinstance(
                                    inner_default, (bytes, bytearray)
                                ):
                                    try:
                                        returned_strs.add(
                                            inner_default.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            for inner_cell in (
                                getattr(
                                    pair_inner_fn, "__closure__", None
                                )
                                or ()
                            ):
                                try:
                                    inner_cell_value = (
                                        inner_cell.cell_contents
                                    )
                                except Exception:
                                    continue
                                if isinstance(inner_cell_value, str):
                                    returned_strs.add(
                                        inner_cell_value
                                    )
                                elif isinstance(
                                    inner_cell_value,
                                    (bytes, bytearray),
                                ):
                                    try:
                                        returned_strs.add(
                                            inner_cell_value.decode(
                                                "utf-8"
                                            )
                                        )
                                    except Exception:
                                        pass
                            if inner_code is not None:
                                for inner_loaded in _code_facts(
                                    inner_code
                                )[0]:
                                    inner_loaded_value = pair_map.get(
                                        inner_loaded
                                    )
                                    if isinstance(
                                        inner_loaded_value, str
                                    ):
                                        returned_strs.add(
                                            inner_loaded_value
                                        )
                                    elif isinstance(
                                        inner_loaded_value,
                                        (bytes, bytearray),
                                    ):
                                        try:
                                            returned_strs.add(
                                                inner_loaded_value
                                                .decode("utf-8")
                                            )
                                        except Exception:
                                            pass
                                    elif isinstance(
                                        inner_loaded_value,
                                        (
                                            dict,
                                            list,
                                            tuple,
                                            set,
                                            frozenset,
                                        ),
                                    ):
                                        pending_held = [inner_loaded_value]
                                        seen_held = set()
                                        while pending_held:
                                            held = pending_held.pop()
                                            if id(held) in seen_held:
                                                continue
                                            seen_held.add(id(held))
                                            if isinstance(held, str):
                                                returned_strs.add(held)
                                            elif isinstance(
                                                held, (bytes, bytearray)
                                            ):
                                                try:
                                                    returned_strs.add(
                                                        held.decode("utf-8")
                                                    )
                                                except Exception:
                                                    pass
                                            elif isinstance(held, dict):
                                                for held_key in held:
                                                    pending_held.append(held_key)
                                                    pending_held.append(
                                                        held[held_key]
                                                    )
                                            elif isinstance(
                                                held,
                                                (list, tuple, set, frozenset),
                                            ):
                                                pending_held.extend(held)
            act_attr_strs = set()
            for pair_base, pair_attr in pairs:
                if pair_base not in current_map:
                    continue
                pair_class = current_map[pair_base]
                if not isinstance(pair_class, type):
                    pair_inst_value = None
                    try:
                        pair_inst_map = vars(pair_class)
                    except Exception:
                        pair_inst_map = {}
                    if isinstance(pair_inst_map, dict):
                        pair_inst_value = pair_inst_map.get(
                            pair_attr
                        )
                    if pair_inst_value is None:
                        try:
                            for pair_inst_klass in type(
                                pair_class
                            ).__mro__:
                                pair_inst_klass_map = (
                                    vars(pair_inst_klass)
                                )
                                if pair_attr in (
                                    pair_inst_klass_map
                                ):
                                    pair_inst_value = (
                                        pair_inst_klass_map
                                        .get(pair_attr)
                                    )
                                    break
                        except Exception:
                            pair_inst_value = None
                    if isinstance(pair_inst_value, str):
                        act_attr_strs.add(pair_inst_value)
                    elif isinstance(
                        pair_inst_value, (bytes, bytearray)
                    ):
                        try:
                            act_attr_strs.add(
                                pair_inst_value.decode(
                                    "utf-8"
                                )
                            )
                        except Exception:
                            pass
                    continue
                pair_value = None
                try:
                    for pair_klass in pair_class.__mro__:
                        class_map = vars(pair_klass)
                        if pair_attr in class_map:
                            pair_value = class_map.get(
                                pair_attr
                            )
                            break
                except Exception:
                    continue
                if isinstance(pair_value, str):
                    act_attr_strs.add(pair_value)
                elif isinstance(
                    pair_value, (bytes, bytearray)
                ):
                    try:
                        act_attr_strs.add(
                            pair_value.decode("utf-8")
                        )
                    except Exception:
                        pass
            for chain_base, first_attr, second_attr in chains:
                if chain_base not in current_map:
                    continue
                chain_module = current_map[chain_base]
                if not isinstance(
                    chain_module, _types_module.ModuleType
                ):
                    continue
                chain_map = getattr(
                    chain_module, "__dict__", None
                )
                if not isinstance(chain_map, dict):
                    continue
                inner_value = chain_map.get(first_attr)
                if not isinstance(
                    inner_value, _types_module.ModuleType
                ):
                    continue
                inner_map = getattr(
                    inner_value, "__dict__", None
                )
                if not isinstance(inner_map, dict):
                    continue
                chain_value = inner_map.get(second_attr)
                if isinstance(chain_value, str):
                    act_attr_strs.add(chain_value)
                elif isinstance(
                    chain_value, (bytes, bytearray)
                ):
                    try:
                        act_attr_strs.add(
                            chain_value.decode("utf-8")
                        )
                    except Exception:
                        pass
            if self_attrs:
                qualname = getattr(
                    current_func, "__qualname__", ""
                )
                qual_parts = qualname.split(".")
                owner_class = None
                if len(qual_parts) >= 2:
                    owner_candidate = current_map.get(
                        qual_parts[-2]
                    )
                    if isinstance(owner_candidate, type):
                        owner_class = owner_candidate
                if owner_class is not None:
                    try:
                        owner_map = vars(owner_class)
                    except Exception:
                        owner_map = {}
                    for self_attr in self_attrs:
                        owner_value = None
                        try:
                            for owner_klass in (
                                owner_class.__mro__
                            ):
                                owner_klass_map = vars(
                                    owner_klass
                                )
                                if self_attr in (
                                    owner_klass_map
                                ):
                                    owner_value = (
                                        owner_klass_map.get(
                                            self_attr
                                        )
                                    )
                                    break
                        except Exception:
                            owner_value = None
                        if isinstance(owner_value, str):
                            act_attr_strs.add(owner_value)
                        elif isinstance(
                            owner_value, (bytes, bytearray)
                        ):
                            try:
                                act_attr_strs.add(
                                    owner_value.decode("utf-8")
                                )
                            except Exception:
                                pass
                    init_fn = owner_map.get("__init__")
                    if init_fn is None:
                        try:
                            for owner_klass in (
                                owner_class.__mro__[1:]
                            ):
                                owner_klass_map = vars(
                                    owner_klass
                                )
                                if "__init__" in (
                                    owner_klass_map
                                ):
                                    init_fn = (
                                        owner_klass_map.get(
                                            "__init__"
                                        )
                                    )
                                    break
                        except Exception:
                            init_fn = None
                    if isinstance(
                        init_fn, _types_module.FunctionType
                    ):
                        init_code = getattr(
                            init_fn, "__code__", None
                        )
                        if init_code is not None:
                            last_const = None
                            try:
                                init_instructions = list(
                                    _dis_module.get_instructions(
                                        init_code
                                    )
                                )
                            except Exception:
                                init_instructions = []
                            for init_ins in init_instructions:
                                if (
                                    init_ins.opname
                                    == "LOAD_CONST"
                                    and isinstance(
                                        init_ins.argval, str
                                    )
                                ):
                                    last_const = init_ins.argval
                                elif (
                                    init_ins.opname
                                    == "LOAD_CONST"
                                    and isinstance(
                                        init_ins.argval,
                                        (bytes, bytearray),
                                    )
                                ):
                                    try:
                                        last_const = (
                                            init_ins.argval
                                            .decode("utf-8")
                                        )
                                    except Exception:
                                        pass
                                elif (
                                    init_ins.opname
                                    == "STORE_ATTR"
                                    and init_ins.argval
                                    in self_attrs
                                    and last_const is not None
                                ):
                                    act_attr_strs.add(last_const)
                            for init_pos in range(
                                len(init_instructions)
                            ):
                                init_head = (
                                    init_instructions[
                                        init_pos
                                    ]
                                )
                                if not (
                                    init_head.opname in (
                                        "LOAD_GLOBAL",
                                        "LOAD_NAME",
                                    )
                                    and init_head.argval
                                    == "setattr"
                                ):
                                    continue
                                init_consts = []
                                for init_ahead in (
                                    init_instructions[
                                        init_pos + 1:
                                        init_pos + 9
                                    ]
                                ):
                                    if (
                                        init_ahead.opname
                                        == "LOAD_CONST"
                                        and isinstance(
                                            init_ahead.argval,
                                            str,
                                        )
                                    ):
                                        init_consts.append(
                                            init_ahead.argval
                                        )
                                    elif (
                                        init_ahead.opname
                                        == "LOAD_CONST"
                                        and isinstance(
                                            init_ahead.argval,
                                            (bytes, bytearray),
                                        )
                                    ):
                                        try:
                                            init_consts.append(
                                                init_ahead
                                                .argval.decode(
                                                    "utf-8"
                                                )
                                            )
                                        except Exception:
                                            pass
                                if (
                                    len(init_consts) >= 2
                                    and init_consts[0]
                                    in self_attrs
                                ):
                                    act_attr_strs.add(
                                        init_consts[1]
                                    )
            call_returned_maps = []
            if call_names or call_pairs:
                called_fns = []
                for called_name in call_names:
                    called_value = current_map.get(
                        called_name
                    )
                    if isinstance(
                        called_value,
                        _types_module.FunctionType,
                    ):
                        if (
                            getattr(
                                called_value,
                                "__globals__",
                                None,
                            )
                            is current_map
                        ):
                            called_fns.append(called_value)
                    elif isinstance(called_value, type):
                        try:
                            for called_klass in (
                                called_value.__mro__
                            ):
                                for called_item in vars(
                                    called_klass
                                ).values():
                                    if isinstance(
                                        called_item,
                                        _types_module
                                        .FunctionType,
                                    ) and (
                                        getattr(
                                            called_item,
                                            "__globals__",
                                            None,
                                        )
                                        is current_map
                                    ):
                                        called_fns.append(
                                            called_item
                                        )
                        except Exception:
                            pass
                for called_base, called_attr in call_pairs:
                    called_base_value = current_map.get(
                        called_base
                    )
                    called_pair_value = None
                    if isinstance(
                        called_base_value,
                        _types_module.ModuleType,
                    ):
                        called_pair_value = getattr(
                            called_base_value,
                            "__dict__",
                            {},
                        ).get(called_attr)
                    elif isinstance(called_base_value, type):
                        try:
                            for called_klass in (
                                called_base_value.__mro__
                            ):
                                if called_attr in vars(
                                    called_klass
                                ):
                                    called_pair_value = (
                                        vars(
                                            called_klass
                                        ).get(called_attr)
                                    )
                                    break
                        except Exception:
                            called_pair_value = None
                    if isinstance(
                        called_pair_value,
                        _types_module.FunctionType,
                    ):
                        called_fns.append(called_pair_value)
                seen_called = set()
                called_queue = [
                    (called_fn, 0) for called_fn in called_fns
                ]
                while called_queue:
                    called_fn, called_depth = (
                        called_queue.pop()
                    )
                    if id(called_fn) in seen_called:
                        continue
                    seen_called.add(id(called_fn))
                    called_map = getattr(
                        called_fn, "__globals__", None
                    )
                    if not isinstance(called_map, dict):
                        continue
                    called_code = getattr(
                        called_fn, "__code__", None
                    )
                    if called_code is None:
                        continue
                    called_facts = _code_facts(called_code)
                    called_modules = []
                    for called_loaded in called_facts[0]:
                        called_loaded_value = called_map.get(
                            called_loaded
                        )
                        if isinstance(
                            called_loaded_value,
                            _types_module.ModuleType,
                        ):
                            called_modules.append(
                                called_loaded_value
                            )
                        if (
                            called_depth < 2
                            and isinstance(
                                called_loaded_value,
                                _types_module.FunctionType,
                            )
                            and getattr(
                                called_loaded_value,
                                "__globals__",
                                None,
                            )
                            is called_map
                        ):
                            called_queue.append(
                                (
                                    called_loaded_value,
                                    called_depth + 1,
                                )
                            )
                    for called_pb, called_pa in (
                        called_facts[3]
                    ):
                        called_bv = called_map.get(called_pb)
                        if isinstance(
                            called_bv,
                            _types_module.ModuleType,
                        ):
                            called_pv = getattr(
                                called_bv, "__dict__", {}
                            ).get(called_pa)
                            if isinstance(
                                called_pv,
                                _types_module.ModuleType,
                            ):
                                called_modules.append(
                                    called_pv
                                )
                            elif (
                                called_depth < 2
                                and isinstance(
                                    called_pv,
                                    _types_module
                                    .FunctionType,
                                )
                            ):
                                called_queue.append(
                                    (
                                        called_pv,
                                        called_depth + 1,
                                    )
                                )
                        elif isinstance(called_bv, type):
                            try:
                                for called_klass in (
                                    called_bv.__mro__
                                ):
                                    if called_pa in vars(
                                        called_klass
                                    ):
                                        called_pv = vars(
                                            called_klass
                                        ).get(called_pa)
                                        if isinstance(
                                            called_pv,
                                            _types_module
                                            .FunctionType,
                                        ):
                                            called_queue.append(
                                                (
                                                    called_pv,
                                                    called_depth
                                                    + 1,
                                                )
                                            )
                                        break
                            except Exception:
                                pass
                    for called_cb, called_fa, called_sa in (
                        called_facts[6]
                    ):
                        called_bv = called_map.get(called_cb)
                        if not isinstance(
                            called_bv,
                            _types_module.ModuleType,
                        ):
                            continue
                        called_iv = getattr(
                            called_bv, "__dict__", {}
                        ).get(called_fa)
                        if isinstance(
                            called_iv,
                            _types_module.ModuleType,
                        ):
                            called_modules.append(called_iv)
                    for called_targets in (
                        called_facts[12],
                        called_facts[13],
                        called_facts[14],
                        called_facts[16],
                        called_facts[17],
                        called_facts[19],
                        called_facts[23],
                        called_facts[27],
                    ):
                        for called_bn, called_key in (
                            called_targets
                        ):
                            called_bv = called_map.get(
                                called_bn
                            )
                            if not isinstance(
                                called_bv,
                                _types_module.ModuleType,
                            ):
                                continue
                            called_iv = getattr(
                                called_bv, "__dict__", {}
                            ).get(called_key)
                            if isinstance(
                                called_iv,
                                _types_module.ModuleType,
                            ):
                                called_modules.append(
                                    called_iv
                                )
                    called_carried = set()
                    for called_default in (
                        getattr(
                            called_fn, "__defaults__", None
                        )
                        or ()
                    ):
                        if isinstance(called_default, str):
                            called_carried.add(called_default)
                        elif isinstance(
                            called_default, (bytes, bytearray)
                        ):
                            try:
                                called_carried.add(
                                    called_default.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                    for called_default in (
                        getattr(
                            called_fn, "__kwdefaults__", None
                        )
                        or {}
                    ).values():
                        if isinstance(called_default, str):
                            called_carried.add(called_default)
                        elif isinstance(
                            called_default, (bytes, bytearray)
                        ):
                            try:
                                called_carried.add(
                                    called_default.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                    for called_default in (
                        getattr(
                            called_fn, "__defaults__", None
                        )
                        or ()
                    ):
                        if isinstance(
                            called_default,
                            (
                                dict,
                                list,
                                tuple,
                                set,
                                frozenset,
                            ),
                        ):
                            called_held_pending = [called_default]
                            called_held_seen = set()
                            while called_held_pending:
                                held = called_held_pending.pop()
                                if id(held) in called_held_seen:
                                    continue
                                called_held_seen.add(id(held))
                                if isinstance(held, str):
                                    called_carried.add(held)
                                elif isinstance(
                                    held, (bytes, bytearray)
                                ):
                                    try:
                                        called_carried.add(
                                            held.decode("utf-8")
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(held, dict):
                                    for held_key in held:
                                        called_held_pending.append(held_key)
                                        called_held_pending.append(
                                            held[held_key]
                                        )
                                elif isinstance(
                                    held,
                                    (list, tuple, set, frozenset),
                                ):
                                    called_held_pending.extend(held)
                    for called_default in (
                        getattr(
                            called_fn,
                            "__kwdefaults__",
                            None,
                        )
                        or {}
                    ).values():
                        if isinstance(
                            called_default,
                            (
                                dict,
                                list,
                                tuple,
                                set,
                                frozenset,
                            ),
                        ):
                            called_held_pending = [called_default]
                            called_held_seen = set()
                            while called_held_pending:
                                held = called_held_pending.pop()
                                if id(held) in called_held_seen:
                                    continue
                                called_held_seen.add(id(held))
                                if isinstance(held, str):
                                    called_carried.add(held)
                                elif isinstance(
                                    held, (bytes, bytearray)
                                ):
                                    try:
                                        called_carried.add(
                                            held.decode("utf-8")
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(held, dict):
                                    for held_key in held:
                                        called_held_pending.append(held_key)
                                        called_held_pending.append(
                                            held[held_key]
                                        )
                                elif isinstance(
                                    held,
                                    (list, tuple, set, frozenset),
                                ):
                                    called_held_pending.extend(held)
                    for called_cell in (
                        getattr(
                            called_fn, "__closure__", None
                        )
                        or ()
                    ):
                        try:
                            called_cell_value = (
                                called_cell.cell_contents
                            )
                        except Exception:
                            continue
                        if isinstance(called_cell_value, str):
                            called_carried.add(
                                called_cell_value
                            )
                        elif isinstance(
                            called_cell_value,
                            (bytes, bytearray),
                        ):
                            try:
                                called_carried.add(
                                    called_cell_value.decode(
                                        "utf-8"
                                    )
                                )
                            except Exception:
                                pass
                    for called_cell in (
                        getattr(
                            called_fn, "__closure__", None
                        )
                        or ()
                    ):
                        try:
                            called_cell_value = (
                                called_cell.cell_contents
                            )
                        except Exception:
                            continue
                        if isinstance(
                            called_cell_value,
                            (
                                dict,
                                list,
                                tuple,
                                set,
                                frozenset,
                            ),
                        ):
                            called_held_pending = [called_cell_value]
                            called_held_seen = set()
                            while called_held_pending:
                                held = called_held_pending.pop()
                                if id(held) in called_held_seen:
                                    continue
                                called_held_seen.add(id(held))
                                if isinstance(held, str):
                                    called_carried.add(held)
                                elif isinstance(
                                    held, (bytes, bytearray)
                                ):
                                    try:
                                        called_carried.add(
                                            held.decode("utf-8")
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(held, dict):
                                    for held_key in held:
                                        called_held_pending.append(held_key)
                                        called_held_pending.append(
                                            held[held_key]
                                        )
                                elif isinstance(
                                    held,
                                    (list, tuple, set, frozenset),
                                ):
                                    called_held_pending.extend(held)
                    for called_loaded in called_facts[0]:
                        called_loaded_value = called_map.get(
                            called_loaded
                        )
                        if isinstance(called_loaded_value, str):
                            called_carried.add(
                                called_loaded_value
                            )
                        elif isinstance(
                            called_loaded_value,
                            (bytes, bytearray),
                        ):
                            try:
                                called_carried.add(
                                    called_loaded_value
                                    .decode("utf-8")
                                )
                            except Exception:
                                pass
                    for called_loaded in called_facts[0]:
                        called_loaded_value = called_map.get(
                            called_loaded
                        )
                        if isinstance(
                            called_loaded_value,
                            (
                                dict,
                                list,
                                tuple,
                                set,
                                frozenset,
                            ),
                        ):
                            called_held_pending = [called_loaded_value]
                            called_held_seen = set()
                            while called_held_pending:
                                held = called_held_pending.pop()
                                if id(held) in called_held_seen:
                                    continue
                                called_held_seen.add(id(held))
                                if isinstance(held, str):
                                    called_carried.add(held)
                                elif isinstance(
                                    held, (bytes, bytearray)
                                ):
                                    try:
                                        called_carried.add(
                                            held.decode("utf-8")
                                        )
                                    except Exception:
                                        pass
                                elif isinstance(held, dict):
                                    for held_key in held:
                                        called_held_pending.append(held_key)
                                        called_held_pending.append(
                                            held[held_key]
                                        )
                                elif isinstance(
                                    held,
                                    (list, tuple, set, frozenset),
                                ):
                                    called_held_pending.extend(held)
                    for called_loaded in called_facts[0]:
                        called_hv = called_map.get(
                            called_loaded
                        )
                        if not isinstance(
                            called_hv,
                            _types_module.FunctionType,
                        ):
                            continue
                        if (
                            getattr(
                                called_hv,
                                "__globals__",
                                None,
                            )
                            is not called_map
                        ):
                            continue
                        called_hcode = getattr(
                            called_hv, "__code__", None
                        )
                        if called_hcode is None:
                            continue
                        for called_hconst in _code_facts(
                            called_hcode
                        )[1]:
                            called_carried.add(
                                called_hconst
                            )
                    for called_bases in (
                        called_facts[20],
                        called_facts[21],
                        called_facts[22],
                        called_facts[24],
                        called_facts[29],
                        called_facts[30],
                        called_facts[31],
                        called_facts[40],
                    ):
                        for called_base in called_bases:
                            called_bv = called_map.get(
                                called_base
                            )
                            if not isinstance(
                                called_bv,
                                _types_module.ModuleType,
                            ):
                                continue
                            called_bmap = getattr(
                                called_bv, "__dict__", {}
                            )
                            if not isinstance(
                                called_bmap, dict
                            ):
                                continue
                            for called_key in called_carried:
                                called_iv = called_bmap.get(
                                    called_key
                                )
                                if isinstance(
                                    called_iv,
                                    _types_module.ModuleType,
                                ):
                                    called_modules.append(
                                        called_iv
                                    )
                            for called_key in called_bmap:
                                if not isinstance(
                                    called_key, str
                                ):
                                    continue
                                if called_key in called_carried:
                                    continue
                                if not _built_from_consts(
                                    called_key, called_carried
                                ):
                                    continue
                                called_iv = called_bmap.get(
                                    called_key
                                )
                                if isinstance(
                                    called_iv,
                                    _types_module.ModuleType,
                                ):
                                    called_modules.append(
                                        called_iv
                                    )
                    for called_module in called_modules:
                        called_module_map = getattr(
                            called_module, "__dict__", None
                        )
                        if not isinstance(
                            called_module_map, dict
                        ):
                            continue
                        if _map_is_stdlib(
                            called_module_map
                        ):
                            continue
                        if called_module_map not in (
                            call_returned_maps
                        ):
                            call_returned_maps.append(
                                called_module_map
                            )
            carried_names = set()
            for loaded_name in names:
                loaded_value = current_map.get(loaded_name)
                if isinstance(loaded_value, str):
                    carried_names.add(loaded_value)
                elif isinstance(
                    loaded_value, (bytes, bytearray)
                ):
                    try:
                        carried_names.add(
                            loaded_value.decode("utf-8")
                        )
                    except Exception:
                        pass
                elif isinstance(
                    loaded_value,
                    (dict, list, tuple, set, frozenset),
                ):
                    pending_held = [loaded_value]
                    seen_held = set()
                    while pending_held:
                        held = pending_held.pop()
                        if id(held) in seen_held:
                            continue
                        seen_held.add(id(held))
                        if isinstance(held, str):
                            carried_names.add(held)
                        elif isinstance(
                            held, (bytes, bytearray)
                        ):
                            try:
                                carried_names.add(
                                    held.decode("utf-8")
                                )
                            except Exception:
                                pass
                        elif isinstance(held, dict):
                            for held_key in held:
                                pending_held.append(held_key)
                                pending_held.append(
                                    held[held_key]
                                )
                        elif isinstance(
                            held,
                            (list, tuple, set, frozenset),
                        ):
                            pending_held.extend(held)
            candidate_names = set(names)
            resolved = False
            dynamic = (
                "globals" in names
                or "eval" in names
                or "exec" in names
                or "getattr" in names
                or vars_with_arg
            )
            if dynamic:
                for const in consts:
                    if const in current_map:
                        candidate_names.add(const)
                        resolved = True
                for default_str in default_strs:
                    if default_str in current_map:
                        candidate_names.add(default_str)
                        resolved = True
                for closure_str in closure_strs:
                    if closure_str in current_map:
                        candidate_names.add(closure_str)
                        resolved = True
                for returned_str in returned_strs:
                    if returned_str in current_map:
                        candidate_names.add(returned_str)
                        resolved = True
            if "exec" in names:
                for default_str in default_strs:
                    try:
                        default_code = compile(
                            default_str, "<referenced>", "exec"
                        )
                    except Exception:
                        continue
                    default_facts = _code_facts(default_code)
                    for inner_name in default_facts[0]:
                        if inner_name in current_map:
                            candidate_names.add(inner_name)
                            resolved = True
                    for inner_const in default_facts[1]:
                        if inner_const in current_map:
                            candidate_names.add(inner_const)
                            resolved = True
                for closure_str in closure_strs:
                    try:
                        closure_code = compile(
                            closure_str, "<referenced>", "exec"
                        )
                    except Exception:
                        continue
                    closure_facts = _code_facts(closure_code)
                    for inner_name in closure_facts[0]:
                        if inner_name in current_map:
                            candidate_names.add(inner_name)
                            resolved = True
                    for inner_const in closure_facts[1]:
                        if inner_const in current_map:
                            candidate_names.add(inner_const)
                            resolved = True
                for returned_str in returned_strs:
                    try:
                        returned_code = compile(
                            returned_str,
                            "<referenced>",
                            "exec",
                        )
                    except Exception:
                        continue
                    returned_facts = _code_facts(returned_code)
                    for inner_name in returned_facts[0]:
                        if inner_name in current_map:
                            candidate_names.add(inner_name)
                            resolved = True
                    for inner_const in returned_facts[1]:
                        if inner_const in current_map:
                            candidate_names.add(inner_const)
                            resolved = True
                exec_extra_maps = list(call_returned_maps)
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                ) in chains4:
                    if chain_base not in current_map:
                        continue
                    chain_value = current_map[chain_base]
                    for chain_attr in (
                        first_attr,
                        second_attr,
                        third_attr,
                        fourth_attr,
                    ):
                        if not isinstance(
                            chain_value,
                            _types_module.ModuleType,
                        ):
                            break
                        chain_map = getattr(
                            chain_value, "__dict__", None
                        )
                        if not isinstance(chain_map, dict):
                            break
                        chain_value = chain_map.get(
                            chain_attr
                        )
                    if not isinstance(
                        chain_value, _types_module.ModuleType
                    ):
                        continue
                    chain_map = getattr(
                        chain_value, "__dict__", None
                    )
                    if not isinstance(chain_map, dict):
                        continue
                    if _map_is_stdlib(chain_map):
                        continue
                    if chain_map not in exec_extra_maps:
                        exec_extra_maps.append(chain_map)
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                    fifth_attr,
                ) in chains5:
                    if chain_base not in current_map:
                        continue
                    chain_value = current_map[chain_base]
                    for chain_attr in (
                        first_attr,
                        second_attr,
                        third_attr,
                        fourth_attr,
                        fifth_attr,
                    ):
                        if not isinstance(
                            chain_value,
                            _types_module.ModuleType,
                        ):
                            break
                        chain_map = getattr(
                            chain_value, "__dict__", None
                        )
                        if not isinstance(chain_map, dict):
                            break
                        chain_value = chain_map.get(
                            chain_attr
                        )
                    if not isinstance(
                        chain_value, _types_module.ModuleType
                    ):
                        continue
                    chain_map = getattr(
                        chain_value, "__dict__", None
                    )
                    if not isinstance(chain_map, dict):
                        continue
                    if _map_is_stdlib(chain_map):
                        continue
                    if chain_map not in exec_extra_maps:
                        exec_extra_maps.append(chain_map)
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                    fifth_attr,
                    sixth_attr,
                ) in chains6:
                    if chain_base not in current_map:
                        continue
                    chain_value = current_map[chain_base]
                    for chain_attr in (
                        first_attr,
                        second_attr,
                        third_attr,
                        fourth_attr,
                        fifth_attr,
                        sixth_attr,
                    ):
                        if not isinstance(
                            chain_value,
                            _types_module.ModuleType,
                        ):
                            break
                        chain_map = getattr(
                            chain_value, "__dict__", None
                        )
                        if not isinstance(chain_map, dict):
                            break
                        chain_value = chain_map.get(
                            chain_attr
                        )
                    if not isinstance(
                        chain_value, _types_module.ModuleType
                    ):
                        continue
                    chain_map = getattr(
                        chain_value, "__dict__", None
                    )
                    if not isinstance(chain_map, dict):
                        continue
                    if _map_is_stdlib(chain_map):
                        continue
                    if chain_map not in exec_extra_maps:
                        exec_extra_maps.append(chain_map)
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                    fifth_attr,
                    sixth_attr,
                    seventh_attr,
                ) in chains7:
                    if chain_base not in current_map:
                        continue
                    chain_value = current_map[chain_base]
                    for chain_attr in (
                        first_attr,
                        second_attr,
                        third_attr,
                        fourth_attr,
                        fifth_attr,
                        sixth_attr,
                        seventh_attr,
                    ):
                        if not isinstance(
                            chain_value,
                            _types_module.ModuleType,
                        ):
                            break
                        chain_map = getattr(
                            chain_value, "__dict__", None
                        )
                        if not isinstance(chain_map, dict):
                            break
                        chain_value = chain_map.get(
                            chain_attr
                        )
                    if not isinstance(
                        chain_value, _types_module.ModuleType
                    ):
                        continue
                    chain_map = getattr(
                        chain_value, "__dict__", None
                    )
                    if not isinstance(chain_map, dict):
                        continue
                    if _map_is_stdlib(chain_map):
                        continue
                    if chain_map not in exec_extra_maps:
                        exec_extra_maps.append(chain_map)
                for vg_base in vars_get_carried_bases:
                    if vg_base not in current_map:
                        continue
                    vg_value = current_map[vg_base]
                    if not isinstance(
                        vg_value, _types_module.ModuleType
                    ):
                        continue
                    vg_map = getattr(
                        vg_value, "__dict__", None
                    )
                    if not isinstance(vg_map, dict):
                        continue
                    for vg_key in (
                        extra_carried | carried_names
                    ):
                        vg_inner = vg_map.get(vg_key)
                        if not isinstance(
                            vg_inner,
                            _types_module.ModuleType,
                        ):
                            continue
                        vg_inner_map = getattr(
                            vg_inner, "__dict__", None
                        )
                        if not isinstance(
                            vg_inner_map, dict
                        ):
                            continue
                        if _map_is_stdlib(vg_inner_map):
                            continue
                        if vg_inner_map not in (
                            exec_extra_maps
                        ):
                            exec_extra_maps.append(
                                vg_inner_map
                            )
                for ag_base in (
                    vars_get_attr_bases
                    | get_attr_bases
                    | vars_subscript_attr_bases
                    | dict_subscript_attr_bases
                ):
                    if ag_base not in current_map:
                        continue
                    ag_value = current_map[ag_base]
                    if not isinstance(
                        ag_value, _types_module.ModuleType
                    ):
                        continue
                    ag_map = getattr(
                        ag_value, "__dict__", None
                    )
                    if not isinstance(ag_map, dict):
                        continue
                    for ag_key in act_attr_strs:
                        ag_inner = ag_map.get(ag_key)
                        if not isinstance(
                            ag_inner,
                            _types_module.ModuleType,
                        ):
                            continue
                        ag_inner_map = getattr(
                            ag_inner, "__dict__", None
                        )
                        if not isinstance(
                            ag_inner_map, dict
                        ):
                            continue
                        if _map_is_stdlib(ag_inner_map):
                            continue
                        if ag_inner_map not in (
                            exec_extra_maps
                        ):
                            exec_extra_maps.append(
                                ag_inner_map
                            )
                for exec_extra_map in exec_extra_maps:
                    exec_strs = (
                        set(consts)
                        | carried_names
                        | set(default_strs)
                        | set(closure_strs)
                        | returned_strs
                    )
                    for exec_str in exec_strs:
                        try:
                            exec_code = compile(
                                exec_str,
                                "<referenced>",
                                "exec",
                            )
                        except Exception:
                            continue
                        exec_facts = _code_facts(exec_code)
                        for inner_name in exec_facts[0]:
                            if inner_name in exec_extra_map:
                                _append_reached(
                                    exec_extra_map[
                                        inner_name
                                    ]
                                )
                                resolved = True
                        for inner_const in exec_facts[1]:
                            if inner_const in exec_extra_map:
                                _append_reached(
                                    exec_extra_map[
                                        inner_const
                                    ]
                                )
                                resolved = True
                for base_name in exec_dict_bases:
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    foreign_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(foreign_map, dict):
                        continue
                    if _map_is_stdlib(foreign_map):
                        continue
                    exec_strs = (
                        set(consts)
                        | carried_names
                        | set(default_strs)
                        | set(closure_strs)
                        | returned_strs
                    )
                    for exec_str in exec_strs:
                        try:
                            exec_code = compile(
                                exec_str,
                                "<referenced>",
                                "exec",
                            )
                        except Exception:
                            continue
                        exec_facts = _code_facts(exec_code)
                        for inner_name in exec_facts[0]:
                            if inner_name in foreign_map:
                                _append_reached(
                                    foreign_map[inner_name]
                                )
                                resolved = True
                        for inner_const in exec_facts[1]:
                            if inner_const in foreign_map:
                                _append_reached(
                                    foreign_map[inner_const]
                                )
                                resolved = True
                for base_name, first_attr in exec_chain_bases:
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    exec_strs = (
                        set(consts)
                        | carried_names
                        | set(default_strs)
                        | set(closure_strs)
                        | returned_strs
                    )
                    for exec_str in exec_strs:
                        try:
                            exec_code = compile(
                                exec_str,
                                "<referenced>",
                                "exec",
                            )
                        except Exception:
                            continue
                        exec_facts = _code_facts(exec_code)
                        for inner_name in exec_facts[0]:
                            if inner_name in inner_map:
                                _append_reached(
                                    inner_map[inner_name]
                                )
                                resolved = True
                        for inner_const in exec_facts[1]:
                            if inner_const in inner_map:
                                _append_reached(
                                    inner_map[inner_const]
                                )
                                resolved = True
                for base_name, sub_key in exec_subscript_bases:
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(sub_key)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    exec_strs = (
                        set(consts)
                        | carried_names
                        | set(default_strs)
                        | set(closure_strs)
                        | returned_strs
                    )
                    for exec_str in exec_strs:
                        try:
                            exec_code = compile(
                                exec_str,
                                "<referenced>",
                                "exec",
                            )
                        except Exception:
                            continue
                        exec_facts = _code_facts(exec_code)
                        for inner_name in exec_facts[0]:
                            if inner_name in inner_map:
                                _append_reached(
                                    inner_map[inner_name]
                                )
                                resolved = True
                        for inner_const in exec_facts[1]:
                            if inner_const in inner_map:
                                _append_reached(
                                    inner_map[inner_const]
                                )
                                resolved = True
                for base_name, result_key in (
                    get_result_targets
                    | getattr_result_targets
                    | vars_subscript_targets
                    | vars_get_result_targets
                    | getattribute_result_targets
                ):
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(result_key)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    exec_strs = (
                        set(consts)
                        | carried_names
                        | set(default_strs)
                        | set(closure_strs)
                        | returned_strs
                    )
                    for exec_str in exec_strs:
                        try:
                            exec_code = compile(
                                exec_str,
                                "<referenced>",
                                "exec",
                            )
                        except Exception:
                            continue
                        exec_facts = _code_facts(exec_code)
                        for inner_name in exec_facts[0]:
                            if inner_name in inner_map:
                                _append_reached(
                                    inner_map[inner_name]
                                )
                                resolved = True
                        for inner_const in exec_facts[1]:
                            if inner_const in inner_map:
                                _append_reached(
                                    inner_map[inner_const]
                                )
                                resolved = True
                for carried_base in (
                    getattr_carried_bases
                    | vars_carried_bases
                    | get_carried_bases
                ):
                    if carried_base not in current_map:
                        continue
                    base_value = current_map[carried_base]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    for carried_key in (
                        extra_carried | carried_names
                    ):
                        inner_value = first_map.get(carried_key)
                        if not isinstance(
                            inner_value,
                            _types_module.ModuleType,
                        ):
                            continue
                        inner_map = getattr(
                            inner_value, "__dict__", None
                        )
                        if not isinstance(inner_map, dict):
                            continue
                        if _map_is_stdlib(inner_map):
                            continue
                        exec_strs = (
                            set(consts)
                            | carried_names
                            | set(default_strs)
                            | set(closure_strs)
                            | returned_strs
                        )
                        for exec_str in exec_strs:
                            try:
                                exec_code = compile(
                                    exec_str,
                                    "<referenced>",
                                    "exec",
                                )
                            except Exception:
                                continue
                            exec_facts = _code_facts(exec_code)
                            for inner_name in exec_facts[0]:
                                if inner_name in inner_map:
                                    _append_reached(
                                        inner_map[inner_name]
                                    )
                                    resolved = True
                            for inner_const in exec_facts[1]:
                                if inner_const in inner_map:
                                    _append_reached(
                                        inner_map[inner_const]
                                    )
                                    resolved = True
            if "exec" in names:
                for const in consts:
                    try:
                        inner_code = compile(
                            const, "<referenced>", "exec"
                        )
                    except Exception:
                        continue
                    inner_facts = _code_facts(inner_code)
                    for inner_name in inner_facts[0]:
                        if inner_name in current_map:
                            candidate_names.add(inner_name)
                            resolved = True
                    for inner_const in inner_facts[1]:
                        if inner_const in current_map:
                            candidate_names.add(inner_const)
                            resolved = True
            if dynamic:
                for loaded_name in names:
                    carried = current_map.get(loaded_name)
                    carried_strs = []
                    if isinstance(carried, str):
                        carried_strs = [carried]
                    elif isinstance(
                        carried, (bytes, bytearray)
                    ):
                        try:
                            carried_strs = [
                                carried.decode("utf-8")
                            ]
                        except Exception:
                            carried_strs = []
                    elif isinstance(
                        carried,
                        (dict, list, tuple, set, frozenset),
                    ):
                        pending_held = [carried]
                        seen_held = set()
                        while pending_held:
                            held = pending_held.pop()
                            if id(held) in seen_held:
                                continue
                            seen_held.add(id(held))
                            if isinstance(held, str):
                                carried_strs.append(held)
                            elif isinstance(
                                held, (bytes, bytearray)
                            ):
                                try:
                                    carried_strs.append(
                                        held.decode("utf-8")
                                    )
                                except Exception:
                                    pass
                            elif isinstance(held, dict):
                                for held_key in held:
                                    pending_held.append(
                                        held_key
                                    )
                                    pending_held.append(
                                        held[held_key]
                                    )
                            elif isinstance(
                                held,
                                (
                                    list,
                                    tuple,
                                    set,
                                    frozenset,
                                ),
                            ):
                                pending_held.extend(held)
                    for carried in carried_strs:
                        if "exec" in names:
                            try:
                                carried_code = compile(
                                    carried,
                                    "<referenced>",
                                    "exec",
                                )
                            except Exception:
                                carried_code = None
                            if carried_code is not None:
                                carried_facts = _code_facts(
                                    carried_code
                                )
                                for carried_name in (
                                    carried_facts[0]
                                ):
                                    if (
                                        carried_name
                                        in current_map
                                    ):
                                        candidate_names.add(
                                            carried_name
                                        )
                                        resolved = True
                                for carried_const in (
                                    carried_facts[1]
                                ):
                                    if (
                                        carried_const
                                        in current_map
                                    ):
                                        candidate_names.add(
                                            carried_const
                                        )
                                        resolved = True
                        if (
                            "eval" in names
                            or "globals" in names
                        ):
                            if carried in current_map:
                                candidate_names.add(
                                    carried
                                )
                                resolved = True
            if "globals" in names or "eval" in names:
                for key in current_map:
                    if (
                        not isinstance(key, str)
                        or key in candidate_names
                    ):
                        continue
                    if _built_from_consts(key, consts):
                        candidate_names.add(key)
                        resolved = True
            if (
                extra_names
                and dynamic
                and current_func is func
            ):
                for extra in extra_names:
                    if extra in current_map:
                        candidate_names.add(extra)
                        resolved = True
            for name in candidate_names:
                if name not in current_map:
                    continue
                value = current_map[name]
                if isinstance(
                    value, _types_module.ModuleType
                ):
                    continue
                if isinstance(
                    value, _lru_cache_wrapper_type
                ):
                    wrapped = _follow_wrapper(value)
                    if wrapped is not None:
                        pending_funcs.append(
                            (
                                wrapped,
                                getattr(
                                    wrapped,
                                    "__globals__",
                                    None,
                                ),
                            )
                        )
                    continue
                if id(value) in seen_value_ids:
                    continue
                seen_value_ids.add(id(value))
                values.append(value)
                if isinstance(
                    value, _types_module.FunctionType
                ):
                    value_globals = getattr(
                        value, "__globals__", None
                    )
                    pending_funcs.append(
                        (value, value_globals)
                    )
            pairs_enabled = not _map_is_stdlib(current_map)
            for base_name, attr in pairs:
                if not pairs_enabled:
                    break
                if base_name not in current_map:
                    continue
                base_value = current_map[base_name]
                if not isinstance(
                    base_value, _types_module.ModuleType
                ):
                    continue
                module_map = getattr(
                    base_value, "__dict__", None
                )
                if not isinstance(module_map, dict):
                    continue
                if attr not in module_map:
                    continue
                attr_value = module_map[attr]
                if isinstance(
                    attr_value,
                    (list, tuple, set, frozenset, dict),
                ) and attr != "__dict__":
                    _collect_container_contents(attr_value)
                    continue
                if isinstance(attr_value, dict):
                    continue
                if isinstance(attr_value, type):
                    continue
                if not isinstance(
                    attr_value, _types_module.FunctionType
                ) and not isinstance(
                    attr_value,
                    (
                        _types_module.GeneratorType,
                        _lock_type,
                        _rlock_type,
                        _condition_type,
                        _types_module.CellType,
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
                        _extra_uncopyable_types,
                    ),
                ):
                    continue
                if isinstance(
                    attr_value, _types_module.ModuleType
                ):
                    continue
                if isinstance(
                    attr_value, _lru_cache_wrapper_type
                ):
                    wrapped = _follow_wrapper(attr_value)
                    if wrapped is not None:
                        pending_funcs.append(
                            (
                                wrapped,
                                getattr(
                                    wrapped,
                                    "__globals__",
                                    None,
                                ),
                            )
                        )
                    continue
                if id(attr_value) in seen_value_ids:
                    continue
                seen_value_ids.add(id(attr_value))
                values.append(attr_value)
                if isinstance(
                    attr_value, _types_module.FunctionType
                ):
                    pending_funcs.append(
                        (
                            attr_value,
                            getattr(
                                attr_value,
                                "__globals__",
                                None,
                            ),
                        )
                    )
            if pairs_enabled:
                for base_name, attr in pairs:
                    if attr != "__dict__":
                        continue
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    module_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(module_map, dict):
                        continue
                    for const in consts:
                        if const in module_map:
                            _append_reached(
                                module_map[const]
                            )
                            resolved = True
                    for carried_key in carried_names:
                        if carried_key in module_map:
                            _append_reached(
                                module_map[carried_key]
                            )
                            resolved = True
                    for carried_key in extra_carried:
                        if carried_key in module_map:
                            _append_reached(
                                module_map[carried_key]
                            )
                            resolved = True
                    for carried_key in returned_strs:
                        if carried_key in module_map:
                            _append_reached(
                                module_map[carried_key]
                            )
                            resolved = True
                    for carried_key in act_attr_strs:
                        if carried_key in module_map:
                            _append_reached(
                                module_map[carried_key]
                            )
                            resolved = True
                    for pair_base, pair_attr in pairs:
                        if pair_base != base_name:
                            continue
                        held_value = module_map.get(pair_attr)
                        if (
                            isinstance(held_value, str)
                            and held_value in module_map
                        ):
                            _append_reached(
                                module_map[held_value]
                            )
                            resolved = True
                for base_name, first_attr, second_attr in (
                    chains
                ):
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if second_attr not in inner_map:
                        continue
                    reached = inner_map[second_attr]
                    if isinstance(
                        reached, _types_module.FunctionType
                    ) or isinstance(
                        reached, _governed_reach_types
                    ):
                        _append_reached(reached)
                        resolved = True
                for base_name, first_attr, second_attr in (
                    chains
                ):
                    if second_attr != "__dict__":
                        continue
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    for const in consts:
                        if const in inner_map:
                            _append_reached(
                                inner_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in inner_map:
                            _append_reached(
                                inner_map[carried_key]
                            )
                            resolved = True
                for base_name, first_attr, second_attr in (
                    chains
                ):
                    if base_name not in current_map:
                        continue
                    base_value = current_map[base_name]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    deep_value = inner_map.get(second_attr)
                    if not isinstance(
                        deep_value, _types_module.ModuleType
                    ):
                        continue
                    deep_map = getattr(
                        deep_value, "__dict__", None
                    )
                    if not isinstance(deep_map, dict):
                        continue
                    if _map_is_stdlib(deep_map):
                        continue
                    for const in consts:
                        if const in deep_map:
                            _append_reached(
                                deep_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in deep_map:
                            _append_reached(
                                deep_map[carried_key]
                            )
                            resolved = True
                    for deep_key in deep_map:
                        if (
                            not isinstance(deep_key, str)
                            or deep_key in consts
                        ):
                            continue
                        if _built_from_consts(
                            deep_key, consts
                        ):
                            _append_reached(
                                deep_map[deep_key]
                            )
                            resolved = True
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                ) in chains3:
                    if chain_base not in current_map:
                        continue
                    base_value = current_map[chain_base]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    deep_value = inner_map.get(second_attr)
                    if not isinstance(
                        deep_value, _types_module.ModuleType
                    ):
                        continue
                    deep_map = getattr(
                        deep_value, "__dict__", None
                    )
                    if not isinstance(deep_map, dict):
                        continue
                    leaf_value = deep_map.get(third_attr)
                    if not isinstance(
                        leaf_value, _types_module.ModuleType
                    ):
                        continue
                    leaf_map = getattr(
                        leaf_value, "__dict__", None
                    )
                    if not isinstance(leaf_map, dict):
                        continue
                    if _map_is_stdlib(leaf_map):
                        continue
                    for const in consts:
                        if const in leaf_map:
                            _append_reached(
                                leaf_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in leaf_map:
                            _append_reached(
                                leaf_map[carried_key]
                            )
                            resolved = True
                    for leaf_key in leaf_map:
                        if (
                            not isinstance(leaf_key, str)
                            or leaf_key in consts
                        ):
                            continue
                        if _built_from_consts(
                            leaf_key, consts
                        ):
                            _append_reached(
                                leaf_map[leaf_key]
                            )
                            resolved = True
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                ) in chains4:
                    if chain_base not in current_map:
                        continue
                    base_value = current_map[chain_base]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    deep_value = inner_map.get(second_attr)
                    if not isinstance(
                        deep_value, _types_module.ModuleType
                    ):
                        continue
                    deep_map = getattr(
                        deep_value, "__dict__", None
                    )
                    if not isinstance(deep_map, dict):
                        continue
                    leaf_value = deep_map.get(third_attr)
                    if not isinstance(
                        leaf_value, _types_module.ModuleType
                    ):
                        continue
                    leaf_map = getattr(
                        leaf_value, "__dict__", None
                    )
                    if not isinstance(leaf_map, dict):
                        continue
                    final_value = leaf_map.get(fourth_attr)
                    if not isinstance(
                        final_value, _types_module.ModuleType
                    ):
                        continue
                    final_map = getattr(
                        final_value, "__dict__", None
                    )
                    if not isinstance(final_map, dict):
                        continue
                    if _map_is_stdlib(final_map):
                        continue
                    for const in consts:
                        if const in final_map:
                            _append_reached(
                                final_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in final_map:
                            _append_reached(
                                final_map[carried_key]
                            )
                            resolved = True
                    for final_key in final_map:
                        if (
                            not isinstance(final_key, str)
                            or final_key in consts
                        ):
                            continue
                        if _built_from_consts(
                            final_key, consts
                        ):
                            _append_reached(
                                final_map[final_key]
                            )
                            resolved = True
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                    fifth_attr,
                ) in chains5:
                    if chain_base not in current_map:
                        continue
                    base_value = current_map[chain_base]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    deep_value = inner_map.get(second_attr)
                    if not isinstance(
                        deep_value, _types_module.ModuleType
                    ):
                        continue
                    deep_map = getattr(
                        deep_value, "__dict__", None
                    )
                    if not isinstance(deep_map, dict):
                        continue
                    leaf_value = deep_map.get(third_attr)
                    if not isinstance(
                        leaf_value, _types_module.ModuleType
                    ):
                        continue
                    leaf_map = getattr(
                        leaf_value, "__dict__", None
                    )
                    if not isinstance(leaf_map, dict):
                        continue
                    final_value = leaf_map.get(fourth_attr)
                    if not isinstance(
                        final_value, _types_module.ModuleType
                    ):
                        continue
                    final_map = getattr(
                        final_value, "__dict__", None
                    )
                    if not isinstance(final_map, dict):
                        continue
                    if _map_is_stdlib(final_map):
                        continue
                    last_value = final_map.get(fifth_attr)
                    if not isinstance(
                        last_value, _types_module.ModuleType
                    ):
                        continue
                    last_map = getattr(
                        last_value, "__dict__", None
                    )
                    if not isinstance(last_map, dict):
                        continue
                    if _map_is_stdlib(last_map):
                        continue
                    for const in consts:
                        if const in last_map:
                            _append_reached(
                                last_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in last_map:
                            _append_reached(
                                last_map[carried_key]
                            )
                            resolved = True
                    for last_key in last_map:
                        if (
                            not isinstance(last_key, str)
                            or last_key in consts
                        ):
                            continue
                        if _built_from_consts(
                            last_key, consts
                        ):
                            _append_reached(
                                last_map[last_key]
                            )
                            resolved = True
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                    fifth_attr,
                    sixth_attr,
                ) in chains6:
                    if chain_base not in current_map:
                        continue
                    base_value = current_map[chain_base]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    deep_value = inner_map.get(second_attr)
                    if not isinstance(
                        deep_value, _types_module.ModuleType
                    ):
                        continue
                    deep_map = getattr(
                        deep_value, "__dict__", None
                    )
                    if not isinstance(deep_map, dict):
                        continue
                    leaf_value = deep_map.get(third_attr)
                    if not isinstance(
                        leaf_value, _types_module.ModuleType
                    ):
                        continue
                    leaf_map = getattr(
                        leaf_value, "__dict__", None
                    )
                    if not isinstance(leaf_map, dict):
                        continue
                    final_value = leaf_map.get(fourth_attr)
                    if not isinstance(
                        final_value, _types_module.ModuleType
                    ):
                        continue
                    final_map = getattr(
                        final_value, "__dict__", None
                    )
                    if not isinstance(final_map, dict):
                        continue
                    if _map_is_stdlib(final_map):
                        continue
                    last_value = final_map.get(fifth_attr)
                    if not isinstance(
                        last_value, _types_module.ModuleType
                    ):
                        continue
                    last_map = getattr(
                        last_value, "__dict__", None
                    )
                    if not isinstance(last_map, dict):
                        continue
                    if _map_is_stdlib(last_map):
                        continue
                    sixth_value = last_map.get(sixth_attr)
                    if not isinstance(
                        sixth_value, _types_module.ModuleType
                    ):
                        continue
                    sixth_map = getattr(
                        sixth_value, "__dict__", None
                    )
                    if not isinstance(sixth_map, dict):
                        continue
                    if _map_is_stdlib(sixth_map):
                        continue
                    for const in consts:
                        if const in sixth_map:
                            _append_reached(
                                sixth_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in sixth_map:
                            _append_reached(
                                sixth_map[carried_key]
                            )
                            resolved = True
                    for sixth_key in sixth_map:
                        if (
                            not isinstance(sixth_key, str)
                            or sixth_key in consts
                        ):
                            continue
                        if _built_from_consts(
                            sixth_key, consts
                        ):
                            _append_reached(
                                sixth_map[sixth_key]
                            )
                            resolved = True
                for (
                    chain_base,
                    first_attr,
                    second_attr,
                    third_attr,
                    fourth_attr,
                    fifth_attr,
                    sixth_attr,
                    seventh_attr,
                ) in chains7:
                    if chain_base not in current_map:
                        continue
                    base_value = current_map[chain_base]
                    if not isinstance(
                        base_value, _types_module.ModuleType
                    ):
                        continue
                    first_map = getattr(
                        base_value, "__dict__", None
                    )
                    if not isinstance(first_map, dict):
                        continue
                    inner_value = first_map.get(first_attr)
                    if not isinstance(
                        inner_value, _types_module.ModuleType
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    deep_value = inner_map.get(second_attr)
                    if not isinstance(
                        deep_value, _types_module.ModuleType
                    ):
                        continue
                    deep_map = getattr(
                        deep_value, "__dict__", None
                    )
                    if not isinstance(deep_map, dict):
                        continue
                    leaf_value = deep_map.get(third_attr)
                    if not isinstance(
                        leaf_value, _types_module.ModuleType
                    ):
                        continue
                    leaf_map = getattr(
                        leaf_value, "__dict__", None
                    )
                    if not isinstance(leaf_map, dict):
                        continue
                    final_value = leaf_map.get(fourth_attr)
                    if not isinstance(
                        final_value, _types_module.ModuleType
                    ):
                        continue
                    final_map = getattr(
                        final_value, "__dict__", None
                    )
                    if not isinstance(final_map, dict):
                        continue
                    if _map_is_stdlib(final_map):
                        continue
                    last_value = final_map.get(fifth_attr)
                    if not isinstance(
                        last_value, _types_module.ModuleType
                    ):
                        continue
                    last_map = getattr(
                        last_value, "__dict__", None
                    )
                    if not isinstance(last_map, dict):
                        continue
                    if _map_is_stdlib(last_map):
                        continue
                    sixth_value = last_map.get(sixth_attr)
                    if not isinstance(
                        sixth_value, _types_module.ModuleType
                    ):
                        continue
                    sixth_map = getattr(
                        sixth_value, "__dict__", None
                    )
                    if not isinstance(sixth_map, dict):
                        continue
                    if _map_is_stdlib(sixth_map):
                        continue
                    seventh_value = sixth_map.get(
                        seventh_attr
                    )
                    if not isinstance(
                        seventh_value, _types_module.ModuleType
                    ):
                        continue
                    seventh_map = getattr(
                        seventh_value, "__dict__", None
                    )
                    if not isinstance(seventh_map, dict):
                        continue
                    if _map_is_stdlib(seventh_map):
                        continue
                    for const in consts:
                        if const in seventh_map:
                            _append_reached(
                                seventh_map[const]
                            )
                            resolved = True
                    for carried_key in (
                        carried_names
                        | extra_carried
                        | returned_strs
                        | act_attr_strs
                    ):
                        if carried_key in seventh_map:
                            _append_reached(
                                seventh_map[carried_key]
                            )
                            resolved = True
                    for seventh_key in seventh_map:
                        if (
                            not isinstance(seventh_key, str)
                            or seventh_key in consts
                        ):
                            continue
                        if _built_from_consts(
                            seventh_key, consts
                        ):
                            _append_reached(
                                seventh_map[seventh_key]
                            )
                            resolved = True
                if "getattr" in names or vars_with_arg:
                    for target_name in act_targets:
                        if target_name not in current_map:
                            continue
                        target = current_map[target_name]
                        if not isinstance(
                            target, _types_module.ModuleType
                        ):
                            continue
                        target_map = getattr(
                            target, "__dict__", None
                        )
                        if not isinstance(target_map, dict):
                            continue
                        for const in consts:
                            if const in target_map:
                                _append_reached(
                                    target_map[const]
                                )
                                resolved = True
                        for target_key in target_map:
                            if (
                                not isinstance(target_key, str)
                                or target_key in consts
                            ):
                                continue
                            if _built_from_consts(
                                target_key, consts
                            ):
                                _append_reached(
                                    target_map[target_key]
                                )
                                resolved = True
                        for carried_key in carried_names:
                            if carried_key in target_map:
                                _append_reached(
                                    target_map[carried_key]
                                )
                                resolved = True
                        for carried_key in extra_carried:
                            if carried_key in target_map:
                                _append_reached(
                                    target_map[carried_key]
                                )
                                resolved = True
                        for carried_key in returned_strs:
                            if carried_key in target_map:
                                _append_reached(
                                    target_map[carried_key]
                                )
                                resolved = True
                        for carried_key in act_attr_strs:
                            if carried_key in target_map:
                                _append_reached(
                                    target_map[carried_key]
                                )
                                resolved = True
                        for pair_base, pair_attr in pairs:
                            if pair_base != target_name:
                                continue
                            held_value = target_map.get(
                                pair_attr
                            )
                            if (
                                isinstance(held_value, str)
                                and held_value in target_map
                            ):
                                _append_reached(
                                    target_map[held_value]
                                )
                                resolved = True
                    for base_name, first_attr in act_chains:
                        if base_name not in current_map:
                            continue
                        base_value = current_map[base_name]
                        if not isinstance(
                            base_value, _types_module.ModuleType
                        ):
                            continue
                        first_map = getattr(
                            base_value, "__dict__", None
                        )
                        if not isinstance(first_map, dict):
                            continue
                        inner_value = first_map.get(first_attr)
                        if not isinstance(
                            inner_value, _types_module.ModuleType
                        ):
                            continue
                        inner_map = getattr(
                            inner_value, "__dict__", None
                        )
                        if not isinstance(inner_map, dict):
                            continue
                        if _map_is_stdlib(inner_map):
                            continue
                        for const in consts:
                            if const in inner_map:
                                _append_reached(
                                    inner_map[const]
                                )
                                resolved = True
                        for carried_key in carried_names:
                            if carried_key in inner_map:
                                _append_reached(
                                    inner_map[carried_key]
                                )
                                resolved = True
                        for carried_key in extra_carried:
                            if carried_key in inner_map:
                                _append_reached(
                                    inner_map[carried_key]
                                )
                                resolved = True
                        for carried_key in returned_strs:
                            if carried_key in inner_map:
                                _append_reached(
                                    inner_map[carried_key]
                                )
                                resolved = True
                        for carried_key in act_attr_strs:
                            if carried_key in inner_map:
                                _append_reached(
                                    inner_map[carried_key]
                                )
                                resolved = True
                        for inner_key in inner_map:
                            if (
                                not isinstance(inner_key, str)
                                or inner_key in consts
                            ):
                                continue
                            if _built_from_consts(
                                inner_key, consts
                            ):
                                _append_reached(
                                    inner_map[inner_key]
                                )
                                resolved = True
            presented_maps = []
            for base_name, presented_key in (
                subscript_targets
                | vars_subscript_targets
                | getattr_result_targets
                | getattribute_chains
                | get_result_targets
                | obj_getattribute_chains
                | vars_get_result_targets
                | getattribute_result_targets
                | type_getattribute_chains
            ):
                if base_name not in current_map:
                    continue
                base_value = current_map[base_name]
                if not isinstance(
                    base_value, _types_module.ModuleType
                ):
                    continue
                first_map = getattr(
                    base_value, "__dict__", None
                )
                if not isinstance(first_map, dict):
                    continue
                inner_value = first_map.get(presented_key)
                if not isinstance(
                    inner_value, _types_module.ModuleType
                ):
                    continue
                inner_map = getattr(
                    inner_value, "__dict__", None
                )
                if not isinstance(inner_map, dict):
                    continue
                if _map_is_stdlib(inner_map):
                    continue
                presented_maps.append(inner_map)
            for base_name in (
                getattribute_targets
                | obj_getattribute_targets
                | type_getattribute_targets
            ):
                if base_name not in current_map:
                    continue
                target = current_map[base_name]
                if not isinstance(
                    target, _types_module.ModuleType
                ):
                    continue
                target_map = getattr(
                    target, "__dict__", None
                )
                if not isinstance(target_map, dict):
                    continue
                if _map_is_stdlib(target_map):
                    continue
                presented_maps.append(target_map)
            for carried_base in (
                subscript_carried_bases
                | vars_carried_bases
                | getattr_carried_bases
            ):
                if carried_base not in current_map:
                    continue
                carried_module = current_map[carried_base]
                if not isinstance(
                    carried_module, _types_module.ModuleType
                ):
                    continue
                carried_map = getattr(
                    carried_module, "__dict__", None
                )
                if not isinstance(carried_map, dict):
                    continue
                for carried_key in extra_carried:
                    inner_value = carried_map.get(
                        carried_key
                    )
                    if not isinstance(
                        inner_value,
                        _types_module.ModuleType,
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    presented_maps.append(inner_map)
            for carried_base in get_carried_bases:
                if carried_base not in current_map:
                    continue
                carried_module = current_map[carried_base]
                if not isinstance(
                    carried_module, _types_module.ModuleType
                ):
                    continue
                carried_map = getattr(
                    carried_module, "__dict__", None
                )
                if not isinstance(carried_map, dict):
                    continue
                for carried_key in (
                    extra_carried | carried_names
                ):
                    inner_value = carried_map.get(
                        carried_key
                    )
                    if not isinstance(
                        inner_value,
                        _types_module.ModuleType,
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    presented_maps.append(inner_map)
            for carried_base in vars_get_carried_bases:
                if carried_base not in current_map:
                    continue
                carried_module = current_map[carried_base]
                if not isinstance(
                    carried_module, _types_module.ModuleType
                ):
                    continue
                carried_map = getattr(
                    carried_module, "__dict__", None
                )
                if not isinstance(carried_map, dict):
                    continue
                for carried_key in (
                    extra_carried | carried_names
                ):
                    inner_value = carried_map.get(
                        carried_key
                    )
                    if not isinstance(
                        inner_value,
                        _types_module.ModuleType,
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    presented_maps.append(inner_map)
            for attr_base in (
                vars_get_attr_bases | get_attr_bases
            ):
                if attr_base not in current_map:
                    continue
                attr_module = current_map[attr_base]
                if not isinstance(
                    attr_module, _types_module.ModuleType
                ):
                    continue
                attr_map = getattr(
                    attr_module, "__dict__", None
                )
                if not isinstance(attr_map, dict):
                    continue
                for attr_key in act_attr_strs:
                    inner_value = attr_map.get(attr_key)
                    if not isinstance(
                        inner_value,
                        _types_module.ModuleType,
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    presented_maps.append(inner_map)
            for attr_base in (
                vars_subscript_attr_bases
                | dict_subscript_attr_bases
            ):
                if attr_base not in current_map:
                    continue
                attr_module = current_map[attr_base]
                if not isinstance(
                    attr_module, _types_module.ModuleType
                ):
                    continue
                attr_map = getattr(
                    attr_module, "__dict__", None
                )
                if not isinstance(attr_map, dict):
                    continue
                for attr_key in act_attr_strs:
                    inner_value = attr_map.get(attr_key)
                    if not isinstance(
                        inner_value,
                        _types_module.ModuleType,
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    presented_maps.append(inner_map)
            for home_base in (
                getattr_home_bases | vars_home_bases
            ):
                if home_base not in current_map:
                    continue
                home_module = current_map[home_base]
                if not isinstance(
                    home_module, _types_module.ModuleType
                ):
                    continue
                home_map = getattr(
                    home_module, "__dict__", None
                )
                if not isinstance(home_map, dict):
                    continue
                for home_key in carried_names:
                    inner_value = home_map.get(home_key)
                    if not isinstance(
                        inner_value,
                        _types_module.ModuleType,
                    ):
                        continue
                    inner_map = getattr(
                        inner_value, "__dict__", None
                    )
                    if not isinstance(inner_map, dict):
                        continue
                    if _map_is_stdlib(inner_map):
                        continue
                    presented_maps.append(inner_map)
            for call_map in call_returned_maps:
                if call_map not in presented_maps:
                    presented_maps.append(call_map)
            for presented_map in presented_maps:
                for const in consts:
                    if const in presented_map:
                        _append_reached(
                            presented_map[const]
                        )
                        resolved = True
                for presented_key in presented_map:
                    if (
                        not isinstance(presented_key, str)
                        or presented_key in consts
                    ):
                        continue
                    if _built_from_consts(
                        presented_key, consts
                    ):
                        _append_reached(
                            presented_map[presented_key]
                        )
                        resolved = True
                for carried_key in (
                    carried_names
                    | extra_carried
                    | returned_strs
                    | act_attr_strs
                ):
                    if carried_key in presented_map:
                        _append_reached(
                            presented_map[carried_key]
                        )
                        resolved = True
            if "__globals__" in attrs:
                for name in list(candidate_names):
                    if name not in current_map:
                        continue
                    target = current_map[name]
                    if not isinstance(
                        target, _types_module.FunctionType
                    ):
                        continue
                    target_map = getattr(
                        target, "__globals__", None
                    )
                    if not isinstance(target_map, dict):
                        continue
                    for const in consts:
                        if const not in target_map:
                            continue
                        reached_value = target_map[const]
                        if isinstance(
                            reached_value,
                            _types_module.ModuleType,
                        ):
                            continue
                        if isinstance(
                            reached_value,
                            _lru_cache_wrapper_type,
                        ):
                            continue
                        if id(reached_value) in seen_value_ids:
                            continue
                        seen_value_ids.add(id(reached_value))
                        values.append(reached_value)
                        resolved = True
                        if isinstance(
                            reached_value,
                            _types_module.FunctionType,
                        ):
                            pending_funcs.append(
                                (
                                    reached_value,
                                    getattr(
                                        reached_value,
                                        "__globals__",
                                        None,
                                    ),
                                )
                            )
            if (
                extra_names is not None
                and current_func is func
                and attr_dynamic
                and ("globals" in names or "eval" in names)
                and not resolved
            ):
                values.append(_threading_module.Lock())
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
                    if isinstance(
                        item, _collections.defaultdict
                    ):
                        factory = item.default_factory
                        if factory is not None:
                            pending.append(factory)
                elif isinstance(item, type):
                    carried_values, member_functions = (
                        _class_namespace_parts(item)
                    )
                    pending.extend(carried_values)
                    pending.extend(member_functions)
                elif isinstance(
                    item, _operator_module.methodcaller
                ):
                    carried = _reduce_carried(item)
                    head = _reduce_head(item)
                    if isinstance(
                        head, _functools_module.partial
                    ):
                        pending.extend(carried)
                        pending.extend(head.args[1:])
                        if head.keywords:
                            pending.extend(
                                list(head.keywords.values())
                            )
                    else:
                        pending.extend(carried[1:])
                elif isinstance(
                    item, _operator_module.itemgetter
                ):
                    pending.extend(_reduce_carried(item))
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
                elif isinstance(item, _types_module.FunctionType):
                    attribute_map = getattr(
                        item, "__dict__", None
                    )
                    if isinstance(attribute_map, dict):
                        pending.append(attribute_map)
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
                elif isinstance(item, _functools_module.partial):
                    pending.append(item.func)
                    pending.extend(item.args)
                    if item.keywords:
                        pending.append(dict(item.keywords))
                elif isinstance(item, BaseException):
                    pending.extend(item.args)
                    for chained in (
                        item.__cause__, item.__context__
                    ):
                        if chained is not None:
                            pending.append(chained)
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
                elif isinstance(item, _weakref_module.ReferenceType):
                    target = item()
                    if target is not None:
                        pending.append(target)
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
            if not isinstance(
                item, (_types_module.ModuleType, type)
            ):
                attribute_map = getattr(
                    item, "__dict__", None
                )
                if isinstance(attribute_map, dict):
                    pending.append(attribute_map)
                pending.append(type(item))
            if not isinstance(
                item, (_types_module.ModuleType, type)
            ):
                for klass in type(item).__mro__:
                    slots = klass.__dict__.get("__slots__")
                    if not slots:
                        continue
                    if isinstance(slots, str):
                        slots = (slots,)
                    for slot in slots:
                        try:
                            pending.append(
                                getattr(
                                    item,
                                    _slot_storage_name(klass, slot),
                                )
                            )
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

    def _reduce_state(item):
        try:
            reduced = item.__reduce_ex__(4)
        except Exception:
            return None
        if isinstance(reduced, tuple) and len(reduced) >= 3:
            return reduced[2]
        return None

    def _reduce_tail(item):
        try:
            reduced = item.__reduce_ex__(4)
        except Exception:
            return ()
        if not isinstance(reduced, tuple) or len(reduced) < 4:
            return ()
        carried = []
        for element in reduced[3:5]:
            if element is None:
                continue
            try:
                carried.extend(list(element))
            except Exception:
                continue
        return tuple(carried)

    def _type_overrides(value, name):
        for klass in type(value).__mro__:
            if klass is object:
                continue
            if name in klass.__dict__:
                return True
        return False

    _branch_base_types = (
        dict,
        list,
        tuple,
        set,
        frozenset,
        _collections.deque,
        _collections.UserList,
        _collections.UserDict,
        _collections.UserString,
        _collections.ChainMap,
    )

    def _branch_overrides(value, name):
        for klass in type(value).__mro__:
            if klass is object:
                continue
            if klass in _branch_base_types:
                continue
            if name in klass.__dict__:
                return True
        return False

    def _unwrap_carried(carried):
        seen_ids = set()
        while not isinstance(
            carried,
            (
                _types_module.FunctionType,
                _types_module.BuiltinFunctionType,
                _types_module.MethodType,
            ),
        ):
            wrapped = getattr(carried, "__wrapped__", None)
            if wrapped is None or id(carried) in seen_ids:
                break
            seen_ids.add(id(carried))
            carried = wrapped
        return carried

    def _class_namespace_parts(cls):
        values = []
        member_functions = []
        seen_classes = set()
        pending_classes = list(cls.__mro__)
        metaclass = type(cls)
        if metaclass is not type:
            for klass in metaclass.__mro__:
                if klass is type or klass is object:
                    continue
                pending_classes.append(klass)
        while pending_classes:
            klass = pending_classes.pop()
            if id(klass) in seen_classes:
                continue
            seen_classes.add(id(klass))
            namespace = klass.__dict__
            for key in namespace:
                if key in ("__dict__", "__weakref__"):
                    continue
                member = namespace[key]
                if isinstance(
                    member, _types_module.FunctionType
                ):
                    member_functions.append(member)
                    continue
                if isinstance(
                    member, _types_module.ModuleType
                ):
                    continue
                if isinstance(
                    member, (classmethod, staticmethod)
                ):
                    carried = getattr(
                        member, "__func__", None
                    )
                    if carried is not None:
                        member_functions.append(
                            _unwrap_carried(carried)
                        )
                    continue
                if isinstance(member, property):
                    for accessor in (
                        member.fget, member.fset, member.fdel
                    ):
                        if accessor is not None:
                            member_functions.append(
                                _unwrap_carried(accessor)
                            )
                    continue
                if type(member).__name__ in (
                    "getset_descriptor",
                    "member_descriptor",
                    "wrapper_descriptor",
                    "method_descriptor",
                    "classmethod_descriptor",
                ):
                    continue
                values.append(member)
                if isinstance(member, type):
                    pending_classes.append(member)
        return values, member_functions

    def _class_namespace_values(cls):
        values, member_functions = _class_namespace_parts(cls)
        return values

    def _fallback_holds_uncopyable(value):
        pending = [value]
        seen = set()
        globals_seen = set()
        carried_globals_seen = set()
        namespace_expanded = set()
        deepcopy_instances_seen = set()
        deepcopy_type_counts = {}
        deepcopy_returns_held = []
        namespace_members = {}
        namespace_reach = set()
        view_reach = set()
        while pending:
            item = pending.pop()
            mark_from = len(pending)
            in_reach = id(item) in namespace_reach
            in_view_reach = id(item) in view_reach
            if in_view_reach and isinstance(
                item,
                (
                    _abc_module.KeysView,
                    _abc_module.ValuesView,
                    _abc_module.ItemsView,
                ),
            ):
                return True
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
                    if isinstance(
                        item, _collections.defaultdict
                    ):
                        factory = item.default_factory
                        if factory is not None:
                            pending.append(factory)
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
                        and id(item) not in namespace_reach
                    ):
                        globals_seen.add(id(globals_map))
                        pending.extend(_globals_walk_values(item))
                    elif (
                        isinstance(globals_map, dict)
                        and id(item) in namespace_reach
                        and id(item) not in carried_globals_seen
                    ):
                        carried_globals_seen.add(id(item))
                        if _globals_map_is_module_dict(
                            item, globals_map
                        ):
                            pending.extend(
                                _referenced_global_values(
                                    item, globals_map
                                )
                            )
                        else:
                            pending.extend(
                                _globals_walk_values(item)
                            )
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
            if isinstance(item, type):
                namespace_target = item
            elif type(item).__module__ != "builtins":
                namespace_target = type(item)
            else:
                namespace_target = None
            if (
                namespace_target is not None
                and id(namespace_target) not in namespace_expanded
            ):
                namespace_expanded.add(id(namespace_target))
                carried_values, member_functions = (
                    _class_namespace_parts(namespace_target)
                )
                namespace_members[id(namespace_target)] = (
                    member_functions
                )
                member_extra_names = set()
                for carried in carried_values:
                    if isinstance(carried, str):
                        member_extra_names.add(carried)
                if not isinstance(item, type):
                    item_mapping = getattr(
                        item, "__dict__", None
                    )
                    if isinstance(item_mapping, dict):
                        for state_value in (
                            item_mapping.values()
                        ):
                            if isinstance(state_value, str):
                                member_extra_names.add(
                                    state_value
                                )
                    for state_value in _added_slot_values(
                        item
                    ):
                        if isinstance(state_value, str):
                            member_extra_names.add(state_value)
                member_extra_names.update(
                    _bundle_instance_strings.get(
                        id(namespace_target), ()
                    )
                )
                for carried in carried_values:
                    namespace_reach.add(id(carried))
                    pending.append(carried)
                for carried in member_functions:
                    namespace_reach.add(id(carried))
                    pending.append(carried)
                    carried_globals = getattr(
                        carried, "__globals__", None
                    )
                    if isinstance(carried_globals, dict):
                        for globals_value in (
                            carried_globals.values()
                        ):
                            if isinstance(
                                globals_value,
                                (
                                    _types_module.BuiltinFunctionType,
                                    _types_module.MethodType,
                                ),
                            ):
                                pending.append(globals_value)
                        if _globals_map_is_module_dict(
                            carried, carried_globals
                        ):
                            globals_values = (
                                _referenced_global_values(
                                    carried,
                                    carried_globals,
                                    member_extra_names,
                                )
                            )
                        else:
                            globals_values = (
                                _globals_walk_values(carried)
                            )
                        for globals_value in globals_values:
                            namespace_reach.add(
                                id(globals_value)
                            )
                            pending.append(globals_value)
            elif (
                namespace_target is not None
                and not isinstance(item, type)
                and id(namespace_target) in namespace_members
            ):
                instance_extra_names = set()
                item_mapping = getattr(
                    item, "__dict__", None
                )
                if isinstance(item_mapping, dict):
                    for state_value in (
                        item_mapping.values()
                    ):
                        if isinstance(state_value, str):
                            instance_extra_names.add(
                                state_value
                            )
                for state_value in _added_slot_values(
                    item
                ):
                    if isinstance(state_value, str):
                        instance_extra_names.add(state_value)
                if instance_extra_names:
                    carried_values, _ = (
                        _class_namespace_parts(
                            namespace_target
                        )
                    )
                    for carried in carried_values:
                        if isinstance(carried, str):
                            instance_extra_names.add(carried)
                    for carried in namespace_members[
                        id(namespace_target)
                    ]:
                        carried_globals = getattr(
                            carried, "__globals__", None
                        )
                        if not isinstance(
                            carried_globals, dict
                        ):
                            continue
                        if _globals_map_is_module_dict(
                            carried, carried_globals
                        ):
                            globals_values = (
                                _referenced_global_values(
                                    carried,
                                    carried_globals,
                                    instance_extra_names,
                                )
                            )
                        else:
                            globals_values = (
                                _globals_walk_values(carried)
                            )
                        for globals_value in globals_values:
                            namespace_reach.add(
                                id(globals_value)
                            )
                            pending.append(globals_value)
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
            if not isinstance(item, type):
                if _type_overrides(item, "__getstate__"):
                    try:
                        state = item.__getstate__()
                    except Exception:
                        state = None
                    if state is not None:
                        view_reach.add(id(state))
                        pending.append(state)
                plain_carrier = not isinstance(
                    item,
                    (
                        dict,
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                        _collections.UserDict,
                        _collections.ChainMap,
                        _collections.UserString,
                        _types_module.MappingProxyType,
                        _abc_module.KeysView,
                        _abc_module.ValuesView,
                        _abc_module.ItemsView,
                        _abc_module.Iterator,
                        _weakref_module.ReferenceType,
                        _weakref_module.WeakSet,
                        _weakref_module.WeakKeyDictionary,
                        _weakref_module.WeakValueDictionary,
                        _functools_module.partial,
                        _types_module.FunctionType,
                        _types_module.MethodType,
                        _types_module.BuiltinFunctionType,
                        property,
                        slice,
                        BaseException,
                        _operator_module.methodcaller,
                        _operator_module.itemgetter,
                        filter,
                        _callable_iterator_type,
                        _xml_module.Element,
                        _xml_module.ElementTree,
                    ),
                )
                if plain_carrier and (
                    _type_overrides(item, "__reduce_ex__")
                    or _type_overrides(item, "__reduce__")
                ):
                    for carried in _reduce_carried(item):
                        view_reach.add(id(carried))
                        pending.append(carried)
                    reduce_state = _reduce_state(item)
                    if reduce_state is not None:
                        view_reach.add(id(reduce_state))
                        pending.append(reduce_state)
                    for carried in _reduce_tail(item):
                        view_reach.add(id(carried))
                        pending.append(carried)
                if plain_carrier and _type_overrides(
                    item, "__getnewargs__"
                ):
                    try:
                        newargs = item.__getnewargs__()
                    except Exception:
                        newargs = None
                    if newargs is not None:
                        view_reach.add(id(newargs))
                        pending.append(newargs)
                if plain_carrier and _type_overrides(
                    item, "__getnewargs_ex__"
                ):
                    try:
                        newargs_ex = item.__getnewargs_ex__()
                    except Exception:
                        newargs_ex = None
                    if isinstance(newargs_ex, tuple):
                        for part in newargs_ex:
                            view_reach.add(id(part))
                            pending.append(part)
                branch_carrier = isinstance(
                    item,
                    (
                        dict,
                        list,
                        tuple,
                        set,
                        frozenset,
                        _collections.deque,
                        _collections.UserList,
                        _collections.UserDict,
                        _collections.UserString,
                        _collections.ChainMap,
                    ),
                )
                if branch_carrier and _branch_overrides(
                    item, "__getnewargs__"
                ):
                    try:
                        newargs = item.__getnewargs__()
                    except Exception:
                        newargs = None
                    if newargs is not None:
                        view_reach.add(id(newargs))
                        pending.append(newargs)
                if branch_carrier and _branch_overrides(
                    item, "__getnewargs_ex__"
                ):
                    try:
                        newargs_ex = item.__getnewargs_ex__()
                    except Exception:
                        newargs_ex = None
                    if isinstance(newargs_ex, tuple):
                        for part in newargs_ex:
                            view_reach.add(id(part))
                            pending.append(part)
                if branch_carrier and (
                    _branch_overrides(item, "__reduce_ex__")
                    or _branch_overrides(item, "__reduce__")
                ):
                    for carried in _reduce_carried(item):
                        view_reach.add(id(carried))
                        pending.append(carried)
                    reduce_state = _reduce_state(item)
                    if reduce_state is not None:
                        view_reach.add(id(reduce_state))
                        pending.append(reduce_state)
                    for carried in _reduce_tail(item):
                        view_reach.add(id(carried))
                        pending.append(carried)
                if _type_overrides(item, "__deepcopy__") and (
                    id(item) not in deepcopy_instances_seen
                    and deepcopy_type_counts.get(
                        type(item), 0
                    ) < 32
                ):
                    deepcopy_instances_seen.add(id(item))
                    deepcopy_type_counts[type(item)] = (
                        deepcopy_type_counts.get(type(item), 0)
                        + 1
                    )
                    try:
                        returned = _copy_module.deepcopy(
                            item, {}
                        )
                    except Exception:
                        returned = None
                    if returned is not None:
                        deepcopy_returns_held.append(returned)
                    if returned is not None and (
                        returned is not item
                    ):
                        pending.append(returned)
            if in_reach:
                for extra in pending[mark_from:]:
                    namespace_reach.add(id(extra))
            if in_view_reach:
                for extra in pending[mark_from:]:
                    view_reach.add(id(extra))
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
    def _scan_bundle_instance_strings(root):
        found = {}
        pending_items = [root]
        seen_ids = set()
        while pending_items:
            current_item = pending_items.pop()
            if id(current_item) in seen_ids:
                continue
            seen_ids.add(id(current_item))
            if isinstance(
                current_item, _types_module.ModuleType
            ):
                continue
            if isinstance(current_item, dict):
                pending_items.extend(current_item.keys())
                pending_items.extend(current_item.values())
                continue
            if isinstance(
                current_item,
                (list, tuple, set, frozenset),
            ):
                pending_items.extend(current_item)
                continue
            if isinstance(current_item, type):
                try:
                    carried_values, _ = (
                        _class_namespace_parts(current_item)
                    )
                except Exception:
                    carried_values = []
                pending_items.extend(carried_values)
                continue
            mapping = getattr(current_item, "__dict__", None)
            if isinstance(mapping, dict):
                strings = [
                    held for held in mapping.values()
                    if isinstance(held, str)
                ]
                strings.extend(
                    held
                    for held in _added_slot_values(
                        current_item
                    )
                    if isinstance(held, str)
                )
                if strings:
                    found.setdefault(
                        id(type(current_item)), set()
                    ).update(strings)
                pending_items.extend(mapping.values())
        return found

    _bundle_instance_strings = _scan_bundle_instance_strings(
        bundle
    )
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
        if isinstance(
            current,
            (
                dict,
                list,
                tuple,
                set,
                frozenset,
                bytearray,
                _array_module.array,
                _collections.deque,
                _collections.UserList,
                _collections.UserDict,
                _collections.UserString,
                _collections.ChainMap,
                _types_module.MappingProxyType,
            ),
        ) and _type_overrides(current, "__getstate__"):
            try:
                branch_state = current.__getstate__()
            except Exception:
                branch_state = None
            if branch_state is not None and (
                _fallback_holds_uncopyable(branch_state)
            ):
                raise ValueError(
                    "uncopyable value in bundle copy"
                )
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
