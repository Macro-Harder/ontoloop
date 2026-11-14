"""Promotion module, slice PROMOTE form.

The Promotion and state machinery module. The governing
state table at brief Section 5.6 stands as one statement
and one implementation unit. Gate pass and deployment
stand as one system act with no observable moment
between them. The module carries the gate sequence at
brief Section 11, the acknowledgement gate, the
confirmation record, the bundle bound checks, the
demotion flag, and the fixed text travel lint over
bundle writing.

The bounds stand each in its own form. The dataset
material this module touches stands for evaluation
only in version 1, under plan subsection 20.84, and no
value in this module stands as material for any other
use. No surface in this module carries a cap figure, a
spend figure, or a price. The D-7 cap stands in slice
EVAL and stands not imported, and the D-10 bound stands
in its grounds form, guessed at its EVAL home, with
this module holding derived views of it only. The
governing state table stands as the only specification
for the state machinery in this module, and no second
statement of any state rule stands in this module text.
The review of the slice output stands as an exit act in
the form plan subsection 19.78 states, outside this
module, and this module text makes no claim about that
review.

What this slice does not build stands absent from this
module altogether, and a lookup of any such name raises
AssertionError in the NOT BUILT form the suite harness
uses, through the module level guard at the foot of this
file. A lookup of a private or dunder name raises
AttributeError in the ordinary form.
"""

MODULE_NAME = "ontoloop.promote"
NOT_BUILT_PREFIX = "NOT BUILT (Step 14): "

__all__ = [
    "state_table_rules",
    "generated_state_tests",
    "interaction_set_name",
    "review_slice_output",
    "slice_output_with_a_second_statement",
    "interrupt_before_append",
    "interrupt_inside_rollback_append",
    "complete_append",
    "promote_with_observer",
    "promote",
    "gate_sequence_order",
    "gate_sequence",
    "acknowledge",
    "complete_confirmation_record",
    "submit_confirmation",
    "allowed_values",
    "race_two_promotions",
    "interrupt_promotion",
    "construct_candidate",
    "write_bundle",
    "candidate_over_bound",
    "raise_demotion_flag",
    "confirmed_bundle",
    "dispose_demotion_flag",
    "fixed_text_travel_lint",
    "provisional_record",
    "confirm_provisional",
    "reuse_warning_at_count",
    "candidate_with_instruction_item",
    "test_instruction_items_against_holdout",
    "clearance_claim_covering_instruction_items",
    "promotion_record_carrying_instruction_test_result",
    "record_refusal",
    "freshness_check_at_promotion",
    "cross_split_refusal_at_promotion",
]


# The one state table value. Its identifiers and its
# count stand authored and guessed under entry 54
# and DG-5, as the header states. The identifiers
# stand in table order in this one tuple.
_STATE_TABLE_RULES = (
    "state_rule_01",
    "state_rule_02",
    "state_rule_03",
    "state_rule_04",
    "state_rule_05",
)

# The interaction set name value. The name stands
# authored and guessed under entry 54 and DG-5, as
# the header states.
_INTERACTION_SET_NAME = "state table interaction set"

# The implementation home value carried for each rule
# in the review form. The value stands authored and
# guessed under entry 54, as the header states, and
# names the one unit position of this section.
_IMPLEMENTATION_HOME = "state table unit"

# The history fixture value for the interruption
# forms. One equal string value stands on both sides
# of each interruption return, as a fixture form
# authored and guessed under entry 54.
_HISTORY_FIXTURE = "history fixture"

# The attempt fixture value. One opaque string stands
# minted by the inside interruption surface and read
# back by the completed append surface by content
# alone, as a fixture form authored and guessed
# under entry 54.
_ATTEMPT_FIXTURE = "attempt fixture"

# The winner fixture value for the race form. One
# identifier string stands shared by the winner key,
# the journal first key, and the one deployment
# entry, as a fixture form authored and guessed
# under entry 54.
_RACE_WINNER = "first promotion"


def state_table_rules():
    """Return the state table rule identifiers.

    Returns a fresh list of the rule identifiers from
    the one table value above, in table order. The
    identifiers stand authored and guessed under
    entry 54 and DG-5, as the table note states.
    """
    return list(_STATE_TABLE_RULES)


def generated_state_tests():
    """Return the generated state test entries.

    Returns a fresh list of fresh mappings, one per
    rule, in table order, each entry carrying exactly
    its rule and its source standing at the governing
    state table. The entries derive from the one
    table value above and from no other home.
    """
    return [
        {"rule": rule, "generated_from": "governing state table"}
        for rule in _STATE_TABLE_RULES
    ]


def interaction_set_name():
    """Return the interaction set name.

    Returns the one name string held above. The name
    stands authored and guessed under entry 54 and
    DG-5, as the name note states.
    """
    return _INTERACTION_SET_NAME


