# Rubric: `exception_clause`

**Question:** Does this span itself suspend, waive or override an ordinary rule, or invoke
special (emergency, exceptional) conditions to do so?

**Subtypes:** none.

## Yes

- A waiver or exemption granted or applied: "the waiver is granted", "the requirement is
  hereby waived", "was exempted from the rule".
- Emergency or exceptional authority invoked: "invoking its emergency powers", "declared a
  state of emergency", "on an emergency basis", "in exceptional circumstances".
- pt: "fica dispensada a licitação", "contratação por dispensa de licitação", "em caráter
  emergencial", "em caráter excepcional", "excepcionalmente", "decretou situação de
  emergência".

## No

- Disclosure exemptions (FOIA codes, *sigilo*): "exempt from disclosure", "(b)(6)". These
  belong to a separate access marker.
- An exception only mentioned as a topic with no rule being set aside: "the debate about
  emergency powers".
- Negated: "no waiver was granted", "não foi dispensada a licitação".

## `invoked`

- `true`: the text sets the rule aside in this matter ("the waiver is granted").
- `false`: the text only **defines** when it could happen, usually with a modal ("the
  agency may waive", "a licitação poderá ser dispensada"), or the span is inside a direct
  quotation or quoted statute.

The span is the shortest phrase that carries the exception, for example "fica dispensada a
licitação", not the whole sentence.
