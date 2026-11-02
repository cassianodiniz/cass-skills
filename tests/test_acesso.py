from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import acesso
import smart_config
import user_folders


class FolderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()

    def test_new_defaults_use_native_video_and_document_folders_without_writes(self):
        with patch.object(user_folders, 'conhecida', side_effect=lambda k: self.root / k):
            d = smart_config.proposta()
        self.assertEqual(d['pastas']['posts'], str(self.root / 'documents/Cass Skills/Carrosséis'))
        self.assertEqual(d['pastas']['videos']['saida'], str(self.root / 'videos/Cass Skills/Prontos'))
        self.assertFalse(d['limpeza']['habilitada'])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_explicit_base_retains_custom_layout(self):
        d = smart_config.proposta(self.root / 'escolhida')
        self.assertEqual(d['pastas']['videos']['entrada'], str(self.root / 'escolhida/videos/brutos'))

    def test_legacy_configuration_is_not_migrated_or_opted_in(self):
        with patch.dict('os.environ', {'CASS_SMART_HOME':str(self.root / 'cfg')}):
            d = smart_config.proposta(self.root / 'antiga')
            del d['limpeza']
            smart_config.salvar(d)
            self.assertEqual(smart_config.carregar(), d)
        self.assertNotIn('limpeza', d)

    def test_open_delivery_opens_its_parent_and_passes_path_as_argument(self):
        file = self.root / 'entrega com espaço.pdf'
        file.write_text('fixture')
        with patch.object(acesso.sys, 'platform', 'darwin'), patch.object(acesso.subprocess, 'run') as run:
            result = acesso.abrir(file)
        run.assert_called_once_with(['open',str(self.root)], check=True)
        self.assertTrue(result['aberta'])

    @unittest.skipIf(sys.platform == 'win32', 'Atalho Windows exige COM; ensaio separado.')
    def test_shortcut_does_not_move_or_overwrite_user_files(self):
        target = self.root / 'Pacientes'
        target.mkdir()
        with patch.object(acesso, 'conhecida', return_value=self.root):
            result = acesso.atalho('Pacientes', target)
            link = Path(result['atalho'])
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), target)
            self.assertTrue(acesso.atalho('Pacientes', target)['existente'])
            link.unlink()
            link.write_text('arquivo do usuario')
            with self.assertRaises(ValueError):
                acesso.atalho('Pacientes', target)
            self.assertEqual(link.read_text(), 'arquivo do usuario')
            with self.assertRaises(ValueError):
                acesso.atalho('../fora', target)

    def test_cleanup_preference_is_typed_and_cannot_lower_retention(self):
        d = smart_config.proposta(self.root / 'media')
        for bad in [{'habilitada':'sim','dias':30}, {'habilitada':True,'dias':1}, None]:
            with self.subTest(value=bad), self.assertRaises(ValueError):
                smart_config.validar({**d,'limpeza':bad})


if __name__ == '__main__':
    unittest.main()
