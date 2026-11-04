# Cass Skills

Um único plugin com **11 skills** de conteúdo, pesquisa e nutrição para Codex e
Claude Code. Versão atual: **1.2.2**.

[Guia com downloads oficiais e prints](https://skills.praxios.com.br/).

| Skill | O que faz |
|---|---|
| [ask-me](skills/ask-me/SKILL.md) | Entrevista o usuário, prepara o prompt com as skills do pacote indicadas e encaminha a execução após autorização. |
| [onboard](skills/onboard/SKILL.md) | Organiza a entrada de pacientes: cria pastas, preenche contratos pelo modelo e monta a Ficha do Paciente com os dados fornecidos. |
| [search](skills/search/SKILL.md) | Pesquisa temas, confere fontes e organiza os resultados e referências. |
| [slides-canva](skills/slides-canva/SKILL.md) | Transforma material fornecido pelo usuário em slides e imagens didáticas no Canva. |
| [carrossel](skills/carrossel/SKILL.md) | Desenvolve posts de saúde e nutrição, da entrevista e pesquisa até a prévia no Canva. |
| [motion-designer](skills/motion-designer/SKILL.md) | Cria animações explicativas para ilustrar trechos de fala. |
| [video-maker](skills/video-maker/SKILL.md) | Edita vídeos e reels, com cortes, ilustrações e legendas opcionais. |
| [dieta](skills/dieta/SKILL.md) | Executa a prescrição dietética em planilha, sob as decisões do nutricionista. |
| [biodisp-nutrients](skills/biodisp-nutrients/SKILL.md) | Consulta o material incluído de Cozzolino sobre nutrientes, metabolismo e biodisponibilidade. |
| [nutricao-canetas](skills/nutricao-canetas/SKILL.md) | Apoia o nutricionista na alimentação de adultos que usam medicamentos para obesidade. |
| [exames-laboratoriais](skills/exames-laboratoriais/SKILL.md) | Consulta conceitos e tabelas de Costa (2013), identificando os limites dessa fonte histórica. |

## Como usar

Escreva o que você quer fazer com suas próprias palavras. Se ainda não souber
como pedir ou qual skill escolher, acrescente **`/ask-me`** ao final do pedido.

```text
Quero criar conteúdo para meus pacientes, mas ainda não sei qual formato usar.
Me ajude a organizar a ideia e decidir por onde começar.
/ask-me
```

A **ask-me é uma skill poderosa para alinhar a IA ao que você quer**: ela faz
perguntas, esclarece o objetivo e prepara um prompt com as skills adequadas.
Depois da sua aprovação, o agente continua com o pedido combinado.

Selecione a skill no menu do aplicativo. No Claude Code, o nome completo é
`/cass-skills:ask-me`. Se já souber qual usar, pode pedi-la diretamente pelo nome.

## Onde encontrar as entregas e como funciona a limpeza

Para novas instalações, a base sugerida é **Documentos → Cass Skills**:

| Conteúdo | Pasta sugerida |
|---|---|
| Carrosséis | `Carrosséis/<tema>/` |
| Vídeos | `Vídeos/`, com Originais, Prontos, Projetos, Transcrições e Aulas |
| Pesquisas | `pesquisas/` |
| Dietas, fichas e contratos | `Pacientes/`, opcional e confirmada na configuração do consultório |

A IA confirma as pastas, oferece atalhos na Área de Trabalho e abre a pasta ao
entregar. Pastas já configuradas são preservadas; atualizar não migra trabalhos.

A limpeza começa **desligada**. Se você ativar, ao usar vídeo ou motion ela pode
remover apenas MP4s intermediários registrados, recriáveis, de projetos encerrados
e sem uso há mais de **30 dias**. Originais, finais aprovados, pacientes, roteiros,
transcrições e arquivos antigos sem registro são preservados. Não há serviço de
limpeza em segundo plano.

## Instalar

No Codex ou no Claude Code, copie o prompt abaixo e envie como uma mensagem.
Ele pede a instalação global para seu usuário e prepara as dependências **fora
da pasta do plugin**, para continuarem disponíveis após as atualizações.

<details>
<summary>Ver e copiar o prompt completo de instalação</summary>

```text
Instale globalmente para o meu usuário o plugin Cass Skills deste repositório: https://github.com/cassianodiniz/cass-skills . Deixe-o disponível em todos os meus projetos no aplicativo que estou usando, Codex ou Claude Code. Faça a instalação e os testes por mim, explicando em português simples.

Identifique o aplicativo, o sistema operacional e a arquitetura. Leia o README e a CONFIGURACAO.md atuais do repositório. Use o catálogo e o instalador oficial do aplicativo; no Claude Code, escolha o escopo user. Confira as 11 skills do pacote. Se o plugin já existir, atualize pela rota oficial, preservando configurações e trabalhos. Se este ambiente não permitir instalar plugins ou acessar o computador, explique o impedimento e o local compatível para continuar, sem afirmar que instalou.

Instale também todas as dependências locais necessárias para as skills funcionarem neste computador. Este pedido já autoriza instalar os componentes gratuitos necessários de fontes oficiais, respeitando as permissões do sistema. Reaproveite instalações compatíveis que já funcionam. Confira Python 3.10+, Node.js 22+ com npm/npx, Git, LibreOffice, um navegador Chromium compatível, WeasyPrint e suas bibliotecas nativas, pypdf no Python usado pela dieta ou pdftotext no PATH, FFmpeg/FFprobe com filtros ASS e drawtext, Pillow, NumPy, HyperFrames na versão fixada pelo plugin e o navegador de renderização exigido por ele. Prepare a transcrição Whisper large-v3-turbo com o motor compatível: MLX em Mac Apple Silicon ou faster-whisper em CPU. Leia os requisitos das skills e complete o que faltar, sem trocar silenciosamente ferramentas ou modelos.

REGRA DE PERSISTÊNCIA: instale programas, ambientes Python, node_modules, navegadores de renderização, modelos de IA e caches de ferramentas FORA da pasta do plugin e de qualquer pasta/cache de skills do Codex ou Claude. Atualizações substituem essas pastas. Use os locais nativos dos aplicativos e os ambientes externos previstos pelo plugin, como ~/.cass-smart-skills/ferramentas e ~/.cass-dieta/weasyprint-venv. Resolva esses caminhos no usuário real e confira o destino efetivo, inclusive links simbólicos. Não execute pip install ou npm install dentro do plugin. Os scripts e modelos distribuídos podem vir no pacote; programas instalados, configurações pessoais e cópias editáveis ficam fora dele. Preserve as cópias externas dos instaladores seguindo CONFIGURACAO.md.

Para meus arquivos, use a pasta Documentos real do sistema, inclusive quando redirecionada ao OneDrive/iCloud, com a base Cass Skills e as subpastas Carrosséis e Vídeos. Dentro de Vídeos, mantenha Originais, Prontos, Projetos, Transcrições e Aulas. Mostre a localização e confirme uma vez antes de salvar a configuração. Se eu quiser usar o consultório, ofereça também Documentos/Cass Skills/Pacientes e configure dieta/onboard pelas rotas próprias, apenas depois da minha escolha. Preserve pastas e configurações anteriores; não mova ou una arquivos antigos sem meu pedido. Não é necessário cadastrar pacientes, preços ou dados profissionais para instalar as ferramentas.

Ofereça atalhos para essas pastas na Área de Trabalho. A limpeza de vídeos começa desligada: pergunte separadamente se quero ativar a remoção de intermediários recriáveis de projetos encerrados e sem uso há mais de 30 dias. Preserve originais, finais aprovados, pacientes e arquivos antigos sem registro; use somente o mecanismo de limpeza do plugin.

Confira também as integrações das skills: Exa para pesquisa, Canva para carrosséis e slides, geração de imagens. Configure o que este aplicativo permitir, reutilizando minhas conexões. Quando depender de login, autorização ou serviço pago, mostre exatamente a pendência e o passo de conexão. Não peça segredos no chat nem crie assinaturas. Recursos opcionais só são necessários para a rota que os usa.

Valide pelos wrappers reais do plugin e pelos ambientes externos configurados, com arquivos sintéticos em pasta temporária externa: recálculo de planilha no LibreOffice, geração e leitura de PDF, vídeo curto com FFmpeg/FFprobe, uma renderização curta usando render.mjs e o HyperFrames, com FFmpeg/FFprobe acessíveis ao processo de Motion e transcrição de áudio sintético no motor escolhido. Guarde downloads grandes e modelos apenas nos destinos externos e informe o espaço ocupado. Não use dados de pacientes nem meus vídeos para testes. Preserve meus arquivos e remova somente os temporários que você criou. Informe os testes aprovados e as pendências por recurso; não declare tudo pronto apenas porque os programas existem.

Ao terminar, mostre onde estão o plugin, os programas e meus arquivos, confirme o escopo global do usuário e diga se preciso abrir um novo chat. Oriente-me a chamar ask-me: ela entrevista sobre o que quero fazer e indica a skill adequada.
```

</details>

É o mesmo [prompt em texto](INSTALAR.txt) oferecido no
[site com o passo a passo](https://skills.praxios.com.br/).

## Dependências essenciais

O prompt verifica o que já funciona e prepara os componentes necessários:

- **Documentos e dietas:** Python 3.10+, LibreOffice, navegador compatível,
  WeasyPrint e leitor de PDF para os scripts.
- **Vídeos e animações:** Node.js 22+, FFmpeg/FFprobe, Pillow, NumPy, HyperFrames
  na versão fixada e Whisper com o motor compatível com o computador.
- **Pesquisa e criação visual:** Exa, Canva e geração de imagens conforme a tarefa.
  Conexões que dependem da sua conta podem pedir autenticação.

Programas, modelos baixados, configurações e arquivos pessoais ficam fora do
plugin. As skills de consulta levam as fontes de apoio; o nutricionista revisa
as decisões clínicas e observa os limites históricos dos materiais.

Detalhes: [configuração](CONFIGURACAO.md),
[pastas e limpeza](references/arquivos-e-limpeza.md),
[validação e limites](VALIDACAO.md) e [histórico de versões](CHANGELOG.md).

Organizado por Cassiano Diniz.
