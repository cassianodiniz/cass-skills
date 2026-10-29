# Configuração que permanece após atualizar

As instruções e scripts distribuídos ficam no plugin. As escolhas e o trabalho do
usuário ficam fora dele. Resolva `scripts/smart_config.py` a partir da raiz deste
plugin; comandos abaixo partem dessa raiz.

1. Rode `python scripts/smart_config.py ler`. Configuração válida: reutilize sem
   perguntar tudo de novo. Falta de configuração: siga o próximo passo. Arquivo
   inválido: mostre o erro e peça correção; não crie outra configuração silenciosa.
2. Rode `python scripts/smart_config.py propor`. Mostre a pasta-base sugerida e
   confirme com o usuário uma única vez, permitindo escolher outra pasta com
   `propor --base <pasta-absoluta>`. No Windows, confira se Documentos é redirecionado
   ao OneDrive; não confunda pastas de nomes iguais. Ainda não cria nada.
3. Guarde a proposta confirmada em um JSON temporário e execute
   `python scripts/smart_config.py salvar --dados <json>`. A configuração fica em
   `~/.cass-smart-skills/config.json`. O script cria somente as pastas escolhidas,
   guarda backup de mudanças e não move/apaga arquivos anteriores.

Padrões propostos, ajustáveis pelo usuário:

| Conteúdo | Pasta |
|---|---|
| Posts e estado por versão | `<base>/posts-instagram/` |
| Pesquisas e fontes | `<base>/pesquisas/` |
| Vídeos recebidos | `<base>/videos/brutos/` |
| Versões aprovadas | `<base>/videos/editados/` |
| Planos e rascunhos | `<base>/videos/trabalho/` |
| Transcrições reutilizáveis | `<base>/videos/transcricoes/` |
| Aulas longas | `<base>/videos/aulas/` |
| Programas/modelos | `~/.cass-smart-skills/ferramentas/` e caches externos dos motores |
| Instaladores preservados | `~/.cass-smart-skills/instaladores/` |

`CASS_SMART_HOME` permite outra pasta de configuração externa (inclusive nos testes).
Nada persistente pode ficar dentro do plugin/cache, nem por link simbólico.
Antes de preparar programas, inclusive após atualização com configuração já válida,
rode `python scripts/smart_config.py preparar-instaladores`. Isso atualiza somente
as cópias externas dos instaladores e guarda versões anteriores, sem reinstalar
programas nem redefinir as pastas. `ler` e `--conferir` continuam sem gravação.
Instalação de programas exige autorização própria; salvar a configuração só preserva
cópias dos instaladores de vídeo e motion, sem executá-los. Use `ferramentas/video-maker`
para a edição e `ferramentas/motion-designer` para HyperFrames. Não execute npm dentro
da skill; os wrappers Motion resolvem o CLI pelo ambiente externo configurado. Scripts de edição vêm da versão atual do plugin; os programas
continuam na pasta externa. Não copie a skill inteira para a pasta de programas.

Antes de atualizar uma instalação antiga, confira `skills/search/pesquisas/` e os
`.video-maker.json` do projeto informado. Se houver dados ali, preserve-os em destino
externo confirmado e confira conteúdo/hash antes de atualizar o cache. Não apague
origens. Nunca migre trabalhos de outras contas por suposição. Na configuração de
vídeo, um arquivo explícito do projeto tem precedência e não é sobrescrito.

O template Canva é configurado somente quando um post precisar dele. Leia
`skills/carrossel/references/templates-canva.md`. Sua escolha é gravada no
mesmo arquivo externo, não na skill instalada. Atualizar não redefine o template.

Atualização do GitHub depende do cliente. No Codex CLI, confira o catálogo com
`codex plugin marketplace upgrade cass-smart-skills` e instale a versão disponível
com `codex plugin add cass-smart-skills@cass-smart-skills`. Um chat aberto pode
continuar com instruções antigas; valide o que o cliente carregou em um novo chat.
Não prometa atualização imediata e não escreva no cache para forçá-la.
