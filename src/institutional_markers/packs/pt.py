"""Portuguese (Brazil) pack. Patterns run on folded text: lower case, no accents (à → a,
ç → c, ã → a), ASCII quotes."""
from __future__ import annotations

import re

from .._types import Pattern

LANG = "pt"

#: "no" is not here: in Portuguese it is "em + o".
NEGATORS = frozenset({"nao", "nunca", "jamais", "nem", "nenhum", "nenhuma", "ninguem", "tampouco"})
NEGATORS_COMPARISON = NEGATORS
MODALS = frozenset({
    "pode", "podem", "podera", "poderao", "poderia", "poderiam", "possa", "possam", "podendo",
    "deve", "devem", "devera", "deverao", "deveria", "deveriam", "devendo",
})
#: Drafting verbs that report a general rule ("o regulamento estabelece que …").
DEFINING = frozenset({"estabelece", "estabelecia", "preve", "previa", "dispoe", "dispunha", "prescreve",
                      "preceitua", "determina"})

#: "por/pelo/pela" names an agent unless it is a manner, cause, rate or vote.
#: agentless-v3: "por lei / por decreto" (no article) is a manner, but "pela Lei 12.651"
#: names the law that did it, so lei/decreto are excluded only after a bare "por".
_AGENT = re.compile(
    r"(?<!\w)(?:(?:pelo|pela|pelos|pelas)\s+|por\s+(?!(?:lei|decreto)\b))"
    r"(?!(?:volta|causa|meio|cento|dia|ano|mes|semana|hora|vez"
    r"|vezes|isso|isto|tanto|fim|conta|ora|enquanto|unanimidade|menos"
    r"|(?:primeira|segunda|terceira|ultima|unica)\s+vez"
    r"|dias|meses|anos|semanas|horas|minutos|decadas|tempo|muito|pouco|completo"
    r"|motivo|razao|razoes|forca|falta|excesso|engano|equivoco"
    # agentless-v2: a duration or an amount is not an agent ("pelo prazo de um ano",
    # "por três anos", "pelo valor de").
    r"|prazo|periodo|valor|montante|total|mais|um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito"
    r"|nove|dez|doze|quinze|vinte|trinta|cem|mil)\b|\d)")


#: Comparison markers (v3): an emphasis note closing a transcribed passage ("(grifos
#: nossos)", "(grifo do peticionante)", "(o grifo não consta do original)").
EMPHASIS_NOTE = re.compile(r"\((?:o\s+|os\s+)?(?:grifos?|destaques?|negritos?|sublinhados?)\b[^)]{0,60}\)")


def has_agent(after: str) -> bool:
    return _AGENT.search(after) is not None


def _alt(*words: str) -> str:
    return "(?:" + "|".join(words) + ")"


def _pp(*stems: str) -> str:
    """Participles agreeing in gender and number: stem + o/a/os/as."""
    return "(?:" + "|".join(s + "[oa]s?" for s in stems) + ")"


# --- exception_clause -------------------------------------------------------------------
_EXC = dict(modal_defines=True)
_RULE = _alt(r"licitac(?:ao|oes)", "exigencias?", "requisitos?", "prazos?", "procedimentos?",
             r"obrigac(?:ao|oes)", "regras?", r"aplicac(?:ao|oes)", r"realizac(?:ao|oes)", "vistorias?",
             "consultas?", "audiencias?", r"autorizac(?:ao|oes)", r"apresentac(?:ao|oes)")
