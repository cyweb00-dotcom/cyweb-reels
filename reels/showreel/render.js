// Render frames: node render.js <first> <last>   -> out/frames/NNNN.png
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const [a, b] = process.argv.slice(2).map(Number);
(async () => {
  fs.mkdirSync('out/frames', { recursive: true });
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.addInitScript(d => { window.LOGO_DATA = d; }, 'data:image/png;base64,' + fs.readFileSync('img/cy-mark-light.png').toString('base64'));
  p.on('pageerror', e => console.error('ERR', e.message));
  await p.goto('file://' + path.resolve('index.html')); await p.evaluate(() => window.READY);
  for (let f = a; f <= b; f++) {
    const url = await p.evaluate(f => window.drawFrame(f), f);
    fs.writeFileSync(`out/frames/${String(f).padStart(4, '0')}.png`, Buffer.from(url.split(',')[1], 'base64'));
  }
  await br.close();
})();
