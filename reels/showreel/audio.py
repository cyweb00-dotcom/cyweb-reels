# Soundtrack built in code: calm 120 BPM bed + one sound per on-screen animation, on its exact time.
import numpy as np, scipy.io.wavfile as wf, scipy.signal as ss, json
SR = 48000; DUR = 22.0; N = int(SR * DUR); rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
sos = lambda k, f: ss.butter(2, f, k, fs=SR, output='sos')
lp = lambda x, f: ss.sosfilt(sos('low', f), x); hp = lambda x, f: ss.sosfilt(sos('high', f), x); bp = lambda x, a, b: ss.sosfilt(sos('band', [a, b]), x)
def verb(x, secs=1.4, mix=.25):
    n = int(secs * SR); ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (secs * SR / 6)); ir = lp(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
    w = ss.fftconvolve(x, ir); o = np.zeros(len(w)); o[:len(x)] += x; return o + mix * w
def put(x, t, g=1, pan=0):
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(N, i + len(x)); L[i:j] += x[:j - i] * g * np.sqrt(.5 * (1 - pan)); R[i:j] += x[:j - i] * g * np.sqrt(.5 * (1 + pan))
k = lambda n: np.arange(n) / SR
def pop(t, f0=700, g=.4):
    n = int(.2 * SR); kk = k(n); f = f0 * (1 + 1.2 * (1 - np.exp(-kk * 40)))
    put(verb(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, kk / .003) * np.exp(-kk / .05), .8, .3), t, g)
def whoosh(peak, ln=.55, g=.5):
    n = int(ln * SR); u = np.arange(n) / n; x = rng.normal(0, 1, n); o = np.zeros(n)
    for s in range(0, n, 512):
        fc = 300 * (25 ** np.sin(np.pi * min(1, s / n))); o[s:s + 512] = bp(x[s:s + 512], fc * .5, min(20000, fc * 1.5))
    e = np.where(u < .6, (u / .6) ** 2.2, np.exp(-(u - .6) * ln / .12)); put(verb(o / np.abs(o).max() * e, 1, .2), peak - .6 * ln, g)
def slam(t, g=.8):
    n = int(1.2 * SR); kk = k(n)
    x = np.sin(2 * np.pi * np.cumsum(55 * np.exp(-kk * 6) + 40) / SR) * np.exp(-kk / .25) + .4 * hp(rng.normal(0, 1, n), 1500) * np.exp(-kk / .02)
    put(verb(x, 1.6, .3), t, g)
def tick(t, f=2400, g=.25):
    n = int(.04 * SR); kk = k(n); put(np.sin(2 * np.pi * f * kk) * np.exp(-kk / .006) + .3 * hp(rng.normal(0, 1, n), 4000) * np.exp(-kk / .002), t, g, .2)
def shimmer(t, g=.3):
    n = int(2.5 * SR); kk = k(n); x = sum(np.sin(2 * np.pi * f * kk + i) for i, f in enumerate((1318, 1760, 2093, 2637))) * np.exp(-kk / .8) * np.minimum(1, kk / .05)
    put(verb(x * .25, 2.2, .45), t, g)
def riser(t0, t1, g=.18):
    n = int((t1 - t0) * SR); u = np.arange(n) / n; ph = 2 * np.pi * np.cumsum(200 * 4 ** u) / SR
    put(verb(lp(np.sin(ph) * u ** 2, 4000) + bp(rng.normal(0, 1, n), 2000, 9000) * u ** 3 * .3, 1, .2), t0, g)
# ---- bed: 120 bpm, Am9 - Fmaj7 - C - G, soft pad + soft kick + hat ----
beat = .5; kk = k(N); bed = np.zeros(N)
chords = [[57, 60, 64, 71], [53, 57, 64, 67], [48, 55, 60, 64], [55, 59, 62, 67]]
for ci in range(int(DUR / 2) + 1):
    i0 = int(ci * 2 * SR); i1 = min(N, i0 + int(2.4 * SR))
    if i0 >= N: break
    t2 = np.arange(i1 - i0) / SR; seg = np.zeros(i1 - i0)
    for m in chords[ci % 4]:
        fr = 440 * 2 ** ((m - 69) / 12); seg += np.sin(2 * np.pi * fr * t2) + .3 * np.sin(4 * np.pi * fr * t2)
    seg *= np.minimum(1, t2 / .3) * np.minimum(1, (t2[-1] - t2) / .4); bed[i0:i1] += seg
bed = verb(lp(bed, 1800) * .045, 2.5, .4)[:N]
for b in np.arange(2.0, 21.0, beat):   # kick enters after the hook, stops for the end
    n = int(.3 * SR); kb = k(n); x = np.sin(2 * np.pi * np.cumsum(48 + 100 * np.exp(-kb * 35)) / SR) * np.exp(-kb / .1)
    i = int(b * SR); j = min(N, i + n); bed[i:j] += x[:j - i] * (.28 if int(b / beat) % 2 == 0 else .16)
bed *= np.clip(kk / .3, 0, 1) * np.clip((21.95 - kk) / .6, 0, 1)
# ---- cues (time in s = the frame where the animation happens) ----
CUES = []
def cue(name, t, fn, *a): CUES.append([name, t]); fn(t, *a)
cue('dot', 0.0, pop, 600, .3)
cue('dots split', 0.5, pop, 900, .35)
cue('NO slam', 1.0, slam, .8); cue('WEBSITE?', 1.12, tick, 1800, .25)
cue('blue panel', 2.0, whoosh); cue('CUSTOMERS', 2.12, tick, 2000, .3); cue("CAN'T", 2.5, slam, .55); cue('FIND YOU', 3.0, slam, .6)
cue('to DESIGN', 4.0, whoosh)
for tt in (4.5, 5.0, 5.5): cue('morph', tt, pop, 800 + 150 * (tt - 4.5), .3)
cue('website', 6.0, pop, 1100, .4)
cue('to BUILD', 6.5, whoosh); cue('dots gather', 7.6, riser, 8.3)
cue('to LAUNCH', 9.0, whoosh); cue('cube snap', 10.2, slam, .45)
cue('to GET FOUND', 11.0, whoosh); cue('ribbon', 11.1, riser, 12.4); cue('pin drop', 12.75, slam, .55)
cue('to rings', 13.5, whoosh)
for tt in (13.5, 14.0, 14.5): cue('ring', tt, pop, 700 + 200 * (tt - 13.5), .3)
cue('logo', 17.0, slam, .9); cue('logo shimmer', 17.0, shimmer)
for i in range(5): cue('letter', 17.5 + i * .1, tick, 2200 + i * 120, .18)
cue('tagline', 18.5, pop, 900, .3); cue('url', 19.5, pop, 1200, .35)
cue('collapse', 21.0, whoosh, .55, .35); cue('dot', 21.6, pop, 600, .3)
L += bed; R += bed
mix = np.stack([L, R], 1); mix /= np.abs(mix).max() / .89
wf.write('out/audio.wav', SR, (mix * 32767).astype(np.int16)); json.dump(CUES, open('out/cues.json', 'w'), indent=0)
print('ok', len(CUES), 'cues')
