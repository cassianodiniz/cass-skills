# Importação da onboard — Cass Skills 1.1.0

Conferência em 01/11/2026, horário de Brasília.

## Origem e adaptação

- Pacote: `https://skills.praxios.com.br/assets/cass-onboard.skill`.
- SHA-256: `63c3416b267e6200e227e8d635a3e51a351b92d918f6b9b3dba76a3713754966`.
- Incorporados 13 arquivos: SKILL.md, sete scripts Python, duas referências e três assets.
- Mudanças mecânicas somente em SKILL.md e nas duas referências: `cass-onboard`
  passou a `onboard`, e o título passou de Cass Onboard para Onboard.
- Scripts e assets comparados byte a byte com o arquivo recebido, sem diferenças.
  Nenhuma das dez skills já existentes foi alterada.

## Verificações executadas

- Arquivo ZIP conferido antes da extração: caminhos contidos, sem links simbólicos
  e sem entradas fora da pasta do pacote.
- Skill Creator: quick_validate.py passou para `skills/onboard`.
- Verificador do pacote passou para onze skills, com nomes, manifestos,
  catálogos, planilha e corpus preservados. Os sete scripts novos passaram na
  análise de sintaxe Python.
- Claude Code reconheceu onze skills na versão 1.1.0 e validou o manifesto sem
  erros ou avisos de manifesto.
- Dez verificações funcionais com Python 3.13 e dados inteiramente sintéticos,
  em pasta temporária: configuração própria e cópia externa do modelo; criação
  de pasta, ficha HTML e contrato ODT; bloqueio de CPF inválido, preço divergente
  e campos ausentes sem gravar; preenchimento completo; preservação de pasta
  existente; leitura do ODT; ausência de planilha sem acesso externo;
  preservação do modelo original.

## Limites

A importação não alterou o fluxo original da skill. Os ensaios dos scripts não
comprovam execução autônoma do agente, validade jurídica do modelo nem uso clínico.
Não houve consulta de pacientes reais, acesso a Google Sheets, conversão por
LibreOffice, envio de contrato ou exportação de PDF. A configuração pessoal
existente e as pastas reais de pacientes não foram usadas ou alteradas.
As suítes dos scripts das outras skills não foram repetidas porque seus arquivos
não mudaram. As verificações anteriores permanecem no histórico abaixo.

## Histórico: ask-me na versão 1.0.1

# Validação da ask-me — Cass Skills 1.0.1

Conferência em 01/11/2026, horário de Brasília.

- Aplicação exata do diff aprovado, com 14 linhas acrescentadas à ask-me.
- Quatro cenários em três repetições por versão congelada: 12 aplicações de A
  (1.0.0) e 12 de B (1.0.1), todas em contextos novos com GPT-6.1 Terra / medium.
- B passou nos 12 casos: indicação de carrossel no prompt antes de autorizar,
  carregamento de search após autorização, ausência de skill aplicável e catálogo
  indisponível. A omitiu a nova informação nos nove casos de fechamento; o
  carregamento de search já funcionou nos três casos de execução de A.
- Revisão independente em GPT-6.1 Sol / high não encontrou defeito bloqueante
  demonstrado ou correção textual necessária; B foi mantida sem novos ajustes.
- Skill Creator: `quick_validate.py skills/ask-me` passou.
- `tests/validar_pacote.py` passou: dez skills, catálogos e três manifestos de
  plugin sincronizados, planilha, corpus e hashes preservados.
- Claude Code validou o manifesto sem erros ou avisos de manifesto e reconheceu
  as dez skills na versão 1.0.1. Codex listou o plugin único 1.0.1 como disponível,
  usando apenas sobreposições locais de configuração do comando.
- O diff reverso confere com a proposta original. As outras nove skills não
  foram alteradas. As suítes de scripts da 1.0.0 não foram repetidas, pois seus
  arquivos e comportamentos não mudaram.

Evidências, cenários e hashes: [validação do encaminhamento](tests/ask-me-routing/README.md).