EXCEPTION = [
    Pattern("exc-dispensada",
            r"(?:fica|ficam|ficou|ficaram|foi|foram|e|sao|esta|estao)\s+(?:\w+mente\s+)?"
            r"(?:dispensad[oa]s?|inexigive(?:l|is)|afastad[oa]s?)(?:\s*,\s*\w+(?:\s+\w+)?\s*,)?\s+(?:a|o|as|os)\s+"
            + _RULE, **_EXC),
    Pattern("exc-isento",
            r"(?:fica|ficam|ficou|ficaram|foi|foram|esta|estao|e|sao)\s+(?:\w+mente\s+)?isent[oa]s?\s+d[aoe]s?",
            **_EXC),
    # "é dispensável a licitação" = MAY be dispensed with: wording that only defines.
    Pattern("exc-dispensavel",
            r"(?:e|sao|sera|serao|era|eram)\s+(?:dispensave(?:l|is)|inexigive(?:l|is))\s+(?:a|o|as|os)\s+" + _RULE,
            always_defined=True, **_EXC),
    Pattern("exc-pode-ser-dispensada",
            r"(?:pode|podera|poderao|podem|poderia|poderiam)\s+ser\s+(?:dispensad|afastad|suspens)[oa]s?", **_EXC),
    Pattern("exc-dispensada-sv",
            _RULE + r"\s+(?:foi|foram|fica|ficam|ficou|ficaram|e|sao)\s+(?:\w+mente\s+)?"
            r"(?:dispensad[oa]s?|afastad[oa]s?|suspens[oa]s?)", **_EXC),
    Pattern("exc-por-dispensa",
            r"(?:por|com|mediante|via|sob)\s+(?:a\s+)?(?:dispensa|inexigibilidade)\s+(?:de\s+)?licitacao", **_EXC),
    Pattern("exc-carater",
            r"em\s+carater\s+(?:emergencial|excepcional|extraordinario|de\s+urgencia|de\s+emergencia)", **_EXC),
    Pattern("exc-excepcionalmente", r"excepcionalmente", **_EXC),
    Pattern("exc-decreta",
            r"(?:decretou|decreta|decretad[oa]|decretaram|reconheceu|reconhecid[oa]|declarou|declarad[oa]"
            r"|declara|instituiu|homologou|homologad[oa])\s+(?:a\s+|o\s+)?(?:situacao\s+de\s+(?:emergencia"
            r"|calamidade)|estado\s+de\s+(?:emergencia|calamidade|sitio|defesa)|calamidade\s+publica)", **_EXC),
    Pattern("exc-situacao",
            r"(?:em|diante\s+da|dada\s+a|ante\s+a|devido\s+a|em\s+razao\s+da)\s+(?:situacao|hipotese)\s+"
            r"(?:de\s+)?(?:emergencia|emergencial|urgencia|calamidade)", **_EXC),
    Pattern("exc-concedida",
            r"(?:foi|foram)\s+(?:\w+mente\s+)?(?:concedid|admitid|aberta|feita)[oa]?s?\s+(?:a\s+|uma\s+)?"
            r"(?:dispensa|isencao|excecao|derrogacao)", **_EXC),
    Pattern("exc-concedeu",
            r"(?:concedeu|concederam|conced[ei]|abriu|abriram|abre)(?:-se)?\s+(?:a\s+|uma\s+)?"
            r"(?:dispensa|isencao|excecao|derrogacao)", **_EXC),
    # "dispensou a licitação" (invoked) / "poderá dispensar a licitação" (defined, by the modal)
    Pattern("exc-dispensar",
            r"(?:dispensar|dispensou|dispensaram|dispensa|dispensam|dispensando|afastar|afastou|afastaram"
            r"|suspender|suspendeu|suspenderam)(?:-se)?\s+(?:a|o|as|os)\s+" + _RULE, **_EXC),
]

# --- burden ------------------------------------------------------------------------------
# burden-v2 (2026-11-15): v1 measured 0.39 on a consumer's real corpora (n=77). Bare
# "presunção de legitimidade/boa-fé…" (1 of 20, almost always a party's defence or a
# heading), "presume-se" and "é presumido" are gone: a presumption only as an ACT on it
# (afastada, ilidida). Nothing inside a party's reported argument ("alega que cabe …").
_PROVE = r"(?:comprovar|provar|demonstrar|produzir\s+(?:a\s+)?prova|evidenciar|justificar)"
_ARGUED = frozenset({"alega", "alegou", "alegam", "alegaram", "sustenta", "sustentou", "sustentam",
                     "argumenta", "argumentou", "argumentam", "defende", "defendeu", "aduz", "aduziu",
                     "aduzem", "requer", "requereu", "pleiteia", "pleiteou", "insiste", "insistiu",
                     "afirma", "afirmou", "assevera", "asseverou", "pondera", "ponderou"})
# burden-v3 (2026-11-15): v2 measured pt 0.79 (23 of 29) on a consumer's audit-court corpus.
# The misses were a rule REPORTED, not stated by the author: a quoted precedent ("Enunciado
# do Acórdão …: cabe ao ordenador provar …"), the case law cited "no sentido de que …", and a
# party's view the court rejects ("Equivoca-se a responsável ao entender que cabe …").
_REPORTED = frozenset({"enunciado", "sumula", "verbete", "sentido", "entende", "entendeu", "entender",
                       "entendem", "entenderam"})