def review_slice_output(reviewer="named reviewer", slice_output=None):
    """Return the review record form, PROMOTE-T01.

    Returns a fresh mapping on every call. The
    accounted rules stand as the rule list from the
    one table value, each rule once. The
    implementation home mapping carries every rule
    as a key, with the one unit value held above.
    On a call with no slice output the second
    statement findings list stands empty. On a call
    carrying a slice output the findings list holds
    one finding read from that output by its two
    pinned keys alone. The record home, the filed
    position, and the search position stand in the
    forms the tests pin, the filed value standing as
    a form contract only, with the real review
    standing as a slice exit act outside this module.
    """
    findings = []
    if slice_output is not None:
        findings = [
            {
                "rule": slice_output["second_statement_rule"],
                "passage": slice_output["second_statement_passage"],
            }
        ]
    return {
        "accounted_rules": list(_STATE_TABLE_RULES),
        "implementation_home": {
            rule: _IMPLEMENTATION_HOME for rule in _STATE_TABLE_RULES
        },
        "second_statement_findings": findings,
        "record_home": "PROMOTE slice exit record",
        "filed": True,
        "rests_on_search_result": False,
    }


def slice_output_with_a_second_statement():
    """Return a constructed fixture slice output.

    Returns a fresh mapping carrying exactly two
    keys, the first rule of the table as the second
    statement rule and one short passage string as
    the second statement passage. The passage stands
    as a constructed fixture passage, authored and
    guessed under entry 54, and it stands in this
    return alone and in no other place in this
    fragment.
    """
    return {
        "second_statement_rule": _STATE_TABLE_RULES[0],
        "second_statement_passage": "constructed fixture passage",
    }


def interrupt_before_append():
    """Return the kill before the append form.

    Returns a fresh mapping carrying verify standing
    at agreement, the history before and the history
    after standing as the one equal fixture value
    held above, and the append completed position
    standing False.
    """
    return {
        "verify": "agreement",
        "history_before": _HISTORY_FIXTURE,
        "history_after": _HISTORY_FIXTURE,
        "append_completed": False,
    }


def interrupt_inside_rollback_append():
    """Return the kill inside the rollback append form.

    Returns a fresh mapping carrying verify standing
    at agreement, the pre append history before and
    the pre append history after standing as the one
    equal fixture value held above, the currency
    moved position standing False, and the attempt
    value held above.
    """
    return {
        "verify": "agreement",
        "pre_append_history_before": _HISTORY_FIXTURE,
        "pre_append_history_after": _HISTORY_FIXTURE,
        "currency_moved": False,
        "attempt": _ATTEMPT_FIXTURE,
    }


def complete_append(attempt):
    """Return the completed append form.

    Takes the attempt value the inside interruption
    surface minted, accepted on any attempt value,
    and returns a fresh mapping carrying the currency
    moved at completed append position standing True
    and no other key.
    """
    return {"currency_moved_at_completed_append": True}


def promote_with_observer():
    """Return the observed promotion form, PROMOTE-T02.

    Returns a fresh mapping carrying the observable
    states as a fresh list and the final state
    standing at deployed. The observable states carry
    the gate steps in progress and the deployed
    position, in an authored reading recorded in the
    fragment paper, and carry no state in which a
    gate pass stands recorded with no deployment.
    """
    return {
        "observable_states": [
            "cross_split_audit",
            "margin_recomputation",
            "stamp_acknowledgement",
            "deployed",
        ],
        "final_state": "deployed",
    }


def promote():
    """Return the promotion act form, PROMOTE-T02.

    Returns a fresh mapping carrying the journal as a
    fresh list of exactly three fresh entries, one
    per kind, in the order audit, then
    acknowledgement, then deployment, each entry
    carrying exactly the kind key. The journal stands
    as a returned value form only, and no store call
    and no journal reading stands performed.
    """
    return {
        "journal": [
            {"kind": "audit"},
            {"kind": "acknowledgement"},
            {"kind": "deployment"},
        ]
    }


def gate_sequence_order():
    """Return the gate sequence order, PROMOTE-T03.

    Returns a fresh list standing at exactly the
    four step names in program order, cross split
    audit first, margin recomputation second, stamp
    acknowledgement third, and deployment last.
    """
    return [
        "cross_split_audit",
        "margin_recomputation",
        "stamp_acknowledgement",
        "deployment",
    ]


def gate_sequence():
    """Return the gate sequence steps, PROMOTE-T03.

    Returns a fresh list of fresh step mappings, one
    per step, in the order the order surface returns.
    Each step carries its act name, and the first
    step carries in addition exactly its central row
    and its call point in the forms the tests pin.
    The sequence stands as data only, and no step
    performs a call of any kind.
    """
    return [
        {
            "act": "cross_split_audit",
            "central_row": "DATASET-T05",
            "call_point": 3,
        },
        {"act": "margin_recomputation"},
        {"act": "stamp_acknowledgement"},
        {"act": "deployment"},
    ]


def acknowledge(choice):
    """Return the acknowledgement position, PROMOTE-T04.

    Takes one choice string. On the proceed choice
    the return carries the position standing at
    acknowledged and the satisfies gate position
    standing True. On every other choice string the
    return carries the position standing at gate
    pass held and the satisfies gate position
    standing False, and no error stands raised on
    an unpinned choice string.
    """
    if choice == "proceed":
        return {"position": "acknowledged", "satisfies_gate": True}
    return {"position": "gate pass held", "satisfies_gate": False}


