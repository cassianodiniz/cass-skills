#!/usr/bin/env python3
"""
Validador determinístico de conteúdo no estilo Cassiano Diniz.
VALIDADOR ÚNICO dos 3 formatos virais (fonte canônica dos limites de char).

Uso:
    python3 validar_cards.py path/to/cards.txt [--formato noticia|card-unico|tela-dividida]

Default: --formato noticia (preserva o comportamento histórico desta skill).
As skills `card-unico` e `tela-dividida` chamam ESTE mesmo script com o --formato delas,
pra existir uma fonte única de regra de estilo e de limite de tamanho.

Formato esperado do arquivo de entrada (markdown simples):

    ## Card 1
    PORQUE FISICULTURISTAS ESTAO FALECENDO...

    ## Card 2
    Frase de cima curta.

    Parágrafo de desenvolvimento embaixo, etc.

Para card-unico, basta um único `## Card 1` com o texto inteiro do card.

Saída zero = passou em tudo (ou só com alertas amarelos). Exit 1 = reprovado. Exit 2 = erro de uso.
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

# Windows: console cp1252 quebra nos emojis do relatório — forçar UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# =============================================================================
# Listas de regras de ESTILO (valem nos 3 formatos) — de references/estilo-cassiano.md
# =============================================================================

PREAMBULOS_INICIO = [
    "vale entender", "vale destacar", "vale lembrar", "vale ressaltar",
    "é importante saber", "e importante saber", "é importante entender", "e importante entender",
    "é importante lembrar", "é importante ressaltar",
    "vamos falar sobre", "vamos entender", "vamos ver",
    "antes de mais nada", "antes de tudo", "antes de falar sobre",
    "primeiro,", "primeiramente",
    "hoje vou te mostrar", "hoje vamos falar",
    "neste post você vai aprender", "neste post vou mostrar",
    "para começar", "pra começar",
]

CONECTORES_FORMAIS = [
    "portanto", "todavia", "ademais", "destarte", "outrossim",
    "em suma", "em síntese", "em sintese",
    "sendo assim", "dessa forma", "desse modo", "desta forma",
    "no entanto", "diante disso", "assim sendo", "por conseguinte",
    "não obstante", "nao obstante",
    "em virtude de", "em vista disso",
]

FRASES_PONTE_VAZIAS = [
    "como vimos", "como visto", "isso significa que", "isso quer dizer que",
    "ou seja,", "em outras palavras", "em resumo", "recapitulando",
    "portanto podemos concluir", "podemos concluir que",
]

HEDGING_DADO = [
    "talvez", "parece que", "pode ser que", "acredita-se",
    "supõe-se", "supoe-se",
]

# Pergunta retórica de ENGAJAMENTO (proibida). Atenção: card-unico e tela-dividida TÊM uma
# pergunta-fecho estrutural legítima (inverte percepção / pergunta moral) — essa é permitida
# e não cai nesses padrões.
PERGUNTA_RETORICA_PATTERNS = [
    r"\byou sabia\b", r"\bvocê sabia\b", r"\bvc sabia\b",
    r"\bjá pensou\b", r"\bja pensou\b",
    r"\bo que você acha\b", r"\bo que vc acha\b",
    r"\bjá se perguntou\b",
]

ADJETIVOS_VAZIOS = [
    "muito importante", "extremamente importante",
    "muito perigoso", "extremamente perigoso",
    "super relevante", "super importante",
    "absolutamente", "muitíssimo", "muitissimo",
    "fundamental para sua",
]

AUTO_REFERENCIA = [
    "eu sempre digo", "eu sempre falo",
    "como costumo dizer", "como costumo falar",
    "aprendi que", "como nutricionista costumo",
]

SAUDACOES = [
    "olá pessoal", "ola pessoal", "fala pessoal", "fala galera",
    "tudo bem?", "tudo bom?",
]

AVISO_ESTRUTURA = [
    "neste slide", "no próximo slide", "no proximo slide",
    "confira abaixo", "veremos a seguir",
    "veja abaixo", "veja a seguir",
]

CITACAO_ACADEMICA_PATTERN = re.compile(
    r"\(([A-Z][a-záàâãéêíóôõúç]+)(?:\s+et\s+al\.?)?,?\s+\d{4}[a-z]?\)",
    re.IGNORECASE,
)

# Fontes institucionais reconhecidas pelo público leigo PODEM aparecer no card (funcionam como
# autoridade, não como citação acadêmica). A regra do estilo permite isso explicitamente.
INSTITUICOES_OK = {
    "vigitel", "ibge", "oms", "opas", "anvisa", "datasus", "sus",
    "ministério", "ministerio", "sbc", "sbd", "sbem", "abeso", "who",
    "guia", "vigilância", "vigilancia", "inca", "fiocruz", "conitec",
}

TRAVESSAO_PATTERN = re.compile(r"[–—]")

LIMITE_PALAVRAS_FRASE = 28
# fatal subiu 40->55 (07/09/2026): posts reais de denúncia têm frase de prosa de ~43 palavras
# (DTRX9V, 3.321 curtidas). >28 vira alerta; só >55 de prosa (não-lista) reprova.
LIMITE_PALAVRAS_FRASE_FATAL = 55

# =============================================================================
# FONTE ÚNICA dos limites de char por formato (medidos nos 13 posts reais).
# total: (reprova_min, alvo_min, alvo_max, reprova_max). Fora de [reprova_min, reprova_max] = grave.
# Dentro do alvo = ok. Entre reprova e alvo = alerta amarelo.
# =============================================================================
LIMITS = {
    "noticia": {
        "total": (1300, 1350, 1800, 2400),  # reprova <1300 ou >2400; alvo 1350-1800. Teto de reprova subiu 2200->2400 (07/09/2026): os posts de DENÚNCIA reais vão a ~2.295 (DTRX9V 3.321 curtidas / golpe pirâmide) — o validador não pode reprovar viral real. Acima de 1800 já é alerta.
        "n_cards": (6, 8),                   # alerta se fora (6-8; eixo 7)
        "gancho": (45, 115),                 # card 1 (alerta; medido 49-111)
        "miolo": (150, 510),                 # cards do meio (lista de solução chega a ~510)
        "cta": (130, 280),                   # último card
        "checa_frase_de_cima": True,
        "checa_aberturas": True,
    },
    "card-unico": {
        "total": (140, 180, 320, 400),  # rep_max 380->400: o card-único real mais longo tem 393 car.
        "n_cards": (1, 1),
        "checa_frase_de_cima": False,
        "checa_aberturas": False,
    },
    "tela-dividida": {
        "total": (450, 470, 900, 1150),  # rep_max 950->1150: telas reais mais longas chegam a ~1.126 car. (>900 já é alerta)
        "n_cards": (4, 5),
        "contraste": (50, 330),  # cards de contraste (roll-call curto a pode/não-pode longo)
        "fecho": (140, 310),     # card de fecho/pergunta moral
        "checa_frase_de_cima": False,
        "checa_aberturas": False,
    },
}

# =============================================================================
# Parser
# =============================================================================

WATERMARK = re.compile(r"^\s*(?:@cassiano\.diniz|cassiano diniz)\s*$", re.IGNORECASE)
PAINEL_TELA = re.compile(
    r"^###\s+Parte\s+(esquerda|direita|superior|inferior)\s*$",
    re.IGNORECASE,
)
SUBTITULO_TELA = re.compile(
    r"^\s*(?:\*\*)?Subtítulo:(?:\*\*)?\s*(.+?)\s*$",
    re.IGNORECASE,
)


def strip_watermark(texto: str) -> str:
    """Remove linhas que são só a marca d'água/assinatura (não são conteúdo do card)."""
    return "\n".join(l for l in texto.split("\n") if not WATERMARK.match(l)).strip()


