const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 for (const [f, out, omit] of [['desk/plate.html', 'desk/plate.png', false], ['desk/labels.html', 'desk/labels.png', true]]) {
   await p.goto('file://' + path.resolve(f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
   await p.screenshot({ path: out, omitBackground: omit });
   if (omit) console.log(await p.evaluate(() => ['b1','b2'].map(id => { const r = document.getElementById(id).getBoundingClientRect(); return id + ' ' + [r.left, r.top, r.width, r.height].map(Math.round).join(','); })));
 }
 await b.close(); })();
