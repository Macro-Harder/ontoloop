"""Cross split audit module, shared at one seam.

One shared module with three call points, at dataset
build, at evaluation, and at promotion, over one
relation set only: the group relation, the signature
relation, and the near verbatim cluster relation.
Paraphrase stands outside the tested relations, and no
return of this module carries a paraphrase clearance
in any form.

Material forms. A call point presents either a single
flagged item, as a string or as a mapping carrying its
group, signature, and text, or a bundle mapping
carrying candidate_items and holdout_items, each item
a mapping of that same shape, with an optional split
field naming its side. A single item presented to the
audit stands as the flagged material in the bundle:
its refusal states presentation as its ground, and it
carries no firing pair and no comparison count,
because no comparison over holdout material runs on
that form. The instruction item act,
audit_instruction_item, takes one instruction text
and the holdout material and decides verbatim and
near verbatim firing over the instruction text field
only, by the near verbatim relation form of this
module, and on firing returns the refusal form of
this module at the occasion named. A
bundle is audited in fact: candidate and holdout items
are compared over an index keyed on the group and
signature relations, pairs sharing neither relation
are not compared, and a pair fires where it shares a
group, shares a signature, or its texts stand in a
near verbatim cluster relation. A bundle with no firing
pair is not refused.

Bounding rule, plan subsection 19.94 point one.
Comparisons run over the group and signature keyed
index, never over all pairs. The revisit volume stands
at 20,000 runs in scope, guessed. Example E prices a
cross split audit comparison per pair at 5 work units,
guessed, replaced by the first cost pilot, and the
cost counting in this module counts comparisons per
pair at that weight.

Charging form, plan subsection 19.36 point three. An
attempt is charged as one completed evaluation where
any case was scored before the refusal, and as no
completed evaluation where no case was scored, at
every call point.

What this module does not build stands absent from it
altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of
this file.
"""

MODULE_NAME = "ontoloop.cross_split_audit"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "audit_at_build",
    "audit_at_evaluation",
    "audit_at_promotion",
    "audit_instruction_item",
    "indexed_comparisons",
    "relations",
]

RELATIONS = ("group", "signature", "near verbatim cluster")

_ERROR_NAME = "flagged material inside candidate bundle"
_TYPED_REASON = (
    "spanning pair over a tested relation between the "
    "candidate bundle and the sealed holdout"
)
_PRESENTATION_REASON = (
    "refused on its presentation as flagged material"
)
_INSTRUCTION_TEST_RESULT = (
    "holdout content found in instruction item"
)
_CHARGING_FORM_AFTER_PARTIAL_SCORING = (
    "standing charging form for a refusal after partial scoring"
)
_AUDIT_RECORD_HOME = "cross split audit record for the candidate"
_COST_WEIGHT_PER_PAIR = 5
_REVISIT_VOLUME_RUNS = 20000
_NEAR_VERBATIM_OVERLAP = 0.75


def relations():
    """Return the relation set, exactly the three relations."""
    return list(RELATIONS)


import array as _array_module
import collections as _collections_module
import types as _types_module
from collections import UserString as _UserString
from collections.abc import ItemsView as _ItemsView
from collections.abc import KeysView as _KeysView
from collections.abc import Mapping as _Mapping
from collections.abc import Sequence as _Sequence
from collections.abc import Set as _Set
from collections.abc import ValuesView as _ValuesView
from weakref import WeakSet as _WeakSet


def _byte_content(value):
    """Return the byte content a byte like value carries.

    A memoryview stands read as the byte content it
    views, and an array in the array form stands read
    as the bytes it holds, in the same form as a byte
    string or a bytearray, whatever typecode the array
    stands in, in parity with a memoryview over the
    same array. An array in the unicode typecode stands
    read as the character content it holds, in the
    same text form as a plain string, and a memoryview
    over such an array stands read in that same form.
    """
    if isinstance(value, memoryview):
        viewed = value.obj
        if isinstance(
            viewed, _array_module.array
        ) and viewed.typecode == "u":
            raw = value.tobytes()
            unit = viewed.itemsize
            trimmed = raw[: len(raw) - len(raw) % unit]
            sliced = _array_module.array("u")
            sliced.frombytes(trimmed)
            return sliced.tounicode().encode("utf-8")
        return value.tobytes()
    if isinstance(value, _array_module.array):
        if value.typecode == "u":
            return value.tounicode().encode("utf-8")
        return value.tobytes()
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    return None


def _is_byte_like(value):
    return _byte_content(value) is not None


def _materialise_kind(value):
    """Name the container form a value stands in.

    A text or byte form stands as a leaf in full: a
    string, a UserString, a byte string, a bytearray,
    a memoryview, an array, and a range each keep the
    reading the neighbouring acts give them, and a
    value carrying no iteration act and no indexed
    access act stands as a leaf in the same way. A
    mapping, a dictionary view, the standing collection
    forms, an iterator, the abstract Set form with a
    WeakSet among the set forms, the abstract Sequence
    form, any other value carrying an iteration act,
    and a value standing in a container form that
    iterates by indexed access alone, carrying an
    indexed access act and no iteration act, each stand
    named for the rebuilding the materialisation act
    gives that form.
    """
    if isinstance(
        value,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return "leaf"
    if isinstance(value, _Mapping):
        return "mapping"
    if isinstance(value, (_ItemsView, _KeysView, _ValuesView)):
        return "dictionary view"
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        return "collection"
    if hasattr(value, "__next__") and hasattr(value, "__iter__"):
        return "iterator"
    if isinstance(value, (_WeakSet, _Set)):
        return "set"
    if isinstance(value, _Sequence):
        return "sequence"
    if hasattr(value, "__iter__"):
        return "iterable"
    if hasattr(value, "__getitem__"):
        return "indexed"
    return "leaf"


def _materialise_iterators(value, depth=0):
    """Return a form of the value with iterators listed once.

    An iterator standing in any position, inside a
    mapping value or inside a collection among them,
    stands replaced by the list of the items it yields,
    so a later re-reading of the returned form stands
    over the same items. Mapping and collection forms
    stand rebuilt in re-iterable forms holding the
    materialised values. A ChainMap standing in any
    position stands rebuilt in the order of its maps,
    a key standing in an earlier map standing before a
    key standing in a later map and standing for the
    entry that map presents where a later map carries
    the same key. A keys view or a values view standing
    over a ChainMap stands rebuilt in the order of its
    maps in the same way, a key standing in an earlier
    map standing before a key standing in a later map.
    A deque, a UserList, and a
    dictionary view stand rebuilt in that same form,
    an items view holding its pairs as tuples, so an
    iterator inside any of them stands listed once in
    the same way. A value standing in any other
    re-iterable container form the caller presents,
    the abstract Sequence form, the abstract Set form
    with a WeakSet among the set forms, and a general
    iterable container among them, stands rebuilt in
    that same form, with every iterator in any position
    inside it standing replaced once by the list of
    its items. A value standing in a container form
    that iterates by indexed access alone stands
    rebuilt in that same form as well, whether it
    stands at the top level, inside a list, or as a
    mapping value, its elements standing read by
    indexed access in presentation order and every
    iterator inside it standing replaced once in the
    same way. Any other value stands as it stands.

    The act walks its containers with an explicit
    stack and no depth cutoff of its own, so an
    iterator stands reached at any nesting depth the
    interpreter itself can present. The depth argument
    stands accepted for the standing call form and
    stands read by no limb. A container standing
    inside itself stands as it stands at the cyclic
    position, so the reading acts downstream meet that
    form in their standing governed forms.
    """
    kind = _materialise_kind(value)
    if kind == "leaf":
        return value
    results = []
    stack = [(value, kind, False, frozenset(), 0, None)]
    while stack:
        current, current_kind, expanded, ancestors, count, keys = (
            stack.pop()
        )
        if expanded:
            if count:
                collected = results[len(results) - count:]
                del results[len(results) - count:]
            else:
                collected = []
            if current_kind == "mapping":
                results.append(dict(zip(keys, collected)))
            elif current_kind == "dictionary view" and isinstance(
                current, _ItemsView
            ):
                results.append(list(zip(keys, collected)))
            else:
                results.append(collected)
            continue
        if current_kind == "leaf" or id(current) in ancestors:
            results.append(current)
            continue
        child_ancestors = ancestors | {id(current)}
        if current_kind == "mapping" and isinstance(
            current, _collections_module.ChainMap
        ):
            keys = []
            children = []
            seen_keys = set()
            for chained in current.maps:
                for chained_key, inner in chained.items():
                    if chained_key in seen_keys:
                        continue
                    seen_keys.add(chained_key)
                    keys.append(chained_key)
                    children.append(inner)
        elif current_kind == "mapping":
            keys = list(current.keys())
            children = [inner for _key, inner in current.items()]
        elif current_kind == "dictionary view" and isinstance(
            current, _ItemsView
        ):
            keys = [key for key, _inner in current]
            children = [inner for _key, inner in current]
        elif current_kind == "dictionary view" and isinstance(
            current, (_KeysView, _ValuesView)
        ):
            underlying = getattr(current, "_mapping", None)
            if isinstance(
                underlying, _collections_module.ChainMap
            ):
                keys = None
                children = []
                seen_keys = set()
                if isinstance(current, _KeysView):
                    for chained in underlying.maps:
                        for chained_key in chained:
                            if chained_key in seen_keys:
                                continue
                            seen_keys.add(chained_key)
                            children.append(chained_key)
                else:
                    for chained in underlying.maps:
                        for chained_key, inner in chained.items():
                            if chained_key in seen_keys:
                                continue
                            seen_keys.add(chained_key)
                            children.append(inner)
            else:
                keys = None
                children = list(current)
        else:
            keys = None
            children = list(current)
        stack.append(
            (current, current_kind, True, ancestors, len(children), keys)
        )
        for child in reversed(children):
            stack.append(
                (
                    child,
                    _materialise_kind(child),
                    False,
                    child_ancestors,
                    0,
                    None,
                )
            )
    return results[0]


def _materialise_view_form(value, ancestors=frozenset()):
    """Return a form of the value with its views carried.

    The materialisation act above lists a dictionary
    view standing in the material as its elements, so
    key material standing in the keys of the viewed
    mapping stands discarded or dissolved by that
    listing before the direct act sees it. A dictionary
    view standing in any position of the material
    therefore stands carried here as a view of the same
    kind standing over a rebuilt mapping, the rebuilt
    mapping standing in the order of its maps where it
    stands as a ChainMap, so the direct act decides the
    carried form as it decides the presentation itself.
    Every other form stands materialised in the same
    way the materialisation act gives it: an iterator
    standing in any position stands listed once only,
    a mapping stands rebuilt with its keys standing as
    they stand and its values materialised, and a
    container form stands rebuilt as the list of its
    materialised elements. A container standing inside
    itself stands as it stands at the cyclic position.
    A view standing over no mapping this reading can
    rebuild stands listed in the standing form.
    """
    kind = _materialise_kind(value)
    if kind == "leaf":
        return value
    if id(value) in ancestors:
        return value
    child_ancestors = ancestors | {id(value)}
    if kind == "dictionary view":
        underlying = getattr(value, "mapping", None)
        if underlying is None:
            underlying = getattr(value, "_mapping", None)
        if not isinstance(underlying, _Mapping):
            return _materialise_iterators(value)
        rebuilt = _materialise_view_form(
            underlying, child_ancestors
        )
        if isinstance(value, _ItemsView):
            return rebuilt.items()
        if isinstance(value, _KeysView):
            return rebuilt.keys()
        return rebuilt.values()
    if kind == "mapping" and isinstance(
        value, _collections_module.ChainMap
    ):
        rebuilt = {}
        for chained in value.maps:
            for chained_key, inner in chained.items():
                if chained_key in rebuilt:
                    continue
                rebuilt[chained_key] = _materialise_view_form(
                    inner, child_ancestors
                )
        return rebuilt
    if kind == "mapping":
        return {
            key: _materialise_view_form(inner, child_ancestors)
            for key, inner in value.items()
        }
    return [
        _materialise_view_form(element, child_ancestors)
        for element in list(value)
    ]


def _is_delegating_container_subclass(value):
    """Whether a value stands in a delegating container
    subclass form at the dataset seam.

    A container form standing in a subclass of a list,
    a tuple, a set, a frozenset, a deque, a UserList,
    the abstract Sequence form, or the abstract Set
    form, whose iteration act stands defined by a class
    standing between its own class and its container
    base, its own class among them, delegating to one
    stored iterator it carries, stands in that form, in
    parity with the direct act reading that walks the
    class order to the same base. A container standing
    in its exact form, a subclass form whose iteration
    act stands inherited from its container base, a
    subclass form carrying no stored iterator, and a
    dictionary view standing in any form, stand in no
    such form here.
    """
    if isinstance(value, (_KeysView, _ItemsView, _ValuesView)):
        return False
    if type(value) in (
        list,
        tuple,
        set,
        frozenset,
        _collections_module.deque,
        _collections_module.UserList,
        _WeakSet,
    ):
        return False
    if not isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
            _Sequence,
            _Set,
        ),
    ):
        return False
    for klass in type(value).__mro__:
        if klass in (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
            _Sequence,
            _Set,
        ):
            return False
        if "__iter__" in klass.__dict__:
            return _carries_stored_iterator(value)
    return False


def _seam_rebuilt_mapping(value, rebuilt):
    """Return a rebuilt mapping in the form the seam
    materialisation carries it in.

    A mapping standing in its exact plain dict form
    stands rebuilt as the plain dict it stands as. A
    mapping standing in any other form stands carried
    in a form carrying its mapping standing, in parity
    with the direct act deciding the presentation
    itself: a mapping standing as a ChainMap stands
    carried in a ChainMap over its rebuilt maps, a
    ChainMap standing in a subclass form standing
    carried in that subclass form over its rebuilt
    maps in the same way, a
    mapping standing in a dict subclass form, an
    OrderedDict, a defaultdict, or a Counter among
    them, stands rebuilt in its own class over its
    rebuilt entries where that class stands rebuilt
    from an iterable of pairs, a mapping standing as a
    UserDict stands rebuilt in its own class over its
    rebuilt entries, and a mapping standing in any
    other form, a mapping proxy among them, stands
    carried as it stands, its standing readings
    governing it as they govern the presentation. A
    rebuild standing empty of the entries the
    presented mapping carries by its governed readings
    stands not carried as the presented mapping in
    any of those forms: the presented mapping stands
    carried as it stands in that case, so no governed
    entry stands lost to a rebuild that succeeds in
    an empty form. A rebuild standing blind to an
    entry the presented mapping carries by its
    governed readings, in the form the blind reading
    below this one states, stands not carried as the
    presented mapping in the same way, whether the
    rebuilt form carries further entries or none.
    """
    if type(value) is dict:
        result = rebuilt
    elif isinstance(value, _collections_module.ChainMap):
        maps = []
        for chained in value.maps:
            carried = {
                chained_key: rebuilt[chained_key]
                for chained_key in chained
                if chained_key in rebuilt
            }
            maps.append(carried)
        if not maps:
            maps = [{}]
        if type(value) is _collections_module.ChainMap:
            result = _collections_module.ChainMap(*maps)
        else:
            try:
                result = type(value)(*maps)
            except Exception:
                try:
                    instance = object.__new__(type(value))
                    instance.maps = maps
                    result = instance
                except Exception:
                    result = value
    elif isinstance(value, _collections_module.UserDict):
        try:
            result = type(value)(rebuilt)
        except Exception:
            result = value
    elif type(value) is _types_module.MappingProxyType:
        result = rebuilt
    elif isinstance(value, dict):
        try:
            result = type(value)(rebuilt)
        except Exception:
            result = value
    else:
        result = value
    if result is not value and (
        (
            not _seam_result_carries_entries(result)
            and _seam_presented_carries_entries(value)
        )
        or _seam_rebuild_stands_blind(value, result)
    ):
        return value
    return result


def _seam_result_carries_entries(result):
    """Whether a rebuilt mapping carries any entry at all,
    read through its items reading in the standing way."""
    try:
        return len(list(result.items())) > 0
    except Exception:
        return True


def _seam_storage_entries(mapping):
    """Return the entries a mapping carries in its
    storage, read past its presented readings.

    A dict form stands read through the storage the
    dict act itself carries, so an entry its items
    reading, its keys reading, and its iteration each
    omit or present in a substituted form stands listed
    here in the form it stands in that storage. A
    UserDict stands read through the storage of the
    mapping it wraps in the same way, and a ChainMap
    through the storage of its maps, a later map
    standing behind an earlier one in the order the
    chain presents them. A mapping carrying no storage
    in any of those forms stands in no part here.
    """
    entries = {}
    if isinstance(mapping, _collections_module.UserDict):
        data = mapping.data
        if isinstance(data, dict):
            for key, inner in dict.items(data):
                entries[key] = inner
        else:
            try:
                for key, inner in data.items():
                    entries[key] = inner
            except Exception:
                pass
        return entries
    if isinstance(mapping, _collections_module.ChainMap):
        for chained in reversed(mapping.maps):
            if isinstance(chained, dict):
                for key, inner in dict.items(chained):
                    entries[key] = inner
            else:
                try:
                    for key, inner in chained.items():
                        entries[key] = inner
                except Exception:
                    pass
        return entries
    if isinstance(mapping, dict):
        for key, inner in dict.items(mapping):
            entries[key] = inner
    return entries


def _seam_presented_carries_entries(value):
    """Whether a presented mapping carries any entry by
    its governed readings.

    A mapping stands read first through its items
    reading, and where that reading presents no entry a
    mapping stands read through the keys it carries and
    the values those keys reach, in the way the direct
    act reaches the governed entry of such a mapping,
    a ChainMap standing read through its maps and a
    UserDict through the mapping it wraps in the same
    way. A mapping stands read through the entries its
    storage carries in the same way, so a form whose
    presented readings present no entry stands read as
    carrying the entries its storage carries. A mapping
    carrying no entry in any of those readings stands
    in no entry form here.
    """
    try:
        if len(list(value.items())) > 0:
            return True
    except Exception:
        pass
    if _seam_storage_entries(value):
        return True
    if isinstance(value, _collections_module.ChainMap):
        try:
            return any(
                len(list(chained.items())) > 0
                for chained in value.maps
            )
        except Exception:
            return False
    if isinstance(value, _collections_module.UserDict):
        try:
            return len(list(value.data.items())) > 0
        except Exception:
            return False
    try:
        for key in value.keys():
            try:
                value[key]
            except Exception:
                continue
            return True
    except Exception:
        pass
    try:
        for key in value:
            try:
                value[key]
            except Exception:
                continue
            return True
    except Exception:
        pass
    return False


def _seam_governed_entry_keys(mapping):
    """List the entry keys a mapping carries by its
    governed readings.

    A mapping stands read through its items reading,
    through the keys it carries and the values those
    keys reach, and through the keys its own iteration
    yields and the values those keys reach, a ChainMap
    standing read through its maps and a UserDict
    through the mapping it wraps in the same way. A
    key stands listed once, in the order its first
    reading presents it, and a reading that presents
    no key stands in no part of the list.
    """
    keys = []

    def _add(key):
        try:
            if key not in keys:
                keys.append(key)
        except Exception:
            pass

    try:
        for key, _inner in mapping.items():
            _add(key)
    except Exception:
        pass
    if isinstance(mapping, _collections_module.ChainMap):
        try:
            for chained in mapping.maps:
                for key, _inner in chained.items():
                    _add(key)
        except Exception:
            pass
    if isinstance(mapping, _collections_module.UserDict):
        try:
            for key, _inner in mapping.data.items():
                _add(key)
        except Exception:
            pass
    try:
        for key in mapping.keys():
            try:
                mapping[key]
            except Exception:
                continue
            _add(key)
    except Exception:
        pass
    try:
        for key in mapping:
            try:
                mapping[key]
            except Exception:
                continue
            _add(key)
    except Exception:
        pass
    for key in _seam_storage_entries(mapping):
        _add(key)
    return keys


