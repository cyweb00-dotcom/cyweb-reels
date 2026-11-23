// Render the 3D desk set (beauty + magenta-keyed screen) via a local http server on :8765
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
 const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
 for (const mode of ['beauty', 'key']) {
   await p.goto(`http://127.0.0.1:8765/desk/set3d.html?mode=${mode}`); await p.waitForFunction(() => window.DONE, null, { timeout: 120000 });
   if (mode === 'beauty') console.log(JSON.stringify({ corners: await p.evaluate(() => window.project()), ball: await p.evaluate(() => window.ballPx()), kb: await p.evaluate(() => window.kbPx()) }));
   await p.screenshot({ path: `desk/set_${mode}.png` });
 }
 await b.close(); })();
