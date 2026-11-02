# Modelo_Contrato_Nutricao.odt

Contrato de prestação de serviços nutricionais já **marcado** para a skill preencher.

> ⚠️ **Este contrato é um EXEMPLO, para você se inspirar — não é consultoria jurídica.**
> Antes de usar com paciente de verdade, sempre consulte um advogado. Quem responde pelo
> conteúdo do contrato é você.

Serve como ponto de partida — quem preferir usar o próprio contrato é só marcar do mesmo
jeito (ver `references/preparar-contrato-modelo.md`).

**Três pacotes** (Mensal, Trimestral e Semestral — 1 consulta por mês, pela duração do
plano). Os valores não estão mais impressos aqui nem no contrato: entram pelos marcadores,
com os preços que VOCÊ configurou.

**35 marcadores**, nesta ordem no documento:

- **De quem atende** (vêm da configuração, preenchidos uma vez só): `{{NUTRI_NOME}}`,
  `{{NUTRI_CRN}}`, `{{NUTRI_CPF}}`, `{{NUTRI_ENDERECO}}`, `{{NUTRI_CIDADE}}` — este último
  aparece duas vezes: no foro (Cláusula 20ª) e na data de fechamento.
- **Do paciente:** `{{NOME}}`, `{{NACIONALIDADE}}`, `{{ESTADO_CIVIL}}`, `{{PROFISSAO}}`,
  `{{CPF}}`, `{{ENDERECO}}`, `{{BAIRRO}}`, `{{CIDADE}}`, `{{ESTADO}}`.
- **Dos preços de tabela** (vêm da lista `pacotes` da configuração, calculados na hora —
  Cláusula 8ª, tabela de opções e base da multa da 16.1): `{{PRECO_MENSAL}}`,
  `{{PRECO_TRIMESTRAL}}`, `{{PRECO_SEMESTRAL}}` e seus `_EXTENSO`;
  `{{ECONOMIA_TRIMESTRAL}}`, `{{ECONOMIA_SEMESTRAL}}` e seus `_EXTENSO`
  (economia = duração × mensal − preço do pacote); `{{TOTAL_TRES_MENSAIS}}`,
  `{{TOTAL_SEIS_MENSAIS}}` e seus `_EXTENSO` (duração × mensal).
- **Do combinado:** `{{PLANO}}`, `{{VALOR}}`, `{{VALOR_EXTENSO}}`, `{{PAGAMENTO}}`,
  `{{DATA_INICIO}}`, `{{DATA_FIM}}`, `{{DATA_HOJE_EXTENSO}}`.

Os calculados saem sozinhos: todo extenso sai do número, a data de término sai do início +
duração, a data de hoje sai do relógio, os preços de tabela e as economias saem dos
pacotes configurados, e o `{{PAGAMENTO}}` (cláusula 7.5) monta a frase inteira — *"em 3
(três) parcelas de R$ 250,00 (duzentos e cinquenta reais), via cartão de crédito, vencendo
a primeira em 05/09/2026"* — com a parcela calculada do total, nunca digitada.

## O que ajustar antes de usar

**1. Os preços NÃO se trocam no Word — eles saem da configuração.** Desde 04/08/2026 a
Cláusula 8ª, a tabela de opções e a base da multa da 16.1 usam marcadores
(`{{PRECO_MENSAL}}`, `{{PRECO_TRIMESTRAL}}`, `{{PRECO_SEMESTRAL}}`, as economias e os
totais de comparação). Os valores entram na hora de preencher, calculados da lista
`pacotes` que você informou na instalação — o preço mora **num lugar só**, e é por isso que
o contrato não consegue mais sair com dois valores diferentes na mesma página. Mudou de
preço? `configurar.py --dados` com a lista nova, e o próximo contrato já sai certo. A
economia é calculada (duração × mensal − preço do pacote); se a conta não fechar, a skill
recusa preencher e explica.

**1b. O cancelamento cobra 10% do valor restante** (Cláusula 16.3) — o "restante" é o total
contratado menos as consultas já realizadas, e o preço do Mensal (item 16.1, preenchido
com o SEU mensal configurado) é a base desse cálculo: quem cancela perde o desconto do
pacote e paga a consulta feita pelo valor avulso. Vale passar essa cláusula pela sua
advogada: contrato com paciente é relação de consumo, e taxa sobre serviço não prestado é o
tipo de cláusula que se discute.

**2. As testemunhas ficaram em branco de propósito.** O contrato original vinha com as
testemunhas de quem o escreveu. Foram apagadas — se fossem junto, todo mundo mandaria
contrato com o nome de duas pessoas que não conhecem. Preencha à mão ou deixe a plataforma
de assinatura cuidar.

## Nota do rodapé

O contrato traz, no rodapé, um aviso de direitos autorais da advogada que o redigiu. Esse
aviso foi **mantido** — apagar a autoria de quem escreveu seria pior do que preservá-la — e
segue impresso em todo contrato gerado a partir deste modelo.

## De onde veio

Preparado a partir de um contrato de prestação de serviços nutricionais real, com **toda** a
identificação das pessoas removida e conferida por varredura: nenhum CPF, CRN, CEP ou nome
de pessoa sobrou no arquivo — nem no corpo, nem nas tabelas, nem no cabeçalho e rodapé.

Ele é um **ponto de partida**, não um contrato pronto para o seu caso. Vale a leitura de uma
advogada antes do primeiro uso, principalmente da cláusula de cancelamento.
