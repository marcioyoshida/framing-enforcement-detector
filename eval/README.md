# Reference measurement

**These numbers say the patterns work at all. They are not a precision any consumer may
use.** The texts are invented and short; real pages are longer, messier and differently
distributed. Measure each marker version on your own corpus with the [rubrics](../rubrics/)
before relying on it (ADR 0001 §6).

## Files

| File | What it is | Labelled by |
|---|---|---|
| `dev_2026-11-15.jsonl` | 198 invented texts (98 en, 100 pt), 188 labels. **Development set.** It started as the first blind held-out set and was consumed: the patterns were fixed after seeing its errors. | an independent labeller who read only the rubrics |
| `dev_firstpass_result_2026-11-15.json` | The one blind score of the first-draft patterns on that set, before any fix. Kept as a record. | — |
| `heldout2.jsonl` | The reference held-out set, written after the patterns were frozen. Scored **once**. | a second independent labeller who read only the rubrics |
| `heldout2_result_2026-11-15.json` | That single score. This is the reference measurement for v0.1.0. | — |

## How a hit is matched

A hit matches a label when the marker is the same and the spans **overlap** (a labeller
may include an article or an object the pattern leaves out). Matching is one-to-one.
`scripts/measure.py` reports, per marker and language:

- **P / R:** span precision and recall with `include_defined=True`, ignoring `invoked`;
- **P(def) / R(def):** what a consumer sees by default (invoked hits only), against the
  invoked labels;
- **inv / sub:** `invoked` and `subtype` accuracy over matched pairs.

## What the first blind pass found (fixed before the reference set was written)

The first-draft patterns scored span P 0.987, R 0.830 and default-mode P 0.831 on the first
blind set. The errors fell into classes, each fixed in general rather than case by case:

- **Single-quoted quotations** were not recognised as quotations, so the speaker's own
  words counted as the text's voice (most `invoked` errors).
