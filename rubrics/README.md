# Labelling rubrics

One rubric per marker. A labeller reads **only the rubric and the text**, never the
patterns in `src/`. Whoever tunes the patterns must not label the set used to measure them.

## What is labelled

Each record is one short text (a sentence or a few) and every marker span a careful reader
finds in it:

```json
{"id": "en-0001", "lang": "en", "text": "...",
 "labels": [{"marker": "hedge", "quote": "reportedly", "subtype": "adverb", "invoked": true}]}
```

- `quote` is copied **verbatim** from `text`. If it appears more than once, add
  `"occurrence": 2` (1-based) for the one meant.
- `invoked` is `true` when the span is in the text's own voice **and** applies to this
  text's matter. It is `false` when the span is inside a direct quotation, only defines a
  rule ("may waive"), or sits in quoted law.
- A text with no marker gets `"labels": []`. These negatives matter as much as the
  positives.

## How a consumer measures precision

1. Run `scan(..., include_defined=True)` on its own sample of pages.
2. For each hit, a labeller answers the rubric's yes/no question, plus `invoked` and
   `subtype`.
3. Precision = yes / hits, per marker **and** per `version`, with n ≥ 30 per language.
   Subtype accuracy and `invoked` accuracy are reported separately from precision.

A version that has not been measured on the consumer's own corpus contributes nothing there.

## Rubrics

| Marker | Group | Rubric |
|---|---|---|
| `exception_clause` | institutional | [exception_clause.md](exception_clause.md) |
| `burden` | institutional | [burden.md](burden.md) |
| `discretion` | institutional | [discretion.md](discretion.md) |
| `agentless_passive` | comparison | [agentless_passive.md](agentless_passive.md) |
| `hedge` | comparison | [hedge.md](hedge.md) |
| `attribution_verb` | comparison | [attribution_verb.md](attribution_verb.md) |
