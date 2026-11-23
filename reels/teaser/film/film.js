// CYWEB teaser — screen film timeline. All keys are reference frame numbers (1-based).
// Measured values: see REF.md. Flat-study px (1280x720) are x1.5 here (1920x1080).
const FPS = 30, F = n => (n - 1) / FPS, X = v => v * 1.5;
const $ = id => document.getElementById(id);
const tl = gsap.timeline({ paused: true });
gsap.defaults({ overwrite: false });

// ---------- helpers ----------
// key a property through measured [frame, value] pairs (linear between samples unless ease given)
function track(target, prop, keys, ease = 'none') {
  gsap.set(target, { [prop]: keys[0][1] });
  for (let i = 1; i < keys.length; i++) {
    const [f0] = keys[i - 1], [f1, v1] = keys[i];
    tl.to(target, { [prop]: v1, duration: (f1 - f0) / FPS, ease }, F(f0));
  }
}
const blurKeys = (target, keys, ease = 'none') => {
  const o = { b: keys[0][1] };
  const apply = () => { const b = Math.max(0, o.b); target.forEach ? target.forEach(t => t.style.filter = b > 0.05 ? `blur(${b}px)` : 'none') : (target.style.filter = b > 0.05 ? `blur(${b}px)` : 'none'); };
  apply();
  for (let i = 1; i < keys.length; i++) {
    const [f0] = keys[i - 1], [f1, v1] = keys[i];
    tl.to(o, { b: v1, duration: (f1 - f0) / FPS, ease, onUpdate: apply }, F(f0));
  }
  tl.call(apply, null, F(keys[keys.length - 1][0]));
};

// ---------- phone screens ----------
document.querySelectorAll('[data-screen]').forEach(el => {
  const k = el.dataset.screen, map = { cafe: 1, salon: 2, clinic: 3, calendar: 4 };
  const user = (window.USER_SCREENS || {})[map[k]];
  el.innerHTML = user ? `<img src="${user}">` : window.SCREENS[k];
});

// ---------- glow: 3 fitted Gaussians per reference frame (tools/glowfit.py) ----------
// Each Gaussian is in captured-G-excess units. Captured colour comes from the measured ramp
// (G -> R,B in the reference), then goes back through the inverse screen transfer to display RGB.
const cv = $('glow'), cx2 = cv.getContext('2d');
const SW = 192, SH = 108, small = document.createElement('canvas'); small.width = SW; small.height = SH;
const sctx = small.getContext('2d'), simg = sctx.createImageData(SW, SH);
const BLK = [13, 18, 20], WHT = [225, 245, 252], GAM = 1.15;
const RAMP = [[18, 14, 20], [40, 10, 40], [60, 6, 60], [80, 4, 80], [100, 2, 99], [120, 2, 113], [140, 40, 132], [160, 66, 150], [180, 99, 168], [200, 128, 204], [220, 150, 227], [255, 200, 250]];
const LUT = [];
for (let e = 0; e < 256; e++) {
  const G = Math.min(255, 18 + e); let j = 0; while (j < RAMP.length - 2 && RAMP[j + 1][0] < G) j++;
  const [g0, r0, b0] = RAMP[j], [g1, r1, b1] = RAMP[j + 1], u = Math.min(1, Math.max(0, (G - g0) / (g1 - g0)));
  const cap = [r0 + (r1 - r0) * u, G, b0 + (b1 - b0) * u];
  LUT.push(cap.map((c, k) => 255 * Math.pow(Math.min(1, Math.max(0, (c - BLK[k]) / (WHT[k] - BLK[k]))), 1 / GAM)));
}
let GLOW3 = [];
function drawGlow(t) {
  cx2.clearRect(0, 0, 1920, 1080);
  if (!GLOW3.length) return;
  const f = t * FPS + 1, i = Math.min(GLOW3.length - 2, Math.max(0, Math.floor(f) - 1)), u = Math.min(1, Math.max(0, f - Math.floor(f)));
  const A0 = GLOW3[i], A1 = GLOW3[i + 1];
  const gs = A0.map((g, k) => { const h = A1[k], L = q => g[q] + (h[q] - g[q]) * u; return [L('cx') / 10, L('cy') / 10, Math.max(.5, L('sx') / 10), Math.max(.5, L('sy') / 10), L('a') * GLOWGAIN]; });
  const d = simg.data;
  for (let y = 0; y < SH; y++) for (let x = 0; x < SW; x++) {
    let e = 0;
    for (const [cx, cy, sx, sy, a] of gs) { const dx = (x + .5 - cx) / sx, dy = (y + .5 - cy) / sy; e += a * Math.exp(-0.5 * (dx * dx + dy * dy)); }
    const c = LUT[Math.min(255, Math.max(0, Math.round(e)))], o = (y * SW + x) * 4;
    d[o] = c[0]; d[o + 1] = c[1]; d[o + 2] = c[2]; d[o + 3] = 255;
  }
  sctx.putImageData(simg, 0, 0);
  cx2.imageSmoothingEnabled = true; cx2.imageSmoothingQuality = 'high';
  cx2.filter = 'blur(6px)'; cx2.drawImage(small, -20, -20, 1960, 1120); cx2.filter = 'none';
}
let GLOWGAIN = 1.0;