- **Negation crossed a quotation:** "'… não existe', disse" read "não" as negating "disse".
- **A modal after the span was not seen** ("in exceptional circumstances, the deadline may
  be extended"), and drafting verbs ("the regulation provides that") were not read as
  defining. Future tense ("will be assessed case by case") was wrongly read as defining.
- **Wording gaps:** derogation, "dispensed with", isentas, "é dispensável", "no right of
  appeal", "a juízo exclusivo", "presumably", "relatou", "prosecutors say", longer gaps
  before "that"/"que", and reported speech closed by an inverted verb.

## Reference result — v0.1.0 on `heldout2.jsonl` (scored once, 2026-11-15)

180 invented texts (90 en, 90 pt), 188 labels, written by a labeller who saw only the
rubrics, after the code was frozen.

| Marker | Lang | Hits | Labels | P | R | P (default) | R (default) | `invoked` acc. | subtype acc. |
|---|---|---|---|---|---|---|---|---|---|
| agentless_passive | en | 17 | 19 | 1.00 | 0.90 | 1.00 | 0.88 | 1.00 | 1.00 |
| agentless_passive | pt | 13 | 18 | 1.00 | 0.72 | 1.00 | 0.73 | 1.00 | 1.00 |
| attribution_verb | en | 22 | 27 | 0.95 | 0.78 | 0.95 | 0.88 | 1.00 | 1.00 |
| attribution_verb | pt | 20 | 27 | 1.00 | 0.74 | 1.00 | 0.75 | 1.00 | 1.00 |
| burden | en | 10 | 11 | 1.00 | 0.91 | 1.00 | 0.62 | 0.80 | 1.00 |
| burden | pt | 9 | 11 | 1.00 | 0.82 | 0.88 | 0.88 | 0.89 | 1.00 |
| discretion | en | 10 | 12 | 1.00 | 0.83 | 1.00 | 0.78 | 1.00 | 1.00 |
| discretion | pt | 9 | 12 | 1.00 | 0.75 | 1.00 | 0.78 | 1.00 | 1.00 |
| exception_clause | en | 8 | 12 | 1.00 | 0.67 | 1.00 | 0.62 | 1.00 | — |
| exception_clause | pt | 10 | 11 | 1.00 | 0.91 | 1.00 | 0.88 | 1.00 | — |
| hedge | en | 15 | 14 | 0.93 | 1.00 | 0.92 | 1.00 | 1.00 | 1.00 |
| hedge | pt | 12 | 14 | 1.00 | 0.86 | 1.00 | 0.91 | 1.00 | 1.00 |
| **overall** | | **155** | **188** | **0.987** | **0.814** | **0.976** | **0.815** | | |

Per cell n is small (8–27 hits): read the overall row, and treat any one cell as a hint.

**What it says:** when a marker fires it is almost always right; it misses about one label
in five. That is the expected shape for closed word lists.

**Residual errors, recorded and NOT fixed** (fixing them against this set would consume it;
they are the v0.2 candidates, to be confirmed on a fresh set):

- **Wording outside the lists** (most misses): "was held", "conceded", "replied" /
  "respondeu", "contou", "esclareceu", base-form "maintain", "lifted the ban", "it falls to
  … to prove", "recai sobre X o ônus", "ao inteiro arbítrio", "a nosso exclusivo critério",
  "não cabe mais recurso", "Exceptionally" (en), "cannot be appealed", "ficam suspensos os
  prazos", "foi interditada", "foi dispensado".
- **Agent check:** "por discurso de ódio" (a cause) read as an agent; "had already been
  seized" missed ("already" is not an allowed adverb).
- **Reporting conditional:** only "teria"/"estaria" are covered; "alcançariam" is missed.
- **Endorsing/distancing verbs without "that"/"que"** ("admitted the readings were wrong",
  "admitiu falhas") are missed by design (the strict complement keeps "confirmed the
  sentence" out).
- **False positives (2):** "the record shows that" (a document as speaker), "so called
  because of its iron arches".
- **`invoked` disagreements (3):** "could not meet the burden" and "must now justify" read
  as defining by their modal; "nos termos do edital, presume-se" read as applied.

## v0.2.0: `burden-v2` on `heldout2.jsonl`

`burden-v2` was changed because of errors on a consumer's real corpora, not on this set, so
this set still measures it fairly. Only the burden rows move (`heldout2_result_v0.2.0.json`):

| Marker | Lang | v1 P | v1 R | v2 P | v2 R |
|---|---|---|---|---|---|
| burden | en | 1.00 | 0.91 | 1.00 | 0.55 |
| burden | pt | 1.00 | 0.82 | 1.00 | 0.46 |

Recall drops because v2 no longer counts "is presumed", "presume-se" or a "burden" without
proof language. On invented text those were mostly right; on real decisions they were
mostly wrong (v1 measured 0.39 there). **Invented-text precision did not predict real
precision for this marker.**

## v0.3.0: `burden-v3`

Portuguese-only change (a burden rule reported rather than stated is dropped). The library
reference set does not exercise it: every row is identical to v0.2.0
(`heldout2_result_v0.3.0.json`).

## Consumer measurements of `burden` on real documents

Reported by a consumer, blind, every sampled hit, a different labeller per version on
documents no earlier labeller saw. These are that consumer's numbers on that corpus, not
precision anyone else may use; they are recorded because they show how far invented-text
results can sit from real ones.

| Version | Corpus | en | pt | Overall |
|---|---|---|---|---|
| burden-v1 | agency rules, court opinions, audit-court decisions | 0.45 | 0.31 | 0.39 (30 of 77) |
| burden-v2 | fresh court opinions, audit-court decisions | 0.39 (12 of 31) | 0.79 (23 of 29) | 0.58 (35 of 60) |
| burden-v3 | fresh audit-court special audits, 29 decisions | — | 0.842 (32 of 38) | — |

The consumer stopped at v3 (bar 0.85). English court text states burdens as doctrine far
more than it applies them, and wording does not tell the two apart. In Portuguese, about a
third of the correct hits hinge on the stock-line reading in `rubrics/burden.md`; under the
strict reading v3 is about 0.55.

## Consumer measurements of `discretion` on real documents

Same consumer, same conditions, two separate blind labellers (one per language). The
reading was fixed **before** labelling: `yes` only when the document, in its own voice,
reserves a decision in its own matter or closes it to review; doctrine, permissive rule
text, quoted or paraphrased material and other senses are `no`.

| Version | Corpus | en | pt |
|---|---|---|---|
| discretion-v1 | fresh agency notices and rules, supreme-court and appeals-court opinions; audit-court decisions | 0.32 (13 of 41) | 0.19 (6 of 32) |

Counting doctrine as `yes` too gives about 0.4 in both languages. In English, court
opinions scored 1 of 28. Agency text scored 12 of 13, but 10 of those were the same
meeting-notice sentence. Of 73 hits, 54 were false: 27 quoted or paraphrased (earlier
decisions, party arguments, transcribed opinions, statute text), 12 doctrine and 12 other
senses (common-law "case-by-case", section headings). Telling a court's own holding from
its account of someone else's words is not something a word list can do.