Os ensaios são sintéticos: os corpos das skills chamadas devolviam um marcador
local e o objetivo do brief. Não foram executados Canva, pesquisa real, instalação
em outra conta ou testes comportamentais no Claude. Os resultados não provam
confiabilidade universal. A ordem efetiva de leitura do catálogo não tem rastros
preservados, e a indisponibilidade de uma skill já selecionada não foi exercitada.
Não houve mudança nas skills pessoais instaladas.

## Histórico: conferência da união na 1.0.0

# Validação da união — Cass Skills 1.0.0

Conferência em 01/11/2026, horário de Brasília.

## Origens preservadas

- Smart: `0ec2bc1` (0.9.0), usado como histórico-base do repositório.
- Nutri: `7271c52fb26b625d571620a31dcf2a8e1aa98bd2` (0.7.0).
- 1.755 arquivos de skills comparados byte a byte com os arquivos rastreados
  nas duas origens, sem diferenças. A ask-me permanece sem alteração.
- Os cinco PDFs, 1.234 páginas pesquisáveis, planilha-modelo e hashes do material
  nutricional passaram pelo verificador `tests/validar_pacote.py`.
- O histórico anterior do Nutri está preservado no repositório arquivado;
  seu changelog também foi incorporado ao changelog deste pacote.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| `tests/validar_pacote.py` | Dez skills, três manifestos de plugin sincronizados, dois catálogos com um único plugin, corpus e integridade conferidos. |
| `python3.13 -m unittest discover -s tests -v` | 37 testes passaram. |
| `python3 skills/search/tests/test_contrato.py` | 21 casos passaram. |
| `python3 -m unittest discover -s skills/video-maker/scripts -p 'test_*.py' -v` | 32 testes passaram. |
| `python3 skills/video-maker/scripts/test_ar_morto.py` | Todas as verificações passaram. |
| `node --test tests/test_motion_runtime.mjs` | Cinco testes passaram com runtime simulado. |
| `claude plugin validate . --strict --json` | Catálogo sem erros ou avisos de manifesto. |
| `claude plugin validate .claude-plugin/plugin.json --strict --json` | Manifesto de plugin sem erros ou avisos. |
| `claude --plugin-dir <repo> plugin details cass-skills` | Dez skills reconhecidas no mesmo plugin 1.0.0. |
| `codex plugin list --marketplace cass-skills --available --json`, com fonte local temporária por `-c` | Um único plugin `cass-skills@cass-skills`, versão 1.0.0, disponível para instalação. |

## Limites

- A primeira execução dos testes gerais usou Python 3.9.6 do sistema. O teste
  do instalador de vídeo parou na exigência de Python 3.10+. A mesma suíte
  passou com Python 3.13, sem alterar código ou enfraquecer a verificação.
- Python 3.13 emitiu ResourceWarnings nos testes antigos de SQLite, sem falhas.
- A conferência do Codex usou apenas sobreposições de configuração para o
  comando; não registrou o catálogo nem instalou o plugin na conta do autor.
- Não foram executadas instalações em contas de alunos, testes reais de Canva,
  pesquisa com serviços externos, transcrição com modelos baixados ou atendimento
  clínico completo. Não foi validada execução real em Windows/Linux.
- A ferramenta do Claude também informa exigências de licença e ícone para
  submissão ao diretório público. Esta entrega usa o catálogo do GitHub,
  preserva as condições de distribuição existentes e não submete ao diretório.
- `propostas/ask-me-roteamento.diff` é uma proposta não aplicada. Sua aplicação
  mecânica é conferida sem modificar a skill; o novo comportamento não foi testado.

## Conferências anteriores do Smart

# Validação da versão 0.7.0

Alteração em 23/10/2026 (Brasília): pesquisa de tema e caso real antes do
esqueleto de post novo, pessoa/fato no card 1 e conexão específica no card 2.
Mapas aprovados, texto final e pedidos explícitos de outro formato são preservados.
Sem caso verificável, uma alternativa fica visível e depende da aprovação do mapa.

- A versão anterior declarava a busca de pessoas opcional; esta contradição com
  o pedido fundamentou a correção. Não foi apresentada como falha observada de agente.
