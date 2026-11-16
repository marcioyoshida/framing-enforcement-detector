"""English pack. Patterns run on folded text: lower case, no accents, ASCII quotes."""
from __future__ import annotations

import re

from .._types import Pattern

LANG = "en"

NEGATORS = frozenset({
    "not", "no", "never", "nobody", "none", "neither", "nor", "nothing",
    "didn", "doesn", "don", "wasn", "weren", "isn", "aren", "hasn", "haven", "hadn",
    "wouldn", "couldn", "shouldn", "cannot",
})
#: Comparison markers (v3) also read "nowhere" ("Nowhere did it say …").
NEGATORS_COMPARISON = NEGATORS | {"nowhere"}
MODALS = frozenset({"may", "might", "can", "could", "shall", "should", "would", "must", "unless"})
#: Drafting verbs that report a general rule ("the regulation provides that …"): a marker
#: after one of these in its clause only defines.
DEFINING = frozenset({"provides", "provided", "stipulates", "stipulated", "prescribes", "prescribed"})

#: "by" names an agent unless it is a time, a rule or a manner ("by Tuesday", "by law").
_AGENT = re.compile(
    r"(?<!\w)by\s+(?!(?:the\s+)?(?:end|time|then|now|tomorrow|today|monday|tuesday|wednesday"
    r"|thursday|friday|saturday|sunday|january|february|march|april|may|june|july|august"
    r"|september|october|november|december|noon|midnight|law|statute|regulation|mistake"
    r"|accident|default|chance|hand|email|mail|phone|order\s+of\s+the\s+court)\b|\d)")


#: Comparison markers (v3): an emphasis note closing a transcribed passage.
EMPHASIS_NOTE = re.compile(r"\((?:emphasis|emphases)\s+(?:added|supplied|in\s+(?:the\s+)?original|omitted|deleted)[^)]{0,40}\)")


def has_agent(after: str) -> bool:
    return _AGENT.search(after) is not None


def _alt(*words: str) -> str:
    return "(?:" + "|".join(words) + ")"


# --- exception_clause -------------------------------------------------------------------
_EXC = dict(modal_defines=True)
_EMERG = _alt("emergency", "exigent", "extraordinary", "exceptional")
EXCEPTION = [
    Pattern("exc-waiver-granted",
            r"(?:waivers?|exemptions?|exceptions?|derogations?)\s+(?:(?:is|are|was|were|has\s+been|have\s+been)\s+)?"
            r"(?:hereby\s+)?granted", **_EXC),
    Pattern("exc-grant-waiver",
            r"(?:granted|grants|granting|approved|approves|issued|issues)\s+(?:[\w'-]+\s+){0,6}?"
            r"(?:waiver|exemption|exception|derogation)(?!\s+from\s+disclosure)", **_EXC),
    Pattern("exc-dispensed-with",
            r"(?:dispensed|dispenses|dispensing)\s+with\s+(?:the\s+|its\s+|a\s+|any\s+)?(?:[\w-]+\s+){0,2}?"
            r"(?:requirements?|rules?|procedures?|hearings?|notice|service|formalities|conditions?|tender|bidding)",
            **_EXC),
    Pattern("exc-hereby",
            r"(?:is|are|was|were|has\s+been|have\s+been)\s+hereby\s+(?:waived|suspended|exempted|set\s+aside)",
            **_EXC),
    Pattern("exc-waived",
            r"(?:was|were|has\s+been|have\s+been)\s+(?:\w+ly\s+)?(?:waived|exempted)(?!\s+from\s+disclosure)",
            **_EXC),
    Pattern("exc-invoke-emergency",
            r"(?:invoked|invoking|invokes|invoke|citing|cited|under|pursuant\s+to|using|used|exercised"
            r"|exercising|relied\s+on|relying\s+on)\s+(?:the\s+|its\s+|his\s+|her\s+|their\s+|an?\s+)?"
            + _EMERG + r"\s+(?:\w+\s+)?(?:authority|authorities|powers?|exception|provisions?|procedures?"
            r"|clause|measures?|procurement)", **_EXC),
    Pattern("exc-declare-emergency",
            r"(?:declared|declares|declaring|declare|proclaimed|proclaims)\s+(?:a\s+|an\s+)?"
            r"(?:state\s+of\s+(?:\w+\s+)?emergency|(?:national\s+|public\s+health\s+)?emergency)", **_EXC),
    Pattern("exc-circumstances",
            r"(?:in|under|given)\s+(?:the(?:se)?\s+)?" + _EMERG + r"\s+circumstances", **_EXC),
    Pattern("exc-emergency-basis", r"on\s+an?\s+(?:emergency|exceptional|urgent)\s+basis", **_EXC),
    Pattern("exc-notwithstanding",
            r"notwithstanding\s+(?:any\s+|the\s+|this\s+)?(?:other\s+)?(?:provisions?|requirements?|rules?"
            r"|sections?|law|regulations?|limits?|procedures?)", **_EXC),
    Pattern("exc-exception-made",
            r"(?:an\s+)?exception\s+(?:was|has\s+been|had\s+been|is\s+being)\s+made", **_EXC),
    # "waived the 30-day comment period" (invoked) / "may waive the fee" (defined, by the modal)
    Pattern("exc-waive-object",
            r"(?:waived|waives|waive|waiving|suspended|suspends|suspend|suspending|exempted|exempts|exempt)\s+"
            r"(?:the\s+|its\s+|a\s+|an\s+|any\s+|all\s+|this\s+|that\s+)?(?:[\w-]+\s+){0,2}?"
            r"(?:requirements?|rules?|fees?|deadlines?|periods?|procedures?|limits?|conditions?|obligations?"
            r"|restrictions?|provisions?|criteria|bidding|tender|competition)", **_EXC),
]

