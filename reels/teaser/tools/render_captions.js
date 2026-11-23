// Render each caption to desk/captions/N.png (transparent, 1080x300)
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const CAPS = JSON.parse(fs.readFileSync('desk/captions.json'));
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 300 } });
 await p.goto('file://' + path.resolve('desk/captions.html')); await p.evaluate(() => document.fonts.load('800 72px IN'));
 for (const [i, c] of CAPS.entries()) {
   await p.evaluate(h => { document.getElementById('c').innerHTML = h; }, c.html);
   const w = await p.evaluate(() => document.getElementById('c').getBoundingClientRect().width);
   if (w > 1000) console.log('WIDE', i, w);
   await p.screenshot({ path: `desk/captions/${i}.png`, omitBackground: true });
 }
 await b.close(); console.log('ok', CAPS.length); })();
