#!/usr/bin/env python3
"""Cria a pasta do paciente e põe o contrato modelo dentro dela.

    python novo_paciente.py "Maria Aparecida Silva"

Não preenche nada — só prepara o terreno. Quem escreve os dados no contrato é o
`preencher_contrato.py`, depois.

Se já existir pasta de alguém com nome parecido, ele AVISA e não cria nada: duas
pastas pra mesma pessoa é o jeito mais fácil de perder um contrato assinado.
Pra criar assim mesmo: `--mesmo-assim`.
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum

SEMELHANCA_QUE_ASSUSTA = 0.8


def criar(nome: str, mesmo_assim: bool = False, cfg: dict | None = None) -> dict:
    cfg = comum.ler_config() if cfg is None else cfg
    nome = ' '.join(str(nome or '').split())
    if not nome:
        return {'ok': False, 'erro': 'faltou o nome do paciente'}

    base = comum.pasta_pacientes(cfg)
    base.mkdir(parents=True, exist_ok=True)
    pasta = base / comum.nome_de_pasta(nome)

    if pasta.exists():
        return {'ok': True, 'ja_existia': True, 'pasta': str(pasta),
                'arquivos': sorted(p.name for p in pasta.iterdir()),
                'aviso': 'a pasta já existia — nada foi sobrescrito.'}

    if not mesmo_assim:
        parecidas = [p.name for p in base.iterdir()
                     if p.is_dir()
                     and comum.parecido(nome, p.name) >= SEMELHANCA_QUE_ASSUSTA]
        if parecidas:
            return {'ok': False, 'nome_parecido': parecidas,
                    'erro': f'já existe pasta com nome parecido: {", ".join(parecidas)}. '
                            'É a mesma pessoa? Se for, use a pasta que já existe. '
                            'Se for outra pessoa mesmo, rode de novo com --mesmo-assim.'}

    pasta.mkdir(parents=True)
    resultado = {'ok': True, 'pasta': str(pasta), 'nome': nome, 'copiados': []}

    # A ficha de anamnese nasce EM BRANCO junto com a pasta (só o layout, pra preencher
    # quando as respostas chegarem) — decisão do Cassiano, 04/08/2026.
    ficha_modelo = (pathlib.Path(__file__).resolve().parent.parent / 'assets'
                    / 'Ficha do Paciente (modelo).html')
    if ficha_modelo.exists():
        ficha = pasta / f'Ficha do Paciente - {comum.nome_de_pasta(nome)}.html'
        shutil.copy2(ficha_modelo, ficha)
        resultado['copiados'].append(ficha.name)
        resultado['ficha'] = str(ficha)

    modelo = cfg.get('contrato_modelo')
    if not modelo:
        resultado['aviso'] = ('nenhum contrato modelo configurado — a pasta foi criada '
                              'vazia. Rode `configurar.py` pra apontar o modelo.')
        return resultado

    origem = os.path.expanduser(str(modelo))
    if not os.path.exists(origem):
        resultado['aviso'] = (f'o contrato modelo configurado não existe mais: {origem}. '
                              'A pasta foi criada vazia — rode `configurar.py` de novo.')
        return resultado

    destino = pasta / f'Contrato - {comum.nome_de_pasta(nome)}.odt'
    shutil.copy2(origem, destino)
    resultado['copiados'].append(destino.name)
    resultado['contrato'] = str(destino)
    return resultado


def main() -> int:
    comum.usar_utf8()
    args = [a for a in sys.argv[1:] if a != '--mesmo-assim']
    if not args:
        print(json.dumps({'ok': False, 'erro': 'uso: novo_paciente.py "Nome do Paciente"'},
                         ensure_ascii=False))
        return 1
    r = criar(' '.join(args), mesmo_assim='--mesmo-assim' in sys.argv)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
