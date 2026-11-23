# Put YOUR desk shot in the reference framing.
#   python3 tools/fit_desk.py assets/desk.jpg            (photo)
#   python3 tools/fit_desk.py assets/desk.mp4            (locked-off clip: corners checked on every frame)
#   optional: --corners x,y,x,y,x,y,x,y  (TL TR BR BL in the source image) if auto-detect picks wrong
# 1. finds the dark screen (largest dark 4-sided region), refines each edge with a line fit
# 2. scale + translate (no rotation/warp of the room) so your screen's centre and width match the
#    reference screen in 1080x1920 (SHOT.md), crops to 1080x1920
# 3. writes desk/plate.png (or desk/plate_frames/ for a clip), desk/corners.json and desk/corners_marked.png
import cv2, numpy as np, json, sys, os
REF = np.float32([[53.7, 556.4], [1055.4, 649.8], [1044.5, 1188.6], [49.5, 1244.0]])
def detect(img):
  g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
  best = None
  for th in (25, 35, 45, 60):
    m = (g < th).astype(np.uint8) * 255
    k = max(9, int(min(g.shape) * 0.02)) | 1
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))   # drop thin dark lines (slat gaps, cables)
    for c in cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
      a = cv2.contourArea(c); x, y, w, h = cv2.boundingRect(c)
      if a < 0.03 * g.size or x <= 2 or y <= 2 or x + w >= g.shape[1] - 2 or y + h >= g.shape[0] - 2: continue
      hull = cv2.convexHull(c); ap = None
      for eps in np.linspace(0.005, 0.08, 16):
        q = cv2.approxPolyDP(hull, eps * cv2.arcLength(hull, True), True)
        if len(q) == 4: ap = q; break
      if ap is not None:
        rect = a / cv2.contourArea(ap); mm = np.zeros_like(g); cv2.drawContours(mm, [ap], -1, 255, -1)
        dark = 1.0 - cv2.mean(g, mm)[0] / 255.0
        sc = a * rect * dark ** 2
        if best is None or sc > best[0]: best = (sc, ap.reshape(4, 2).astype(np.float32))
  if best is None: raise SystemExit('screen not found: pass --corners')
  p = best[1]; s = p.sum(1); d = np.diff(p, axis=1).ravel()
  return np.float32([p[np.argmin(s)], p[np.argmin(d)], p[np.argmax(s)], p[np.argmax(d)]])
def fit_transform(c):
  # uniform scale from the screen's mean width, translate centres
  w_src = (np.linalg.norm(c[1] - c[0]) + np.linalg.norm(c[2] - c[3])) / 2
  w_ref = (np.linalg.norm(REF[1] - REF[0]) + np.linalg.norm(REF[2] - REF[3])) / 2
  s = w_ref / w_src; t = REF.mean(0) - c.mean(0) * s
  return np.float32([[s, 0, t[0]], [0, s, t[1]]])
def place(img, A): return cv2.warpAffine(img, A, (1080, 1920), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
def mark(img, c):
  m = img.copy()
  cv2.polylines(m, [c.astype(np.int32)], True, (0, 255, 255), 3)
  for n, p in zip(('TL', 'TR', 'BR', 'BL'), c):
    cv2.circle(m, tuple(int(v) for v in p), 12, (0, 0, 255), 3)
    cv2.putText(m, f'{n} {p[0]:.0f},{p[1]:.0f}', (int(p[0]) + 14, int(p[1]) - 14), 0, 1.0, (0, 255, 255), 2)
  return m
if __name__ == '__main__':
  src = sys.argv[1]; man = None
  if '--corners' in sys.argv: man = np.float32([float(v) for v in sys.argv[sys.argv.index('--corners') + 1].split(',')]).reshape(4, 2)
  os.makedirs('desk', exist_ok=True)
  if src.lower().endswith(('.mp4', '.mov', '.m4v')):
    cap = cv2.VideoCapture(src); frames = []
    while True:
      ok, f = cap.read()
      if not ok: break
      frames.append(f)
    c0 = man if man is not None else detect(frames[0]); A = fit_transform(c0)
    drift = [float(np.abs(detect(f) - c0).max()) if man is None else 0.0 for f in frames]
    os.makedirs('desk/plate_frames', exist_ok=True)
    for i, f in enumerate(frames): cv2.imwrite(f'desk/plate_frames/{i:04d}.png', place(f, A))
    plate = place(frames[0], A); print('corner drift over clip: max %.2f px' % max(drift))
  else:
    img = cv2.imread(src); c0 = man if man is not None else detect(img); A = fit_transform(c0); plate = place(img, A); drift = [0.0]
  C = (np.hstack([c0, np.ones((4, 1), np.float32)]) @ A.T).astype(np.float32)
  cv2.imwrite('desk/plate.png', plate); cv2.imwrite('desk/corners_marked.png', mark(plate, C))
  json.dump({'plate': 'desk/plate.png', 'corners': C.round(1).tolist(), 'source': src, 'source_corners': c0.round(1).tolist(),
             'max_corner_drift_px': max(drift), 'ref_corners': REF.tolist()}, open('desk/corners.json', 'w'), indent=1)
  print('corners (out px):', C.round(1).tolist())
