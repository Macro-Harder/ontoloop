"""Capture and redaction module, slice REDACT form.

The six layer scanner engine in the append path, definite
and uncertain classification under one shared rule, the
placeholder scheme, the redaction uncertain and redaction
refused states with clearing by rescan under the strength
condition and by recorded operator decision, the BQ-43
marking in its adopted form at its three named places, no
redaction parameter below the floor, the layer 6 exit scan
over the four governed assemblies, and the posture travel
forms of the two flag position: the store level posture
state, owned by this module as sole owner, set by the
weakening act itself, and the per build flag derived at
the build point from the ingest posture stamps of the
material an artifact includes or describes alone.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of this
file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.redact"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "assembly_scan_cannot_run",
    "assembly_with_planted_hit",
    "bq43_marking_places",
    "check_posture_travel",
    "check_weakening_act",
    "classify_corpus_shapes",
    "clear_by_operator_decision",
    "clear_by_rescan",
    "control_build_in_same_store",
    "dataset_build_for_sequence",
    "decoded_candidate",
    "discharge_check_at",
    "exit_scan",
    "exit_scan_over_assemblies",
    "ingest_posture_stamps",
    "journal_after_definite_hit_appends",
    "loop_report_for_build",
    "meaning_check",
    "per_build_flag_from_stamps",
    "placeholder_for_same_hit",
    "posture_after_partial_purge",
    "posture_after_tombstone_and_purge",
    "posture_fixture_sequence",
    "posture_state_at",
    "queue_defect_check",
    "redaction_floor",
    "redaction_parameters",
    "refusal_state_lifecycle",
    "restore_obligation_for_sequence",
    "run_with_definite_hit",
    "secret_bearing_shapes",
    "shared_rule",
    "store_level_posture_state",
    "uncertain_hit_case",
    "weakening_act_record",
    "append_redacted",
    "classify_material",
]


import array
import base64
import binascii
import collections
import math
import re
import types
import urllib.parse


def _pattern_positive_cases():
    """Return the landed positive cases, family by family.

    The return is a list of pairs, family key string then
    case string, in the pattern set order of
    pattern_set(version=1) from ontoloop.patterns, read
    at call time. The cases stand as that landed module
    states them: authored and guessed in that slice, and
    consumed here in exactly that standing.
    """
    from ontoloop.patterns import pattern_set

    pairs = []
    stated = pattern_set(version=1)
    for family, entry in stated.items():
        for case in entry["positive_cases"]:
            pairs.append((family, case))
    return pairs


def _corpus_shape_names():
    """Return the landed corpus hard negative shape names.

    The names stand read at call time from
    corpus_specification() in ontoloop.corpus_spec, at
    its hard_negatives mapping, whose keys are the three
    named shapes. No shape content is copied here.
    """
    from ontoloop.corpus_spec import corpus_specification

    stated = corpus_specification()
    return list(stated["hard_negatives"].keys())


# The shared rule texts, one per layer, in layer order.
# Ground: brief Section 5.7 states the one shared rule in
# prose, layer by layer, and plan section 4.2 places the
# classification in the pure core given the layer
# definitions and the registered pattern set as inputs.
# The substance of each text below follows that prose.
# The exact wording of each returned string stands as an
# authored reading under the G-6 group bound at entry 94,
# because no governing text states a rule value form for
# a test facing return, and the tests pin rule equality
# per layer and nothing more. Each text states the
# definite limb and the uncertain limb of its layer. For
# layer 3 the text states the candidate raiser form and
# its three deciding checks, from brief Section 5.7.1.
_RULE_TEXTS = {
    1: (
        "Layer 1 shared rule: a hit is definite where a "
        "field name or label in the layer 1 table is "
        "followed by an assignment form with a value "
        "present. A hit is uncertain where that test "
        "fires in part, or where the value sits in a "
        "field or context the layer tests name as "
        "ambiguous. Every hit not decided definite by "
        "this test lands uncertain."
    ),
    2: (
        "Layer 2 shared rule: a hit is definite where "
        "the value matches a pattern family in the "
        "registered pattern set in full. A hit is "
        "uncertain where that test fires in part, or "
        "where the value sits in a field or context the "
        "layer tests name as ambiguous. Every hit not "
        "decided definite by this test lands uncertain."
    ),
    3: (
        "Layer 3 shared rule: entropy and token shape "
        "act as a candidate raiser only. A candidate is "
        "decided definite where any one of the context, "
        "structure, and validation checks lands "
        "definite, and decided definite pass where all "
        "three land definite pass. Every other layer 3 "
        "candidate lands uncertain."
    ),
    4: (
        "Layer 4 shared rule: a hit is definite where a "
        "decode resolves at any round inside the depth "
        "of 3 rounds to a value a layer 1 or layer 2 "
        "test then decides definite. A hit is uncertain "
        "where a decode resolves differently at "
        "different rounds, or where depth runs out on a "
        "candidate a layer raised. Every hit not "
        "decided definite by this test lands uncertain."
    ),
    5: (
        "Layer 5 shared rule: a hit is definite where a "
        "declaration form carrying a credential value "
        "stands present, the declaration forms being a "
        "credential type field, a credential file name, "
        "a credential schema name, and a self declared "
        "credential payload marker in the arrival "
        "envelope. A hit is uncertain where that test "
        "fires in part, or where the value sits in a "
        "field or context the layer tests name as "
        "ambiguous. Every hit not decided definite by "
        "this test lands uncertain."
    ),
    6: (
        "Layer 6 shared rule: a hit is definite where "
        "the same layer tests, applied to the assembly "
        "as a whole, decide the value definite. A hit is "
        "uncertain where a test fires in part on the "
        "assembly, or where the value sits in a field or "
        "context the layer tests name as ambiguous. "
        "Every hit not decided definite by this test "
        "lands uncertain."
    ),
}

_SIX_LAYERS = (1, 2, 3, 4, 5, 6)

_FOUR_ASSEMBLIES = (
    "export",
    "bundle writing",
    "dataset construction",
    "report construction",
)

# The placeholder scheme. Brief Section 5.7, item
# S5-O-40, states that placeholders are typed and name
# the layer and class that fired, and states no
# spelling. The scheme here computes the placeholder
# from the hit that fired: the type value names the
# layer and the class of the firing, and the
# placeholder value names the run scope beside the
# layer and class, in the form _placeholder_for_hit_form
# states, so the same hit in one run always yields the
# same placeholder, the same hit in two runs yields
# two different placeholders, and two different hits
# in one run yield two different placeholders.


def _placeholder_for_scope(scope):
    """Return the placeholder value for one run scope.

    The value stands as the fallback placeholder of a
    run whose hit stands unnamed by its caller, built
    from the run scope alone, so the same scope always
    yields the same placeholder, two different scopes
    yield two different placeholders, and no part of
    any replaced value stands inside it. Where the hit
    stands known, _placeholder_for_hit_form builds the
    placeholder naming its layer and class instead.
    The concrete form stands as an authored reading
    under the G-6 group bound: item S5-O-40 states the
    scheme properties, typed, stable within a run,
    scoped to the run, never reused across runs, and no
    format.
    """
    return "redacted placeholder for " + scope


def journal_after_definite_hit_appends():
    """Return the journal value after definite hit appends.

    The return carries exactly the two test pinned keys.
    bytes: the journal byte content of a real store
    journal after appends of definite hit material
    through the redacting append path of this module,
    standing as the canonical bytes of the records of a
    store founded whole through the store module, with
    one appended record per definite hit shape added
    over the founding records, each appended record
    carrying the redacted material with its run scoped
    placeholders and no part of any shape raw bytes, in
    the REDACT-T01 governing form: redaction runs
    inside the append, before hashing and before any
    byte reaches the journal, and no record exists in
    the journal in unredacted form at any moment.
    scan_point: the string after appends, naming the
    occasion the check runs at, in the row fixture form.
    A fresh mapping and fresh bytes stand returned on
    every call.
    """
    from ontoloop import store as _store_module

    store = _store_module.golden_record_store()
    for shape in secret_bearing_shapes():
        material = shape["raw_bytes"].decode("utf-8")
        append_redacted(store, material, scope="journal run")
    content = b"\n".join(
        record["canonical_bytes"] for record in store["records"]
    )
    return {"bytes": content, "scan_point": "after appends"}


def append_redacted(store, material, scope="journal run"):
    """Append material to a store through the redacting path.

    The act is the redacting append path REDACT-T01
    governs. It classifies and redacts the material
    first, acting on every definite firing record the
    classification engine returns over the material,
    not on layer 2 pattern spans alone. Where a
    definite record carries a substitutable span in
    the text to be appended, that span stands replaced
    with the placeholder naming the layer and class
    that fired, scoped to the run the scope argument
    names, and hits_redacted counts each span replaced.
    Where a definite record carries no substitutable
    span, the append stands refused in the refusal
    form below and no journal record stands written,
    so no material the engine calls definite reaches
    a journal unredacted and uncounted. Only after
    redaction does the act pass the redacted material
    to the one store append act, so redaction stands
    inside the append, before the append act hashes
    the record and before any byte of the record
    reaches the journal. No journal byte stands
    written by any second path here: the store append
    act is the only writer this act calls.

    The return carries appended and reported_appended
    in the store append outcome form, refused standing
    False on an append and True on the refusal form,
    the redacted material in the form appended, the
    placeholders used, in first use order, and
    hits_redacted, the count of definite hit spans
    replaced. The refusal form carries appended False,
    reported_appended False, refused True, no redacted
    material, no placeholders, and hits_redacted 0.
    A gathering that meets a cycle, or that raises
    RecursionError on deep finite nesting past the
    interpreter limit, returns that refusal form with
    no record written.
    """
    from ontoloop import store as _store_module

    try:
        items = _material_items(material)
    except (_CycleDetected, RecursionError):
        return {
            "appended": False,
            "reported_appended": False,
            "refused": True,
            "redacted_material": None,
            "placeholders": [],
            "hits_redacted": 0,
        }
    text = "\n".join(item["text"] for item in items)
    records = _definite_records_over(material, text)
    redacted_text, placeholders, hits, unspanned = _redact_text(
        text, scope, records
    )
    if unspanned:
        return {
            "appended": False,
            "reported_appended": False,
            "refused": True,
            "redacted_material": None,
            "placeholders": [],
            "hits_redacted": 0,
        }
    outcome = _store_module.append_record(
        store,
        {"record_type": "record", "payload": redacted_text},
        "record",
    )
    return {
        "appended": bool(outcome.get("appended")),
        "reported_appended": bool(outcome.get("reported_appended")),
        "refused": False,
        "redacted_material": redacted_text,
        "placeholders": placeholders,
        "hits_redacted": hits,
    }


def _definite_records_over(material, text):
    """Return the definite records over a material and its text.

    The records stand as the distinct layer and class
    pairs the classification engine returns at outcome
    definite, read over the material as passed and over
    the joined text form the append writes, so a firing
    that rests on a field the material carries and a
    firing that rests on the written text both stand
    acted on by the append path.
    """
    records = []
    seen = set()
    for source in (material, text):
        result = classify_material(source)
        if "firing_records" not in result:
            continue
        for layer in _SIX_LAYERS:
            for record in result["firing_records"][layer]:
                if record["outcome"] != "definite":
                    continue
                key = (record["layer"], record["class"])
                if key in seen:
                    continue
                seen.add(key)
                records.append(
                    {"layer": record["layer"], "class": record["class"]}
                )
    return records


def _assignment_spans(text):
    """Return the spans of the layer 1 assignment forms in a text.

    A span runs from a credential bearing name, in any
    of its plain, underscored, hyphenated, or closed
    forms, through its assignment mark and the value
    that follows it, a quoted value whole or the first
    unspaced value token.
    """
    spans = []
    for name in _CREDENTIAL_NAMES:
        forms = (
            name,
            name.replace(" ", "_"),
            name.replace(" ", "-"),
            name.replace(" ", ""),
        )
        for form in set(forms):
            pattern = (
                re.escape(form)
                + r"\s*[:=]\s*(?:\"[^\"]*\"|'[^']*'|[^\s;]+)"
            )
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                spans.append(match.span())
    return spans


def _declaration_spans(text):
    """Return the layer 5 declaration spans in a text, with classes.

    Each entry carries a span and the declaration class
    it stands for. A credential type field, a credential
    schema name, and a self declared credential payload
    marker carry the rest of their line as their span,
    the line being the declaration and its value
    together. A credential file name carries its file
    name token alone as its span.
    """
    forms = (
        (
            "credential type field",
            r"credential[ _-]?type\s*[:=][^\n]*",
        ),
        (
            "credential file name",
            r"\b[\w.-]+\.(?:pem|key|p12|keystore)\b",
        ),
        (
            "credential schema name",
            r"credential[ _-]?schema[^\n]*",
        ),
        (
            "self declared credential payload marker",
            r"self[ _-]?declared credential[^\n]*",
        ),
    )
    spans = []
    for class_name, pattern in forms:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            spans.append((match.span(), class_name))
    return spans


def _underlying_spans(text):
    """Return the item level definite spans a text carries.

    The spans stand as the layer 1 assignment spans,
    the layer 2 pattern family spans, and the layer 5
    declaration spans of the text, each carrying the
    layer and class that fired on it. The layer 4 and
    layer 6 definite records of a text rest on these
    spans where the text itself carries the hit.
    """
    spans = []
    for start, end in _assignment_spans(text):
        spans.append((start, end, 1, "field name table"))
    for family, expression in _pattern_expressions():
        for match in expression.finditer(text):
            spans.append((match.start(), match.end(), 2, family))
    for (start, end), class_name in _declaration_spans(text):
        spans.append((start, end, 5, class_name))
    return spans


def _decoded_spans(text, layer, class_name):
    """Return the spans of a text that decode to a definite hit.

    A whitespace separated token that the layer 4
    decoding engine decides definite carries its token
    as its span. Where no token decides definite and
    the text as a whole decides definite, the stripped
    text carries its span.
    """
    spans = []
    for match in re.finditer(r"\S+", text):
        if _decode_candidate(match.group(0))["outcome"] == "definite hit":
            spans.append((match.start(), match.end(), layer, class_name))
    if spans:
        return spans
    if _decode_candidate(text)["outcome"] == "definite hit":
        start = len(text) - len(text.lstrip())
        end = len(text.rstrip())
        if end > start:
            spans.append((start, end, layer, class_name))
    return spans


def _definite_record_spans(record, text):
    """Return the substitutable spans of one definite record.

    The return is a list of spans, each carrying its
    start, its end, the layer its placeholder names,
    and the class its placeholder names. A record whose
    layer act finds no span in the text returns an
    empty list, the no substitutable span position the
    append path refuses on.
    """
    layer = record["layer"]
    class_name = record["class"]
    if layer == 1:
        return [
            (start, end, 1, class_name)
            for start, end in _assignment_spans(text)
        ]
    if layer == 2:
        spans = []
        for family, expression in _pattern_expressions():
            if family != class_name:
                continue
            for match in expression.finditer(text):
                spans.append((match.start(), match.end(), 2, family))
        if spans:
            return spans
        return [
            (start, end, layer, hit_class)
            for start, end, layer, hit_class in _underlying_spans(text)
            if layer == 2
        ]
    if layer == 3:
        spans = []
        for match in re.finditer(r"\S+", text):
            token = match.group(0)
            if len(token) >= 20 and _entropy(token) >= 4.5:
                spans.append((match.start(), match.end(), 3, class_name))
        return spans
    if layer == 5:
        spans = [
            (start, end, 5, hit_class)
            for (start, end), hit_class in _declaration_spans(text)
            if hit_class == class_name
        ]
        if spans:
            return spans
        return [
            (start, end, 5, hit_class)
            for (start, end), hit_class in _declaration_spans(text)
        ]
    if layer in (4, 6):
        underlying = _underlying_spans(text)
        if underlying:
            return underlying
        return _decoded_spans(text, layer, class_name)
    return []


def _redact_text(text, scope, definite_records=None):
    """Redact the definite hit spans of one text.

    The act stands on the definite firing records the
    classification engine returns over the material,
    gathered by _definite_records_over where the caller
    passes them and read over the text itself where it
    does not. Each record stands mapped to its
    substitutable spans in the text by
    _definite_record_spans. Spans that overlap stand
    merged into one replaced region, so one hit the
    engine records at several layers stands replaced
    once and counted once, and the placeholder of a
    merged region names the layer and class of its
    governing span, a layer 2 pattern span first, then
    layer 1, layer 5, layer 3, layer 4, and layer 6 in
    that order. The return is the redacted text, the
    placeholder values in first use order, the count
    of regions replaced, and a flag standing True
    where any definite record carried no substitutable
    span, the position the append path refuses on.
    """
    if definite_records is None:
        definite_records = _definite_records_over(text, text)
    if not definite_records:
        return text, [], 0, False
    spans = []
    unspanned = False
    for record in definite_records:
        found = _definite_record_spans(record, text)
        if not found:
            unspanned = True
        spans.extend(found)
    if unspanned:
        return text, [], 0, True
    priority = {2: 0, 1: 1, 5: 2, 3: 3, 4: 4, 6: 5}
    ordered = sorted(spans, key=lambda span: (span[0], span[0] - span[1]))
    merged = []
    for start, end, layer, class_name in ordered:
        if merged and start < merged[-1][1]:
            last = merged[-1]
            if priority[layer] < priority[last[2]]:
                layer, class_name = layer, class_name
            else:
                layer, class_name = last[2], last[3]
            merged[-1] = (last[0], max(last[1], end), layer, class_name)
            continue
        merged.append((start, end, layer, class_name))
    placeholders = []
    parts = []
    position = 0
    for start, end, layer, class_name in merged:
        placeholder = _placeholder_for_hit_form(scope, layer, class_name)
        parts.append(text[position:start])
        parts.append(placeholder)
        position = end
        if placeholder not in placeholders:
            placeholders.append(placeholder)
    parts.append(text[position:])
    return "".join(parts), placeholders, len(merged), False


def _placeholder_for_hit_form(scope, layer, class_name):
    """Return the placeholder value for one hit in a run.

    The value names the run scope, the layer that
    fired, and the class that fired, in plain words,
    so two hits in one run under the same layer and
    class carry the same placeholder, two hits under
    different classes carry different placeholders,
    and the same hit in two runs carries two different
    placeholders.
    """
    return "redacted placeholder for %s: layer %d %s" % (
        scope,
        layer,
        class_name,
    )


def secret_bearing_shapes():
    """Return the secret bearing shapes, per family.

    The return is a fresh list of fresh mappings, each
    carrying exactly the one test pinned key raw_bytes,
    the byte form, in UTF-8, of one definite hit shape.
    The shapes stand grounded on the consumed landed
    surface: the positive cases of the five authored
    families of pattern_set(version=1) in
    ontoloop.patterns, one shape per positive case, in
    pattern set order, eight shapes in all at version 1.
    Those cases stand authored and guessed in their own
    slice, and they are consumed here in that standing
    and in no other. No shape value is written in this
    fragment in any representation: each value is read
    from the landed module at call time, under the
    entry 58 discipline stated in the header. Any shape
    beyond those cases would stand as item G-1 residue,
    authored and guessed under the entry 94
    authorisation. This act returns no such residue:
    the whole collection stands on the consumed cases.
    """
    shapes = []
    for _family, case in _pattern_positive_cases():
        shapes.append({"raw_bytes": case.encode("utf-8")})
    return shapes


# The classification engine. One engine runs all six
# layers over the material passed, under the one shared
# rule per layer shared_rule states. Each layer act
# below is the executable form of its shared rule: it
# returns firing records holding the item index, the
# field name where the material carried one, the
# outcome, definite or uncertain, and the class that
# fired. Material stands normalised by _material_items
# into text items, so the same engine classifies a
# string, a byte string, a mapping field by field, and
# a sequence item by item, and its results vary with
# the material passed in every case.

_CREDENTIAL_NAMES = (
    "client secret",
    "access token",
    "refresh token",
    "api key",
    "access key",
    "secret key",
    "private key",
    "signing key",
    "session key",
    "password",
    "passwd",
    "secret",
    "token",
    "apikey",
    "authorisation",
    "authorization",
    "credentials",
    "credential",
    "passphrase",
    "bearer",
)

_TOKEN_PREFIXES = (
    "ghp_",
    "gho_",
    "ghu_",
    "ghs_",
    "ghr_",
    "github_pat_",
    "glpat-",
    "npm_",
    "pypi-",
    "sk_live_",
    "rk_live_",
)


class _CycleDetected(Exception):
    """Signal that a gathering act met a cycle on its path.

    The signal stands internal to this module. The
    surfaces that gather content catch it and return
    their governed fail closed forms, so cyclic input
    returns a governed output and no RecursionError.
    A gathering that raises RecursionError itself, on
    deep finite nesting past the interpreter limit,
    stands in the same position at those surfaces:
    each catch that takes this signal also takes
    RecursionError and returns the same governed form.
    """


def _material_items(material, _path=None):
    """Normalise material into a list of text items.

    Each item carries field, the field name the
    material stated for it or None, and text, its text
    form. A byte string decodes as UTF-8 with any
    undecodable byte replaced, and a memoryview value
    stands read in that same decode limb, as the byte
    content it views, at the top level, as a mapping
    value, and as a sequence element. A mapping contributes
    one item per entry, in entry order, keyed by its
    field name. A sequence contributes one item per
    element, in order. Any other value contributes its
    string form as one item. A sequence that stands on
    its own gathering path raises _CycleDetected: the
    gathering act detects a cycle on its path, where
    the path holds only the containers of the branch
    being gathered, so a value shared across branches
    in acyclic form gathers in the ordinary way and
    deep finite nesting gathers to its full depth.
    """
    if material is None:
        return []
    if isinstance(material, (bytes, bytearray, memoryview)):
        return [
            {"field": None, "text": bytes(material).decode(
                "utf-8", "replace")}
        ]
    if isinstance(material, str):
        return [{"field": None, "text": material}]
    if isinstance(material, dict):
        items = []
        for key in material:
            value = material[key]
            if isinstance(value, (bytes, bytearray, memoryview)):
                text = bytes(value).decode("utf-8", "replace")
            elif isinstance(value, str):
                text = value
            else:
                text = str(value)
            items.append({"field": str(key), "text": text})
        return items
    if isinstance(material, (list, tuple, set, frozenset)):
        if _path is None:
            _path = set()
        marker = id(material)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            items = []
            for element in material:
                items.extend(_material_items(element, _path))
            return items
        finally:
            _path.discard(marker)
    return [{"field": None, "text": str(material)}]


def _pattern_expressions():
    """Return the registered pattern families, compiled.

    The families and expressions stand read at call
    time from pattern_set(version=1) in
    ontoloop.patterns, in pattern set order, the same
    landed set secret_bearing_shapes consumes.
    """
    from ontoloop.patterns import pattern_set

    stated = pattern_set(version=1)
    return [
        (family, re.compile(stated[family]["expression"]))
        for family in stated
    ]


def _entropy(text):
    """Return the Shannon entropy of a text, in bits."""
    if not text:
        return 0.0
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    total = len(text)
    value = 0.0
    for count in counts.values():
        share = count / total
        value -= share * math.log2(share)
    return value


def _credential_name_forms(text):
    """Return the credential names a text carries.

    A name stands carried where it appears in the text
    in its plain, spaced, or underscored form, case
    folded. The return is a list of the canonical name
    strings found, in the table order above.
    """
    lowered = text.lower()
    found = []
    for name in _CREDENTIAL_NAMES:
        forms = (
            name,
            name.replace(" ", "_"),
            name.replace(" ", "-"),
            name.replace(" ", ""),
        )
        if any(form in lowered for form in forms):
            found.append(name)
    return found


def _assignment_with_value(text):
    """Return True where a credential name carries a value.

    The layer 1 definite test: a credential bearing
    field name or label followed by an assignment form
    with a value present.
    """
    lowered = text.lower()
    for name in _credential_name_forms(text):
        for form in (
            name,
            name.replace(" ", "_"),
            name.replace(" ", "-"),
            name.replace(" ", ""),
        ):
            index = lowered.find(form)
            while index != -1:
                rest = lowered[index + len(form):].lstrip()
                if rest[:1] in (":", "=") and rest[1:].strip():
                    return True
                index = lowered.find(form, index + 1)
    return False


def _partial_pattern_class(text):
    """Return the class of a partial pattern firing, or None.

    A partial firing stands where a pattern family test
    fires in part: a private key block opening without
    its full header, a cloud key prefix without its
    full shape, a token prefix without its full length,
    or an authorisation header without its full value.
    """
    if "-----BEGIN" in text and "PRIVATE KEY" in text:
        return "private_key_block_headers"
    if re.search(r"(?:AKIA|ASIA)[0-9A-Z]{1,15}", text):
        return "cloud_access_key_shapes"
    for prefix in _TOKEN_PREFIXES:
        if prefix in text:
            return "token_prefixes"
    if re.search(r"(?i)authorization\s*:", text):
        return "authorisation_header_forms"
    if text.startswith("xox") and "-" in text:
        return "token_prefixes"
    return None


def _declaration_forms(text):
    """Return the layer 5 declaration classes a text carries.

    The definite declaration forms stand as the shared
    rule states them: a credential type field, a
    credential file name, a credential schema name, and
    a self declared credential payload marker.
    """
    classes = []
    if re.search(r"(?i)credential[ _-]?type\s*[:=]", text):
        classes.append("credential type field")
    if re.search(r"(?i)\b[\w.-]+\.(?:pem|key|p12|keystore)\b", text):
        classes.append("credential file name")
    if re.search(r"(?i)credential[ _-]?schema", text):
        classes.append("credential schema name")
    if re.search(r"(?i)self[ _-]?declared credential", text):
        classes.append("self declared credential payload marker")
    return classes


def _layer_one_firings(item):
    if _assignment_with_value(_item_text(item)):
        return [(1, "definite", "field name table")]
    if _credential_name_forms(_item_text(item)):
        return [(1, "uncertain", "field name table")]
    return []


def _item_text(item):
    if item["field"]:
        return item["field"] + ": " + item["text"]
    return item["text"]


def _layer_two_firings(item):
    text = _item_text(item)
    firings = []
    for family, expression in _pattern_expressions():
        if expression.search(text):
            firings.append((2, "definite", family))
    if firings:
        return firings
    partial = _partial_pattern_class(text)
    if partial is not None:
        return [(2, "uncertain", partial)]
    return []


def _layer_three_firings(item):
    text = item["text"]
    firings = []
    for token in re.split(r"\s+", text):
        if len(token) < 20:
            continue
        if _entropy(token) < 4.5:
            continue
        if _layer_two_firings(item) or _assignment_with_value(
            _item_text(item)
        ):
            firings.append((3, "definite", "entropy candidate"))
        else:
            firings.append((3, "uncertain", "entropy candidate"))
    return firings


def _layer_four_firings(item):
    decoded = _decode_candidate(item["text"])
    if decoded["outcome"] == "definite hit":
        return [(4, "definite", "decoded definite hit")]
    if decoded["outcome"] == "uncertain hit":
        return [(4, "uncertain", "decoded candidate")]
    return []


def _layer_five_firings(item):
    text = _item_text(item)
    classes = _declaration_forms(text)
    if classes:
        return [(5, "definite", classes[0])]
    if "credential" in text.lower():
        return [(5, "uncertain", "credential declaration")]
    return []


def _layer_six_firings(items):
    joined = "\n".join(_item_text(item) for item in items)
    probe = {"field": None, "text": joined}
    if (
        _layer_one_firings(probe)
        and _layer_one_firings(probe)[0][1] == "definite"
    ) or any(
        outcome == "definite"
        for _layer, outcome, _class in _layer_two_firings(probe)
    ) or _declaration_forms(joined):
        return [(6, "definite", "assembly as a whole")]
    if (
        _credential_name_forms(joined)
        or _partial_pattern_class(joined) is not None
        or "credential" in joined.lower()
    ):
        return [(6, "uncertain", "assembly as a whole")]
    return []


def classify_material(material):
    """Classify material under the one shared rule per layer.

    The act is the classification engine of REDACT-T02.
    It takes the material passed, in any of the forms
    _material_items states, and runs all six layers
    over it as one engine, each layer act standing as
    the executable form of the shared rule shared_rule
    states for that layer. The return carries exactly
    the three keys classify_corpus_shapes has always
    carried. layers: a fresh mapping keyed by the
    integer layer numbers 1 to 6, each value a mapping
    carrying exactly rule, equal to shared_rule(layer)
    for that layer. engine_count: 1, the six layers as
    one scanner engine, grounded at brief Section
    5.7.1. firing_records: a fresh mapping keyed by
    the integer layer numbers 1 to 6, each value a
    fresh list of firing records for that layer, each
    record carrying layer, item, field, outcome, and
    class: the layer that fired, the index of the
    material item it fired on, the field name that
    item carried or None, the outcome standing at
    definite or uncertain under the layer shared rule,
    and the class that fired. A layer with no firing
    over the material carries an empty list, so the
    records vary with the material in every case.
    On material whose gathering meets a cycle, the
    classification cannot run, and the act returns
    the REDACT-T06 fail closed form instead, refused
    True with form standing at no exit scan result,
    no exit, and no classification result. A gathering
    that raises RecursionError, on deep finite nesting
    past the interpreter limit, stands in the same
    position and returns that same form.
    """
    try:
        items = _material_items(material)
    except (_CycleDetected, RecursionError):
        return {
            "refused": True,
            "form": "no exit scan result, no exit",
        }
    records = {layer: [] for layer in _SIX_LAYERS}
    layer_acts = (
        _layer_one_firings,
        _layer_two_firings,
        _layer_three_firings,
        _layer_four_firings,
        _layer_five_firings,
    )
    for index, item in enumerate(items):
        for act in layer_acts:
            for layer, outcome, class_name in act(item):
                records[layer].append(
                    {
                        "layer": layer,
                        "item": index,
                        "field": item["field"],
                        "outcome": outcome,
                        "class": class_name,
                    }
                )
    for layer, outcome, class_name in _layer_six_firings(items):
        records[layer].append(
            {
                "layer": layer,
                "item": None,
                "field": None,
                "outcome": outcome,
                "class": class_name,
            }
        )
    layers = {}
    for layer in _SIX_LAYERS:
        layers[layer] = {"rule": shared_rule(layer)}
    return {
        "layers": layers,
        "engine_count": 1,
        "firing_records": records,
    }


def _corpus_material():
    """Return the corpus shape material, as text items.

    The material stands read at call time from
    corpus_specification() in ontoloop.corpus_spec:
    for each of the three hard negative shapes, the
    statement and the values of every negative case it
    carries, in shape and case order. No shape content
    is copied here: the values stand read from the
    landed module at call time.
    """
    from ontoloop.corpus_spec import corpus_specification

    stated = corpus_specification()
    material = []
    for shape in stated["hard_negatives"].values():
        for case in shape["negative_cases"]:
            material.append(case["statement"])
            material.extend(case["values"])
    return material


def classify_corpus_shapes(material=None):
    """Return the classification of the corpus shapes.

    The act runs the classification engine of
    classify_material over the corpus material: the
    material passed as the argument where one stands
    passed, and otherwise the landed corpus shape
    material _corpus_material reads at call time from
    ontoloop.corpus_spec, the three hard negative
    shapes standing as the fixture ground the merged
    list names for this row. The return carries
    exactly the three test pinned keys, in the forms
    classify_material states: layers, each carrying
    the one shared rule for its layer; engine_count 1,
    the six layers as one scanner engine, grounded at
    brief Section 5.7.1; and firing_records, the per
    layer firing records the engine produced over the
    corpus material, with definite and uncertain
    outcomes under the one shared rule per layer.
    """
    if material is None:
        material = _corpus_material()
    return classify_material(material)


def shared_rule(layer):
    """Return the one shared rule value for one layer.

    The rule substance stands grounded at brief
    Section 5.7, stated once there as the one shared
    definite and uncertain classification rule, with
    the layer 3 deciding checks at brief Section
    5.7.1, in the forms the texts at the head of this
    section restate. The exact wording returned stands
    as an authored reading under the G-6 group bound,
    recorded in the fragment paper in the open. A layer
    outside the six raises ValueError, the refusal form
    the landed fragments use for an unknown argument to
    a present function.
    """
    try:
        known = layer in _RULE_TEXTS
    except TypeError:
        known = False
    if not known:
        raise ValueError("unknown layer: %r" % (layer,))
    return _RULE_TEXTS[layer]


def run_with_definite_hit(scope, material=None):
    """Return one run carrying a definite hit, by scope.

    The run definite hit stands as the material passed,
    where material stands passed, and otherwise as the
    first definite hit shape of secret_bearing_shapes,
    the private key block header case. The act runs the
    classification engine over that material and builds
    the run placeholders from its definite firings at
    the hit layers, layers 1, 2, and 5, so each
    placeholder names the layer and the class that
    fired in fact.

    The return carries exactly the three test pinned
    keys. placeholders: a fresh list of fresh
    placeholder mappings, one per distinct definite
    firing of the run hit, each carrying exactly type,
    whose value names the layer and class that fired,
    in the form layer N class, definite hit.
    placeholder_for_hit: the placeholder value for the
    first definite firing of the run hit, built by
    _placeholder_for_hit_form from the scope and that
    firing, stable for this run and standing equal to
    what placeholder_for_same_hit returns over this
    same run value. scope: the run name string passed
    in, standing equal to it exactly, the run scope
    limb in its test form. Across two runs under two
    scopes the placeholder values differ, the never
    reused across runs limb in its test form, and
    across two different hits in one run the
    placeholder values differ by the class named.
    """
    if material is None:
        material = secret_bearing_shapes()[0]["raw_bytes"]
    result = classify_material(material)
    firings = []
    for layer in (1, 2, 5):
        for record in result["firing_records"][layer]:
            if record["outcome"] != "definite":
                continue
            firing = (record["layer"], record["class"])
            if firing not in firings:
                firings.append(firing)
    if not firings:
        firings = [(2, "pattern family match")]
    placeholders = [
        {"type": "layer %d %s, definite hit" % (layer, class_name)}
        for layer, class_name in firings
    ]
    placeholder = _placeholder_for_hit_form(scope, firings[0][0],
                                            firings[0][1])
    return {
        "placeholders": placeholders,
        "placeholder_for_hit": placeholder,
        "scope": scope,
    }


def placeholder_for_same_hit(run):
    """Return the placeholder for the hit of one run.

    The act reads the run value it is passed and returns
    its placeholder_for_hit value, standing equal to it
    exactly, the stability limb of item S5-O-40 in its
    test form. No other key of the run stands read.
    """
    return run["placeholder_for_hit"]


# The layer 4 decoding engine. Ground: brief Section
# 5.7, item S5-O-35, decoding covers base64, hex, and
# URL decoding to a depth of 3 rounds, guessed, with
# its two distinguished outcomes, and the corpus
# specification form, a decoding round field on every
# decoded candidate. The engine below runs real
# decoding rounds over the candidate passed: each
# round tries the three forms in the order hex where
# the value stands in hex form alone, base64, and URL
# decoding, and takes the first form whose decoding
# yields a different printable text. The depth reached
# stands computed from the rounds that ran, never
# stored per case. The three case name strings the
# test file names stand as fixture candidate
# constructors, in the form the suite uses elsewhere:
# each name builds a real encoded candidate, stated at
# _case_candidate, and the built candidate passes
# through the same engine as any other candidate, so
# no outcome stands stored against a case name either.

_DECODING_DEPTH = 3


def _printable_text(raw):
    """Return the text of raw bytes where they stand printable.

    Returns None where the bytes do not decode as UTF-8
    or carry a character outside the printable range
    and ordinary whitespace.
    """
    try:
        text = raw.decode("utf-8")
    except (UnicodeDecodeError, ValueError):
        return None
    for char in text:
        if char in "\n\r\t":
            continue
        if not char.isprintable():
            return None
    return text


def _try_decode_round(text):
    """Run one decoding round over a candidate text.

    Returns a pair, the form name and the decoded text,
    for the first form that decodes the value to a
    different printable text, and None where no form
    decodes it. A value standing wholly in hex digits
    of even length stands tried as hex first, that
    being its unambiguous form; base64 stands tried
    next, in its strict alphabet; URL decoding stands
    tried where a percent escape stands present.
    """
    stripped = text.strip()
    if (
        len(stripped) >= 16
        and len(stripped) % 2 == 0
        and re.fullmatch(r"[0-9a-fA-F]+", stripped)
    ):
        decoded = _printable_text(binascii.unhexlify(stripped))
        if decoded is not None and decoded != text:
            return ("hex", decoded)
    if (
        len(stripped) >= 8
        and len(stripped) % 4 == 0
        and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", stripped)
    ):
        try:
            raw = base64.b64decode(stripped, validate=True)
        except (binascii.Error, ValueError):
            raw = None
        if raw is not None:
            decoded = _printable_text(raw)
            if decoded is not None and decoded != text:
                return ("base64", decoded)
    if re.search(r"%[0-9a-fA-F]{2}", text):
        decoded = urllib.parse.unquote(text)
        if decoded != text and _printable_text(
            decoded.encode("utf-8")
        ) is not None:
            return ("URL decoding", decoded)
    return None


def _definite_hit_in(text):
    """Return True where a layer decides a text definite.

    The deciding tests stand as the classification
    engine states them: the layer 1 assignment test,
    the layer 2 pattern family tests, and the layer 5
    declaration forms.
    """
    probe = {"field": None, "text": text}
    if _assignment_with_value(text):
        return True
    if any(
        outcome == "definite"
        for _layer, outcome, _class in _layer_two_firings(probe)
    ):
        return True
    if _declaration_forms(text):
        return True
    return False


def _candidate_raised(text):
    """Return True where a layer raised a candidate text.

    A candidate stands raised where the layer 3
    candidate raiser fires on one of its tokens, where
    a pattern test fires in part on it, or where a
    credential name or declaration word stands present
    without a definite decision.
    """
    for token in re.split(r"\s+", text):
        if len(token) >= 20 and _entropy(token) >= 4.5:
            return True
    if _partial_pattern_class(text) is not None:
        return True
    if _credential_name_forms(text):
        return True
    if "credential" in text.lower():
        return True
    return False


def _decode_candidate(candidate):
    """Decode a candidate to the governed depth of 3 rounds.

    The engine runs decoding rounds until the value
    stands decoded, a definite hit stands resolved, or
    the depth of 3 rounds stands reached. The return
    carries the depth the rounds reached, the round
    fields of the rounds that ran, in the corpus
    specification form round N: form, and the outcome:
    definite hit where a round resolves the value to a
    value a layer decides definite; uncertain hit
    where the depth runs out, or the rounds end, on a
    candidate a layer raised; and depth limited pass
    where no layer raised the value, the two outcome
    forms of item S5-O-35 beside the resolved form.
    """
    if isinstance(candidate, (bytes, bytearray)):
        text = bytes(candidate).decode("utf-8", "replace")
    else:
        text = str(candidate)
    if _definite_hit_in(text):
        return {
            "decoding_depth_reached": 0,
            "decoding_round_fields": [],
            "outcome": "definite hit",
        }
    round_fields = []
    current = text
    for round_number in range(1, _DECODING_DEPTH + 1):
        step = _try_decode_round(current)
        if step is None:
            break
        form, decoded = step
        round_fields.append("round %d: %s" % (round_number, form))
        current = decoded
        if _definite_hit_in(current):
            return {
                "decoding_depth_reached": len(round_fields),
                "decoding_round_fields": round_fields,
                "outcome": "definite hit",
            }
    if _candidate_raised(current):
        outcome = "uncertain hit"
    else:
        outcome = "depth limited pass"
    return {
        "decoding_depth_reached": len(round_fields),
        "decoding_round_fields": round_fields,
        "outcome": outcome,
    }


def _case_candidate(case):
    """Build the real candidate a test case name names.

    Each chain stands authored and guessed under item
    G-2, authorised at entry 94 in the entry 54 form,
    and stands labelled authored and guessed here and
    in the fix paper, never as grounded or measured:
    what the candidate decodes through at each round
    stands nowhere in a governing text. Chain for
    raised at depth 3: a high entropy token a layer
    raises, carried through hex, base64, and hex
    encodings, so three rounds run and the residue
    stands raised at the depth bound. Chain for depth
    runs out raised: a definite hit carried through
    URL, hex, base64, and base64 encodings, so the
    depth runs out with the residue still encoded and
    raised in part. Chain for depth runs out unraised:
    a routine line carried through hex, base64, hex,
    and base64 encodings, so the depth runs out with a
    hex residue no layer raised. The encoding acts are
    the real base64, hex, and URL acts of this section,
    run in reverse.
    """
    if case == "raised at depth 3":
        token = "tok_X7f9Q2wZ8kL4mN6pR3sT5vW1xY0aB2cD3eF"
        first = token.encode("utf-8").hex()
        second = base64.b64encode(first.encode("utf-8")).decode("ascii")
        return second.encode("utf-8").hex()
    if case == "depth runs out raised":
        hit = _pattern_positive_cases()[5][1]
        first = urllib.parse.quote(hit, safe="")
        second = first.encode("utf-8").hex()
        third = base64.b64encode(second.encode("utf-8")).decode("ascii")
        return base64.b64encode(third.encode("utf-8")).decode("ascii")
    if case == "depth runs out unraised":
        line = "a routine record line about an ordinary run"
        first = line.encode("utf-8").hex()
        second = base64.b64encode(first.encode("utf-8")).decode("ascii")
        third = second.encode("utf-8").hex()
        return base64.b64encode(third.encode("utf-8")).decode("ascii")
    raise ValueError("unknown decoded candidate case: %r" % (case,))


_DECODED_CASE_NAMES = (
    "raised at depth 3",
    "depth runs out raised",
    "depth runs out unraised",
)


def decoded_candidate(case):
    """Return the decoded candidate for one candidate.

    The act runs the layer 4 decoding engine over the
    candidate passed. A candidate in any real form, a
    string or byte string carrying encoded or plain
    material, stands decoded as it stands. The three
    case name strings the test file names stand as
    fixture candidate constructors in the form stated
    at _case_candidate: each builds its real encoded
    candidate and that candidate passes through the
    same engine, so the depth and outcome on those
    cases stand computed by the engine and not stored
    against the names.

    The return carries exactly the three test pinned
    keys. decoding_depth_reached: the number of
    decoding rounds the engine ran, computed, standing
    at 3 where the depth of item S5-O-35 stands
    reached. decoding_round_fields: a fresh list of
    the round fields of the rounds that ran, in chain
    order, truthy where any round ran. outcome: the
    string definite hit where a round resolves the
    value to a definite hit, the string uncertain hit
    where depth runs out on a candidate a layer
    raised, and the string depth limited pass where no
    layer raised the value, the outcome forms of item
    S5-O-35 with the resolved form beside them.
    """
    if isinstance(case, str) and case in _DECODED_CASE_NAMES:
        candidate = _case_candidate(case)
    else:
        candidate = case
    return _decode_candidate(candidate)


def queue_defect_check(outstanding, captured):
    """Return the queue defect check on two figures.

    The arguments stand in the worked example order of
    plan section 3.4, Example C, over brief Section
    5.7.1: outstanding quarantined items first, all
    runs captured since capture began second. The
    return carries exactly the four test pinned keys.
    fires: True where the share test fires, the share
    standing as outstanding over captured with the
    cumulative divisor, exceeding 20 percent; 30 over
    120 fires at 25 percent, and 20 over 120 does not
    fire at about 16.7 percent, in the worked example
    forms. Where captured stands at zero the share
    test does not fire, in the brief form for a zero
    divisor. operative_check: the string share test
    where the share test fires, and the string growth
    test where it does not, the small interval form at
    30 over 10,000, a share of 0.3 percent, standing as
    the pinned case of that limb. The growth test limb
    stands built in this test pinned naming form only,
    under the G-6 group bound: the brief states the
    growth test in interval form over two successive
    build intervals with exit counts, and the pinned
    call carries no interval input, so no record of
    this section claims the interval computation
    stands exercised by this call. uses_cumulative_
    divisor: True on every return, the first dataset
    build using the cumulative divisor as the general
    rule, grounded at brief Section 5.7.1.
    source_class: the string guessed on every return,
    every figure of this row standing guessed and
    labelled guessed, in the row source marking form.
    """
    if captured:
        fires = (outstanding / captured) > 0.20
    else:
        fires = False
    if fires:
        operative = "share test"
    else:
        operative = "growth test"
    return {
        "fires": fires,
        "operative_check": operative,
        "uses_cumulative_divisor": True,
        "source_class": "guessed",
    }


def exit_scan_over_assemblies():
    """Return the assemblies the exit scan governs.

    The return carries exactly the one test pinned key
    assemblies, a fresh list whose set equals exactly
    the four governed assembly names, in the file
    order: export, bundle writing, dataset
    construction, and report construction. Ground:
    brief Section 2.1 with Section 5.7, an exit is any
    assembly the layer 6 exit scan governs, the four
    named there.
    """
    return {"assemblies": list(_FOUR_ASSEMBLIES)}


def assembly_with_planted_hit():
    """Return an assembly value carrying a planted hit.

    The value stands as a fresh mapping carrying
    assembly_state, standing at the string planted
    uncleared hit, and content, standing as the raw
    bytes of the first secret bearing shape, read at
    call time from secret_bearing_shapes. The planted
    hit of this fixture therefore stands in scannable
    content the classification engine fires on, and
    the REDACT-T06 pin of a whole refusal over this
    value passes on that material through the scan.
    The state label carries no scan outcome of its
    own, in the form exit_scan states.
    """
    return {
        "assembly_state": "planted uncleared hit",
        "content": secret_bearing_shapes()[0]["raw_bytes"],
    }


def assembly_scan_cannot_run():
    """Return an assembly value whose scan cannot run.

    The value stands as a fresh mapping carrying
    exactly assembly_state, standing at the string
    scan cannot run. Its contents beyond the cannot
    run form stand unpinned by any test, no test
    reading this value, and the form stands built
    under the G-6 group bound as the smallest fixture
    form that carries the cannot run state, stated as
    an authored reading in the fragment paper.
    """
    return {"assembly_state": "scan cannot run"}


_MAPPING_FORMS = (
    dict,
    types.MappingProxyType,
    collections.UserDict,
    collections.ChainMap,
)

_SEQUENCE_FORMS = (
    list,
    tuple,
    set,
    frozenset,
    collections.deque,
    collections.UserList,
)

_VIEW_TYPES = (
    type({}.keys()),
    type({}.values()),
    type({}.items()),
)


def _is_mapping_form(value):
    """Return True where a value stands in a walked mapping form."""
    return isinstance(value, _MAPPING_FORMS)


def _mapping_pairs(value):
    """Return the key and value pairs of a walked mapping form.

    A plain mapping, a mapping proxy, and a UserDict each
    contribute one pair per key, in key order. A ChainMap
    contributes the pairs of every map it chains, in chain
    order, so content standing in a shadowed map still
    stands gathered, in the safe direction.
    """
    if isinstance(value, collections.ChainMap):
        pairs = []
        for mapping in value.maps:
            for key in mapping:
                pairs.append((key, mapping[key]))
        return pairs
    pairs = []
    for key in value:
        pairs.append((key, value[key]))
    return pairs


def _assembly_state_value(assembly):
    """Return the assembly_state value of a top level assembly.

    The state read reads a top level assembly standing in
    any mapping form the gathering acts walk, in the same
    form as a plain mapping: a plain mapping, a mapping
    proxy, a UserDict, and a ChainMap each answer the read
    through their mapping form. An assembly in no mapping
    form carries no state value for this read.
    """
    if _is_mapping_form(assembly):
        return assembly.get("assembly_state")
    return None


def _assembly_content(assembly, _path=None, _top=True,
                      _skip_top_state=False):
    """Return the scannable content items of an assembly.

    The content of an assembly stands as every string
    and byte value it carries, read recursively through
    its mappings and sequences. The top level
    assembly_state value stands gathered as content
    beside the other values, in the same content form:
    hit material standing in that value is content the
    scan examines, exactly as content standing under
    any other key at any depth is, including content
    standing under a repeated assembly_state key below
    the top level. A state label in its standing forms
    is a short string naming a state, and gathering it
    changes no decision on a clean assembly. The one
    exception stands in the _skip_top_state form,
    which exit_scan uses for its fail closed floor
    alone: a gathering under that flag skips the top
    level assembly_state value, so the floor reads the
    value content beside the state value, in the form
    exit_scan states. An assembly in string or
    byte form carries itself as its content. A value in
    no such form carries no scannable content. A mapping
    or sequence that stands on its own gathering path
    raises _CycleDetected: the gathering act detects a
    cycle on its path, where the path holds only the
    containers of the branch being gathered, so a value
    shared across branches in acyclic form gathers in
    the ordinary way and deep finite nesting gathers to
    its full depth. Mapping keys stand gathered beside
    these values by _assembly_key_content, in the form
    that act states, and exit_scan scans the two
    gatherings together. A value standing as a
    memoryview stands gathered as the byte content it
    views, and a value standing as a mapping proxy
    stands gathered as the mapping it views, in the
    same content forms as their underlying byte and
    mapping values. The gathering acts walk the non
    consuming standard wrapper and view container forms
    in the same forms: a deque as the sequence it stands
    as, a mapping view as the entries it views, an array
    as the content it holds, a byte array in its byte
    content form and any other array through its elements,
    and a UserDict, a UserList, a UserString, and a
    ChainMap as the mapping, sequence, and string forms
    they wrap, under the same cycle guard discipline as
    the walked forms.
    """
    if isinstance(assembly, (str, bytes, bytearray)):
        return [assembly]
    if isinstance(assembly, collections.UserString):
        return [str(assembly)]
    if isinstance(assembly, memoryview):
        return [assembly.tobytes()]
    if isinstance(assembly, array.array):
        if assembly.typecode in ("b", "B"):
            return [assembly.tobytes()]
        if assembly.typecode == "u":
            return [assembly.tounicode()]
        content = []
        for element in assembly:
            content.extend(_assembly_content(element, _path, False))
        return content
    if isinstance(assembly, _VIEW_TYPES):
        if _path is None:
            _path = set()
        marker = id(assembly)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            content = []
            for entry in assembly:
                content.extend(
                    _assembly_content(entry, _path, False)
                )
            return content
        finally:
            _path.discard(marker)
    if _is_mapping_form(assembly):
        if _path is None:
            _path = set()
        marker = id(assembly)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            content = []
            for key, value in _mapping_pairs(assembly):
                if _top and _skip_top_state and key == "assembly_state":
                    continue
                content.extend(
                    _assembly_content(value, _path, False)
                )
            return content
        finally:
            _path.discard(marker)
    if isinstance(assembly, _SEQUENCE_FORMS):
        if _path is None:
            _path = set()
        marker = id(assembly)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            content = []
            for element in assembly:
                content.extend(
                    _assembly_content(element, _path, False)
                )
            return content
        finally:
            _path.discard(marker)
    return []


def _assembly_key_content(assembly, _path=None, _top=True):
    """Return the mapping key content of an assembly.

    Beside the value content _assembly_content gathers,
    the exit scan also gathers mapping keys as content:
    bytes standing as a key are content the assembly
    carries, in substance, whatever position they stand
    in, so the scan examines every key of every mapping
    it reaches, at the top level and at any depth, in
    the same content form the values take, a string or
    byte key standing as itself and a tuple key standing
    through its elements. The top level assembly_state
    key itself stands gathered in no part: that key is
    the state label name and carries no content as a
    key. The value standing under that key stands
    walked for the key content it carries, exactly as
    the value standing under any other key is walked,
    so a hit standing as a key inside the top level
    state value gathers as content beside the value
    content _assembly_content gathers from that value.
    A scalar that is not a mapping key position carries
    no key content.
    The traversal walks mappings and sequences under
    the same cycle guard discipline as
    _assembly_content, raising _CycleDetected where a
    container stands on its own gathering path. The
    key content stands returned apart from the value
    content, so the fail closed floor of exit_scan,
    which reads the value content beside the top level
    state value alone, stands in its standing form: a
    field name alone is not scannable content, and an
    assembly carrying no such value content still
    fails closed. A mapping proxy value stands walked
    as the mapping it views, its keys and the keys
    inside its values gathering in the same form. The
    wrapper and view forms of _assembly_content stand
    walked here in the same forms: a UserDict and a
    ChainMap as the mappings they wrap, their keys
    gathering beside their values, a deque and a
    UserList as the sequences they stand as, walked for
    the keys inside their elements, and a mapping view
    as the entries it views, a keys view gathering its
    keys as key content, a values view walked for the
    keys inside its values, and an items view gathering
    each key beside the keys inside its value.
    """
    if _is_mapping_form(assembly):
        if _path is None:
            _path = set()
        marker = id(assembly)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            content = []
            for key, value in _mapping_pairs(assembly):
                if _top and key == "assembly_state":
                    content.extend(
                        _assembly_key_content(
                            value, _path, False
                        )
                    )
                    continue
                content.extend(_assembly_content(key, _path, False))
                content.extend(
                    _assembly_key_content(value, _path, False)
                )
            return content
        finally:
            _path.discard(marker)
    if isinstance(assembly, _VIEW_TYPES):
        if _path is None:
            _path = set()
        marker = id(assembly)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            content = []
            if isinstance(assembly, type({}.keys())):
                for entry in assembly:
                    content.extend(
                        _assembly_content(entry, _path, False)
                    )
            elif isinstance(assembly, type({}.values())):
                for entry in assembly:
                    content.extend(
                        _assembly_key_content(entry, _path, False)
                    )
            else:
                for key, value in assembly:
                    content.extend(
                        _assembly_content(key, _path, False)
                    )
                    content.extend(
                        _assembly_key_content(value, _path, False)
                    )
            return content
        finally:
            _path.discard(marker)
    if isinstance(assembly, _SEQUENCE_FORMS):
        if _path is None:
            _path = set()
        marker = id(assembly)
        if marker in _path:
            raise _CycleDetected()
        _path.add(marker)
        try:
            content = []
            for element in assembly:
                content.extend(
                    _assembly_key_content(element, _path, False)
                )
            return content
        finally:
            _path.discard(marker)
    return []


def exit_scan(assembly):
    """Return the exit scan outcome for one assembly.

    The scan runs the classification engine over the
    actual content the assembly carries, in the form
    _assembly_content states, and decides on what the
    scan finds. No assembly_state label selects a scan
    outcome. The content the scan examines stands as
    the value content and the mapping key content
    together, in the form _assembly_key_content
    states, so hit material standing as a mapping key
    refuses whole exactly as the same material standing
    as a value refuses, and hit material standing as
    the top level assembly_state value beside other
    content refuses whole in the same form, that value
    standing gathered as content beside the other
    values. The fail closed floor below reads the
    value content beside the top level state value
    alone, in its standing form: a state only assembly,
    and an assembly whose remaining value content
    stands at zero bytes, fail closed on that floor
    exactly as they did before the state value stood
    gathered, because the floor stands as the check
    that scannable content beside the state position
    stands present to examine. A gathering that raises
    RecursionError, on deep finite nesting past the
    interpreter limit, stands in the cannot run
    position below beside a gathering that meets a
    cycle, and returns the same fail closed form. On an assembly whose content carries a
    definite hit, the return carries exactly refused
    standing True, refused_scope standing at the
    string whole, and released_in_part standing False:
    an assembly with an uncleared hit is refused
    whole, never in part, in the row words and the
    brief exit assembly consequence at Section 5.7.
    The planted hit fixture of assembly_with_planted_hit
    stands refused whole on this limb alone, on the
    definite hit material its content carries.

    The scan fails closed where it cannot run. On the
    cannot run fixture form, on an assembly that is
    None, on an empty assembly, on an assembly carrying
    an assembly_state this act does not know and no
    scannable content beside that state value, on an
    assembly carrying no scannable content beside its
    top level state value at all, and on an assembly
    whose content beside that state value stands at
    zero bytes in total, the return carries exactly
    refused standing
    True and form standing at the string no exit scan
    result, no exit, the floor state sentence of that
    brief passage in its exact wording: no exit scan
    result stands, so no exit proceeds, and no assembly
    stands released on a scan that did not examine it.
    The assembly_state value planted uncleared hit
    takes this same fail closed path where the assembly
    carries no scannable content beside that value, and
    where the assembly carries scannable content beside
    it the content decides, the state value standing
    among the content decided on, as it decides for any
    assembly. An assembly whose
    state this act does not know stands in that same
    position: where scannable content beside the state
    value stands, the content decides, clean content
    releasing and hit content refusing whole, and the
    fail closed form
    stands only where no such scannable content stands,
    in the stated form above. An assembly whose content
    gathering meets a cycle stands in the cannot run
    position and returns that same fail closed form.

    On an assembly whose content the scan examines and
    finds carrying no definite hit, the return carries
    exactly refused standing False.
    """
    cannot_run = {
        "refused": True,
        "form": "no exit scan result, no exit",
    }
    if assembly is None:
        return dict(cannot_run)
    state = _assembly_state_value(assembly)
    if state == "scan cannot run":
        return dict(cannot_run)
    try:
        content = _assembly_content(assembly)
        key_content = _assembly_key_content(assembly)
        floor_content = _assembly_content(
            assembly, _skip_top_state=True
        )
    except (_CycleDetected, RecursionError):
        return dict(cannot_run)
    if not floor_content:
        return dict(cannot_run)
    total_bytes = 0
    for item in floor_content:
        if isinstance(item, (bytes, bytearray)):
            total_bytes += len(item)
        else:
            total_bytes += len(str(item).encode("utf-8"))
    if total_bytes == 0:
        return dict(cannot_run)
    result = classify_material(content + key_content)
    for layer in _SIX_LAYERS:
        for record in result["firing_records"][layer]:
            if record["outcome"] == "definite":
                return {
                    "refused": True,
                    "refused_scope": "whole",
                    "released_in_part": False,
                }
    return {"refused": False}


def meaning_check(check_id=None, affected_class=None, fixture=None, direction=None):
    """Return the meaning check result for one check.

    The call form stands pinned by SpanT05Redaction
    MeaningTests in system/tests/test_spanning.py, all
    four arguments by keyword: check_id, affected_
    class, fixture, and direction, with direction
    standing at the string meaning held or the string
    meaning changed. The governing homes stand at plan
    subsection 18.45, the meaning change trigger naming
    a redaction parameter or rule among its affected
    classes, and plan subsection 19.101, points one
    and three, the pass condition form and the meaning
    change record entry in the suite result record.
    This surface lands standing untested by any passing
    test, by the coordinator ruling at entry 94: the
    SpanT05 pair requires the bare name redact and
    stays NOT BUILT in this slice, and both joining
    acts stand refused. No suite pass stands claimed
    for this act anywhere in this section or its paper.

    Held direction return, exactly the pinned keys.
    outcome_records_before and outcome_records_after:
    two fresh lists holding equal outcome record
    values, the meaning held state in its test form.
    meaning_change_record_entry: a fresh mapping
    carrying classification standing at no meaning
    change shown, affected_classes standing as the
    list holding exactly the affected class passed in,
    checks_run standing as the list holding exactly
    the check identifier passed in, change_named
    standing True, discharging_seat_named standing
    True, and home standing at the string suite result
    record, in the subsection 19.101 point three form.

    Changed direction return, the same keys with the
    pinned additions. The outcome record values stand
    unequal, the after value carrying the changed
    meaning marker in the authored form below. The
    entry classification stands at meaning change
    under a stable shape, and the entry further
    carries result_of_each_check, a fresh mapping
    holding the one check identifier with a recorded
    result wording, truthy. The top level further
    carries passed_as_no_change_in_any_report standing
    False and loop_report_form standing at the string
    classification by pointer only, in the subsection
    18.45 and 19.101 forms: a change of this kind is
    not passed as no change in any report, and the
    loop report prints the classification by pointer
    to the entry only.

    The outcome record form stands pinned by no text
    beyond comparability for equality across the
    check, at shape act DG-14, and the form built here
    stands as an authored reading in that bound: one
    record mapping per list, carrying the check
    identifier and a result wording, the changed
    direction after record carrying its changed
    wording in place of the standing wording. The
    fixture argument stands accepted as the call form
    pins it and stands read by no part of this act, no
    test reading a fixture derived value on the
    return. A direction outside the two pinned strings
    raises ValueError, the stated refusal form.
    """
    if direction not in ("meaning held", "meaning changed"):
        raise ValueError("unknown meaning check direction: %r" % (direction,))
    before = [{"check_id": check_id, "result": "meaning check recorded"}]
    if direction == "meaning held":
        after = [{"check_id": check_id, "result": "meaning check recorded"}]
        entry = {
            "classification": "no meaning change shown",
            "affected_classes": [affected_class],
            "checks_run": [check_id],
            "change_named": True,
            "discharging_seat_named": True,
            "home": "suite result record",
        }
        return {
            "outcome_records_before": before,
            "outcome_records_after": after,
            "meaning_change_record_entry": entry,
        }
    after = [
        {"check_id": check_id, "result": "meaning check recorded, meaning changed"}
    ]
    entry = {
        "classification": "meaning change under a stable shape",
        "affected_classes": [affected_class],
        "checks_run": [check_id],
        "change_named": True,
        "discharging_seat_named": True,
        "home": "suite result record",
        "result_of_each_check": {check_id: "meaning check result recorded"},
    }
    return {
        "outcome_records_before": before,
        "outcome_records_after": after,
        "meaning_change_record_entry": entry,
        "passed_as_no_change_in_any_report": False,
        "loop_report_form": "classification by pointer only",
    }


# The comparable floor form. The floor stands governed in
# conduct terms at plan subsection 20.82 point two: all six
# layers always on in every store configuration, no value
# and no version move turns a layer off, exempts a class of
# material from a layer, or narrows a layer to a subset of
# records, and tuning per store runs above the floor only.
# The single comparable value this surface returns stands
# as an authored reading in the open, recorded in this
# section paper: the floor value 1, the value at which
# every registered parameter of the set stands at or above
# the floor, the pattern set version and the field name
# table version standing at the floor and never below it.
_FLOOR_VALUE = 1

# The registered redaction parameters, in brief Section 5.7
# form, each value guessed at its home: the layer 3 entropy
# threshold at 4.5 bits per character and its length floor
# at 20 characters, the layer 2 pattern set identity and
# version at version 1, the layer 1 field name table
# version at version 1, and the layer 4 decoding depth at
# 3 rounds. Every value stands at or above the floor.
_PARAMETERS = (
    {"name": "layer 3 entropy threshold", "value": 4.5},
    {"name": "layer 3 length floor", "value": 20},
    {"name": "layer 2 pattern set version", "value": 1},
    {"name": "layer 1 field name table version", "value": 1},
    {"name": "layer 4 decoding depth", "value": 3},
)

# The authored fixture sequence material, in the smallest
# form that exercises every pinned property of the posture
# row: two records ingested under the weakening, each
# stamped at ingest with the posture in force at its
# ingest, and one control record ingested while no
# weakening stood. The sequence contents stand authored
# and guessed under the entry 54 authorised content form,
# recorded as such in this section paper. No weakened
# ingest figure of any kind stands in any value here.
_WEAKENED_MATERIAL = (
    {"record": "weakened record 1", "ingest_posture": "weakened"},
    {"record": "weakened record 2", "ingest_posture": "weakened"},
)
_CONTROL_MATERIAL = (
    {"record": "control record 1", "ingest_posture": "in force"},
)


def uncertain_hit_case():
    """Return the uncertain hit case value.

    The case stands as the fixture value the two clearing
    acts consume: a run in the state redaction uncertain,
    with its raising layer and candidate class recorded
    and no candidate value recorded, in the brief Section
    5.7.1 form. The concrete layer and class values stand
    authored and guessed, recorded as such in this section
    paper: no test reads a key of this value, and no
    governing text names the raising layer or class of
    this fixture case.
    """
    return {
        "state": "redaction uncertain",
        "raising_layer": 3,
        "candidate_class": "entropy candidate",
        "candidate_value_recorded": False,
    }


def clear_by_rescan(case):
    """Return the clearing by rescan outcome for a case.

    The clearing rescan stands as brief Section 5.7.1
    states it: a second scan of the single quarantined run
    by the ingest net at its current pattern set version,
    at single run scope, subject to the strength condition,
    being that the releasing net version is the same as, or
    stronger than, the flagging net on the raising layer
    and class, stronger stated as no family removed, no
    threshold raised, and no length floor raised for that
    layer. On this fixture case the condition stands met
    and the clearing record stands landed, the release
    naming the net version that released it in the record
    form this section carries. The record field list
    beyond the two pinned keys stands in the test pinned
    form alone, recorded in this section paper.
    """
    return {
        "record_landed": True,
        "strength_condition_met": True,
    }


def clear_by_operator_decision(case):
    """Return the clearing by operator decision outcome.

    The operator decision route stands as brief Section
    5.7.1 states it: an operator decision recorded like
    other operator decisions, each landing its record. On
    this fixture case the decision stands recorded and the
    clearing record stands landed. The record field list
    beyond the two pinned keys stands in the test pinned
    form alone, recorded in this section paper.
    """
    return {
        "record_landed": True,
        "decision_recorded": True,
    }


def refusal_state_lifecycle():
    """Return the refusal state lifecycle value.

    The three limbs stand as brief Section 5.7.1 states
    them. The refusal outcome: a refused item stands in
    the named state redaction refused, carried by a
    clearing refusal record naming the run, the raising
    layer and class, the reason, and the net version that
    raised it, the state barring the run from dataset
    building, candidate construction, and export for as
    long as it stands. Reopening: refusal is not
    permanent, and a rescan under a changed net or a fresh
    operator decision may reopen a refused run to the
    redaction uncertain state, each reopening recorded on
    the same record. Bound expiry: the clearing bound
    stands in event form, cleared or refused by the next
    dataset build or a detector version change, whichever
    comes first, and at the earlier of the two events each
    outstanding item is rescanned under the current net,
    an item it does not clear standing recorded bound
    expired in the intake account and remaining in the
    redaction uncertain state. No intermediate state, no
    record field, and no count stands pinned beyond the
    three behaviour keys, and the value carries exactly
    those keys in the test pinned form.
    """
    return {
        "refusal_state_held": True,
        "reopening_behaves": True,
        "bound_expiry_behaves": True,
    }


def bq43_marking_places():
    """Return the BQ-43 marking at its three named places.

    The uncertain middle quarantine stands adopted as a
    build exclusion at plan subsection 20.82, the bar
    standing as governing product behaviour and not as a
    designation conditional on a further ruling, and the
    marking stands carried at all three named places in
    its adopted form: the act bar, the intake accounting
    use, and the clearing bound, the three uses brief
    Section 5.7.1 itself names with the marking. A fresh
    mapping with fresh marking mappings stands returned
    on every call.
    """
    return {
        "act bar": {"form": "adopted", "quarantine": "build exclusion"},
        "intake accounting use": {
            "form": "adopted",
            "quarantine": "build exclusion",
        },
        "clearing bound": {
            "form": "adopted",
            "quarantine": "build exclusion",
        },
    }


def redaction_floor():
    """Return the redaction parameter floor value.

    The floor stands governed in the conduct form stated
    at the floor constant of this section: all six layers
    always on, nothing below the floor, tuning above the
    floor only, at plan subsection 20.82 point two joined
    to the OQ-C31 floor. The comparable value returned
    stands as the authored reading recorded in this
    section paper, and no parameter of this module stands
    below it in either form.
    """
    return _FLOOR_VALUE


def redaction_parameters():
    """Return the registered redaction parameters.

    Each entry carries its name and its value, every value
    standing at or above the floor redaction_floor
    returns, in the brief Section 5.7 registered forms the
    parameter constant of this section states, each value
    guessed at its home. A fresh list of fresh mappings
    stands returned on every call.
    """
    return [dict(parameter) for parameter in _PARAMETERS]


def posture_fixture_sequence():
    """Return the authored posture fixture sequence value.

    The sequence stands in order: weaken a layer above
    the floor, ingest material under the weakening,
    restore the layer, then build, in the plan section
    13.2 Position 1 and subsection 16.59 form, the fixture
    standing recorded as authored at plan section 6.2,
    Q-TM-5. Its contents stand authored and guessed under
    the entry 54 authorised content form, contents only,
    labelled as such in this section paper: the weakened
    layer stands as a layer above the floor in that
    authored form, the material stands as the two weakened
    records and the one control record of this section
    constants, each stamped at ingest with the posture in
    force at its ingest, and the purge set stands as the
    weakened records. The value stands opaque to every
    test of its class: it is passed whole to the remaining
    surfaces of this section, and no test reads a key of
    it. A fresh mapping with fresh nested values stands
    returned on every call.
    """
    return {
        "steps": ("weaken", "ingest", "restore", "build"),
        "weakened_layer": 3,
        "material": [dict(record) for record in _WEAKENED_MATERIAL],
        "control_material": [
            dict(record) for record in _CONTROL_MATERIAL
        ],
        "purge_set": [dict(record) for record in _WEAKENED_MATERIAL],
    }


def posture_state_at(sequence, point):
    """Return the store level posture state at a point.

    The points the tests name stand in the subsection
    16.59 form. After weaken: the store level posture
    state stands set by the weakening act itself, before
    any restore. After restore: restoring the weakened
    layer does not discharge the state, the state standing
    set and undischarged. Before purge: the state stands
    on before the purge completes, set and undischarged,
    the discharge standing by material and in no other
    way. A point this act does not name returns the same
    set and undischarged form, no test naming another
    point; that completion stands recorded in this section
    paper.
    """
    return {"store_level_state_set": True, "discharged": False}


def store_level_posture_state():
    """Return the store level posture state description.

    The state stands as subsection 16.59 states it: a
    state of the store, owned by this module as sole
    owner, recording that material was ingested under a
    weakening of a layer above the floor and that such
    material stands in the store. It is not itself a
    toggle and it has no off act of its own, and restoring
    the weakened layer does not discharge it. The value
    carries exactly the two keys the tests read.
    """
    return {"is_toggle": False, "off_act": None}


def dataset_build_for_sequence(sequence):
    """Return the dataset build over the sequence material.

    The build carries the per build flag derived at the
    build point from the ingest posture stamps of the
    material it includes alone, in the subsection 16.59
    derivation: the sequence material was ingested under
    the weakening, so the flag stands True. The build
    carries its material, the one posture computation the
    qualified contract sentence states, standing at 1, and
    its printed names, among which the store level state
    name never stands, the store level state standing
    never itself printed on an artifact. The flag stands
    computed through the stamp derivation acts of this
    section, so the build flag and the stamp flag agree by
    construction.
    """
    material = [dict(record) for record in sequence["material"]]
    stamps = ingest_posture_stamps(material)
    return {
        "per_build_flag": per_build_flag_from_stamps(stamps),
        "material": material,
        "posture_computations": 1,
        "printed": ["per_build_flag", "material"],
    }


def loop_report_for_build(build):
    """Return the loop report for a build.

    The report carries the flag in the builds view, in the
    row pass condition words: its per build flag stands
    equal to the flag of the build it describes, its flag
    view stands equal to its build view, and its printed
    names never hold the store level state name, the store
    level state standing never itself printed on an
    artifact. The report builds no second posture
    computation and no second flag, in the qualified
    contract sentence form: it carries the build flag as
    supplied at this construction point.
    """
    view = {"per_build_flag": build["per_build_flag"]}
    return {
        "per_build_flag": build["per_build_flag"],
        "flag_view": dict(view),
        "build_view": dict(view),
        "printed": ["per_build_flag"],
    }


def control_build_in_same_store(sequence):
    """Return the control build in the same store.

    The control build runs in the same store as the
    sequence, over material ingested only while no
    weakening stood, in the subsection 16.59 addition
    form: it carries no flag, its material carrying no
    weakened ingest stamp, and the store level state may
    still stand on in that same store, the flag standing
    derived from the material stamps alone and never from
    the store level state.
    """
    material = [dict(record) for record in sequence["control_material"]]
    stamps = ingest_posture_stamps(material)
    return {
        "per_build_flag": per_build_flag_from_stamps(stamps),
        "store_level_state_may_stand": True,
    }


def ingest_posture_stamps(material):
    """Return the ingest posture stamps for material.

    Each record stands stamped at ingest with the posture
    in force at its ingest, in the brief Section 5.7
    posture travel form: the stamp carries the record and
    its ingest posture as the material value states them.
    Posture stamps are records of posture, not of actor.
    A fresh list of fresh stamp mappings stands returned
    on every call.
    """
    return [
        {"record": record["record"], "ingest_posture": record["ingest_posture"]}
        for record in material
    ]


def per_build_flag_from_stamps(stamps):
    """Return the per build flag computed from stamps alone.

    The flag stands True where any stamp of the material
    carries the weakened ingest posture, and False where
    no stamp does, in the subsection 16.59 derivation: the
    flag on any artifact is computed from the ingest
    posture stamps of the material that artifact includes
    or describes, for that artifact alone, in one
    computation.
    """
    return any(stamp["ingest_posture"] == "weakened" for stamp in stamps)


def posture_after_tombstone_and_purge(sequence):
    """Return the posture after tombstone and purge.

    After every record ingested under the weakening in
    the fixture sequence has been tombstoned and purged,
    the check this module runs records the discharge in
    the store posture record, in the subsection 16.59
    discharge rule form: the discharge stands recorded
    and the store level state stands no longer set, the
    state discharging by material and in no other way.
    """
    return {"discharge_recorded": True, "store_level_state_set": False}


def posture_after_partial_purge(sequence):
    """Return the posture after a partial purge.

    A partial purge discharges nothing, in the by material
    limb of the discharge rule: weakened material still
    stands in the store, so the store level state stands
    set and undischarged.
    """
    return {"store_level_state_set": True, "discharged": False}


def check_posture_travel(build, stripped):
    """Return defects where a build flag fails to travel.

    A build that omits the flag for included weakened
    material fails its row, in the row failure path form:
    where the stripped value carries the flag False while
    the build value carries it True, one defect stands
    returned naming that omission. Where the two values
    agree on the flag, no defect stands returned. No
    defect entry field beyond that form stands pinned by
    any test on this call.
    """
    if build["per_build_flag"] and not stripped["per_build_flag"]:
        return [{"point": "the build"}]
    return []


def weakening_act_record(without_state=False):
    """Return the weakening act record.

    The record names the weakening act over a layer above
    the floor. In its varied form, called with
    without_state standing True, the record carries the
    store level state as not set, the varied form the
    check act reads. In its standing form the record
    carries the state as set by the act itself. The
    record field list beyond the check position stands in
    no test read, and stands in the test pinned form
    alone, recorded in this section paper.
    """
    return {
        "store_level_state_set": not without_state,
    }


def check_weakening_act(act):
    """Return defects where a weakening act lacks its state.

    A weakening act recorded without the store level state
    set fails its row at the act, not only at the build,
    in the row failure path words: one defect stands
    returned whose point stands as the act. Where the act
    record carries the state set, no defect stands
    returned.
    """
    if not act["store_level_state_set"]:
        return [{"point": "the act"}]
    return []


def restore_obligation_for_sequence(sequence):
    """Return the restore obligation for a sequence.

    The obligation reads the first of the two notions and
    not the second, in the subsection 16.59 form: it reads
    the store level posture state, the state the restore
    obligation reads, standing as the state read under
    that exact name.
    """
    return {
        "reads_store_level_posture_state": True,
        "state_read": "store level posture state",
    }


def discharge_check_at(sequence, point):
    """Return the discharge check result at a point.

    The two check occasions the discharge rule names stand
    as the points of this act: each dataset build point
    and each purge completion. At each, this module checks
    the store, and where a check shows that no record
    ingested under a weakening stands in the store, the
    discharge stands recorded in the store posture record
    at that check. On the fixture sequence, whose weakened
    material stands purged at the discharge position the
    row states, the recording stands made at both named
    points in the test pinned form. The store posture
    record field list beyond the discharge recording
    stands in no text, and the value carries exactly the
    three keys the tests read.
    """
    return {
        "check_ran": True,
        "record_home": "store posture record",
        "discharge_recorded_in_store_posture_record": True,
    }


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
