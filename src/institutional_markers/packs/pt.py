"""Portuguese (Brazil) pack. Patterns run on folded text: lower case, no accents (à → a,
ç → c, ã → a), ASCII quotes."""
from __future__ import annotations

import re

from .._types import Pattern

LANG = "pt"

#: "no" is not here: in Portuguese it is "em + o".
NEGATORS = frozenset({"nao", "nunca", "jamais", "nem", "nenhum", "nenhuma", "ninguem", "tampouco"})
MODALS = frozenset({
    "pode", "podem", "podera", "poderao", "poderia", "poderiam", "possa", "possam", "podendo",
    "deve", "devem", "devera", "deverao", "deveria", "deveriam", "devendo",
})
#: Drafting verbs that report a general rule ("o regulamento estabelece que …").
DEFINING = frozenset({"estabelece", "estabelecia", "preve", "previa", "dispoe", "dispunha", "prescreve",
                      "preceitua", "determina"})

#: "por/pelo/pela" names an agent unless it is a manner, cause, rate or vote.
_AGENT = re.compile(
    r"(?<!\w)(?:por|pelo|pela|pelos|pelas)\s+(?!(?:volta|causa|meio|cento|dia|ano|mes|semana|hora|vez"
    r"|vezes|isso|isto|tanto|fim|conta|ora|enquanto|unanimidade|menos|primeira|segunda|ultima|unica"
    r"|dias|meses|anos|semanas|horas|minutos|decadas|tempo|muito|pouco|completo"
    r"|motivo|razao|razoes|forca|falta|excesso|engano|equivoco|lei|decreto)\b|\d)")


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
_PROVE = r"(?:comprovar|provar|demonstrar|produzir\s+(?:a\s+)?prova|evidenciar|justificar)"
BURDEN = [
    Pattern("bur-cabe",
            r"(?:cabe|cabia|cabera|caberia|incumbe|incumbia|incumbira|incumbiria|compete|competia|competira)"
            r"\s+(?:a|ao|aos|as|o)\s+(?:\w+\s+){0,3}?" + _PROVE, subtype="burden", modal_defines=True),
    Pattern("bur-onus-cabe",
            r"onus\s+(?:da\s+prova|probatorio|de\s+(?:provar|comprovar|demonstrar)(?:\s+[^.;:,]{0,60}?)?)"
            r"(?:\s*,[^,]{0,60},)?"
            r"\s+(?:\w+\s+)?(?:cabe|cabia|cabera|recai|recaia|recaiu|recaira|incumbe|incumbia|compete|competia"
            r"|pertence|pertencia|e|era|sera|fica|ficava|permanece)\s+(?:a|ao|aos|as|d[oa]s?|sobre|com)(?!\w)",
            subtype="burden", modal_defines=True),
    Pattern("bur-inversao",
            r"(?:defiro|defere|deferiu|deferid[oa]|determino|determinou|determinad[oa]|decreto|decretou|aplico"
            r"|aplicou|aplicad[oa]|reconheco|reconheceu|admito|admitiu|admitid[oa]|operou-se|opera-se|cabivel"
            r"|procede|procedeu-se)\s+(?:a\s+)?inversao\s+do\s+onus(?:\s+da\s+prova|\s+probatorio)?",
            subtype="burden", modal_defines=True),
    Pattern("bur-inverto", r"invert(?:o|eu|eram|id[oa])\s+o\s+onus(?:\s+da\s+prova|\s+probatorio)?",
            subtype="burden", modal_defines=True),
    Pattern("bur-desincumbiu",
            r"(?:se\s+)?desincumb(?:iu|iram|ir|indo|e|em|iria)(?:-se)?\s+(?:a\s+contento\s+)?"
            r"d[oa]\s+(?:seu\s+|sua\s+|respectivo\s+)?(?:onus|encargo)(?:\s+(?:probatorio|da\s+prova|de\s+(?:provar|comprovar)))?",
            subtype="burden", negatable=False, modal_defines=True),
    Pattern("pres-presume", r"presume(?:m)?-se|presumia-se|presumir-se-a|presumir-se|se\s+presumir",
            subtype="presumption", modal_defines=True),
    Pattern("pres-presumido", r"(?:e|sao|foi|foram|era|eram|sera|serao)\s+presumid[oa]s?",
            subtype="presumption", modal_defines=True),
    Pattern("pres-afastou",
            r"(?:afast(?:ou|ar|a|ad[oa])|ilid(?:iu|ir|id[oa])|elid(?:iu|ir|id[oa])|infirm(?:ou|ar|ad[oa])"
            r"|derrub(?:ou|ar|ad[oa])|reconhec(?:eu|ida))\s+(?:a\s+)?presuncao",
            subtype="presumption", negatable=False, modal_defines=True),
    Pattern("pres-restou",
            r"presuncao\s+(?:\w+\s+){0,5}?(?:foi|restou|ficou|resta)\s+(?:\w+mente\s+)?"
            r"(?:afastada|ilidida|elidida|infirmada|derrubada|mantida|confirmada|preservada)",
            subtype="presumption", negatable=False, modal_defines=True),
    Pattern("pres-de",
            r"presuncao\s+(?:relativa\s+|absoluta\s+)?de\s+(?:legitimidade|veracidade|inocencia|boa-fe|legalidade"
            r"|regularidade|certeza|liquidez|culpa|dano)",
            subtype="presumption", modal_defines=True),
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
_AUX = r"(?:foi|foram|tinha\s+sido|tinham\s+sido|havia\s+sido|haviam\s+sido|teria\s+sido|teriam\s+sido)"
_ADV = r"(?:\s+\w+mente)?"
_PASSIVE = dict(agent_check=True, modal_blocks=True)


def _passive(pid: str, subtype: str, participles: str) -> Pattern:
    return Pattern(pid, _AUX + _ADV + r"\s+" + participles, subtype=subtype, **_PASSIVE)


AGENTLESS = [
    _passive("pas-harm", "harm", _pp(
        "mort", "ferid", "balead", "agredid", "atacad", "assassinad", "detid", "pres", "encarcerad",
        "deportad", "despejad", "torturad", "sequestrad", "espancad", "desalojad", "esfaquead",
        "atingid", "alvejad")),
    _passive("pas-sanction", "sanction", _pp(
        "multad", "sancionad", "punid", "suspens", "banid", "bloquead", "advertid", "penalizad",
        "censurad", "condenad", "inabilitad", "declarad[oa]s?\\s+inidone")),
    _passive("pas-removal", "removal", _pp(
        "removid", "excluid", "apagad", "demitid", "exonerad", "afastad", "retirad", "revogad",
        "cancelad", "rejeitad", "indeferid", "destruid", "apreendid", "confiscad", "negad", "derrubad",
        "encerrad", "cassad", "vetad", "expuls", "suprimid", "tarjad")),
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
_HYPOTHETICAL = frozenset({"tivesse", "tivessem", "houvesse", "houvessem", "fosse", "fossem", "caso"})
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
            r"teriam?\s+(?:\w+mente\s+)?(?:sido\s+)?" + _PARTICIPLE,
            subtype="report_conditional", blocked_by=_HYPOTHETICAL, **_HEDGE),
    Pattern("hedge-estaria", r"estariam?\s+(?:\w+mente\s+)?\w+ndo",
            subtype="report_conditional", blocked_by=_HYPOTHETICAL, **_HEDGE),
]

