---
name: motion-designer
description: 'Use quando o usuário pedir motion graphics, animação explicativa ou vídeo ilustrativo para um trecho de fala, na metade superior de um reel ou em tela cheia; também ao enviar fala, vídeo com início e fim ou print de uma ferramenta (como um chat de IA) para animar. Não use para editar o reel completo, colocar legendas na fala, montar carrossel, story, apresentação, página ou PDF.'
---

# Motion designer

© 2026 Cassiano Diniz. Skill criada por [Cassiano Diniz](https://instagram.com/cassiano.diniz).

Crie motion graphics que tornem uma fala mais fácil de entender. Mostre a coisa acontecendo — tela, objeto, fluxo ou diagrama — em vez de repetir a frase que a pessoa já está falando. Priorize composição, contraste, movimento com propósito e leitura no celular.

Serve para explicar conceitos técnicos (por exemplo, como uma IA se comporta) e de saúde (órgãos, estruturas anatômicas e processos fisiológicos). O padrão é um vídeo ilustrativo na metade de cima de um reel, enquanto o apresentador fala na metade de baixo. Não promete um número de visualizações.

## Entrada e ambiente

Leia e execute [pastas, acesso e limpeza](../../references/arquivos-e-limpeza.md):
novos trabalhos usam Projetos na pasta Vídeos/Filmes, com os MP4s aprovados em
Prontos. Ao retomar, marque o projeto em andamento antes de limpar os demais.
Limpeza exige a preferência do usuário e preserva originais, finais e trabalhos ativos.

Use a fala e a duração já fornecidas. Se faltarem tema ou tempo, faça até três perguntas curtas, com uma sugestão concreta: o que ilustrar, duração e formato. Não invente o tema. Exemplo: “Pode colar a fala e dizer quantos segundos ela dura? Sugiro um motion mudo para a metade superior, 1080×960.”

Antes de criar arquivos, leia [configuração persistente](../../CONFIGURACAO.md), reutilize as pastas externas e confira as ferramentas disponíveis. Este fluxo usa HTML + GSAP + HyperFrames, Node.js 22 ou superior e, para MP4 e conferência, FFmpeg com FFprobe. Funciona com scripts Node em macOS, Linux e Windows; a transcrição opcional com MLX exige ambiente compatível. Uma conversa sem arquivos ou terminal pode ajudar no briefing e roteiro visual, mas deve explicar que a execução precisa de um agente com essas ferramentas. Não declare HTML ou MP4 criado sem o arquivo correspondente.

Os comandos abaixo partem da pasta desta skill. Resolva essa pasta a partir do `SKILL.md` carregado; não suponha caminhos de uma pessoa ou de outro repositório. O pacote inclui scripts, base HTML, GSAP, fontes, vetor auxiliar, as seis imagens de `assets/fisiologia/` e os dois exemplos de estilo de `references/estilo/`. Capturas de interfaces de IA não fazem parte dele: o usuário fornece os prints.

Antes de compor qualquer cena, leia `references/estilo.md`: é a receita de desenho, com os dois exemplos aprovados.

## Régua visual

| Item | Padrão |
|---|---|
| Tamanho | 1080×960, metade superior. 1080×1920 quando o pedido for tela cheia ou a cena precisar de espaço. |
| Duração | Exatamente o trecho de fala. Últimos 0,4 s com os elementos principais parados. |
| Som e assinatura | Mudo, sem logo de assinatura, @ promocional ou marca-d'água; entram na edição do reel. |
| Paleta | Use a identidade fornecida. Sem identidade: papel `#F5F2EA`, verde `#009348`, coral `#E2603F`, tinta `#111511`, carvão `#141A16`; em tema de IA, destaque dourado `#EFA819` para marcar texto. Contorno sobre imagem/objeto usa vermelho `#FF3B30` com brilho. Preserve as cores que identificam estruturas na referência anatômica. |
| Fundo | Tema de IA ou técnico: fundo escuro limpo ou a cor da própria tela mostrada. Saúde e aula: papel claro. |
| Texto | Sem headlines ou legenda adicional. Texto só dentro de tela real (chat, menu, painel) ou rótulos presentes na referência anatômica, em português, legíveis quando reduzidos a 360 px de largura. |
| Preenchimento | Elementos ocupando o quadro, em tamanho consistente. Sobrou área vazia, aproxime a câmera ou aumente o elemento. |
| Anotação à mão | Círculo, sublinhado ou seta contornam o bloco de texto inteiro a pelo menos 24 px das letras. Cada marca diz alguma coisa; enfeite solto não entra. |
| Ritmo | No máximo 2,5 s no mesmo enquadramento; varie plano, ângulo ou zoom conforme a fala. |
| Exemplos | Neutros, pertinentes à saúde, sem assumir o negócio do usuário. Ex.: “Ilustre o trajeto dos alimentos no sistema digestório”. |

**Tela de IA ou de app.** A estrutura da tela (barras, botões, caixa de mensagem, textos fixos) é a do print real fornecido pelo usuário; o estilo do motion vale só para o que acontece dentro dela (pessoas, imagens geradas, anotações). Antes de desenhar, escreva `print aberto: <arquivo>` para cada tela. Sem print daquele app naquele aparelho (celular ou computador), peça um ao usuário em vez de desenhar de memória. Celular inclinado: tudo da tela fica dentro do mesmo grupo do celular, para texto e botões inclinarem junto. Erro de IA: pedido plausível e resposta errada de um jeito que se entende na hora, com destaque no instante do erro.

Print de post mantém o cabeçalho real (foto, @ e selo) visível desde o primeiro quadro e durante o primeiro zoom. Anime a câmera sobre o print e os destaques na palavra falada; não reconstrua um cabeçalho ampliado por cima.

Antes de ilustrar órgãos ou fisiologia, leia `assets/fisiologia/REFERENCIAS.md`, escolha a imagem pelo conteúdo e abra o JPEG correspondente. A biblioteca cobre rins, olho, visão geral dos órgãos, sistema digestório, comparativo de cirurgias bariátricas e vaso com placa/obstrução. Use as imagens como referência de anatomia, composição e relações entre estruturas. São esquemas pequenos, sem fonte bibliográfica indicada: não constituem validação clínica. Para cenas grandes, reconstrua o esquema com vetores/elementos da composição em vez de ampliar o JPEG. Se a estrutura necessária não estiver nas referências, peça uma referência ao profissional ou proponha um diagrama conceitual identificado como tal.

Pessoa real citada: use mídia real fornecida ou autorizada em cartão 3D. Primeira aparição leve e quase parada; depois, movimento e elementos ao redor. Vídeos usados pelo HyperFrames devem estar em 8 bits (`yuv420p`); converta HDR com tratamento de cor apropriado antes de usar. Vetor auxiliar: `assets/vetores/brasil.json` (`{viewBox, locations:[{name, path}]}`), quando a cena precisar dele.

## Criar e revisar

1. **Alinhe a fala.** Se recebeu vídeo + início/fim, procure uma transcrição já fornecida. Se não houver e `mlx_whisper` estiver disponível em ambiente compatível, use `node scripts/trecho.mjs <video> <inicio> <fim> <pasta-fala>` (segundos ou `mm:ss`). Ele mantém Whisper MLX local, com português e tempo por palavra. Se o transcritor faltar ou falhar, informe e peça o texto do trecho; não substitua por serviço pago ou envie o vídeo para fora sem autorização. A fala escrita com duração basta para criar.

2. **Prepare a composição.** Use `node scripts/novo.mjs <pasta-saida> <duracao-segundos>`; acrescente `tela-cheia` para 1080×1920. Escolha uma pasta nova no projeto do usuário. O script copia base, fontes e GSAP; não sobrescreve uma pasta existente. Se falhar, corrija o caminho ou a duração e tente novamente.

3. **Desenhe o motion.** Edite o `index.html` criado. A base já registra `window.__timelines["main"]` e as dimensões. Use GSAP pausado e tempos explícitos. Leia `references/hyperframes.md` antes de animar: estados iniciais em t=0, `immediateRender:false` nas animações posteriores do mesmo elemento e centralização por `xPercent` em elementos que recebem transformações. Use as fontes em `assets/fontes/` pela base copiada, carregando apenas as necessárias. Se usar uma das imagens de fisiologia na composição, copie o JPEG para a pasta do motion e use um caminho relativo.

4. **Confira e entregue o HTML primeiro.** Use o HyperFrames da pasta externa `ferramentas/motion-designer`. Se faltar, leia CONFIGURACAO.md para atualizar as cópias externas com `preparar-instaladores`, peça autorização para a instalação e execute o instalador: `node <instaladores>/instalar_motion.mjs --destino <ferramentas>/motion-designer`. Ele mantém o HyperFrames 0.7.56 definido no pacote, sem instalar dentro da skill. O navegador usado pelo motor também deve ficar no cache externo do usuário. Não reinstale programas apenas porque o plugin mudou. Se Node, FFmpeg ou navegador necessário não estiverem disponíveis, explique o que falta e preserve o projeto. Rode `node scripts/hyperframes.mjs check <pasta-saida> --json` e `node scripts/hyperframes.mjs snapshot <pasta-saida> --frames 6 --describe false`. Se houver erros, corrija e repita, no máximo três rodadas. Abra e olhe os quadros e uma redução a 360 px: sem cortes, sobreposições ou texto ilegível. Entregue HTML **e seus arquivos locais** juntos, ou ZIP, com 2–3 linhas sobre o que ilustra. Pergunte: “Autoriza criar o MP4 ou prefere ajustar algo?” Se a autorização já tiver sido dada explicitamente para esta composição, prossiga.

5. **Após autorização, renderize.** Use `node scripts/render.mjs <pasta-saida>`. Ele roda a verificação, renderiza MP4 a 30 fps, verifica tamanho/duração/ausência de áudio e extrai quadros em `conferir/`. Abra `folha.png` e `celular_*.png`: a conferência final é sobre o MP4, porque preview e render podem divergir. Se houver defeito, preserve o MP4 anterior no caminho registrado, ajuste a composição e renderize uma nova versão com outro nome, no máximo três renders. O script recusa substituir um MP4 existente. Ao atingir o limite, entregue o estado real e explique a pendência, sem chamar o resultado de aprovado.

## Falhas que merecem atenção

- GSAP ou fonte não carrega: confira os caminhos relativos no projeto e entregue os arquivos junto do HTML.
- HyperFrames não encontrado: prepare o ambiente externo autorizado ou indique a limitação; não troque o motor silenciosamente.
- Sem MLX: use a fala fornecida. O restante do fluxo não depende da transcrição.
- Sem referência da estrutura anatômica necessária: peça uma referência ao profissional ou use um diagrama conceitual acordado.
- Movimento no final, cena ausente ou texto pequeno: confira os quadros do MP4 e corrija antes da entrega final.

Exemplo de pedido suficiente: “Ilustre o trajeto dos alimentos no sistema digestório, durante 7 s, na metade de cima.” Use `assets/fisiologia/sistema-digestorio__visao-geral.jpeg` como referência para o percurso visual; não escreva essa fala como título. Entregue a composição revisável antes de gerar o MP4.

Motion longo (mais de 15 s): entregue primeiro uma cena-piloto pelo passo 4; com ela aprovada, siga o mesmo padrão nas outras.