# --- burden ------------------------------------------------------------------------------
# burden-v2 (2026-11-15): v1 measured 0.39 on a consumer's real corpora (n=77). "Burden" now
# only in the proof sense (paperwork "hour burden" and who "bears the burden" of a payment
# were most English errors); a presumption only as an ACT on it (rebutted, overcome) — bare
# mentions and "is presumed" were 2 of 12; nothing inside a party's reported argument.
_PROOF = r"(?:proof|persuasion|production|going\s+forward|(?:proving|showing|establishing|demonstrating))"
_ADJ = (r"(?:(?!tax\b|paperwork\b|hour\b|hours\b|reporting\b|recordkeeping\b|compliance\b|financial\b"
        r"|economic\b|regulatory\b|administrative\b|fiscal\b|debt\b|cost\b|disease\b|annual\b|total\b)"
        r"[\w-]+\s+){0,2}")
#: Words that put the span inside a party's reported argument ("the State argues that the
#: burden rests on …"): the author is not assigning it.
_ARGUED = frozenset({"argues", "argued", "contends", "contended", "asserts", "asserted", "claims",
                     "claimed", "maintains", "maintained", "urges", "urged", "insists", "insisted",
                     "suggests", "suggested", "posits", "posited", "submits", "submitted"})
_BUR = dict(subtype="burden", modal_defines=True, blocked_by=_ARGUED)
_PRES = dict(subtype="presumption", negatable=False, modal_defines=True, blocked_by=_ARGUED)
BURDEN = [
    # met / carried / discharged its (prima facie) burden — act verbs, proof sense
    Pattern("bur-met",
            r"(?:met|meet|meets|carried|carry|carries|discharged|discharge|discharges|satisfied|satisfy"
            r"|satisfies|sustained|sustain|sustains)\s+(?:its|their|his|her|the|this|that|a|an)\s+" + _ADJ
            + r"(?:burden|onus)(?:\s+of\s+" + _PROOF + r")?",
            negatable=False, **_BUR),
    # bears / shoulders the burden — only "of proof" and its kin
    Pattern("bur-bears",
            r"(?:bears|bore|bear|bearing|shouldered|shoulders|shoulder)\s+(?:the|its|their|his|her|a|an)\s+"
            + _ADJ + r"(?:burden|onus)\s+of\s+" + _PROOF, **_BUR),
    # the burden of proof rests on …
    Pattern("bur-rests",
            r"(?:burden|onus)\s+of\s+" + _PROOF + r"(?:\s+[^.;:]{0,80}?)?\s+(?:is|was|lies|lay|rests|rested|remains"
            r"|remained|falls|fell|shifts|shifted|(?:shall|will|must|should)\s+(?:be|rest|lie|fall|remain))\s+"
            r"(?:squarely\s+|firmly\s+)?(?:on|upon|with)", **_BUR),
    # the burden is on the Government to prove …
    Pattern("bur-is-on-to",
            r"(?:burden|onus)\s+(?:is|was|lies|rests|remains)\s+(?:squarely\s+|firmly\s+)?(?:on|upon|with)\s+"
            r"(?:the\s+)?[\w'-]+(?:\s+[\w'-]+){0,2}\s+to\s+(?:prove|show|establish|demonstrate|justify|rebut)",
            **_BUR),
    Pattern("bur-shift",
            r"(?:shifted|shifts|shifting|reversed|reverses|reversing|placed|places|placing)\s+the\s+"
            r"(?:burden|onus)\s+of\s+" + _PROOF, **_BUR),
    Pattern("pres-rebutted",
            r"presumption\s+(?:of\s+[\w-]+(?:\s+[\w-]+)?\s+)?(?:was|has\s+been|had\s+been|is|is\s+not|was\s+not"
            r"|has\s+not\s+been)\s+(?:rebutted|overcome|displaced)", **_PRES),
    Pattern("pres-rebut",
            r"(?:rebutted|rebuts|overcame|overcome|overcomes|displaced|displaces)\s+the\s+presumption", **_PRES),
]