def parse_cards(content: str) -> list[dict]:
    blocos = re.split(r"^##\s+Card\s+(\d+)\s*$", content, flags=re.MULTILINE)
    cards = []
    for i in range(1, len(blocos), 2):
        num = int(blocos[i])
        texto = strip_watermark(blocos[i + 1].strip())
        cards.append({"num": num, "texto": texto})
    return cards


def texto_visivel_tela(texto: str) -> str:
    """Retira rótulos de direção, mas preserva o subtítulo e a copy que vão ao layout."""
    linhas = []
    for linha in texto.split("\n"):
        if PAINEL_TELA.match(linha.strip()):
            continue
        subtitulo = SUBTITULO_TELA.match(linha)
        if subtitulo:
            linhas.append(subtitulo.group(1).strip())
            continue
        linhas.append(linha)
    return "\n".join(linhas).strip()


def quebrar_frases(texto: str) -> list[str]:
    # Quebra por LINHA e por BULLET (cada item de lista é uma unidade própria — não juntar 8 bullets
    # numa "frase" de 80 palavras), depois por pontuação dentro da linha. O bullet "•" costuma vir
    # colado no meio da linha na exportação do design ("peso• Consumir..."); tratamos como separador.
    frases = []
    for linha in texto.split("\n"):
        # bullets e ponto-e-vírgula separam itens de lista (checklist/protocolo de dose)
        for pedaco in re.split(r"[•▪·;]", linha):
            limpo = re.sub(r"^\s*[\-\*]\s*", "", pedaco).strip()
            if not limpo:
                continue
            # split por pontuação: com espaço (letra/dígito); OU colado a maiúscula ("importante).Proteína",
            # "seria:Pressão", "40%Evitar"); OU "%" colado a dígito ("50%150"). Itens de lista/dose costumam
            # vir colados na exportação do design. Não quebra decimais ("1.2") — o caso colado exige maiúscula.
            for f in re.split(
                r"(?<=[.!?])\s+(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ\d])"
                r"|(?<=[.!?:%)])(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ])"
                r"|(?<=%)(?=\d)",
                limpo,
            ):
                f = f.strip()
                if f:
                    frases.append(f)
    return frases


