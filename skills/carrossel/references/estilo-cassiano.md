# Estilo de escrita de @cassiano.diniz — manual de plágio

Ficha consolidada a partir da microscopia dos 7 carrosséis mais virais (237K a 6,5K likes), feita em 24/05/2026 com 7 agentes Sonnet em paralelo, 1 por post.

**Posts analisados:** Preta Gil/Câncer (237K) · Maderite/Infarto (37K) · Caneta/Jessica (27K) · Ozzy/Parkinson (13K) · Golpe Farmacêutico/Pressão (8,4K) · Vitaminas/Coma (7,3K) · The Rock/Hormônios (6,5K).

> **Correção 27/06/2026 — viés de amostra.** Esta ficha saiu de 7 campeões de ALCANCE de saúde geral.
> Cruzada com o corpus maior >1000 curtidas, algumas regras se mostraram erradas ou estreitas demais —
> corrigidas inline abaixo (§2 tamanho de frase, §3 fluidez, §7 pessoa, §9/§12 citação). Onde a medida
> não pôde ser confirmada no corpus, virou **direção**, não regra dura.

---

## 0. A REGRA MESTRE (vale acima de tudo)

> **Se uma frase pode ser deletada sem perder dado, deletar. Nunca anunciar o dado — entregar o dado.**

Cada frase carrega informação (dado, consequência, ação, mecanismo). Nenhuma frase existe pra preparar o leitor pra próxima. Ele entra no dado **antes** de anunciar que vai entrar no dado. Quem escreve no estilo dele e coloca "vale entender que..." está errando.

---

## 1. Anatomia da frase

- Frases simples ou com 1 subordinada (no máximo 2 níveis encadeados).
- **Travessão:** ZERO em todos os 7 posts. Nunca usar.
- **Ponto-e-vírgula:** quase zero. Substituir por ponto ou vírgula.
- **Parênteses:** só pra (a) tradução técnica imediata em linha (ex: "14/9 (140/90 mmHg)") ou (b) fonte rápida (ex: "(Vigitel, 2023)"). Nunca pra comentário lateral.
- **Dois-pontos:** raro, só pra abrir lista ou conclusão direta ("O infarto não acontece do nada:").
- **Aspas:** só pra ironia ("'manipuladas'", "morte na cama").

## 2. Tamanho das frases em palavras  *(DIREÇÃO, não regra — corrigido 27/06)*

> O corpus (jsonl) não guarda a quebra por frase, então estes números são **direção, não medida fechada**.
> A leitura no corpus maior >1000 diverge da ficha original: a frase típica é **mais curta** (mediana ~12)
> e o teto **mais alto** (máx ~34); frase de 1 palavra **existe** (rara). Use como faixa, não como gabarito.

- Faixa típica: **~12 palavras/frase** (mediana), variando bastante.
- Frases de lista: 4-10 palavras cada item.
- **Padrão recorrente:** frase longa com dado denso seguida de frase curta de tradução/fechamento.
- Punchline curtíssima (1-3 palavras) **pode aparecer**, mas é rara — o ritmo vem sobretudo da sequência de dados, não da estilização.

## 3. Ritmo e cadência

- Cadência constante, **sem aceleração dramática**. Cada frase carrega dado.
- Aceleração quando empilha itens em lista por vírgula ("bacon, linguiça, peito de peru e mortadela"). Respiração vem do ponto final, não da vírgula.
- Densidade alta: cada frase entrega 1 dado + 1 consequência.
- Estrutura recorrente do card narrativo: **[dado numérico] → [tradução/exemplificação] → [frase curta de fechamento]**.
- **FLUIDEZ por formato** *(corrigido 27/06 — medido nos 13 reais).*
  **Carrossel-notícia: PROSA em 2-3 blocos visuais por card** — frases que emendam com conectores
  (e, mas, porque, já que, então), NÃO um bloco corrido único e NÃO escadinha telegráfica de uma frase
  por linha. O card respira em 2-3 blocos de prosa. **Tela-dividida e card-único: PICADO** — blocos
  curtos/labels espelhados ("Pode no Brasil:" / "Não pode:"), o contraste é o design. Ou seja: notícia =
  prosa em poucos blocos; tela-dividida/card-único = telegráfico/labels. Aplicar "texto contínuo único"
  como regra geral erra os 3.

## 4. Como abre cada card

**6 padrões de abertura validados** (escolher 1 por card, NÃO repetir o mesmo padrão em 2 cards consecutivos — varia ritmo e evita texto monótono):

