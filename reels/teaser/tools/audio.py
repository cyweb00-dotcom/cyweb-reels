# Soundtrack, built in code. Every cue sits on a hit measured in the reference waveform (REF.md "Sound"),
# plus the hook (label slam f1, CTA tick f7) and a soft pop on each caption change.
# Layers: warm 92 bpm bed (keys, sub, kick, shaker, sidechain), whooshes, clicks, riser + ticks, cinematic hits.
import numpy as np, scipy.io.wavfile as wf, scipy.signal as ss, json
SR = 48000; DUR = 12.0; N = int(SR * DUR); rng = np.random.default_rng(5)
T = lambda f: (f - 1) / 30.0
L = np.zeros(N); R = np.zeros(N); duck = np.ones(N)
def put(sig, t, g=1.0, pan=0.0, st=None):
  i = int(t * SR)
  if i < 0: sig = sig[-i:]; st = st[-i:] if st is not None else None; i = 0
  j = min(N, i + len(sig)); s = sig[:j - i] * g
  if st is not None:  # stereo pair (left, right)
    L[i:j] += st[0][:j - i] * g; R[i:j] += st[1][:j - i] * g; return
  L[i:j] += s * np.sqrt(.5 * (1 - pan)); R[i:j] += s * np.sqrt(.5 * (1 + pan))
def sos(kind, f, order=2): return ss.butter(order, f, kind, fs=SR, output='sos')
lp = lambda x, f: ss.sosfilt(sos('low', f), x); hp = lambda x, f: ss.sosfilt(sos('high', f), x); bp = lambda x, a, b: ss.sosfilt(sos('band', [a, b]), x)
def verb(x, secs=1.8, mix=.25, bright=6000):
  n = int(secs * SR); ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (secs * SR / 6.5)); ir = lp(ir, bright); ir /= np.sqrt((ir ** 2).sum())
  wet = ss.fftconvolve(x, ir); out = np.zeros(len(wet)); out[:len(x)] += x; return out + mix * wet
def duck_at(t, depth=.55, rel=.35):
  i = int(t * SR); n = int(rel * SR); j = min(N, i + n)
  if i >= N: return
  duck[i:j] = np.minimum(duck[i:j], 1 - depth * np.exp(-np.arange(j - i) / (rel * SR / 3)))
# ---------------- cues ----------------
def whoosh(peak, length=.75, lo=250, hi=7000, pan_from=-.6, pan_to=.6, g=.55):
  n = int(length * SR); k = np.arange(n) / SR; u = k / length; pk = .6
  shape = np.where(u < pk, (u / pk) ** 2.4, np.exp(-(u - pk) * length / .16))
  noise = rng.normal(0, 1, n); out = np.zeros(n); seg = 512
  for s in range(0, n, seg):
    uu = s / n; fc = lo * (hi / lo) ** np.sin(np.pi * min(1, uu / (pk * 2)))
    out[s:s + seg] = bp(noise[s:s + seg], max(80, fc * .5), min(20000, fc * 1.5))
  tone = np.sin(2 * np.pi * np.cumsum(420 * np.exp(-u * 1.8) + 90) / SR) * .25     # pitched air
  x = (out / (np.abs(out).max() + 1e-9) + tone) * shape
  pan = pan_from + (pan_to - pan_from) * u; l = x * np.sqrt(.5 * (1 - pan)); r = x * np.sqrt(.5 * (1 + pan))
  L_, R_ = verb(l, 1.2, .22), verb(r, 1.2, .22)
  i = int((peak - pk * length) * SR)
  if i < 0: L_, R_, i = L_[-i:], R_[-i:], 0          # cue starts before the reel: keep the tail
  j = min(N, i + len(L_)); L[i:j] += L_[:j - i] * g; R[i:j] += R_[:j - i] * g