_BUR = dict(subtype="burden", modal_defines=True, blocked_by=_ARGUED | _REPORTED)
_PRES = dict(subtype="presumption", negatable=False, modal_defines=True, blocked_by=_ARGUED | _REPORTED)
BURDEN = [
    Pattern("bur-cabe",
            r"(?:cabe|cabia|cabera|caberia|incumbe|incumbia|incumbira|incumbiria|compete|competia|competira)"
            r"\s+(?:a|ao|aos|as|o)\s+(?:\w+\s+){0,3}?" + _PROVE, **_BUR),
    Pattern("bur-onus-cabe",
            r"onus\s+(?:da\s+prova|probatorio|de\s+(?:provar|comprovar|demonstrar)(?:\s+[^.;:,]{0,60}?)?)"
            r"(?:\s*,[^,]{0,60},)?"
            r"\s+(?:\w+\s+)?(?:cabe|cabia|cabera|recai|recaia|recaiu|recaira|incumbe|incumbia|compete|competia"
            r"|pertence|pertencia|e|era|sera|fica|ficava|permanece)\s+(?:a|ao|aos|as|d[oa]s?|sobre|com)(?!\w)",
            **_BUR),
    Pattern("bur-inversao",
            r"(?:defiro|defere|deferiu|deferid[oa]|determino|determinou|determinad[oa]|decreto|decretou|aplico"
            r"|aplicou|aplicad[oa]|reconheco|reconheceu|admito|admitiu|admitid[oa]|operou-se|opera-se"
            r"|procedeu-se)\s+(?:a\s+)?inversao\s+do\s+onus(?:\s+da\s+prova|\s+probatorio)?", **_BUR),
    Pattern("bur-inverto", r"invert(?:o|eu|eram)\s+o\s+onus(?:\s+da\s+prova|\s+probatorio)?", **_BUR),
    Pattern("bur-desincumbiu",
            r"(?:se\s+)?desincumb(?:iu|iram|ir|indo|e|em|iria)(?:-se)?\s+(?:a\s+contento\s+)?"
            r"d[oa]\s+(?:seu\s+|sua\s+|respectivo\s+)?(?:onus|encargo)(?:\s+(?:probatorio|da\s+prova|de\s+(?:provar|comprovar)))?",
            subtype="burden", negatable=False, modal_defines=True, blocked_by=_ARGUED | _REPORTED),
    Pattern("pres-afastou",
            r"(?:afast(?:ou|aram|ad[oa])|ilid(?:iu|iram|id[oa])|elid(?:iu|iram|id[oa])|infirm(?:ou|aram|ad[oa])"
            r"|derrub(?:ou|aram|ad[oa]))\s+(?:a\s+)?presuncao", **_PRES),
    Pattern("pres-restou",
            r"presuncao\s+(?:\w+\s+){0,5}?(?:foi|restou|ficou|resta)\s+(?:\w+mente\s+)?"
            r"(?:afastada|ilidida|elidida|infirmada|derrubada)", **_PRES),
]

