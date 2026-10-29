# Mentores e WhatsApp

Somente quando o usuário pedir envio ou leitura. Use o conector ou skill de
WhatsApp disponível no ambiente e o destinatário que ele fornecer. Esta distribuição
não inclui acesso, contatos nem grupos do autor. Sem integração, prepare a mensagem
para o usuário copiar e diga que não enviou.
Antes do envio: confira versão/hash exibidos, registre `envio_autorizado_hash`,
consuma e persista a autorização; só então envie uma vez. Registre o message_id.
Timeout não autoriza repetir. Leia mensagens com origem e identificador e processe
cada uma uma vez. Preserve a mídia quando disponível; não infira conteúdo inacessível.
Mentores aconselham; o usuário decide o que incorporar. Não reenvie automaticamente.
