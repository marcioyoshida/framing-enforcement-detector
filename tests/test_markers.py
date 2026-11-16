"""Per-marker cases, en and pt. Each case lists EVERY hit of that marker in the text
(include_defined=True), as (quote, subtype, invoked). Invented text only: the repo is public.

These are the tuner's own development cases. The blind held-out set is eval/heldout.jsonl,
labelled from the rubrics by someone who never saw the patterns.
"""
import pytest

from institutional_markers import scan

N = None  # no subtype

CASES = [
    # --- v0.5.0 comparison fixes (agentless-v3, hedge-v3, attribution-v3) -------------
    # "claims" as a plural noun is not speech; as a verb before "that" it still is.
    ("en", "The case includes other claims that purportedly have nothing to do with it.",
     "attribution_verb", []),
    ("en", "The Court applied rational-basis review to sex-discrimination claims until 1970.",
     "attribution_verb", []),
    ("en", "These claims that were dismissed are not before us.", "attribution_verb", []),
    ("en", "The company claims that the data was lost.", "attribution_verb",
     [("claims", "distancing", True)]),
    ("en", '"The deal is fair," the company claims.', "attribution_verb",
     [("claims", "distancing", True)]),
    # Guards need a word boundary: "is" inside "Chris" or "Davis" does not block "said".
    ("en", "Chris said that the vote was close.", "attribution_verb", [("said", "neutral", True)]),
    ("en", "Davis said the plan was dead.", "attribution_verb", [("said", "neutral", True)]),
    # "says nothing / little" introduces no statement.
    ("en", "The text of Rule 23 says nothing about provisional classes.", "attribution_verb", []),
    # "aponta para a …" is evidence pointing, not speech.
    ("pt", "A sentença aponta para a inexistência da irregularidade.", "attribution_verb", []),
    ("pt", "A unidade técnica aponta que houve sobrepreço.", "attribution_verb",
     [("aponta", "endorsing", True)]),
    # A conditional passive is not a passive event (the hedge reads it).
    ("pt", "O processo teria sido encerrado por meio de sentença.", "agentless_passive", []),
    # "pela Lei 12.651" names an agent; "por lei" is a manner.
    ("pt", "A referida lei foi revogada pela Lei 12.651, de 2012.", "agentless_passive", []),
    ("pt", "O benefício foi suspenso por lei.", "agentless_passive",
     [("foi suspenso", "sanction", True)]),
    # "inabilitada" in a procurement is a removal; "inabilitado para o exercício" a sanction.
    ("pt", "Das duas empresas, uma foi inabilitada no certame.", "agentless_passive",
     [("foi inabilitada", "removal", True)]),
    ("pt", "O gestor foi inabilitado para o exercício de cargo em comissão.", "agentless_passive",
     [("foi inabilitado", "sanction", True)]),
    # An indirect question is not a reporting conditional.
    ("pt", "Não souberam dizer se cada item teria sido, ou não, objeto do contrato.", "hedge", []),
    # An emphasis note closes a transcribed passage that has no quotation marks.
    ("pt", "132. A defesa alega, nos seguintes termos: a suposta dívida foi paga em dia. "
     "(grifos nossos)\n\n133. Não há prova da suposta entrega.", "hedge",
     [("suposta", "label", False), ("suposta", "label", True)]),
    ("en", "The panel wrote: the allegedly unlawful order stood (emphasis added). "
     "We disagree.", "hedge", [("allegedly", "adverb", False)]),
    # No colon before the note: the author's own words before the quotation stay invoked.
    ("en", 'The allegedly abusive father, Jones told the doctor, was "not abusive." '
     "Id. (emphasis added).", "hedge", [("allegedly", "adverb", True)]),
    # A single quote before "(..)" opens a quotation.
    ("pt", "Informa a responsável: '(..) os materiais da suposta dívida foram entregues.' Fim.",
     "hedge", [("suposta", "label", False)]),
    # attribution-v3, second round (fresh-sample errors).
    ("en", "Nowhere did the statute say that the agency must act.", "attribution_verb", []),
    ("en", "The rule adds the option of a hearing.", "attribution_verb", []),
    ("en", "The officer added that the car was stolen.", "attribution_verb",
     [("added", "neutral", True)]),
    ("en", "All told, the program cost billions.", "attribution_verb", []),
    ("en", "Stated simply, the claim fails.", "attribution_verb", []),
    ("en", "The statutory scheme confirms that Congress meant it.", "attribution_verb", []),
    ("en", "The agency confirms that the data was lost.", "attribution_verb",
     [("confirms", "endorsing", True)]),
    ("pt", "Vários documentos mostram que o pagamento foi feito.", "attribution_verb", []),
    ("pt", "Esta prática revela que o controle falhou.", "attribution_verb", []),
    ("pt", "O auditor revela que o controle falhou.", "attribution_verb",
     [("revela", "endorsing", True)]),
    ("en", "A comparison with other statutes shows that the word is temporal.", "attribution_verb", []),
    ("en", "The Supremacy Clause tells us that state law must yield.", "attribution_verb", []),
    ("pt", "Vários documentos, contrariamente, mostram que eles residiram juntos.", "attribution_verb", []),
    # hedge-v3: "presumably" is the author's own inference; an indirect question is not a report.
    ("en", "The panel presumably read the record.", "hedge", []),
    ("pt", "Cabe saber se a falha teria prejudicado a concorrência.", "hedge", []),
    # --- v0.4.0 comparison fixes (agentless-v2, hedge-v2, attribution-v2) -------------
    # A PDF line wrap no longer ends the clause: the agent, the negator and the
    # hypothetical are seen across it.
    ("pt", "Tal circunstância foi\ntotalmente ignorada pela segunda auditoria.", "agentless_passive", []),
    ("pt", "Os itens não\nforam removidos do contrato.", "agentless_passive", []),
    ("en", "The account was\nsuspended by the platform.", "agentless_passive", []),
    ("en", "The account was\nsuspended on Friday.", "agentless_passive",
     [("was\nsuspended", "sanction", True)]),
    # "pela segunda vez" is still not an agent; "pela segunda auditoria" is.
    ("pt", "O perfil foi suspenso pela segunda vez.", "agentless_passive",
     [("foi suspenso", "sanction", True)]),
    # A duration or an amount is not an agent.
    ("pt", "A empresa foi declarada inidônea\npelo prazo de um ano.", "agentless_passive",
     [("foi declarada inidônea", "sanction", True)]),
    ("pt", "A empresa foi declarada inidônea por três anos.", "agentless_passive",
     [("foi declarada inidônea", "sanction", True)]),
    # "atingido" means "reached" in official text: no longer a harm verb.
    ("pt", "A finalidade da contratação foi atingida.", "agentless_passive", []),
    # Present perfect after a future or a time/condition word is not a reported event.
    ("en", "I will confirm that the information has been destroyed.", "agentless_passive", []),
    ("en", "The bracelet is useless after it has been removed.", "agentless_passive", []),
    ("en", "The post has been removed.", "agentless_passive",
     [("has been removed", "removal", True)]),
    # pt counterfactuals: the condition before (across a wrap) or after the span.
    ("pt", "Se o despacho não tivesse sido assinado pelo titular (em férias,\ndoença), certamente "
     "teria sido assinado por outra pessoa.", "hedge", []),
    ("pt", "A proposta teria sido escolhida, caso a obra estivesse prevista no edital.", "hedge", []),
    # "no caso" is not a hypothetical any more.
    ("pt", "No caso sob análise, os recursos teriam sido desviados.", "hedge",
     [("teriam sido desviados", "report_conditional", True)]),
    # attribution: fixed phrases and adjectives that are not speech.
    ("pt", "No que diz respeito ao presente caso, nada há a acrescentar.", "attribution_verb", []),
    ("pt", "Os apontamentos se mostram consistentes: a cautelar se justifica.", "attribution_verb", []),
    ("pt", "Os apontamentos se\n mostram consistentes: a cautelar se justifica.", "attribution_verb", []),
    ("pt", "A unidade técnica mostrou que o preço estava acima do mercado.", "attribution_verb",
     [("mostrou", "endorsing", True)]),
    ("en", "The Court sat at Boston, within and for said County, on the first day.", "attribution_verb", []),
    ("en", "The office is not bound unless otherwise stated.", "attribution_verb", []),
    ("en", "There is something to be said for waiting.", "attribution_verb", []),
    ("en", "The Complaint nowhere alleges that he knew.", "attribution_verb", []),
    ("en", "There is nothing he could say to rebut it.", "attribution_verb", []),
    ("en", "The lawyer said that the client would appeal.", "attribution_verb",
     [("said", "neutral", True)]),
    # Double quotes are paired by direction: one stray mark does not flip later pairs.
    ("en", 'He wrote 12" of notes. The filing says "the bank claimed that it knew nothing" in 2019.',
     "attribution_verb", [("says", "neutral", True), ("claimed", "distancing", False)]),
    # An elided start opens a single-quoted quotation.
    ("pt", "A concessionária cita a deliberação ('... a revogada cautelar e o suposto sobrepreço ...').",
     "hedge", [("suposto", "label", False)]),
    # --- exception_clause, en ---------------------------------------------------------
    ("en", "The waiver is granted for the 2026 cycle.", "exception_clause",
     [("waiver is granted", N, True)]),
    ("en", "The requirement is hereby waived.", "exception_clause",
     [("is hereby waived", N, True)]),
    ("en", "Invoking its emergency powers, the Agency skipped the hearing.", "exception_clause",
     [("Invoking its emergency powers", N, True)]),
    ("en", "The Governor declared a state of emergency on Friday.", "exception_clause",
     [("declared a state of emergency", N, True)]),
    ("en", "The contract was awarded on an emergency basis.", "exception_clause",
     [("on an emergency basis", N, True)]),
    ("en", "The Board waived the 30-day comment period.", "exception_clause",
     [("waived the 30-day comment period", N, True)]),
    ("en", "The agency may waive the fee in exceptional circumstances.", "exception_clause",
     [("waive the fee", N, False), ("in exceptional circumstances", N, False)]),
    ("en", "No waiver was granted.", "exception_clause", []),
    ("en", "The records were exempt from disclosure under exemption 6.", "exception_clause", []),
    ("en", "Lawmakers debated emergency powers for hours.", "exception_clause", []),
    # --- exception_clause, pt ---------------------------------------------------------
    ("pt", "Fica dispensada a licitação para a compra de vacinas.", "exception_clause",
     [("Fica dispensada a licitação", N, True)]),
    ("pt", "A contratação ocorreu por dispensa de licitação.", "exception_clause",
     [("por dispensa de licitação", N, True)]),
    ("pt", "Excepcionalmente, o prazo foi prorrogado.", "exception_clause",
     [("Excepcionalmente", N, True)]),
    ("pt", "O município decretou situação de emergência.", "exception_clause",
     [("decretou situação de emergência", N, True)]),
    ("pt", "A licitação poderá ser dispensada em caráter emergencial.", "exception_clause",
     [("poderá ser dispensada", N, False), ("em caráter emergencial", N, False)]),
    ("pt", "Nos termos da lei, é dispensável a licitação em caso de calamidade.", "exception_clause",
     [("é dispensável a licitação", N, False)]),
    ("pt", "As associações ficaram isentas da taxa em 2025.", "exception_clause",
     [("ficaram isentas da", N, True)]),
    ("en", "The regulation provides that, in exceptional circumstances, the deadline may be extended.",
     "exception_clause", [("in exceptional circumstances", N, False)]),
    ("en", "The Commission granted the two cooperatives a one-season derogation from the ban.",
     "exception_clause", [("granted the two cooperatives a one-season derogation", N, True)]),
    ("pt", "Não foi dispensada a licitação.", "exception_clause", []),
    ("pt", "O seminário discutiu as hipóteses de dispensa de licitação.", "exception_clause", []),
    # --- burden, en -------------------------------------------------------------------
    ("en", "The applicant has not met its burden.", "burden",
     [("met its burden", "burden", True)]),
    ("en", "The burden of proof rests on the claimant.", "burden",
     [("burden of proof rests on", "burden", True)]),
    ("en", "The burden of proof shall be on the applicant.", "burden",
     [("burden of proof shall be on", "burden", False)]),
    # burden-v2: "is presumed" alone is not an act on a presumption
    ("en", "The permit is presumed valid until revoked.", "burden", []),
    ("en", "The presumption was rebutted by the audit.", "burden",
     [("presumption was rebutted", "presumption", True)]),
    ("en", "Small firms bear the tax burden.", "burden", []),
    ("en", "Presumably the office was closed.", "burden", []),
    # --- burden, pt -------------------------------------------------------------------
    ("pt", "Cabe à ré comprovar o pagamento.", "burden",
     [("Cabe à ré comprovar", "burden", True)]),
    ("pt", "O ônus da prova recai sobre o autor.", "burden",
     [("ônus da prova recai sobre", "burden", True)]),
    ("pt", "Defiro a inversão do ônus da prova.", "burden",
     [("Defiro a inversão do ônus da prova", "burden", True)]),
    ("pt", "A autora não se desincumbiu do ônus probatório.", "burden",
     [("se desincumbiu do ônus probatório", "burden", True)]),
    # burden-v2: "presume-se" and bare "presunção de …" are gone
    ("pt", "Presume-se a boa-fé do contribuinte.", "burden", []),
    ("pt", "Os responsáveis invocam a presunção de legitimidade dos atos.", "burden", []),
    ("pt", "O Tribunal afastou a presunção de boa-fé do gestor.", "burden",
     [("afastou a presunção", "presumption", True)]),
    ("pt", "O responsável alega que cabe ao Tribunal comprovar o dano.", "burden", []),
    # burden-v3: a rule reported (precedent, case law, a party's view) is not the author's
    ("pt", "Enunciado do Acórdão 10/2020: em direito financeiro, cabe ao gestor provar a aplicação.",
     "burden", []),
    ("pt", "A jurisprudência é pacífica no sentido de que compete ao gestor demonstrar o uso dos recursos.",
     "burden", []),
    ("pt", "Equivoca-se o responsável ao entender que cabe ao Tribunal comprovar o dano.", "burden", []),
    ("pt", "Rejeito a defesa. Cabe ao gestor comprovar a boa aplicação dos recursos.", "burden",
     [("Cabe ao gestor comprovar", "burden", True)]),
    # --- burden-v2: proof sense only, en ------------------------------------------------
    ("en", "The estimated paperwork burden is 3 hours per response.", "burden", []),
    ("en", "Small entities would bear the burden of the new fee.", "burden", []),
    ("en", "The Government has met its prima facie burden.", "burden",
     [("met its prima facie burden", "burden", True)]),
    ("en", "Respondent bears the burden of proof on that defense.", "burden",
     [("bears the burden of proof", "burden", True)]),
    ("en", "The burden is on the Government to prove intent.", "burden",
     [("burden is on the Government to prove", "burden", True)]),
    ("en", "The State argues that the burden of proof rests on petitioner.", "burden", []),
    ("pt", "Compete ao Município fiscalizar a obra.", "burden", []),
    # --- discretion, en ----------------------------------------------------------------
    ("en", "The decision is at the discretion of the Director.", "discretion",
     [("at the discretion of", "reserved", True)]),
    ("en", "Grants are reviewed on a case-by-case basis.", "discretion",
     [("on a case-by-case basis", "reserved", True)]),
    ("en", "The ruling is final and unreviewable.", "discretion",
     [("final and unreviewable", "review_closed", True)]),
    ("en", "The agency may, at its sole discretion, extend the deadline.", "discretion",
     [("at its sole discretion", "reserved", False)]),
    ("en", "The order is not subject to judicial review.", "discretion",
     [("is not subject to judicial review", "review_closed", True)]),
    ("en", "The matter was handled with discretion.", "discretion", []),
    # --- discretion, pt ----------------------------------------------------------------
    ("pt", "A prorrogação fica a critério da autoridade.", "discretion",
     [("a critério da", "reserved", True)]),
    ("pt", "A escolha observa juízo de conveniência e oportunidade.", "discretion",
     [("juízo de conveniência e oportunidade", "reserved", True)]),
    ("pt", "A decisão é irrecorrível.", "discretion",
     [("irrecorrível", "review_closed", True)]),
    ("pt", "Contra essa decisão não cabe recurso.", "discretion",
     [("não cabe recurso", "review_closed", True)]),
    ("pt", "O órgão poderá, a seu critério, prorrogar o prazo.", "discretion",
     [("a seu critério", "reserved", False)]),
    # --- agentless_passive, en ---------------------------------------------------------
    ("en", "Two protesters were killed on Tuesday.", "agentless_passive",
     [("were killed", "harm", True)]),
    ("en", "The account was suspended without notice.", "agentless_passive",
     [("was suspended", "sanction", True)]),
    ("en", "Mistakes were made.", "agentless_passive",
     [("Mistakes were made", "error", True)]),
    ("en", "The files were later deleted.", "agentless_passive",
     [("were later deleted", "removal", True)]),
    ("en", '"Mistakes were made," the minister said.', "agentless_passive",
     [("Mistakes were made", "error", False)]),
    ("en", "Two protesters were killed by soldiers.", "agentless_passive", []),
    ("en", "The form shall be removed after review.", "agentless_passive", []),
    ("en", "He would have been fined.", "agentless_passive", []),
    ("en", "No one was arrested.", "agentless_passive", []),
    ("en", "Accounts are removed every day.", "agentless_passive", []),
    ("en", "The fee was paid by Tuesday and the report was removed by law.", "agentless_passive",
     [("was removed", "removal", True)]),
    ("en", "Decision No. 45 was revoked.", "agentless_passive",
     [("was revoked", "removal", True)]),
    # --- agentless_passive, pt ---------------------------------------------------------
    ("pt", "Foram mortos dois manifestantes.", "agentless_passive",
     [("Foram mortos", "harm", True)]),
    ("pt", "O perfil foi suspenso ontem.", "agentless_passive",
     [("foi suspenso", "sanction", True)]),
    ("pt", "Foram cometidos erros graves na apuração.", "agentless_passive",
     [("Foram cometidos erros", "error", True)]),
    ("pt", "Os documentos foram posteriormente destruídos.", "agentless_passive",
     [("foram posteriormente destruídos", "removal", True)]),
    ("pt", "O perfil foi suspenso pela plataforma.", "agentless_passive", []),
    ("pt", "O recurso foi rejeitado por unanimidade.", "agentless_passive",
     [("foi rejeitado", "removal", True)]),
    ("pt", "O relatório deverá ser apresentado em março.", "agentless_passive", []),
    ("pt", "O suspeito não foi preso.", "agentless_passive", []),
    # --- hedge, en ----------------------------------------------------------------------
    ("en", "The minister reportedly resigned.", "hedge", [("reportedly", "adverb", True)]),
    ("en", "The so-called reform cut costs.", "hedge", [("so-called", "label", True)]),
    ("en", "The alleged victim testified.", "hedge", [("alleged", "label", True)]),
    ("en", "The official is said to have resigned.", "hedge",
     [("is said to have", "report_conditional", True)]),
    ("en", '"He allegedly lied," the lawyer said.', "hedge", [("allegedly", "adverb", False)]),
    ("en", "The form was supposed to be filed in May.", "hedge", []),
    ("en", "The company alleged that the bid was rigged.", "hedge", []),
    # --- hedge, pt ----------------------------------------------------------------------
    ("pt", "O prefeito supostamente desviou verbas.", "hedge", [("supostamente", "adverb", True)]),
    ("pt", "A suposta fraude foi investigada.", "hedge", [("suposta", "label", True)]),
    ("pt", "O deputado teria desviado verbas.", "hedge",
     [("teria desviado", "report_conditional", True)]),
    ("pt", "O grupo estaria negociando um acordo, segundo relatos.", "hedge",
     [("estaria negociando", "report_conditional", True), ("segundo relatos", "label", True)]),
    ("pt", "Se tivesse chovido, o evento teria sido cancelado.", "hedge", []),
    ("pt", "O chamado foi aberto na segunda-feira.", "hedge", []),
    # --- attribution_verb, en ------------------------------------------------------------
    ("en", "The ministry said that the plan was final.", "attribution_verb", [("said", "neutral", True)]),
    ("en", "The company claimed, without evidence, that the bid was rigged.", "attribution_verb",
     [("claimed", "distancing", True)]),
    ("en", "The agency confirmed that the data was lost.", "attribution_verb",
     [("confirmed", "endorsing", True)]),
    ("en", '"We will appeal," the lawyer said.', "attribution_verb", [("said", "neutral", True)]),
    ("en", '"The plan failed," admitted the director.', "attribution_verb",
     [("admitted", "endorsing", True)]),
    ("en", "The court confirmed the sentence.", "attribution_verb", []),
    ("en", "He was told to leave.", "attribution_verb", []),
    ("en", "The said contract was signed in May.", "attribution_verb", []),
    ("en", "The member states agreed.", "attribution_verb", []),
    # --- attribution_verb, pt ------------------------------------------------------------
    ("pt", "O ministério afirmou que o plano era definitivo.", "attribution_verb",
     [("afirmou", "neutral", True)]),
    ("pt", "A empresa alegou que não houve dano.", "attribution_verb", [("alegou", "distancing", True)]),
    ("pt", '"Reconhecemos o erro", admitiu o diretor.', "attribution_verb",
     [("admitiu", "endorsing", True)]),
    ("pt", "O Tribunal reconheceu a prescrição.", "attribution_verb", []),
    ("pt", "O ministério não confirmou que houve vazamento.", "attribution_verb", []),
    ("pt", "Foi informado que a reunião seria adiada.", "attribution_verb", []),
    # --- quotations in single quotes, and negation that must not cross a quote ----------
    ("en", "'Mistakes were made, and we apologise,' the director said.", "agentless_passive",
     [("Mistakes were made", "error", False)]),
    ("en", "'These are unverified claims,' the spokesman insisted.", "attribution_verb",
     [("insisted", "distancing", True)]),
    ("en", "The agency's director confirmed that the files were lost.", "attribution_verb",
     [("confirmed", "endorsing", True)]),
    ("pt", "'Esse suposto rombo não existe', disse o secretário.", "attribution_verb",
     [("disse", "neutral", True)]),
    ("pt", "'O pretenso acordo nunca existiu', sustentou a defesa.", "hedge",
     [("pretenso", "label", False)]),
    ("pt", "Os alertas foram ignorados por meses.", "agentless_passive",
     [("foram ignorados", "error", True)]),
    ("en", "Reimbursements will be assessed case by case, the Ministry said.", "discretion",
     [("case by case", "reserved", True)]),
    # --- reported speech closed by an inverted verb, no quotation marks ----------------
    ("pt", "Foram mortos dois manifestantes, alegou o sindicato.", "attribution_verb",
     [("alegou", "distancing", True)]),
    ("en", "The plant was safe, claimed the operator.", "attribution_verb",
     [("claimed", "distancing", True)]),
    ("pt", "O juiz, em decisão monocrática, reconheceu a prescrição.", "attribution_verb", []),
]


@pytest.mark.parametrize("lang,text,marker,expected", CASES,
                         ids=[f"{c[0]}-{c[2]}-{i}" for i, c in enumerate(CASES)])
def test_marker_case(lang, text, marker, expected):
    got = [(h.quote, h.subtype, h.invoked)
           for h in scan(text, lang=lang, markers=[marker], include_defined=True)]
    assert got == expected
