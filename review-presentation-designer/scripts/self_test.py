#!/usr/bin/env python3
"""Minimal package smoke test: generation, editability and epistemic validation."""
import json
import csv
import sys
import tempfile
import subprocess
from pathlib import Path
from pptx import Presentation
from validate_review_plan import validate

ROOT=Path(__file__).resolve().parents[1]
DEMO=json.loads((ROOT/'examples/demo_review_plan.json').read_text(encoding='utf-8'))
assert len(DEMO['slides'])==15
check=validate(DEMO,[],[],strict=True,plan_dir=ROOT/'examples')
assert check['errors']==0,check

sources=[dict(source_id='S001',title='Example verified original',authors='Test author',year='2025',
              doi_or_url='',source_file='paper.pdf',identity_status='verified_original')]
claims=[dict(claim_id='C001',claim_text='Paper states a tested finding',epistemic_status='source_reported',
             verification_status='verified_against_source',source_ids='S001',source_locator='Table 1',
             verification_basis='',comparability_scope='same endpoint/split',limitations='',slide_ids='2')]
prod=dict(mode='production',slides=[dict(type='cover',title='Review test'),
       dict(type='big_idea',title='Test claim',claim_ids=['C001'],source_ids=['S001'],
            epistemic_status='source_reported',statement='Source claim',pillars=['A','B','C'])])
assert validate(prod,claims,sources,strict=True)['errors']==0
bad_claims=[dict(claims[0],source_ids='S404')]
assert validate(prod,bad_claims,sources,strict=True)['errors']>=1
claims[0]['epistemic_status']='independently_verified'
assert validate(prod,claims,sources,strict=True)['errors']>=1, 'Independent verification must have a basis'

with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'smoke.pptx'
    subprocess.run([sys.executable,str(ROOT/'scripts/build_review_deck.py'),
                    '--plan',str(ROOT/'examples/demo_review_plan.json'),
                    '--out',str(out)],check=True,capture_output=True,text=True)
    prs=Presentation(out)
    assert len(prs.slides)==15
    text_shapes=sum(1 for sl in prs.slides for sh in sl.shapes if sh.has_text_frame and sh.text.strip())
    picture_shapes=sum(1 for sl in prs.slides for sh in sl.shapes if sh.shape_type==13)
    assert text_shapes>150,(text_shapes,picture_shapes)
    assert picture_shapes==1,picture_shapes
    # A real project will produce these CSV files from inspected original papers.
    srcfile=Path(td)/'sources.csv'
    with srcfile.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=sources[0].keys()); w.writeheader(); w.writerows(sources)
    baseclaim=dict(claims[0],epistemic_status='source_reported')
    claimfile=Path(td)/'claims.csv'
    with claimfile.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=baseclaim.keys()); w.writeheader(); w.writerow(baseclaim)
    prodfile=Path(td)/'prod.json'
    prodfile.write_text(json.dumps(prod,ensure_ascii=False),encoding='utf-8')
    proddeck=Path(td)/'production.pptx'
    subprocess.run([sys.executable,str(ROOT/'scripts/build_review_deck.py'),
                    '--plan',str(prodfile),'--claims',str(claimfile),
                    '--sources',str(srcfile),'--out',str(proddeck)],check=True,capture_output=True,text=True)
    assert len(Presentation(proddeck).slides)==2
print('PASS: 15-slide demo, native-editable text shapes, figure embedding and source-validation guards')
