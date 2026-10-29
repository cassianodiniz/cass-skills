# Notion: registro compartilhado de ideias e posts

## Sem banco configurado

Use esta rota local e não execute as rotas de banco abaixo. Ideia avulsa:
procure por assunto em `posts-instagram/ideias/`, crie `<slug>.md` com status
`Ideia` e a fala literal; não desenvolva o post. Para listar/retomar ideias,
leia esses arquivos. Para um post em trabalho, guarde as três seções abaixo
em `registro.md` na pasta do post; releia antes de sobrescrever e preserve
edições manuais. Registre `Rascunho` localmente antes da primeira prévia Canva; `Pronto` só após aprovação final. O fluxo de banco
abaixo só entra quando o usuário fornecer um banco acessível.


O banco **Posts Carrossel** é onde ideias e posts ficam visíveis para o Cassiano e para a Carine. Cada um tem a sua própria cópia da skill e grava no mesmo banco. Por isso, o que um começa o outro consegue ler e continuar. As pastas locais (`posts/<slug>/`) são o bastidor de quem está escrevendo, e o Notion guarda o que a outra pessoa precisa para continuar.

- Banco, fonte de dados e autor: use somente os que o usuário fornecer e tiver acesso.
- Sem banco configurado, salve as três seções em `registro.md` na pasta do post.

## O que vai para onde

Cada linha do banco é uma página. As colunas são:

| Coluna | Conteúdo |
|---|---|
| TEMA | nome do post ou da ideia |
| CONTEÚDO | prévia curta: a frase do card 1, ou a ideia como foi dita |
| CRIADO POR | quem começou. Quem continua o post não altera este campo |
| DATA | dia da publicação. Fica vazia até a publicação ser confirmada |
| STATUS | `Ideia`, `Rascunho`, `Pra revisar`, `Pronto` ou `Enviado` |

O corpo da página tem exatamente três seções, nesta ordem:

```
# Texto do post
## Card 1
<texto verbatim do card>
## Card 2
...

# Fontes
- <autor ou veículo, ano> — <URL> — <o que essa fonte sustenta no post>

# Onde paramos
<etapa atual> · copy v<N> · <DD/MM/AAAA>
Pendente: <o que falta>
Próximo passo: <a próxima ação concreta>
```

- **Texto do post** é o `copy.md` atual, card por card, sem nenhuma alteração.
- **Fontes** usa links abertos para qualquer pessoa. Caminho de pasta local (`C:\...`, `/Users/...`) não serve como fonte, porque a outra pessoa não consegue abrir.
- O restante fica **somente local**: `estado.json`, `estrutura.md`, `fatos.md` completo, revisões, versões antigas, material e mídias.

`estado.json` guarda `notion_page_url` e `notion_editado_em`, que é o horário da última edição da página visto pela skill.

## Status

| Status | Quando |
|---|---|
| `Ideia` | ideia anotada que ninguém está desenvolvendo |
| `Rascunho` | post em trabalho, incluindo a criação da primeira prévia Canva |
| `Pra revisar` | existe uma versão da copy esperando decisão |
| `Pronto` | o usuário aprovou a versão final do post; criar ou pedir uma prévia no Canva não equivale a essa aprovação |
| `Enviado` | publicação confirmada. Preencha DATA com o dia |

A skill não decide quem pode aprovar. Ela só registra o que foi decidido. Mandar o post aos mentores não muda o status para `Enviado`.

## Quando gravar

Grave sem perguntar. Se a gravação dependesse de alguém lembrar de pedir, a outra pessoa abriria a página e encontraria uma versão velha.

- **Ideia** ("anota essa ideia", "ideia de post"): crie a linha na hora com `STATUS = Ideia`, o TEMA, e a ideia verbatim em CONTEÚDO. Não desenvolva, não pesquise e não crie pasta local. Antes de criar, procure por TEMA parecido: se já existir uma ideia ou um post sobre o mesmo assunto, avise e não crie outra linha.
- **Post**, ao fim de cada etapa:
  1. mapa aprovado: `Rascunho` e Onde paramos;
  2. versão da copy mostrada: `Pra revisar`, Texto do post, Fontes e Onde paramos;
  3. pausa ou fim da conversa: Onde paramos;
  4. primeira prévia Canva: registre `Rascunho` antes da criação e o ID imediatamente após; depois de conferir o design salvo, use `Pra revisar` com o link em Onde paramos. Aprovação final muda para `Pronto`;
  5. publicação confirmada: `Enviado` e DATA.
- **Primeira gravação de um post:** procure antes pelo TEMA, para não duplicar. Se existir uma linha `Ideia` sobre o assunto, use essa mesma linha. Se não existir, crie a página. Depois, guarde o `notion_page_url`.

## Antes de gravar: releia

1. Busque a página (`notion-fetch`).
2. Se o horário da última edição da página for diferente de `notion_editado_em`, alguém mexeu nela depois da última leitura. Mostre o que mudou e pergunte o que fazer. Não sobrescreva. Se `notion_editado_em` estiver vazio (post migrado, primeira leitura), compare o Texto do post com o `copy.md`: se forem iguais, só registre o horário; se diferirem, pergunte.
3. Texto editado à mão no Notion vale como o Cassiano editando `copy.md` à mão: preserve, gere uma nova versão e não mande ao revisor sem pedido explícito.
4. Altere somente as três seções e as colunas. Se a página tiver outras seções, deixe-as como estão.
5. Depois de gravar, atualize `notion_editado_em` com o horário retornado.

## Retomar e continuar post de outra pessoa

Pedidos como "continua o post da Carine sobre X", "meus rascunhos", "o que está pra revisar", "quais ideias temos" ou um link do Notion:

1. Com link, abra a página direto. Sem link, consulte a fonte de dados por TEMA e STATUS, e por CRIADO POR quando for "meus" ou "da Carine". Se houver mais de um candidato, mostre a lista e pergunte qual é.
2. Leia Texto do post, Fontes e Onde paramos. Se a página tiver seções extras, use-as só como contexto.
3. Se não existir pasta local, crie `posts/<slug>/` com:
   - `copy.md` = Texto do post;
   - `fatos.md` = Fontes, cada uma marcada "a conferir";
   - `estado.json`, com `notion_page_url`, `notion_editado_em`, `copy_origem: cassiano_rascunho` (copy recebida: não nasce aprovada e não exige mapa) e a fase deduzida de Onde paramos;
   - se a página tiver um mapa card a card numa seção extra, `estrutura.md` com esse mapa, como contexto e sem aprovação.

   Se a pasta já existir e a página tiver mudado depois da última leitura, o texto da página prevalece e vira uma nova versão.
4. Siga o próximo passo de Onde paramos pelo fluxo normal da skill.

## Se o Notion falhar

Continue o trabalho localmente e avise numa linha que não salvou no Notion. Tente de novo ao fim da próxima etapa, procurando a página antes de criar, para não duplicar. Persista o estado local antes do efeito externo. Se o Notion estiver indisponível, registre a pendência e continue localmente com a prévia, sem declarar gravação no banco. `Pronto` só após aprovação final.
