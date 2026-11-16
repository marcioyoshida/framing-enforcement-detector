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

## Hard cases (from a consumer measurement on court and audit-court text)

Decide these before labelling, write the decision down and apply it to every span.

- **Reported, not said.** A court restating an earlier decision ("in X the Court held the
  order was not subject to review"), a party's argument, a transcribed opinion of another
  body, or statute text paraphrased without quotation marks is `invoked: false`, the same
  as a direct quotation. It is the hardest case for a word list and the most common one.
- **Doctrine.** A general statement of law ("hardship findings are unreviewable",
  "a Administração dispõe de discricionariedade…") is `invoked: false` unless it is tied
  to a decision in this matter.
- **Common-law "case-by-case".** "Courts develop the rule case by case" describes how law
  is made, not a reserved decision: answer `no`.
- **Headings and topic lists.** A bare noun ("Discricionariedade", "Discretion") naming a
  section or an issue is `no`.

