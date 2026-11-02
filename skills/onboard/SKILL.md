---
name: onboard
description: Use quando alguém falar de paciente novo no consultório — "fechou com uma paciente", "cria a pasta da Maria", "preenche o contrato dela", "chegou paciente nova", "monta o contrato do paciente", "onde ficam os dados da fulana". Vale também para o contrato de quem já tem pasta — "gera o PDF do contrato dela", "converte o contrato pra PDF", "manda o contrato da Ana em PDF" — para a Ficha do Paciente ("monta a ficha da Maria", "organiza a anamnese dela", "transforma as respostas do formulário na ficha") — e quando a pessoa só der o nome de quem acabou de fechar, sem dizer o que quer que aconteça. Serve ainda para preparar a skill numa máquina nova ("prepara a skill pra mim", "roda o check-up"). Não é para paciente que já é atendido há tempo — é para quem está entrando agora.
---

# Onboard — paciente novo, pasta e contrato

© 2026 Cassiano Diniz. Skill criada por [Cassiano Diniz](https://instagram.com/cassiano.diniz).

Esta skill faz duas coisas, e só duas: **cria a pasta do paciente** no computador e
**preenche o contrato** dele a partir de um modelo. Não manda mensagem, não cobra, não
mexe em sistema nenhum — quem envia o contrato é a pessoa. O que sai daqui é uma pasta
com o contrato pronto para conferir. O PDF é ela quem exporta, depois de conferir
(decisão de 04/08/2026 — ver "Quando pedirem o PDF").

## Onde ficam os scripts — leia antes do primeiro comando

Todo comando desta skill começa com `${CLAUDE_SKILL_DIR}`, que é **a pasta onde este
arquivo está**. O Claude Code troca isso pelo caminho real sozinho, antes de você ler.

**Se você está vendo o texto `${CLAUDE_SKILL_DIR}` escrito assim mesmo**, a sua ferramenta
não faz essa troca (é o caso do Codex). Então use a pasta onde este `SKILL.md` está — a
mesma que contém `scripts/` e `assets/` — e siga igual. Não invente caminho e não peça o
caminho à pessoa: ela não tem como saber.

## Ao iniciar — este comando vem antes de tudo

```bash
python "${CLAUDE_SKILL_DIR}/scripts/configurar.py" --conferir
```

Rode **sempre**, antes de responder qualquer coisa e antes de perguntar qualquer coisa.
Ele devolve, numa tela só, as quatro coisas sem as quais você trabalha no escuro:

| O que volta | Para que serve |
|---|---|
| `pasta dos pacientes` | onde a pasta do paciente vai nascer |
| `contrato modelo` | **o caminho do contrato** — é este arquivo que vai ser preenchido |
| `marcadores no modelo` | **exatamente quais campos aquele contrato pede** |
| `pacotes e preços` | os pacotes dela e quanto custa cada um |

A lista de marcadores é a coisa mais importante da tela: **é dela que sai o que perguntar.**
Sem rodar isto, você não sabe onde está o contrato nem o que ele quer, e acaba perguntando
dado que não entra em lugar nenhum.

Se vier `pendencias`, resolva-as antes de seguir. Se não houver configuração nenhuma, vá
para "Primeira vez nesta máquina".

Depois disso: a pessoa já disse o nome de um paciente → Passo 1. Pediu para configurar →
"Primeira vez". Não disse nada → ofereça as três opções (paciente novo do zero, só
preencher o contrato de quem já tem pasta, conferir a configuração).

### Como passar dados para os scripts

Os scripts recebem JSON por **`--dados caminho/arquivo.json`**. Escreva o arquivo com a
Write tool numa pasta temporária (`C:/Users/<você>/AppData/Local/Temp/` no Windows,
`/tmp/` no Mac) e passe o caminho.

**Nunca use `< arquivo.json`.** No PowerShell — terminal padrão do Windows — esse
redirecionamento não existe: ele responde *"Operador '<' reservado para uso futuro"* e o
comando nem chega a rodar.

## Primeira vez nesta máquina

Quando a pessoa disser que é a primeira vez ("prepara a skill pra mim", "acabei de
instalar"), mande **uma única mensagem** com esta forma — contexto, lista com exemplos, e
o item opcional por último:

```
Pra deixar tudo pronto eu preciso de algumas coisas suas, de uma vez:

• Nome completo — como vai aparecer no contrato
• CRN — ex.: CRN-3 12345
• CPF — ex.: 000.000.000-00
• Endereço profissional — ex.: Rua Exemplo, 100, sala 2, Centro, Cidade/UF
• Cidade — a que vai no foro e na assinatura do contrato, ex.: Bauru-SP
• Seus pacotes e preços — ex.: Mensal R$ 300 (1 mês), Trimestral R$ 750 (3 meses),
  Semestral R$ 1.140 (6 meses)

Onde você quer guardar as pastas dos pacientes? Se você não tiver preferência eu uso
[CAMINHO PADRÃO], que é a pasta Documentos do seu computador.

E, se você tiver: o link da planilha do Google onde anota seus pacientes. Se não
tiver, tudo bem — a gente digita os dados na hora.
```

Os cinco primeiros vão no contrato de **todo** paciente, por isso são perguntados uma vez
só. Duas observações sobre os outros dois:

- **`[CAMINHO PADRÃO]` não é para copiar literalmente** — troque pelo valor que o
  `--conferir` devolveu em `pasta dos pacientes`. Perguntar isso importa: tem gente que
  quer no Drive, na pasta do consultório ou num HD externo, e depois de criada a primeira
  pasta mudar de lugar é trabalho manual.
- **Os preços não são detalhe.** Se ela não disser, a skill grava os preços do contrato que
  vem junto (que são de outro consultório) e depois **recusa** os contratos dela por não
  bater com o pacote. Ela leva um erro sem entender de onde veio o número.

Escreva o JSON e rode:

```json
{
  "nutricionista": {"nome": "...", "crn": "...", "cpf": "...",
                    "endereco": "...", "cidade": "..."},
  "pasta_pacientes": "C:/Users/você/Documents/Pacientes",
  "pacotes": [{"nome": "Pacote Nutricional Mensal", "valor": 300, "meses": 1},
              {"nome": "Pacote Nutricional Trimestral", "valor": 750, "meses": 3},
              {"nome": "Pacote Nutricional Semestral", "valor": 1140, "meses": 6}],
  "planilha": "https://docs.google.com/spreadsheets/d/.../edit"
}
```

Só `nutricionista` é essencial. Sem `pasta_pacientes` vai no padrão; sem `pacotes` a skill
grava os do contrato que vem junto.

```bash
python "${CLAUDE_SKILL_DIR}/scripts/configurar.py" --primeira-vez --dados <TMP>/cfg.json
```

Isso cria a pasta dos pacientes, **copia o contrato modelo para fora da skill** (para dentro
da pasta dela), grava a configuração e já devolve a conferência completa — **não precisa
rodar `--conferir` em seguida**. Rodar de novo é seguro: se ela já editou o contrato dela,
ele é mantido.

Se a conferência acusar algo faltando, mostre o comando e **peça autorização antes de
instalar**:

| Faltou | O que é | Windows | Mac |
|---|---|---|---|
| LibreOffice | converte para `.odt` o contrato que ela trouxer em Word, e é onde ela abre o contrato pronto para conferir e exportar o PDF | `winget install TheDocumentFoundation.LibreOffice` | `brew install --cask libreoffice` |

**Não há mais nada para instalar** além do Python e do LibreOffice — nenhum `pip install`.
O contrato é um `.odt`, que por dentro é um ZIP com XML, e isso o Python lê sozinho.

O LibreOffice não entra para preencher — isso é feito por dentro do arquivo, sem abrir
programa nenhum. Ele entra por dois motivos: é ele que converte para `.odt` um contrato
que venha em outro formato, e é nele que ela abre o contrato pronto para conferir e
exportar o PDF (a exportação é dela, nunca do agente — ver "Quando pedirem o PDF").

Qualquer chave dentro de `nutricionista` vira um marcador `{{NUTRI_<CHAVE>}}` no contrato.
Se o contrato dela pedir algo que não está na lista acima (por exemplo `{{NUTRI_CNPJ}}`),
basta acrescentar a chave.

O check-up avulso, quando algo falhar depois: `configurar.py --conferir`.

A configuração fica em `~/.onboard-paciente.json`, **fora da skill** — a skill é igual
para todo mundo, a configuração é de cada pessoa. O contrato dela também mora fora, pelo
mesmo motivo: atualizar a skill não pode apagar o trabalho dela.

### O contrato modelo já vem dentro da skill

**Não peça um contrato a ela antes de olhar em `assets/`.** A skill é distribuída com um
contrato de nutrição pronto e marcado lá dentro, e o `--primeira-vez` copia esse arquivo
para a pasta dela. Se o `--conferir` disser que falta contrato modelo, ele devolve junto
`modelo_que_vem_junto` com o caminho — a saída é rodar `--primeira-vez`, não perguntar.

Isso vale também quando ela **apaga ou move** a pasta `_Modelo`: rodar `--primeira-vez` de
novo recupera o arquivo, e **nunca sobrescreve** um modelo que já esteja lá.

Só há dois casos em que ela precisa entrar:

1. **Ela prefere usar o contrato dela.** Aí sim: leia com ela
   `references/preparar-contrato-modelo.md` e ajude a marcar o documento.
2. **Preencher as testemunhas** no modelo que veio junto (ficaram em branco de propósito).
   Os preços NÃO são mais trabalho de Word: desde 04/08/2026 o modelo usa marcadores
   (`{{PRECO_MENSAL}}`, `{{ECONOMIA_TRIMESTRAL}}`…) e os valores — inclusive as economias,
   os totais de comparação e a base da multa da Cláusula 16.1 — saem todos da lista
   `pacotes` da configuração, calculados na hora de preencher. Preço mora num lugar só.

**Onde as pastas nascem:** o padrão é `Documentos/Pacientes`, igual no Windows e no Mac. No
Windows é o caminho real (`C:\Users\<usuário>\Documents`), de propósito fora do OneDrive.
**Pergunte antes de assumir** — está na mensagem de primeira vez — e grave a escolha dela
em `pasta_pacientes`.

## Passo 1 — Criar a pasta

Precisa **só do nome**. Não pergunte CPF, endereço nem valor nessa hora: nada disso
impede a pasta de nascer, e travar aqui para perguntar é o jeito mais rápido de a pessoa
desistir no meio.

> 🔑 **Se houver planilha configurada, faça o Passo 2 ANTES deste.** A pessoa quase sempre
> diz o nome pela metade ("a Luna Notari"), e a pasta nasce com o nome que você passar. Se
> a planilha tem "Luna Notari Sparvieri", a pasta e o arquivo do contrato ficam com o nome
> curto para sempre enquanto o contrato lá dentro tem o nome completo — e a trava 3 proíbe
> refazer. Busque primeiro, crie a pasta com o **nome completo** que voltou.

```bash
python "${CLAUDE_SKILL_DIR}/scripts/novo_paciente.py" "Maria Aparecida Silva"
```

O script cria a pasta e copia o contrato modelo para dentro dela já com o nome certo no
arquivo. Leia a resposta:

- `nome_parecido` → **pare e pergunte.** Já existe pasta de alguém com nome parecido. Se
  for a mesma pessoa, use a pasta que existe. Se for outra pessoa mesmo, rode de novo com
  `--mesmo-assim`.
- `ja_existia: true` → a pasta já estava lá, nada foi sobrescrito. Siga para o Passo 2.
- `aviso` → o contrato modelo não está configurado ou sumiu do lugar. Diga isso e resolva
  antes de seguir.

## Passo 2 — Juntar os dados do paciente

Os dados chegam de três jeitos. Use o que a pessoa já ofereceu — não empurre o dela para
o seu. Quem colou uma ficha inteira no chat não quer responder pergunta por pergunta.

**a) Planilha do Google** (só se houver uma configurada):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/buscar_planilha.py" "Maria Aparecida Silva"
```

- `ok: true` → **mostre os dados encontrados para a pessoa confirmar** antes de usar.
  Confira também `faltando` (o que veio vazio), `cpf_valido` e `cpf_corrigido`.
- `endereco_separado` → a planilha guardava o endereço todo numa coluna só e ele foi
  **partido em rua, bairro, cidade, estado e CEP por palpite**. Se vier
  `confianca: "media"` ou `"baixa"`, ou se houver `motivos`, **mostre o resultado partido
  para a pessoa conferir** antes de escrever no contrato. Endereço errado num contrato é
  do tipo que ninguém percebe até o documento estar assinado.
- `ambiguo` ou `sugestoes` → mais de uma pessoa combina, ou nenhuma bateu. **Pergunte qual
  é.** Nunca escolha o primeiro da lista por conta própria.
- `sem_planilha` → normal, muita gente não usa planilha. Vá para (b) ou (c).

**b) Texto colado no chat.** Leia e tire os campos você mesmo — não existe script para
isso e não precisa existir. Depois **repita de volta o que entendeu, campo por campo**,
antes de usar: texto de ficha vem torto, e o que você leu como bairro pode ser
complemento do endereço.

**c) Documento apontado** (ficha de anamnese, cadastro antigo, contrato anterior):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/ler_documento.py" "caminho/da/ficha.odt"
```

Lê `.odt`, `.txt`, `.md` e `.csv` direto, tabelas incluídas. Se a ficha vier em `.docx`,
`.doc` ou `.rtf`, o próprio script converte pelo LibreOffice antes de ler — as tabelas
sobrevivem à conversão, e você **não pede** à nutricionista para converter nada.
**PDF não passa por aí** —
abra o PDF com a sua própria ferramenta de leitura. Depois de ler, mesma regra do (b):
repita o que entendeu antes de usar.

### A mensagem de perguntas — é UMA, e tem esta forma

Depois dos três caminhos acima, monte a lista do que ainda falta e mande **uma única
mensagem**, com estas três partes, nesta ordem:

1. **Uma linha de contexto** dizendo para quem é e quantos itens são.
2. **Uma lista**, um item por campo, cada um com um exemplo curto do formato esperado.
3. **A pergunta do pacote/valor** (Passo 3), se ainda não foi respondida.

Exemplo do formato certo:

```
Pra montar o contrato da Fernanda faltam 4 coisas — me passa todas de uma vez:

• Nacionalidade — ex.: brasileira
• Estado civil — ex.: solteira
• Profissão — ex.: arquiteta
• Bairro dela — a planilha trouxe a rua e a cidade, mas não o bairro

E o pacote: Trimestral (R$ 750,00) ou Semestral (R$ 1.140,00)?
```

**De onde sai essa lista:** dos `marcadores no modelo` que o `--conferir` devolveu, menos
o que você já tem. Nem um campo a mais.

- Os `{{NUTRI_*}}` já estão na configuração — nunca pergunte.
- Os calculados saem sozinhos — nunca pergunte: `{{VALOR_EXTENSO}}`, `{{VALOR_PARCELA}}`,
  `{{DATA_FIM}}`, `{{DATA_HOJE}}`, `{{DATA_HOJE_EXTENSO}}`, `{{PRIMEIRO_NOME}}`.
- `{{PAGAMENTO}}` é montado sozinho, **mas com dados que só ela tem**: em quantas vezes,
  por qual meio, e quando cai a primeira parcela. Esses três vão na pergunta do Passo 3 —
  sem eles a cláusula 7.5 sai como "em parcela única", que é verdade só para quem pagou à
  vista.
- **O contrato que vem junto com a skill não pede telefone, e-mail, data de nascimento nem
  CEP.** Se você se pegou perguntando um desses, é porque não olhou a lista de marcadores.

Se a resposta dela vier incompleta, a segunda mensagem segue a mesma forma: lista do que
ainda falta, de uma vez. Nunca uma pergunta por mensagem.

Contrato de **casal** pede os dados das duas pessoas — nesse caso mande a segunda com
sufixo `_2` (`"nome_2"`, `"cpf_2"`), que ela ganha a mesma conferência de CPF e o mesmo
ajuste de data que a primeira.

## Passo 3 — Confirmar o valor ANTES de preencher

Nunca escreva um valor no contrato sem passar por aqui. Preço é o campo que ninguém confere
depois de impresso, e é o único que a pessoa lesa a si mesma se errar.

Mostre os pacotes que estão na configuração dela (`configurar.py --conferir` traz a linha
"pacotes e preços") e pergunte **numa mensagem só**:

```
Os seus pacotes hoje estão assim:
  Pacote Nutricional Mensal — R$ 300,00 (1 mês)
  Pacote Nutricional Trimestral — R$ 750,00 (3 meses)
  Pacote Nutricional Semestral — R$ 1.140,00 (6 meses)

Para a [Nome]:
• Qual deles, pelo valor de tabela? (se combinou outro valor com ela, me diz qual
  — eu uso só neste contrato; se o seu preço mudou de vez, eu atualizo o padrão)
• Como ela vai pagar? À vista ou parcelado em quantas vezes, por qual meio
  (PIX, cartão, transferência)
• Quando cai a primeira parcela?
• Foi pagamento misto (ex.: uma parte no PIX e o resto no cartão)? Então me diz
  o valor, a forma e a data de CADA parte
```

**Pagamento misto** vai no JSON como `pagamento_partes` — uma lista, cada parte com
`valor`, `forma` e, se tiver, `parcelas` e `data`:

```json
"pagamento_partes": [{"valor": 300, "forma": "PIX", "data": "05/08/2026"},
                     {"valor": 840, "forma": "cartão de crédito", "parcelas": 3,
                      "data": "05/09/2026"}]
```

A cláusula sai descrevendo cada parte, e **a soma das partes tem que fechar o valor do
contrato** — senão o script recusa (`pagamento_nao_fecha`). Some você a conta antes de
perguntar de novo: quase sempre o que falta é uma parte que ela esqueceu de citar.

Os itens vão todos **na mesma mensagem** — os que não são o pacote alimentam a cláusula de
pagamento (7.5) e não têm de onde sair sozinhos.

Isso não é formalidade: se o valor não bater com o pacote, o `preencher_contrato.py`
**recusa** com `valor_diferente_do_pacote`, e aí há dois caminhos, que são coisas
diferentes e não devem ser confundidos:

| Ela disse | O que fazer |
|---|---|
| "com essa paciente combinei diferente" | mande `"ignorar_valor_diferente": true` — vale só neste contrato |
| "meu preço mudou" | atualize o padrão: `configurar.py --dados` com a lista `pacotes` — vale daqui pra frente |

## Passo 4 — Preencher o contrato

Escreva os dados num JSON e rode:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/preencher_contrato.py" --dados <TMP>/dados.json
```

O JSON mínimo é `odt` (o contrato dentro da pasta do paciente) + `nome`. Todo campo a
mais vira um marcador: `"convenio": "Unimed"` preenche `{{CONVENIO}}`. O script calcula
sozinho o que dá para calcular — primeiro nome, valor por extenso, valor da parcela, data
de término, data de hoje. Esses são justamente os campos que saem errados quando alguém
faz de cabeça.

Um JSON completo, com as chaves que o contrato que vem junto pede:

```json
{
  "odt": "<pasta do paciente>/Contrato - Maria Aparecida Silva.odt",
  "nome": "Maria Aparecida Silva", "cpf": "12345678909",
  "nacionalidade": "brasileira", "estado_civil": "solteira", "profissao": "arquiteta",
  "endereco": "Rua das Flores, 123", "bairro": "Centro",
  "cidade": "Bauru", "estado": "SP",
  "plano": "Pacote Nutricional Trimestral", "valor": 750,
  "parcelas": 3, "forma_pagamento": "PIX", "data_primeira_parcela": "05/09/2026",
  "data_inicio": "01/09/2026"
}
```

**A duração não vai no JSON.** `{{DATA_FIM}}` sai de `data_inicio` + os meses do pacote,
que já estão na configuração. Se o `plano` não bater com nenhum pacote configurado, aí sim
mande `"duracao_meses": 3` — senão o contrato é recusado com `faltando: DATA_FIM`.

Ele **não salva** e devolve `ok: false` nestes casos:

| Resposta | O que houve | O que fazer |
|---|---|---|
| `cpf_invalido` | o CPF não passa no dígito verificador | conferir o número com a pessoa. Contrato com CPF errado só é recusado lá na frente, quando já está na mão do paciente. Se vier `pistas`, o número provavelmente perdeu zeros à esquerda na planilha — mostre a sugestão e confirme |
| `cpf_igual_ao_seu` | o CPF do paciente é o mesmo que está configurado como o da nutricionista | quase sempre é cópia-e-cola errada. Peça o CPF do paciente de novo — o contrato sairia com a mesma pessoa nos dois lados, e o número é válido, então nada mais reclamaria |
| `valor_diferente_do_pacote` | o valor não bate com o preço do pacote escolhido | ver a tabela do Passo 3 — valor combinado só com esta paciente é uma coisa, preço novo é outra |
| `faltando` | sobrou marcador sem dado no documento | mandar os campos que faltam. Se algum tiver mesmo que ficar pendente, `"ignorar_faltando": true` salva com o marcador **aparecendo** no texto (`{{CIDADE}}` no meio da frase) — é feio de propósito, para ninguém imprimir sem ver |
| `valores_fixos` | há dinheiro escrito FIXO no texto, fora de marcador — é assim que o contrato sai com dois preços na mesma página | se for o modelo antigo da skill, troque pelo novo (rode `--primeira-vez` numa pasta nova ou recopie de `assets/`). Se for proposital (ex.: taxa fixa do contrato próprio dela), mostre os `trechos` a ela e, com o OK dela, grave o aceite **uma vez**: `configurar.py --dados` com `{"valores_fixos_aceitos": [...]}`. Só para esta rodada: `"ignorar_valores_fixos": true` |
| `economia_nao_positiva` | o texto promete "economia" num pacote longo, mas com os preços configurados a conta dá zero ou negativo — o contrato afirmaria algo falso | confirme os preços com ela. Ou o preço configurado está errado (corrija com `configurar.py --dados`), ou ela realmente cobra assim — e aí o TEXTO do contrato é que precisa mudar, por decisão explícita dela (trava 5: você aponta, ela edita) |
| `pacotes_duplicados` | dois pacotes com a mesma duração na configuração — ambíguo qual preço entra na tabela | pergunte qual vale e corrija a lista `pacotes` |

### Quando vier `omitidos` — pare e pergunte

Alguns trechos do contrato só entram se o dado existir (é o caso dos pedaços do endereço).
Quando um dado não vem, **o trecho inteiro sai da frase** em vez de deixar buraco: sem
bairro, a frase vira *"residente e domiciliado(a) na Av. Agua Santa 440, Cidade de
Capelinha e estado de MG"* — correta, só mais curta.

O contrato é salvo, mas **ele não está pronto até ela decidir**. Diga qual dado faltou e
ofereça as três saídas, com o custo de cada uma:

```
Faltou o bairro da [Nome] — a planilha não tinha esse pedaço.
Salvei o contrato sem ele: a frase do endereço ficou correta, só sem o bairro.

O que você prefere?
  a) Me passa o bairro agora → eu refaço o contrato completo em segundos.
  b) Deixa assim → o contrato é válido, mas o endereço fica incompleto no documento.
  c) Você preenche à mão antes de imprimir → eu marco o lugar pra você não esquecer.
