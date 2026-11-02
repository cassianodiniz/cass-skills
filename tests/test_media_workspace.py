import datetime as dt
import json
import os
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import media_workspace as media


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.work = self.base / 'Projetos'
        self.work.mkdir()
        self.original = self.base / 'Originais' / 'fala.mp4'
        self.original.parent.mkdir()
        self.original.write_bytes(b'original')
        self.final = self.base / 'Prontos' / 'video.mp4'
        self.final.parent.mkdir()
        self.final.write_bytes(b'final aprovado')
        self.pastas = {'trabalho': str(self.work), 'entrada': str(self.original.parent),
                       'saida': str(self.final.parent), 'aulas': str(self.base / 'Aulas'),
                       'transcricoes': str(self.base / 'Transcricoes')}
        self.now = dt.datetime(2026, 11, 2, 12, tzinfo=dt.timezone.utc)
        self.old = self.now - dt.timedelta(days=31)
        self.clock = patch.object(media, 'agora', return_value=self.old)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.project = self.work / 'meu-video'
        media.iniciar(self.project, self.pastas)
        self.recipe = self.project / 'plano.json'
        self.recipe.write_text('{"edicao":"sintetica"}')
        self.file = self.project / 'descartaveis' / 'previa.mp4'
        self.file.write_bytes(b'previa descartavel')
        media.registrar(self.project, self.file, [self.original], self.recipe,
                        ['python', 'montar.py', str(self.recipe)], self.pastas)
        os.utime(self.file, (self.old.timestamp(), self.old.timestamp()))

    def clean(self, enabled=True):
        return media.limpar(self.pastas, enabled, now=self.now)

    def close(self):
        media.encerrar(self.project, self.final, self.pastas)

    def test_requires_opt_in(self):
        self.close()
        self.assertEqual(self.clean(False)['removidos'], [])
        self.assertTrue(self.file.exists())

    def test_only_registered_stale_intermediate_is_removed(self):
        self.close()
        other = self.file.with_name('nao-registrado.mp4')
        other.write_bytes(b'do usuario')
        result = self.clean()
        self.assertEqual(result['bytes_removidos'], len(b'previa descartavel'))
        self.assertFalse(self.file.exists())
        for file in [other, self.final, self.original, self.recipe]:
            self.assertTrue(file.exists())
        self.assertEqual(self.clean()['removidos'], [])

    def test_active_project_is_preserved(self):
        self.assertEqual(self.clean()['removidos'], [])
        self.assertTrue(self.file.exists())

    def test_other_operation_locks_project_and_cleanup_preserves_it(self):
        self.close()
        with media.travar(self.project):
            result=self.clean()
            self.assertEqual(result['removidos'],[])
            self.assertTrue(result['avisos'])
            with self.assertRaises(ValueError):
                media.iniciar(self.project,self.pastas)
        self.assertTrue(self.file.exists())
        self.assertFalse((self.project/'.cass-media.lock').exists())

    def test_reopening_resets_retention_and_activity(self):
        self.close()
        with patch.object(media, 'agora', return_value=self.now):
            media.iniciar(self.project, self.pastas)
        self.assertEqual(self.clean()['removidos'], [])
        self.assertTrue(self.file.exists())

    def test_recent_close_and_recently_modified_artifact_are_preserved(self):
        with patch.object(media, 'agora', return_value=self.now):
            self.close()
        self.assertTrue(self.clean()['removidos'] == [])
        self.close()
        os.utime(self.file, (self.now.timestamp(), self.now.timestamp()))
        self.assertEqual(self.clean()['removidos'], [])

    def test_changed_file_or_missing_source_prevents_cleanup(self):
        self.close()
        self.file.write_bytes(b'alterado pelo usuario')
        os.utime(self.file, (self.old.timestamp(), self.old.timestamp()))
        self.assertEqual(self.clean()['removidos'], [])
        self.file.write_bytes(b'previa descartavel')
        self.original.unlink()
        self.assertEqual(self.clean()['removidos'], [])

    def test_changed_recipe_source_or_final_prevents_cleanup(self):
        self.close()
        for path in [self.recipe, self.original, self.final]:
            before = path.read_bytes()
            path.write_bytes(b'modificado')
            self.assertEqual(self.clean()['removidos'], [])
            self.assertTrue(self.file.exists())
            path.write_bytes(before)

    def test_source_in_disposable_folder_is_not_recreatable(self):
        with self.assertRaises(ValueError):
            media.registrar(self.project, self.file, [self.file], self.recipe,
                            ['python', 'montar.py'], self.pastas)

    def test_rejects_original_final_and_traversal_registration(self):
        for file in [self.original, self.final, self.project / '../fora.mp4']:
            with self.subTest(file=file), self.assertRaises(ValueError):
                media.registrar(self.project, file, [self.original], self.recipe,
                                ['python', 'montar.py'], self.pastas)

    def test_no_legacy_folder_is_adopted(self):
        legacy = self.work / 'antigo'
        legacy.mkdir()
        (legacy / 'video.mp4').write_bytes(b'antigo')
        result=self.clean()
        self.assertTrue(result['avisos'])
        self.assertTrue((legacy / 'video.mp4').exists())

    def test_corrupt_manifest_is_reported_and_preserved(self):
        (self.project / media.MANIFEST).write_text('{invalid')
        result = self.clean()
        self.assertTrue(result['avisos'])
        self.assertTrue(self.file.exists())

    def test_symlink_or_hardlink_is_never_removed(self):
        self.close()
        self.file.unlink()
        self.file.symlink_to(self.original)
        self.assertEqual(self.clean()['removidos'], [])
        self.assertTrue(self.original.exists())
        self.file.unlink()
        os.link(self.original, self.file)
        self.assertEqual(self.clean()['removidos'], [])

    def test_symlink_project_and_overlapping_roots_are_rejected(self):
        link = self.work / 'alias'
        link.symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(ValueError):
            media.iniciar(link, self.pastas)
        bad = {**self.pastas, 'saida': str(self.work / 'finais')}
        with self.assertRaises(ValueError):
            media.iniciar(self.work / 'novo', bad)

    def test_tampered_path_cannot_escape_project(self):
        self.close()
        manifest = self.project / media.MANIFEST
        data = json.loads(manifest.read_text())
        data['artefatos'][0]['arquivo']['caminho'] = '../../Originais/fala.mp4'
        manifest.write_text(json.dumps(data))
        self.assertEqual(self.clean()['removidos'], [])
        self.assertTrue(self.original.exists())

    def test_cli_uses_utf8_bom_and_protects_current_project_before_cleanup(self):
        import smart_config
        config_home = self.base / 'config'
        config_home.mkdir()
        cfg = smart_config.proposta(self.base / 'media')
        cfg['pastas']['videos'] = self.pastas
        cfg['limpeza']['habilitada'] = True
        (config_home / 'config.json').write_text(json.dumps(cfg,ensure_ascii=False),encoding='utf-8')
        effective = self.base / 'pastas-com-acentos.json'
        effective.write_text(json.dumps(self.pastas,ensure_ascii=False),encoding='utf-8-sig')
        self.close()
        p = subprocess.run([sys.executable,str(ROOT/'scripts/media_workspace.py'),
                            '--pastas',str(effective),'limpar','--atual',str(self.project)],
                           env={**os.environ,'CASS_SMART_HOME':str(config_home)},
                           capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout)['removidos'],[])
        self.assertTrue(self.file.exists())
        self.assertEqual(json.loads((self.project/media.MANIFEST).read_text())['estado'],'em_andamento')

    def test_two_immutable_render_paths_can_be_registered(self):
        next_file = self.file.with_name('previa-v2.mp4')
        next_file.write_bytes(b'outra versao')
        media.registrar(self.project,next_file,[self.original],self.recipe,
                        ['node','render.mjs',str(self.project),'--saida',next_file.name],self.pastas)
        state=json.loads((self.project/media.MANIFEST).read_text())
        self.assertEqual(len(state['artefatos']),2)
        self.assertEqual(self.file.read_bytes(),b'previa descartavel')


if __name__ == '__main__':
    unittest.main()
