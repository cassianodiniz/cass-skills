#!/usr/bin/env python3
"""Ler e escrever texto dentro de um arquivo ODF (.odt) — sem biblioteca externa.

Um `.odt` é um ZIP com XML dentro. Ler ZIP e XML já vem no Python, então a skill
inteira roda sem `pip install` nenhum. Foi por isso que o formato mudou de `.docx`
para `.odt` em 31/07/2026: além de o LibreOffice deixar de perguntar em que formato
salvar — pergunta que fazia a nutricionista criar um gêmeo `.odt` e congelar o
`.docx` que a skill usava, sem ninguém avisar —, sumiu a dependência que mais dava
problema de instalação.

O texto de um documento ODF mora em duas partes:
  - `content.xml` — o corpo, incluindo tabelas
  - `styles.xml`  — cabeçalho e rodapé

Aqui se mexe no XML como TEXTO, não como árvore: um ODF declara umas trinta
namespaces no topo, e reescrever a árvore com uma biblioteca genérica embaralha
esses prefixos. Trocando só o pedaço que interessa, o resto do arquivo sai igual
ao que entrou.
"""
from __future__ import annotations

import re
import shutil
import zipfile

PARTES_DE_TEXTO = ('content.xml', 'styles.xml')

# <text:p> e <text:h> são o parágrafo e o título. Não aninham entre si, por isso o
# casamento não-guloso resolve. A versão que se fecha sozinha (<text:p/>) não tem
# texto dentro e não interessa.
PARAGRAFO = re.compile(r'<text:([ph])(?:\s[^>]*)?>(.*?)</text:\1>', re.S)
MARCADOR = re.compile(r'\{\{\s*([A-Za-z0-9_]+)\s*\}\}')
PRIMEIRO_SPAN = re.compile(r'<text:span\b[^>]*>')


def escapar(txt) -> str:
    return str(txt).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def desescapar(txt: str) -> str:
    return (txt.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
               .replace('&apos;', "'").replace('&amp;', '&'))


def texto_visivel(inner: str) -> str:
    """O que uma pessoa leria naquele parágrafo, sem as marcações.

    Espaço, tabulação e quebra de linha são elementos próprios no ODF, não
    caracteres — precisam virar caractere aqui, senão palavras vizinhas grudam e um
    marcador partido deixa de ser reconhecido.
    """
    s = re.sub(r'<text:line-break\s*/>', '\n', inner)
    s = re.sub(r'<text:tab\s*/>', '\t', s)
    s = re.sub(r'<text:s\s+text:c="(\d+)"\s*/>', lambda m: ' ' * int(m.group(1)), s)
    s = re.sub(r'<text:s\s*/>', ' ', s)
    return desescapar(re.sub(r'<[^>]+>', '', s))


def achatar(inner: str, novo_texto: str) -> str:
    """Reescreve o parágrafo com um texto só, herdando a formatação do primeiro pedaço.

    Só é usado quando a troca cirúrgica não dá — marcador partido ao meio, ou trecho
    opcional que atravessa vários pedaços. O preço é o parágrafo inteiro passar a ter
    a formatação do primeiro pedaço, por isso é o último recurso e não o primeiro.
    """
    m = PRIMEIRO_SPAN.search(inner)
    escapado = escapar(novo_texto)
    return f'{m.group(0)}{escapado}</text:span>' if m else escapado


def trocar_marcadores(inner: str, valor_de) -> str:
    """Troca os marcadores que estão INTEIROS no XML, sem tocar em mais nada.

    `valor_de(nome)` devolve o texto, ou None para deixar o marcador como está.
    Preserva negrito, tamanho e fonte do resto do parágrafo — que é o que se perde
    quando se reescreve o parágrafo todo.
    """
    def trocar(m):
        v = valor_de(m.group(1).upper())
        return escapar(v) if v is not None else m.group(0)
    return MARCADOR.sub(trocar, inner)


def paragrafos(xml: str):
    """Cada parágrafo do XML, como (match, inner)."""
    return [(m, m.group(2)) for m in PARAGRAFO.finditer(xml)]


def mapear(xml: str, transformar) -> str:
    """Aplica `transformar(inner) -> inner_novo` em cada parágrafo do XML."""
    return PARAGRAFO.sub(
        lambda m: f'{m.group(0)[:m.start(2) - m.start(0)]}'
                  f'{transformar(m.group(2))}'
                  f'{m.group(0)[m.end(2) - m.start(0):]}',
        xml)


# ── arquivo ───────────────────────────────────────────────────────────────────

def ler_partes(caminho) -> dict[str, str]:
    """As partes de texto do documento: {'content.xml': ..., 'styles.xml': ...}."""
    with zipfile.ZipFile(str(caminho)) as z:
        nomes = set(z.namelist())
        return {p: z.read(p).decode('utf-8') for p in PARTES_DE_TEXTO if p in nomes}


def gravar_partes(caminho, partes: dict[str, str]) -> None:
    """Regrava o .odt trocando só as partes indicadas; o resto sai igual ao original.

    O `mimetype` tem que ser o PRIMEIRO arquivo do pacote e ficar SEM compressão — é
    assim que um leitor reconhece um ODF antes de abrir o resto. Recriar o zip sem
    respeitar isso gera arquivo que às vezes abre e às vezes é recusado, que é pior
    do que não abrir nunca.
    """
    caminho = str(caminho)
    temporario = caminho + '.novo'
    with zipfile.ZipFile(caminho) as origem:
        itens = sorted(origem.infolist(), key=lambda i: i.filename != 'mimetype')
        with zipfile.ZipFile(temporario, 'w', zipfile.ZIP_DEFLATED) as destino:
            for item in itens:
                novo = partes.get(item.filename)
                bruto = novo.encode('utf-8') if novo is not None \
                    else origem.read(item.filename)
                if item.filename == 'mimetype':
                    destino.writestr(zipfile.ZipInfo('mimetype'), bruto,
                                     compress_type=zipfile.ZIP_STORED)
                else:
                    destino.writestr(item, bruto)
    shutil.move(temporario, caminho)
