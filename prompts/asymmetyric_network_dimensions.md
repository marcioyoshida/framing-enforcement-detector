# Tier 3 Module: Network & Attribution Asymmetry Scorer

## Instructions
Evaluate the provided text strictly for observable textual indicators of **Network & Attribution Asymmetry** (Dimensions 15–19) and **Symmetry Counter-Signals**.

### Rules
1. **Extract Before Scoring:** You MUST extract exact verbatim substrings (`evidence_quote`) from the input text *before* assigning any integer score (`0` to `5`). If no verbatim span supports the dimension, the score MUST be `0`.
2. **Diagnostic Neutrality:** Score only structural and rhetorical patterns present in the text. Do not infer hidden geopolitical intent or legal guilt.
3. **Pairwise Mode (Optional):** If both `Text_A` (baseline/ally) and `Text_B` (target/adversary) are supplied, evaluate the divergence in attribution standards, deflection, and jurisdictional framing between the two texts.

## Output Schema (Strict JSON)

```json
{
  "mode": "single | comparative",
  "domain": "string",
  "dominant_profile": ["dimension_name_1", "dimension_name_2", "dimension_name_3"],
  "max_cluster_score": 0.0,
  "composite_score": 0.0,
  "dimensions": [
    {
      "id": 15,
      "name": "Attribution laundering / proxy indirection",
      "evidence_quote": "verbatim substring or null",
      "score": 0,
      "rationale": "concise explanation tied to the quote"
    }
  ],
  "counter_signals": [
    {
      "type": "explicit_provenance | symmetric_criteria | acknowledged_tradeoffs",
      "evidence_quote": "verbatim substring"
    }
  ],
  "confidence_note": "string"
}
```
