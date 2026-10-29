# DNA — Carrossel estilo NOTÍCIA

Fonte canônica de estrutura/receita/medida do formato **notícia**. Substitui a Parte 1 do antigo
`dna-formato-cassiano.md` (aposentado 07/09/2026), agora com a medição por formato.

> **VOZ (como soar como ele na frase):** `dna-viral-cassiano.md` + `estilo-cassiano.md`. Este arquivo é só o
> FORMATO. Não duplicar voz aqui.
> **Limites de tamanho:** a fonte única é `scripts/validar_cards.py` (notícia: total 1.350–2.100 car., 6–8
> cards, gancho 45–115). Os números medidos abaixo são o **alvo/forma dentro** desses limites — se um mudar,
> mude no validador na mesma passada (exceção #7).
> **Postura que performa:** ver `posicionamento.md` (notícia é onde mora o compartilhamento).

---

## 1. O que é
Pega um acontecimento externo com atenção já existente (morte, celebridade, susto médico, remédio em alta,
golpe, diretriz nova) e transforma em **alerta de saúde pública** com conduta. Não parece aula desde o card 1
— parece alerta. É o formato de **maior alcance** e **máquina de compartilhamento**.

## 2. Ficha medida (14 posts de alta curtida, ancorada nos mais virais)
Onde os virais fortes e os posts fracos divergem, **prevalece o forte** (os fracos não puxam o perfil).

| Traço | Alvo | Nota |
|---|---|---|
| cards | **7** | 6–8 (um viral forte, Caneta/62k, foi a 9) |
| caracteres totais | **~1.400–2.100** | não esticar além disso |
| `?` e `!` no corpo | **0** | formato declarativo; pergunta/exclamação não é daqui |
| pessoa | **3ª pessoa**; "você" 1–2×, perto do fecho | impessoal |

**Média por posição do card (núcleo forte):**
| Card | caracteres | palavras | pal/frase |
|---|---|---|---|
| C1 (capa) | **74** (70–85; até ~110 se o gancho for composto: estatística + celebridade) | 12 | 12 |
| C2 | 199 | 30 | 15 |
| C3 | 275 | 52 | 17 |
| C4 | 281 | 44 | 21 |
| C5 (pico) | **327** | 59 | 15 |
| C6 | 286 | 47 | 16 |
| **fecho (último)** | **~230** | 38 | 15 |

**Assinatura:** capa minúscula de 1 linha (~74 car.) → o corpo sobe até o **pico no C5** → e o **fecho é um card
CHEIO (~230 car.), não uma linha**. Frase mais longa no miolo (~16–21 palavras), curta e batida na capa e no
fecho. Posts "longos" têm cards mais densos, não mais cards.

## 3. Arco (o que cada card faz)
```
Card 1  CAPA = gancho (manchete)                       ← sempre
Card 2  contexto / caso real (a vítima ou celebridade) ← ou contexto da polêmica (Exceção 2)
Miolo   dado + explicação(mecanismo) + contraste + consequência  ← as funções aparecem, a ORDEM varia
Penúlt. recomendação com números práticos              ← ~9 em 14
Último  CTA = compartilhar com destinatário             ← sempre, card cheio
```
> A ordem do miolo **não é fixa** — foi onde 2 leitores independentes mais divergiram. Só capa=gancho e
> fecho=CTA são travados. Não engessar "card 3 = ponte, card 4 = prova".

**Duas sub-formas (1 formato, 2 variações):**
- **(a) Educativa / alerta** — gancho → caso → dado → explicação → **recomendação numérica** → CTA de ajudar.
  Fecho em esperança. Ex.: Preta Gil (câncer), Vitamina (coma), Caneta, Ozzy (sono), The Rock (hormônios),
  Energético, BOMB4, Anabolizante/bactéria, Mounjaro/lesões.
- **(b) Denúncia / conflito de interesse** — gancho → contexto → **contraste moral (vilão)** → dado →
  explicação → CTA, **sem** recomendação, fechando em **indignação** ("isso é correto?"). Ex.: golpe
  farmacêutico da pressão, pirâmide dos EUA comprada, Conselho vai punir, "como uma mentira tira vidas",
  "quem lucra com sua ansiedade".

## 4. Emoção por posição
Abre no **medo** → sustenta medo, com **surpresa** nos dados contra-intuitivos e **culpa** no contraste
meta×realidade → **esperança** na recomendação ("aqui está o que fazer") → fecho em esperança (educativo) ou
indignação (denúncia). Padrão **problema → agita → resolve**.

## 5. Psicologia de atenção (técnica observada, não causa provada)
| Alavanca | Exemplo | Contraexemplo |
|---|---|---|
| Especificidade numérica | "aumenta em 18%" (Preta Gil) | BOMB4 abre sem número |
| Lacuna de curiosidade | "usar BOMB4 quase destruiu os rins desse Influencer" (BOMB4) | Energético entrega tudo na capa |
| Selo de autoridade | "a própria OMS recomenda…" (Preta Gil); "11x mais chance (Baggish 2017)" (The Rock) | BOMB4 não cita instituição |
| Contraste moral / vilão | "diretriz beneficia quem financia os estudos" (pirâmide EUA) | Ozzy/sono não tem vilão |
| Compart. por prova social | "alguém que você conhece usa energético todo dia" (Energético) | BOMB4 fecha no medo |

## 6. Template
```
Card 1 — MANCHETE  (~74 car., 1 linha, afirmação; SEM pergunta)
  [número/caso grave] + [grupo amplo] + [doença/risco] + [pessoa/caso]
Card 2 — CASO  (quem, o que aconteceu, ressalva de causa se for morte)  ← ou contexto da polêmica
Miolo (~3 cards, ~280 car. cada) — DADO (número exato) + MECANISMO (linguagem visual) + CONTRASTE
  sempre com um selo de autoridade em algum ponto
Penúltimo — CONDUTA  (checklist 4–6 itens: proteína g/kg, min/semana, exames, sinais)  ← só na sub-forma educativa
Card final — FECHAMENTO  (~230 car., card cheio): frase-tese + CTA COM DESTINATÁRIO, sem dado
```

## 7. Fórmulas de gancho (card 1)
- **Celebridade + risco coletivo:** "[X]% dos brasileiros têm estilo de vida que favorece [doença] que
  [celebridade] teve."
- **Produto em alta + consequência extrema:** "[Produto] deixa [pessoa] [consequência grave]."
- **Usuário específico + risco estatístico:** "[X]% dos usuários de [substância] terão [problema] que assustou
  [pessoa]."
- **Boato + correção / denúncia:** "Estão dizendo que [boato]. Mas a explicação correta é outra." / "[golpe/
  conflito] vai tirar a vida de milhões."

