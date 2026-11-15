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
_NOT_TAX = r"(?:(?!tax\b|financial\b|economic\b|regulatory\b|administrative\b|fiscal\b|debt\b|cost\b)\w+\s+)?"
BURDEN = [
    Pattern("bur-met",
            r"(?:met|meet|meets|carried|carry|carries|discharged|discharge|discharges|satisfied|satisfy"
            r"|satisfies|sustained|sustain|sustains|bears|bore|bear|shouldered|shoulders)\s+"
            r"(?:its|their|his|her|the|this|that|a|an)\s+" + _NOT_TAX + r"(?:burden|onus)(?!\s+on\s+(?:small|business))",
            subtype="burden", negatable=False, modal_defines=True),
    Pattern("bur-rests",
            r"(?:burden|onus)(?:\s+of\s+(?:proof|persuasion|production|(?:proving|showing|establishing"
            r"|demonstrating)(?:\s+[^.;:]{0,80}?)?))?\s+(?:is|was|lies|lay|rests|rested|remains|remained|falls|fell|shifts|shifted"
            r"|(?:shall|will|must|should)\s+(?:be|rest|lie|fall|remain))\s+(?:squarely\s+|firmly\s+)?(?:on|upon|with)",
            subtype="burden", modal_defines=True),
    Pattern("bur-shift",
            r"(?:shifted|shifts|shifting|reversed|reverses|reversing|placed|places|placing|put|puts)\s+the\s+"
            r"(?:burden|onus)(?:\s+of\s+proof)?", subtype="burden", modal_defines=True),
    Pattern("pres-presumed",
            r"(?:is|are|was|were|be|been)\s+presumed\s+(?:to|that|valid|lawful|innocent|correct|regular"
            r"|legitimate|genuine|authentic|true|accurate|reasonable|constitutional|in\s+good\s+faith)",
            subtype="presumption", modal_defines=True),
    Pattern("pres-presumption",
            r"presumption\s+(?:of\s+\w+(?:\s+\w+)?\s+)?(?:applies|applied|attaches|attached"
            r"|arises|arose|was\s+rebutted|has\s+been\s+rebutted|is\s+rebutted|stands|was\s+not\s+rebutted"
            r"|has\s+not\s+been\s+rebutted|was\s+overcome|governs|operates)",
            subtype="presumption", negatable=False, modal_defines=True),
    Pattern("pres-rebut",
            r"(?:rebutted|rebuts|overcame|overcome|overcomes|displaced)\s+the\s+presumption",
            subtype="presumption", negatable=False, modal_defines=True),
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
_AUX = r"(?:was|were|has\s+been|have\s+been|had\s+been|was\s+being|were\s+being)"
_ADV = r"(?:\s+(?:\w+ly|later|then|also|subsequently|eventually|soon|since|once|twice|again))?"
_PASSIVE = dict(agent_check=True, modal_blocks=True)


def _passive(pid: str, subtype: str, verbs: str) -> Pattern:
    return Pattern(pid, _AUX + _ADV + r"\s+" + verbs, subtype=subtype, **_PASSIVE)


AGENTLESS = [
    _passive("pas-harm", "harm", _alt(
        "killed", "injured", "wounded", "shot", "beaten", "attacked", "assaulted", "detained",
        "arrested", "imprisoned", "jailed", "deported", "evicted", "tortured", "abducted",
        "kidnapped", "displaced", "hurt", "harmed", "stabbed", "tear-gassed", "teargassed")),
    _passive("pas-sanction", "sanction", _alt(
        "fined", "sanctioned", "penali[sz]ed", "punished", "disciplined", "censured", "reprimanded",
        "suspended", "banned", "barred", "blocked", "debarred", "blacklisted", "demoted",
        "sentenced")),
    _passive("pas-removal", "removal", _alt(
        "removed", "deleted", "dismissed", "fired", "sacked", "withdrawn", "revoked", "cancell?ed",
        "terminated", "rejected", "denied", "withheld", "destroyed", "seized", "confiscated",
        "shredded", "erased", "expelled", r"shut\s+down", r"taken\s+down", r"closed\s+down",
        r"struck\s+(?:down|off)", "purged", "redacted", "scrapped", "discontinued")),
    _passive("pas-error", "error", _alt(
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
    Pattern("hedge-adverb", _alt("reportedly", "allegedly", "purportedly", "supposedly", "ostensibly",
                                 "presumably"),
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
_NOT_PASSIVE = r"(?<!was\s)(?<!were\s)(?<!been\s)(?<!being\s)(?<!the\s)(?<!of\s)(?<!is\s)(?<!to\s)"
_NEUTRAL = _alt("said", "says", "say", "stated", "told", "tells", "added", "adds", "wrote", "writes",
                "declared", "declares")
_DISTANCING = _alt("claimed", "claims", "alleged", "alleges", "insisted", "insists", "maintained",
                   "maintains", "contended", "contends", "asserted", "asserts")
_ENDORSING = _alt("confirmed", "confirms", "revealed", "reveals", "acknowledged", "acknowledges",
                  "admitted", "admits", "explained", "explains", r"pointed\s+out", r"points\s+out",
                  "showed", "shows")

ATTRIBUTION = [
    Pattern("attr-neutral", _NOT_PASSIVE + r"(?P<m>" + _NEUTRAL + r")" + _LOOSE, subtype="neutral"),
    Pattern("attr-distancing", _NOT_PASSIVE + r"(?P<m>" + _DISTANCING + r")" + _STRICT,
            subtype="distancing"),
    Pattern("attr-endorsing", _NOT_PASSIVE + r"(?P<m>" + _ENDORSING + r")" + _STRICT,
            subtype="endorsing"),
    # '"…," the minister claimed' / '"…," claimed the minister'
    Pattern("attr-distancing-inv", _CLOSE_Q + r"(?P<m>" + _DISTANCING + r")",
            subtype="distancing", lead_boundary=False),
    Pattern("attr-endorsing-inv", _CLOSE_Q + r"(?P<m>" + _ENDORSING + r")",
            subtype="endorsing", lead_boundary=False),
    # "…, claimed the union." (no quotation marks): distancing only; endorsing verbs after a
    # comma are too often acts ("…, confirmed the sentence").
    Pattern("attr-distancing-comma",
            r",\s*(?P<m>" + _DISTANCING + r")\s+(?:the\s+)?[\w'-]+(?:\s+[\w'-]+){0,4}\s*(?:[.;!?]|$)",
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
