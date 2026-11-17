# Framing Enforcement Detector

Analytical runbook agent for scoring texts and excerpts on framing, enforcement language, informational asymmetry, selective application patterns, and related institutional features.

Applicable across academia, law, medicine, regulators, finance, social media, technology platforms, NGOs, and other institutional sources.

**Scores reflect observable textual features only. They are diagnostic, not proof of intent or actual selective enforcement.**

## Purpose

Given a text or excerpt, the agent scores the intensity of language patterns associated with:
- Selective or asymmetric application of rules/standards
- Informational asymmetry and process opacity
- Narrative pre-emption
- Differential evidentiary or burden standards
- Institutional coordination signals

Higher scores indicate stronger textual alignment with these patterns. The framework is symmetric and can be applied to any source.

## Core Scoring Dimensions (0–5 each)

### Original dimensions
1. **Selective scope language** — Elastic or identity-conditioned definitions of harm, risk, or standards.
2. **Enforcement asymmetry cues** — Differential intensity language for comparable cases.
3. **Opacity and process control** — Limits on external verification or concentrated decision rights.
4. **Narrative pre-emption** — Framing that delegitimizes scrutiny of the rule or its application.
5. **Institutional coordination signals** — Heavy reliance on aligned external bodies.
6. **Legitimacy-preserving abstraction** — Emphasis on formal neutrality while remaining silent on outcome distributions.

### Additional subtle dimensions
7. **Temporal standard shift** — Criteria or burden change across time for comparable cases.
8. **Evidentiary asymmetry** — Differential demands for evidence quality or quantity.
9. **Burden and presumption reversal** — Who must prove safety, legitimacy, or absence of harm.
10. **Exceptionalism / emergency framing** — Special conditions used to suspend ordinary rules.
11. **Identity- or affiliation-contingent qualifiers** — Application conditioned on speaker or institutional identity.
12. **Omission and selective silence** — Systematic absence of expected comparative cases (strongest in comparative mode).
13. **Authority substitution** — Secondary institutional endorsement replacing primary evidence.
14. **Risk externalization language** — Downside risk framed as exclusively external to the enforcing institution.

### Tier 3: Network & Attribution Asymmetry Dimensions (0–5 each) Gemini

15. **Attribution laundering / proxy indirection** — Reliance on unverified secondary sources, circular citations, or commercial cut-outs that obscure primary institutional sponsorship.
16. **Dialect & subcultural mimicry** — Abrupt shifts between standardized bureaucratic framing and hyper-local slang, regional idioms, or niche grievance framing designed to simulate grassroots origin.
17. **Whataboutism / false equivalence pivot** — Structural deflection where scrutiny of an actor's policy is countered by invoking an unrelated historical or external grievance rather than addressing the primary claim.
18. **Strategic flooding / volume camouflage** — Excessive deployment of benign cultural, humanitarian, or technical boilerplate used to bury or crowd out critical substantive disclosures.
19. **Regulatory & jurisdictional arbitrage** — Language exploiting gaps between national laws, academic norms, and commercial agreements (e.g., framing state-directed policy initiatives strictly as private exchanges).


### Symmetry & Transparency Counter-Signals (Diagnostic Offsets)

To prevent false positives on rigorous legal, scientific, or regulatory texts, the agent also logs explicit counter-signals:

- **Explicit provenance & funding disclosure** — Clear attribution of institutional sponsorship, conflicts of interest, or primary data sources.
- **Falsifiable & symmetric criteria** — Explicit statement of conditions under which the rule applies equally to allies, internal actors, or the enforcing institution itself.
- **Acknowledged trade-offs & limitations** — Transparent discussion of uncertainties, edge cases, or unintended consequences.

## Output Format (JSON & Markdown)

For any prompted text (or `(Text_A, Text_B)` comparative pair):

1. **Profile Metrics:** Top-3 Dominant Pattern Profile, Max-Cluster Score, and Overall Composite Score.
2. **Span-Grounded Dimension Scores:** Score (`0–5`), verbatim evidence substring (`quote`), and brief rationale.
3. **Counter-Signal Log:** Detected transparency or symmetry markers.
4. **Primary Domain Classification & Confidence Note.**
5. **Comparative Delta Flag:** Explicit shift analysis when a baseline corpus or paired text is provided.

## Domain Notes

Surface vocabulary changes by domain (peer review “rigor,” prosecutorial “discretion,” platform “trust and safety,” medical “precautionary principle,” etc.), but the underlying dimensions remain the same.

## Implementation

This repository documents the scoring protocol. It can be implemented as:
- A prompted LLM agent
- A fine-tuned classifier with human review
- A hybrid system

See [TECHNIQUES.md](TECHNIQUES.md) for an overview of NLP approaches (classical, fine-tuned encoders, LLM-as-judge, hybrids) and practical recommendations.

Ready-to-use prompt templates are in the [`prompts/`](prompts/) directory:
- `system_prompt.md` — base instructions
- `dimension_template.md` — reusable single-dimension scoring template
- `example_selective_scope.md` — worked example

Comparative / longitudinal mode (scoring against prior texts from the same institution) substantially improves detection of the subtler dimensions.

## Implementation: `institutional-markers` (deterministic markers)

The observable part of the protocol — wording you can point to in one text — is
implemented as a small Python library in [`src/institutional_markers/`](src/institutional_markers/).
It does **not** score, compare or judge. See [ADR 0001](docs/adr/0001-shared-marker-library.md).

- Python ≥ 3.11, standard library only. No model, no network, no state.
- English and Portuguese (Brazil).
- Every hit is a verbatim span: `hit.quote == text[hit.start:hit.end]`.

```python
from institutional_markers import scan

for h in scan("Two protesters were killed on Tuesday, the ministry claimed that police acted lawfully."):
    print(h.marker, h.subtype, repr(h.quote), h.invoked)
# agentless_passive harm 'were killed' True
# attribution_verb distancing 'claimed' True
```

| Marker | Group | Protocol dims | Subtypes |
|---|---|---|---|
| `exception_clause` | institutional | 10 | — |
| `burden` | institutional | 8, 9 | burden, presumption |
| `discretion` | institutional | 1, 3, 11 (wording) | reserved, review_closed |
| `agentless_passive` | comparison | 3, 14 (wording) | harm, sanction, removal, error |
| `hedge` | comparison | 8, 15 (wording) | adverb, label, report_conditional |
| `attribution_verb` | comparison | 8, 15 (wording) | neutral, distancing, endorsing |

`scan(text, lang="en", markers=None, exclude=(), include_defined=False)`:
`exclude` takes spans you already know are quoted law or citations; `include_defined=True`
also returns hits that only define a rule ("may waive") or sit inside a quotation.

**A single hit is not evidence of bias.** "Allegedly" is often legally required, and a
passive is often just style. Comparison markers only mean something when a consumer pairs
comparable cases, and that comparison is the consumer's decision.

**Measure before you rely on it.** Precision measured on one corpus does not transfer to
another. Label a sample of your own pages with the [rubrics](rubrics/) and key the result
by `hit.version`. The repository's own reference measurement is in [`eval/`](eval/).

```bash
python3 -m pytest                       # unit tests
python3 -I scripts/measure.py eval/heldout2.jsonl   # score a labelled set
```

Install a pinned tag: `pip install "institutional-markers @ git+https://github.com/marcioyoshida/framing-enforcement-detector@v0.7.0"`.

## License

MIT — see [LICENSE](LICENSE).

---

Analytical tool only. Not a determination of institutional motive or legal violation.