// ---------- beam: the V-shaped teal bloom over the logo (f337–348) ----------
const beam = $('beam');
beam.style.background = 'linear-gradient(180deg,rgba(190,250,245,1),rgba(40,200,195,.9) 45%,rgba(0,150,155,0) 80%)';
beam.style.clipPath = 'polygon(0 0,100% 0,58% 100%,42% 100%)';
gsap.set(beam, { xPercent: -50, width: 1300, height: 760, opacity: 0, filter: 'blur(40px)' });
tl.to(beam, { opacity: 1, duration: F(347) - F(337), ease: 'power2.in' }, F(337));
tl.set(beam, { opacity: 0 }, F(349));

// ========== 1. TITLE (f1–32) ==========
const title = $('title'), tWith = $('tWith'), tName = $('tName'), slot = $('slot'), icon = $('icon');
slot.appendChild(icon); icon.style.position = 'relative'; icon.style.display = 'inline-block';
icon.style.verticalAlign = 'middle'; icon.style.width = icon.style.height = '140px'; icon.style.borderRadius = '34px';
icon.querySelector('img').style.width = '114px';
slot.style.display = 'inline-flex'; slot.style.justifyContent = 'center'; slot.style.alignItems = 'center';
slot.style.overflow = 'visible'; slot.style.verticalAlign = 'middle'; slot.style.height = '0px';
gsap.set(title, { transformOrigin: '0% 50%' });
gsap.set(icon, { scale: 0, opacity: 0 });
// left edge of "With" (flat px), measured per frame; cap-centre y ≈ 356 flat
track(title, 'x', [[1, X(575)], [3, X(560)], [5, X(520)], [9, X(467)], [11, X(458)], [13, X(450)], [15, X(441)], [17, X(436)], [19, X(431)], [21, X(428)], [23, X(426)], [25, X(423)], [27, X(421)], [29, X(414)], [31, X(409)], [32, X(394)], [35, X(330)], [39, X(300)], [45, X(288)], [52, X(281)], [60, X(272)], [67, X(271)]]);
track(title, 'y', [[1, X(331)], [67, X(327)]]);
// scale relative to f25 (line width 498 flat); f45–67 from "With" cap height 47 vs 39
track(title, 'scale', [[1, .86], [11, .862], [13, .89], [15, .929], [17, .953], [19, .968], [21, .976], [23, .99], [25, 1], [27, 1.008], [29, 1.035], [31, 1.055], [33, 1.1], [39, 1.17], [45, 1.2], [60, 1.205], [67, 1.21]]);
// product name: absent until the flash, then blur-in
gsap.set(tName, { opacity: 0 });
tl.to(tName, { opacity: 1, duration: F(10) - F(7), ease: 'power1.out' }, F(7));
blurKeys([tWith], [[1, 0.6], [2, 2], [3, 5], [5, 12], [7, 16], [9, 6], [10, 2.5], [11, 0.8], [13, 0]]);
blurKeys([tName], [[1, 18], [7, 18], [9, 7], [10, 3], [11, 1], [13, 0]]);
// split: slot opens, icon lands between the words (f32–45)
gsap.set(slot, { width: 22 });
tl.to(slot, { width: 208, duration: F(43) - F(32), ease: 'expo.out' }, F(32));
tl.to(icon, { scale: 1, opacity: 1, duration: F(41) - F(33), ease: 'back.out(1.4)' }, F(33));
blurKeys([icon], [[1, 10], [33, 10], [36, 3], [39, 0]]);
// slight dim on the name as the icon lands (reference: name goes deeper teal by f60)
tl.to(tName, { opacity: .82, duration: F(60) - F(40) }, F(40));

