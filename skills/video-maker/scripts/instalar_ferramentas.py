"""Prepara ambiente isolado de edição; usar apenas com instalação autorizada."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--destino', required=True)
    p.add_argument('--transcricao', action='store_true')
    a = p.parse_args()
    if sys.version_info < (3, 10):
        p.error('Use Python 3.10 ou mais novo para preparar as ferramentas.')
    root = Path(a.destino).expanduser().resolve()
    plugin = Path(__file__).resolve().parents[3]
    blocked = [Path.home()/'.codex/plugins', Path.home()/'.codex/.tmp', Path.home()/'.agents/skills',
               Path.home()/'.codex/skills', Path.home()/'.claude/plugins', Path.home()/'.claude/skills']
    if (plugin/'plugin.json').exists():
        blocked.append(plugin)
    if any(root == b.resolve() or b.resolve() in root.parents for b in blocked):
        p.error('Instale as ferramentas fora da pasta do plugin e do cache de skills.')
    if root.exists() and not (root / 'pyvenv.cfg').exists():
        p.error('Escolha uma pasta nova ou um ambiente Video Maker já preparado.')
    venv.EnvBuilder(with_pip=True, symlinks=os.name != 'nt').create(root)
    python = root / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    deps = ['Pillow>=10,<13', 'numpy>=1.26,<3', 'static-ffmpeg>=3,<4']
    if a.transcricao:
        deps.append('faster-whisper>=1.2,<2')
    subprocess.run([str(python), '-m', 'pip', 'install', *deps], check=True)
    # O pacote baixa FFmpeg/FFprobe para este ambiente, nunca altera o PATH global.
    code = '''import static_ffmpeg,subprocess
static_ffmpeg.add_paths()
subprocess.run(['ffmpeg','-version'],check=True)
subprocess.run(['ffprobe','-version'],check=True)
filters=subprocess.check_output(['ffmpeg','-hide_banner','-filters'],text=True,stderr=subprocess.STDOUT)
assert ' ass ' in filters and ' drawtext ' in filters, 'FFmpeg sem os filtros de legenda/texto necessários'
'''
    subprocess.run([str(python), '-c', code], check=True)
    freeze = subprocess.check_output([str(python), '-m', 'pip', 'freeze'], text=True)
    (root / 'ferramentas-instaladas.txt').write_text(freeze, encoding='utf-8')
    print('Ferramentas prontas em: ' + str(root))
    print('O modelo Whisper é baixado no primeiro uso; a transcrição acontece localmente.')


if __name__ == '__main__':
    main()