def _seam_stored_carries_view(value, ancestors=frozenset()):
    """Whether a stored form carries a dictionary view
    in substance, read on its stored entries.

    A form standing carried by the standing any view
    reading stands carried here in the same way. A
    mapping standing in no such form stands read
    through the entries its storage carries, in the
    form the seam storage reading states, so a view
    standing in the storage of a mapping whose
    presented readings present a substituted value at
    that entry stands reached here in substance, at
    any further mapping depth the storage nests it,
    and a container standing in that storage stands
    read element by element in the same way. A form
    standing inside itself stands in no part here at
    the cyclic position.
    """
    if _carries_any_view(value):
        return True
    if id(value) in ancestors:
        return False
    child_ancestors = ancestors | {id(value)}
    if isinstance(value, _Mapping):
        for stored_key, stored_inner in (
            _seam_storage_entries(value).items()
        ):
            if _seam_stored_carries_view(
                stored_key, child_ancestors
            ) or _seam_stored_carries_view(
                stored_inner, child_ancestors
            ):
                return True
        return False
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        return any(
            _seam_stored_carries_view(
                inner, child_ancestors
            )
            for inner in _container_elements_preserved(value)
        )
    return False


def _seam_view_underlying_keys(view):
    """List the entry keys of the mapping a dictionary
    view stands over, or None where that mapping stands
    in no readable form here."""
    underlying = getattr(view, "mapping", None)
    if underlying is None:
        underlying = getattr(view, "_mapping", None)
    if not isinstance(underlying, _Mapping):
        return None
    try:
        return list(underlying.keys())
    except Exception:
        return None


