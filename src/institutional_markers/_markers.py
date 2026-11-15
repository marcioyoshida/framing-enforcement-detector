"""The marker registry. A version string changes on ANY change to that marker, in any pack."""
from __future__ import annotations

from ._types import MarkerSpec

MARKERS: dict[str, MarkerSpec] = {m.name: m for m in (
    # Institutional: how a text applies its rules (ADR 0001 §4).
    MarkerSpec("exception_clause", "exception-v1", "institutional"),
    MarkerSpec("burden", "burden-v2", "institutional", ("burden", "presumption")),
    MarkerSpec("discretion", "discretion-v1", "institutional", ("reserved", "review_closed")),
    # Comparison building blocks: single-passage features a consumer may pair and compare.
    MarkerSpec("agentless_passive", "agentless-v1", "comparison",
               ("harm", "sanction", "removal", "error")),
    MarkerSpec("hedge", "hedge-v1", "comparison", ("adverb", "label", "report_conditional")),
    MarkerSpec("attribution_verb", "attribution-v1", "comparison",
               ("neutral", "distancing", "endorsing")),
)}

MARKER_VERSIONS: dict[str, str] = {name: m.version for name, m in MARKERS.items()}
