# Prévia em novo rascunho e alterações no Canva

Leia depois do esqueleto aprovado, da escrita e da revisão. A primeira prévia
visual precede a aprovação final do carrossel. O pedido para criar um carrossel
inclui montar esse rascunho novo; não peça aprovação final da copy para começá-lo.
Preserve o template padrão e todos os posts anteriores.

## Preparar

Leia `templates-canva.md`, carregue a escolha persistente e confira seu acesso.
Registre a versão/hash da copy e o status `Rascunho` no estado e no registro local
ou banco configurado. Não marque `Pronto` antes da decisão final. Mapeie cada card
para os campos reais do modelo. Dados incertos não entram como fatos.

## Primeira prévia: criar um design preenchido

Quando o modelo tiver campos de preenchimento compatíveis:
1. Consulte o dataset apropriado ao tipo real (design comum ou Brand Template).
2. Use a operação de preenchimento que cria novo design, com `update_in_place=false`
   quando disponível, título `Rascunho — <tema> — v<N>` e valores dos campos reais.
   Não envie ID de um design comum como se fosse Brand Template, nem o contrário.
3. Registre imediatamente o ID retornado em `template_copia_id`; ele precisa ser
   diferente do template e do modelo de origem. Timeout é resultado incerto:
   procure o design criado antes de repetir para não gerar duplicatas.
4. Leia o resultado salvo e suas páginas; confira textos, ordem, imagens, vazios e
   excesso de texto. Não diga que está montado se só houver job ou link de preview
   de uma transação temporária. Consulte o job conforme as instruções da ferramenta.
5. Entregue a prévia e o link novo como **rascunho**, com pendências e fontes, antes
   de pedir a aprovação final. Pergunte: “Quer ajustar alguma coisa ou aprovar este
   rascunho? Depois posso preparar a entrega final.”

## Modelo sem preenchimento por dados

Não use geração livre para imitar o modelo. Copie o template para um novo design,
persista o ID, abra a transação nessa cópia e preencha somente os elementos
existentes. Mostre as prévias retornadas. Se o conector exigir aprovação após a
prévia para salvar, explique essa exigência e peça aprovação **para salvar essa
cópia de rascunho**. A autorização editorial final é outra decisão. Não salve sem
cumprir a regra da ferramenta e não finja que o link da cópia mostra edições ainda
não salvas. Após aprovação, salve, releia, confira e entregue o link do rascunho.
Falha de transação mantém o estado pendente e os arquivos locais preservados.

## Ajustes e aprovação final

Uma alteração só ocorre quando o usuário a pedir ou autorizar. “Troque o título
por X” já autoriza essa mudança, sem repetir a pergunta inicial. Preserve as partes
editadas à mão; releia o design e o texto antes de aplicar ajustes. Não use
preenchimento em lugar para sobrescrever o design inteiro quando só um trecho foi
pedido. Se a ferramenta exigir aprovação da prévia para salvar, cumpra essa etapa.

Mudança na copy cria nova versão/hash e segue a revisão aplicável; texto declarado
final pelo usuário permanece literal e dispensa revisão automática. Registre a
versão que corresponde ao design salvo. Só marque `Pronto` após aprovação final.
Depois de ajuste ou aprovação, informe o que concluiu e pergunte o próximo passo
adequado: outro ajuste, exportação ou entrega. Não publique nem envie a terceiros.

Upload de imagem usa recurso local suportado pelo conector ou URL pública já
fornecida; nunca hospede arquivo privado temporariamente. Mostre e confira os
assets e thumbnails. Nunca edite o template padrão ou o modelo de origem.
