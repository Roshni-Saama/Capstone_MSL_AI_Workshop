"""Browser QA and PDF export. Requires Playwright and an installed Edge browser."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json, os, sys
HERE=Path(__file__).resolve().parent
try:
    import playwright
except ImportError:
    sys.path.insert(0,str(Path(os.environ.get('TEMP',''))/'codex-msl-ui-playwright'))
from playwright.sync_api import sync_playwright, expect

def main():
    qa=HERE/'qa'
    qa.mkdir(exist_ok=True)
    errors=[]
    checks=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto((HERE/'index.html').as_uri(),wait_until='load')
        expect(page.locator('.slide')).to_have_count(16)
        for i in range(1,17):
            page.evaluate('(i)=>location.hash="slide="+i',i)
            expect(page.locator('.slide.active')).to_have_attribute('data-index',str(i-1))
            collisions=page.locator('.slide.active').evaluate('(slide)=>{const footer=slide.querySelector("footer").getBoundingClientRect();return [...slide.querySelector(".slide-body").children].filter(el=>el.getBoundingClientRect().bottom>footer.top-5).length}')
            checks.append({'check':f'Slide {i} content fits','passed':collisions==0})
            if i in (1,8,9,11,12):
                page.screenshot(path=str(qa/f'slide_{i:02}.png'))
        page.evaluate('location.hash="slide=1"')
        page.keyboard.press('ArrowRight')
        expect(page.locator('.slide.active')).to_have_attribute('data-index','1')
        page.get_by_role('button',name='Presenter notes',exact=True).click()
        expect(page.locator('#notes')).to_be_visible()
        page.get_by_role('button',name='Slides',exact=True).click()
        page.get_by_role('link',name='09 | A deterministic flow around bounded model calls',exact=True).click()
        expect(page.locator('.slide.active')).to_have_attribute('data-index','8')
        checks.append({'check':'Keyboard, notes and outline navigation','passed':True})
        for view in ['profile','tasks','requests','pubmed-filters','pubmed-results','trial-filters','trial-results','drafts']:
            page.evaluate('(view)=>location.hash="demo="+view',view)
            expect(page.locator('#showcase')).to_be_visible()
            page.wait_for_function('document.getElementById("demoImage").complete && document.getElementById("demoImage").naturalWidth>0')
            checks.append({'check':f'Walkthrough view {view}','passed':True})
        page.locator('#demoImage').click()
        expect(page.locator('#zoom')).to_be_visible()
        page.keyboard.press('Escape')
        expect(page.locator('#zoom')).not_to_be_visible()
        page.set_viewport_size({'width':430,'height':932})
        for i in range(1,17):
            page.evaluate('(i)=>location.hash="slide="+i',i)
            expect(page.locator('.slide.active')).to_have_attribute('data-index',str(i-1))
            checks.append({'check':f'Mobile slide {i} has no horizontal overflow','passed':not page.evaluate('document.documentElement.scrollWidth>innerWidth')})
        page.evaluate('location.hash="demo=profile"')
        checks.append({'check':'Mobile walkthrough has no horizontal overflow','passed':not page.evaluate('document.documentElement.scrollWidth>innerWidth')})
        page.set_viewport_size({'width':1440,'height':900})
        page.evaluate('location.hash="slide=1"')
        page.emulate_media(media='print')
        print_overflow=page.locator('.slide').evaluate_all('(slides)=>slides.map(slide=>{const footer=slide.querySelector("footer").getBoundingClientRect();return [...slide.querySelector(".slide-body").children].some(el=>el.getBoundingClientRect().bottom>footer.top-5)})')
        checks.append({'check':'All print slides fit before their footers','passed':not any(print_overflow)})
        page.pdf(path=str(HERE/'presentation.pdf'),print_background=True,prefer_css_page_size=True)
        offline=browser.new_context(offline=True,viewport={'width':1440,'height':900})
        local=offline.new_page()
        local.on('pageerror',lambda error:errors.append(str(error)))
        local.goto((HERE/'index.html').as_uri(),wait_until='load')
        expect(local.locator('.slide.active')).to_have_attribute('data-index','0')
        local.evaluate('location.hash="demo=profile"')
        local.wait_for_function('document.getElementById("demoImage").complete && document.getElementById("demoImage").naturalWidth>0')
        checks.append({'check':'Standalone HTML and walkthrough work offline','passed':True})
        browser.close()
    checks.append({'check':'No JavaScript exceptions','passed':not errors})
    # Optional PDF inspection using the existing temporary reader, never a project dependency.
    sys.path.insert(0,str(Path(os.environ.get('TEMP',''))/'codex-raw-review-pypdf'))
    from pypdf import PdfReader
    reader=PdfReader(str(HERE/'presentation.pdf'))
    checks.append({'check':'PDF has exactly 16 pages','passed':len(reader.pages)==16})
    extracted='\n'.join(page.extract_text() or '' for page in reader.pages)
    normalized=' '.join(extracted.split())
    checks.append({'check':'PDF includes agent roles and recorded QA counts','passed':all(text in normalized for text in ['KOL Context','Scientific Source','Follow-up Agent','126'])})
    report={'checked_at':datetime.now(ZoneInfo('Asia/Kolkata')).isoformat(timespec='seconds'),'slide_count':16,'walkthrough_views':8,'checks':checks,'javascript_errors':errors,'passed':all(item['passed'] for item in checks)}
    (qa/'presentation_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'Presentation QA: {sum(item["passed"] for item in checks)}/{len(checks)} checks passed; PDF pages: {len(reader.pages)}.')
    return 0 if report['passed'] else 1
if __name__=='__main__':
    raise SystemExit(main())
