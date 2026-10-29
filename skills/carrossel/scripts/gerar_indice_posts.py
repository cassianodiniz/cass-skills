#!/usr/bin/env python3
"""Gera a tabela de posts do references/posts-virais/INDICE.md a partir dos arquivos dos posts.

Os arquivos `<formato>-<assunto>.md` são a fonte única de texto e métrica; a tabela do
índice é derivada deles e nunca editada à mão.

Uso:
    python3 gerar_indice_posts.py            regrava o bloco gerado do INDICE.md
    python3 gerar_indice_posts.py --check    só confere se o INDICE.md está em dia (exit 1 se não)
"""

import re
import sys
from pathlib import Path

POSTS = Path(__file__).resolve().parents[1] / "references" / "posts-virais"
INDICE = POSTS / "INDICE.md"
INICIO = "<!-- TABELA-GERADA:inicio (não editar à mão; rode scripts/gerar_indice_posts.py) -->"
FIM = "<!-- TABELA-GERADA:fim -->"

FORMATOS = [
    ("noticia", "Notícia"),
    ("tela-dividida", "Tela dividida"),
    ("card-unico", "Card único"),
]
METRICAS = [
    ("Visualizações", "Views"),
    ("Curtidas", "Curtidas"),
    ("Comentários", "Coment."),
    ("Salvamentos", "Salv."),
    ("Compartilhamentos", "Compart."),
    ("Seguidores ganhos", "Seguidores"),
]


class PostInvalido(Exception):
    pass


def _campo(texto, rotulo, arquivo):
    achado = re.search(rf"(?m)^\| {re.escape(rotulo)} \| (.+?) \|$", texto)
    if not achado:
        raise PostInvalido(f"{arquivo}: falta a métrica '{rotulo}'")
    return achado.group(1)


def _classificacao(texto, rotulo):
    achado = re.search(rf"(?m)^- \*\*{re.escape(rotulo)}:\*\* (.+)$", texto)
    return achado.group(1).strip() if achado else ""


def _gancho(texto, arquivo, card_unico):
    blocos = re.findall(r"```text\n(.*?)\n```", texto, flags=re.S)
    if not blocos:
        raise PostInvalido(f"{arquivo}: sem bloco de transcrição")
    linhas = [l for l in blocos[0].split("\n") if not re.fullmatch(r"(?i)\s*(@?cassiano[ .]diniz)\s*", l)]
    paragrafos = [re.sub(r"\s+", " ", p).strip() for p in "\n".join(linhas).strip().split("\n\n")]
    paragrafos = [p for p in paragrafos if p]
    if card_unico and len(paragrafos) > 2:
        # no card único o texto inteiro é o post; o gancho é a abertura + a pergunta final
        paragrafos = [paragrafos[0], "[…]", paragrafos[-1]]
    return " / ".join(paragrafos).replace("|", "/")


def ler_post(caminho):
    texto = caminho.read_text(encoding="utf-8")
    titulo = re.match(r"# Post (?:sem métrica )?(\w+) - (.+)", texto)
    if not titulo:
        raise PostInvalido(f"{caminho.name}: título fora do padrão '# Post N - ...'")
    nome = re.sub(r"^(Tela dividida|Card único) / ", "", titulo.group(2).strip())
    metricas = {curto: _campo(texto, longo, caminho.name) for longo, curto in METRICAS}
    views = metricas["Views"].replace(".", "")
    if not views.isdigit():
        raise PostInvalido(f"{caminho.name}: visualizações não numéricas")
    return {
        "arquivo": caminho.name,
        "numero": titulo.group(1),
        "nome": nome,
        "sobre": " — ".join(p for p in (_classificacao(texto, "Subtipo"), _classificacao(texto, "Tema")) if p),
        "gancho": _gancho(texto, caminho.name, caminho.name.startswith("card-unico-")),
        "cards": len(re.findall(r"(?m)^### Card \d+", texto)) or 1,
        "views_int": int(views),
        **metricas,
    }


def gerar_bloco():
    partes = [INICIO, ""]
    for prefixo, rotulo in FORMATOS:
        posts = sorted((ler_post(c) for c in POSTS.glob(f"{prefixo}-*.md")), key=lambda p: -p["views_int"])
        partes.append(f"### {rotulo} ({len(posts)} posts)")
        partes.append("")
        partes.append("| Nº | Post | Arquivo | Cards | " + " | ".join(c for _, c in METRICAS) + " |")
        partes.append("|---|---|---|---:|" + "---:|" * len(METRICAS))
        for p in posts:
            partes.append(
                f"| {p['numero']} | {p['nome']} | `{p['arquivo']}` | {p['cards']} | "
                + " | ".join(p[c] for _, c in METRICAS) + " |"
            )
        partes.append("")
        for p in posts:
            partes.append(f"- **{p['nome']}** (`{p['arquivo']}`)")
            partes.append(f"  - Sobre: {p['sobre']}")
            partes.append(f"  - Gancho (card 1): \"{p['gancho']}\"")
        partes.append("")
    partes.append(FIM)
    return "\n".join(partes)


def main(argv):
    atual = INDICE.read_text(encoding="utf-8")
    if atual.count(INICIO) != 1 or atual.count(FIM) != 1:
        print(f"ERRO: marcadores do bloco gerado ausentes ou repetidos em {INDICE.name}")
        return 1
    antes, resto = atual.split(INICIO)
    _, depois = resto.split(FIM)
    try:
        novo = antes + gerar_bloco() + depois
    except PostInvalido as erro:
        print(f"ERRO: {erro}")
        return 1
    if "--check" in argv:
        if novo != atual:
            print("INDICE.md desatualizado: rode scripts/gerar_indice_posts.py")
            return 1
        print("INDICE.md em dia")
        return 0
    INDICE.write_text(novo, encoding="utf-8")
    total = sum(len(list(POSTS.glob(f"{prefixo}-*.md"))) for prefixo, _ in FORMATOS)
    print(f"INDICE.md regravado ({total} posts)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