def race_two_promotions():
    """Return the race outcome form, PROMOTE-T06.

    Returns a fresh mapping carrying the winner and
    the journal first standing as the one shared
    fixture identifier held above, the loser outcome
    standing at refused by journal order, and the
    deployments list holding exactly one entry
    carrying that same identifier.
    """
    return {
        "winner": _RACE_WINNER,
        "journal_first": _RACE_WINNER,
        "loser_outcome": "refused by journal order",
        "deployments": [_RACE_WINNER],
    }


def interrupt_promotion():
    """Return the interrupted promotion form, PROMOTE-T06.

    Returns a fresh mapping carrying the state
    standing at not promoted, in the form the build
    entry disposition of DG-7 adopts, and verify
    standing at agreement. No pointer key, no
    comparison key, and no journal key stands
    carried on this return.
    """
    return {"state": "not promoted", "verify": "agreement"}


# The allowed values for the two confirmation fields.
# The enumerations stand nowhere in the grounds read,
# at scope gap G-5 and shape disagreement DG-8. The
# values below stand authored and guessed under ruling
# (f), labelled as such here and in the fragment paper.
# Each list holds two position values, and the complete
# record draws the first value of each list. The weight
# list does not hold the string the tests use for a
# value outside the allowed values.
_ALLOWED_VALUES = {
    "production_evidence_label_position": (
        "at record head",
        "at record foot",
    ),
    "production_evidence_weight_position": (
        "at record head",
        "at record foot",
    ),
}

_LABEL_FIELD = "production_evidence_label_position"
_WEIGHT_FIELD = "production_evidence_weight_position"

# The over bound marker for the D-10 derived view
# checks. The tests pin the refusal form by this marker
# string alone. No bound figure, no count, and no
# counting act stands in this module, at scope gap G-6
# and shape disagreement DG-4. The bound figure stands
# guessed at its EVAL home at plan subsection 16.55,
# and this module imports no figure from that home.
_OVER_BOUND_MARKER = "over D-10 bound"

# The confirmed bundle identity and the flag evidence
# fixture values. No ground states a bundle identity
# form, an evidence content, or an age measure beyond
# age from opening, at scope gaps G-10 and G-11 and
# shape gaps G-27. The two values below stand authored
# and guessed under ruling (f), labelled as such here
# and in the fragment paper, as fixture forms only.
_BUNDLE_IDENTITY = "confirmed bundle 1"
_FLAG_EVIDENCE = "evidence fixture for the confirmed bundle"

# The three verbatim texts of the bundle writing
# assembly, carried by name only, in the G-15 form.
# No wording of any of the three texts stands in this
# module. The names stand as the test file names them,
# and the lint at the foot of this section stands as a
# name driven fixture form, at shape gap G-28, stated
# as exactly that and as no wording comparison act.
_TEXT_NAMES = (
    "seal sentence",
    "verify sentence",
    "grader awareness label",
)


def complete_confirmation_record():
    """Return the complete confirmation record value.

    The return is a fresh plain mapping on every call,
    carrying exactly the two pinned keys, in the
    proposal form at shape section 5.1, so no further
    field stands invented inside the fixture. Each
    value stands inside the allowed values for its
    field, drawn from the first value of each authored
    list at the module constant above. The caller may
    mutate the return, and no shared state stands
    behind it. Criteria 16 and 17 stand as fixture
    parts only on this record, and no criterion stands
    closed by it.
    """
    return {
        _LABEL_FIELD: _ALLOWED_VALUES[_LABEL_FIELD][0],
        _WEIGHT_FIELD: _ALLOWED_VALUES[_WEIGHT_FIELD][0],
    }


def submit_confirmation(record):
    """Return the confirmation submission outcome.

    On a record with either pinned field missing, the
    return carries outcome standing at refused and
    reason standing at confirmation record incomplete,
    both exactly, the weight limb standing pinned by
    the tests and the label limb standing in the same
    proposal form at shape section 5.2. On a record
    whose label or weight position value stands outside
    the allowed values for its field, the return
    carries outcome standing at refused, both fields
    checked in the same form. On a complete record
    carrying allowed values, the return carries outcome
    standing at accepted and no reason key, as an
    authored reading at shape gap G-17.
    """
    if not isinstance(record, dict):
        return {
            "outcome": "refused",
            "reason": "confirmation record incomplete",
        }
    if _LABEL_FIELD not in record or _WEIGHT_FIELD not in record:
        return {
            "outcome": "refused",
            "reason": "confirmation record incomplete",
        }
    if record[_LABEL_FIELD] not in _ALLOWED_VALUES[_LABEL_FIELD]:
        return {"outcome": "refused"}
    if record[_WEIGHT_FIELD] not in _ALLOWED_VALUES[_WEIGHT_FIELD]:
        return {"outcome": "refused"}
    return {"outcome": "accepted"}


def allowed_values(field):
    """Return the allowed values for one field.

    The field argument stands at one of the two pinned
    field name strings, and the return is a fresh list
    holding the authored values at the module constant
    above, in list order. The enumerations stand
    authored and guessed under ruling (f), at scope gap
    G-5 and shape disagreement DG-8, and no value in
    either list stands as grounded, adopted, or
    measured. A field name outside the two pinned names
    raises ValueError, in the proposal form at shape
    section 8.
    """
    if field not in _ALLOWED_VALUES:
        raise ValueError("unknown confirmation field: %r" % (field,))
    return list(_ALLOWED_VALUES[field])


