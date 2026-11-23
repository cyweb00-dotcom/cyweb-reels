// Render the screen film frame by frame (with sub-frames for motion blur).
// Streams PNG sub-frames to stdout as [u32 frame][u32 sub][u32 nsub][u32 len][png].
// usage: node tools/render_film.js <first> <last> [nsub]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const [first, last, nsubArg] = process.argv.slice(2).map(Number);
const NSUB = nsubArg || 5;
const shutter = f => (f >= 204 && f <= 290) ? 1.0 : 0.5;   // 360° in the whip and the count, 180° elsewhere
(async () => {
  const b = await chromium.launch({ args: ['--disable-gpu-vsync', '--force-device-scale-factor=1'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const screens = {};
  for (let i = 1; i <= 4; i++) { const f = path.resolve(__dirname, `../assets/screens/${i}.png`); if (fs.existsSync(f)) screens[i] = 'data:image/png;base64,' + fs.readFileSync(f).toString('base64'); }
  await p.addInitScript(s => { window.USER_SCREENS = s; }, screens);
  await p.goto('file://' + path.resolve(__dirname, '../film/index.html'));
  await p.evaluate(() => window.READY);
  await p.waitForTimeout(300);
  for (let k = first; k <= last; k++) {
    const F1 = k + 1;
    // whip: 12 sub-frames for smooth heavy blur; count: 2 sub-frames = the reference's 2-frame blend
    const n = (F1 >= 205 && F1 <= 243) ? 12 : (F1 >= 244 && F1 <= 288) ? 2 : NSUB, sh = shutter(F1);
    for (let s = 0; s < n; s++) {
      // count beat: the reference shows frame n-1 blended with frame n
      const off = (n === 2) ? (s - 1) : n === 1 ? 0 : (s / (n - 1) - 0.5) * sh;
      await p.evaluate(f => window.seekFrame(f), Math.max(0, k + off));
      const png = await p.screenshot({ type: 'png' });
      const h = Buffer.alloc(16); h.writeUInt32LE(k, 0); h.writeUInt32LE(s, 4); h.writeUInt32LE(n, 8); h.writeUInt32LE(png.length, 12);
      process.stdout.write(h); process.stdout.write(png);
    }
    process.stderr.write(`\rframe ${k}`);
  }
  await b.close(); process.stderr.write('\n');
})();