def click(t, g=.6):
  n = int(.08 * SR); k = np.arange(n) / SR
  tick = hp(rng.normal(0, 1, n), 2500) * np.exp(-k / .0012)
  body = np.sin(2 * np.pi * 1700 * k) * np.exp(-k / .008) + .5 * np.sin(2 * np.pi * 380 * k) * np.exp(-k / .02)
  put(verb(tick * .8 + body, .6, .18)[:int(.5 * SR)], t, g, .2)
def pop(t, f0=700, g=.32):
  n = int(.18 * SR); k = np.arange(n) / SR; f = f0 * (1 + .9 * (1 - np.exp(-k * 40)))     # upward 'bloop'
  x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, k / .004) * np.exp(-k / .045)
  put(verb(x, .9, .3), t, g)
def tick(t, g=.18, f=3200):
  n = int(.03 * SR); k = np.arange(n) / SR; put(np.sin(2 * np.pi * f * k) * np.exp(-k / .004) + hp(rng.normal(0, .4, n), 4000) * np.exp(-k / .001), t, g, .3)
def riser(t0, t1, g=.22):
  n = int((t1 - t0) * SR); k = np.arange(n) / SR; u = k / (t1 - t0)
  f = 180 * 5 ** (u ** 1.3); ph = 2 * np.pi * np.cumsum(f) / SR
  tone = (np.sin(ph) + .4 * np.sin(2.005 * ph) + .25 * ss.sawtooth(ph * .5)) * (.1 + .9 * u ** 2)
  air = bp(rng.normal(0, 1, n), 2000, 12000) * u ** 3 * .35
  x = lp(tone, 1500 + 6000 * u.mean()) + air; x *= np.minimum(1, (n - np.arange(n)) / (.02 * SR))
  put(verb(x, 1.4, .25), t0, g)
def hit(t, big=1.0):
  n = int(2.6 * SR); k = np.arange(n) / SR
  sub = np.sin(2 * np.pi * np.cumsum(62 * np.exp(-k * 4) + 34) / SR) * np.exp(-k / .55)
  punch = np.sin(2 * np.pi * np.cumsum(140 * np.exp(-k * 25) + 60) / SR) * np.exp(-k / .06)
  crack = hp(rng.normal(0, 1, n), 1200) * np.exp(-k / .018)
  shimmer = sum(np.sin(2 * np.pi * fr * k + rng.uniform(0, 6)) for fr in (1760, 2217, 2637, 3520)) * np.exp(-k / .7) * .05
  x = sub + .7 * punch + .35 * crack + shimmer
  put(verb(x, 2.6, .4, 4500), t, .75 * big); duck_at(t, .7 * min(1, big), .6)
# ---------------- music bed: 92 bpm, Am9 – Fmaj7 – Cadd9 – G6, warm keys ----------------
bpm = 92; beat = 60 / bpm; k = np.arange(N) / SR
chords = [[57, 60, 64, 71], [53, 57, 64, 67], [48, 55, 62, 64], [55, 59, 62, 64]]
keys = np.zeros(N); bass = np.zeros(N)
for ci in range(int(DUR / (beat * 4)) + 2):
  t0 = ci * beat * 4; i0 = int(t0 * SR)
  if i0 >= N: break
  i1 = min(N, int((t0 + beat * 4 + .6) * SR)); kk = np.arange(i1 - i0) / SR; seg = np.zeros(i1 - i0)
  for m in chords[ci % 4]:
    fr = 440 * 2 ** ((m - 69) / 12)
    for h, a in ((1, 1), (2, .35), (3, .12), (4, .05)):                       # e-piano-ish partials
      seg += a * np.sin(2 * np.pi * fr * h * kk + h) * np.exp(-kk * (1.2 + h * .6))
  seg *= (1 + .15 * np.sin(2 * np.pi * 4.5 * kk)) * np.minimum(1, kk / .01)
  keys[i0:i1] += seg
  root = 440 * 2 ** ((chords[ci % 4][0] - 12 - 69) / 12)
  for b in range(4):
    j0 = int((t0 + b * beat) * SR); j1 = min(N, j0 + int(beat * .9 * SR))
    if j0 >= N: break
    kb = np.arange(j1 - j0) / SR; bass[j0:j1] += np.sin(2 * np.pi * root * kb) * np.minimum(1, kb / .01) * np.exp(-kb / .5)
