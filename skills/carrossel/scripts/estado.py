#!/usr/bin/env python3
"""Estado determinístico do pipeline de carrossel."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class EstadoInvalido(RuntimeError):
    pass


ORIGENS_COPY = {"skill", "cassiano_rascunho", "cassiano_final"}

DEFAULTS = {
    "schema_version": 5,
    "tema": "",
    "modo_autoria": "gerar",
    "perfil_editorial": "",
    "dominios_pesquisa": [],
    "formato": "",
    "fase": "captura",
    "fase_detalhe": "",
    "eixo_confirmado": False,
    "copy_versao": 0,
    "copy_hash": "",
    "estrutura_hash": "",
    "estrutura_aprovada_hash": None,
    "copy_origem": None,
    "revisor_dispensa_motivo": None,
    "trechos_bloqueados": [],
    "voz_ancora": [],
    "revisor_modelo": "gpt-6-sol",
    "revisor_effort": "high",
    "revisor_rodadas": 0,
    "copy_aprovada_versao": None,
    "copy_aprovada_hash": None,
    "envio_autorizado_hash": None,
    "envio_autorizacao_consumida_em": None,
    "msg_grupo_id": None,
    "enviado_grupo_em": None,
    "feedback_processado_ids": [],
    "midias_mentores": [],
    "instagram_referencias": [],
    "parecer_cassiano": None,
    "canva_original_id": None,
    "template_copia_id": None,
    "canva_lote_autorizado_hash": None,
    "canva_commit_em": None,
    "links_fontes": [],
    "notion_page_url": None,
    "notion_editado_em": None,
}


def criar_estado(tema: str = "") -> dict:
    novo = copy.deepcopy(DEFAULTS)
    novo["tema"] = tema
    return novo


# schema 4 → 5: o revisor deixou de ser o Fable (chaves fable_*) e passou a ser o GPT.
# Os valores antigos migram para as chaves novas; o histórico de quem revisou fica.
CHAVES_ANTIGAS = {
    "fable_dispensa_motivo": "revisor_dispensa_motivo",
    "fable_modelo": "revisor_modelo",
    "fable_effort": "revisor_effort",
    "fable_rodadas": "revisor_rodadas",
}


def carregar_estado(caminho: str | Path) -> dict:
    recebido = json.loads(Path(caminho).read_text(encoding="utf-8"))
    if not isinstance(recebido, dict):
        raise EstadoInvalido("estado.json precisa conter um objeto JSON")
    for antiga, nova in CHAVES_ANTIGAS.items():
        if antiga in recebido:
            valor = recebido.pop(antiga)
            recebido.setdefault(nova, valor)
    migrado = criar_estado(str(recebido.get("tema", "")))
    migrado.update(recebido)
    migrado["schema_version"] = 5
    return migrado


def salvar_estado(caminho: str | Path, atual: dict) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = destino.with_name(destino.name + ".tmp")
    temporario.write_text(
        json.dumps(atual, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporario.replace(destino)


def hash_copy(conteudo: str) -> str:
    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()


def registrar_estrutura(atual: dict, conteudo: str) -> dict:
    """Registra o mapa card a card. Um mapa novo invalida a aprovação do anterior."""
    novo = copy.deepcopy(atual)
    novo["schema_version"] = 5
    novo["estrutura_hash"] = hash_copy(conteudo)
    novo["estrutura_aprovada_hash"] = None
    return novo


def aprovar_estrutura(atual: dict, estrutura_hash: str) -> None:
    if not estrutura_hash or estrutura_hash != atual.get("estrutura_hash"):
        raise EstadoInvalido("a aprovação não corresponde à estrutura corrente")
    atual["estrutura_aprovada_hash"] = estrutura_hash


def registrar_copy(
    atual: dict, conteudo: str, *, origem: str = "skill", voz_ancora: list | None = None
) -> dict:
    """Registra uma copy nova.

    origem="skill": a skill escreveu; exige mapa aprovado (estrutura_aprovada_hash == estrutura_hash).
    origem="cassiano_rascunho": texto recebido para auditar ou incrementar; sem mapa, sem aprovação.
    origem="cassiano_final": use registrar_copy_final_cassiano().
    voz_ancora: posts reais do Cassiano usados como âncora de voz ao escrever (informativo,
    rastreabilidade — não altera a copy).
    """
    if origem not in ORIGENS_COPY:
        raise EstadoInvalido("origem de copy inválida")
    if origem == "skill" and (
        not atual.get("estrutura_hash")
        or atual.get("estrutura_aprovada_hash") != atual.get("estrutura_hash")
    ):
        raise EstadoInvalido("a copy da skill exige estrutura aprovada")

    novo = copy.deepcopy(atual)
    novo["schema_version"] = 5
    novo["copy_origem"] = origem
    novo["voz_ancora"] = list(voz_ancora) if voz_ancora else []
    novo["revisor_dispensa_motivo"] = None
    novo["copy_versao"] = int(novo.get("copy_versao", 0)) + 1
    novo["copy_hash"] = hash_copy(conteudo)
    novo["copy_aprovada_versao"] = None
    novo["copy_aprovada_hash"] = None
    novo["envio_autorizado_hash"] = None
    novo["envio_autorizacao_consumida_em"] = None
    novo["revisor_rodadas"] = 0
    novo["template_copia_id"] = None
    novo["canva_lote_autorizado_hash"] = None
    novo["canva_commit_em"] = None
    return novo


def registrar_copy_final_cassiano(atual: dict, conteudo: str) -> dict:
    """Versão declarada final pelo Cassiano: preservada, já aprovada, sem revisor automático."""
    novo = registrar_copy(atual, conteudo, origem="cassiano_final")
    novo["copy_aprovada_versao"] = novo["copy_versao"]
    novo["copy_aprovada_hash"] = novo["copy_hash"]
    novo["revisor_dispensa_motivo"] = "versao_final_fornecida_por_cassiano"
    novo["fase"] = "decisao_final"
    novo["fase_detalhe"] = "versao_final_fornecida_por_cassiano"
    return novo


def autorizar_envio(atual: dict, copy_hash: str) -> None:
    if not copy_hash or copy_hash != atual.get("copy_hash"):
        raise EstadoInvalido("a autorização não corresponde à copy corrente")
    atual["envio_autorizado_hash"] = copy_hash
    atual["envio_autorizacao_consumida_em"] = None


def consumir_autorizacao(atual: dict, copy_hash: str, momento: str | None = None) -> None:
    if atual.get("envio_autorizado_hash") != copy_hash:
        raise EstadoInvalido("não há autorização para este hash")
    if atual.get("envio_autorizacao_consumida_em"):
        raise EstadoInvalido("a autorização já foi consumida")
    if copy_hash != atual.get("copy_hash"):
        raise EstadoInvalido("a copy mudou depois da autorização")
    atual["envio_autorizacao_consumida_em"] = momento or datetime.now(
        timezone.utc
    ).isoformat()


def registrar_rodada_revisor(
    atual: dict, *, modelo: str = "gpt-6-sol", effort: str = "high"
) -> None:
    rodadas = int(atual.get("revisor_rodadas", 0))
    if rodadas >= 2:
        raise EstadoInvalido("limite de 2 rodadas do revisor atingido para esta versão")
    atual["revisor_modelo"] = modelo
    atual["revisor_effort"] = effort
    atual["revisor_rodadas"] = rodadas + 1
