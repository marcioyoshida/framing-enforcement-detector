# NLP Techniques for the Framing Enforcement Detector

This document summarizes practical NLP approaches for implementing the multi-dimensional scoring protocol defined in the README.

The task is multi-aspect ordinal classification: each of the 14 dimensions is scored independently on a 0–5 scale, ideally with supporting evidence excerpts. Many signals are subtle, context-dependent, or comparative.

## 1. Classical feature-based methods
- **Approach**: TF-IDF / bag-of-words / n-grams + linear models (logistic regression, linear SVM) or gradient boosting.
- **Strengths**: Fast, interpretable, low data requirements, excellent baselines for explicit lexical cues.
- **Limits**: Weak on long-range context, implicit framing, and subtle dimensions (temporal shift, omission, authority substitution).
- **Use case**: Cheap first-pass filter or high-precision detectors for overt phrases (“heightened scrutiny”, “precautionary principle”, “trust and safety”, etc.).

## 2. Fine-tuned encoder models
- **Models**: BERT, RoBERTa, DeBERTa, or domain-adapted variants (LegalBERT, SciBERT, BioBERT, SPECTER, etc.).
- **Setup**: Multi-task or multi-label heads (shared encoder + per-dimension classifiers or ordinal regressors). Focal loss or ordinal regression helps with imbalance.
- **Strengths**: Highest accuracy once labeled data exists; efficient inference; strong on standard classification benchmarks.
- **Limits**: Requires labeled examples per dimension; less flexible for open rationales or pure comparative mode without additional engineering.
- **Note**: Fine-tuned smaller transformers frequently match or outperform pure in-context LLMs on classification tasks when sufficient labels are available.

## 3. LLM prompting / LLM-as-judge (recommended starting point)
- **Approach**: Zero-shot or few-shot structured prompting with explicit rubrics.
- **Key practices that improve reliability**:
  - Dimension-specific rubrics with clear 0–5 anchors and positive/negative examples.
  - Quote-before-score (extract evidence first, then assign the number).
  - Separate scoring calls per dimension (or carefully grouped) to avoid signal bleed.
  - Chain-of-thought / step-by-step reasoning.
  - Low temperature + structured JSON output.
  - Few-shot calibration examples.
  - Optional reflection or self-consistency passes.
- **Strengths**: No training data required; handles subtle and comparative patterns; produces human-readable rationales and evidence; easy to iterate.
- **Limits**: Cost, latency, and the need for calibration against human judgments. Positional and verbosity biases must be managed.

## 4. Hybrid approaches (recommended long-term)
- **LLM-generated labels → fine-tune small model**: Use a strong LLM to score a seed corpus, then train a BERT-class model for production speed and cost.
- **Explanation-guided training**: LLM produces explanations that become additional features for a smaller classifier.
- **Comparative / longitudinal mode**: Retrieve prior texts from the same institution or domain and score the current excerpt relative to them. Especially valuable for temporal shift and omission dimensions.
- **Principle-based prompting**: Agents first extract distinguishing principles from examples, then apply them.

## Practical implementation priority

| Approach | Data needed | Best for | Recommendation |
|----------|-------------|----------|----------------|
| LLM-as-judge (structured + CoT + few-shot) | None / few examples | Rapid start, subtle dimensions, explainability | Start here |
| Fine-tuned encoder (multi-task) | Hundreds of labels per dimension | Production scale & consistency | Highest accuracy path |
| Hybrid (LLM labels → small model) | Moderate | Best balance | Strong long-term choice |
| Classical TF-IDF + linear | Minimal | Explicit cues & baselines | Useful filter layer |

## Calibration advice
- Define tight rubrics with score anchors and examples before scaling.
- Force evidence quotation before the numeric score.
- Score dimensions independently where possible.
- Measure agreement against human annotations on a held-out set and iterate.
- Prefer smaller ordinal scales or well-anchored 0–5 scales over vague high-range scores.

See `prompts/` for ready-to-use templates.