def contar_palavras(frase: str) -> int:
    return len([w for w in re.findall(r"\b\w+\b", frase)])


# =============================================================================
# Checks de estilo (todos os formatos)
# =============================================================================

def _scan(card_num, texto, termos, rotulo, dica):
    out = []
    low = texto.lower()
    for t in termos:
        if t in low:
            out.append(f"  [Card {card_num}] {rotulo}: '{t}' ({dica})")
    return out


def check_preambulos(card_num, frases):
    out = []
    for f in frases:
        fl = f.lower().strip()
        for p in PREAMBULOS_INICIO:
            if fl.startswith(p):
                out.append(f"  [Card {card_num}] PREAMBULO no início: '{f[:80]}...' (entregar o dado, não anunciar)")
                break
    return out


def check_conectores_formais(card_num, texto):
    out = []
    low = texto.lower()
    for c in CONECTORES_FORMAIS:
        if re.search(rf"(?:^|[\.\,\!\?\;\:\s])({re.escape(c)})(?:[\.\,\!\?\;\:\s])", low):
            out.append(f"  [Card {card_num}] AVISO: CONECTOR FORMAL '{c}' (preferir mas/por isso/fazendo/embora; aparece em posts reais, não reprova)")
    return out


def check_hedging(card_num, texto):
    out = []
    low = texto.lower()
    for h in HEDGING_DADO:
        if re.search(rf"\b{re.escape(h)}\b", low):
            out.append(f"  [Card {card_num}] HEDGING: '{h}' (afirmar ou citar fonte direta)")
    return out


def check_pergunta_retorica(card_num, texto):
    out = []
    low = texto.lower()
    for p in PERGUNTA_RETORICA_PATTERNS:
        if re.search(p, low):
            out.append(f"  [Card {card_num}] PERGUNTA RETORICA de engajamento: padrão '{p}' (proibido)")
    return out


def check_citacao_academica(card_num, texto):
    out = []
    for m in CITACAO_ACADEMICA_PATTERN.finditer(texto):
        nome = m.group(1).lower()
        if nome in INSTITUICOES_OK:
            continue  # instituição reconhecida = autoridade permitida, não citação acadêmica
        out.append(f"  [Card {card_num}] AVISO: CITACAO ACADEMICA '{m.group(0)}' — ok em tema técnico (hormônio/dose; ex.: The Rock usa 'Baggish et al., 2017'); em tema geral, mover pra legenda")
    return out


def check_travessao(card_num, texto):
    # Ignora traço entre dígitos (intervalo numérico legítimo: "30–60 min", "1–2x/semana", "3–6 mg").
    # Só o travessão de PROSA (entre palavras/espaços) é o que o estilo do Cassiano evita.
    prosa = re.sub(r"(?<=\d)\s?[–—]\s?(?=\d)", " ", texto)
    return [f"  [Card {card_num}] TRAVESSAO (— ou –) — trocar por vírgula/ponto"] if TRAVESSAO_PATTERN.search(prosa) else []