## 8. Banco de finais (card cheio, com destinatário)
> "Compartilhe com alguém que usa [substância/produto]." · "Esse post pode ajudar alguém a procurar ajuda
> antes." · "Se você conhece alguém nessa situação, envie esse post." · (denúncia) "Você acha isso correto?"

## 9. Checklist antes de publicar (0–2 pontos cada)
Atualidade · Pessoa/caso · Gravidade (morte/câncer/coração/rim) · Coletivo (X%, 1 em cada) · Proximidade ·
Prevenção · Contradição/conflito · Utilidade (checklist/sinais) · Visual (rosto/print) · CTA com destinatário.
**0–7** educativo comum · **8–12** bom · **13–16** alto potencial · **17–20** forte candidato.

## 10. Exceções anti-template (medido; NÃO engessar)
1. **Prosa em 2–3 blocos por card, não picado telegráfico** (o escadinha é da tela-dividida).
2. **Card 2 = caso humano OU contexto da polêmica** (sem vítima em denúncia; não forçar "pessoa + idade").
3. **Número traduzido só quando técnico/dose** ("50g = 2 fatias"); prevalência/idade/amostra não.
4. **Imperativo de ação OK no checklist** ("Evite", "Pratique"); imperativo de engajamento ("compartilhe") só
   no CTA.

## 11. Critérios de desempenho (o formato é máquina de compartilhamento)
Forte quando: compart/views acima de 1% (muito forte >2%), salvamentos/views >0,20% (>0,35%),
interações/views >3% (>5%). Não avaliar notícia pela taxa de seguidor qualificado (isso é da tela-dividida).

## 12. Ressalvas
Ficha = descrição dos vencedores observados, não causa de alcance (escrita é piso; tema/timing é teto — ver
`posicionamento.md`). Firme: cards/posição, pontuação, tipo de dado. Exploratório: ordem do miolo, emoção nas
fronteiras. Sem controle (só vencedores desta conta).