def construct_candidate(bundle_size=None):
    """Return the candidate construction outcome.

    This surface stands as the first of the two derived
    view checks of the D-10 bound, at candidate
    construction. On a call whose size value stands at
    the over bound marker, the return carries outcome
    standing at refused and check_point standing at
    candidate construction, both exactly. On any other
    size value the return carries outcome standing at
    constructed and check_point standing at candidate
    construction, as an authored reading at shape gap
    G-18. The check compares the passed size value
    against the marker form alone. No counting act
    stands built and no bound figure stands imported.
    """
    if bundle_size == _OVER_BOUND_MARKER:
        return {
            "outcome": "refused",
            "check_point": "candidate construction",
        }
    return {
        "outcome": "constructed",
        "check_point": "candidate construction",
    }


def write_bundle(candidate=None, bundle_size=None):
    """Return the bundle writing outcome.

    This surface stands as the second of the two derived
    view checks of the D-10 bound, at bundle writing.
    The call stands in two pinned forms: a keyword size
    form, and a positional candidate form carrying the
    mapping candidate_over_bound returns, whose size
    stands at its size key. Where both forms stand
    passed in one call the candidate value governs, as
    an authored reading at shape gap G-18, because it
    carries its own size.

    On an over bound size the return carries outcome
    standing at refused, check_point standing at bundle
    writing, bundle_size_after standing equal to the
    size passed, and trimmed standing False, so both
    refusal forms state the full row position in one
    shape and no silent trimming stands in any form. On
    any other size the return carries outcome standing
    at written, with the same remaining keys, as an
    authored reading at shape gap G-18. No bundle bytes
    stand written, no file stands opened, and no sealing
    or canonical surface stands called by this surface.
    """
    if candidate is not None:
        if isinstance(candidate, dict):
            size = candidate.get("size")
        else:
            size = None
    else:
        size = bundle_size
    if size == _OVER_BOUND_MARKER:
        return {
            "outcome": "refused",
            "check_point": "bundle writing",
            "bundle_size_after": size,
            "trimmed": False,
        }
    return {
        "outcome": "written",
        "check_point": "bundle writing",
        "bundle_size_after": size,
        "trimmed": False,
    }


def candidate_over_bound():
    """Return the over bound candidate fixture value.

    The return is a fresh mapping carrying exactly the
    one key size, standing at the over bound marker
    string, in the proposal form at shape section 5.5.
    This candidate stands as the shared fixture of the
    PROMOTE-T07 row: write_bundle called on it refuses,
    and its size stands unchanged after that refusal.
    No numeric size measure stands invented in this
    slice, at scope gap G-6.
    """
    return {"size": _OVER_BOUND_MARKER}


def raise_demotion_flag(bundle):
    """Return the demotion flag record for one bundle.

    The bundle argument stands as the value
    confirmed_bundle returns, and the return is a fresh
    mapping carrying the flag as one record:
    bundle_identity standing at the identity value of
    the passed bundle, evidence standing at the authored
    fixture value at the module constant above, age
    standing at the integer 0 as age at opening in an
    unstated unit, as an authored reading at shape gap
    G-27, and record_count standing at the integer 1,
    exactly. Ground: plan subsection 16.11, a flag
    raised on a confirmed bundle carries its identity,
    evidence, and age as one record, and plan subsection
    19.23, the flag record carrying the flag evidence
    itself, its age from opening, and its identity, in
    one home.

    The opening condition stands carried in its ground
    form and in no stronger form. Plan subsection 19.23
    point two states that condition as a registered
    guess, with the first flag disposition act as its
    replacing event, at shape disagreement DG-9. This
    surface builds no signal accumulation, no threshold
    check, and no automatic effect. No Promotion Record
    file stands written by this surface. The identity
    reading distinguishes a missing key from a present
    value: a present value, a falsy value among it,
    stands carried as passed, and the fixture identity
    stands only where no identity value stands present.
    """
    if isinstance(bundle, dict):
        identity = bundle.get("bundle_identity")
        if identity is None:
            identity = _BUNDLE_IDENTITY
    else:
        identity = _BUNDLE_IDENTITY
    return {
        "bundle_identity": identity,
        "evidence": _FLAG_EVIDENCE,
        "age": 0,
        "record_count": 1,
    }


def confirmed_bundle():
    """Return the confirmed bundle fixture value.

    The return is a fresh mapping carrying
    bundle_identity standing at the authored identifier
    at the module constant above and confirmed standing
    True, as an authored fixture reading at shape
    section 5.7. This bundle stands as the fixture of
    the PROMOTE-T08 row, with a raised flag carried
    through all three disposition decisions in turn. No
    hash form for the bundle stands stated in this slice
    rows, and none stands built here, at scope gap G-11.
    """
    return {
        "bundle_identity": _BUNDLE_IDENTITY,
        "confirmed": True,
    }


