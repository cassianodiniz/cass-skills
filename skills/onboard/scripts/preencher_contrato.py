#!/usr/bin/env python3
"""Preenche o contrato do paciente trocando os marcadores do modelo pelos dados.

Como funciona: o contrato modelo tem marcadores escritos assim → {{NOME}}, {{CPF}}.
Este script abre o contrato que já está na pasta do paciente, troca cada marcador
pelo dado certo e salva por cima. O modelo original nunca é tocado.

Dois usos:

    # 1. Ver quais marcadores o modelo tem (antes de usar pela primeira vez)
    python preencher_contrato.py --conferir "caminho/do/modelo.odt"

    # 2. Preencher
    python preencher_contrato.py --dados dados.json

Use `--dados`. O redirecionamento `< dados.json` **não funciona no PowerShell**, que é o
terminal padrão do Windows — ele responde "Operador '<' reservado para uso futuro" e o
comando nem chega a rodar.

O JSON:
{
  "odt":         "C:/Users/você/Documents/Pacientes/Maria Silva/Contrato - Maria Silva.odt",
  "nome":        "Maria Aparecida Silva",
  "cpf":         "12345678909",
  "nascimento":  "17/01/1993",
  "email":       "maria@email.com",
  "telefone":    "49991234567",
  "endereco":    "Rua das Flores, 123",
  "bairro":      "Centro",
  "cidade":      "Chapecó - SC",
  "cep":         "89800-000",
  "valor":       "R$ 1.800,00",
  "parcelas":    6,
  "forma_pagamento": "Cartão de crédito",
  "data_inicio": "01/08/2026",
  "duracao_meses": 6
}

Só `odt` e `nome` são obrigatórios. Todo campo a mais que você mandar vira um
marcador — `"convenio": "Unimed"` preenche `{{CONVENIO}}`.

Ele PARA sem salvar em dois casos, porque os dois viram problema depois que o
contrato já está na mão do paciente:
  - CPF que não passa no dígito verificador  → `"ignorar_cpf_invalido": true`
  - marcador que ficou sem preencher no documento → `"ignorar_faltando": true`
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum
import odf

MARCADOR = re.compile(r'\{\{\s*([A-Za-z0-9_]+)\s*\}\}')

# Trecho que só entra no contrato se os dados dele existirem: [[Bairro {{BAIRRO}}, ]]
# Sem isso, endereço sem bairro produzia "residente na Rua X, Bairro , Cidade de Y" —
# um buraco no meio da frase que ninguém nota antes de imprimir.
BLOCO_OPCIONAL = re.compile(r'\[\[(.*?)\]\]', re.S)


def _resolver_blocos(texto: str, valores: dict) -> tuple[str, list[str]]:
    """Tira os trechos opcionais cujos dados não vieram. Devolve (texto, omitidos)."""
    omitidos: list[str] = []

    def decidir(m):
        dentro = m.group(1)
        nomes = [n.upper() for n in MARCADOR.findall(dentro)]
        vazios = [n for n in nomes if not str(valores.get(n, '')).strip()]
        if nomes and vazios:
            omitidos.extend(n for n in vazios if n not in omitidos)
            return ''
        return dentro

    return BLOCO_OPCIONAL.sub(decidir, texto), omitidos


# ── varrer o documento ────────────────────────────────────────────────────────

def texto_do_arquivo(caminho) -> str:
    """Todo o texto do documento: corpo, tabelas, cabeçalho e rodapé.

    Contrato costuma guardar o bloco de assinatura numa tabela e o nome da
    profissional no rodapé. No ODF o corpo e as tabelas moram em `content.xml` e o
    cabeçalho/rodapé em `styles.xml` — varrer só um dos dois deixaria marcador cru
    no documento final.
    """
    return '\n'.join(odf.texto_visivel(inner)
                     for xml in odf.ler_partes(caminho).values()
                     for _, inner in odf.paragrafos(xml))


def marcadores_do_arquivo(caminho) -> list[str]:
    achados = []
    for nome in MARCADOR.findall(texto_do_arquivo(caminho)):
        if nome.upper() not in achados:
            achados.append(nome.upper())
    return achados


def _trocar_no_paragrafo(inner: str, valores: dict, fora: list) -> str:
    """Troca os marcadores de um parágrafo. Devolve o parágrafo novo.

    Dois caminhos, nesta ordem:

    1. **Cirúrgico** — troca o marcador onde ele está, sem tocar em mais nada, e
       negrito, tamanho e fonte do resto do parágrafo ficam intactos.
    2. **Achatar** — só quando o marcador está partido entre pedaços (o editor faz
       isso sozinho quando alguém edita no meio da palavra) ou quando há trecho
       opcional, que atravessa vários pedaços e só dá pra decidir olhando o
       parágrafo inteiro. Aí o parágrafo é reescrito herdando a formatação do
       primeiro pedaço.
    """
    visivel = odf.texto_visivel(inner)

    if '[[' in visivel:
        novo, omitidos = _resolver_blocos(visivel, valores)
        fora.extend(n for n in omitidos if n not in fora)
        novo = MARCADOR.sub(lambda m: valores.get(m.group(1).upper(), m.group(0)), novo)
        return odf.achatar(inner, novo) if novo != visivel else inner

    if not MARCADOR.search(visivel):
        return inner

    novo_inner = odf.trocar_marcadores(inner, valores.get)

    # sobrou marcador depois da troca cirúrgica = ele está partido no XML
    sobrou = odf.texto_visivel(novo_inner)
    resolvido = MARCADOR.sub(
        lambda m: valores.get(m.group(1).upper(), m.group(0)), sobrou)
    return odf.achatar(inner, resolvido) if resolvido != sobrou else novo_inner


# ── dados ─────────────────────────────────────────────────────────────────────

def _somar_meses(data: datetime.date, meses: int) -> datetime.date:
    mes = data.month - 1 + int(meses)
    ano = data.year + mes // 12
    mes = mes % 12 + 1
    dia = min(data.day, [31, 29 if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)
                         else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1])
    return datetime.date(ano, mes, dia)


def _parcelas_extenso(n: int) -> str:
    """Extenso no feminino, porque conta PARCELAS: 2 → 'duas', não 'dois'."""
    return {1: 'uma', 2: 'duas'}.get(int(n)) or comum.numero_extenso(n)


def _fragmento_parcelas(valor: float, n: int) -> str:
    """"3 (três) parcelas de R$ …" — com a soma FECHANDO o total, sempre.

    R$ 1.000 em 3× não divide: 3 × R$ 333,33 = R$ 999,99, um centavo a menos do que o
    total escrito na mesma página — a mesma família de contradição da obra de 04/08/2026,
    em miniatura. A conta é feita em centavos inteiros e, quando não divide, a última
    parcela fecha a diferença e a frase diz isso com todas as letras.
    """
    cents = round(valor * 100)
    base, ultima = cents // n, cents - (cents // n) * (n - 1)
    if base == ultima:
        p = base / 100
        return (f'em {n} ({_parcelas_extenso(n)}) parcelas de '
                f'{comum.formatar_brl(p)} ({comum.extenso_reais(p)})')
    pb, pu = base / 100, ultima / 100
    return (f'em {n} ({_parcelas_extenso(n)}) parcelas — '
            f'{n - 1} ({_parcelas_extenso(n - 1)}) de '
            f'{comum.formatar_brl(pb)} ({comum.extenso_reais(pb)}) e a última de '
            f'{comum.formatar_brl(pu)} ({comum.extenso_reais(pu)}), fechando o total')


def frase_pagamento(valor: float, parcelas: int, forma: str | None,
                    data_primeira: str | None) -> str:
    """Monta a frase que vai na cláusula de pagamento — o `{{PAGAMENTO}}` do contrato.

    À vista e parcelado mudam a redação inteira ("pago em" x "vencendo a primeira em"),
    e escrever isso à mão a cada contrato é onde entra erro de conta: 3 x R$ 250 tem que
    fechar com o total. Aqui a parcela é sempre calculada do total, nunca digitada.

    O que a pessoa não informar simplesmente não aparece na frase — melhor uma frase
    curta e verdadeira do que um espaço em branco no meio da cláusula.
    """
    if parcelas and parcelas > 1:
        frase = _fragmento_parcelas(valor, parcelas)
        quando = 'vencendo a primeira em'
    else:
        frase = (f'em parcela única de {comum.formatar_brl(valor)} '
                 f'({comum.extenso_reais(valor)})')
        quando = 'pago em'

    if forma:
        frase += f', via {forma}'
    if data_primeira:
        frase += f', {quando} {data_primeira}'
    return frase


def frase_pagamento_partes(partes: list) -> str:
    """Frase da cláusula de pagamento quando o pagamento é MISTO — cada parte com o seu
    valor, forma e data (ex.: uma entrada no PIX e o resto parcelado no cartão).

    Pedido do Cassiano em 01/08/2026: acordo bom descreve o pagamento como ele de fato
    aconteceu. A conta de cada parcela continua saindo daqui, nunca da digitação; a soma
    das partes é conferida contra o total antes de chegar aqui (`pagamento_nao_fecha`).
    """
    pedacos = []
    for p in partes:
        val = comum.parse_valor(p.get('valor')) or 0
        n = int(comum.parse_valor(p.get('parcelas')) or 1)
        if n > 1:
            txt = (f'{comum.formatar_brl(val)} ({comum.extenso_reais(val)}) '
                   + _fragmento_parcelas(val, n))
            quando = 'vencendo a primeira em'
        else:
            txt = f'{comum.formatar_brl(val)} ({comum.extenso_reais(val)})'
            quando = 'pago em'
        if p.get('forma'):
            txt += f', via {p["forma"]}'
        if p.get('data'):
            txt += f', {quando} {comum.normalizar_data(p["data"])}'
        pedacos.append(txt)
    return 'da seguinte forma: ' + '; e '.join(pedacos)


# Dinheiro escrito por extenso no texto (fora de marcador). O que este padrão achar no
# documento é valor FIXO — e valor fixo é a segunda fonte de verdade que produz contrato
# com dois preços na mesma página (bug de 03/08/2026).
DINHEIRO = re.compile(r'R\$\s*[\d.]+,\d{2}')

# Os preços de tabela do contrato são chaveados pela DURAÇÃO do pacote (`meses` na
# configuração), não pelo nome: nome de pacote é texto livre e não serve de ID.
_TABELA = {1: 'PRECO_MENSAL', 3: 'PRECO_TRIMESTRAL', 6: 'PRECO_SEMESTRAL'}
_DERIVADOS = {3: ('ECONOMIA_TRIMESTRAL', 'TOTAL_TRES_MENSAIS'),
              6: ('ECONOMIA_SEMESTRAL', 'TOTAL_SEIS_MENSAIS')}


def _pacotes_por_meses(cfg: dict) -> tuple[dict, list]:
    """{meses: preço} a partir da configuração + lista de durações duplicadas."""
    por_meses: dict[int, float] = {}
    duplicados: list[str] = []
    for pac in (cfg.get('pacotes') or []):
        try:
            m = int(comum.parse_valor(pac.get('meses')) or 0)
        except (TypeError, ValueError):
            continue
        preco = comum.parse_valor(pac.get('valor'))
        if m not in _TABELA or preco is None:
            continue
        if m in por_meses:
            duplicados.append(f"{pac.get('nome')} ({m} meses)")
        else:
            por_meses[m] = preco
    return por_meses, duplicados


def _precos_de_tabela(cfg: dict) -> dict:
    """Marcadores de preço da Cláusula 8ª/tabela/multa, calculados dos pacotes.

    Economia = meses × mensal − preço do pacote; total = meses × mensal. O contrato
    não calcula nada — recebe tudo pronto daqui (uma fonte só de verdade).
    """
    por_meses, _ = _pacotes_por_meses(cfg)
    v: dict[str, str] = {}
    for m, marcador in _TABELA.items():
        if m in por_meses:
            v[marcador] = comum.formatar_brl(por_meses[m])
            v[marcador + '_EXTENSO'] = comum.extenso_reais(por_meses[m])
    mensal = por_meses.get(1)
    if mensal is not None:
        for m, (eco, total) in _DERIVADOS.items():
            if m in por_meses:
                economia = m * mensal - por_meses[m]
                v[eco] = comum.formatar_brl(economia)
                v[eco + '_EXTENSO'] = comum.extenso_reais(economia)
                v[total] = comum.formatar_brl(m * mensal)
                v[total + '_EXTENSO'] = comum.extenso_reais(m * mensal)
    return v


def montar_valores(dados: dict, cfg: dict, hoje: datetime.date | None = None) -> dict:
    """Dados crus → marcadores prontos ({'NOME': 'Maria', 'CPF': '123...'}).

    Além do que veio no JSON, calcula o que dá pra calcular: primeiro nome, valor
    por extenso, valor da parcela, data de término. São justamente os campos que
    dão erro quando alguém faz de cabeça na pressa.
    """
    hoje = hoje or datetime.date.today()
    v: dict[str, str] = {}

    for chave, valor in dados.items():
        if chave in ('odt', 'force', 'ignorar_cpf_invalido', 'ignorar_faltando',
                     'ignorar_valores_fixos', 'pagamento_partes'):
            continue
        v[chave.upper()] = '' if valor is None else str(valor)

    nome = str(dados.get('nome') or '').strip()
    if nome:
        v['NOME'] = nome
        v['PRIMEIRO_NOME'] = nome.split()[0]

    # Vale pra `cpf` e também pra `cpf_2` / `nascimento_2`: contrato de nutrição para
    # casal traz duas pessoas, e a segunda merece o mesmo cuidado que a primeira.
    for chave, valor in dados.items():
        if not valor:
            continue
        if chave == 'cpf' or chave.startswith('cpf_'):
            v[chave.upper()] = comum.formatar_cpf(valor)
        elif chave == 'nascimento' or chave.startswith('nascimento_'):
            v[chave.upper()] = comum.normalizar_data(valor)

    if dados.get('data_primeira_parcela'):
        v['DATA_PRIMEIRA_PARCELA'] = comum.normalizar_data(dados['data_primeira_parcela'])

    valor_num = comum.parse_valor(dados.get('valor'))
    if valor_num is not None:
        v['VALOR'] = comum.formatar_brl(valor_num)
        v['VALOR_EXTENSO'] = comum.extenso_reais(valor_num)
        parcelas = int(comum.parse_valor(dados.get('parcelas')) or 1)
        if parcelas > 1:
            parcela = round(valor_num / parcelas, 2)
            v['PARCELAS'] = str(parcelas)
            v['VALOR_PARCELA'] = comum.formatar_brl(parcela)
            v['VALOR_PARCELA_EXTENSO'] = comum.extenso_reais(parcela)
        if dados.get('pagamento_partes'):
            v['PAGAMENTO'] = frase_pagamento_partes(dados['pagamento_partes'])
        else:
            v['PAGAMENTO'] = frase_pagamento(
                valor_num, parcelas, dados.get('forma_pagamento'),
                v.get('DATA_PRIMEIRA_PARCELA'))

    inicio_txt = comum.normalizar_data(dados.get('data_inicio'))
    if inicio_txt:
        v['DATA_INICIO'] = inicio_txt

    # A duração já está na configuração, dentro do pacote escolhido. Sem esta busca, o
    # SKILL.md prometia `{{DATA_FIM}}` como "calculado, nunca pergunte" mas ele só saía se
    # o JSON trouxesse `duracao_meses` — chave que a documentação não mostrava em exemplo
    # nenhum. O contrato era recusado com `faltando: DATA_FIM` e não havia como adivinhar
    # o nome da chave (teste de pressão de 30/07/2026).
    meses = dados.get('duracao_meses')
    plano = str(dados.get('plano') or '').strip()
    if not meses and plano:
        for pac in (cfg.get('pacotes') or []):
            if comum.normalizar(pac.get('nome', '')) == comum.normalizar(plano):
                meses = pac.get('meses')
                break
    if inicio_txt and meses:
        try:
            d, m, a = (int(x) for x in inicio_txt.split('/'))
            fim = _somar_meses(datetime.date(a, m, d), int(meses))
            v['DATA_FIM'] = fim.strftime('%d/%m/%Y')
            v['DURACAO_MESES'] = str(int(meses))
        except (ValueError, TypeError):
            pass

    v['DATA_HOJE'] = hoje.strftime('%d/%m/%Y')
    v['DATA_HOJE_EXTENSO'] = comum.data_extenso(hoje)

    # Dados de quem atende vêm da configuração, não do JSON: são sempre os mesmos
    # e redigitar a cada contrato é como o CRN errado entra no documento.
    for chave, valor in (cfg.get('nutricionista') or {}).items():
        v[f'NUTRI_{chave.upper()}'] = str(valor or '')

    # Preços de tabela (Cláusula 8ª, tabela de opções, base da multa da 16.1) saem da
    # MESMA lista `pacotes` — o texto do contrato nunca carrega preço digitado.
    v.update(_precos_de_tabela(cfg))

    return v


# ── principal ─────────────────────────────────────────────────────────────────

def preencher(dados: dict, cfg: dict | None = None) -> dict:
    cfg = comum.ler_config() if cfg is None else cfg
    caminho = pathlib.Path(str(dados.get('odt') or '')).expanduser()
    if not str(caminho) or not caminho.exists():
        return {'ok': False, 'erro': f'contrato não encontrado: {caminho}'}
    if not str(dados.get('nome') or '').strip():
        return {'ok': False, 'erro': 'faltou o nome do paciente'}

    ruins, pistas = [], []
    for c in dados:
        if not (c == 'cpf' or c.startswith('cpf_')) or not dados[c]:
            continue
        if comum.cpf_valido(dados[c]):
            continue
        ruins.append(f'{c}={dados[c]}')
        arrumado, corrigiu = comum.arrumar_cpf(dados[c])
        if corrigiu:
            pistas.append(f'{c}: com zero(s) na frente vira {comum.formatar_cpf(arrumado)}, '
                          'que é válido — a planilha costuma comer zero à esquerda. '
                          'Confirme com a pessoa e mande o número completo.')
    if ruins and not dados.get('ignorar_cpf_invalido'):
        return {'ok': False, 'cpf_invalido': True, 'cpfs': ruins, 'pistas': pistas,
                'erro': f"CPF que não passa no dígito verificador: {', '.join(ruins)}. "
                        + (' '.join(pistas) if pistas else
                           'Confira o número com a pessoa.')
                        + ' Pra preencher assim mesmo: "ignorar_cpf_invalido": true'}

    # Achado no teste de pressão de 28/07/2026: dois agentes diferentes receberam, como
    # CPF da paciente, o CPF da própria nutricionista — cópia-e-cola errada. O número é
    # válido, então nada reclamava, e o contrato sairia com a mesma pessoa nos dois lados.
    meu_cpf = comum.so_digitos((cfg.get('nutricionista') or {}).get('cpf'))
    if meu_cpf and comum.so_digitos(dados.get('cpf')) == meu_cpf \
            and not dados.get('ignorar_cpf_igual'):
        return {'ok': False, 'cpf_igual_ao_seu': True,
                'erro': 'o CPF informado para o paciente é o MESMO que está configurado '
                        'como o seu. O contrato sairia com a mesma pessoa como CONTRATADO '
                        'e CONTRATANTE. Confirme o CPF do paciente. Se for mesmo assim '
                        '(você atendendo alguém do seu CPF), use "ignorar_cpf_igual": true'}

    # O valor tem que bater com o preço do pacote escolhido. Sem esta conferência já saiu
    # contrato dizendo "Pacote Trimestral" com valor de outro pacote — o documento se
    # contradiz na mesma página e nada reclamava (eval de 28/07/2026).
    escolhido = str(dados.get('plano') or '').strip()
    valor_num = comum.parse_valor(dados.get('valor'))
    if escolhido and valor_num is not None and not dados.get('ignorar_valor_diferente'):
        for pac in (cfg.get('pacotes') or []):
            if comum.normalizar(pac.get('nome', '')) != comum.normalizar(escolhido):
                continue
            padrao = comum.parse_valor(pac.get('valor'))
            if padrao is not None and abs(padrao - valor_num) > 0.01:
                return {'ok': False, 'valor_diferente_do_pacote': True,
                        'pacote': pac.get('nome'), 'valor_padrao': comum.formatar_brl(padrao),
                        'valor_informado': comum.formatar_brl(valor_num),
                        'erro': f"o {pac.get('nome')} custa {comum.formatar_brl(padrao)}, "
                                f'mas o valor informado é {comum.formatar_brl(valor_num)}. '
                                'Confirme com ela: é um valor combinado só para este '
                                'paciente (então mande "ignorar_valor_diferente": true), '
                                'ou o preço do pacote mudou (então atualize o padrão em '
                                '`pacotes`, na configuração)?'}
            break

    # Pagamento misto: a soma das partes tem que fechar o total. Sem esta trava, a
    # cláusula de pagamento sairia descrevendo um dinheiro diferente do contratado —
    # e ninguém confere essa soma depois de impresso.
    partes = dados.get('pagamento_partes')
    if partes:
        soma = sum(comum.parse_valor(p.get('valor')) or 0 for p in partes)
        total = comum.parse_valor(dados.get('valor'))
        if total is None or abs(soma - total) > 0.01:
            return {'ok': False, 'pagamento_nao_fecha': True,
                    'soma_das_partes': comum.formatar_brl(soma),
                    'valor_total': comum.formatar_brl(total or 0),
                    'erro': f'as partes do pagamento somam {comum.formatar_brl(soma)}, '
                            f'mas o valor do contrato é {comum.formatar_brl(total or 0)}. '
                            'Confira com ela os valores de cada parte — a soma tem que '
                            'fechar com o total.'}

    valores = montar_valores(dados, cfg)

    partes = odf.ler_partes(caminho)
    antes = [n.upper() for xml in partes.values()
             for _, inner in odf.paragrafos(xml)
             for n in MARCADOR.findall(odf.texto_visivel(inner))]

    # ── travas de preço, ANTES de qualquer escrita ────────────────────────────
    usa_tabela = any(m.startswith(('PRECO_', 'ECONOMIA_', 'TOTAL_')) for m in antes)
    por_meses, duplicados = _pacotes_por_meses(cfg)

    if usa_tabela and duplicados:
        return {'ok': False, 'pacotes_duplicados': duplicados,
                'erro': 'o contrato NÃO foi preenchido: a configuração tem mais de um '
                        'pacote com a mesma duração — ' + ', '.join(duplicados)
                        + '. Os preços de tabela são escolhidos pela duração (meses), '
                          'então duração repetida deixa ambíguo qual preço entra. '
                          'Ajuste a lista `pacotes` na configuração e rode de novo.'}

    mensal = por_meses.get(1)
    if usa_tabela and mensal is not None:
        for m, (eco, _total) in _DERIVADOS.items():
            if eco in antes and m in por_meses and m * mensal - por_meses[m] <= 0:
                return {'ok': False, 'economia_nao_positiva': True,
                        'erro': f'o contrato NÃO foi preenchido: o texto promete uma '
                                f'"economia" no pacote de {m} meses, mas a conta não '
                                f'fecha — {m} × {comum.formatar_brl(mensal)} (mensal) = '
                                f'{comum.formatar_brl(m * mensal)}, e o pacote custa '
                                f'{comum.formatar_brl(por_meses[m])}. Sem economia real, '
                                f'o contrato sairia dizendo uma coisa falsa. Confirme os '
                                f'preços com ela e corrija a configuração (ou o texto do '
                                f'contrato, por decisão explícita dela).'}

    # Dinheiro escrito FIXO no texto (fora de marcador) é segunda fonte de verdade — o
    # exato desenho que produziu contrato com dois preços na mesma página (03/08/2026).
    # Multa fixa proposital existe (ex.: R$ 100 de taxa), então o aceite é dela, UMA vez:
    # fica gravado em `valores_fixos_aceitos` na configuração.
    fixos = sorted({comum.formatar_brl(comum.parse_valor(t))
                    for xml in partes.values()
                    for _, inner in odf.paragrafos(xml)
                    for t in DINHEIRO.findall(odf.texto_visivel(inner).replace('\xa0', ' '))
                    if comum.parse_valor(t) is not None})
    aceitos = {str(a).replace('\xa0', ' ') for a in (cfg.get('valores_fixos_aceitos') or [])}
    nao_aceitos = [f for f in fixos if f.replace('\xa0', ' ') not in aceitos]
    # `antes` vazio = documento já preenchido (nenhum marcador restante): o dinheiro no
    # texto é o que a própria skill escreveu, não fonte fixa — a trava não se aplica.
    if antes and nao_aceitos and not dados.get('ignorar_valores_fixos'):
        trechos = []
        for xml in partes.values():
            for _, inner in odf.paragrafos(xml):
                txt = odf.texto_visivel(inner).replace('\xa0', ' ')
                if any(v.replace('\xa0', ' ') in txt for v in nao_aceitos):
                    trechos.append(txt.strip()[:160])
        return {'ok': False, 'valores_fixos': nao_aceitos, 'trechos': trechos[:10],
                'erro': 'o contrato NÃO foi preenchido: há dinheiro escrito FIXO no texto '
                        '(fora de marcador) — ' + ', '.join(nao_aceitos)
                        + '. Preço fixo no texto é como o contrato sai com dois valores '
                          'diferentes na mesma página. Se este é o modelo antigo da '
                          'skill, troque pelo novo (os preços viraram marcadores). Se o '
                          'valor é proposital (ex.: taxa fixa do contrato dela), mostre '
                          'os trechos a ela e, com o OK dela, grave o aceite uma única '
                          'vez: `configurar.py --dados` com {"valores_fixos_aceitos": '
                          '[...]}. Para este preenchimento apenas: '
                          '"ignorar_valores_fixos": true.'}

    omitidos: list[str] = []
    novas = {nome: odf.mapear(xml, lambda i: _trocar_no_paragrafo(i, valores, omitidos))
             for nome, xml in partes.items()}

    faltando = []
    for xml in novas.values():
        for _, inner in odf.paragrafos(xml):
            for n in MARCADOR.findall(odf.texto_visivel(inner)):
                if n.upper() not in faltando:
                    faltando.append(n.upper())

    preenchidos = [m for m in dict.fromkeys(antes)
                   if m not in faltando and m not in omitidos]

    if faltando and not dados.get('ignorar_faltando'):
        return {'ok': False, 'faltando': faltando, 'preenchidos': preenchidos,
                'erro': 'o contrato NÃO foi salvo: estes marcadores ficaram sem dado — '
                        + ', '.join('{{%s}}' % m for m in faltando)
                        + '. Mande esses campos no JSON, ou "ignorar_faltando": true pra '
                          'salvar assim mesmo — nesse caso o marcador continua APARECENDO '
                          'no documento (`{{CIDADE}}` escrito no meio da frase), de '
                          'propósito: campo apagado ninguém nota antes de imprimir, '
                          'marcador cru salta aos olhos.'}

    odf.gravar_partes(caminho, novas)
    r = {'ok': True, 'odt': str(caminho), 'preenchidos': preenchidos,
         'faltando': faltando, 'omitidos': omitidos}
    if omitidos:
        r['aviso'] = ('estes dados não vieram e o trecho deles foi RETIRADO da frase, '
                      'em vez de deixar buraco no texto: '
                      + ', '.join(omitidos)
                      + '. Não dê o contrato por pronto sem perguntar a ela o que quer '
                        'fazer com eles.')
    return r


def main() -> int:
    comum.usar_utf8()
    if '--conferir' in sys.argv:
        i = sys.argv.index('--conferir')
        if i + 1 >= len(sys.argv):
            print(json.dumps({'ok': False, 'erro': 'uso: --conferir <arquivo.odt>'},
                             ensure_ascii=False))
            return 1
        alvo = pathlib.Path(sys.argv[i + 1]).expanduser()
        if not alvo.exists():
            print(json.dumps({'ok': False, 'erro': f'não encontrei {alvo}'},
                             ensure_ascii=False))
            return 1
        achados = marcadores_do_arquivo(alvo)
        print(json.dumps({'ok': True, 'arquivo': str(alvo), 'marcadores': achados,
                          'total': len(achados)}, ensure_ascii=False, indent=2))
        return 0 if achados else 1

    dados, erro = comum.ler_json_entrada(sys.argv)
    if erro or not dados:
        print(json.dumps({'ok': False, 'erro': erro or
                          'não recebi os dados. Use: --dados caminho/dados.json'},
                         ensure_ascii=False))
        return 1

    r = preencher(dados)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get('ok') else 1


if __name__ == '__main__':
    sys.exit(main())
