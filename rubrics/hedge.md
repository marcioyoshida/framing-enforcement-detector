# Rubric: `hedge`

**Question:** Does this word or phrase signal that the claim it is attached to is unverified,
reported second-hand, or disputed?

This rubric asks about **form**. "Allegedly" is often legally required when reporting an
unproven accusation. A hit is not evidence of bias.

**Subtypes:**

| Subtype | en | pt |
|---|---|---|
| `adverb` | reportedly, allegedly, purportedly, supposedly, ostensibly | supostamente, alegadamente, pretensamente, presumivelmente |
| `label` | so-called, self-styled, self-proclaimed, alleged (before a noun), purported, unverified, unconfirmed | suposto, pretenso, alegado (before a noun), autodenominado, autoproclamado, "o chamado" + quoted term, não confirmado, segundo relatos |
| `report_conditional` | "is said to have", "is reported to have", "is believed to have", "is alleged to have" | the reporting conditional: "teria desviado", "teriam recebido", "estaria negociando" |

## No

- "Supposed to" meaning obligation: "the form was supposed to be filed".
- A true hypothetical: "if it had rained, the event would have been cancelled", "se
  chovesse, teria cancelado".
- "Alleged" as the verb that introduces a statement ("the company alleged that…"): that is
  `attribution_verb`.
- "O chamado" meaning a ticket or call: "o chamado foi aberto".

## `invoked`

- `true`: in the text's own voice.
- `false`: inside a direct quotation (the quoted person's hedge, not the text's).

The span is the hedge itself ("reportedly", "teria desviado"), not the whole claim.