def check_tamanho_frase(card_num, frases):
    out = []
    for f in frases:
        n = contar_palavras(f)
        if n <= LIMITE_PALAVRAS_FRASE:
            continue
        # lista/checklist colado (várias medidas, ou ";") não é uma frase de prosa — no design são itens
        # separados. Só reprova (grave) prosa REALMENTE longa (>55) que não é lista.
        eh_lista = len(re.findall(r"\d+\s*(?:%|mg|ml|g|kg|mcg|min|/dl|/kg|x8)\b", f, re.I)) >= 2 or ";" in f
        if n > LIMITE_PALAVRAS_FRASE_FATAL and not eh_lista:
            out.append(f"  [Card {card_num}] FRASE LONGA DEMAIS ({n} palavras): '{f[:90]}...' (>{LIMITE_PALAVRAS_FRASE_FATAL}; provável parágrafo colado — quebrar)")
        else:
            out.append(f"  [Card {card_num}] AVISO: frase/bloco longo ({n} palavras): '{f[:70]}...' (direção: máx medido ~34; se for lista/dose, no design são itens separados)")
    return out


def check_frase_de_cima(card_num, texto):
    linhas = [l.strip() for l in texto.split("\n")]
    if len(linhas) < 3:
        return []
    primeira = linhas[0]
    if not primeira or linhas[1].strip() != "":
        return []
    if not any(l for l in linhas[2:]):
        return []
    # Exceção: lead-ins canônicos de card de solução não são rótulo ("O que você pode fazer hoje:",
    # "Adote essas medidas:", "Para evitar..."). Aparecem nos posts reais e são legítimos.
    if re.match(r"^(o que você pode|o que voce pode|adote essas|para (evitar|prevenir)|o que fazer)", primeira.lower()):
        return []
    n = contar_palavras(primeira)
    if n < 8:
        return [f"  [Card {card_num}] AVISO: frase de cima curta ({n} palavras): '{primeira[:60]}' — pode ter virado rótulo (mín ~8)"]
    if n > 18:
        return [f"  [Card {card_num}] AVISO: frase de cima longa ({n} palavras): '{primeira[:60]}...' — pode ter virado parágrafo (máx ~18)"]
    return []


def extrair_primeira_frase(texto):
    for linha in texto.split("\n"):
        linha = linha.strip()
        if linha:
            m = re.match(r"^([^.!?]+[.!?])", linha)
            return m.group(1).strip() if m else linha.strip()
    return ""


def classificar_abertura(frase):
    if not frase:
        return "vazio"
    fl = frase.lower().strip()
    if re.match(r"^(o problema é|pressão alta não|o infarto não|.+ não (dói|acontece|sente))", fl):
        return "negacao"
    if re.search(r"^[A-Za-zçãâê]+ é (quando|um|uma|o|a)\b", frase):
        return "definicao"
    if re.match(r"^[\d]", frase) or re.match(r"^(cerca de \d|aos? \d|mais de \d|hoje \d|cada porção)", fl):
        return "dado_numerico"
    if re.match(r"^(isso|isto|essa|esse|essas|esses|é o que|esses dados)\b", fl):
        return "pronome_retomando"
    if re.match(r"^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]?[a-záàâãéêíóôõúç]*\s+(perdeu|morreu|teve|faleceu|sofreu|passou|recebeu|usou|começou)", frase):
        return "nome_proprio_verbo"
    if re.match(r"^(o|a|os|as|um|uma|essas?|esses?|aos|nos|nas|do|da|dos|das)\s", fl):
        return "sujeito_tematico"
    return "outro"


def check_aberturas_repetidas(cards):
    if len(cards) < 3:
        return []
    miolo = [c for c in cards if c["num"] not in (1, len(cards))]
    aberturas = [(c["num"], classificar_abertura(extrair_primeira_frase(c["texto"])), extrair_primeira_frase(c["texto"])) for c in miolo]
    out = []
    for i in range(1, len(aberturas)):
        na, pa, fa = aberturas[i]
        nb, pb, fb = aberturas[i - 1]
        if pa == pb and pa not in ("outro", "vazio"):
            out.append(f"  [Cards {nb} e {na}] AVISO: abertura repetida (padrão '{pa}') — variar ajuda, mas não é erro fatal")
    return out


# =============================================================================
# Checks estruturais POR FORMATO
# =============================================================================