// cursor glides onto the icon (tip, flat px)
const cur = $('cursor');
gsap.set(cur, { x: X(800), y: X(395), opacity: 0 });
tl.to(cur, { opacity: 1, duration: F(44) - F(41) }, F(41));
tl.to(cur, { x: X(541), y: X(392), duration: F(59) - F(41), ease: 'power2.out' }, F(41));
tl.to(cur, { x: X(535), y: X(388), duration: F(67) - F(59), ease: 'none' }, F(59));

// ========== 2. PUSH INTO THE ICON (f67–90) ==========
// Reference: words drop and blur away, the icon grows and rises, then settles into the panel's logo tile.
const fly = icon.cloneNode(true); fly.id = 'fly'; $('stage').appendChild(fly);
Object.assign(fly.style, { position: 'absolute', left: '0', top: '0', width: '147px', height: '147px', borderRadius: '36px' });
fly.querySelector('img').style.width = '120px';
gsap.set(fly, { xPercent: -50, yPercent: -50, x: X(481), y: X(341), scale: 1, opacity: 0, zIndex: 5 });
tl.set(fly, { opacity: 1 }, F(72)); tl.set(icon, { opacity: 0 }, F(72));
tl.to(fly, { x: X(533), y: X(293), scale: 160 / 98, duration: F(77) - F(72), ease: 'power2.in' }, F(72));
tl.to(fly, { x: X(613), y: X(398), scale: 1.6, duration: F(89) - F(77), ease: 'expo.out' }, F(77));
tl.to(fly, { x: X(635), y: X(410), duration: F(97) - F(89), ease: 'sine.out' }, F(89));   // panel logo tile (moved down for the services row)
tl.to(fly, { opacity: 0, duration: F(92) - F(88) }, F(88));
blurKeys([fly], [[1, 0], [72, 0], [75, 3], [77, 5], [81, 2], [85, 0]]);
tl.to(title, { y: `+=${X(90)}`, duration: F(77) - F(70), ease: 'power2.in' }, F(70));
blurKeys([s1], [[1, 0], [72, 0], [75, 3], [77, 10], [78, 16]], 'power1.in');
tl.to(s1, { opacity: 0, duration: F(78) - F(73), ease: 'power1.in' }, F(73));
// cursor rides with the icon into the panel (tip offsets measured f79/f85/f105)
tl.to(cur, { x: X(585), y: X(345), duration: F(77) - F(72), ease: 'power2.in' }, F(72));
tl.to(cur, { x: X(639), y: X(432), duration: F(79) - F(77), ease: 'none' }, F(77));
tl.to(cur, { x: X(690), y: X(432), duration: F(85) - F(79), ease: 'power1.out' }, F(79));

// ========== 3. GLASS PANEL (f73–124) ==========
const pw = $('panelWrap'), panel = $('panel'), pIcon = $('pIcon');
// fitted: centre (957.9,454.7) W1312.6 H729.4 rotateX 32.0 rotateY 0.24, perspective 1920
gsap.set(panel, { left: 957.9 - 656.3, top: 454.7 - 364.7, width: 1312.6, height: 729.4, rotationX: 50, rotationY: 0.24, y: -700, scale: 1.0, transformOrigin: '50% 50%' });
tl.to(pw, { opacity: 1, duration: F(77) - F(72), ease: 'power1.out' }, F(72));
track(panel, 'y', [[72, -900], [74, -800], [77, -520], [79, -260], [81, -170], [83, -120], [85, -90], [89, -20], [95, 0]]);
track(panel, 'scale', [[74, 1.25], [79, 1.15], [85, 1.1], [89, 1.03], [95, 1]]);
track(panel, 'rotationX', [[74, 50], [79, 44], [85, 35], [89, 32]]);
gsap.set(pIcon, { opacity: 0 }); tl.to(pIcon, { opacity: 1, duration: F(91) - F(87) }, F(87));
blurKeys([pw], [[1, 10], [74, 10], [79, 5], [84, 1], [87, 0], [120, 0], [124, 14]]);
tl.to(panel, { x: 6, duration: F(119) - F(91), ease: 'sine.inOut' }, F(91));
tl.to(panel, { y: -140, rotationX: 40, duration: F(124) - F(119), ease: 'power2.in' }, F(119));
tl.to(pw, { opacity: 0, duration: F(124) - F(120), ease: 'power1.in' }, F(120));
// cursor: enters with the panel, settles at the logo tile's lower right, clicks at f107
tl.to(cur, { x: X(700), y: X(452), duration: F(97) - F(85), ease: 'sine.out' }, F(85));
tl.to(cur, { scale: .82, duration: F(107) - F(105), ease: 'power2.in' }, F(105))
  .to(cur, { scale: 1, duration: F(111) - F(107), ease: 'power2.out' }, F(107));
