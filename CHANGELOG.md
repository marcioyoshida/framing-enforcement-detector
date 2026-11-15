# Changelog

Package versions follow semver (ADR 0001 §7): patch = docs/tests only; minor = a new marker
or a marker version bump; major = an interface change. **Every marker version change is
listed here.** A consumer that upgrades re-measures the markers whose version changed.

## 0.3.0 — 2026-11-15

- `burden` **burden-v2 → burden-v3** (Portuguese rules only; English behaves as in v2, but
  the version string is per marker, so consumers re-measure `burden` in both languages).
  - Why: measured by a consumer on fresh audit-court and court documents, blind, every hit:
    **v2 precision 0.58 (35 of 60): pt 0.79 (23 of 29), en 0.39 (12 of 31).** The pt misses
    were a burden rule REPORTED rather than stated by the author: a quoted precedent
    ("Enunciado do Acórdão …"), case law cited "no sentido de que …", a party's view the court
    rejects ("ao entender que …"). A pt burden is now dropped when its clause holds one of
    those cues.
  - English is NOT fixed: court opinions state who bears a burden as abstract doctrine far
    more often than they apply it, and wording does not separate the two. A consumer with a
    court-heavy English corpus should not rely on `burden` in English.
  - Known limit (unchanged since v0.1.0): the three-word negation window can cross a comma
    ("não procede, pois cabe ao gestor …" is dropped). Fixing it touches every marker.
  - Library reference set (`eval/heldout2.jsonl`): unchanged from v0.2.0.

## 0.2.0 — 2026-11-15

- `burden` **burden-v1 → burden-v2.** Consumers re-measure `burden`; every other marker is
  unchanged.
  - Why: measured by a consumer on its own corpora (court opinions, agency rules, audit-court
    decisions), blind, every hit: **v1 precision 0.39 (30 of 77)**. Most errors were "burden"
    in the economic or paperwork sense, a bare mention of a presumption (usually a party's
    defence or a heading), and presumptions stated as law.
  - "Burden" now only in the proof sense: an act verb on it ("met / carried / discharged its
    burden"), "bears the burden **of proof**", "the burden of proof rests on …", "the burden is
    on X to prove …". "Bear / shoulder the burden" without "of proof" no longer fires.
  - A presumption only as an act on it: "the presumption was rebutted", "afastou a presunção",
    "a presunção restou ilidida". "Is presumed", "presume-se", "é presumido" and a bare
    "presunção de legitimidade / boa-fé …" no longer fire.
  - A burden inside a party's reported argument ("the State argues that …", "o responsável
    alega que …") is dropped.
  - Library reference set (`eval/heldout2.jsonl`, not used to make these changes): burden
    en P 1.0 R 0.55, pt P 1.0 R 0.46 (v1: en P 1.0 R 0.91, pt P 1.0 R 0.82). Overall
    span P 0.986, R 0.771.

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
