"""Capture module, slice CAPTURE form.

Live capture at the review act, with the fidelity floor
fields fixed at capture, the signature, the group key,
and the pool stamp computed from the named structured
fields only and without reading the review outcome or
any correction, Step predecessor chains, the partial
flag, the pending outcome state and its two closing
routes, capture refusal at the D-13 caps with no
truncation, a run with no outcome counted in runs seen
only, and capture refused while the store stands
suspect. The D-13 cap values, 64 KiB per journal line
and 32 KiB per text field, stand labelled guessed
wherever they stand in this module.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of
this file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.capture"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "capture_example_a",
    "capture_into_store",
    "capture_payload",
    "computation_inputs",
    "d13_caps",
    "example_a_chain",
    "meaning_check",
    "membership_counts",
    "pending_outcome_close_routes",
    "pool_stamp",
    "submit_outcome",
    "validate_chain",
]


import hashlib


# The Example A structured field values, in brief
# Section 5.3 named field order: the review target
# identity, the task kind, and the template or
# instruction version in force. Their standing
# stands as follows, value by value. The task kind
# value, the word review, stands on the CORE form at
# run_missing_required_structured_field, where a
# review run carries that kind value. The template
# version value, 1, stands on the CORE forms, where
# a review run carries template version 1 and the
# Example A record carries workflow definition
# version 1. The review target identity value
# stands on no ground: no text states an Example A
# target value, and it stands authored and guessed
# under scope item G-1. The signature version
# value, 1, stands in the same position: plan
# subsection 16.9 names a signature version as the
# signature instrument input and states no value,
# and the value here stands authored and guessed
# under scope item G-1.
_TARGET_IDENTITY = "example-a-review-target"
_TASK_KIND = "review"
_TEMPLATE_VERSION = 1
_SIGNATURE_VERSION = 1


# The Example A group rotation position, authored
# and guessed under scope item G-1. The fixture
# group stands as the first new group in store
# sequence order, at rotation position 1. Brief
# Section 5.3 states the rotation in full: a new
# group receives its pool stamp at its first
# acceptance, in fixed rotation over new groups in
# store sequence order, so that every third new
# group in that order is stamped holdout eligible
# and the other two are not, and the stamp is
# permanent from that acceptance. Position 1 is not
# a third position, so the stamp this fixture group
# carries stands at the not holdout eligible form.
# Later runs in the group carry this stamp by
# inheritance, in the subsection 16.9 form, and no
# varied call in this section founds a new group, so
# no varied call receives a fresh stamp.
_ROTATION_POSITION = 1


# The Example A chain step identities, in order.
# They stand on the landed CORE form at
# example_a_record, whose payload steps carry the
# step identity values example-a-step-one and
# example-a-step-two, in that order. The chain
# contents built over them, the order list form and
# the broken form below, stand authored and
# guessed under scope item G-2, as the fragment
# paper states.
_STEP_ONE = "example-a-step-one"
_STEP_TWO = "example-a-step-two"


# The broken chain predecessor value, authored and
# guessed under scope item G-2. In the broken form
# the second step predecessor names a step that
# does not exist in the chain, one of the four
# broken chain forms brief Section 5.3 names. No
# governing text states which broken form the
# chain break variation exercises.
_BROKEN_PREDECESSOR = "example-a-step-nonexistent"

# The Example A chain run identity, authored and
# guessed under scope item G-2 in the same standing
# as the chain contents: the chain form carries the
# identity of the run its steps stand in, so chain
# validation can detect a predecessor naming a step
# in another run.
_RUN_IDENTITY = "example-a-run"


def _digest(domain, parts):
    text = domain
    for part in parts:
        text = text + "\x00" + str(part)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _signature():
    return _digest(
        "signature",
        (
            _TARGET_IDENTITY,
            _TASK_KIND,
            _TEMPLATE_VERSION,
            _SIGNATURE_VERSION,
        ),
    )


def _group_key():
    return _digest(
        "group key",
        (_TARGET_IDENTITY, _TASK_KIND, _TEMPLATE_VERSION),
    )


def pool_stamp(position):
    """Return the pool stamp for one rotation position.

    The stamp act reads the two inputs computation_inputs
    names for it in fact: the store sequence order, given
    here as the rotation position of the new group in that
    order, and the group first acceptance standing, this
    act standing as the assignment at first acceptance
    itself. Every third new group in store sequence order
    is stamped holdout eligible and the other positions
    are not, in the brief Section 5.3 rotation form, and
    the stamp is permanent from that acceptance. A
    position that is not a positive integer raises
    ValueError.
    """
    if not isinstance(position, int) or isinstance(position, bool):
        raise ValueError("unknown rotation position: %r" % (position,))
    if position < 1:
        raise ValueError("unknown rotation position: %r" % (position,))
    if position % 3 == 0:
        return "holdout eligible"
    return "not holdout eligible"


def _pool_stamp():
    return pool_stamp(_ROTATION_POSITION)


# The computation input names, by computation, in
# the forms the acts in this section read in fact.
# The signature and group key names stand on the
# brief Section 5.3 named fields, with the
# signature version name standing on plan
# subsection 16.9. The pool stamp names stand on
# the subsection 16.9 split form: that computation
# reads the store sequence order position and the
# group first acceptance standing, and no run
# field. Any name in these lists beyond those
# grounds stands authored and guessed under scope
# item G-1.
_COMPUTATION_INPUTS = {
    "signature": (
        "review target identity",
        "task kind",
        "template or instruction version in force",
        "signature version",
    ),
    "group_key": (
        "review target identity",
        "task kind",
        "template or instruction version in force",
    ),
    "pool_stamp": (
        "store sequence order",
        "group first acceptance",
    ),
}

_CAPTURE_VARIATIONS = (None, "outcome only", "outcome and correction")

_CHAIN_VARIATIONS = (None, "chain break")


def capture_example_a(varied_by=None):
    """Return the Example A capture values.

    The return carries exactly the three test pinned
    keys. signature: the task signature of the
    Example A review run, computed by the section
    signature act from the named structured fields
    and the signature version, and from nothing
    else. group_key: the group key of that run,
    computed by the section group key act from the
    named structured fields, and from nothing else,
    computed at capture and frozen in the brief
    form. pool_stamp: the pool stamp of that run,
    assigned at group first acceptance by the fixed
    rotation over new groups in store sequence
    order, in the subsection 16.9 split form stated
    in the header, permanent from that acceptance.
    None of the three acts reads the review outcome
    or any correction, under brief Section 5.3 item
    S5-O-15, so the base call and each varied call
    return the same three values by construction:
    the varied_by argument names a variation of the
    run outcome, or of the outcome and the
    correction together, and no act in this section
    reads that argument value beyond checking it
    stands among the pinned variation forms.
    The concrete value forms stand as follows. The
    signature and group key values stand as SHA-256
    hex digest strings over a domain word and the
    field values in named order: that computation
    form and those value forms stand authored and
    guessed under scope item G-1, no text stating a
    computation form or a value form for either
    value. The pool stamp value stands as one of
    the two brief rotation wordings, holdout
    eligible or not holdout eligible, at the
    rotation position stated in this section: that
    value form stands authored and guessed under
    scope item G-1 in the same way, the rotation
    rule itself standing grounded at brief
    Section 5.3 and plan subsection 16.9.
    A varied_by value outside the pinned forms
    raises ValueError. A fresh mapping stands
    returned on every call.
    """
    if varied_by not in _CAPTURE_VARIATIONS:
        raise ValueError("unknown capture variation: %r" % (varied_by,))
    return {
        "signature": _signature(),
        "group_key": _group_key(),
        "pool_stamp": _pool_stamp(),
    }


def computation_inputs(name):
    """Return the input names of one computation.

    The argument is one computation name string,
    signature, group_key, or pool_stamp. The return
    is a tuple of input name strings, the inputs the
    section act for that computation reads in fact,
    in the table above this section. The tests pin
    two exclusions and no inclusion: the string
    review outcome stands in none of the three
    tuples, and the string correction stands in
    none of the three tuples, and both exclusions
    hold here by construction, no act in this
    section carrying either name as an input.
    A name outside the three raises ValueError.
    """
    try:
        known = name in _COMPUTATION_INPUTS
    except (TypeError, ValueError):
        known = False
    if not known:
        raise ValueError("unknown computation: %r" % (name,))
    return tuple(_COMPUTATION_INPUTS[name])


def example_a_chain(varied_by=None):
    """Return the Example A predecessor chain.

    The return carries the two test pinned keys and
    the run identity key stated below. order: a fresh
    list holding the two step identity values in
    chain order, on the CORE ground stated at the
    step constants above.
    steps: a fresh list of two fresh step mappings,
    each carrying step_identity and predecessor.
    The first step predecessor stands as None, the
    stated predecessor value of none at brief
    Section 5.3. The second step predecessor names
    the first step identity, the immediately
    preceding step in the same run, under the Step
    predecessor rule at brief Section 5.3 item
    S5-O-1. The step key form stands as predecessor
    here, in the test pinned form: the landed CORE
    payload states the same fact under the key
    predecessor_reference, and that form difference
    stands recorded at shape act DG-4 and in the
    fragment paper in the open.
    In the varied form, varied_by standing at the
    string chain break, the second step predecessor
    names a step that does not exist in the chain,
    in the authored and guessed broken form stated
    at the broken predecessor constant above, under
    scope item G-2. The order value and the step
    identities stand unmoved in that form.
    The chain carries its run identity at the top
    level under run_identity, and each step carries
    the same identity under run, so a predecessor
    naming a step in another run stands detectable
    by validate_chain: a step may carry
    predecessor_run naming the run its predecessor
    stands in, and a predecessor_run differing from
    the step own run stands as a cross run
    predecessor. The run identity value stands
    authored and guessed under scope item G-2 in
    the same standing as the chain contents.
    A varied_by value outside the pinned forms
    raises ValueError.
    """
    if varied_by not in _CHAIN_VARIATIONS:
        raise ValueError("unknown chain variation: %r" % (varied_by,))
    second_predecessor = _STEP_ONE
    if varied_by == "chain break":
        second_predecessor = _BROKEN_PREDECESSOR
    return {
        "order": [_STEP_ONE, _STEP_TWO],
        "run_identity": _RUN_IDENTITY,
        "steps": [
            {
                "step_identity": _STEP_ONE,
                "predecessor": None,
                "run": _RUN_IDENTITY,
            },
            {
                "step_identity": _STEP_TWO,
                "predecessor": second_predecessor,
                "run": _RUN_IDENTITY,
            },
        ],
    }


def validate_chain(chain):
    """Return the validation result for one chain.

    The argument is a chain value in the form
    example_a_chain returns. The act reads the
    chain order and steps by their stated keys
    only, and checks the chain in the brief
    Section 5.3 completion form: the chain carries
    at least one step; the first step predecessor
    stands as None; and each later step
    predecessor names the immediately preceding
    step in the same chain, a predecessor naming a
    step in another run, a step that does not
    exist, a step that appears later in the order,
    or the step itself standing as a broken chain
    in that check.
    The return carries exactly the four test
    pinned keys. valid: True on a chain that
    passes every check, and False on a broken
    chain. order: a fresh list holding the chain
    order value, standing equal to the list form
    of the chain order on every return. refused:
    False on every return of this section.
    flagged_partial: True on a broken chain, and
    False on a valid chain.
    The broken chain limb stands adopted in this
    form, stated in the open: brief Section 5.3
    states a broken chain sets the partial flag on
    the run and stands as a build drop reason
    counted in the intake account, and states no
    refusal consequence for a broken chain, so
    this act carries the flagged partial limb and
    not the refusal limb, at shape act DG-4. The
    test reads the two keys in disjunction only,
    and no wider consequence stands built or
    claimed here: no partial flag key on a run
    value and no intake count stands in this
    return, at shape item G-5.
    A chain value in no chain form stands refused
    in the one governed ValueError form the sibling
    surfaces of this module use on an input in no
    stated form: a chain that is not a mapping, a
    chain carrying no order or no steps value, an
    order or steps value in no list form, a step
    entry in no mapping form, and a step entry
    carrying no predecessor all raise ValueError
    naming the unknown chain form. A chain in chain
    form whose checks fail takes the flagged
    partial limb above, never this refusal.
    """
    if not isinstance(chain, dict):
        raise ValueError("unknown chain form: %r" % (chain,))
    if "order" not in chain or "steps" not in chain:
        raise ValueError("unknown chain form: %r" % (chain,))
    if isinstance(chain["order"], (str, bytes, bytearray)) or not isinstance(
        chain["order"], (list, tuple)
    ):
        raise ValueError("unknown chain form: %r" % (chain,))
    if isinstance(chain["steps"], (str, bytes, bytearray)) or not isinstance(
        chain["steps"], (list, tuple)
    ):
        raise ValueError("unknown chain form: %r" % (chain,))
    order = list(chain["order"])
    steps = list(chain["steps"])
    for step in steps:
        if not isinstance(step, dict):
            raise ValueError("unknown chain step form: %r" % (step,))
        if "predecessor" not in step:
            raise ValueError("unknown chain step form: %r" % (step,))
    chain_run = chain.get("run_identity")
    identities = []
    for index, step in enumerate(steps):
        if "step_identity" in step:
            identities.append(step["step_identity"])
        elif index < len(order):
            identities.append(order[index])
        else:
            identities.append(None)
    broken = False
    if not steps:
        broken = True
    if len(steps) != len(order):
        broken = True
    if identities != order:
        broken = True
    for index, step in enumerate(steps):
        step_run = step.get("run", chain_run)
        if chain_run is not None and step_run != chain_run:
            broken = True
        predecessor = step["predecessor"]
        if index == 0:
            if predecessor is not None:
                broken = True
            continue
        predecessor_run = step.get("predecessor_run", step_run)
        if predecessor_run != step_run:
            broken = True
        if predecessor not in identities:
            broken = True
        elif predecessor == identities[index]:
            broken = True
        elif identities.index(predecessor) >= index:
            broken = True
        elif predecessor != identities[index - 1]:
            broken = True
    if broken:
        return {
            "valid": False,
            "order": order,
            "refused": False,
            "flagged_partial": True,
        }
    return {
        "valid": True,
        "order": order,
        "refused": False,
        "flagged_partial": False,
    }


# The two pending outcome closing routes, in brief
# Section 5.3 form: an Outcome record for the run is
# appended and the state reads attached from that
# append, or the operator records none will follow on
# the operator surface, with a reason. The tests pin
# the count of two and no entry value. The spelling of
# each entry stands as an authored reading in the
# open, under the bound at step record entry 99 item
# (d) for scope gap G-6, recorded in the fragment
# paper.
_CLOSE_ROUTES = (
    "outcome record appended",
    "operator records none will follow",
)

# The D-13 cap entries. The values stand grounded in
# the register entry D-13 at brief Section 3.4: 64 KiB
# per journal line and 32 KiB per text field, guessed
# overall. Each entry carries its guessed source class
# in the same view, so no cap value of this module
# stands without its guessed label. The list form
# stands authorised as authored and guessed under
# step record entry 99 item (c) G-3 only to the
# extent the grounded D-13 terms do not reach it: the
# two cap kinds and their figures stand on the D-13
# terms, and the entry key form, being the name key,
# the limit key, and the source class key, stands as
# the authored residue alone, labelled as such here
# and in the fragment paper.
_D13_CAPS = (
    {
        "name": "journal line",
        "limit": "64 KiB",
        "source_class": "guessed",
    },
    {
        "name": "text field",
        "limit": "32 KiB",
        "source_class": "guessed",
    },
)

# The membership figure names the counting return
# carries. Brief Section 5.3 names the intake account
# figures beside runs seen, among them runs with
# outcomes, runs dropped per reason, and pool counts.
# The tests pin no figure name and no figure count,
# and an empty mapping would satisfy the counting
# test as written. The set carried here stands as an
# authored reading in the open, under the bound at
# step record entry 99 item (d) for scope gap G-6,
# recorded in the fragment paper.
_MEMBERSHIP_FIGURES = (
    "runs with outcomes",
    "runs dropped per reason",
    "pool counts",
)


def pending_outcome_close_routes():
    """Return the pending outcome close routes.

    The return is a fresh list holding exactly the two
    route entries of this section, in their authored
    spelling form stated at the route constant above.
    Its ground is brief Section 5.3: the pending
    outcome state closes in exactly two ways, and no
    bound closes pending automatically. The test pins
    the length of the return at 2 and reads no entry.
    """
    return list(_CLOSE_ROUTES)


def submit_outcome(case):
    """Return the outcome submission outcome for a case.

    The act reads the run state the case states, in
    either of the forms it accepts: a case name string,
    or a mapping carrying the run state under the key
    state or the key run_state. On a closed state, the
    none will follow state or the attached state, the
    return carries exactly the two test pinned keys.
    refused: True. reason: the string closed state.
    Its ground is the outcome precedence passage at
    brief Section 5.3: an Outcome appended for a run
    already closed as none will follow, and a second
    Outcome appended for a run already in the attached
    state, are each refused with a named error naming
    the closed state, and dataset eligibility follows
    the first closed outcome only. The case name late
    stands read as the none will follow case and the
    case name second as the attached case, in the
    plain reading the shape act states, and that
    mapping stands as an authored reading in the open
    under the bound at step record entry 99 item (d).
    On an open pending state the submission stands
    accepted: the return carries refused False and
    reason standing at the string outcome appended,
    the pending outcome state closing by the outcome
    record route pending_outcome_close_routes names.
    A case stating no state this act knows raises
    ValueError, the refusal form the landed fragments
    use for an unknown argument to a present function.
    """
    state = case
    if isinstance(case, dict):
        state = case.get("state", case.get("run_state"))
    if state in ("late", "second", "attached", "none will follow"):
        return {"refused": True, "reason": "closed state"}
    if state in ("pending", "open"):
        return {"refused": False, "reason": "outcome appended"}
    raise ValueError("unknown outcome submission case: %r" % (case,))


_JOURNAL_LINE_CAP_BYTES = 64 * 1024
_TEXT_FIELD_CAP_BYTES = 32 * 1024


def _value_byte_form(value, _path=None):
    """Return the byte form of one payload value, in substance.

    Bytes, a bytearray, and a memoryview stand as the
    byte content they carry or view, so a memoryview
    stands measured by the bytes it views and not by
    the string form of the view, which states no part
    of that content. A string stands in its UTF-8 byte
    form. A container value stands as the joined byte
    forms of the content it carries at any position
    inside it, so a memoryview nested inside a list
    standing as a mapping value stands measured in
    substance in the same way. Any other value
    stands in the UTF-8 byte form of its string form.
    It reads recursively.
    """
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, (dict, list, tuple, set, frozenset)):
        if _path is None:
            _path = set()
        marker = id(value)
        if marker in _path:
            return b""
        _path.add(marker)
        try:
            if isinstance(value, dict):
                parts = []
                for key in value:
                    parts.append(_value_byte_form(key, _path))
                    parts.append(_value_byte_form(value[key], _path))
                return b"".join(parts)
            return b"".join(
                _value_byte_form(element, _path) for element in value
            )
        finally:
            _path.discard(marker)
    return str(value).encode("utf-8")


def _payload_fields(payload):
    """Return the text fields of a payload, as byte strings.

    A mapping payload contributes one field per value,
    in key order, each value read through
    _value_byte_form, in the substance form that act
    states. A string or bytes payload stands as a
    single text field in its byte form, and a
    memoryview payload stands as that single field in
    the byte content it views. Any other payload form
    raises ValueError.
    """
    if isinstance(payload, dict):
        fields = []
        for key in payload:
            fields.append(_value_byte_form(payload[key]))
        return fields
    if isinstance(payload, (bytes, bytearray, memoryview)):
        return [bytes(payload)]
    if isinstance(payload, str):
        return [payload.encode("utf-8")]
    raise ValueError("unknown payload form: %r" % (type(payload),))


def _measure_payload(payload):
    """Measure a payload against both D-13 caps.

    The journal line size stands as the total of the
    field byte sizes plus one separator byte between
    fields. The text field size stands as the largest
    single field byte size. Each mapping key stands
    counted in its byte form toward the measured
    sizes beside the value fields: a key stands
    measured as a field of the journal line its entry
    writes, so a key whose byte form passes a cap
    refuses the payload in the same standing. The
    return carries both measured sizes and the
    refusal standing: refused where either size
    passes its cap, a payload at a cap standing
    accepted whole.
    """
    fields = _payload_fields(payload)
    line_size = sum(len(field) for field in fields)
    if len(fields) > 1:
        line_size += len(fields) - 1
    field_size = max([len(field) for field in fields], default=0)
    if isinstance(payload, dict):
        key_size = max(
            [len(_value_byte_form(key)) for key in payload],
            default=0,
        )
        field_size = max(field_size, key_size)
    refused = (
        line_size > _JOURNAL_LINE_CAP_BYTES
        or field_size > _TEXT_FIELD_CAP_BYTES
    )
    return {
        "journal_line_bytes": line_size,
        "text_field_bytes": field_size,
        "refused": refused,
    }


def capture_payload(case):
    """Return the payload capture outcome for a payload.

    The act measures the payload it is given against
    both D-13 caps and decides on the measurement. A
    real payload stands accepted in either of the
    payload forms _payload_fields states: a string or
    bytes payload as a single text field on one journal
    line, or a mapping payload field by field. The two
    case name strings the Step 13 tests name stand as
    fixture payload constructors in the form the suite
    uses elsewhere: the string at cap builds the
    two field payload whose fields stand at the text
    field cap and one byte under it, measuring exactly
    at the journal line cap with its separator byte,
    and the string over cap builds the two field
    payload with both fields at the text field cap,
    measuring one byte over the journal line cap. Both
    fixture payloads pass through the same measurement
    act as any real payload, and no outcome stands
    stored against either name.

    The return carries exactly the five keys the
    tests pin across this class. Accepted whole:
    accepted True, truncated False, refused False,
    truncation_written False, and
    partial_record_written False. Refused: accepted
    False, truncated False, refused True,
    truncation_written False, and
    partial_record_written False. Its ground is the
    capture cap failure form at brief Section 5.3:
    where a journal line would pass the D-13 line
    cap or a text field would pass the D-13 field
    cap on legitimate work, capture refuses that run
    and records no part of it, and no truncation
    happens at capture. The cap values stand at
    D-13, 64 KiB per journal line and 32 KiB per text
    field, guessed, and stand labelled guessed at
    the caps surface of this module. A payload in no
    stated form raises ValueError.
    """
    if case == "at cap":
        payload = {
            "first": "a" * _TEXT_FIELD_CAP_BYTES,
            "second": "b" * (_TEXT_FIELD_CAP_BYTES - 1),
        }
    elif case == "over cap":
        payload = {
            "first": "a" * _TEXT_FIELD_CAP_BYTES,
            "second": "b" * _TEXT_FIELD_CAP_BYTES,
        }
    else:
        payload = case
    measured = _measure_payload(payload)
    if measured["refused"]:
        return {
            "accepted": False,
            "truncated": False,
            "refused": True,
            "truncation_written": False,
            "partial_record_written": False,
        }
    return {
        "accepted": True,
        "truncated": False,
        "refused": False,
        "truncation_written": False,
        "partial_record_written": False,
    }


def d13_caps():
    """Return the D-13 caps, each labelled guessed.

    The return is a fresh list of fresh mappings, one
    per cap of the register entry D-13, in the form
    stated at the caps constant of this section. Each
    entry carries name, limit, and source_class, with
    source_class standing at the string guessed on
    every entry, in the test pinned form. The figures
    stand at 64 KiB per journal line and 32 KiB per
    text field, guessed overall at their home in the
    brief register, and the guessed label stands on
    each entry here in the same view as its figure.
    """
    return [dict(cap) for cap in _D13_CAPS]


def membership_counts(case):
    """Return the membership counts for one state.

    On the state the tests name, none will follow,
    the return carries exactly the two test pinned
    keys. runs_seen_delta: 1. membership_figures: a
    fresh mapping keyed by the figure names of this
    section, every value standing at 0. Its ground
    is brief Section 5.3: a dataset build counts a
    pending run in runs seen and in no other
    membership figure, and the test argument names
    the none will follow state of the row fixture.
    In its pinned form this counting value therefore
    stands in no membership figure for the named
    run: the run contributes to runs seen alone.
    The figure set stands as the authored reading
    stated at the figure constant above, under the
    bound at step record entry 99 item (d) for
    scope gap G-6. The act accepts the state in
    either form it is stated in: a state name string,
    or a mapping carrying the state under the key
    state. The pending state counts in the same form
    as the none will follow state, a run in either
    state carrying no outcome: it counts in runs seen
    and in no membership figure. A state outside the
    two this act knows raises ValueError.
    """
    state = case
    if isinstance(case, dict):
        state = case.get("state")
    if state not in ("none will follow", "pending"):
        raise ValueError("unknown membership counts state: %r" % (case,))
    figures = {}
    for figure in _MEMBERSHIP_FIGURES:
        figures[figure] = 0
    return {"runs_seen_delta": 1, "membership_figures": figures}


def capture_into_store(case):
    """Return the capture into store outcome for a case.

    On the suspect case, the return carries exactly
    the three test pinned keys. refused: True.
    reason: the string store suspect. captured:
    False. The reason string stands grounded
    character for character on the landed store
    surface at system/ontoloop/store.py, where
    capture_append on a suspect store refuses in
    terms with that reason wording. The act accepts
    the case in either form it is stated in: the
    case name string the test passes, standing as
    the suspect position in value form, or a real
    store value, a mapping carrying the store
    records, which this act passes to the store
    capture append act itself and reports in the
    same three key form: on a suspect store value
    the refusal stands as above, and on a store
    value the append act accepts, captured stands
    True with refused False and the reason standing
    at the string captured. Its ground beside that
    form is the row behaviour, capture refuses while
    the store stands suspect, at plan section 6.5. A
    case in neither form raises ValueError.
    """
    if case == "suspect":
        return {"refused": True, "reason": "store suspect", "captured": False}
    if isinstance(case, dict) and "records" in case:
        from ontoloop import store as _store_module

        outcome = _store_module.capture_append(case)
        if outcome.get("refused"):
            return {
                "refused": True,
                "reason": outcome.get("reason", "store suspect"),
                "captured": False,
            }
        return {"refused": False, "reason": "captured", "captured": True}
    raise ValueError("unknown capture into store case: %r" % (case,))


def meaning_check(check_id, affected_class, fixture, direction):
    """Return the meaning check result for one check.

    The call form stands pinned by
    SpanT03NormalisationMeaningTests and
    SpanT06TruncationMeaningTests in
    system/tests/test_spanning.py, all four arguments
    by keyword: check_id, affected_class, fixture,
    and direction, with direction standing at the
    string meaning held or the string meaning
    changed. The governing homes stand at plan
    subsection 18.45, the meaning change trigger
    naming a normalisation parameter or rule and a
    truncation parameter or rule among its affected
    classes in the capture path, and plan subsection
    19.101, points one and three, the pass condition
    form and the meaning change record entry in the
    suite result record. This surface lands standing
    untested by any passing test, by the coordinator
    ruling at step record entry 99 item (a): the
    SpanT03 and SpanT06 pairs require the bare name
    capture and stay NOT BUILT in this slice, and
    both joining acts stand refused. No suite pass
    stands claimed for this act anywhere in this
    fragment or its paper.

    Held direction return, exactly the pinned keys.
    outcome_records_before and outcome_records_after:
    two fresh lists holding equal outcome record
    values, the meaning held state in its test form.
    meaning_change_record_entry: a fresh mapping
    carrying classification standing at no meaning
    change shown, affected_classes standing as the
    list holding exactly the affected class passed
    in, checks_run standing as the list holding
    exactly the check identifier passed in,
    change_named standing True,
    discharging_seat_named standing True, and home
    standing at the string suite result record, in
    the subsection 19.101 point three form.

    Changed direction return, the same keys with
    the pinned additions. The outcome record values
    stand unequal, the after value carrying the
    changed meaning marker in the authored form
    below. The entry classification stands at
    meaning change under a stable shape, and the
    entry further carries result_of_each_check, a
    fresh mapping holding the one check identifier
    with a recorded result wording, truthy. The top
    level further carries
    passed_as_no_change_in_any_report standing
    False and loop_report_form standing at the
    string classification by pointer only.

    The outcome record form stands pinned by no
    text beyond comparability for equality across
    the check, and the form built here stands as an
    authored reading in that bound: one record
    mapping per list, carrying the check identifier
    and a result wording, the changed direction
    after record carrying its changed wording in
    place of the standing wording. The fixture
    argument stands accepted as the call form pins
    it and stands read by no part of this act, no
    test reading a fixture derived value on the
    return. A direction outside the two pinned
    strings raises ValueError.
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


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