- 16 testes de configuração e fallback passaram com Python 3.13; o Python padrão
  3.9 estava abaixo do mínimo do instalador. Não houve correção de produto por isso.
- 21 verificações do contrato de pesquisa passaram.
- Quatro casos em três contextos novos (12 aplicações textuais): pessoa e ponte,
  morte sem relação sustentada, falha de acesso a fontes e preservação de texto
  final/ajustes pontuais. Resultados passaram na B congelada.
- Revisão independente encontrou dois gatilhos antigos que adiavam a pesquisa
  até existir mapa. C corrigiu apenas as aberturas das rotas de saúde e IA.
  Os comportamentos não afetados e testes dos scripts foram reutilizados.
- A entrada sem mapa em saúde e IA foi aplicada em três novos contextos C
  (seis ramos simulados), todos seguindo a pesquisa antes da estrutura.
  O achado foi reconfirmado independentemente como corrigido.
- Não houve notícia real pesquisada ou gravação no Canva nesta validação;
  os resultados simulados não provam desempenho de engajamento.

# Histórico: validação da versão 0.6.0

Verificação em 23/10/2026, horário de Brasília. Escopo: configuração externa,
fluxos carrossel/pesquisa/vídeo e preservação do runtime Motion. A sincronização
editorial completa de slides-canva e motion-designer não faz parte desta versão.

## Executado

- 16 testes Python de configuração e fallback: proposta sem criar pastas, ausência
  e corrupção de configuração, backup sem perda de mídia, template persistente,
  pesquisa sem sobrescrever, precedência do projeto, recusa de caminhos de cache,
  troca de versão, instaladores com configuração intacta e bloqueio ao iniciar Codex.
- 42 regressões dos scripts de carrossel, usando fixtures: estado, copy, prompts e
  índice. O revisor real foi simulado; não houve chamada a outro modelo.
- 32 testes dos scripts de vídeo e o script de regressões de corte de silêncio.
- 21 verificações do contrato de pesquisa e proveniência.
- 5 testes Node do runtime Motion: ausência de configuração, resolução externa e
  substituição da versão do plugin, recusa de caminho interno e de link simbólico
  de volta ao plugin, recusa de instalação interna antes de chamar npm.
- JSON/YAML, nomes de skills, links locais, sintaxe Python/Node e diff sem erros.
- Três contextos independentes avaliaram seis cenários cada: ambiente vazio,
  prévia com campos, modelo sem campos e revisor bloqueado, notícia sem causa de
  morte confirmada, atualização com configuração legada, e edição manual final.
  Foram 18 trajetórias simuladas aprovadas, não 18 integrações executadas.
- Revisão independente identificou e conferiu as correções de inicialização do
  revisor e de runtime/instaladores externos. Os casos novos falharam antes da
  correção e passaram depois; não foram apresentados como falhas de agente.

## Reproduzir os testes incluídos

Use Python 3.10+, Node 22+ e as dependências de edição para os testes de vídeo:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_motion_runtime.mjs
python3 skills/search/tests/test_contrato.py
python3 -m unittest discover -s skills/video-maker/scripts -p 'test_*.py' -v
python3 skills/video-maker/scripts/test_ar_morto.py
```

As 42 regressões de carrossel são da bateria local da fonte e foram executadas
contra uma cópia dos scripts distribuídos; essa bateria não faz parte do pacote.

## Limites

Não houve pesquisa real Sider/Exa nem gravação real no Canva. A rota de criação
por preenchimento depende de campos compatíveis e do acesso do usuário. Quando
não for suportada, a edição da cópia exige a aprovação de salvamento do conector;
a skill declara essa limitação e não inventa um link de conteúdo salvo.

Não foram instalados nem renderizados HyperFrames ou modelos de transcrição nesta
verificação. O engine continua HyperFrames 0.7.56; o que mudou foi seu destino e
sua resolução. Windows/Linux não foram executados nesta publicação. Os testes
com dublês verificam o encadeamento, sem provar o comportamento de serviços ou
programas ausentes. O profissional continua responsável pelas decisões clínicas.
