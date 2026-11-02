# Entregas acessíveis e limpeza de vídeos

Leia ao configurar pastas, iniciar uma edição/motion, retomar ou encerrar um projeto.
Os scripts abaixo ficam em `scripts/` na raiz do plugin; resolva pelo local desta
referência, sem assumir o diretório de trabalho nem um caminho pessoal do autor.

## Pastas e acesso

- Usuário novo: `smart_config.py propor` sugere Documentos/Cass Skills/Carrosséis
  e a pasta Vídeos do sistema (Filmes no Mac)/Cass Skills, com Originais, Prontos,
  Projetos, Transcrições e Aulas. Mostre as pastas e confirme uma vez.
- Preserve as pastas já configuradas e os projetos com `.video-maker.json` próprio.
  Não mova trabalhos, não una consultórios nem crie outra pasta de pacientes em silêncio.
- Dieta e onboard reutilizam a pasta de pacientes confirmada pelo usuário. Dieta
  continua abrindo a pasta ao terminar. Nenhuma limpeza de vídeo alcança esses dados.
- Ofereça na primeira configuração os atalhos visíveis na Área de Trabalho. Depois
  do aceite, execute `python scripts/acesso.py atalho --nome Vídeos --pasta <Prontos>`,
  e o equivalente para Carrosséis e, quando confirmada, a pasta Pacientes. Não
  substitua atalhos/arquivos existentes; se houver conflito, informe e preserve.
- Ao entregar vídeo, carrossel ou motion, devolva o arquivo/link e abra a pasta da
  entrega com `python scripts/acesso.py abrir <arquivo-ou-pasta>`. Em carrossel,
  abra a pasta local com copy e estado e forneça também o link Canva; exportação
  só quando solicitada. Se o ambiente não abrir janelas, informe o caminho real
  e mantenha o link de arquivo na conversa, sem alegar que abriu.

## Política que cada usuário escolhe uma vez

Apresente: “Posso remover automaticamente os MP4s intermediários recriáveis de
projetos encerrados e sem uso há mais de 30 dias? Originais e vídeos finais ficam
guardados.” Só após o sim, grave `limpeza: {habilitada: true, dias: 30}` na
configuração central usando `smart_config.py salvar --dados <json>`. Preserve os
demais campos. Um não grava `habilitada: false`. A pessoa pode mudar depois.
Uma configuração antiga sem essa preferência equivale a limpeza desligada;
pergunte uma vez quando a skill de vídeo for usada, sem migrar pastas.

## Ao iniciar video-maker ou motion-designer

1. Leia as pastas efetivas. Se houver configuração própria do projeto, ela prevalece.
2. Execute `python scripts/media_workspace.py limpar` com a preferência central.
   Ao retomar, use `limpar --atual <projeto>`: o próprio comando marca esse projeto
   em andamento antes de limpar os demais. Não faça uma limpeza anterior a isso.
   Para pastas de projeto próprias, grave somente as cinco pastas efetivas num JSON
   temporário e use `python scripts/media_workspace.py --pastas <json> limpar`.
   Nunca limpe a base central no lugar da base específica em uso.
3. Informe quantidade/tamanho removidos e tamanho dos finais registrados que foram
   preservados. `bytes_removidos` é o tamanho dos arquivos excluídos, não uma medição
   do espaço livre físico. Mostre avisos de itens preservados por falta de segurança.
   O script não inicia serviço em segundo plano: a checagem ocorre ao usar a skill.
4. Se a limpeza falhar, preserve os arquivos, informe a limitação e continue a edição
   possível. Nunca substitua por `rm`, busca por MP4 antigo ou limpeza da Lixeira.

## Ciclo de um projeto

Use uma pasta nova por tema em `pastas.trabalho` (Projetos). Após criá-la, execute
`python scripts/media_workspace.py iniciar --projeto <pasta>`. Execute o mesmo
comando ao retomar: atualiza o último uso e marca o projeto em andamento.
Para projetos fora da base gerenciada, preserve a localização e explique que
não participam da limpeza automática; não os mova para habilitar a limpeza.

Roteiro, plano, transcrições, imagens e arquivos necessários à recriação ficam
fora da subpasta `descartaveis`. Somente MP4s intermediários recém-gerados pela
skill são escritos nela. Video-maker: use esse destino no plano de renderização.
Motion: `render.mjs` já grava o MP4 em `descartaveis`, com nome único por geração.
Não renomeie um MP4 depois de registrá-lo. Cada nova versão recebe outro nome.

Após gerar e verificar um intermediário, registre-o. O JSON de `--dados` tem:

```json
{
  "arquivo": "<projeto>/descartaveis/previa-v1.mp4",
  "origens": ["<caminho-absoluto-da-gravacao-original>"],
  "receita": "<projeto>/plano.json",
  "comando": ["<python-do-ambiente>", "<skill>/scripts/montar.py", "<projeto>/plano.json"]
}
```

Execute `python scripts/media_workspace.py registrar --projeto <pasta> --dados <json>`.
Use os caminhos e o comando reais da geração, incluindo todos os insumos que ela
exige. No motion, preserve index.html, scripts, fontes e imagens, inclua-os em
`origens` e guarde uma receita JSON com o comando `node <skill>/scripts/render.mjs
<projeto> --saida <nome-exato-deste-intermediario.mp4>`. Assim a receita recria
esse caminho quando não existir, em vez de produzir outra versão anônima.
Nunca registre um arquivo antigo ou fornecido pelo usuário como
“gerado” apenas para a limpeza aceitá-lo. Registro incompleto = arquivo preservado.

Depois da aprovação explícita e das conferências já exigidas pela skill, copie
o MP4 aprovado para um nome novo em Prontos/`pastas.saida`. Não mova o original.
Execute `python scripts/media_workspace.py encerrar --projeto <pasta> --final <MP4-aprovado>`
somente quando o usuário concluir o trabalho. Ajuste pendente/rascunho continua
em andamento. Retomar exige `iniciar` antes da próxima limpeza desse projeto;
portanto, ao reabrir um projeto, marque-o primeiro e depois limpe os outros.

Todos os comandos de ciclo aceitam `--pastas <json>` antes da ação, quando as
pastas efetivas forem específicas de um projeto. Sem configuração central,
configure-a primeiro; não improvise exclusão para “destravar”.

## O que é preservado

Originais, finais aprovados, PDFs, planilhas, fichas, roteiros, transcrições,
projetos ativos, pastas antigas sem registro e arquivos não registrados. A remoção
é definitiva e só alcança MP4s registrados diretamente em `descartaveis`, após
30 dias desde o encerramento, último uso, registro e modificação do arquivo.
Sem final aprovado intacto, receita intacta e todas as origens intactas, nada é
removido. Arquivos modificados, links, junções e registros inválidos são preservados.
Nunca esvazie a Lixeira nem ative políticas de limpeza do sistema operacional.
