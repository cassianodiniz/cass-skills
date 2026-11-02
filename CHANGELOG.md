# Changelog

## 1.2.1 — Instalação global e arquivos em Documentos

- Prompt único para instalar o plugin globalmente para o usuário e preparar as dependências fora do plugin/cache.
- Novas instalações agrupam carrosséis e vídeos em Documentos/Cass Skills; Pacientes é uma opção confirmada nos configuradores próprios.
- Configurações e organização anteriores permanecem sem migração automática.
- Instaladores de vídeo e Motion recusam também os caches de skills do Claude e do Codex.

## 1.2.0 — Pastas acessíveis e intermediários de vídeo

- Novas instalações usam Vídeos/Filmes para mídia e Documentos para carrosséis; configurações antigas são preservadas.
- Abertura das pastas de entrega e atalhos visíveis sem substituir itens existentes.
- Limpeza opcional ao iniciar vídeo/motion, restrita a intermediários MP4 registrados de projetos encerrados e sem uso há mais de 30 dias.
- Originais, finais aprovados, pacientes, transcrições e projetos ativos preservados.
- Registros de geração com hashes, origens, receita e nomes imutáveis por render.

## 1.1.0 — Onboard

- Incluída a skill `onboard`, importada do pacote público `cass-onboard.skill`.
- Preservados os sete scripts e os modelos; renomeados somente o acionamento e as referências ao nome da skill.
- Atualizados a tabela do README, as dependências e os manifestos para onze skills.

## 1.0.1 — Encaminhamento pela ask-me

- Aplicado o diff aprovado: consulta das skills irmãs e indicação de seus nomes no prompt final.
- Após autorização, carregamento das skills selecionadas com o brief combinado.
- Ausência de skill adequada ou de acesso ao catálogo é informada, sem inventar nomes.
- Preservados o fluxo de entrevista, a pergunta final e as outras nove skills.

## 1.0.0 — Cass Skills

- União das seis skills do Smart com as quatro do Nutri, preservando seus arquivos.
- Catálogos para Codex e Claude Code com uma única identidade `cass-skills`.
- README com tabela das dez skills, instalação e migração dos pacotes antigos.
- Proposta de encaminhamento da ask-me entregue em diff, sem aplicação.

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


# Histórico do pacote Nutri antes da união

# Alterações

## 0.7.0

- Distribuição completa das fontes, livros, páginas, tabelas, imagens e índices disponíveis, conforme pedido do usuário.
- Consultas usam arquivos da skill instalada, sem configuração ou download separado de corpus.
- Incluídos cinco PDFs originais: Cozzolino, Costa e os três documentos de nutrição com canetas.

## 0.6.0

- Adicionada Exames Laboratoriais (`exames-laboratoriais`) a partir da skill local de Costa (2013).
- Fontes, tabelas e revisão visual mantidas privadas no corpus externo; fluxo e scripts originais preservados.

## 0.5.0

- Adicionada Nutrição Canetas (`nutricao-canetas`), com resumos e instruções da skill local.
- Corpus integral privado externo, preservado entre atualizações; buscador original mantido.

## 0.4.1

- Renomeada `book-biodisp-nutrients` para `biodisp-nutrients` no acionamento e na pasta da skill.
- Referências e testes ajustados; corpus e identificador do pacote original preservados.

## 0.4.0

- Renomeada `cass-dieta` para `dieta` no acionamento e na pasta da skill.
- Renomeada `cass-book-biodisp-nutrients` para `book-biodisp-nutrients` no acionamento e na pasta da skill.
- Referências, exemplos de uso e testes apontam para os novos nomes; dados externos e motores preservados.

## 0.2.0

- Adicionada cass-book-biodisp-nutrients, com busca e proveniência pelo motor original do corpus local.
- Preparador com validação de hashes/SQLite, corpus externo preservado e recusa de sobrescrita; o livro e seus índices não entram no repositório público.
- Incluídos testes sintéticos do preparador; dieta preservada sem alterações.

## 0.1.0

- Publicação da cass-dieta a partir do pacote público fornecido, preservando os 22 arquivos.