tl.to(pIcon, { scale: .93, duration: F(107) - F(105), ease: 'power2.in' }, F(105))
  .to(pIcon, { scale: 1, duration: F(112) - F(107), ease: 'back.out(2)' }, F(107));
tl.to(cur, { opacity: 0, y: '-=120', duration: F(124) - F(119), ease: 'power2.in' }, F(119));

// ========== 4. INVITE (f125–157) ==========
const inv = $('invite'), iA = $('iA'), iB = $('iB');
inv.style.fontSize = '93px';
gsap.set(inv, { transformOrigin: '50% 50%', xPercent: -50, yPercent: -50, x: X(635), opacity: 1 });
gsap.set([iA, iB], { opacity: 0 });
tl.to(iA, { opacity: 1, duration: F(128) - F(125), ease: 'power1.out' }, F(125));
tl.to(iB, { opacity: 1, duration: F(131) - F(128), ease: 'power1.out' }, F(128));
blurKeys([iA], [[1, 14], [125, 14], [127, 6], [129, 2], [131, 0], [138, 0], [140, 10], [142, 16], [144, 4], [145, 0]]);
blurKeys([iB], [[1, 14], [128, 14], [130, 5], [132, 1], [133, 0], [138, 0], [140, 10], [142, 16], [144, 4], [145, 0]]);
// bbox-centre y per frame (flat)
track(inv, 'y', [[125, X(460)], [126, X(447.5)], [127, X(440)], [128, X(429.5)], [129, X(420.5)], [130, X(415)], [131, X(409)], [132, X(405)], [133, X(400.5)], [134, X(394.5)], [135, X(390)], [136, X(387)], [137, X(384.5)], [139, X(384)], [142, X(375)], [145, X(367)], [150, X(362.5)], [157, X(362)], [165, X(362)], [177, X(362)]]);
track(inv, 'scale', [[125, .976], [129, .976], [133, 1.014], [138, 1], [150, 1], [153, .986], [155, .925], [157, .863], [161, .66], [165, .6], [177, .58]]);
gsap.set(inv, { opacity: 0 }); tl.set(inv, { opacity: 1 }, F(125));
blurKeys([inv], [[1, 0], [177, 0], [179, 8], [181, 16]]);
tl.to(inv, { opacity: 0, duration: F(182) - F(177), ease: 'power1.in' }, F(177));

