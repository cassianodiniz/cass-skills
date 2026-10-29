from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/carrossel/scripts'))
import estado
import revisar_copy

class InitFailureTests(unittest.TestCase):
    def test_process_init_failure_prepares_session_subagent(self):
        for error in [PermissionError('restrição do ambiente'),FileNotFoundError('executável não encontrado')]:
            with self.subTest(error=type(error).__name__), tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)
                for name,txt in [('copy.md','Texto original'),('fatos.md','Fatos fornecidos'),('eixo.md','Eixo'),('regras.md','Regras')]:
                    (p/name).write_text(txt)
                st=estado.registrar_estrutura(estado.criar_estado('teste'),'Eixo')
                estado.aprovar_estrutura(st,st['estrutura_hash']);st=estado.registrar_copy(st,'Texto original')
                estado.salvar_estado(p/'estado.json',st)
                out=p/'nova-pasta/revisao.json'
                with patch.object(revisar_copy.subprocess,'run',side_effect=error):
                    with self.assertRaises(revisar_copy.UsarSubagente) as ctx:
                        revisar_copy.revisar(p/'copy.md',p/'fatos.md',p/'eixo.md',p/'regras.md',p/'estado.json',out,codex_command='codex-fixture')
                self.assertTrue(ctx.exception.prompt_path.exists())
                self.assertIn('Texto original',ctx.exception.prompt_path.read_text())
                after=estado.carregar_estado(p/'estado.json')
                self.assertEqual(after['revisor_rodadas'],0)
                self.assertEqual(after['fase_detalhe'],'gpt_falhou_usar_subagente')
                self.assertEqual((p/'copy.md').read_text(),'Texto original')

if __name__=='__main__':unittest.main()
