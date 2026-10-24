"""Build a portable presentation from curated slides and saved local QA evidence."""
from pathlib import Path
from html import escape
import base64, hashlib, json, re, shutil
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
P=HERE.parent
R=P/'test_scenarios/results'

def build():
    slides=json.loads((HERE/'slides.json').read_text(encoding='utf-8'))
    tree=ET.parse(R/'automated_tests.xml')
    tests=len(list(tree.iter('testcase')))
    harness=json.loads((P/'harness/results/agent_evaluation.json').read_text())
    browser=json.loads((R/'aligned_layout_browser.json').read_text())
    assert not list(tree.iter('failure')) and not list(tree.iter('error')) and harness['failed']==0
    assert all(check['passed'] for check in browser['checks'])
    image_files=set()
    def img(name,caption):
        image_files.add(name)
        data=base64.b64encode((R/name).read_bytes()).decode()
        return f'<figure><img class="zoomable" tabindex="0" src="data:image/png;base64,{data}" alt="{escape(caption)}"><figcaption>{escape(caption)}</figcaption></figure>'
    sections=[]
    for index,slide in enumerate(slides):
        body=slide['body'].replace('{{TESTS}}',str(tests)).replace('{{HARNESS}}',str(harness['total'])).replace('{{BROWSER}}',str(len(browser['checks'])))
        body=re.sub(r'\[\[image:([^|]+)\|([^\]]+)\]\]',lambda m:img(m[1],m[2]),body)
        sections.append(f'<section class="slide" data-index="{index}" aria-label="Slide {index+1}"><div class="eyebrow">{slide["kicker"]}</div><h2>{slide["title"]}</h2><p class="lead">{slide["lead"]}</p><div class="slide-body">{body}</div><footer><span>Local evidence | 24 October 2026</span><span>{index+1:02} / {len(slides):02}</span></footer></section>')
    gallery_specs=[('profile','KOL profile','crm_profile_desktop.png','Review assignment, preferences, scientific interests and the planned meeting.'),('tasks','Follow-up tasks','aligned_tasks_desktop.png','Inspect recorded status, owner, dates and overdue flags; no task is changed.'),('requests','Medical requests','aligned_requests_desktop.png','Review the question, response and source-pack status and linked task.'),('pubmed-filters','PubMed filters','aligned_pubmed_filters_desktop.png','Narrow by publication, evidence, scientific focus, affiliation and access.'),('pubmed-results','PubMed results','aligned_pubmed_results_desktop.png','Actual public-search snapshot. The visible preview is an Offline excerpt, not an AI summary.'),('trial-filters','Trial filters','aligned_trials_filters_desktop.png','Narrow by treatment, location, recruitment, phase, design and eligibility.'),('trial-results','Trial results','aligned_trials_results_desktop.png','Inspect registered details. Planned outcomes are not study results.'),('drafts','Draft workspace','presentation_draft_workspace.png','Current Offline workspace: no scientific sources were selected, so the briefing abstains. A recorded, reviewed live OpenAI output remains pending.')]
    gallery=[]
    for identifier,title,name,caption in gallery_specs:
        image_files.add(name)
        gallery.append(dict(id=identifier,title=title,caption=caption,image='data:image/png;base64,'+base64.b64encode((R/name).read_bytes()).decode()))
    template=(HERE/'template.html').read_text(encoding='utf-8')
    notes=[dict(title=re.sub('<[^>]+>','',s['title']),notes=s['notes'],refs=s['refs']) for s in slides]
    html=template.replace('__SLIDES__',''.join(sections)).replace('__GALLERY__',json.dumps(gallery).replace('</','<\\/')).replace('__NOTES__',json.dumps(notes).replace('</','<\\/'))
    (HERE/'index.html').write_text(html,encoding='utf-8')
    text='# Presenter notes | Medical Engagement Workbench\n\nPrepared 24 October 2026. Allow 12-15 minutes including a six-minute live walkthrough.\n\n'
    for i,s in enumerate(notes,1):
        text+=f'## {i:02}. {s["title"]}\n\n{s["notes"]}\n\nEvidence: '+', '.join('`'+ref+'`' for ref in s['refs'])+'\n\n'
    (HERE/'presenter-notes.md').write_text(text.rstrip()+'\n',encoding='utf-8')
    evidence=HERE/'evidence'
    evidence.mkdir(exist_ok=True)
    copies={'latest_run.txt':R/'latest_run.md','automated_tests.xml':R/'automated_tests.xml','agent_evaluation.json':P/'harness/results/agent_evaluation.json','aligned_layout_browser.json':R/'aligned_layout_browser.json','requirement-test-matrix.txt':P/'specs/requirement-test-matrix.md','evaluation-and-review.txt':P/'specs/evaluation-and-review.md'}
    for name,source in copies.items():
        shutil.copyfile(source,evidence/name)
    files=[P/'app.py',P/'agents.py',P/'workflow.py',P/'llm.py',P/'data/kol_records.json',P/'styles.css',P/'.streamlit/config.toml',HERE/'template.html',HERE/'slides.json',HERE/'build_presentation.py',*copies.values()]
    manifest=dict(prepared_on='2026-10-24',slide_count=len(slides),automated_tests_passed=tests,harness_cases_passed=harness['total'],browser_checks_passed=len(browser['checks']),live_openai_reviewed=False,public_app_deployed=False,images_embedded=True,palette='A - Navy & Azure',palette_colors={'navy':'#102A43','primary':'#2563EB','ink':'#172B4D','background':'#F4F7FC','soft':'#EFF6FF'},input_sha256={str(p.relative_to(P)).replace(chr(92),'/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},screenshots={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in sorted(image_files)})
    (HERE/'presentation-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(slides)} slides and {len(gallery)} walkthrough views. Evidence: {tests} tests, {harness["total"]} harness cases, {len(browser["checks"])} browser checks.')
if __name__=='__main__':
    build()
