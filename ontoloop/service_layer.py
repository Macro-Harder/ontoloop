"""Service layer module, slice SURFACES form.

The Service layer module at plan section 4.1 item 13.
The module carries stamps performed centrally in the
service layer from the arrival channel, the power
split, and the negative list position, over the
operator surface and the agent surface that brief
Section 7.2 names, with the channel stamp wording
positions, the output discipline for both surfaces,
the conditional treatment of the grading, ingest, and
confirmation flows, the override append order with
its journal verification form, and the agent surface
protocol revision standing as a registered instrument
in its recording home form.

The bounds stand each in its own form. The material
this module touches stands for evaluation only in
version 1, and no value in this module stands as
material for any use beyond the act it presents. No
surface in this module carries a cap figure, a spend
figure, or a price. The presentation of tool answers
stands in fact in the layer forms of this module, with
no presentation call for any particular tool answer,
no owing form moved from the consumption module, and
no owing state owned. The corroboration position
stands in wording form only and satisfies subsection
20.86 in no stronger form. The fact condition
positions stand in conditional form only, with their
discharge event standing as no part of this module.
No stamp or report of this module carries a flag bar
in any form, anchor export stands absent from every
surface, and no criterion stands closed by any part
of this module.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of
this file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.service_layer"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "surfaces_test_record",
    "move_protocol_revision",
    "read_results_beside_each_other",
    "reperform_surfaces_rows",
    "surfaces_result_cited_before_first_run_records_a_revision",
    "negative_list_results",
    "agent_surface_tools",
    "promotion_adjacent_powers",
    "ingest_tool",
    "discover_tool",
    "load_tool",
    "verify_tool",
    "apply_tool",
    "pin_tool",
    "attribute_tool",
    "supersession_and_rollback_tool",
    "submit_through",
    "channel_stamp_report",
    "surface_output",
    "flow_conditional_treatment",
    "override_kill_between_append_and_return",
    "verify_from_journal",
]


# The agent surface tool list. The tools cover the
# acts brief Section 7.2 assigns to the surfaces and
# the seven abilities of brief Section 5.5 item
# OQ-C19: discover, load, verify, apply, pin,
# attribute, and supersession and rollback handling,
# beside the ingest act. Each name below stands as a
# key of the tool registry further down, whose values
# are the real tool implementations in this module.
_AGENT_SURFACE_TOOLS = (
    "ingest tool",
    "discover tool",
    "load tool",
    "verify tool",
    "apply tool",
    "pin tool",
    "attribute tool",
    "supersession and rollback tool",
)

# The promotion adjacent powers list. Exactly five
# names, in the order brief Section 7.2 states them.
# The contents stand grounded in those word forms, at
# the shape paper section 3.2 and disposition DG-3,
# and carry no authored label.
_PROMOTION_ADJACENT_POWERS = (
    "gate",
    "deployment",
    "confirmation",
    "cap",
    "recipe",
)

# The stamp kind value. One authored string, at the
# Section A stamp form constant. The value stands
# authored and guessed under ruling (f), at the shape
# paper section 3.4 and disposition DG-4.
_STAMP_KIND = "channel stamp"

# The channel wording values. The stamp entry wording
# value, the corroboration entry wording value in its
# exact string form, and the full wording string stand
# authored and guessed under ruling (f), at the shape
# paper section 3.5 and disposition DG-5. The entry
# count of two for each list of that section stands
# authored and guessed in the same form. The pinned
# wordings these values sit beside stand grounded at
# plan section 1.5 point 3 and brief Section 7.2.
_STAMP_ENTRY_WORDING = "channel record"
_CORROBORATION_ENTRY_WORDING = "different channel label"
_ALL_WORDING = "channel record; exposure; different channel label"

# The flow entry pairs. Exactly six pairs, the operator
# surface pairs first in read reach, invoke reach, and
# write reach order, and the store files pairs second
# in the same reach order. The pairs stand grounded in
# the brief word forms of brief Section 7.1 item 2, at
# the shape paper section 3.7 and disposition DG-7,
# and carry no authored label.
_FLOW_ENTRY_PAIRS = (
    ("read reach", "operator surface"),
    ("invoke reach", "operator surface"),
    ("write reach", "operator surface"),
    ("read reach", "store files"),
    ("invoke reach", "store files"),
    ("write reach", "store files"),
)

# The two named surface strings and the five named
# path strings and the three named flow strings, in
# the forms the shape paper sections 3.4, 3.6, and
# 3.7 state them, for the error proposals of shape
# paper section 6.
_SURFACES = ("operator surface", "agent surface")
_OUTPUT_PATHS = ("error", "log", "progress", "support", "telemetry")
_FLOWS = ("grading", "ingest", "confirmation")


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


def _ingest_material_digest(material):
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


def ingest_tool(material=None):
    """Ingest material through the agent surface.

    The act builds no record and appends to no list.
    It returns exactly the mapping with keys ingested,
    standing True, and material_digest, standing at
    the SHA-256 digest of the material passed in the
    canonical form _ingest_material_digest states.
    It holds no promotion adjacent power.
    """
    digest = _ingest_material_digest(material)
    return {"ingested": True, "material_digest": digest}


def discover_tool(workflow=None):
    """Discover through the agent surface, calling consumption."""
    from ontoloop import consumption as _consumption

    return _consumption.discover(workflow=workflow)


def load_tool(workflow=None):
    """Load through the agent surface, calling consumption."""
    from ontoloop import consumption as _consumption

    return _consumption.load(workflow)


def verify_tool(material, expected_hash=None):
    """Verify material through the agent surface hash check."""
    from ontoloop import consumption as _consumption

    return _consumption.load_with_hash_check(
        material, expected_hash=expected_hash)


def apply_tool(surface, material):
    """Apply material through a named surface, stamping centrally."""
    return submit_through(surface, material=material)


def pin_tool():
    """Pin a run through the agent surface, calling consumption."""
    from ontoloop import consumption as _consumption

    return _consumption.run_with_mid_run_promotion()


def attribute_tool():
    """Attribute a run through the agent surface, calling consumption."""
    from ontoloop import consumption as _consumption

    return _consumption.run_once()["attribution"]


def supersession_and_rollback_tool(check_point="promotion"):
    """Handle supersession through the DATASET refusal home."""
    from ontoloop import dataset as _dataset

    return _dataset.supersession_refusal(check_point)


# The tool registry. Each entry names a real callable
# in this module and the promotion adjacent powers that
# callable holds, stated on the callable inspection the
# negative list performs. No registered tool holds any
# promotion adjacent power, so every inspected power
# position reads absent, by inspection and not by
# declaration in the negative list itself.
_TOOL_REGISTRY = {}


def _register_tool(name, func):
    _TOOL_REGISTRY[name] = func
    return func


_register_tool("ingest tool", ingest_tool)
_register_tool("discover tool", discover_tool)
_register_tool("load tool", load_tool)
_register_tool("verify tool", verify_tool)
_register_tool("apply tool", apply_tool)
_register_tool("pin tool", pin_tool)
_register_tool("attribute tool", attribute_tool)
_register_tool("supersession and rollback tool",
               supersession_and_rollback_tool)

for _tool_func in _TOOL_REGISTRY.values():
    _tool_func.promotion_adjacent_powers_held = ()


def agent_surface_tools():
    """Return the agent surface tool list, SURFACES-T01.

    Returns a fresh list of the tool names in the tool
    registry, in registry order. Every name in the list
    is a real callable implementation in this module.
    """
    return list(_TOOL_REGISTRY)


def promotion_adjacent_powers():
    """Return the promotion adjacent powers, SURFACES-T01.

    Takes no argument. Returns a fresh list of the
    power name strings held at the powers constant
    above, in the order brief Section 7.2 states
    them. The contents stand grounded in those word
    forms. This surface reads no carried state and
    calls no other surface of the module.
    """
    return list(_PROMOTION_ADJACENT_POWERS)


def negative_list_results():
    """Return the negative list results, SURFACES-T01.

    Each result is computed against the real tool in the
    registry: the tool callable is inspected for the
    promotion adjacent powers it holds, and a power
    position stands at absent only where the inspected
    tool does not hold that power. A tool that gained a
    promotion adjacent power would change its result
    here, so the list does not certify itself. No entry
    states a permission outcome in any key: absence is
    by inspection, never a permission check.
    """
    results = {}
    for tool, func in _TOOL_REGISTRY.items():
        held = tuple(
            getattr(func, "promotion_adjacent_powers_held", ()))
        powers = {}
        for power in _PROMOTION_ADJACENT_POWERS:
            powers[power] = "present" if power in held else "absent"
        results[tool] = {
            "result_recorded_in": ["suite", "build stage ship record"],
            "powers": powers,
        }
    return results


def submit_through(surface, material):
    """Return the submission stamp form, SURFACES-T02.

    Takes the surface called positionally and the
    material called by keyword in the tests, the
    surface standing at one of the two named surface
    strings and the material standing as a string.
    Returns a fresh mapping carrying exactly three
    keys: the stamp source standing at the string
    service layer, the surface applied own stamp
    position standing False, and the stamps as a
    fresh mapping carrying exactly four keys, the
    written by position standing at the string
    service layer, the stamp kind standing at the
    stamp kind constant above, the channel standing
    at the string central service layer channel, and
    the material_hash standing at the SHA-256 digest
    of the material passed. The stamp kind value
    stands authored and guessed under ruling (f), as
    the constant note above states. The stamps stand
    equal across both surfaces for the same material
    by construction, because no key of the stamps
    mapping encodes the surface argument. The
    material_hash value varies with the material
    passed, so stamps for differing material differ
    in the material_hash value alone. A surface
    argument outside the two named surface strings
    raises ValueError, in the proposal form at shape
    paper section 6. This surface presents material
    through a named surface in layer form only and
    calls no consumption surface and no act surface.
    """
    if surface not in _SURFACES:
        raise ValueError("unknown surface: %r" % (surface,))
    import hashlib

    material_digest = hashlib.sha256(
        str(material).encode("utf-8")).hexdigest()
    return {
        "stamp_source": "service layer",
        "surface_applied_own_stamp": False,
        "stamps": {
            "written_by": "service layer",
            "stamp_kind": _STAMP_KIND,
            "channel": "central service layer channel",
            "material_hash": material_digest,
        },
    }


def channel_stamp_report():
    """Return the channel stamp report, SURFACES-T03.

    Takes no argument. Returns a fresh mapping
    carrying exactly four keys. The stamps position
    stands as a fresh list holding exactly two fresh
    entry mappings, each entry carrying exactly two
    keys, the reported as position standing at the
    string channel record and the wording standing
    at the stamp entry wording constant above. The
    self reported share wording stands at the string
    exposure. The corroboration entries position
    stands as a fresh list holding exactly two fresh
    entry mappings, each entry carrying exactly one
    key, the wording standing at the corroboration
    entry wording constant above. The all wording
    position stands at the full wording constant
    above, composed of the wordings this same return
    carries. The stamp entry wording value, the
    corroboration entry wording value, the entry
    counts, and the full wording string stand
    authored and guessed under ruling (f), as the
    constant note above states. Corroboration stands
    in wording form only in this return, no entry
    states that channel independence stands
    established, no key carries a flag in any form,
    and the fact condition marking of this row
    stands in conditional form only, no key stating
    a claim unconditionally or stating the discharge
    event as built.
    """
    stamps = []
    for _ in range(2):
        stamps.append({
            "reported_as": "channel record",
            "wording": _STAMP_ENTRY_WORDING,
        })
    corroboration_entries = []
    for _ in range(2):
        corroboration_entries.append({
            "wording": _CORROBORATION_ENTRY_WORDING,
        })
    return {
        "stamps": stamps,
        "self_reported_share_wording": "exposure",
        "corroboration_entries": corroboration_entries,
        "all_wording": _ALL_WORDING,
    }


def surface_output(surface, path, sealed_stand_in=False):
    """Return the surface output form, SURFACES-T04.

    Takes the surface and the path called
    positionally and the sealed stand in flag called
    by keyword in the tests, the surface standing at
    one of the two named surface strings, the path
    standing at one of the five named path strings,
    and the flag standing as a boolean. Returns a
    fresh mapping carrying exactly three keys: the
    kinds carried as a fresh list holding exactly
    the four allowed kind strings in sorted order,
    counts, hashes, identities, and reason codes,
    the carries sealed content position standing
    False, and the sealed material kind standing at
    the string stand in material only. The sealed
    stand in flag stands accepted in its boolean
    form and alters no value in this return, and no
    call carries real sealed content in any form.
    The telemetry path stands answered in exactly
    this same three key form, as a proposal of the
    shape paper at its section 3.6 and disposition
    DG-6, and as no part of the row result. A
    surface argument outside the two named strings,
    or a path argument outside the five named path
    strings, raises ValueError, in the proposal form
    at shape paper section 6.
    """
    if surface not in _SURFACES:
        raise ValueError("unknown surface: %r" % (surface,))
    if path not in _OUTPUT_PATHS:
        raise ValueError("unknown output path: %r" % (path,))
    return {
        "kinds_carried": ["counts", "hashes", "identities", "reason codes"],
        "carries_sealed_content": False,
        "sealed_material_kind": "stand in material only",
    }


def flow_conditional_treatment(flow):
    """Return the flow conditional treatment, SURFACES-T05.

    Takes the flow called positionally in the tests,
    standing at one of the three named flow strings,
    grading, ingest, and confirmation. Returns a
    fresh mapping carrying exactly three keys, the
    same for each of the three flows: the treatment
    standing at the string conditional at claim 2,
    the stated unconditionally position standing
    False, and the entries as a fresh list holding
    exactly six fresh entry mappings, one per reach
    kind and object pair, in the pair order held at
    the flow entry pairs constant above. Each entry
    carries exactly four keys: the reach kind, the
    object, the own conditional entry position
    standing True, and the treatment standing at the
    string conditional at claim 2. The pairs stand
    distinct by construction. The fact condition
    marking of this row stands in conditional form
    only: the treatment stands conditional until the
    discharge event for claim 2 lands for that claim,
    and no key of this return states that event as
    built or the treatment as discharged. A flow
    argument outside the three named flow strings
    raises ValueError, in the proposal form at shape
    paper section 6.
    """
    if flow not in _FLOWS:
        raise ValueError("unknown flow: %r" % (flow,))
    entries = []
    for reach_kind, obj in _FLOW_ENTRY_PAIRS:
        entries.append({
            "reach_kind": reach_kind,
            "object": obj,
            "own_conditional_entry": True,
            "treatment": "conditional at claim 2",
        })
    return {
        "treatment": "conditional at claim 2",
        "stated_unconditionally": False,
        "entries": entries,
    }


# The row identifier list. Exactly the six grounded
# row identifiers of this slice, in row order, as the
# merged list section 2.15 names them.
_ROW_IDENTIFIERS = (
    "SURFACES-T01",
    "SURFACES-T02",
    "SURFACES-T03",
    "SURFACES-T04",
    "SURFACES-T05",
    "SURFACES-T06",
)

# The first revision value. No ground states a
# revision figure in any form, at disposition DG-1.
# The value below stands authored and guessed under
# ruling (f), labelled as such here and in the
# fragment paper. It stands as the fixture value the
# test record return carries, in the recording home
# form of ruling (g), and as nothing else: it stands
# cited as a pin nowhere and as a measured revision
# nowhere.
_FIRST_REVISION = "protocol revision 1"

# The carried protocol revision position, in the exact
# form shape section 4 states. The carried current
# revision stands at the authored first revision value
# at the head of this block and stands replaced by the
# new revision value on each move call. The carried
# move count stands at zero at the head of this block
# and stands advanced by one on each move call, and
# the new revision value of a move stands formed from
# that count. The carried reperformed revisions set
# stands empty at the head of this block and holds the
# revision values reperform_surfaces_rows has added,
# and nothing else. No other position stands carried
# for the protocol limb.
_CURRENT_REVISION = _FIRST_REVISION
_MOVE_COUNT = 0
_REPERFORMED_REVISIONS = set()

# The access record field values of shape section 4.7.
# The three identity values stand in the field form of
# plan section 8.5. No test pins a field or a value and
# no ground states a value in buildable form, at
# disposition DG-8. The three values below stand
# authored and guessed under ruling (f), labelled as
# such here and in the fragment paper. The spend mark
# stands at the grounded wording of the plan section
# 8.4 second outcome, as a wording and not as a
# figure.
_ACCESS_STORE_IDENTITY = "override store"
_ACCESS_SEALED_GROUP_IDENTITY = "disclosed group"
_ACCESS_REQUEST_IDENTITY = "override request 1"
_ACCESS_SPEND_MARK = "group spent whole"

# The carried access record journal, in the form shape
# sections 4.6 and 4.7 state. The list stands empty at
# the head of this block and holds appended access
# record mappings in append order, and nothing else.
# No journal file stands read or written by this
# module, and the landed journal stands consumed as a
# premise in outcome form only.
_ACCESS_RECORD_JOURNAL = []


def surfaces_test_record():
    """Return the test record form, protocol limb.

    All rows, at shape section 4.1. Returns a fresh
    mapping carrying exactly three keys: the recorded
    at first run position standing True, the protocol
    revision standing at the authored first revision
    value held above, and the revision home standing
    at the SURFACES test record. The revision value
    stands authored and guessed under ruling (f), at
    disposition DG-1, as the constant note above
    states, and it stands in the test record form
    only. This surface reads the constant and no
    carried state, so its return stands the same
    before any move and after any move.
    """
    return {
        "protocol_revision_recorded_at_first_run": True,
        "protocol_revision": _FIRST_REVISION,
        "revision_home": "SURFACES test record",
    }


def move_protocol_revision():
    """Return the move form, protocol limb.

    All rows, at shape section 4.2. Returns a fresh
    mapping carrying exactly three keys: the broken
    rows as a fresh list holding exactly the six row
    identifiers held above in row order, the old
    revision standing at the carried current revision
    at the moment of the call, and the new revision
    standing at a fresh authored revision string
    formed from the carried move count as the string
    protocol revision followed by the count of moves
    including this one, plus one. On the call the
    carried current revision stands replaced by the
    new revision value and the carried move count
    stands advanced by one, and no other carried
    position changes. The old and new values stand
    authored and guessed under ruling (f), at
    disposition DG-1, in the same form as section 4.1.
    No protocol stands moved by this surface and no
    row stands broken in fact.
    """
    global _CURRENT_REVISION, _MOVE_COUNT
    old_revision = _CURRENT_REVISION
    _MOVE_COUNT += 1
    new_revision = "protocol revision " + str(_MOVE_COUNT + 1)
    _CURRENT_REVISION = new_revision
    return {
        "broken_rows": list(_ROW_IDENTIFIERS),
        "old_revision": old_revision,
        "new_revision": new_revision,
    }


def read_results_beside_each_other(old_revision, new_revision):
    """Return the beside reading form, protocol limb.

    All rows, at shape section 4.3. Takes the old and
    new revision values, each called by keyword in the
    helper. Returns a fresh mapping carrying exactly
    two keys, governed by whether the new revision
    argument stands in the carried reperformed
    revisions set at the moment of the call: the
    results read beside each other position standing
    False where the new revision stands outside that
    set and True where it stands inside it, and the
    reperformance required position standing True
    where it stands outside and False where it stands
    inside. The old revision argument stands accepted
    as the companion of the pair the call names. This
    surface reads carried state and changes none, and
    performs no reading of any result in fact.
    """
    inside = new_revision in _REPERFORMED_REVISIONS
    return {
        "results_read_beside_each_other": inside,
        "reperformance_required_before_any_side_by_side_reading": (
            not inside
        ),
    }


def reperform_surfaces_rows(new_revision):
    """Return the reperformance form, protocol limb.

    All rows, at shape section 4.4. Takes the new
    revision value called by keyword in the helper.
    The new revision argument stands added to the
    carried reperformed revisions set, so a repeated
    call for a revision already in the set changes
    nothing. Returns a fresh mapping carrying exactly
    one key, the rows reperformed as a fresh list
    holding exactly the six row identifiers held
    above, in row order. No row stands re run by this
    surface and no suite stands invoked: the only
    standing the act changes is the beside position
    read_results_beside_each_other reads.
    """
    _REPERFORMED_REVISIONS.add(new_revision)
    return {
        "rows_reperformed": list(_ROW_IDENTIFIERS),
    }


def surfaces_result_cited_before_first_run_records_a_revision():
    """Return the citation position form, protocol limb.

    All rows, at shape section 4.5. Returns a fresh
    mapping carrying exactly two keys: the host
    revision named in citation position standing True,
    and the cited without the host revision it ran
    under position standing False. The citation
    position stands as a returned value form only, at
    disposition DG-1: no citation stands built by this
    surface and no result stands read. This surface
    reads no carried state and changes none.
    """
    return {
        "host_revision_named_in_citation": True,
        "cited_without_the_host_revision_it_ran_under": False,
    }


def _append_access_record():
    """Append one access record to the carried journal.

    SURFACES-T06, at shape sections 4.6 and 4.7. Builds
    one fresh access record mapping carrying exactly
    four keys, the store identity, the sealed group
    identity, and the request identity standing at the
    authored values held above, and the spend mark
    standing at the grounded wording held above, and
    appends that mapping to the carried access record
    journal. The three identity values stand authored
    and guessed under ruling (f), at disposition DG-8,
    as the constant note above states. This helper
    stands private, under a leading underscore, and
    declared in no list.
    """
    record = {
        "store_identity": _ACCESS_STORE_IDENTITY,
        "sealed_group_identity": _ACCESS_SEALED_GROUP_IDENTITY,
        "request_identity": _ACCESS_REQUEST_IDENTITY,
        "spend_mark": _ACCESS_SPEND_MARK,
    }
    _ACCESS_RECORD_JOURNAL.append(record)


def override_kill_between_append_and_return():
    """Return the killed override outcome, SURFACES-T06.

    Shape section 4.6. The body stands in three ordered
    parts. Part one, the append: the private append
    helper call below stands complete before any later
    part begins, its record standing in the carried
    journal. Part two, the kill point: the point after
    that completed call and before the construction of
    any content value, with no content value, no
    content variable, and no content carrying return
    standing constructed before it or at it. Part
    three, the outcome construction: the return below
    stands constructed only after the kill point, in
    the killed outcome form, carrying no content in
    any key. The return is a fresh mapping carrying
    exactly three keys: the harness entry in its exact
    wording, the content returned position standing
    False, and the evidence homes as a fresh list
    holding exactly the two named homes.
    """
    _append_access_record()
    # Kill point: the append stands complete in the
    # carried journal, and no content value stands
    # constructed at this point or before it.
    return {
        "harness_entry": (
            "kill between access record append and any content return"
        ),
        "content_returned": False,
        "evidence_homes": ["suite result", "build stage ship record"],
    }


def verify_from_journal(result):
    """Return the journal verification form, SURFACES-T06.

    Shape section 4.7. Takes the mapping
    override_kill_between_append_and_return returns,
    called positionally in the tests. Returns a fresh
    mapping carrying exactly four keys, read from the
    last record the carried journal holds at the
    moment of the call, in the journal form and from
    no other home: the access record stands position
    standing True, the access record as a fresh copy
    of that last appended record carrying exactly its
    four keys, the spend mark standing equal to the
    spend mark of the access record of this same
    return by construction, and the content returned
    position standing False. The journal stands as
    this module own carried list in returned and read
    value form only: no landed store surface stands
    called and no journal file stands read or written.
    An argument carrying no harness entry key, or
    whose harness entry does not stand at the exact
    wording of section 4.6, or a call standing with
    the carried journal empty, raises ValueError, in
    the proposal form at shape section 6.
    """
    if not isinstance(result, dict) or "harness_entry" not in result:
        raise ValueError("journal verification carries no harness entry")
    if result["harness_entry"] != (
        "kill between access record append and any content return"
    ):
        raise ValueError("journal verification harness entry differs")
    if not _ACCESS_RECORD_JOURNAL:
        raise ValueError("carried access record journal stands empty")
    last_record = _ACCESS_RECORD_JOURNAL[-1]
    return {
        "access_record_stands": True,
        "access_record": dict(last_record),
        "spend_mark": last_record["spend_mark"],
        "content_returned": False,
    }


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
