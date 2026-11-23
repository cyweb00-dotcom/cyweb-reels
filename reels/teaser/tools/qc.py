# Per-frame QC on the desk render.
# 1. lock: for every frame, find each screen edge from the image itself (profile across the edge at
#    24 points per edge, sub-pixel crossing) and compare with the corner lines. Low-contrast samples skipped.
# 2. text clearance: in text beats, distance from any bright text pixel to the screen edge (film px).
# 3. overlap: labels vs each other, vs the monitor (bezel/light bar) and vs the screen.
import cv2, numpy as np, json, glob, sys
C = np.float32(json.load(open('desk/corners.json'))['corners'])
frames = sorted(glob.glob('out/desk/*.png'))
edges = [(C[0], C[1]), (C[1], C[2]), (C[2], C[3]), (C[3], C[0])]
cen = C.mean(0)
def samples():
  S = []
  for a, b in edges:
    d = (b - a) / np.linalg.norm(b - a); n = np.array([-d[1], d[0]])
    if np.dot(cen - (a + b) / 2, n) < 0: n = -n                     # n points into the screen
    for t in np.linspace(0.06, 0.94, 24): S.append((a + (b - a) * t, n))
  return S
S = samples(); offs = np.linspace(-7, 7, 57)
rows = []; allo = []
for k, f in enumerate(frames):
  g = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY).astype(np.float32)
  g = cv2.GaussianBlur(g, (0, 0), 0.7); found = []
  for p, n in S:
    pts = p[None] + offs[:, None] * n[None]
    prof = cv2.remap(g, pts[:, 0:1].astype(np.float32), pts[:, 1:2].astype(np.float32), cv2.INTER_LINEAR).ravel()
    out_, in_ = prof[:12].mean(), prof[-12:].mean()
    if in_ - out_ < 14: continue                                    # dark screen here: no edge to measure
    mid = (out_ + in_) / 2; i = np.argmax(prof > mid)
    if i == 0: continue
    x = offs[i - 1] + (mid - prof[i - 1]) / (prof[i] - prof[i - 1] + 1e-6) * (offs[i] - offs[i - 1])
    found.append(x)
  found = np.array(found)
  rows.append((k, len(found), float(np.median(found)) if len(found) else None, float(np.abs(found - np.median(found)).max()) if len(found) else None))
  if len(found): allo.append(np.median(found))
allo = np.array(allo)
lock = dict(frames=len(frames), frames_with_measurable_edges=int((np.array([r[1] for r in rows]) > 0).sum()),
            edge_offset_median_px=round(float(np.median(allo)), 3), edge_offset_frame_to_frame_jitter_px=round(float(np.abs(np.diff(allo)).max()) if len(allo) > 1 else 0, 3),
            edge_offset_range_px=round(float(allo.max() - allo.min()), 3))
# 2. text clearance (film frames, text beats only; film px; screen edge = film frame edge)
beats = {'title': range(10, 72), 'invite': range(130, 157), 'payoff': range(188, 200), 'closing': range(300, 327), 'logo': range(330, 348), 'end': range(350, 360)}
clear = {}
for name, rg in beats.items():
  m = 1e9
  for k in rg:
    im = cv2.imread(f'film/out/{k:04d}.png').astype(np.int16); mn = im.min(2); mx = im.max(2)
    if name == 'end': t = (mx < 120)
    else: t = (mn > 200) & (mx - mn < 40)
    ys, xs = np.where(t)
    if len(xs) < 30: continue
    m = min(m, xs.min(), ys.min(), 1919 - xs.max(), 1079 - ys.max())
  clear[name] = int(m) if m < 1e9 else None
# 3. overlap
lab = cv2.imread('desk/labels.png', cv2.IMREAD_UNCHANGED)[..., 3]
ys, xs = np.where(lab > 0)
rows_used = np.where((lab > 0).any(1))[0]
runs = np.split(rows_used, np.where(np.diff(rows_used) > 1)[0] + 1)
boxes = [(int(r[0]), int(r[-1])) for r in runs]
screen_top = float(min(C[0, 1], C[1, 1])); lightbar_top = 505
ov = dict(label_boxes_y=boxes, gap_between_labels_px=boxes[1][0] - boxes[0][1] - 1, label_bottom_to_lightbar_px=lightbar_top - boxes[-1][1],
          label_bottom_to_screen_px=round(screen_top - boxes[-1][1], 1), labels_inside_frame=bool(xs.min() > 0 and xs.max() < 1079 and ys.min() > 0))
rep = dict(lock=lock, text_clearance_film_px=clear, overlap=ov)
json.dump(dict(report=rep, per_frame=rows), open('out/qc.json', 'w'), indent=1)
print(json.dumps(rep, indent=1))
