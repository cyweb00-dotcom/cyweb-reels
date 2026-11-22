const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file:///home/user/cyweb-reels/reels/cyweb-remake-reel/index.html');
  await page.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
  const FPS = 30, DUR = 20, N = FPS * DUR;
  for (let i = 0; i < N; i++) {
    const t = i / FPS;
    const fp = `/home/user/scratch/remake-frames/f_${String(i).padStart(4,"0")}.png`; if (require("fs").existsSync(fp)) continue;
    await page.evaluate((tt) => window.__render(tt), t);
    await page.screenshot({ path: `/home/user/scratch/remake-frames/f_${String(i).padStart(4,'0')}.png` });
  }
  await browser.close();
  console.log('done', N);
})().catch(e => { console.error(e); process.exit(1); });
