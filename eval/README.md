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

## Consumer measurements of the comparison markers on real documents

Same consumer, 2026-11-16, library 0.3.0. One blind labeller per marker and language,
who saw only that marker's rubric, rulings written before labelling, and the sample (up
to 35 hits per cell, at most 4 per document in English and 6 in Portuguese, except
passives, which were taken whole). **Default mode**: the hits a consumer sees (`invoked`
only). A hit counts when the labeller says the form is right **and** the span is in the
document's own voice, not inside a direct quotation.

Corpus: **en**, US federal criminal and civil court filings released by a prosecutor's
office (100 documents, mostly OCR'd scans); **pt**, audit-court decisions (9 decisions,
551 pages). Legal and audit text, not news: a news consumer still measures its own.

| Marker | Version | en | pt | Subtype accuracy (correct hits) |
|---|---|---|---|---|
| agentless_passive | agentless-v1 | 0.94 (33 of 35) | 0.75 (21 of 28) | en 33/33, pt 22/25 |
| hedge | hedge-v1 | 0.97 (34 of 35) | 0.86 (30 of 35) | 34/34, 33/33 |
| attribution_verb | attribution-v1 | 0.69 (24 of 35) | 0.86 (30 of 35) | 27/27, 31/31 |

The Portuguese passive cell is under 30 because the whole corpus held only 28 hits.

**What went wrong.** These were the v0.4 candidates; v0.4.0 fixed most of them (see
`CHANGELOG.md` and the v2 measurement below):

- **Quotation the library did not see** (12 hits across cells): excerpts transcribed with
  "(...)" elisions and no opening mark in view, block quotes of a party's petition, a
  quoted e-mail, and a filing quoting another party's language.
