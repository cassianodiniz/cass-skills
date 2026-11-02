"""Instaladores copiados não podem instalar em caches substituídos por updates."""
from contextlib import redirect_stderr
import io
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class InstallerLocations(unittest.TestCase):
    def test_video_installer_rejects_all_host_caches_before_creating_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            # Simula a cópia externa preservada, fora da distribuição original.
            installer = home / 'app/instaladores/instalar_video.py'
            installer.parent.mkdir(parents=True)
            installer.write_bytes((ROOT / 'skills/video-maker/scripts/instalar_ferramentas.py').read_bytes())
            for cache in ['.claude/plugins', '.claude/skills', '.codex/plugins',
                          '.codex/skills', '.codex/.tmp', '.agents/skills']:
                with self.subTest(cache=cache):
                    destination = home / cache / 'runtime'
                    error = io.StringIO()
                    with patch.object(Path, 'home', return_value=home), \
                         patch.object(sys, 'argv', [str(installer), '--destino', str(destination)]), \
                         patch('venv.EnvBuilder.create', side_effect=AssertionError('Tentou criar ambiente no cache')), \
                         redirect_stderr(error), self.assertRaises(SystemExit) as raised:
                        runpy.run_path(str(installer), run_name='__main__')
                    self.assertEqual(raised.exception.code, 2)
                    self.assertIn('fora da pasta do plugin', error.getvalue())
                    self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
