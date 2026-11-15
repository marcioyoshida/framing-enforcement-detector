# Rubric: `agentless_passive`

**Question:** Is this a **past-tense** passive of an action verb, with **no agent** (no "by …"
/ "por …" phrase naming who did it) in the same clause?

This rubric asks about **form**, not intent. A passive is often plain style. Labelling one
as a hit says nothing about bias.

**Subtypes:** `harm`, `sanction`, `removal`, `error`.

| Subtype | Verbs (en / pt) |
|---|---|
| `harm` | killed, injured, wounded, shot, beaten, attacked, detained, arrested, imprisoned, deported, evicted / morto, ferido, baleado, agredido, atacado, detido, preso, deportado, despejado |
| `sanction` | fined, sanctioned, penalized, punished, disciplined, suspended, banned, barred, blocked / multado, sancionado, punido, suspenso, banido, bloqueado |
| `removal` | removed, deleted, dismissed, fired, withdrawn, revoked, cancelled, terminated, rejected, denied, withheld, destroyed, seized, confiscated / removido, excluído, apagado, demitido, exonerado, afastado, retirado, revogado, cancelado, rejeitado, indeferido, destruído, apreendido |
| `error` | "mistakes/errors were made", overlooked, mishandled / "foram cometidos erros", ignorado |

## Yes

"Two protesters were killed on Tuesday." "The account was suspended." "Mistakes were made."
"Foram mortos dois manifestantes." "O perfil foi suspenso."

## No

- An agent is named in the clause: "were killed by soldiers", "foi suspenso pela
  plataforma".
- Modal or future passives, typical of statutes: "shall be removed", "will be fined",
  "deverá ser apresentado", "será multado".
- Adjectival states: "is located", "está situado", "was interested".
- Negated: "no one was killed", "não foi preso".
- Present habitual: "accounts are removed every day".

## `invoked`

- `true`: in the text's own voice.
- `false`: inside a direct quotation ("'Mistakes were made,' the minister said").

The span runs from the auxiliary to the participle ("were killed", "foi suspenso"), including
one adverb between them if present ("were reportedly killed").
