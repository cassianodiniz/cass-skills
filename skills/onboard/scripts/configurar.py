#!/usr/bin/env python3
"""Guarda as escolhas de quem usa a skill: onde ficam as pastas, qual é o contrato
modelo, e os dados de quem atende.

A configuração fica em `~/.onboard-paciente.json` — na pasta pessoal, fora da skill.
Ninguém precisa mexer no arquivo à mão: manda um JSON com o que quer mudar.

    # primeira vez nesta máquina (cria a pasta e copia o contrato modelo pra fora daqui)
    python configurar.py --primeira-vez --dados config.json

    # ver como está (e o que está faltando)
    python configurar.py --conferir

    # mudar o que precisar (só o que vier no JSON é alterado)
    python configurar.py --dados config.json

JSON aceito:
{
  "pasta_pacientes": "C:/Users/você/Documents/Pacientes",
  "contrato_modelo": "C:/Users/você/Documents/Modelos/Contrato modelo.odt",
  "nutricionista": {
    "nome": "Maria Nutricionista",
    "cpf": "123.456.789-09",
    "crn": "CRN-10 1234",
    "endereco": "Rua X, 100, Centro, Chapecó/SC",
    "cidade": "Chapecó-SC"
  },
  "planilha": "https://docs.google.com/spreadsheets/d/ID_DA_PLANILHA/edit#gid=0"
}

Nada aqui é obrigatório. Sem `pasta_pacientes`, ela cai em Documentos/Pacientes.
Sem `planilha`, os dados do paciente são digitados na conversa.

Qualquer chave dentro de `nutricionista` vira um marcador `{{NUTRI_<CHAVE>}}` no contrato:
`cidade` → `{{NUTRI_CIDADE}}`, `crn` → `{{NUTRI_CRN}}`. Rode
`preencher_contrato.py --conferir <modelo>` para ver quais o SEU contrato pede.

Use `--dados arquivo.json`. O redirecionamento `< arquivo.json` **não funciona no
PowerShell** (terminal padrão do Windows) — ele nem executa o comando.
"""
from __future__ import annotations

import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum


def conferir() -> dict:
    cfg = comum.ler_config()
    itens, pendencias = [], []
    vem_junto = None

    pasta = comum.pasta_pacientes(cfg)
    padrao = not cfg.get('pasta_pacientes')
    itens.append({
        'item': 'pasta dos pacientes',
        'ok': True,
        'detalhe': f'{pasta}' + (' (padrão)' if padrao else ' (escolhida por você)')
                   + ('' if pasta.exists() else ' — ainda não existe, será criada no '
                                                'primeiro paciente'),
    })

    modelo = cfg.get('contrato_modelo')
    existe = bool(modelo) and os.path.exists(os.path.expanduser(str(modelo)))
    itens.append({'item': 'contrato modelo', 'ok': existe,
                  'detalhe': str(modelo) if modelo else 'nenhum configurado'})
    if not existe:
        # A skill traz um contrato pronto em `assets/`. Antes desta conferência a
        # pendência mandava "aponte o contrato modelo" mesmo com ele dentro do pacote,
        # e o agente ia pedir à nutricionista um arquivo que ela já tinha.
        junto = comum.modelo_que_vem_junto()
        if junto:
            vem_junto = str(junto)
            sumiu = ' O que estava configurado não está mais lá.' if modelo else ''
            pendencias.append(
                f'Há um contrato modelo pronto dentro da skill ({junto.name}).{sumiu} '
                'Rode `configurar.py --primeira-vez` para copiá-lo para a pasta dela — '
                'ele NÃO sobrescreve um modelo que já exista. Só peça um contrato a ela '
                'se ela preferir usar o próprio.')
        else:
            pendencias.append('Aponte o contrato modelo (.odt com os marcadores) em '
                              '`contrato_modelo`.')

    marcadores = []
    if existe:
        try:
            import preencher_contrato
            marcadores = preencher_contrato.marcadores_do_arquivo(
                os.path.expanduser(str(modelo)))
        except ImportError:
            marcadores = []
        except Exception as e:  # arquivo corrompido, não-ODF, protegido
            pendencias.append(f'Não consegui ler o contrato modelo: {e}')
    itens.append({'item': 'marcadores no modelo', 'ok': bool(marcadores),
                  'detalhe': ', '.join('{{%s}}' % m for m in marcadores)
                             or 'nenhum marcador {{ASSIM}} encontrado'})
    if existe and not marcadores:
        pendencias.append('O modelo não tem nenhum marcador {{ASSIM}} — sem eles não '
                          'há o que preencher. Ver references/preparar-contrato-modelo.md.')

    dados_nutri = cfg.get('nutricionista') or {}
    itens.append({'item': 'seus dados (vão no contrato)', 'ok': bool(dados_nutri),
                  'detalhe': ', '.join(sorted(dados_nutri)) or 'nenhum preenchido'})

    pacotes = cfg.get('pacotes') or []
    de_exemplo = bool(cfg.get('pacotes_de_exemplo'))
    itens.append({'item': 'pacotes e preços', 'ok': bool(pacotes) and not de_exemplo,
                  'detalhe': (' · '.join(
                      f"{p.get('nome')} {comum.formatar_brl(comum.parse_valor(p.get('valor')) or 0)}"
                      f" ({p.get('meses')} meses)" for p in pacotes) or 'nenhum configurado')
                      + (' — SÃO OS PREÇOS DO CONTRATO DE EXEMPLO' if de_exemplo else '')})
    if de_exemplo:
        pendencias.append(
            'Os preços gravados são os do contrato que vem junto, de outro consultório. '
            'Pergunte a ela quais são os pacotes e preços dela e grave com '
            '`configurar.py --dados` (chave `pacotes`). Enquanto não trocar, ou o contrato '
            'sai com preço que não é o dela, ou é recusado por não bater com o pacote.')

    # O preço mora num lugar só: a lista `pacotes` da configuração. O contrato puxa de lá
    # por marcador ({{PRECO_MENSAL}} etc.) — dinheiro escrito FIXO no texto é segunda
    # fonte de verdade, e foi assim que um contrato saiu com dois preços na mesma página
    # (bug de 03/08/2026, desenho novo de 04/08). Valor fixo proposital (ex.: taxa de
    # R$ 100 do contrato próprio dela) existe: o aceite é dela, uma vez, gravado em
    # `valores_fixos_aceitos`.
    if existe:
        try:
            import preencher_contrato
            texto = preencher_contrato.texto_do_arquivo(
                os.path.expanduser(str(modelo))).replace('\xa0', ' ')
            fixos = sorted({comum.formatar_brl(comum.parse_valor(t))
                            for t in preencher_contrato.DINHEIRO.findall(texto)
                            if comum.parse_valor(t) is not None})
            aceitos = {str(a).replace('\xa0', ' ') for a in
                       (cfg.get('valores_fixos_aceitos') or [])}
            novos = [f for f in fixos if f.replace('\xa0', ' ') not in aceitos]
            usa_marcadores = any(m.startswith(('PRECO_', 'ECONOMIA_', 'TOTAL_'))
                                 for m in marcadores)
            if novos:
                itens.append({'item': 'preços no texto do contrato', 'ok': False,
                              'detalhe': 'valor escrito fixo, sem aceite: '
                                         + ', '.join(novos)})
                pendencias.append(
                    'O contrato tem dinheiro escrito FIXO no texto (fora de marcador): '
                    + ', '.join(novos)
                    + '. É assim que o contrato sai com dois valores diferentes na mesma '
                      'página. Se este é o modelo antigo da skill, troque pelo novo — os '
                      'preços agora são marcadores preenchidos pela configuração. Se o '
                      'valor é proposital, mostre o trecho a ela e grave o aceite uma '
                      'única vez com `configurar.py --dados` '
                      '{"valores_fixos_aceitos": [...]}. '
                      'NÃO EDITE O DOCUMENTO (trava 5 do SKILL.md). O arquivo é: '
                    + str(modelo))
            else:
                itens.append({'item': 'preços no texto do contrato', 'ok': True,
                              'detalhe': ('preenchidos por marcador, da configuração'
                                          if usa_marcadores else
                                          'nenhum valor fixo sem aceite no texto')})

            # Economia prometida no texto tem que fechar a conta — plano longo mais caro
            # que a soma dos mensais faria o contrato afirmar uma "economia" falsa.
            por_meses, duplicados = preencher_contrato._pacotes_por_meses(cfg)
            if usa_marcadores and duplicados:
                pendencias.append('Mais de um pacote com a mesma duração na configuração: '
                                  + ', '.join(duplicados)
                                  + '. Os preços de tabela são escolhidos pela duração — '
                                    'ajuste a lista `pacotes`.')
            mensal = por_meses.get(1)
            if usa_marcadores and mensal is not None:
                for m, (eco, _t) in preencher_contrato._DERIVADOS.items():
                    if eco in marcadores and m in por_meses \
                            and m * mensal - por_meses[m] <= 0:
                        pendencias.append(
                            f'A conta da economia do pacote de {m} meses não fecha: '
                            f'{m} × {comum.formatar_brl(mensal)} = '
                            f'{comum.formatar_brl(m * mensal)}, e o pacote custa '
                            f'{comum.formatar_brl(por_meses[m])}. O contrato promete '
                            f'economia que não existe — confirme os preços com ela.')
        except Exception:
            pass  # não deu pra ler o texto: o resto do check-up já cobre isso

    itens.append({'item': 'planilha de dados (opcional)',
                  'ok': True,
                  'detalhe': cfg.get('planilha') or 'nenhuma — os dados são digitados '
                                                    'na conversa'})

    # LibreOffice não entra para preencher — o preenchimento é feito por dentro do
    # arquivo, sem abrir programa nenhum (ODT é ZIP com XML, e isso o Python lê sozinho:
    # foi assim que o `pip install python-docx` saiu da instalação em 31/07/2026). Ele
    # entra porque é ele que converte para ODT o contrato que ela trouxer em Word, e
    # porque é nele que ela abre o contrato pronto para conferir e exportar o PDF —
    # a exportação é dela, nunca do agente (etapa de PDF automática removida em
    # 04/08/2026; ver SKILL.md, "Quando pedirem o PDF").
    soffice = comum.achar_soffice()
    itens.append({'item': 'LibreOffice (converte Word e abre o contrato pronto)',
                  'ok': bool(soffice),
                  'detalhe': soffice or 'não encontrado'})
    if not soffice:
        pendencias.append(
            'Instale o LibreOffice — é ele que converte um contrato em Word para o '
            'formato da skill, e é nele que ela abre o contrato pronto para conferir e '
            'exportar o PDF. Windows: '
            '`winget install TheDocumentFoundation.LibreOffice`. Mac: '
            '`brew install --cask libreoffice`. Peça autorização antes de instalar.')

    r = {'ok': not pendencias, 'config': str(comum.CONFIG_PATH),
         'itens': itens, 'pendencias': pendencias}
    if vem_junto:
        r['modelo_que_vem_junto'] = vem_junto
    return r


