from playwright.sync_api import sync_playwright
from pathlib import Path
import json, shutil
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium') or None,args=['--no-sandbox']); page=b.new_page(viewport={'width':1280,'height':900}); errors=[]; page.on('pageerror',lambda e:errors.append(str(e))); page.set_content((root/'index.html').read_text(encoding='utf-8')); checks=[]
    assert page.locator('#prev').is_disabled(); checks.append('first-page boundary')
    for i in range(1,16):
        assert page.locator('#count').inner_text()==f'{i} / 15'
        assert page.locator('.sources a').count()>1
        if i<15: page.locator('#next').click()
    assert page.locator('#next').is_disabled(); checks.append('15 pages, citations, last-page boundary')
    page.locator('[data-i="3"]').click(); page.locator('#obp').fill('0.5'); assert page.locator('#ops').inner_text()=='1.100'; checks.append('OPS slider')
    page.locator('[data-i="7"]').click(); page.locator('#hr').fill('20'); assert page.locator('#fip').inner_text()=='4.60'; checks.append('FIP slider')
    page.locator('[data-i="14"]').click(); page.locator('[data-q="0"]').nth(1).click(); assert '再試' in page.locator('#feedback0').inner_text(); page.locator('[data-q="0"]').first.click(); assert '答對' in page.locator('#feedback0').inner_text(); checks.append('quiz feedback')
    page.keyboard.press('ArrowLeft'); assert page.locator('#count').inner_text()=='14 / 15'; checks.append('keyboard navigation')
    page.set_viewport_size({'width':390,'height':844}); assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'); checks.append('mobile width')
    assert not errors,errors; checks.append('no JavaScript page errors'); b.close()
    (root/'logs/browser_test.json').write_text(json.dumps({'passed':checks,'errors':errors},indent=2),encoding='utf-8'); print('\n'.join(checks))