def check_card_unico(cards):
    """1 card: lista mesma unidade + ordem crescente + pergunta-fecho que inverte percepção."""
    out = []
    if len(cards) != 1:
        out.append(f"  [card-unico] AVISO: esperado 1 card, achei {len(cards)} (o formato é UMA imagem só)")
        return out
    texto = cards[0]["texto"]
    # itens da lista: SÓ linhas que começam com bullet (•/-/*) — evita pegar números do título/cabeçalho
    itens = [l.strip() for l in texto.split("\n") if re.match(r"^\s*[•\-\*]", l) and re.search(r"\d", l)]
    nums = []
    for l in itens:
        m = re.findall(r"(\d+(?:[\.,]\d+)?)", l)
        if m:
            nums.append(float(m[-1].replace(".", "").replace(",", ".")))
    if len(nums) >= 3:
        if nums != sorted(nums):
            out.append("  [card-unico] AVISO: itens podem não estar em ordem CRESCENTE de risco (o golpe é começar no medo pequeno e subir)")
    else:
        out.append("  [card-unico] AVISO: não detectei lista comparativa de 3+ itens com número (é o coração do formato)")
    if "?" not in texto:
        out.append("  [card-unico] AVISO: falta a pergunta-fecho que inverte a percepção de risco (ex: 'estamos nos preocupando com as coisas certas?')")
    return out


def check_tela_dividida(cards, limits):
    """contraste por card + pergunta moral no fecho."""
    out = []
    if not cards:
        return out
    # contraste: ao menos metade dos cards de miolo tem marca de dois lados
    contraste_marcas = re.compile(r"(pode no brasil|não pode|nao pode|vs\.?|x ci[eê]ncia|de um lado|do outro|faleceu aos|antes e depois|permitido|proibido)", re.IGNORECASE)
    miolo = cards[:-1] if len(cards) >= 2 else cards
    def tem_par_estruturado(card):
        nomes = set(_paineis_tela(card["texto"]))
        return nomes in ({"esquerda", "direita"}, {"superior", "inferior"})

    com_contraste = sum(
        1 for c in miolo
        if tem_par_estruturado(c) or contraste_marcas.search(texto_visivel_tela(c["texto"]))
    )
    if com_contraste == 0:
        out.append("  [tela-dividida] AVISO: nenhum card de miolo tem par ESPELHADO claro (pode/não pode, fama/ciência, nome/faleceu). A simetria é o recurso do formato")

    # Detecta subtipo ROLL-CALL: 3+ cards com "faleceu/morreu aos N"
    morte = re.compile(r"\b(faleceu|morreu)\s+aos?\s+\d", re.IGNORECASE)
    n_mortes = sum(1 for c in cards if morte.search(c["texto"]))
    eh_rollcall = n_mortes >= 3

    if eh_rollcall:
        # SEGURANÇA EDITORIAL: post com mortes reais nomeadas precisa de ressalva de causa não comprovada.
        texto_todo = " ".join(texto_visivel_tela(c["texto"]) for c in cards).lower()
        ressalva = re.compile(r"(não sabemos|nao sabemos|não se sabe|nao se sabe|não está confirmad|nao esta confirmad|sem saber a causa|a causa não|a causa nao|não foi confirmad)")
        if not ressalva.search(texto_todo):
            out.append("  [tela-dividida] RESSALVA EDITORIAL FALTANDO: roll-call com mortes reais nomeadas precisa de uma ressalva de causa não comprovada ('Não sabemos qual foi a causa de X'). Sem isso vira abutre — Cassiano não publica assim. (revisar à mão; o validador não sabe se a causa é pública)")
        # roll-call NÃO fecha com pergunta — não cobrar pergunta moral aqui.
    else:
        # fecho com pergunta moral (alerta — alguns fechos reais terminam em afirmação + CTA, ex: post Virgínia)
        if "?" not in texto_visivel_tela(cards[-1]["texto"]):
            out.append("  [tela-dividida] AVISO: o card final costuma fechar com pergunta moral em aberto ('quem está sendo protegido, afinal?'); confira se a afirmação atual segura o mesmo peso")
    # por-card range
    lo_c, hi_c = limits.get("contraste", (0, 9999))
    lo_f, hi_f = limits.get("fecho", (0, 9999))
    for idx, c in enumerate(cards):
        n = len(texto_visivel_tela(c["texto"]))
        ultimo = (idx == len(cards) - 1)
        lo, hi = (lo_f, hi_f) if ultimo else (lo_c, hi_c)
        if n < lo or n > hi:
            papel = "fecho" if ultimo else "contraste"
            out.append(f"  [Card {c['num']}] AVISO: {n} chars fora da faixa {papel} {lo}-{hi}")
    return out


