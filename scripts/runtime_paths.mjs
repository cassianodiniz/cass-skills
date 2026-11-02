import { existsSync, realpathSync, readFileSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
const plugin = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
function realFuture(p) {
  let base = p; const tail = [];
  while (!existsSync(base)) { tail.unshift(path.basename(base)); const parent=path.dirname(base); if(parent===base) break; base=parent; }
  return path.join(realpathSync(base),...tail);
}
export function external(value) {
  if(typeof value!=='string'||!path.isAbsolute(value)||value.includes('\0')) throw new Error('Use uma pasta absoluta externa ao plugin.');
  const p=realFuture(path.resolve(value));
  for(const b of [plugin,path.join(os.homedir(),'.codex/plugins'),path.join(os.homedir(),'.codex/.tmp'),path.join(os.homedir(),'.agents/skills'),path.join(os.homedir(),'.codex/skills'),path.join(os.homedir(),'.claude/plugins'),path.join(os.homedir(),'.claude/skills')]) {
    const rel=path.relative(realFuture(b),p);
    if(rel===''||(!rel.startsWith('..'+path.sep)&&rel!=='..'&&!path.isAbsolute(rel))) throw new Error('A pasta precisa ficar fora do plugin e do cache de skills.');
  }
  return p;
}
export function hyperframesCli() {
  const home=external(process.env.CASS_SMART_HOME||path.join(os.homedir(),'.cass-smart-skills'));
  const file=path.join(home,'config.json');
  if(!existsSync(file)) throw new Error('Smart não configurado. Siga CONFIGURACAO.md antes de preparar as ferramentas.');
  const config=JSON.parse(readFileSync(file,'utf8'));
  if(config.versao!==1) throw new Error('Versão da configuração inválida.');
  const cli=external(path.join(external(config.ferramentas),'motion-designer/node_modules/hyperframes/dist/cli.js'));
  if(!existsSync(cli)) throw new Error('HyperFrames externo ausente. Com instalação autorizada, use o instalador Motion na pasta externa configurada.');
  return cli;
}
