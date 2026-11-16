# Rubric: `attribution_verb`

**Question:** Is this a verb that introduces what someone said or wrote, and is its subtype
right?

This rubric asks about **form**. The subtype describes how the verb frames the statement,
not whether the statement is true.

**Subtypes:**

| Subtype | Frames the statement as… | en | pt |
|---|---|---|---|
| `neutral` | said | said, says, stated, told, added, wrote, declared | disse, diz, afirmou, afirma, declarou, informou, acrescentou, escreveu |
| `distancing` | contested or merely asserted | claimed, alleged, insisted, maintained, contended, asserted | alegou, alega, sustentou, insistiu, argumentou, garantiu |
| `endorsing` | established or conceded | confirmed, revealed, acknowledged, admitted, explained, pointed out, showed | confirmou, revelou, reconheceu, admitiu, explicou, apontou, mostrou |

## Yes

"The ministry said that…", "the company claimed, without evidence, that…", "'We will
appeal,' the lawyer said." "O ministério afirmou que…", "a empresa alegou que…".

## No

- The verb is not introducing a statement: "the report showed a decline" is about data,
  not speech. Label it **no** unless a person or body is the speaker.
- A text itself as the subject is not a speaker: "the statute tells us", "the phrase tells
  employers", "a comparison with other statutes shows", "o dispositivo diz", "vários
  documentos mostram", "esta prática revela". Label it **no**. A person or body speaking
  through a document it wrote still counts ("the complaint alleges", "o relator afirmou").
- Fixed phrases and manner: "all told", "stated simply", "something to be said for",
  "unless otherwise stated", "no que diz respeito", "aponta para a …": **no**.
- "Alleged" as an adjective before a noun ("the alleged victim"): that is `hedge`.
- Negated: "the ministry did not say", "o ministério não confirmou".

## `invoked`

- `true`: the text itself attributes the statement.
- `false`: inside a direct quotation (a speaker quoting someone else).

The span is the verb alone ("claimed", "alegou").
