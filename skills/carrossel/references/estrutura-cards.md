# Estrutura card a card

Leia depois da captura e da classificação de domínio, antes de escrever, usando a pesquisa pertinente já coletada.

## Por que existe

O Cassiano decide a arquitetura do post, não a frase. Uma tese confirmada em prosa não é o mesmo que um mapa de cards aprovado: a tese diz "sobre o quê"; o mapa diz "o que entra em cada card e para que serve". A skill só escreve depois do mapa.

## Entrada adaptativa

1. Resuma em até 5 linhas o que entendeu: tese provável, público, material disponível, decisão ainda aberta.
2. Se perfil editorial (saúde ou IA) e formato não estiverem inequívocos no material, pergunte os dois **numa pergunta só**, no começo. Se o material já responde, confirme no resumo e não pergunte.
3. Pergunte somente o que ainda estiver faltando e que mudaria o mapa. Não repita perguntas já respondidas nem imponha entrevista quando o material é suficiente.

## Mapa provisório

Um portão único: o mapa carrega o eixo no cabeçalho. Não existe aprovação separada de eixo.

**Cabeçalho (3 linhas):** tese, público, tensão.

**Tabela:**

| Card | O que entra | Para que serve | Status ou pendência |
|---|---|---|---|

- `Status ou pendência` só quando houver dado ainda incerto, decisão real ou lacuna que impeça o card. Em card sem pendência, deixe vazio.
- A skill **pode propor por conta própria** uma linha de hipótese ("fala pública dela em 2022, a verificar") quando percebe uma lacuna que o Cassiano não pediu. Hipótese aparece no mapa como hipótese e nunca entra na copy como fato sem passar pela pesquisa.
- Não escreva frases finais de copy nesta etapa. O mapa diz o que o card faz, não como ele fala.

Após definir o tema de um post novo, execute `pesquisa-e-casos.md` antes deste
esqueleto: pesquise o assunto e um caso real relacionado, sem outra autorização.
Com caso verificável, as duas primeiras linhas do mapa são:

| Card | O que entra | Para que serve | Status ou pendência |
|---|---|---|---|
| 1 | Nome da pessoa e acontecimento sustentado pela fonte | Apresentar um gancho concreto de reconhecimento/curiosidade | Fonte e limite quando necessários |
| 2 | Conexão específica entre esse caso e o tema; o que ele ajuda a entender | Fazer a ponte para o conteúdo e motivar a continuação | Distinguir fato e interpretação |

Essas linhas descrevem função e conteúdo, ainda sem copy final. Registre pessoa,
fonte e justificativa no mapa; demais cards desenvolvem a tese com as evidências.
O card 2 precisa retomar algo específico do caso: só mencionar o famoso no card 1
e abandoná-lo no card 2 não realiza a conexão. O objetivo é interesse e retenção;
não prometa viralização nem invente uma relação para obter cliques.
Sem caso adequado, apresente a lacuna e a alternativa de `pesquisa-e-casos.md`.
Pedido explícito de outro formato pelo usuário vale sobre essa abertura padrão.
Retomada, ajuste pontual e texto final preservam as regras de autoria/atalhos.

Verifique as alegações selecionadas antes de aprovar os cards; se a conferência
mudar a arquitetura, destaque a mudança antes da aprovação. A seleção do caso é
proposta junto do mapa; não crie uma aprovação separada só para escolher a pessoa.

## Gate

Termine sempre com: “Isto é só o esqueleto: a estrutura dos cards, ainda sem a copy final. Quer editar algo ou posso escrever? Digite escreve para seguir.” Aprovar, “escreve” ou pedido equivalente autoriza registrar este mapa e escrever, sem outra pergunta de execução.

Ao receber aprovação explícita:

1. salve o mapa exato em `posts/<slug>/estrutura.md`;
2. execute `registrar_estrutura` e depois `aprovar_estrutura` (`scripts/estado.py`);
3. persista o estado.

Não escreva a copy enquanto `estrutura_aprovada_hash != estrutura_hash`. Qualquer mudança no mapa gera hash novo e exige nova aprovação.

## Atalhos

- `auditar`: não usa este gate porque não escreve.
- `incrementar`: mostre somente os cards afetados se o restante não mudar.
- `cassiano_final`: preserve a versão enviada; não reconstrua mapa.
- `retomar` em post antigo sem `estrutura_hash`: a primeira parada é montar o mapa a partir da copy existente e pedir aprovação; só então nova versão da skill.
