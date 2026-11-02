"""Abrir a pasta da entrega e criar atalhos visíveis, sem mover arquivos."""
from pathlib import Path
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from user_folders import conhecida


def abrir(value):
    p = Path(value).expanduser().resolve(strict=True)
    folder = p if p.is_dir() else p.parent
    if sys.platform == 'win32':
        os.startfile(str(folder))
    else:
        subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', str(folder)], check=True)
    return {'pasta': str(folder), 'aberta': True}


def atalho(nome, value):
    if not re.fullmatch(r'[\wÀ-ÿ -]{1,70}', nome) or nome in ['.', '..']:
        raise ValueError('Nome de atalho inválido.')
    target = Path(value).expanduser().resolve(strict=True)
    if not target.is_dir():
        raise ValueError('O atalho precisa apontar para uma pasta.')
    desktop = conhecida('desktop')
    if not desktop.is_dir():
        raise ValueError('Área de Trabalho indisponível; a pasta original foi preservada.')
    link = desktop / ('Cass Skills - ' + nome + ('.lnk' if sys.platform == 'win32' else ''))
    if link.exists() or link.is_symlink():
        if sys.platform != 'win32' and link.is_symlink() and link.resolve() == target:
            return {'atalho':str(link), 'existente':True}
        raise ValueError('Já existe um item com esse nome na Área de Trabalho; não foi substituído.')
    if sys.platform == 'win32':
        fd, temp = tempfile.mkstemp(suffix='.lnk', dir=desktop)
        os.close(fd)
        Path(temp).unlink()
        try:
            # Os caminhos são dados JSON num ambiente só deste processo.
            script = '$d=ConvertFrom-Json $env:CASS_ATALHO_JSON; $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut($d[0]); $s.TargetPath=$d[1]; $s.Save()'
            encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
            subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded],
                           env={**os.environ, 'CASS_ATALHO_JSON':json.dumps([temp,str(target)])}, check=True)
            os.rename(temp, link)  # Windows recusa destino existente, inclusive em corrida.
        finally:
            Path(temp).unlink(missing_ok=True)
    else:
        link.symlink_to(target, target_is_directory=True)
    return {'atalho':str(link), 'destino':str(target)}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='acao', required=True)
    a=sub.add_parser('abrir');a.add_argument('caminho')
    a=sub.add_parser('atalho');a.add_argument('--nome', required=True);a.add_argument('--pasta', required=True)
    a=p.parse_args()
    try:
        result=abrir(a.caminho) if a.acao=='abrir' else atalho(a.nome,a.pasta)
        print(json.dumps(result,ensure_ascii=False))
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        p.exit(2,'Não consegui abrir/criar o atalho: '+str(e)+'\n')
