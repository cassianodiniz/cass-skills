import { existsSync, mkdirSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import path from 'node:path';
import { external } from './runtime_paths.mjs';

export function saidaDoRender(project, name) {
  const folder = path.join(project, 'descartaveis');
  if (external(folder) !== folder) throw new Error('Descartaveis não pode ser um atalho.');
  if (name && (path.basename(name) !== name || /[\\/\0]/.test(name) || !name.endsWith('.mp4'))) {
    throw new Error('--saida recebe apenas um nome de arquivo .mp4, sem pastas.');
  }
  mkdirSync(folder, { recursive: true });
  const file = path.join(folder, name || `${path.basename(project)}-${randomUUID()}.mp4`);
  if (existsSync(file)) throw new Error('O MP4 já existe. Use outro nome; nenhuma versão foi substituída.');
  return file;
}
