"""Hit, marker and pattern types."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Hit:
    """One marker span. ``quote == text[start:end]`` always holds."""

    marker: str
    version: str
    start: int
    end: int
    quote: str
    pattern_id: str
    subtype: str | None
    #: In the text's own voice and applied here (True), or only defined, quoted, inside a
    #: direct quotation or inside a caller-excluded span (False).
    invoked: bool


@dataclass(frozen=True)
class MarkerSpec:
    name: str
    #: Bumped on ANY change to this marker's patterns or rules, in any language.
    version: str
    group: str  # "institutional" | "comparison"
    subtypes: tuple[str, ...] = ()


@dataclass(frozen=True)
class Pattern:
    """One pattern over FOLDED text (lower case, no accents, ASCII quotes).

    The reported span is the named group ``m`` when the regex has one, else the whole
    match, so a pattern can require context (a following "that") without reporting it.
    """

    id: str
    regex: str
    subtype: str | None = None
    #: A negator in the three words before the span drops the hit ("no waiver was granted").
    #: False where a negated form is still the marker ("has not met its burden").
    negatable: bool = True
    #: Institutional markers: a modal in the clause before the span, or inside it, means the
    #: text only DEFINES the rule ("may waive"), so the hit is invoked=False.
    modal_defines: bool = False
    #: Agentless passives: an agent phrase ("by …", "pelo …") later in the clause drops the hit.
    agent_check: bool = False
    #: Agentless passives: a modal right before the span drops it ("would have been fined").
    modal_blocks: bool = False
    #: Words that drop the hit when they occur in the clause before the span (a reporting
    #: conditional after "if it had…" is a hypothetical, not a hedge).
    blocked_by: frozenset[str] = frozenset()
    #: Words that drop the hit when they occur in the clause right after the span (a
    #: reporting conditional followed by "caso … estivesse" is a hypothetical).
    blocked_after: frozenset[str] = frozenset()
    #: Words that drop the hit when they occur among the NEAR_WINDOW words right before the
    #: span, read across quoted passages with their interiors skipped (the subject of a
    #: speech verb: 'the phrase "during a national emergency" tells', attribution-v4).
    blocked_near: frozenset[str] = frozenset()
    #: The wording itself only defines a rule ("é dispensável a licitação" = may be
    #: dispensed with): always invoked=False.
    always_defined: bool = False
    #: False for a pattern that starts at punctuation (a closing quote right after a word).
    lead_boundary: bool = True
    compiled: re.Pattern[str] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        lead = r"(?<!\w)" if self.lead_boundary else ""
        wrapped = lead + r"(?:" + self.regex + r")(?!\w)"
        object.__setattr__(self, "compiled", re.compile(wrapped))
