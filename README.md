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

## Output Format

For any prompted text:
1. Overall composite score
2. Dimension-level scores with short rationales and evidence excerpts
3. Primary domain classification
4. Confidence note
5. Optional comparative flag (when prior corpus context is available)

## Domain Notes

Surface vocabulary changes by domain (peer review “rigor,” prosecutorial “discretion,” platform “trust and safety,” medical “precautionary principle,” etc.), but the underlying dimensions remain the same.

## Implementation

This repository documents the scoring protocol. It can be implemented as:
- A prompted LLM agent
- A fine-tuned classifier with human review
- A hybrid system

Comparative / longitudinal mode (scoring against prior texts from the same institution) substantially improves detection of the subtler dimensions.

## License

MIT — see LICENSE if added.

---

Analytical tool only. Not a determination of institutional motive or legal violation.
