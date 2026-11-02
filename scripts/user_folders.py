"""Pastas pessoais do sistema; não cria nem migra conteúdo."""
from pathlib import Path
import json
import os
import re
import subprocess
import sys


def conhecida(kind):
    if kind not in ['documents', 'videos', 'desktop']:
        raise ValueError('Pasta pessoal desconhecida.')
    if sys.platform == 'win32':
        import ctypes
        from ctypes import wintypes
        import uuid
        ids = {'documents': 'FDD39AD0-238F-46AF-ADB4-6C85480369C7',
               'videos': '18989B1D-99B5-455B-841C-AB7C74E4DDFC',
               'desktop': 'B4BFCC3A-DB2C-424C-B029-7FE99A87C641'}
        guid = (ctypes.c_ubyte * 16).from_buffer_copy(uuid.UUID(ids[kind]).bytes_le)
        result = ctypes.c_wchar_p()
        shell = ctypes.WinDLL('shell32', use_last_error=True)
        fn = shell.SHGetKnownFolderPath
        fn.argtypes = [ctypes.c_void_p, wintypes.DWORD, wintypes.HANDLE,
                       ctypes.POINTER(ctypes.c_wchar_p)]
        fn.restype = ctypes.c_long
        if fn(ctypes.byref(guid), 0x4000, None, ctypes.byref(result)) != 0:
            raise ValueError('Não consegui localizar a pasta pessoal do Windows.')
        try:
            return Path(result.value)
        finally:
            ole = ctypes.WinDLL('ole32')
            ole.CoTaskMemFree.argtypes = [ctypes.c_void_p]
            ole.CoTaskMemFree(ctypes.cast(result, ctypes.c_void_p))
    if sys.platform == 'darwin':
        term = {'documents': 'documents folder', 'videos': 'movies folder',
                'desktop': 'desktop folder'}[kind]
        try:
            result = subprocess.run(['osascript', '-e', 'POSIX path of (path to ' + term + ' without folder creation)'],
                                    capture_output=True, text=True, timeout=10, check=True)
            path = Path(result.stdout.strip())
            if path.is_absolute():
                return path
        except (OSError, subprocess.SubprocessError):
            pass
        return Path.home() / {'documents': 'Documents', 'videos': 'Movies', 'desktop': 'Desktop'}[kind]
    file = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'user-dirs.dirs'
    key = {'documents': 'DOCUMENTS', 'videos': 'VIDEOS', 'desktop': 'DESKTOP'}[kind]
    if file.exists():
        for line in file.read_text(encoding='utf-8').splitlines():
            match = re.fullmatch(r'XDG_' + key + r'_DIR=(".*")', line.strip())
            if match:
                # JSON decodifica somente a string; nenhum shell/eval é executado.
                value = json.loads(match[1]).replace('$HOME', str(Path.home()))
                path = Path(value)
                if path.is_absolute():
                    return path
    return Path.home() / {'documents': 'Documents', 'videos': 'Videos', 'desktop': 'Desktop'}[kind]
