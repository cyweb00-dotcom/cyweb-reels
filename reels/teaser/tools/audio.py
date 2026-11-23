# Soundtrack built in code. Every cue sits on a hit found in the reference waveform
# (spectral-flux onsets, tools in REF.md "Sound"); output frame n -> t = (n-1)/30 s.
import numpy as np, scipy.io.wavfile as wf, scipy.signal as ss, json
SR = 48000; DUR = 12.0; N = int(SR * DUR); rng = np.random.default_rng(3)
T = lambda f: (f - 1) / 30.0
L = np.zeros(N); R = np.zeros(N)
def put(sig, t, gain=1.0, pan=0.0):
  i = int(t * SR); j = min(N, i + len(sig))
  if i < 0: sig = sig[-i:]; i = 0
  if j <= i: return
  s = sig[: j - i] * gain
  L[i:j] += s * np.sqrt(0.5 * (1 - pan)); R[i:j] += s * np.sqrt(0.5 * (1 + pan))
def env(n, a, d):  # attack/decay in samples
  e = np.ones(n); a = max(1, a); e[:a] = np.linspace(0, 1, a) ** 2
  e[a:] = np.exp(-np.arange(n - a) / max(1, d)); return e
def bp(x, lo, hi): return ss.sosfilt(ss.butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f): return ss.sosfilt(ss.butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return ss.sosfilt(ss.butter(2, f, 'high', fs=SR, output='sos'), x)
def verb(x, secs=1.6, mix=.25):
  n = int(secs * SR); ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (secs * SR / 6)); ir = lp(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
  return x + mix * ss.fftconvolve(x, ir)[: len(x)]
# --- cues ---
def whoosh(peak_t, length=.7, lo=300, hi=5000):
  n = int(length * SR); x = rng.normal(0, 1, n); out = np.zeros(n); seg = 256
  pk = .55
  for s in range(0, n, seg):
    u = s / n; fc = lo * (hi / lo) ** (np.sin(np.pi * min(1, u / pk * .5 if u < pk else .5 + (u - pk) / (1 - pk) * .5)))
    out[s:s + seg] = bp(x[s:s + seg], max(60, fc * .6), min(20000, fc * 1.6))
  e = np.where(np.arange(n) < pk * n, (np.arange(n) / (pk * n)) ** 2.2, np.exp(-(np.arange(n) - pk * n) / (0.18 * SR)))
  put(verb(out * e, 1.0, .2) / 3, peak_t - pk * length, .55)
def click(t):
  n = int(.06 * SR); k = np.arange(n) / SR
  x = (np.sin(2 * np.pi * 2400 * k) * np.exp(-k / .006) + rng.normal(0, .5, n) * np.exp(-k / .0015))
  put(hp(x, 800), t, .55, .15)
def pop(t, f0=1100):
  n = int(.12 * SR); k = np.arange(n) / SR; f = f0 * np.exp(-k * 6)
  x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, int(.003 * SR), int(.035 * SR))
  put(verb(x, .8, .3), t, .34)
def rise(t0, t1):
  n = int((t1 - t0) * SR); k = np.arange(n) / SR; u = k / (t1 - t0)
  f = 220 * (4 ** u); ph = 2 * np.pi * np.cumsum(f) / SR
  x = (np.sin(ph) + .35 * np.sin(2 * ph) + .2 * np.sin(3.01 * ph)) * (.15 + .85 * u ** 1.6) * (1 + .25 * np.sin(2 * np.pi * (6 + 10 * u) * k))
  x *= np.minimum(1, (n - np.arange(n)) / (.03 * SR))
  put(verb(lp(x, 5000), 1.2, .25), t0, .16)
def hit(t, big=1.0):
  n = int(2.2 * SR); k = np.arange(n) / SR
  boom = np.sin(2 * np.pi * np.cumsum(58 * np.exp(-k * 3) + 38) / SR) * np.exp(-k / .45)
  tr = hp(rng.normal(0, 1, n), 1500) * np.exp(-k / .02)
  shim = bp(rng.normal(0, 1, n), 3000, 9000) * np.exp(-k / .5) * .25
  put(verb(boom + .35 * tr + shim, 2.2, .35), t, .8 * big)
# --- bed: 92 bpm, Am–F–C–G pad, soft pulse ---
bpm = 92; beat = 60 / bpm; k = np.arange(N) / SR
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 64], [55, 59, 62]]
pad = np.zeros(N)
for ci in range(int(DUR / (beat * 4)) + 1):
  t0 = ci * beat * 4; i0 = int(t0 * SR); i1 = min(N, int((t0 + beat * 4 + .3) * SR))
  if i0 >= N: break
  kk = np.arange(i1 - i0) / SR; seg = np.zeros(i1 - i0)
  for m in chords[ci % 4]:
    fr = 440 * 2 ** ((m - 69) / 12)
    for det in (-.12, .12): seg += ss.sawtooth(2 * np.pi * fr * (1 + det / 100) * kk)
  seg *= np.minimum(1, kk / .25) * np.minimum(1, (kk[-1] - kk) / .3 + .0)
  pad[i0:i1] += seg
pad = lp(pad, 1400) * .05
sub = np.sin(2 * np.pi * 55 * k) * 0
kick = np.zeros(N)
for b in np.arange(0, DUR, beat):
  n = int(.4 * SR); kk = np.arange(n) / SR
  kx = np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-kk * 30)) / SR) * np.exp(-kk / .12)
  i = int(b * SR); j = min(N, i + n); kick[i:j] += kx[: j - i] * (.22 if (round(b / beat) % 2 == 0) else .12)
bed = verb(pad, 2.5, .3) + kick
bed *= np.clip((k - 0) / .4, 0, 1) * np.clip((11.95 - k) / .4, 0, 1)
L += bed; R += bed
# --- cue sheet (reference onset frame -> my cue) ---
CUES = [('whoosh', 4.0), ('pop', 34.5), ('whoosh', 72.5), ('click', 107.5), ('whoosh', 121.5), ('pop', 125.5), ('pop', 128.5),
        ('whoosh', 138.0), ('whoosh', 158.0), ('whoosh', 181.0), ('pop', 185.5), ('whoosh', 211.5), ('rise', 241.0), ('hit-s', 277.0),
        ('hit', 289.0), ('pop', 294.5), ('pop', 310.5), ('hit', 329.0), ('hit-big', 345.5)]
for kind, f in CUES:
  t = T(f)
  if kind == 'whoosh': whoosh(t)
  elif kind == 'pop': pop(t)
  elif kind == 'click': click(t)
  elif kind == 'rise': rise(t, T(277))
  elif kind == 'hit': hit(t, .8)
  elif kind == 'hit-s': hit(t, .45)
  elif kind == 'hit-big': hit(t, 1.1)
# duck the bed under the big hits (already mixed: simple master limiter instead)
mix = np.stack([L, R], 1); mix /= np.abs(mix).max() / 0.89
wf.write('out/audio.wav', SR, (mix * 32767).astype(np.int16))
json.dump(CUES, open('out/cues.json', 'w'))
print('ok', len(CUES), 'cues')
