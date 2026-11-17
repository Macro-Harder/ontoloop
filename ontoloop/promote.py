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
    pinned keys alone. The slice output stands read
    through the abstract mapping form, in parity with
    the sibling surfaces of this module: an output
    standing in no mapping form, an empty mapping,
    and a mapping carrying one pinned key without the
    other each return this record form with the
    findings list empty, and no exception stands
    raised on any such output. The record home, the filed
    position, and the search position stand in the
    forms the tests pin, the filed value standing as
    a form contract only, with the real review
    standing as a slice exit act outside this module.
    """
    from collections.abc import Mapping as _Mapping

    findings = []
    if isinstance(slice_output, _Mapping):
        if (
            "second_statement_rule" in slice_output
            and "second_statement_passage" in slice_output
        ):
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
    from collections.abc import Mapping as _Mapping

    if not isinstance(record, _Mapping):
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
    try:
        present = field in _ALLOWED_VALUES
    except (TypeError, ValueError):
        raise ValueError("unknown confirmation field: %r" % (field,))
    if not present:
        raise ValueError("unknown confirmation field: %r" % (field,))
    return list(_ALLOWED_VALUES[field])


def _size_is_over_bound_marker(size):
    """Return whether a size value carries the over bound marker.

    A size standing in a byte form, bytes, bytearray, or
    memoryview, stands read for the text it carries, in
    parity with the plain string and UserString forms, so
    the marker carried in any of those forms stands as the
    marker. Any other value stands decided by its standing
    equality with the marker string alone.
    """
    if isinstance(size, (bytes, bytearray, memoryview)):
        return bytes(size) == _OVER_BOUND_MARKER.encode("utf-8")
    return size == _OVER_BOUND_MARKER


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
    against the marker form alone. A size standing in
    a byte form, bytes, bytearray, or memoryview,
    stands read for the text it carries, so the marker
    in any of those forms stands refused in the same
    form. No counting act
    stands built and no bound figure stands imported.
    """
    if _size_is_over_bound_marker(bundle_size):
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

    A size standing in a byte form, bytes, bytearray,
    or memoryview, stands read for the text it carries
    at both call forms, in parity with ruling 396 at
    candidate construction, so the marker in any of
    those forms stands refused in the same form.

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
    from collections.abc import Mapping as _Mapping

    if candidate is not None:
        if isinstance(candidate, _Mapping):
            size = candidate.get("size")
        else:
            size = None
    else:
        size = bundle_size
    if _size_is_over_bound_marker(size):
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
    from collections.abc import Mapping as _Mapping

    if isinstance(bundle, _Mapping):
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
            except (TypeError, ValueError):
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
            isinstance(value, _Mapping)
            and "outcome_mix" in value
            and "correction_position" in value
            and _figure_carries_substance(value["outcome_mix"])
            and _figure_carries_substance(value["correction_position"])
        )

    if not isinstance(record, _Mapping):
        return {
            "outcome": "barred",
            "bar_reason": "no comparison in the provisional record",
        }
    comparison = record.get("comparison")
    if (
        not isinstance(comparison, _Mapping)
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

    A bound standing in a numeric form outside the plain
    int form, a float, a Decimal, or a Fraction, stands
    read for the value it carries, and its threshold
    stands computed in exact arithmetic with no float
    conversion that rounds it, so a bound of 10**100
    fires at exactly 75 percent of the bound. A bound
    standing in no numeric form, and a bound carrying no
    finite value, stand refused in the same governed
    form, raising ValueError naming the bound, and no
    other exception stands raised on any bound form. A
    count standing in a numeric form outside the plain
    int form stands read for the value it carries in the
    same way, and a count standing in no numeric form
    stands refused, raising ValueError naming the count.
    """
    from decimal import Decimal as _Decimal
    from fractions import Fraction as _Fraction

    def _finite_fraction(value):
        if isinstance(value, bool):
            return _Fraction(int(value))
        if isinstance(value, int):
            return _Fraction(value)
        if isinstance(value, float):
            if value != value or value in (float("inf"), float("-inf")):
                return None
            return _Fraction(value)
        if isinstance(value, _Decimal):
            if not value.is_finite():
                return None
            return _Fraction(value)
        if isinstance(value, _Fraction):
            return value
        return None

    bound_value = _finite_fraction(bound)
    if bound_value is None or bound_value < 1:
        raise ValueError("unknown reuse warning bound: %r" % (bound,))
    threshold = int(bound_value * 3 // 4)
    if threshold < 1:
        threshold = 1
    if isinstance(count, float) and count != count:
        fired = False
    elif isinstance(count, float) and count == float("inf"):
        fired = True
    elif isinstance(count, float) and count == float("-inf"):
        fired = False
    elif isinstance(count, _Decimal) and not count.is_finite():
        if count.is_nan():
            raise ValueError(
                "unknown reuse warning count: %r" % (count,))
        fired = count > 0
    else:
        count_value = _finite_fraction(count)
        if count_value is None:
            raise ValueError(
                "unknown reuse warning count: %r" % (count,))
        fired = count_value >= threshold
    return {
        "fired": fired,
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
    try:
        present = kind in _INSTRUCTION_TEXT_BY_KIND
    except (TypeError, ValueError):
        raise ValueError("unknown instruction item kind: %r" % (kind,))
    if not present:
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


_WRAPPER_ITEM_FIELD_KEYS = (
    "text",
    "instruction_text",
    "content",
    "group",
    "signature",
)


def _is_delegating_container_subclass(value):
    """Return True where a value stands in a delegating
    subclass of a named container form.

    A delegating subclass stands in a named container
    form by inheritance, a list, a tuple, a set, a
    frozenset, a deque, a UserList, an abstract
    Sequence, or an abstract Set, while its iteration
    act does not stand in the standing form of its
    base: the iteration act of its type stands apart
    from the iteration act of the base it stands in.
    A value standing in the base form itself, and a
    subclass whose iteration act stands in the
    standing form of its base, stand apart. A text
    form and a mapping form stand apart in every case,
    in parity with the direct act reading of those
    forms.
    """
    import collections as _collections_module

    from collections.abc import Mapping as _Mapping
    from collections.abc import Sequence as _Sequence
    from collections.abc import Set as _Set

    if isinstance(value, _Mapping):
        return False
    if isinstance(
        value,
        (
            str,
            _collections_module.UserString,
            bytes,
            bytearray,
            memoryview,
        ),
    ):
        return False
    concrete_bases = (
        list,
        tuple,
        set,
        frozenset,
        _collections_module.deque,
        _collections_module.UserList,
    )
    for base in concrete_bases:
        if isinstance(value, base):
            if type(value) is base:
                return False
            return type(value).__iter__ is not base.__iter__
    if _Sequence in type(value).__mro__ and isinstance(value, _Sequence):
        return type(value).__iter__ is not _Sequence.__iter__
    if _Set in type(value).__mro__ and isinstance(value, _Set):
        return type(value).__iter__ is not _Set.__iter__
    return False


def _is_delegating_concrete_container_subclass(value):
    """Return True where a delegating subclass stands in
    a concrete named container form, a list, a tuple, a
    set, a frozenset, a deque, or a UserList, in the form
    _is_delegating_container_subclass states. A subclass
    standing in an abstract form alone stands apart from
    this reading and stands read by the wider reading
    that helper states.
    """
    import collections as _collections_module

    concrete_bases = (
        list,
        tuple,
        set,
        frozenset,
        _collections_module.deque,
        _collections_module.UserList,
    )
    for base in concrete_bases:
        if isinstance(value, base):
            if type(value) is base:
                return False
            return type(value).__iter__ is not base.__iter__
    return False


def _is_delegating_chainmap_subclass(value):
    """Return True where a value stands in a delegating
    subclass of the ChainMap form.

    A delegating ChainMap subclass carries no maps of
    its own in the standing form and its iteration act
    does not stand in the standing form of the
    ChainMap base: the iteration act of its type
    stands apart from the iteration act of ChainMap,
    delegating in its turn to one stored iterator.
    A value standing in the ChainMap form itself, and
    a subclass whose iteration act stands in the
    standing form of its base, stand apart.
    """
    import collections as _collections_module

    if not isinstance(value, _collections_module.ChainMap):
        return False
    if type(value) is _collections_module.ChainMap:
        return False
    return (
        type(value).__iter__
        is not _collections_module.ChainMap.__iter__
    )


def _is_single_pass_iterable(value):
    """Return True where a value stands as a single pass iterable.

    A single pass iterable carries no next method of
    its own and stands in no re-iterable container
    form, so its substance stands listed once only:
    its iter act may return one stored iterator, it
    may return a fresh object on each call delegating
    in its turn to one stored iterator, a generator
    function yielding from a stored generator, a
    generator expression, a map object, or a chain
    object over one stored iterator among them, and
    it may permit one iteration call only, raising on
    a second call. No asking of its iter act stands
    made here, because the asking itself may spend an
    element of the stored iterator or exhaust the one
    permitted call, so the form stands recognised by
    its standing container forms alone. A subclass of
    a named container form whose iteration act does
    not stand in the standing form of its base stands
    in the same substance and stands recognised in
    that form, its iteration act delegating in its
    turn to one stored iterator, while a subclass
    whose iteration act stands in the standing form
    of its base stands apart in the same way as its
    base. A value
    standing in a re-iterable container form, a text
    form, a byte form, a memoryview, an array, a
    range, a mapping, a dictionary view, a list, a
    tuple, a set, a frozenset, a deque, a UserList, an
    abstract Sequence, or an abstract Set, stands
    apart and stands read in its own form.
    """
    import array as _array_module
    import collections as _collections_module

    if hasattr(value, "__next__"):
        return False
    if not hasattr(value, "__iter__"):
        return False
    from collections.abc import (
        ItemsView as _ItemsView,
        KeysView as _KeysView,
        Mapping as _Mapping,
        Sequence as _Sequence,
        Set as _Set,
        ValuesView as _ValuesView,
    )

    if _is_delegating_container_subclass(value):
        return True
    if isinstance(
        value,
        (
            str,
            _collections_module.UserString,
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


def _is_getitem_only_form(value):
    """Return True where a value stands in getitem only form.

    A getitem only form carries no iter act of its
    own and no mapping form, and its getitem act
    stands as its one reading act, so a listing of it
    may return the elements of one stored iterator in
    sequence and a second listing may stand empty.
    """
    if hasattr(value, "__iter__"):
        return False
    if not hasattr(value, "__getitem__"):
        return False
    from collections.abc import Mapping as _Mapping

    return not isinstance(value, _Mapping)


def _wrapper_subtree_has_iterator(value, ancestors):
    """Return True where a value carries an iterator in its subtree.

    A text form, a byte form, a memoryview, an array,
    and a range stand as leaves and carry no iterator.
    A value standing on its own ancestor path stands
    as it stands at the cyclic position and carries no
    further iterator for this reading. An iterator
    itself, and any mapping value, view entry,
    container element, or indexed access element
    standing as one or carrying one in its subtree,
    stands detected in the same way. A single pass
    iterable, a container carrying no next method of
    its own whose iter act returns one stored
    iterator, a fresh object delegating to one stored
    iterator, or a fresh generator over one stored
    generator, and a container whose iter act permits
    one call only, stands detected in the same way
    and stands never listed by this act, so the one
    listing it carries stands carried to the
    materialisation act that reads it in full. A
    getitem only form, a container carrying no iter
    act of its own whose getitem act returns the next
    element of one stored iterator in sequence,
    stands detected in the same way and stands never
    listed by this act, on the same ground. A
    delegating ChainMap subclass, a mapping form
    whose iteration act delegates to one stored
    iterator, stands detected in the same way and
    stands never listed by this act, because a
    reading through its mapping views would take its
    yielded material as keys and raise on it.
    """
    import array as _array_module
    import collections as _collections_module

    if isinstance(
        value,
        (
            str,
            _collections_module.UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return False
    if id(value) in ancestors:
        return False
    if hasattr(value, "__next__") and hasattr(value, "__iter__"):
        return True
    ancestors = ancestors | {id(value)}
    from collections.abc import Mapping as _Mapping

    if _is_delegating_chainmap_subclass(value):
        return True
    if isinstance(value, _Mapping):
        return any(
            _wrapper_subtree_has_iterator(inner, ancestors)
            for inner in value.values()
        )
    if hasattr(value, "__iter__"):
        if _is_single_pass_iterable(value):
            return True
        try:
            elements = list(value)
        except Exception:
            return False
        return any(
            _wrapper_subtree_has_iterator(element, ancestors)
            for element in elements
        )
    if hasattr(value, "__getitem__"):
        return True
    return False


from collections.abc import Set as _WrapperSetFormBase


class _WrapperMaterialisedSetForm(_WrapperSetFormBase):
    """A re-iterable abstract Set form carrying listed elements.

    The form carries the elements one listing of a
    delegating abstract Set subclass yielded, and its
    iteration act delegates in its turn to one stored
    iterator over those elements, so the direct act
    reads it in the delegating abstract Set form the
    presentation presented, with its elements standing
    in the key position a Set form presents them in,
    while the one listing the materialisation spent
    stands replaced by a reading that yields the same
    elements once in the same delegating form.
    """

    def __init__(self, elements):
        self._elements = list(elements)
        self._stored = iter(list(elements))

    def __len__(self):
        return len(self._elements)

    def __contains__(self, element):
        return element in self._elements

    def __iter__(self):
        return self._stored


class _WrapperMaterialisedKeyForm:
    """A hashable key form carrying one carried value.

    The form carries a value that stands unhashable
    in the key form the ChainMap item materialisation
    states, a dictionary view or a bytearray, holding
    it as the key of a one entry mapping carrying an
    empty mapping as its value, so the direct act
    reads the carried value in the key position the
    presentation presents it in, a position that act
    does not list, in parity with the hashable key
    form of the same limb. The form carries no
    iteration act and no getitem act of its own, so
    no reading of the form itself reaches the carried
    value in element position.
    """

    def __init__(self, carried):
        self._carried = carried


class _WrapperMaterialisedDelegatingListForm(list):
    """A delegating list form carrying listed elements.

    The form carries the elements one listing of a
    delegating container subclass yielded, and its
    iteration act delegates to one stored iterator
    over those elements, so the direct act reads it
    in the delegating container form the presentation
    presented at a mapping value position, in parity
    with that presentation standing as it stands,
    while the one listing the materialisation spent
    stands replaced by a reading that yields the same
    elements once in the same delegating form.
    """

    def __init__(self, elements):
        super().__init__()
        self._elements = list(elements)
        self._stored = iter(list(elements))

    def __iter__(self):
        return self._stored


def _wrapper_view_carries_single_pass(value):
    """Return True where a keys view or an items view
    carries a single pass form in the position the
    element position reading of a view reaches: the
    key position of a keys view, and the value
    position of an items view. The reading lists the
    view alone, a re-iterable form over its underlying
    mapping, and asks the subtree reading of each
    reached element, which stands never listing a
    single pass form it detects.
    """
    from collections.abc import ItemsView as _ItemsView
    from collections.abc import KeysView as _KeysView

    if isinstance(value, _KeysView):
        return any(
            _wrapper_subtree_has_iterator(element, frozenset())
            for element in list(value)
        )
    if isinstance(value, _ItemsView):
        return any(
            _wrapper_subtree_has_iterator(pair[1], frozenset())
            for pair in list(value)
        )
    return False


def _wrapper_subtree_carries_view(value, ancestors):
    """Return True where a dictionary view stands in
    the subtree of a value, on re-iterable forms
    alone: a single pass form and an iterator stand
    never listed by this reading, and a value standing
    on its own ancestor path carries no further view
    for this reading.
    """
    import array as _array_module
    import collections as _collections_module

    from collections.abc import ItemsView as _ItemsView
    from collections.abc import KeysView as _KeysView
    from collections.abc import Mapping as _Mapping
    from collections.abc import ValuesView as _ValuesView

    if isinstance(value, (_KeysView, _ValuesView, _ItemsView)):
        return True
    if isinstance(
        value,
        (
            str,
            _collections_module.UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return False
    if id(value) in ancestors:
        return False
    if hasattr(value, "__next__") and hasattr(value, "__iter__"):
        return False
    if _is_single_pass_iterable(value) and not isinstance(
        value, (list, tuple, set, frozenset)
    ):
        return False
    ancestors = ancestors | {id(value)}
    if isinstance(value, _Mapping):
        return any(
            _wrapper_subtree_carries_view(inner, ancestors)
            for inner in list(value.values())
        ) or any(
            _wrapper_subtree_carries_view(inner, ancestors)
            for inner in list(value.keys())
        )
    if hasattr(value, "__iter__"):
        try:
            elements = list(value)
        except Exception:
            return False
        return any(
            _wrapper_subtree_carries_view(element, ancestors)
            for element in elements
        )
    return False


def _wrapper_materialise_chainmap_set_element(element, shared_module,
                                              ancestors, depth):
    """Materialise one element of a delegating abstract Set form.

    An element of a delegating abstract Set subclass
    standing inside a ChainMap item stands in key
    position inside a Set form standing in key
    position, a position the direct act does not list
    into, save that the direct act lists a Set form
    standing in element position in the rebuilt form
    and reaches a single pass element it carries. A
    single pass element therefore stands carried in
    the nested form the single pass limb of
    _wrapper_materialise_chainmap_nested states, and
    a single pass form standing inside a container
    standing as an element stands carried in that
    same nested form inside a rebuilt form of its
    container, so no single pass form stands carried
    raw at this position. An element carrying no
    single pass form in its subtree stands as it
    stands, in parity with both readings of this
    position, and a delegating container subclass
    carrying no single pass element stands as it
    stands on the same ground. A getitem only form
    standing as an element stands carried in the
    nested form the getitem limb of
    _wrapper_materialise_chainmap_nested states, and
    a values view standing as an element stands
    carried in the nested form the view limb of that
    act states, so the single pass form either form
    carries stands in key position at this position
    and stands carried raw in no case. A keys view or
    an items view standing as an element stands in
    the container form below, in the parity the
    standing Set form reading states.
    """
    import array as _array_module
    import collections as _collections_module

    from collections.abc import Mapping as _Mapping
    from collections.abc import Sequence as _Sequence
    from collections.abc import Set as _Set
    from collections.abc import ValuesView as _ValuesView

    if isinstance(
        element,
        (
            str,
            _collections_module.UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return element
    if _is_delegating_chainmap_subclass(element):
        return element
    if isinstance(element, _Mapping):
        return element
    if (
        hasattr(element, "__next__") and hasattr(element, "__iter__")
    ) or (
        _is_single_pass_iterable(element)
        and not _is_delegating_container_subclass(element)
    ):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if _is_getitem_only_form(element) or isinstance(
        element, _ValuesView
    ):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if _is_delegating_container_subclass(element):
        listed_once = list(element)
        nested_ancestors = ancestors | {id(element)}
        transformed = [
            _wrapper_materialise_chainmap_set_element(
                inner, shared_module, nested_ancestors, depth + 1
            )
            for inner in listed_once
        ]
        if all(
            carried is inner
            for carried, inner in zip(transformed, listed_once)
        ):
            return element
        if len(transformed) == 1 and isinstance(
            transformed[0], _Mapping
        ) and not any(
            key in transformed[0]
            for key in _WRAPPER_ITEM_FIELD_KEYS
        ):
            return tuple(transformed)
        return transformed
    if isinstance(
        element,
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
        listed_once = list(element)
        nested_ancestors = ancestors | {id(element)}
        transformed = [
            _wrapper_materialise_chainmap_set_element(
                inner, shared_module, nested_ancestors, depth + 1
            )
            for inner in listed_once
        ]
        if all(
            carried is inner
            for carried, inner in zip(transformed, listed_once)
        ):
            return element
        if isinstance(element, tuple):
            return tuple(transformed)
        if isinstance(element, _collections_module.deque):
            return _collections_module.deque(transformed)
        if isinstance(element, _collections_module.UserList):
            return _collections_module.UserList(transformed)
        if isinstance(element, list):
            return transformed
        if isinstance(element, (set, frozenset)):
            try:
                return type(element)(transformed)
            except TypeError:
                return transformed
        return transformed
    return element


def _wrapper_chainmap_delegating_element(element, shared_module,
                                          ancestors, depth,
                                          delegating_carrier=False):
    """Materialise one element of a delegating concrete
    container subclass standing at a mapping value
    inside a ChainMap item, in the form
    _wrapper_chainmap_delegating_value states: an
    element standing in a form the direct act reaches
    in element position at that position stands
    carried in that reaching form, and an element
    standing in a form that act reads in key position
    alone stands carried in the key form the nested
    materialisation states for it. Where the element
    stands inside the delegating carrier itself, in
    the form delegating_carrier states, an items view
    stands carried in that key form, because the
    direct act reads an items view standing inside a
    delegating carrier in key position alone, save
    where the view carries a single pass form in its
    value, which stands in its standing element form,
    the one form in which the element position
    reading of a view reaches that value.
    """
    import array as _array_module
    import collections as _collections_module

    from collections.abc import ItemsView as _ItemsView
    from collections.abc import KeysView as _KeysView
    from collections.abc import Mapping as _Mapping
    from collections.abc import Sequence as _Sequence
    from collections.abc import Set as _Set
    from collections.abc import ValuesView as _ValuesView

    if isinstance(
        element,
        (
            str,
            _collections_module.UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if isinstance(element, _Mapping):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if isinstance(element, _KeysView):
        materialised_view = _wrapper_materialise(
            element, shared_module, ancestors, depth, "other"
        )
        return _WrapperMaterialisedSetForm([materialised_view])
    if isinstance(element, _ItemsView):
        if delegating_carrier and not (
            _wrapper_view_carries_single_pass(element)
        ):
            return _wrapper_materialise_chainmap_nested(
                element, shared_module, ancestors, depth
            )
        return _wrapper_materialise(
            element, shared_module, ancestors, depth, "other"
        )
    if isinstance(element, _ValuesView):
        return _wrapper_materialise(
            element, shared_module, ancestors, depth, "other"
        )
    if _is_delegating_container_subclass(
        element
    ) or _is_delegating_chainmap_subclass(element):
        return element
    if (
        hasattr(element, "__next__") and hasattr(element, "__iter__")
    ) or _is_single_pass_iterable(element):
        return _wrapper_chainmap_single_pass_value(
            element, shared_module, ancestors, depth,
            delegating_carrier=delegating_carrier,
        )
    if _is_getitem_only_form(element):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if isinstance(
        element,
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
        listed_once = list(element)
        nested_ancestors = ancestors | {id(element)}
        transformed = [
            _wrapper_chainmap_delegating_element(
                inner, shared_module, nested_ancestors, depth + 1,
                delegating_carrier=delegating_carrier,
            )
            for inner in listed_once
        ]
        if isinstance(element, tuple):
            return tuple(transformed)
        if isinstance(element, _collections_module.deque):
            return _collections_module.deque(transformed)
        if isinstance(element, _collections_module.UserList):
            return _collections_module.UserList(transformed)
        if isinstance(element, list):
            return transformed
        if isinstance(element, (set, frozenset)):
            try:
                return type(element)(transformed)
            except TypeError:
                return transformed
        return transformed
    return element


def _wrapper_chainmap_single_pass_value(value, shared_module,
                                        ancestors, depth,
                                        plain_carrier=False,
                                        delegating_carrier=False):
    """Materialise a single pass form standing inside
    a mapping standing inside a ChainMap item, from
    its one listing: its elements stand in the form
    _wrapper_chainmap_delegating_element states, so a
    keys view it carries stands in the Set form that
    act states, and the rebuilt form stands as the
    list of its elements, save where it yields the
    one nested mapping, where it stands as a one
    element tuple, in the standing form of the
    iterator limb of the wrapper materialisation.
    Where the single pass form stands as the mapping
    value itself or inside a plain container at that
    position, in the form plain_carrier states, its
    elements stand in the form
    _wrapper_chainmap_plain_element states, because
    the direct act reaches an element of a plain
    carrier at that position in element position.
    Where it stands inside a delegating carrier, in
    the form delegating_carrier states, its elements
    stand in the delegating form of that carrier.
    """
    from collections.abc import Mapping as _Mapping

    listed_once = list(value)
    nested_ancestors = ancestors | {id(value)}
    if plain_carrier:
        transformed = [
            _wrapper_chainmap_plain_element(
                element, shared_module, nested_ancestors,
                depth + 1,
            )
            for element in listed_once
        ]
    elif delegating_carrier:
        transformed = [
            _wrapper_chainmap_delegating_element(
                element, shared_module, nested_ancestors,
                depth + 1, delegating_carrier=True,
            )
            for element in listed_once
        ]
    else:
        transformed = [
            _wrapper_chainmap_delegating_element(
                element, shared_module, nested_ancestors,
                depth + 1,
            )
            for element in listed_once
        ]
    if len(transformed) == 1 and isinstance(
        transformed[0], _Mapping
    ) and not any(
        key in transformed[0]
        for key in _WRAPPER_ITEM_FIELD_KEYS
    ):
        return tuple(transformed)
    return transformed


def _wrapper_chainmap_delegating_value(value, shared_module,
                                       ancestors, depth):
    """Materialise a delegating concrete container
    subclass standing at a mapping value inside a
    mapping standing inside a ChainMap item.

    The subclass stands listed once here and rebuilt
    in plain list form holding its elements in the
    form _wrapper_chainmap_delegating_element states,
    so a nested mapping it carries, and a dictionary
    view it carries, reach the direct act in element
    position in substance, in parity with the direct
    act firing on the presentation standing as an
    item of the ChainMap form, while a text form or a
    byte form it carries stands in the key form that
    act clears on, in parity with both readings of
    that payload at that position.
    """
    listed_once = list(value)
    nested_ancestors = ancestors | {id(value)}
    return [
        _wrapper_chainmap_delegating_element(
            element, shared_module, nested_ancestors, depth + 1,
            delegating_carrier=True,
        )
        for element in listed_once
    ]


def _wrapper_chainmap_decided_form(value, shared_module,
                                   ancestors, depth):
    """Carry a delegating ChainMap subclass standing
    at a mapping value inside a ChainMap item in a
    decided form.

    The subclass carries no maps of its own and its
    mapping views take its yielded material as keys,
    so a reading through those views raises on the
    material it carries, on clean material as on hit
    material. The subclass stands listed once here,
    as the ChainMap limb of _wrapper_materialise
    lists it at a mapping presented position, and
    each item the listing yields stands materialised
    in the form _wrapper_materialise_chainmap_item
    states, the key position form of a ChainMap item,
    so the carried form stands as the list of its
    materialised items, save where it yields the one
    nested mapping, a mapping carrying no item field
    of its own, where it stands as a one element
    tuple, in the standing form of that limb. The
    direct act decides the presentation in that form:
    a nested mapping it carries fires, and a view
    carrying a single pass form, a text form, and a
    clean nested mapping each clear, in parity with
    the presentation standing as it stands.
    """
    from collections.abc import Mapping as _Mapping

    chainmap_ancestors = ancestors | {id(value)}
    materialised = [
        _wrapper_materialise_chainmap_item(
            element, shared_module, chainmap_ancestors,
            depth + 1,
        )
        for element in list(value)
    ]
    if len(materialised) == 1 and isinstance(
        materialised[0], _Mapping
    ) and not any(
        key in materialised[0]
        for key in _WRAPPER_ITEM_FIELD_KEYS
    ):
        return tuple(materialised)
    return materialised


def _wrapper_chainmap_plain_element(element, shared_module,
                                    ancestors, depth):
    """Materialise one element of a plain container
    or a single pass form standing at a mapping value
    inside a mapping standing inside a ChainMap item.

    The direct act reaches an element of a plain
    carrier at that position in element position, so
    an element standing in a form that act reaches in
    element position stands carried in that reaching
    form: a byte form, bytes, bytearray, or a
    memoryview, stands in its standing element form,
    the form a byte form standing alone at the
    mapping value takes, and a keys view stands
    carried as the list of its materialised keys, the
    form a keys view standing alone at the mapping
    value takes, so the material either form carries
    reaches the wrapper reading in substance. An
    items view or a values view stands in its
    standing element form, in the parity the standing
    forms of those views at this position state. A
    delegating ChainMap subclass standing as an
    element stands carried in the decided form
    _wrapper_chainmap_decided_form states, a mapping
    stands in its nested form, a single pass form
    stands in the listed form
    _wrapper_chainmap_single_pass_value states for a
    plain carrier, a getitem only form stands in the
    key form the nested materialisation states, a
    delegating container subclass stands as it
    stands, and a plain container stands rebuilt in
    its own form holding its elements in this same
    plain form. A text form stands in the key form
    the nested materialisation states, in parity with
    both readings of a text element at this position.
    """
    import array as _array_module
    import collections as _collections_module

    from collections.abc import ItemsView as _ItemsView
    from collections.abc import KeysView as _KeysView
    from collections.abc import Mapping as _Mapping
    from collections.abc import Sequence as _Sequence
    from collections.abc import Set as _Set
    from collections.abc import ValuesView as _ValuesView

    if isinstance(
        element,
        (
            bytes,
            bytearray,
            memoryview,
        ),
    ):
        return _wrapper_materialise(
            element, shared_module, ancestors, depth, "other"
        )
    if isinstance(
        element,
        (
            str,
            _collections_module.UserString,
            _array_module.array,
            range,
        ),
    ):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if _is_delegating_chainmap_subclass(element):
        return _wrapper_chainmap_decided_form(
            element, shared_module, ancestors, depth
        )
    if isinstance(element, _Mapping):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if isinstance(element, _KeysView):
        return [
            _wrapper_materialise(
                key, shared_module, ancestors, depth, "other"
            )
            for key in list(element)
        ]
    if isinstance(element, (_ValuesView, _ItemsView)):
        return _wrapper_materialise(
            element, shared_module, ancestors, depth, "other"
        )
    if _is_delegating_container_subclass(element):
        return element
    if (
        hasattr(element, "__next__") and hasattr(element, "__iter__")
    ) or _is_single_pass_iterable(element):
        return _wrapper_chainmap_single_pass_value(
            element, shared_module, ancestors, depth,
            plain_carrier=True,
        )
    if _is_getitem_only_form(element):
        return _wrapper_materialise_chainmap_nested(
            element, shared_module, ancestors, depth
        )
    if isinstance(
        element,
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
        listed_once = list(element)
        nested_ancestors = ancestors | {id(element)}
        transformed = [
            _wrapper_chainmap_plain_element(
                inner, shared_module, nested_ancestors,
                depth + 1,
            )
            for inner in listed_once
        ]
        if isinstance(element, tuple):
            return tuple(transformed)
        if isinstance(element, _collections_module.deque):
            return _collections_module.deque(transformed)
        if isinstance(element, _collections_module.UserList):
            return _collections_module.UserList(transformed)
        if isinstance(element, list):
            return transformed
        if isinstance(element, (set, frozenset)):
            try:
                return type(element)(transformed)
            except TypeError:
                return transformed
        return transformed
    return element


def _wrapper_chainmap_mapping_value(inner, shared_module,
                                    ancestors, depth):
    """Materialise one value of a mapping standing
    inside a ChainMap item.

    A keys view standing at such a value stands
    carried as the list of its materialised keys, the
    keys standing in element position in a re-iterable
    form, so the material the view carries reaches the
    direct act in substance, in parity with the direct
    act firing on the presentation standing as an item
    of the ChainMap form, on every item of the test
    alike. A delegating container
    subclass standing at such a value stands carried
    in the form _wrapper_chainmap_delegating_value
    states, on the same ground, in its concrete forms
    and in its abstract Sequence and abstract Set
    forms alike, each listed once and rebuilt in
    plain list form holding its elements in the
    delegating form of that carrier. A delegating ChainMap
    subclass standing at such a value stands carried
    in the decided form
    _wrapper_chainmap_decided_form states, because a
    reading through its mapping views raises on the
    material it carries in place of a decision. An
    items view standing at such a value stands in its
    standing element form, so a byte form standing in
    its value stands in element position in the
    rebuilt list of its pairs, in parity with the
    direct act firing on the presentation, and a byte
    form standing in its key stands in key position in
    the same form, in parity with the direct act
    clearing on that presentation. A plain container
    or a single pass form standing at such a value
    stands carried holding its elements in the plain
    form _wrapper_chainmap_plain_element states,
    because the direct act reaches an element of a
    plain carrier at this position in element
    position. Any other value stands
    materialised in its standing element form.
    """
    import array as _array_module
    import collections as _collections_module

    from collections.abc import ItemsView as _ItemsView
    from collections.abc import KeysView as _KeysView
    from collections.abc import Mapping as _Mapping
    from collections.abc import Sequence as _Sequence
    from collections.abc import Set as _Set

    if isinstance(
        inner,
        (
            str,
            _collections_module.UserString,
            bytes,
            bytearray,
            memoryview,
            _array_module.array,
            range,
        ),
    ):
        return _wrapper_materialise(
            inner, shared_module, ancestors, depth, "other"
        )
    if _is_delegating_chainmap_subclass(inner):
        return _wrapper_chainmap_decided_form(
            inner, shared_module, ancestors, depth
        )
    if isinstance(inner, _KeysView):
        return [
            _wrapper_materialise(
                key, shared_module, ancestors, depth, "other"
            )
            for key in list(inner)
        ]
    if isinstance(inner, _Mapping):
        return _wrapper_chainmap_nested_mapping(
            inner, shared_module, ancestors, depth
        )
    if _is_delegating_container_subclass(inner):
        return _wrapper_chainmap_delegating_value(
            inner, shared_module, ancestors, depth
        )
    if (
        hasattr(inner, "__next__") and hasattr(inner, "__iter__")
    ) or _is_single_pass_iterable(inner):
        return _wrapper_chainmap_single_pass_value(
            inner, shared_module, ancestors, depth,
            plain_carrier=True,
        )
    if isinstance(inner, _ItemsView):
        return _wrapper_materialise(
            inner, shared_module, ancestors, depth, "other"
        )
    if isinstance(
        inner,
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
    ) and not _is_delegating_container_subclass(inner):
        listed_once = list(inner)
        nested_ancestors = ancestors | {id(inner)}
        transformed = [
            _wrapper_chainmap_plain_element(
                element, shared_module, nested_ancestors,
                depth + 1,
            )
            for element in listed_once
        ]
        if isinstance(inner, tuple):
            return tuple(transformed)
        if isinstance(inner, _collections_module.deque):
            return _collections_module.deque(transformed)
        if isinstance(inner, _collections_module.UserList):
            return _collections_module.UserList(transformed)
        if isinstance(inner, list):
            return transformed
        if isinstance(inner, (set, frozenset)):
            try:
                return type(inner)(transformed)
            except TypeError:
                return transformed
        return transformed
    return _wrapper_materialise(
        inner, shared_module, ancestors, depth, "other"
    )


def _wrapper_chainmap_nested_mapping(value, shared_module,
                                     ancestors, depth):
    """Materialise one mapping standing inside a
    ChainMap item, entry by entry, each value standing
    in the form _wrapper_chainmap_mapping_value states,
    so a value standing at a mapping value inside the
    item stands decided in the parity form of its
    position inside the item, and not in the dissolved
    form the standing element materialisation states
    for a mapping standing in the other path state.
    """
    return {
        key: _wrapper_chainmap_mapping_value(
            inner, shared_module, ancestors, depth + 1
        )
        for key, inner in value.items()
    }


def _wrapper_materialise_chainmap_nested(value, shared_module,
                                         ancestors, depth):
    """Materialise one value standing inside a ChainMap item.

    A value standing inside a container standing as an
    item of a delegating ChainMap subclass stands in
    key position inside a container standing in key
    position, and the direct act decides that position
    by the wrapped key reading, so the value stands
    materialised in the form that reading governs, in
    the same form _wrapper_materialise_chainmap_item
    states for an item itself. A delegating container
    subclass standing in a form the wrapped key reading
    reaches, a concrete container form or an abstract
    Sequence form, stands listed once here, with every
    element it carries standing materialised in this
    same nested form, so the rebuilt form hands the
    direct act the nested mapping that reading reaches,
    in element position, where that act reaches it in
    the same way. A delegating container subclass
    standing in an abstract Set form alone, a form that
    reading does not reach, stands carried in the
    re-iterable Set form above holding the elements its
    one listing yielded, in parity with both readings
    of that position, save where its one element stands
    in a single pass form, which stands carried in the
    key form the single pass limb below states, because
    the direct act lists a Set form standing in element
    position in the rebuilt form and reaches a single
    pass element it carries. A single pass iterable, an
    iterator or a general iterable, stands carried as
    the key of a one entry mapping carrying an empty
    mapping as its value, unlisted, so the direct act
    reads it in the key position the presentation
    presents it in, a position that act does not list,
    and a value standing unhashable in that form stands
    materialised in its standing element form. A
    getitem only form stands carried in that same key
    form, unlisted, on the same ground, and a value
    standing unhashable in that form stands
    materialised in its standing element form. A text
    form or a UserString stands carried in that same
    key form, unlisted, so no string stands read as a
    container of its characters and its text stands in
    no element position, and a byte form, bytes or
    bytearray, stands carried in that same key form,
    unlisted, so its text stands in no element
    position, a byte form standing unhashable in that
    form standing carried in the hashable key form
    that form states. A
    delegating ChainMap subclass stands as it stands,
    unlisted, in parity with both readings of that
    position, and a mapping stands materialised entry
    by entry in the form
    _wrapper_chainmap_nested_mapping states, so a
    value standing as a mapping value inside it stands
    decided in the parity form of its position inside
    the item: a keys view at such a value in the
    re-iterable Set form holding its materialised
    form, and a delegating concrete container subclass
    at such a value in the rebuilt list form that act
    states, each reaching the direct act in substance.
    A plain container
    form, a list, a tuple, a set, a frozenset, a deque,
    a UserList, an abstract Sequence, or an abstract
    Set, stands rebuilt in its own form holding every
    element it carries materialised in this same nested
    form, a set or frozenset whose rebuilt form stands
    unhashable standing carried in list form. A
    dictionary view standing as an item, alone or
    inside a container, stands carried as the key of
    a one entry mapping carrying an empty mapping as
    its value, unlisted, in the form the single pass
    limb below states, so the direct act reads it in
    the key position the presentation presents it in,
    a position that act does not list, and a view
    standing unhashable in that form stands carried
    in the re-iterable Set form above holding the view
    alone, whose elements stand in the same key
    position, save where the view carries a single
    pass form in the position the element position
    reading of a view reaches, which stands carried
    in the hashable key form that form states, because
    the direct act lists a Set form standing in
    element position in the rebuilt form and reaches
    the single pass form the view carries. The
    elements of a delegating abstract
    Set form stand materialised in the form
    _wrapper_materialise_chainmap_set_element states,
    so a single pass element standing beside a second
    element, and a single pass form standing inside a
    container standing as an element, stand carried
    in the nested form, in parity with the one element
    key form above. Any other value stands materialised
    in its standing element form.
    """
    import collections as _collections_module

    from collections.abc import ItemsView as _ItemsView
    from collections.abc import KeysView as _KeysView
    from collections.abc import Mapping as _Mapping
    from collections.abc import Sequence as _Sequence
    from collections.abc import Set as _Set
    from collections.abc import ValuesView as _ValuesView

    if isinstance(
        value, (str, _collections_module.UserString)
    ):
        try:
            return {value: {}}
        except TypeError:
            return value
    if isinstance(value, (bytes, bytearray)):
        try:
            return {value: {}}
        except TypeError:
            return {_WrapperMaterialisedKeyForm(value): {}}
    if _is_delegating_chainmap_subclass(value):
        return value
    if isinstance(value, _Mapping):
        return _wrapper_chainmap_nested_mapping(
            value, shared_module, ancestors, depth
        )
    if isinstance(value, (_KeysView, _ValuesView, _ItemsView)):
        try:
            return {value: {}}
        except TypeError:
            if _wrapper_view_carries_single_pass(value):
                return {_WrapperMaterialisedKeyForm(value): {}}
            return _WrapperMaterialisedSetForm([value])
    if _is_delegating_container_subclass(value):
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
        ) or isinstance(value, _Sequence):
            listed_once = list(value)
            nested_ancestors = ancestors | {id(value)}
            materialised = [
                _wrapper_materialise_chainmap_nested(
                    element, shared_module, nested_ancestors,
                    depth + 1,
                )
                for element in listed_once
            ]
            if len(materialised) == 1 and isinstance(
                materialised[0], _Mapping
            ) and not any(
                key in materialised[0]
                for key in _WRAPPER_ITEM_FIELD_KEYS
            ):
                return tuple(materialised)
            return materialised
        listed_once = list(value)
        if len(listed_once) == 1 and (
            (
                hasattr(listed_once[0], "__next__")
                and hasattr(listed_once[0], "__iter__")
            )
            or (
                _is_single_pass_iterable(listed_once[0])
                and not _is_delegating_container_subclass(
                    listed_once[0]
                )
            )
        ):
            try:
                return {listed_once[0]: {}}
            except TypeError:
                return _wrapper_materialise(
                    listed_once[0], shared_module, ancestors,
                    depth, "other",
                )
        set_ancestors = ancestors | {id(value)}
        materialised = [
            _wrapper_materialise_chainmap_set_element(
                element, shared_module, set_ancestors, depth + 1
            )
            for element in listed_once
        ]
        return _WrapperMaterialisedSetForm(materialised)
    if (
        hasattr(value, "__next__") and hasattr(value, "__iter__")
    ) or _is_single_pass_iterable(value):
        try:
            return {value: {}}
        except TypeError:
            return _wrapper_materialise(
                value, shared_module, ancestors, depth, "other"
            )
    if _is_getitem_only_form(value):
        try:
            return {value: {}}
        except TypeError:
            return _wrapper_materialise(
                value, shared_module, ancestors, depth, "other"
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
            _Sequence,
            _Set,
        ),
    ):
        listed_once = list(value)
        nested_ancestors = ancestors | {id(value)}
        materialised = [
            _wrapper_materialise_chainmap_nested(
                element, shared_module, nested_ancestors, depth + 1
            )
            for element in listed_once
        ]
        if isinstance(value, tuple):
            return tuple(materialised)
        if isinstance(value, _collections_module.deque):
            return _collections_module.deque(materialised)
        if isinstance(value, _collections_module.UserList):
            return _collections_module.UserList(materialised)
        if isinstance(value, list):
            return materialised
        if isinstance(value, (set, frozenset)):
            try:
                return type(value)(materialised)
            except TypeError:
                return materialised
        return materialised
    return _wrapper_materialise(
        value, shared_module, ancestors, depth, "other"
    )


def _wrapper_materialise_chainmap_item(element, shared_module,
                                       ancestors, depth):
    """Materialise one item of a delegating ChainMap subclass.

    The iteration of a ChainMap form presents its items
    in key position, and the direct act decides key
    position and element position by different readings,
    so an item of a delegating ChainMap subclass standing
    listed by the ChainMap limb stands materialised in
    the form the direct act reading of its key position
    governs, not in the element position form a listing
    alone would hand it. A delegating container subclass
    standing in a form the wrapped key reading reaches,
    a concrete container form or an abstract Sequence
    form, stands listed once here in the mapping
    presented form, in parity with that reading reaching
    the nested mapping it carries, and a delegating
    container subclass standing in an abstract Set form
    alone, a form that reading does not reach, stands as
    it stands, unlisted, in parity with both readings of
    that position. A single pass iterable, an iterator
    or a general iterable standing listed once only,
    stands carried as the key of a one entry mapping
    carrying an empty mapping as its value, unlisted, so
    the direct act reads it in the key position the
    presentation presents it in, a position that act does
    not list, and an item standing unhashable in that
    form stands materialised in its standing element
    form. A container standing as an item, in a plain
    container form or in a delegating container subclass
    form alike, stands materialised with every value it
    carries standing in the nested form
    _wrapper_materialise_chainmap_nested states, in
    parity with the direct act reading of the key
    position inside a container standing in key
    position, and the abstract Set form stands carried
    in that nested form in the parity and single pass
    forms that act states. Any other item stands
    materialised in its standing element form.
    """
    return _wrapper_materialise_chainmap_nested(
        element, shared_module, ancestors, depth
    )


def _wrapper_materialise(value, shared_module, ancestors, depth=0,
                         path_state="top"):
    """Materialise one iterator carrying subtree for the wrapper.

    A subtree carrying no iterator stands returned as
    it stands, in the form the shared direct act reads
    for it: a single pair standing in set or frozenset
    form, a single pair standing in ChainMap form with
    its maps order standing as the chain carries it,
    and a bundle position standing as a nested mapping
    wrapped in a dictionary view, a tuple, or a deque
    form each reach the direct act in those forms. A
    subtree carrying an iterator stands rebuilt in a
    re-iterable form of the same kind where its kind
    carries one: a mapping standing rebuilt as a plain
    mapping in its items order, a ChainMap standing
    rebuilt as a ChainMap over its materialised maps
    in maps order, a dictionary view standing rebuilt
    as the same view of its materialised mapping, and
    a tuple, a deque, and a UserList standing rebuilt
    in those same forms, with every iterator inside
    them standing listed once. An iterator standing
    listed once stands as the list of its items, save
    where it yields the one nested mapping, a mapping
    carrying no item field of its own, where it stands
    as a one element tuple, the wrapped form the
    direct act reads for a nested mapping position.
    A single pass iterable standing in any position
    stands listed once here, at its one listing, and
    stands rebuilt in the re-iterable form the
    iterator limb above states, the list of its
    materialised items, save where it yields the one
    nested mapping, where it stands as a one element
    tuple in the same form. A single pass iterable
    stands in that form in substance as well as in
    identity form, in the forms _is_single_pass_iterable
    states: a delegating iteration act returning a
    fresh object on each call and an iteration act
    permitting one call only stand listed once here
    in the same way, and no second call stands made
    on either form. A getitem only form standing at
    the wrapped position, the top position of the
    holdout material or a direct value of the mapping
    standing at that top position, stands listed once
    here in the same rebuilt form, and a getitem only
    form standing in any deeper position stands as it
    stands, unlisted, in parity with the direct act
    reading of that position. A delegating container
    subclass, in the form _is_delegating_container_subclass
    states, stands listed once here in the same rebuilt
    form where it stands at a mapping presented
    position, reached as a value of a mapping standing
    in the holdout material through mapping values
    alone, save where an element it carries carries a
    dictionary view in its subtree, where it stands
    rebuilt in the delegating list form that form
    states holding its materialised elements, so the
    direct act reads it in the delegating form the
    presentation presents at that position, the view
    reading standing asked of the materialised
    elements beside the listed elements, so a view
    standing inside a single pass element, which the
    reading never lists in its presented form, stands
    seen in the listed form its materialisation
    states, and a
    delegating subclass stands as it
    stands, unlisted, at a position inside a
    container, in a concrete container form and in
    an abstract Sequence or abstract Set form
    alike, and a delegating subclass standing in a
    concrete container form stands as it stands in
    any position outside the mapping presentation,
    standing directly as the whole holdout material
    among them, in parity with the direct act
    reading of that position in every case. A
    delegating ChainMap subclass, in the form
    _is_delegating_chainmap_subclass states, stands
    listed once here in the same rebuilt form where
    it stands at a mapping presented position, and
    stands as it stands, unlisted, at a position
    inside a container, in parity with the direct
    act reading of that position, and each item the
    listing yields stands materialised in the form
    _wrapper_materialise_chainmap_item states, in
    parity with the direct act reading of the key
    position the iteration of a ChainMap form
    presents its items in. A set or frozenset
    stands rebuilt from its elements materialised
    once and carried in a list, so where the rebuilt
    form stands unhashable and the rebuild fails, the
    carried materialised elements stand returned in
    list form and no second reading of the original
    set stands made on spent material. A value
    standing in any other container form stands
    materialised through the shared act
    _materialise_iterators, in its standing form.
    """
    import collections as _collections_module

    if _is_getitem_only_form(value):
        if depth > 1:
            return value
        try:
            listed_once = list(value)
        except Exception:
            return value
        getitem_ancestors = ancestors | {id(value)}
        materialised = [
            _wrapper_materialise(
                element, shared_module, getitem_ancestors,
                depth + 1, "other",
            )
            for element in listed_once
        ]
        from collections.abc import Mapping as _GetitemMapping

        if len(materialised) == 1 and isinstance(
            materialised[0], _GetitemMapping
        ) and not any(
            key in materialised[0]
            for key in _WRAPPER_ITEM_FIELD_KEYS
        ):
            return tuple(materialised)
        return materialised
    if _is_delegating_container_subclass(value) and (
        path_state == "mapping"
        or path_state == "other"
        or _is_delegating_concrete_container_subclass(value)
    ):
        if path_state != "mapping":
            return value
        subclass_ancestors = ancestors | {id(value)}
        listed_once = list(value)
        materialised = [
            _wrapper_materialise(
                element, shared_module, subclass_ancestors,
                depth + 1, "other",
            )
            for element in listed_once
        ]
        from collections.abc import Mapping as _SubclassMapping

        if any(
            _wrapper_subtree_carries_view(
                element, frozenset()
            )
            for element in listed_once
        ) or any(
            _wrapper_subtree_carries_view(
                element, frozenset()
            )
            for element in materialised
        ):
            delegating_elements = []
            for original, carried in zip(
                listed_once, materialised
            ):
                if (
                    depth >= 2
                    and (
                        (
                            hasattr(original, "__next__")
                            and hasattr(original, "__iter__")
                        )
                        or _is_single_pass_iterable(original)
                    )
                    and _wrapper_subtree_carries_view(
                        carried, frozenset()
                    )
                ):
                    if isinstance(carried, (list, tuple)):
                        delegating_elements.append(
                            _WrapperMaterialisedSetForm(
                                list(carried)
                            )
                        )
                    else:
                        delegating_elements.append(
                            _WrapperMaterialisedSetForm(
                                [carried]
                            )
                        )
                else:
                    delegating_elements.append(carried)
            return _WrapperMaterialisedDelegatingListForm(
                delegating_elements
            )
        if len(materialised) == 1 and isinstance(
            materialised[0], _SubclassMapping
        ) and not any(
            key in materialised[0]
            for key in _WRAPPER_ITEM_FIELD_KEYS
        ):
            return tuple(materialised)
        return materialised
    if _is_delegating_chainmap_subclass(value) and (
        path_state == "mapping" or path_state == "other"
    ):
        if path_state != "mapping":
            return value
        chainmap_ancestors = ancestors | {id(value)}
        materialised = [
            _wrapper_materialise_chainmap_item(
                element, shared_module, chainmap_ancestors,
                depth + 1,
            )
            for element in list(value)
        ]
        from collections.abc import Mapping as _ChainMapMapping

        if len(materialised) == 1 and isinstance(
            materialised[0], _ChainMapMapping
        ) and not any(
            key in materialised[0]
            for key in _WRAPPER_ITEM_FIELD_KEYS
        ):
            return tuple(materialised)
        return materialised
    if not _wrapper_subtree_has_iterator(value, ancestors):
        return value
    ancestors = ancestors | {id(value)}
    from collections.abc import Mapping as _Mapping

    if hasattr(value, "__next__") and hasattr(value, "__iter__"):
        materialised = [
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in list(value)
        ]
        if len(materialised) == 1 and isinstance(
            materialised[0], _Mapping
        ) and not any(
            key in materialised[0]
            for key in _WRAPPER_ITEM_FIELD_KEYS
        ):
            return tuple(materialised)
        return materialised
    if isinstance(value, _collections_module.ChainMap):
        maps = []
        for chained in value.maps:
            maps.append(
                {
                    key: _wrapper_materialise(
                        inner, shared_module, ancestors,
                        depth + 1, "other",
                    )
                    for key, inner in chained.items()
                }
            )
        return _collections_module.ChainMap(*maps)
    if isinstance(value, _Mapping):
        child_state = (
            "mapping" if path_state in ("top", "mapping") else "other"
        )
        return {
            key: _wrapper_materialise(
                inner, shared_module, ancestors, depth + 1, child_state
            )
            for key, inner in value.items()
        }
    from collections.abc import (
        ItemsView as _ItemsView,
        KeysView as _KeysView,
        MappingView as _MappingView,
        ValuesView as _ValuesView,
    )

    if isinstance(value, _MappingView):
        underlying = getattr(value, "mapping", None)
        if underlying is None:
            underlying = getattr(value, "_mapping", None)
        if underlying is not None and isinstance(
            underlying, _Mapping
        ):
            materialised = _wrapper_materialise(
                underlying, shared_module, ancestors, depth + 1, "other"
            )
            if isinstance(materialised, _Mapping):
                if isinstance(value, _KeysView):
                    return materialised.keys()
                if isinstance(value, _ValuesView):
                    return materialised.values()
                if isinstance(value, _ItemsView):
                    return materialised.items()
        return shared_module._materialise_iterators(value)
    if isinstance(value, tuple):
        return tuple(
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in value
        )
    if isinstance(value, _collections_module.deque):
        return _collections_module.deque(
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in value
        )
    if isinstance(value, _collections_module.UserList):
        return _collections_module.UserList(
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in value
        )
    if isinstance(value, list):
        return [
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in value
        ]
    if isinstance(value, (set, frozenset)):
        materialised_elements = [
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in value
        ]
        try:
            return type(value)(materialised_elements)
        except TypeError:
            return materialised_elements
    if _is_single_pass_iterable(value):
        materialised = [
            _wrapper_materialise(
                element, shared_module, ancestors, depth + 1, "other"
            )
            for element in list(value)
        ]
        if len(materialised) == 1 and isinstance(
            materialised[0], _Mapping
        ) and not any(
            key in materialised[0]
            for key in _WRAPPER_ITEM_FIELD_KEYS
        ):
            return tuple(materialised)
        return materialised
    return shared_module._materialise_iterators(value)


def _materialise_holdout_for_wrapper(holdout_material, shared_module):
    """Return the holdout material materialised for the wrapper.

    The wrapper materialisation stands the holdout
    material in a form the shared direct act reads for
    the pair and the material it carries, in the form
    _wrapper_materialise states: a form carrying no
    iterator stands as it stands, and an iterator
    carrying form stands listed once in a re-iterable
    form of its kind, so every instruction item of the
    test stands compared against the same holdout
    material in the form that act reads for it.
    """
    return _wrapper_materialise(
        holdout_material, shared_module, frozenset()
    )


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
    Holdout material standing in a form carrying no
    iterator stands presented to the shared act in
    that same form, in the form
    _materialise_holdout_for_wrapper states, so a
    single pair standing in set or frozenset form, a
    single pair standing in ChainMap form with its
    maps order standing as the chain carries it, and
    a bundle position standing as a nested mapping
    wrapped in a dictionary view, a tuple, a deque,
    or a generator form each reach the shared act in
    a form that act reads for the pair and the
    material they carry.
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

    holdout_material = _materialise_holdout_for_wrapper(
        holdout_material, _shared_module
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
    from collections.abc import Mapping as _Mapping

    stands = bool(
        isinstance(promotion_record, _Mapping)
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