def primeira_vez(novo: dict | None = None) -> dict:
    """Deixa a máquina pronta na primeira vez: pasta, modelo e configuração.

    O modelo de contrato é COPIADO para fora da skill, para dentro da pasta da pessoa.
    Isso não é capricho de organização: ela vai editar o contrato (preço, cláusulas,
    testemunhas), e a skill é atualizada de tempos em tempos. Se o contrato que ela usa
    morasse dentro da skill, uma atualização apagaria o trabalho dela sem avisar.

    Nunca sobrescreve um modelo que já esteja lá — se já existe, mantém o dela.
    """
    novo = dict(novo or {})
    cfg = comum.ler_config()
    passos = []

    base = comum.pasta_pacientes({**cfg, **novo})
    base.mkdir(parents=True, exist_ok=True)
    passos.append(f'pasta dos pacientes pronta: {base}')

    semente = comum.modelo_que_vem_junto()
    destino = base / '_Modelo' / 'Contrato modelo.odt'

    if novo.get('contrato_modelo'):
        passos.append('contrato modelo: usando o que você indicou')
    elif destino.exists():
        novo['contrato_modelo'] = str(destino)
        passos.append(f'contrato modelo: já existia em {destino} — mantido como está')
    elif semente:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(semente, destino)
        novo['contrato_modelo'] = str(destino)
        passos.append(f'contrato modelo copiado para {destino} — edite ESTE arquivo, '
                      'não o que está dentro da skill')
    else:
        passos.append('nenhum contrato modelo veio junto: aponte o seu com '
                      '"contrato_modelo" quando tiver ele marcado '
                      '(ver references/preparar-contrato-modelo.md)')

    # Preços de partida, os mesmos do contrato que vem junto. Ficam na configuração —
    # e não no código — porque cada nutricionista cobra o que quiser, e porque é isso que
    # permite conferir, na hora de preencher, se o valor bate com o pacote escolhido.
    if not cfg.get('pacotes') and not novo.get('pacotes'):
        novo['pacotes'] = [
            {'nome': 'Pacote Nutricional Mensal', 'valor': 300, 'meses': 1},
            {'nome': 'Pacote Nutricional Trimestral', 'valor': 750, 'meses': 3},
            {'nome': 'Pacote Nutricional Semestral', 'valor': 1140, 'meses': 6},
        ]
        # Marcados como de exemplo para o check-up NÃO dar verde neles. Sem esta marca,
        # `pacotes e preços: ok` era só "tem alguma coisa preenchida" — e o que estava
        # preenchido era o preço de outro consultório, justamente no campo que o SKILL.md
        # chama de "o único que a pessoa lesa a si mesma se errar" (pressão de 30/07/2026).
        novo['pacotes_de_exemplo'] = True
        passos.append('preços de partida gravados (Mensal R$ 300,00 / Trimestral '
                      'R$ 750,00 / Semestral R$ 1.140,00) — são de outro '
                      'consultório, PERGUNTE os dela')

    r = aplicar(novo)
    r['passos'] = passos
    r['conferencia'] = conferir()
    return r


