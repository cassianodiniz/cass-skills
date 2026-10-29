# Template padrão persistente

Antes do primeiro post no Canva, leia a configuração externa do plugin
(`../../../CONFIGURACAO.md`, relativo a este arquivo). Se houver
`canva.template_padrao_id`, use esse design e confira o acesso. Sem ID, peça ao
usuário o link do seu modelo. Não use modelos pessoais do autor.

Confira o design fornecido e crie uma cópia para o modelo de trabalho chamado
**Template padrão de carrossel**. A operação de copiar não recebe título em todos
os conectores. Renomeie somente essa nova cópia se houver operação compatível;
se renomear exigir salvar edição, mostre a prévia e obtenha a aprovação exigida
pelo conector uma única vez. Não alegue que o título mudou sem verificar.
Grave ID do modelo recebido em `canva.template_origem_id` e o ID confirmado da
cópia em `canva.template_padrao_id`, usando `smart_config.salvar` (preserva demais
campos). Se só a cópia foi criada e a configuração falhou, informe o ID e retome
esse mesmo design; não crie outro modelo automaticamente.

Depois de configurado, nunca edite o template padrão durante um post. Cada post
nasce em novo design derivado do template atual. Se o usuário trocar foto, cor ou
fonte nesse template, as novas cópias refletirão a alteração. Posts já criados não
mudam retroativamente. Não refaça a cópia padrão a cada sessão.

Confira campos de preenchimento com a ferramenta adequada: dataset do design
comum ou dataset do Brand Template, conforme o tipo real. Registre campos e tipos
em `cards.json` do trabalho, nunca invente nomes de campo. Um template com texto
editável não é necessariamente preenchível por dados. Sem campos, use a rota de
edição com as aprovações exigidas em `canva.md`.

Preserve fonte, cor, posição e proporção. Quebras de parágrafo são semânticas;
não fragmente frases para imitar largura. Se não couber, proponha o ajuste da copy.
