"""scan(): run the packs over one text and return verbatim hits."""
from __future__ import annotations

import re
from types import ModuleType
from typing import Iterable, Sequence

from ._context import Clauses, emphasis_intervals, inside, quoted_intervals, tokens, window_start
from ._fold import fold
from ._markers import MARKERS
from ._types import Hit, Pattern
from .packs import en, pt

PACKS: dict[str, ModuleType] = {"en": en, "pt": pt}
LANGS = tuple(PACKS)

#: Words checked for a negator, counted back from the span, inside its clause.
NEGATION_WINDOW = 3
#: Words checked for a modal before an institutional marker, inside its clause.
MODAL_WINDOW = 8
#: Characters after an agentless passive searched for an agent phrase, inside its clause.
AGENT_WINDOW = 80
#: Characters after an institutional marker searched for a modal, inside its clause
#: ("in exceptional circumstances, the deadline may be extended").
MODAL_AFTER = 60
#: Words before a span checked for ``blocked_near``: quoted interiors skipped, and never
#: before the last comma, colon, dash or full stop ("Under that standard, the Court
#: explained"; "§1415(l).6 The District maintains", where a footnote hides the stop).
NEAR_WINDOW = 3


def scan(
    text: str,
    lang: str = "en",
    markers: Iterable[str] | None = None,
    exclude: Iterable[Sequence[int]] = (),
    include_defined: bool = False,
) -> list[Hit]:
    """Every marker span in ``text``, ordered by position.

    ``exclude``: spans the caller knows are quoted law or citations; a hit there is never
    invoked. ``include_defined``: also return invoked=False hits (for labelling negatives).
    """
    if lang not in PACKS:
        raise ValueError(f"unsupported lang {lang!r}; one of {LANGS}")
    names = tuple(MARKERS) if markers is None else tuple(markers)
    for name in names:
        if name not in MARKERS:
            raise ValueError(f"unknown marker {name!r}; one of {tuple(MARKERS)}")
    pack = PACKS[lang]
    folded = fold(text)
    # Institutional markers keep the hard clause and quote rules their versions were
    # measured with; comparison markers read across PDF line wraps (see _context).
    ctx = {
        "institutional": (Clauses(text), quoted_intervals(folded)),
        "comparison": (Clauses(text, soft_wrap=True),
                       sorted(quoted_intervals(folded, elided_open=True)
                              + emphasis_intervals(folded, pack.EMPHASIS_NOTE))),
    }
    excluded = [tuple(s) for s in exclude]

    hits: list[Hit] = []
    for name in names:
        clauses, quotes = ctx[MARKERS[name].group]
        found = [h for p in pack.PATTERNS.get(name, ()) for h in _apply(
            p, name, text, folded, clauses, quotes, excluded, pack)]
        hits.extend(_dedupe(found))
    if not include_defined:
        hits = [h for h in hits if h.invoked]
    return sorted(hits, key=lambda h: (h.start, h.end, h.marker))


def _apply(p: Pattern, name: str, text: str, folded: str, clauses: Clauses,
           quotes: list[tuple[int, int]], excluded: list, pack: ModuleType) -> list[Hit]:
    out: list[Hit] = []
    has_m = "m" in p.compiled.groupindex
    for m in p.compiled.finditer(folded):
        start, end = m.span("m") if has_m and m.group("m") is not None else m.span()
        c_start, c_end = clauses.bounds(start, end)
        left = min(start, m.start())
        before = tokens(folded[window_start(c_start, left, quotes):left])

        negators = pack.NEGATORS if MARKERS[name].group == "institutional" else pack.NEGATORS_COMPARISON
        if p.negatable and _negated(before[-(NEGATION_WINDOW + 1):], negators):
            continue
        if p.modal_blocks and before and before[-1] in pack.MODALS:
            continue
        if p.blocked_by and set(before) & p.blocked_by:
            continue
        if p.blocked_near and set(_near(folded, c_start, left, quotes)) & p.blocked_near:
            continue
        if p.blocked_after and set(tokens(folded[end:min(c_end, end + AGENT_WINDOW)])) & p.blocked_after:
            continue
        if p.agent_check:
            after = folded[end:min(c_end, end + AGENT_WINDOW)]
            if pack.has_agent(after):
                continue

        invoked = not (inside(start, end, quotes) or inside(start, end, excluded))
        if p.always_defined:
            invoked = False
        if invoked and p.modal_defines:
            after_end = min(c_end, end + MODAL_AFTER)
            for qs, _qe in quotes:
                if end <= qs < after_end:
                    after_end = qs
            window = (set(before[-MODAL_WINDOW:]) | set(tokens(folded[start:end]))
                      | set(tokens(folded[end:after_end])))
            if window & pack.MODALS or set(before) & pack.DEFINING:
                invoked = False

        quote = text[start:end]
        assert quote == text[start:end] and start < end
        out.append(Hit(marker=name, version=MARKERS[name].version, start=start, end=end,
                       quote=quote, pattern_id=f"{pack.LANG}:{p.id}", subtype=p.subtype,
                       invoked=invoked))
    return out


_NEAR_CUT = re.compile(r"[,:—]|\s-\s|\.\d{0,3}\s")
_LINE_HYPHEN = re.compile(r"(\w)-\s+(\w)")


def _near(folded: str, c_start: int, left: int, quotes: list[tuple[int, int]]) -> list[str]:
    """The NEAR_WINDOW words before ``left`` in its clause, quoted interiors skipped."""
    chars = list(folded[c_start:left])
    for s, e in quotes:
        for i in range(max(s, c_start), min(e, left)):
            chars[i - c_start] = " "
    # A word hyphenated across a line ("dic-\ntionaries") is read whole.
    seg = _LINE_HYPHEN.sub(r"\1\2", "".join(chars))
    cuts = [m.end() - 1 for m in _NEAR_CUT.finditer(seg)]
    cut = cuts[-1] if cuts else -1
    # A section number does not push the noun out of the window ("Section 1101(a)(13)(C)(v)
    # says", "§3322(a) just says"): numbers and one-letter tokens are skipped.
    seg = seg[cut + 1:].replace("§", " section ")
    return [t for t in tokens(seg) if len(t) > 1 and not t.isdigit()][-NEAR_WINDOW:]


def _negated(window: list[str], negators: frozenset[str]) -> bool:
    """A negator among the last NEGATION_WINDOW words. A negator followed by a number is
    an abbreviation, not a negation ("Decision No. 45 was revoked")."""
    tail = window[-NEGATION_WINDOW:]
    offset = len(window) - len(tail)
    for i, tok in enumerate(tail):
        if tok in negators:
            nxt = window[offset + i + 1] if offset + i + 1 < len(window) else ""
            if not nxt.isdigit():
                return True
    return False


def _dedupe(hits: list[Hit]) -> list[Hit]:
    """One hit per region for a marker: the earliest, then the longest, wins."""
    kept: list[Hit] = []
    for h in sorted(hits, key=lambda h: (h.start, -(h.end - h.start))):
        if not any(h.start < k.end and k.start < h.end for k in kept):
            kept.append(h)
    return kept