# --- attribution_verb ----------------------------------------------------------------------
_LOOSE = (r"(?=(?:[\s,]+(?!que\b)\w+){0,6}?[\s,]+que\b|(?:\s+\w+){0,8}\s*[,:;.!?]|\s*[\"']"
          r"|(?:\s+\w+){0,8}\s*$)")
_STRICT = r"(?=(?:[\s,]+(?!que\b)\w+){0,6}?[\s,]+que\b|\s*:|\s*[\"'])"
#: Right after a closing quote: '"…", admitiu o diretor' / "'…', sustentou a defesa".
_CLOSE_Q = r"(?:[,.!?]\s*[\"']|[\"']\s*,)\s*(?:\w+\s+){0,3}?"
#: Not after a passive auxiliary ("foi dito", "foi informado").
_NOT_PASSIVE = r"(?<!foi\s)(?<!foram\s)(?<!sido\s)(?<!ser\s)"

_NEUTRAL = _alt("disse", "disseram", "diz", "dizem", "afirmou", "afirmaram", "afirma", "afirmam",
                "declarou", "declararam", "declara", "declaram", "informou", "informaram", "informa",
                "informam", "acrescentou", "acrescentaram", "escreveu", "escreveram", "relatou",
                "relataram", "relata", "relatam")
_DISTANCING = _alt("alegou", "alegaram", "alega", "alegam", "sustentou", "sustentaram", "sustenta",
                   "sustentam", "insistiu", "insistiram", "insiste", "insistem", "argumentou",
                   "argumentaram", "argumenta", "argumentam", "garantiu", "garantiram", "garante",
                   "garantem")
_ENDORSING = _alt("confirmou", "confirmaram", "confirma", "confirmam", "revelou", "revelaram", "revela",
                  "revelam", "reconheceu", "reconheceram", "reconhece", "reconhecem", "admitiu",
                  "admitiram", "admite", "admitem", "explicou", "explicaram", "explica", "explicam",
                  "apontou", "apontaram", "aponta", "apontam", "mostrou", "mostraram", "mostra", "mostram")

ATTRIBUTION = [
    Pattern("attr-neutral", _NOT_PASSIVE + r"(?P<m>" + _NEUTRAL + r")" + _LOOSE, subtype="neutral"),
    Pattern("attr-distancing", _NOT_PASSIVE + r"(?P<m>" + _DISTANCING + r")" + _STRICT,
            subtype="distancing"),
    Pattern("attr-endorsing", _NOT_PASSIVE + r"(?P<m>" + _ENDORSING + r")" + _STRICT,
            subtype="endorsing"),
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