// ========== 5. PHONE TUNNEL (f155–209) ==========
const tw = $('tunnelWrap'), tun = $('tunnel');
const A = 908, B = 546, D = 1100, PW = 1100, PL = 1900, ZC = -D + PL / 2;
const PWS = { phL: 820, phR: 880, phT: 1100, phB: 1100, phW: 1100 };
document.querySelectorAll('.phone').forEach(p => { p.style.width = (PWS[p.id] || PW) + 'px'; p.style.height = PL + 'px'; });
const walls = {
  wL: `translate3d(${-A}px,0,${ZC}px) rotateY(90deg) rotateZ(90deg)`,
  wR: `translate3d(${A}px,0,${ZC}px) rotateY(-90deg) rotateZ(-90deg)`,
  wT: `translate3d(0,${-B}px,${ZC}px) rotateX(-90deg) rotateZ(180deg)`,
  wB: `translate3d(0,${B}px,${ZC}px) rotateX(90deg)`,
};
const off = { wL: [-1, 0], wR: [1, 0], wT: [0, -1], wB: [0, 1] }, wallOff = {};
for (const k in walls) {
  const w = $(k), ph = w.querySelector('.phone'); ph.style.transform = `translate(${-(PWS[ph.id]) / 2}px,${-PL / 2}px)`;
  wallOff[k] = { o: 1 };
  const upd = () => { const [dx, dy] = off[k], o = wallOff[k].o * 1500; w.style.transform = `translate3d(${dx * o}px,${dy * o}px,0) ` + walls[k]; };
  upd(); wallOff[k].upd = upd;
}
const startF = { wB: 155, wL: 157, wR: 157, wT: 159 };
tl.set(tw, { opacity: 1 }, F(155));
for (const k in walls) {
  tl.to(wallOff[k], { o: 0, duration: F(startF[k] + 9) - F(startF[k]), ease: 'expo.out', onUpdate: wallOff[k].upd }, F(startF[k]));
  if (k !== 'wB') tl.to(wallOff[k], { o: 1.1, duration: F(210) - F(202), ease: 'power3.in', onUpdate: wallOff[k].upd }, F(202));
}
tl.set($('wB'), { opacity: 0 }, F(209));
gsap.set(tun, { rotationZ: -4, z: 0 });
tl.to(tun, { rotationZ: 3, z: 160, duration: F(205) - F(161), ease: 'sine.inOut' }, F(161));
tl.set(tw, { opacity: 0 }, F(211));
blurKeys([tw], [[1, 6], [155, 6], [161, 0], [202, 0], [208, 8]]);

// payoff line swap (f181–203)
const payB = $('payB'), payWords = payB.querySelectorAll('.w');
$('payA').style.display = 'none';
gsap.set(payB, { xPercent: -50, yPercent: -50, x: X(639.5), y: X(361), scale: .9, transformOrigin: '50% 50%' });
gsap.set(payWords, { opacity: 0 });
payWords.forEach((w, i) => {
  tl.to(w, { opacity: 1, duration: F(186 + i) - F(181 + i), ease: 'power1.out' }, F(181 + i));
  blurKeys([w], [[1, 14], [181 + i, 14], [184 + i, 5], [187 + i, 1.5], [190 + i, 0], [200, 0], [203, 10]]);
});
tl.to(payB, { scale: 1, duration: F(192) - F(181), ease: 'expo.out' }, F(181));
tl.to(payWords, { opacity: 0, duration: F(203) - F(200), ease: 'power1.in' }, F(200));

// ========== 6. WHIP (f207–241) ==========
const whip = $('whip');
whip.querySelector('.phone').style.transform = `translate(${-PW / 2}px,0px)`;
gsap.set(whip, { transformOrigin: '0px 0px' });
// centre x/y (film px), rotation, scale, tilt — read off the reference frames
gsap.set(whip, { x: 960, y: 830, rotation: 0, rotationX: 72, scale: .5, opacity: 0 });
tl.set(whip, { opacity: 1 }, F(207));
// island (top-edge centre) path in film px, rotation, tilt, scale — read off ref f209–243
const WK = [[207, 960, 830, 0, 72, .5], [209, 960, 810, 0, 70, .5], [211, 967, 705, 5, 55, .55], [213, 975, 640, 14, 40, .7], [215, 971, 620, 40, 25, 1.2], [217, 960, 660, 55, 15, 1.5], [219, 930, 700, 63, 9, 1.65], [221, 906, 745, 70, 5, 1.7], [225, 860, 790, 71, 2, 1.85], [229, 904, 800, 72, 0, 1.9], [233, 820, 700, 76, 0, 1.9], [237, 720, 561, 80, 0, 1.9], [240, 540, 580, 83, 0, 1.9], [243, -200, 580, 90, 0, 1.9]];
for (let i = 1; i < WK.length; i++) {
  const [f0] = WK[i - 1], [f1, x, y, r, rx, s] = WK[i];
  tl.to(whip, { x, y, rotation: r, rotationX: rx, scale: s, duration: (f1 - f0) / FPS, ease: 'none' }, F(f0));
}
tl.set(whip, { opacity: 0 }, F(244));