- **Fixed phrases that are not speech** (`attribution_verb`): pt "no que diz respeito" /
  "diz respeito" (3 hits), "se mostram" ("prove to be"); en "said" as an adjective ("said
  Commonwealth"), "unless otherwise stated", "something to be said for", "writes
  eloquently" (manner, no statement).
- **Negation and modality missed** (`attribution_verb`): "nowhere alleges", modal "could
  say", present-habitual "the agreements say".
- **Wrong verb sense** (`agentless_passive`): pt "foi atingida / atingido" means "was
  reached" in audit text, not harm (3 hits, subtype wrong); an agent named by "pela/pelo"
  after an adverb and a line break was missed (2 hits); hypothetical "after it has been
  removed" (en).
- **True counterfactuals read as reporting conditionals** (`hedge`, pt): "se … não tivesse
  sido firmado, … teria sido firmado".
- **"So-called" introducing a technical term** without doubt ("the so-called KYC
  standard"): 1 hit.

### v2 (library 0.4.0) on fresh documents

Same consumer, same rulings, six **new** blind labellers, 2026-11-16. The documents were
never labelled for these markers. **en**: supreme-court and appeals-court opinions plus a
few agency rules (25–29 documents per cell). **pt**: audit-court decisions (27–30 per
cell). 35 hits per cell, at most 3 per document, default mode.

| Marker | Version | en | pt | Subtype accuracy (correct hits) |
|---|---|---|---|---|
| agentless_passive | agentless-v2 | 1.00 (35 of 35) | 0.94 (33 of 35) | 35/35, 32/33 |
| hedge | hedge-v2 | 0.94 (33 of 35) | 0.89 (31 of 35) | 33/33, 34/34 |
| attribution_verb | attribution-v2 | 0.91 (32 of 35) | 0.94 (33 of 35) | 32/32, 34/34 |

The corpus differs from the v1 measurement (opinions, not filings), so read the two tables
side by side, not as a controlled A/B.

**Remaining errors** (the v0.5 candidates; v0.5.0 fixed most of them, see v3 below):

- **Quotation the library cannot see** (pt, 4): a party's petition or a newspaper excerpt
  reproduced as a block without marks ("grifo do peticionante").
- `attribution_verb`: en "claims" as a plural noun before a that-clause ("claims that were
  dismissed"), "says nothing" (negation by object); pt "aponta para" + noun ("points to",
  evidence, not speech).
- `hedge`: en "so-called" before a neutral legal term ("the so-called Spending Clause");
  pt "teria sido" inside an indirect question.
- `agentless_passive`: pt "teria sido encerrada" (a conditional auxiliary, which the rubric
  excludes); "pela Lei 12.651" (an agent the duration/amount filter must not hide);
  "inabilitada" typed `sanction` where the labeller read removal.

### v3 (library 0.5.0) on fresh documents

Same consumer, 2026-11-16. Every cell used new blind labellers, documents no earlier
comparison labeller saw, and rulings written before labelling; 34–35 hits per cell, at most 3
per document. **en**: Supreme Court opinions (mostly the 2024 term), a few appeals-court
opinions and agency rules. **pt**: audit-court decisions.

| Marker | Version | en | pt |
|---|---|---|---|
| agentless_passive | agentless-v3 | 0.97 (33 of 34) | 0.97 (34 of 35) |
| hedge | hedge-v3 | 1.00 (33 of 33)* | 0.94 (33 of 35)*, 0.89 (31 of 35) |
| attribution_verb | attribution-v3 | **0.74 (26 of 35), twice** | 0.89 (31 of 35)*, 0.77 (27 of 35) |

\* Round 1. These fixes were then made from that round's errors, and v3's later changes to
these markers only remove hits, so the figure is the v3 subset of that fresh sample. The
second figure is a second fresh round.

**English attribution in court opinions does not reach the bar.** Two fresh rounds gave 0.74
each, and each round's misses were new forms:
- verb senses that are not speech: "confirms that the preconditions are met" (verifies),
  "would have said so", "a conclusion confirmed by the fact";
- "claims" as a noun after "bring" or "defeat";
- declarations or a contract as the subject.

Opinions narrate other people's words in too many ways for a word list. Measure before using
it on court text; on English news headlines a consumer measured 0.90.

**Portuguese attribution depends on the reading.** Round 2's labeller counted documents a body
wrote ("a Nota Técnica informou", "o relatório afirma") as non-speakers. Round 1's did not.
The rubric now says a body speaking through a document it wrote still counts, so ≈ 0.89 is the
reading the library intends. Decide this before labelling your own sample.

**Not fixed in v0.5.0** (still open after v0.6.0 unless noted below):
- en "so-called" before a neutral legal term;
- passages reproduced without any marks and without an emphasis note;
- `removal` typed for "removed to federal court" and `harm`-less "fired" (a gun);
- "if … were removed";
- pt "informa" meaning "shapes";
- OCR "Relatou" for "Relator".

### attribution-v4 (library 0.6.0) on fresh documents

Same consumer, 2026-11-16. Only English `attribution_verb` changed (attribution-v3 → v4); every
other marker returns exactly the same hits as in 0.5.0, so its cells above still hold. That
includes Portuguese attribution: v4's Portuguese hits are identical to v3's on every audit-court
document the consumer measured.

**How v4 was made.** The fixes come from the two failed English rounds above and from reading
about 230 unlabelled hits from documents those rounds had already used (Supreme Court opinions
of the 2023–2025 terms, appeals-court opinions, agency rules). None came from the measurement
documents. On those development hits the tuner's own reading put v3 at about 0.7 and v4 at
about 0.9; that reading is not a measurement.

**Measurement.** One fresh round. US federal court opinions published on GovInfo in September
2025: Second Circuit, Court of Federal Claims and district courts. No document had been seen by
any labeller or by the tuner before v4 was frozen. 505 v4 hits in 59 of the 80 opinions; 35
were drawn at random, at most 3 per document. A new blind labeller had only the rubric, the
same rulings as round 2 above and the contexts.

| Marker | Version | en | pt |
|---|---|---|---|
| attribution_verb | attribution-v4 | **0.86 (30 of 35)**, one round | 0.89 (31 of 35)*, unchanged hits |

\* The v3 figure. The hits are the same.

Subtype accuracy was 30 of 30. **0.86 clears the 0.85 bar by one item.** With 35 items the
uncertainty is roughly ±0.1, so treat English court text as borderline and measure your own
sample. The five errors were again forms no earlier round showed:
- a medical test as the subject ("an MRI revealed", "a repeat echocardiogram revealed"), twice;
- "account stated", the name of a cause of action;
- "herein expressly stated";
- "plaintiffs who have alleged actual damages", a generic requirement.

**What v4 gives up.** v4 only removes hits: about 15% of English attribution hits on the
development corpus, with no new span. On the reference held-out set, recall drops from 0.67 to
0.63 with precision unchanged: '"…," the governor declared.' is no longer found, because
"declared" now needs a that-clause or a colon. That is a v0.7 candidate. It was seen on the
held-out set after v4 was frozen, so fixing it needs a fresh set.

### attribution-v5 (library 0.7.0)

One change: "declared / declares" right after a closing quotation counts again (the v0.6.0
regression above). v5 = v4 plus that pattern. On the development pools it adds one span and
removes none, and every other marker is unchanged.

**Second fresh round on court opinions.** 80 more US federal court opinions from the same
GovInfo month, from the next page of the listing (Eighth Circuit and district courts), none seen
before. 248 v5 hits in 36 documents; 35 drawn at random, at most 3 per document. A new blind
labeller had the same rubric and rulings.

| Marker | Version | en | pt |
|---|---|---|---|
| attribution_verb | attribution-v5 | **0.89 (31 of 35)**; v4 had 0.86 (30 of 35) | 0.89*, unchanged hits |

\* The v3 figure. The Portuguese hits have been identical since then.

The new pattern fired on none of the 248 hits, so this round also measures v4's code a second
time. Subtypes 33 of 33. The four errors:
- two passages reproduced as block quotes without quotation marks (a known gap: nothing marks
  them);
- "his discrimination claims, asserting that …", where "claims" is a noun after a noun;
- "the certified trust fund statement reveals that …", where a document is the subject.

These are v0.8 candidates. The reference held-out set's English attribution recall is back to
0.67 (precision 1.00). The fixed item was seen when v0.6.0 was scored, so that figure is no
longer blind for it.

