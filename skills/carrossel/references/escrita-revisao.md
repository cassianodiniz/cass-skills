# Escrita e revisão

Leia este arquivo somente depois de confirmar no estado que `estrutura_aprovada_hash == estrutura_hash`. Se não coincidir, volte para `estrutura-cards.md` e não escreva a copy.

## Referências de escrita

Carregue:

1. `dna-viral-cassiano.md` e `estilo-cassiano.md` (VOZ);
2. a referência do formato escolhido: `dna-noticia.md`, `dna-tela-dividida.md` ou `dna-card-unico.md`;
3. `posicionamento.md` quando o ângulo/postura (contra o quê bater, o que desmistificar) estiver em jogo — é o teto de tema, não regra de escrita;
4. `posts-virais/INDICE.md` e, dele, só os posts escolhidos como âncora de voz (passo 2 abaixo);
5. `psicologia-viral-cassiano.md` e `risco-editorial.md` quando forem relevantes;
6. lições existentes somente do mesmo domínio e formato.

Durante a escrita, não carregue WhatsApp ou Instagram. Concluída a revisão, carregue `canva.md` para montar a prévia em rascunho antes da aprovação final.

## Ordem obrigatória

1. Leia `estrutura.md` e preserve a função e o dado escolhidos para cada card.
2. Âncora de voz: escolha 1 ou 2 posts reais do Cassiano pelo `posts-virais/INDICE.md`, do MESMO formato e de OUTROS temas — a âncora dá a voz, não o assunto (tema distante evita copiar conteúdo). Tenha-os à frente ao escrever, com a instrução: imite tom, ritmo, cadência e persona; nunca copie conteúdo, dado, caso ou frase; o post é só sobre o tema atual, com os fatos da folha. Registre quais foram usados (`voz_ancora`, via `registrar_copy`).
3. Escreva preservando fatos, cabeçalho do mapa e trechos bloqueados.
4. Execute `scripts/validar_cards.py`.
5. Execute `scripts/revisar_copy.py` com copy, fatos, eixo e regras.
6. O GPT devolve a copy completa revisada e um resumo curto das alterações.
7. Execute o validador novamente.
8. Se ainda houver erro corrigível, faça uma única segunda rodada do revisor.
9. Monte a prévia em um novo rascunho conforme `canva.md`, antes da aprovação final, e mostre o link confirmado. Também mostre a versão ao usuário em `posts/<slug>/copy.md`: informe o caminho e abra o arquivo no editor quando o ambiente permitir. Ele pode editar à mão; quando avisar que salvou, releia o arquivo. O que ele alterou é preservado como está — não reescreva nem passe pelo revisor, salvo pedido explícito dele.

```powershell
# revisão (copy escrita pela skill)
python scripts/revisar_copy.py --copy posts/<slug>/copy.md --fatos posts/<slug>/fatos.md --eixo posts/<slug>/estrutura.md --regras references/risco-editorial.md --estado posts/<slug>/estado.json --saida posts/<slug>/revisao.json --modo revisar
# auditoria (só por pedido explícito do Cassiano; devolve achados, não reescreve)
python scripts/revisar_copy.py ... --modo auditar
# auditoria de uma versão final dele: só com pedido separado e inequívoco
python scripts/revisar_copy.py ... --modo auditar --permitir-auditoria-final
```

`--eixo` recebe o `estrutura.md` (o mapa aprovado carrega tese, público e tensão no cabeçalho). Em auditoria de copy recebida sem mapa, aponte `--eixo` para `estrutura.md` mesmo assim: se o arquivo não existir, o script usa o marcador "eixo não declarado" e não falha.

## Versão final do Cassiano

Quando ele declara "esta é a versão final": salve o texto exato em `copy.md`, registre com `registrar_copy_final_cassiano` (nasce aprovada, `copy_origem: cassiano_final`), rode o validador **só como informação** (mostre os alertas, não bloqueie, não altere nada) e siga para a entrega pedida. Não chame o revisor. Não reconstrua mapa. Auditoria dessa versão só com pedido separado dele, e devolve achados.

Regras antivício, limites de cards, contraste e rastreabilidade são determinísticos; não dependem da opinião do revisor.

## Contrato do revisor

- Modelo: `gpt-6-sol`, esforço `high`, chamado pelo Codex CLI (`codex exec`).
- Não existe outro modelo no script. Se o GPT falhar, estourar 10 minutos, devolver saída inválida ou o Codex não estiver instalado, o script sai com código 2, escreve `USAR_SUBAGENTE` e grava o pedido completo em `<saida>.prompt.md` (ex.: `posts/<slug>/revisao.json.prompt.md`). Nada conta como rodada.
- Nesse caso, lance um subagente com a ferramenta Agent **sem trocar o modelo** (herda o modelo da sessão), passando o conteúdo integral desse arquivo como prompt e pedindo que responda só com o JSON. O subagente não recebe esta conversa, só o pedido. Salve a resposta dele em `posts/<slug>/revisao-subagente.json` e registre:
  `python scripts/revisar_copy.py --copy ... --estado ... --saida posts/<slug>/revisao.json --fatos ... --eixo ... --regras ... --modo <o mesmo> --registrar-subagente posts/<slug>/revisao-subagente.json --modelo-subagente <modelo da sessão>`
  O registro passa pelas mesmas travas (hash da copy, 2 rodadas, versão final) e grava em `revisor_modelo` quem entregou. Diga ao Cassiano, numa linha, que o GPT falhou e a revisão foi feita pelo subagente.
- Contexto limpo: sessão descartável (`--ephemeral`), somente leitura, rodando numa pasta temporária vazia; o material inteiro vai no prompt.
- Pode limpar linguagem, ritmo, clareza, redundância e adequação ao formato.
- Não pode mudar tese, fatos, fontes, números ou trechos bloqueados.
- Em modo `auditar`, entrega achados; não reescreve a copy. Só roda por pedido explícito do Cassiano.
- Nunca roda automaticamente em copy com `copy_origem: cassiano_final`.
- Máximo de 2 rodadas por versão.
- Só bloqueia a apresentação se o GPT e o subagente falharem. Nenhum outro modelo entra.