```

**Nunca escolha por ela e nunca diga "pronto" antes da resposta.** Dado de endereço que
falta é o tipo de coisa que só aparece quando o contrato já está assinado.

**Nunca preencha um campo com texto de exemplo** para destravar o salvamento. Se a pessoa
disser "põe qualquer coisa que eu troco depois", explique que o marcador aparecendo no
documento cumpre esse papel melhor: "Rua Principal, 100" passa despercebido na hora de
imprimir, `{{ENDERECO}}` não.

Quando salvar, **mostre para a pessoa conferir**: nome completo, CPF, valor e datas.

## A Ficha do Paciente — as respostas da anamnese viram o documento de consulta

Quando ela pedir a ficha ("monta a ficha da Maria", "organiza a anamnese dela"), ou
quando as respostas do formulário de anamnese chegarem junto com os dados do contrato:
**leia `references/ficha-do-paciente.md` e siga à risca.** É trabalho seu de leitura e
julgamento — as regras de formato, os gatilhos de negrito e o gabarito estão lá.

O que não muda nunca: **fidelidade total** — a ficha só contém o que a paciente informou;
categoria sem resposta sai fora; dado confuso vira pergunta, não suposição. A ficha nasce
na pasta da paciente (`Ficha do Paciente - <nome>.html`), e ela confere antes de dar por
pronta, igual ao contrato.

## Quando pedirem o PDF — é ela quem exporta, você NUNCA converte

A skill parou de gerar PDF em 04/08/2026, de propósito: a geração automática entregava,
em certos erros, um PDF velho ou vazio com cara de pronto — e ninguém via, porque máquina
não olha o que exporta. Ela exportando à mão olha: o contrato está aberto na tela dela no
momento exato de criar o arquivo que vai pro paciente.

Quando ela pedir "gera o PDF" (ou "converte", "manda em PDF"), o seu trabalho é guiar:

1. Abra o contrato: `open ~/Documents/Pacientes/"<nome>"/"Contrato - <nome>.odt"` (Mac) ou
   `start "" "C:\...\Contrato - <nome>.odt"` (Windows).
2. Peça que ela **confira na tela** — especialmente os valores, em TODAS as partes onde
   dinheiro aparece (tabela de planos, cláusula 8ª, multa da 16.1 e a opção escolhida).
   Contrato preenchido por versão antiga da skill pode ter preço divergente entre partes:
   este é o único momento em que alguém olha.
3. Aí ela exporta: **Arquivo → Exportar como PDF → Exportar**. O PDF nasce onde ela
   salvar; sugira a própria pasta do paciente, com o mesmo nome.
4. Se já existir um PDF antigo na pasta, pergunte ANTES se ele já foi enviado a alguém —
   duas versões do mesmo contrato circulando é o problema, não o arquivo em si.

**Proibido:** rodar `soffice --convert-to`, `--headless` ou qualquer conversão automática
de PDF por conta própria, mesmo que ela peça "faz aí pra mim". O motivo de a etapa ter
saído é exatamente que a conversão sem olhos entregava o arquivo errado com selo de
sucesso. Máquina não confere; ela confere. Exportar é um clique — o clique é dela.

Depois abra a pasta para ela ver os arquivos:

```bash
# Windows
explorer "C:\Users\<usuário>\Documents\Pacientes\Maria Aparecida Silva"
# Mac
open ~/Documents/Pacientes/"Maria Aparecida Silva"
```

## Travas — valem em qualquer passo

Estas cinco moram aqui, e não dentro dos passos, porque valem entrando por qualquer
porta — inclusive quando a pessoa pede só o contrato de alguém que já tem pasta.

**1. Nunca inventar dado de paciente.** CPF, endereço, data de nascimento e valor: se não
vieram da planilha nem da pessoa, **pergunte**. Um contrato é documento — dado plausível
que ninguém confirmou vale menos que campo em branco, porque em branco alguém percebe e
preenchido errado ninguém percebe.

**2. Conferência antes de dar por pronto.** Depois de preencher, exiba nome, CPF, valor e
datas e espere a pessoa dizer que está certo. Não é burocracia: o contrato sai daqui para
a mão de outra pessoa e depois disso o erro custa uma conversa constrangedora.

**3. Não sobrescrever o que já existe.** Pasta que já existe não é recriada, contrato já
preenchido não é preenchido de novo sem a pessoa mandar. Se ela pedir para refazer, diga
o que vai ser perdido antes.

**4. Dado de paciente nunca entra na pasta da skill.** As pastas dos pacientes ficam em
`Documentos/Pacientes` e a configuração na pasta pessoal. A skill é copiada e atualizada;
o que estiver dentro dela vaza junto.

**5. Nunca edite o texto do contrato.** Você preenche marcador. Você não escreve cláusula,
não troca número dentro do texto e não apaga trecho. Nem uma palavra.

Isto vale **principalmente quando você tem certeza de que está certo**:

| O que você viu | O que fazer |
|---|---|
| o preço da cláusula não bate com o configurado | **liste os pontos e pare** — não troque o número |
| o contrato oferece um pacote que ela não vende | **diga a ela** — não apague a cláusula |
| erro de português, cláusula repetida, numeração fora de ordem | **aponte** — não corrija |
| ela disse "pode ajustar pra mim" | peça **item por item** e confirme cada um antes de tocar |

"Ajusta o que precisar" não é autorização para reescrever contrato. Autorização é ela
dizendo qual trecho, qual valor novo, um de cada vez.

**Por que é absoluto:** o documento vai ser assinado. Cláusula que some não deixa buraco
visível — o contrato continua parecendo inteiro e ninguém procura o que não está lá. Em
31/07/2026, dois agentes apagaram o Pacote Semestral do modelo (cláusula, linha da tabela e
valor) para "consertar" uma contradição de preço. Os dois avisaram, e nos dois casos a aluna
ficaria com um contrato diferente do da colega, sem saber o que perdeu.

Se o preço não bate, o trabalho é este: **mostrar onde está cada ocorrência e qual seria o
número certo**, para ela trocar no Word em dois minutos. Apontar é ajudar; editar é decidir
por ela num documento que leva a assinatura dela.

### Se você pensou isso, pare

- "o CPF dela deve ser esse, está quase certo" → nunca deduza documento
- "vou preencher com um valor de exemplo e ela ajusta depois" → contrato não tem rascunho
- "achei um nome parecido na planilha, deve ser ela" → pergunte
- "ela já falou o endereço lá em cima" → releia; se não estiver escrito, não foi dito
- "o contrato ia sair contraditório, então corrigi o texto" → apontar é consertar; editar é
  decidir por ela
- "é só trocar um número na cláusula" → número em contrato é o valor da obrigação dela
- "ela não vende esse pacote, essa cláusula não faz sentido" → não fazer sentido é problema
  dela para resolver, não seu para apagar
- "eu avisei o que fiz, então está tudo bem" → avisar não desfaz. O contrato já mudou

## Quando algo não funciona

| Sinal | Causa quase sempre |
|---|---|
| LibreOffice não encontrado | `winget install TheDocumentFoundation.LibreOffice` (Windows) · `brew install --cask libreoffice` (Mac) |
| pediram PDF | você não converte — guie a exportação manual (seção "Quando pedirem o PDF") |
| falta contrato modelo | **olhe em `assets/` antes de perguntar** — vem um pronto na skill; `--primeira-vez` copia |
| o Google devolveu a tela de login | a planilha não está compartilhada como "qualquer pessoa com o link pode ver" |
| nenhum marcador encontrado no modelo | o contrato modelo ainda não foi marcado — ver `references/preparar-contrato-modelo.md` |
| a pasta apareceu no OneDrive | `pasta_pacientes` foi configurada apontando pra lá; tire da configuração para voltar ao padrão |
| o script ficou parado sem responder | versão antiga: sem `--dados` ela esperava texto para sempre. Corrigido em 30/07/2026 |
