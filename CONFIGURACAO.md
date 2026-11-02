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

Padrões novos, ajustáveis pelo usuário. A pasta Vídeos é a pasta nativa do sistema
(Filmes no Mac); Documentos também é resolvida pelo sistema. Configurações já
existentes e `propor --base` mantêm sua organização, sem migração automática.

| Conteúdo | Pasta |
|---|---|
| Posts e estado por versão | `Documentos/Cass Skills/Carrosséis/<tema>/` |
| Pesquisas e fontes | `<base>/pesquisas/` |
| Vídeos recebidos | `Vídeos/Cass Skills/Originais/` |
| Versões aprovadas | `Vídeos/Cass Skills/Prontos/` |
| Planos e rascunhos | `Vídeos/Cass Skills/Projetos/<tema>/` |
| Transcrições reutilizáveis | `Vídeos/Cass Skills/Transcrições/` |
| Aulas longas | `Vídeos/Cass Skills/Aulas/` |
| Programas/modelos | `~/.cass-smart-skills/ferramentas/` e caches externos dos motores |
| Instaladores preservados | `~/.cass-smart-skills/instaladores/` |

`CASS_SMART_HOME` permite outra pasta de configuração externa (inclusive nos testes).
Nada persistente pode ficar dentro do plugin/cache, nem por link simbólico.

Na configuração inicial, ofereça os atalhos na Área de Trabalho e a preferência
de limpeza de intermediários após 30 dias. Só ative a limpeza depois do aceite
daquele usuário: `limpeza: {habilitada: true, dias: 30}`. Sem preferência ou com
`false`, não há exclusão. Não altere pastas e outros padrões ao salvar essa opção.
Leia [o fluxo de pastas, entrega e limpeza](references/arquivos-e-limpeza.md) para
criar os atalhos, abrir as entregas e registrar projetos/MP4s descartáveis.
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
`codex plugin marketplace upgrade cass-skills` e instale a versão disponível
com `codex plugin add cass-skills@cass-skills`. Um chat aberto pode
continuar com instruções antigas; valide o que o cliente carregou em um novo chat.
Não prometa atualização imediata e não escreva no cache para forçá-la.

O nome Cass Skills unifica os pacotes sem migrar configurações: o nome externo
`CASS_SMART_HOME` e a pasta `~/.cass-smart-skills/` são mantidos por compatibilidade.
As skills de consulta nutricional usam os materiais incluídos, sem exigir essa
configuração. Dados de pacientes e entregas continuam fora do plugin.