# --- discretion --------------------------------------------------------------------------
DISCRETION = [
    Pattern("disc-seu-criterio",
            r"a\s+(?:seu|sua)\s+(?:exclusivo\s+|livre\s+|inteiro\s+|unico\s+|prudente\s+)?criterio",
            subtype="reserved", modal_defines=True),
    Pattern("disc-criterio-de",
            r"a\s+criterio\s+(?:exclusivo\s+|discricionario\s+)?d(?:a|o|as|os|e)(?!\w)",
            subtype="reserved", modal_defines=True),
    Pattern("disc-conveniencia",
            r"(?:(?:juizo|criterios?|analise|avaliacao)\s+de\s+)?conveniencia\s+e\s+oportunidade",
            subtype="reserved", modal_defines=True),
    Pattern("disc-caso-a-caso", r"caso\s+a\s+caso", subtype="reserved", modal_defines=True),
    Pattern("disc-juizo-de",
            r"a\s+juizo\s+(?:exclusivo\s+|discricionario\s+|livre\s+)?d(?:a|o|as|os|e)(?!\w)",
            subtype="reserved", modal_defines=True),
    Pattern("disc-judiciario",
            r"nao\s+(?:cabe|cabia|compete|competia)\s+(?:a|ao)\s+(?:poder\s+)?judiciario\s+"
            r"(?:rever|revisar|reexaminar|substituir|adentrar|controlar|sindicar)",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-exercicio",
            r"(?:no\s+)?exercicio\s+d[eoa]\s+(?:seu\s+|sua\s+)?(?:poder\s+discricionario|discricionariedade"
            r"|competencia\s+discricionaria)", subtype="reserved", modal_defines=True),
    Pattern("disc-discricionario",
            r"(?:poder|ato|decisao|competencia|escolha|juizo)\s+discricionari[oa]",
            subtype="reserved", modal_defines=True),
    Pattern("disc-discricionariedade", r"discricionariedade", subtype="reserved", modal_defines=True),
    Pattern("disc-como-entender",
            r"(?:como|quando|se|conforme)\s+(?:melhor\s+)?(?:entender|entendeu|julgar|julgou|considerar"
            r"|considerou|reputar|reputou)\s+"
            r"(?:cabivel|conveniente|adequado|necessario|oportuno|pertinente)",
            subtype="reserved", modal_defines=True),
    Pattern("disc-irrecorrivel", r"irrecorrive(?:l|is)", subtype="review_closed", modal_defines=True),
    Pattern("disc-nao-cabe-recurso",
            r"(?:nao\s+(?:cabe|cabendo|cabera|caber|comporta|comportando|admite)|descabe|descabid[oa]|incabivel"
            r"|inadmissivel)\s+(?:qualquer\s+)?recursos?",
            subtype="review_closed", modal_defines=True),
    Pattern("disc-insuscetivel",
            r"insuscetive(?:l|is)\s+de\s+(?:recurso|revisao|reexame|impugnacao|controle\s+judicial)",
            subtype="review_closed", modal_defines=True),
]

# --- agentless_passive -------------------------------------------------------------------
#: agentless-v3: "teria sido" left out; a conditional passive is excluded by the rubric (and
#: is a reporting conditional, which `hedge` reads).
_AUX = r"(?:foi|foram|tinha\s+sido|tinham\s+sido|havia\s+sido|haviam\s+sido)"
_ADV = r"(?:\s+\w+mente)?"
_PASSIVE = dict(agent_check=True, modal_blocks=True)


def _passive(pid: str, subtype: str, participles: str) -> Pattern:
    return Pattern(pid, _AUX + _ADV + r"\s+" + participles, subtype=subtype, **_PASSIVE)


AGENTLESS = [
    _passive("pas-harm", "harm", _pp(
        "mort", "ferid", "balead", "agredid", "atacad", "assassinad", "detid", "pres", "encarcerad",
        "deportad", "despejad", "torturad", "sequestrad", "espancad", "desalojad", "esfaquead",
        # agentless-v2: "atingid" dropped; in official text it means "reached" ("a meta foi
        # atingida") far more often than "hit".
        "alvejad")),
    _passive("pas-sanction", "sanction", _pp(
        "multad", "sancionad", "punid", "suspens", "banid", "bloquead", "advertid", "penalizad",
        "censurad", "condenad", "declarad[oa]s?\\s+inidone",
        # agentless-v3: "inabilitado para o exercício de cargo" is a sanction; a bidder
        # "inabilitada" in a procurement is removed from it (below).
        r"inabilitad(?=[oa]s?\s+para\s+(?:o\s+)?(?:exercicio|exercer|cargo|funcao))")),
    _passive("pas-removal", "removal", _pp(
        "removid", "excluid", "apagad", "demitid", "exonerad", "afastad", "retirad", "revogad",
        "cancelad", "rejeitad", "indeferid", "destruid", "apreendid", "confiscad", "negad", "derrubad",
        "encerrad", "cassad", "vetad", "expuls", "suprimid", "tarjad", "inabilitad")),
    _passive("pas-error", "error", _pp(
        "ignorad", "negligenciad", "perdid", "extraviad", "desconsiderad", "omitid")),
    Pattern("pas-cometidos",
            _AUX + _ADV + r"\s+cometid[oa]s?\s+(?:\w+\s+)?(?:erros?|falhas?|equivocos?|irregularidades?|excessos?)",
            subtype="error", **_PASSIVE),
    Pattern("pas-erros-cometidos",
            r"(?:erros?|falhas?|equivocos?|excessos?)\s+(?:foi|foram|tinham\s+sido|haviam\s+sido)" + _ADV
            + r"\s+cometid[oa]s?", subtype="error", **_PASSIVE),
]

