"""institutional-markers: deterministic, span-grounded markers of institutional language.

    from institutional_markers import scan
    for hit in scan("Two protesters were killed, the ministry claimed.", lang="en"):
        print(hit.marker, hit.subtype, hit.quote)

No model, no network, no state, standard library only. Every hit is a verbatim span of the
input (``hit.quote == text[hit.start:hit.end]``). The library never scores, never counts
across texts and never compares parties: see docs/adr/0001-shared-marker-library.md.

Precision is NOT shipped. Measure each marker version on your own corpus with the rubrics
in rubrics/ before you rely on it.
"""
from __future__ import annotations

from ._markers import MARKER_VERSIONS, MARKERS
from ._scan import LANGS, scan
from ._types import Hit, MarkerSpec

PACKAGE_VERSION = "0.6.0"

__all__ = ["scan", "Hit", "MarkerSpec", "MARKERS", "MARKER_VERSIONS", "LANGS",
           "PACKAGE_VERSION"]
