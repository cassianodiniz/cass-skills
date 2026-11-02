// Instalador preservável fora do plugin. Execute somente com autorização.
import { mkdirSync, existsSync, readFileSync, writeFileSync, realpathSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
try {
  const args=process.argv.slice(2);
  if(args.length!==2||args[0]!=='--destino'||!path.isAbsolute(args[1])) throw new Error('Uso: node instalar_motion.mjs --destino <pasta-externa-absoluta>');
  if(Number(process.versions.node.split('.')[0])<22) throw new Error('Use Node.js 22 ou superior.');
  let target=path.resolve(args[1]), base=target; const tail=[];
  while(!existsSync(base)){tail.unshift(path.basename(base));base=path.dirname(base);}
  target=path.join(realpathSync(base),...tail);
  const sourceRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
  const forbidden=['.codex/plugins','.codex/.tmp','.agents/skills','.codex/skills','.claude/plugins','.claude/skills'].map(p=>path.join(os.homedir(),p));
  if(existsSync(path.join(sourceRoot,'plugin.json')))forbidden.push(sourceRoot);
  for(const item of forbidden){
    let base=path.resolve(item);const tail=[];
    while(!existsSync(base)){tail.unshift(path.basename(base));base=path.dirname(base);}
    const resolved=path.join(realpathSync(base),...tail);
    const rel=path.relative(resolved,target);
    if(rel===''||(!rel.startsWith('..'+path.sep)&&rel!=='..'&&!path.isAbsolute(rel)))throw new Error('Instale fora do plugin/cache.');
  }
  const pkg=path.join(target,'package.json');
  if(existsSync(target)&&!existsSync(pkg))throw new Error('Escolha uma pasta nova ou o ambiente Motion já preparado.');
  if(existsSync(pkg)&&JSON.parse(readFileSync(pkg,'utf8')).name!=='cass-smart-motion-runtime')throw new Error('Esta pasta pertence a outro projeto; escolha uma pasta nova.');
  mkdirSync(target,{recursive:true});
  writeFileSync(pkg,JSON.stringify({name:'cass-smart-motion-runtime',private:true,type:'module',dependencies:{hyperframes:'0.7.56'}},null,2)+'\n');
  const nodeDir=path.dirname(process.execPath);
  const npmCli=[process.env.npm_execpath,path.join(nodeDir,'node_modules/npm/bin/npm-cli.js'),path.join(nodeDir,'../lib/node_modules/npm/bin/npm-cli.js')].find(p=>p&&existsSync(p)&&path.basename(p)==='npm-cli.js');
  if(process.platform==='win32'&&!npmCli)throw new Error('npm CLI não localizado junto do Node. Preserve este ambiente e corrija a instalação do Node/npm antes de tentar novamente.');
  const command=npmCli?process.execPath:'npm';
  const argv=[...(npmCli?[npmCli]:[]),'install','--prefix',target,'--omit=dev','--no-audit','--no-fund'];
  const r=spawnSync(command,argv,{stdio:'inherit',shell:false});
  if(r.error||r.status!==0)throw new Error(r.error?.message||'Falha na instalação; ambiente preservado para diagnóstico.');
  if(!existsSync(path.join(target,'node_modules/hyperframes/dist/cli.js')))throw new Error('A instalação não produziu o CLI esperado.');
  console.log(`HyperFrames 0.7.56 preservado fora do plugin: ${target}`);
}catch(e){console.error(e.message);process.exit(2);}