# --- discretion --------------------------------------------------------------------------
_DISC_ADJ = r"(?:(?:sole|absolute|full|own|reasonable|unfettered|exclusive|broad|complete)\s+)*"
DISCRETION = [
    Pattern("disc-of", r"(?:at|in|to|within)\s+(?:the\s+)?" + _DISC_ADJ + r"discretion\s+of",
            subtype="reserved", modal_defines=True),
    Pattern("disc-poss", r"(?:at|in)\s+(?:its|his|her|their|our)\s+" + _DISC_ADJ + r"discretion",
            subtype="reserved", modal_defines=True),
    Pattern("disc-genitive", r"at\s+(?:the\s+)?[\w-]+'s\s+" + _DISC_ADJ + r"discretion",
            subtype="reserved", modal_defines=True),
    Pattern("disc-deems",
            r"as\s+(?:it|he|she|they|we|the\s+\w+)\s+(?:deems?|deemed|considers?|considered|determines?"
            r"|determined|judges?|judged)\s+(?:appropriate|necessary|fit|proper|suitable|warranted|advisable)",
            subtype="reserved", modal_defines=True),
    Pattern("disc-deemed",
            r"as\s+(?:deemed|considered|determined|judged)\s+(?:appropriate|necessary|fit|proper|warranted)",
            subtype="reserved", modal_defines=True),
    Pattern("disc-see-fit", r"as\s+(?:it|he|she|they)\s+(?:sees?|saw)\s+fit",
            subtype="reserved", modal_defines=True),
    Pattern("disc-case-by-case", r"(?:on\s+a\s+)?case[-\s]by[-\s]case(?:\s+basis)?",
            subtype="reserved", modal_defines=True),
    Pattern("disc-exercise",
            r"(?:exercised|exercising|exercises|exercise|used|uses)\s+(?:its|his|her|their|the)\s+(?:\w+\s+)?discretion",
            subtype="reserved", modal_defines=True),
    Pattern("disc-exercise-of",
            r"in\s+the\s+exercise\s+of\s+(?:its|his|her|their)\s+(?:\w+\s+)?discretion",
            subtype="reserved", modal_defines=True),
    Pattern("disc-discretionary",
            r"(?:is|was|are|were|remains|remained)\s+(?:entirely\s+|purely\s+|wholly\s+|fully\s+)?discretionary",
            subtype="reserved", modal_defines=True),
    Pattern("disc-not-subject",
            r"(?:(?:is|are|was|were|shall|will|be)\s+)?not\s+(?:be\s+)?subject\s+to\s+(?:any\s+)?"
            r"(?:judicial\s+|further\s+|administrative\s+|external\s+|independent\s+)?(?:review|appeal|challenge)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-exempt-review",
            r"(?:exempt|insulated|shielded|precluded)\s+from\s+(?:judicial\s+|further\s+|any\s+)?(?:review|appeal)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-final",
            r"final\s+and\s+(?:binding|unreviewable|non-?appealable|conclusive|unappealable|not\s+subject\s+to\s+appeal)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-unreviewable", r"(?:unreviewable|non-?reviewable|non-?appealable|unappealable)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-no-appeal",
            r"no\s+(?:further\s+)?(?:right\s+of\s+)?appeal\s+(?:lies|is\s+available|shall\s+lie|may\s+be\s+taken|exists)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-no-right-appeal", r"(?:there\s+is\s+)?no\s+(?:further\s+)?right\s+(?:of|to)\s+(?:appeal|review)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-commits",
            r"(?:commits?|committed|committing|leaves|left|leaving)\s+(?:[\w'-]+\s+){0,3}?to\s+(?:the\s+)?"
            r"(?:[\w'-]+\s+)?discretion", subtype="reserved", modal_defines=True),
    Pattern("disc-own-judgment",
            r"(?:according\s+to|in|by|at)\s+(?:its|his|her|their)\s+own\s+(?:judge?ment|discretion)",
            subtype="reserved", modal_defines=True),
]

