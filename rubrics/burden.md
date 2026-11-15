# Rubric: `burden`

**Question:** Does this span assign, apply or test a burden of proof, or a presumption, for
a party?

**Subtypes:** `burden`, `presumption`.

## Yes

- `burden`: "the burden rests on the applicant", "the applicant has not met its burden",
  "failed to carry its burden", "the onus is on the claimant". pt: "cabe ao responsável
  comprovar", "incumbe à parte autora provar", "o ônus da prova recai sobre", "defiro a
  inversão do ônus da prova", "não se desincumbiu do ônus".
- `presumption`: "is presumed valid", "the presumption was rebutted". pt: "presume-se",
  "são presumidos legítimos".

A failed or rebutted burden is still a **yes**: the burden was applied. "Has not met its
burden" is a hit, not a negation.

## No

- A party simply asked to provide something with no proof standard: "please submit the
  form".
- "Burden" in another sense: "a tax burden", "the burden on small businesses".
- "Presumably" as a hedge: that is `hedge`, not `burden`.

## `invoked`

- `true`: the text applies it in this matter ("the applicant has not met its burden").
- `false`: a general rule ("the burden of proof shall be on the applicant", "o ônus caberá
  a quem alegar" in a statute), a modal definition, or inside a direct quotation.
