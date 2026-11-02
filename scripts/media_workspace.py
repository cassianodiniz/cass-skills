"""Projetos de vídeo e descarte explícito de intermediários recriáveis.

Não varre o computador por extensão/idade, não executa receitas e não remove pastas.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

from smart_config import externo

MANIFEST = '.cass-media.json'
DIAS = 30


def agora():
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=-3)))


def dentro(path, base):
    return path == base or base in path.parents


def sem_links(path):
    p = Path(os.path.abspath(Path(path).expanduser()))
    for part in [p, *p.parents]:
        if part.is_symlink():
            raise ValueError('Link simbólico não participa da limpeza: ' + str(part))
        if part.exists() and getattr(part.lstat(), 'st_file_attributes', 0) & 0x400:
            raise ValueError('Junção/ponto de redirecionamento não participa da limpeza.')
    return p


def raizes(pastas):
    roots = {k: externo(str(sem_links(pastas[k]))) for k in
             ['trabalho', 'entrada', 'saida', 'aulas', 'transcricoes']}
    for a, x in roots.items():
        for b, y in roots.items():
            if a != b and dentro(x, y):
                raise ValueError('Pastas de vídeo sobrepostas: ' + a + ' e ' + b)
    return roots


def projeto_seguro(project, pastas):
    roots = raizes(pastas)
    project = sem_links(project)
    if project.parent != roots['trabalho']:
        raise ValueError('Use uma pasta de projeto diretamente dentro de Projetos/trabalho.')
    return project, roots


def assinatura(path):
    path = sem_links(path)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError('É necessário um arquivo regular, sem links adicionais.')
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(block)
    return {'caminho': str(path), 'sha256': digest.hexdigest(), 'bytes': info.st_size,
            'mtime_ns': info.st_mtime_ns}


def data(value):
    result = dt.datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('Data de projeto sem fuso horário.')
    return result


def ler(project):
    path = sem_links(project / MANIFEST)
    if path.stat().st_size > 4 * 1024 * 1024:
        raise ValueError('Registro de projeto excessivamente grande.')
    d = json.loads(path.read_text(encoding='utf-8'))
    if (not isinstance(d, dict) or d.get('versao') != 1 or
            d.get('estado') not in ['em_andamento', 'concluido'] or
            not isinstance(d.get('artefatos'), list)):
        raise ValueError('Registro de projeto inválido.')
    data(d['ultimo_uso'])
    return d


def gravar(project, d):
    sem_links(project / MANIFEST)
    fd, name = tempfile.mkstemp(prefix='.cass-media-', dir=project)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(name, project / MANIFEST)
    finally:
        Path(name).unlink(missing_ok=True)


@contextmanager
def travar(project):
    lock = sem_links(project / '.cass-media.lock')
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise ValueError('Projeto em uso em outra operação; arquivos preservados.') from None
    try:
        yield
    finally:
        owned = os.fstat(fd)
        os.close(fd)
        if lock.exists():
            current = lock.lstat()
            if (current.st_dev, current.st_ino) == (owned.st_dev, owned.st_ino):
                lock.unlink()


def iniciar(project, pastas):
    project, _ = projeto_seguro(project, pastas)
    project.mkdir(parents=True, exist_ok=True)
    with travar(project):
        return _iniciar(project, pastas)


def registrar(project, file, origens, receita, comando, pastas):
    project, _ = projeto_seguro(project, pastas)
    with travar(project):
        return _registrar(project, file, origens, receita, comando, pastas)


def encerrar(project, final, pastas):
    project, _ = projeto_seguro(project, pastas)
    with travar(project):
        return _encerrar(project, final, pastas)


def _iniciar(project, pastas):
    project, _ = projeto_seguro(project, pastas)
    project.mkdir(parents=True, exist_ok=True)
    d = ler(project) if (project / MANIFEST).exists() else {'versao': 1, 'artefatos': []}
    d.update(estado='em_andamento', ultimo_uso=agora().isoformat())
    d.pop('encerrado_em', None)
    # Só este diretório é elegível. Arquivos existentes fora dele não são adotados.
    sem_links(project / 'descartaveis').mkdir(exist_ok=True)
    gravar(project, d)
    return d


def _registrar(project, file, origens, receita, comando, pastas):
    project, roots = projeto_seguro(project, pastas)
    d = ler(project)
    file = sem_links(file)
    if file.parent != project / 'descartaveis' or file.suffix.lower() != '.mp4':
        raise ValueError('Registre apenas um MP4 recém-gerado em descartaveis, sem subpastas.')
    if not origens or not isinstance(comando, list) or not comando or any(
            not isinstance(x, str) or not x.strip() or '\0' in x for x in comando):
        raise ValueError('Informe origens preservadas, receita e comando para recriar.')
    preservados = [sem_links(p) for p in [*origens, receita]]
    for path in preservados:
        if dentro(path, roots['trabalho']) and 'descartaveis' in path.relative_to(roots['trabalho']).parts:
            raise ValueError('Uma receita/origem não pode depender de arquivos descartáveis.')
    item = {'arquivo': assinatura(file), 'origens': [assinatura(p) for p in origens],
            'receita': assinatura(receita), 'comando': comando,
            'registrado_em': agora().isoformat()}
    item['arquivo']['caminho'] = str(file.relative_to(project))
    if any(x['arquivo']['caminho'] == item['arquivo']['caminho'] for x in d['artefatos']):
        raise ValueError('Arquivo já registrado. Não sobrescreva uma prévia anterior.')
    d['artefatos'].append(item)
    d.update(estado='em_andamento', ultimo_uso=agora().isoformat())
    gravar(project, d)
    return item


def _encerrar(project, final, pastas):
    project, roots = projeto_seguro(project, pastas)
    final = sem_links(final)
    if not dentro(final, roots['saida']):
        raise ValueError('A versão aprovada precisa estar na pasta de saída, fora do trabalho.')
    d = ler(project)
    d.update(estado='concluido', final=assinatura(final),
             ultimo_uso=agora().isoformat(), encerrado_em=agora().isoformat())
    gravar(project, d)
    return d


def confere(record, path=None):
    current = assinatura(path or record['caminho'])
    if any(current[k] != record[k] for k in ['sha256', 'bytes']):
        raise ValueError('Arquivo mudou desde o registro: ' + current['caminho'])
    return current


def remover(file, expected):
    """Ancoragem no diretório, sem seguir symlink, inclusive durante a leitura."""
    file = sem_links(file)
    if os.name == 'posix':
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        parent_fd = os.open(file.parent, flags)
        try:
            fd = os.open(file.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
            with os.fdopen(fd, 'rb') as f:
                info = os.fstat(f.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise ValueError('Arquivo deixou de ser regular.')
                digest = hashlib.sha256()
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    digest.update(block)
                digest = digest.hexdigest()
                if digest != expected['sha256'] or info.st_mtime_ns != expected['mtime_ns']:
                    raise ValueError('Arquivo mudou antes da remoção.')
                check = os.stat(file.name, dir_fd=parent_fd, follow_symlinks=False)
                if (check.st_dev, check.st_ino) != (info.st_dev, info.st_ino):
                    raise ValueError('Arquivo substituído antes da remoção.')
                os.unlink(file.name, dir_fd=parent_fd)
        finally:
            os.close(parent_fd)
    elif os.name == 'nt':
        remover_windows(file, expected)
    else:
        raise ValueError('Limpeza automática indisponível neste sistema; arquivos preservados.')


def remover_windows(file, expected):
    """Bloqueia renomeação das pastas; valida e apaga pelo handle do arquivo."""
    import ctypes
    from ctypes import wintypes as w
    import msvcrt
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    class Info(ctypes.Structure):
        _fields_ = [('attributes', w.DWORD), ('created', w.FILETIME),
                    ('accessed', w.FILETIME), ('written', w.FILETIME),
                    ('volume', w.DWORD), ('size_hi', w.DWORD), ('size_lo', w.DWORD),
                    ('links', w.DWORD), ('index_hi', w.DWORD), ('index_lo', w.DWORD)]
    kernel.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, ctypes.c_void_p,
                                  w.DWORD, w.DWORD, w.HANDLE]
    kernel.CreateFileW.restype = w.HANDLE
    kernel.CloseHandle.argtypes = [w.HANDLE]
    kernel.GetFileInformationByHandle.argtypes = [w.HANDLE, ctypes.POINTER(Info)]
    kernel.SetFileInformationByHandle.argtypes = [w.HANDLE, ctypes.c_int,
                                                 ctypes.c_void_p, w.DWORD]
    handles = []
    def open_handle(path, access, share, flags):
        handle = kernel.CreateFileW(str(path), access, share, None, 3, flags, None)
        if handle == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        info = Info()
        if not kernel.GetFileInformationByHandle(handle, ctypes.byref(info)) or info.attributes & 0x400:
            kernel.CloseHandle(handle)
            raise ValueError('Ponto de redirecionamento/arquivo inacessível; preservado.')
        return handle, info
    try:
        for parent in reversed(file.parents):
            # SHARE_READ|WRITE, sem SHARE_DELETE: impede trocar uma pasta por junção.
            h, _ = open_handle(parent, 0x80, 3, 0x02000000 | 0x00200000)
            handles.append(h)
        h, info = open_handle(file, 0x80000000 | 0x00010000, 1, 0x00200000)
        try:
            fd = msvcrt.open_osfhandle(h, os.O_RDONLY)
        except Exception:
            kernel.CloseHandle(h)
            raise
        with os.fdopen(fd, 'rb') as f:
            st = os.fstat(f.fileno())
            digest = hashlib.sha256()
            for block in iter(lambda: f.read(1024 * 1024), b''):
                digest.update(block)
            if (info.links != 1 or not stat.S_ISREG(st.st_mode) or
                    digest.hexdigest() != expected['sha256'] or st.st_mtime_ns != expected['mtime_ns']):
                raise ValueError('Arquivo mudou antes da remoção; preservado.')
            disposition = ctypes.c_ubyte(1)
            if not kernel.SetFileInformationByHandle(h, 4, ctypes.byref(disposition), 1):
                raise ctypes.WinError(ctypes.get_last_error())
    finally:
        for handle in reversed(handles):
            kernel.CloseHandle(handle)


def limpar(pastas, habilitada=False, now=None):
    if type(habilitada) is not bool:
        raise ValueError('A preferência de limpeza precisa ser verdadeira ou falsa.')
    result = {'habilitada': habilitada, 'removidos': [], 'bytes_removidos': 0,
              'bytes_finais_preservados': 0, 'avisos': []}
    roots = raizes(pastas)
    now = now or agora()
    cutoff = now - dt.timedelta(days=DIAS)
    if not roots['trabalho'].exists():
        return result
    finais_contados = set()
    for project in sorted(roots['trabalho'].iterdir()):
        if not project.is_dir():
            continue
        if not (project / MANIFEST).exists():
            result['avisos'].append(project.name + ': projeto sem registro; arquivos preservados.')
            continue
        try:
            with travar(project):
                project, _ = projeto_seguro(project, pastas)
                d = ler(project)
                if 'final' in d:
                    final = sem_links(d['final']['caminho'])
                    if not dentro(final, roots['saida']):
                        raise ValueError('Final fora da pasta de saída.')
                    final_info = confere(d['final'])
                    if final not in finais_contados:
                        result['bytes_finais_preservados'] += final_info['bytes']
                        finais_contados.add(final)
                if d['estado'] != 'concluido':
                    continue
                if 'final' not in d:
                    raise ValueError('Projeto encerrado sem final aprovado; preservado.')
                if not habilitada or max(data(d['ultimo_uso']), data(d['encerrado_em'])) >= cutoff:
                    continue
                for item in d['artefatos']:
                    try:
                        relative = Path(item['arquivo']['caminho'])
                        if relative.is_absolute() or relative.parts[:1] != ('descartaveis',) or len(relative.parts) != 2:
                            raise ValueError('Caminho de temporário inválido.')
                        if relative.suffix.lower() != '.mp4':
                            raise ValueError('Somente intermediários MP4 podem ser removidos.')
                        file = project / relative
                        sem_links(file)
                        if not file.exists():
                            continue
                        if data(item['registrado_em']) >= cutoff:
                            continue
                        current = confere(item['arquivo'], file)
                        if dt.datetime.fromtimestamp(file.stat().st_mtime, tz=now.tzinfo) >= cutoff:
                            continue
                        if not item['origens'] or not item['comando']:
                            raise ValueError('Registro sem origens/comando de recriação.')
                        for record in [*item['origens'], item['receita']]:
                            path = sem_links(record['caminho'])
                            if dentro(path, roots['trabalho']) and 'descartaveis' in path.relative_to(roots['trabalho']).parts:
                                raise ValueError('Origem/receita descartável.')
                            confere(record)
                        remover(file, current)
                        result['removidos'].append(str(file))
                        result['bytes_removidos'] += current['bytes']
                    except (OSError, ValueError, KeyError, TypeError) as e:
                        result['avisos'].append(str(project.name) + ': ' + str(e))
        except (OSError, ValueError, KeyError, TypeError) as e:
            result['avisos'].append(str(project.name) + ': ' + str(e))
    return result


def main():
    import smart_config
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pastas', help='JSON com as pastas efetivas; necessário em projetos legados.')
    sub = p.add_subparsers(dest='acao', required=True)
    cleanup = sub.add_parser('limpar')
    cleanup.add_argument('--atual', help='Projeto retomado: protege-o antes de limpar os demais.')
    for action in ['iniciar', 'registrar', 'encerrar']:
        s = sub.add_parser(action)
        s.add_argument('--projeto', required=True)
        if action == 'registrar':
            s.add_argument('--dados', required=True)
        if action == 'encerrar':
            s.add_argument('--final', required=True)
    a = p.parse_args()
    try:
        cfg = smart_config.carregar()
        pastas = json.loads(Path(a.pastas).read_text(encoding='utf-8-sig')) if a.pastas else cfg['pastas']['videos']
        if a.acao == 'limpar':
            if a.atual:
                iniciar(a.atual, pastas)
            result = limpar(pastas, cfg.get('limpeza', {}).get('habilitada', False))
        elif a.acao == 'iniciar':
            result = iniciar(a.projeto, pastas)
        elif a.acao == 'encerrar':
            result = encerrar(a.projeto, a.final, pastas)
        else:
            item = json.loads(Path(a.dados).read_text(encoding='utf-8-sig'))
            result = registrar(a.projeto, item['arquivo'], item['origens'], item['receita'], item['comando'], pastas)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as e:
        p.exit(2, 'Arquivos preservados: ' + str(e) + '\n')


if __name__ == '__main__':
    main()
