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
