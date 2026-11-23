# Match the rebuilt set's colour to the reference room (LAB mean/std transfer, in horizontal bands,
# measured outside the screen and the labels), so the plate sits in the same light as the reference.
import cv2, numpy as np, json
C = np.float32(json.load(open('desk/corners.json'))['corners'])
plate = cv2.imread('desk/set_beauty.png')
ref = cv2.resize(cv2.imread('ref/frames/0001.png'), (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
mask = np.ones(plate.shape[:2], np.uint8)
cv2.fillPoly(mask, [C.astype(np.int32)], 0)
mask[240:470, 150:930] = 0                                      # labels (reference has its own there)
mask = cv2.erode(mask, np.ones((15, 15), np.uint8))
P = cv2.cvtColor(plate, cv2.COLOR_BGR2LAB).astype(np.float32); R = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).astype(np.float32)
bands = [0, 520, 1300, 1500, 1920]                               # wall top / wall by monitor / under monitor / desk
out = np.zeros_like(P); wsum = np.zeros(P.shape[:2] + (1,), np.float32)
for i in range(len(bands) - 1):
  y0, y1 = bands[i], bands[i + 1]; m = mask[y0:y1] > 0
  ps, rs = P[y0:y1][m], R[y0:y1][m]
  mu_p, sd_p, mu_r, sd_r = ps.mean(0), ps.std(0) + 1e-3, rs.mean(0), rs.std(0) + 1e-3
  g = (P - mu_p) / sd_p * sd_r + mu_r
  # smooth band weights so there are no seams
  yy = np.arange(1920)[:, None, None].astype(np.float32); c = (y0 + y1) / 2; h = (y1 - y0) / 2 + 120
  w = np.clip(1 - np.abs(yy - c) / h, 0.001, 1) ** 2
  out += g * w; wsum += w
  print(f'band {y0}-{y1}: L {mu_p[0]:.0f}->{mu_r[0]:.0f}  a {mu_p[1]:.0f}->{mu_r[1]:.0f}  b {mu_p[2]:.0f}->{mu_r[2]:.0f}')
out = np.clip(out / wsum, 0, 255).astype(np.uint8)
g = cv2.cvtColor(out, cv2.COLOR_LAB2BGR)
# keep the ball lamp's own colour (it is a light, not a surface)
yy, xx = np.mgrid[0:1920, 0:1080]; ball = (((xx - 990) ** 2 + (yy - 1376) ** 2) < 112 ** 2)[..., None]
g = np.where(ball, (plate * 0.55 + g * 0.45).astype(np.uint8), g)
cv2.imwrite('desk/set_graded.png', g)
# keep true blacks (monitor body, felt) neutral like the reference bezel
dark = (cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY) < 14)[..., None]
g = cv2.imread('desk/set_graded.png'); g = np.where(dark, plate, g); cv2.imwrite('desk/set_graded.png', g)
