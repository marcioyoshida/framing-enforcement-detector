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

### Hard case: the stock burden line

Audit courts and agencies repeat a fixed sentence ("cabe ao gestor comprovar a boa e regular
aplicação dos recursos", "the burden is on the applicant") in their own voice, often in
reply to a party's defence or in a headnote, without weighing that party's proof. Decide
before labelling whether it counts as applied in this matter, write the decision down, and
apply it to every such span. A consumer measured the same hits at about 0.84 under the
lenient reading and about 0.55 under the strict one: the rubric reading moved precision
more than any pattern change did.