# --- agentless_passive -------------------------------------------------------------------
_AUX = r"(?:was|were|had\s+been|was\s+being|were\s+being)"
#: A present perfect is a reported past event, except after a future or a time/condition
#: subordinator in its clause: "I will confirm that the data has been destroyed", "after it
#: has been removed" (agentless-v2).
_AUX_PERFECT = r"(?:has\s+been|have\s+been)"
_PERFECT_BLOCKED = frozenset({"will", "shall", "once", "until", "after", "unless", "whether", "if"})
_ADV = r"(?:\s+(?:\w+ly|later|then|also|subsequently|eventually|soon|since|once|twice|again))?"
_PASSIVE = dict(agent_check=True, modal_blocks=True)


def _passive(pid: str, subtype: str, verbs: str) -> list[Pattern]:
    return [Pattern(pid, _AUX + _ADV + r"\s+" + verbs, subtype=subtype, **_PASSIVE),
            Pattern(pid + "-perfect", _AUX_PERFECT + _ADV + r"\s+" + verbs, subtype=subtype,
                    blocked_by=_PERFECT_BLOCKED, **_PASSIVE)]


AGENTLESS = [
    *_passive("pas-harm", "harm", _alt(
        "killed", "injured", "wounded", "shot", "beaten", "attacked", "assaulted", "detained",
        "arrested", "imprisoned", "jailed", "deported", "evicted", "tortured", "abducted",
        "kidnapped", "displaced", "hurt", "harmed", "stabbed", "tear-gassed", "teargassed")),
    *_passive("pas-sanction", "sanction", _alt(
        "fined", "sanctioned", "penali[sz]ed", "punished", "disciplined", "censured", "reprimanded",
        "suspended", "banned", "barred", "blocked", "debarred", "blacklisted", "demoted",
        "sentenced")),
    *_passive("pas-removal", "removal", _alt(
        "removed", "deleted", "dismissed", "fired", "sacked", "withdrawn", "revoked", "cancell?ed",
        "terminated", "rejected", "denied", "withheld", "destroyed", "seized", "confiscated",
        "shredded", "erased", "expelled", r"shut\s+down", r"taken\s+down", r"closed\s+down",
        r"struck\s+(?:down|off)", "purged", "redacted", "scrapped", "discontinued")),
    *_passive("pas-error", "error", _alt(
        "overlooked", "mishandled", "misplaced", "mislaid", "lost", "missed", "ignored", "neglected",
        "misreported", "miscounted")),
    Pattern("pas-mistakes-made",
            r"(?:mistakes|errors|misjudgments|misjudgements|missteps|failures)\s+(?:were|have\s+been|had\s+been)"
            + _ADV + r"\s+made", subtype="error", **_PASSIVE),
]

# --- hedge -------------------------------------------------------------------------------
_HEDGE = dict(negatable=False)
_DET = _alt("the", "a", "an", "his", "her", "their", "its", "this", "that", "these", "those", "of", "for",
            "on", "in", "with", "over", "about", "and", "or", "any", "two", "three", "several", "an",
            "into", "to", "from", "after", "against")
HEDGE = [
    # hedge-v3: "presumably" dropped; it marks the author's own inference, not a report
    # (the rubric's English list never had it).
    Pattern("hedge-adverb", _alt("reportedly", "allegedly", "purportedly", "supposedly", "ostensibly"),
            subtype="adverb", **_HEDGE),
    Pattern("hedge-label", _alt("so-called", r"so\s+called", "self-styled", "self-proclaimed", "self-described",
                                "unverified", "unconfirmed", "unsubstantiated"),
            subtype="label", **_HEDGE),
    Pattern("hedge-label-adj",
            _DET + r"\s+(?P<m>alleged|purported|supposed)(?=\s+(?!to\b|that\b)\w)",
            subtype="label", **_HEDGE),
    Pattern("hedge-said-to",
            r"(?:is|are|was|were)\s+(?:widely\s+)?(?:said|reported|alleged|believed|thought|rumou?red|claimed)"
            r"\s+to\s+(?:have|be)", subtype="report_conditional", **_HEDGE),
]

