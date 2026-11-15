"""Case and accent folding that keeps every offset.

Patterns match the folded text; hits are reported as offsets into the ORIGINAL text. That
only works if folding maps each character to exactly one character, so this module never
uses a normalisation that changes length (NFD, casefold of "ß", lower of "İ").
"""
from __future__ import annotations

import unicodedata
from functools import lru_cache

#: Typographic quotes and apostrophes folded to their ASCII form, one for one.
_PUNCT = {
    "‘": "'", "’": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "‟": '"', "″": '"',
    "«": '"', "»": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-",
    " ": " ", " ": " ",
}


@lru_cache(maxsize=4096)
def _fold_char(ch: str) -> str:
    if ch in _PUNCT:
        return _PUNCT[ch]
    low = ch.lower()
    if len(low) != 1:
        low = ch
    base = unicodedata.normalize("NFD", low)[0]
    # A lone combining mark (text already decomposed) folds to itself; patterns will not
    # match across it, which is the documented limit: pass NFC text.
    return base


def fold(text: str) -> str:
    """Lower-case, strip accents, ASCII quotes and dashes; same length as ``text``."""
    out = "".join(_fold_char(c) for c in text)
    assert len(out) == len(text)
    return out
