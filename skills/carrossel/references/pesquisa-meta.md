# Pesquisa editorial no Meta AI

Carregue esta referência somente quando Cassiano pedir explicitamente para procurar posts ou
referências **no Meta** ou **no Instagram**. Não a carregue para um pedido comum de criação, para
ideias genéricas nem para verificação factual do mapa.

Esta rota apenas abre a conversa no Meta AI e entrega o controle ao Cassiano. Ela não é uma segunda
forma de escrever o post.

## Pesquisa

1. Preserve o tema e qualquer filtro dito pelo Cassiano.
2. Gere o prompt sem salvar arquivos:

   ```bash
   python3 scripts/prompt_meta.py "<tema>"
   ```

   Os padrões são carrosséis dos últimos 90 dias, 10 ou mais resultados, conjunto inicial com pelo
   menos 6 em português, prioridade para 20 mil ou mais curtidas e complemento a partir de 10 mil.
   Se Cassiano mudar período ou formato, use `--dias` e `--formato`.
3. Use o MCP `meta-ai-browser`. Verifique `browser_status`; se faltar apenas uma aba do Meta AI,
   abra `https://www.meta.ai/` no Chrome existente e repita. Reutilize a aba em vez de abrir outra.
4. Envie uma única vez o texto gerado com `ask_meta` e `confirm_send: true`. O pedido explícito com
   tema e destino autoriza esse envio; não crie uma confirmação intermediária.
5. Deixe a aba aberta para Cassiano continuar diretamente no Meta. Não resuma, filtre, copie nem
   salve os resultados e não acione a skill `search`.

Se o MCP falhar, reporte o erro real. Não conclua automaticamente que a depuração remota está
desativada: diferencie conexão recusada de ausência da aba `meta.ai`.

## Transcrição escolhida

Somente quando Cassiano escolher uma publicação e pedir a transcrição, gere:

```bash
python3 scripts/prompt_meta.py "<url>" --transcrever
```

Envie esse prompt pelo mesmo MCP. A transcrição é feita pelo Meta AI e contém somente o texto visível
card por card. Não use OCR, download ou transcritor local. Depois, deixe a conversa aberta; o material
só entra no fluxo editorial quando Cassiano o trouxer de volta e pedir para criar ou incrementar o post.

## Limites

- Pesquisa editorial não é pesquisa factual e não valida alegações.
- Métricas declaradas pelo Meta podem aparecer como `não verificado`.
- Nada desta rota cria `posts/<slug>/`, estado, mapa, copy, revisor, Canva ou envio.
- O fluxo canônico de escrita permanece o único responsável pela criação do post.
