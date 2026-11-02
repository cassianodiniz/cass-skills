"""Configuração persistente do Smart. Nunca grava dentro do plugin."""
from __future__ import annotations
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import tempfile

PLUGIN = Path(__file__).resolve().parents[1]

def dentro(path, base):
    return path == base or base in path.parents

def externo(value):
    if not isinstance(value, str) or not value.strip() or '\x00' in value:
        raise ValueError('Informe um caminho absoluto válido.')
    p = Path(value).expanduser()
    if not p.is_absolute():
        raise ValueError('A pasta precisa ter caminho absoluto.')
    p = p.resolve()
    proibidos = [PLUGIN, Path.home()/'.codex/plugins', Path.home()/'.agents/skills',
                 Path.home()/'.codex/.tmp', Path.home()/'.codex/skills',
                 Path.home()/'.claude/plugins', Path.home()/'.claude/skills']
    if any(dentro(p, x.resolve()) for x in proibidos):
        raise ValueError('Escolha uma pasta fora do plugin e do cache de skills.')
    return p

def raiz():
    return externo(os.environ.get('CASS_SMART_HOME', str(Path.home()/'.cass-smart-skills')))

def arquivo():
    return raiz()/'config.json'

def proposta(base=None):
    custom = base is not None
    if not custom:
        from user_folders import conhecida
    base = externo(str(base or conhecida('documents')/'Cass Skills'))
    videos = base/'videos' if custom else externo(str(conhecida('videos')/'Cass Skills'))
    nomes = ({'entrada':'brutos','saida':'editados','trabalho':'trabalho',
              'transcricoes':'transcricoes','aulas':'aulas'} if custom else
             {'entrada':'Originais','saida':'Prontos','trabalho':'Projetos',
              'transcricoes':'Transcrições','aulas':'Aulas'})
    return {'versao': 1, 'pastas': {
        'base': str(base), 'posts': str(base/('posts-instagram' if custom else 'Carrosséis')),
        'pesquisas': str(base/'pesquisas'),
        'videos': {k: str(videos/v) for k,v in nomes.items()}},
        'ferramentas': str(raiz()/'ferramentas'),
        'instaladores': str(raiz()/'instaladores'),
        'canva': {'template_padrao_id': None, 'template_origem_id': None},
        'video': {'perfil':'ia','headline':True,'legendas':False,'perfil_instagram':''},
        'limpeza': {'habilitada':False, 'dias':30}}

def validar(d):
    if not isinstance(d,dict) or type(d.get('versao')) is not int or d['versao'] != 1:
        raise ValueError('Versão de configuração inválida.')
    if any(not isinstance(d.get(k),dict) for k in ['canva','video','pastas']):
        raise ValueError('As seções de configuração precisam conter objetos.')
    if not isinstance(d['pastas'].get('videos'),dict):
        raise ValueError('Informe as pastas de vídeo.')
    if 'limpeza' in d:
        l=d['limpeza']
        if not isinstance(l,dict) or type(l.get('habilitada')) is not bool or type(l.get('dias')) is not int or l['dias']!=30:
            raise ValueError('Limpeza: escolha habilitada verdadeiro/falso; retenção fixa de 30 dias.')
    try:
        caminhos=[d['pastas'][k] for k in ['base','posts','pesquisas']]
        caminhos += [d['pastas']['videos'][k] for k in ['entrada','saida','trabalho','transcricoes','aulas']]
        caminhos += [d[k] for k in ['ferramentas','instaladores']]
        for p in caminhos: externo(p)
        if len(set(str(externo(p)) for p in caminhos[3:8])) != 5:
            raise ValueError('Brutos, editados, trabalho, transcrições e aulas precisam de pastas distintas.')
        for key in ['template_padrao_id','template_origem_id']:
            if d['canva'].get(key) is not None and not isinstance(d['canva'][key],str):
                raise ValueError('ID do template inválido.')
        v=d['video']
        if v['perfil'] not in ['ia','nutricao'] or any(type(v[k]) is not bool for k in ['headline','legendas']) or not isinstance(v['perfil_instagram'],str):
            raise ValueError('Preferências de vídeo inválidas.')
    except (KeyError,TypeError) as e:
        raise ValueError('Configuração incompleta.') from e
    return d

def carregar():
    p=arquivo()
    if not p.exists():
        raise ValueError('Smart ainda não configurado. Mostre a proposta de pastas e confirme com o usuário antes de salvar.')
    return validar(json.loads(p.read_text(encoding='utf-8')))

def salvar(d):
    validar(d)
    p=arquivo();p.parent.mkdir(parents=True,exist_ok=True)
    # Sem migração silenciosa: nenhuma mídia antiga é movida ou apagada.
    if p.exists():
        anterior=p.read_bytes()
        if json.loads(anterior)==d:
            preparar_instaladores(d)
            return p
        stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%Y%m%d-%H%M%S-%f')
        backup=p.with_name('config-anterior-'+stamp+'.json')
        with backup.open('xb') as f:f.write(anterior)
    paths=[d['pastas'][k] for k in ['base','posts','pesquisas']]
    paths += list(d['pastas']['videos'].values())+[d['ferramentas'],d['instaladores']]
    for value in paths:externo(value).mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.config-',dir=p.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
        os.replace(tmp,p)
    finally:
        if Path(tmp).exists():Path(tmp).unlink()
    preparar_instaladores(d)
    return p

def preparar_instaladores(d):
    validar(d)
    externo(d['instaladores']).mkdir(parents=True,exist_ok=True)
    fonte=PLUGIN/'skills/video-maker/scripts/instalar_ferramentas.py'
    if fonte.exists():
        destino=externo(d['instaladores'])/'instalar_video.py'
        if destino.exists() and destino.read_bytes()!=fonte.read_bytes():
            # Cada versão preservada; o nome estável aponta para o instalador mais recente.
            import hashlib
            antigo=destino.with_name('instalar_video-'+hashlib.sha256(destino.read_bytes()).hexdigest()[:12]+'.py')
            if not antigo.exists():shutil.copy2(destino,antigo)
        shutil.copy2(fonte,destino)
    motion=PLUGIN/'scripts/instalar_motion.mjs'
    if motion.exists():
        target=externo(d['instaladores'])/'instalar_motion.mjs'
        if target.exists() and target.read_bytes()!=motion.read_bytes():
            import hashlib
            backup=target.with_name('instalar_motion-'+hashlib.sha256(target.read_bytes()).hexdigest()[:12]+'.mjs')
            if not backup.exists():shutil.copy2(target,backup)
        shutil.copy2(motion,target)
    return externo(d['instaladores'])

def video_config():
    d=carregar()
    return {'versao':1,'sistema':{'darwin':'mac-apple-silicon' if __import__('platform').machine()=='arm64' else 'mac-intel','win32':'windows'}.get(__import__('sys').platform,'linux'),
            'origem':'pasta','entrega':'pasta',**d['video'],'pastas':d['pastas']['videos'],
            'ferramentas':str(externo(d['ferramentas'])/'video-maker')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='acao',required=True)
    plan=sub.add_parser('propor');plan.add_argument('--base')
    sub.add_parser('ler');sub.add_parser('video');sub.add_parser('preparar-instaladores')
    save=sub.add_parser('salvar');save.add_argument('--dados',required=True)
    a=p.parse_args()
    try:
        if a.acao=='salvar':print(salvar(json.loads(Path(a.dados).read_text(encoding='utf-8'))))
        elif a.acao=='preparar-instaladores':print(preparar_instaladores(carregar()))
        else:print(json.dumps(proposta(a.base) if a.acao=='propor' else video_config() if a.acao=='video' else carregar(),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
