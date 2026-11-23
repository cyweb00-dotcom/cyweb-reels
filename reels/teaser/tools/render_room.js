// Render the room passes (needs: python3 -m http.server 8765 in reels/teaser)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
 const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 p.on('pageerror', e => console.log('ERR', e.message));
 const only = process.argv[2];
 const jobs = [['base', ''], ['depth', ''], ...[0, 1, 2, 3, 4, 5].map(k => ['light', k])].filter(([m]) => !only || only === m);
 fs.mkdirSync('desk/room', { recursive: true });
 for (const [mode, k] of jobs) {
   await p.goto(`http://127.0.0.1:8765/desk/room.html?mode=${mode}&k=${k}`); await p.waitForFunction(() => window.DONE, null, { timeout: 300000 });
   const name = mode === 'light' ? `light${k}` : mode;
   await p.screenshot({ path: `desk/room/${name}.png` });
   if (mode === 'base') { fs.writeFileSync('desk/room/corners.json', JSON.stringify(await p.evaluate(() => window.corners()))); fs.writeFileSync('desk/room/monitor_top.json', JSON.stringify(await p.evaluate(() => window.monitorTop()))); }
   console.log('done', name);
 }
 await b.close(); })();