| Padrão | Exemplo literal | Quando usar |
|---|---|---|
| **1. Nome próprio + verbo** | "Henrique Maderite perdeu a vida aos 50 anos..." | Card 2 (âncora com celebridade/caso) |
| **2. Dado numérico imediato** | "Hoje 1 em cada 12 mortes no Brasil..." / "27,9% da população já tem pressão alta..." | Card de escala ou impacto |
| **3. Sujeito temático nominal** | "O sódio retém água no sangue..." / "Os estudos STEP-1 e STEP-4 mostram..." | Card de mecanismo ou autoridade |
| **4. Pronome retomando gancho** | "Isso é o que provavelmente acontece..." / "É o que estão dizendo depois..." | Card que comenta o gancho |
| **5. Negação ou contraste** | "O infarto não acontece do nada" / "Pressão alta não dói" | Card de mecanismo silencioso |
| **6. Definição direta** | "Pressão alta é quando os valores estão a partir de 14/9..." | Card didático de termo técnico |

**REGRA DE VARIAÇÃO:** não usar o mesmo padrão em cards consecutivos. Se card 2 abre com nome próprio (padrão 1), card 3 abre com dado (padrão 2) ou sujeito temático (padrão 3). Se card 4 abriu com negação ("O problema é que..."), card 5 não pode abrir com negação ("O problema é que..."/"Pressão alta não..." de novo). Repetir abertura cansa e denuncia mão de IA.

**Nunca abre com:**
- Advérbio de introdução ("primeiramente", "vale lembrar")
- Pergunta retórica ("Você sabia que...?")
- Verbo de chamada ("Vamos ver", "Hoje vou falar")
- Vocativo vazio

## 5. Conectores

**USA (vocabulário inteiro de transição):**
| Conector | Uso |
|---|---|
| **mas** | Contraste/virada. No início de frase ou no meio. 1-3x por post |
| **por isso** | Causa-efeito direto |
| **fazendo** | Consequência embutida na mesma frase ("o sódio retém água, fazendo a pressão aumentar") |
| **embora** | Concessão rápida |
| **pior ainda quando** | Escalar gravidade |
| **além disso** | Adição sem pausa |
| **também** | Adição leve |
| **porque** | Causa coloquial |
| **quando** | Temporal-condicional |
| **e** | Encadeamento simples |
| **ao contrário do que alguns estão falando** | Virada (em vez de "no entanto") |

**NUNCA USA (PROIBIDOS):**
- portanto · todavia · ademais · destarte · em suma · sendo assim · dessa forma · no entanto · diante disso · assim sendo · outrossim · não obstante · destarte · em virtude de · por conseguinte

## 6. Léxico e coloquialismo

- Registro **neutro a semi-formal**. Não acadêmico, não gíria.
- "**para**" predomina sobre "pra". Texto evita "tá", "tô", "né", "olha", "imagina", "gente".
- Coloquialismo entra em **verbo ou metáfora pontual**, nunca como tom geral:
  - "faxina" (cérebro faz uma)
  - "bagunça" (dormir mal bagunça os hormônios)
  - "entupindo" (artéria vai entupindo)
  - "canetinha" (caneta emagrecedora)
  - "tá na moda" (uma vez no post de vitaminas)
- **Anglicismos:** só termos técnicos entre parênteses ("leaky gut", "dead-in-bed syndrome"), nunca como tom.
- **Nomes concretos do cotidiano:** "bacon", "salsicha", "banana", "batata doce", "presunto", "mortadela". Carregam o dado abstrato sem precisar de explicação.

## 7. Voz e pessoa

- **3ª pessoa domina o miolo todo.** O leitor observa, não é interpelado.
- **"Você" entra raramente:**
  - Para incluir o leitor no impacto ("mas você não sente nada", "De cada três pessoas que você conhece")
  - Para abrir o card de solução ("O que você pode fazer hoje:")
  - Para abrir o CTA final ("Compartilhe...")
- **"Eu" e "a gente" (corrigido 27/06):** a 3ª pessoa DOMINA o miolo, mas NÃO é "nunca aparecem". A 1ª pessoa entra: nos CTAs ("lembra de me seguir", "quando eu posto"), em posts de **opinião** onde ele assina a crítica ("me pareceu inadequada"), e como **"nós" editorial** em ressalva de incerteza ("não sabemos"). Regra certa: miolo em 3ª; 1ª pessoa reservada a CTA, opinião assinada e ressalva. **Correção 11/09/2026:** em carrossel de notícia, nem a frase de revelação usa "eu" ("Estou falando da Meta AI" foi vetado pelo Cassiano; usar "Isso é o que a Meta AI está fazendo"). Gancho e revelação também não levam ponto no meio da frase: uma frase só, emendada com conector.
- **Imperativo (corrigido 27/06):** imperativo de AÇÃO é permitido no card de checklist/conduta ("Evite", "Use", "Pratique", "Durma", "Procure" — visto em Ozzy/Pressão). O imperativo de ENGAJAMENTO ("Compartilhe", "Lembra de me seguir") fica no CTA.
- No card de solução, pode usar infinitivo em vez de imperativo ("Evitar embutidos", "Reduzir álcool").

