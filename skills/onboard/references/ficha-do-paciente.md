# A Ficha do Paciente — como montar

> Parte da skill `onboard`. Aberto sob demanda pelo `SKILL.md`.

A Ficha do Paciente é o documento de trabalho da nutricionista: as respostas cruas do
formulário de anamnese da paciente, reorganizadas num padrão fixo que ela lê antes da
consulta. **Quem monta é você** — isto é trabalho de leitura e julgamento (calcular idade,
decidir o que destacar, excluir o que não foi respondido), não de script.

**A pasta da paciente já nasce com a ficha EM BRANCO** (`Ficha do Paciente -
<nome>.html`, copiada de `assets/` pelo `novo_paciente.py` — só o layout). Quando as
respostas da anamnese chegarem, é ESSE arquivo que você preenche, mantendo o nome. Se a
ficha já tiver conteúdo (não estiver em branco), pergunte antes de sobrescrever (trava 3).

## Regra que está acima de todas

**100% fiel ao que a paciente informou.** Você reorganiza, padroniza e destaca — você
NUNCA inventa, deduz ou completa dado clínico. Categoria sem nenhuma resposta **sai do
documento** (não fica título vazio). Informação confusa que você não conseguiu encaixar
com certeza: pergunte antes, ou registre com a dúvida explícita — nunca "arrume" por
conta própria. Inventar sintoma, dose ou histórico numa ficha clínica é o equivalente
aqui do CPF inventado no contrato.

## Estrutura (siga o gabarito no fim — em conflito de formato, o gabarito manda)

**Cabeçalho** — linhas soltas:
- `FICHA DO PACIENTE` (título)
- **Nome:** EM MAIÚSCULAS E NEGRITO
- **Idade:** calcule da data de nascimento (confira a conta duas vezes; na dúvida,
  escreva também a data de nascimento entre parênteses)
- **Profissão:** como informado
- **Interesse em uso de medicação:** transcreva a resposta
- **Relata que:** a atividade física em frase padrão — tipo, frequência e duração +
  tempo de prática. Ex.: "Musculação 3x/semana, cerca de 1h. Há 6 a 12 meses"

**Objetivo, Impedimento, O que espera da equipe** — três linhas com títulos fixos:
`Objetivo:` / `Impedimento:` / `O que espera da equipe:` — transcrever.

**Dados de Saúde e Preferências** — um parágrafo corrido por subtópico (sem lista):
- **Sono:** horário de dormir e acordar, se acorda à noite, recurso pra dormir, qualidade.
  **Negrito** se dorme menos de 7h30 ou mais de 8h30, ou se relata que quer melhorar.
- **Hidratação e urina:** quantidade de água e cor/tipo da urina. **Negrito** se consome
  menos de 2L ou se a urina for tipo 4 ou superior.
- **Intestino:** evacua diariamente?, tipo das fezes (1 a 7), sintomas ligados
  (constipação, diarreia, desconforto, alimentos que influenciam). **Negrito** se não
  evacua todos os dias ou se as fezes forem fora do tipo 3 ou 4.
- **Estimulantes:** café, chimarrão, energético, chá etc. — frequência e quantidade.

**Histórico de saúde** — lista com marcadores (é lista, como no gabarito): doenças,
medicamentos com dose, cirurgias, tratamento psicológico/psiquiátrico. Explicação de
condição/medicação/cirurgia entre parênteses, quando houver.
- **Exames:** se houver, aqui — nome do exame, valor e referência; **negrito** no
  marcador fora do valor de referência.

**Histórico familiar** — lista com marcadores, por parentesco (pai, mãe, irmão, avós,
tios, primos), cada um com as condições informadas.

**Sintomas** — parágrafo corrido: dores, tontura, TPM, insônia, alterações menstruais,
libido (destaque **libido baixa** em negrito se mencionado), energia, humor.

**Consumo de álcool** — frequência e tipo. Ex.: "1x/mês, 2 latas de cerveja".

**Outros pontos** — o que ela mencionou e não coube acima, mesmo que pareça irrelevante.

**Refeições Habitualmente Consumidas** — lista com marcadores, uma por refeição:
`Café da manhã:` / `Almoço:` / `Lanche da tarde:` / `Jantar:` — descrever como informado.
Depois, linhas soltas: `Lanches extras:` (se houver) / `Alimentos que menos gosta:` /
`Alimentos favoritos:` / alimentos que causam constipação, desconforto, azia etc. /
com quem mora, quem cozinha, onde come e o tempo que demora pra comer.