# --- hedge -------------------------------------------------------------------------------
_HEDGE = dict(negatable=False)
#: A true hypothetical ("se tivesse chovido, teria cancelado") is not a reporting conditional.
#: hedge-v2: "caso" left out; across a wrapped line it is mostly "no caso" ("in this case"),
#: and a conditional "caso" carries one of these subjunctives anyway.
_HYPOTHETICAL = frozenset({"tivesse", "tivessem", "houvesse", "houvessem", "fosse", "fossem",
                           "estivesse", "estivessem"})
#: hedge-v2: the condition can also follow ("teria sido escolhida, caso … estivesse").
_HYPOTHETICAL_AFTER = _HYPOTHETICAL
#: hedge-v3: an indirect question ("cabe saber se a falha teria prejudicado …").
_INDIRECT_Q = frozenset({"saber", "indagar", "perguntar", "questionar", "averiguar"})
_PARTICIPLE = r"\w+(?:ad[oa]s?|id[oa]s?|it[oa]s?|ost[oa]s?|ert[oa]s?|ist[oa]s?|eit[oa]s?)"
_DET = _alt("o", "a", "os", "as", "um", "uma", "uns", "umas", "do", "da", "dos", "das", "no", "na",
            "nos", "nas", "pelo", "pela", "pelos", "pelas", "ao", "aos", "e", "de", "seu", "sua", "seus",
            "suas", "esse", "essa", "este", "esta", "sobre", "contra", "com")
HEDGE = [
    Pattern("hedge-adverb", _alt("supostamente", "alegadamente", "pretensamente", "presumivelmente"),
            subtype="adverb", **_HEDGE),
    Pattern("hedge-suposto", r"(?:supost|pretens)[oa]s?(?=\s+\w)", subtype="label", **_HEDGE),
    Pattern("hedge-alegado", _DET + r"\s+(?P<m>alegad[oa]s?)(?=\s+(?!que\b|pel[oa]s?\b|por\b)\w)",
            subtype="label", **_HEDGE),
    Pattern("hedge-autodenominado",
            r"auto-?(?:denominad|proclamad|intitulad|declarad)[oa]s?", subtype="label", **_HEDGE),
    Pattern("hedge-o-chamado", r"(?:o|a|os|as)\s+chamad[oa]s?(?=\s*[\"'])", subtype="label", **_HEDGE),
    Pattern("hedge-nao-confirmado", r"nao\s+(?:confirmad|verificad)[oa]s?", subtype="label", **_HEDGE),
    Pattern("hedge-segundo-relatos", r"(?:segundo|conforme|de\s+acordo\s+com)\s+(?:relatos|rumores)",
            subtype="label", **_HEDGE),
    Pattern("hedge-teria",
            # hedge-v3: "se … teria sido, ou não, …" is an indirect question.
            r"teriam?\s+(?:\w+mente\s+)?(?:sido\s+)?" + _PARTICIPLE + r"(?!\s*,?\s*ou\s+nao\b)",
            subtype="report_conditional", blocked_by=_HYPOTHETICAL | _INDIRECT_Q,
            blocked_after=_HYPOTHETICAL_AFTER, **_HEDGE),
    Pattern("hedge-estaria", r"estariam?\s+(?:\w+mente\s+)?\w+ndo",
            subtype="report_conditional", blocked_by=_HYPOTHETICAL, blocked_after=_HYPOTHETICAL_AFTER,
            **_HEDGE),
]

# --- attribution_verb ----------------------------------------------------------------------
_LOOSE = (r"(?=(?:[\s,]+(?!que\b)\w+){0,6}?[\s,]+que\b|(?:\s+\w+){0,8}\s*[,:;.!?]|\s*[\"']"
          r"|(?:\s+\w+){0,8}\s*$)")
