"""Offline REPO-R1 compatibility checks, following the LAYOUT-R1 relocation map.

Run from a full Git checkout with the baseline commit available. Default is
read-only. --write-receipt writes a separate layout-compatibility receipt and
never overwrites the original REPO-R1 validation.json.
External link availability, native app/UI behavior and physical correctness are
not tested. The inventory unit receipt must match the current scanner/test source.
"""
from __future__ import annotations
import argparse,ast,collections,hashlib,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[2]
REVIEW=ROOT/'docs/repository_review'

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def text_hash(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()

def check(creating_receipt=False):
    pending_output=(ROOT/'reports/repository_review/layout-review-compatibility.json').resolve() if creating_receipt else None
    relocation=json.loads((ROOT/'archive/relocation-manifest.json').read_text())
    moved={m['old_path']:m['new_path'] for m in relocation['moves']}
    def locate(path):return ROOT/moved.get(path,path)
    reg=json.loads((REVIEW/'gap-register.json').read_text(encoding='utf-8'))
    inv=json.loads((REVIEW/'baseline-inventory.json').read_text(encoding='utf-8'))
    base=reg['baseline_commit'];assert inv['baseline_commit']==base
    before={r['path']:r for r in inv['files']}
    tracked=[p for p in git('ls-tree','-r','--name-only',base).decode().splitlines() if not Path(p).name.lower().startswith('license')]
    assert set(before)==set(tracked),'Baseline inventory incomplete'
    findings=reg['findings'];ids=[g['id'] for g in findings]
    assert len(ids)==len(set(ids))
    ranks=[g['priority_rank'] for g in findings];assert ranks==list(range(1,len(findings)+1))
    severity={'critical':0,'high':1,'medium':2,'low':3}
    assert [severity[g['severity']] for g in findings]==sorted(severity[g['severity']] for g in findings)
    for g in findings:
        assert set(g['six_hats'])=={'white','red','black','yellow','green','blue'}
        assert all(g['six_hats'].values()) and g['decision'] and g['remaining_action'] and g['resolution_status']
        for path in g['changed_paths']:assert locate(path).is_file() or locate(path).resolve()==pending_output,(g['id'],'Missing deliverable',path)
        for e in g['evidence']:
            assert e['baseline_commit']==base
            original=git('show',f"{base}:{e['path']}")
            assert hashlib.sha256(original).hexdigest()==before[e['path']]['baseline_blob_sha256']
            assert 1<=e['line']<=len(original.decode('utf-8-sig').splitlines())
    # Preserve actual engineering/native assets, old executables and example data.
    preserved=[]
    legacy_paths={
        'software/arduino/telemetry_logger_stub/telemetry_logger_stub.ino',
        'software/raspberry_pi/src/jom_data_logger.py',
        'software/raspberry_pi/config/data_logger_config.template.yaml',
        'software/raspberry_pi/requirements.txt','configs/classes.yaml','configs/datasets.yaml',
        'reports/dataset_inventory.json','reports/model_runs/sample_run.json',
        'src/junkomatic/__init__.py','src/junkomatic/config.py','src/junkomatic/reporting.py',
        'scripts/download/bootstrap_datasets.py'}
    tree={}
    for line in git('ls-tree','-r',base).decode().splitlines():
        meta,path=line.split('\t');tree[path]=meta.split()[2]
    for path in tracked:
        protect=(path.startswith(('hardware/v2/','software/v2/','reports/v2/')) or
                 Path(path).suffix in {'.pdf','.FCStd','.step','.png','.xlsx','.docx'} or
                 path in legacy_paths or path.startswith('validation/sample_data/') and path.endswith('.csv'))
        if protect:
            if Path(path).suffix=='.md':continue # Navigation edits are covered by the new layout check.
            dest=moved.get(path,path)
            current=git('hash-object','--path',dest,dest).decode().strip()
            assert current==tree[path],('Protected baseline changed',path)
            preserved.append(path)
    held=json.loads((ROOT/'docs/reconciliation/export-status.json').read_text())['held_pdfs']
    for p in held:assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
    # These three legacy pages must keep their original bodies beneath the new notice.
    for p in ('docs/project_scope_v1a.md','docs/test_procedure_v1a.md','docs/v1_to_v2_exit_criteria.md'):
        assert locate(p).read_text(encoding='utf-8').strip().endswith(git('show',f'{base}:{p}').decode().strip()),p
    def declarations(data):return [s.strip() for s in data.splitlines() if s.strip() and not s.lstrip().startswith('#')]
    assert declarations(locate('requirements.txt').read_text())==declarations(git('show',f'{base}:requirements.txt').decode())
    # New/revised documentation only: unchanged historical sources retain their own scope.
    changed=set(git('diff','--name-only',base).decode().splitlines())
    changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
    markdown=sorted({locate(p) for p in changed if p.endswith('.md') and locate(p).is_file()})
    links=0
    for p in markdown:
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
            if target.startswith(('http://','https://','mailto:','#')):continue
            dest=unquote(target.split('#')[0]).strip('<>')
            assert (p.parent/dest).exists() or (p.parent/dest).resolve()==pending_output,('Broken local link',p.relative_to(ROOT).as_posix(),target)
            links+=1
    syntax=[]
    for p in sorted({locate(p) for p in changed if p.endswith('.py') and locate(p).is_file()}):
        ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p));syntax.append(p.relative_to(ROOT).as_posix())
    tests=json.loads((ROOT/'reports/repository_review/inventory-tests.json').read_text())
    assert tests['passed'] and tests['tests_run']==8
    for path,digest in tests['source_sha256_lf'].items():assert text_hash(locate(path).read_bytes())==digest,('Unit receipt stale',path)
    reproduction=json.loads((ROOT/'reports/repository_review/legacy-parser-reproduction.json').read_text())
    assert reproduction['legacy_counted_rows']==1 and len(reproduction['blank_measurement_columns'])==9 and not reproduction['real_serial_opened']
    for path in ('data/external/example.jpg','reports/local/dataset_inventory.json','.venv-v2/pyvenv.cfg','runs/example/serial.raw','test_data/example/video.mp4','config.local.yml'):
        r=subprocess.run(['git','check-ignore','-q',path],cwd=ROOT);assert r.returncode==0,('Not ignored',path)
    assert len((REVIEW/'github-about.txt').read_text().strip())<=350
    return {'revision':'LAYOUT-R1 / REPO-R1 compatibility','review_date':reg['review_date'],'baseline_commit':base,
            'baseline_files_excluding_license':len(tracked),'legacy_files_reviewed':sum(r['commit_date']<'2026-06-01' for r in before.values()),
            'findings_by_severity':dict(collections.Counter(g['severity'] for g in findings)),
            'checks':[{'name':'Prioritized register, all six hats, baseline citations and deliverable paths','result':'passed','findings':len(findings)},
                      {'name':'Revised/new Markdown local file links','result':'passed','links_checked':links,'documents_checked':len(markdown)},
                      {'name':'Preserved engineering/legacy/example sources (Git normalized blobs)','result':'passed','files':len(preserved)},
                      {'name':'Held PDF byte hashes','result':'passed','files':len(held)},
                      {'name':'Historical page bodies and root dependency declarations retained','result':'passed'},
                      {'name':'Changed Python AST syntax','result':'passed','files':syntax},
                      {'name':'Inventory behavior unit receipt and source correspondence','result':'passed','tests':tests['tests_run']},
                      {'name':'Legacy parser mismatch reproduced using fake serial only','result':'passed'},
                      {'name':'Local evidence/dataset/output/venv ignore rules','result':'passed'}],
            'limits':['License content/interpretation excluded as requested.',
                      'No physical test, serial hardware contact, software upload, Pi deployment, native-app or Streamlit/browser run.',
                      'External URL availability, dependency security/locking and full historical runtime hardening not tested.',
                      'Original engineering receipts remain historical; unrelated firmware/CAD test suites not rerun.',
                      'Original REPO-R1 records retain their historical paths/status; this compatibility check follows archive relocation.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write-receipt',action='store_true');a=p.parse_args()
    result=check(a.write_receipt)
    if a.write_receipt:
        (ROOT/'reports/repository_review/layout-review-compatibility.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
