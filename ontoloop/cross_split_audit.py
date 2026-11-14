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


def _item_fields(item):
    if isinstance(item, str):
        return {"group": None, "signature": None, "text": item}
    if isinstance(item, dict):
        text = item.get("text")
        if text is None:
            text = item.get("instruction_text")
        if text is None:
            text = item.get("content")
        return {
            "group": item.get("group"),
            "signature": item.get("signature"),
            "text": text,
        }
    return {"group": None, "signature": None, "text": None}


def _split_items(material):
    """Partition bundle material into candidate and holdout items."""
    candidate = []
    holdout = []
    if isinstance(material, dict):
        for key in ("candidate_items", "candidate"):
            value = material.get(key)
            if isinstance(value, (list, tuple)):
                candidate.extend(value)
        for key in ("holdout_items", "holdout"):
            value = material.get(key)
            if isinstance(value, (list, tuple)):
                holdout.extend(value)
        items = material.get("items")
        if isinstance(items, (list, tuple)):
            for item in items:
                side = None
                if isinstance(item, dict):
                    side = item.get("split") or item.get("side")
                if side in ("holdout", "sealed holdout"):
                    holdout.append(item)
                else:
                    candidate.append(item)
        pairs = material.get("pairs")
        if isinstance(pairs, (list, tuple)):
            for pair in pairs:
                if isinstance(pair, (list, tuple)) and len(pair) == 2:
                    candidate.append(pair[0])
                    holdout.append(pair[1])
    elif isinstance(material, (list, tuple)):
        for item in material:
            side = None
            if isinstance(item, dict):
                side = item.get("split") or item.get("side")
            if side in ("holdout", "sealed holdout"):
                holdout.append(item)
            else:
                candidate.append(item)
    return candidate, holdout


def _is_bundle(material):
    if isinstance(material, (list, tuple)):
        return True
    if isinstance(material, dict):
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


def _keyed_index(items):
    index = {}
    for position, item in enumerate(items):
        fields = _item_fields(item)
        for relation in ("group", "signature"):
            value = fields[relation]
            if value is not None:
                index.setdefault((relation, value), []).append(position)
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
            for hold_pos in index.get((relation, value), []):
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
    """
    if _is_bundle(material):
        bundle = _audit_bundle(material)
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


def _audit(material, scored_before_refusal):
    if _is_bundle(material):
        bundle = _audit_bundle(material)
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
    if isinstance(instruction_text, dict):
        for key in ("instruction_text", "text", "content"):
            value = instruction_text.get(key)
            if value is not None:
                return value
        return None
    return instruction_text


def _holdout_items_of(holdout_material):
    if holdout_material is None:
        return []
    if isinstance(holdout_material, str):
        return [holdout_material]
    if isinstance(holdout_material, dict):
        if _is_bundle(holdout_material):
            candidate, holdout = _split_items(holdout_material)
            return holdout
        return [holdout_material]
    if isinstance(holdout_material, (list, tuple)):
        return list(holdout_material)
    return [holdout_material]


def audit_instruction_item(
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
    bundle mapping carrying holdout_items. It compares
    the instruction text field only, and the text field
    of each holdout item only: no group, no signature,
    and no wider field of either side takes part. A
    pair fires where the texts stand equal (the
    verbatim case, also recorded on the verbatim key)
    or where the module _text_overlap form, dividing
    by the smaller of the two word counts, stands at
    or above the near verbatim threshold.

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
    points.
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
