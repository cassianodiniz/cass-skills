# Configuração local da Video Maker

Leia antes da primeira edição. Esta distribuição trabalha apenas com arquivos
locais: não contém integração com Fotos, iCloud ou banco Notion do autor.
Leia [a configuração persistente](../../../CONFIGURACAO.md). Rode
`python scripts/configurar.py carregar` para obter pastas e padrões. A configuração
central mora fora do plugin e é reutilizada após atualizações. Para novas
instalações, os padrões são Originais, Prontos, Projetos, Transcrições e Aulas
em Vídeos/Filmes → Cass Skills. Pastas anteriores são preservadas. Não escolha o primeiro arquivo
por ordem: liste candidatos e confira nome, conteúdo e duração.

Quando o usuário indicar explicitamente um projeto com `.video-maker.json`, use
`python scripts/configurar.py carregar --projeto <projeto>`: esse arquivo tem
precedência e seus caminhos relativos são resolvidos pelo projeto. Arquivo inválido
é erro; não passe silenciosamente à configuração central. Nunca sobrescreva uma
configuração anterior só porque a sessão ou o plugin mudou.

## Salvar e usar

Grave o JSON do prompt em um arquivo temporário e rode, da pasta da skill,
`python scripts/configurar.py salvar --projeto <projeto> --dados <json>`.
O script valida os dados e guarda a configuração anterior. Não cria pastas de
mídia. Caminhos relativos em `pastas` são relativos ao projeto que contém a
configuração. Crie uma pasta nova por tema em `pastas.trabalho` e guarde nela
plano, versões e conferências. Transcrições JSON/MD ficam em `pastas.transcricoes`, com tema/versão e referência para o arquivo de origem; o plano aponta para elas. Nunca sobrescreva vídeo existente.

| Campo | Uso |
|---|---|
| `sistema` | Declarado pelo usuário; confirme o ambiente real. |
| `origem` e `entrega` | Sempre `pasta`; não acessar biblioteca Fotos. |
| `perfil` | `ia`: dourado; `nutricao`: verde, passar `--nutricao` nos scripts de texto. |
| `headline` | Criar ou dispensar a sobreposição inicial. |
| `legendas` | Desligadas por padrão; criar quando configurado ou pedido no vídeo atual. |
| `perfil_instagram` | Usar só quando ele pedir CTA de seguir; vazio significa sem @ configurado. |
| `pastas` | Entrada, trabalho, saída, aulas e transcrições escolhidas pelo usuário. |

Pedido explícito no vídeo atual substitui o padrão só naquele vídeo. Rascunhos
ficam no trabalho; a pasta de saída recebe a versão aprovada, entregue também
na conversa. Não mover nem apagar originais.

## Ferramentas incluídas e preparação

O pacote leva scripts, fontes e um instalador das ferramentas. Os executáveis
FFmpeg/FFprobe e os modelos de transcrição são grandes e específicos de cada
sistema; são baixados no computador do usuário, não embutidos no `.skill`.

Antes, atualize as cópias externas com `preparar-instaladores` de CONFIGURACAO.md (não instala programas nem redefine suas escolhas). Com instalação autorizada, rode Python 3.10+:
`python <instaladores>/instalar_video.py --destino <ferramentas>/video-maker
--transcricao`, com os caminhos retornados pela configuração. A cópia do instalador
fica na pasta externa e versões anteriores são preservadas. O comando também existe
no pacote em `scripts/instalar_ferramentas.py`, sempre com destino externo. Cria um ambiente isolado, instala Pillow/NumPy e baixa
FFmpeg/FFprobe via static-ffmpeg; `--transcricao` inclui faster-whisper.
Não pede senha e não altera o PATH global. Python precisa existir antes; se
faltar, explique e ofereça instalação conforme as permissões do usuário.

Execute os scripts com o Python desse ambiente:
- Windows: `<ferramentas>/video-maker/Scripts/python.exe`.
- Mac/Linux: `<ferramentas>/video-maker/bin/python`.

Passe `scripts/executar.py <script.py> <argumentos>` a esse Python. O launcher
põe FFmpeg/FFprobe no PATH somente do processo e carrega os scripts da skill.
Exemplo: `<python-do-ambiente> scripts/executar.py montar.py <plano.json>`.
`configurar.py verificar` informa presença de ferramentas, não prova funcionamento.
Confirme também FFmpeg, FFprobe e o filtro ASS se houver legendas.

## Transcrição local no PC

O modelo permanece Whisper large-v3-turbo. Em Mac com `mlx_whisper` disponível,
o processamento usa MLX. Sem ele, usa faster-whisper/CTranslate2 em CPU int8,
com português e tempos por palavra. A skill informa qual motor executou; o JSON
guarda o motor e não reaproveita cache entre eles. O modelo é baixado no primeiro
uso; o áudio é processado localmente, sem upload. O CPU pode demorar.

Sem transcritor pronto, aceite `fala.json` no formato do script com palavras e
início/fim. Texto simples sem tempos não basta para sincronização automática.
Não substitua o modelo ou envie áudio para serviço externo sem autorização.

## Recursos opcionais e limites

- Motion: skill Motion Designer separada; não é requisito para editar cenas fornecidas.
- Links: use o yt-dlp disponível ou peça o arquivo; não faça login nem colete cookies automaticamente.
- Emoji: o script original usa Apple Color Emoji. Em PC sem essa fonte, crie
  headline sem emoji e explique. As fontes Inter da edição estão incluídas.
- Folha de contato: `python scripts/folha.py <video> <imagem>` funciona sem Bash.
- As bibliotecas usadas suportam Windows, Mac e Linux; os testes locais desta
  distribuição não equivalem a execução validada em todos os sistemas.

Se uma ferramenta falhar, preserve os arquivos e mostre o erro com a alternativa
possível. Em áudio, sem escuta direta, a conferência fica pendente e a entrega é
rascunho. Transcrição ou imagem não comprovam que alguém ouviu a fala.

Depois da versão aprovada ou de um ajuste, informe o resultado e pergunte se o usuário quer ajustar, exportar ou concluir. Um próximo passo já explicitamente pedido deve ser executado sem repetir a mesma autorização.
