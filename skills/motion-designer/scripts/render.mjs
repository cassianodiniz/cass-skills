import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { external, hyperframesCli } from '../../../scripts/runtime_paths.mjs';
import { saidaDoRender } from '../../../scripts/media_output.mjs';
function run(command, args) {
  const r = spawnSync(command, args, { encoding: 'utf8', shell: false, maxBuffer: 20 * 1024 * 1024 });
  if (r.error || r.status !== 0) throw new Error(`${command}: ${r.error?.message || r.stderr || r.stdout || 'falhou'}`);
  return r.stdout;
}
try {
  const [destination, option, name, ...extra] = process.argv.slice(2);
  if (!destination || extra.length || (option && (option !== '--saida' || !name))) throw new Error('Uso: node scripts/render.mjs <pasta-do-motion> [--saida versao.mp4] (após aprovação do MP4)');
  const project = external(path.resolve(destination));
  const cli = hyperframesCli();
  const html = readFileSync(path.join(project, 'index.html'), 'utf8');
  const attr = name => Number(html.match(new RegExp(`\\b${name}=["']([\\d.]+)["']`))?.[1]);
  const expected = { width: attr('data-width'), height: attr('data-height'), duration: attr('data-duration') };
  if (Object.values(expected).some(v => !Number.isFinite(v) || v <= 0)) throw new Error('Dimensões ou duração inválidas no index.html.');
  // Uma geração nova ganha nome imutável; --saida reproduz o caminho da receita.
  const video = saidaDoRender(project, name);
  run('ffmpeg', ['-version']); run('ffprobe', ['-version']);
  console.log('Conferindo a composição...');
  const check = run(process.execPath, [cli, 'check', project, '--json']);
  writeFileSync(path.join(project, 'check.json'), check);
  console.log('Renderizando...');
  const log = run(process.execPath, [cli, 'render', project, '-o', video, '-f', '30', '-q', 'high', '--strict', '--quiet']);
  writeFileSync(path.join(project, 'render.log'), log);
  if (!existsSync(video) || statSync(video).size === 0) throw new Error('Render terminou sem MP4 válido.');
  const metadata = JSON.parse(run('ffprobe', ['-v', 'error', '-show_streams', '-show_format', '-of', 'json', video]));
  const stream = metadata.streams.find(s => s.codec_type === 'video');
  const duration = Number(metadata.format.duration);
  if (!stream || stream.width !== expected.width || stream.height !== expected.height || Math.abs(duration - expected.duration) > 0.1) throw new Error('MP4 diverge das dimensões ou duração da composição.');
  if (metadata.streams.some(s => s.codec_type === 'audio')) throw new Error('MP4 possui áudio: o motion deve ser mudo.');
  const review = path.join(project, 'conferir'); mkdirSync(review, { recursive: true });
  const frameTime = part => Math.max(0, Math.min(duration - 0.1, duration * part)).toFixed(3);
  const requiredImages = [path.join(review, 'folha.png')];
  run('ffmpeg', ['-v', 'error', '-y', '-i', video, '-vf', `fps=12/${duration},scale=360:-1,tile=4x3:padding=6:color=white`, '-frames:v', '1', path.join(review, 'folha.png')]);
  for (const part of [0.08, 0.25, 0.42, 0.58, 0.75, 0.95]) {
    const time = frameTime(part);
    const file = path.join(review, `t_${time}.png`); requiredImages.push(file);
    run('ffmpeg', ['-v', 'error', '-y', '-ss', time, '-i', video, '-frames:v', '1', file]);
  }
  for (const part of [0.3, 0.6, 0.99]) {
    const time = frameTime(part);
    const file = path.join(review, `celular_${time}.png`); requiredImages.push(file);
    run('ffmpeg', ['-v', 'error', '-y', '-ss', time, '-i', video, '-frames:v', '1', '-vf', 'scale=360:-1', file]);
  }
  for (const file of requiredImages) if (!existsSync(file) || statSync(file).size === 0) throw new Error(`Quadro de conferência não foi gerado: ${file}`);
  writeFileSync(path.join(review, 'metadados.json'), JSON.stringify({ width: stream.width, height: stream.height, duration, audio: false }, null, 2));
  console.log(`MP4 criado: ${video}\nAbra e confira ${review}; a checagem técnica não substitui a revisão visual, inclusive do final parado.`);
} catch (error) {
  console.error(error.message); process.exit(2);
}
