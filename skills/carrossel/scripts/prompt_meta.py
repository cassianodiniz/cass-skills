#!/usr/bin/env python3
"""Gera os prompts aprovados para pesquisa e transcrição no Meta AI."""

import argparse


def prompt_pesquisa(tema: str, dias: int, formato: str) -> str:
    return f"""Pesquise agora no Instagram {formato} sobre **{tema}** publicados nos últimos {dias} dias.
Traga pelo menos 10 publicações e acrescente outras quando houver achados fortes.
Priorize posts com 20 mil curtidas ou mais. Se não encontrar 10, complete com publicações a partir de 10 mil curtidas e sinalize essa flexibilização.
No conjunto inicial, inclua pelo menos 6 publicações em português. As demais podem ser em inglês ou de outros países quando tiverem métricas superiores ou abordagens relevantes.
Para cada resultado, informe perfil, assunto, data, idioma, quantidade de curtidas e link direto.
Ordene da maior para a menor quantidade de curtidas. Não invente informações: marque como “não verificado” qualquer número que não consiga confirmar.
Pesquise apenas {formato}, salvo se eu pedir outro formato. Não transcreva ainda; aguarde minha escolha."""


def prompt_transcricao(url: str) -> str:
    return f"""Abra esta publicação do Instagram: {url}
Transcreva literalmente somente o texto visível de cada card, card por card e na ordem original.
Não resuma, não reescreva e não complete trechos ilegíveis. Se não conseguir acessar algum card, identifique a lacuna sem inventar conteúdo."""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Tema da pesquisa ou URL da publicação")
    parser.add_argument("--dias", type=int, default=90, help="Janela da pesquisa")
    parser.add_argument("--formato", default="carrosséis", help="Formato pedido")
    parser.add_argument("--transcrever", action="store_true", help="Gerar prompt de transcrição")
    args = parser.parse_args()

    entrada = args.entrada.strip()
    if not entrada:
        parser.error("a entrada não pode ser vazia")
    if args.dias < 1:
        parser.error("--dias deve ser maior que zero")

    if args.transcrever:
        print(prompt_transcricao(entrada))
    else:
        print(prompt_pesquisa(entrada, args.dias, args.formato.strip() or "carrosséis"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