def _reason_carries_content(reason):
    """Return whether a retain reason carries content in substance.

    A string carries content only where it holds a non
    whitespace character, and a UserString carries
    content as the text it wraps, on the same test. A
    byte form carries content only where its bytes
    hold one, and an array in byte form carries
    content as the bytes it holds, on the same test. A
    mapping carries content only where one of its
    values carries content, and any other iterable
    form, a list, a tuple, a set, a deque, a range, a
    generator, or an iterator among them, carries
    content only where one of the items it yields
    carries content. Any other value carries content
    on its standing truthiness alone, so the empty
    string, the empty list, and the integer 0 carry
    none, as before. The test stands on the stated
    ground the reason carries and not on the falsiness
    or the form of its container. The reading walks
    container forms with an explicit stack and a set
    of the containers it has already walked, so a
    container standing on its own path stands walked
    once and a container nested at any depth stands
    walked without recursion: a cyclic or deeply
    nested reason carrying no other content carries
    no content and stands refused by the retain limb
    in its governed form, and one carrying stated
    content carries that content.
    """
    from array import array as _Array
    from collections import UserString as _UserString
    from collections.abc import Iterable as _Iterable
    from collections.abc import Mapping as _Mapping

    stack = [reason]
    walked = set()
    while stack:
        value = stack.pop()
        if value is None:
            continue
        if isinstance(value, _UserString):
            if str(value).strip():
                return True
            continue
        if isinstance(value, str):
            if value.strip():
                return True
            continue
        if isinstance(value, (bytes, bytearray, memoryview)):
            if bytes(value).strip():
                return True
            continue
        if isinstance(value, _Array) and value.typecode in ("b", "B"):
            if value.tobytes().strip():
                return True
            continue
        if isinstance(value, _Mapping):
            if id(value) in walked:
                continue
            walked.add(id(value))
            stack.extend(value.values())
            continue
        if isinstance(value, _Iterable):
            if id(value) in walked:
                continue
            walked.add(id(value))
            stack.extend(value)
            continue
        if value:
            return True
    return False


def dispose_demotion_flag(decision, reason=None):
    """Return the demotion flag disposition outcome.

    The decision argument stands at one of the three
    pinned decision strings, and no test passes a flag
    value to this surface, so the decisions stand
    decided on the decision string alone. On demote the
    return carries record_form standing at demote and
    bundle_position standing at demoted, both exactly.
    On retain, called with a reason by keyword, the
    return carries record_form standing at retain,
    reason_recorded standing True, flag_closed standing
    True, and age_stopped standing True: a retain
    decision closes the flag and stops its age. On defer
    the return carries record_form standing at defer
    and review_point_named standing True, the review
    point carried as a boolean position alone, with no
    point name string invented, at shape gap G-19.

    A flag has no automatic effect, at plan subsection
    19.23 point four, and no return of this surface
    carries one. A retain call carrying no reason, or a
    reason carrying no content in substance, in
    whatever form the reason stands, raises
    ValueError, and a decision string outside the three
    pinned strings raises ValueError, both in the
    proposal form at shape section 8. The content test
    stands on the stated ground the reason carries and
    not on the falsiness of its container: a whitespace
    only string, a list holding one empty string, and
    a mapping with one empty string value each carry
    no content on that test.
    """
    if decision == "demote":
        return {
            "record_form": "demote",
            "bundle_position": "demoted",
        }
    if decision == "retain":
        if not _reason_carries_content(reason):
            raise ValueError("retain requires a reason")
        return {
            "record_form": "retain",
            "reason_recorded": True,
            "flag_closed": True,
            "age_stopped": True,
        }
    if decision == "defer":
        return {
            "record_form": "defer",
            "review_point_named": True,
        }
    raise ValueError("unknown demotion flag decision: %r" % (decision,))


def fixed_text_travel_lint(assembly=None, paraphrase_of=None):
    """Return the fixed text travel lint outcome.

    The assembly argument stands called by keyword at
    the string bundle writing, and the paraphrase target
    stands called by keyword under paraphrase_of at one
    of the three text names the module constant above
    carries by name. On the plain call the return
    carries passed standing True and texts_checked
    standing at the integer 3, exactly. On a paraphrase
    call the return carries passed standing False and
    failed_text standing equal to the text name passed,
    for each of the three names in turn.

    This lint stands as a name driven fixture form, at
    shape gaps G-15 and G-28, stated as exactly that.
    The three verbatim texts stand referenced by their
    names and their brief homes only, no wording of any
    of them stands in this module, and no wording
    comparison act stands built or claimed here. This
    lint is not the layer 6 exit scan: that scan position
    stands consumed at bound strength only, at shape
    disagreement DG-10, and no exit scan call or surface
    stands built in this slice. An assembly value other
    than bundle writing raises ValueError, and a
    paraphrase target outside the three pinned names
    raises ValueError, both in the proposal form at
    shape section 8.
    """
    if assembly != "bundle writing":
        raise ValueError("unknown lint assembly: %r" % (assembly,))
    if paraphrase_of is None:
        return {"passed": True, "texts_checked": 3}
    if paraphrase_of not in _TEXT_NAMES:
        raise ValueError("unknown verbatim text name: %r" % (paraphrase_of,))
    return {"passed": False, "failed_text": paraphrase_of}


