---
name: video-maker
description: 'Use quando o usuário pedir pra editar, montar ou finalizar um vídeo ou reel dele, normalmente com os vídeos que acabou de gravar no iPhone ("edita os vídeos de hoje", "monta o reel do diário", "faz o vídeo que gravei agora"); quando pedir pra cortar silêncio, tirar palavras ou trechos da fala, legendar ou juntar telas na metade de cima; quando colar link de TikTok, Instagram ou YouTube pra virar ilustração do reel; ou quando quiser transformar uma aula ou vídeo longo em cortes virais pro Instagram. NÃO use para criar só a animação de um trecho (motion), para anúncio com roteiro anotado ou avatar, para reel de cenas gravadas com trilha (imóvel, tour), nem para colar frases em lote em cortes já prontos.'
---

# Video maker

Edita arquivos de vídeo do usuário e entrega MP4. O padrão é tela dividida:
fala na metade inferior e ilustração na superior. Não acessa Fotos, iCloud,
Google Drive ou Notion do autor. Não inclui mídia dele.

## Configurar antes de começar

Leia e execute [pastas, acesso e limpeza](../../references/arquivos-e-limpeza.md).
Ao retomar um projeto, marque-o em andamento antes de limpar os demais. A limpeza
só remove intermediários registrados, com preferência ativada pelo usuário;
originais, finais e projetos em andamento são preservados. Não deduza descarte pela idade.

Leia [references/configuracao.md](references/configuracao.md). Use as pastas e os
padrões da configuração persistente do plugin. Um `.video-maker.json` do projeto
explicitamente informado prevalece; não o sobrescreva. Sem configuração, confirme
as pastas propostas uma vez, como descrito na referência. Os comandos `scripts/` são relativos
à pasta deste SKILL.md, não ao projeto de vídeo. Use o Python do ambiente isolado
com `scripts/executar.py <script.py> <argumentos>` quando as ferramentas tiverem
sido preparadas pelo instalador incluído.

Por padrão, headline inicial e sem legenda dinâmica. O pedido atual e as escolhas
salvas pelo usuário prevalecem. O modelo de transcrição é Whisper large-v3-turbo:
MLX em Mac compatível, faster-whisper local em CPU nos demais ambientes. Informe
o backend usado; não prometa resultados idênticos entre os dois. Os tempos são
apoio; a conferência auditiva continua obrigatória para declarar a fala revisada.

Guarde os arquivos de trabalho em uma subpasta nova de `pastas.trabalho` e a final
aprovada em `pastas.saida`. Nunca substitua uma versão existente. Os scripts podem
sobrescrever um caminho de saída: escolha um nome novo antes de executá-los.

## Reel de um tema

1. **Achar os vídeos.** Use os arquivos fornecidos ou a pasta `pastas.entrada` da configuração. Confira cada vídeo com ffprobe e uma folha de contato. Mostre a lista (nome, duração e conteúdo) e confirme quais entram antes de planejar; não use vídeos pessoais por suposição. Observe enquadramento e espelhamento; `--espelhar` em `cortar_trechos.py` só quando necessário.

2. **Transcrever a fala:** `python3 scripts/transcrever.py <fala> <pastas.transcricoes>/<tema>-<versao>.json`. Gera também o `.md` com tempos; preserve ambas as versões na pasta externa de transcrições. O cache só é reutilizado quando fonte, trecho e processamento coincidem. Use esse caminho no plano e na legenda; não suponha que a transcrição esteja no trabalho.
3. **Limpar a fala, só se ele pedir.** Pra tirar silêncio, leia [references/silencio.md](references/silencio.md). Pra tirar palavras pelo texto, leia [references/edicao-por-texto.md](references/edicao-por-texto.md). Se a fala for uma gravação bruta, com a mesma frase repetida em várias tentativas, leia [references/gravacao-bruta.md](references/gravacao-bruta.md). Daí em diante, use a transcrição do vídeo limpo.
4. **Planejar com ele.** Mostre uma tabela com tempo no reel, frase dele e o que aparece em cima. Inclua a última palavra (o corte final), onde entra motion e onde fica tela cheia. Espere o ok. Leia [references/tela-dividida.md](references/tela-dividida.md).
5. **Ilustrações.** As telas são os outros vídeos que ele gravou. Motion vem da skill `motion-designer`: passe a frase e a duração exata do trecho, e ela sai em 1080×960. Link de TikTok ou Instagram: leia [references/baixar.md](references/baixar.md).
6. **Headline e legenda:** leia [references/legenda.md](references/legenda.md). O vídeo é de IA (padrão, destaque dourado) ou de nutrição (verde).
7. **Montar:** `python3 scripts/montar.py <trabalho>/plano.json`. Faz uma passada só; inclua `legenda` no plano somente quando ela foi pedida.
8. **Conferir e entregar** (abaixo).

