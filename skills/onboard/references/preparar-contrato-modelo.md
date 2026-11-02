# Preparar o contrato modelo

> Parte da skill `onboard`. Aberto sob demanda pelo `SKILL.md`.

O contrato modelo é o **seu** contrato de sempre, com os pedaços que mudam de paciente para
paciente trocados por **marcadores**. Marcador é uma palavra entre duas chaves: `{{NOME}}`.
É só isso — não precisa mexer em mais nada, nem no layout, nem na formatação, nem nas
cláusulas.

> **Se o seu contrato está em Word, não converta nada.** Aponte o arquivo como está e a
> skill converte para `.odt` sozinha, usando o LibreOffice. Converter documento é trabalho
> da máquina, não seu.

## Como marcar (leva 10 minutos, uma vez só)

1. Abra o seu contrato no LibreOffice e salve uma cópia com o nome
   **Contrato modelo.odt**. Guarde essa cópia fora da pasta dos pacientes — ela é o
   carimbo, não um contrato.
2. Onde estiver o nome de um paciente antigo, apague e escreva `{{NOME}}`.
3. Faça o mesmo com CPF, endereço, valor, datas. Use os nomes da tabela abaixo.
4. Salve. Aponte o arquivo na configuração (`contrato_modelo`).
5. Confira o que ficou marcado:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/preencher_contrato.py" --conferir "caminho/do/Contrato modelo.odt"
```

Ele lista todos os marcadores que achou. Se a lista vier vazia, alguma coisa saiu errada
no passo 2 — provavelmente as chaves foram digitadas com o corretor automático ligado e
viraram outro caractere. Apague e digite de novo.

## O antes e o depois

**Antes** (contrato de um paciente antigo):

> Pelo presente instrumento, **Ana Paula Ferreira**, inscrita no CPF sob o nº
> **123.456.789-09**, residente na **Rua das Acácias, 45, Centro, Chapecó - SC**,
> contrata os serviços pelo valor de **R$ 1.200,00 (mil e duzentos reais)**.

**Depois** (modelo marcado):

> Pelo presente instrumento, **{{NOME}}**, inscrita no CPF sob o nº **{{CPF}}**,
> residente na **{{ENDERECO}}, {{BAIRRO}}, {{CIDADE}}**, contrata os serviços pelo valor
> de **{{VALOR}} ({{VALOR_EXTENSO}})**.

## Marcadores que existem

**Do paciente** — vêm da planilha, do texto colado ou do documento apontado:

| Marcador | O que entra |
|---|---|
| `{{NOME}}` | nome completo |
| `{{PRIMEIRO_NOME}}` | só o primeiro nome (calculado) |
| `{{CPF}}` | CPF já com pontos e traço |
| `{{NASCIMENTO}}` | data de nascimento, dd/mm/aaaa |
| `{{EMAIL}}` · `{{TELEFONE}}` | contato |
| `{{ENDERECO}}` · `{{BAIRRO}}` · `{{CIDADE}}` · `{{ESTADO}}` · `{{CEP}}` | endereço |
| `{{NACIONALIDADE}}` · `{{ESTADO_CIVIL}}` · `{{PROFISSAO}}` | o que o bloco "DAS PARTES" pede |
| `{{REPRESENTANTE}}` | quando o paciente é representado por outra pessoa |

**Contrato de casal:** repita os marcadores com `_2` — `{{NOME_2}}`, `{{CPF_2}}`,
`{{NASCIMENTO_2}}`, `{{PROFISSAO_2}}`. O CPF da segunda pessoa é conferido e formatado
igual ao da primeira, e a data dela é arrumada igual. *(O modelo que vem junto é
individual — se você atende casal, acrescente esses marcadores ao seu.)*

### A frase de pagamento — `{{PAGAMENTO}}`

Este merece um parágrafo próprio porque poupa a conta que mais dá erro. Você informa o
**valor total**, o **número de parcelas**, a **forma** e a **data da primeira**, e ele
escreve a frase inteira, com a parcela calculada do total:

- `valor 750, parcelas 3, forma "cartão de crédito", primeira 05/09/2026` →
  *em 3 (três) parcelas de R$ 250,00 (duzentos e cinquenta reais), via cartão de crédito,
  vencendo a primeira em 05/09/2026*
- `valor 1140, parcelas 1, forma "PIX", primeira 05/09/2026` →
  *em parcela única de R$ 1.140,00 (mil cento e quarenta reais), via PIX, pago em 05/09/2026*

O que você não informar simplesmente não entra na frase — melhor curta e verdadeira do que
com um buraco no meio da cláusula. No contrato modelo ela mora na cláusula 7.5.

**Do combinado** — você informa na hora:

| Marcador | O que entra |
|---|---|
| `{{PLANO}}` | o pacote escolhido (ex.: "Pacote Nutricional Trimestral") |
| `{{PAGAMENTO}}` | a frase inteira da forma de pagamento, montada sozinha (calculado) |
| `{{VALOR}}` | valor total, formatado (R$ 750,00) |
| `{{VALOR_EXTENSO}}` | o mesmo valor por extenso (calculado) |
| `{{PARCELAS}}` | número de parcelas |
| `{{VALOR_PARCELA}}` · `{{VALOR_PARCELA_EXTENSO}}` | valor de cada parcela (calculado) |
| `{{FORMA_PAGAMENTO}}` | como vai pagar |
| `{{DATA_INICIO}}` · `{{DURACAO_MESES}}` · `{{DATA_FIM}}` | vigência (o fim é calculado) |
| `{{DATA_PRIMEIRA_PARCELA}}` | quando cai a primeira parcela (ou o pagamento à vista) |
| `{{DATA_HOJE}}` · `{{DATA_HOJE_EXTENSO}}` | data da assinatura |

**Seus** — vêm da configuração, preenchidos uma vez só:

| Marcador | O que entra |
|---|---|
| `{{NUTRI_NOME}}` · `{{NUTRI_CPF}}` · `{{NUTRI_CRN}}` · `{{NUTRI_ENDERECO}}` | seus dados |

Qualquer campo que você inventar também funciona: mandar `"convenio": "Unimed"` preenche
`{{CONVENIO}}`. Não precisa avisar ninguém — o marcador que existir no documento e no
dado enviado é preenchido.

**Preços de tabela** — OPCIONAIS, para quem tem tabela de preços escrita no contrato
(calculados da lista `pacotes` da configuração, pela duração de cada pacote):

| Marcador | O que entra |
|---|---|
| `{{PRECO_MENSAL}}` · `{{PRECO_TRIMESTRAL}}` · `{{PRECO_SEMESTRAL}}` (+ `_EXTENSO`) | o preço do pacote de 1, 3 e 6 meses |
| `{{ECONOMIA_TRIMESTRAL}}` · `{{ECONOMIA_SEMESTRAL}}` (+ `_EXTENSO`) | duração × mensal − preço do pacote (calculado) |
| `{{TOTAL_TRES_MENSAIS}}` · `{{TOTAL_SEIS_MENSAIS}}` (+ `_EXTENSO`) | duração × mensal (calculado) |

Se o seu contrato não tem tabela de preços, ignore esta seção — `{{VALOR}}` continua
bastando. **Mas atenção ao dinheiro escrito fixo:** se o seu contrato tiver um valor em
reais digitado no texto (uma taxa fixa, uma multa), a skill vai PARAR no primeiro
preenchimento, mostrar o trecho, e pedir a sua confirmação de que aquele valor é
proposital — uma vez só. Preço digitado no texto é como o contrato sai dizendo um valor
numa cláusula e outro em outra, então tudo que for preço de pacote deve virar marcador; só
fica fixo o que for realmente fixo.

## Trechos que só entram se o dado existir — `[[ ]]`

Endereço de paciente às vezes vem sem bairro, sem complemento, sem CEP. Se o contrato
simplesmente deixar o campo vazio, a frase vira *"residente na Rua X, Bairro , Cidade de
Y"* — um buraco no meio do texto que ninguém nota antes de imprimir.

Para isso existe o colchete duplo: **o que estiver entre `[[` e `]]` só aparece no contrato
se todos os marcadores de dentro tiverem dado.**

No modelo:

> residente e domiciliado(a) na `{{ENDERECO}}[[, Bairro {{BAIRRO}}]][[, Cidade de {{CIDADE}}]][[ e estado de {{ESTADO}}]]`

Com bairro → *residente e domiciliado(a) na Rua Senegal, 30, Bairro Parque Monte Alegre,
Cidade de São Paulo e estado de SP*

Sem bairro → *residente e domiciliado(a) na Av. Agua Santa 440, Cidade de Capelinha e
estado de MG* — mais curta, e correta.

Repare que a vírgula e a palavra "Bairro" ficam **dentro** do colchete: elas fazem parte do
trecho que some. Serve para qualquer campo, não só endereço.

O que foi omitido é sempre reportado, e a skill é obrigada a perguntar o que você quer
fazer antes de dar o contrato por pronto — omitir não é esconder.

## Duas coisas que dão errado

**Marcador escrito de um jeito no modelo e mandado de outro.** `{{CPF}}` no contrato e
`"documento"` no dado não se encontram. O script avisa: devolve `faltando` com a lista do
que ficou sem preencher, e **não salva** — o contrato nunca sai com `{{CPF}}` visível por
acidente.

**O Word parte a palavra no meio.** Quando alguém edita no meio de um marcador, o Word
grava o texto em pedaços por baixo dos panos e a palavra fica partida. O script junta os
pedaços sozinho antes de trocar, então isso não quebra nada — mas se o marcador foi
digitado errado (`{{NOM E}}`), aí é erro de digitação mesmo e o `--conferir` mostra.
