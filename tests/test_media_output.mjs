import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, readFileSync, rmSync, symlinkSync, realpathSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { saidaDoRender } from '../scripts/media_output.mjs';

function fixture(t) {
  const root = mkdtempSync(path.join(tmpdir(), 'cass-render-'));
  t.after(() => rmSync(root, {recursive:true,force:true}));
  // canonical temp path matters on macOS (/var is an alias of /private/var).
  return realpathSync(root);
}
test('successive renders preserve existing versions', t => {
  const root = fixture(t);
  const first = saidaDoRender(root);
  writeFileSync(first, 'primeira versao');
  const second = saidaDoRender(root);
  assert.notEqual(first, second);
  writeFileSync(second, 'segunda versao');
  assert.equal(readFileSync(first,'utf8'),'primeira versao');
});
test('explicit recipe path can be recreated but never overwritten', t => {
  const root = fixture(t);
  const file = saidaDoRender(root, 'previa-v1.mp4');
  writeFileSync(file, 'v1');
  assert.throws(() => saidaDoRender(root, 'previa-v1.mp4'), /já existe/);
  rmSync(file);
  assert.equal(saidaDoRender(root,'previa-v1.mp4'),file);
  assert.throws(() => saidaDoRender(root,'../final.mp4'));
});
test('disposable directory cannot redirect the render', t => {
  const root = fixture(t), other = fixture(t);
  symlinkSync(other,path.join(root,'descartaveis'),'dir');
  assert.throws(() => saidaDoRender(root));
});
