# Rubric: `discretion`

**Question:** Does this span reserve a decision to someone's judgment, or close it to review
or appeal?

**Subtypes:** `reserved`, `review_closed`.

## Yes

- `reserved`: "at the discretion of the Director", "at its sole discretion", "as it deems
  appropriate", "on a case-by-case basis", "exercised its discretion". pt: "a critério da
  autoridade", "a seu exclusivo critério", "juízo de conveniência e oportunidade", "caso a
  caso", "no exercício do poder discricionário".
- `review_closed`: "not subject to review", "final and unreviewable", "non-appealable". pt:
  "decisão irrecorrível", "não cabe recurso".

## No

- A neutral decision with no reservation: "the Director decided to approve".
- "Discretion" meaning confidentiality or tact: "handled with discretion".

## `invoked`

- `true`: the text reserves or closes in this matter ("the decision is at the discretion of
  the Director", "decisão irrecorrível").
- `false`: a modal or general definition ("the agency may, at its discretion, …", "poderá, a
  seu critério"), or inside a direct quotation or quoted statute.