// ========== 7. LOADING BAR (f239–288) ==========
const bar = $('bar'), pct = $('pct');
// percent read off every frame; tip x (flat) = 338 + 7.38 * p, retreats 36 px after f280
const PK = { 239: 4, 240: 5, 241: 7, 242: 10, 243: 13, 244: 18, 245: 24, 246: 33, 247: 43, 248: 51, 249: 58, 250: 64, 251: 69, 252: 72, 253: 76, 254: 78, 255: 81, 256: 83, 257: 85, 258: 87, 259: 88, 260: 90, 261: 91, 262: 92, 263: 93, 264: 94, 265: 95, 266: 95.5, 267: 96, 268: 96.8, 269: 97.3, 270: 97.8, 271: 98.1, 272: 98.4, 273: 98.8, 274: 99.1, 275: 99.4, 276: 99.7, 277: 100 };
const RET = { 280: 0, 284: 10, 286: 16, 287: 22, 288: 36 };
const bs = { f: 239 };
const barUpd = () => {
  const f = bs.f, fl = Math.floor(f), u = f - fl;
  const pv = k => PK[k] !== undefined ? PK[k] : 100;
  const p = pv(fl) + (pv(fl + 1) - pv(fl)) * u;
  const rk = Object.keys(RET).map(Number); let ret = 0;
  for (let i = 0; i < rk.length - 1; i++) if (f >= rk[i] && f <= rk[i + 1]) ret = RET[rk[i]] + (RET[rk[i + 1]] - RET[rk[i]]) * (f - rk[i]) / (rk[i + 1] - rk[i]);
  if (f > 288) ret = 36;
  const tip = X(338 + 7.38 * p - ret);
  bar.style.width = (tip + 900) + 'px';
  pct.textContent = Math.round(p) + '%';           // numbers count, never swap
  pct.style.left = (tip + 900 - X(100) - pct.offsetWidth) + 'px';
  pct.style.top = (X(325 - 228) - 151 * 0.26) + 'px';
};
gsap.set(bar, { opacity: 0 });
tl.set(bar, { opacity: 1 }, F(238));
tl.to(bs, { f: 290, duration: F(290) - F(239), ease: 'none', onUpdate: barUpd }, F(239));
barUpd();
tl.to(bar, { opacity: 0, duration: F(289) - F(287) }, F(287));

// contour lines sweeping up behind the bar (f254–288)
const svg = $('contours'), NS = 'http://www.w3.org/2000/svg';
svg.innerHTML = `<defs>
  <radialGradient id="cg" cx="900" cy="1000" r="760" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#3ff2df"/><stop offset=".55" stop-color="#14b9b0"/><stop offset="1" stop-color="#0a6e6c" stop-opacity="0"/></radialGradient>
  <mask id="cm"><rect width="1920" height="1080" fill="url(#cmg)"/></mask>
  <radialGradient id="cmg" cx="950" cy="1050" r="820" gradientUnits="userSpaceOnUse"><stop offset=".45" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
</defs><g id="cgrp" mask="url(#cm)"></g>`;
const cg = svg.querySelector('#cgrp');
for (let i = 0; i < 18; i++) {
  const r = 1250 + i * 52;
  const band = document.createElementNS(NS, 'circle');
  band.setAttribute('cx', 1700); band.setAttribute('cy', 2350); band.setAttribute('r', r);
  band.setAttribute('fill', 'none'); band.setAttribute('stroke', i % 2 ? 'url(#cg)' : '#04312f');
  band.setAttribute('stroke-width', i % 2 ? 44 : 9); band.setAttribute('opacity', i % 2 ? .9 : .9);
  cg.appendChild(band);
}
gsap.set(svg, { y: 420, rotation: 8, transformOrigin: '1700px 2350px', opacity: 0 });
tl.to(svg, { opacity: 1, duration: F(262) - F(254), ease: 'power1.out' }, F(254));
tl.to(svg, { y: 0, rotation: 0, duration: F(272) - F(254), ease: 'expo.out' }, F(254));
tl.to(svg, { rotation: -4, duration: F(289) - F(272), ease: 'none' }, F(272));
tl.to(svg, { opacity: 0, duration: F(290) - F(287) }, F(287));

