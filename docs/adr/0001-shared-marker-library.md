# ADR 0001 — A shared marker library, not a scoring service

- **Status:** PROPOSED 2026-11-15. Nothing built. **Owner decided 2026-11-15: all six
  markers ship in v1** (§9 Q2). The other §9 questions are open.
- **Context date:** repository at `d7493de` (dimensions 1–19, counter-signals, scoring prompts).
- **Decision owner:** the repository owner (§9).

## 1. Context

This repository documents a **scoring protocol**. An LLM reads a text, quotes evidence and
scores 19 dimensions of institutional language from 0 to 5, then produces a composite score
and a comparative delta. Nothing is implemented yet, no labelled set exists, and no
agreement with human judgment has been measured.

Several internal document-intelligence products could use parts of it. The ones that ingest
institutional prose are court and audit-court decisions, agency releases, regulator notices
and rule versions. Each product already has its own engine, tenancy and display rules. The
question is how to share this work between them: as a **service** they call, or as a
**library** they import.

Evaluated on 2026-11-15, the two halves of the protocol answer differently:

| | LLM scoring (0–5, composite, comparative) | Observable markers (wording in one text) |
|---|---|---|
| Needs a model at runtime | yes | **no** |
| Same answer on every run | no: a comparable LLM framing baseline moved 0.620–0.665 macro-F1 between runs on one gold set | **yes** |
| Measured accuracy | none | none yet, but measurable per span (§6) |
| Consumers that would call it today | **none**: one rejects scores outright (it shows cited evidence and never verdicts); one closed hosted framing after a 0.30 macro-F1 test; one has framing parked until first customers | at least one (the first adopter's proposed dimensions); two more ingest regulator text |
| Data that would leave the consumer | whole documents, some under per-tenant encryption that must not cross a boundary | **none**: the code runs inside the consumer |

## 2. Decision

1. **Build the observable markers as a pure-Python library** in this repository. Each
   consumer imports it and runs it in-process.
2. **Do not build a scoring service now.** §8 says when to revisit.
3. **The protocol stays.** README dimensions, prompts and TECHNIQUES.md are unchanged. The
   library implements only the part of the protocol that is wording observable in one text.

## 3. What the library is

- **Name (proposed):** distribution `institutional-markers`, import `institutional_markers`.
  It is not named "framing" or "enforcement": consumers show marker names to readers, and the
  names must describe text, not judge an institution (§9 Q1).
- **Python ≥ 3.11, standard library only.** Consumers deploy to serverless runtimes by
  copying pure-Python source, so there are no wheels and no dependencies.
- **Deterministic.** Compiled pattern tables per language. No model, no network, no state.

### Interface

```python
from institutional_markers import scan, MARKERS, PACKAGE_VERSION

hits = scan(
    text,                      # one page or one passage, as the consumer stores it
    lang="pt",                 # "en" | "pt"
    markers=None,              # default: every marker in MARKERS
    exclude=[(120, 340)],      # spans the consumer already knows are quoted law or citations
    include_defined=False,     # True returns defined/quoted hits too (for labelling negatives)
)
# -> list[Hit]

@dataclass(frozen=True)
class Hit:
    marker: str          # "exception_clause"
    version: str         # "exception-v1"; bumped on ANY change to this marker's patterns
    start: int
    end: int
    quote: str           # always == text[start:end]; checked before return
    pattern_id: str      # which pattern fired, for error analysis
    subtype: str | None  # a closed class within the marker, e.g. "distancing"; None if the marker has none
    invoked: bool        # in this text's own voice and applied here (True) vs only defined,
                         # quoted or reported from someone else (False)
```

- **Every hit is a verbatim span.** `quote == text[start:end]` is asserted before return.
  A hit that cannot name its offsets does not exist. The protocol's own rule ("extract
  before scoring") is enforced in code here, not just asked of a model.
- **No scores, no composite, no counts across documents.** The consumer counts, thresholds
  and decides what to show.
- **`exclude`** exists because citation detection is the consumer's job: its own detector
  already knows where a statute is quoted. A marker inside an excluded span is never invoked.

### Rules every pattern obeys

These come from a consumer's relation-class tables, where each rule fixed a measured defect:

- **Accent and case folding** before matching (pt *ônus* = *onus*).
- **Patterns match at a word start.** A substring match would let *indeferiu* hit *deferiu*.
- **A negated marker is not a hit.** "não se aplica a dispensa" and "no waiver is granted"
  return nothing. There is no "negated" class to put them in.
- **Invoked, not defined.** "The agency may waive…" defines an exception. "The waiver is
  granted" invokes one. Only invoked hits return by default, because statutes and
  regulations define exceptions, burdens and discretion constantly. Counting definitions
  is the base-rate trap: a detector that fires in every corpus separates nothing.

## 4. Markers in the first version

Six markers in two groups: three that show how an institution applies its rules, and three
building blocks a consumer can compare across parties. **All six ship in v1** (owner,
2026-11-15). That means 12 pattern packs (six markers × en, pt), six rubrics, and fixtures
for every marker and language before the first tag.

### Institutional markers

| Marker | Version | Protocol dims | Invoked when the text… | en / pt examples |
|---|---|---|---|---|
| `exception_clause` | `exception-v1` | 10 | suspends, waives or overrides an ordinary rule **for this matter** | "the waiver is granted", "under emergency authority, the requirement is suspended" / "fica dispensada a licitação", "em caráter emergencial" |
| `burden` | `burden-v1` | 8, 9 | assigns a burden of proof or a presumption to a party | "the applicant has not met its burden", "is presumed" / "cabe ao responsável comprovar", "presume-se" |
| `discretion` | `discretion-v1` | 1 (wording), 3 (decision rights), 11 (wording) | reserves judgment or closes review | "at the discretion of the Director", "not subject to review" / "a critério da autoridade", "decisão irrecorrível" |

### Comparison building blocks

Asymmetric language is a **difference between two comparable passages**: the same act, or
the same rule, described differently for different parties. The library never compares.
These three markers are the single-passage features a consumer can pair and compare
itself. They are lexical, they give the same answer on every run, and readers recognise
them once they are pointed out.

| Marker | Version | Protocol dims | Subtypes | Fires on | en / pt examples |
|---|---|---|---|---|---|
| `agentless_passive` | `agentless-v1` | 3, 14 (wording) | `harm`, `sanction`, `removal`, `error` | a **past-tense** passive of a verb from a closed list, with **no agent phrase** in the same clause | "two protesters were killed", "the account was suspended", "mistakes were made" / "foram mortos dois manifestantes", "o perfil foi suspenso", "foram cometidos erros" |
| `hedge` | `hedge-v1` | 8, 15 (wording) | `adverb`, `label`, `report_conditional` | an epistemic hedge or distancing label attached to a claim | "reportedly", "allegedly", "purportedly", "so-called" / "supostamente", "alegadamente", "o chamado", "segundo relatos", and the reporting conditional "teria desviado" |
| `attribution_verb` | `attribution-v1` | 8, 15 (wording) | `neutral`, `distancing`, `endorsing` | a verb that introduces someone's statement, classified by a closed table | neutral "said", "stated" / "disse", "afirmou"; distancing "claimed", "alleged", "insisted" / "alegou", "alega", "insistiu"; endorsing "confirmed", "revealed", "acknowledged" / "confirmou", "revelou", "reconheceu" |

Rules specific to these three:

- **`agentless_passive` uses a closed verb list, past tense only.** Statutes and
  regulations are full of agentless passives ("the form shall be submitted", "deverá ser
  apresentado"), so modal and future passives never fire. Neither do adjectival passives
  ("is located", "está situado"). A clause with an agent ("by the police", "pela polícia")
  is not agentless and returns nothing.
- **`hedge` and `attribution_verb` inside a direct quotation are `invoked=False`.** They
  belong to the person quoted, not to the text's own voice.
- **No actor is attached.** Who a hedge or a passive is about is the consumer's
  entity-resolution job. The library returns the span. The consumer decides which actor or
  case it belongs to, and whether two spans are comparable.
- **A single hit means nothing about bias, and consumers must not show it as bias.**
  "Allegedly" is often a legal requirement when reporting an unproven accusation, and a
  passive is often just style. The signal, if there is one, is the **difference in
  distribution between comparable cases**. That comparison is the consumer's decision,
  under its own display rules (§5).
- **Base rate:** all three occur in almost every text. Their per-span precision is
  measurable (§6), but a raw count separates nothing. A consumer that elects or scores
  anything from counts alone will be measuring the base rate.

**Next candidates:** the README's three **counter-signals** (`provenance_disclosure`,
`symmetric_criteria`, `acknowledged_limits`). They are neutral, observable wording, and a
consumer can show them without implying anything about an institution. They are excluded
from v1 only to keep the first measurement small.

## 5. What the library will not contain

| Protocol part | Why it stays out |
|---|---|
| 0–5 scores, composite, max-cluster, dominant profile | not observable as a span; un-measurable as one number |
| Asymmetry itself: comparing spans across parties or cases | deciding that two cases are comparable is a judgment. The library returns the building blocks (§4); pairing and comparing them is the consumer's call |
| Dims 2, 4, 6, 14 as scores | they need two cases compared, or a reading of effect or intent. Dim 14's wording appears only as `agentless_passive` spans |
| Dims 5, 13 | they need a "relies on" edge between bodies. If wanted, that is a relation detector and a separate ADR |
| Dims 7, 12 | they need a corpus over time. Consumers that keep release histories compute them there |
| Dims 15–19 as scores (dim 15's wording appears only as `hedge` and `attribution_verb` spans) | proxy indirection and circular citation need multiple documents; dialect mimicry, whataboutism and flooding judge intent |
| Pairwise / comparative mode | the consumer's choice and the consumer's corpus; some consumers ban cross-document synthesis |
| Display names, colours, verdict words | each consumer's display rules govern what a reader sees |

## 6. Measurement: the library ships the method, each consumer ships the number

A precision figure measured on one corpus does not transfer to another. One consumer found
3.17 frames per document live against 1.3 in its gold set, and a model tuned toward one
distribution moved away from the other. So:

- **The library ships `rubrics/<marker>.md`:** one yes/no question per marker (*"Does this
  span itself invoke an exception that applies in this text's matter?"*), positive and
  negative examples (invoked, defined, quoted, negated), and a JSONL label schema. For the
  comparison markers the question is about form, not effect (*"Is this a past-tense
  passive with no agent in its clause?"*, *"Does this word hedge the claim it is attached
  to?"*). A marker's subtype (`distancing`, `harm`, …) is labelled and measured separately
  from whether the span is a hit at all.
- **Each consumer measures its own precision row** (n ≥ 30 spans per language, labelled by
  someone other than the person tuning) and keys it by the marker `version`. A version the
  consumer has not measured contributes nothing.
- **The library ships a reference measurement** on its own test fixtures, labelled as such.
  It shows the patterns work at all. It is not a precision any consumer may use.
- **Test fixtures are synthetic or public-domain government text.** This repository is
  public: no client documents, no personal data, no copyrighted excerpts.

## 7. Versioning and distribution

- **Per-marker versions** (`exception-v1` → `-v2`) change on any pattern or rule change.
  Consumers re-measure that marker and nothing else.
- **Package semver:** patch = docs/tests only; minor = a new marker or a marker version bump;
  major = an interface change. `CHANGELOG.md` lists every marker version change.
- **Distribution:** a git tag, pinned by each consumer
  (`institutional-markers @ git+https://github.com/marcioyoshida/framing-enforcement-detector@v0.1.0`),
  or the pure-Python source vendored at that tag. No package index until a second consumer
  ships.
- **Consumers pin.** An upgrade is a deliberate change in the consumer: bump, re-measure,
  replay its calibration. It is never automatic.
- **License:** the README says MIT but there is no `LICENSE` file. Add one before any
  consumer vendors the code.

### Repository layout after the change

```
README.md                    protocol (unchanged) + an "Implementation: markers" section
TECHNIQUES.md, prompts/      unchanged
pyproject.toml               stdlib-only package
src/institutional_markers/   __init__.py, scan.py, fold.py, packs/en.py, packs/pt.py
rubrics/                     one labelling rubric per marker
tests/                       fixtures per marker: invoked, defined, quoted, negated, excluded
docs/adr/                    this file
CHANGELOG.md
```

## 8. When a service would make sense

Revisit a hosted scoring service only when **all three** hold:

1. **A production-funded model is approved for it.** A personal subscription cannot back
   production traffic, and the cheapest hosted option measured 0.30 macro-F1 on a framing test.
2. **A gold set with measured agreement exists** for the dimensions it would serve, per
   language and per domain.
3. **At least two consumers commit** to using scores or comparative mode under their own
   display rules.

If that happens, it follows the existing internal-API pattern: one API key per consumer,
signed calls, a contract version each consumer pins in its tests, and display rules each
consumer enforces. The marker library stays as its deterministic first pass.

## 9. Open questions for the owner

1. **Package name:** `institutional-markers`, or another?
2. ~~**First markers:** all six in §4, or the three institutional markers first?~~
   **DECIDED 2026-11-15: all six ship in v1.**
3. **Counter-signals:** add them in v1 as well (nine markers), or keep them as next?
4. **Where it lives:** in this repository beside the protocol (proposed), or a separate repo?