def _seam_material_equal(left, right, ancestors=frozenset()):
    """Whether two forms stand equal in substance.

    A form stands equal to itself. Two dictionary views
    stand equal where the view match reading below
    judges them matched. Two mappings stand equal where
    their entry keys stand equal in order and their
    values stand equal in substance entry by entry. Two
    plain containers stand equal where their elements
    stand equal in substance in order. Any other two
    forms stand equal where their own equality reading
    returns true. A form standing inside itself stands
    in no part here at the cyclic position.
    """
    if left is right:
        return True
    if isinstance(
        left, (_KeysView, _ItemsView, _ValuesView)
    ) and isinstance(
        right, (_KeysView, _ItemsView, _ValuesView)
    ):
        return _seam_view_forms_match(left, right)
    if id(left) in ancestors or id(right) in ancestors:
        return False
    child_ancestors = ancestors | {id(left), id(right)}
    if isinstance(left, _Mapping) and isinstance(
        right, _Mapping
    ):
        try:
            left_items = list(left.items())
            right_items = list(right.items())
        except Exception:
            return False
        if len(left_items) != len(right_items):
            return False
        for (left_key, left_inner), (
            right_key,
            right_inner,
        ) in zip(left_items, right_items):
            if not _seam_material_equal(
                left_key, right_key, child_ancestors
            ):
                return False
            if not _seam_material_equal(
                left_inner, right_inner, child_ancestors
            ):
                return False
        return True
    if isinstance(
        left,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ) and isinstance(
        right,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        if len(left) != len(right):
            return False
        return all(
            _seam_material_equal(
                left_inner, right_inner, child_ancestors
            )
            for left_inner, right_inner in zip(left, right)
        )
    try:
        result = left == right
    except Exception:
        return False
    return result if isinstance(result, bool) else False


def _seam_collect_views(value, from_storage, ancestors=frozenset()):
    """List the dictionary views a form carries in
    substance, in the order they stand in it.

    A form standing as a dictionary view in its own
    form stands listed as itself. A mapping stands read
    through the entries its storage carries where the
    storage form is asked for, and through the entries
    its items reading presents where it is not, so a
    view standing inside a plain container in the
    storage of a mapping, or inside a mapping standing
    in that storage, stands listed in the same way. A
    plain container stands read element by element. A
    form standing inside itself stands in no part here
    at the cyclic position.
    """
    if isinstance(value, (_KeysView, _ItemsView, _ValuesView)):
        return [value]
    if id(value) in ancestors:
        return []
    child_ancestors = ancestors | {id(value)}
    views = []
    if isinstance(value, _Mapping):
        if from_storage:
            entries = _seam_storage_entries(value)
        else:
            try:
                entries = dict(value.items())
            except Exception:
                entries = {}
        for key, inner in entries.items():
            views.extend(
                _seam_collect_views(key, from_storage, child_ancestors)
            )
            views.extend(
                _seam_collect_views(inner, from_storage, child_ancestors)
            )
        return views
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        for inner in _container_elements_preserved(value):
            views.extend(
                _seam_collect_views(inner, from_storage, child_ancestors)
            )
    return views


def _seam_view_forms_match(presented, rebuilt):
    """Whether a rebuilt dictionary view stands in the
    material form of the view it rebuilds.

    Two views standing as views in their own forms
    stand matched where they stand in the same view
    kind, where the mappings they stand over carry the
    same entry keys, key for key, in the order they
    present them, and, for an items view or a values
    view, where the values those mappings carry stand
    equal in substance entry by entry in the same
    order, a rebuilt view standing over a rebuilt
    mapping whose entries stand as they stood standing
    matched in that form. A form standing in no view
    form of its own, or a view whose underlying mapping
    stands unreadable here, stands in no mismatch here,
    its standing readings governing it as they stand.
    """
    if not isinstance(
        presented, (_KeysView, _ItemsView, _ValuesView)
    ):
        return True
    if not isinstance(
        rebuilt, (_KeysView, _ItemsView, _ValuesView)
    ):
        return True
    if type(presented) is not type(rebuilt) and not (
        isinstance(presented, _KeysView)
        == isinstance(rebuilt, _KeysView)
        and isinstance(presented, _ItemsView)
        == isinstance(rebuilt, _ItemsView)
        and isinstance(presented, _ValuesView)
        == isinstance(rebuilt, _ValuesView)
    ):
        return False
    presented_keys = _seam_view_underlying_keys(presented)
    rebuilt_keys = _seam_view_underlying_keys(rebuilt)
    if presented_keys is None or rebuilt_keys is None:
        return True
    if len(presented_keys) != len(rebuilt_keys):
        return False
    for presented_key, rebuilt_key in zip(
        presented_keys, rebuilt_keys
    ):
        if presented_key is rebuilt_key:
            continue
        try:
            if presented_key == rebuilt_key:
                continue
        except Exception:
            pass
        return False
    if isinstance(presented, (_ItemsView, _ValuesView)):
        presented_underlying = getattr(presented, "mapping", None)
        if presented_underlying is None:
            presented_underlying = getattr(
                presented, "_mapping", None
            )
        rebuilt_underlying = getattr(rebuilt, "mapping", None)
        if rebuilt_underlying is None:
            rebuilt_underlying = getattr(rebuilt, "_mapping", None)
        if isinstance(
            presented_underlying, _Mapping
        ) and isinstance(rebuilt_underlying, _Mapping):
            try:
                presented_values = list(
                    presented_underlying.values()
                )
                rebuilt_values = list(rebuilt_underlying.values())
            except Exception:
                return True
            if len(presented_values) != len(rebuilt_values):
                return False
            for presented_value, rebuilt_value in zip(
                presented_values, rebuilt_values
            ):
                if not _seam_material_equal(
                    presented_value, rebuilt_value
                ):
                    return False
    return True


def _seam_rebuild_stands_blind(value, result):
    """Whether a rebuilt mapping stands blind to an
    entry the presented mapping carries.

    A rebuild stands blind where an entry key the
    presented mapping carries by its governed
    readings stands in no entry key the rebuilt form
    carries by the same readings, whether the rebuilt
    form carries further entries or none, so a rebuild
    standing in that blind form stands not carried as
    the presented mapping in the guard above. A
    rebuild stands blind in the same way where it
    substitutes a clean value at a governed entry: an
    entry whose value in the storage the presented
    mapping carries carries a dictionary view in
    substance, whose rebuilt value carries no view in
    substance, stands lost to the rebuild in
    substance, so a rebuild standing in that
    substituted form stands not carried as the
    presented mapping in the same way. A rebuild
    stands blind in the same way where it substitutes
    a dictionary view over other material at a
    governed entry: an entry whose value in the
    storage the presented mapping carries carries a
    dictionary view in substance, read on its stored
    entries in the form the stored view reading above
    states, whose rebuilt value carries a dictionary
    view standing over entry keys other than the keys
    the presented view stands over, stands lost to
    the rebuild in substance in the same way. A
    rebuild stands blind in the same way where the
    view its storage carries stands in a wrapped or
    nested form, inside a plain container in that
    storage or inside a mapping standing in that
    storage, and the rebuilt value carries no view
    standing matched with it in the form the view
    match reading states, the views of each side
    standing collected in substance in the form the
    collected views reading above states. A presented
    mapping carrying no entry key in any of those
    readings stands in no blind form here.
    """
    presented_keys = _seam_governed_entry_keys(value)
    if not presented_keys:
        return False
    result_keys = _seam_governed_entry_keys(result)
    if any(
        key not in result_keys for key in presented_keys
    ):
        return True
    presented_storage = _seam_storage_entries(value)
    if not presented_storage:
        return False
    result_storage = (
        _seam_storage_entries(result)
        if isinstance(result, _Mapping)
        else {}
    )
    for key, inner in presented_storage.items():
        rebuilt_inner = result_storage.get(key)
        if rebuilt_inner is inner:
            continue
        if not _seam_stored_carries_view(inner):
            continue
        if rebuilt_inner is None or not _carries_any_view(
            rebuilt_inner
        ):
            return True
        stored_views = _seam_collect_views(inner, True)
        if stored_views:
            rebuilt_views = _seam_collect_views(
                rebuilt_inner, False
            )
            if any(
                not any(
                    _seam_view_forms_match(
                        stored_view, rebuilt_view
                    )
                    for rebuilt_view in rebuilt_views
                )
                for stored_view in stored_views
            ):
                return True
            continue
        if not _seam_view_forms_match(inner, rebuilt_inner):
            return True
    return False


def _materialise_view_form_seam(value, ancestors=frozenset()):
    """Return a form of the value with its views carried,
    for the dataset instruction item surface.

    This reading stands as the reading above in every
    form but two: a container standing in a delegating
    container subclass form stands as it stands, in
    parity with the direct act deciding that same
    presentation, so no view standing inside such a
    container stands carried by a rebuilding that
    strips the subclass form it stands in, and a
    mapping standing in a non plain form stands
    rebuilt in a form carrying its mapping standing,
    in the form the rebuilt mapping reading above
    this one states, so no mapping stands dissolved
    into the plain form before the direct act sees it. Every other
    form stands materialised as the reading above
    gives it, a dictionary view standing carried as a
    view of the same kind standing over a rebuilt
    mapping, an iterator standing listed once only,
    a mapping standing rebuilt with its keys standing
    as they stand, and a container form standing
    rebuilt as the list of its materialised elements.
    A container standing inside itself stands as it
    stands at the cyclic position.
    """
    kind = _materialise_kind(value)
    if kind == "leaf":
        return value
    if id(value) in ancestors:
        return value
    if _is_delegating_container_subclass(value):
        return value
    child_ancestors = ancestors | {id(value)}
    if kind == "dictionary view":
        underlying = getattr(value, "mapping", None)
        if underlying is None:
            underlying = getattr(value, "_mapping", None)
        if not isinstance(underlying, _Mapping):
            return _materialise_iterators(value)
        rebuilt = _materialise_view_form_seam(
            underlying, child_ancestors
        )
        if isinstance(value, _ItemsView):
            return rebuilt.items()
        if isinstance(value, _KeysView):
            return rebuilt.keys()
        return rebuilt.values()
    if kind == "mapping" and isinstance(
        value, _collections_module.ChainMap
    ):
        rebuilt = {}
        for chained in value.maps:
            for chained_key, inner in chained.items():
                if chained_key in rebuilt:
                    continue
                rebuilt[chained_key] = _materialise_view_form_seam(
                    inner, child_ancestors
                )
        return _seam_rebuilt_mapping(value, rebuilt)
    if kind == "mapping":
        rebuilt = {
            key: _materialise_view_form_seam(inner, child_ancestors)
            for key, inner in value.items()
        }
        return _seam_rebuilt_mapping(value, rebuilt)
    return [
        _materialise_view_form_seam(element, child_ancestors)
        for element in list(value)
    ]


def _resolve_text(value):
    """Read the text a value carries, in its stated forms.

    A string stands as its own text, and a UserString
    stands read as the text it wraps, in the same form
    as a plain string, ahead of the general iterable
    limb below. A mapping stands
    read for the text under its instruction_text, text,
    or content key, in that order, and that value may
    itself stand in any of these forms. A list, tuple,
    set, or frozenset stands read for the texts of its
    elements, joined in presentation order where the
    form carries one and in element order otherwise.
    A byte string or bytearray stands read for the text
    it carries, decoded as UTF-8. A memoryview stands
    read as the byte content it views, and a byte array
    in the array form stands read as the bytes it holds,
    in that same decoded form. An iterator value, a
    generator among them, stands read for the texts of
    the items it yields, and any other iterable value
    stands read for the texts of its elements in the
    same joined form. A value standing in a container
    form that iterates by indexed access alone, carrying
    no iteration act of its own, stands read for the
    texts of the elements its indexed access yields, in
    the same joined form, where its elements stand
    readable by that access. Any other value stands as
    it stands.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, _UserString):
        return str(value)
    byte_content = _byte_content(value)
    if byte_content is not None:
        return byte_content.decode("utf-8", "replace")
    if isinstance(value, _Mapping):
        for key in ("instruction_text", "text", "content"):
            inner = value.get(key)
            if inner is not None:
                return _resolve_text(inner)
        return None
    if isinstance(value, (list, tuple, set, frozenset)):
        parts = []
        for element in value:
            resolved = _resolve_text(element)
            if resolved:
                parts.append(str(resolved))
        if parts:
            return " ".join(parts)
        return None
    if hasattr(value, "__iter__"):
        parts = []
        for element in value:
            resolved = _resolve_text(element)
            if resolved:
                parts.append(str(resolved))
        if parts:
            return " ".join(parts)
        return None
    if hasattr(value, "__getitem__"):
        try:
            children = list(value)
        except Exception:
            return value
        parts = []
        for element in children:
            resolved = _resolve_text(element)
            if resolved:
                parts.append(str(resolved))
        if parts:
            return " ".join(parts)
        return None
    return value


def _item_fields(item):
    if isinstance(item, str):
        return {"group": None, "signature": None, "text": item}
    if isinstance(item, _UserString):
        return {"group": None, "signature": None, "text": str(item)}
    byte_content = _byte_content(item)
    if byte_content is not None:
        return {
            "group": None,
            "signature": None,
            "text": byte_content.decode("utf-8", "replace"),
        }
    if isinstance(item, _Mapping):
        text = item.get("text")
        if text is None:
            text = item.get("instruction_text")
        if text is None:
            text = item.get("content")
        return {
            "group": item.get("group"),
            "signature": item.get("signature"),
            "text": _resolve_text(text),
        }
    resolved = _resolve_text(item)
    if isinstance(resolved, str):
        return {"group": None, "signature": None, "text": resolved}
    return {"group": None, "signature": None, "text": None}


def _unwrapped_items(element):
    """Yield the items a bundle position element carries.

    An element standing in a container form, a list, a
    tuple, a set, a frozenset, a deque, or a UserList,
    stands unwrapped for the items it carries, in that
    same form at any wrap depth. An element standing in
    an iterator form, a generator, a zip object, a map
    object, or a filter object among them, stands
    unwrapped in the same form, its items standing
    listed once in that reading so no presented item
    stands consumed by an earlier read, and an element
    standing in the enumerate form stands read for the
    item standing in second place in each pair it
    yields. An element standing in an abstract Sequence
    form, in an abstract Set form, or in a general
    iterable container form stands unwrapped in the
    same form, and an element standing in a container
    form that iterates by indexed access alone stands
    unwrapped in the same form where its elements stand
    readable by that access. A text form, a byte form,
    a mapping, and any other element standing in no
    container form stands yielded as it stands, a
    mapping standing as the item it stands as and never
    as the keys it carries.
    """
    if isinstance(element, enumerate):
        for pair in list(element):
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                yield from _unwrapped_items(pair[1])
            else:
                yield from _unwrapped_items(pair)
        return
    if isinstance(
        element,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
        ),
    ):
        yield element
        return
    if isinstance(
        element,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        for inner in element:
            yield from _unwrapped_items(inner)
        return
    if hasattr(element, "__next__") and hasattr(element, "__iter__"):
        for inner in list(element):
            yield from _unwrapped_items(inner)
        return
    if isinstance(element, (_Sequence, _Set, _WeakSet)):
        for inner in list(element):
            yield from _unwrapped_items(inner)
        return
    if hasattr(element, "__iter__"):
        for inner in list(element):
            yield from _unwrapped_items(inner)
        return
    if hasattr(element, "__getitem__"):
        try:
            children = list(element)
        except Exception:
            yield element
            return
        for inner in children:
            yield from _unwrapped_items(inner)
        return
    yield element


def _is_partitionable_form(value):
    """Whether a bundle position value stands in a read form.

    A list, a tuple, a deque, a UserList, an abstract
    Sequence, a general iterable container, an iterator,
    a set form, a frozenset form, a dictionary view, and
    a value standing in a container form that iterates
    by indexed access alone each stand read for the
    items they carry, in parity with the unwrapping and
    materialisation readings of this module. A text
    form, a byte form, an array, a range, and a mapping
    stand in no read form here, in their standing forms:
    a single mapping standing at a position and a bare
    string standing at a position keep the standing
    presentation refusal at the bundle surfaces.
    """
    if isinstance(
        value,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
        ),
    ):
        return False
    if isinstance(
        value, (list, tuple, _collections_module.deque,
                _collections_module.UserList)
    ):
        return True
    if isinstance(
        value, (set, frozenset, _WeakSet, _Set)
    ):
        return True
    if isinstance(value, (_ItemsView, _KeysView, _ValuesView)):
        return True
    if isinstance(value, _Sequence):
        return True
    if hasattr(value, "__next__") and hasattr(value, "__iter__"):
        return True
    if hasattr(value, "__iter__"):
        return True
    if hasattr(value, "__getitem__"):
        return True
    return False


def _is_single_pass_iterable(value):
    """Whether a value stands listed once only.

    A general iterable container carrying an iteration
    act of its own, carrying no next method, and standing
    in no re-iterable container form stands listed once
    only: its first listing yields its elements and its
    later listings yield none. A detection reading of
    such a form stands spent once and carried, in the
    listed form the first listing builds.
    """
    if hasattr(value, "__next__"):
        return False
    if not hasattr(value, "__iter__"):
        return False
    if isinstance(
        value,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
            _ItemsView,
            _KeysView,
            _ValuesView,
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
            _Sequence,
            _Set,
        ),
    ):
        return False
    return True


def _contains_single_use(value):
    """Whether a value carries a single use form inside it.

    A value standing as an iterator or as a general
    iterable standing listed once only carries such a
    form, and a list or a tuple carries one where any
    element it carries carries one in the same way.
    Any other value carries none here.
    """
    if _is_single_pass_iterable(value):
        return True
    if hasattr(value, "__next__"):
        return True
    if isinstance(value, (list, tuple)):
        return any(
            _contains_single_use(element) for element in value
        )
    return False


def _position_elements(value):
    """List a bundle position value once, or return None.

    A value standing in a partitionable form stands
    listed once in this reading, so an iterator in a
    bundle position stands consumed by no earlier read
    and its items stand held in the list this act
    builds. A value standing in no such form returns
    None, and its material stands unpartitioned.
    """
    if not _is_partitionable_form(value):
        return None
    return list(value)


def _is_index_pair_form(element):
    """Whether an element stands as an enumerate index pair.

    An element standing as a two element list, tuple,
    deque, or UserList with an integer standing in first
    place stands as an index pair of the form an
    enumerate object yields. An element standing as a
    two element abstract Sequence, as a two element
    general iterable container, or as a set or frozenset
    holding an integer beside the pair it carries stands
    as an index pair in the same way, in parity with the
    pair reading, which reads each of those forms as a
    pair in its own right. A dictionary view, a text
    form, a byte form, a mapping, and an iterator each
    stand in no index pair form here.
    """
    if isinstance(
        element,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
            _ItemsView,
            _KeysView,
            _ValuesView,
        ),
    ):
        return False
    if _is_single_pass_iterable(element):
        return False
    if isinstance(element, (set, frozenset)):
        if len(element) != 2:
            return False
        return any(
            isinstance(entry, int) for entry in element
        ) and any(
            not isinstance(entry, int) for entry in element
        )
    if isinstance(
        element,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        return len(element) == 2 and isinstance(element[0], int)
    if isinstance(element, _Sequence):
        try:
            return len(element) == 2 and isinstance(
                element[0], int
            )
        except Exception:
            return False
    if hasattr(element, "__next__"):
        return False
    if hasattr(element, "__iter__") or hasattr(
        element, "__getitem__"
    ):
        try:
            listed = list(element)
        except Exception:
            return False
        return len(listed) == 2 and isinstance(listed[0], int)
    return False


def _index_pair_second(element):
    """Return the item standing in second place of an index pair.

    A set or frozenset index pair carries no order, so
    the item it carries stands as its one element that
    stands in no integer form. Any other index pair
    stands read for the element its second place holds,
    by indexed access where that access stands and by
    its listed form where it does not.
    """
    if isinstance(element, (set, frozenset)):
        for entry in element:
            if not isinstance(entry, int):
                return entry
        return None
    if _is_single_pass_iterable(element):
        return list(element)[1]
    try:
        return element[1]
    except Exception:
        return list(element)[1]


def _enumerate_carried(element):
    """Return the item an enumerate index pair carries.

    An element standing as a two element list or tuple
    with an integer standing in first place stands as an
    index pair an enumerate object yields, and the item
    it carries stands in second place. Index pairs
    standing nested, as a further enumerate layer yields
    them, stand stripped in the same way until no index
    pair stands. An index pair standing in a deque form
    or a UserList form stands stripped in the same way,
    and an index pair standing in an abstract Sequence
    form, in a general iterable container form, or in a
    set or frozenset form stands stripped in the same
    way, the set forms carrying no order between the
    integer and the pair they carry, and an index pair
    standing in an iterator form, a
    generator, a map object, or a list iterator among
    them, each yielding the one index pair, stands
    stripped in the same way, the iterator standing
    listed once in that reading. A one element list or
    tuple holding one index pair, the form a listed
    iterator index pair takes, stands stripped in the
    same way. Any other element stands as it stands,
    an iterator element standing listed once where it
    stands consumed by this reading.
    """
    while True:
        if _is_single_pass_iterable(element):
            element = list(element)
            continue
        if _is_index_pair_form(element):
            element = _index_pair_second(element)
            continue
        if (
            isinstance(element, (list, tuple))
            and len(element) == 1
            and _is_single_pass_iterable(element[0])
        ):
            element = list(element[0])
            continue
        if (
            isinstance(element, (list, tuple))
            and len(element) == 1
            and _is_index_pair_form(element[0])
        ):
            element = _index_pair_second(element[0])
            continue
        if (
            isinstance(element, (list, tuple))
            and len(element) == 1
            and isinstance(element[0], (list, tuple))
        ):
            element = element[0]
            continue
        if hasattr(element, "__next__") and hasattr(
            element, "__iter__"
        ):
            listed = list(element)
            if len(listed) == 1 and _is_single_pass_iterable(
                listed[0]
            ):
                element = list(listed[0])
                continue
            if len(listed) == 1 and _is_index_pair_form(
                listed[0]
            ):
                element = _index_pair_second(listed[0])
                continue
            if len(listed) == 1 and isinstance(
                listed[0], (list, tuple)
            ):
                element = listed[0]
                continue
            if _is_index_pair_form(listed):
                element = listed[1]
                continue
            return listed
        return element


def _pairs_position_elements(value):
    """List a pairs position value once, or return None.

    A pairs position standing as an enumerate object
    stands read for the pair standing in second place in
    each pair it yields, in parity with the enumerate
    reading the unwrapping act gives inside the bundle
    positions. A pairs position standing as a zip object
    stands read for the pair each one element tuple it
    yields carries, beside the parallel iterables form a
    zip object also presents, whose tuples stand as the
    pairs themselves. A pairs position standing as a
    dictionary items view stands read for the pair each
    entry it yields carries in second place, in parity
    with the enumerate reading of the same shape, with
    enumerate index pairs stripped from the pair each
    entry carries and a carried value standing itself as
    an items view, or as a one element list holding one,
    standing read for the pairs that view carries.
    Material standing as an entry key of such a view, as
    a mapping, as a wrapped key, or as a container formed
    key, stands read beside the entry values in the same
    way, as a pair whose holdout side that material
    carries. Listed
    elements still standing as enumerate index pairs, as
    a further enumerate layer standing inside the
    position yields them, stand stripped to the pair
    each one carries. Any other partitionable form
    stands listed in the standing position reading, and
    a value standing in no such form returns None.
    """
    if isinstance(value, _ValuesView):
        key_sides = _values_view_key_sides(value)
        if key_sides is not None:
            return [[key_sides[0], key_sides[1]]]
    if isinstance(value, enumerate):
        listed = [
            _enumerate_carried(element) for element in list(value)
        ]
        return listed
    if isinstance(value, zip):
        listed = []
        for element in list(value):
            if isinstance(element, tuple) and len(element) == 1:
                listed.append(_enumerate_carried(element[0]))
            else:
                listed.append(_enumerate_carried(element))
        return listed
    if isinstance(value, _ItemsView):
        pairs = []
        entries = _chain_map_items_entries(value)
        if entries is None:
            entries = list(value)
        for _key, inner in entries:
            carried = _enumerate_carried(inner)
            if isinstance(carried, _ItemsView):
                pairs.extend(_pairs_position_elements(carried))
            elif (
                isinstance(carried, (list, tuple))
                and len(carried) == 1
                and isinstance(carried[0], _ItemsView)
            ):
                pairs.extend(_pairs_position_elements(carried[0]))
            else:
                pairs.append(carried)
            if isinstance(_key, _Mapping):
                key_material = _mapping_position_material([_key])
            else:
                wrapped = _wrapped_key_holdout(_key)
                if wrapped:
                    key_material = _mapping_position_material(
                        wrapped
                    )
                else:
                    key_material = []
            for key_item in key_material:
                for unwrapped in _unwrapped_items(key_item):
                    pairs.append([{}, unwrapped])
        return pairs
    listed = _position_elements(value)
    if listed is None:
        return None
    return [_enumerate_carried(element) for element in listed]


def _pair_elements(pair):
    """Return the two sides a pair presents, or None.

    A pair stands in its two element form, as a list, a
    tuple, a deque, a UserList, an abstract Sequence, a
    general iterable container, a set of its two items,
    or an iterator listed once, or in its mapping form,
    holding its candidate and holdout entries by name.
    A pair standing as a zip object stands listed once
    to the one tuple it yields, and that listed form of
    one element standing as a two element tuple stands
    read as that tuple, in parity with the neighbouring
    iterator pair forms. A pair standing as an enumerate
    object stands read for the items its index pairs
    carry: two carried items stand as the two sides, and
    one carried item stands read as a pair in its own
    right, so a malformed pair presented through an
    enumerate object returns no sides here, in parity
    with the same pair in list form. A pair standing as
    a dictionary view or in a container form that iterates by indexed
    access alone stands in no pair form here and returns
    None, in its standing form, so no such pair stands
    selected for a comparison by this reading. Any other
    form returns None, in its standing form.
    """
    if isinstance(pair, (_ItemsView, _KeysView, _ValuesView)):
        return None
    if hasattr(pair, "__getitem__") and not hasattr(
        pair, "__iter__"
    ):
        return None
    if isinstance(pair, enumerate):
        carried = [
            _enumerate_carried(element) for element in list(pair)
        ]
        if len(carried) == 2:
            return carried[0], carried[1]
        if len(carried) == 1:
            return _pair_elements(carried[0])
        return None
    if isinstance(pair, _Mapping):
        cand = pair.get("candidate")
        if cand is None:
            cand = pair.get("candidate_item")
        hold = pair.get("holdout")
        if hold is None:
            hold = pair.get("holdout_item")
        if cand is not None and hold is not None:
            return cand, hold
        return None
    elements = _position_elements(pair)
    if elements is not None and len(elements) == 2:
        return elements[0], elements[1]
    if elements is not None and len(elements) == 1:
        inner = elements[0]
        if isinstance(inner, (list, tuple)) and len(inner) == 2:
            return inner[0], inner[1]
    return None


def _is_bare_bundle_form(material):
    """Whether a bare bundle stands in a read form.

    A list, a tuple, a deque, and a general iterable
    container each stand read as a bare bundle for the
    items they carry. An iterator standing alone, a
    text form, a byte form, a mapping, and a set form
    stand in no bare bundle form here, in their
    standing forms.
    """
    if isinstance(material, (list, tuple)):
        return True
    if isinstance(material, _collections_module.deque):
        return True
    if isinstance(
        material,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
            set,
            frozenset,
            _WeakSet,
            _Set,
            _ItemsView,
            _KeysView,
            _ValuesView,
        ),
    ):
        return False
    if hasattr(material, "__next__"):
        return False
    if hasattr(material, "__iter__"):
        return True
    return False


def _split_items(material):
    """Partition bundle material into candidate and holdout items.

    An item standing in a container form inside the
    bundle positions stands read for the item it
    carries, split side included, in the form the
    unwrapping act gives. A position value standing in
    a deque form, a UserList form, an abstract Sequence
    form, or a general iterable container form, with
    iterators listed once in that reading, stands read
    for the items it carries in the same form, and a
    bare bundle standing as a deque or as a general
    iterable container stands read in the same form.
    Each side of a pair, in both pair forms, stands
    read through the same unwrapping act the other
    bundle positions use, split side as the pair states
    it, so a wrapped side reaches the comparison index
    as the item it carries. A position value standing
    in a set form, a frozenset form, a dictionary view
    form, or a container form that iterates by indexed
    access alone stands read for the items it carries
    in the same form, a pair standing as a set of its
    two items stands read as a pair in the same form,
    and a pairs position standing as an enumerate
    object or as a zip object stands read through the
    pairs position reading for the pairs it carries.
    """
    candidate = []
    holdout = []
    if isinstance(material, _Mapping):
        for key in ("candidate_items", "candidate"):
            elements = _position_elements(material.get(key))
            if elements is not None:
                for element in elements:
                    candidate.extend(_unwrapped_items(element))
        for key in ("holdout_items", "holdout"):
            elements = _position_elements(material.get(key))
            if elements is not None:
                for element in elements:
                    holdout.extend(_unwrapped_items(element))
            side_value = material.get(key)
            if isinstance(side_value, _ValuesView):
                for element in _mapping_position_material(
                    _values_view_key_holdout(side_value)
                ):
                    holdout.extend(_unwrapped_items(element))
        items = _position_elements(material.get("items"))
        if items is not None:
            for element in items:
                for item in _unwrapped_items(element):
                    side = None
                    if isinstance(item, _Mapping):
                        side = item.get("split") or item.get("side")
                    if side in ("holdout", "sealed holdout"):
                        holdout.append(item)
                    else:
                        candidate.append(item)
        pairs = _pairs_position_elements(material.get("pairs"))
        if pairs is not None:
            for pair in pairs:
                sides = _pair_elements(pair)
                if sides is not None:
                    candidate.extend(_unwrapped_items(sides[0]))
                    holdout.extend(_unwrapped_items(sides[1]))
    elif _is_bare_bundle_form(material):
        for element in list(material):
            for item in _unwrapped_items(element):
                side = None
                if isinstance(item, _Mapping):
                    side = item.get("split") or item.get("side")
                if side in ("holdout", "sealed holdout"):
                    holdout.append(item)
                else:
                    candidate.append(item)
    return candidate, holdout


def _is_bundle(material):
    if _is_bare_bundle_form(material):
        return True
    if isinstance(material, _Mapping):
        return any(
            key in material
            for key in (
                "candidate_items",
                "holdout_items",
                "candidate",
                "holdout",
                "items",
                "pairs",
            )
        )
    return False


class _UnhashableIndexValue(Exception):
    """A group or signature value stands in no hashable form."""


def _index_key(relation, value):
    try:
        hash(value)
    except (TypeError, ValueError):
        raise _UnhashableIndexValue(
            "unhashable index value for relation %r" % (relation,)
        )
    return (relation, value)


def _keyed_index(items):
    index = {}
    for position, item in enumerate(items):
        fields = _item_fields(item)
        for relation in ("group", "signature"):
            value = fields[relation]
            if value is not None:
                index.setdefault(
                    _index_key(relation, value), []
                ).append(position)
    return index


def _selected_pairs(candidate, holdout):
    """Select pairs over the group and signature keyed index.

    Returns a list of candidate and holdout positions.
    A pair sharing neither a group nor a signature
    stands in no index bucket together and is never
    selected, so it is never compared.
    """
    index = _keyed_index(holdout)
    selected = []
    seen = set()
    for cand_pos, item in enumerate(candidate):
        fields = _item_fields(item)
        for relation in ("group", "signature"):
            value = fields[relation]
            if value is None:
                continue
            for hold_pos in index.get(_index_key(relation, value), []):
                pair = (cand_pos, hold_pos)
                if pair not in seen:
                    seen.add(pair)
                    selected.append(pair)
    return selected


def _text_overlap(text_a, text_b):
    if not text_a or not text_b:
        return 0.0
    words_a = set(str(text_a).split())
    words_b = set(str(text_b).split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / min(len(words_a), len(words_b))


def _pair_relations(cand_item, hold_item):
    cand = _item_fields(cand_item)
    hold = _item_fields(hold_item)
    fired = []
    if cand["group"] is not None and cand["group"] == hold["group"]:
        fired.append("group")
    if (
        cand["signature"] is not None
        and cand["signature"] == hold["signature"]
    ):
        fired.append("signature")
    if _text_overlap(cand["text"], hold["text"]) >= _NEAR_VERBATIM_OVERLAP:
        fired.append("near verbatim cluster")
    return fired


def _audit_bundle(material):
    candidate, holdout = _split_items(material)
    selected = _selected_pairs(candidate, holdout)
    firing = []
    for cand_pos, hold_pos in selected:
        fired = _pair_relations(candidate[cand_pos], holdout[hold_pos])
        if fired:
            firing.append(
                {
                    "candidate_position": cand_pos,
                    "holdout_position": hold_pos,
                    "relations": fired,
                }
            )
    return {
        "comparisons": len(selected),
        "cost_units": len(selected) * _COST_WEIGHT_PER_PAIR,
        "firing_pairs": firing,
        "flagged": bool(firing),
        "typed_reason": _TYPED_REASON,
    }


def indexed_comparisons(material):
    """Return the indexed comparison count and its cost.

    The count stands over the group and signature
    keyed index only. Pairs sharing neither relation
    are not compared and are not counted. The cost
    stands at the Example E weight per pair compared.
    A text form its reading recurses past the
    interpreter limit, and a group or signature value
    standing in no hashable form, each meet the stated
    no count form of this surface, with no exception
    escaping. The count stands over the pairs material
    in its materialised form, in parity with the bundle
    surfaces, so a pair standing inside two plain
    iterators at the pairs position, its single pass
    forms listed once only and carried within the act,
    stands counted in the same form the bundle surfaces
    count it.
    """
    if _is_bundle(material):
        try:
            bundle = _audit_bundle(
                _materialised_pairs_material(material)
            )
        except (RecursionError, _UnhashableIndexValue):
            bundle = {"comparisons": 0}
        comparisons = bundle["comparisons"]
    else:
        comparisons = 0
    return {
        "comparisons": comparisons,
        "cost_units": comparisons * _COST_WEIGHT_PER_PAIR,
        "cost_weight_per_pair": _COST_WEIGHT_PER_PAIR,
        "cost_weight_source_class": "guessed",
        "revisit_volume_runs": _REVISIT_VOLUME_RUNS,
        "index_keys": ["group", "signature"],
        "all_pairs_compared": False,
    }


_SIDE_KEYS = ("candidate_items", "candidate", "holdout_items", "holdout")
_POSITION_KEYS = _SIDE_KEYS + ("items", "pairs")


def _ungoverned_side(material):
    """Whether a bundle position stands in no partitioned form.

    A candidate or holdout side standing in a
    partitionable form stands read for its items by the
    partitioning act: a list, a tuple, a deque, a
    UserList, an abstract Sequence, a general iterable
    container, an iterator listed once by that act, a
    set form, a dictionary view, or a container form
    that iterates by indexed access alone, and the
    items and pairs positions stand read by that act
    in the same forms. A position present in any other
    form, a single mapping or a bare string among them,
    stands read by no limb of that act, so its material
    never reaches a comparison. This reading tests
    forms alone and lists no iterator: a pairs position
    standing as an iterator, and a pair standing as an
    iterator inside it, stand governed on their forms
    and stand listed once by the audit act reading
    below, which materialises the pairs position of a
    bundle once for the whole audit, so a malformed
    pair standing in a generator form stands decided
    by this reading in the same form as the same pair
    in list form. A pairs position standing as a
    dictionary items view stands tested beside its
    entry forms by the pairs the pairs position reading
    extracts from it, so a malformed pair standing
    inside such a position stands decided by this
    reading as the same pair in list form decides.
    """
    if not isinstance(material, _Mapping):
        return False
    for key in _POSITION_KEYS:
        if key in material:
            value = material[key]
            if value is not None and not _is_partitionable_form(
                value
            ):
                return True
    pairs = material.get("pairs")
    if _is_partitionable_form(pairs) and not hasattr(
        pairs, "__next__"
    ):
        for pair in list(pairs):
            if hasattr(pair, "__next__"):
                continue
            if _pair_elements(_enumerate_carried(pair)) is not None:
                continue
            return True
    if isinstance(pairs, _ItemsView):
        for pair in _pairs_position_elements(pairs):
            if hasattr(pair, "__next__"):
                continue
            if _pair_elements(pair) is not None:
                continue
            return True
    return False


def _materialised_pairs_material(material):
    """Return the bundle with its pairs position listed once.

    A pairs position standing as an iterator, and a
    pair standing as an iterator inside a pairs
    position, each stand listed once in this reading
    and held in the list form this act builds, in a
    shallow copy of the bundle, so the governed refusal
    reading and the partitioning act that follow stand
    over the same pairs and no presented pair stands
    consumed by an earlier read. A pair standing as an
    enumerate object stands listed in that same form as
    the items its index pairs carry, so the pair stands
    judged in the form it presents. A pairs position
    standing as a dictionary items view stands listed in
    that same form as the pairs the pairs position
    reading extracts from it. A pair standing as a zip
    object inside a list or a tuple element of the pairs
    position stands listed once in the same way, the one
    tuple it yields standing carried through the
    enumerate carried reading, so a single pass iterable
    standing inside that tuple stands listed once only
    and carried within the act. A pair standing as a plain
    iterator whose one carried element stands as a list or
    a tuple holding a single pass iterable stands listed
    once in the same way, the carried element standing
    read through the enumerate carried reading, so the
    single pass iterable stands listed once only and its
    listed form stands carried within the act. A bundle
    carrying no
    iterator at its pairs position stands as it stands.
    """
    if not isinstance(material, _Mapping):
        return material
    if "pairs" not in material:
        return material
    pairs = material.get("pairs")
    if pairs is None:
        return material
    listed = None
    if isinstance(pairs, _ItemsView):
        listed = _pairs_position_elements(pairs)
    elif hasattr(pairs, "__next__"):
        listed = _pairs_position_elements(pairs)
    elif _is_single_pass_iterable(pairs):
        listed = _pairs_position_elements(pairs)
    elif _is_partitionable_form(pairs):
        candidates = list(pairs)
        if any(
            hasattr(pair, "__next__")
            or _is_single_pass_iterable(pair)
            or _contains_single_use(pair)
            for pair in candidates
        ):
            listed = candidates
    if listed is None:
        return material
    new_pairs = []
    for pair in listed:
        if isinstance(pair, zip):
            listed_once = list(pair)
            if len(listed_once) == 1:
                new_pairs.append(
                    _enumerate_carried(listed_once[0])
                )
            else:
                new_pairs.append(listed_once)
        elif isinstance(pair, enumerate):
            new_pairs.append(
                [
                    _enumerate_carried(element)
                    for element in list(pair)
                ]
            )
        elif hasattr(pair, "__next__"):
            listed_once = list(pair)
            if len(listed_once) == 1 and _is_single_pass_iterable(
                listed_once[0]
            ):
                new_pairs.append(
                    _enumerate_carried(listed_once[0])
                )
            elif len(listed_once) == 1 and _is_index_pair_form(
                listed_once[0]
            ):
                new_pairs.append(
                    _enumerate_carried(listed_once[0])
                )
            elif len(listed_once) == 1 and _contains_single_use(
                listed_once[0]
            ):
                new_pairs.append(
                    _enumerate_carried(listed_once[0])
                )
            elif _is_index_pair_form(listed_once):
                new_pairs.append(listed_once[1])
            else:
                new_pairs.append(listed_once)
        elif _is_single_pass_iterable(pair):
            new_pairs.append(_enumerate_carried(pair))
        elif _contains_single_use(pair):
            new_pairs.append(_enumerate_carried(pair))
        else:
            new_pairs.append(pair)
    copied = dict(material)
    copied["pairs"] = new_pairs
    return copied


def _audit(material, scored_before_refusal):
    material = _materialised_pairs_material(material)
    if _ungoverned_side(material):
        return True, {
            "comparisons": 0,
            "cost_units": 0,
            "firing_pairs": [],
            "typed_reason": _PRESENTATION_REASON,
        }
    if _is_bundle(material):
        try:
            bundle = _audit_bundle(material)
        except (RecursionError, _UnhashableIndexValue):
            return True, {
                "comparisons": 0,
                "cost_units": 0,
                "firing_pairs": [],
                "typed_reason": _PRESENTATION_REASON,
            }
        return bundle["flagged"], bundle
    if material is None:
        return False, {"comparisons": 0, "cost_units": 0, "firing_pairs": []}
    if isinstance(material, str) and not material.strip():
        return False, {"comparisons": 0, "cost_units": 0, "firing_pairs": []}
    if isinstance(material, (list, tuple)) and not material:
        return False, {"comparisons": 0, "cost_units": 0, "firing_pairs": []}
    return True, {
        "comparisons": 0,
        "cost_units": 0,
        "firing_pairs": [],
        "typed_reason": _PRESENTATION_REASON,
    }


def _charged(scored_before_refusal):
    return 1 if scored_before_refusal else 0


def _refusal(record_home, scored_before_refusal, bundle):
    return {
        "error": _ERROR_NAME,
        "wording_variants": [],
        "candidate_bundle_refused": True,
        "promotion_proceeded": False,
        "evaluation_state": "not scored",
        "typed_reason": bundle.get("typed_reason", _TYPED_REASON),
        "record_home": record_home,
        "completed_evaluations_charged": _charged(scored_before_refusal),
        "relations": list(RELATIONS),
        "comparisons": bundle["comparisons"],
        "comparison_cost_units": bundle["cost_units"],
        "firing_pairs": bundle["firing_pairs"],
    }


def _clearance(record_home, scored_before_refusal, bundle):
    return {
        "error": None,
        "wording_variants": [],
        "candidate_bundle_refused": False,
        "promotion_proceeded": True,
        "evaluation_state": "scored",
        "typed_reason": None,
        "record_home": record_home,
        "completed_evaluations_charged": _charged(scored_before_refusal),
        "relations": list(RELATIONS),
        "comparisons": bundle["comparisons"],
        "comparison_cost_units": bundle["cost_units"],
        "firing_pairs": bundle["firing_pairs"],
    }


def _instruction_text_of(instruction_text):
    return _resolve_text(instruction_text)


_ITEM_FIELD_KEYS = ("text", "instruction_text", "content", "group", "signature")


def _unread_position_items(value):
    """List the items a bundle position in no read form carries.

    A single mapping standing at a position stands as
    the one item it stands as, and a bare string or a
    byte form standing at a position stands as the one
    text item it carries. An items view stands read for
    the values it views, beside the standing readings
    for the remaining forms.
    """
    if isinstance(value, _Mapping):
        return [value]
    if isinstance(value, (str, _UserString)) or _is_byte_like(value):
        return [value]
    if isinstance(value, _ItemsView):
        return [inner for _key, inner in value]
    if isinstance(value, (_ValuesView, _KeysView)):
        return list(value)
    if hasattr(value, "__getitem__"):
        try:
            return list(value)
        except Exception:
            return []
    if hasattr(value, "__iter__"):
        return list(value)
    return []


def _wrapped_key_holdout(key):
    """Return the holdout material a wrapped key carries.

    A key standing as a mapping stands in no wrapped
    form here, its standing reading standing elsewhere.
    A key standing as a single pass iterable carrying a
    pair stands listed once only in this reading and
    read for the holdout side that pair carries. A key
    standing in a container form, a tuple, a list, a
    set, or a frozenset among them, holding a nested
    mapping stands read for that nested mapping, and a
    key standing in such a form holding the two sides
    of a pair as its two elements stands read for the
    holdout side of that pair, a set form carrying no
    order between its sides and standing read for both
    of them. A container key holding a further wrapped
    key stands read in the same way at any depth. Any
    other key stands in no wrapped form here and
    returns None.
    """
    if isinstance(key, _Mapping):
        return None
    if isinstance(
        key,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return None
    if _is_single_pass_iterable(key):
        carried = _enumerate_carried(list(key))
        sides = _pair_elements(carried)
        if sides is not None and all(
            isinstance(side, _Mapping)
            and _is_pair_side_item(side)
            for side in sides
        ):
            return [sides[1]]
        if isinstance(carried, _Mapping):
            return [carried]
        return None
    if isinstance(
        key,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ) or isinstance(key, _Sequence):
        try:
            elements = list(key)
        except Exception:
            return None
        nested = [
            element
            for element in elements
            if isinstance(element, _Mapping)
            and not any(
                field in element for field in _ITEM_FIELD_KEYS
            )
        ]
        if nested:
            return nested
        if len(elements) == 2 and all(
            isinstance(element, _Mapping)
            and _is_pair_side_item(element)
            for element in elements
        ):
            if isinstance(key, (set, frozenset)):
                return elements
            return [elements[1]]
        carried = []
        for element in elements:
            inner = _wrapped_key_holdout(element)
            if inner:
                carried.extend(inner)
        if carried:
            return carried
        return None
    return None


def _mapping_position_values(value):
    """Return the values a mapping bundle position carries.

    A mapping standing at a bundle position and carrying
    no item field of its own stands as a container of
    items, and the items it carries stand in its values,
    in parity with the generic mapping reading the
    direct act gives that same mapping at its top level.
    A mapping carrying an item field stands as the one
    item it stands as, and returns None here. Material
    standing as a wrapped or container formed key of
    such a mapping stands carried beside its values in
    the same reading, through the wrapped key reading.
    """
    if isinstance(value, _Mapping) and not any(
        key in value for key in _ITEM_FIELD_KEYS
    ):
        carried = []
        for key in value.keys():
            if isinstance(key, _Mapping):
                carried.append(key)
            else:
                wrapped = _wrapped_key_holdout(key)
                if wrapped:
                    carried.extend(wrapped)
        return carried + list(value.values())
    return None


def _carries_nested_mapping(listed):
    """Whether listed elements carry a nested mapping.

    An element standing as a mapping carrying no item
    field of its own and standing as no pair in its own
    right stands as a nested mapping in this reading,
    and an element standing in a container form, a list,
    a tuple, a deque, a UserList, a set, or a frozenset
    among them, stands as carrying one where any element
    it carries stands as one or carries one in the same
    way, at any depth the presentation nests it. An
    element standing in a dictionary view form, in an
    iterator form, or in any other iterable form stands
    as carrying one in the same way, on the elements the
    form carries, an items view standing read for the
    entries it yields, whose elements stand in the entry
    tuples the view yields, and for the entry keys it
    yields in the same way, a values view standing read
    for the keys of the mapping it stands over in the
    same way, so a nested mapping standing
    inside a carrier form, or inside a second carrier
    form the first carrier carries, stands reached in
    the same way.
    """
    for element in listed:
        if isinstance(element, _Mapping) and not any(
            key in element for key in _ITEM_FIELD_KEYS
        ) and _pair_elements(element) is None:
            return True
        if isinstance(
            element,
            (
                str,
                _UserString,
                bytes,
                bytearray,
                memoryview,
                _array_module.array,
                range,
                _Mapping,
            ),
        ):
            continue
        if isinstance(
            element,
            (
                list,
                tuple,
                set,
                frozenset,
                _collections_module.deque,
                _collections_module.UserList,
            ),
        ) and _carries_nested_mapping(list(element)):
            return True
        if isinstance(element, _ItemsView):
            if _carries_nested_mapping(
                [inner for _entry_key, inner in element]
            ):
                return True
            if _carries_nested_mapping(
                [
                    entry_key
                    for entry_key, _inner in element
                    if isinstance(entry_key, _Mapping)
                    or isinstance(
                        entry_key,
                        (
                            list,
                            tuple,
                            set,
                            frozenset,
                            _collections_module.deque,
                            _collections_module.UserList,
                        ),
                    )
                ]
            ):
                return True
            continue
        if isinstance(element, _ValuesView):
            if _carries_nested_mapping(list(element)):
                return True
            underlying = getattr(element, "mapping", None)
            if underlying is None:
                underlying = getattr(element, "_mapping", None)
            if _is_plain_mapping(underlying):
                if _carries_nested_mapping(
                    [
                        entry_key
                        for entry_key in underlying.keys()
                        if isinstance(entry_key, _Mapping)
                        or isinstance(
                            entry_key,
                            (
                                list,
                                tuple,
                                set,
                                frozenset,
                                _collections_module.deque,
                                _collections_module.UserList,
                            ),
                        )
                    ]
                ):
                    return True
            continue
        if isinstance(element, _KeysView):
            if _carries_nested_mapping(
                [
                    entry
                    for entry in element
                    if isinstance(entry, _Mapping)
                    or isinstance(
                        entry,
                        (
                            list,
                            tuple,
                            set,
                            frozenset,
                            _collections_module.deque,
                            _collections_module.UserList,
                        ),
                    )
                ]
            ):
                return True
            continue
        if hasattr(element, "__next__") or hasattr(
            element, "__iter__"
        ):
            try:
                children = list(element)
            except Exception:
                continue
            if _carries_nested_mapping(children):
                return True
    return False


def _carrier_relisted_form(element):
    """Return a re-readable form of a carrier element.

    An element standing as an iterator stands listed
    once in this reading, the list holding the relisted
    forms of the items it yields, so a later reading of
    the returned form stands over the same items and no
    presented item stands consumed by an earlier read.
    An element standing in a re-readable container or
    view form stands rebuilt in a list of its relisted
    elements where any element it carries stands
    relisted, and stands as it stands where none does,
    so a form carrying no iterator keeps its standing
    presentation. A text form, a byte form, a mapping,
    and any other element standing in no carrier form
    stands as it stands.
    """
    if isinstance(
        element,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
        ),
    ):
        return element
    if hasattr(element, "__next__"):
        return [
            _carrier_relisted_form(inner)
            for inner in list(element)
        ]
    if _is_single_pass_iterable(element):
        return [
            _carrier_relisted_form(inner)
            for inner in list(element)
        ]
    if isinstance(element, _ItemsView):
        entries = [
            (key, _carrier_relisted_form(inner))
            for key, inner in element
        ]
        if all(
            new_inner is old_inner
            for (_key, new_inner), (_old_key, old_inner) in zip(
                entries, list(element)
            )
        ):
            return element
        return entries
    if isinstance(element, (_ValuesView, _KeysView)):
        listed = [
            _carrier_relisted_form(inner) for inner in element
        ]
        if all(
            new is old for new, old in zip(listed, list(element))
        ):
            return element
        return listed
    if isinstance(
        element,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ) or isinstance(
        element, (_Sequence, _Set)
    ) or hasattr(
        element, "__iter__"
    ) or hasattr(
        element, "__getitem__"
    ):
        try:
            raw = list(element)
        except Exception:
            return element
        listed = [_carrier_relisted_form(inner) for inner in raw]
        if all(new is old for new, old in zip(listed, raw)):
            return element
        return listed
    return element


def _mapping_position_material(values):
    """Expand mapping values carrying material in their values.

    A value standing as a mapping carrying no item field
    of its own and standing as no pair in its own right
    stands read for the material its own values carry, in
    the same reading its position receives, at any depth
    the presentation nests it. A value standing as a list
    or a tuple stands read in the same way for the
    elements it carries. A value standing in a container
    or iterator form, a deque, a UserList, a list holding
    a list, a general iterable container, or a generator
    among them, carrying a nested mapping in the elements
    it carries, at any depth the presentation nests it,
    stands read in the same way for the material the
    nested mapping carries, the form standing listed once
    in that reading where it stands as an iterator. A
    value standing as a dictionary view form carrying a
    nested mapping stands read in the same way, a values
    view for the values it views, a keys view for the
    keys it views, and an items view for the values its
    entries carry, beside any entry key standing itself
    as a mapping. Any other value stands as it stands.
    """
    expanded = []
    for value in values:
        if isinstance(value, _Mapping) and not any(
            key in value for key in _ITEM_FIELD_KEYS
        ) and _pair_elements(value) is None:
            carried = []
            for key in value.keys():
                if isinstance(key, _Mapping):
                    carried.append(key)
                else:
                    wrapped = _wrapped_key_holdout(key)
                    if wrapped:
                        carried.extend(wrapped)
            expanded.extend(
                _mapping_position_material(
                    carried + list(value.values())
                )
            )
        elif isinstance(value, (_ValuesView, _KeysView)):
            expanded.extend(
                _mapping_position_material(list(value))
            )
        elif isinstance(value, _ItemsView):
            collected = []
            for entry_key, inner in value:
                if isinstance(entry_key, _Mapping):
                    collected.append(entry_key)
                else:
                    wrapped = _wrapped_key_holdout(entry_key)
                    if wrapped:
                        collected.extend(wrapped)
                collected.append(inner)
            expanded.extend(
                _mapping_position_material(collected)
            )
        elif isinstance(
            value,
            (
                str,
                _UserString,
                bytes,
                bytearray,
                memoryview,
                _array_module.array,
                range,
                _Mapping,
                _ItemsView,
                _KeysView,
                _ValuesView,
            ),
        ):
            expanded.append(value)
        elif isinstance(
            value, (list, tuple)
        ) or hasattr(value, "__iter__") or hasattr(
            value, "__next__"
        ):
            is_iterator = hasattr(value, "__next__")
            raw_listed = list(value)
            listed = [
                _carrier_relisted_form(element)
                for element in raw_listed
            ]
            if _carries_nested_mapping(listed):
                expanded.append(
                    _mapping_position_material(listed)
                )
            elif is_iterator or _is_single_pass_iterable(value):
                expanded.append(listed)
            elif any(
                new is not old
                for new, old in zip(listed, raw_listed)
            ):
                expanded.append(listed)
            else:
                expanded.append(value)
        else:
            expanded.append(value)
    return expanded


def _is_pair_side_item(value):
    """Whether a value stands as an item a pair side carries.

    A mapping carrying an item field of its own, a text
    form, and a byte form each stand as such an item.
    Any other value stands in no such form here.
    """
    if isinstance(value, _Mapping):
        return any(key in value for key in _ITEM_FIELD_KEYS)
    return isinstance(
        value, (str, _UserString)
    ) or _is_byte_like(value)


def _chain_map_items_entries(value):
    """Return the entries of a ChainMap items view in maps order.

    An items view of a ChainMap yields its entries in
    the reverse of the order of its maps, as the ruling
    527 reading records for the same position. The
    entries of such a view therefore stand listed in
    the order of its maps in this reading, a key standing
    in an earlier map standing for the entry that map
    presents where a later map carries the same key. An
    items view over any other mapping stands in no form
    here and returns None, so the standing view order
    listing decides it.
    """
    underlying = getattr(value, "_mapping", None)
    if not isinstance(
        underlying, _collections_module.ChainMap
    ):
        return None
    seen = set()
    entries = []
    for chained in underlying.maps:
        for key, inner in chained.items():
            if key in seen:
                continue
            seen.add(key)
            entries.append((key, inner))
    return entries


def _chain_map_view_sides(value):
    """Return the two sides a ChainMap dictionary view carries.

    A dictionary view of a ChainMap yields its entries
    in the reverse of the order of its maps, the order
    its sides stand presented, as the ruling 527 reading
    records for the mapping form of the same position.
    A view standing over a ChainMap therefore stands
    read in the order of its maps in this reading: a
    keys view for the keys its maps carry in maps order,
    and a values view or an items view for the values
    its maps carry in maps order, a key standing in an
    earlier map standing for the entry that map presents
    where a later map carries the same key. A view over
    any other mapping, and a ChainMap view carrying any
    count of sides but two, stands in no form here and
    returns None, so the standing view order reading
    decides it.
    """
    underlying = getattr(value, "_mapping", None)
    if not isinstance(
        underlying, _collections_module.ChainMap
    ):
        return None
    seen = set()
    sides = []
    if isinstance(value, _KeysView):
        for chained in underlying.maps:
            for key in chained:
                if key in seen:
                    continue
                seen.add(key)
                sides.append(key)
    elif isinstance(value, (_ValuesView, _ItemsView)):
        for chained in underlying.maps:
            for key, inner in chained.items():
                if key in seen:
                    continue
                seen.add(key)
                sides.append(inner)
    else:
        return None
    if len(sides) == 2:
        return sides[0], sides[1]
    return None


def _mapping_key_sides(value):
    """Return the two sides standing as the keys of a mapping.

    A mapping carrying two keys, each standing as an
    item a pair side carries in mapping form, stands
    read for those keys as its pair sides. A ChainMap
    stands read in the order of its maps, in parity
    with ruling 569, a key standing in an earlier map
    standing before a key standing in a later map. Any
    other mapping stands read in its standing key
    order. A mapping standing in no such form returns
    None.
    """
    if not isinstance(value, _Mapping):
        return None
    if _pair_elements(value) is not None:
        return None
    if len(value) != 2:
        return None
    if not all(
        isinstance(key, _Mapping) and _is_pair_side_item(key)
        for key in value.keys()
    ):
        return None
    if isinstance(value, _collections_module.ChainMap):
        sides = []
        for chained in value.maps:
            for key in chained.keys():
                if any(key is held for held in sides):
                    continue
                sides.append(key)
        if len(sides) == 2:
            return sides[0], sides[1]
        return None
    listed = list(value.keys())
    if len(listed) != 2:
        return None
    return listed[0], listed[1]


def _values_view_key_sides(value):
    """Return the pair sides a values view key carries.

    A values view carries the values of its mapping and
    reaches no key in its own listing. A key of the
    underlying mapping standing in a container form
    holding the two sides of a pair stands read here
    for those sides, in parity with the items view and
    keys view forms of the same mapping, which reach
    the key in full. A view over any other mapping, and
    a key standing in no such form, stands in no form
    here and returns None.
    """
    underlying = getattr(value, "mapping", None)
    if underlying is None:
        underlying = getattr(value, "_mapping", None)
    if not isinstance(underlying, _Mapping):
        return None
    for key in underlying.keys():
        if isinstance(key, _Mapping):
            continue
        if isinstance(
            key,
            (
                list,
                tuple,
                set,
                frozenset,
                _collections_module.deque,
                _collections_module.UserList,
            ),
        ) or isinstance(key, _Sequence):
            sides = _pair_elements(key)
            if sides is not None and all(
                _is_pair_side_item(side) for side in sides
            ):
                return sides
    return None


def _values_view_key_holdout(value):
    """Return the holdout material a values view key carries.

    A key of the underlying mapping standing as a
    wrapped key or as a container formed key stands
    read here for the holdout material it carries,
    through the wrapped key reading, in parity with
    the keys view form of the same mapping. A view over
    any other mapping, and a key standing in no such
    form, carries no material here.
    """
    underlying = getattr(value, "mapping", None)
    if underlying is None:
        underlying = getattr(value, "_mapping", None)
    if not isinstance(underlying, _Mapping):
        return []
    carried = []
    for key in underlying.keys():
        if isinstance(key, _Mapping):
            continue
        wrapped = _wrapped_key_holdout(key)
        if wrapped:
            carried.extend(wrapped)
    return carried


def _single_pair_sides(value):
    """Return the two sides a single pair position value carries.

    A pairs position value standing as a single pair
    stands read through the pair reading for the sides it
    carries. A value standing as a dictionary items view
    or values view, whose pair reading stands in no pair
    form, stands read for the two values it views, and a
    value standing as a dictionary keys view, whose pair
    reading stands in no pair form in the same way,
    stands read for the two keys it views, in parity with
    the values view form. A value standing as a dictionary
    view of a ChainMap stands read for the pair it carries
    in the order of its maps, in parity with the maps
    order reading the mapping form of the same position
    receives. A value standing in a container
    form that iterates by indexed access alone stands
    read for the two elements its indexed access yields,
    in the same form. A view standing as the one element
    a view, a container, or a mapping value carries
    stands read in the same way at any depth, a mapping
    standing read for the pair its values carry and for
    the pair standing as its two keys, a ChainMap in
    the order of its maps. A single pass iterable
    standing as a mapping value or in any other position
    this reading reaches stands listed once only in
    this reading and read for the pair its listed form
    carries, in parity with its items view and values
    view forms.
    """
    if _is_index_pair_form(value):
        return _single_pair_sides(_index_pair_second(value))
    if _is_single_pass_iterable(value):
        return _single_pair_sides(list(value))
    if isinstance(value, _KeysView):
        chain_sides = _chain_map_view_sides(value)
        if chain_sides is not None:
            return chain_sides
        listed = list(value)
        if len(listed) == 2:
            return listed[0], listed[1]
        if len(listed) == 1:
            return _single_pair_sides(listed[0])
        return None
    if isinstance(value, _ItemsView):
        chain_sides = _chain_map_view_sides(value)
        if chain_sides is not None:
            return chain_sides
        carried = [
            _enumerate_carried(inner) for _key, inner in value
        ]
        if len(carried) == 2:
            return carried[0], carried[1]
        if len(carried) == 1:
            return _single_pair_sides(carried[0])
        return None
    if isinstance(value, _ValuesView):
        chain_sides = _chain_map_view_sides(value)
        if chain_sides is not None:
            return chain_sides
        listed = list(value)
        if len(listed) == 2:
            return listed[0], listed[1]
        key_sides = _values_view_key_sides(value)
        if key_sides is not None:
            return key_sides
        if len(listed) == 1:
            return _single_pair_sides(listed[0])
        return None
    if isinstance(value, _Mapping):
        sides = _pair_elements(value)
        if sides is not None:
            return sides
        key_sides = _mapping_key_sides(value)
        if key_sides is not None:
            return key_sides
        for inner in value.values():
            sides = _single_pair_sides(inner)
            if sides is not None:
                return sides
        return None
    if hasattr(value, "__getitem__") and not hasattr(
        value, "__iter__"
    ):
        try:
            listed = list(value)
        except Exception:
            return None
        if len(listed) == 2:
            return listed[0], listed[1]
        if len(listed) == 1:
            return _single_pair_sides(listed[0])
        return None
    if hasattr(value, "__next__"):
        listed = _position_elements(value)
        if listed is not None and len(listed) == 1:
            sides = _single_pair_sides(listed[0])
            if sides is not None:
                return sides
        return _pair_elements(listed)
    listed = _position_elements(value)
    if listed is not None and len(listed) == 1:
        sides = _single_pair_sides(listed[0])
        if sides is not None:
            return sides
    return _pair_elements(value)


def _mappings_within(value):
    """Yield the mappings a value stands as or carries.

    A mapping stands yielded as it stands, and a value
    standing in a re-iterable container form, a list, a
    tuple, a set, a frozenset, a deque, or a UserList,
    stands read for the mappings its elements stand as
    or carry in the same way, at any depth the
    presentation nests them. Any other value yields
    nothing here, and no iterator stands listed by this
    reading.
    """
    if isinstance(value, _Mapping):
        yield value
        return
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        for element in value:
            yield from _mappings_within(element)


def _mappings_within_deep(value, seen=None):
    """Yield the mappings a value stands as or carries deep.

    A mapping stands yielded as it stands, and stands
    read in the same way for the mappings its own values
    stand as or carry, so a mapping standing at a second
    or a third mapping value depth stands yielded in the
    same form as a mapping standing at the first depth.
    A value standing in a re-iterable container form, a
    list, a tuple, a set, a frozenset, a deque, or a
    UserList, stands read for the mappings its elements
    stand as or carry in the same way, at any depth the
    presentation nests them. A dictionary view stands
    read for the mapping it stands over and for the
    mappings its elements stand as or carry in the same
    way, so a carrier mapping presented through a view
    standing at a mapping value, or inside a container,
    stands yielded in the same form as the mapping
    standing there itself. A mapping or a container
    already yielded on this walk stands yielded once
    only, so a cyclic presentation stands bounded and no
    mapping stands counted twice. Any other value yields
    nothing here, and no iterator stands listed by this
    reading.
    """
    if seen is None:
        seen = set()
    if isinstance(value, _Mapping):
        if id(value) in seen:
            return
        seen.add(id(value))
        yield value
        for inner in value.values():
            yield from _mappings_within_deep(inner, seen)
        return
    if isinstance(value, (_KeysView, _ValuesView, _ItemsView)):
        if id(value) in seen:
            return
        seen.add(id(value))
        underlying = getattr(value, "mapping", None)
        if underlying is None:
            underlying = getattr(value, "_mapping", None)
        if not _is_plain_mapping(underlying):
            return
        yield from _mappings_within_deep(underlying, seen)
        try:
            listed = list(value)
        except Exception:
            listed = []
        for element in listed:
            yield from _mappings_within_deep(element, seen)
        return
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        if id(value) in seen:
            return
        seen.add(id(value))
        for element in value:
            yield from _mappings_within_deep(element, seen)


def _is_plain_mapping(value):
    """Whether a mapping stands in a plain walked form.

    A mapping standing in its own form, a plain
    dictionary, a dictionary subclass, an OrderedDict,
    a mapping proxy, and a ChainMap standing in its own
    form among them, stands walked by the view readings
    of this round. A ChainMap standing in a subclass
    form stands in no part of those readings, its
    standing readings governing it, because a walk of
    such a mapping can stand as a delegation act on it.
    """
    return isinstance(value, _Mapping) and not (
        isinstance(value, _collections_module.ChainMap)
        and type(value) is not _collections_module.ChainMap
    )


def _keys_within_view_containers(value, seen=None):
    """List the keys of mappings reached through views.

    A mapping stands read for its own keys in the
    standing way elsewhere, and stands in no part here.
    A dictionary view standing inside a container form,
    a list, a tuple, a set, a frozenset, a deque, or a
    UserList, or standing as a mapping value, stands
    read here for the keys of the mapping it stands
    over, in parity with the same view standing at the
    position itself, and a container or a mapping value
    carrying such a view stands read in the same way at
    any depth the presentation nests it. A view or a
    container already walked on this reading stands
    walked once only, so a cyclic presentation stands
    bounded. Any other value carries no key here, and
    no iterator stands listed by this reading.
    """
    if seen is None:
        seen = set()
    try:
        if isinstance(value, (_KeysView, _ValuesView, _ItemsView)):
            if id(value) in seen:
                return []
            seen.add(id(value))
            keys = []
            underlying = getattr(value, "mapping", None)
            if underlying is None:
                underlying = getattr(value, "_mapping", None)
            if _is_plain_mapping(underlying):
                keys.extend(list(underlying.keys()))
                for inner in underlying.values():
                    keys.extend(
                        _keys_within_view_containers(inner, seen)
                    )
                for element in list(value):
                    keys.extend(
                        _keys_within_view_containers(element, seen)
                    )
            return keys
        if isinstance(value, _Mapping):
            if not _is_plain_mapping(value):
                return []
            if id(value) in seen:
                return []
            seen.add(id(value))
            keys = []
            for inner in value.values():
                keys.extend(
                    _keys_within_view_containers(inner, seen)
                )
            return keys
        if isinstance(
            value,
            (
                list,
                tuple,
                set,
                frozenset,
                _collections_module.deque,
                _collections_module.UserList,
            ),
        ):
            if id(value) in seen:
                return []
            seen.add(id(value))
            keys = []
            for element in value:
                keys.extend(
                    _keys_within_view_containers(element, seen)
                )
            return keys
    except Exception:
        return []
    return []


def _direct_bundle_extra_holdout(bundle, seen_ids=frozenset()):
    """Return holdout items from bundle positions in no read form.

    The plain dictionary bundle limb of the direct act
    reading takes its holdout side from the partitioning
    act, which reads no single mapping position and no
    bare string position. A holdout side position, an
    items position, or a pairs position standing in one
    of those forms in a plain dictionary bundle stands
    read here for the holdout material it carries, in
    parity with the readings the bundle surfaces and
    the direct act top level forms already give, so no
    holdout item the bundle presents stands dropped on
    that route in silence. A position standing as a
    mapping carrying no item field of its own stands
    read here for the holdout material its values carry,
    in that same parity, and a value of such a mapping
    standing itself as a mapping carrying no item field
    of its own stands read for the material its own
    values carry in the same way. A pairs position
    standing as a single pair, in a plain container
    form, an iterator form, a dictionary view form, an
    abstract Sequence or general iterable form, a set
    form, or a form that iterates by indexed access
    alone, stands read here for the holdout side that
    pair carries, where no element of the position
    stands as a pair in its own right, a pair standing
    in a set form standing read for both of its sides,
    the set carrying no order between them. Material
    standing as a key wrapped in a container form, and
    material standing as a container formed key, of a
    mapping presented directly at a holdout side, an
    items, or a pairs position, and material standing
    as an entry key of an items view at the pairs
    position, stands read here in the same way, in
    parity with its keys view forms, through the
    wrapped key reading. Material standing as a wrapped
    key at the items position stands read here in the
    same way, in parity with its holdout side, pairs,
    and holdout forms, and material standing as a
    container formed key of a mapping presented through
    its values view at a holdout side position stands
    read in the partitioning act through the values
    view key reading. Material standing as a key of a
    mapping standing two or three mapping values deep
    at the pairs position stands read here in the same
    way, through the deep mapping reading, in parity
    with its one mapping value form, and material
    standing as a key of a mapping presented through a
    keys view or a values view standing at the items
    position stands read here in the same way, through
    the keys of the mapping the view stands over, in
    parity with its plain mapping and items view forms
    at that position. Material standing as a key of a
    mapping presented through a view standing at a
    mapping value of the pairs position, or through a
    view standing inside a container or as a mapping
    value at the items position, or through a view
    standing inside a container at a holdout side
    position, stands read here in the same way, through
    the keys of the mapping the view stands over and
    through the deep mapping reading, in parity with
    the same views standing at those positions
    themselves.
    """
    extra = []
    for key in ("holdout_items", "holdout"):
        if key in bundle:
            value = bundle[key]
            if isinstance(value, _ItemsView):
                collected = []
                for entry_key, _inner in value:
                    if isinstance(entry_key, _Mapping):
                        collected.append(entry_key)
                    else:
                        wrapped = _wrapped_key_holdout(entry_key)
                        if wrapped:
                            collected.extend(wrapped)
                for element in _mapping_position_material(
                    collected
                ):
                    extra.extend(_unwrapped_items(element))
            if not isinstance(
                value, (_KeysView, _ValuesView, _ItemsView)
            ):
                nested_keys = _keys_within_view_containers(value)
                if nested_keys:
                    nested_material = []
                    for nested_key in nested_keys:
                        if isinstance(nested_key, _Mapping):
                            continue
                        wrapped = _wrapped_key_holdout(nested_key)
                        if wrapped:
                            nested_material.extend(wrapped)
                    if nested_material:
                        held_ids = {
                            id(item) for item in extra
                        } | set(seen_ids)
                        for element in _mapping_position_material(
                            nested_material
                        ):
                            for item in _unwrapped_items(element):
                                if id(item) in held_ids:
                                    continue
                                held_ids.add(id(item))
                                extra.append(item)
            if value is None or _is_partitionable_form(value):
                continue
            values = _mapping_position_values(value)
            if values is not None:
                for element in _mapping_position_material(values):
                    extra.extend(_unwrapped_items(element))
                continue
            for element in _unread_position_items(value):
                extra.extend(_unwrapped_items(element))
    if "items" in bundle:
        value = bundle["items"]
        items_start = len(extra)
        if isinstance(value, _ItemsView):
            collected = []
            for entry_key, _inner in value:
                if isinstance(entry_key, _Mapping):
                    collected.append(entry_key)
                else:
                    wrapped = _wrapped_key_holdout(entry_key)
                    if wrapped:
                        collected.extend(wrapped)
            for element in _mapping_position_material(collected):
                for item in _unwrapped_items(element):
                    side = None
                    if isinstance(item, _Mapping):
                        side = item.get("split") or item.get("side")
                    if side in ("holdout", "sealed holdout"):
                        extra.append(item)
        if value is not None and not _is_partitionable_form(value):
            values = _mapping_position_values(value)
            if values is not None:
                elements = _mapping_position_material(values)
            else:
                elements = _unread_position_items(value)
            for element in elements:
                for item in _unwrapped_items(element):
                    side = None
                    if isinstance(item, _Mapping):
                        side = item.get("split") or item.get("side")
                    if side in ("holdout", "sealed holdout"):
                        extra.append(item)
        wrapped_keys = []
        if isinstance(value, _ItemsView):
            wrapped_keys = [
                entry_key for entry_key, _inner in value
            ]
        elif isinstance(value, (_KeysView, _ValuesView)):
            underlying = getattr(value, "mapping", None)
            if underlying is None:
                underlying = getattr(value, "_mapping", None)
            if isinstance(underlying, _Mapping):
                wrapped_keys = list(underlying.keys())
        elif isinstance(value, _Mapping):
            wrapped_keys = list(value.keys())
        wrapped_keys.extend(_keys_within_view_containers(value))
        wrapped_material = []
        for wrapped_key in wrapped_keys:
            if isinstance(wrapped_key, _Mapping):
                continue
            wrapped = _wrapped_key_holdout(wrapped_key)
            if wrapped:
                wrapped_material.extend(wrapped)
        if wrapped_material:
            held_ids = {
                id(item) for item in extra[items_start:]
            } | set(seen_ids)
            if isinstance(value, _KeysView):
                split_elements = _position_elements(value)
                if split_elements is not None:
                    for split_element in split_elements:
                        for split_item in _unwrapped_items(
                            split_element
                        ):
                            if isinstance(split_item, _Mapping):
                                split_side = (
                                    split_item.get("split")
                                    or split_item.get("side")
                                )
                                if split_side in (
                                    "holdout",
                                    "sealed holdout",
                                ):
                                    held_ids.add(id(split_item))
            for element in _mapping_position_material(
                wrapped_material
            ):
                for item in _unwrapped_items(element):
                    side = None
                    if isinstance(item, _Mapping):
                        side = item.get("split") or item.get("side")
                    if side in ("candidate",):
                        continue
                    if id(item) in held_ids:
                        continue
                    held_ids.add(id(item))
                    extra.append(item)
    if "pairs" in bundle:
        value = bundle["pairs"]
        if value is not None:
            if isinstance(value, _Mapping):
                key_material = []
                for key in value.keys():
                    if isinstance(key, _Mapping):
                        continue
                    wrapped = _wrapped_key_holdout(key)
                    if wrapped:
                        key_material.extend(wrapped)
                if key_material:
                    for element in _mapping_position_material(
                        key_material
                    ):
                        extra.extend(_unwrapped_items(element))
            if isinstance(value, _ItemsView):
                for entry_key, _entry_inner in value:
                    if isinstance(entry_key, _Mapping):
                        entry_material = [entry_key]
                    else:
                        entry_material = (
                            _wrapped_key_holdout(entry_key) or []
                        )
                    for element in _mapping_position_material(
                        entry_material
                    ):
                        extra.extend(_unwrapped_items(element))
            values = _mapping_position_values(value)
            if isinstance(value, _Mapping) and (
                _pair_elements(value) is not None
            ):
                sides = _pair_elements(value)
                extra.extend(_unwrapped_items(sides[1]))
            elif (
                isinstance(value, _Mapping)
                and values is not None
                and len(values) == 2
                and all(
                    _is_pair_side_item(element)
                    for element in values
                )
            ):
                pair_values = values
                if isinstance(
                    value, _collections_module.ChainMap
                ):
                    pair_values = [
                        inner
                        for chained in value.maps
                        for inner in chained.values()
                    ]
                extra.extend(_unwrapped_items(pair_values[1]))
            elif (
                isinstance(value, _Mapping)
                and len(value) == 2
                and all(
                    _is_pair_side_item(key) for key in value.keys()
                )
            ):
                key_sides = _mapping_key_sides(value)
                if key_sides is not None:
                    extra.extend(_unwrapped_items(key_sides[1]))
                else:
                    listed_keys = list(value.keys())
                    if len(listed_keys) == 2:
                        extra.extend(
                            _unwrapped_items(listed_keys[1])
                        )
            elif values is not None:
                keyed_sides = None
                for element in values:
                    keyed_sides = _mapping_key_sides(element)
                    if keyed_sides is not None:
                        break
                if keyed_sides is not None:
                    view_sides = keyed_sides
                else:
                    view_sides = None
                if view_sides is None:
                    for element in values:
                        view_sides = _single_pair_sides(element)
                        if view_sides is not None:
                            break
                if view_sides is not None:
                    extra.extend(
                        _unwrapped_items(view_sides[1])
                    )
                else:
                    carrier_start = len(extra)
                    carrier_material = []
                    for element in values:
                        for mapping in _mappings_within_deep(element):
                            for carrier_key in mapping.keys():
                                if isinstance(
                                    carrier_key, _Mapping
                                ):
                                    continue
                                wrapped = _wrapped_key_holdout(
                                    carrier_key
                                )
                                if wrapped:
                                    carrier_material.extend(wrapped)
                    if carrier_material:
                        for element in _mapping_position_material(
                            carrier_material
                        ):
                            extra.extend(_unwrapped_items(element))
                    held_ids = {
                        id(item) for item in extra[carrier_start:]
                    }
                    for element in _mapping_position_material(
                        values
                    ):
                        sides = _pair_elements(element)
                        if sides is not None:
                            for item in _unwrapped_items(sides[1]):
                                if id(item) in held_ids:
                                    continue
                                held_ids.add(id(item))
                                extra.append(item)
            elif not _is_partitionable_form(value):
                for element in _unread_position_items(value):
                    sides = _pair_elements(element)
                    if sides is not None:
                        extra.extend(_unwrapped_items(sides[1]))
            elif _is_partitionable_form(value):
                sides = _single_pair_sides(value)
                if sides is not None:
                    listed = _pairs_position_elements(value)
                    if listed is not None and not any(
                        _pair_elements(element) is not None
                        for element in listed
                    ):
                        if isinstance(value, _Set) and not isinstance(
                            value, (_KeysView, _ValuesView, _ItemsView)
                        ):
                            extra.extend(
                                _unwrapped_items(sides[0])
                            )
                        extra.extend(_unwrapped_items(sides[1]))
            carrier_material = []
            for mapping in _mappings_within_deep(value):
                for carrier_key in mapping.keys():
                    if isinstance(carrier_key, _Mapping):
                        continue
                    wrapped = _wrapped_key_holdout(carrier_key)
                    if wrapped:
                        carrier_material.extend(wrapped)
            if carrier_material:
                held_ids = {
                    id(item) for item in extra
                } | set(seen_ids)
                for element in _mapping_position_material(
                    carrier_material
                ):
                    for item in _unwrapped_items(element):
                        if id(item) in held_ids:
                            continue
                        held_ids.add(id(item))
                        extra.append(item)
    return extra


def _nested_mapping_from_value(value):
    """Return the nested mapping a wrapped form carries, or None.

    A mapping carrying no item field of its own stands
    as the nested mapping it stands as. A dictionary
    view stands read for the nested mapping its elements
    carry, an items view standing read as the mapping
    its entries rebuild where every entry carries one.
    Any other container, iterator, Sequence, Set, or
    iterable form stands read for the nested mapping
    standing in the elements it carries, through the
    listed form reading below. A text form, a byte form,
    and a mapping carrying an item field of its own each
    stand in no nested mapping form here.
    """
    if isinstance(value, _Mapping):
        if not any(
            field in value for field in _ITEM_FIELD_KEYS
        ):
            return value
        return None
    if isinstance(
        value,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return None
    if isinstance(value, _ItemsView):
        entries = list(value)
        if entries and all(
            isinstance(inner, _Mapping)
            and not any(
                field in inner for field in _ITEM_FIELD_KEYS
            )
            for _entry_key, inner in entries
        ):
            return dict(entries)
        return _nested_mapping_from_listed(
            [inner for _entry_key, inner in entries]
        )
    if isinstance(value, (_ValuesView, _KeysView)):
        return _nested_mapping_from_listed(list(value))
    if (
        hasattr(value, "__next__")
        or hasattr(value, "__iter__")
        or hasattr(value, "__getitem__")
    ):
        try:
            listed = list(value)
        except Exception:
            return None
        return _nested_mapping_from_listed(listed)
    return None


def _nested_mapping_from_listed(listed):
    """Return the nested mapping a listed form carries, or None.

    A listed form holding the one element stands read
    for the nested mapping that element carries, in the
    reading above, at any depth the presentation nests
    it. A listed form standing as an enumerate index
    pair, an integer standing in first place beside the
    element it carries, stands read for the nested
    mapping its second element carries, in the same way.
    Any other listed form stands in no nested mapping
    form here.
    """
    if len(listed) == 1:
        return _nested_mapping_from_value(listed[0])
    if len(listed) == 2 and isinstance(listed[0], int):
        return _nested_mapping_from_value(listed[1])
    return None


def _wrapped_probe(listed):
    """Probe a listed wrapped form for the mapping it carries.

    The listed elements stand relisted in the carrier
    relisted form first, so an iterator element stands
    held in its listed form and no element stands
    consumed by the probe where the form carries no
    nested mapping. A dictionary view element stands as
    it stands in this probe, so a single pass key the
    view carries stands consumed by no probe listing
    and stands read by the key readings that follow.
    Returns the nested mapping the form
    carries or None, the relisted form, and whether any
    element stands relisted, so a form the probe changed
    stands replaced by its relisted form where it
    carries no nested mapping, in the standing form of
    the generator limb of the wrapped position reading.
    """
    relisted = [
        element
        if isinstance(element, (_KeysView, _ValuesView, _ItemsView))
        else _carrier_relisted_form(element)
        for element in listed
    ]
    nested = _nested_mapping_from_listed(relisted)
    changed = any(
        new is not old for new, old in zip(relisted, listed)
    )
    return nested, relisted, changed


def _multi_nested_replacement(relisted):
    """Return a mapping holding every element of a listed form.

    A wrapped form carrying a nested mapping beside a
    further element, or carrying two or more nested
    mappings, stands in no single nested mapping form.
    Where the listed form carries a nested mapping in
    that way, the elements stand held in a mapping of
    their own positions, so the readings that follow
    stand over the material each element carries, in
    the same form the mapping position reading gives a
    mapping standing at the position itself.
    """
    if _carries_nested_mapping(relisted):
        return dict(enumerate(relisted))
    return None


def _view_mapping_form(element):
    """Return the mapping a dictionary view element carries.

    A dictionary view standing as an element of a
    container at a bundle position stands read in the
    wrapped nested reading as the mapping it stands
    over, in parity with the keys view form of the same
    reading standing at the position itself, so the key
    material the viewed mapping carries stands read by
    the readings that follow and no part of it stands
    dissolved by the listing of the view. A ChainMap
    stands read in the order of its maps in the same
    way. Any other element stands as it stands.
    """
    if isinstance(element, (_KeysView, _ValuesView, _ItemsView)):
        underlying = getattr(element, "mapping", None)
        if underlying is None:
            underlying = getattr(element, "_mapping", None)
        if not _is_plain_mapping(underlying):
            return element
        try:
            if isinstance(
                underlying, _collections_module.ChainMap
            ):
                carried = {}
                for chained in underlying.maps:
                    for chained_key, inner in chained.items():
                        if chained_key in carried:
                            continue
                        carried[chained_key] = inner
                return carried
            if isinstance(underlying, _Mapping):
                return dict(underlying)
        except Exception:
            return element
    return element


def _carries_stored_iterator(value):
    """Whether a value carries an iterator in its store.

    A delegating container form carries the one stored
    iterator its iteration act returns, standing in its
    own store beside any elements it holds. A container
    carrying its elements in a re-iterable store carries
    no iterator in that store.
    """
    try:
        stored = vars(value)
    except Exception:
        return False
    if not isinstance(stored, _Mapping):
        return False
    return any(
        hasattr(inner, "__next__") for inner in stored.values()
    )


def _is_delegating_container(element):
    """Whether a container element stands delegating.

    A list, a tuple, a deque, or a UserList standing in
    a subclass form whose iteration act stands defined
    by a class standing between its own class and its
    container base, its own class among them, stands as
    a delegating form, in the form the promote wrapper
    papers state for that family, delegating to one
    stored iterator it carries, and stands read by no
    reading that rebuilds it. A subclass form whose
    iteration act stands inherited from its container
    base, the UserList base inheriting its act from the
    abstract Sequence form among them, and a subclass
    form carrying no stored iterator, stand in no
    delegating form here.
    """
    bases = (
        list,
        tuple,
        _collections_module.deque,
        _collections_module.UserList,
    )
    if not isinstance(element, bases):
        return False
    if type(element) in bases:
        return False
    if not _carries_stored_iterator(element):
        return False
    for klass in type(element).__mro__:
        if klass in bases:
            return False
        if "__iter__" in klass.__dict__:
            return True
    return False


def _carries_keys_view(value, ancestors=frozenset()):
    """Whether a listed form carries a keys view.

    A keys view standing in the listed form itself, or
    inside a container or a mapping standing in it,
    stands carried. An iterator standing in the listed
    form stands in no part here, so a reading that
    lists an iterator to try it stands bounded by the
    forms the listing itself reached.
    """
    if isinstance(value, _KeysView):
        return True
    if isinstance(value, (_ItemsView, _ValuesView)):
        return False
    if hasattr(value, "__next__"):
        return False
    if id(value) in ancestors:
        return False
    child_ancestors = ancestors | {id(value)}
    if isinstance(value, _Mapping):
        return any(
            _carries_keys_view(key, child_ancestors)
            or _carries_keys_view(inner, child_ancestors)
            for key, inner in value.items()
        )
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        return any(
            _carries_keys_view(inner, child_ancestors)
            for inner in value
        )
    return False


def _carries_any_view(value, ancestors=frozenset()):
    """Whether a listed form carries a dictionary view.

    A keys view, an items view, or a values view standing
    in the listed form itself, or inside a container or a
    mapping standing in it, stands carried, an items view
    and a values view standing read through the keys and
    values of the mapping they stand over. An iterator
    standing in the listed form stands in no part here,
    in the form of the keys view reading above.
    """
    if isinstance(value, _KeysView):
        return True
    if isinstance(value, (_ItemsView, _ValuesView)):
        underlying = getattr(value, "mapping", None)
        if underlying is None:
            underlying = getattr(value, "_mapping", None)
        if isinstance(underlying, _Mapping):
            return True
        return False
    if hasattr(value, "__next__"):
        return False
    if id(value) in ancestors:
        return False
    child_ancestors = ancestors | {id(value)}
    if isinstance(value, _Mapping):
        return any(
            _carries_any_view(key, child_ancestors)
            or _carries_any_view(inner, child_ancestors)
            for key, inner in value.items()
        )
    if isinstance(
        value,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        return any(
            _carries_any_view(inner, child_ancestors)
            for inner in _container_elements_preserved(value)
        )
    return False


def _is_indexed_only_container(value):
    """Whether a value carries its elements by indexed
    access alone.

    A container standing with a length act and an item
    access act, and standing with no iteration act and
    no next act of its own, and standing in none of the
    forms the neighbouring readings name, a text form, a
    byte form, a mapping, a dictionary view, a range, or
    a standing container form among them, carries its
    elements in that form here.
    """
    if hasattr(value, "__next__") or hasattr(value, "__iter__"):
        return False
    if not hasattr(value, "__getitem__"):
        return False
    if not hasattr(value, "__len__"):
        return False
    if isinstance(
        value,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
            _KeysView,
            _ItemsView,
            _ValuesView,
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
            _Set,
            _WeakSet,
        ),
    ):
        return False
    return True


def _indexed_elements(value):
    """Return the elements a container carrying its
    elements by indexed access alone presents, in
    presentation order, or None where that reading
    stands refused on the form presented."""
    try:
        return [value[index] for index in range(len(value))]
    except Exception:
        return None


def _is_generic_iterable_container(value):
    """Whether a value stands in a generic iterable form.

    A container carrying its elements by an iteration
    act of its own, carrying no next act, and standing
    in none of the forms the deep view reading rebuilds
    in its own limbs, the exact and subclass container
    forms, the mapping and view forms, and the set
    forms among them, stands in a generic iterable
    form here. A container carrying a stored iterator
    stands in no such form here: its standing readings
    govern it as they govern a delegating form.
    """
    if hasattr(value, "__next__"):
        return False
    if not hasattr(value, "__iter__"):
        return False
    if isinstance(
        value,
        (
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
            _Mapping,
            _KeysView,
            _ItemsView,
            _ValuesView,
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
            _Set,
            _WeakSet,
        ),
    ):
        return False
    return True


def _deep_listed_expansion(items, seen=frozenset()):
    """Expand a listed form for the deep view reading.

    Each element of the listed form stands in a node of
    its own: a plain element stands as the value it
    stands as, an iterator element stands as the
    expansion of its own listed form, and a generic
    iterable element standing in no delegating form
    stands as the expansion of its listed form in the
    same way, so a keys view standing inside an iterator
    standing inside an iterator, or inside a generic
    iterable container, stands reached by the expansion
    at any depth the presentation nests those forms.
    The expansion also reports whether any node carries
    a keys view, a plain element carrying one standing
    read by the standing keys view reading. The report
    also stands where a plain element carries an items
    view or a values view, read by the any view reading,
    and an element carrying its elements by indexed
    access alone stands as the expansion of its indexed
    elements in the same way. An element
    standing inside itself stands as a plain value.
    Returns the nodes and the carrying report.
    """
    nodes = []
    carries = False
    for inner in items:
        if hasattr(inner, "__next__"):
            if id(inner) in seen:
                nodes.append(("value", inner, None))
                continue
            children, child_carries = _deep_listed_expansion(
                list(inner), seen | {id(inner)}
            )
            nodes.append(("listed", children, None))
            carries = carries or child_carries
        elif _is_generic_iterable_container(
            inner
        ) and not _carries_stored_iterator(inner):
            if id(inner) in seen:
                nodes.append(("value", inner, None))
                continue
            children, child_carries = _deep_listed_expansion(
                list(inner), seen | {id(inner)}
            )
            restore = (
                None if _is_single_pass_iterable(inner) else inner
            )
            nodes.append(("listed", children, restore))
            carries = carries or child_carries
        elif isinstance(
            inner,
            (
                list,
                tuple,
                _collections_module.deque,
                _collections_module.UserList,
            ),
        ) and not _is_delegating_container(inner):
            if id(inner) in seen:
                nodes.append(("value", inner, None))
                continue
            children, child_carries = _deep_listed_expansion(
                list(inner), seen | {id(inner)}
            )
            nodes.append(
                (
                    "container",
                    (children, _beside_container_type(inner)),
                    None,
                )
            )
            carries = carries or child_carries
        elif _is_indexed_only_container(inner):
            if id(inner) in seen:
                nodes.append(("value", inner, None))
                continue
            indexed = _indexed_elements(inner)
            if indexed is None:
                nodes.append(("value", inner, None))
                continue
            children, child_carries = _deep_listed_expansion(
                indexed, seen | {id(inner)}
            )
            nodes.append(("listed", children, inner))
            carries = carries or child_carries
        else:
            nodes.append(("value", inner, None))
            if _carries_keys_view(inner) or _carries_any_view(
                inner
            ):
                carries = True
    return nodes, carries


def _deep_rebuilt_container(children, container_type):
    """Return a container of the given exact form
    standing over the given elements, in the form the
    deep view reading rebuilds a container in."""
    if container_type is tuple:
        return tuple(children)
    if container_type is _collections_module.deque:
        return _collections_module.deque(children)
    if container_type is _collections_module.UserList:
        return _collections_module.UserList(children)
    return list(children)


def _deep_expanded_form(nodes):
    """Return the listed form an expansion stands for,
    with each listed node standing as the list of its
    own expanded form and each container node standing
    rebuilt in its exact container form over its own
    expanded form."""
    expanded = []
    for kind, payload, _restore in nodes:
        if kind == "listed":
            expanded.append(_deep_expanded_form(payload))
        elif kind == "container":
            children, container_type = payload
            expanded.append(
                _deep_rebuilt_container(
                    _deep_expanded_form(children), container_type
                )
            )
        else:
            expanded.append(payload)
    return expanded


def _deep_restored_form(nodes):
    """Return the listed form an expansion restores,
    with each listed node standing restored in the form
    it stood in: a re-iterable container stands as it
    stands, and a listed form standing listed once only
    stands as an iterator over its restored elements,
    and each container node standing rebuilt in its
    exact container form over its restored elements."""
    restored = []
    for kind, payload, restore in nodes:
        if kind == "listed":
            if restore is not None:
                restored.append(restore)
            else:
                children = _deep_restored_form(payload)
                restored.append(
                    (inner for inner in children)
                )
        elif kind == "container":
            children, container_type = payload
            restored.append(
                _deep_rebuilt_container(
                    _deep_restored_form(children), container_type
                )
            )
        else:
            restored.append(payload)
    return restored


def _deep_carried_form(nodes):
    """Return the listed form an expansion carries,
    with each node standing in the form the deep view
    reading carries it in: a plain element stands as
    it stands, a keys view among them standing
    preserved as the view it stands as, and a listed
    or container node standing as the list of its own
    carried form, a container node standing for an
    exact container form an iterator yielded, a zip
    object yielding its element standing in a tuple
    among them."""
    carried = []
    for kind, payload, _restore in nodes:
        if kind == "value":
            carried.append(payload)
        elif kind == "container":
            children, _container_type = payload
            carried.append(_deep_carried_form(children))
        else:
            carried.append(_deep_carried_form(payload))
    return carried


def _deep_carried_view_form(element, ancestors=frozenset()):
    """Return an expanded element with its views carried
    in mapping form.

    An items view or a values view standing in the
    expanded form stands read in the mapping form the
    view reading gives it, in parity with a keys view
    standing in the same form, and an exact container
    standing in the expanded form stands rebuilt in its
    own form with its elements carried in the same way.
    Any other element stands read in the deep view
    reading in its standing form.
    """
    if isinstance(element, (_ItemsView, _ValuesView)):
        return _view_mapping_form(element)
    if type(element) in (
        list,
        tuple,
        _collections_module.deque,
        _collections_module.UserList,
    ):
        rebuilt = [
            _deep_carried_view_form(inner, ancestors)
            for inner in element
        ]
        if isinstance(element, tuple):
            return tuple(rebuilt)
        if isinstance(element, _collections_module.deque):
            return _collections_module.deque(rebuilt)
        if isinstance(element, _collections_module.UserList):
            return _collections_module.UserList(rebuilt)
        return rebuilt
    return _view_mapping_form_deep(element, ancestors, top=False)


def _view_mapping_form_deep(element, ancestors=frozenset(), top=True):
    """Return an element with its deep keys views carried.

    An element standing as a dictionary view stands
    read in the mapping form the reading above gives
    it, in its standing form. An element standing in a
    re-iterable container form standing in its exact
    form, a list, a tuple, a deque, or a UserList,
    stands rebuilt in the same form with a keys view
    standing inside it, at any further container depth
    the presentation nests it, standing read in that
    same mapping form, in parity with the same keys
    view standing as a direct element of the position
    container. A container standing in a plain subclass
    form of one of those container forms, its iteration
    act standing inherited from its container base,
    stands rebuilt in the exact form of that base in
    the same way, in parity with the same keys view
    standing inside the exact form at the same depth.
    A container standing in a delegating subclass form
    stands as it stands, its standing readings
    governing it in the same way as at the first
    container level. An iterator standing inside a
    container and carrying a keys view stands listed
    once in this reading and stands rebuilt as the
    list of its elements read in the same way, in
    parity with the same keys view standing inside a
    container the reading rebuilds. An iterator
    carrying no keys view stands listed once in this
    reading and stands carried as an iterator over
    its listed elements, in its standing form in
    every other part. A keys view standing inside an
    iterator standing inside an iterator stands
    reached in the same way, the expansion of the
    listed form standing in place of the listing
    itself, in parity with the same keys view standing
    inside one iterator. A keys view standing inside
    a generic iterable container, a container carrying
    its elements by an iteration act of its own and
    standing in none of the forms above, stands read
    in the same way, in parity with the same keys view
    standing inside a carried container form, a
    generic container standing in a delegating form
    standing as it stands. A plain mapping standing as
    an element stands rebuilt with its values read in
    the same way, its keys standing as they stand, so
    a keys view standing inside a generic iterable
    container standing at a mapping value of the
    mapping stands carried in the form the mapping
    value readings decide, in parity with the same
    keys view standing inside a carried container at
    that value. A keys view standing at a value of a
    plain mapping stands preserved as the view it
    stands as, and a keys view standing inside a
    container standing at such a value stands carried
    in the carried form of its expansion, so a plain
    mapping standing as an element of a container
    stands read in the same way as the same mapping
    standing at the position itself. An items view or
    a values view standing inside a generic iterable
    container, or inside a container carrying its
    elements by indexed access alone, stands carried
    in the mapping form of its expanded form, in
    parity with the same view standing inside a
    carried container form, and a keys view standing
    inside a container carrying its elements by
    indexed access alone stands read in the same way.
    A container standing inside
    itself stands as it stands at the cyclic position.
    Any other element stands as it stands.
    """
    if isinstance(element, (_KeysView, _ValuesView, _ItemsView)):
        if top or isinstance(element, _KeysView):
            return _view_mapping_form(element)
        return element
    if type(element) in (
        list,
        tuple,
        _collections_module.deque,
        _collections_module.UserList,
    ):
        if id(element) in ancestors:
            return element
        child_ancestors = ancestors | {id(element)}
        rebuilt = [
            _view_mapping_form_deep(
                inner, child_ancestors, top=False
            )
            for inner in element
        ]
        if isinstance(element, tuple):
            return tuple(rebuilt)
        if isinstance(element, _collections_module.deque):
            return _collections_module.deque(rebuilt)
        if isinstance(element, _collections_module.UserList):
            return _collections_module.UserList(rebuilt)
        return rebuilt
    if isinstance(
        element,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        if _is_delegating_container(element):
            return element
        if id(element) in ancestors:
            return element
        child_ancestors = ancestors | {id(element)}
        rebuilt = [
            _view_mapping_form_deep(
                inner, child_ancestors, top=False
            )
            for inner in element
        ]
        if isinstance(element, tuple):
            return tuple(rebuilt)
        if isinstance(element, _collections_module.deque):
            return _collections_module.deque(rebuilt)
        if isinstance(element, _collections_module.UserList):
            return _collections_module.UserList(rebuilt)
        return rebuilt
    if type(element) is dict:
        if id(element) in ancestors:
            return element
        child_ancestors = ancestors | {id(element)}
        rebuilt = {}
        for key, inner in element.items():
            if isinstance(inner, _KeysView):
                rebuilt[key] = inner
                continue
            if _is_generic_iterable_container(
                inner
            ) and not _carries_stored_iterator(inner):
                nodes, carries = _deep_listed_expansion(
                    list(inner), child_ancestors | {id(inner)}
                )
                if carries:
                    rebuilt[key] = _deep_carried_form(nodes)
                elif _is_single_pass_iterable(inner):
                    rebuilt[key] = (
                        carried
                        for carried in _deep_restored_form(
                            nodes
                        )
                    )
                else:
                    rebuilt[key] = inner
                continue
            if isinstance(
                inner,
                (
                    list,
                    tuple,
                    _collections_module.deque,
                    _collections_module.UserList,
                ),
            ) and not _is_delegating_container(inner):
                nodes, carries = _deep_listed_expansion(
                    list(inner), child_ancestors | {id(inner)}
                )
                if carries:
                    rebuilt[key] = _deep_carried_form(nodes)
                    continue
            elif hasattr(inner, "__next__"):
                listed_inner = list(inner)
                nodes, carries = _deep_listed_expansion(
                    listed_inner, child_ancestors | {id(inner)}
                )
                if carries:
                    rebuilt[key] = _deep_carried_form(nodes)
                    continue
                rebuilt[key] = (
                    carried
                    for carried in _deep_restored_form(nodes)
                )
                continue
            elif _is_indexed_only_container(inner):
                indexed = _indexed_elements(inner)
                if indexed is not None:
                    nodes, carries = _deep_listed_expansion(
                        indexed, child_ancestors | {id(inner)}
                    )
                    if carries:
                        rebuilt[key] = _deep_carried_form(nodes)
                        continue
            rebuilt[key] = _view_mapping_form_deep(
                inner, child_ancestors, top=False
            )
        return rebuilt
    if isinstance(element, _Mapping) and _is_plain_mapping(
        element
    ):
        if id(element) in ancestors:
            return element
        child_ancestors = ancestors | {id(element)}
        rebuilt = {}
        changed = False
        for key, inner in element.items():
            if isinstance(inner, _KeysView):
                rebuilt[key] = inner
                continue
            if _is_generic_iterable_container(
                inner
            ) and not _carries_stored_iterator(inner):
                nodes, carries = _deep_listed_expansion(
                    list(inner), child_ancestors | {id(inner)}
                )
                if carries:
                    rebuilt[key] = _deep_carried_form(nodes)
                    changed = True
                elif _is_single_pass_iterable(inner):
                    rebuilt[key] = (
                        carried
                        for carried in _deep_restored_form(
                            nodes
                        )
                    )
                    changed = True
                else:
                    rebuilt[key] = inner
                continue
            if isinstance(
                inner,
                (
                    list,
                    tuple,
                    _collections_module.deque,
                    _collections_module.UserList,
                ),
            ) and not _is_delegating_container(inner):
                nodes, carries = _deep_listed_expansion(
                    list(inner), child_ancestors | {id(inner)}
                )
                if carries:
                    rebuilt[key] = _deep_carried_form(nodes)
                    changed = True
                    continue
            elif hasattr(inner, "__next__"):
                listed_inner = list(inner)
                nodes, carries = _deep_listed_expansion(
                    listed_inner, child_ancestors | {id(inner)}
                )
                if carries:
                    rebuilt[key] = _deep_carried_form(nodes)
                    changed = True
                    continue
                rebuilt[key] = (
                    carried
                    for carried in _deep_restored_form(nodes)
                )
                changed = True
                continue
            elif _is_indexed_only_container(inner):
                indexed = _indexed_elements(inner)
                if indexed is not None:
                    nodes, carries = _deep_listed_expansion(
                        indexed, child_ancestors | {id(inner)}
                    )
                    if carries:
                        rebuilt[key] = _deep_carried_form(nodes)
                        changed = True
                        continue
            rebuilt[key] = _view_mapping_form_deep(
                inner, child_ancestors, top=False
            )
            if rebuilt[key] is not inner:
                changed = True
        if not changed:
            return element
        return rebuilt
    if hasattr(element, "__next__"):
        if id(element) in ancestors:
            return element
        child_ancestors = ancestors | {id(element)}
        listed = list(element)
        nodes, carries = _deep_listed_expansion(
            listed, child_ancestors
        )
        if not carries:
            return (
                inner for inner in _deep_restored_form(nodes)
            )
        return [
            _deep_carried_view_form(inner, child_ancestors)
            for inner in _deep_expanded_form(nodes)
        ]
    if _is_generic_iterable_container(
        element
    ) and not _carries_stored_iterator(element):
        if id(element) in ancestors:
            return element
        child_ancestors = ancestors | {id(element)}
        nodes, carries = _deep_listed_expansion(
            list(element), child_ancestors
        )
        if not carries:
            if _is_single_pass_iterable(element):
                return (
                    inner
                    for inner in _deep_restored_form(nodes)
                )
            return element
        return [
            _deep_carried_view_form(inner, child_ancestors)
            for inner in _deep_expanded_form(nodes)
        ]
    if _is_indexed_only_container(element):
        if id(element) in ancestors:
            return element
        indexed = _indexed_elements(element)
        if indexed is None:
            return element
        child_ancestors = ancestors | {id(element)}
        nodes, carries = _deep_listed_expansion(
            indexed, child_ancestors
        )
        if not carries:
            return element
        return [
            _deep_carried_view_form(inner, child_ancestors)
            for inner in _deep_expanded_form(nodes)
        ]
    return element


def _beside_container_type(value):
    """Return the exact container form a container
    stands in or stands a subclass of, a list, a tuple,
    a deque, or a UserList, in the order its class
    order carries them, or None where it stands in
    none of those forms."""
    for klass in type(value).__mro__:
        if klass in (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ):
            return klass
    return None


def _preserved_beside_element(original, relisted, container_type):
    """Return one element of a beside sibling replacement
    with its view material preserved.

    A keys view element stands preserved as the view
    it stands as, so the readings that follow stand
    over the keys of the mapping it stands over. An
    items view or a values view element stands
    preserved in the same way where its container
    stands as a list, a tuple, a deque, or a UserList,
    and stands in its relisted form in every other
    container, in the bounded form the ruling of this
    round states for those containers.
    A plain mapping element carrying no item field of
    its own and standing as no pair stands read as the
    keys view of that mapping, in parity with the same
    mapping standing alone inside the same container.
    A container element standing in an exact container
    form stands rebuilt from its elements in the same
    way. A container element standing in a plain
    subclass of one of those forms stands rebuilt from
    its elements in the same way, under the container
    form it stands a subclass of, in parity with the
    same presentation standing inside the exact form.
    A container element standing in a delegating form
    stands in its relisted form, its standing readings
    governing it. An iterator element stands rebuilt
    from its relisted form in the same way, the
    relisted form standing as the listing the readings
    before this one took of it. A container element
    standing in a generic iterable form stands rebuilt
    from its elements in the same way, a single pass
    element standing rebuilt from its relisted form
    itself, and a container element carrying its
    elements by indexed access alone stands rebuilt
    from its indexed elements in the same way, a
    generic element standing in a delegating form
    standing in its relisted form. Any other element
    stands in its relisted form.
    """
    if isinstance(original, _KeysView):
        return original
    if isinstance(original, (_ItemsView, _ValuesView)):
        if container_type in (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ):
            return original
        return relisted
    if isinstance(original, _Mapping):
        if container_type in (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ) and _is_plain_mapping(original) and not any(
            field in original for field in _ITEM_FIELD_KEYS
        ) and _pair_elements(original) is None and any(
            isinstance(key, (tuple, list, set, frozenset))
            and _wrapped_key_holdout(key)
            for key in original.keys()
        ):
            try:
                return original.keys()
            except Exception:
                return relisted
        return relisted
    if isinstance(
        original,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        if _is_delegating_container(original):
            return relisted
        try:
            original_listed = list(original)
            relisted_listed = list(relisted)
        except Exception:
            return relisted
        if len(original_listed) != len(relisted_listed):
            return relisted
        return [
            _preserved_beside_element(
                inner_original,
                inner_relisted,
                _beside_container_type(original),
            )
            for inner_original, inner_relisted in zip(
                original_listed, relisted_listed
            )
        ]
    if hasattr(original, "__next__"):
        try:
            relisted_listed = list(relisted)
        except Exception:
            return relisted
        return [
            _preserved_beside_element(inner, inner, list)
            for inner in relisted_listed
        ]
    if _is_generic_iterable_container(
        original
    ) and not _carries_stored_iterator(original):
        try:
            relisted_listed = list(relisted)
        except Exception:
            return relisted
        if _is_single_pass_iterable(original):
            return [
                _preserved_beside_element(inner, inner, list)
                for inner in relisted_listed
            ]
        try:
            original_listed = list(original)
        except Exception:
            return relisted
        if len(original_listed) != len(relisted_listed):
            return relisted
        return [
            _preserved_beside_element(
                inner_original,
                inner_relisted,
                list,
            )
            for inner_original, inner_relisted in zip(
                original_listed, relisted_listed
            )
        ]
    if _is_indexed_only_container(original):
        original_listed = _indexed_elements(original)
        if original_listed is None:
            return relisted
        try:
            relisted_listed = list(relisted)
        except Exception:
            return relisted
        if len(original_listed) != len(relisted_listed):
            return relisted
        return [
            _preserved_beside_element(
                inner_original,
                inner_relisted,
                list,
            )
            for inner_original, inner_relisted in zip(
                original_listed, relisted_listed
            )
        ]
    return relisted


def _preserved_multi_replacement(original_value, relisted):
    """Return the multi nested replacement for a beside
    sibling presentation, with its view material
    preserved.

    The multi nested replacement above holds the
    elements of a beside sibling presentation in a
    mapping of their own positions, in a form where a
    dictionary view element stands dissolved into the
    mapping it stands over, so the readings that
    follow stand over no key the view carries. Where
    the position container stands in an exact form, a
    list, a tuple, a deque, or a UserList, the
    replacement stands rebuilt here with each element
    standing in the preserved form the reading above
    gives it, in parity with the same presentation
    standing alone inside the same container. Where
    the position container stands in a plain subclass
    of one of those forms, the replacement stands
    rebuilt in the same way, under the container form
    it stands a subclass of. Where the position
    container stands as an iterator, the replacement
    stands rebuilt from the relisted form itself, the
    relisted form standing as the listing the readings
    before this one took of it. A position container
    standing in a delegating form, and a position
    container standing in any other form, keeps the
    standing replacement in full. Where the position
    container stands in a generic iterable form, a
    container carrying its elements by an iteration act
    of its own and standing in none of the forms above,
    the replacement stands rebuilt in the same way from
    its listed elements, a single pass container standing
    rebuilt from the relisted form itself, and where the
    position container carries its elements by indexed
    access alone the replacement stands rebuilt from its
    indexed elements in the same way, in parity with the
    same presentation standing inside a carried container
    form, a generic container standing in a delegating
    form standing as it stands.
    """
    multi = _multi_nested_replacement(relisted)
    if multi is None:
        return None
    if hasattr(original_value, "__next__"):
        return {
            index: _preserved_beside_element(
                element, element, list
            )
            for index, element in enumerate(relisted)
        }
    if not isinstance(
        original_value,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        if _is_generic_iterable_container(
            original_value
        ) and not _carries_stored_iterator(original_value):
            if _is_single_pass_iterable(original_value):
                return {
                    index: _preserved_beside_element(
                        element, element, list
                    )
                    for index, element in enumerate(relisted)
                }
            try:
                original_listed = list(original_value)
            except Exception:
                return multi
            if len(original_listed) != len(relisted):
                return multi
            return {
                index: _preserved_beside_element(
                    original,
                    relisted_element,
                    list,
                )
                for index, (
                    original,
                    relisted_element,
                ) in enumerate(
                    zip(original_listed, relisted)
                )
            }
        if _is_indexed_only_container(original_value):
            original_listed = _indexed_elements(original_value)
            if original_listed is None:
                return multi
            if len(original_listed) != len(relisted):
                return multi
            return {
                index: _preserved_beside_element(
                    original,
                    relisted_element,
                    list,
                )
                for index, (
                    original,
                    relisted_element,
                ) in enumerate(
                    zip(original_listed, relisted)
                )
            }
        return multi
    if _is_delegating_container(original_value):
        return multi
    try:
        original_listed = list(original_value)
    except Exception:
        return multi
    if len(original_listed) != len(relisted):
        return multi
    return {
        index: _preserved_beside_element(
            original,
            relisted_element,
            _beside_container_type(original_value),
        )
        for index, (original, relisted_element) in enumerate(
            zip(original_listed, relisted)
        )
    }


class _ListedSinglePassForm:
    """A single pass iterable standing over listed
    elements, in the form of the single pass forms the
    pairs position reading lists.

    Its first listing yields its elements and its
    later listings yield none, and it carries no next
    act of its own, so a single pass form standing
    listed by that reading stands restored in this
    form with its elements standing as they stood.
    """

    def __init__(self, items):
        self._items = list(items)
        self._spent = False

    def __iter__(self):
        if self._spent:
            return iter(())
        self._spent = True
        return iter(self._items)


def _pairs_probe_element(element):
    """Probe an element a pairs position carrier
    carries, returning whether it carries a dictionary
    view in substance, the restored element, and
    whether the restored element stands in a changed
    form.

    A dictionary view stands carried in substance. An
    iterator stands listed once, its elements standing
    probed in the same way and standing restored as a
    generator over their restored forms. A container
    standing in an exact container form stands rebuilt
    in that form over its probed elements. A single
    pass iterable stands listed once and stands
    restored in the listed single pass form above. A
    Sequence form carrier, a generic iterable
    container, and a container carrying its elements
    by indexed access alone stand listed in the same
    way, their elements standing probed, the carrier
    itself standing restored as it stands where no
    element it carries stands changed by the probing,
    and standing in no restored form here where an
    element does, its caller deciding that case. Any
    other element stands as it stands, read for a
    carried view in the standing way.
    """
    if isinstance(element, (_KeysView, _ItemsView, _ValuesView)):
        return (True, element, False)
    if hasattr(element, "__next__"):
        probed = [
            _pairs_probe_element(inner)
            for inner in list(element)
        ]
        restored = (
            inner for inner in [entry[1] for entry in probed]
        )
        return (
            any(entry[0] for entry in probed),
            restored,
            True,
        )
    if isinstance(
        element,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        probed = [
            _pairs_probe_element(inner) for inner in element
        ]
        restored_list = [entry[1] for entry in probed]
        if isinstance(element, tuple):
            restored = tuple(restored_list)
        elif isinstance(element, _collections_module.deque):
            restored = _collections_module.deque(restored_list)
        elif isinstance(element, _collections_module.UserList):
            restored = _collections_module.UserList(
                restored_list
            )
        else:
            restored = restored_list
        return (
            any(entry[0] for entry in probed),
            restored,
            any(entry[2] for entry in probed),
        )
    if _is_single_pass_iterable(element):
        probed = [
            _pairs_probe_element(inner)
            for inner in list(element)
        ]
        restored = _ListedSinglePassForm(
            [entry[1] for entry in probed]
        )
        return (
            any(entry[0] for entry in probed),
            restored,
            True,
        )
    if isinstance(element, _Sequence) or (
        _is_generic_iterable_container(element)
    ) or _is_indexed_only_container(element):
        listed = _pairs_carrier_elements(element)
        if listed is None:
            return (_carries_any_view(element), element, False)
        probed = [
            _pairs_probe_element(inner) for inner in listed
        ]
        return (
            any(entry[0] for entry in probed),
            element,
            any(entry[2] for entry in probed),
        )
    return (_carries_any_view(element), element, False)


def _pairs_carrier_elements(old):
    """List the elements a pairs position carrier
    carries, in the form its own reading presents
    them, or return None where it carries none in a
    listed form."""
    try:
        if hasattr(old, "__next__"):
            return list(old)
        if _is_indexed_only_container(old) and not hasattr(
            old, "__iter__"
        ):
            return _indexed_elements(old)
        return list(old)
    except Exception:
        return None


def _pairs_carried_entry(old):
    """Return the carried form of a mapping value at
    the pairs position, in two kinds.

    A value standing in an exact or subclass container
    form, a list, a tuple, a set, a frozenset, a deque,
    or a UserList, a mapping, a dictionary view, or a
    text or byte form stands in no part of this
    reading, its standing readings governing it at the
    pairs position as they stand: this reading returns
    None for it and lists nothing it carries. A value
    standing as an iterator, as a Sequence form
    carrier, as a generic iterable container, or as a
    container carrying its elements by indexed access
    alone stands listed once here. Where an element it
    carries stands as a dictionary view or carries one
    in substance, the entry stands charged: this
    reading returns the deep view form of its probed
    elements, in the form the deep view reading
    carries such a carrier, as the first element of
    its return. Where no element carries a view, its
    probed elements stand restored in their standing
    kinds, as the second element of the return, so no
    material stands lost to the listing: an iterator
    stands restored as a generator over its probed
    elements, a single pass iterable stands restored
    in the listed single pass form, in the bounded
    form of ruling 722, and a carrier standing
    re-iterable with no element changed by the probing
    stands as it stands, this reading returning None
    for it.
    """
    if isinstance(
        old,
        (
            list,
            tuple,
            set,
            frozenset,
            _collections_module.deque,
            _collections_module.UserList,
            _Mapping,
            _KeysView,
            _ItemsView,
            _ValuesView,
            str,
            _UserString,
            bytes,
            bytearray,
            memoryview,
        ),
    ):
        return (None, None)
    if not (
        hasattr(old, "__next__")
        or isinstance(old, _Sequence)
        or _is_generic_iterable_container(old)
        or _is_indexed_only_container(old)
    ):
        return (None, None)
    listed = _pairs_carrier_elements(old)
    if listed is None:
        return (None, None)
    probed = [
        _pairs_probe_element(element) for element in listed
    ]
    restored_list = [entry[1] for entry in probed]
    if any(entry[0] for entry in probed):
        return (
            _view_mapping_form_deep(restored_list),
            None,
        )
    if hasattr(old, "__next__"):
        return (
            None,
            (inner for inner in restored_list),
        )
    if _is_single_pass_iterable(old):
        return (None, _ListedSinglePassForm(restored_list))
    if any(entry[2] for entry in probed):
        return (None, restored_list)
    return (None, None)


def _delegating_container_elements(value):
    """Return the elements a delegating container
    subclass form carries, listed once through its
    delegating iteration act.

    The listing consumes the one stored iterator the
    form delegates to, so that iterator stands restored
    in the form store over the listed elements in the
    same act, and the form stands readable again in its
    standing form for every reading that follows, at
    this surface and at every other governed surface.
    A form whose iteration act raises stands in no part
    here, its standing readings governing it as they
    stand.
    """
    try:
        elements = list(value)
    except Exception:
        return None
    try:
        stored = vars(value)
    except Exception:
        stored = None
    if isinstance(stored, _Mapping):
        for name, inner in list(stored.items()):
            if hasattr(inner, "__next__"):
                try:
                    stored[name] = iter(elements)
                except Exception:
                    pass
    return elements


def _container_elements_preserved(value):
    """Return the elements a container reading stands
    to iterate, in a form that leaves the container
    standing as it stands.

    A container standing in a delegating container
    subclass form stands listed through the delegating
    container elements reading above, its stored
    iterator standing restored over its listed
    elements, so a reading that lists it to judge it
    takes no material from it. A container standing in
    any other form stands as it stands, its own
    iteration act governing the listing in its standing
    form.
    """
    if _is_delegating_container_subclass(value):
        elements = _delegating_container_elements(value)
        if elements is not None:
            return elements
    return value


def _pairs_position_entry(old, ancestors=frozenset()):
    """Return the carried form of one mapping value at
    the pairs or holdout_items position, in two kinds,
    beside whether the entry stands touched at all.

    An entry standing in the carrier forms the pairs
    carried entry reading governs stands carried or
    restored in the form that reading states. An entry
    An entry standing as a dict form carrying no item field of
    its own stands read entry by entry in the same
    way, at any mapping depth the presentation nests
    it, so a carrier standing at a value of a mapping
    standing at a value of the position mapping stands
    carried in substance in the same form. An entry
    standing as a UserDict or a ChainMap carrying no
    item field of its own stands read entry by entry
    in the same way. An entry standing as a mapping in
    a mappingproxy form, or in a custom Mapping form,
    stands read entry by entry in the same way. An
    entry standing in a plain container form, a list,
    a tuple, a deque, or a UserList, in its exact form
    or in a subclass form of one of those, stands read
    element by element in the same way and stands
    rebuilt in its own container form over its carried
    elements where any element it carries stands
    carried, a container standing in a delegating
    container subclass form standing read element by
    element in the same way through the delegating
    container elements reading above, its stored
    iterator standing restored over its listed
    elements so no material stands lost to the
    listing, so a carrier
    standing inside a plain
    container at the entry, and a mapping standing
    inside a plain container at the entry carrying a
    carrier at its own value, stand carried in
    substance in the same form. An entry standing
    inside itself stands untouched at the cyclic
    position. An entry standing in any other form
    stands untouched here.
    """
    charged, restored = _pairs_carried_entry(old)
    if charged is not None:
        return (charged, True)
    if restored is not None:
        return (restored, True)
    if id(old) in ancestors:
        return (None, False)
    child_ancestors = ancestors | {id(old)}
    if isinstance(
        old,
        (
            dict,
            _collections_module.UserDict,
            _collections_module.ChainMap,
        ),
    ) and not any(
        field in old for field in _ITEM_FIELD_KEYS
    ):
        carried = {}
        touched = False
        for carried_key, inner in old.items():
            new, inner_touched = _pairs_position_entry(
                inner, child_ancestors
            )
            if inner_touched:
                carried[carried_key] = new
                touched = True
            else:
                carried[carried_key] = inner
        if touched:
            return (carried, True)
    if isinstance(
        old, _types_module.MappingProxyType
    ) or (
        isinstance(old, _Mapping)
        and not isinstance(
            old,
            (
                dict,
                _collections_module.UserDict,
                _collections_module.ChainMap,
            ),
        )
    ):
        try:
            other_items = list(old.items())
        except Exception:
            other_items = None
        if other_items is not None:
            try:
                has_item_field = any(
                    field in old for field in _ITEM_FIELD_KEYS
                )
            except Exception:
                has_item_field = False
            if not has_item_field:
                carried = {}
                touched = False
                for carried_key, inner in other_items:
                    new, inner_touched = _pairs_position_entry(
                        inner, child_ancestors
                    )
                    if inner_touched:
                        carried[carried_key] = new
                        touched = True
                    else:
                        carried[carried_key] = inner
                if touched:
                    return (carried, True)
    if isinstance(
        old,
        (
            list,
            tuple,
            _collections_module.deque,
            _collections_module.UserList,
        ),
    ):
        if _is_delegating_container_subclass(old):
            elements = _delegating_container_elements(old)
            if elements is None:
                return (None, False)
            probed = []
            for inner in elements:
                try:
                    probed.append(
                        _pairs_position_entry(
                            inner, child_ancestors
                        )
                    )
                except Exception:
                    probed.append((None, False))
        else:
            elements = list(old)
            probed = [
                _pairs_position_entry(inner, child_ancestors)
                for inner in elements
            ]
        if any(entry_touched for _new, entry_touched in probed):
            rebuilt_list = [
                new if entry_touched else inner
                for (new, entry_touched), inner in zip(
                    probed, elements
                )
            ]
            if isinstance(old, tuple):
                return (tuple(rebuilt_list), True)
            if isinstance(old, _collections_module.deque):
                return (
                    _collections_module.deque(rebuilt_list),
                    True,
                )
            if isinstance(old, _collections_module.UserList):
                return (
                    _collections_module.UserList(rebuilt_list),
                    True,
                )
            return (rebuilt_list, True)
    return (None, False)


def _holdout_carried_form(new):
    """Return a carried form of a holdout_items entry
    with its items views standing in mapping form.

    An items view standing carried in a listed form at
    this position stands read by both the partitioning
    act and the extra holdout reading in that form, so
    its material stands counted twice where every
    other view form at this position stands counted
    once. An items view therefore stands carried here
    as the mapping it stands over, in the form the
    view mapping reading gives it, in parity with the
    keys view form of the same presentation. A deque
    or a UserList standing in the carried form stands
    rebuilt in its own form over its carried elements
    in the same way, so an items view standing inside
    such a container stands counted once in the same
    form. Any other form stands as it stands.
    """
    if isinstance(new, _ItemsView):
        return _view_mapping_form(new)
    if isinstance(new, list):
        return [_holdout_carried_form(inner) for inner in new]
    if isinstance(new, _collections_module.deque):
        return _collections_module.deque(
            _holdout_carried_form(inner) for inner in new
        )
    if isinstance(new, _collections_module.UserList):
        return _collections_module.UserList(
            [_holdout_carried_form(inner) for inner in new]
        )
    if isinstance(new, tuple):
        return tuple(
            _holdout_carried_form(inner) for inner in new
        )
    if isinstance(new, dict):
        return {
            key: _holdout_carried_form(inner)
            for key, inner in new.items()
        }
    return new


def _wrapped_nested_position_material(material):
    """Return the bundle with a wrapped nested position read.

    A bundle position standing as a nested mapping, a
    mapping carrying no item field of its own, where the
    position itself stands wrapped in a values view, an
    items view, a tuple, a deque, or a generator form,
    stands read in this reading as the nested mapping it
    carries, in a shallow copy of the bundle, so the
    direct act readings that follow stand over the
    material the nested mapping carries. A values view
    holding the one nested mapping stands read as that
    mapping, an items view whose entries carry nested
    mappings stands read as the mapping its entries
    rebuild, and a tuple, a deque, or a generator holding
    the one nested mapping stands read as that mapping,
    a generator standing listed once in that reading.
    A position standing wrapped in a list, a UserList, a
    set, a frozenset, a zip, or an enumerate form, or
    standing one container deeper inside a list holding
    a list, a tuple holding a tuple, a double tuple, a
    double deque, or a deque inside a tuple, stands read
    as the nested mapping it carries in the same way,
    through the nested mapping reading above, a zip
    object standing read for the tuple it yields and an
    enumerate object for the pair it yields.
    A keys view standing inside two or more containers
    at a position stands carried in the mapping form of
    the deep view reading above, in parity with the same
    keys view standing inside one container at that
    position.
    A dictionary view standing inside a container at a
    position beside a second element stands carried in
    the preserved form of the multi nested replacement
    above, in parity with the same presentation
    standing alone inside the same container, in the
    bounded form that replacement states for an items
    view or a values view standing beside a second
    element inside a tuple, a deque, or a UserList.
    A position standing in any other form stands as it
    stands, a generator position standing listed once
    where it stands consumed by this reading and stands
    in no wrapped nested form.
    """
    if not isinstance(material, _Mapping):
        return material
    copied = None
    for key in _POSITION_KEYS:
        if key not in material:
            continue
        value = material[key]
        if value is None:
            continue
        replacement = None
        if isinstance(value, _ValuesView):
            listed = list(value)
            relisted = [
                _carrier_relisted_form(element)
                for element in listed
            ]
            changed = any(
                new is not old
                for new, old in zip(relisted, listed)
            )
            if len(relisted) == 1 and isinstance(
                relisted[0], _Mapping
            ) and not any(
                field in relisted[0] for field in _ITEM_FIELD_KEYS
            ):
                replacement = relisted[0]
            else:
                nested = _nested_mapping_from_listed(relisted)
                if nested is not None:
                    replacement = nested
                else:
                    replacement = _multi_nested_replacement(
                        relisted
                    )
                if replacement is None and changed:
                    replacement = relisted
        elif isinstance(value, _ItemsView):
            entries = list(value)
            relisted_entries = [
                (entry_key, _carrier_relisted_form(inner))
                for entry_key, inner in entries
            ]
            changed = any(
                new_inner is not old_inner
                for (_new_key, new_inner), (
                    _old_key, old_inner
                ) in zip(relisted_entries, entries)
            )
            if relisted_entries and all(
                isinstance(inner, _Mapping)
                and not any(
                    field in inner for field in _ITEM_FIELD_KEYS
                )
                for _entry_key, inner in relisted_entries
            ):
                replacement = dict(relisted_entries)
            else:
                nested = _nested_mapping_from_listed(
                    [
                        inner
                        for _entry_key, inner in relisted_entries
                    ]
                )
                if nested is not None:
                    replacement = nested
                else:
                    replacement = _multi_nested_replacement(
                        [
                            inner
                            for _entry_key, inner
                            in relisted_entries
                        ]
                    )
                if replacement is None and changed:
                    replacement = dict(relisted_entries).items()
        elif isinstance(value, _KeysView):
            nested, relisted, changed = _wrapped_probe(
                list(value)
            )
            multi = _multi_nested_replacement(relisted)
            if key == "items" and (
                nested is not None or multi is not None
            ):
                underlying = getattr(value, "mapping", None)
                if underlying is None:
                    underlying = getattr(
                        value, "_mapping", None
                    )
                if isinstance(underlying, _Mapping):
                    replacement = dict(underlying)
                elif nested is not None:
                    replacement = nested
                else:
                    replacement = multi
            elif nested is not None:
                replacement = nested
            elif multi is not None:
                replacement = multi
            elif changed:
                replacement = relisted
        elif isinstance(
            value,
            (
                str,
                _UserString,
                bytes,
                bytearray,
                memoryview,
                _array_module.array,
                range,
                _Mapping,
            ),
        ):
            replacement = None
            if key == "items" and isinstance(
                value, _Mapping
            ) and _is_plain_mapping(
                value
            ) and not any(
                field in value for field in _ITEM_FIELD_KEYS
            ):
                deep_value = _view_mapping_form_deep(value)
                if deep_value is not value and len(
                    deep_value
                ) == len(value):
                    carried = {}
                    took = False
                    for carried_key, old in value.items():
                        new = deep_value[carried_key]
                        if new is not old and (
                            not (
                                type(old) is list
                                and len(old) == 1
                                and hasattr(old[0], "__next__")
                            )
                            or _carries_any_view(new)
                        ):
                            carried[carried_key] = new
                            took = True
                        else:
                            carried[carried_key] = old
                    if took:
                        replacement = carried
            if key in ("pairs", "holdout_items") and isinstance(
                value, _Mapping
            ) and _is_plain_mapping(
                value
            ) and not any(
                field in value for field in _ITEM_FIELD_KEYS
            ):
                carried = {}
                touched = False
                for carried_key, old in value.items():
                    new, entry_touched = _pairs_position_entry(
                        old
                    )
                    if entry_touched:
                        if key == "holdout_items":
                            new = _holdout_carried_form(new)
                        carried[carried_key] = new
                        touched = True
                    else:
                        carried[carried_key] = old
                if touched:
                    replacement = carried
        elif isinstance(
            value, (tuple, _collections_module.deque)
        ) or hasattr(value, "__next__"):
            listed = [
                _view_mapping_form_deep(element)
                for element in list(value)
            ]
            nested, relisted, changed = _wrapped_probe(listed)
            multi = _preserved_multi_replacement(value, relisted)
            if nested is not None:
                replacement = nested
            elif multi is not None:
                replacement = multi
            elif hasattr(value, "__next__"):
                replacement = relisted
            elif changed:
                replacement = relisted
        elif isinstance(
            value,
            (
                list,
                _collections_module.UserList,
                set,
                frozenset,
            ),
        ) or isinstance(
            value, (_Sequence, _Set)
        ) or hasattr(
            value, "__iter__"
        ) or hasattr(
            value, "__getitem__"
        ):
            try:
                listed = [
                    _view_mapping_form_deep(element)
                    for element in list(value)
                ]
            except Exception:
                listed = None
            if listed is not None:
                nested, relisted, changed = _wrapped_probe(
                    listed
                )
                multi = _preserved_multi_replacement(
                    value, relisted
                )
                if nested is not None:
                    replacement = nested
                elif multi is not None:
                    replacement = multi
                elif _is_single_pass_iterable(value):
                    replacement = relisted
                elif changed:
                    replacement = relisted
        if replacement is not None:
            if copied is None:
                copied = dict(material)
            copied[key] = replacement
    if copied is None:
        return material
    return copied


def _holdout_items_of(holdout_material):
    if holdout_material is None:
        return []
    if isinstance(holdout_material, str):
        return [holdout_material]
    if isinstance(holdout_material, _UserString):
        return [str(holdout_material)]
    byte_content = _byte_content(holdout_material)
    if byte_content is not None:
        return [byte_content.decode("utf-8", "replace")]
    if isinstance(holdout_material, _Mapping):
        if isinstance(holdout_material, dict) and _is_bundle(
            holdout_material
        ):
            holdout_material = _wrapped_nested_position_material(
                holdout_material
            )
            holdout_material = _materialised_pairs_material(
                holdout_material
            )
            candidate, holdout = _split_items(holdout_material)
            return holdout + _direct_bundle_extra_holdout(
                holdout_material,
                seen_ids=frozenset(
                    id(item) for item in holdout
                ),
            )
        if holdout_material and not any(
            key in holdout_material for key in _ITEM_FIELD_KEYS
        ):
            values = list(holdout_material.values())
            if all(
                isinstance(value, (str, _UserString, _Mapping))
                or _is_byte_like(value)
                for value in values
            ):
                return values
            collected = []
            recognised = False
            for value in values:
                if isinstance(
                    value, (str, _UserString, _Mapping)
                ) or _is_byte_like(
                    value
                ):
                    collected.append(value)
                    recognised = True
                elif hasattr(value, "__iter__"):
                    elements = list(value)
                    if elements:
                        collected.extend(elements)
                        recognised = True
                elif hasattr(value, "__getitem__"):
                    try:
                        elements = list(value)
                    except Exception:
                        elements = []
                    if elements:
                        collected.extend(elements)
                        recognised = True
            if recognised and collected:
                return collected
        return [holdout_material]
    if isinstance(holdout_material, (list, tuple, set, frozenset)):
        return list(holdout_material)
    if hasattr(holdout_material, "__next__") and hasattr(
        holdout_material, "__iter__"
    ):
        return list(holdout_material)
    if hasattr(holdout_material, "__iter__"):
        return list(holdout_material)
    if hasattr(holdout_material, "__getitem__"):
        try:
            return list(holdout_material)
        except Exception:
            return [holdout_material]
    return [holdout_material]


def _audit_instruction_item_impl(
    instruction_text,
    holdout_material,
    occasion="candidate construction",
    after_partial_scoring=False,
):
    """Return the instruction item firing outcome, plan 19.86.

    This act is the one firing decision home for the
    instruction item content test. It takes one
    instruction text, as a string or as a mapping
    carrying its instruction text field, and the
    holdout material, as a single holdout text, as one
    holdout item, as a list of holdout items, or as a
    bundle mapping carrying holdout_items. Holdout
    material standing as a set, a frozenset, a generator,
    or a mapping of items stands unpacked into its items
    and compared in the same way. Holdout material
    standing as a byte string or a bytearray stands read
    for the text it carries, and holdout material
    standing as a deque, a dictionary view, a plain
    iterable, or a mapping whose values carry items in
    list or tuple form or beside a value of another kind
    stands unpacked into its items in the same way. An
    instruction text value standing as a list or a mapping,
    and an item itself standing as a list, stand read for
    the text they carry, and an instruction text value
    standing as bytes or as a generator stands read for
    the text it carries in the same way. It compares
    the instruction text field only, and the text field
    of each holdout item only: no group, no signature,
    and no wider field of either side takes part. A
    pair fires where the texts stand equal (the
    verbatim case, also recorded on the verbatim key)
    or where the module _text_overlap form, dividing
    by the smaller of the two word counts, stands at
    or above the near verbatim threshold. Holdout
    material, and an instruction text, standing in a
    container form that iterates by indexed access
    alone stand read for the material they carry, in
    parity with the materialisation reading the call
    points give that form.

    The return carries, on every case: fired, the
    firing decision; fired_item, the instruction text
    where fired and None where not; instruction_text;
    verbatim; field_scope; wider_material_compared,
    standing False; comparisons, the count of holdout
    texts compared; firing_pairs, one entry per firing
    holdout item, each carrying candidate_position 0,
    its holdout_position, and relations standing at
    the near verbatim cluster relation only;
    cross_split_audit_result, the refusal form of this
    module where fired and its clearance form where
    not, at the record home of the occasion named;
    audit_record, carrying the audit record home, the
    fired item, and the test result recording
    position; and the charging positions
    completed_evaluations_charged, charging_form, and
    charged_under_the_standing_charging_rules. On
    firing it also carries test_result, standing at
    the holdout content found wording, and
    refusal_form, standing at cross split audit
    refusal; where not fired, test_result and
    refusal_form stand at None. The occasion stands at
    candidate construction or promotion; an occasion
    outside those two raises ValueError. Where
    after_partial_scoring stands True on a firing
    case, completed_evaluations_charged stands at 1
    and charging_form stands at the standing charging
    form for a refusal after partial scoring; on every
    other case the charge stands at 0 and
    charging_form stands at None.
    """
    if occasion not in ("candidate construction", "promotion"):
        raise ValueError(
            "unknown instruction test occasion: %r" % (occasion,)
        )
    text = _instruction_text_of(instruction_text)
    holdout_items = _holdout_items_of(holdout_material)
    firing_pairs = []
    verbatim = False
    comparisons = 0
    for hold_pos, holdout_item in enumerate(holdout_items):
        hold_text = _item_fields(holdout_item)["text"]
        if not text or not hold_text:
            continue
        comparisons += 1
        if str(text) == str(hold_text):
            verbatim = True
            firing_pairs.append(
                {
                    "candidate_position": 0,
                    "holdout_position": hold_pos,
                    "relations": ["near verbatim cluster"],
                }
            )
        elif _text_overlap(text, hold_text) >= _NEAR_VERBATIM_OVERLAP:
            firing_pairs.append(
                {
                    "candidate_position": 0,
                    "holdout_position": hold_pos,
                    "relations": ["near verbatim cluster"],
                }
            )
    bundle = {
        "comparisons": comparisons,
        "cost_units": comparisons * _COST_WEIGHT_PER_PAIR,
        "firing_pairs": firing_pairs,
    }
    record_home = (
        "Promotion Record"
        if occasion == "promotion"
        else "evaluation record"
    )
    base = {
        "instruction_text": text,
        "verbatim": verbatim,
        "field_scope": "instruction text field",
        "wider_material_compared": False,
        "comparisons": comparisons,
        "firing_pairs": firing_pairs,
    }
    if not firing_pairs:
        result = dict(base)
        result.update(
            {
                "fired": False,
                "fired_item": None,
                "test_result": None,
                "refusal_form": None,
                "cross_split_audit_result": _clearance(
                    record_home, False, bundle
                ),
                "audit_record": {
                    "home": _AUDIT_RECORD_HOME,
                    "fired_item": None,
                    "test_result_recorded": False,
                    "test_result": None,
                },
                "completed_evaluations_charged": 0,
                "charging_form": None,
                "charged_under_the_standing_charging_rules": False,
            }
        )
        return result
    scored = bool(after_partial_scoring)
    result = dict(base)
    result.update(
        {
            "fired": True,
            "fired_item": text,
            "test_result": _INSTRUCTION_TEST_RESULT,
            "refusal_form": "cross split audit refusal",
            "cross_split_audit_result": _refusal(
                record_home, scored, bundle
            ),
            "audit_record": {
                "home": _AUDIT_RECORD_HOME,
                "fired_item": text,
                "test_result_recorded": True,
                "test_result": _INSTRUCTION_TEST_RESULT,
            },
            "completed_evaluations_charged": _charged(scored),
            "charging_form": (
                _CHARGING_FORM_AFTER_PARTIAL_SCORING if scored else None
            ),
            "charged_under_the_standing_charging_rules": scored,
        }
    )
    return result


def audit_instruction_item(
    instruction_text,
    holdout_material,
    occasion="candidate construction",
    after_partial_scoring=False,
):
    """Return the instruction item firing outcome, plan 19.86.

    The decision act stands at _audit_instruction_item_impl.
    A text form standing in the shared recursive reading
    that recurses past the interpreter limit, a deeply
    nested form or a cyclic form among them, returns the
    governed refusal form of this surface in the
    S15-R4-N03 stated form, marked on the return under
    text_form_refused, with no exception escaping and no
    clearance issued on material never compared.
    """
    try:
        return _audit_instruction_item_impl(
            instruction_text,
            holdout_material,
            occasion=occasion,
            after_partial_scoring=after_partial_scoring,
        )
    except RecursionError:
        record_home = (
            "Promotion Record"
            if occasion == "promotion"
            else "evaluation record"
        )
        bundle = {
            "comparisons": 0,
            "cost_units": 0,
            "firing_pairs": [],
            "typed_reason": _PRESENTATION_REASON,
        }
        return {
            "instruction_text": None,
            "verbatim": False,
            "field_scope": "instruction text field",
            "wider_material_compared": False,
            "comparisons": 0,
            "firing_pairs": [],
            "fired": True,
            "fired_item": None,
            "test_result": _INSTRUCTION_TEST_RESULT,
            "refusal_form": "cross split audit refusal",
            "text_form_refused": True,
            "cross_split_audit_result": _refusal(
                record_home, False, bundle
            ),
            "audit_record": {
                "home": _AUDIT_RECORD_HOME,
                "fired_item": None,
                "test_result_recorded": False,
                "test_result": None,
            },
            "completed_evaluations_charged": 0,
            "charging_form": None,
            "charged_under_the_standing_charging_rules": False,
        }


def audit_at_build(material, scored_before_refusal=None):
    """Return the cross split audit outcome at dataset build.

    On flagged material the candidate bundle is
    refused, no promotion proceeds on it, and the
    evaluation stands recorded as not scored with its
    typed reason, on the evaluation record. The
    charging form stands at one completed evaluation
    where a case was scored before the refusal and at
    no completed evaluation where none was scored.
    """
    flagged, bundle = _audit(material, scored_before_refusal)
    if flagged:
        return _refusal("evaluation record", scored_before_refusal, bundle)
    return _clearance("evaluation record", scored_before_refusal, bundle)


def audit_at_evaluation(material, scored_before_refusal=None):
    """Return the cross split audit outcome at evaluation.

    The refusal form and the charging form stand as at
    the build call point, on the evaluation record.
    """
    flagged, bundle = _audit(material, scored_before_refusal)
    if flagged:
        return _refusal("evaluation record", scored_before_refusal, bundle)
    return _clearance("evaluation record", scored_before_refusal, bundle)


def audit_at_promotion(material, scored_before_refusal=None):
    """Return the cross split audit outcome at promotion.

    On flagged material the candidate bundle is
    refused, no promotion proceeds on it, and the
    refusal stands recorded on the Promotion Record.
    The charging form stands as at the other call
    points. A candidate or holdout side standing in a
    form the partitioning act does not read, a single
    mapping or a bare string among them, returns this
    same refusal form at every bundle call point, with
    no comparisons counted for items never partitioned.
    Material standing in the items position or the pairs
    position in a form that act does not read, a mapping
    or a bare string among them, returns the same refusal
    form in the same way.
    """
    flagged, bundle = _audit(material, scored_before_refusal)
    if flagged:
        return _refusal("Promotion Record", scored_before_refusal, bundle)
    result = _clearance("Promotion Record", scored_before_refusal, bundle)
    return result


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
