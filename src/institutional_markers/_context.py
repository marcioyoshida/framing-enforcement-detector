"""Clause bounds, quotations and token windows, all on offsets shared by both texts."""
from __future__ import annotations

import re
from bisect import bisect_left, bisect_right
from typing import Iterable, Sequence

_WORD = re.compile(r"\w+")
#: A full stop ends a clause only before whitespace and an upper-case letter, a quote or the
#: end of text, so "Art. 75" and "n. 123" stay inside one clause.
_STOP = re.compile(r"[;!?\n]|\.(?=\s+[A-ZÀ-Ý\"“«']|\s*$)")


#: Comparison markers (since agentless-v2, hedge-v2, attribution-v2): a line break ends a
#: clause only at a blank line. PDF and OCR text wraps every line, and a hard stop at each
#: wrap hid agents ("foi\ntotalmente ignorada pela auditoria"), negators and hypotheticals.
_SOFT_STOP = re.compile(r"[;!?]|\n[ \t]*\n|\.(?=\s+[A-ZÀ-Ý\"“«']|\s*$)")


class Clauses:
    def __init__(self, original: str, soft_wrap: bool = False) -> None:
        stop = _SOFT_STOP if soft_wrap else _STOP
        self._stops = [m.start() for m in stop.finditer(original)]
        self._len = len(original)

    def bounds(self, start: int, end: int) -> tuple[int, int]:
        """The clause holding [start, end): just after the previous stop to the next stop."""
        i = bisect_left(self._stops, start)
        left = self._stops[i - 1] + 1 if i > 0 else 0
        j = bisect_right(self._stops, max(start, end - 1))
        right = self._stops[j] if j < len(self._stops) else self._len
        return left, right


def tokens(folded: str) -> list[str]:
    return _WORD.findall(folded)


#: A single quote opens a quotation after whitespace or an opening bracket and before a
#: letter; it closes one after a non-space and before whitespace, punctuation or the end.
#: An apostrophe between letters ("agency's", "d'água") is neither.
_SQ_OPEN = re.compile(r"(?:^|(?<=[\s(\[{:—-]))'(?=[\w\"])")
#: Comparison markers also open a quotation on an elided start: "('... revogada cautelar".
_SQ_OPEN_ELIDED = re.compile(r"(?:^|(?<=[\s(\[{:—-]))'(?=[\w\"]|\.\.\.|…|\()")
_SQ_CLOSE = re.compile(r"(?<=[^\s'])'(?=[\s.,;:!?)\]}\"]|$)")


def quoted_intervals(folded: str, elided_open: bool = False) -> list[tuple[int, int]]:
    """Interiors of quoted passages. Typographic quotes are already folded to '"' and "'".

    ``elided_open`` (comparison markers): a single quote before "..." also opens one."""
    if elided_open:
        spans = _directional_double(folded)
    else:
        marks = [i for i, c in enumerate(folded) if c == '"']
        spans = [(marks[k] + 1, marks[k + 1]) for k in range(0, len(marks) - 1, 2)]
    opens = [m.start() for m in (_SQ_OPEN_ELIDED if elided_open else _SQ_OPEN).finditer(folded)]
    closes = [m.start() for m in _SQ_CLOSE.finditer(folded)]
    ci = 0
    for o in opens:
        while ci < len(closes) and closes[ci] <= o:
            ci += 1
        if ci == len(closes):
            break
        if not any(s <= o < e for s, e in spans):
            spans.append((o + 1, closes[ci]))
        ci += 1
    return sorted(spans)


_DQ_OPEN = re.compile(r'(?:^|(?<=[\s(\[{:—-]))"(?=\S)')
_DQ_CLOSE = re.compile(r'(?<=\S)"(?=[\s.,;:!?)\]}]|$)')


def _directional_double(folded: str) -> list[tuple[int, int]]:
    """Double quotes paired by direction, not by count (comparison markers). A mark after a
    space that starts a word opens; a mark after a word, before a space or punctuation,
    closes. One stray mark (a quotation opened on an earlier page, OCR noise) then no longer
    flips every pair after it."""
    marks = sorted([(m.start(), "o") for m in _DQ_OPEN.finditer(folded)]
                   + [(m.start(), "c") for m in _DQ_CLOSE.finditer(folded)])
    spans, open_at = [], None
    for pos, kind in marks:
        if kind == "o" and open_at is None:
            open_at = pos
        elif kind == "c" and open_at is not None and pos > open_at:
            spans.append((open_at + 1, pos))
            open_at = None
    return spans


#: A paragraph starts after a blank line or at a numbered line ("\n 132. Informa").
_PARA = re.compile(r"\n[ \t]*\n|\n[ \t]*\d{1,3}(?:\.\d{1,3})*\.[ \t]+(?=\S)")
#: A colon that introduces a transcription: followed by whitespace, a quote or a dash.
_COLON = re.compile(r":(?=[\s\"'—-])")
#: How far back an emphasis note may reach (characters).
EMPHASIS_REACH = 800


def emphasis_intervals(folded: str, note: re.Pattern[str]) -> list[tuple[int, int]]:
    """Comparison markers (v3): an emphasis note ("(grifos nossos)", "(emphasis added)") ends
    a transcribed passage that often carries no quotation marks. The passage is taken to
    start after the last colon before the note, inside the note's paragraph (at most
    EMPHASIS_REACH characters back): "O normativo explica: As informações … (grifo nosso)".
    With no such colon nothing is marked, so the author's own words before a quotation
    ("Jones told Dr. Potts that …") stay the author's."""
    out = []
    for m in note.finditer(folded):
        q = m.start()
        lo = max(0, q - EMPHASIS_REACH)
        starts = [p.end() for p in _PARA.finditer(folded, lo, q)]
        para = starts[-1] if starts else lo
        colons = [c.end() for c in _COLON.finditer(folded, para, q)]
        if colons:
            out.append((colons[-1], q))
    return out


def window_start(c_start: int, start: int, quotes: list[tuple[int, int]]) -> int:
    """Where the words before a span begin: the clause start, but never across a quotation
    boundary ("'… não existe', disse" must not read "não" as negating "disse")."""
    left = c_start
    for s, e in quotes:
        if e < start:
            left = max(left, e + 1)
        elif s <= start:
            left = max(left, s)
    return left


def inside(start: int, end: int, spans: Iterable[Sequence[int]]) -> bool:
    """True when [start, end) overlaps any span."""
    return any(start < s_end and s_start < end for s_start, s_end in spans)