def _paineis_tela(texto: str) -> dict[str, list[str]]:
    paineis: dict[str, list[str]] = {}
    atual = None
    for linha in texto.split("\n"):
        marcador = PAINEL_TELA.match(linha.strip())
        if marcador:
            atual = marcador.group(1).lower()
            paineis.setdefault(atual, [])
        elif atual is not None:
            paineis[atual].append(linha)
    return paineis


def check_estrutura_tela(cards):
    """Exige que a copy declare a geometria e o subtítulo de cada painel."""
    out = []
    # Copy em texto puro (transcrição, rascunho de conteúdo) não tem a geometria de painel — que é
    # scaffolding de AUTORIA pro Canva, não conteúdo. Não reprovar: um viral real transcrito sem
    # '### Parte ...' continua sendo copy válida. Só avisa uma vez pra declarar antes do Canva.
    if not any(_paineis_tela(c["texto"]) for c in cards):
        return ["  [tela-dividida] AVISO: copy sem geometria de painel declarada — adicionar '### Parte esquerda/direita' + '**Subtítulo:**' de cada lado antes de montar no Canva"]
    for card in cards:
        paineis = _paineis_tela(card["texto"])
        nomes = set(paineis)
        horizontal = {"esquerda", "direita"}
        vertical = {"superior", "inferior"}
        if nomes not in (horizontal, vertical):
            out.append(
                f"  [Card {card['num']}] PAINÉIS AUSENTES OU INCOMPLETOS: declarar "
                "'### Parte esquerda' + '### Parte direita' (padrão), ou "
                "'### Parte superior' + '### Parte inferior'"
            )

        alvos = nomes if nomes else {"esquerda", "direita"}
        for nome in sorted(alvos):
            linhas = paineis.get(nome, [])
            if not any(SUBTITULO_TELA.match(linha) for linha in linhas):
                out.append(
                    f"  [Card {card['num']}] SUBTÍTULO AUSENTE na parte {nome}: "
                    "usar '**Subtítulo:** <texto>'"
                )
    return out


def check_fragmentacao_tela(card_num, texto):
    """Bloqueia rajadas artificiais de microfrases no corpo, sem punir subtítulos curtos."""
    sequencia = []
    achadas = []

    def fechar_sequencia():
        nonlocal sequencia
        if len(sequencia) >= 2:
            achadas.extend(sequencia)
        sequencia = []

    for linha in texto.split("\n"):
        limpo = linha.strip()
        if not limpo or PAINEL_TELA.match(limpo) or SUBTITULO_TELA.match(limpo):
            fechar_sequencia()
            continue
        palavras = contar_palavras(limpo)
        if 1 <= palavras <= 3 and re.search(r"[.!?]$", limpo):
            sequencia.append(limpo)
        else:
            fechar_sequencia()
    fechar_sequencia()

    if not achadas:
        return []
    trecho = " / ".join(achadas[:4])
    return [
        f"  [Card {card_num}] MICROFRASES EM SEQUÊNCIA: '{trecho}' "
        "(juntar a ideia em frase/bloco semântico; subtítulos curtos continuam permitidos)"
    ]


def check_total_chars(cards, limits, formato):
    total = sum(
        len(texto_visivel_tela(c["texto"])) if formato == "tela-dividida" else len(c["texto"])
        for c in cards
    )
    rep_min, alvo_min, alvo_max, rep_max = limits["total"]
    out = []
    grave = False
    if total < rep_min:
        out.append(f"  TOTAL {total} chars: abaixo do mínimo {rep_min} — raso demais, ampliar")
        grave = True
    elif total > rep_max:
        out.append(f"  TOTAL {total} chars: acima do máximo {rep_max} — cortar gordura")
        grave = True
    elif total < alvo_min:
        out.append(f"  AVISO: TOTAL {total} chars abaixo do ALVO {alvo_min}-{alvo_max} (passa; comprimento não prediz alcance — não puxar artificialmente pra baixo)")
    elif total > alvo_max:
        out.append(f"  AVISO: TOTAL {total} chars acima do ALVO {alvo_min}-{alvo_max} (passa; cortar apenas frase que não carrega dado)")
    return total, out, grave