def aplicar(novo: dict) -> dict:
    cfg = comum.ler_config()
    avisos = []

    for chave, valor in (novo or {}).items():
        if chave == 'nutricionista' and isinstance(valor, dict):
            atual = dict(cfg.get('nutricionista') or {})
            atual.update(valor)
            cfg['nutricionista'] = atual
        else:
            cfg[chave] = valor

    # Preço que ela informou deixa de ser "de exemplo".
    if 'pacotes' in (novo or {}) and not (novo or {}).get('pacotes_de_exemplo'):
        cfg.pop('pacotes_de_exemplo', None)

    modelo = cfg.get('contrato_modelo')
    if modelo:
        caminho = os.path.expanduser(str(modelo))
        if not os.path.exists(caminho):
            avisos.append(f'atenção: o contrato modelo não existe em {caminho}')
        elif not caminho.lower().endswith('.odt'):
            # Ela apontou o contrato dela em Word (ou outro formato). Converter é
            # trabalho da máquina, não dela: o LibreOffice já é requisito e faz isso
            # sozinho. Pedir que ela converta seria empurrar para a pessoa uma tarefa
            # que a ferramenta faz em segundos.
            novo, erro = comum.converter_para_odt(caminho)
            if novo:
                cfg['contrato_modelo'] = str(novo)
                avisos.append(f'o contrato estava em {os.path.splitext(caminho)[1]} e foi '
                              f'convertido para .odt: {novo}. O original continua na pasta.')
            else:
                avisos.append(f'atenção: o contrato modelo precisa ser .odt e a conversão '
                              f'não deu certo — {erro}')

    comum.gravar_config(cfg)
    return {'ok': True, 'config': str(comum.CONFIG_PATH),
            'pasta_pacientes': str(comum.pasta_pacientes(cfg)),
            'avisos': avisos}


def main() -> int:
    comum.usar_utf8()
    if '--conferir' in sys.argv or '--mostrar' in sys.argv:
        r = conferir()
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r['ok'] else 1

    inicial = '--primeira-vez' in sys.argv
    novo, erro = comum.ler_json_entrada(sys.argv)
    if erro:
        print(json.dumps({'ok': False, 'erro': erro}, ensure_ascii=False))
        return 1
    if not inicial and not novo:
        print(json.dumps({'ok': False, 'erro': 'nada a fazer. Use --conferir, '
                                               '--primeira-vez, ou mande um JSON.'},
                         ensure_ascii=False))
        return 1

    r = primeira_vez(novo) if inicial else aplicar(novo)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