// ========== 8. CLOSING LINE (f289–328) ==========
const cl = $('close'), cA = $('cA'), cB = $('cB'), cC = $('cC');
gsap.set(cl, { yPercent: -50, y: X(361.5), transformOrigin: '0% 50%' });
gsap.set([cA, cB, cC], { opacity: 0 });
const refFull = 449; // "Pro Workflow Unleashed" width at f310 (flat)
let clOff = 0;
tl.call(() => { }, null, 0);
// left-edge track (flat), offset so my full line lands centred like the reference
const CLK = [[291, 575], [296, 570], [298, 558], [299, 553], [301, 545], [303, 538], [305, 530], [307, 525], [308, 512], [309, 499], [310, 483], [311, 470], [312, 460], [313, 453], [315, 442], [317, 436], [319, 432], [321, 429], [323, 425], [325, 417], [326, 410], [328, 405]];
const clState = { f: 291 };
const clUpd = () => {
  const myW = cl.offsetWidth / 1.5; const offFlat = (refFull - myW) / 2;
  const f = clState.f; let L = CLK[0][1];
  for (let i = 0; i < CLK.length - 1; i++) if (f >= CLK[i][0] && f <= CLK[i + 1][0]) L = CLK[i][1] + (CLK[i + 1][1] - CLK[i][1]) * (f - CLK[i][0]) / (CLK[i + 1][0] - CLK[i][0]);
  if (f > CLK[CLK.length - 1][0]) L = CLK[CLK.length - 1][1];
  gsap.set(cl, { x: X(L + offFlat) });
};
tl.to(clState, { f: 328, duration: F(328) - F(291), ease: 'none', onUpdate: clUpd }, F(291));
[[cA, 291, 6], [cB, 297, 3], [cC, 309, 3]].forEach(([w, f, d]) => {
  tl.to(w, { opacity: 1, duration: F(f + d) - F(f), ease: 'power1.out' }, F(f));
  blurKeys([w], [[1, 14], [f, 14], [f + d * .5, 5], [f + d, 0]]);
});
tl.to([cA, cB, cC], { opacity: 0, duration: F(329) - F(327), ease: 'power1.in' }, F(327));

// ========== 9. LOGO + BLOOM (f329–360) ==========
const logo = $('logo'), white = $('white'), logoEnd = $('logoEnd');
const LH = 190, LW = LH * 918 / 652;   // ≈ reference mark height 101 flat → 152 film
gsap.set(logo, { width: LW, height: LH, xPercent: -50, yPercent: -50, y: X(362), x: X(722), opacity: 0 });
tl.set(logo, { opacity: 1 }, F(329));
track(logo, 'x', [[329, X(722)], [330, X(702)], [331, X(689)], [332, X(679)], [333, X(672)], [334, X(665)], [335, X(660)], [336, X(656)], [337, X(653)], [338, X(650)], [339, X(647)], [340, X(645)], [341, X(643)], [342, X(641)], [343, X(640)], [348, X(638)]]);
blurKeys([logo], [[1, 10], [329, 10], [330, 4], [331, 1], [332, 0]]);
tl.to(white, { opacity: 1, duration: F(349) - F(347), ease: 'power2.in' }, F(347));
gsap.set(logoEnd, { width: 470, height: 470 * 934 / 1172, xPercent: -50, yPercent: -50, x: X(637), y: X(361), opacity: 0 });   // full logo + tagline
tl.set(logoEnd, { opacity: 1 }, F(349));
const url = $('url'); gsap.set(url, { xPercent: -50, x: X(637), y: X(361) + 230, opacity: 0, filter: 'blur(10px)' });
tl.to(url, { opacity: 1, filter: 'blur(0px)', duration: F(354) - F(349), ease: 'expo.out' }, F(349));   // end card: where to go
tl.set(logo, { opacity: 0 }, F(349));

// ---------- seek API for the renderer ----------
GLOW3 = window.GLOW3; window.READY = document.fonts.ready.then(() => Promise.all([...document.images].map(i => i.decode().catch(() => 0))));
window.seekFrame = f => { // f: 0-based output frame (may be fractional for sub-frames)
  const t = Math.min(f / FPS, tl.duration());
  tl.seek(t, false); drawGlow(t); barUpd(); clUpd();
};
window.TL = tl;