def check_n_cards(cards, limits):
    lo, hi = limits["n_cards"]
    n = len(cards)
    if n < lo or n > hi:
        return [f"  AVISO: {n} cards (faixa típica do formato: {lo}-{hi})"]
    return []


# =============================================================================
# Runner
# =============================================================================

def validar(path: Path, formato: str) -> int:
    if formato not in LIMITS:
        print(f"ERRO: formato '{formato}' inválido. Use: {', '.join(LIMITS)}")
        return 2
    if not path.exists():
        print(f"ERRO: arquivo não encontrado: {path}")
        return 2

    limits = LIMITS[formato]
    content = path.read_text(encoding="utf-8")
    cards = parse_cards(content)
    if not cards:
        print("ERRO: nenhum card encontrado. Formato esperado: '## Card N' como cabeçalho.")
        return 2

    violacoes = []
    alertas = 0
    graves = 0

    def add(items):
        nonlocal alertas, graves
        for v in items:
            violacoes.append(v)
            if "AVISO" in v:
                alertas += 1
            else:
                graves += 1

    for c in cards:
        texto_analise = texto_visivel_tela(c["texto"]) if formato == "tela-dividida" else c["texto"]
        frases = quebrar_frases(texto_analise)
        add(check_preambulos(c["num"], frases))
        add(check_conectores_formais(c["num"], texto_analise))
        add(_scan(c["num"], texto_analise, FRASES_PONTE_VAZIAS, "AVISO: FRASE-PONTE VAZIA", "enxugar — não carrega dado; mas aparece em posts reais, não reprova"))
        add(check_hedging(c["num"], texto_analise))
        add(check_pergunta_retorica(c["num"], texto_analise))
        add(_scan(c["num"], texto_analise, ADJETIVOS_VAZIOS, "ADJETIVO VAZIO", "cortar"))
        add(_scan(c["num"], texto_analise, AUTO_REFERENCIA, "AUTO-REFERENCIA", "cortar"))
        add(_scan(c["num"], texto_analise, SAUDACOES, "SAUDACAO", "proibido"))
        add(_scan(c["num"], texto_analise, AVISO_ESTRUTURA, "AVISO DE ESTRUTURA", "meta-conteúdo proibido"))
        add(check_citacao_academica(c["num"], texto_analise))
        # card-unico legitimamente usa "–" como separador de lista; e é lista, não prosa,
        # então pula travessão e tamanho-de-frase nesse formato.
        if formato == "noticia":
            # travessão de prosa é regra da NOTÍCIA; tela e card usam "–" como separador estrutural
            add(check_travessao(c["num"], texto_analise))
        if formato != "card-unico":
            add(check_tamanho_frase(c["num"], frases))
        if limits.get("checa_frase_de_cima"):
            add(check_frase_de_cima(c["num"], texto_analise))

    total, vc, grave_total = check_total_chars(cards, limits, formato)
    add(vc)
    add(check_n_cards(cards, limits))
    if limits.get("checa_aberturas"):
        add(check_aberturas_repetidas(cards))
    if formato == "card-unico":
        add(check_card_unico(cards))
    elif formato == "tela-dividida":
        add(check_estrutura_tela(cards))
        for c in cards:
            add(check_fragmentacao_tela(c["num"], c["texto"]))
        add(check_tela_dividida(cards, limits))

    print("=== VALIDADOR — estilo Cassiano Diniz ===")
    print(f"Arquivo: {path}")
    print(f"Formato: {formato}")
    print(f"Cards: {len(cards)} | Total chars: {total} (alvo {limits['total'][1]}-{limits['total'][2]})")
    print()

    if not violacoes:
        print("✅ PASSOU — nenhuma violação. Pronto.")
        return 0

    print(f"⚠️  {graves} grave(s) + {alertas} alerta(s):\n")
    for v in violacoes:
        print(v)
    print()
    if graves > 0:
        print(f"❌ REPROVADO — corrigir {graves} violação(ões) grave(s).")
        return 1
    print("⚠️  PASSOU COM RESSALVAS — só alertas amarelos, revisar caso a caso.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Validador de conteúdo estilo Cassiano (3 formatos).")
    ap.add_argument("arquivo")
    ap.add_argument("--formato", default="noticia", choices=list(LIMITS.keys()))
    args = ap.parse_args()
    sys.exit(validar(Path(args.arquivo), args.formato))


if __name__ == "__main__":
    main()
