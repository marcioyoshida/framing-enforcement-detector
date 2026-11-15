"""scan(): run the packs over one text and return verbatim hits."""
from __future__ import annotations

from types import ModuleType
from typing import Iterable, Sequence

from ._context import Clauses, inside, quoted_intervals, tokens, window_start
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
    clauses = Clauses(text)
    quotes = quoted_intervals(folded)
    excluded = [tuple(s) for s in exclude]

    hits: list[Hit] = []
    for name in names:
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

        if p.negatable and _negated(before[-(NEGATION_WINDOW + 1):], pack.NEGATORS):
            continue
        if p.modal_blocks and before and before[-1] in pack.MODALS:
            continue
        if p.blocked_by and set(before) & p.blocked_by:
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