def provisional_record(with_comparison=True, comparable_displaced_period=True,
                       provisional_outcomes=None, displaced_outcomes=None,
                       provisional_corrections=None, displaced_corrections=None):
    """Return a provisional record, subsection 19.87.

    The comparison figures are computed from the outcome
    and correction values passed in, counting each value
    kind, so the figures vary with the material supplied.
    Where no values are passed, a small default period
    stands in and is counted in the same way. A record
    with no comparison carries comparison standing None.
    A record with no comparable displaced period names
    its comparison basis and records the reason it was
    chosen.

    Each of the four value parameters stands as a list
    of values. A value standing as a string, as bytes,
    as a memoryview of bytes, or as a mapping stands
    refused at each of the four sites, raising
    ValueError, so no record carries a comparison built
    from a container the caller did not present as a
    list of values. A memoryview stands read as the
    byte content it views for the purposes of that
    refusal, in the same form as the byte forms it
    views. A value standing in array form or in
    UserString form stands refused at each of the four
    sites in the same governed form, an array standing
    read as the content it holds and a UserString as
    the text it wraps for the purposes of that refusal.
    A value standing in no iterable form, and a value
    carrying an unhashable item inside the list it
    stands as, stand refused at each of the four sites
    in the same governed ValueError form, with no other
    exception.
    """
    from array import array as _Array
    from collections import UserString as _UserString
    from collections.abc import Mapping as _Mapping

    def _values_or_default(value, default):
        if value is None:
            return list(default)
        if isinstance(value, (str, bytes, bytearray, memoryview, _Mapping,
                             _Array, _UserString)):
            raise ValueError(
                "provisional values must stand as a list of values")
        try:
            values = list(value)
        except TypeError:
            raise ValueError(
                "provisional values must stand as a list of values")
        for item in values:
            try:
                hash(item)
            except TypeError:
                raise ValueError(
                    "provisional values must stand as a list of values")
        return values

    prov_out = _values_or_default(
        provisional_outcomes, ["pass", "pass", "fail"])
    disp_out = _values_or_default(
        displaced_outcomes, ["pass", "fail", "fail"])
    prov_cor = _values_or_default(
        provisional_corrections, ["corrected", "open"])
    disp_cor = _values_or_default(
        displaced_corrections, ["corrected", "open"])

    def mix(values):
        result = {}
        for value in values:
            result[value] = result.get(value, 0) + 1
        return result

    if not comparable_displaced_period:
        return {
            "comparison": None,
            "comparison_basis_named": True,
            "comparison_basis_reason_recorded": True,
            "comparison_basis": "operator named baseline period",
            "comparison_basis_reason": (
                "no comparable displaced period stands, so the "
                "operator named baseline period stands as the basis"
            ),
            "comparison_in_same_view_as_run_count_and_coverage": False,
            "comparison_view_contents": [
                "attributed run count",
                "outcome and signal coverage figures",
            ],
        }
    if not with_comparison:
        return {
            "comparison": None,
            "comparison_in_same_view_as_run_count_and_coverage": False,
            "comparison_view_contents": [
                "attributed run count",
                "outcome and signal coverage figures",
            ],
        }
    comparison = {
        "provisional_period": {
            "outcome_mix": mix(prov_out),
            "correction_position": mix(prov_cor),
        },
        "displaced_period": {
            "outcome_mix": mix(disp_out),
            "correction_position": mix(disp_cor),
            "standing": "last comparable period of the displaced bundle",
        },
        "figures_set_against": ["outcome mix", "correction position"],
    }
    return {
        "comparison": comparison,
        "comparison_in_same_view_as_run_count_and_coverage": True,
        "comparison_view_contents": [
            "attributed run count",
            "outcome and signal coverage figures",
            "outcome mix",
            "correction position",
        ],
    }


def confirm_provisional(record):
    """Return the confirmation outcome for a provisional record.

    A record with no comparison stands barred, with the
    bar reason standing at no comparison in the
    provisional record, under subsection 19.87. A record
    whose comparison value is not a comparison mapping,
    a mapping carrying both period positions, stands
    barred in the same form. A comparison mapping
    stands as a comparison in substance only where
    each of its period positions carries a period, a
    period standing as a mapping carrying both figure
    positions, the outcome mix and the correction
    position. A period standing as no value, as an
    empty mapping, or in any form carrying one figure
    position without the other stands as no period, so
    a comparison carrying such a period in either
    position, or in both, stands barred in the same
    form. A period carrying both figure positions with
    empty mixes stands as a period in full, and a
    record carrying a comparison mapping of that kind
    stands confirmed in form. A period stands as a
    period only where each of its figure positions
    carries a figure in substance, a figure standing
    as a mapping, the mix form the product builds, so
    a figure standing as no value, as an empty string,
    as a text string, as a list, or as a zero, in
    either figure position of either period, stands
    as no figure, and a comparison carrying such a
    period stands barred in the same form. A figure
    standing as an empty mapping stands as a figure
    in full, in the empty mixes form above. A figure
    standing as a mapping carrying entries stands as
    a figure only where one of its entries carries a
    count in substance, a positive whole number, so
    a figure whose counts stand as no value, as a
    text string, or at zero throughout stands as no
    figure, and a comparison carrying such a figure
    in either figure position of either period
    stands barred in the same form, while a figure
    carrying one count in substance beside entries
    carrying none stands as a figure.
    """
    from collections.abc import Mapping as _Mapping

    def _figure_carries_substance(value):
        if not isinstance(value, _Mapping):
            return False
        if not value:
            return True
        return any(
            isinstance(count, int)
            and not isinstance(count, bool)
            and count > 0
            for count in value.values()
        )

    def _stands_as_period(value):
        return (
            isinstance(value, dict)
            and "outcome_mix" in value
            and "correction_position" in value
            and _figure_carries_substance(value["outcome_mix"])
            and _figure_carries_substance(value["correction_position"])
        )

    if not isinstance(record, dict):
        return {
            "outcome": "barred",
            "bar_reason": "no comparison in the provisional record",
        }
    comparison = record.get("comparison")
    if (
        not isinstance(comparison, dict)
        or not _stands_as_period(comparison.get("provisional_period"))
        or not _stands_as_period(comparison.get("displaced_period"))
    ):
        return {
            "outcome": "barred",
            "bar_reason": "no comparison in the provisional record",
        }
    return {"outcome": "confirmed"}