_STRICT = r"(?=(?:[\s,]+(?!que\b)\w+){0,6}?[\s,]+que\b|\s*:|\s*[\"'])"
#: Right after a closing quote: '"…", admitiu o diretor' / "'…', sustentou a defesa".
_CLOSE_Q = r"(?:[,.!?]\s*[\"']|[\"']\s*,)\s*(?:\w+\s+){0,3}?"
#: Not after a passive auxiliary ("foi dito", "foi informado").
#: attribution-v3: word boundaries on every guard.
_NOT_PASSIVE = r"(?<!\bfoi\s)(?<!\bforam\s)(?<!\bsido\s)(?<!\bser\s)"

_NEUTRAL = _alt("disse", "disseram", "diz", "dizem", "afirmou", "afirmaram", "afirma", "afirmam",
                "declarou", "declararam", "declara", "declaram", "informou", "informaram", "informa",
                "informam", "acrescentou", "acrescentaram", "escreveu", "escreveram", "relatou",
                "relataram", "relata", "relatam")
_DISTANCING = _alt("alegou", "alegaram", "alega", "alegam", "sustentou", "sustentaram", "sustenta",
                   "sustentam", "insistiu", "insistiram", "insiste", "insistem", "argumentou",
                   "argumentaram", "argumenta", "argumentam", "garantiu", "garantiram", "garante",
                   "garantem")
#: attribution-v3: a text, evidence or a practice as the subject is not a speaker ("vários
#: documentos, contrariamente, mostram", "esta prática … revela", "o dispositivo diz").
#: Checked over the clause before the verb.
_TEXT_SUBJECT_PT = frozenset({
    "lei", "norma", "normas", "dispositivo", "artigo", "texto", "regulamento", "resolucao",
    "documentos", "documento", "elementos", "elemento", "dados", "provas", "prova", "autos", "fatos",
    "pratica", "praticas", "analise", "conduta", "registros", "evidencias", "indicios", "historico",
    "tabela", "quadro", "manutencao"})
_ENDORSING = _alt("confirmou", "confirmaram", "confirma", "confirmam", "revelou", "revelaram", "revela",
                  "revelam", "reconheceu", "reconheceram", "reconhece", "reconhecem", "admitiu",
                  "admitiram", "admite", "admitem", "explicou", "explicaram", "explica", "explicam",
                  "apontou", "apontaram", "aponta", "apontam", "mostrou", "mostraram", "mostra", "mostram")

ATTRIBUTION = [
    # attribution-v2: "no que diz respeito" ("regarding") is not speech.
    Pattern("attr-neutral", _NOT_PASSIVE + r"(?P<m>" + _NEUTRAL + r")(?!\s+respeito\b)" + _LOOSE,
            subtype="neutral"),
    Pattern("attr-distancing", _NOT_PASSIVE + r"(?P<m>" + _DISTANCING + r")" + _STRICT,
            subtype="distancing"),
    # attribution-v2: a reflexive "se mostra / mostrou-se" means "proves to be", not speech.
    # attribution-v3: "aponta para a …" means "points to" (evidence), not speech.
    Pattern("attr-endorsing", _NOT_PASSIVE + r"(?<!\bse\s)(?<!\bse\s\s)(?P<m>" + _ENDORSING + r")(?!-se\b)"
            + r"(?!\s+para\s+(?:a|o|as|os)\b)" + _STRICT,
            subtype="endorsing", blocked_by=_TEXT_SUBJECT_PT),
    Pattern("attr-distancing-inv", _CLOSE_Q + r"(?P<m>" + _DISTANCING + r")",
            subtype="distancing", lead_boundary=False),
    Pattern("attr-endorsing-inv", _CLOSE_Q + r"(?P<m>" + _ENDORSING + r")",
            subtype="endorsing", lead_boundary=False),
    # "…, alegou o sindicato." (sem aspas): só distanciamento; "…, reconheceu a prescrição"
    # é um ato, não uma fala.
    Pattern("attr-distancing-comma",
            r",\s*(?P<m>" + _DISTANCING + r")\s+(?:o|a|os|as)\s+\w+(?:\s+\w+){0,4}\s*(?:[.;!?]|$)",
            subtype="distancing", lead_boundary=False),
]

PATTERNS: dict[str, list[Pattern]] = {
    "exception_clause": EXCEPTION,
    "burden": BURDEN,
    "discretion": DISCRETION,
    "agentless_passive": AGENTLESS,
    "hedge": HEDGE,
    "attribution_verb": ATTRIBUTION,
}
