# Alterações

## 0.9.0

- Carrossel fixada em saúde/nutrição; removida escolha de perfil e rota editorial de IA.
- Estado novo começa em saúde. Retomadas preservam texto final e mapa aprovado.
- Pesquisa, casos, revisão e prévia Canva permanecem no fluxo.

## 0.8.0

- Renomeada `cass-carrossel` para `carrossel` no acionamento e na pasta da skill.
- Referências, exemplos de uso e testes apontam para os novos nomes; dados externos e motores preservados.

## 0.6.0

- Configuração persistente externa: pastas de posts/pesquisas/vídeo, template Canva, programas e instaladores preservados entre versões; backup e compatibilidade com configuração explícita do projeto.
- Vídeo com pastas padrão brutos/editados/trabalho/transcrições/aulas; transcrições reutilizáveis fora do cache.
- Pesquisa salva fora da skill; Sider para papers e search/web para notícias e casos.
- Carrossel com entrevista, busca opcional de notícias/pessoas, esqueleto aprovado, revisão com subagente e primeira prévia em novo rascunho Canva antes da aprovação final. Modelos sem preenchimento cumprem aprovação de salvamento exigida pelo conector.
- Template padrão persistente preservado e pergunta de continuidade após ajuste ou aprovação.
- Runtime Motion conserva HyperFrames 0.7.56 em pasta externa, com wrapper e instalador preservado; preparação também funciona após atualização com configuração intacta.
- Bloqueio ao iniciar o Codex agora prepara o prompt do subagente sem consumir rodada nem alterar a copy.

## 0.5.0

- Adicionada cass-carrossel a partir do pacote público https://skills.praxios.com.br/assets/cass-carrossel.skill, preservando seus 49 arquivos sem alterações.
- Incluídos o fluxo de mapa card a card, as referências de estilo e posts, o estado por versão e os scripts de validação e revisão da copy.
- Atualizados os dois manifestos e o README para seis skills, com origem e hash do pacote importado.

## 0.4.0

- Nova skill video-maker: edição de reels com arquivos locais, tela dividida, headline, legendas opcionais, cortes por texto e silêncio, transcrição local e conferência da fala.
- Reutilizados os adaptadores públicos do Comercial para configuração de pastas e preparação isolada das ferramentas, sem Fotos, iCloud, Notion ou cookies do autor.
- Incluídos testes de regressão da edição e registrada no README a conferência das quatro skills existentes com as fontes locais.
- slides-canva e motion-designer têm atualizações locais pendentes, descritas no README; seu conteúdo não mudou nesta versão.

## 0.3.0

- Removida a skill no-ai-slop.

## 0.2.0

- Nova skill motion-designer: motion graphics explicativo com HyperFrames, guia de estilo com dois exemplos aprovados, referências de fisiologia, ritmo de até 2,5 s, anotação com folga e tela de app copiada do print fornecido pelo usuário.
- ask-me: pergunta aberta única, entendimento compartilhado antes do pedido, perguntas sempre numeradas e fechamento com o pedido pronto e uma pergunta de execução.

## 0.1.0

- Publicação inicial de ask-me, search, slides-canva e no-ai-slop.
- Arquivamento de pesquisas dentro da skill, sem Drive ou publicação de estante.
- Slides com modelos e imagens fornecidos por cada usuário, sem assets pessoais incluídos.
- Manifesto portátil e catálogo para instalação pelo GitHub.
