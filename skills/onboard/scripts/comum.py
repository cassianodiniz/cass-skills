#!/usr/bin/env python3
"""Peças que todos os scripts desta skill usam.

Nada aqui fala com a internet e nada aqui guarda dado de paciente: a configuração
mora na pasta pessoal de quem usa (`~/.onboard-paciente.json`), nunca dentro da
skill. Isso é de propósito — a skill é a mesma para todo mundo, a configuração é
de cada um.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import sys
import unicodedata

CONFIG_PATH = pathlib.Path.home() / '.onboard-paciente.json'


def ler_json_entrada(argv: list) -> tuple[dict, str | None]:
    """Lê o JSON de `--dados arquivo.json`. Devolve (dados, erro).

    Só `--dados`, de propósito. O redirecionamento `< arquivo.json` **não funciona no
    PowerShell**, que é o terminal padrão do Windows: ele responde "Operador '<'
    reservado para uso futuro" e o comando nem roda (eval de 28/07/2026).

    E ler da entrada padrão quando não vem `--dados` era pior: rodado por um agente —
    que nunca tem terminal de verdade — o script ficava PARADO esperando um texto que
    nunca chegaria, sem mensagem nenhuma. Travava justamente o
    `configurar.py --primeira-vez` sem argumento, que é o caminho de recuperar o
    contrato modelo. Sem `--dados`, agora, não há JSON: quem precisa dele reclama na
    hora (auditoria de 30/07/2026).
    """
    import json
    caminho = None
    if '--dados' in argv:
        i = argv.index('--dados')
        if i + 1 >= len(argv):
            return {}, 'faltou o arquivo depois de --dados'
        caminho = argv[i + 1]

    if not caminho:
        return {}, None

    try:
        # utf-8-sig e não utf-8: o `Set-Content -Encoding utf8` do PowerShell grava
        # uma marca invisível (BOM) no começo do arquivo, e o leitor de JSON recusa
        # com "Unexpected UTF-8 BOM" — erro que não diz nada a quem escreveu o
        # arquivo. Com `-sig`, arquivo com e sem a marca funcionam igual.
        bruto = pathlib.Path(caminho).expanduser().read_text(encoding='utf-8-sig')
    except OSError as e:
        return {}, f'não consegui ler {caminho}: {e}'

    bruto = bruto.strip().lstrip('﻿')
    if not bruto:
        return {}, None
    try:
        return json.loads(bruto), None
    except json.JSONDecodeError as e:
        return {}, f'JSON inválido: {e}'


def usar_utf8() -> None:
    """Faz a saída sair com acento certo no terminal do Windows.

    Sem isso o console do Windows escreve em cp1252 e "padrão" vira "padr?o" na
    tela — parece dado corrompido e não é. Chamada no começo de cada script.
    """
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass

CAMPOS_PACIENTE = [
    'nome', 'cpf', 'nascimento', 'email', 'telefone',
    'endereco', 'bairro', 'cidade', 'estado', 'cep',
    # O bloco "DAS PARTES" de um contrato de nutrição pede estes também.
    'nacionalidade', 'estado_civil', 'profissao',
    # Dinheiro. Ficavam de fora e eram o dado mais perigoso a se perder: a planilha
    # tinha o valor escrito e a skill descartava, levando a perguntar de novo ou chutar.
    'valor', 'plano',
]


# ── onde as coisas ficam ──────────────────────────────────────────────────────

def pasta_documentos() -> pathlib.Path:
    """A pasta Documentos do computador — de propósito SEM passar pelo OneDrive.

    No Windows o "Documentos" que o Explorer mostra pode estar redirecionado pro
    OneDrive; quem lê o registro cai lá dentro. Aqui vamos direto no caminho físico
    (`C:\\Users\\<usuário>\\Documents`), que é o mesmo lugar no Mac (`~/Documents`).
    Assim a pasta do paciente nasce no mesmo lugar nas duas máquinas.
    """
    if os.name == 'nt':
        base = os.environ.get('USERPROFILE') or str(pathlib.Path.home())
        return pathlib.Path(base) / 'Documents'
    return pathlib.Path.home() / 'Documents'


def ler_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return {}
    return {}


def gravar_config(cfg: dict) -> None:
    CONFIG_PATH.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')


def pasta_pacientes(cfg: dict | None = None) -> pathlib.Path:
    """Pasta-mãe onde cada paciente ganha a sua. Padrão: Documentos/Pacientes."""
    cfg = ler_config() if cfg is None else cfg
    escolhida = (cfg or {}).get('pasta_pacientes')
    if escolhida:
        return pathlib.Path(escolhida).expanduser()
    return pasta_documentos() / 'Pacientes'


def modelo_que_vem_junto() -> pathlib.Path | None:
    """O contrato modelo que é distribuído DENTRO da skill (`assets/*.odt`).

    Existe como função — e não como caminho escrito à mão em cada script — porque o
    agente não tem como adivinhar que a skill traz um contrato pronto. Sem isto, o
    check-up pedia à nutricionista um contrato que já estava no pacote dela
    (auditoria de 30/07/2026).
    """
    assets = pathlib.Path(__file__).resolve().parent.parent / 'assets'
    candidatos = sorted(assets.glob('*.odt')) if assets.is_dir() else []
    return candidatos[0] if candidatos else None


ESPERA_CONVERSAO = 120  # segundos: a primeira conversão da máquina é a mais lenta


def converter_para_odt(caminho) -> tuple[pathlib.Path | None, str | None]:
    """Converte um documento (.docx, .doc, .rtf) para .odt. Devolve (novo, erro).

    A skill trabalha em ODT porque é ZIP com XML — que o Python lê sem instalar nada —
    e porque no ODT o LibreOffice para de perguntar em que formato salvar. Essa
    pergunta era uma armadilha: quem clicasse em "Utilizar o formato ODF" ganhava um
    `.odt` novo e um `.docx` velho congelado, e a skill seguia usando o velho sem
    ninguém avisar (31/07/2026).

    Quem converte é o LibreOffice, que já é requisito. A nutricionista não precisa
    saber que isso aconteceu — ela aponta o contrato dela no formato que tiver.
    """
    import subprocess
    origem = pathlib.Path(str(caminho)).expanduser()
    if not origem.exists():
        return None, f'não encontrei {origem}'
    if origem.suffix.lower() == '.odt':
        return origem, None

    soffice = achar_soffice()
    if not soffice:
        return None, ('preciso do LibreOffice para converter este arquivo em .odt. '
                      'Windows: `winget install TheDocumentFoundation.LibreOffice`. '
                      'Mac: `brew install --cask libreoffice`.')

    # A conversão sai numa pasta temporária LIMPA, e só vai pro destino se produziu
    # arquivo NOVO de verdade. Antes ela saía direto na pasta da origem: quando a
    # conversão falhava e já existia um .odt velho do lado (de uma conversão anterior,
    # antes de a pessoa editar o Word), o velho era entregue como se fosse o novo, sem
    # erro nenhum — provado por execução em 04/08/2026. Mesma família de defeito que
    # aposentou a geração automática de PDF.
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as perfil, \
            tempfile.TemporaryDirectory() as saida:
        try:
            subprocess.run(
                [soffice, f'-env:UserInstallation={pathlib.Path(perfil).as_uri()}',
                 '--headless', '--norestore', '--convert-to', 'odt',
                 '--outdir', saida, str(origem)],
                capture_output=True, text=True, timeout=ESPERA_CONVERSAO)
        except (subprocess.TimeoutExpired, OSError) as e:
            return None, f'não consegui converter para .odt: {e}'

        recem = pathlib.Path(saida) / (origem.stem + '.odt')
        if not recem.exists() or recem.stat().st_size == 0:
            return None, ('a conversão para .odt não produziu arquivo. Quase sempre é o '
                          'documento aberto no Word ou no LibreOffice — feche e tente '
                          'de novo.')
        novo = origem.with_suffix('.odt')
        shutil.move(str(recem), str(novo))
    return novo, None


def achar_soffice() -> str | None:
    """Caminho do LibreOffice, que é quem converte o contrato para PDF.

    Procura no PATH e nos lugares onde o instalador põe por padrão. Devolve None
    quando não acha — a skill continua funcionando sem PDF, só avisa.
    """
    achado = shutil.which('soffice') or shutil.which('soffice.exe')
    if achado:
        return achado
    for tentativa in (
        r'C:\Program Files\LibreOffice\program\soffice.exe',
        r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',
        '/usr/bin/soffice',
    ):
        if os.path.exists(tentativa):
            return tentativa
    return None


# ── nomes ─────────────────────────────────────────────────────────────────────

def normalizar(txt: str) -> str:
    """Tira acento, pontuação e caixa — só pra COMPARAR nomes, nunca pra exibir."""
    s = unicodedata.normalize('NFKD', str(txt or ''))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9 ]', ' ', s.lower()).strip()


def parecido(a: str, b: str) -> float:
    """0 a 1 — quantas palavras do nome menor aparecem no maior.

    Serve pra achar 'Maria Silva' quando a planilha guardou 'Maria da Silva Souza'.
    Comparação por palavra em vez de letra a letra porque o que muda de verdade
    entre as duas grafias é palavra inteira (preposição, sobrenome a mais).
    """
    pa, pb = set(normalizar(a).split()), set(normalizar(b).split())
    if not pa or not pb:
        return 0.0
    return len(pa & pb) / min(len(pa), len(pb))


def nome_de_pasta(nome: str) -> str:
    """Nome seguro pra pasta: sem os caracteres que Windows e Mac recusam."""
    limpo = re.sub(r'[<>:"/\\|?*]', '', str(nome or '')).strip().rstrip('.')
    return re.sub(r'\s+', ' ', limpo)


# ── endereço ──────────────────────────────────────────────────────────────────

UFS = {'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
       'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE',
       'TO'}

ESTADOS = {
    'acre': 'AC', 'alagoas': 'AL', 'amapa': 'AP', 'amazonas': 'AM', 'bahia': 'BA',
    'ceara': 'CE', 'distrito federal': 'DF', 'espirito santo': 'ES', 'goias': 'GO',
    'maranhao': 'MA', 'mato grosso': 'MT', 'mato grosso do sul': 'MS',
    'minas gerais': 'MG', 'para': 'PA', 'paraiba': 'PB', 'parana': 'PR',
    'pernambuco': 'PE', 'piaui': 'PI', 'rio de janeiro': 'RJ',
    'rio grande do norte': 'RN', 'rio grande do sul': 'RS', 'rondonia': 'RO',
    'roraima': 'RR', 'santa catarina': 'SC', 'sao paulo': 'SP', 'sergipe': 'SE',
    'tocantins': 'TO',
}


def separar_endereco(texto: str) -> dict:
    """Endereço escrito numa linha só → rua, bairro, cidade, estado, cep.

    Planilha e ficha guardam tudo numa célula — "Rua Senegal, 30, Parque Monte Alegre,
    São Paulo, São Paulo, 6756420" — e o contrato tem um marcador para cada pedaço.
    Sem isto, ou o bolo inteiro cai no lugar da rua (e a frase fica sem sentido), ou
    perguntam à pessoa um bairro que já estava escrito na planilha.

    O palpite é bom mas NÃO é certeza: a ordem varia, tem endereço sem bairro e tem
    endereço com a rua repetida. Por isso devolve `confianca` e `motivos` — quem usa
    tem que MOSTRAR o resultado para a pessoa confirmar antes de escrever no contrato.
    """
    partes = [p.strip(' -–') for p in re.split(r'[,\n]', str(texto or '')) if p.strip(' -–')]
    achado = {'endereco': '', 'bairro': '', 'cidade': '', 'estado': '', 'cep': ''}
    motivos = []
    if not partes:
        return {**achado, 'confianca': 'nenhuma', 'motivos': ['veio vazio'], 'partes': []}

    # CEP: aceita 7 dígitos porque a planilha come o zero à esquerda (`06756420` chega
    # como `6756420`). Sem isso o CEP era confundido com cidade — e o palpite saía
    # marcado como confiável, que é pior do que sair errado.
    for p in list(partes):
        d = so_digitos(p)
        if d == so_digitos(p.replace('-', '')) and 7 <= len(d) <= 8 and \
                re.fullmatch(r'[\d\-–\s]+', p):
            d = d.zfill(8)
            achado['cep'] = f'{d[:5]}-{d[5:]}'
            partes.remove(p)
            break

    def _uf_no_fim(p):
        """'Curitiba -PR', 'Timon(ma)', 'Macaé - Rio de Janeiro' → (UF, o que sobra)."""
        m = re.search(r'[\s\-–(]([A-Za-z]{2})\)?\s*$', p)
        if m and m.group(1).upper() in UFS:
            return m.group(1).upper(), p[:m.start()].strip(' -–(')
        m = re.search(r'\s[-–]\s*(.+?)\s*$', p)
        if m and normalizar(m.group(1)) in ESTADOS:
            return ESTADOS[normalizar(m.group(1))], p[:m.start()].strip()
        return None, p

    # estado: pedaço próprio ("SP", "Santa Catarina") ou grudado na cidade
    for i in range(len(partes) - 1, -1, -1):
        p = partes[i]
        if p.strip().upper() in UFS:
            achado['estado'] = p.strip().upper()
            partes.pop(i)
            break
        if normalizar(p) in ESTADOS:
            achado['estado'] = ESTADOS[normalizar(p)]
            partes.pop(i)
            break
        uf, resto = _uf_no_fim(p)
        if uf:
            achado['estado'] = uf
            partes.pop(i)
            if resto:
                achado['cidade'] = resto
            break
    if not achado['estado']:
        motivos.append('não achei o estado')

    # A mesma rua escrita duas vezes acontece de verdade (planilha preenchida às pressas).
    # Só depois de tirar CEP e estado: em "…, São Paulo, São Paulo, …" os dois iguais são
    # cidade e estado — juntá-los antes apagaria a cidade.
    partes = [p for i, p in enumerate(partes)
              if i == 0 or normalizar(p) != normalizar(partes[i - 1])]

    if not achado['cidade']:
        if len(partes) >= 2:
            achado['cidade'] = partes.pop()
        else:
            motivos.append('não achei a cidade')

    if len(partes) >= 2:
        achado['bairro'] = partes.pop()
    else:
        motivos.append('não achei o bairro')

    achado['endereco'] = ', '.join(partes)
    if not achado['endereco']:
        motivos.append('não sobrou nada para a rua')

    completos = sum(1 for c in ('endereco', 'bairro', 'cidade', 'estado') if achado[c])
    confianca = 'alta' if completos == 4 else 'media' if completos == 3 else 'baixa'
    return {**achado, 'confianca': confianca, 'motivos': motivos}


# ── CPF ───────────────────────────────────────────────────────────────────────

def so_digitos(raw) -> str:
    return re.sub(r'\D', '', str(raw or ''))


def cpf_valido(raw) -> bool:
    """CPF passa no dígito verificador? Aceita com ou sem pontuação.

    Existe porque contrato com CPF errado só é recusado lá na frente — no cartório,
    no banco ou na plataforma de assinatura — quando já foi mandado pro paciente.
    Conferir aqui custa nada.
    """
    d = so_digitos(raw)
    if len(d) != 11 or d == d[0] * 11:
        return False
    for corte in (9, 10):
        soma = sum(int(d[i]) * (corte + 1 - i) for i in range(corte))
        dv = (soma * 10) % 11 % 10
        if dv != int(d[corte]):
            return False
    return True


def arrumar_cpf(raw) -> tuple[str, bool]:
    """Devolve (cpf_em_digitos, foi_corrigido).

    A planilha do Google entrega o CPF como número, e número não guarda zero à
    esquerda: `00123456797` chega como `123456797`. Quem começa com dois zeros
    perde dois. O resultado é um CPF de 9 ou 10 dígitos que reprova na conferência
    e faz parecer que a pessoa digitou errado — quando o dado dela está certo.

    Só repõe os zeros quando isso torna o número válido; se continuar reprovando,
    devolve como veio, porque aí o problema é outro e inventar dígito num documento
    é pior que avisar.
    """
    d = so_digitos(raw)
    if 9 <= len(d) < 11:
        completo = d.zfill(11)
        if cpf_valido(completo):
            return completo, True
    return d, False


def formatar_cpf(raw) -> str:
    d = so_digitos(raw)
    return f'{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}' if len(d) == 11 else str(raw or '')


# ── dinheiro ──────────────────────────────────────────────────────────────────

_UNI = ['', 'um', 'dois', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove']
_DEZ_DEZENOVE = ['dez', 'onze', 'doze', 'treze', 'catorze', 'quinze', 'dezesseis',
                 'dezessete', 'dezoito', 'dezenove']
_DEZENAS = ['', '', 'vinte', 'trinta', 'quarenta', 'cinquenta', 'sessenta',
            'setenta', 'oitenta', 'noventa']
_CENTENAS = ['', 'cento', 'duzentos', 'trezentos', 'quatrocentos', 'quinhentos',
             'seiscentos', 'setecentos', 'oitocentos', 'novecentos']


def _tres_digitos(n: int) -> str:
    if n == 0:
        return ''
    if n == 100:
        return 'cem'
    partes = []
    if n // 100:
        partes.append(_CENTENAS[n // 100])
    resto = n % 100
    if resto:
        if resto < 10:
            partes.append(_UNI[resto])
        elif resto < 20:
            partes.append(_DEZ_DEZENOVE[resto - 10])
        elif resto % 10 == 0:
            partes.append(_DEZENAS[resto // 10])
        else:
            partes.append(f'{_DEZENAS[resto // 10]} e {_UNI[resto % 10]}')
    return ' e '.join(partes)


def _inteiro_extenso(n: int) -> str:
    if n == 0:
        return 'zero'
    milhares, resto = n // 1000, n % 1000
    partes = []
    if milhares:
        partes.append('mil' if milhares == 1 else f'{_tres_digitos(milhares)} mil')
    if resto:
        if milhares and (resto < 100 or resto % 100 == 0):
            partes.append(f'e {_tres_digitos(resto)}')
        else:
            partes.append(_tres_digitos(resto))
    return ' '.join(partes)


def numero_extenso(n: int) -> str:
    """3 → 'três'. Para escrever "em 3 (três) parcelas" no contrato."""
    return _inteiro_extenso(int(n))


def extenso_reais(valor: float) -> str:
    cents = round(valor * 100)
    reais, cent = cents // 100, cents % 100
    if reais == 0:
        reais_txt = ''
    elif reais == 1:
        reais_txt = 'um real'
    else:
        reais_txt = f'{_inteiro_extenso(reais)} reais'
    if cent:
        cent_txt = f'{_inteiro_extenso(cent)} ' + ('centavo' if cent == 1 else 'centavos')
        return f'{reais_txt} e {cent_txt}' if reais else cent_txt
    return reais_txt or 'zero reais'


def parse_valor(val) -> float | None:
    """'R$ 1.500,00' / '1.500,00' / 1500 → 1500.0 (formato brasileiro)."""
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val or '').replace('R$', '').replace('r$', '').strip()
    if not s:
        return None
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def formatar_brl(v: float) -> str:
    return 'R$ ' + f'{v:,.2f}'.replace(',', '§').replace('.', ',').replace('§', '.')


# ── datas ─────────────────────────────────────────────────────────────────────

_MESES = ['', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
          'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']


def data_extenso(d) -> str:
    return f'{d.day:02d} de {_MESES[d.month]} de {d.year}'


def normalizar_data(raw) -> str:
    """'17.01.1993', '17011993', '1993-01-17' → '17/01/1993'. O resto volta igual.

    Planilha e digitação escrevem data de todo jeito; o contrato só aceita um.
    """
    s = str(raw or '').strip()
    if not s:
        return ''
    iso = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', s)
    if iso:
        return f'{iso.group(3)}/{iso.group(2)}/{iso.group(1)}'
    d = so_digitos(s)
    if len(d) == 8:
        return f'{d[:2]}/{d[2:4]}/{d[4:]}'
    return s