kick = np.zeros(N); hat = np.zeros(N)
for bi, b in enumerate(np.arange(0, DUR, beat / 2)):
  i = int(b * SR)
  if bi % 2 == 0 and T(30) < b:                                                 # kick in after the hook
    n = int(.35 * SR); kk = np.arange(n) / SR; kx = np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-kk * 35)) / SR) * np.exp(-kk / .11)
    j = min(N, i + n); kick[i:j] += kx[:j - i] * (.5 if bi % 4 == 0 else .32)
  n = int(.06 * SR); kk = np.arange(n) / SR; hx = hp(rng.normal(0, 1, n), 7000) * np.exp(-kk / (.012 if bi % 2 else .025))
  j = min(N, i + n); hat[i:j] += hx[:j - i] * (.05 if bi % 2 else .03)
# filter opens over the first 3 s (intro), full from the bar onwards
cut = np.interp(k, [0, T(90), T(241), T(289), 12], [700, 2600, 4200, 9000, 9000])
keys_f = np.zeros(N); blk = 2400
for s in range(0, N, blk): keys_f[s:s + blk] = lp(keys[s:s + blk], cut[min(N - 1, s)])
pump = np.ones(N)
for b in np.arange(0, DUR, beat):
  i = int(b * SR); n = int(beat * SR); j = min(N, i + n); pump[i:j] *= 1 - .35 * np.exp(-np.arange(j - i) / (.12 * SR))
bed = (verb(keys_f * .07, 2.4, .35)[:N] + lp(bass, 220) * .16) * pump + kick * .9 + hat
bed *= np.clip(k / .25, 0, 1) * np.clip((11.98 - k) / .5, 0, 1)
# ---------------- cue sheet (reference onset frame -> cue) ----------------
CUES = [('hit-hook', 1.0), ('tick', 7.0), ('whoosh', 4.0), ('pop', 34.5), ('whoosh', 72.5), ('click', 107.5), ('whoosh', 121.5),
        ('pop', 125.5), ('pop', 128.5), ('whoosh', 138.0), ('whoosh', 158.0), ('whoosh', 181.0), ('pop', 185.5), ('whoosh', 211.5),
        ('rise', 241.0), ('hit-s', 277.0), ('hit', 289.0), ('pop', 294.5), ('pop', 310.5), ('hit', 329.0), ('hit-big', 345.5)]
caps = json.load(open('desk/captions.json'))
for c in caps[1:]:                                                              # soft pop on caption changes not already covered
  if all(abs(c['from'] - f) > 4 for _, f in CUES): CUES.append(('cap-pop', float(c['from'])))
for kind, f in CUES:
  t = T(f)
  if kind == 'whoosh': whoosh(t)
  elif kind == 'pop': pop(t)
  elif kind == 'cap-pop': pop(t, 900, .2)
  elif kind == 'click': click(t)
  elif kind == 'tick': tick(t, .3, 2600)
  elif kind == 'rise':
    riser(t, T(277))
    pk = {241: 7, 245: 24, 249: 58, 253: 76, 257: 85, 261: 91, 265: 95, 269: 97, 273: 99}   # count ticks
    for fr in pk: tick(T(fr), .12, 2400 + pk[fr] * 15)
  elif kind == 'hit': hit(t, .8)
  elif kind == 'hit-s': hit(t, .45)
  elif kind == 'hit-big': hit(t, 1.1)
  elif kind == 'hit-hook': hit(t + 0.005, .9)
L += bed * duck; R += bed * duck
mix = np.stack([L, R], 1); mix /= np.abs(mix).max() / 0.89
wf.write('out/audio.wav', SR, (mix * 32767).astype(np.int16))
json.dump(sorted(CUES, key=lambda c: c[1]), open('out/cues.json', 'w'))
print('ok', len(CUES), 'cues')