## 8. Tipos de informação numérica

| Categoria | Como aparece | Exemplo literal |
|---|---|---|
| **Prevalência populacional** | "X% dos brasileiros" / "1 em cada N" | "70% dos brasileiros tem estilo de vida que favorece", "1 em cada 12 mortes" |
| **Risco relativo** | "X vezes mais chance" / "dobrar/triplicar" / "+X%" | "11x mais chance", "pode dobrar ou triplicar", "aumenta em 18%" |
| **Limite clínico** | número + unidade técnica + (tradução) | "14/9 (140/90 mmHg)", "Colesterol LDL abaixo de 100ng/dl" |
| **Equivalência cotidiana** | número técnico = quantidade caseira | "50g = duas fatias de presunto ou uma salsicha", "500mg = uma banana", "5g sal = 1 colher de chá" |
| **Hábito de proteção quantificado** | ação + número + redução | "Não fumar: reduz em 50%", "150 min/semana de exercício: reduz ~40%" |
| **Dose comportamental** | quantos x por semana / quantas horas | "musculação 2x por semana", "7-9 horas por noite", "8h antes de dormir" |
| **Linha do tempo fisiológica** | tempo + dano | "5-10 minutos células em sofrimento; 20-40 minutos morte irreversível" |
| **Biográfico da celebridade** | idade + dado de vida | "53 anos", "130kg para 100kg", "morreu em julho de 2025" |
| **Tamanho do estudo** | N de pessoas pra credibilidade | "Um estudo que acompanhou 88.461 adultos", "20.286 fisiculturistas" |

**REGRA DE OURO DOS NÚMEROS (corrigido 27/06):** número TÉCNICO/dose recebe equivalência concreta ("50g = duas fatias de presunto"). Prevalência/idade/amostra/ranking ("72% dos brasileiros", "88.461 adultos", "172 doenças") NÃO recebem equivalência forçada — ficam crus. Traduzir quando ajuda a entender; nunca inventar equivalência.

## 9. Construção do dado

- **Dado primeiro, explicação depois.** Sempre.
- **Fonte = instituição com nome completo,** funcionando como sujeito da frase ("A própria Organização Mundial da Saúde recomenda...", "Segundo o Ministério da Saúde, 72%...")
- **Estudo acadêmico:** citado pelo TAMANHO da amostra ("Um estudo que acompanhou 88.461 adultos descobriu..."), não por autor/revista.
- **Sobrenome + ano (corrigido 27/06):** entre parênteses no FINAL da frase ("11x mais chance... (Baggish et al., 2017)"). **VARIA POR TEMA:** nos temas técnicos (hormônio, esteroides) é NORMAL e até frequente nos virais >1000 — não "evitar". Em pauta de saúde geral, é raro. Regra: segue o tema, não proíbe.
- **Nunca:** "segundo estudo publicado no Journal of...", "de acordo com pesquisa publicada em 2023".

## 10. Encadeamento entre cards

- **ZERO gancho verbal** ("no próximo slide...", "continue lendo", "descubra abaixo").
- A continuidade é **temática implícita**. Cada card responde à pergunta que o card anterior gerou.
- Progressão padrão: gancho → âncora emocional → escala/dimensão → mecanismo → ação → CTA.
- Cada card termina com ponto final, dado fechado. Próximo abre com novo dado.

## 11. Como a celebridade é apresentada e conectada ao tema

Padrão consistente em 6 dos 7 posts (o sétimo é polêmica institucional, sem celebridade):

