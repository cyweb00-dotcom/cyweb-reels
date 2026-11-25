const { chromium } = require('playwright'); const fs = require('fs');
const [a, b] = process.argv.slice(2).map(Number);
(async () => { const br = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
 const p = await br.newPage({ viewport: { width: 1920, height: 1080 } }); p.on('pageerror', e => console.error('ERR', e.message));
 await p.goto('http://127.0.0.1:8801/hero.html'); await p.waitForFunction(() => window.DONE, null, { timeout: 120000 });
 fs.mkdirSync('out/raw', { recursive: true });
 for (let f = a; f <= b; f++) { await p.evaluate(t => window.setT(t), f / 30); await p.screenshot({ path: `out/raw/${String(f).padStart(4, '0')}.png` }); }
 await br.close(); })();
