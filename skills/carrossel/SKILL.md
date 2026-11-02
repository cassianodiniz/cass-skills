---
name: carrossel
description: Use quando Cassiano pede para criar, desenvolver, revisar, retomar ou montar no Canva um post de Instagram; anotar ou listar ideias de post; continuar um post que a Carine começou ou abrir um post do banco Posts Carrossel no Notion; ou pede explicitamente para procurar carrosséis de referência no Meta AI ou Instagram. Não usar para stories, reels, vídeos ou análise isolada de métricas.
---

# Carrossel

© 2026 Cassiano Diniz. Skill criada por [Cassiano Diniz](https://instagram.com/cassiano.diniz).

Cria o post do tema ao Canva pronto, preservando autoria, fatos verificáveis e autorização operacional.

## Raiz

Para facilitar o acesso à entrega, siga [pastas e abertura](../../references/arquivos-e-limpeza.md#pastas-e-acesso).
Ao entregar uma versão, abra a pasta local do post, forneça o arquivo e o link
Canva quando houver. Não execute limpeza de vídeos ao criar carrosséis.

Use como raiz de instruções e scripts a pasta deste SKILL.md.
Antes de criar um trabalho, leia [configuração persistente](../../CONFIGURACAO.md).
Reutilize `pastas.posts` da configuração externa; sem configuração, proponha as
pastas e confirme uma vez. Guarde o trabalho em `<pastas.posts>/<slug>/`, sem
escrever nos exemplos da skill. Resolva `scripts/` e `references/` a partir desta skill;
`posts/<slug>/` nas referências significa essa pasta absoluta de trabalho.
Na entrada, conduza o alinhamento com a skill `ask-me` disponível no plugin, usando
apenas as perguntas ainda abertas. A resposta pronta da entrevista é o esqueleto
card a card descrito abaixo; “escreve” é a autorização para executá-lo. Se o pedido
já autoriza a execução e o esqueleto foi aprovado, não crie outra confirmação.
Sem ask-me disponível, siga diretamente as rodadas de `estrutura-cards.md`.

## Perfil desta distribuição

Esta carrossel é voltada exclusivamente a **saúde e nutrição**. Use sempre
`perfil_editorial="saude"`; não pergunte se o perfil é saúde ou inteligência
artificial e não ofereça modelos editoriais de IA. Pergunte apenas tema, público,
objetivo e formato ainda não informados. As ferramentas de IA usadas para
pesquisar ou revisar continuam disponíveis; isso não muda o perfil do conteúdo.

## Configuração desta distribuição

Esta é a versão pública da skill do Cassiano. Nas instruções operacionais,
“Cassiano”, “Carine” e “ele” significam o usuário que está criando/aprovando o post.
Posts e métricas do Cassiano são referências do autor, nunca histórico do usuário.
Os códigos internos `cassiano_final` e `cassiano_rascunho` são mantidos para o motor
de estado funcionar; representam texto final ou rascunho fornecido pelo usuário.
Canva, Notion e WhatsApp só usam conta, modelo, banco e destinatário fornecidos
pelo usuário. Sem configuração de integração, mantenha os arquivos locais e
explique o que falta; nunca procure as contas pessoais do autor.
O revisor usa o mesmo GPT pelo Codex CLI da versão local; requer Codex instalado
e autenticado. Sua alternativa é o subagente da sessão, conforme escrita-revisao.md.

## Travas permanentes

1. Classifique o pedido como `gerar`, `incrementar` ou `auditar`. Em `auditar`, não reescreva silenciosamente.
2. Não invente fatos, fontes, falas, links, métricas ou experiências do Cassiano.
3. A copy é escrita sempre depois do mapa card a card aprovado, com a âncora de voz. Copy escrita ou alterada pela skill passa pelo revisor GPT 6 Sol (esforço high, via Codex) antes de ser mostrada, no máximo 2 rodadas por versão. Copy declarada final pelo Cassiano é preservada, registrada como aprovada e não chama o revisor; o validador roda nela só como informação, sem bloquear.
4. Auditoria só quando o Cassiano pedir explicitamente: modo `auditar`, devolve achados e nunca reescreve. Auditar uma versão final dele exige pedido separado. O revisor é sempre o GPT pelo Codex; se ele falhar, a revisão vai para um subagente do modelo da sessão (ver `escrita-revisao.md`); só pare e explique se o subagente também falhar. Nenhum outro modelo entra.
5. Quem está no post (Cassiano ou Carine) decide depois de ler a versão revisada: aprovar, pedir ajustes ou mandar aos mentores. A skill não julga quem pode decidir; o pedido de criar a prévia no Canva não é aprovação final do post.
6. WhatsApp exige versão e hash exatos, autorização expressa e um único intento de envio. Timeout não autoriza repetição.
7. Mentores aconselham; não aprovam nem mudam automaticamente a copy.
8. Canva sempre preserva o template padrão. Depois do esqueleto aprovado e da revisão da copy, crie a primeira prévia em um rascunho novo com link, antes da aprovação final do post. Use a criação por preenchimento quando suportada; qualquer edição/salvamento cumpre as aprovações exigidas pelo conector (`canva.md`).
9. Persista o estado antes de cada efeito externo.
10. Pesquisa editorial no Meta só acontece quando Cassiano pedir explicitamente pela fonte. Ela não
    faz parte automática de `gerar`, `incrementar` ou `auditar` e não substitui a pesquisa factual.
11. Ideias e posts moram no banco Posts Carrossel do Notion, compartilhado com a Carine: só texto do post,
    fontes e onde paramos vão para lá, gravados sem perguntar ao fim de cada etapa e relendo a página antes
    (ver `notion.md`). O resto fica local.

## Progressive disclosure

Carregue somente o necessário para a etapa atual:

| Situação | Ler |
|---|---|
| Anotar ou listar ideia, gravar etapa, retomar ou continuar post do Notion (inclusive da Carine) | [references/notion.md](references/notion.md) |
| Entrada, retomada, classificação e aprendizado | [references/fluxo-base.md](references/fluxo-base.md) |
| Entender o pedido e propor o mapa card a card antes da copy | [references/estrutura-cards.md](references/estrutura-cards.md) |
| Criar, migrar ou validar estado | [references/estado.md](references/estado.md) |
| Definir voz, domínio e rota de pesquisa | [references/perfil-editorial.md](references/perfil-editorial.md) |
| Pesquisar notícias, pessoas, casos ou escolher search/Sider/web | [references/pesquisa-e-casos.md](references/pesquisa-e-casos.md) |
| Configurar pastas e recuperar preferências após uma atualização | [Configuração persistente](../../CONFIGURACAO.md) |
| Verificar os fatos escolhidos para o mapa | [references/politica-factual.md](references/politica-factual.md), depois a rota do domínio |
| Pedido explícito para procurar posts no Meta ou Instagram | [references/pesquisa-meta.md](references/pesquisa-meta.md) |
| Escrever ou revisar | [references/escrita-revisao.md](references/escrita-revisao.md) e só as referências de formato indicadas ali |
| Enviar aos mentores ou ler respostas | [references/mentores-whatsapp.md](references/mentores-whatsapp.md) |
| Aparecer link do Instagram | [references/instagram-link.md](references/instagram-link.md) |
| Montar no Canva | [references/canva.md](references/canva.md) e [references/templates-canva.md](references/templates-canva.md) |
| Dúvida sobre qual referência responde a quê, ou consulta a um post real do Cassiano (texto, métrica) | [references/LEIA-PRIMEIRO.md](references/LEIA-PRIMEIRO.md) (mapa de todas as referências) e [references/posts-virais/INDICE.md](references/posts-virais/INDICE.md) |

Não carregue Canva, WhatsApp, Instagram, pesquisa no Meta ou pesquisa de outro domínio antecipadamente.

## Fluxo canônico

Se o pedido for só anotar uma ideia, registre-a como `Ideia` seguindo `notion.md` (localmente quando não houver banco configurado) e pare.
Se o pedido for somente procurar referências no Meta ou Instagram, execute `pesquisa-meta.md` e pare.
Não crie estado, mapa ou copy. O fluxo abaixo só começa quando Cassiano trouxer um material e pedir a
criação ou alteração do post.

1. Capture o material e classifique autoria e domínio.
2. Explique em até 5 linhas o que entendeu; use o perfil saúde e pergunte somente o formato, se faltar, e depois só as lacunas que mudariam o post.
3. Definido o tema de um post novo, pesquise o assunto e um caso real de pessoa relacionado a ele, antes do esqueleto, pelas rotas de `pesquisa-e-casos.md`. Essa pesquisa já faz parte da criação: não peça autorização separada para pesquisar. Use Sider para papers e busca web para notícias/casos. Proponha o esqueleto com o nome da pessoa e o fato sustentado no card 1 e uma conexão específica entre o caso e o tema no card 2, além de tese, público, tensão, fontes e lacunas. Sem caso verificável, siga a alternativa explícita daquela referência. Preserve texto final do usuário e mapas já aprovados na retomada.
4. Mostre o esqueleto identificado como estrutura provisória e pergunte: “Quer editar algo ou posso escrever? Digite escreve para seguir.” Espere a aprovação explícita do usuário. Só com o mapa aprovado a copy é escrita — com a âncora de voz — e passa pelo validador determinístico.
5. GPT 6 Sol high revisa e limpa a versão (se falhar, subagente do modelo da sessão). Revalide; se necessário, faça somente uma segunda rodada corretiva.
6. Monte a primeira prévia em novo rascunho do Canva conforme `canva.md` e mostre o link, a copy completa, fontes, lacunas, versão e resultado das validações. Se faltar template, conexão ou operação compatível, entregue a copy local e explique o passo pendente; não invente link salvo.
7. Quem está no post escolhe: aprovar, editar à mão (no `copy.md` ou no Notion), revisar ou enviar aos mentores. Edição à mão é preservada e não passa pelo revisor, salvo pedido explícito.
8. Após ajuste ou aprovação, preserve o que foi aceito, informe o resultado e pergunte o próximo passo apropriado (ajustar, exportar ou entregar). Um pedido explícito de ajuste já autoriza esse ajuste; não repita a autorização. Canva e integrações seguem suas próprias rotas.

Ao fim de cada etapa (mapa aprovado, versão mostrada, pausa, pedido de Canva, publicação), grave no Notion conforme `notion.md`.

## Estado por post

O texto final, as fontes e onde paramos ficam no Notion (`notion.md`). O bastidor de cada post vive em `posts/<slug>/`:

- `estado.json`: máquina de estados e autorizações;
- `estrutura.md`: mapa card a card aprovado;
- `material/`: anexos e insumos preservados;
- `fatos.md`: alegações e fontes;
- `copy.md`: versão textual atual;
- `cards.json`: mapeamento visual;
- `feedback-mentores.md`: respostas processadas.

Ao retomar, leia primeiro a página do Notion (se houver), `estado.json`, `copy.md` e apenas as referências da fase atual. Sem pasta local (post da Carine, outra máquina), recrie-a a partir da página. Arquivos legados são consultados sob demanda.

## Saída obrigatória antes da decisão

Apresente:

- copy completa;
- versão e hash;
- status do validador;
- quantidade de rodadas do revisor e modelo usado;
- fontes e lacunas relevantes;
- escolhas disponíveis: aprovar, revisar ou enviar aos mentores.
