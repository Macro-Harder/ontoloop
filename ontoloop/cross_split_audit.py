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
    materialised values. A deque, a UserList, and a
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
        if current_kind == "mapping":
            keys = list(current.keys())
            children = [inner for _key, inner in current.items()]
        elif current_kind == "dictionary view" and isinstance(
            current, _ItemsView
        ):
            keys = [key for key, _inner in current]
            children = [inner for _key, inner in current]
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


def _enumerate_carried(element):
    """Return the item an enumerate index pair carries.

    An element standing as a two element list or tuple
    with an integer standing in first place stands as an
    index pair an enumerate object yields, and the item
    it carries stands in second place. Index pairs
    standing nested, as a further enumerate layer yields
    them, stand stripped in the same way until no index
    pair stands. Any other element stands as it stands.
    """
    while (
        isinstance(element, (list, tuple))
        and len(element) == 2
        and isinstance(element[0], int)
    ):
        element = element[1]
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
    standing read for the pairs that view carries. Listed
    elements still standing as enumerate index pairs, as
    a further enumerate layer standing inside the
    position yields them, stand stripped to the pair
    each one carries. Any other partitionable form
    stands listed in the standing position reading, and
    a value standing in no such form returns None.
    """
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
        for _key, inner in value:
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
    escaping.
    """
    if _is_bundle(material):
        try:
            bundle = _audit_bundle(material)
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
            if _pair_elements(pair) is not None:
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
    reading extracts from it. A bundle carrying no
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
    elif _is_partitionable_form(pairs):
        candidates = list(pairs)
        if any(hasattr(pair, "__next__") for pair in candidates):
            listed = candidates
    if listed is None:
        return material
    new_pairs = []
    for pair in listed:
        if isinstance(pair, enumerate):
            new_pairs.append(
                [
                    _enumerate_carried(element)
                    for element in list(pair)
                ]
            )
        elif hasattr(pair, "__next__"):
            new_pairs.append(list(pair))
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


def _mapping_position_values(value):
    """Return the values a mapping bundle position carries.

    A mapping standing at a bundle position and carrying
    no item field of its own stands as a container of
    items, and the items it carries stand in its values,
    in parity with the generic mapping reading the
    direct act gives that same mapping at its top level.
    A mapping carrying an item field stands as the one
    item it stands as, and returns None here.
    """
    if isinstance(value, _Mapping) and not any(
        key in value for key in _ITEM_FIELD_KEYS
    ):
        return list(value.values())
    return None


def _mapping_position_material(values):
    """Expand mapping values carrying material in their values.

    A value standing as a mapping carrying no item field
    of its own and standing as no pair in its own right
    stands read for the material its own values carry, in
    the same reading its position receives, at any depth
    the presentation nests it. A value standing as a list
    or a tuple stands read in the same way for the
    elements it carries. Any other value stands as it
    stands.
    """
    expanded = []
    for value in values:
        if isinstance(value, _Mapping) and not any(
            key in value for key in _ITEM_FIELD_KEYS
        ) and _pair_elements(value) is None:
            expanded.extend(
                _mapping_position_material(list(value.values()))
            )
        elif isinstance(value, (list, tuple)) and any(
            isinstance(element, _Mapping)
            and not any(
                key in element for key in _ITEM_FIELD_KEYS
            )
            and _pair_elements(element) is None
            for element in value
        ):
            expanded.append(
                _mapping_position_material(list(value))
            )
        else:
            expanded.append(value)
    return expanded


def _single_pair_sides(value):
    """Return the two sides a single pair position value carries.

    A pairs position value standing as a single pair
    stands read through the pair reading for the sides it
    carries. A value standing as a dictionary items view
    or values view, whose pair reading stands in no pair
    form, stands read for the two values it views, and a
    value standing in a container form that iterates by
    indexed access alone stands read for the two elements
    its indexed access yields, in the same form.
    """
    if isinstance(value, _ItemsView):
        carried = [
            _enumerate_carried(inner) for _key, inner in value
        ]
        if len(carried) == 2:
            return carried[0], carried[1]
        return None
    if isinstance(value, _ValuesView):
        listed = list(value)
        if len(listed) == 2:
            return listed[0], listed[1]
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
        return None
    return _pair_elements(value)


def _direct_bundle_extra_holdout(bundle):
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
    the set carrying no order between them.
    """
    extra = []
    for key in ("holdout_items", "holdout"):
        if key in bundle:
            value = bundle[key]
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
    if "pairs" in bundle:
        value = bundle["pairs"]
        if value is not None:
            values = _mapping_position_values(value)
            if isinstance(value, _Mapping) and (
                _pair_elements(value) is not None
            ):
                sides = _pair_elements(value)
                extra.extend(_unwrapped_items(sides[1]))
            elif values is not None:
                for element in _mapping_position_material(values):
                    sides = _pair_elements(element)
                    if sides is not None:
                        extra.extend(_unwrapped_items(sides[1]))
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
                        if isinstance(value, _Set):
                            extra.extend(
                                _unwrapped_items(sides[0])
                            )
                        extra.extend(_unwrapped_items(sides[1]))
    return extra


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
            holdout_material = _materialised_pairs_material(
                holdout_material
            )
            candidate, holdout = _split_items(holdout_material)
            return holdout + _direct_bundle_extra_holdout(
                holdout_material
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
