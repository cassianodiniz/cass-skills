#!/usr/bin/env python3
"""Despeja o texto de um documento na tela, pra dele tirar os dados do paciente.

    python ler_documento.py "caminho/da/ficha.odt"

Serve quando a pessoa aponta um arquivo em vez de colar o texto ou usar planilha:
ficha de anamnese, cadastro antigo, contrato anterior. Este script só LÊ e mostra —
quem entende o que é nome, o que é CPF e o que é endereço é quem está lendo.

Formatos: .odt, .txt, .md e .csv são lidos direto; .docx, .doc e .rtf passam antes
pelo LibreOffice. Tabela sai junto, porque ficha de cadastro quase sempre é tabela.

**PDF não passa por aqui** — abra o PDF com a sua própria ferramenta de leitura.
Instalar mais uma biblioteca só pra isso não compensa.
"""
from __future__ import annotations

import csv
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum

# `.odt` é lido direto (é ZIP com XML, o Python dá conta sozinho). Os formatos de
# editor — Word e companhia — passam antes pelo LibreOffice, que já é requisito da
# skill: assim a ficha que ela tiver serve, seja qual for o programa que a gerou, e
# nenhuma biblioteca extra precisa ser instalada.
NATIVOS = {'.odt', '.txt', '.md', '.csv'}
VIA_LIBREOFFICE = {'.docx', '.doc', '.rtf', '.odf'}
SUPORTADOS = NATIVOS | VIA_LIBREOFFICE


def _do_odt(caminho: pathlib.Path) -> list[str]:
    import odf
    linhas = []
    for xml in odf.ler_partes(caminho).values():
        for _, inner in odf.paragrafos(xml):
            texto = odf.texto_visivel(inner).strip()
            if texto:
                linhas.append(texto)
    return linhas


def _convertendo(caminho: pathlib.Path) -> list[str]:
    """Converte para .odt numa pasta temporária e lê de lá — o original não é tocado."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        copia = pathlib.Path(tmp) / caminho.name
        shutil.copy2(caminho, copia)
        novo, erro = comum.converter_para_odt(copia)
        if not novo:
            raise RuntimeError(erro or 'a conversão não produziu arquivo')
        return _do_odt(novo)


def ler(caminho_txt: str) -> dict:
    caminho = pathlib.Path(str(caminho_txt or '')).expanduser()
    if not caminho.exists():
        return {'ok': False, 'erro': f'não encontrei o arquivo: {caminho}'}

    ext = caminho.suffix.lower()
    if ext == '.pdf':
        return {'ok': False, 'pdf': True,
                'erro': 'este é um PDF — abra com a sua própria ferramenta de leitura '
                        'em vez deste script.'}
    if ext not in SUPORTADOS:
        return {'ok': False, 'erro': f'não sei ler {ext}. Formatos: '
                                     + ', '.join(sorted(SUPORTADOS))}

    try:
        if ext == '.odt':
            linhas = _do_odt(caminho)
        elif ext in VIA_LIBREOFFICE:
            linhas = _convertendo(caminho)
        elif ext == '.csv':
            with caminho.open(encoding='utf-8', errors='replace', newline='') as f:
                linhas = [' | '.join(l) for l in csv.reader(f) if any(l)]
        else:
            linhas = [l.strip() for l in
                      caminho.read_text(encoding='utf-8', errors='replace').splitlines()
                      if l.strip()]
    except Exception as e:
        return {'ok': False, 'erro': f'não consegui ler o arquivo: {type(e).__name__}: {e}'}

    return {'ok': True, 'arquivo': str(caminho), 'linhas': len(linhas),
            'texto': '\n'.join(linhas)}


def main() -> int:
    comum.usar_utf8()
    if len(sys.argv) < 2:
        print(json.dumps({'ok': False, 'erro': 'uso: ler_documento.py "caminho/do/arquivo"'},
                         ensure_ascii=False))
        return 1
    r = ler(' '.join(sys.argv[1:]))
    if r.get('ok'):
        print(f"# {r['arquivo']} ({r['linhas']} linhas)\n")
        print(r['texto'])
        return 0
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 1


if __name__ == '__main__':
    sys.exit(main())
