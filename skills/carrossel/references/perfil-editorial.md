# Perfil editorial e domínios de pesquisa

## Dois conceitos que não podem ser misturados

- **`perfil_editorial`** = para qual Instagram e público o post será escrito. Valores: `saude` ou
  `ia`. Só o Cassiano decide.
- **`dominios_pesquisa`** = áreas em que os fatos precisam ser buscados. Valores possíveis:
  `["saude"]`, `["ia"]` ou `["saude", "ia"]`. A skill detecta; o Cassiano pode corrigir.

O perfil orienta o texto. Os domínios orientam as fontes. Escolher um perfil NUNCA apaga um domínio
factual relevante.

## Gate antes da pesquisa aprofundada

Depois da captura e da leitura inicial do material, mas antes da pesquisa aprofundada:

1. Detectar os domínios presentes e mostrar a leitura em uma linha.
2. Considerar o perfil informado SOMENTE quando o Cassiano o escolheu de forma inequívoca para este
   post na conversa atual ou quando `estado.json` já guarda uma escolha explícita dele. Tema, domínio,
   copy antiga, fala de mentor e mera menção a um Instagram não contam como escolha.
3. Sem uma dessas duas provas, pedir que ele escolha o perfil editorial. Não inferir pelo
   assunto, mesmo quando o post parece pertencer claramente a saúde ou IA. Se ele disser “os dois”,
   perguntar qual é o perfil principal deste post; não persistir `ambos`. Se o formato também
   estiver em aberto, perfil e formato vão **numa pergunta só**, no começo (decisão do Cassiano,
   04/09/2026); se o material já responder um dos dois, confirme no resumo e pergunte só o outro.
4. Se o Cassiano corrigir os domínios detectados, a correção dele vence. Persistir os dois campos no
   `estado.json` antes de iniciar a pesquisa.

Exemplo híbrido:

> Detectei um tema de IA com implicações de saúde. Pesquisa necessária: IA + saúde. Qual perfil
> editorial você quer usar?

Uma leitura superficial para classificar os domínios é permitida; busca aprofundada e escrita
esperam perfil e formato.

Posts antigos sem esses campos não são reescritos em massa. Na retomada, a ausência de
`perfil_editorial` exige a pergunta; não reconstruir a escolha a partir do histórico.

## O que o perfil muda

O perfil muda público pressuposto, vocabulário, exemplos, contexto, promessa e CTA. Não muda a voz do
Cassiano, pontuação, formatos, limites, validador ou travas factuais.

- **Perfil saúde:** explica a tecnologia pelo impacto para pacientes e profissionais de saúde.
- **Perfil IA:** explica o caso pelo funcionamento, uso, limites e responsabilidade da IA.
- **Tema híbrido:** mantém evidências dos dois lados. O domínio secundário pode sustentar, limitar,
  contradizer ou invalidar o argumento. Se invalidar o ângulo escolhido, parar antes da copy, mostrar o
  conflito ao Cassiano e esperar uma nova direção; nunca forçar a evidência a caber na tese.

## Pesquisa por domínio

Depois de persistir `dominios_pesquisa`, carregue somente:

- `saude`: [pesquisa-saude.md](pesquisa-saude.md);
- `ia`: [pesquisa-ia.md](pesquisa-ia.md);
- ambos: as duas referências, mantendo as evidências separadas.

Não carregue a rota de nutrição/saúde num post exclusivamente de IA, nem a rota de IA num post
exclusivamente de saúde.