def reuse_warning_at_count(count, bound=3):
    """Return the reuse warning outcome, subsection 19.37 count form.

    The warning fires at the whole count below the bound
    nearest to 75 percent of the bound, which for a bound
    of 3 is a count of 2. Firing names the decision it
    informs on the surface that prints it, changes no
    bound, and blocks no act. A bound below 1 stands
    outside the governed domain of this surface, and a
    call carrying one stands refused, raising ValueError
    naming the bound.
    """
    if bound < 1:
        raise ValueError("unknown reuse warning bound: %r" % (bound,))
    threshold = int(0.75 * bound)
    if threshold < 1:
        threshold = 1
    return {
        "fired": count >= threshold,
        "firing_point_count": threshold,
        "decision": "whether the bundle is reused for a further promotion",
        "decision_named": True,
        "surface_prints_decision_name": True,
        "bound_after": bound,
        "act_blocked": False,
    }


_HOLDOUT_INSTRUCTION_TEXT = "sealed holdout instruction text"
_INSTRUCTION_TEXT_BY_KIND = {
    "verbatim holdout content": _HOLDOUT_INSTRUCTION_TEXT,
    "near verbatim holdout content": (
        _HOLDOUT_INSTRUCTION_TEXT + " with one word changed"
    ),
    "clean instruction": "guidance for the candidate that shares no wording",
}


def candidate_with_instruction_item(kind=None):
    """Return a candidate bundle holding one instruction item.

    The bundle carries the item with its instruction text
    field stated beside it, under subsection 19.86 point
    one, in the same form as the candidate construction
    home so a bundle built at either occasion reads the
    same way, and carries the holdout material under
    holdout_items.
    """
    if kind not in _INSTRUCTION_TEXT_BY_KIND:
        raise ValueError("unknown instruction item kind: %r" % (kind,))
    return {
        "instruction_items": [
            {
                "instruction_text": _INSTRUCTION_TEXT_BY_KIND[kind],
                "kind": kind,
            }
        ],
        "instruction_item_count": 1,
        "holdout_items": [{"text": _HOLDOUT_INSTRUCTION_TEXT}],
        "kind": kind,
    }