Aula longa que vira cortes pro Instagram: leia [references/cortes-virais.md](references/cortes-virais.md).

## Conferir antes de entregar

- **Fala e imagem têm conferências diferentes.** Em gravação com tentativas, cumprir a [conferência da fala](references/gravacao-bruta.md#conferencia-da-fala) antes de chamar o corte de revisado. Uma transcrição limpa não prova ausência de sílaba repetida; imagens a cada 0,05 s não verificam som.
- A duração do MP4 bate com o plano.
- Folha de contato do reel (`python scripts/folha.py reel.mp4 folha.png 0 "" 2`) e tiras de 0,05 s em volta de cada emenda. Abra as imagens e olhe de verdade:
  - nenhum quadro preto nem cena parada;
  - ninguém com a cabeça cortada;
  - legenda legível (a sombra escura atrás segura a leitura até sobre fundo claro).
- Quadro 0 da metade de cima: extraia o primeiro quadro do reel, recorte os 1080×960 de cima e olhe. Tem de aparecer a ilustração, nunca papel vazio ou tela escura (regra de 19/10/2026, abaixo). Se não aparecer, a cena de abertura volta pra `motion-designer` ou o clipe é recortado de novo a partir de um quadro com conteúdo.
- Transcreva os últimos 4 s como apoio à checagem da palavra final. Isso não substitui a conferência de todos os trechos, emendas e vídeo integral.

## Entregar

Cada versão vai só na conversa: mande o MP4, explique em 2 ou 3 linhas o que aparece em cada parte e pergunte o que ajustar. Se ele pedir uma versão leve pro celular, faça em 720×1280 com crf 28.

Em cortes de gravação bruta, `conferencia_fala.py verificar` precisa terminar sem pendências para declarar a fala revisada. Com pendência, o arquivo é **rascunho**, com o item que falta explicitado; não diga que ouviu ou conferiu a fala usando apenas Whisper, quadros ou detecção de silêncio. Quando não houver recurso para escuta direta nesta sessão, continue os cortes e verificações possíveis, prepare os áudios de revisão e entregue o rascunho com essa limitação. Não preencha declaração de escuta por inferência.

Depois da aprovação explícita, copie a final para `pastas.saida` sem mover nem apagar originais. Não importe para álbuns nem acesse bibliotecas pessoais.
Abra a pasta de saída com `scripts/acesso.py` da raiz do plugin e entregue o link
do arquivo. Só marque o projeto como concluído quando o usuário encerrar o trabalho,
conforme a referência de pastas e limpeza.

## Padrões visuais da skill (as escolhas do usuário prevalecem)

- Tela de cima em largura cheia, sem faixas desfocadas nas laterais.
- Legenda sobre o vídeo de cima, logo acima da divisão. Visual limpo, sem efeito além do pulo de entrada.
- Fechar em tela cheia nele funciona bem.
- No reel do diário, com antes e depois, ele preferiu o resultado ("depois") primeiro. Sugira essa ordem.
- A cor do vídeo dele não muda. O iPhone grava em HDR; `cortar_trechos.py` e `montar.py` já convertem.
- A ilustração entra na palavra que ela mostra: o picolé aparece em "picolé", o café da manhã em "seguiu o café da manhã".
- Desde o quadro 0, a metade de cima já mostra imagem (19/10/2026: "PRECISO que desde o segundo zero apareça alguma imagem"). Vale pra motion, tela gravada ou vídeo de link: nada abre com papel vazio, tela escura ou animação nascendo do nada. Vídeo baixado ou recortado começa num quadro com conteúdo, sem a abertura escura da fonte.
