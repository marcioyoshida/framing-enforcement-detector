# Dimension Scoring Prompt Template

Use this template for scoring a single dimension. Replace the placeholders.

---

**System**: (use contents of system_prompt.md)

**User**:

Dimension: {{DIMENSION_NAME}}

Definition: {{DIMENSION_DEFINITION}}

Scoring rubric (0–5):
- 0: No detectable evidence of the pattern.
- 1: Very weak or incidental language that could be read as consistent with the pattern.
- 2: Mild presence; some suggestive phrasing but limited or ambiguous.
- 3: Clear but moderate presence of the pattern in the text.
- 4: Strong and repeated or structurally central presence.
- 5: Dominant framing; the pattern is a primary organizing feature of the text.

{{OPTIONAL_FEW_SHOT_EXAMPLES}}

Text to evaluate:
"""
{{TEXT}}
"""

Instructions:
1. Quote the most relevant short excerpt(s) that support your assessment (or state "no clear evidence").
2. Assign an integer score from 0 to 5.
3. Provide a one-sentence rationale grounded in the quoted evidence.

Respond only with valid JSON in this format:
{
  "dimension": "{{DIMENSION_NAME}}",
  "evidence": ["excerpt 1", "excerpt 2"],
  "score": 0,
  "rationale": "..."
}