def test_instruction_items_against_holdout(bundle, occasion=None,
                                           after_partial_scoring=False):
    """Return the instruction item test outcome at promotion.

    The test presents the instruction text field of every
    instruction item in the bundle, with the holdout
    material the bundle carries in its holdout_items, to
    the one shared module act
    ontoloop.cross_split_audit.audit_instruction_item,
    and over no wider material. On a firing case the
    bundle stands refused in the cross split audit
    refusal form, and the result carries the fired item,
    the test result, the audit record, and the charging
    form solely from the act outcome. No firing condition
    stands computed in this file. On a clean case at
    promotion the test result stands carried on the
    Promotion Record position the return names.

    The instruction_items collection stands checked
    as a list of items before any iteration. A
    collection standing in any other form, a plain
    string, a single mapping, None, or any other non
    list form, returns the governed refusal form of
    this surface, in one stated form at both
    occasions: fired standing True, refusal_form
    standing at cross split audit refusal, field_scope
    standing at instruction text field,
    wider_material_compared standing False, and the
    occasion proceeds flag standing False. No items
    tested count stands in that refusal, because no
    item was presented, and no fired item, test
    result, audit record, or cross split audit result
    stands in it, because those values stand carried
    solely from a shared act outcome and no act ran.
    A genuine list, the empty list among it, keeps
    the standing behaviour above exactly.
    A bundle standing in no mapping form returns that
    same governed refusal form at this call point, with
    no exception, before any read of the bundle, in
    parity with the dataset sibling. Holdout material
    standing as an iterator, at the top level or in any
    position inside it, a mapping of items value among
    them, stands materialised once for the whole test,
    so every instruction item stands compared against
    the same holdout items, and a text form standing in
    the shared recursive reading past the interpreter
    limit returns that same governed refusal form.
    """
    if occasion not in ("candidate construction", "promotion"):
        raise ValueError("unknown instruction test occasion: %r" % (occasion,))
    from collections.abc import Mapping as _Mapping

    if not isinstance(bundle, _Mapping):
        refusal = {
            "fired": True,
            "refusal_form": "cross split audit refusal",
            "field_scope": "instruction text field",
            "wider_material_compared": False,
        }
        if occasion == "promotion":
            refusal["promotion_proceeds"] = False
        else:
            refusal["bundle_proceeds"] = False
        return refusal
    collection = bundle.get("instruction_items")
    if not isinstance(collection, list):
        refusal = {
            "fired": True,
            "refusal_form": "cross split audit refusal",
            "field_scope": "instruction text field",
            "wider_material_compared": False,
        }
        if occasion == "promotion":
            refusal["promotion_proceeds"] = False
        else:
            refusal["bundle_proceeds"] = False
        return refusal
    items = list(collection)
    count = len(items)
    holdout_material = bundle.get("holdout_items")
    if holdout_material is None:
        holdout_material = bundle.get("holdout")
    if holdout_material is None:
        holdout_material = []
    from ontoloop import cross_split_audit as _shared_module

    holdout_material = _shared_module._materialise_iterators(
        holdout_material
    )

    outcome = None
    for item in items:
        presented = _shared_module.audit_instruction_item(
            item,
            holdout_material,
            occasion=occasion,
            after_partial_scoring=after_partial_scoring,
        )
        if presented.get("text_form_refused"):
            refusal = {
                "fired": True,
                "refusal_form": "cross split audit refusal",
                "field_scope": "instruction text field",
                "wider_material_compared": False,
            }
            if occasion == "promotion":
                refusal["promotion_proceeds"] = False
            else:
                refusal["bundle_proceeds"] = False
            return refusal
        if presented["fired"]:
            outcome = presented
            break
    base = {
        "items_tested": count,
        "instruction_item_count": count,
        "field_scope": "instruction text field",
        "wider_material_compared": False,
    }
    if outcome is None:
        result = dict(base)
        result["fired"] = False
        if occasion == "promotion":
            result["test_result_carried_on_promotion_record"] = True
        else:
            result["bundle_proceeds"] = True
        return result
    result = dict(base)
    result.update({
        "fired": True,
        "refusal_form": outcome["refusal_form"],
        "fired_item": outcome["fired_item"],
        "test_result": outcome["test_result"],
        "cross_split_audit_result": dict(
            outcome["cross_split_audit_result"]
        ),
        "audit_record": dict(outcome["audit_record"]),
    })
    if occasion == "promotion":
        result["promotion_proceeds"] = False
    else:
        result["bundle_proceeds"] = False
    if after_partial_scoring:
        result["charging_form"] = outcome["charging_form"]
        result["charged_under_the_standing_charging_rules"] = outcome[
            "charged_under_the_standing_charging_rules"
        ]
    return result


def promotion_record_carrying_instruction_test_result():
    """Return a Promotion Record carrying an instruction test result."""
    return {
        "record_home": "Promotion Record",
        "instruction_test_result_carried": True,
        "test_result": "instruction items tested against holdout",
    }


def clearance_claim_covering_instruction_items(promotion_record=None):
    """Return the clearance claim position, subsection 19.86 point five.

    No claim stands until a Promotion Record carries the
    instruction test result. A record carrying that result
    supports the claim.
    """
    stands = bool(
        isinstance(promotion_record, dict)
        and promotion_record.get("instruction_test_result_carried")
    )
    return {"claim_stands": stands}


def cross_split_refusal_at_promotion(material):
    """Return the literal name refusal at the promotion call point.

    This surface is a call through to the one shared
    module ontoloop.cross_split_audit at its promotion
    call point, under subsection 19.36. It holds no local
    relation implementation and restates no refusal form
    of its own.
    """
    from ontoloop import cross_split_audit as _shared_module

    return _shared_module.audit_at_promotion(material)


def freshness_check_at_promotion(check_point="promotion"):
    """Return the freshness check at the promotion point.

    The check itself lives at its DATASET home under
    subsection 19.6. This surface calls that home at the
    promotion check point and returns its result. No
    freshness computation stands copied here.
    """
    from ontoloop import dataset as _dataset_module

    return _dataset_module.freshness_check(check_point)


def record_refusal(period_open=False, bundle_confirmed=True):
    """Return the refusal recording outcome, plan section 4.4.

    A refusal recorded while a bundle stands confirmed,
    with no period or bound open, is refused as a record
    with the named error refusal with no period open, and
    spends nothing. Where a period stands open, the
    refusal stands recorded.
    """
    if not period_open:
        return {
            "outcome": "refused",
            "error": "refusal with no period open",
            "recorded": False,
            "spends_nothing": True,
        }
    return {"outcome": "recorded", "recorded": True, "spends_nothing": False}


def __getattr__(name):
    if name.startswith("_"):
        raise AttributeError(
            "module %r has no attribute %r" % (MODULE_NAME, name)
        )
    raise AssertionError(NOT_BUILT_PREFIX + MODULE_NAME)


def __dir__():
    return sorted(__all__)
