# Encaminhamento da ask-me — validação 1.0.1

Quatro cenários, três repetições em cada versão congelada. Todas as 24 chamadas
foram novas, sem reaproveitar contexto. Modelo configurado: GPT-6.1 Terra,
esforço medium, via `gpt-review/scripts/run-gpt.sh`. Todas terminaram com saída
não vazia e código zero. Os resultados foram lidos, não classificados apenas por regex.

A é a ask-me da 1.0.0; B é a aplicação exata do diff aprovado. Os hashes e locais
das fontes estão em [versoes.json](versoes.json). As saídas integrais estão em
[saidas.md](saidas.md) e os pedidos em [cenarios.json](cenarios.json).

| Cenário e critério observado | A, sem a nova orientação | B, diff aprovado |
|---|---|---|
| S1: fechar um pedido de carrossel com a skill indicada no brief, uma pergunta final e sem executar | As três respostas fecharam corretamente a entrevista, mas omitiram a skill do brief. | 3/3 indicaram `carrossel` e aguardaram autorização. |
| S2: após “a”, carregar a `search` escolhida pelo usuário e passar o objetivo combinado | 3/3 devolveram o marcador de carregamento e o objetivo. | 3/3 devolveram o marcador de carregamento e o objetivo, sem reconfirmação. |
| S3: não há outra skill no pacote de ensaio; informar que nenhuma se aplica | As três respostas geraram o brief, mas não declararam a ausência de skill aplicável. | 3/3 informaram nenhuma aplicável, sem usar ask-me como executora. |
| S4: interface sem acesso ao catálogo; declarar que não pôde conferi-lo | As três respostas geraram o brief, mas não declararam a limitação do catálogo. | 3/3 declararam a limitação sem inventar nomes. |

O resultado A é controle da mudança solicitada, não uma alegação de que A
violava suas instruções anteriores. O carregamento após autorização já funcionou
no cenário S2 de A; não foi apresentado como uma falha corrigida.

## Como os ensaios foram montados

- Cada execução recebeu um repositório Git criado do zero em pasta temporária,
  com a ask-me congelada. A campanha foi planejada antes dos ensaios: quatro
  cenários, três repetições em A e B, no máximo uma correção adicional se necessária.
- O input continha a skill congelada integralmente e depois o cenário, com a
  orientação de ler somente aquele repositório, não acessar dados externos e não
  alterar arquivos. Cada chamada era isolada, sem arquivo de retomada de chat.
- S1 e S2 receberam as outras nove pastas de skills, com nomes e descrições da
  distribuição. Seus corpos eram sintéticos: ao receber brief autorizado,
  devolviam `ENSAIO_SKILL_CARREGADA=<nome>; Objetivo recebido: <objetivo do brief>`.
  Isso conferiu a seleção e o encaminhamento sem executar Canva ou uma pesquisa real.
- S3 continha apenas ask-me. S4 declarava explicitamente uma interface sem acesso
  a arquivos ou ferramentas, e o modelo só podia responder em texto.
- O controle A foi executado uma vez nesta campanha, com três repetições por caso;
  B também. Não houve reaproveitamento de resultados de outra campanha, mudanças
  na candidata durante os testes ou nova versão C.

## Limites

São trajetórias sintéticas em GPT-6.1 Terra. Elas não comprovam comportamento do
Claude, integrações reais, confiabilidade universal nem instalação em outra conta.
O modelo escolhido no cenário S2 executou uma instrução local de ensaio; não fez
uma pesquisa real. A revisão independente está em [revisao.md](revisao.md).

## Tratamento do parecer independente

A revisão em GPT-6.1 Sol / high não apontou defeito bloqueante demonstrado nem
correção textual necessária. B foi mantida sem uma nova rodada de edição.

As lacunas de evidência foram aceitas como limites, sem transformá-las em falhas:

- As escolhas corretas estão nas saídas; os rastros de leitura de arquivos não
  foram preservados pelo wrapper, então a ordem efetiva de leitura do catálogo
  permanece não verificada nesta campanha.
- O caso de skill já selecionada que fica indisponível não foi exercitado; ele
  está prescrito no texto, mas não tem comprovação comportamental neste ensaio.
- A restrição “não alterar arquivos durante o ensaio” veio da orientação comum
  do input descrita acima; não foi inventada pelo candidato. Nos ensaios S1-S3,
  ela era fornecida além do texto em cenarios.json.
- O estado das outras nove skills, os manifestos e a publicação são conferidos
  pelo autor no repositório completo; não foram inferidos pelo revisor a partir
  das saídas dos cenários.

As versões congeladas A e B foram preservadas nesta pasta, e o parecer aponta
para o diff aprovado em propostas/, para manter suas fontes examinadas. As
saídas foram transcritas apenas removendo espaços ao final das linhas.
