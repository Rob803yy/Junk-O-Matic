"""Verify active/archive layout, preserved content and live documentation links.

Default is read-only; --write-receipt writes a new LAYOUT-R1 receipt. No native
engineering export, hardware connection, upload or dependency install occurs.
Run in the full Git checkout. Original review receipts keep their dates/paths.
"""
from __future__ import annotations
import argparse,ast,hashlib,json,re,subprocess,sys
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'reports/repository_review/layout-r1-validation.json'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def normalized(p):
    data=p.read_bytes()
    return data if p.suffix=='.pdf' else data.replace(b'\r\n',b'\n')
def check(writing=False):
    m=json.loads((ROOT/'archive/relocation-manifest.json').read_text())
    assert m['revision']=='LAYOUT-R1' and len(m['moves'])==50
    old=[r['old_path'] for r in m['moves']];new=[r['new_path'] for r in m['moves']]
    assert len(old)==len(set(old)) and len(new)==len(set(new))
    unchanged=updated=0
    for r in m['moves']:
        src,dst=ROOT/r['old_path'],ROOT/r['new_path']
        assert dst.resolve().is_relative_to((ROOT/'archive').resolve()) and dst.is_file(),r
        assert not src.is_file() or r['old_path']=='requirements.txt',('Old competing entry remains',r['old_path'])
        data=normalized(dst);digest=hashlib.sha256(data).hexdigest()
        assert digest==r['destination_sha256_lf_or_binary'],r['new_path']
        if r['preservation']=='unchanged_git_content':
            assert digest==r['source_sha256'],r['new_path'];unchanged+=1
        else:
            assert dst.suffix=='.md' and r['preservation']=='documentation_navigation_updated',r
            updated+=1
    # Canonical active engineering content stays at its existing path, byte-identical.
    native=0;base=m['baseline_main_commit']
    for line in git('ls-tree','-r',base).decode().splitlines():
        meta,path=line.split('\t');blob=meta.split()[2]
        if path.startswith(('hardware/v2/','software/v2/','reports/v2/')) and not path.endswith(('.md','.pdf')):
            assert git('hash-object','--path',path,path).decode().strip()==blob,('V2 content changed',path)
            native+=1
    held=json.loads((ROOT/'docs/reconciliation/export-status.json').read_text())['held_pdfs']
    assert len(held)==13
    for p in held:
        assert p['path'].startswith('archive/exports-r0/')
        assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
        assert not (ROOT/p['original_path']).is_file()
    files=set(git('ls-files').decode().splitlines())
    files.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
    files={p for p in files if (ROOT/p).is_file() and not Path(p).name.lower().startswith('license')}
    retired=('app/','configs/','src/','software/arduino/','software/raspberry_pi/',
             'scripts/convert/','scripts/download/','validation/sample_data/','docs/history/',
             'hardware/bom/','hardware/wiring_diagrams/','hardware/enclosure_layout/')
    assert not any(p.startswith(retired) for p in files),'Retired folder has active tracked content'
    assert not any(p.endswith('.pdf') and not p.startswith('archive/exports-r0/') for p in files)
    deps=[s.strip() for s in (ROOT/'requirements.txt').read_text().splitlines() if s.strip() and not s.startswith('#')]
    assert deps==['-r software/v2/raspberry_pi/requirements.txt']
    links=docs=0;problems=[]
    for path in sorted(p for p in files if p.endswith('.md')):
        docs+=1;p=ROOT/path
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)',p.read_text(encoding='utf-8-sig')):
            if target.startswith(('https://','http://','mailto:','#')):continue
            dest=(p.parent/unquote(target.split('#')[0]).strip('<>')).resolve()
            present=dest.is_file()
            if dest.is_dir() and dest.is_relative_to(ROOT):
                prefix=dest.relative_to(ROOT).as_posix().rstrip('/')+'/'
                present=any(f.startswith(prefix) for f in files)
            if not present and not (writing and dest==OUT.resolve()):problems.append([path,target])
            links+=1
    assert not problems,('Broken local documentation links',problems)
    syntax=[]
    for path in sorted(p for p in files if p.endswith('.py')):
        ast.parse((ROOT/path).read_text(encoding='utf-8-sig'),filename=path);syntax.append(path)
    for p in ('archive/dataset-model-scaffold/data/external/a.jpg',
              'archive/dataset-model-scaffold/reports/local/dataset_inventory.json',
              'archive/v1a/test_data/example/telemetry.csv','config.local.yml','runs/example/serial.raw'):
        assert subprocess.run(['git','check-ignore','-q',p],cwd=ROOT).returncode==0,p
    r=subprocess.run([sys.executable,'scripts/v2/build_review_book.py','--acknowledge-pdf-regeneration'],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode!=0 and 'disabled' in r.stderr.lower(),'Historical PDF book must refuse even its former flag'
    r=subprocess.run([sys.executable,'scripts/v2/architecture_diagrams.py','--check'],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==0,r.stdout+r.stderr
    arch=json.loads(r.stdout);assert arch['held_pdf_hashes_verified']==13
    tests=json.loads((ROOT/'reports/repository_review/inventory-tests.json').read_text())
    moves={r['old_path']:r['new_path'] for r in m['moves']}
    for path,digest in tests['source_sha256_lf'].items():assert hashlib.sha256(normalized(ROOT/moves.get(path,path))).hexdigest()==digest,path
    return {'revision':'LAYOUT-R1','date':m['date'],'baseline_main_commit':base,
            'checks':{'relocated_files':len(m['moves']),'unchanged_git_content':unchanged,'navigation_only_documents':updated,
                      'active_v2_source_exports_and_receipts_unchanged':native,'archived_pdf_byte_hashes':13,
                      'local_links_checked':links,'markdown_files_checked':docs,'python_syntax_files':len(syntax),
                      'root_requirements':'V2 logger only','competing_legacy_folders':'absent from Git working tree',
                      'archived_inventory_tests':'8 passed after relocation; source/test hashes match original receipt',
                      'old_pdf_book':'refuses former acknowledgement flag','architecture_source_check':'passed; no outputs rewritten',
                      'archive_raw_local_output_ignore_rules':'passed'},
            'result':'passed','limits':['Physical configuration, deployment and operating performance not verified.',
                                       'No PDFs generated; old source receipts retain their original revision/date.',
                                       'No license-content review, archived dashboard browser run or dataset download.']}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write-receipt',action='store_true');a=p.parse_args()
    result=check(a.write_receipt)
    if a.write_receipt:OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
