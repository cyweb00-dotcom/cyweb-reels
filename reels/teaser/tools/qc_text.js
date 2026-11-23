// Text clearance: on every frame, bounding boxes of every visible text/logo element vs the screen edge (film px).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
 await p.goto('file://' + path.resolve('film/index.html')); await p.evaluate(() => window.READY);
 const res = await p.evaluate(() => {
   const ids = { title: 'title', invite: 'invite', payoff: 'payB', percent: 'pct', closing: 'close', logo: 'logo', logoEnd: 'logoEnd' };
   const vis = el => { let e = el, o = 1; while (e && e.nodeType === 1) { const cs = getComputedStyle(e); o *= +cs.opacity; if (cs.display === 'none') return 0; e = e.parentElement; } return o; };
   const out = {}; const lines = {};
   for (let f = 0; f < 360; f++) {
     window.seekFrame(f); let onScreen = 0;
     for (const [k, id] of Object.entries(ids)) {
       const el = document.getElementById(id);
       // text that is a line: use visible word spans only
       const parts = el.querySelectorAll('.w').length ? [...el.querySelectorAll('.w')] : [el];
       for (const w of parts) {
         if (vis(w) < 0.05) continue;
         const r = w.getBoundingClientRect(); if (r.width < 2) continue;
         const m = Math.min(r.left, r.top, 1920 - r.right, 1080 - r.bottom);
         if (k !== 'percent') onScreen++;
         if (!out[k] || m < out[k].min) out[k] = { min: Math.round(m), frame: f + 1 };
       }
     }
     // one line at a time: count distinct line groups visible (title/invite/payoff/closing)
     const groups = ['title', 'invite', 'payB', 'close'].filter(id => [...document.getElementById(id).querySelectorAll('.w')].some(w => vis(w) > 0.3));
     if (groups.length > 1) lines[f + 1] = groups;
   }
   return { clearance: out, framesWithTwoLines: lines };
 });
 fs.writeFileSync('out/qc_text.json', JSON.stringify(res, null, 1)); console.log(JSON.stringify(res, null, 1)); await b.close(); })();