1. **Slide 1 (gancho):** nome próprio aparece com dado% ou com consequência grave. Apresentação curta, ~5-12 palavras de papel + idade.
2. **Slide 2 (âncora):** nome completo + idade + causa específica + **detalhe revelador**. O detalhe é o que diferencia: "sinal de Frank na orelha" (Maderite), "escala de Bristol" (Preta Gil), "de 130kg para 100kg" (The Rock), "engasgou com o próprio vômito" (Jessica), "único órgão que funcionava era o coração" (Perinalva), "morreu em julho de 2025 mencionando sofrimento" (Ozzy).
3. **Transição pro problema do leitor:** vem na FRASE imediatamente seguinte, sem ponte ("No Brasil, 2 em cada 3 pessoas têm um estilo de vida que pode favorecer..."). Não usa "como vimos com o Ozzy", não usa "isso pode acontecer com você".
4. **Celebridade desaparece** depois do slide 2. Não volta no miolo nem no CTA. O post não é sobre ela — é sobre o leitor.

**Por que funciona:** a celebridade é gancho de reconhecimento (entra em segundos). O detalhe revelador é o que prende (informação que ninguém sabia conecta a aparência ao risco). A saída rápida transfere o problema pro leitor sem moralismo.

## 12. ANTI-ESTILO — o que NUNCA aparece

Confirmado em todos os 7 posts. Se aparecer no rascunho, deletar.

- **Preâmbulos:** "vale entender que", "é importante saber", "vamos falar sobre", "antes de mais nada", "primeiro,", "hoje vou te mostrar", "neste post você vai aprender"
- **Hedging em dado:** "talvez", "parece que", "pode ser que", "acredita-se", "possivelmente". Exceção: "provavelmente" pode aparecer 1x quando ancora especulação legítima sobre comportamento privado de pessoa pública.
- **Pergunta retórica de engajamento:** "Você sabia que...?", "Já pensou nisso?", "O que você acha?"
- **Adjetivo vazio:** "muito importante", "extremamente perigoso", "super relevante", "fundamental", "absolutamente"
- **Auto-referência:** "eu sempre digo", "como costumo dizer", "como nutricionista costumo recomendar", "aprendi que"
- **Citação acadêmica COMPLETA:** "segundo estudo publicado no Journal of...", DOI, PMID, link de paper. *(Ressalva 27/06: sobrenome+ano entre parênteses NÃO é banido — é normal em tema técnico/hormônio; ver §9. O que fica banido é a citação completa/formato acadêmico.)*
- **Frase-ponte vazia:** "como vimos", "isso significa que", "ou seja", "em outras palavras", "portanto podemos concluir", "diante disso"
- **Resumo do que foi dito:** "em resumo", "recapitulando", "como vimos até aqui"
- **Saudação:** "olá", "fala pessoal", "tudo bem?"
- **Aviso de estrutura:** "neste slide você vai ver", "no próximo card", "confira abaixo", "veremos a seguir"
- **Qualificador de intensidade vazio:** "bastante", "muitíssimo", "demais"
- **Conector formal:** ver lista de proibidos na seção 5

---

## 13. NÃO super-polir — a aspereza controlada faz parte da voz

O maior risco ao "reproduzir o estilo" é **polir demais** e apagar o Cassiano. Os posts reais têm
imperfeição oral proposital, e ela é parte do que faz soar humano e não-IA:

- **Coloquialismo pontual vive:** "Tá na moda", "a canetinha", "Imagina uma loja de carros", "Pois é...".
- **Cortes secos e frases duras** são bem-vindos. Nem toda frase precisa de transição suave.
- **"pra" aparece** em contexto casual, mesmo que "para" predomine nos CTAs. Não trocar todo "pra" por "para".
- **Não reescrever pra ficar "redondo".** Se a frase real dele é meio torta mas direta, manter torta e direta.

A régua: limpar preâmbulo, hedging, conector formal e jargão acadêmico (isso É lixo de IA). Mas
**não** alisar a voz até virar texto institucional. Quando o rascunho ficar liso e elegante demais,
provavelmente perdeu o Cassiano. Aspereza controlada > perfeição sem identidade.

---

## Checklist pra usar antes de enviar pro Canva

Antes de fechar um card, conferir:

- [ ] Frase de abertura é dado, nome próprio ou afirmação direta?
- [ ] Cada número TÉCNICO/dose tem equivalência concreta ao lado? (prevalência/idade/amostra ficam crus — não forçar)
- [ ] Conector usado está na lista permitida (mas/por isso/fazendo/embora/além disso)?
- [ ] Nenhuma frase começa com "vale", "vamos", "é importante", "antes de mais nada"?
- [ ] Não tem travessão, parênteses gordos, ponto-e-vírgula?
- [ ] Voz em 3ª pessoa? "Você" só pra inclusão ou CTA?
- [ ] Celebridade entrou em 1-2 cards no máximo e saiu?
- [ ] Cada frase carrega dado/consequência/ação? Pode deletar alguma sem perder informação? Se sim, deletar.