## Gabarito (paciente FICTÍCIA — siga este formato à risca)

> **FICHA DO PACIENTE**
> **Nome: CARLA MARTINS DE MELO**
> Idade: 41 anos
> Profissão: Biomédica, atualmente trabalha com estética
> Interesse em uso de medicação: Sim, se for necessário
> Relata que: Musculação e caminhada/HIIT, 4 a 6 vezes/semana, cerca de 1h45 por dia
> (musculação de manhã, caminhada à tarde/noite). Pratica há 1 a 2 anos.
>
> **Objetivo, Impedimento, O que espera da equipe**
> Objetivo: Emagrecer e cuidar da saúde
> Impedimento: Falta de acompanhamento nutricional e organização da rotina
> O que espera da equipe: Auxílio com plano alimentar, estratégias alimentares e ajuda
> para manter níveis de marcadores inflamatórios baixos
>
> **Dados de Saúde e Preferências**
> **Sono:** Dorme rápido (5 a 10 minutos) com uso de melatonina. Costuma dormir por volta
> de 22h30/23h e acordar 6h/7h. Relata que poderia dormir mais cedo para melhorar a
> qualidade. **Deseja melhorar o sono.**
> **Hidratação e urina:** Ingesta de 2 a 3 litros de água por dia. Urina tipo 3.
> **Intestino:** Evacua diariamente, fezes tipo 4. Relata que farináceos causam
> constipação e inchaço, além de azia.
> **Estimulantes:** Café pela manhã, uma caneca.
>
> **Histórico de saúde:**
> - Ansiedade generalizada
> - Síndrome do pânico
> - TDAH
> - Enxaqueca
> - Tontura em exercícios intensos ou movimentos bruscos da cabeça
> - Medicamentos: Escitalopram (transtorno de pânico), Metformina (indicado por
>   neurologista)
> - Cirurgias: retirada de amígdalas, cesárea, mastopexia e abdominoplastia
> - Tratamento psicológico/psiquiátrico: sim, para ansiedade, pânico e atualmente TDAH
>
> **Histórico familiar:**
> - Pai: diabetes tipo 2, duas pontes de safena, hipertensão, colesterol alto, Leucemia
>   Mieloide Crônica
> - Mãe: Alzheimer, ansiedade e pânico, TDAH, hipertensão, hipercolesterolemia familiar
> - Irmão: TDAH
> (…um marcador por parente, como veio…)
>
> **Sintomas:** Enxaqueca, tontura em situações específicas (agachamentos rápidos,
> exercícios muito intensos, movimentos bruscos da cabeça). Energia baixa durante o dia,
> mais disposição à noite. **Libido baixa.** Alterações de humor em alguns períodos do mês
> e desejo por doces. Sensação de inchaço e falta de energia em determinados momentos do
> ciclo, mesmo sem menstruar.
> **Consumo de álcool:** Raramente, nos últimos meses não consumiu nada.
> **Outros pontos:** Não se expõe ao sol. Não fuma.
>
> **Refeições Habitualmente Consumidas**
> - Café da manhã: Café com whey, canela e adoçante (Agave). Pão integral ou "Ezequiel
>   bread" com requeijão ou pasta de amendoim. Uma fruta (kiwi, uva ou morango). Às
>   vezes, ovos.
> - Almoço: Salada variada (…como informado…). Sobremesa: frutas ou doce de leite sem
>   açúcar.
> - Lanche da tarde: Iogurte grego desnatado com frutas vermelhas ou iogurte de coco com
>   granola. Às vezes biscoito integral ou ovo.
> - Jantar: Por volta das 19h/20h, batida de kefir com morango e blueberry (pode
>   adicionar whey se proteína for insuficiente).
> Lanches extras: Não citados.
> Alimentos que menos gosta: Alguns vegetais (falta de tempo para preparo), algumas
> frutas (banana, manga, mamão – não gosta do sabor nos EUA).

## Antes de entregar

1. Releia a ficha CONTRA as respostas cruas: cada afirmação da ficha tem que existir no
   que ela informou. O que você não achar na fonte, tire.
2. Confira a idade contra a data de nascimento.
3. Confira que toda regra de negrito aplicada tem o gatilho dela na fonte (ex.: negrito
   no sono exige o horário que prova menos de 7h30 — não "impressão de dormir pouco").
4. Mostre a ficha pra nutricionista conferir antes de dar por pronta — mesma regra do
   contrato (trava 2).
