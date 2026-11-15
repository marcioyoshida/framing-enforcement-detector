# Changelog

Package versions follow semver (ADR 0001 §7): patch = docs/tests only; minor = a new marker
or a marker version bump; major = an interface change. **Every marker version change is
listed here.** A consumer that upgrades re-measures the markers whose version changed.

## 0.1.0 — 2026-11-15

First release of `institutional-markers` (ADR 0001).

- `scan(text, lang, markers, exclude, include_defined)` → `Hit(marker, version, start, end,
  quote, pattern_id, subtype, invoked)`. Python ≥ 3.11, standard library only.
- Languages: `en`, `pt` (Brazil).
- New markers:
  - `exception_clause` **exception-v1**
  - `burden` **burden-v1** (subtypes burden, presumption)
  - `discretion` **discretion-v1** (reserved, review_closed)
  - `agentless_passive` **agentless-v1** (harm, sanction, removal, error)
  - `hedge` **hedge-v1** (adverb, label, report_conditional)
  - `attribution_verb` **attribution-v1** (neutral, distancing, endorsing)
- Rules: offset-preserving accent and case folding; word-start matching; negation within
  three words (never across a quotation); quotations in double, single and typographic
  quotes are `invoked=False`; institutional markers with a modal in the clause, or after a
  drafting verb ("provides that", "estabelece que"), are `invoked=False`; agentless
  passives need a past-tense auxiliary, a closed verb list and no agent phrase.
- Rubrics for all six markers (`rubrics/`), a scoring script (`scripts/measure.py`), and a
  reference measurement on invented text (`eval/`).
- Reference measurement (`eval/heldout2.jsonl`, blind, scored once): span precision
  0.987, recall 0.814; default mode precision 0.976, recall 0.815. Not a precision any
  consumer may use: measure on your own corpus.
