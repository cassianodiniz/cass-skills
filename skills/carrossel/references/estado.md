# Estado e invariantes

Use `posts/<slug>/estado.json` com `schema_version: 5`.

## Campos

```json
{
  "schema_version": 5,
  "tema": "",
  "modo_autoria": "gerar",
  "perfil_editorial": "",
  "dominios_pesquisa": [],
  "formato": "",
  "fase": "captura",
  "fase_detalhe": "",
  "eixo_confirmado": false,
  "copy_versao": 0,
  "copy_hash": "",
  "estrutura_hash": "",
  "estrutura_aprovada_hash": null,
  "copy_origem": null,
  "revisor_dispensa_motivo": null,
  "trechos_bloqueados": [],
  "voz_ancora": [],
  "revisor_modelo": "gpt-6-sol",
  "revisor_effort": "high",
  "revisor_rodadas": 0,
  "copy_aprovada_versao": null,
  "copy_aprovada_hash": null,
  "envio_autorizado_hash": null,
  "envio_autorizacao_consumida_em": null,
  "msg_grupo_id": null,
  "enviado_grupo_em": null,
  "feedback_processado_ids": [],
  "midias_mentores": [],
  "instagram_referencias": [],
  "parecer_cassiano": null,
  "canva_original_id": null,
  "template_copia_id": null,
  "canva_lote_autorizado_hash": null,
  "canva_commit_em": null,
  "links_fontes": [],
  "notion_page_url": null,
  "notion_editado_em": null
}
```

## Invariantes

- `copy_hash` é SHA-256 do conteúdo exato de `copy.md`; `estrutura_hash` é SHA-256 do conteúdo exato de `estrutura.md` (o mapa card a card).
- Copy escrita pela skill (`copy_origem: skill`) exige `estrutura_aprovada_hash == estrutura_hash`. Um mapa novo zera a aprovação.
- Copy recebida do Cassiano para auditar ou incrementar usa `copy_origem: cassiano_rascunho`: não exige mapa e não nasce aprovada.
- Copy declarada final pelo Cassiano usa `copy_origem: cassiano_final`, já nasce aprovada e registra `revisor_dispensa_motivo`. O revisor não roda automaticamente nela.
- Defaults de migração nunca presumem estrutura aprovada nem versão final: estado antigo retomado exige mapa antes de nova copy da skill.
- Alterar a copy incrementa `copy_versao`, recalcula o hash e invalida aprovação, autorização de envio e autorização do lote Canva anteriores.
- Uma autorização de WhatsApp vale para um hash e é consumida no primeiro intento, inclusive se houver timeout.
- `revisor_rodadas` nunca passa de 2 para a mesma versão. A revisão usa `gpt-6-sol` (high, via Codex); se ele falhar, a revisão vai para um subagente do modelo da sessão (registrado com `--registrar-subagente`, `revisor_effort: sessao`) — isso conta como uma rodada, e `revisor_modelo` guarda quem entregou.
- Estado antigo com chaves `fable_*` (schema 4) migra sozinho ao carregar: os valores passam para as chaves `revisor_*`.
- `voz_ancora` lista os posts reais usados como âncora de voz ao escrever. É informativo (rastreabilidade); não altera a copy.
- Cada resposta de mentor entra uma vez por `message_id`.
- Mídia registra origem, `message_id`, tipo, URL disponível, caminho local e estado de download.
- Persista o estado antes de chamar WhatsApp, Instagram ou Canva.
- `notion_page_url` liga o post à página do banco Posts Carrossel; `notion_editado_em` é o horário da última edição da página visto pela skill. Divergência significa que alguém mexeu na página: releia antes de gravar (ver `notion.md`).

## Legado

Migre campos conhecidos somente quando o post for retomado. Campos ausentes recebem defaults seguros: nenhuma aprovação, nenhuma autorização e nenhum efeito externo presumido.
