import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, cpSync, rmSync, existsSync, symlinkSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const wrapper=path.join(root,'skills/motion-designer/scripts/hyperframes.mjs');
function fixture(t){const p=mkdtempSync(path.join(tmpdir(),'smart-motion-'));t.after(()=>rmSync(p,{recursive:true,force:true}));const home=path.join(p,'settings');mkdirSync(home);return {p,home,env:{...process.env,CASS_SMART_HOME:home}};}
function invoke(wrapper,env,args=[]){return spawnSync(process.execPath,[wrapper,...args],{encoding:'utf8',env});}
test('absent configuration is clear and creates no runtime',t=>{const f=fixture(t);const r=invoke(wrapper,f.env,['check','fake']);assert.equal(r.status,2);assert.match(r.stderr,/não configurado/);assert.equal(existsSync(path.join(f.home,'config.json')),false);});
test('wrapper resolves external CLI and survives a plugin release replacement',t=>{
 const f=fixture(t);const tools=path.join(f.p,'tools');const cli=path.join(tools,'motion-designer/node_modules/hyperframes/dist/cli.js');mkdirSync(path.dirname(cli),{recursive:true});writeFileSync(cli,"console.log(JSON.stringify(process.argv.slice(2)));\n");writeFileSync(path.join(f.home,'config.json'),JSON.stringify({versao:1,ferramentas:tools}));
 for(const version of ['v1','v2']){
  const pkg=path.join(f.p,version);mkdirSync(path.join(pkg,'scripts'),{recursive:true});mkdirSync(path.join(pkg,'skills/motion-designer/scripts'),{recursive:true});cpSync(path.join(root,'scripts/runtime_paths.mjs'),path.join(pkg,'scripts/runtime_paths.mjs'));cpSync(wrapper,path.join(pkg,'skills/motion-designer/scripts/hyperframes.mjs'));
  const r=invoke(path.join(pkg,'skills/motion-designer/scripts/hyperframes.mjs'),f.env,['check','fixture','--json']);assert.equal(r.status,0,r.stderr);assert.deepEqual(JSON.parse(r.stdout),['check','fixture','--json']);
  if(version==='v1')rmSync(pkg,{recursive:true});
 }
 assert.equal(existsSync(cli),true);
});
test('runtime configured inside plugin is rejected',t=>{const f=fixture(t);writeFileSync(path.join(f.home,'config.json'),JSON.stringify({versao:1,ferramentas:path.join(root,'tools')}));const r=invoke(wrapper,f.env);assert.equal(r.status,2);assert.match(r.stderr,/fora do plugin/);});
test('external alias back to plugin is rejected',t=>{const f=fixture(t);const link=path.join(f.p,'alias');symlinkSync(root,link,'dir');writeFileSync(path.join(f.home,'config.json'),JSON.stringify({versao:1,ferramentas:link}));const r=invoke(wrapper,f.env);assert.equal(r.status,2);assert.match(r.stderr,/fora do plugin/);});
test('installer refuses cache/plugin before invoking npm',t=>{const f=fixture(t);const r=invoke(path.join(root,'scripts/instalar_motion.mjs'),f.env,['--destino',path.join(root,'runtime-test-never')]);assert.equal(r.status,2);assert.match(r.stderr,/fora do plugin/);assert.equal(existsSync(path.join(root,'runtime-test-never')),false);});
test('preserved installer rejects Claude and Codex skill caches before npm',t=>{
 const f=fixture(t);const installer=path.join(f.p,'instaladores/instalar_motion.mjs');mkdirSync(path.dirname(installer));cpSync(path.join(root,'scripts/instalar_motion.mjs'),installer);
 for(const cache of ['.claude/plugins','.claude/skills','.codex/plugins','.codex/skills','.codex/.tmp','.agents/skills']) {
  const target=path.join(f.p,cache,'runtime');mkdirSync(target,{recursive:true});writeFileSync(path.join(target,'package.json'),'{"name":"other-project"}');
  const r=invoke(installer,{...f.env,HOME:f.p,USERPROFILE:f.p},['--destino',target]);
  assert.equal(r.status,2);assert.match(r.stderr,/fora do plugin/);
 }
});
