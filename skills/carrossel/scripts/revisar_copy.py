#!/usr/bin/env python3
"""Prepara revisão (modo revisar) ou auditoria (modo auditar) por um subagente da sessão.

O revisor é sempre um subagente do próprio modelo que roda a sessão (sem escolher modelo).
O script grava o pedido pronto em `<saida>.prompt.md` e sai com código 2: quem roda a skill
entrega esse pedido a um subagente e registra a resposta com `--registrar-subagente`,
que aplica as travas (hash da copy, 2 rodadas, versão final).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import estado


class RevisaoErro(RuntimeError):
    pass


class UsarSubagente(RevisaoErro):
    """O pedido ficou gravado para um subagente do modelo da sessão."""

    def __init__(self, motivo: str, prompt_path: Path):
        super().__init__(motivo)
        self.prompt_path = prompt_path


MODELO_SESSAO = "sessao"
CODIGO_USAR_SUBAGENTE = 2

SCHEMAS = {
    "revisar": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["revisado", "aprovado"]},
            "copy_revisada": {"type": "string"},
            "resumo_alteracoes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["status", "copy_revisada", "resumo_alteracoes"],
        "additionalProperties": False,
    },
    "auditar": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["sem_achados", "achados"]},
            "achados": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["status", "achados"],
        "additionalProperties": False,
    },
}


def _ler(caminho: str | Path) -> str:
    return Path(caminho).read_text(encoding="utf-8")


def _ler_eixo(caminho: str | Path, modo: str) -> str:
    """Em auditoria de copy recebida pode não existir mapa; revisar continua exigindo o arquivo."""
    caminho = Path(caminho)
    if caminho.exists():
        return _ler(caminho)
    if modo == "auditar":
        return "(eixo não declarado: copy recebida para auditoria, sem mapa card a card)"
    raise FileNotFoundError(f"eixo/estrutura não encontrado: {caminho}")


def _validar(candidato, modo: str) -> dict:
    if not isinstance(candidato, dict):
        raise RevisaoErro("revisor não devolveu a estrutura de revisão")
    if modo == "revisar":
        if not isinstance(candidato.get("copy_revisada"), str) or not candidato["copy_revisada"].strip():
            raise RevisaoErro("revisor devolveu copy vazia")
        if not isinstance(candidato.get("resumo_alteracoes"), list):
            raise RevisaoErro("revisor devolveu resumo inválido")
        if candidato.get("status") not in {"revisado", "aprovado"}:
            raise RevisaoErro("revisor devolveu status inválido")
    else:
        if not isinstance(candidato.get("achados"), list):
            raise RevisaoErro("revisor devolveu achados inválidos")
        if candidato.get("status") not in {"sem_achados", "achados"}:
            raise RevisaoErro("revisor devolveu status de auditoria inválido")
    return candidato


def _extrair_json(texto: str, modo: str) -> dict:
    """A resposta do subagente é o próprio JSON (cercas ```json são toleradas)."""
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.split("\n", 1)[1] if "\n" in texto else ""
        texto = texto.rsplit("```", 1)[0]
    try:
        return _validar(json.loads(texto), modo)
    except json.JSONDecodeError as exc:
        raise RevisaoErro("revisor devolveu JSON inválido") from exc


def _salvar_json(caminho: str | Path, conteudo: dict) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = destino.with_name(destino.name + ".tmp")
    temporario.write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporario.replace(destino)


def _checar_travas(copy_path, estado_path, modo: str, permitir_auditoria_final: bool):
    if modo not in SCHEMAS:
        raise RevisaoErro("modo inválido; use revisar ou auditar")
    copy_texto = _ler(copy_path)
    atual = estado.carregar_estado(estado_path)
    if atual.get("copy_hash") != estado.hash_copy(copy_texto):
        raise estado.EstadoInvalido("copy.md diverge do hash registrado")
    if atual.get("copy_origem") == "cassiano_final":
        if modo == "revisar":
            raise estado.EstadoInvalido("versão final do Cassiano não passa pelo revisor")
        if not permitir_auditoria_final:
            raise estado.EstadoInvalido("auditoria de versão final exige pedido separado do Cassiano")
    if int(atual.get("revisor_rodadas", 0)) >= 2:
        raise estado.EstadoInvalido("limite de 2 rodadas do revisor atingido para esta versão")
    return copy_texto, atual


def _concluir(atual: dict, estado_path, saida_path, resultado: dict, modelo: str, effort: str, detalhe: str) -> dict:
    _salvar_json(saida_path, resultado)
    estado.registrar_rodada_revisor(atual, modelo=modelo, effort=effort)
    atual["fase_detalhe"] = detalhe
    estado.salvar_estado(estado_path, atual)
    return resultado


def revisar(
    copy_path: str | Path,
    fatos_path: str | Path,
    eixo_path: str | Path,
    regras_path: str | Path,
    estado_path: str | Path,
    saida_path: str | Path,
    *,
    modo: str = "revisar",
    permitir_auditoria_final: bool = False,
) -> dict:
    """modo="revisar": o revisor limpa e devolve a copy inteira (só copy escrita pela skill).
    modo="auditar": o revisor devolve achados, nunca reescreve; só por pedido explícito do Cassiano.
    Copy com copy_origem == "cassiano_final" nunca passa por revisar; auditar exige
    permitir_auditoria_final=True, que representa um pedido separado e inequívoco do Cassiano.
    """
    copy_texto, atual = _checar_travas(copy_path, estado_path, modo, permitir_auditoria_final)

    if modo == "revisar":
        instrucao = """Limpe clareza, ritmo, redundância e adequação ao formato sem alterar tese,
fatos, fontes, números ou trechos bloqueados. Não invente conteúdo. Devolva a copy
completa, não somente um diff."""
    else:
        instrucao = """Audite a copy e devolva somente achados localizados por card. Não reescreva
a copy, não ofereça versão substituta e não altere tese, fatos, fontes, números ou trechos
bloqueados. Se não houver achado, devolva status sem_achados e lista vazia. Instrução literal:
não reescreva."""

    prompt = f"""Você é o revisor de uma copy de Instagram. Trabalhe só com o material abaixo:
não abra arquivos nem rode comandos.

{instrucao}

EIXO:
{_ler_eixo(eixo_path, modo)}

FATOS:
{_ler(fatos_path)}

REGRAS:
{_ler(regras_path)}

COPY:
{copy_texto}
"""
    atual["fase"] = "revisao"
    atual["fase_detalhe"] = "revisor_em_execucao"
    estado.salvar_estado(estado_path, atual)

    # O revisor é um subagente do modelo da sessão: o pedido fica gravado e nada conta
    # como rodada até a resposta ser registrada (ver registrar_subagente).
    prompt_path = Path(str(saida_path) + ".prompt.md")
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(
        prompt
        + "\nResponda SOMENTE com um objeto JSON (sem texto antes ou depois) que siga este schema:\n"
        + json.dumps(SCHEMAS[modo], ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    atual["fase_detalhe"] = "aguardando_subagente"
    estado.salvar_estado(estado_path, atual)
    raise UsarSubagente("revisão preparada para o subagente da sessão", prompt_path)


def registrar_subagente(
    copy_path: str | Path,
    estado_path: str | Path,
    saida_path: str | Path,
    resposta_path: str | Path,
    modelo: str | None = None,
    *,
    modo: str = "revisar",
    permitir_auditoria_final: bool = False,
) -> dict:
    """Registra a resposta do subagente (modelo da sessão) aplicando as travas."""
    modelo = (modelo or "").strip() or MODELO_SESSAO
    _, atual = _checar_travas(copy_path, estado_path, modo, permitir_auditoria_final)
    resultado = _extrair_json(_ler(resposta_path), modo)
    return _concluir(atual, estado_path, saida_path, resultado, modelo, "sessao", "subagente_concluido")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy", required=True)
    parser.add_argument("--fatos", required=True)
    parser.add_argument("--eixo", required=True)
    parser.add_argument("--regras", required=True)
    parser.add_argument("--estado", required=True)
    parser.add_argument("--saida", required=True)
    parser.add_argument("--modo", choices=sorted(SCHEMAS), default="revisar")
    parser.add_argument(
        "--permitir-auditoria-final",
        action="store_true",
        help="só com pedido separado e inequívoco do Cassiano para auditar uma versão final dele",
    )
    parser.add_argument(
        "--registrar-subagente",
        metavar="RESPOSTA_JSON",
        help="registra a resposta do subagente do modelo da sessão",
    )
    parser.add_argument("--modelo-subagente", help="opcional: nome do modelo da sessão, só para registro")
    args = parser.parse_args()
    try:
        if args.registrar_subagente:
            registrar_subagente(
                args.copy, args.estado, args.saida, args.registrar_subagente, args.modelo_subagente,
                modo=args.modo, permitir_auditoria_final=args.permitir_auditoria_final,
            )
            print(args.saida)
            return 0
        revisar(
            args.copy,
            args.fatos,
            args.eixo,
            args.regras,
            args.estado,
            args.saida,
            modo=args.modo,
            permitir_auditoria_final=args.permitir_auditoria_final,
        )
    except UsarSubagente as exc:
        print(
            f"{exc}\nUSAR_SUBAGENTE: entregue {exc.prompt_path} a um subagente do modelo da sessão "
            "e registre a resposta com --registrar-subagente.",
            file=sys.stderr,
        )
        return CODIGO_USAR_SUBAGENTE
    except (OSError, estado.EstadoInvalido, RevisaoErro) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(args.saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