# --- attribution_verb ----------------------------------------------------------------------
#: Say-verbs: a "that" clause within four words, punctuation within four words, a quote,
#: or the end of the text ('"…," he said.' / 'said in a statement.').
_LOOSE = (r"(?=(?:[\s,]+(?!that\b)[\w']+){0,6}?[\s,]+that\b|(?:\s+[\w']+){0,8}\s*[,:;.!?]|\s*[\"']"
          r"|(?:\s+[\w']+){0,8}\s*$|\s+(?:they|he|she|it|we|the)\s+\w+)")
#: Verbs that also mean an act ("confirmed the sentence", "claimed the land"): a "that"
#: clause, a colon or a quote only. Inversions after a quote are a separate pattern.
_STRICT = r"(?=(?:[\s,]+(?!that\b)[\w']+){0,6}?[\s,]+that\b|\s*:|\s*[\"'])"
#: Right after a closing quote: '…," the minister claimed' / '…,' admitted the director.
_CLOSE_Q = r"(?:[,.!?]\s*[\"']|[\"']\s*,)\s*(?:[\w'-]+\s+){0,3}?"

#: Not after a passive auxiliary ("he was told to leave") or a determiner ("the said
#: contract", legal usage). "states" is left out: "member states." is a noun.
_NOT_PASSIVE = (r"(?<!\bwas\s)(?<!\bwere\s)(?<!\bbeen\s)(?<!\bbeing\s)(?<!\bthe\s)(?<!\bof\s)(?<!\bis\s)(?<!\bto\s)"
                # attribution-v2: "something to be said for", "unless otherwise stated",
                # "the complaint nowhere alleges".
                r"(?<!\bbe\s)(?<!\botherwise\s)(?<!\bnowhere\s)")
#: attribution-v3: every guard above needs a word boundary; without it "Chris said" and
#: "Davis said" were dropped ("is" inside the name) since v1.
#: attribution-v2: "said" after a preposition is the legal adjective ("in said County",
#: "within and for said Court"), not a speech verb.
_NOT_SAID_ADJ = (r"(?<!\bin\s)(?<!\bfor\s)(?<!\bwithin\s)(?<!\bfrom\s)(?<!\bupon\s)(?<!\bunder\s)(?<!\bby\s)"
                 r"(?<!\bat\s)(?<!\bon\s)(?<!\bwith\s)")
#: attribution-v3: "told", "tells", "added" and "adds" also take a plain object ("adds the
#: option", "tells us nothing"), so they need a that-clause, a colon or a quotation (strict).
_NEUTRAL = _alt(_NOT_SAID_ADJ + "said", "says", "say", "stated", "wrote", "writes", "declared", "declares")
_NEUTRAL_STRICT = _alt(r"(?<!\ball\s)told", "tells", "added", "adds")
#: attribution-v3: a manner phrase ("stated simply", "put differently") is not a statement.
_NOT_MANNER = r"(?!\s+(?:simply|differently|otherwise|briefly|generally|plainly|broadly|another\s+way|more\s+\w+ly)\b)"
#: attribution-v3: a text or evidence as the subject is not a speaker ("the statute tells
#: us", "a comparison with other statutes shows that", "the record confirms"). Checked over
#: the clause before the verb, for the verbs that take such subjects.
_TEXT_SUBJECT_EN = frozenset({
    "statute", "statutes", "clause", "phrase", "text", "rule", "rules", "provision", "provisions",
    "law", "section", "constitution", "amendment", "regulation", "regulations", "language", "word",
    "words", "scheme", "canon", "definition", "structure", "history", "record", "records",
    "evidence", "comparison", "data", "document", "documents", "study", "studies", "results",
    "testimony", "precedent", "precedents", "context", "experience"})
_DISTANCING_VERBS = ("claimed", "alleged", "alleges", "insisted", "insists", "maintained",
                     "maintains", "contended", "contends", "asserted", "asserts")
