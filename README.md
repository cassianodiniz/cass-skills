# Cass Smart Skills

Plugin de skills distribuído pelo GitHub. Versão atual: 0.9.0.

| Skill | Uso |
|---|---|
| ask-me | Alinhar decisões por entrevista antes de executar. |
| search | Pesquisar com Exa, conferir fontes e guardar pesquisas localmente. |
| slides-canva | Preparar slides, editar no Canva e criar imagens a partir do material fornecido. |
| motion-designer | Criar motion graphics mudo que ilustra um trecho de fala (metade de cima de um reel ou tela cheia), com HyperFrames. |
| video-maker | Editar reels com pastas persistentes de brutos, editados e transcrições, headline e legendas opcionais. |
| carrossel | Entrevistar, pesquisar, aprovar o esqueleto, revisar e criar prévia em novo rascunho Canva, com template persistente. |

## Instalação no Codex

Com uma versão do Codex que suporte plugins, registre o catálogo deste repositório e instale o pacote:

```sh
codex plugin marketplace add cassianodiniz/cass-smart-skills --ref main
codex plugin add cass-smart-skills@cass-smart-skills
```

Esses comandos são instruções para quem quiser instalar. A criação deste repositório não instala o plugin na conta do autor. O registro do catálogo segue a [documentação oficial de plugins](https://developers.openai.com/plugins/build/plugins).

Depois de instalar, invoque a skill pelo nome. Exemplos:

- “Use ask-me para alinhar este pedido comigo.”
- “Use search para pesquisar este tema e guardar as fontes.”
- “Use slides-canva com este texto e o modelo que estou fornecendo.”
- “Use motion-designer para ilustrar esta fala de 7 segundos.”
- “Use video-maker para montar um reel com estes vídeos.”
- “Use carrossel para criar um carrossel sobre este tema.”

## Dependências

As skills são instruções e arquivos auxiliares. O pacote não instala nem hospeda serviços externos.

- ask-me precisa apenas de um agente capaz de ler skills.
- motion-designer requer Node.js 22 ou superior, FFmpeg com FFprobe e o HyperFrames 0.7.56 em ambiente externo (`node <instaladores>/instalar_motion.mjs --destino <ferramentas>/motion-designer`). A transcrição opcional usa Whisper MLX local. Prints de telas de app ou de IA são fornecidos pelo usuário.
- search requer acesso ao Exa e ferramentas de busca/leitura compatíveis. Configure a conexão `https://mcp.exa.ai/mcp` e autentique pelo fluxo disponível no seu cliente; a disponibilidade de nomes de ferramentas deve ser conferida ali. Os scripts locais requerem Python 3.10 ou superior. Delegação usa os agentes e modelos disponíveis no ambiente; sem agentes, o fluxo deve ser executado diretamente e a limitação informada.
- slides-canva requer um conector Canva para editar e salvar apresentações e uma ferramenta de geração de imagens para essa parte do trabalho. O usuário fornece modelos, material científico e referências visuais. Chrome é necessário apenas quando solicitado para abrir o resultado.
- video-maker requer Python 3.10+, FFmpeg/FFprobe, Pillow e NumPy. O pacote inclui um instalador para ambiente isolado e os scripts/fontes da edição; executáveis e modelos são baixados apenas na preparação autorizada. Transcrição local: Whisper large-v3-turbo via MLX em Mac compatível ou faster-whisper em CPU. Motion Designer é opcional para cenas animadas.
- carrossel usa Python 3.10+ para seus scripts e Codex CLI autenticado para a revisão com GPT 6 Sol high; sem esse revisor, o fluxo prevê subagente da sessão. A edição visual requer conector Canva e template fornecido pelo usuário. Notion, WhatsApp, Instagram e pesquisa dependem das integrações disponíveis e da rota solicitada; sem banco configurado, há registro local.
- Configurações, mídia, programas e pesquisas ficam fora do plugin, conforme [CONFIGURACAO.md](CONFIGURACAO.md). O cache pode ser somente leitura; as pastas externas precisam permitir gravação.

## Pesquisas locais

A search resolve o destino pelo local do próprio script, nunca pelo diretório de trabalho:

```text
<pastas.pesquisas>/
  BIBLIOTECA.md
  INDICE-MESTRE.md
  tema-AAAA-MM-DD/
    estudo.md
    referencias/
      INDICE.md
      fonte.md
```

O agente atualiza os índices durante a pesquisa. Execuções com o mesmo tema e data
recebem sufixos. A pasta é lida da configuração externa, não da skill instalada.
Antes de atualizar uma instalação antiga que tinha `skills/search/pesquisas/`,
preserve os resultados externamente conforme CONFIGURACAO.md; a atualização não
migra nem apaga pesquisas antigas automaticamente.

## Motion graphics

A motion-designer cria um vídeo mudo que ilustra o que a pessoa está falando, sem repetir a frase na tela. O padrão é 1080×960, para a metade de cima de um reel em tela dividida; 1080×1920 quando a cena pede tela cheia.

Fluxo:

1. O usuário cola a fala com a duração, ou aponta um vídeo com início e fim (a transcrição local é opcional).
2. A skill cria a pasta do motion com `node scripts/novo.mjs <pasta> <segundos>`, escreve a animação em HTML + GSAP e confere quadros reduzidos ao tamanho de um celular.
3. Entrega o HTML para aprovação e só então renderiza o MP4 com `node scripts/render.mjs <pasta>`, que verifica tamanho, duração, ausência de áudio e final parado.

O que vem no pacote:

- `references/estilo.md`: a receita de desenho (a coisa real no centro, câmera que passeia, enquadramentos de até 2,5 s, destaque que entra na palavra falada, anotação a pelo menos 24 px das letras, tela cheia de conteúdo) e dois exemplos aprovados em `references/estilo/`.
- `assets/fisiologia/`: seis esquemas de anatomia para temas de saúde, como referência de composição, sem validação clínica.
- Base HTML, GSAP, fontes e um mapa do Brasil por estado.

O que não vem: capturas de telas de aplicativos ou de IA. Quando a cena mostra uma tela, a estrutura segue o print que o próprio usuário fornece; sem print daquele app naquele aparelho, a skill pede um em vez de desenhar de memória. Motion acima de 15 s começa por uma cena-piloto para aprovação.

## Edição de vídeo

A video-maker recebe arquivos locais e monta MP4 vertical em 1080×1920. O padrão
é fala na metade inferior, ilustração na superior e headline inicial; legendas
dinâmicas entram quando solicitadas. Também permite cortes por texto, remoção de
silêncio e cortes de aulas longas. Planejamento e versão final passam pela aprovação
do usuário. A revisão da fala exige escuta; transcrição e quadros não a substituem.

Antes de usar, leia `skills/video-maker/references/configuracao.md`. A configuração
`.video-maker.json` pertence ao projeto do usuário e define suas pastas e padrões.
O pacote não integra Fotos, iCloud ou Notion do autor. Não inclui vídeos pessoais,
cookies nem acesso às suas contas. Trabalho e entrega ficam nas pastas configuradas.

Os comandos são relativos à pasta da skill. Se as ferramentas forem preparadas
pelo instalador incluído, use o Python do ambiente com `scripts/executar.py`.
O modelo de transcrição é baixado no primeiro uso e processa o áudio localmente.
Não foi validada nesta publicação a execução real em Windows/Linux ou a transcrição
com modelos baixados.

## Conferência com as fontes locais em 23/10/2026

| Skill | Resultado |
|---|---|
| ask-me | Idêntica à fonte local. |
| search | Conteúdo de pesquisa alinhado. Destino local de arquivamento, escolha de agentes e testes foram adaptados para distribuição pública. |
| slides-canva | Há atualizações locais ainda não incorporadas: receita de escrita por função do slide e fluxo geral de desenhos didáticos. Templates e assets pessoais são adaptações de distribuição, não pendências de sincronização. |
| motion-designer | Há atualizações locais ainda não incorporadas: imagem desde o quadro 0, catálogo de gestos aprovados e biblioteca de interfaces. O runtime Node do plugin é uma adaptação portátil do fluxo local. |
| video-maker | Adicionada a partir da fonte local atual e dos adaptadores públicos já existentes no Comercial. |

A versão 0.4.0 adicionou video-maker. A versão 0.6.0 atualiza pesquisa, carrossel e configuração de vídeo; as pendências de slides-canva e motion-designer acima continuam abertas.

## Posts de Instagram

A `carrossel` foi incorporada na versão 0.5.0 a partir do
[pacote público fornecido](https://skills.praxios.com.br/assets/cass-carrossel.skill).
São 49 arquivos: instruções, referências de estilo e formato, exemplos de posts e
cinco scripts. O SHA-256 do pacote importado é
`5ff0d63c9c7b7ded3de90cf4f1bedb04741dcc26782943d709b9978ea8112211`.

Na versão 0.6.0, a skill usa entrevista, pesquisa proporcional e esqueleto aprovado antes da copy, preserva texto final do usuário,
valida o conteúdo e organiza a revisão. A primeira prévia é um novo rascunho com link, antes da aprovação final, a partir do template padrão persistente. O preenchimento por dados cria um novo design; modelos sem campos exigem edição e a aprovação de salvamento do conector. O template permanece intacto. Arquivos de trabalho ficam em `<pastas.posts>/<slug>/`; contas, banco e destinatários são configurados pelo usuário, conforme as
instruções do pacote. Exemplos e métricas incluídos são referências do autor.

A inclusão inicial foi validada pela integridade dos arquivos, pelos links internos e pelos scripts locais. A versão 0.7.0 pesquisa o assunto e um caso real antes do esqueleto: card 1 apresenta a pessoa e o fato; card 2 faz a conexão com o tema. A escolha é proposta junto do mapa, mantendo uma só aprovação antes da copy. Sem caso verificável, a lacuna e uma alternativa são apresentadas para decisão. Sider continua sendo a rota de papers. Veja [CONFIGURACAO.md](CONFIGURACAO.md) para padrões de vídeo, transcrições e instaladores externos. Integrações externas e revisão real com GPT não foram executadas
nesta publicação.

Os nomes de acionamento não repetem o nome do plugin. Use `Cass Smart Skills: carrossel`.

## Atualizações

A publicação de novas versões é manual, somente quando solicitada ao mantenedor. Não há automação de sincronização com as skills pessoais. As versões publicadas neste repositório são adaptadas para uso por outras pessoas.

## Créditos

Pacote organizado por Cassiano Diniz. A biblioteca padrão Python basta para os scripts de pesquisa. Nenhuma licença global adicional foi atribuída ao restante do pacote.

## Validação

```sh
python3 skills/search/tests/test_contrato.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/video-maker/scripts -p 'test_*.py' -v
python3 skills/video-maker/scripts/test_ar_morto.py
```

A validação cobre o contrato de fontes, o arquivamento local e regressões da edição: cortes, processamento de transcrição com motor simulado e conferência da fala com áudio sintético. Ela não cobre a motion-designer, que depende de Node, FFmpeg e HyperFrames instalados, nem prova execução real de uma pesquisa Exa, edição Canva ou geração de imagens; esses fluxos dependem dos serviços configurados no cliente.

Detalhes dos testes executados e seus limites: [VALIDACAO.md](VALIDACAO.md).

A carrossel desta distribuição usa sempre o perfil **saúde e nutrição**, sem
seleção de perfil ou modelos editoriais de inteligência artificial. O usuário
continua fornecendo seu template Canva. Pesquisa e revisão com IA são ferramentas
do fluxo, sem alterar o perfil editorial.
