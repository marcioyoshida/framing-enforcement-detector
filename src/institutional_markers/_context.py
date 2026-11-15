"""Clause bounds, quotations and token windows, all on offsets shared by both texts."""
from __future__ import annotations

import re
from bisect import bisect_left, bisect_right
from typing import Iterable, Sequence

_WORD = re.compile(r"\w+")
#: A full stop ends a clause only before whitespace and an upper-case letter, a quote or the
#: end of text, so "Art. 75" and "n. 123" stay inside one clause.
_STOP = re.compile(r"[;!?\n]|\.(?=\s+[A-ZÀ-Ý\"“«']|\s*$)")


class Clauses:
    def __init__(self, original: str) -> None:
        self._stops = [m.start() for m in _STOP.finditer(original)]
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
_SQ_CLOSE = re.compile(r"(?<=[^\s'])'(?=[\s.,;:!?)\]}\"]|$)")


def quoted_intervals(folded: str) -> list[tuple[int, int]]:
    """Interiors of quoted passages. Typographic quotes are already folded to '"' and "'"."""
    marks = [i for i, c in enumerate(folded) if c == '"']
    spans = [(marks[k] + 1, marks[k + 1]) for k in range(0, len(marks) - 1, 2)]
    opens = [m.start() for m in _SQ_OPEN.finditer(folded)]
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
