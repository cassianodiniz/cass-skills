#!/usr/bin/env python3
"""Busca os dados do paciente numa planilha do Google (opcional).

    python buscar_planilha.py "Maria Silva"

Só funciona se a planilha estiver configurada (`configurar.py`) E compartilhada
como "qualquer pessoa com o link pode ver" — senão o Google devolve a página de
login em vez dos dados, e o script avisa isso em vez de fingir que não achou.

Quem não usa planilha não precisa de nada disso: os dados são digitados na conversa.

As colunas são reconhecidas pelo nome do cabeçalho (uma coluna chamada "Seu CPF"
vira `cpf`). Se a sua planilha usa nomes muito diferentes, dá pra dizer quais são
na configuração:

    "colunas": {"nome": "Paciente", "cpf": "Documento"}
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum

# Palavras que aparecem no cabeçalho de cada campo, da mais específica pra menos.
PISTAS = {
    'nome': ['nome completo', 'nome do paciente', 'paciente', 'nome'],
    'cpf': ['cpf'],
    'nascimento': ['data de nascimento', 'nascimento', 'data nasc'],
    'email': ['e mail', 'email', 'endereco de e mail'],
    'telefone': ['whatsapp', 'telefone', 'celular', 'contato'],
    'endereco': ['endereco completo', 'endereco', 'rua', 'logradouro'],
    'bairro': ['bairro'],
    'cidade': ['cidade'],
    # `estado_civil` vem ANTES de `estado`: a coluna "Estado civil" contém a palavra
    # "estado" e seria roubada pelo campo errado se a ordem fosse a outra.
    'estado_civil': ['estado civil'],
    'estado': ['estado', 'uf'],
    'cep': ['cep'],
    'nacionalidade': ['nacionalidade'],
    'profissao': ['profissao', 'ocupacao'],
    'valor': ['valor', 'preco', 'investimento'],
    'plano': ['plano', 'pacote'],
}

SEMELHANCA_MINIMA = 0.6


def url_csv(planilha: str) -> str | None:
    """Link normal da planilha → link que devolve o conteúdo em CSV."""
    txt = str(planilha or '').strip()
    if not txt:
        return None
    ident = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', txt)
    chave = ident.group(1) if ident else (txt if re.fullmatch(r'[a-zA-Z0-9-_]{20,}', txt) else None)
    if not chave:
        return None
    aba = re.search(r'[#&?]gid=(\d+)', txt)
    return (f'https://docs.google.com/spreadsheets/d/{chave}/export?format=csv'
            f'&gid={aba.group(1) if aba else 0}')


def baixar(url: str, timeout: int = 20) -> tuple[str | None, str | None]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            bruto = r.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return None, (f'o Google recusou o acesso ({e.code}). Abra a planilha, clique em '
                      'Compartilhar e deixe "qualquer pessoa com o link" como leitor.')
    except Exception as e:
        return None, f'não consegui baixar a planilha: {e}'
    if bruto.lstrip()[:15].lower().startswith('<!doctype html') or '<html' in bruto[:200].lower():
        return None, ('a planilha não está pública: o Google devolveu a tela de login. '
                      'Compartilhe como "qualquer pessoa com o link pode ver".')
    return bruto, None


def mapear_colunas(cabecalho: list[str], forcado: dict | None = None) -> dict:
    """Cabeçalho da planilha → qual coluna é qual campo."""
    forcado = forcado or {}
    normalizados = [comum.normalizar(c) for c in cabecalho]
    mapa: dict[str, int] = {}

    for campo, titulo in forcado.items():
        alvo = comum.normalizar(titulo)
        if alvo in normalizados:
            mapa[campo] = normalizados.index(alvo)

    for campo, pistas in PISTAS.items():
        if campo in mapa:
            continue
        for pista in pistas:
            achou = next((i for i, c in enumerate(normalizados)
                          if pista in c and i not in mapa.values()), None)
            if achou is not None:
                mapa[campo] = achou
                break
    return mapa


def buscar(nome: str, cfg: dict | None = None) -> dict:
    cfg = comum.ler_config() if cfg is None else cfg
    url = url_csv(cfg.get('planilha'))
    if not url:
        return {'ok': False, 'sem_planilha': True,
                'erro': 'nenhuma planilha configurada — os dados do paciente precisam '
                        'ser digitados na conversa.'}

    bruto, erro = baixar(url)
    if erro:
        return {'ok': False, 'erro': erro}

    linhas = list(csv.reader(io.StringIO(bruto)))
    if not linhas:
        return {'ok': False, 'erro': 'a planilha está vazia'}

    cabecalho, dados = linhas[0], linhas[1:]
    mapa = mapear_colunas(cabecalho, cfg.get('colunas'))
    if 'nome' not in mapa:
        return {'ok': False, 'erro': 'não achei a coluna do nome na planilha. Diga qual é '
                                     'na configuração: "colunas": {"nome": "<cabeçalho>"}'}

    def valor(linha, campo):
        i = mapa.get(campo)
        return linha[i].strip() if i is not None and i < len(linha) else ''

    candidatos = []
    for linha in dados:
        na_planilha = valor(linha, 'nome')
        if not na_planilha:
            continue
        candidatos.append((comum.parecido(nome, na_planilha), na_planilha, linha))
    candidatos.sort(key=lambda c: -c[0])

    if not candidatos or candidatos[0][0] < SEMELHANCA_MINIMA:
        return {'ok': False, 'nao_encontrado': True,
                'sugestoes': [c[1] for c in candidatos[:5]],
                'erro': f'não achei "{nome}" na planilha.'}

    empatados = [c for c in candidatos if abs(c[0] - candidatos[0][0]) < 0.01]
    if len(empatados) > 1:
        return {'ok': False, 'ambiguo': True,
                'sugestoes': [c[1] for c in empatados[:5]],
                'erro': f'mais de uma pessoa na planilha combina com "{nome}". '
                        'Pergunte qual é antes de seguir.'}

    _, encontrado, linha = candidatos[0]
    achados = {campo: valor(linha, campo) for campo in comum.CAMPOS_PACIENTE}
    achados['nome'] = encontrado
    if achados.get('nascimento'):
        achados['nascimento'] = comum.normalizar_data(achados['nascimento'])

    corrigido = False
    if achados.get('cpf'):
        achados['cpf'], corrigido = comum.arrumar_cpf(achados['cpf'])
        achados['cpf'] = comum.formatar_cpf(achados['cpf'])

    # Quase toda planilha guarda o endereço inteiro numa coluna só, e o contrato tem um
    # marcador para cada pedaço. Separar aqui evita perguntar à pessoa um bairro que já
    # estava escrito na planilha dela. É PALPITE: vai em `endereco_separado`, com o grau
    # de confiança, para ser mostrado e confirmado — não se escreve no contrato às cegas.
    separado = None
    if achados.get('endereco') and not any(achados.get(c) for c in ('bairro', 'cidade')):
        separado = comum.separar_endereco(achados['endereco'])
        for campo in ('endereco', 'bairro', 'cidade', 'estado', 'cep'):
            if separado.get(campo):
                achados[campo] = separado[campo]

    vazios = [c for c, v in achados.items() if not v]
    return {'ok': True, 'encontrado': encontrado, 'dados': achados,
            'faltando': vazios, 'cpf_corrigido': corrigido,
            'endereco_separado': separado,
            'cpf_valido': comum.cpf_valido(achados.get('cpf')) if achados.get('cpf') else None}


def main() -> int:
    comum.usar_utf8()
    if len(sys.argv) < 2:
        print(json.dumps({'ok': False, 'erro': 'uso: buscar_planilha.py "Nome do Paciente"'},
                         ensure_ascii=False))
        return 1
    r = buscar(' '.join(sys.argv[1:]))
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