#: attribution-v3: "claims" is far more often the plural noun ("other claims that have
#: nothing to do with…", "sex-discrimination claims"); it gets its own, stricter pattern.
_DISTANCING = _alt(*_DISTANCING_VERBS)
#: After a quotation or a comma the verb reading is safe, so "claims" stays there.
_DISTANCING_INV = _alt("claims", *_DISTANCING_VERBS)
_NOUN_BEFORE = "".join(rf"(?<!\b{w}\s)" for w in (
    "the", "these", "those", "their", "his", "her", "its", "our", "your", "such", "any", "all",
    "both", "other", "and", "or", "of", "no", "two", "new", "similar", "related", "remaining",
    "state", "federal", "these", "whose", "many", "several", "some", "those", "pending"))
#: A that-clause opening a relative clause ("claims that were dismissed") is not speech.
_RELATIVE = (r"(?!\s+(?:\w+ly\s+)?(?:were|are|is|was|have|had|has|could|would|can|may|might|must"
             r"|should|do|did|does|arise|arose|remain|involve|relate|concern|seek|sought)\b)")
_CLAIMS_STRICT = r"(?=(?:[\s,]+(?!that\b)[\w']+){0,6}?[\s,]+that\b" + _RELATIVE + r"|\s*:)"
_ENDORSING = _alt("confirmed", "confirms", "revealed", "reveals", "acknowledged", "acknowledges",
                  "admitted", "admits", "explained", "explains", r"pointed\s+out", r"points\s+out",
                  "showed", "shows")

#: attribution-v2: a modal right before the verb is a possible statement, not one made
#: ("nothing he could say").
_ATTR = dict(modal_blocks=True,
             # attribution-v3: "Nowhere did the statute say …" (the negator can sit far back).
             blocked_by=frozenset({"nowhere"}))
_TEXT_BLOCK = _TEXT_SUBJECT_EN | {"nowhere"}

ATTRIBUTION = [
    # attribution-v3: "says nothing / little / no" introduces no statement.
    Pattern("attr-neutral", _NOT_PASSIVE + r"(?P<m>" + _NEUTRAL + r")(?!\s+(?:nothing|little|no)\b)" + _NOT_MANNER
            + _LOOSE, subtype="neutral", **_ATTR),
    Pattern("attr-neutral-strict", _NOT_PASSIVE + r"(?P<m>" + _NEUTRAL_STRICT + r")(?!\s+(?:nothing|little|no)\b)"
            + _STRICT, subtype="neutral", modal_blocks=True, blocked_by=_TEXT_BLOCK),
    Pattern("attr-distancing", _NOT_PASSIVE + r"(?P<m>" + _DISTANCING + r")" + _STRICT,
            subtype="distancing", **_ATTR),
    Pattern("attr-distancing-claims", _NOT_PASSIVE + _NOUN_BEFORE + r"(?P<m>claims)" + _CLAIMS_STRICT,
            subtype="distancing", **_ATTR),
    Pattern("attr-endorsing", _NOT_PASSIVE + r"(?P<m>" + _ENDORSING + r")" + _STRICT,
            subtype="endorsing", modal_blocks=True, blocked_by=_TEXT_BLOCK),
    # '"…," the minister claimed' / '"…," claimed the minister'
    Pattern("attr-distancing-inv", _CLOSE_Q + r"(?P<m>" + _DISTANCING_INV + r")",
            subtype="distancing", lead_boundary=False),
    Pattern("attr-endorsing-inv", _CLOSE_Q + r"(?P<m>" + _ENDORSING + r")",
            subtype="endorsing", lead_boundary=False),
    # "…, claimed the union." (no quotation marks): distancing only; endorsing verbs after a
    # comma are too often acts ("…, confirmed the sentence").
    Pattern("attr-distancing-comma",
            r",\s*(?P<m>" + _DISTANCING_INV + r")\s+(?:the\s+)?[\w'-]+(?:\s+[\w'-]+){0,4}\s*(?:[.;!?]|$)",
            subtype="distancing", lead_boundary=False),
]

PATTERNS: dict[str, list[Pattern]] = {
    "exception_clause": EXCEPTION,
    "burden": BURDEN,
    "discretion": DISCRETION,
    "agentless_passive": AGENTLESS,
    "hedge": HEDGE,
    "attribution_verb": ATTRIBUTION,
}
